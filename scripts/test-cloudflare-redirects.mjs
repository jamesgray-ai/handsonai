#!/usr/bin/env node
// Unit test for src/integrations/cloudflare-redirects.mjs — run with `node scripts/test-cloudflare-redirects.mjs`.
import assert from 'node:assert/strict';
import { renderRedirects } from '../src/integrations/cloudflare-redirects.mjs';

const out = renderRedirects({
  '/old/': '/new/',
  '/gone/': { status: 302, destination: '/elsewhere/' },
  '/keep/': '/keep/',
});
const lines = out.trim().split('\n').filter((l) => l && !l.startsWith('#'));

// Each Astro redirect becomes a Cloudflare rule, matched both with and without the trailing slash.
assert.ok(lines.includes('/old/ /new/ 301'), 'string redirect → 301');
assert.ok(lines.includes('/old /new/ 301'), 'also matches the no-trailing-slash form');
assert.ok(lines.includes('/gone/ /elsewhere/ 302'), 'object redirect keeps its status');
assert.ok(!lines.some((l) => l.startsWith('/keep')), 'self-redirects are dropped');
assert.equal(lines.length, 4, `expected 4 rules, got ${lines.length}:\n${lines.join('\n')}`);
assert.ok(out.startsWith('#'), 'file opens with a generated-file comment');

console.log('ok - cloudflare-redirects');
