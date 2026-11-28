// Unit tests for registry-template/tools/registry-lib.js: the OKF v0.3 readers
// (domain state, both link forms, bundle version, verified lists, the loader's
// bundle boundary). Run: node --test scripts/test-registry-lib.test.cjs
// (scripts/test-compose-registry.sh runs it too, so CI covers it.)
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const lib = require('../registry-template/tools/registry-lib');

// --- stateOf: domain state from `state`, or from a domain value left in `status`
test('stateOf reads state', () => {
  assert.equal(lib.stateOf({ state: 'backlog' }), 'backlog');
  assert.equal(lib.stateOf({ state: 'retired', status: 'deprecated' }), 'retired');
});
test('stateOf falls back to a domain value in status (OKF 0.2 form)', () => {
  assert.equal(lib.stateOf({ status: 'in-production' }), 'in-production');
  assert.equal(lib.stateOf({ status: 'active' }), 'active');
});
test('stateOf never reads a lifecycle value as domain state', () => {
  for (const s of ['draft', 'stable', 'deprecated']) assert.equal(lib.stateOf({ status: s }), null);
});
test('stateOf: absent, empty or null is no state (OKF 0.3 §11.2)', () => {
  assert.equal(lib.stateOf({}), null);
  assert.equal(lib.stateOf({ state: '' }), null);
  assert.equal(lib.stateOf(null), null);
});

// --- okf version
test('isLegacyVersion: none or below 0.3 is legacy; 0.3 and later, or unknown, are not', () => {
  assert.equal(lib.isLegacyVersion(null), true);
  assert.equal(lib.isLegacyVersion('0.2'), true);
  assert.equal(lib.isLegacyVersion('0.1'), true);
  assert.equal(lib.isLegacyVersion('0.3'), false);
  assert.equal(lib.isLegacyVersion('0.4'), false);
  assert.equal(lib.isLegacyVersion('1.0'), false);
  assert.equal(lib.isLegacyVersion('next'), false); // best effort (§12), never refused
});
test('okfVersionOf reads the root index frontmatter', () => {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'reglib-'));
  fs.writeFileSync(path.join(d, 'index.md'), '---\nokf_version: "0.3"\ntitle: X\n---\n# X\n');
  assert.equal(lib.okfVersionOf(d), '0.3');
  fs.writeFileSync(path.join(d, 'index.md'), '# X\n');
  assert.equal(lib.okfVersionOf(d), null);
});

// --- resolveHref: OKF 0.3 §6
const R = (href, from, legacy) => lib.resolveHref(href, from, { legacy, bundleName: 'registry' });
test('resolveHref: a URL is external; a bare fragment is skipped', () => {
  assert.equal(R('https://x.test/a', '/workflows/a.md').kind, 'external');
  assert.equal(R('#top', '/workflows/a.md').kind, 'fragment');
});
test('resolveHref: leading / resolves from the bundle root', () => {
  assert.deepEqual(R('/processes/p.md#x', '/workflows/a.md'), { kind: 'bundle', path: '/processes/p.md', form: 'root', href: '/processes/p.md#x' });
});
test('resolveHref: file-relative out of the bundle, by depth', () => {
  const a = R('../../framework/a/requirements.md', '/workflows/a.md');
  assert.equal(a.kind, 'outside'); assert.equal(a.path, 'framework/a/requirements.md'); assert.equal(a.form, 'relative');
  const b = R('../.claude/skills/s/SKILL.md', '/index.md');
  assert.equal(b.kind, 'outside'); assert.equal(b.path, '.claude/skills/s/SKILL.md');
  assert.equal(R('../../framework/a/', '/workflows/a.md').path, 'framework/a/'); // directory target keeps its /
});
test('resolveHref: file-relative inside the bundle is still in the bundle', () => {
  const r = R('../processes/p.md', '/workflows/a.md');
  assert.equal(r.kind, 'bundle'); assert.equal(r.path, '/processes/p.md'); assert.equal(r.form, 'relative');
  const s = R('../registry/notes/n.md', '/index.md');
  assert.equal(s.kind, 'bundle'); assert.equal(s.path, '/notes/n.md');
});
test('resolveHref: in a 0.3 bundle a bare path is file-relative (and lands in the bundle)', () => {
  const r = R('framework/a/requirements.md', '/workflows/a.md', false);
  assert.equal(r.kind, 'bundle'); assert.equal(r.path, '/workflows/framework/a/requirements.md');
});
test('resolveHref: in a 0.2 bundle a bare path is relative to the registry\'s parent folder', () => {
  const r = R('framework/a/requirements.md', '/workflows/a.md', true);
  assert.deepEqual(r, { kind: 'outside', path: 'framework/a/requirements.md', form: 'legacy', href: 'framework/a/requirements.md' });
  // ...and the 0.3 form is read file-relative there too
  assert.equal(R('../../framework/a/requirements.md', '/workflows/a.md', true).path, 'framework/a/requirements.md');
});
test('resolveHref: percent-encoded paths are decoded', () => {
  assert.equal(R('../../sops/my%20sop.md', '/workflows/a.md').path, 'sops/my sop.md');
});

// --- linkTo: the form a writer uses
test('linkTo writes file-relative by depth in a 0.3 bundle', () => {
  const L = (t, from, legacy) => lib.linkTo(t, from, { legacy, bundleName: 'registry' });
  assert.equal(L('framework/a/requirements.md', '/workflows/a.md'), '../../framework/a/requirements.md');
  assert.equal(L('.claude/skills/s/SKILL.md', '/index.md'), '../.claude/skills/s/SKILL.md');
  assert.equal(L('framework/a/', '/workflows/a.md'), '../../framework/a/');
  assert.equal(L('/processes/p.md', '/workflows/a.md'), '/processes/p.md');
  assert.equal(L('framework/a/requirements.md', '/workflows/a.md', true), 'framework/a/requirements.md');
});

// --- classifyLinks with the linking file
test('classifyLinks(raw, from) resolves each link; without from it keeps the 0.2 reading', () => {
  const raw = '- [R](../../framework/a/requirements.md)\n- [P](/processes/p.md)\n- [U](https://x.test)\n- [S](sops/x.md)';
  const c = lib.classifyLinks(raw, '/workflows/a.md', { legacy: true, bundleName: 'registry' });
  assert.deepEqual(c.inBundle, ['/processes/p.md']);
  assert.deepEqual(c.repo, ['framework/a/requirements.md', 'sops/x.md']);
  assert.deepEqual(c.external, ['https://x.test']);
  assert.equal(c.links.length, 4);
  const old = lib.classifyLinks('- [S](sops/x.md)');
  assert.deepEqual(old.repo, ['sops/x.md']);
});

// --- resolveOutside: existence, with the framework/ fallback only for the 0.2 form
test('resolveOutside applies the framework/ fallback only to a legacy link', () => {
  const ws = fs.mkdtempSync(path.join(os.tmpdir(), 'reglib-'));
  fs.mkdirSync(path.join(ws, 'framework', 'a'), { recursive: true });
  fs.writeFileSync(path.join(ws, 'framework', 'a', 'requirements.md'), 'x');
  assert.equal(lib.resolveOutside({ path: 'a/requirements.md', form: 'legacy' }, ws), 'framework/a/requirements.md');
  assert.equal(lib.resolveOutside({ path: 'a/requirements.md', form: 'relative' }, ws), null);
  assert.equal(lib.resolveOutside({ path: 'framework/a/requirements.md', form: 'relative' }, ws), 'framework/a/requirements.md');
  assert.equal(lib.resolveOutside({ path: 'framework/a/', form: 'relative' }, ws), 'framework/a/');
});

// --- parseFrontmatter: OKF 0.3 verified/sources shapes, quoted flow-map values
test('flow-map values may be quoted (the v0.3 examples quote timestamps)', () => {
  const { fields } = lib.parseFrontmatter('---\ntype: Note\ngenerated: { by: process:test, at: "2026-11-01T00:00:00Z" }\n---\n');
  assert.deepEqual(fields.generated, { by: 'process:test', at: '2026-11-01T00:00:00Z' });
});
test('verified as a flow list of maps', () => {
  const { fields, error } = lib.parseFrontmatter('---\ntype: Note\nverified: [{ by: human:ana, at: 2026-11-01T00:00:00Z }, { by: process:x, at: 2026-11-02T00:00:00Z }]\n---\n');
  assert.equal(error, undefined);
  assert.deepEqual(fields.verified, [{ by: 'human:ana', at: '2026-11-01T00:00:00Z' }, { by: 'process:x', at: '2026-11-02T00:00:00Z' }]);
});
test('verified and sources as a block list of one-line maps', () => {
  const { fields, error } = lib.parseFrontmatter('---\ntype: Note\nverified:\n  - { by: human:ana, at: 2026-11-01T00:00:00Z }\n  - { by: process:x, at: 2026-11-02T00:00:00Z }\nsources:\n  - { id: a, resource: ../../sops/a.md }\ntitle: T\n---\n');
  assert.equal(error, undefined);
  assert.equal(fields.verified.length, 2);
  assert.deepEqual(fields.sources, [{ id: 'a', resource: '../../sops/a.md' }]);
  assert.equal(fields.title, 'T');
});
test('a block list is still refused for any other key', () => {
  const { fields, error } = lib.parseFrontmatter('---\ntype: Note\ntags:\n  - a\n---\n');
  assert.equal(fields, null); assert.match(error, /multi-line/);
});
test('a plain list still splits on commas', () => {
  assert.deepEqual(lib.parseFrontmatter('---\ntags: [a, b]\n---\n').fields.tags, ['a', 'b']);
});
test('verifiedEvents treats a bare map as a list of one (§5.2)', () => {
  assert.deepEqual(lib.verifiedEvents({ verified: { by: 'human:a', at: '2026-01-01T00:00:00Z' } }), [{ by: 'human:a', at: '2026-01-01T00:00:00Z' }]);
  assert.deepEqual(lib.verifiedEvents({}), []);
});

// --- loadBundle: OKF 0.3 §3.2 rules 4-5
test('loadBundle skips dot-paths and symlinks that leave the bundle', () => {
  const ws = fs.mkdtempSync(path.join(os.tmpdir(), 'reglib-'));
  const b = path.join(ws, 'registry');
  fs.mkdirSync(path.join(b, '.obsidian'), { recursive: true });
  fs.mkdirSync(path.join(b, 'notes'), { recursive: true });
  fs.writeFileSync(path.join(b, '.obsidian', 'workspace.md'), 'x');
  fs.writeFileSync(path.join(b, 'notes', 'n.md'), '---\ntype: Note\n---\n');
  fs.writeFileSync(path.join(ws, 'outside.md'), '---\ntype: Note\n---\n');
  fs.symlinkSync(path.join(ws, 'outside.md'), path.join(b, 'notes', 'link.md'));
  fs.symlinkSync(path.join(b, 'notes', 'n.md'), path.join(b, 'notes', 'inside.md'));
  const keys = [...lib.loadBundle(b).nodes.keys()].sort();
  assert.deepEqual(keys, ['/notes/inside.md', '/notes/n.md']);
});

// --- upgrade-registry.js: OKF 0.2 -> 0.3, format-only
const up = require('../registry-template/tools/upgrade-registry');
function ws02() {
  const ws = fs.mkdtempSync(path.join(os.tmpdir(), 'regup-'));
  const w = (p, t) => { fs.mkdirSync(path.dirname(path.join(ws, p)), { recursive: true }); fs.writeFileSync(path.join(ws, p), t); };
  w('registry/index.md', '---\nokf_version: "0.2"\n---\n# AI Registry\n\n- [Workflows](/workflows/index.md) — w\n');
  w('registry/workflows/a.md', '---\ntype: Workflow\ntitle: A\ndescription: d\ngenerated: { by: process:analyze, at: 2026-10-01T00:00:00Z }\nstatus: retired\nx-acme-owner: ana\n---\n# A\n\nSee `[code](sops/a.md)` and:\n\n```\n[fenced](sops/a.md)\n```\n\n# Artifacts\n- [Requirements](framework/a/requirements.md#goal)\n- [SOP](sops/a.md)\n- [Old](a/design-plan.md)\n- [Web](https://x.test)\n\n# Skills\n- [s](.claude/skills/s/SKILL.md)\n');
  w('registry/businesses/b.md', '---\ntype: Business\ntitle: B\ndescription: d\ngenerated: { by: process:scaffolding-registry, at: 2026-10-01T00:00:00Z }\nstatus: active\n---\n# B\n');
  w('registry/lines-of-business/l.md', '---\ntype: LineOfBusiness\ntitle: L\ndescription: d\ngenerated: { by: process:scaffolding-registry, at: 2026-10-01T00:00:00Z }\nstatus: "dormant"\nfolder: lob-files/\n---\n# L\n');
  w('registry/processes/p.md', '---\ntype: Process\ntitle: P\ndescription: d\ngenerated: { by: process:scaffolding-registry, at: 2026-10-01T00:00:00Z }\nowner: ops\nstatus: retired\nguide: guides/p.md\n---\n# P\n');
  w('registry/log.md', '# Registry Log\n\nWhat this log holds.\n\n## 2026-09-01 — Registry scaffolded\n\nSet up for a business the owner runs alone.\n\nDashboard Artifact: https://claude.ai/x\n2026-10-10: A went live after test round 1\n2026-10-12: A: re-checked, ready\n');
  w('framework/a/requirements.md', 'x'); w('framework/a/design-plan.md', 'x');
  return ws;
}
test('upgrade: version, state, lifecycle, links and path fields; generated untouched', () => {
  const ws = ws02();
  const r = up.upgrade(path.join(ws, 'registry'));
  assert.ok(r.changed.length >= 6);
  const rd = (p) => fs.readFileSync(path.join(ws, p), 'utf8');
  assert.match(rd('registry/index.md'), /^---\nokf_version: "0\.3"\n---\n/);
  const a = rd('registry/workflows/a.md');
  assert.match(a, /\nstate: retired\nstatus: deprecated\n/);
  assert.match(a, /\nx-acme-owner: ana\n/); // unknown keys kept (§4.1)
  assert.match(a, /generated: \{ by: process:analyze, at: 2026-10-01T00:00:00Z \}/); // format-only (§5.2)
  assert.match(a, /\[Requirements\]\(\.\.\/\.\.\/framework\/a\/requirements\.md#goal\)/);
  assert.match(a, /\[SOP\]\(\.\.\/\.\.\/sops\/a\.md\)/);
  assert.match(a, /\[Old\]\(\.\.\/\.\.\/framework\/a\/design-plan\.md\)/); // the 0.2 fallback, made explicit
  assert.match(a, /\[Web\]\(https:\/\/x\.test\)/);
  assert.match(a, /\[s\]\(\.\.\/\.\.\/\.claude\/skills\/s\/SKILL\.md\)/);
  assert.match(a, /`\[code\]\(sops\/a\.md\)`/); // inline code untouched
  assert.match(a, /```\n\[fenced\]\(sops\/a\.md\)\n```/); // fenced code untouched
  assert.match(rd('registry/businesses/b.md'), /\nstate: active\n/);
  assert.match(rd('registry/lines-of-business/l.md'), /\nstate: "dormant"\nfolder: \.\.\/\.\.\/lob-files\/\n/);
  const p = rd('registry/processes/p.md');
  assert.match(p, /\nstatus: deprecated\nguide: \.\.\/\.\.\/guides\/p\.md\n/);
  assert.doesNotMatch(p, /state:/);
});
test('upgrade: log.md to OKF §9, newest date first, every word kept', () => {
  const ws = ws02();
  up.upgrade(path.join(ws, 'registry'));
  const log = fs.readFileSync(path.join(ws, 'registry/log.md'), 'utf8');
  assert.equal(log, '# Registry Log\n\nWhat this log holds.\n\n## 2026-10-12\n\n- A: re-checked, ready\n\n## 2026-10-10\n\n- A went live after test round 1\n\n## 2026-09-01\n\n- **Registry scaffolded** — Set up for a business the owner runs alone.\n- Dashboard Artifact: https://claude.ai/x\n');
});
test('upgrade: idempotent, and --check reports without writing', () => {
  const ws = ws02();
  const before = fs.readFileSync(path.join(ws, 'registry/workflows/a.md'), 'utf8');
  const dry = up.upgrade(path.join(ws, 'registry'), { check: true });
  assert.ok(dry.changed.length > 0);
  assert.equal(fs.readFileSync(path.join(ws, 'registry/workflows/a.md'), 'utf8'), before);
  up.upgrade(path.join(ws, 'registry'));
  assert.deepEqual(up.upgrade(path.join(ws, 'registry')).changed, []);
});
test('upgrade: legacy layout (registry/ inside the framework folder) converts from the resolved path', () => {
  const ws = fs.mkdtempSync(path.join(os.tmpdir(), 'regup-'));
  fs.mkdirSync(path.join(ws, 'registry', 'workflows'), { recursive: true });
  fs.mkdirSync(path.join(ws, 'a'), { recursive: true });
  fs.writeFileSync(path.join(ws, 'a', 'requirements.md'), 'x');
  fs.writeFileSync(path.join(ws, 'registry', 'index.md'), '---\nokf_version: "0.2"\n---\n');
  fs.writeFileSync(path.join(ws, 'registry', 'workflows', 'a.md'), '---\ntype: Workflow\nstatus: backlog\n---\n# Artifacts\n- [Requirements](a/requirements.md)\n');
  up.upgrade(path.join(ws, 'registry'));
  assert.match(fs.readFileSync(path.join(ws, 'registry/workflows/a.md'), 'utf8'), /\(\.\.\/\.\.\/a\/requirements\.md\)/);
});
test('upgrade: a bundle with no okf_version gets one', () => {
  const ws = fs.mkdtempSync(path.join(os.tmpdir(), 'regup-'));
  fs.mkdirSync(path.join(ws, 'registry'));
  fs.writeFileSync(path.join(ws, 'registry', 'index.md'), '# AI Registry\n');
  up.upgrade(path.join(ws, 'registry'));
  assert.equal(fs.readFileSync(path.join(ws, 'registry/index.md'), 'utf8'), '---\nokf_version: "0.3"\n---\n# AI Registry\n');
});

// --- review fixes (code review of commits 1-5)
test('upgrade: a 0.2 link that reaches inside the bundle becomes root-relative', () => {
  const ws = fs.mkdtempSync(path.join(os.tmpdir(), 'regup-'));
  fs.mkdirSync(path.join(ws, 'registry', 'workflows'), { recursive: true });
  fs.writeFileSync(path.join(ws, 'registry', 'workflows', 'w.md'), '---\ntype: Workflow\nstatus: backlog\n---\n');
  fs.writeFileSync(path.join(ws, 'registry', 'index.md'), '---\nokf_version: "0.2"\n---\n- [s](.claude/skills/s/SKILL.md) (used by: [W](registry/workflows/w.md))\n');
  up.upgrade(path.join(ws, 'registry'));
  const t = fs.readFileSync(path.join(ws, 'registry', 'index.md'), 'utf8');
  assert.match(t, /\[W\]\(\/workflows\/w\.md\)/);
  assert.match(t, /\[s\]\(\.\.\/\.claude\/skills\/s\/SKILL\.md\)/);
});
test('toMillis: an impossible date is null, never NaN or a rolled-over day', () => {
  assert.equal(lib.toMillis('2026-13-45'), null);
  assert.equal(lib.toMillis('2026-02-30'), null);
  assert.equal(lib.toMillis('2026-02-30T00:00:00Z'), null);
  assert.equal(lib.toMillis('2028-02-29'), Date.parse('2028-02-29T00:00:00Z'));
});
test('upgrade and linkTo keep a link percent-encoded', () => {
  const r = lib.resolveHref('framework/my%20wf/requirements.md', '/workflows/a.md', { legacy: true, bundleName: 'registry' });
  assert.equal(lib.linkTo(r.path, '/workflows/a.md', { bundleName: 'registry' }), '../../framework/my%20wf/requirements.md');
});
test('a quoted flow-map value may hold a comma', () => {
  const { fields, error } = lib.parseFrontmatter('---\nsources: [{ id: a, title: "Smith, 2025", resource: x }]\ngenerated: { by: process:x, at: "2026-01-01T00:00:00Z" }\n---\n');
  assert.equal(error, undefined);
  assert.deepEqual(fields.sources, [{ id: 'a', title: 'Smith, 2025', resource: 'x' }]);
});
test('in a 0.2 bundle a ./ link keeps its 0.2 meaning (from the parent folder)', () => {
  const r = lib.resolveHref('./framework/a/r.md', '/workflows/a.md', { legacy: true, bundleName: 'registry' });
  assert.equal(r.kind, 'outside'); assert.equal(r.path, 'framework/a/r.md'); assert.equal(r.form, 'legacy');
});
test('upgradeLog: date-only headings oldest first are put newest first', () => {
  assert.equal(up.upgradeLog('# Log\n\n## 2026-01-01\n\n- a\n\n## 2026-02-01\n\n- b\n'), '# Log\n\n## 2026-02-01\n\n- b\n\n## 2026-01-01\n\n- a\n');
});
test('upgradeLog: a list inside an entry keeps its lines', () => {
  assert.equal(up.upgradeLog('# Log\n\n## 2026-01-01 — T\n\nPara:\n- one\n- two\n'), '# Log\n\n## 2026-01-01\n\n- **T** — Para:\n  - one\n  - two\n');
});
