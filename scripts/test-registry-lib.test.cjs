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
