#!/usr/bin/env node
// registry-template/tools/framework-state.js
// Works out where an AI Workflow Framework workflow is (routing states 0 to 11)
// by the routing rule: each skill's references/routing.md, whose canonical copy
// is scripts/framework/routing.md in the handsonai repo. That file is this
// script's specification and its written fallback: when the script can't run,
// or exits non-zero, the skill applies routing.md by hand.
//
// Read-only: it never writes, moves or creates a file. Zero npm dependencies --
// Node >=18 built-ins only, and self-contained (no require of registry-lib.js),
// because the plugin ships an identical copy at plugins/handsonai/tools/.
//
// What it reads (routing.md "What it reads"): the workflow folder's current
// files; history/ only for whether a set-aside-*/ folder exists, the newest
// set-aside build record (the live test with no registry), and the finished
// rounds (history/test-results-round-*.md), for the last Ready round it reports
// as a fact. Never a dated copy (design-spec-2026-09-20.md, history/[file]-
// YYYY-MM-DD-HHMM.md), never an earlier-version-*/ folder, no install check.
//
// Usage:
//   node framework-state.js <workflow-folder>        one workflow's state
//   node framework-state.js --continue <folder>      "continue my workflow"
//                                                    over a framework folder,
//                                                    or a workspace holding one
// Options:
//   --registry <dir>   the registry/ bundle to read (default: found beside or
//                      inside the framework folder)
//   --no-registry      read as if there were no registry
//   --json             print the JSON only
//   --line             print the readable line only
//
// Default output: the readable line, then the JSON (the state, its owner and
// every fact the rule used), then MODEL_NOTE, one line telling the skill that
// reads it not to describe it to the leader. Exit 0 with a state; 1 on bad
// usage; 2 when a folder or file can't be read or parsed, or no state matches
// -- the caller then falls back to routing.md.
'use strict';
const fs = require('fs');
const path = require('path');

const STATE_NAMES = {
  0: 'Not a framework workflow, or retired',
  1: 'Earlier version',
  2: 'Redo pending',
  3: 'Requirements needed',
  4: 'Plan needed',
  5: 'Plan to approve',
  6: 'Build needed',
  7: 'Waiting on an open item',
  8: 'Test needed',
  9: 'Waiting on access',
  10: 'Ready to go live',
  11: 'Live',
};
const STATE_OWNERS = {
  0: null, 2: 'Deconstruct', 3: 'Deconstruct', 4: 'Design', 5: 'Design',
  6: 'Build', 7: 'Design', 8: 'Test', 9: 'Test', 10: 'Test', 11: 'Test',
};
const START_PHRASES = {
  Analyze: 'run the analyze skill',
  Deconstruct: 'run the deconstruct skill',
  Design: 'run the design skill',
  Build: 'run the build skill',
  Test: 'test the workflow I built',
};
// Folders inside the framework folder that are never workflow folders.
const NOT_WORKFLOW_DIRS = new Set(['history', 'registry']);

class Unreadable extends Error {}

// --- File access (read-only) -------------------------------------------------

function statOrNull(p) {
  try {
    return fs.statSync(p);
  } catch (e) {
    if (e.code === 'ENOENT' || e.code === 'ENOTDIR') return null;
    throw new Unreadable(`can't read ${p}: ${e.code || e.message}`);
  }
}
function isDir(p) { const s = statOrNull(p); return !!(s && s.isDirectory()); }
function isFile(p) { const s = statOrNull(p); return !!(s && s.isFile()); }

function readText(p) {
  try {
    return fs.readFileSync(p, 'utf8').replace(/^﻿/, '').replace(/\r\n/g, '\n');
  } catch (e) {
    throw new Unreadable(`can't read ${p}: ${e.code || e.message}`);
  }
}
function readTextIfFile(p) { return isFile(p) ? readText(p) : null; }

function listDir(p) {
  try {
    return fs.readdirSync(p, { withFileTypes: true });
  } catch (e) {
    throw new Unreadable(`can't read folder ${p}: ${e.code || e.message}`);
  }
}

// --- A small YAML subset -----------------------------------------------------
// The framework's files use block maps, block lists (of flow maps or of block
// maps), flow maps and lists, and plain or quoted scalars. That subset is all
// this parses; anything else throws, so a malformed file exits non-zero rather
// than routing on a misread fact.

function scalar(raw) {
  const v = raw.trim();
  if (v === '' || v === '~' || v === 'null') return null;
  if (v === 'true') return true;
  if (v === 'false') return false;
  if (/^-?\d+$/.test(v)) return Number(v);
  if (/^-?\d+\.\d+$/.test(v)) return v; // versions such as 4.0 stay strings
  return v;
}

function parseFlow(src) {
  let i = 0;
  const ws = () => { while (i < src.length && /\s/.test(src[i])) i++; };
  const fail = (msg) => { throw new Error(`${msg} at column ${i + 1} in "${src}"`); };
  function quoted() {
    const q = src[i++];
    let out = '';
    while (i < src.length && src[i] !== q) {
      if (q === '"' && src[i] === '\\' && i + 1 < src.length) { out += src[i + 1]; i += 2; continue; }
      if (q === "'" && src[i] === "'" && src[i + 1] === "'") { out += "'"; i += 2; continue; }
      out += src[i++];
    }
    if (src[i] !== q) fail('unterminated string');
    i++;
    return out;
  }
  function plain(stops) {
    const start = i;
    while (i < src.length && !stops.includes(src[i])) {
      if (src[i] === ':' && stops.includes(':') && (i + 1 >= src.length || /\s/.test(src[i + 1]))) break;
      i++;
    }
    return src.slice(start, i);
  }
  function value(stops) {
    ws();
    if (src[i] === '{') return map();
    if (src[i] === '[') return list();
    if (src[i] === '"' || src[i] === "'") return quoted();
    return scalar(plain(stops));
  }
  function map() {
    i++;
    const out = {};
    ws();
    if (src[i] === '}') { i++; return out; }
    for (;;) {
      ws();
      const key = (src[i] === '"' || src[i] === "'") ? quoted() : plain([':', ',', '}']).trim();
      ws();
      if (src[i] !== ':') fail('expected ":"');
      i++;
      out[key] = value([',', '}']);
      ws();
      if (src[i] === ',') { i++; continue; }
      if (src[i] === '}') { i++; return out; }
      fail('expected "," or "}"');
    }
  }
  function list() {
    i++;
    const out = [];
    ws();
    if (src[i] === ']') { i++; return out; }
    for (;;) {
      out.push(value([',', ']']));
      ws();
      if (src[i] === ',') { i++; continue; }
      if (src[i] === ']') { i++; return out; }
      fail('expected "," or "]"');
    }
  }
  const v = value([]);
  ws();
  if (i < src.length) fail('unexpected text after the value');
  return v;
}

function inlineValue(raw) {
  const v = raw.trim();
  if (v.startsWith('{') || v.startsWith('[')) return parseFlow(v);
  if ((v.startsWith('"') && v.endsWith('"') && v.length > 1) || (v.startsWith("'") && v.endsWith("'") && v.length > 1)) {
    return parseFlow(v);
  }
  return scalar(v);
}

function parseYaml(text) {
  const lines = text.split('\n')
    .map((l, n) => ({ n: n + 1, indent: l.match(/^ */)[0].length, text: l.trim() }))
    .filter((l) => l.text !== '' && !l.text.startsWith('#'));
  let pos = 0;
  const err = (l, msg) => { throw new Error(`line ${l.n}: ${msg}: "${l.text}"`); };
  const KEY = /^("[^"]*"|'[^']*'|[^\s:][^:]*?):(?:\s+(.*))?$/;

  function block(indent) {
    const first = lines[pos];
    if (first.text === '-' || first.text.startsWith('- ')) return seq(indent);
    return mapping(indent);
  }
  function mapping(indent, out = {}) {
    while (pos < lines.length && lines[pos].indent === indent) {
      const l = lines[pos];
      if (l.text === '-' || l.text.startsWith('- ')) break;
      const m = l.text.match(KEY);
      if (!m) err(l, 'expected "key: value"');
      const key = m[1].replace(/^["']|["']$/g, '');
      pos++;
      if (m[2] !== undefined && m[2] !== '') {
        if (/^[>|]/.test(m[2])) err(l, 'block scalars are not supported');
        out[key] = inlineValue(m[2]);
      } else if (pos < lines.length && lines[pos].indent > indent) {
        out[key] = block(lines[pos].indent);
      } else if (pos < lines.length && lines[pos].indent === indent && lines[pos].text.startsWith('- ')) {
        out[key] = seq(indent); // a list written at the key's own indent
      } else {
        out[key] = null;
      }
    }
    if (pos < lines.length && lines[pos].indent > indent) err(lines[pos], 'unexpected indent');
    return out;
  }
  function seq(indent) {
    const out = [];
    while (pos < lines.length && lines[pos].indent === indent && (lines[pos].text === '-' || lines[pos].text.startsWith('- '))) {
      const l = lines[pos];
      const rest = l.text.slice(1).trim();
      if (rest === '') {
        pos++;
        out.push(pos < lines.length && lines[pos].indent > indent ? block(lines[pos].indent) : null);
      } else if (/^[{["']/.test(rest) || !KEY.test(rest)) {
        pos++;
        out.push(inlineValue(rest));
      } else {
        // "- key: value" opens a block map whose keys sit two columns in.
        const inner = indent + (l.text.length - rest.length);
        lines[pos] = { n: l.n, indent: inner, text: rest };
        out.push(mapping(inner));
      }
    }
    return out;
  }
  if (!lines.length) return {};
  if (lines[0].indent !== 0) err(lines[0], 'unexpected indent');
  const out = mapping(0);
  if (pos < lines.length) err(lines[pos], 'could not parse');
  return out;
}

// Splits a Markdown file into { fm, body }. fm is null with no frontmatter.
function splitFrontmatter(text, file) {
  if (!text.startsWith('---\n')) return { fm: null, body: text };
  let end = text.indexOf('\n---\n', 3);
  let bodyStart = end + 5;
  if (end === -1 && text.endsWith('\n---')) { end = text.length - 4; bodyStart = text.length; }
  if (end === -1) throw new Unreadable(`${file}: unterminated frontmatter (no closing "---")`);
  try {
    return { fm: parseYaml(text.slice(4, end + 1)), body: text.slice(bodyStart) };
  } catch (e) {
    throw new Unreadable(`${file}: can't parse frontmatter: ${e.message}`);
  }
}

function readDoc(p) {
  const text = readTextIfFile(p);
  if (text === null) return null;
  const { fm, body } = splitFrontmatter(text, p);
  return { fm, body, text };
}

// --- Markdown helpers ----------------------------------------------------------

// The text under a "## Heading" (to the next "## " heading), or null.
function section(body, heading) {
  const lines = body.split('\n');
  const start = lines.findIndex((l) => l.replace(/\s+$/, '') === `## ${heading}`);
  if (start === -1) return null;
  const out = [];
  for (let i = start + 1; i < lines.length; i++) {
    if (/^## /.test(lines[i]) || /^# /.test(lines[i])) break;
    out.push(lines[i]);
  }
  return out.join('\n');
}

// Every Markdown table in a block of text, as arrays of row objects keyed by
// the header cells.
function tables(text) {
  const out = [];
  const lines = (text || '').split('\n');
  for (let i = 0; i < lines.length - 1; i++) {
    if (!/^\s*\|/.test(lines[i]) || !/^\s*\|[\s|:-]+\|\s*$/.test(lines[i + 1])) continue;
    const cells = (l) => l.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
    const header = cells(lines[i]);
    const rows = [];
    let j = i + 2;
    for (; j < lines.length && /^\s*\|/.test(lines[j]); j++) {
      const c = cells(lines[j]);
      const row = {};
      header.forEach((h, k) => { row[h] = c[k] === undefined ? '' : c[k]; });
      rows.push(row);
    }
    out.push({ header, rows });
    i = j - 1;
  }
  return out;
}

const clean = (s) => String(s == null ? '' : s).replace(/[`*]/g, '').trim();
const num = (v) => {
  if (typeof v === 'number') return v;
  const m = String(v == null ? '' : v).match(/^\s*(\d+)\s*$/);
  return m ? Number(m[1]) : null;
};
const asList = (v) => (Array.isArray(v) ? v : []);

// --- The registry --------------------------------------------------------------

function isRegistryDir(p) {
  return isDir(p) && (isFile(path.join(p, 'SCHEMA.md')) || isDir(path.join(p, 'workflows')));
}

// The registry sits in the workspace beside the framework folder (Claude Code,
// Codex) or inside the framework folder (a drive, Claude desktop).
function findRegistry(frameworkDir, opts) {
  if (opts.noRegistry) return null;
  if (opts.registry) {
    if (!isDir(opts.registry)) throw new Unreadable(`can't read the registry folder ${opts.registry}`);
    return path.resolve(opts.registry);
  }
  for (const cand of [path.join(frameworkDir, 'registry'), path.join(path.dirname(frameworkDir), 'registry')]) {
    if (isRegistryDir(cand)) return cand;
  }
  return null;
}

function readNode(registryDir, slug) {
  const p = path.join(registryDir, 'workflows', `${slug}.md`);
  const doc = readDoc(p);
  if (!doc) return null;
  const fm = doc.fm || {};
  // Linked skills or agents (only for N-B44, never a sign of an earlier version).
  const linked = (name) => {
    const m = doc.body.match(new RegExp(`^# ${name}\\s*\\n([\\s\\S]*?)(?=^# |$(?![\\s\\S]))`, 'm'));
    return !!(m && /\[[^\]]+\]\([^)]+\)/.test(m[1]));
  };
  return {
    path: p,
    status: fm.status == null ? null : String(fm.status),
    big_change: fm.big_change == null || fm.big_change === '' ? null : String(fm.big_change),
    links_skills_or_agents: linked('Skills') || linked('Agents'),
  };
}

// A workflow's node is registry/workflows/<slug>.md, where <slug> is its folder's
// name: a rename keeps the node's ID and the folder's name, and changes only the
// name and description. A folder left with a name no node has (a rename made
// before that rule) is matched to the node whose # Artifacts link into it, so
// its status and big_change are still read rather than missed (fail closed: a
// live workflow must still read as live).
function nodeForFolder(registryDir, slug) {
  const byName = readNode(registryDir, slug);
  if (byName) return byName;
  const dir = path.join(registryDir, 'workflows');
  if (!isDir(dir)) return null;
  const esc = slug.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const linkInto = new RegExp(`\\]\\((?:\\.\\/)?(?:framework\\/)?${esc}\\/[^)]*\\)`);
  const found = [];
  for (const d of listDir(dir)) {
    if (!d.isFile() || !d.name.endsWith('.md') || d.name === 'index.md') continue;
    const doc = readDoc(path.join(dir, d.name));
    if (!doc) continue;
    const m = doc.body.match(/^# Artifacts\s*\n([\s\S]*?)(?=^# |$(?![\s\S]))/m);
    if (m && linkInto.test(m[1])) found.push(d.name.slice(0, -3));
  }
  if (found.length !== 1) return null;
  return { ...readNode(registryDir, found[0]), slug: found[0], found_by_link: true };
}

function listNodes(registryDir) {
  const dir = path.join(registryDir, 'workflows');
  if (!isDir(dir)) return [];
  return listDir(dir)
    .filter((d) => d.isFile() && d.name.endsWith('.md') && d.name !== 'index.md')
    .map((d) => ({ slug: d.name.slice(0, -3), ...readNode(registryDir, d.name.slice(0, -3)) }));
}

// --- Reading one workflow folder -------------------------------------------------

function liveSinceIn(body) {
  // The record's top section, for people: everything before its first table
  // section. "Live since [date]" sits there once Test has taken it live.
  const top = body.split(/^## (?!What was built)/m)[0];
  const m = top.match(/(?:^|\n)\s*(?:[-*]\s*)?Live since (\d{4}-\d{2}-\d{2})/);
  return m ? m[1] : null;
}

function planTasks(body) {
  const tasksText = section(body, 'Tasks');
  if (tasksText === null) return [];
  const out = [];
  const parts = tasksText.split(/^### /m).slice(1);
  for (const part of parts) {
    const id = clean(part.split('\n')[0].split(/\s+[—–-]\s+/)[0]);
    const field = (name) => {
      const m = part.match(new RegExp(`^\\s*-\\s*\\*\\*${name}:\\*\\*\\s*(.*)$`, 'mi'));
      return m ? m[1].trim() : null;
    };
    const revRaw = field('rev');
    out.push({ id, rev: revRaw === null ? null : num(clean(revRaw)), depends_on: field('Depends on') || '' });
  }
  return out;
}

function openItems(body) {
  const text = section(body, 'Open items');
  if (text === null) return [];
  const items = [];
  for (const line of text.split('\n')) {
    const m = line.match(/^\s*(\d+)\.\s+(.*)$/);
    if (!m) continue;
    const t = m[2];
    const blocks = (t.match(/Blocks:\s*([^.]*)/i) || [, ''])[1].match(/\b(T\d+|KW|SCH)\b/g) || [];
    items.push({ n: Number(m[1]), answered: /\banswered\b/i.test(t) && !/\bto ask\b/i.test(t), blocks });
  }
  return items;
}

function recordRows(body) {
  const rows = [];
  for (const t of tables(body)) {
    if (!t.header.includes('Built rev') || !t.header.includes('Task')) continue;
    for (const r of t.rows) {
      const task = clean(r.Task);
      if (!task || task === '—' || task === '-') continue;
      rows.push({ task, status: clean(r.Status), saved: clean(r.Saved).toLowerCase(), built_rev: num(clean(r['Built rev'])) });
    }
  }
  return rows;
}

const BUILT_STATUS = /^(created|reused|extended|installed|built|updated|rebuilt|reinstalled|adopted)\b/i;

function issuesAtLevel(body, level) {
  const text = section(body, 'Issues identified');
  if (!text) return 0;
  let n = 0;
  for (const t of tables(text)) {
    if (!t.header.includes('Level')) continue;
    for (const r of t.rows) if (clean(r.Level).toLowerCase() === level) n++;
  }
  return n;
}

function setAsideDirs(historyDir) {
  if (!isDir(historyDir)) return [];
  return listDir(historyDir)
    .filter((d) => d.isDirectory() && /^set-aside-/.test(d.name))
    .map((d) => d.name)
    .sort();
}

// --- Earlier versions (routing.md "Earlier versions"; rules 11.2) -----------------

function earlierVersion(f) {
  const signs = [];
  if (f.requirements) {
    const fm = f.requirements.fm || {};
    const body = f.requirements.body;
    if (!('revision' in fm)) signs.push({ owner: 'Deconstruct', sign: 'requirements.md has no revision:' });
    else if (/^\|\s*Definition Type\s*\|/m.test(body)) signs.push({ owner: 'Deconstruct', sign: 'requirements.md has a Definition Type row' });
    else if (/^## Steps Overview\s*$/m.test(body)) signs.push({ owner: 'Deconstruct', sign: 'requirements.md has a ## Steps Overview heading' });
    else if (/^## Inputs\s*$/m.test(body) && !/^## Path\s*$/m.test(body)) signs.push({ owner: 'Deconstruct', sign: 'requirements.md has ## Inputs with no ## Path' });
  }
  if (f.design_spec_exists) signs.push({ owner: 'Design', sign: 'the plan is a design-spec.md' });
  else if (f.plan && !('requirements_revision' in (f.plan.fm || {}))) signs.push({ owner: 'Design', sign: 'design-plan.md has no requirements_revision:' });
  if (f.results && !f.record && !f.set_aside.length) signs.push({ owner: 'Build', sign: 'test-results.md with no build-record.md and no history/set-aside-*/' });
  if (f.results && !('round' in (f.results.fm || {}))) signs.push({ owner: 'Test', sign: 'test-results.md has no round:' });
  return signs;
}

// --- The state ------------------------------------------------------------------

function workflowState(folder, opts = {}) {
  folder = path.resolve(folder);
  const slug = path.basename(folder);
  const frameworkDir = path.dirname(folder);
  if (!isDir(frameworkDir)) throw new Unreadable(`can't read the framework folder ${frameworkDir}`);
  const st = statOrNull(folder);
  if (st && !st.isDirectory()) throw new Unreadable(`${folder} is not a folder`);
  const folderExists = !!st;
  if (folderExists) listDir(folder); // fails on a folder that exists but can't be read

  const registryDir = opts.registryDir !== undefined ? opts.registryDir : findRegistry(frameworkDir, opts);
  const node = registryDir ? nodeForFolder(registryDir, slug) : null;

  const at = (name) => path.join(folder, name);
  const f = {
    requirements: folderExists ? readDoc(at('requirements.md')) : null,
    plan: folderExists ? readDoc(at('design-plan.md')) : null,
    record: folderExists ? readDoc(at('build-record.md')) : null,
    results: folderExists ? readDoc(at('test-results.md')) : null,
    design_spec_exists: folderExists && isFile(at('design-spec.md')),
    progress_exists: folderExists && isFile(at('deconstruct-in-progress.md')),
    run_guide_exists: folderExists && isFile(at('run-guide.md')),
    old_run_log_exists: folderExists && (isFile(at('runs.md')) || isFile(at('run-log.md')) || isDir(at('test-runs'))),
    set_aside: folderExists ? setAsideDirs(at('history')) : [],
  };

  const facts = {
    workflow: slug,
    folder,
    folder_exists: folderExists,
    registry: registryDir,
    node: registryDir ? (node ? { status: node.status, big_change: node.big_change, links_skills_or_agents: node.links_skills_or_agents, ...(node.found_by_link ? { slug: node.slug, found_by: 'a link in its # Artifacts into this folder' } : {}) } : 'missing') : null,
    files: {
      'requirements.md': !!f.requirements,
      'deconstruct-in-progress.md': f.progress_exists,
      'design-plan.md': !!f.plan,
      'build-record.md': !!f.record,
      'test-results.md': !!f.results,
      'design-spec.md': f.design_spec_exists,
      'run-guide.md': f.run_guide_exists,
      'old run log': f.old_run_log_exists,
    },
    set_aside: f.set_aside,
  };
  const warnings = [];
  if (node && node.found_by_link) warnings.push(`the folder ${slug} has no node of its own name; the node ${node.slug} links into it and is read instead`);
  if (registryDir && !node) warnings.push(`the registry has no Workflow node for ${slug}: its status and big_change can't be read`);

  const done = (state, reason, extra = {}) => ({
    workflow: slug,
    state,
    name: STATE_NAMES[state],
    owner: extra.owner !== undefined ? extra.owner : STATE_OWNERS[state],
    reason,
    ...extra,
    facts,
    warnings,
  });

  // Live (routing.md "Terms").
  let liveSince = null;
  let liveFrom = null;
  if (f.record) { liveSince = liveSinceIn(f.record.body); if (liveSince) liveFrom = 'build-record.md'; }
  if (!liveSince && f.set_aside.length) {
    for (const d of f.set_aside.slice().reverse()) {
      const rec = readTextIfFile(path.join(folder, 'history', d, 'build-record.md'));
      if (rec === null) continue;
      const { body } = splitFrontmatter(rec, path.join(folder, 'history', d, 'build-record.md'));
      liveSince = liveSinceIn(body);
      if (liveSince) liveFrom = `history/${d}/build-record.md`;
      break; // only the newest set-aside build record
    }
  }
  const live = registryDir ? !!(node && node.status === 'in-production') : !!liveSince;
  facts.live = live;
  if (!registryDir) facts.live_since = liveSince ? `${liveSince} (${liveFrom})` : null;

  // State 0.
  if (registryDir && node && node.status === 'retired') {
    return done(0, 'the node is retired', { kind: 'retired', line: 'retired line' });
  }
  if (registryDir && node && node.status === 'in-production' && !folderExists) {
    return done(0, 'the node is in-production and the workflow has no folder (running work)', { kind: 'running-work', line: 'running-work message' });
  }

  // State 1.
  const signs = folderExists ? earlierVersion(f) : [];
  facts.earlier_version_signs = signs.map((s) => `${s.sign} (${s.owner})`);
  if (signs.length) {
    const nb44 = !!(
      (node && node.status === 'in-production') ||
      (node && node.links_skills_or_agents) ||
      f.results || f.run_guide_exists || f.old_run_log_exists
    );
    return done(1, `earlier version: ${signs[0].sign}`, { owner: signs[0].owner, n_b44: nb44, line: 'N-T22 (when this step is not the owner)' });
  }

  // State 2.
  const bigChange = registryDir ? (node ? node.big_change : null)
    : (f.requirements && f.requirements.fm && f.requirements.fm.big_change ? String(f.requirements.fm.big_change) : null);
  facts.big_change = bigChange;
  if (bigChange) return done(2, `big_change is set: ${bigChange}`);

  // State 3.
  if (!f.requirements) return done(3, folderExists ? 'no requirements.md' : 'no workflow folder yet');
  if (f.progress_exists) return done(3, 'deconstruct-in-progress.md is there');

  // Facts for states 4 to 11.
  const req = f.requirements.fm || {};
  const reqRevision = num(req.revision);
  const unaffected = new Set(asList(req.revisions).filter((r) => r && r.plan_unaffected === true).map((r) => num(r.revision)));
  let effectiveRevision = reqRevision;
  while (effectiveRevision !== null && effectiveRevision > 1 && unaffected.has(effectiveRevision)) effectiveRevision--;
  facts.requirements_revision = reqRevision;
  if (unaffected.size) facts.requirements_revision_not_counting_plan_unaffected = effectiveRevision;

  if (!f.plan) return done(4, 'no design-plan.md');
  const plan = f.plan.fm || {};
  const tasks = planTasks(f.plan.body);
  const planRevision = tasks.length && tasks.every((t) => t.rev !== null) ? Math.max(...tasks.map((t) => t.rev)) : null;
  facts.plan_requirements_revision = num(plan.requirements_revision);
  facts.plan_revision = planRevision;
  facts.plan_approved = plan.approved === true || plan.approved === 'true';
  if (tasks.some((t) => t.rev === null)) warnings.push(`a task in design-plan.md has no rev: ${tasks.filter((t) => t.rev === null).map((t) => t.id).join(', ')}`);

  const logged = new Set(asList(plan.changes).map((c) => c && String(c.id)));
  const requests = [];
  for (const [file, doc] of [['build-record.md', f.record], ['test-results.md', f.results]]) {
    if (!doc || !doc.fm) continue;
    for (const r of asList(doc.fm.change_requests)) {
      // An entry with no id can't be matched against the plan's changes:, so it
      // can't be routed: fail closed (exit 2, the written fallback) rather than skip it.
      if (!r || typeof r !== 'object' || r.id == null || String(r.id).trim() === '') {
        throw new Unreadable(`${file}: a change_requests entry has no id`);
      }
      const t = asList(r.tasks).map(String);
      const scheduleOnly = t.length > 0 && t.every((x) => x === 'SCH');
      requests.push({ id: String(r.id), file, schedule_only: scheduleOnly, logged: logged.has(String(r.id)) });
    }
  }
  const unlogged = requests.filter((r) => !r.logged && !r.schedule_only).map((r) => `${r.id} (${r.file})`);
  facts.unlogged_change_requests = unlogged;
  const schedOnly = requests.filter((r) => !r.logged && r.schedule_only).map((r) => r.id);
  if (schedOnly.length) facts.schedule_only_requests_not_counted = schedOnly;

  if (effectiveRevision !== null && facts.plan_requirements_revision !== null && effectiveRevision > facts.plan_requirements_revision) {
    return done(4, `the requirements' revision ${effectiveRevision} is above the plan's requirements_revision ${facts.plan_requirements_revision}`);
  }
  if (unlogged.length) return done(4, `an unlogged change request: ${unlogged.join(', ')}`);

  // State 5.
  if (!facts.plan_approved) return done(5, 'the plan is not approved: true');

  // Open items and waiting tasks.
  const items = openItems(f.plan.body);
  const unanswered = items.filter((i) => !i.answered);
  const waiting = new Set();
  for (const t of tasks) {
    const refs = (t.depends_on.match(/open item (\d+)/gi) || []).map((s) => Number(s.match(/\d+/)[0]));
    if (refs.some((n) => unanswered.some((i) => i.n === n))) waiting.add(t.id);
  }
  for (const i of unanswered) for (const id of i.blocks) if (tasks.some((t) => t.id === id)) waiting.add(id);
  // A task that depends on a waiting task can't be built either.
  for (let changed = true; changed;) {
    changed = false;
    for (const t of tasks) {
      if (waiting.has(t.id)) continue;
      const deps = t.depends_on.match(/\b(T\d+|KW|SCH)\b/g) || [];
      if (deps.some((d) => waiting.has(d))) { waiting.add(t.id); changed = true; }
    }
  }
  facts.unanswered_open_items = unanswered.map((i) => i.n);
  facts.tasks_waiting_on_open_items = [...waiting];

  // Rounds.
  const results = f.results ? (f.results.fm || {}) : null;
  const lastRound = results ? (num(results.round) || 0) : 0;
  const record = f.record ? (f.record.fm || {}) : null;
  const lastClose = record ? num(record.last_close_after_round) : null;
  const closeAfterLastRound = lastClose !== null && lastClose >= lastRound;
  facts.last_round = lastRound;
  if (results) {
    facts.last_round_status = results.round_status || null;
    facts.last_round_readiness = results.readiness || null;
    facts.last_round_plan_revision = num(results.plan_revision);
    facts.go_live = results.go_live || null;
    if (results.direct_edit) facts.direct_edit = results.direct_edit;
  }
  facts.record_plan_revision = record ? num(record.plan_revision) : null;
  facts.last_close_after_round = lastClose;
  facts.build_close_after_last_round = closeAfterLastRound;
  const buildIssues = f.results ? issuesAtLevel(f.results.body, 'build') : 0;
  facts.issues_at_level_build = buildIssues;
  // A round left behind (routing.md): Test abandons it before it opens the next.
  if (results && results.round_status === 'in-progress' &&
      ((facts.last_round_plan_revision !== null && facts.last_round_plan_revision !== planRevision) ||
       (lastClose !== null && lastRound <= lastClose))) {
    facts.round_left_behind = lastRound;
  }
  facts.last_ready_round = lastReadyRound(folder, f.results, warnings);

  // State 6.
  if (!f.record) return done(6, 'no build-record.md');
  const rows = recordRows(f.record.body);
  const notBuilt = [];
  const behind = [];
  for (const t of tasks) {
    const mine = rows.filter((r) => r.task === t.id);
    const builtAndSaved = mine.length > 0 && mine.every((r) => BUILT_STATUS.test(r.status) && r.saved === 'yes');
    if (!builtAndSaved && !waiting.has(t.id)) notBuilt.push(t.id);
    const builtRevs = mine.map((r) => r.built_rev).filter((v) => v !== null);
    if (builtAndSaved && t.rev !== null && (!builtRevs.length || t.rev > Math.min(...builtRevs))) behind.push(t.id);
  }
  facts.tasks_not_built_and_saved = notBuilt;
  facts.tasks_above_built_rev = behind;
  const fixMode = results && results.readiness === 'not-ready' && buildIssues > 0 && !closeAfterLastRound;
  if (notBuilt.length) return done(6, `not built and saved: ${notBuilt.join(', ')}`, { fix_mode: !!fixMode });
  if (behind.length) return done(6, `a task's rev is above its built rev: ${behind.join(', ')}`, { fix_mode: !!fixMode });
  if (!waiting.size && (facts.record_plan_revision === null || facts.record_plan_revision !== planRevision)) {
    return done(6, facts.record_plan_revision === null
      ? "the build record's plan_revision isn't set (Build hasn't closed)"
      : `the build record's plan_revision ${facts.record_plan_revision} isn't the plan revision ${planRevision}`, { fix_mode: !!fixMode });
  }
  if (results && results.direct_edit === 'undo' && !closeAfterLastRound) {
    return done(6, `direct_edit: undo in round ${lastRound} with no Build close after it`);
  }
  if (fixMode) return done(6, `round ${lastRound} is not-ready with an Issues row at Level build and no Build close after it`, { fix_mode: true });

  // State 7.
  if (waiting.size) return done(7, `waiting on open item ${facts.unanswered_open_items.join(', ')}: ${[...waiting].join(', ')}`);

  // State 8.
  if (!f.results) return done(8, 'no test-results.md');
  if (results.round_status === 'in-progress') return done(8, `round ${lastRound} is in progress${facts.round_left_behind ? ' (left behind: Test abandons it and opens the next)' : ''}`);
  if (closeAfterLastRound) return done(8, `a Build close after round ${lastRound}`);
  if (results.readiness === 'not-ready' && !buildIssues && results.direct_edit !== 'undo') {
    return done(8, `round ${lastRound} is not-ready with nothing in it for Build`);
  }

  // State 9.
  if (results.readiness === 'waiting-on-access') return done(9, `round ${lastRound} is waiting-on-access`);

  // State 10.
  if (results.readiness === 'ready' && facts.last_round_plan_revision === planRevision && results.go_live === 'pending') {
    return done(10, `round ${lastRound} is ready for plan revision ${planRevision}, with go_live: pending`, live ? { already_live: true } : {});
  }

  // State 11.
  if (live) return done(11, registryDir ? 'the node is in-production and nothing above matched' : `live since ${liveSince} and nothing above matched`);

  const err = new Unreadable('no state matched: the files are in a combination the routing rule does not cover');
  err.partial = done(null, 'no state matched');
  throw err;
}

// The last Ready round: by number among test-results.md and the finished rounds
// in history/, skipping set-aside-*/ and earlier-version-*/ (only history/'s top
// level is listed) and any round marked abandoned.
function lastReadyRound(folder, current, warnings) {
  const rounds = [];
  if (current && current.fm) rounds.push(current.fm);
  const hist = path.join(folder, 'history');
  if (isDir(hist)) {
    for (const d of listDir(hist)) {
      if (!d.isFile() || !/^test-results-round-\d+\.md$/.test(d.name)) continue;
      // Reported as a fact only; routing never depends on it, so a finished
      // round that can't be parsed is a warning, not a failure.
      try {
        const doc = readDoc(path.join(hist, d.name));
        if (doc && doc.fm) rounds.push(doc.fm);
      } catch (e) {
        if (!(e instanceof Unreadable)) throw e;
        warnings.push(`history/${d.name} skipped for the last Ready round: ${e.message}`);
      }
    }
  }
  const ready = rounds.filter((r) => r.round_status !== 'abandoned' && r.readiness === 'ready' && num(r.round) !== null);
  return ready.length ? Math.max(...ready.map((r) => num(r.round))) : null;
}

// --- "Continue my workflow" (routing.md) ------------------------------------------

function continueState(target, opts = {}) {
  target = path.resolve(target);
  if (!isDir(target)) throw new Unreadable(`can't read the folder ${target}`);
  listDir(target);
  // A workspace holding framework/ (Claude Code, Codex), or the framework
  // folder itself (a drive, Claude desktop). A workspace with no framework/
  // yet (it has .claude/) has nothing in it to continue. A drive's framework
  // folder holds registry/ itself, which is never a workflow folder.
  let frameworkDir = target;
  if (isDir(path.join(target, 'framework')) || isDir(path.join(target, '.claude'))) frameworkDir = path.join(target, 'framework');
  const registryDir = findRegistry(isDir(frameworkDir) ? frameworkDir : target, opts) ||
    (!opts.noRegistry && !opts.registry && isRegistryDir(path.join(target, 'registry')) ? path.join(target, 'registry') : null);

  const frameworkExists = isDir(frameworkDir);
  const folders = frameworkExists
    ? listDir(frameworkDir).filter((d) => d.isDirectory() && !NOT_WORKFLOW_DIRS.has(d.name) && !d.name.startsWith('.')).map((d) => d.name).sort()
    : [];
  const analyzeInProgress = frameworkExists && isFile(path.join(frameworkDir, 'analyze-in-progress.md'));

  const workflows = folders.map((slug) => workflowState(path.join(frameworkDir, slug), { ...opts, registryDir }));
  const notRetired = workflows.filter((w) => !(w.state === 0 && w.kind === 'retired'));
  const inProgress = notRetired.filter((w) => w.state !== 11);

  const nodes = registryDir ? listNodes(registryDir) : [];
  const claimed = new Set(workflows.map((w) => (w.facts.node && w.facts.node.slug) || w.workflow));
  const backlogNodes = nodes.filter((n) => n.status === 'backlog' && !folders.includes(n.slug) && !claimed.has(n.slug)).map((n) => n.slug);
  // backlog.md is the backlog only where there's no registry: once a registry
  // exists, its backlog nodes are the backlog, and Analyze offers to register
  // what backlog.md still lists (Deconstruct's backlog choice reads only nodes).
  const backlogFile = frameworkExists && !registryDir ? readTextIfFile(path.join(frameworkDir, 'backlog.md')) : null;
  const backlogFileEntries = backlogFile ? (backlogFile.match(/^\s*(?:\d+\.|[-*])\s+\S/gm) || []).length : 0;

  const facts = {
    framework_folder: frameworkExists ? frameworkDir : null,
    registry: registryDir,
    analyze_in_progress: analyzeInProgress,
    workflows: workflows.map((w) => ({ workflow: w.workflow, state: w.state, name: w.name, owner: w.owner, kind: w.kind })),
    retired: workflows.filter((w) => w.state === 0 && w.kind === 'retired').map((w) => w.workflow),
    in_progress: inProgress.map((w) => w.workflow),
    backlog_nodes: backlogNodes,
    backlog_md_entries: backlogFileEntries,
    ...(registryDir && frameworkExists && isFile(path.join(frameworkDir, 'backlog.md')) ? { backlog_md_beside_registry: true } : {}),
  };
  const option = (w) => ({ workflow: w.workflow, state: w.state, name: w.name, owner: w.owner });

  if (analyzeInProgress) {
    if (!notRetired.length) return { continue: 'analyze', owner: 'Analyze', reason: 'analyze-in-progress.md and no workflow that is not retired has a folder', facts };
    return {
      continue: 'ask', line: 'N-F9', owner: null,
      options: [...notRetired.map(option), { workflow: 'analyze', owner: 'Analyze', name: 'unfinished Analyze session' }],
      reason: 'analyze-in-progress.md beside workflows with a folder',
      facts,
    };
  }
  if (inProgress.length === 1) {
    const w = inProgress[0];
    return { continue: 'pick', workflow: w.workflow, state: w.state, name: w.name, owner: w.owner, reason: 'the only workflow in progress', result: w, facts };
  }
  if (!inProgress.length && notRetired.length === 1) {
    const w = notRetired[0];
    return { continue: 'pick', workflow: w.workflow, state: w.state, name: w.name, owner: w.owner, line: w.state === 11 ? 'N-T19' : undefined, reason: 'none in progress and only one workflow', result: w, facts };
  }
  if (inProgress.length > 1 || notRetired.length > 1) {
    const list = inProgress.length > 1 ? inProgress : notRetired;
    return { continue: 'ask', line: 'N-F9', owner: null, options: list.map(option), reason: inProgress.length > 1 ? 'several workflows in progress' : 'none in progress and several workflows', facts };
  }
  if (backlogNodes.length || backlogFileEntries) {
    return { continue: 'deconstruct-start-phrase', owner: 'Deconstruct', reason: 'no workflow folder that is not retired, but backlog candidates', facts };
  }
  return { continue: 'nothing', owner: 'Analyze', reason: 'nothing to continue yet', facts };
}

// --- Output -----------------------------------------------------------------------

// The skills call the default output; its last line keeps the model from narrating it.
const MODEL_NOTE = 'Note for you, not the leader: write no text about this output, the script or the rule. Your next text is a line for the leader.';

function lineFor(r) {
  if (r.continue) {
    switch (r.continue) {
      case 'analyze': return 'continue: the unfinished Analyze session; Analyze resumes it.';
      case 'ask': return `continue: ask which (N-F9): ${r.options.map((o) => o.workflow === 'analyze' ? 'the unfinished Analyze session' : `${o.workflow} (state ${o.state}, ${o.name})`).join(', ')}.`;
      case 'pick': return `continue: ${r.workflow}, state ${r.state} (${r.name}); ${r.state === 11 ? 'say N-T19' : `${r.owner}: "${START_PHRASES[r.owner]}"`}.`;
      case 'deconstruct-start-phrase': return `continue: no workflow folder yet, but backlog candidates; Deconstruct: "${START_PHRASES.Deconstruct}".`;
      default: return `continue: nothing to continue yet; Analyze: "${START_PHRASES.Analyze}".`;
    }
  }
  const owner = r.owner ? `${r.owner}: "${START_PHRASES[r.owner]}"` : 'no owner';
  const extra = r.state === 1 ? (r.n_b44 ? '; the owner asks N-B44 first' : '; no N-B44') : '';
  return `${r.workflow}: state ${r.state} (${r.name}), ${owner}${extra}. Because ${r.reason}.`;
}

function main(argv) {
  const opts = {};
  const pos = [];
  let mode = 'workflow';
  let out = 'both';
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--continue') mode = 'continue';
    else if (a === '--registry') opts.registry = argv[++i];
    else if (a === '--no-registry') opts.noRegistry = true;
    else if (a === '--json') out = 'json';
    else if (a === '--line') out = 'line';
    else if (a === '-h' || a === '--help') { const src = fs.readFileSync(__filename, 'utf8').split('\n'); const from = src.findIndex((l) => l === '// Usage:'); const to = src.findIndex((l) => l === "'use strict';"); process.stdout.write(src.slice(from, to).map((l) => l.replace(/^\/\/ ?/, '')).join('\n') + '\n'); return 0; }
    else if (a.startsWith('--')) { process.stderr.write(`framework-state: unknown option ${a}\n`); return 1; }
    else pos.push(a);
  }
  if (pos.length !== 1 || (opts.registry === undefined && argv.includes('--registry'))) {
    process.stderr.write('usage: framework-state.js [--continue] [--registry <dir> | --no-registry] [--json | --line] <folder>\n');
    return 1;
  }
  try {
    const r = mode === 'continue' ? continueState(pos[0], opts) : workflowState(pos[0], opts);
    if (out !== 'json') process.stdout.write(lineFor(r) + '\n');
    if (out !== 'line') process.stdout.write(JSON.stringify(r, (k, v) => (k === 'result' ? undefined : v), 2) + '\n');
    if (out === 'both') process.stdout.write(MODEL_NOTE + '\n');
    return 0;
  } catch (e) {
    if (!(e instanceof Unreadable)) throw e;
    process.stderr.write(`framework-state: ${e.message}. Fall back to routing.md.\n`);
    if (e.partial && out !== 'line') process.stdout.write(JSON.stringify(e.partial, null, 2) + '\n');
    if (out === 'both') process.stdout.write(MODEL_NOTE + '\n');
    return 2;
  }
}

if (require.main === module) process.exitCode = main(process.argv.slice(2));

module.exports = { workflowState, continueState, parseYaml, STATE_NAMES };
