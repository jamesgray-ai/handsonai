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
const TOOLS_VERSION = '11.1.1';

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
  // Domain state (`state`, read through stateOf, so a 0.2 node's `status` counts).
  Workflow: { state: ['backlog', 'under-development', 'in-production', 'retired'] },
  Business: { state: ['active', 'incubating', 'dormant'] },
  LineOfBusiness: { state: ['active', 'incubating', 'dormant'] },
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
  // OKF v0.3 §4: a producer never writes a key twice. Keep the last value, as before, and
  // report the key so lint can warn.
  const duplicates = [];
  const setField = (k, v) => { if (Object.prototype.hasOwnProperty.call(fields, k) && !duplicates.includes(k)) duplicates.push(k); fields[k] = v; };
  const head = raw.slice(4, end);
  const lines = head.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    if (/^\s/.test(line)) {
      return { fields: null, body: raw, error: `multi-line YAML is not supported in this bundle -- indented continuation line: "${line.trim()}"` };
    }
    // The one block form admitted: `verified:` or `sources:` with an empty value,
    // followed by indented `- { ... }` one-line maps (OKF v0.3 §5.1-5.2).
    const blk = line.match(/^(verified|sources):\s*$/);
    if (blk && i + 1 < lines.length && /^\s+-\s/.test(lines[i + 1])) {
      const items = [];
      while (i + 1 < lines.length && /^\s+-\s/.test(lines[i + 1])) {
        const item = lines[++i].replace(/^\s+-\s+/, '').trim();
        const map = item.startsWith('{') && item.endsWith('}') ? parseFlowMap(item) : null;
        if (!map) return { fields: null, body: raw, error: `bad ${blk[1]} entry (each must be a one-line { ... } map): "${item}"` };
        items.push(map);
      }
      setField(blk[1], items);
      continue;
    }
    if (/^[\w-]+:\s*[>|][+-]?\s*$/.test(line)) {
      return { fields: null, body: raw, error: `multi-line YAML block scalar is not supported in this bundle: "${line.trim()}"` };
    }
    const m = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (!m) return { fields: null, body: raw, error: `bad frontmatter line: "${line}"` };
    let v = m[2].trim();
    if (v.startsWith('[') && v.endsWith(']')) {
      const inner = v.slice(1, -1).trim();
      if (inner.startsWith('{')) {
        // A flow list of flow maps: `verified: [{ by, at }, { by, at }]` (OKF v0.3 §5.2).
        const items = [];
        const re = /\{[^{}]*\}/g;
        let mm;
        while ((mm = re.exec(inner))) {
          const map = parseFlowMap(mm[0]);
          if (!map) return { fields: null, body: raw, error: `bad flow map entry in list: "${mm[0]}"` };
          items.push(map);
        }
        if (inner.replace(re, '').replace(/[\s,]/g, '') !== '') return { fields: null, body: raw, error: `bad flow list of maps: "${v}"` };
        v = items;
      } else {
        v = inner.split(',').map((s) => unquote(s.trim())).filter(Boolean);
      }
    } else if (v.startsWith('"') && v.endsWith('"')) {
      v = v.slice(1, -1).replace(/\\(["\\])/g, '$1');
    } else if (v.startsWith("'") && v.endsWith("'")) {
      v = v.slice(1, -1);
    } else if (v.startsWith('{') && v.endsWith('}')) {
      const map = parseFlowMap(v);
      if (!map) return { fields: null, body: raw, error: `bad flow map entry: "${v}"` };
      v = map;
    }
    setField(m[1], v);
  }
  return { fields, body: raw.slice(end + 5), duplicates };
}

function unquote(v) {
  if (v.length > 1 && v.startsWith('"') && v.endsWith('"')) return v.slice(1, -1).replace(/\\(["\\])/g, '$1');
  if (v.length > 1 && v.startsWith("'") && v.endsWith("'")) return v.slice(1, -1);
  return v;
}

// Single-line YAML flow map -- the nested value the single-line profile admits
// (`generated: { by, at }`, a `verified` event, a `sources` entry). Split on
// commas; keys split at the FIRST colon so actor ids (human:jamesgray) survive;
// a quoted value (OKF v0.3's examples quote timestamps) is unquoted. Returns
// null on an entry with no colon.
function splitOutsideQuotes(text) {
  const parts = [];
  let cur = '';
  let q = null;
  for (const ch of text) {
    if (q) { if (ch === q) q = null; cur += ch; continue; }
    if (ch === '"' || ch === "'") { q = ch; cur += ch; continue; }
    if (ch === ',') { parts.push(cur); cur = ''; continue; }
    cur += ch;
  }
  parts.push(cur);
  return parts;
}
function parseFlowMap(text) {
  const map = {};
  for (const part of splitOutsideQuotes(text.trim().slice(1, -1))) {
    if (!part.trim()) continue;
    const c = part.indexOf(':');
    if (c === -1) return null;
    map[part.slice(0, c).trim()] = unquote(part.slice(c + 1).trim());
  }
  return map;
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

// OKF v0.3 §3.2: a .md file with no frontmatter is not a concept, and readers skip it. One whose
// frontmatter is there but can't be read (unterminated, multi-line) still counts, so lint reports it.
function isConcept(node) {
  return !!(node && (node.fm || node.error));
}

// --- Domain state and lifecycle (OKF v0.3 §5.4; SCHEMA.md "Domain state and lifecycle")
// `status` is the spec's lifecycle only; domain state lives in `state`. stateOf()
// reads either form, so a registry written before 11.1.0 (domain values in
// `status`) reads the same. Every reader of a node's state goes through it.
const LIFECYCLE_STATUS = ['draft', 'stable', 'deprecated'];
function present(v) { return v !== undefined && v !== null && String(v) !== ''; }
function stateOf(fm) {
  if (!fm) return null;
  if (present(fm.state)) return String(fm.state);
  if (present(fm.status) && !LIFECYCLE_STATUS.includes(String(fm.status))) return String(fm.status);
  return null;
}

// The types that carry domain state.
const STATE_TYPES = new Set(['Workflow', 'Business', 'LineOfBusiness']);

// OKF v0.3 §7: an actor is <producer>/<version> (an agent or tool, e.g.
// claude-code/claude-opus-5-5) or <scheme>:<id> (human:, team:, process:, or any other).
function isActor(v) {
  const s = String(v || '');
  return /^[a-z][a-z0-9+.-]*:\S+$/i.test(s) || /^[^\s/:]+\/\S+$/.test(s);
}

// OKF v0.3 §5: a timestamp is an RFC 3339 date-time with an offset, or a date only (the start of
// that UTC day). Milliseconds, or null when it doesn't parse.
function toMillis(v) {
  const s = String(v === undefined || v === null ? '' : v).trim();
  const m = s.match(/^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2}))?$/);
  if (!m) return null;
  // A real calendar day and time: Date.parse would roll 2026-02-30 over into March.
  const [y, mo, d] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const day = new Date(Date.UTC(y, mo - 1, d));
  if (day.getUTCFullYear() !== y || day.getUTCMonth() !== mo - 1 || day.getUTCDate() !== d) return null;
  if (m[4] === undefined) return day.getTime();
  if (Number(m[4]) > 23 || Number(m[5]) > 59 || Number(m[6]) > 59) return null;
  const t = Date.parse(s);
  return Number.isNaN(t) ? null : t;
}

// --- Bundle version (OKF v0.3 §8.1, §12)
// The root index.md's okf_version, or null. No version, or one below 0.3, is the
// 0.2 reading (§12.1's fallbacks apply); a version this code doesn't know is read
// best-effort as current, never refused.
function okfVersionOf(bundleDir) {
  let raw;
  try { raw = normalizeLineEndings(fs.readFileSync(path.join(bundleDir, 'index.md'), 'utf8')); } catch { return null; }
  const { fields } = parseFrontmatter(raw);
  return fields && present(fields.okf_version) ? String(fields.okf_version) : null;
}
function isLegacyVersion(v) {
  if (!present(v)) return true;
  const m = /^(\d+)\.(\d+)/.exec(String(v));
  if (!m) return false;
  return Number(m[1]) === 0 && Number(m[2]) < 3;
}

// --- Links and paths (OKF v0.3 §6; SCHEMA.md "Links")
// resolveHref(href, from, { legacy, bundleName }) -> { kind, path, form, href }
//   kind: 'external' (a URI scheme) | 'fragment' (#... only) | 'bundle' | 'outside'
//   form: 'root' (leading /) | 'relative' (from the linking file's own folder)
//         | 'legacy' (0.2 only: from the registry's parent folder)
//   path: 'bundle' -> '/dir/file.md'; 'outside' -> the path from the registry's
//         parent folder (the working folder), e.g. 'framework/x/requirements.md'
//         ('../...' when it climbs out of the working folder too). A trailing '/'
//         (a directory target) is kept; a #fragment is dropped.
// `from` is the linking file's bundle path ('/workflows/x.md'). In a 0.2 bundle
// (legacy) a bare path that doesn't start with './' or '../' keeps its 0.2
// meaning; the 0.3 form is read file-relative in either.
function decodePath(p) { try { return decodeURI(p); } catch { return p; } }
function resolveHref(href, from, opts = {}) {
  const bundleName = opts.bundleName || 'registry';
  if (/^[a-z][a-z0-9+.-]*:/i.test(href)) return { kind: 'external', path: href, form: 'url', href };
  if (href.startsWith('#')) return { kind: 'fragment', path: href, form: 'fragment', href };
  const bare = decodePath(href.replace(/[#?].*$/, ''));
  if (bare.startsWith('/')) return { kind: 'bundle', path: bare, form: 'root', href };
  // In 0.2 a bare path (./ included) is read from the registry's parent folder; only ../ is
  // read file-relative there, which is the 0.3 form 11.1.0's steps write into a 0.2 registry.
  if (opts.legacy && !bare.startsWith('../')) return { kind: 'outside', path: bare.replace(/^(\.\/)+/, ''), form: 'legacy', href };
  const fromDir = path.posix.dirname(from || '/index.md'); // '/workflows' or '/'
  let joined = path.posix.normalize(path.posix.join(bundleName, fromDir, bare));
  if (bare.endsWith('/') && !joined.endsWith('/')) joined += '/';
  if (joined === bundleName || joined === bundleName + '/' || joined.startsWith(bundleName + '/')) {
    return { kind: 'bundle', path: '/' + joined.slice(bundleName.length + 1), form: 'relative', href };
  }
  return { kind: 'outside', path: joined, form: 'relative', href };
}

// The link a writer puts in a file at bundle path `from` for `target`: a bundle
// path ('/dir/x.md') stays root-relative; a path from the working folder becomes
// file-relative by the file's depth ('../../framework/x/requirements.md' from a
// node, '../.claude/skills/s/SKILL.md' from the root index.md). In a 0.2 bundle
// (legacy) it keeps the 0.2 form, so derived views there don't change.
function linkTo(target, from, opts = {}) {
  if (target.startsWith('/') || opts.legacy || /^[a-z][a-z0-9+.-]*:/i.test(target)) return target;
  const bundleName = opts.bundleName || 'registry';
  const fromDir = path.posix.join(bundleName, path.posix.dirname(from || '/index.md'));
  let rel = path.posix.relative(fromDir, target.replace(/\/$/, ''));
  if (target.endsWith('/')) rel += '/';
  // A link is a URI reference (OKF v0.3 §6): a space or other reserved character is
  // percent-encoded, as resolveHref decodes it.
  return encodeURI(rel);
}

// All markdown link hrefs in text, classified per SCHEMA.md's discriminator.
// With `from` (the linking file's bundle path) each link is resolved as
// resolveHref says: inBundle holds bundle paths, repo the paths from the working
// folder, and `links` every resolved link (for checks that need the form).
// Without `from` the text is read the 0.2 way (every bare path from the working
// folder), for callers that only need in-bundle links.
function classifyLinks(raw, from, opts = {}) {
  const out = { inBundle: [], repo: [], external: [], links: [] };
  const re = /\]\(([^)\s]+)\)/g;
  let m;
  while ((m = re.exec(raw || ''))) {
    const href = m[1];
    const r = from === undefined ? resolveHref(href, '/index.md', { ...opts, legacy: true }) : resolveHref(href, from, opts);
    if (r.kind === 'fragment') continue;
    out.links.push(r);
    if (r.kind === 'external') out.external.push(href);
    else if (r.kind === 'bundle') out.inBundle.push(r.path);
    else out.repo.push(r.path);
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
  let realRoot = absRoot;
  try { realRoot = fs.realpathSync(absRoot); } catch { /* missing: the walk finds nothing */ }
  const nodes = new Map();
  const errors = [];
  (function walk(dir) {
    let entries;
    try { entries = fs.readdirSync(dir).sort(); } catch { return; }
    for (const name of entries) {
      // OKF v0.3 §3.2: dot-paths are not part of the bundle, and a symbolic link
      // that leaves the bundle root is not followed.
      if (name.startsWith('.')) continue;
      const full = path.join(dir, name);
      let st;
      try { st = fs.statSync(full); } catch { continue; }
      try {
        if (fs.lstatSync(full).isSymbolicLink()) {
          const real = fs.realpathSync(full);
          if (real !== realRoot && !real.startsWith(realRoot + path.sep)) continue;
        }
      } catch { continue; }
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
// The framework folder is framework/ in the registry's parent folder (the working
// folder), beside registry/, on every platform; the legacy layout with registry/
// inside the framework folder still reads <slug>/; an old relative link resolves
// through framework/ (resolveRepoLink). (SCHEMA.md "Layered model".)

// A workflow folder holds at least one of these record files.
const RECORD_MARKERS = ['requirements.md', 'deconstruct-in-progress.md', 'design-plan.md', 'build-record.md', 'test-results.md'];
// Folders in the framework folder that are never workflow folders.
const NOT_WORKFLOW_DIRS = new Set(['history', 'registry']);

function isDirSafe(p) { try { return fs.statSync(p).isDirectory(); } catch { return false; } }

// { dir: absolute framework folder, prefix: link prefix for its workflow
// folders ('framework/' on every platform, '' in the legacy layout with
// registry/ inside the framework folder) }. A working folder
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
// cannot stat. With an empty prefix (the legacy layout, registry/ inside the
// framework folder, read as <slug>/) only folders holding a record file count,
// so sops/, process-guides/ and the like are never mistaken for workflows.
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

// The repo path a relative link resolves to from the registry's parent folder:
// the link as written when it resolves, else framework/ + the link when the link
// doesn't already start with framework/ and that resolves, so an old relative
// link (such as <slug>/requirements.md) resolves through framework/. A trailing
// '/' marks a directory target. A link that climbs with '..' never takes the
// fallback. Returns null when neither resolves. Nothing is rewritten.
function resolveRepoLink(href, workspaceRoot) {
  const isDirLink = href.endsWith('/');
  const resolves = (rel) => {
    const target = path.join(workspaceRoot, rel);
    return isDirLink ? isDirSafe(target) : fs.existsSync(target);
  };
  if (resolves(href)) return href;
  if (href.startsWith('framework/') || href.split('/').includes('..')) return null;
  const fallback = `framework/${href}`;
  return resolves(fallback) ? fallback : null;
}

// The path from the working folder that a resolved 'outside' link reaches, or
// null when nothing is there. Only a 0.2-form link gets resolveRepoLink's
// framework/ fallback; a file-relative link means exactly what it says.
function resolveOutside(link, workspaceRoot) {
  if (link.form === 'legacy') return resolveRepoLink(link.path, workspaceRoot);
  const isDirLink = link.path.endsWith('/');
  const target = path.join(workspaceRoot, link.path);
  return (isDirLink ? isDirSafe(target) : fs.existsSync(target)) ? link.path : null;
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

// OKF v0.3 §5.2: `verified` is a list of { by, at } events; a bare map is a
// list of one; an event without both keys is ignored.
function verifiedEvents(fm) {
  const v = fm && fm.verified;
  if (!present(v)) return [];
  const list = Array.isArray(v) ? v : [v];
  return list.filter((e) => e && typeof e === 'object' && present(e.by) && present(e.at));
}

// Last-content-change accessor (generated.at).
function lastChanged(fm) {
  if (!fm) return '';
  if (fm.generated && typeof fm.generated === 'object' && fm.generated.at) return fm.generated.at;
  return '';
}

module.exports = {
  TOOLS_VERSION,
  DIR_TYPES, RESERVED, ENUMS, LEGACY_TOLERATED, BANNED_FIELDS, SECTION_NAMES,
  ARTIFACT_LABELS, LEGACY_LABELS, AT_INSTANT, AT_DATE, RECORD_MARKERS,
  LIFECYCLE_STATUS, STATE_TYPES, isActor, toMillis, stateOf, isConcept, okfVersionOf, isLegacyVersion, resolveHref, linkTo, resolveOutside, verifiedEvents,
  normalizeLineEndings, parseFrontmatter, parseCapabilityFrontmatter, parseSections, orderedLinks, classifyLinks, slugOf,
  findGeneratedBlocks, renderGeneratedBlock, replaceGeneratedBlock,
  loadBundle, scanSops, frameworkFolder, scanFrameworkFolders, resolveRepoLink, runLogHasEntries, artifactLabels, scanCapabilities,
  isGitIgnored, lastChanged,
};
