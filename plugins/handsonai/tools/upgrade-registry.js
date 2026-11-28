#!/usr/bin/env node
// registry-template/tools/upgrade-registry.js
// Upgrade an AI Registry bundle from OKF v0.2 to v0.3. See registry/SCHEMA.md.
// Usage: node tools/upgrade-registry.js [--check] [bundleDir]   (default: registry/)
//   --check  list what would change and write nothing (exit 1 when anything would)
//
// A format-only change (OKF v0.3 §5.2): no `generated` line moves, every key it
// doesn't own is kept (§4.1), and only the lines it changes are rewritten (§4).
//   - root index.md: okf_version "0.3" (added when absent)
//   - Workflow, Business, LineOfBusiness: a domain value in `status` moves to
//     `state`; a retired Workflow also says `status: deprecated` (§5.4)
//   - any other node with a domain value in `status` (a retired Process):
//     `status: deprecated`
//   - links and the guide:/folder: path fields written the 0.2 way (from the
//     registry's parent folder) become file-relative (§6), from what they reach:
//     framework/x/requirements.md -> ../../framework/x/requirements.md in a node.
//     Code spans and fenced blocks are never touched.
//   - log.md: entries regrouped under `## YYYY-MM-DD` headings, newest date
//     first, each entry a bullet (§9); every word kept.
// Running it again changes nothing. Zero npm dependencies.
'use strict';
const fs = require('fs');
const path = require('path');
const lib = require('./registry-lib');

const STATE_TYPES = new Set(['Workflow', 'Business', 'LineOfBusiness']);
const PATH_FIELDS = ['guide', 'folder'];

// Rewrite markdown link targets outside code: fenced blocks and inline code spans
// are left exactly as they are.
function mapLinksOutsideCode(text, fn) {
  let inFence = false;
  return text.split('\n').map((line) => {
    if (/^\s*(```|~~~)/.test(line)) { inFence = !inFence; return line; }
    if (inFence) return line;
    return line.split(/(`[^`]*`)/).map((seg, i) => (i % 2 === 1 ? seg
      : seg.replace(/\]\(([^)\s]+)\)/g, (m, href) => `](${fn(href)})`))).join('');
  }).join('\n');
}

// A 0.2-form link or path value as the 0.3 form for a file at bundle path `from`.
function upgradeHref(href, from, workspaceRoot, bundleName) {
  const r = lib.resolveHref(href, from, { legacy: true, bundleName });
  if (r.form !== 'legacy') return href;
  const frag = (href.match(/[#?].*$/) || [''])[0];
  const reach = lib.resolveOutside(r, workspaceRoot) || r.path;
  // A 0.2 link that reaches back into the registry (compose's used-by text in the root
  // index, registry/workflows/x.md) is a link between pages: root-relative.
  if (reach.startsWith(bundleName + '/')) return '/' + reach.slice(bundleName.length + 1) + frag;
  return lib.linkTo(reach, from, { bundleName }) + frag;
}

// links: false (a bundle already at 0.3, where a bare path already means
// file-relative) moves only a domain value left in `status`.
function upgradeNode(raw, relPath, workspaceRoot, bundleName, links = true) {
  const { fields } = lib.parseFrontmatter(raw);
  if (!fields) return { raw, notes: [] }; // no frontmatter: not a concept (§3.2), and not ours to touch
  const end = raw.indexOf('\n---\n', 4);
  const head = raw.slice(0, end);
  const body = raw.slice(end);
  const notes = [];
  const type = fields.type;
  const lines = head.split('\n');
  const out = [];
  const hasState = lib.stateOf({ state: fields.state }) !== null;
  for (const line of lines) {
    const st = line.match(/^status:\s*(.*)$/);
    if (st) {
      const value = st[1].trim();
      const plain = value.replace(/^["']|["']$/g, '');
      if (!plain || lib.LIFECYCLE_STATUS.includes(plain)) { out.push(line); continue; }
      if (STATE_TYPES.has(type) && !hasState) {
        out.push(`state: ${value}`);
        if (type === 'Workflow' && plain === 'retired') out.push('status: deprecated');
        continue;
      }
      if (!STATE_TYPES.has(type) && plain === 'retired') { out.push('status: deprecated'); continue; }
      notes.push(`${relPath}: status "${plain}" left as it is (move it by hand: domain state goes in state, status is draft, stable or deprecated)`);
      out.push(line);
      continue;
    }
    const pf = line.match(/^([\w-]+):\s*(.*)$/);
    if (links && pf && PATH_FIELDS.includes(pf[1]) && pf[2].trim()) {
      const v = pf[2].trim();
      const q = /^["']/.test(v) ? v[0] : '';
      const inner = q ? v.slice(1, -1) : v;
      const nu = upgradeHref(inner, relPath, workspaceRoot, bundleName);
      out.push(`${pf[1]}: ${q}${nu}${q}`);
      continue;
    }
    out.push(line);
  }
  const newBody = links ? mapLinksOutsideCode(body, (href) => upgradeHref(href, relPath, workspaceRoot, bundleName)) : body;
  return { raw: out.join('\n') + newBody, notes };
}

function upgradeIndex(raw, relPath, workspaceRoot, bundleName) {
  let text = mapLinksOutsideCode(raw, (href) => upgradeHref(href, relPath, workspaceRoot, bundleName));
  if (relPath !== '/index.md') return text;
  if (text.startsWith('---\n')) {
    const end = text.indexOf('\n---\n', 4);
    const head = text.slice(4, end);
    const rest = text.slice(end);
    const newHead = /^okf_version:/m.test(head)
      ? head.replace(/^okf_version:.*$/m, 'okf_version: "0.3"')
      : `okf_version: "0.3"\n${head}`;
    return `---\n${newHead}${rest}`;
  }
  return `---\nokf_version: "0.3"\n---\n${text}`;
}

// log.md -> OKF v0.3 §9. Recognized entries: `## YYYY-MM-DD — Title` headings with
// their paragraphs, and `YYYY-MM-DD: text` lines. A line with no date of its own
// (a "Dashboard Artifact:" line) stays with the entry before it. Text before the
// first entry (the title and the description) stays on top.
function upgradeLog(raw) {
  const lines = raw.replace(/\s+$/, '').split('\n');
  const HEAD = /^## (\d{4}-\d{2}-\d{2})(?:\s*(?:—|–|-|:)\s*(.*))?\s*$/;
  const LINE = /^(\d{4}-\d{2}-\d{2}):\s+(.*)$/;
  const heads = lines.filter((l) => /^## /.test(l));
  const dates = heads.map((l) => (l.match(/^## (\d{4}-\d{2}-\d{2})\s*$/) || [])[1]);
  const isConformant = lines.every((l) => !LINE.test(l)) && dates.every((d, i) => d && (i === 0 || d <= dates[i - 1]));
  if (isConformant) return raw;
  const preamble = [];
  const entries = []; // { date, order, title, paras: [string] } | { date, order, text }
  let cur = null;
  let lastDate = null;
  let started = false;
  let para = [];
  const flush = () => { if (cur && para.length) { cur.paras.push(para.join(' ')); } para = []; };
  for (const l of lines) {
    const h = l.match(HEAD);
    const d = l.match(LINE);
    if (h) {
      flush(); started = true; lastDate = h[1];
      cur = { date: h[1], order: entries.length, title: (h[2] || '').trim(), paras: [] };
      entries.push(cur);
      continue;
    }
    if (d) {
      flush(); started = true; lastDate = d[1]; cur = null;
      entries.push({ date: d[1], order: entries.length, text: d[2].trim() });
      continue;
    }
    if (!started) { preamble.push(l); continue; }
    if (!l.trim()) { flush(); continue; }
    // The dashboard's link is its own entry, dated by the entry before it.
    if (/^Dashboard Artifact:/.test(l.trim())) { flush(); cur = null; entries.push({ date: lastDate, order: entries.length, text: l.trim() }); continue; }
    // Under a date-only heading (already the §9 form) a top-level bullet is an entry of its own,
    // and an indented line belongs to the entry before it.
    if (cur && !cur.title && /^[-*]\s/.test(l)) { flush(); entries.push({ date: lastDate, order: entries.length, text: l.replace(/^[-*]\s+/, '').trim(), extra: [] }); continue; }
    const last = entries[entries.length - 1];
    if (cur && !cur.title && /^\s+\S/.test(l) && last && last.extra) { last.extra.push(l.replace(/\s+$/, '')); continue; }
    // A list or table line inside a titled entry keeps its own line, under the entry's bullet.
    if (cur && /^\s*([-*+]\s|\d+[.)]\s|\|)/.test(l)) { flush(); cur.paras.push({ raw: l.replace(/\s+$/, '') }); continue; }
    if (cur) { para.push(l.trim()); continue; }
    entries.push({ date: lastDate, order: entries.length, text: l.trim() });
  }
  flush();
  const byDate = new Map();
  for (const e of entries) {
    if (!byDate.has(e.date)) byDate.set(e.date, []);
    byDate.get(e.date).push(e);
  }
  const order = [...byDate.keys()].sort().reverse();
  const out = [preamble.join('\n').replace(/\s+$/, '')];
  for (const date of order) {
    out.push('', `## ${date}`, '');
    for (const e of byDate.get(date)) {
      if (e.text !== undefined) { out.push(`- ${e.text}`); for (const x of e.extra || []) out.push(x); continue; }
      if (!e.title && !e.paras.length) continue; // a date-only heading: its bullets are entries of their own
      const firstIsText = e.paras.length && typeof e.paras[0] === 'string';
      const first = firstIsText ? e.paras[0] : '';
      const more = firstIsText ? e.paras.slice(1) : e.paras;
      const lead = e.title ? `**${e.title}**${first ? ` — ${first}` : ''}` : (first || '');
      out.push(`- ${lead}`);
      for (const p of more) out.push(typeof p === 'string' ? `  ${p}` : `  ${p.raw}`);
    }
  }
  return out.join('\n').replace(/^\n+/, '') + '\n';
}

function upgrade(bundleDir, opts = {}) {
  const absBundle = path.resolve(bundleDir || 'registry');
  const workspaceRoot = path.dirname(absBundle);
  const bundleName = path.basename(absBundle);
  const changed = [];
  const notes = [];
  const legacy = lib.isLegacyVersion(lib.okfVersionOf(absBundle));
  const writes = new Map();
  const { nodes } = lib.loadBundle(absBundle);
  for (const [relPath, n] of nodes) {
    const base = path.posix.basename(relPath);
    let next = n.raw;
    if (base === 'log.md') next = upgradeLog(n.raw);
    else if (base === 'index.md') next = legacy ? upgradeIndex(n.raw, relPath, workspaceRoot, bundleName) : n.raw;
    else if (base === 'SCHEMA.md') next = n.raw; // the schema itself is replaced from the template, never patched
    else {
      const r = upgradeNode(n.raw, relPath, workspaceRoot, bundleName, legacy);
      next = r.raw;
      notes.push(...r.notes);
    }
    if (next !== n.raw) { changed.push(relPath); writes.set(path.join(absBundle, relPath.slice(1)), next); }
  }
  if (!nodes.has('/index.md')) {
    changed.push('/index.md');
    writes.set(path.join(absBundle, 'index.md'), '---\nokf_version: "0.3"\n---\n');
  }
  if (!opts.check) for (const [file, text] of writes) fs.writeFileSync(file, text);
  return { changed: changed.sort(), notes };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const check = args.includes('--check');
  const unknown = args.filter((a) => a.startsWith('-') && a !== '--check');
  if (unknown.length) {
    console.error(`upgrade-registry: unknown option ${unknown.join(' ')}`);
    console.error('Usage: node tools/upgrade-registry.js [--check] [bundleDir]');
    process.exit(2);
  }
  const dir = args.find((a) => !a.startsWith('-')) || 'registry';
  if (!fs.existsSync(path.join(dir, 'SCHEMA.md'))) {
    console.error(`upgrade-registry: no registry at ${dir} (no SCHEMA.md) -- nothing written`);
    process.exit(2);
  }
  const { changed, notes } = upgrade(dir, { check });
  for (const n of notes) console.log(`NOTE  ${n}`);
  for (const c of changed) console.log(`${check ? 'would change' : 'changed'}  ${path.posix.join(dir, c.slice(1))}`);
  console.log(`upgrade-registry: ${changed.length} file(s) ${check ? 'to change' : 'changed'}`);
  process.exit(check && changed.length ? 1 : 0);
}

module.exports = { upgrade, upgradeLog };
