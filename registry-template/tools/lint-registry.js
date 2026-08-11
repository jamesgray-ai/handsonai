#!/usr/bin/env node
// registry-template/tools/lint-registry.js
// Lint the AI Registry bundle. See registry/SCHEMA.md.
// Usage: node tools/lint-registry.js [bundleDir]   (default: registry/)
// Exit 0 clean or warnings-only; exit 1 on errors. Zero npm dependencies.
'use strict';
const fs = require('fs');
const path = require('path');
const lib = require('./registry-lib');

function lint(bundleDir) {
  const dir = bundleDir || 'registry';
  const absBundle = path.resolve(dir);
  const workspaceRoot = path.dirname(absBundle);
  const { nodes, errors: loadErrors } = lib.loadBundle(dir);

  const errors = [...loadErrors];
  const warnings = [];
  const today = new Date().toISOString().slice(0, 10);

  const concepts = [];
  const indexes = [];
  for (const [relPath, node] of nodes) {
    const base = path.posix.basename(relPath);
    if (base === 'index.md') { indexes.push(node); continue; }
    if (lib.RESERVED.has(base)) continue; // SCHEMA.md, log.md
    concepts.push(node);
  }

  // Directory-derived "kind" -- classification stays stable even when a
  // node's own `type:` field disagrees with its directory (that disagreement
  // is itself rule 1's error, not a reason to misclassify the node).
  const kindOf = (n) => {
    const topDir = n.relPath.split('/')[1];
    return lib.DIR_TYPES[topDir];
  };

  // 1. Frontmatter parse + directory<->type agreement + required fields +
  //    enums + banned fields + `generated` shape + legacy definition_type.
  for (const c of concepts) {
    const topDir = c.relPath.split('/')[1];
    const expected = lib.DIR_TYPES[topDir];
    if (!expected) { errors.push(`${c.relPath}: unknown bundle directory "${topDir}"`); continue; }
    if (!c.fm) {
      errors.push(c.error
        ? `${c.relPath}: unparseable frontmatter (${c.error})`
        : `${c.relPath}: missing required frontmatter block (file must start with "---")`);
      continue;
    }
    if (c.fm.type !== expected) errors.push(`${c.relPath}: type "${c.fm.type || '(none)'}", expected "${expected}" (directory<->type agreement)`);
    for (const req of ['title', 'description']) {
      if (!c.fm[req]) errors.push(`${c.relPath}: missing required field "${req}"`);
    }
    const generated = c.fm.generated;
    if (generated === undefined) {
      errors.push(`${c.relPath}: missing required frontmatter "generated"`);
    } else if (typeof generated !== 'object' || !generated.by || !generated.at) {
      errors.push(`${c.relPath}: "generated" must be a single-line flow map with "by" and "at"`);
    } else {
      if (!/^\d{4}-\d{2}-\d{2}/.test(generated.at)) errors.push(`${c.relPath}: "generated.at" must start YYYY-MM-DD`);
      if (!/^(human:|process:)\S+$/.test(generated.by)) {
        warnings.push(`${c.relPath}: generated.by "${generated.by}" does not follow the OKF actor convention (human:<id> or process:<skill-name>) -- malformed actor string`);
      }
    }
    if (expected === 'Workflow' && !c.fm.status) errors.push(`${c.relPath}: missing required field "status"`);
    if (expected === 'Process' && !c.fm.owner) errors.push(`${c.relPath}: missing required field "owner" (must reference an existing Function slug)`);

    const enums = Object.assign({}, lib.ENUMS['*'], lib.ENUMS[expected] || {});
    for (const [field, allowed] of Object.entries(enums)) {
      const val = c.fm[field];
      if (val === undefined) continue;
      if (field === 'definition_type' && lib.LEGACY_TOLERATED.includes(val)) {
        warnings.push(`${c.relPath}: definition_type "${val}" is a legacy spelling -- migrate to step-driven/goal-driven`);
        continue;
      }
      if (!allowed.includes(val)) errors.push(`${c.relPath}: ${field} "${val}" not in [${allowed.join(', ')}]`);
    }

    // Banned fields (SCHEMA.md "Deliberately not concept types").
    for (const banned of lib.BANNED_FIELDS) {
      if (c.fm[banned] !== undefined) errors.push(`${c.relPath}: field "${banned}" is banned from nodes (event-fact / derived -- see SCHEMA.md)`);
    }
    if (expected === 'Workflow' && c.fm.owner !== undefined) {
      errors.push(`${c.relPath}: field "owner" is banned from Workflow nodes (ownership lives on Process -- see SCHEMA.md)`);
    }
  }

  // 2. Links: in-bundle first-segment + resolution; repo-relative existence
  //    (with gitignore tolerance for the raw-source layer, e.g. outputs/).
  for (const [relPath, n] of nodes) {
    const links = lib.classifyLinks(n.raw);
    for (const href of links.inBundle) {
      const first = href.split('/')[1];
      const rootFile = ['SCHEMA.md', 'index.md', 'log.md'].includes(first);
      if (!rootFile && !lib.DIR_TYPES[first]) {
        errors.push(`${relPath}: in-bundle link ${href} -- first segment "${first}" is not a bundle directory`);
        continue;
      }
      if (href.endsWith('.md') && !nodes.has(href)) errors.push(`${relPath}: broken in-bundle link ${href}`);
    }
    for (const href of links.repo) {
      const target = path.join(workspaceRoot, href);
      const isDirLink = href.endsWith('/');
      const exists = isDirLink
        ? (fs.existsSync(target) && fs.statSync(target).isDirectory())
        : fs.existsSync(target);
      if (!exists && !lib.isGitIgnored(href, workspaceRoot)) {
        errors.push(`${relPath}: repo link ${href} -- ${isDirLink ? 'directory' : 'file'} not found`);
      }
    }
  }

  const byKind = (type) => concepts.filter((c) => kindOf(c) === type);
  const businesses = byKind('Business');
  const lobs = byKind('LineOfBusiness');
  const processes = byKind('Process');
  const workflows = byKind('Workflow');
  const functions = byKind('Function');
  const notes = byKind('Note');

  // 3. LOB <-> Business membership: every LOB in exactly one Business
  //    curated `# Lines of Business` list (the list is the edge and order).
  const lobMembership = new Map();
  for (const b of businesses) {
    if (!b.fm) continue;
    for (const l of lib.orderedLinks(b.sections['Lines of Business'] || '')) {
      if (!lobMembership.has(l.href)) lobMembership.set(l.href, []);
      lobMembership.get(l.href).push(b.relPath);
    }
  }
  for (const lob of lobs) {
    const members = lobMembership.get(lob.relPath) || [];
    if (members.length === 0) errors.push(`${lob.relPath}: not listed in any Business # Lines of Business list`);
    if (members.length > 1) errors.push(`${lob.relPath}: listed in ${members.length} Business lists (${members.join(', ')}) -- must be exactly one`);
  }

  // 4. Process <-> LOB membership: every Process in exactly one LOB
  //    curated `# Processes` list.
  const processMembership = new Map();
  for (const lob of lobs) {
    if (!lob.fm) continue;
    for (const l of lib.orderedLinks(lob.sections['Processes'] || '')) {
      if (!processMembership.has(l.href)) processMembership.set(l.href, []);
      processMembership.get(l.href).push(lob.relPath);
    }
  }
  for (const p of processes) {
    const members = processMembership.get(p.relPath) || [];
    if (members.length === 0) errors.push(`${p.relPath}: not listed in any LineOfBusiness # Processes list`);
    if (members.length > 1) errors.push(`${p.relPath}: listed in ${members.length} LOB lists (${members.join(', ')}) -- must be exactly one`);
  }
  const lobOfProcess = new Map([...processMembership.entries()].map(([p, ls]) => [p, ls[0]]));

  // 5. Workflow <-> Process membership: every Workflow in exactly one
  //    Process curated `# Workflows` list (the edge AND value-chain order).
  const workflowMembership = new Map();
  for (const p of processes) {
    if (!p.fm) continue;
    for (const l of lib.orderedLinks(p.sections['Workflows'] || '')) {
      if (!workflowMembership.has(l.href)) workflowMembership.set(l.href, []);
      workflowMembership.get(l.href).push(p.relPath);
    }
  }
  for (const w of workflows) {
    const procs = workflowMembership.get(w.relPath) || [];
    if (procs.length === 0) {
      if (w.fm && w.fm.status === 'in-production') {
        errors.push(`${w.relPath}: in-production workflow not listed in any Process # Workflows list`);
      } else {
        warnings.push(`${w.relPath}: not listed in any Process # Workflows list (unassigned)`);
      }
      continue;
    }
    if (procs.length > 1) errors.push(`${w.relPath}: listed in ${procs.length} Process lists (${procs.join(', ')}) -- must be exactly one`);
    // LOB-vs-artifact-path sanity: an artifact link outside the derived LOB
    // folder (when the LOB declares one) is a warning, never an error.
    const lobPath = lobOfProcess.get(procs[0]);
    const lobNode = lobPath && nodes.get(lobPath);
    const lobFolder = lobNode && lobNode.fm && lobNode.fm.folder;
    if (lobFolder && w.fm) {
      const folderPrefix = lobFolder.replace(/\/$/, '');
      const repoLinks = lib.classifyLinks(w.raw).repo;
      for (const h of repoLinks) {
        if (h.startsWith('sops/') || h.startsWith('outputs/')) continue; // shared workspace layers
        if (!h.startsWith(folderPrefix)) {
          warnings.push(`${w.relPath}: artifact link ${h} outside derived LOB folder ${lobFolder}`);
          break;
        }
      }
    }
  }

  // 6. Process ownership -> Function resolution; Function retirement
  //    warning; Function `# Owns` GENERATED block presence + content sync
  //    (this bundle has no compose-time hash, so a mismatch between the
  //    block's content and the derivable owners list is how "hand-edited"
  //    content is caught -- see registry-lib.js's GENERATED-block comment).
  const fnSlugs = new Set(functions.map((f) => lib.slugOf(f.relPath)));
  const ownersByFunction = new Map(); // function slug -> [process node]
  for (const p of processes) {
    if (!p.fm) continue;
    const owner = p.fm.owner;
    if (!owner) continue; // already an error above (missing required field)
    if (!fnSlugs.has(owner)) {
      errors.push(`${p.relPath}: owner "${owner}" does not resolve to registry/functions/${owner}.md`);
      continue;
    }
    if (!ownersByFunction.has(owner)) ownersByFunction.set(owner, []);
    ownersByFunction.get(owner).push(p);
  }
  for (const f of functions) {
    const fSlug = lib.slugOf(f.relPath);
    const owned = (ownersByFunction.get(fSlug) || []).slice().sort((a, b) => (a.relPath < b.relPath ? -1 : a.relPath > b.relPath ? 1 : 0));
    if (owned.length === 0) warnings.push(`${f.relPath}: function owns no processes -- retire or assign`);
    const blocks = lib.findGeneratedBlocks(f.raw).filter((b) => b.name === 'owns');
    if (blocks.length === 0) {
      errors.push(`${f.relPath}: missing GENERATED:owns block for # Owns (compose can't fill what doesn't exist -- add the marker)`);
      continue;
    }
    const block = blocks[0];
    if (block.unterminated) {
      errors.push(`${f.relPath}: GENERATED:owns block missing <!-- /GENERATED --> terminator`);
      continue;
    }
    const expectedContent = owned.map((p) => `- [${p.fm && p.fm.title ? p.fm.title : lib.slugOf(p.relPath)}](${p.relPath})`).join('\n');
    if (block.content.trim() !== expectedContent.trim()) {
      errors.push(`${f.relPath}: GENERATED:owns # Owns content was hand-edited or is stale (does not match the derived owners list) -- recompose instead of editing between the markers`);
    }
  }

  // 7. Orphan capabilities: skills/agents in the workspace referenced by no
  //    Workflow node. A single summary warning keeps lint scannable.
  const referencedCapabilities = new Set();
  for (const w of workflows) {
    for (const href of lib.classifyLinks(w.raw).repo) referencedCapabilities.add(href.replace(/\/$/, ''));
  }
  const orphanCaps = lib.scanCapabilities(workspaceRoot).filter((c) => !referencedCapabilities.has(c));
  if (orphanCaps.length) {
    warnings.push(`${orphanCaps.length} orphan skill(s)/agent(s) referenced by no Workflow node (${orphanCaps.join(', ')}) -- capture the workflow(s) that use them`);
  }

  // 8. Claims sweep: every SOP and outputs/<slug>/ folder claimed by exactly
  //    one Workflow node's # Artifacts links; run-log evidence must not
  //    contradict status.
  const claims = new Map(); // repo path (no trailing slash) -> [workflow relPaths]
  for (const w of workflows) {
    for (const href of lib.classifyLinks(w.raw).repo) {
      const key = href.replace(/\/$/, '');
      if (!claims.has(key)) claims.set(key, []);
      claims.get(key).push(w.relPath);
    }
  }
  const wfSlugs = new Set(workflows.map((w) => lib.slugOf(w.relPath)));
  for (const sop of lib.scanSops(workspaceRoot)) {
    const claimedBy = claims.get(sop.path) || [];
    if (claimedBy.length === 0) errors.push(`${sop.path}: SOP not claimed by any Workflow node's # Artifacts links (claims sweep)`);
    if (claimedBy.length > 1) errors.push(`${sop.path}: SOP claimed by ${claimedBy.length} Workflow nodes (${claimedBy.join(', ')}) -- claims sweep requires exactly one`);

    // 9. SOP frontmatter back-pointer agreement.
    const { fields: sopFm } = lib.parseFrontmatter(sop.raw);
    const backPtr = sopFm && sopFm.workflow;
    if (claimedBy.length === 1 && backPtr) {
      const claimingSlug = lib.slugOf(claimedBy[0]);
      if (backPtr !== claimingSlug) {
        errors.push(`${sop.path}: workflow: back-pointer "${backPtr}" disagrees with claiming node ${claimedBy[0]} (back-pointer mismatch)`);
      }
    }
  }
  for (const folder of lib.scanOutputsFolders(workspaceRoot)) {
    const claimedByLink = [...claims.keys()].some((k) => k === folder.path || k.startsWith(folder.path + '/'));
    const claimedBySlug = wfSlugs.has(folder.slug);
    if (!claimedByLink && !claimedBySlug) {
      warnings.push(`${folder.path}/: outputs folder not claimed by any Workflow node`);
    }
    if (folder.hasRuns && lib.runsHasEntries(workspaceRoot, folder.slug)) {
      const node = workflows.find((w) => lib.slugOf(w.relPath) === folder.slug);
      if (node && node.fm && node.fm.status && node.fm.status !== 'in-production') {
        errors.push(`${node.relPath}: status "${node.fm.status}" contradicts run log evidence (${folder.path}/runs.md has entries)`);
      }
    }
  }

  // 10. GENERATED block integrity sweep (structural, across every node).
  for (const [relPath, n] of nodes) {
    for (const b of lib.findGeneratedBlocks(n.raw)) {
      if (b.unterminated && !(kindOf(n) === 'Function' && b.name === 'owns')) {
        // Function `# Owns` unterminated blocks are already reported above
        // with a more specific message; avoid a duplicate here.
        errors.push(`${relPath}: GENERATED:${b.name} block missing <!-- /GENERATED --> terminator`);
      }
    }
  }

  // 11. Freshness warnings.
  for (const w of workflows) {
    if (!w.fm) continue;
    if (w.fm.stale_after && w.fm.stale_after <= today) warnings.push(`${w.relPath}: stale_after ${w.fm.stale_after} is past -- review due`);
    if (w.fm.status === 'backlog') {
      const t = lib.lastChanged(w.fm);
      if (t) {
        const age = (Date.parse(today) - Date.parse(t)) / 86400000;
        if (age > 183) warnings.push(`${w.relPath}: backlog for ${Math.round(age)} days -- triage or retire`);
      }
    }
  }

  // 12. Index coverage: every directory index.md links every concept file
  // (and every subdirectory index) in its directory; every directory that
  // holds concept nodes has an index.md.
  for (const idx of indexes) {
    const dirRel = path.posix.dirname(idx.relPath);
    const linked = new Set(lib.classifyLinks(idx.raw).inBundle);
    const absDir = path.join(absBundle, dirRel === '/' ? '.' : dirRel.slice(1));
    let entries;
    try { entries = fs.readdirSync(absDir); } catch { entries = []; }
    for (const name of entries) {
      const full = path.join(absDir, name);
      if (fs.statSync(full).isDirectory()) {
        const subIdx = path.posix.join(dirRel === '/' ? '/' : dirRel, name, 'index.md');
        if (nodes.has(subIdx) && !linked.has(subIdx)) errors.push(`${idx.relPath}: index coverage -- missing link to ${name}/index.md`);
        continue;
      }
      if (!name.endsWith('.md') || lib.RESERVED.has(name)) continue;
      const target = path.posix.join(dirRel === '/' ? '/' : dirRel, name);
      if (!linked.has(target)) errors.push(`${idx.relPath}: index coverage -- missing link to ${name}`);
    }
  }
  const dirsWithConcepts = new Set(concepts.map((c) => path.posix.dirname(c.relPath)));
  for (const d of dirsWithConcepts) {
    if (!nodes.has(path.posix.join(d, 'index.md'))) errors.push(`${d}: missing index.md (index coverage)`);
  }

  // Notes linking no bundle node are probably misfiled.
  for (const n of notes) {
    if (lib.classifyLinks(n.raw).inBundle.length === 0) warnings.push(`${n.relPath}: Note links no bundle nodes -- probably misfiled`);
  }

  return { errors, warnings };
}

if (require.main === module) {
  const bundleDir = process.argv[2] || 'registry';
  const { errors, warnings } = lint(bundleDir);
  for (const w of warnings) console.log(`WARN  ${w}`);
  for (const e of errors) console.log(`ERROR ${e}`);
  console.log(`lint-registry: ${errors.length} error(s), ${warnings.length} warning(s)`);
  process.exit(errors.length ? 1 : 0);
}

module.exports = { lint };
