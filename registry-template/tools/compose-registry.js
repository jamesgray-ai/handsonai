#!/usr/bin/env node
// registry-template/tools/compose-registry.js
// Compose the AI Registry's derived views. See registry/SCHEMA.md.
// Usage: node tools/compose-registry.js [--check] [--island-only] [bundleDir]
//   --check        build in memory and exit 1 if any output differs from disk
//   --island-only  print the data island JSON to stdout; write nothing
//
// Rewrites GENERATED blocks (Function `# Owns`, Workflow `# Insights`, root
// `index.md` skills/agents inventories), refreshes the plain directory
// `index.md` bullet lists, emits
// the repo-root REGISTRY.md dashboard, and injects the data island into
// registry-dashboard.html when that file exists (--island-only prints it instead).
//
// Deterministic: stable code-point ordering only (`.sort()`, never
// `localeCompare`), no `Date.now()`/`new Date()` anywhere in this file --
// "today" enters composed output nowhere; it is strictly a lint-time warning
// concern (see lint-registry.js). Refuses to emit while lint reports errors,
// except broken-link / index-coverage errors attributed to a file this run is
// about to rewrite wholesale (self-healing a rename) -- a post-emit lint pass
// is the backstop for that suppression.
'use strict';
const fs = require('fs');
const path = require('path');
const lib = require('./registry-lib');
const { lint } = require('./lint-registry');
// The routing rule, shipped beside these tools: one implementation, so the
// dashboard and the five step skills always agree on where a workflow is.
const { workflowState } = require('./framework-state');

// Plural directory -> display title for the plain (non-curated) directory
// index.md bullet lists compose regenerates. Every bundle directory except
// SCHEMA.md/log.md/root index.md gets one of these (SCHEMA.md "Types and
// directories").
const DIR_TITLES = {
  businesses: 'Businesses',
  'lines-of-business': 'Lines of Business',
  functions: 'Functions',
  processes: 'Processes',
  workflows: 'Workflows',
  notes: 'Notes',
};

// Matches the ai-registry-template skeleton's placeholder body exactly, so a
// freshly-scaffolded (all-empty) bundle round-trips through compose with zero
// diff -- a student's first Action run should not rewrite untouched files.
const EMPTY_INDEX_BODY = '_No entries yet — your AI assistant fills this index as nodes are added._';

// Leader-facing labels (indexing-registry's registry-bundle.md section 5): no
// raw autonomy or execution_mode value, and never a step number.
const HOW_IT_DECIDES = {
  deterministic: 'Deterministic: follows your instructions',
  guided: 'Guided: makes bounded decisions with your method',
  autonomous: 'Autonomous: works toward a goal you set',
};
const HOW_IT_RUNS = { manual: 'Runs with you', augmented: 'Runs with you', automated: 'Runs without you' };

function dash(v) { return v || '—'; }
// A markdown table cell: a `|` inside the value would split the cell.
function cell(v) { return dash(v).replace(/\|/g, '\\|'); }
// Skill/agent descriptions may span lines (`|`, `>`, blank lines); every view shows one line.
function oneLine(v) { return v ? String(v).replace(/\s+/g, ' ').trim() : v; }
function cmpPath(a, b) { return a.relPath < b.relPath ? -1 : a.relPath > b.relPath ? 1 : 0; }
function nodeTitle(n) { return (n.fm && n.fm.title) || lib.slugOf(n.relPath); }

// Drop only `undefined` keys -- `null` is a deliberate island value (e.g. an
// unassigned workflow's processId/lobId), never stripped.
function clean(obj) {
  const out = {};
  for (const k of Object.keys(obj)) if (obj[k] !== undefined) out[k] = obj[k];
  return out;
}

// --- git remote -> GitHub blob base (nodeUrl support) -----------------------
// Reads ONLY <workspaceRoot>/.git/config -- never walks upward (an upward walk
// would leak the enclosing (this template's own) repo's remote into fixture
// goldens run from a nested checkout). No remote configured (e.g. a fresh
// `git init` with no `git remote add`, as every test fixture stages) -> null,
// and every nodeUrl is simply omitted.
function githubBlobBase(workspaceRoot) {
  let raw;
  try { raw = fs.readFileSync(path.join(workspaceRoot, '.git', 'config'), 'utf8'); } catch { return null; }
  const section = raw.match(/\[remote "origin"\]([^[]*)/);
  if (!section) return null;
  const urlLine = section[1].match(/^\s*url\s*=\s*(\S+)\s*$/m);
  if (!urlLine) return null;
  const url = urlLine[1].trim();
  let m = url.match(/^git@github\.com:([^/]+)\/(.+?)(\.git)?$/);
  if (!m) m = url.match(/^https?:\/\/github\.com\/([^/]+)\/([^/]+?)(\.git)?\/?$/);
  if (!m) return null;
  // Link only to a branch that exists on the remote -- never assume `main`
  // (a repo on `master`, or one never pushed, would get dead links).
  const branch = pushedBranch(workspaceRoot);
  if (!branch) return null;
  return `https://github.com/${m[1]}/${m[2]}/blob/${branch}/`;
}

// The current branch (from .git/HEAD), only if origin has it: a loose ref
// under refs/remotes/origin/ or a line in packed-refs. Detached HEAD or a
// branch never pushed -> null.
function pushedBranch(workspaceRoot) {
  const gitDir = path.join(workspaceRoot, '.git');
  let head;
  try { head = fs.readFileSync(path.join(gitDir, 'HEAD'), 'utf8').trim(); } catch { return null; }
  const hm = head.match(/^ref:\s*refs\/heads\/(.+)$/);
  if (!hm) return null;
  const branch = hm[1];
  if (fs.existsSync(path.join(gitDir, 'refs', 'remotes', 'origin', ...branch.split('/')))) return branch;
  let packed = '';
  try { packed = fs.readFileSync(path.join(gitDir, 'packed-refs'), 'utf8'); } catch { return null; }
  return packed.split('\n').some((l) => l.trim().endsWith(` refs/remotes/origin/${branch}`)) ? branch : null;
}

// Paths under registry/ that exist on origin/<branch>. Needs the git binary;
// any failure (no git, no such ref) -> null, and every nodeUrl is omitted
// rather than risking a dead link.
function pushedFiles(workspaceRoot, branch) {
  if (!branch) return null;
  try {
    const out = require('child_process').execFileSync(
      'git', ['ls-tree', '-r', '--name-only', `origin/${branch}`, '--', 'registry'],
      { cwd: workspaceRoot, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
    return new Set(out.split('\n').filter(Boolean));
  } catch { return null; }
}

// --- Bundle classification (mirrors lint-registry.js's own grouping) -------
function classify(nodes) {
  const concepts = [];
  for (const [relPath, node] of nodes) {
    const base = path.posix.basename(relPath);
    if (base === 'index.md') continue;
    if (lib.RESERVED.has(base)) continue; // SCHEMA.md, log.md
    concepts.push(node);
  }
  const kindOf = (n) => lib.DIR_TYPES[n.relPath.split('/')[1]];
  const byKind = (type) => concepts.filter((c) => kindOf(c) === type);
  return { concepts, byKind };
}

// --- Skills/agents scan (workspace layer -- never duplicated into the bundle) ---
function scanSkillsAndAgents(workspaceRoot) {
  const skills = [];
  const agents = [];
  for (const p of lib.scanCapabilities(workspaceRoot)) {
    let raw;
    try { raw = lib.normalizeLineEndings(fs.readFileSync(path.join(workspaceRoot, p), 'utf8')); } catch { continue; } // broken symlink, unreadable
    const fields = lib.parseCapabilityFrontmatter(raw);
    const isSkill = p.endsWith('/SKILL.md');
    const rec = {
      id: isSkill ? path.posix.basename(path.posix.dirname(p)) : path.posix.basename(p).replace(/\.md$/, ''),
      title: (fields && (fields.name || fields.title)) || undefined,
      description: oneLine(fields && fields.description) || '',
      quickStartPrompt: oneLine(fields && (fields.quick_start_prompt || fields.quickstart_prompt)) || undefined,
      path: p,
    };
    (isSkill ? skills : agents).push(rec);
  }
  skills.sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
  agents.sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
  return { skills, agents };
}

// Progress: the routing state's NAME, read from the workflow's folder by the
// framework-state script -- never from which links a node has, never a number.
// State 0's one name covers two different things, so the views split it by the
// script's kind: "Runs outside the framework" for running work Analyze recorded
// (in-production, no folder), "Retired" for a retired workflow.
// The folder is <framework folder>/<slug>/ (framework/<slug>/ in a workspace,
// <slug>/ beside registry/ on the web and Claude desktop). Anything the script
// can't read or settle -> undefined, and the views leave progress blank rather
// than guess. Deterministic: framework-state reads files only.
const STATE_0_LABELS = { 'running-work': 'Runs outside the framework', retired: 'Retired' };
function workflowProgress(w, frameworkDir, absBundle) {
  if (!frameworkDir) return undefined;
  try {
    const r = workflowState(path.join(frameworkDir, lib.slugOf(w.relPath)), { registryDir: absBundle });
    if (r && r.state === 0) return STATE_0_LABELS[r.kind];
    return r && typeof r.name === 'string' ? r.name : undefined;
  } catch {
    return undefined;
  }
}

// --- Compose (build everything in memory; caller decides what to do with it) ---
function compose(bundleDir) {
  const dir = bundleDir || 'registry';
  const absBundle = path.resolve(dir);
  const workspaceRoot = path.dirname(absBundle);
  const outputs = new Map(); // absolute path -> content

  const { nodes } = lib.loadBundle(dir);
  const byPath = nodes;
  const { byKind } = classify(nodes);

  const businesses = byKind('Business').slice().sort(cmpPath);
  const functionsAll = byKind('Function').slice().sort(cmpPath);
  const processesAll = byKind('Process').slice().sort(cmpPath);
  const workflowsAll = byKind('Workflow').slice().sort(cmpPath);
  const notesAll = byKind('Note').slice().sort(cmpPath);

  const business = businesses[0]; // single-business model (SCHEMA "traversal root")
  const lobOrder = business ? lib.orderedLinks(business.sections['Lines of Business'] || '').map((l) => l.href) : [];
  const lobs = lobOrder.map((h) => byPath.get(h)).filter(Boolean);

  const processesOfLob = (lob) => lib.orderedLinks(lob.sections['Processes'] || '').map((l) => byPath.get(l.href)).filter(Boolean);
  const membersOfProcess = (p) => lib.orderedLinks(p.sections['Workflows'] || '').map((l) => byPath.get(l.href)).filter(Boolean);

  const { skills, agents } = scanSkillsAndAgents(workspaceRoot);

  // No framework folder yet (a fresh workspace): every workflow has no folder,
  // which the routing rule reads the same from the workspace.
  const fwDir = lib.frameworkFolder(workspaceRoot).dir;
  const frameworkDir = fwDir && fs.existsSync(fwDir) ? fwDir : (fwDir ? workspaceRoot : null);
  const progress = new Map(workflowsAll.map((w) => [w.relPath, workflowProgress(w, frameworkDir, absBundle)]));

  // Workflow -> Skill/Agent is the Workflow node's `# Skills` / `# Agents`
  // body links (SCHEMA.md "Relationships"); usedBy is the reverse view.
  const usedBy = new Map(); // asset workspace path -> [workflow node]
  for (const w of workflowsAll) {
    const links = lib.orderedLinks(w.sections['Skills'] || '').concat(lib.orderedLinks(w.sections['Agents'] || ''));
    for (const l of links) {
      const key = l.href.replace(/^\.\//, '');
      if (!usedBy.has(key)) usedBy.set(key, []);
      usedBy.get(key).push(w);
    }
  }
  const usedByLinkText = (assetPath) => {
    const ws = usedBy.get(assetPath) || [];
    return ws.map((w) => `[${nodeTitle(w)}](registry${w.relPath})`).join(', ');
  };

  const absPathOf = (relPath) => path.join(absBundle, relPath.replace(/^\//, ''));
  const setIfChanged = (file, content) => {
    const current = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
    if (current !== content) outputs.set(file, content);
  };

  // --- Rewrite Function `# Owns` GENERATED blocks (reverse view of Process.owner) ---
  for (const fn of functionsAll) {
    const slug = lib.slugOf(fn.relPath);
    const owned = processesAll.filter((p) => p.fm && p.fm.owner === slug).slice().sort(cmpPath);
    const content = owned.map((p) => `- [${nodeTitle(p)}](${p.relPath})`).join('\n');
    const { raw, replaced } = lib.replaceGeneratedBlock(fn.raw, 'owns', content);
    if (replaced && raw !== fn.raw) setIfChanged(absPathOf(fn.relPath), raw);
  }

  // --- Rewrite Workflow `# Insights` GENERATED blocks (reverse view of a
  // Note's body links -- SCHEMA.md "Relationships": "Insight -> Workflow/
  // Process ... the Note's body links" is the single home of the edge; this
  // is its derived reverse view, same architecture as Function `# Owns`
  // above). notesAll is already code-point sorted, so iteration order (and
  // therefore emitted bullet order) is deterministic.
  for (const w of workflowsAll) {
    const linking = notesAll.filter((n) => lib.classifyLinks(n.raw).inBundle.includes(w.relPath));
    const content = linking.map((n) => `- [${nodeTitle(n)}](${n.relPath}) — ${n.fm.description}`).join('\n');
    const { raw, replaced } = lib.replaceGeneratedBlock(w.raw, 'insights', content);
    if (replaced && raw !== w.raw) setIfChanged(absPathOf(w.relPath), raw);
  }

  // --- Rewrite root index.md's skills/agents inventory GENERATED blocks -----
  const rootIndexPath = '/index.md';
  const rootIndex = byPath.get(rootIndexPath);
  if (rootIndex) {
    let raw = rootIndex.raw;
    const skillLines = skills.map((s) => {
      const used = usedByLinkText(s.path);
      return `- [${s.id}](${s.path}) — ${s.description}${used ? ` (used by: ${used})` : ''}`;
    });
    ({ raw } = lib.replaceGeneratedBlock(raw, 'skills', `## Skills inventory (${skills.length})\n${skillLines.join('\n')}`));
    const agentLines = agents.map((a) => {
      const used = usedByLinkText(a.path);
      return `- [${a.id}](${a.path}) — ${a.description}${used ? ` (used by: ${used})` : ''}`;
    });
    ({ raw } = lib.replaceGeneratedBlock(raw, 'agents', `## Agents inventory (${agents.length})\n${agentLines.join('\n')}`));
    if (raw !== rootIndex.raw) setIfChanged(absPathOf(rootIndexPath), raw);
  }

  // --- Refresh plain directory index.md bullet lists (index-coverage view) --
  for (const [dirName, title] of Object.entries(DIR_TITLES)) {
    const files = byKind(lib.DIR_TYPES[dirName]).slice().sort(cmpPath);
    const lines = [`# ${title}`, ''];
    if (files.length === 0) lines.push(EMPTY_INDEX_BODY);
    else for (const f of files) lines.push(`- [${nodeTitle(f)}](${f.relPath})`);
    setIfChanged(path.join(absBundle, dirName, 'index.md'), lines.join('\n') + '\n');
  }

  // --- REGISTRY.md dashboard --------------------------------------------
  const registryLink = (n) => `[${nodeTitle(n)}](registry${n.relPath})`;
  const wfHeader = ['| Workflow | Status | Progress | How it decides | How it runs | Re-check by |', '|---|---|---|---|---|---|'];
  const wfRow = (w) => `| ${registryLink(w)} | ${dash(w.fm.status)} | ${cell(progress.get(w.relPath))} | ${cell(HOW_IT_DECIDES[w.fm.autonomy])} | ${cell(HOW_IT_RUNS[w.fm.execution_mode])} | ${dash(w.fm.stale_after)} |`;

  const L = [];
  L.push(business ? (business.fm.url ? `# [${business.fm.title}](${business.fm.url})` : `# ${business.fm.title}`) : '# AI Registry');
  L.push('');

  const assigned = new Set();
  if (lobs.length === 0) {
    L.push('_No workflows yet — add a Business, Line of Business, and Process node, then run this again._');
    L.push('');
  }
  for (const lob of lobs) {
    L.push(`## ${lob.fm.title}`);
    L.push('');
    for (const p of processesOfLob(lob)) {
      L.push(`### ${p.fm.title}`);
      L.push('');
      const members = membersOfProcess(p);
      members.forEach((w) => assigned.add(w.relPath));
      L.push(...wfHeader);
      for (const w of members) L.push(wfRow(w));
      L.push('');
    }
  }
  const unassigned = workflowsAll.filter((w) => !assigned.has(w.relPath));
  if (unassigned.length) {
    L.push('## Unassigned');
    L.push('');
    L.push(...wfHeader);
    for (const w of unassigned) L.push(wfRow(w));
    L.push('');
  }

  // Re-check dates -- deterministic ascending stale_after; no "due" computation
  // (today never enters composed output; lint warns when a re-check is due).
  const reviews = workflowsAll
    .filter((w) => w.fm && w.fm.stale_after)
    .slice()
    .sort((a, b) => (a.fm.stale_after < b.fm.stale_after ? -1 : a.fm.stale_after > b.fm.stale_after ? 1 : cmpPath(a, b)));
  L.push('## Re-check dates');
  L.push('');
  if (reviews.length) for (const w of reviews) L.push(`- ${w.fm.stale_after} — ${registryLink(w)}`);
  else L.push('_No re-check dates set._');
  L.push('');

  const inventoryTable = (title, singular, items) => {
    const hasQSP = items.some((i) => i.quickStartPrompt);
    L.push(`## ${title} (${items.length})`);
    L.push('');
    L.push(hasQSP ? `| ${singular} | Description | Used by | Quick Start Prompt |` : `| ${singular} | Description | Used by |`);
    L.push(hasQSP ? '|---|---|---|---|' : '|---|---|---|');
    for (const item of items) {
      const used = dash(usedByLinkText(item.path));
      const row = `| [${item.id}](${item.path}) | ${cell(item.description)} | ${used}`;
      L.push(hasQSP ? `${row} | ${cell(item.quickStartPrompt)} |` : `${row} |`);
    }
    L.push('');
  };
  inventoryTable('Skills', 'Skill', skills);
  inventoryTable('Agents', 'Agent', agents);

  L.push('*Generated from registry/ — do not edit by hand.*');
  setIfChanged(path.join(workspaceRoot, 'REGISTRY.md'), L.join('\n') + '\n');

  // --- Data island ---------------------------------------------------------
  const blobBase = githubBlobBase(workspaceRoot);
  const regPath = (relPath) => 'registry' + relPath;
  // Link only to files that are actually on the remote branch -- a node
  // scaffolded but never committed or pushed would otherwise get a dead link.
  const pushed = blobBase ? pushedFiles(workspaceRoot, pushedBranch(workspaceRoot)) : null;
  const nodeUrl = (p) => (blobBase && pushed && pushed.has(p) ? blobBase + p : undefined);

  const island = { business: null, lobs: [], functions: [], processes: [], workflows: [], notes: [], skills: [], agents: [] };

  if (business) {
    const p = regPath(business.relPath);
    island.business = clean({
      id: lib.slugOf(business.relPath),
      title: business.fm.title,
      description: business.fm.description,
      url: business.fm.url,
      status: business.fm.status,
      nodePath: p,
      nodeUrl: nodeUrl(p),
    });
  }

  for (const lob of lobs) {
    const p = regPath(lob.relPath);
    island.lobs.push(clean({
      id: lib.slugOf(lob.relPath),
      title: lob.fm.title,
      description: lob.fm.description,
      status: lob.fm.status,
      folder: lob.fm.folder,
      processes: processesOfLob(lob).map((pr) => lib.slugOf(pr.relPath)),
      nodePath: p,
      nodeUrl: nodeUrl(p),
    }));
  }

  for (const fn of functionsAll) {
    const p = regPath(fn.relPath);
    const slug = lib.slugOf(fn.relPath);
    const owned = processesAll.filter((pr) => pr.fm && pr.fm.owner === slug).slice().sort(cmpPath);
    island.functions.push(clean({
      id: slug,
      title: fn.fm.title,
      description: fn.fm.description,
      lead: fn.fm.lead,
      owns: owned.map((pr) => lib.slugOf(pr.relPath)),
      nodePath: p,
      nodeUrl: nodeUrl(p),
    }));
  }

  // Processes/workflows in dashboard traversal order (LOB curated -> Process
  // curated -> Workflow curated); code-point order as the fallback for
  // anything a curated list doesn't reach (only possible for a non-error,
  // legitimately-unassigned Workflow -- see SCHEMA.md "Relationships").
  const seenProc = new Set();
  const seenWf = new Set();
  const pushWorkflow = (w, pr, lob) => {
    if (seenWf.has(w.relPath)) return;
    seenWf.add(w.relPath);
    const p = regPath(w.relPath);
    island.workflows.push(clean({
      id: lib.slugOf(w.relPath),
      title: w.fm.title,
      description: w.fm.description,
      status: w.fm.status,
      definitionType: w.fm.definition_type,
      executionMode: w.fm.execution_mode,
      autonomy: w.fm.autonomy,
      trigger: w.fm.trigger,
      staleAfter: w.fm.stale_after,
      processId: pr ? lib.slugOf(pr.relPath) : null,
      lobId: lob ? lib.slugOf(lob.relPath) : null,
      state: progress.get(w.relPath),
      skills: lib.orderedLinks(w.sections['Skills'] || '').map((l) => l.href),
      agents: lib.orderedLinks(w.sections['Agents'] || '').map((l) => l.href),
      nodePath: p,
      nodeUrl: nodeUrl(p),
    }));
  };
  for (const lob of lobs) {
    for (const pr of processesOfLob(lob)) {
      if (seenProc.has(pr.relPath)) continue;
      seenProc.add(pr.relPath);
      const p = regPath(pr.relPath);
      island.processes.push(clean({
        id: lib.slugOf(pr.relPath),
        title: pr.fm.title,
        description: pr.fm.description,
        ownerId: pr.fm.owner,
        lobId: lib.slugOf(lob.relPath),
        guide: pr.fm.guide,
        workflows: membersOfProcess(pr).map((w) => lib.slugOf(w.relPath)),
        nodePath: p,
        nodeUrl: nodeUrl(p),
      }));
      for (const w of membersOfProcess(pr)) pushWorkflow(w, pr, lob);
    }
  }
  for (const w of workflowsAll) pushWorkflow(w, null, null); // unassigned, code-point order

  for (const n of notesAll) {
    const p = regPath(n.relPath);
    island.notes.push(clean({
      id: lib.slugOf(n.relPath),
      title: n.fm.title,
      description: n.fm.description,
      links: lib.classifyLinks(n.raw).inBundle,
      nodePath: p,
      nodeUrl: nodeUrl(p),
    }));
  }

  for (const s of skills) {
    island.skills.push(clean({
      id: s.id,
      title: s.title || s.id,
      description: s.description,
      usedBy: (usedBy.get(s.path) || []).map((w) => lib.slugOf(w.relPath)),
      quickStartPrompt: s.quickStartPrompt,
      nodePath: s.path,
    }));
  }
  for (const a of agents) {
    island.agents.push(clean({
      id: a.id,
      title: a.title || a.id,
      description: a.description,
      usedBy: (usedBy.get(a.path) || []).map((w) => lib.slugOf(w.relPath)),
      quickStartPrompt: a.quickStartPrompt,
      nodePath: a.path,
    }));
  }

  return { outputs, island, workspaceRoot, absBundle };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const check = args.includes('--check');
  const islandOnly = args.includes('--island-only');
  const bundleDir = args.find((a) => !a.startsWith('--')) || 'registry';

  // A null-frontmatter node (missing/unparseable frontmatter) makes compose()
  // itself throw a raw TypeError on an unguarded `.fm.<field>` deref, well
  // before the lint gate below ever runs -- the user would see a stack trace
  // instead of the lint-refusal message. Run lint FIRST in that case and
  // surface its "refusing to emit" report instead; a crash unrelated to a
  // lint-catchable issue (lint comes back clean) is still a real bug and
  // re-thrown rather than swallowed.
  let composed;
  try {
    composed = compose(bundleDir);
  } catch (composeErr) {
    const preErrors = lint(bundleDir).errors;
    if (preErrors.length) {
      for (const e of preErrors) console.error(`ERROR   ${e}`);
      console.error(`compose-registry: refusing to emit — fix ${preErrors.length} lint error(s) first`);
      process.exit(1);
    }
    throw composeErr;
  }
  const { outputs, island, workspaceRoot, absBundle } = composed;

  // Renaming a node leaves stale links/index-coverage gaps behind in the very
  // files compose is about to regenerate (a directory index.md, the root
  // index.md's GENERATED skills/agents inventories). Gating on those deadlocks:
  // compose refuses to emit the file whose regeneration would clear the error.
  // Suppress exactly those two error classes, and only for bundle files this
  // run rewrites; every other error still blocks. The post-emit lint below is
  // the backstop, so a genuine broken link in hand-written content (e.g. a
  // Note's own prose) can never slip through.
  const willRewrite = new Set(
    [...outputs.keys()]
      .filter((f) => f.startsWith(absBundle + path.sep))
      .map((f) => '/' + path.relative(absBundle, f).split(path.sep).join('/'))
  );
  const selfHealing = (e) => {
    const m = /^(\/[^:]+): (?:broken in-bundle link |index coverage -- missing link to )/.exec(e);
    return m !== null && willRewrite.has(m[1]);
  };
  const errors = lint(bundleDir).errors.filter((e) => !selfHealing(e));
  if (errors.length) {
    for (const e of errors) console.error(`ERROR   ${e}`);
    console.error(`compose-registry: refusing to emit — fix ${errors.length} lint error(s) first`);
    process.exit(1);
  }

  if (islandOnly) {
    console.log(JSON.stringify(island, null, 2));
    process.exit(0);
  }

  // `<` is escaped to `\u003c` so the serialized island can never be
  // misread as closing an embedding <script> tag (e.g. a description
  // containing a literal "</script>"). Valid JSON either way -- \u003c is
  // just the unicode escape for "<".
  const escapeForEmbedding = (s) => s.replace(/</g, '\\u003c');

  // Inject into registry-dashboard.html when it exists. Uses the
  // FUNCTION form of .replace() -- a plain `$1${json}$2` template string is
  // unsafe because JSON.stringify output can legitimately contain `$&`,
  // `` $` ``, `$'`, or `$<name>`-shaped substrings, which the string form of
  // .replace() would interpret as replacement-pattern tokens and corrupt.
  const dashboardPath = path.join(workspaceRoot, 'registry-dashboard.html');
  if (fs.existsSync(dashboardPath)) {
    const html = fs.readFileSync(dashboardPath, 'utf8');
    const re = /(<script type="application\/json" id="data">)[\s\S]*?(<\/script>)/;
    if (re.test(html)) {
      const escapedIsland = escapeForEmbedding(JSON.stringify(island));
      const updated = html.replace(re, (_m, open, close) => open + escapedIsland + close);
      if (updated !== html) outputs.set(dashboardPath, updated);
    }
  }

  if (check) {
    if (outputs.size) {
      for (const f of outputs.keys()) console.error(`STALE   ${path.relative(workspaceRoot, f)}`);
      console.error(`compose-registry --check: ${outputs.size} file(s) need regeneration (run: node tools/compose-registry.js)`);
      process.exit(1);
    }
    console.log('compose-registry --check: all derived views current');
    process.exit(0);
  }

  for (const [file, content] of outputs) {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
    console.log(`wrote ${path.relative(workspaceRoot, file)}`);
  }
  if (!outputs.size) console.log('compose-registry: all derived views already current');

  // Backstop: anything suppressed above should have been repaired by the
  // emit. If an error survives regeneration it was never compose's to fix.
  if (outputs.size) {
    const residual = lint(bundleDir).errors;
    if (residual.length) {
      for (const e of residual) console.error(`ERROR   ${e}`);
      console.error(`compose-registry: ${residual.length} lint error(s) remain after regeneration — these need a source fix`);
      process.exit(1);
    }
  }
}

module.exports = { compose };
