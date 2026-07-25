#!/usr/bin/env node
/**
 * Internal link and anchor checker for the built site.
 *
 * Runs against `dist/` after `astro build`, so it sees exactly what ships.
 * Catches two failures a build cannot:
 *
 *   1. A link to a page that no longer exists (moved or renamed).
 *   2. A `#fragment` whose heading was reworded, so the id it points at is gone.
 *
 * The second is the quiet one — the page still loads, the reader just lands at
 * the top instead of the section, and nothing anywhere reports it. Course
 * material deep-links this site by anchor, so a reworded heading breaks a
 * student's instructions without breaking the build.
 *
 * External links (github.com, brew.sh, …) are deliberately NOT checked: that
 * needs network in CI and produces flaky failures from rate limiting.
 *
 * Usage:  node scripts/check-links.js [distDir]
 * Exit:   0 = clean, 1 = broken links found
 */

import fs from 'node:fs';
import path from 'node:path';

const DIST = path.resolve(process.argv[2] || 'dist');

/** Every .html file under dist, as absolute paths. */
function htmlFiles(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) htmlFiles(p, out);
    else if (entry.name.endsWith('.html')) out.push(p);
  }
  return out;
}

/**
 * Map a site-root-relative URL path to the file that serves it.
 * Astro emits directory-style routes: /a/b/ -> dist/a/b/index.html.
 */
function resolveRoute(urlPath) {
  const clean = urlPath.replace(/\/+$/, '');
  const candidates = [
    path.join(DIST, clean, 'index.html'),
    path.join(DIST, `${clean}.html`),
    path.join(DIST, clean), // already a file (e.g. /llms.txt)
  ];
  return candidates.find((c) => fs.existsSync(c) && fs.statSync(c).isFile()) || null;
}

/** id="..." values present in a rendered page. */
function idsIn(file) {
  const html = fs.readFileSync(file, 'utf8');
  const ids = new Set();
  for (const m of html.matchAll(/\sid="([^"]+)"/g)) ids.add(m[1]);
  return ids;
}

const idCache = new Map();
function idsFor(file) {
  if (!idCache.has(file)) idCache.set(file, idsIn(file));
  return idCache.get(file);
}

// ---------------------------------------------------------------------------
// Sidebar coverage
//
// CLAUDE.md: "When adding new docs to `src/content/docs/`, also update the
// sidebar in `astro.config.mjs`". Nothing enforced that, so a new page could
// ship reachable only by inline link — which happened to the repository
// creation guide, the page every student is now sent to for setup.
//
// Two sections are structurally absent from the sidebar by design, and a
// handful of pages predate this check. New gaps fail; pre-existing ones warn,
// so they stay visible without blocking anyone.
// ---------------------------------------------------------------------------

/** Sections the sidebar deliberately does not enumerate. */
const SIDEBAR_EXEMPT_PREFIXES = [
  '/blog', // starlight-blog renders its own index
  '/questions', // surfaced through the Q&A hub, not the nav tree
];

/** Individual pages intentionally outside the nav. */
const SIDEBAR_EXEMPT_ROUTES = new Set([
  '/CONTRIBUTING', // repo meta, not reader-facing
  '/feed', // feed landing page
]);

/**
 * Pages that were already missing when this check was added. Not endorsed —
 * each is worth a decision. Remove entries as they are either added to the
 * sidebar or consciously exempted above.
 */
const SIDEBAR_KNOWN_GAPS = new Set([
  '/ai-engineering',
  '/courses/builders/week-1',
  '/courses/builders/week-1/mcp-connectors-setup',
  '/platforms/overview',
  '/platforms/resources',
]);

function checkSidebar() {
  const configPath = path.resolve('astro.config.mjs');
  const srcDir = path.resolve('src/content/docs');
  if (!fs.existsSync(configPath) || !fs.existsSync(srcDir)) return { newGaps: [], knownGaps: [] };

  const cfg = fs.readFileSync(configPath, 'utf8');
  const linked = new Set(
    [...cfg.matchAll(/link:\s*'([^']+)'/g)].map((m) => m[1].replace(/\/+$/, '') || '/')
  );

  const docs = [];
  (function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(p);
      else if (/\.mdx?$/.test(entry.name)) docs.push(p);
    }
  })(srcDir);

  const newGaps = [];
  const knownGaps = [];
  for (const file of docs) {
    let route = '/' + path.relative(srcDir, file).replace(/\.mdx?$/, '').replace(/\/index$/, '');
    if (route === '/index') route = '/';
    if (linked.has(route) || linked.has(`${route}/`)) continue;
    if (SIDEBAR_EXEMPT_PREFIXES.some((p) => route === p || route.startsWith(`${p}/`))) continue;
    if (SIDEBAR_EXEMPT_ROUTES.has(route)) continue;
    (SIDEBAR_KNOWN_GAPS.has(route) ? knownGaps : newGaps).push(route);
  }
  return { newGaps: newGaps.sort(), knownGaps: knownGaps.sort() };
}

if (!fs.existsSync(DIST)) {
  console.error(`check-links: ${DIST} not found — run \`npm run build\` first.`);
  process.exit(1);
}

const pages = htmlFiles(DIST);
const problems = [];
let checked = 0;

for (const page of pages) {
  const html = fs.readFileSync(page, 'utf8');
  const from = '/' + path.relative(DIST, page).replace(/\/?index\.html$/, '').replace(/\.html$/, '');

  for (const m of html.matchAll(/<a\s[^>]*href="([^"]+)"/g)) {
    const href = m[1];

    // Skip anything that isn't an internal page link.
    if (/^(https?:|mailto:|tel:|javascript:|data:)/i.test(href)) continue;
    if (href.startsWith('#')) {
      // Same-page fragment.
      checked++;
      const frag = decodeURIComponent(href.slice(1));
      if (frag && !idsFor(page).has(frag)) {
        problems.push(`${from} → ${href} (no element with that id on this page)`);
      }
      continue;
    }
    if (!href.startsWith('/')) continue; // relative links are rare here; skip rather than guess

    checked++;
    const [rawPath, rawFrag] = href.split('#');
    const target = resolveRoute(rawPath);

    if (!target) {
      problems.push(`${from} → ${href} (page does not exist)`);
      continue;
    }
    if (rawFrag) {
      const frag = decodeURIComponent(rawFrag);
      if (!idsFor(target).has(frag)) {
        problems.push(`${from} → ${href} (page exists, but no element with id "${frag}")`);
      }
    }
  }
}

const { newGaps, knownGaps } = checkSidebar();
let failed = false;

if (problems.length) {
  console.error(`check-links: ${problems.length} broken of ${checked} internal links\n`);
  for (const p of problems.sort()) console.error(`  BROKEN  ${p}`);
  console.error(`\nA missing id usually means a heading was reworded. Fix the link, or restore the heading.\n`);
  failed = true;
} else {
  console.log(`check-links: ${checked} internal links and anchors OK across ${pages.length} pages`);
}

if (newGaps.length) {
  console.error(`check-links: ${newGaps.length} page(s) missing from the sidebar\n`);
  for (const r of newGaps) console.error(`  NO SIDEBAR ENTRY  ${r}`);
  console.error(
    `\nCLAUDE.md: when adding docs to src/content/docs/, add them to the sidebar in\n` +
    `astro.config.mjs too — otherwise the page is reachable only by inline link.\n` +
    `If it is deliberately outside the nav, add it to SIDEBAR_EXEMPT_ROUTES in this script.\n`
  );
  failed = true;
} else {
  console.log(`check-links: sidebar covers every doc (${knownGaps.length} pre-existing gap(s) allowed)`);
}

if (knownGaps.length) {
  console.warn(`\ncheck-links: pre-existing sidebar gaps, not blocking — each still wants a decision:`);
  for (const r of knownGaps) console.warn(`  known gap  ${r}`);
}

if (failed) process.exit(1);
