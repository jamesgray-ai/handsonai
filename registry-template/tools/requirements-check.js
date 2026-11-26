#!/usr/bin/env node
// registry-template/tools/requirements-check.js
// Check a workflow's requirements.md against Deconstruct's requirements
// template (AI Workflow Framework 11.0.0). Deconstruct runs it before it saves
// the file; Design runs it on entry. Deconstruct's self-check is its
// specification and its written fallback, so every check here has a line there.
//
// Usage: node tools/requirements-check.js <requirements.md | workflow folder>
//          [--registry | --no-registry]   (default: look for registry/SCHEMA.md above the folder)
//          [--before-save]                (Deconstruct's pre-save run: big_change is never allowed)
// Exit 0 valid; exit 1 invalid; exit 2 on a usage error or an unreadable file.
// Each problem names the section and the line. A note (printed, exit unchanged)
// names a practice input whose `tests:` still lists a line a `revisions:` entry
// records and the file no longer has: a removed line, which Test or Design takes
// out of the header (a problem under --before-save). Zero npm dependencies.
// A byte-for-byte copy ships at plugins/handsonai/tools/requirements-check.js.
'use strict';
const fs = require('fs');
const path = require('path');

const SECTIONS = [
  'Goal', 'Value & Measurement', 'Metadata', 'Path', 'Inputs', 'Context Inventory',
  'Acceptance Criteria', 'Example Scenarios', 'Rules & Constraints', 'Human Gates',
  'Security, Privacy & Safety',
];
// 11.0 (shape release): an optional ## Output after the Goal. A file with it is checked as 11.0;
// a file without it is a 10.x file, checked on the old rules, unless --before-save (a file
// Deconstruct is about to save is always 11.0).
const ALL_SECTIONS = ['Goal', 'Output', ...SECTIONS.slice(1)];
const OUTPUT_LINES = ['What', 'For', 'Form', 'Voice', 'Structure', 'Delivered as'];
const AC_INTRO_11 = "Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line.";
const FM_KEYS = ['revision', 'revisions', 'track', 'big_change'];
const METHOD_PREFS = ['same way every time', 'AI works it out each time', 'some of each'];
const PATH_PROPOSED = 'Path: proposed by AI';
const PATH_NONE = 'Path: none — the AI plans each run from the goal';
const AI_PLANS = '- The AI plans this part';
const VALUE_ROWS = ['Business Objective', 'Desired Outcome', 'Measure', 'Baseline', 'Target'];
const META_ROWS = ['Workflow Name', 'Description', 'Trigger', 'Owner', 'Lens'];
const META_OPTIONAL = ['Starts', 'Per run', 'Stakeholders', 'Runs today', 'Remembers'];
// The rows' one order, required and optional together (deconstruct 12.2): a Starts row sits
// right after Trigger, so ordering required rows before optional ones would fail it.
const META_ORDER = ['Workflow Name', 'Description', 'Trigger', 'Starts', 'Per run', 'Owner', 'Lens', 'Stakeholders', 'Runs today', 'Remembers'];
const STARTS_FORMS = /^(you|you, when \S.*|schedule: \S.*|event: \S.*? · checked \S.*)$/;
const PER_RUN_FORMS = /^(one \S.*|a batch of \S.*)$/;
const SETTLED_BY = ['a rule on a value', 'your criteria', 'open judgment'];
// A decision line, with `settled by:` anchored to its three values so a following tag can't be
// swallowed into it, then the optional `· criteria:` tag, then the optional `· value read by AI`.
const DECISION = /^- D(\d+)(?: \(Step (\d+)\))?: (.+?) · settled by: (a rule on a value|your criteria|open judgment)(?: · criteria:(.*?))?( · value read by AI)?$/;
const DECISION_LOOSE = /^- D(\d+)(?: \(Step (\d+)\))?: (.+?) · settled by: (.+)$/;
const POLICY_VALUES = /^(Allowed|No — \S.* left out|No — details removed first \((Step (\d+)|R(\d+))\)|No — not live until approved|Not sure — to check)$/;
const POLICY_TOKEN = 'Policy check'; // Test's confirmation names no ID: `lines: [Policy check]` (rules 6.2)
const AFTER_EACH_RUN = 'after each run'; // a flag sent to the leader after each run, allowed with steps
// The plain glosses (deconstruct 12.2): optional, fixed text, the first line under their heading.
const GLOSSES = {
  'Context Inventory': '*The sources it uses, what we call its context.*',
  'Example Scenarios': "*The practice runs: each input it's tested on, and what should happen.*",
  'Rules & Constraints': '*Its rules: what it always does, never does, and does when something happens.*',
  'Human Gates': '*The checkpoints: where a person checks or approves the work.*',
};
const CTX_HEADER = ['ID', 'Artifact', 'Used By', 'Status', 'Sensitivity', 'Provenance', 'AI Accessible', 'Location / Source', 'Key Contents'];
const EX_HEADER = ['ID', 'Scenario', 'Input', 'What to look for in the output', 'Golden Example'];
const RULES_HEADER = ['ID', 'Kind', 'Rule'];
const GATES_HEADER = ['ID', 'Where', 'Checkpoint'];
const SEC_HEADER = ['ID', 'Constraint', 'Source'];
const SEC_TABLES = ['Boundaries', 'Access', 'Traceability', 'Prohibited actions'];
const AC_INTRO = "Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.";
const NO_GATES = 'No human gates — the workflow runs end-to-end with final review only.';
const NO_SENSITIVITY = 'No sensitivity constraints — personal data only, read-only, human-triggered.';
const ONLY_PROHIBITION = /^No sensitivity constraints beyond the prohibition(s|\(s\))? below — personal data only, read-only, human-triggered\.$/;
const ROLE_TAG = / · \([^()]+\)$/;
const STEP_REF = /^Step (\d+)$/;
const AI_PART = /^the AI's part(?: after Step (\d+))?$/;
const ID_FAMILIES = /^(AC|R|G|D|I|W|C|E|P)\d+$|^Step \d+$/;
const SECRET_PATTERNS = [
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/,
  /\bsk-[A-Za-z0-9_-]{20,}/,
  /\bAKIA[0-9A-Z]{16}\b/,
  /\bgh[pousr]_[A-Za-z0-9]{30,}/,
  /\bxox[abprs]-[A-Za-z0-9-]{10,}/,
  /\bAIza[0-9A-Za-z_-]{35}\b/,
  /\b(password|passwd|api[ _-]?key|secret|access[ _-]?token)\s*[:=]\s*["']?[^\s"'[\]<>{}]{8,}/i,
];

// ---------------------------------------------------------------- helpers

function cells(line) {
  let s = line.trim();
  if (s.startsWith('|')) s = s.slice(1);
  if (s.endsWith('|')) s = s.slice(0, -1);
  return s.split('|').map((c) => c.trim());
}
const isSeparator = (line) => /^\|(\s*:?-{3,}:?\s*\|)+\s*$/.test(line.trim());
const sameList = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
const unquote = (v) => v.replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1');

// Minimal frontmatter reader for the four keys rules 6.2 allows: scalars,
// `revisions: []`, and a block list of maps with flow lists (`lines: [AC3, R2]`).
function parseFrontmatter(lines) {
  const fm = { keys: [], values: {}, lineOf: {}, revisions: null, problems: [] };
  if (lines[0] !== '---') return { fm: null, end: 0 };
  let end = -1;
  for (let i = 1; i < lines.length; i++) if (lines[i] === '---') { end = i; break; }
  if (end === -1) return { fm: null, end: 0, unterminated: true };
  let current = null; // the revisions entry being read
  for (let i = 1; i < end; i++) {
    const line = lines[i];
    const n = i + 1;
    if (!line.trim()) continue;
    const top = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (top) {
      current = null;
      const [, key, raw] = top;
      fm.keys.push(key);
      fm.lineOf[key] = n;
      fm.values[key] = raw.trim();
      if (key === 'revisions') {
        if (raw.trim() === '[]') fm.revisions = [];
        else if (raw.trim() === '') fm.revisions = [];
        else fm.problems.push({ line: n, msg: '`revisions:` must be `[]` or a list of entries' });
      }
      continue;
    }
    const item = line.match(/^\s+-\s+([A-Za-z_]+):\s*(.*)$/);
    const field = line.match(/^\s+([A-Za-z_]+):\s*(.*)$/);
    if (item && fm.keys[fm.keys.length - 1] === 'revisions' && fm.revisions) {
      current = { line: n, fields: {} };
      fm.revisions.push(current);
      current.fields[item[1]] = item[2].trim();
    } else if (field && current) {
      current.fields[field[1]] = field[2].trim();
    } else if (/^\s+-\s*\{/.test(line) && fm.keys[fm.keys.length - 1] === 'revisions') {
      fm.problems.push({ line: n, msg: 'write each `revisions:` entry in block form: `- revision: 3`, then `by:`, `lines:` (and `plan_unaffected: true`) on their own indented lines, never as `{ … }`' });
    } else {
      fm.problems.push({ line: n, msg: `unreadable frontmatter line "${line.trim()}"` });
    }
  }
  return { fm, end };
}

function findRegistry(startDir) {
  let dir = path.resolve(startDir);
  for (let i = 0; i < 4; i++) {
    if (fs.existsSync(path.join(dir, 'registry', 'SCHEMA.md'))) return true;
    const up = path.dirname(dir);
    if (up === dir) break;
    dir = up;
  }
  return false;
}

// ---------------------------------------------------------------- check

function check(file, opts = {}) {
  const problems = [];
  const notes = []; // printed, never failing: a removed line still named in an input's tests:
  const add = (line, section, msg) => problems.push({ line, section, msg });
  const text = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
  const lines = text.split('\n');
  const folder = path.dirname(path.resolve(file));
  const hasRegistry = opts.registry === undefined ? findRegistry(path.dirname(folder)) : opts.registry;

  // ---- frontmatter (deconstruct 12.1, rules 6.2)
  const FM = 'frontmatter';
  const { fm, end: fmEnd, unterminated } = parseFrontmatter(lines);
  const revisedIds = new Set(); // every ID a revisions entry lists: added, changed or removed
  if (!fm) {
    add(1, FM, unterminated
      ? 'the frontmatter has no closing `---`'
      : 'no frontmatter: the file must open with `---`, then `revision`, `track` and `revisions` (a file with no `revision:` is an earlier version)');
  } else {
    for (const p of fm.problems) add(p.line, FM, p.msg);
    for (const k of fm.keys) {
      if (!FM_KEYS.includes(k)) add(fm.lineOf[k], FM, `unexpected key \`${k}\` (only revision, revisions, track and big_change)`);
    }
    const seen = new Set();
    for (const k of fm.keys) { if (seen.has(k)) add(fm.lineOf[k], FM, `\`${k}\` appears twice`); seen.add(k); }
    let revision = null;
    if (!('revision' in fm.values)) add(2, FM, 'no `revision:` (a file with no `revision:` is an earlier version)');
    else if (!/^[1-9]\d*$/.test(fm.values.revision)) add(fm.lineOf.revision, FM, `\`revision: ${fm.values.revision}\` must be a whole number from 1`);
    else revision = Number(fm.values.revision);
    if (!('track' in fm.values)) add(2, FM, 'no `track:` (light or full)');
    else if (!['light', 'full'].includes(fm.values.track)) add(fm.lineOf.track, FM, `\`track: ${fm.values.track}\` must be light or full`);
    if (!('revisions' in fm.values)) add(2, FM, 'no `revisions:` (`[]` at revision 1)');
    else if (fm.revisions) {
      const byRev = new Map();
      for (const r of fm.revisions) {
        const f = r.fields;
        for (const k of Object.keys(f)) {
          if (!['revision', 'by', 'lines', 'plan_unaffected'].includes(k)) add(r.line, FM, `revisions entry has unexpected key \`${k}\``);
        }
        if (!/^\d+$/.test(f.revision || '')) { add(r.line, FM, 'revisions entry has no whole-number `revision`'); continue; }
        const rv = Number(f.revision);
        if (rv < 2) add(r.line, FM, `revisions entry for revision ${rv}: entries start at revision 2 (revision 1 has none)`);
        if (revision !== null && rv > revision) add(r.line, FM, `revisions entry for revision ${rv} is above \`revision: ${revision}\``);
        if (byRev.has(rv)) add(r.line, FM, `two revisions entries for revision ${rv}`);
        byRev.set(rv, r);
        if (!['deconstruct', 'design', 'test'].includes(f.by)) add(r.line, FM, `revisions entry ${rv}: \`by\` must be deconstruct, design or test`);
        const lm = (f.lines || '').match(/^\[(.*)\]$/);
        if (!lm || !lm[1].trim()) add(r.line, FM, `revisions entry ${rv}: \`lines\` must list the IDs added, changed or removed, as [AC3, R2]`);
        else {
          for (const id of lm[1].split(',').map((s) => s.trim())) {
            if (id === POLICY_TOKEN) continue;
            revisedIds.add(id);
            if (/^(M|RF)\d+$/.test(id)) add(r.line, FM, `revisions entry ${rv} names \`${id}\`: there are no M or RF lines (a must-always or must-never line is an R line)`);
            else if (!ID_FAMILIES.test(id)) add(r.line, FM, `revisions entry ${rv} names \`${id}\`, which isn't a label in this file's families`);
          }
        }
        if ('plan_unaffected' in f) {
          if (f.plan_unaffected !== 'true') add(r.line, FM, `revisions entry ${rv}: \`plan_unaffected\` is only ever \`true\``);
          if (f.by !== 'test') add(r.line, FM, `revisions entry ${rv}: only Test's entries carry \`plan_unaffected\``);
        }
      }
      if (revision !== null) {
        for (let rv = 2; rv <= revision; rv++) {
          if (!byRev.has(rv)) add(fm.lineOf.revisions, FM, `no revisions entry for revision ${rv} (every revision above 1 has one)`);
        }
      }
    }
    if ('big_change' in fm.values) {
      const n = fm.lineOf.big_change;
      if (hasRegistry) add(n, FM, '`big_change` appears only with no registry; with a registry it is on the Workflow node');
      else if (opts.beforeSave) add(n, FM, '`big_change` is removed when the redo is saved; a saved file never holds it');
      else if (!/^.+, \d{4}-\d{2}-\d{2}$/.test(unquote(fm.values.big_change))) add(n, FM, '`big_change` must read "[reason], [YYYY-MM-DD]"');
    }
  }

  // ---- title and sections (deconstruct 12.2)
  const bodyStart = fmEnd ? fmEnd + 1 : 0;
  let title = null;
  const heads = [];
  for (let i = bodyStart; i < lines.length; i++) {
    const h1 = lines[i].match(/^# (.+)$/);
    const h2 = lines[i].match(/^## (.+?)\s*$/);
    if (h1 && !title && !heads.length) title = { line: i + 1, text: h1[1] };
    else if (h1) add(i + 1, 'title', `a second \`#\` title "${h1[1]}"; the file has one title`);
    if (h2) heads.push({ name: h2[1], index: i });
  }
  const firstContent = lines.findIndex((l, i) => i >= bodyStart && l.trim());
  if (!title) add(firstContent + 1, 'title', 'no `# [Workflow Name] — Workflow Requirements` title');
  else {
    if (!/^.+ — Workflow Requirements$/.test(title.text)) add(title.line, 'title', 'the title must read `# [Workflow Name] — Workflow Requirements`');
    if (firstContent + 1 !== title.line) add(firstContent + 1, 'title', 'text before the title; the title comes first, under the frontmatter');
  }
  const names = heads.map((h) => h.name);
  const is11 = names.includes('Output') || !!opts.beforeSave;
  const required = is11 ? ALL_SECTIONS : SECTIONS;
  for (const h of heads) {
    if (!ALL_SECTIONS.includes(h.name)) add(h.index + 1, `## ${h.name}`, `unexpected section "## ${h.name}" (exactly the twelve sections, named exactly)`);
  }
  for (const s of required) {
    const count = names.filter((n) => n === s).length;
    if (count === 0) add(heads.length ? heads[heads.length - 1].index + 1 : 1, `## ${s}`, `section "## ${s}" is missing`);
    if (count > 1) add(heads.filter((h) => h.name === s)[1].index + 1, `## ${s}`, `section "## ${s}" appears ${count} times`);
  }
  const known = heads.filter((h) => ALL_SECTIONS.includes(h.name));
  for (let i = 1; i < known.length; i++) {
    if (ALL_SECTIONS.indexOf(known[i].name) < ALL_SECTIONS.indexOf(known[i - 1].name)) {
      add(known[i].index + 1, `## ${known[i].name}`, `"## ${known[i].name}" is out of order: it comes before "## ${known[i - 1].name}" (order: ${required.join('; ')})`);
    }
  }
  const sec = {};
  heads.forEach((h, i) => {
    if (sec[h.name]) return;
    const stop = i + 1 < heads.length ? heads[i + 1].index : lines.length;
    sec[h.name] = [];
    for (let j = h.index + 1; j < stop; j++) sec[h.name].push({ n: j + 1, t: lines[j] });
  });
  for (const [name, gloss] of Object.entries(GLOSSES)) {
    const first = (sec[name] || []).find((l) => l.t.trim());
    if (!first) continue;
    const t = first.t.trim();
    if (t === gloss) sec[name] = sec[name].filter((l) => l !== first);
    else if (/^\*[^*].*\*$/.test(t)) {
      add(first.n, `## ${name}`, `the line under \`## ${name}\` is its fixed gloss, word for word: \`${gloss}\` (or no line)`);
      sec[name] = sec[name].filter((l) => l !== first);
    }
  }
  const body = (name) => (sec[name] || []).filter((l) => l.t.trim());

  // ---- whole-file sweeps: M and RF lines, absolute paths, secrets
  for (let i = bodyStart; i < lines.length; i++) {
    const t = lines[i];
    const where = sectionAt(heads, i);
    // An M or RF label in an ID position: a table's first cell, a list item, a bold label.
    const mrf = t.match(/^\|\s*((?:M|RF)\d+)\s*\|/) || t.match(/^\s*(?:\d+\.|-)\s+(?:\*\*)?((?:M|RF)\d+)\b/);
    if (mrf) add(i + 1, where, `\`${mrf[1]}\`: there are no M or RF lines; a must-always or must-never line is an R line`);
    for (const m of t.matchAll(/`([^`]+)`/g)) {
      const p = m[1];
      const absolute = /^(~|[A-Za-z]:[\\/])/.test(p) || p.startsWith('file:') || /^\/[^\s/]+\/|^\/\S*\.\w+$/.test(p);
      if (absolute) add(i + 1, where, `\`${p}\` is an absolute path; paths are relative to the workflow folder`);
      else if (/^framework\//.test(p) || /(^|\/)\.\.(\/|$)/.test(p)) add(i + 1, where, `\`${p}\` isn't relative to the workflow folder (write \`inputs/…\` or \`context/…\`)`);
    }
    if (SECRET_PATTERNS.some((re) => re.test(t))) add(i + 1, where, 'this line looks like it holds a password or key; replace it with a placeholder');
  }

  // ---- Goal
  if (sec.Goal && !body('Goal').length) add(heads.find((h) => h.name === 'Goal').index + 1, '## Goal', 'the goal is empty');
  if (sec.Output) {  // What, For, Form, Voice, Structure (a skeleton below it, or a context file), Delivered as
    const W = '## Output';
    const at = heads.find((h) => h.name === 'Output').index + 1;
    const got = body('Output').map((l) => (l.t.match(/^([A-Z][a-z]+(?: as)?):/) || [])[1]).filter(Boolean);
    for (const k of OUTPUT_LINES) if (!got.includes(k)) add(at, W, `Output: ${k}: is missing`);
    const order = got.filter((k) => OUTPUT_LINES.includes(k));
    if (order.join() !== OUTPUT_LINES.filter((k) => order.includes(k)).join()) add(at, W, `Output: the lines read ${OUTPUT_LINES.join(', ')}, in that order`);
  }

  // ---- Value & Measurement, Metadata (field tables)
  const fieldTable = (name, required, optional, rowOrder) => {
    const rows = body(name);
    if (!sec[name]) return {};
    const where = `## ${name}`;
    const out = {};
    if (!rows.length) { add(heads.find((h) => h.name === name).index + 1, where, 'the table is missing'); return out; }
    if (!sameList(cells(rows[0].t), ['Field', 'Value'])) add(rows[0].n, where, 'the table header must be `| Field | Value |`');
    if (!rows[1] || !isSeparator(rows[1].t)) add((rows[1] || rows[0]).n, where, 'the table has no `|---|---|` separator line');
    const seenRows = [];
    for (const r of rows.slice(2)) {
      if (!r.t.trim().startsWith('|')) { add(r.n, where, 'only the table belongs in this section'); continue; }
      const c = cells(r.t);
      if (c.length !== 2) { add(r.n, where, 'a row must have two cells, Field and Value'); continue; }
      if (![...required, ...optional].includes(c[0])) { add(r.n, where, `unexpected row "${c[0]}" (rows: ${[...required, ...optional].join(', ')})`); continue; }
      if (!c[1]) add(r.n, where, `"${c[0]}" has no value`);
      out[c[0]] = { v: c[1], n: r.n };
      seenRows.push(c[0]);
    }
    const order = rowOrder || [...required, ...optional];
    const ordered = seenRows.filter((x) => order.includes(x));
    for (let i = 1; i < ordered.length; i++) {
      if (order.indexOf(ordered[i]) < order.indexOf(ordered[i - 1])) add(out[ordered[i]].n, where, `row "${ordered[i]}" is out of order (rows: ${order.join(', ')})`);
    }
    for (const req of required) if (!out[req]) add(rows[0].n, where, `no "${req}" row`);
    return out;
  };
  const vm = fieldTable('Value & Measurement', VALUE_ROWS, []);
  if (vm.Baseline && !/ · (Measured|Estimated|Unknown)$/.test(vm.Baseline.v)) add(vm.Baseline.n, '## Value & Measurement', 'Baseline must end `· Measured`, `· Estimated` or `· Unknown`');
  const meta = fieldTable('Metadata', META_ROWS, META_OPTIONAL, META_ORDER);
  if (meta.Starts && meta.Starts.v && !STARTS_FORMS.test(meta.Starts.v)) add(meta.Starts.n, '## Metadata', '"Starts" must read `you`, `you, when [event]`, `schedule: [when]` or `event: [event] · checked [interval]`');
  if (meta['Per run'] && meta['Per run'].v && !PER_RUN_FORMS.test(meta['Per run'].v)) add(meta['Per run'].n, '## Metadata', '"Per run" must read `one [case]` or `a batch of [cases]`');
  if (meta.Lens && !['Individual', 'Organizational'].includes(meta.Lens.v)) add(meta.Lens.n, '## Metadata', `Lens "${meta.Lens.v}" must be Individual or Organizational`);
  if (meta.Stakeholders && meta.Lens && meta.Lens.v !== 'Organizational') add(meta.Stakeholders.n, '## Metadata', 'the Stakeholders row belongs to the Organizational lens only');
  if (title && meta['Workflow Name'] && title.text !== `${meta['Workflow Name'].v} — Workflow Requirements`) {
    add(title.line, 'title', `the title's name doesn't match Metadata's Workflow Name "${meta['Workflow Name'].v}"`);
  }

  // ---- Path (deconstruct 12.2 line formats and order)
  const P = '## Path';
  const steps = new Map(); // number -> { name, n, fixed }
  const stepRefs = []; // { num, n, where }
  const ctxRefs = []; // { id, n, where }
  const writeRefs = []; // { id, n, where }
  let pathNone = false;
  let aiPlans = 0;
  let method = null;
  const decisions = new Set();
  if (sec.Path) {
    const rows = body('Path');
    let i = 0;
    if (!rows.length || !rows[0].t.startsWith('Method preference:')) {
      add(rows.length ? rows[0].n : heads.find((h) => h.name === 'Path').index + 1, P, '`## Path` must open with the `Method preference:` line');
    } else {
      method = rows[0].t.replace(/^Method preference:\s*/, '').trim();
      if (!METHOD_PREFS.includes(method)) add(rows[0].n, P, `\`Method preference: ${method}\` must be one of: ${METHOD_PREFS.join('; ')}`);
      i = 1;
    }
    if (rows[i] && rows[i].t.startsWith('Path:')) {
      if (rows[i].t === PATH_NONE) pathNone = true;
      else if (rows[i].t !== PATH_PROPOSED) add(rows[i].n, P, `unknown \`Path:\` line; it is \`${PATH_PROPOSED}\` or \`${PATH_NONE}\``);
      i++;
    }
    let phase = 'steps';
    let detailStep = null;
    for (; i < rows.length; i++) {
      const { n, t } = rows[i];
      if (t.startsWith('Method preference:')) { add(n, P, 'the `Method preference:` line comes first in `## Path`, once'); continue; }
      if (t.startsWith('Path:')) { add(n, P, 'the `Path:` line comes straight after the `Method preference:` line'); continue; }
      if (t.startsWith('### ')) {
        if (t === '### Decisions') {
          if (phase !== 'steps') add(n, P, '`### Decisions` comes after the step lines and before the step detail blocks');
          phase = 'decisions';
          continue;
        }
        const dm = t.match(/^### Step (\d+) — (.+)$/);
        if (dm) {
          phase = 'detail';
          detailStep = Number(dm[1]);
          const s = steps.get(detailStep);
          if (!s) add(n, P, `detail block "Step ${detailStep}" has no matching step line`);
          else if (s.name !== dm[2]) add(n, P, `detail block's name "${dm[2]}" doesn't match Step ${detailStep}'s name "${s.name}"`);
          continue;
        }
        add(n, P, `unexpected heading "${t}" (only \`### Decisions\` and \`### Step N — [Name]\` detail blocks)`);
        continue;
      }
      if (phase === 'steps') {
        if (t === AI_PLANS) { aiPlans++; if (pathNone) add(n, P, '`Path: none` has no step lines and no `The AI plans this part` lines'); continue; }
        if (/^- Step \d+/.test(t)) {
          if (pathNone) add(n, P, '`Path: none` has no step lines');
          checkStepLine(t, n, steps, stepRefs, ctxRefs, writeRefs, add);
          continue;
        }
        add(n, P, 'expected a step line (`- Step N — [Name] · produces …`) or `- The AI plans this part`');
      } else if (phase === 'decisions') {
        const d = t.match(DECISION);
        const loose = d ? null : t.match(DECISION_LOOSE);
        if (!d && !loose) { add(n, P, 'decision lines read `- D1 (Step 3): When [condition], it [path] · settled by: …`'); continue; }
        const [, dn, dstep, dtext] = d || loose;
        if (decisions.has(dn)) add(n, P, `D${dn} is used twice`);
        decisions.add(dn);
        if (dstep) stepRefs.push({ num: Number(dstep), n, where: P });
        if (!/^When .+?, it /.test(dtext)) add(n, P, `D${dn} isn't in the "When…, it…" shape`);
        if (loose) {
          if (!SETTLED_BY.some((v) => loose[4].startsWith(`${v} · `))) add(n, P, `D${dn}: \`settled by:\` must be a rule on a value, your criteria or open judgment`);
          else add(n, P, `D${dn}: after \`settled by:\`, only \`· criteria: [the leader's words]\`, then \`· value read by AI\`, in that order`);
        } else if (d[5] !== undefined) {
          const crit = d[5];
          if (!crit.trim()) add(n, P, `D${dn}: \`· criteria:\` has no text`);
          else if (!/^ \S/.test(crit)) add(n, P, `D${dn}: write \`· criteria: [the leader's words]\`, one space after the colon`);
          else if (crit.includes(' · ')) add(n, P, `D${dn}: the criteria text can't contain " · " (the tag separator); reword it`);
        }
      } else if (phase === 'detail') {
        if (!/^\*\*[^*]+:\*\* \S/.test(t)) add(n, P, `detail block for Step ${detailStep}: each line is one bold-labelled field (\`**Rule:** …\`)`);
      }
    }
    if (!pathNone && steps.size === 0 && aiPlans === 0 && method) add(rows[0].n, P, 'no step lines: write the steps, or `Path: none — the AI plans each run from the goal`');
    if (method === 'some of each' && !pathNone) {
      const fixed = [...steps.values()].some((s) => s.fixed);
      if (!fixed || !aiPlans) add(rows[0].n, P, '"some of each" needs at least one fixed step and at least one `- The AI plans this part` line');
    }
  }

  // ---- Inputs
  const ctxIds = new Map();
  const inputIds = new Set();
  if (sec.Inputs) {
    const seen = inputIds;
    for (const { n, t } of body('Inputs')) {
      const m = t.match(/^- I(\d+) · (.+?) · from (.+?) · Status: (.+)$/);
      if (!m) { add(n, '## Inputs', 'input lines read `- I1 · [what comes in] · from [source or C#] · Status: available`'); continue; }
      if (seen.has(m[1])) add(n, '## Inputs', `I${m[1]} is used twice`);
      seen.add(m[1]);
      if (!['available', 'not available yet', 'Not sure — to check'].includes(m[4])) add(n, '## Inputs', `I${m[1]}: Status must be available, not available yet or Not sure — to check`);
      for (const c of m[3].matchAll(/\bC(\d+)\b/g)) ctxRefs.push({ id: `C${c[1]}`, n, where: '## Inputs' });
    }
  }

  // ---- Context Inventory
  const sensitivity = new Set();
  const provenance = new Set();
  if (sec['Context Inventory']) {
    const W = '## Context Inventory';
    const rows = body('Context Inventory');
    if (!(rows.length === 1 && rows[0].t === 'None')) {
      tableRows(rows, CTX_HEADER, W, add, (c, n) => {
        const id = c[0].match(/^C(\d+)$/);
        if (!id) { add(n, W, `"${c[0]}" isn't a context ID (C1, C2…)`); return; }
        if (ctxIds.has(c[0])) add(n, W, `${c[0]} is used twice`);
        ctxIds.set(c[0], n);
        for (const u of c[2].split(',').map((s) => s.trim())) {
          const sm = u.match(STEP_REF);
          const am = u.match(AI_PART);
          if (sm) stepRefs.push({ num: Number(sm[1]), n, where: W });
          else if (am) { if (am[1]) stepRefs.push({ num: Number(am[1]), n, where: W }); }
          else if (u !== 'All' && u !== '—') add(n, W, `${c[0]}: Used By "${u}" must name \`Step N\`, the AI's part, All or —`);
        }
        if (!['Exists', 'Needs Creation'].includes(c[3])) add(n, W, `${c[0]}: Status must be Exists or Needs Creation`);
        if (!['Public', 'Internal', 'Confidential', 'Regulated'].includes(c[4])) add(n, W, `${c[0]}: Sensitivity must be Public, Internal, Confidential or Regulated`);
        else sensitivity.add(c[4]);
        if (!['Authored', 'External'].includes(c[5])) add(n, W, `${c[0]}: Provenance must be Authored or External`);
        else provenance.add(c[5]);
        if (!['Yes', 'Partial', 'No'].includes(c[6])) add(n, W, `${c[0]}: AI Accessible must be Yes, Partial or No`);
        const loc = c[7].match(/`([^`]+)`/);
        if (loc && !loc[1].startsWith('context/') && !/^[a-z]+:\/\//.test(loc[1])) add(n, W, `${c[0]}: a file's location is \`context/${c[0]}-[short-name].md\``);
        if (loc && loc[1].startsWith('context/') && !new RegExp(`^context/${c[0]}-[a-z0-9]+(-[a-z0-9]+)*\\.md$`).test(loc[1])) add(n, W, `${c[0]}: the file is named \`context/${c[0]}-[short-name].md\` in kebab-case`);
        if (c[3] === 'Needs Creation' && !/^Create as `context\//.test(c[7])) add(n, W, `${c[0]}: a Needs Creation item's location reads "Create as \`context/${c[0]}-[short-name].md\`"`);
        if (!c[1]) add(n, W, `${c[0]}: Artifact is empty`);
      });
    }
  }

  // ---- Acceptance Criteria
  const acIds = new Set();
  const acFrom = []; // { ac, id, n }: 11.0's `· from:` sources, checked once Rules are read
  if (sec['Acceptance Criteria']) {
    const W = '## Acceptance Criteria';
    let refLine = null;
    for (const { n, t } of body('Acceptance Criteria')) {
      if (t === AC_INTRO || (is11 && t === AC_INTRO_11)) continue;
      const rm = t.match(/^Reference example: (.+)$/);
      if (rm) {
        refLine = n;
        if (rm[1] !== '—') { if (/^C\d+$/.test(rm[1])) ctxRefs.push({ id: rm[1], n, where: W }); else add(n, W, '`Reference example:` names one C# or "—"'); }
        continue;
      }
      const m = t.match(/^\d+\. \*\*AC(\d+)( \(must\))?\*\* — (\S.*)$/);
      if (!m) { add(n, W, is11 ? 'acceptance criteria read `1. **AC1** — [yes-or-no statement] · from: [I#, C#, R# | the output alone]`' : 'acceptance criteria read `1. **AC1 (must)** — [yes-or-no statement]`'); continue; }
      if (is11) {
        if (m[2]) add(n, W, `AC${m[1]}: no (must) in this format; every check is required`);
        const fm = m[3].match(/ · from: (.+)$/);
        if (!fm) add(n, W, `AC${m[1]}: add "· from:" naming where its information comes from (I#, C#, R#) or "the output alone"`);
        else if (fm[1] !== 'the output alone') {
          for (const id of fm[1].split(',').map((x) => x.trim())) {
            if (/^(I|C|R)\d+$/.test(id)) acFrom.push({ ac: `AC${m[1]}`, id, n });
            else add(n, W, `AC${m[1]}: from names "${id}"; use I#, C#, R# or "the output alone"`);
          }
        }
      }
      if (refLine) add(n, W, '`Reference example:` comes after the AC lines');
      if (acIds.has(`AC${m[1]}`)) add(n, W, `AC${m[1]} is used twice`);
      acIds.add(`AC${m[1]}`);
    }
    if (!acIds.size) add(heads.find((h) => h.name === 'Acceptance Criteria').index + 1, W, 'no acceptance criteria: at least one AC line');
    if (!refLine) add(heads.find((h) => h.name === 'Acceptance Criteria').index + 1, W, 'no `Reference example:` line (C# or "—")');
  }

  // ---- Rules & Constraints
  const rIds = new Set();
  if (sec['Rules & Constraints']) {
    const W = '## Rules & Constraints';
    tableRows(body('Rules & Constraints'), RULES_HEADER, W, add, (c, n) => {
      const id = c[0].match(/^R(\d+)$/);
      if (!id) { add(n, W, `"${c[0]}" isn't a rule ID (R1, R2…)`); return; }
      if (rIds.has(c[0])) add(n, W, `${c[0]} is used twice`);
      rIds.add(c[0]);
      const ruleText = c[2].replace(ROLE_TAG, '');
      const shapes = { Always: /^It always /, Never: /^It never /, When: /^When .+?, \S/, Fallback: /^When .+?, \S/ };
      if (!shapes[c[1]]) add(n, W, `${c[0]}: Kind "${c[1]}" must be Always, Never, When or Fallback`);
      else if (!shapes[c[1]].test(ruleText)) {
        const want = { Always: '"It always…"', Never: '"It never…"', When: '"When…, it…"', Fallback: '"When…, it…"' }[c[1]];
        add(n, W, `${c[0]}: a ${c[1]} rule reads ${want}`);
      }
    });
  }

  // ---- Example Scenarios (and the practice inputs they list)
  const gIds = new Set();
  const inputChecks = [];
  if (sec['Example Scenarios']) {
    const W = '## Example Scenarios';
    let count = 0;
    const eSeen = new Set();
    tableRows(body('Example Scenarios'), EX_HEADER, W, add, (c, n) => {
      const id = c[0].match(/^E(\d+)$/);
      if (!id) { add(n, W, `"${c[0]}" isn't a practice-input ID (E1, E2…)`); return; }
      count++;
      if (eSeen.has(c[0])) add(n, W, `${c[0]} is used twice`);
      eSeen.add(c[0]);
      if (is11 ? !/\((real|made up)\)$/.test(c[1]) : !/\((real|proposed)(, hard)?\)$/.test(c[1])) {
        add(n, W, is11 ? `${c[0]}: Scenario ends "(real)" or "(made up)"` : `${c[0]}: Scenario ends "(real)" or "(proposed)", with ", hard" where it is`);
      }
      const im = c[2].match(/^`([^`]+)` — \S/);
      if (is11 && /^Test writes it — \S/.test(c[2])) { /* 11.0: Test writes the practice input; no file yet */ }
      else if (!im) { add(n, W, `${c[0]}: Input reads \`inputs/${c[0]}-[short-name].md\` — [description], path first`); }
      else if (!new RegExp(`^inputs/${c[0]}-[a-z0-9]+(-[a-z0-9]+)*\\.md$`).test(im[1])) {
        add(n, W, `${c[0]}: the input's path must be \`inputs/${c[0]}-[short-name].md\` (relative to the workflow folder, kebab-case)`);
      } else inputChecks.push({ id: c[0], rel: im[1], n });
      if (c[4] !== '—') { if (/^C\d+$/.test(c[4])) ctxRefs.push({ id: c[4], n, where: W }); else add(n, W, `${c[0]}: Golden Example is one C# (a real output) or "—"`); }
    });
    if (!count) add(heads.find((h) => h.name === 'Example Scenarios').index + 1, W, 'no practice inputs: at least one E line');
  }

  // ---- Human Gates
  let runsWithout = false;
  if (sec['Human Gates']) {
    const W = '## Human Gates';
    const rows = body('Human Gates');
    if (!rows.length || !/^Runs: with(out)? you$/.test(rows[0].t)) {
      add(rows.length ? rows[0].n : heads.find((h) => h.name === 'Human Gates').index + 1, W, 'Human Gates opens with `Runs: with you` or `Runs: without you`');
    } else runsWithout = rows[0].t === 'Runs: without you';
    const rest = rows.slice(rows.length && rows[0].t.startsWith('Runs:') ? 1 : 0);
    if (rest.length === 1 && rest[0].t === NO_GATES) { /* none */ } else if (!rest.length) {
      add(rows.length ? rows[0].n : 1, W, `no checkpoints table and no "${NO_GATES}" line`);
    } else {
      tableRows(rest, GATES_HEADER, W, add, (c, n) => {
        const id = c[0].match(/^G(\d+)$/);
        if (!id) { add(n, W, `"${c[0]}" isn't a checkpoint ID (G1, G2…)`); return; }
        if (gIds.has(c[0])) add(n, W, `${c[0]} is used twice`);
        gIds.add(c[0]);
        const sm = c[1].match(STEP_REF);
        const am = c[1].match(AI_PART);
        if (sm) stepRefs.push({ num: Number(sm[1]), n, where: W });
        else if (am) { if (am[1]) stepRefs.push({ num: Number(am[1]), n, where: W }); }
        else if (steps.size) add(n, W, `${c[0]}: Where names \`Step N\` or the AI's part ("the AI's part after Step 2")`);
        else if (!c[1]) add(n, W, `${c[0]}: Where is empty`);
        if (!ROLE_TAG.test(c[2])) add(n, W, `${c[0]}: a checkpoint ends with the role tag of who performs it (\`· (you)\`)`);
        if (!/^When .+?, it /.test(c[2].replace(ROLE_TAG, ''))) add(n, W, `${c[0]} isn't in the "When…, it…" shape`);
      });
    }
  }

  // ---- Security, Privacy & Safety
  const writes = new Set();
  if (sec['Security, Privacy & Safety']) {
    const W = '## Security, Privacy & Safety';
    const rows = body('Security, Privacy & Safety');
    const pIds = new Map();
    const worked = [];
    let lastTable = -1;
    let regime = null;
    let policy = null;
    let writesAt = null;
    let oneLine = null;
    let i = 0;
    if (rows[i] && /^\*Scope: .+\*$/.test(rows[i].t)) i++;
    if (rows[i] && (rows[i].t === NO_SENSITIVITY || ONLY_PROHIBITION.test(rows[i].t))) { oneLine = rows[i]; i++; }
    let current = null;
    let tableBuf = [];
    const flush = () => {
      if (!current) return;
      const name = current.name;
      const W2 = `${W} › ### ${name}`;
      if (!tableBuf.length) add(current.n, W2, 'the table is missing');
      tableRows(tableBuf, SEC_HEADER, W2, add, (c, n) => {
        const id = c[0].match(/^P(\d+)$/);
        if (!id) { add(n, W2, `"${c[0]}" isn't a constraint ID: every constraint has a \`P\` ID (P1, P2…), one series across the four tables`); return; }
        if (pIds.has(c[0])) add(n, W2, `${c[0]} is used twice (P IDs run in one series across ${SEC_TABLES.join(', ')}; ${c[0]} is first at line ${pIds.get(c[0])})`);
        else pIds.set(c[0], n);
        if (!c[1]) add(n, W2, `${c[0]}: Constraint is empty`);
        if (!c[2]) add(n, W2, `${c[0]}: no Source (a person, policy, control ID, or \`Self\`)`);
      });
      current = null;
      tableBuf = [];
    };
    for (; i < rows.length; i++) {
      const { n, t } = rows[i];
      const hm = t.match(/^### (.+)$/);
      if (hm) {
        flush();
        if (hm[1] === 'Writes') { writesAt = n; i++; break; }
        const idx = SEC_TABLES.indexOf(hm[1]);
        if (idx === -1) { add(n, W, `unexpected heading "${t}" (Boundaries, Access, Traceability, Prohibited actions, then Writes)`); continue; }
        if (regime) add(n, W, `"### ${hm[1]}" comes before the \`Governing regime:\` line`);
        if (idx <= lastTable) add(n, W, `"### ${hm[1]}" is out of order (${SEC_TABLES.join(', ')})`);
        lastTable = idx;
        worked.push(hm[1]);
        current = { name: hm[1], n };
        continue;
      }
      if (t.startsWith('Governing regime:')) {
        flush();
        if (regime) add(n, W, 'a second `Governing regime:` line');
        regime = { n, v: t.replace(/^Governing regime:\s*/, '').trim() };
        if (!regime.v) add(n, W, '`Governing regime:` names the regime, None, or Not sure — to check');
        continue;
      }
      if (t.startsWith('Policy check:')) {
        flush();
        if (policy) { add(n, W, 'a second `Policy check:` line (it appears once)'); continue; }
        policy = { n, v: t.replace(/^Policy check:\s*/, '').trim() };
        if (!regime) add(n, W, 'the `Policy check:` line comes after the `Governing regime:` line');
        const pm = policy.v.match(POLICY_VALUES);
        if (!pm) add(n, W, '`Policy check:` reads Allowed; No — [source] left out; No — details removed first (Step N) or (R n), as `(Step 2)` or `(R4)`; No — not live until approved; or Not sure — to check');
        else if (pm[3]) stepRefs.push({ num: Number(pm[3]), n, where: W });
        else if (pm[4] && !rIds.has(`R${pm[4]}`)) add(n, W, `\`Policy check:\` names R${pm[4]}, which isn't in Rules & Constraints`);
        continue;
      }
      if (current) { tableBuf.push(rows[i]); continue; }
      add(n, W, t.startsWith('*Scope:') ? 'the `*Scope:*` line comes first' : 'unexpected line (a constraint table, `Governing regime:`, `Policy check:` or `### Writes`)');
    }
    flush();
    const secHead = heads.find((h) => h.name === 'Security, Privacy & Safety').index + 1;
    if (!regime) add(secHead, W, 'no `Governing regime:` line (it comes before `### Writes`)');
    if (!writesAt) add(secHead, W, 'no `### Writes` heading (W lines, or `None`)');
    else {
      const wrows = rows.slice(i);
      if (!wrows.length) add(writesAt, `${W} › ### Writes`, 'no W lines and no `None`');
      else if (!(wrows.length === 1 && wrows[0].t === 'None')) {
        for (const { n, t } of wrows) {
          const m = t.match(/^- W(\d+) · (.+?) · (.+?) · (.+)$/);
          if (/^Policy check:/.test(t)) { add(n, `${W} › ### Writes`, 'the `Policy check:` line comes before `### Writes`, right after `Governing regime:`'); continue; }
          if (!m) { add(n, `${W} › ### Writes`, 'write lines read `- W1 · [system] · [action] · Step 3` (or `· after each run`; `· after [moment]` with no steps)'); continue; }
          if (writes.has(`W${m[1]}`)) add(n, `${W} › ### Writes`, `W${m[1]} is used twice`);
          writes.add(`W${m[1]}`);
          const sm = m[4].match(STEP_REF);
          if (sm) stepRefs.push({ num: Number(sm[1]), n, where: `${W} › ### Writes` });
          else if (m[4] === AFTER_EACH_RUN) { /* a flag after each run: allowed with or without steps */ }
          else if (!/^after .+/.test(m[4])) add(n, `${W} › ### Writes`, `W${m[1]} ends with \`Step N\`, \`after each run\` or \`after [moment]\``);
          else if (steps.size) add(n, `${W} › ### Writes`, `W${m[1]}: name the step that writes (\`Step N\`); \`after [moment]\` is for a path with no steps (a flag sent after every run reads \`after each run\`)`);
        }
      }
    }
    // Which categories are worked is derived (deconstruct 12.2), never asked again.
    const need = new Map();
    const want = (cat, why) => { if (!need.has(cat)) need.set(cat, why); };
    if (writes.size || runsWithout) { want('Prohibited actions', writes.size ? 'it writes to a live system' : 'it runs without you'); want('Traceability', writes.size ? 'it writes to a live system' : 'it runs without you'); }
    if (provenance.has('External')) { want('Boundaries', 'a Context Inventory row is External'); want('Prohibited actions', 'a Context Inventory row is External'); }
    if (sensitivity.has('Confidential')) { want('Boundaries', 'a Context Inventory row is Confidential'); want('Access', 'a Context Inventory row is Confidential'); }
    if (sensitivity.has('Regulated')) {
      want('Boundaries', 'a Context Inventory row is Regulated'); want('Access', 'a Context Inventory row is Regulated');
      if (regime && /^None$/i.test(regime.v)) add(regime.n, W, '`Governing regime:` names the regime, or `Not sure — to check`, when a row is Regulated');
    }
    for (const [cat, why] of need) {
      if (!worked.includes(cat)) add(secHead, W, `"### ${cat}" must be worked because ${why}`);
    }
    if (oneLine) {
      if (oneLine.t === NO_SENSITIVITY && worked.length) add(oneLine.n, W, 'the "No sensitivity constraints" line stands alone; with constraint tables, drop it');
      if (ONLY_PROHIBITION.test(oneLine.t) && !worked.includes('Prohibited actions')) add(oneLine.n, W, 'the line names a prohibition below, but there is no `### Prohibited actions` table');
      if (ONLY_PROHIBITION.test(oneLine.t) && worked.some((w) => w !== 'Prohibited actions')) add(oneLine.n, W, 'with other categories worked, the "beyond the prohibition" line doesn\'t apply');
      if (need.size) add(oneLine.n, W, `"No sensitivity constraints" doesn't apply: ${[...need.values()][0]}`);
    } else if (!worked.length) add(secHead, W, `no constraint tables: with nothing tripped, the section reads "${NO_SENSITIVITY}"`);
  }

  // ---- cross-references
  for (const r of stepRefs) {
    if (!steps.has(r.num)) add(r.n, r.where, `"Step ${r.num}" matches no step line in ## Path`);
  }
  for (const r of ctxRefs) {
    if (!ctxIds.has(r.id)) add(r.n, r.where, `${r.id} isn't in the Context Inventory`);
  }
  for (const f of acFrom) {
    const [has, where] = f.id[0] === 'I' ? [inputIds.has(f.id.slice(1)), 'Inputs']
      : f.id[0] === 'C' ? [ctxIds.has(f.id), 'the Context Inventory'] : [rIds.has(f.id), 'Rules & Constraints'];
    if (!has) add(f.n, '## Acceptance Criteria', `${f.ac}: from names ${f.id}, which isn't in ${where}`);
  }
  for (const r of writeRefs) {
    if (!writes.has(r.id)) add(r.n, r.where, `${r.id} isn't under ### Writes`);
  }

  // ---- practice inputs on disk: header lines, tests IDs, no secrets
  const allIds = new Set([...acIds, ...rIds, ...gIds, ...[...decisions].map((d) => `D${d}`)]);
  for (const ic of inputChecks) {
    const W = '## Example Scenarios';
    const abs = path.join(folder, ic.rel);
    if (!fs.existsSync(abs)) { add(ic.n, W, `${ic.id}: \`${ic.rel}\` doesn't exist in the workflow folder`); continue; }
    const il = fs.readFileSync(abs, 'utf8').replace(/\r\n/g, '\n').split('\n');
    if (!/^source: \S+/.test(il[0] || '')) add(ic.n, W, `${ic.id}: \`${ic.rel}\` line 1 must be the \`source:\` header`);
    const tm = (il[1] || '').match(/^tests: (.+)$/);
    if (!tm) add(ic.n, W, `${ic.id}: \`${ic.rel}\` line 2 must be the \`tests:\` header (the AC, R, G and D lines it exercises)`);
    else {
      for (const id of tm[1].split(',').map((s) => s.trim())) {
        if (!/^(AC|R|G|D)\d+$/.test(id)) add(ic.n, W, `${ic.id}: \`${ic.rel}\` tests "${id}"; \`tests:\` names AC, R, G and D lines only`);
        else if (!allIds.has(id) && revisedIds.has(id) && !opts.beforeSave) {
          notes.push({ line: ic.n, section: W, msg: `${ic.id}: \`${ic.rel}\` tests ${id}, a line a revision removed; take ${id} out of its \`tests:\` header` });
        } else if (!allIds.has(id)) add(ic.n, W, `${ic.id}: \`${ic.rel}\` tests ${id}, which isn't in the file`);
      }
    }
    // An optional third header line, `expect:` (R-D9): then the blank line is line 4 and the
    // input starts at line 5. Required on Deconstruct's own inputs when it saves.
    const hasExpect = /^expect:/.test(il[2] || '');
    if (hasExpect && !/^expect: \S/.test(il[2])) add(ic.n, W, `${ic.id}: \`${ic.rel}\` line 3, \`expect:\`, is empty: it says what should happen, in plain words`);
    if (!hasExpect && opts.beforeSave && /^source: deconstruct\s*$/.test(il[0] || '')) {
      add(ic.n, W, `${ic.id}: \`${ic.rel}\` has no \`expect:\` line (line 3): every input Deconstruct writes says what should happen, from the practice-run playback`);
    }
    const blankAt = hasExpect ? 3 : 2;
    if ((il[blankAt] || '') !== '') {
      add(ic.n, W, hasExpect
        ? `${ic.id}: \`${ic.rel}\` line 4 must be blank, after the three header lines`
        : `${ic.id}: \`${ic.rel}\` line 3 must be blank, or the \`expect:\` header, after the \`source:\` and \`tests:\` lines`);
    }
    if (!il.slice(blankAt + 1).some((l) => l.trim())) add(ic.n, W, `${ic.id}: \`${ic.rel}\` holds no input under its headers`);
    il.forEach((l, k) => { if (SECRET_PATTERNS.some((re) => re.test(l))) add(ic.n, W, `${ic.id}: \`${ic.rel}\` line ${k + 1} looks like it holds a password or key`); });
  }

  problems.sort((a, b) => a.line - b.line);
  problems.notes = notes;
  return problems;
}

function checkStepLine(t, n, steps, stepRefs, ctxRefs, writeRefs, add) {
  const P = '## Path';
  const parts = t.split(' · ');
  const head = parts[0].match(/^- Step (\d+) — (\S.*)$/);
  if (!head) { add(n, P, 'a step line opens `- Step N — [Name]`'); return; }
  const num = Number(head[1]);
  const label = `Step ${num}`;
  if (steps.has(num)) add(n, P, `${label} is used twice`);
  const entry = { name: head[2], n, fixed: false };
  steps.set(num, entry);
  if (!parts[1] || !/^produces \S/.test(parts[1])) add(n, P, `${label} has no \`produces\` (name · produces · mark are required)`);
  const ORDER = ['uses', 'mark', 'writes', 'role', 'parallel', 'proposed'];
  let last = -1;
  let mark = false;
  for (const tag of parts.slice(parts[1] && parts[1].startsWith('produces ') ? 2 : 1)) {
    let kind = null;
    if (/^uses \S/.test(tag)) {
      kind = 'uses';
      for (const c of tag.matchAll(/\bC(\d+)\b/g)) ctxRefs.push({ id: `C${c[1]}`, n, where: P });
    } else if (/^fixed \((regulation|policy|your judgment)\)$/.test(tag) || tag === 'flexible') {
      kind = 'mark'; mark = true; entry.fixed = tag !== 'flexible';
    } else if (/^fixed\b/.test(tag)) {
      add(n, P, `${label}: "${tag}" — fixed carries its reason: fixed (regulation), fixed (policy) or fixed (your judgment)`); kind = 'mark'; mark = true; entry.fixed = true;
    } else if (/^writes W\d+(, W\d+)*$/.test(tag)) {
      kind = 'writes';
      for (const w of tag.matchAll(/W\d+/g)) writeRefs.push({ id: w[0], n, where: P });
    } else if (/^\([^()]+\)$/.test(tag)) {
      kind = 'role';
    } else if (/^parallel with Step \d+((, | and )Step \d+)*$/.test(tag)) {
      kind = 'parallel';
      for (const s of tag.matchAll(/Step (\d+)/g)) stepRefs.push({ num: Number(s[1]), n, where: P });
    } else if (tag === 'proposed by AI') {
      kind = 'proposed';
    } else { add(n, P, `${label}: unknown tag "${tag}"`); continue; }
    const k = ORDER.indexOf(kind);
    if (k === last) add(n, P, `${label}: the ${kind} tag appears twice`);
    else if (k < last) add(n, P, `${label}: tags out of order — produces, uses, fixed/flexible, writes, role, parallel with, proposed by AI`);
    last = Math.max(last, k);
  }
  if (!mark) add(n, P, `${label} has no fixed-or-flexible mark (fixed (regulation | policy | your judgment) or flexible), also on a step a person does`);
}

function tableRows(rows, header, where, add, onRow) {
  if (!rows.length) return;
  if (!rows[0].t.trim().startsWith('|') || !sameList(cells(rows[0].t), header)) {
    add(rows[0].n, where, `the table header must be \`| ${header.join(' | ')} |\``);
    if (!rows[0].t.trim().startsWith('|')) return;
  }
  if (!rows[1] || !isSeparator(rows[1].t)) add((rows[1] || rows[0]).n, where, 'the table has no separator line under its header');
  for (const r of rows.slice(2)) {
    if (!r.t.trim().startsWith('|')) { add(r.n, where, 'unexpected line inside the table'); continue; }
    const c = cells(r.t);
    if (c.length !== header.length) { add(r.n, where, `the row has ${c.length} cells; the table has ${header.length} columns`); continue; }
    onRow(c, r.n);
  }
}

function sectionAt(heads, index) {
  let name = 'title';
  for (const h of heads) if (h.index <= index) name = `## ${h.name}`;
  return name;
}

// ---------------------------------------------------------------- CLI

function main(argv) {
  const args = argv.slice(2);
  const opts = {};
  const files = [];
  for (const a of args) {
    if (a === '--registry') opts.registry = true;
    else if (a === '--no-registry') opts.registry = false;
    else if (a === '--before-save') opts.beforeSave = true;
    else if (a === '-h' || a === '--help') { console.log('Usage: requirements-check.js <requirements.md | workflow folder> [--registry | --no-registry] [--before-save]'); return 0; }
    else if (a.startsWith('--')) { console.error(`requirements-check: unknown option ${a}`); return 2; }
    else files.push(a);
  }
  if (files.length !== 1) { console.error('Usage: requirements-check.js <requirements.md | workflow folder> [--registry | --no-registry] [--before-save]'); return 2; }
  let file = files[0];
  try { if (fs.statSync(file).isDirectory()) file = path.join(file, 'requirements.md'); } catch (e) { /* reported below */ }
  let problems;
  try { problems = check(file, opts); } catch (e) {
    console.error(`requirements-check: can't read ${file} (${e.code || e.message})`);
    return 2;
  }
  const rel = file;
  for (const p of problems.notes || []) console.log(`${rel}:${p.line} · ${p.section} · note: ${p.msg}`);
  if (!problems.length) { console.log(`requirements-check: ${rel} matches the requirements template`); return 0; }
  for (const p of problems) console.log(`${rel}:${p.line} · ${p.section} · ${p.msg}`);
  console.log(`requirements-check: ${problems.length} problem${problems.length === 1 ? '' : 's'} in ${rel}`);
  return 1;
}

module.exports = { check };
if (require.main === module) process.exit(main(process.argv));
