// registry-template/tools/registry-lib.js
// Shared parsing/scan helpers for the AI Registry bundle. See registry/SCHEMA.md.
// Zero npm dependencies -- Node >=18 built-ins only. Self-contained: unlike the
// private business-repo reference this is generalized from, this file has no
// cross-repo require (no okf-lib, no orphan-capabilities.js, no derive-pipeline.js).
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

// Plural directories -> singular concept type. Directory<->type agreement is
// lint-enforced (SCHEMA.md "Types and directories").
const DIR_TYPES = {
  businesses: 'Business',
  'lines-of-business': 'LineOfBusiness',
  processes: 'Process',
  workflows: 'Workflow',
  notes: 'Note',
  functions: 'Function',
};

// Reserved files: no required concept frontmatter, never directory-checked.
const RESERVED = new Set(['SCHEMA.md', 'index.md', 'log.md']);

// Per-type enum constraints. `*` applies to any type carrying the field.
const ENUMS = {
  Workflow: { status: ['backlog', 'under-development', 'in-production', 'retired'] },
  Business: { status: ['active', 'incubating', 'dormant'] },
  LineOfBusiness: { status: ['active', 'incubating', 'dormant'] },
  '*': {
    definition_type: ['step-driven', 'goal-driven'],
    execution_mode: ['manual', 'augmented', 'automated'],
    autonomy: ['deterministic', 'guided', 'autonomous'],
  },
};

// Legacy definition_type spellings tolerated as a migration warning, never as
// an error, and never written into a new node (SCHEMA.md "Enums").
const LEGACY_TOLERATED = ['step-decomposed', 'outcome-driven', 'Outcome-Driven'];

// Event-fact / derived fields banned from every node (SCHEMA.md "Deliberately
// not concept types"). `owner` is ALSO banned, but only on Workflow nodes
// (ownership lives on Process) -- checked separately by the linter.
const BANNED_FIELDS = [
  'current_step', 'health', 'last_run', 'run_count', 'next_review',
  'notion_url', 'timestamp', 'lob', 'sequence', 'process',
];

// Reserved body-section names this bundle recognizes. Only H1 headings with
// exactly these names delimit sections; any other `# ` line -- including
// headings inside fenced code blocks -- is prose content.
const SECTION_NAMES = new Set([
  'Lines of Business', 'Processes', 'Workflows', 'Artifacts', 'Skills', 'Agents', 'Insights', 'Owns',
]);

// --- Frontmatter -----------------------------------------------------------
// Deliberately restricted to single-line YAML values (SCHEMA.md "Frontmatter").

function parseFrontmatter(text) {
  const raw = String(text || '');
  if (!raw.startsWith('---\n')) {
    // No frontmatter at all. Not itself an error here -- reserved files
    // (index.md, log.md) legitimately carry none. Whether a concept file
    // requires one is a lint-time (directory-aware) decision, not a parse
    // one; see lint-registry.js rule 1.
    return { fields: null, body: raw };
  }
  const end = raw.indexOf('\n---\n', 4);
  if (end === -1) {
    return { fields: null, body: raw, error: 'unterminated frontmatter block (no closing "---")' };
  }
  const fields = {};
  const head = raw.slice(4, end);
  for (const line of head.split('\n')) {
    if (!line.trim()) continue;
    if (/^\s/.test(line)) {
      return { fields: null, body: raw, error: `multi-line YAML is not supported in this bundle -- indented continuation line: "${line.trim()}"` };
    }
    if (/^[\w-]+:\s*[>|][+-]?\s*$/.test(line)) {
      return { fields: null, body: raw, error: `multi-line YAML block scalar is not supported in this bundle: "${line.trim()}"` };
    }
    const m = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (!m) return { fields: null, body: raw, error: `bad frontmatter line: "${line}"` };
    let v = m[2].trim();
    if (v.startsWith('[') && v.endsWith(']')) {
      v = v.slice(1, -1).split(',').map((s) => s.trim()).filter(Boolean);
    } else if (v.startsWith('"') && v.endsWith('"')) {
      v = v.slice(1, -1).replace(/\\(["\\])/g, '$1');
    } else if (v.startsWith("'") && v.endsWith("'")) {
      v = v.slice(1, -1);
    } else if (v.startsWith('{') && v.endsWith('}')) {
      // Single-line YAML flow map -- the only nested value the single-line
      // profile admits (OKF v0.2 `generated: { by, at }`). Split on commas;
      // keys split at the FIRST colon so actor ids (human:jamesgray) survive.
      const map = {};
      for (const part of v.slice(1, -1).split(',')) {
        if (!part.trim()) continue;
        const c = part.indexOf(':');
        if (c === -1) return { fields: null, body: raw, error: `bad flow map entry: "${part.trim()}"` };
        map[part.slice(0, c).trim()] = part.slice(c + 1).trim();
      }
      v = map;
    }
    fields[m[1]] = v;
  }
  return { fields, body: raw.slice(end + 5) };
}

function parseSections(text, sectionNames = SECTION_NAMES) {
  const sections = { _preamble: '' };
  let current = '_preamble';
  let inFence = false;
  for (const line of String(text || '').split('\n')) {
    if (/^(```|~~~)/.test(line)) inFence = !inFence;
    const m = !inFence && line.match(/^# (.+)$/);
    if (m && sectionNames.has(m[1].trim())) { current = m[1].trim(); sections[current] = ''; continue; }
    sections[current] += line + '\n';
  }
  for (const k of Object.keys(sections)) {
    sections[k] = sections[k].replace(/^\n+/, '').replace(/\n+$/, '\n');
    if (sections[k] === '\n') sections[k] = '';
  }
  return sections;
}

// Curated ordered list items: `- [Title](href)` / `1. [Title](href)`.
function orderedLinks(sectionText) {
  const out = [];
  const re = /^\s*(?:[-*]|\d+\.)\s+\[([^\]]+)\]\(([^)]+)\)/gm;
  let m;
  while ((m = re.exec(sectionText || ''))) out.push({ title: m[1], href: m[2] });
  return out;
}

// All markdown link hrefs in text, classified per SCHEMA.md's discriminator.
function classifyLinks(raw) {
  const out = { inBundle: [], repo: [], external: [] };
  const re = /\]\(([^)\s]+)\)/g;
  let m;
  while ((m = re.exec(raw || ''))) {
    const href = m[1];
    if (/^[a-z][a-z0-9+.-]*:/i.test(href)) out.external.push(href);
    else if (href.startsWith('#')) continue;
    else if (href.startsWith('/')) out.inBundle.push(href);
    else out.repo.push(href.replace(/#.*$/, ''));
  }
  return out;
}

function slugOf(relPath) {
  return path.posix.basename(relPath, '.md');
}

// --- GENERATED blocks: <!-- GENERATED:name --> ... <!-- /GENERATED -->
// Hash-less markers (SCHEMA.md "Derived views & maintenance") -- this bundle
// has no compose-time hash to compare against, so "hand-edited" is detected
// by content mismatch against the derivable value (see lint-registry.js's
// Function `# Owns` check), not by a stored digest.
const GEN_OPEN_SRC = '<!-- GENERATED:(\\w[\\w-]*) -->';
const GEN_CLOSE = '<!-- /GENERATED -->';

function findGeneratedBlocks(raw) {
  const re = new RegExp(GEN_OPEN_SRC, 'g');
  const blocks = [];
  let m;
  while ((m = re.exec(raw || ''))) {
    const end = raw.indexOf(GEN_CLOSE, m.index);
    if (end === -1) { blocks.push({ name: m[1], start: m.index, unterminated: true }); continue; }
    const content = raw.slice(m.index + m[0].length, end).replace(/^\n/, '').replace(/\n$/, '');
    blocks.push({ name: m[1], start: m.index, content });
  }
  return blocks;
}

function renderGeneratedBlock(name, content) {
  const c = String(content || '').replace(/\n+$/, '');
  return c ? `<!-- GENERATED:${name} -->\n${c}\n${GEN_CLOSE}` : `<!-- GENERATED:${name} -->\n${GEN_CLOSE}`;
}

function replaceGeneratedBlock(raw, name, content) {
  const re = new RegExp(`<!-- GENERATED:${name} -->[\\s\\S]*?${GEN_CLOSE}`);
  if (!re.test(raw)) return { raw, replaced: false };
  return { raw: raw.replace(re, renderGeneratedBlock(name, content)), replaced: true };
}

// --- Bundle loader -----------------------------------------------------------
// loadBundle(rootDir) -> { nodes: Map<path, {type, fm, body, sections}>, errors }
// `path` keys are bundle-root-relative with a leading "/" -- the same shape
// as the in-bundle link discriminator (SCHEMA.md "Links"), so an in-bundle
// href can be resolved with a plain `nodes.has(href)`.
function loadBundle(rootDir) {
  const absRoot = path.resolve(rootDir);
  const nodes = new Map();
  const errors = [];
  (function walk(dir) {
    let entries;
    try { entries = fs.readdirSync(dir).sort(); } catch { return; }
    for (const name of entries) {
      const full = path.join(dir, name);
      let st;
      try { st = fs.statSync(full); } catch { continue; }
      if (st.isDirectory()) { walk(full); continue; }
      if (!name.endsWith('.md')) continue;
      const relPath = '/' + path.relative(absRoot, full).split(path.sep).join('/');
      const raw = fs.readFileSync(full, 'utf8');
      const { fields, body, error } = parseFrontmatter(raw);
      nodes.set(relPath, {
        type: fields ? fields.type : undefined,
        fm: fields,
        body,
        sections: parseSections(body),
        raw,
        relPath,
        error,
      });
    }
  })(absRoot);
  return { nodes, errors };
}

// --- Workspace scans (skills/agents/SOPs/outputs are never duplicated into
// the bundle; the linter and compose read them from the workspace directly).

function scanSops(workspaceRoot) {
  const out = [];
  const dir = path.join(workspaceRoot, 'sops');
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir).sort()) {
    if (!name.endsWith('.md')) continue;
    const full = path.join(dir, name);
    if (!fs.statSync(full).isFile()) continue;
    out.push({ path: `sops/${name}`, raw: fs.readFileSync(full, 'utf8') });
  }
  return out;
}

function scanOutputsFolders(workspaceRoot) {
  const out = [];
  const dir = path.join(workspaceRoot, 'outputs');
  if (!fs.existsSync(dir)) return out;
  for (const name of fs.readdirSync(dir).sort()) {
    const full = path.join(dir, name);
    if (!fs.statSync(full).isDirectory()) continue;
    out.push({ slug: name, path: `outputs/${name}`, hasRuns: fs.existsSync(path.join(full, 'runs.md')) });
  }
  return out;
}

// runs.md has at least one data row (a table row beyond header/separator).
function runsHasEntries(workspaceRoot, slug) {
  const file = path.join(workspaceRoot, 'outputs', slug, 'runs.md');
  if (!fs.existsSync(file)) return false;
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  let tableRows = 0;
  for (const l of lines) {
    if (/^\s*\|/.test(l) && !/^\s*\|[\s\-|:]+\|\s*$/.test(l)) tableRows++;
  }
  return tableRows > 1; // header + >=1 data row
}

// Capability inventory for the orphan-capabilities warning: any `skills/*/SKILL.md`
// at any depth (matches `**/skills/*/SKILL.md`), plus `.claude/agents/*.md` and
// top-level `agents/*.md`. Excludes `tools/fixtures/**` -- the template repo
// ships test fixtures containing their own `.claude/skills/` trees, and
// composing at the template-repo root must not leak those fictional
// capabilities into a student's registry.
function scanCapabilities(workspaceRoot) {
  const out = [];
  const seen = new Set();
  const add = (full) => {
    const rel = path.relative(workspaceRoot, full).split(path.sep).join('/');
    if (seen.has(rel)) return;
    seen.add(rel);
    out.push(rel);
  };
  (function walk(dir, depth) {
    if (depth > 8) return;
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0)); } catch { return; }
    for (const e of entries) {
      if (e.name === '.git' || e.name === 'node_modules') continue;
      const full = path.join(dir, e.name);
      if (!e.isDirectory()) continue;
      const rel = path.relative(workspaceRoot, full).split(path.sep).join('/');
      if (rel === 'tools/fixtures' || rel.startsWith('tools/fixtures/')) continue;
      if (e.name === 'skills') {
        let subs;
        try { subs = fs.readdirSync(full).sort(); } catch { subs = []; }
        for (const sub of subs) {
          const skillFile = path.join(full, sub, 'SKILL.md');
          if (fs.existsSync(skillFile)) add(skillFile);
        }
      }
      walk(full, depth + 1);
    }
  })(workspaceRoot, 0);
  for (const dir of [path.join(workspaceRoot, '.claude', 'agents'), path.join(workspaceRoot, 'agents')]) {
    if (!fs.existsSync(dir)) continue;
    for (const name of fs.readdirSync(dir).sort()) {
      if (name.endsWith('.md')) add(path.join(dir, name));
    }
  }
  return out.sort();
}

// Links into gitignored territory (raw-source layer: outputs/) are
// declarations lint cannot verify in a fresh checkout -- `git check-ignore`
// works on patterns regardless of whether the file exists. Non-git
// directories (or any error) tolerate as "nothing ignored".
function isGitIgnored(relPath, cwd) {
  try {
    execFileSync('git', ['check-ignore', '-q', relPath], { cwd });
    return true;
  } catch {
    return false;
  }
}

// OKF v0.2 last-content-change accessor.
function lastChanged(fm) {
  if (!fm) return '';
  if (fm.generated && typeof fm.generated === 'object' && fm.generated.at) return fm.generated.at;
  return '';
}

module.exports = {
  DIR_TYPES, RESERVED, ENUMS, LEGACY_TOLERATED, BANNED_FIELDS, SECTION_NAMES,
  parseFrontmatter, parseSections, orderedLinks, classifyLinks, slugOf,
  findGeneratedBlocks, renderGeneratedBlock, replaceGeneratedBlock,
  loadBundle, scanSops, scanOutputsFolders, runsHasEntries, scanCapabilities,
  isGitIgnored, lastChanged,
};
