// registry-template/tools/registry-lib.js
// Shared parsing/scan helpers for the AI Registry bundle. See registry/SCHEMA.md.
// Zero npm dependencies -- Node >=18 built-ins only. Self-contained: unlike the
// private business-repo reference this is generalized from, this file has no
// cross-repo require (no okf-lib, no orphan-capabilities.js, no derive-pipeline.js).
'use strict';
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

// The registry tools' version. indexing-registry compares the workspace's
// tools/package.json "version" with the plugin's and offers the update when
// the workspace's is missing or lower; package.json carries the same number.
// Raise both together whenever compose, lint, this file, the dashboard
// template or the data-island schema change.
const TOOLS_VERSION = '10.0.0';

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

// Legacy definition_type spellings tolerated as a warning, never as an error,
// and never written into a new node (SCHEMA.md "Enums").
const LEGACY_TOLERATED = ['step-decomposed', 'outcome-driven', 'Outcome-Driven'];

// Event-fact / derived fields banned from every node (SCHEMA.md "Deliberately
// not concept types"). `owner` is ALSO banned, but only on Workflow nodes
// (ownership lives on Process) -- checked separately by the linter.
const BANNED_FIELDS = [
  'current_step', 'health', 'last_run', 'run_count', 'next_review',
  'notion_url', 'timestamp', 'lob', 'sequence', 'process',
];

// Artifact labels (SCHEMA.md "Artifact labels"). LEGACY_LABELS come from
// earlier versions of the framework: tolerated on older nodes (a bare-date
// generated.at), never written -- a node stamped with a UTC instant that
// carries one is a lint error.
const ARTIFACT_LABELS = ['Raw source', 'Run log', 'Output', 'SOP', 'Opportunity report', 'Requirements', 'Design plan', 'Test results'];
const LEGACY_LABELS = ['Design spec', 'Run guide', 'Improvement plan'];

// generated.at: a UTC instant, or (on an older node only) a bare date.
const AT_INSTANT = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
const AT_DATE = /^\d{4}-\d{2}-\d{2}$/;

// Reserved body-section names this bundle recognizes. Only H1 headings with
// exactly these names delimit sections; any other `# ` line -- including
// headings inside fenced code blocks -- is prose content.
const SECTION_NAMES = new Set([
  'Lines of Business', 'Processes', 'Workflows', 'Artifacts', 'Skills', 'Agents', 'Insights', 'Owns',
]);

// Windows checkouts (core.autocrlf=true) or a Windows-authored file hand off
// CRLF line endings. Every parser in this module (frontmatter delimiter,
// sections, GENERATED blocks) is written against LF-only text, so normalize
// once at the read boundary (see loadBundle/scanSops/scanSkillsAndAgents)
// rather than teaching every regex to tolerate an optional \r. A no-op on
// already-LF text, so composed output stays byte-identical on LF systems.
function normalizeLineEndings(text) {
  return String(text || '').replace(/\r\n/g, '\n');
}

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

// Skill and agent files are not registry nodes: their authors (and the platforms
// that create them) routinely write `description: >`, `|`, or a plain value
// continued on indented lines. Read their top-level scalars leniently so the
// dashboard shows the text; registry nodes stay on the strict parser above.
function parseCapabilityFrontmatter(text) {
  const raw = String(text || '').replace(/^\uFEFF/, '');
  if (!raw.startsWith('---\n')) return {};
  const end = raw.indexOf('\n---\n', 4);
  if (end === -1) return {};
  const lines = raw.slice(4, end).split('\n');
  const fields = {};
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (!m) continue;
    const cont = [];
    while (i + 1 < lines.length && (/^\s/.test(lines[i + 1]) || !lines[i + 1].trim())) cont.push(lines[++i].trim());
    while (cont.length && !cont[cont.length - 1]) cont.pop();
    let v = m[2].trim();
    const block = v.match(/^([>|])(?:[+-]?\d?|\d[+-])$/);
    if (block) {
      v = block[1] === '|' ? cont.join('\n') : cont.filter(Boolean).join(' ');
    } else {
      v = [v, ...cont.filter(Boolean)].join(' ');
      if (v.length > 1 && v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1).replace(/\\(["\\])/g, '$1');
      else if (v.length > 1 && v.startsWith("'") && v.endsWith("'")) v = v.slice(1, -1).replace(/''/g, "'");
    }
    fields[m[1]] = v;
  }
  return fields;
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
  // Function-form replacer -- derived content (e.g. a Process titled with a
  // literal "$&") can legitimately contain `$&`/`` $` ``/`$'`/`$<name>`, which
  // the string form of .replace() would misread as replacement-pattern
  // tokens and corrupt (same hazard compose-registry.js's dashboard inject
  // guards against).
  const block = renderGeneratedBlock(name, content);
  return { raw: raw.replace(re, () => block), replaced: true };
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
      const raw = normalizeLineEndings(fs.readFileSync(full, 'utf8'));
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

// --- Workspace scans (skills/agents/SOPs/framework records are never duplicated into
// the bundle; the linter and compose read them from the workspace directly).

function scanSops(workspaceRoot) {
  const out = [];
  const dir = path.join(workspaceRoot, 'sops');
  let names;
  try { names = fs.readdirSync(dir).sort(); } catch { return out; } // missing, or not a directory
  for (const name of names) {
    if (!name.endsWith('.md')) continue;
    const full = path.join(dir, name);
    let raw;
    try {
      if (!fs.statSync(full).isFile()) continue;
      raw = fs.readFileSync(full, 'utf8');
    } catch { continue; } // broken symlink, unreadable
    out.push({ path: `sops/${name}`, raw: normalizeLineEndings(raw) });
  }
  return out;
}

// --- The framework folder ----------------------------------------------------
// The registry's parent folder is the workspace on Claude Code and Codex, which
// holds framework/ beside registry/; on the web and Claude desktop it is the
// framework folder itself, which holds registry/ beside the workflow folders.
// (SCHEMA.md "Layered model".)

// A workflow folder holds at least one of these record files.
const RECORD_MARKERS = ['requirements.md', 'deconstruct-in-progress.md', 'design-plan.md', 'build-record.md', 'test-results.md'];
// Folders in the framework folder that are never workflow folders.
const NOT_WORKFLOW_DIRS = new Set(['history', 'registry']);

function isDirSafe(p) { try { return fs.statSync(p).isDirectory(); } catch { return false; } }

// { dir: absolute framework folder, prefix: link prefix for its workflow
// folders ('framework/' in a workspace, '' beside registry/) }. A workspace
// with no framework/ yet is treated as one (prefix 'framework/') when it has
// no workflow-shaped sibling of registry/ either.
function frameworkFolder(workspaceRoot) {
  const local = path.join(workspaceRoot, 'framework');
  if (isDirSafe(local)) return { dir: local, prefix: 'framework/' };
  if (fs.existsSync(local)) return { dir: null, prefix: 'framework/' }; // a plain file named framework
  if (scanWorkflowFolders(workspaceRoot, '').length) return { dir: workspaceRoot, prefix: '' };
  return { dir: local, prefix: 'framework/' };
}

// Workflow folders directly under `dir` (relative path prefix `prefix`).
// Skips anything that is not a readable folder: a broken symlink, an entry it
// cannot stat. With an empty prefix (a drive-shaped framework folder) only
// folders holding a record file count, so sops/, process-guides/ and the like
// are never mistaken for workflows.
function scanWorkflowFolders(dir, prefix) {
  const out = [];
  let names;
  try { names = fs.readdirSync(dir).sort(); } catch { return out; } // missing, or not a directory
  for (const name of names) {
    if (NOT_WORKFLOW_DIRS.has(name) || name.startsWith('.')) continue;
    const full = path.join(dir, name);
    if (!isDirSafe(full)) continue;
    if (prefix === '' && !RECORD_MARKERS.some((m) => fs.existsSync(path.join(full, m)))) continue;
    out.push({ slug: name, path: `${prefix}${name}`, abs: full });
  }
  return out;
}

// The workflow folders in the registry's parent folder, wherever its framework
// folder is. Each holds the workflow's record: requirements, design plan,
// build record, test results (+ inputs/, context/, package/, history/). Never
// its run log, which lives where the workflow runs.
function scanFrameworkFolders(workspaceRoot) {
  const fw = frameworkFolder(workspaceRoot);
  return fw.dir ? scanWorkflowFolders(fw.dir, fw.prefix) : [];
}

// A run log (runs.md or runs-<slug>.md) has at least one data row: a table
// row beyond the header and separator. `file` is an absolute path.
function runLogHasEntries(file) {
  let text;
  try {
    if (!fs.statSync(file).isFile()) return false;
    text = fs.readFileSync(file, 'utf8');
  } catch { return false; }
  let tableRows = 0;
  for (const l of normalizeLineEndings(text).split('\n')) {
    if (/^\s*\|/.test(l) && !/^\s*\|[\s\-|:]+\|\s*$/.test(l)) tableRows++;
  }
  return tableRows > 1; // header + >=1 data row
}

// A Workflow node's `# Artifacts` link labels, as written.
function artifactLabels(node) {
  return orderedLinks((node.sections && node.sections['Artifacts']) || '').map((l) => l.title.trim());
}

// Capability inventory for the orphan-capabilities warning: any `skills/*/SKILL.md`
// at any depth (matches `**/skills/*/SKILL.md`), plus `.claude/agents/*.md`,
// top-level `agents/*.md` and agents staged in a workflow's package/. Skips every
// `history/` folder. Excludes `tools/fixtures/**` -- the template repo
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
      // history/ holds kept copies, set-asides and earlier versions: never live capabilities.
      if (e.name === 'history') continue;
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
  // Agents Build staged in a workflow's package/ (framework/<slug>/package/agents/*.md)
  // count too: Build stages skills and agents there on platforms it can't install to.
  // Skills staged there are found by the walk above (package/skills/<name>/SKILL.md).
  const agentDirs = [path.join(workspaceRoot, '.claude', 'agents'), path.join(workspaceRoot, 'agents')];
  for (const f of scanFrameworkFolders(workspaceRoot)) agentDirs.push(path.join(f.abs, 'package', 'agents'));
  for (const dir of agentDirs) {
    let names;
    try { names = fs.readdirSync(dir).sort(); } catch { continue; } // missing, or not a directory
    for (const name of names) {
      if (name.endsWith('.md')) add(path.join(dir, name));
    }
  }
  return out.sort();
}

// Links into gitignored territory (a workflow's own output) are
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
  TOOLS_VERSION,
  DIR_TYPES, RESERVED, ENUMS, LEGACY_TOLERATED, BANNED_FIELDS, SECTION_NAMES,
  ARTIFACT_LABELS, LEGACY_LABELS, AT_INSTANT, AT_DATE, RECORD_MARKERS,
  normalizeLineEndings, parseFrontmatter, parseCapabilityFrontmatter, parseSections, orderedLinks, classifyLinks, slugOf,
  findGeneratedBlocks, renderGeneratedBlock, replaceGeneratedBlock,
  loadBundle, scanSops, frameworkFolder, scanFrameworkFolders, runLogHasEntries, artifactLabels, scanCapabilities,
  isGitIgnored, lastChanged,
};
