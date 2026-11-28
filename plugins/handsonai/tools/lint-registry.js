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
  // OKF v0.3 §6 / §12.1: a bundle that declares no okf_version, or one below
  // 0.3, keeps the 0.2 reading of a bare link (from the registry's parent folder).
  const okfVersion = lib.okfVersionOf(absBundle);
  const legacy = lib.isLegacyVersion(okfVersion);
  const linkOpts = { legacy, bundleName: path.basename(absBundle) };
  const linksOf = (n) => lib.classifyLinks(n.raw, n.relPath, linkOpts);
  // A resolved outside link's path from the working folder: what it reaches
  // (with the 0.2 framework/ fallback for a 0.2-form link), else as written.
  const reachOf = (l) => lib.resolveOutside(l, workspaceRoot) || l.path;

  const errors = [...loadErrors];
  const warnings = [];
  const today = new Date().toISOString().slice(0, 10);
  const now = Date.now();
  if (legacy) {
    warnings.push(`registry is OKF ${okfVersion ? okfVersion : '0.2 (index.md declares no okf_version)'} -- say "upgrade my registry" to move it to 0.3 (node tools/upgrade-registry.js), which changes only the form, never the content`);
  }

  const concepts = [];
  const indexes = [];
  for (const [relPath, node] of nodes) {
    const base = path.posix.basename(relPath);
    if (base === 'index.md') { indexes.push(node); continue; }
    if (lib.RESERVED.has(base)) continue; // SCHEMA.md, log.md
    if (!lib.isConcept(node)) {
      // OKF v0.3 §3.2: not a concept; a validator warns, and every check skips it.
      warnings.push(`${relPath}: no frontmatter, so not a registry page -- skipped (add type, title, description and generated if it should be one)`);
      continue;
    }
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
  //    enums + banned fields + `generated` shape + legacy definition_type +
  //    legacy artifact labels (tolerated on older nodes, never written).
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
    for (const k of (lib.parseFrontmatter(c.raw).duplicates || [])) {
      warnings.push(`${c.relPath}: frontmatter key "${k}" appears more than once -- the last value is read (OKF v0.3 §4: write each key once)`);
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
      // A UTC instant; a bare date is accepted on an older node (SCHEMA.md "Frontmatter").
      if (!lib.AT_INSTANT.test(generated.at) && !lib.AT_DATE.test(generated.at)) {
        errors.push(`${c.relPath}: "generated.at" must be a UTC instant (YYYY-MM-DDTHH:MM:SSZ), or a bare YYYY-MM-DD date on an older node`);
      }
      if (!lib.isActor(generated.by)) {
        warnings.push(`${c.relPath}: generated.by "${generated.by}" does not follow the OKF actor convention (process:<skill-name>, human:<id>, or <app>/<model id>) -- malformed actor string`);
      }
    }
    if (expected === 'Workflow' && !lib.stateOf(c.fm)) errors.push(`${c.relPath}: missing required field "state"`);
    if (expected === 'Process' && !c.fm.owner) errors.push(`${c.relPath}: missing required field "owner" (must reference an existing Function slug)`);

    // Domain state and lifecycle (OKF v0.3 §5.4; SCHEMA.md "Domain state and lifecycle").
    const hasStateField = c.fm.state !== undefined && c.fm.state !== null && String(c.fm.state) !== '';
    if (hasStateField && !lib.STATE_TYPES.has(expected)) {
      errors.push(`${c.relPath}: field "state" belongs on Workflow, Business and LineOfBusiness nodes`);
    }
    const status = c.fm.status === undefined || c.fm.status === null || String(c.fm.status) === '' ? null : String(c.fm.status);
    if (status && !lib.LIFECYCLE_STATUS.includes(status)) {
      // A 0.2 registry keeps domain state in status: still read (stateOf), never an error there.
      // Before 0.3 nothing checked status on a Process, Function or Note, so a 0.2 registry
      // never gets a new error for it.
      const oldForm = legacy && !hasStateField;
      if (!oldForm) {
        if (lib.STATE_TYPES.has(expected) && !hasStateField && ((lib.ENUMS[expected] || {}).state || []).includes(status)) {
          errors.push(`${c.relPath}: status "${status}" is domain state -- write it as state: ${status}${status === 'retired' ? ' and status: deprecated' : ''} (status is the lifecycle: draft, stable or deprecated; OKF v0.3 §5.4)`);
        } else {
          errors.push(`${c.relPath}: status "${status}" not in [draft, stable, deprecated]${status === 'retired' ? ` -- a retired ${expected} is status: deprecated` : ''}`);
        }
      }
    }
    if (hasStateField && String(c.fm.state) === 'retired' && status !== 'deprecated') {
      errors.push(`${c.relPath}: state "retired" needs status: deprecated (OKF v0.3 §5.4)`);
    }
    if (c.fm.superseded_by !== undefined && c.fm.superseded_by !== '') {
      const r = lib.resolveHref(String(c.fm.superseded_by), c.relPath, linkOpts);
      if (r.kind !== 'bundle' || !nodes.has(r.path)) errors.push(`${c.relPath}: superseded_by ${c.fm.superseded_by} -- no such concept in this bundle`);
      if (status !== 'deprecated') warnings.push(`${c.relPath}: superseded_by without status: deprecated -- it means something only on a deprecated node (OKF v0.3 §5.4)`);
    }

    // stale_after (§5.5): a date (the start of that UTC day) or a UTC instant; one that doesn't
    // parse is never read as fresh.
    if (c.fm.stale_after !== undefined && c.fm.stale_after !== null && String(c.fm.stale_after) !== '' && lib.toMillis(c.fm.stale_after) === null) {
      (legacy ? warnings : errors).push(`${c.relPath}: stale_after "${c.fm.stale_after}" is not a date (YYYY-MM-DD) or a UTC instant -- never read as fresh (OKF v0.3 §5.5)`);
    }

    // verified (§5.2-5.3): events need both by and at; a check counts only while it is current.
    if (c.fm.verified !== undefined && c.fm.verified !== null && c.fm.verified !== '') {
      const raw = Array.isArray(c.fm.verified) ? c.fm.verified : [c.fm.verified];
      if (raw.some((e) => !e || typeof e !== 'object' || !e.by || !e.at)) warnings.push(`${c.relPath}: verified event without both by and at is ignored (OKF v0.3 §5.2)`);
      const events = lib.verifiedEvents(c.fm);
      for (const e of events) {
        if (lib.toMillis(e.at) === null) warnings.push(`${c.relPath}: verified at "${e.at}" is not a date or a UTC instant`);
        if (!lib.isActor(e.by)) warnings.push(`${c.relPath}: verified by "${e.by}" does not follow the OKF actor convention`);
      }
      const genAt = generated && typeof generated === 'object' ? lib.toMillis(generated.at) : null;
      const times = events.map((e) => lib.toMillis(e.at)).filter((t) => t !== null);
      if (genAt !== null && times.length && times.every((t) => t < genAt)) {
        const latest = events.reduce((a, e) => (lib.toMillis(e.at) > lib.toMillis(a.at) ? e : a));
        warnings.push(`${c.relPath}: verified before the last change (${latest.at} < generated.at ${generated.at}) -- unverified until someone checks it again (OKF v0.3 §5.3)`);
      }
    }

    const enums = Object.assign({}, lib.ENUMS['*'], lib.ENUMS[expected] || {});
    for (const [field, allowed] of Object.entries(enums)) {
      const val = field === 'state' ? (lib.stateOf(c.fm) ?? undefined) : c.fm[field];
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
    // big_change ("[reason], [date]") marks a pending redo; it belongs on a Workflow only.
    // OKF v0.3 §11.2: an empty or null value is the same as an absent key.
    if (c.fm.big_change !== undefined && c.fm.big_change !== null && String(c.fm.big_change).trim() !== '') {
      if (expected !== 'Workflow') errors.push(`${c.relPath}: field "big_change" belongs on Workflow nodes only`);
      else if (typeof c.fm.big_change !== 'string' || !c.fm.big_change.trim()) errors.push(`${c.relPath}: "big_change" must give the reason and the date ("[reason], [date]")`);
    }

    // Legacy artifact labels ("Design spec", "Run guide", "Improvement plan") are
    // tolerated on older nodes -- those whose generated.at is a bare date -- and never
    // written: a node stamped with a UTC instant that carries one was written by a
    // current step, which must not write it.
    if (expected === 'Workflow' && generated && typeof generated === 'object' && lib.AT_INSTANT.test(generated.at || '')) {
      const legacy = lib.artifactLabels(c).filter((l) => lib.LEGACY_LABELS.some((x) => x.toLowerCase() === l.toLowerCase()));
      if (legacy.length) {
        errors.push(`${c.relPath}: legacy artifact label(s) ${legacy.map((l) => `"${l}"`).join(', ')} written on a current node -- use "Design plan" or "Test results"; legacy labels are tolerated only on older nodes`);
      }
    }
  }

  // 2. Links: in-bundle first-segment + resolution; repo-relative existence
  //    (with gitignore tolerance for a workflow's own output, e.g. outputs/).
  //    A repo link resolves as written, else through framework/ (an old
  //    relative link; lib.resolveRepoLink).
  for (const [relPath, n] of nodes) {
    for (const l of linksOf(n).links) {
      if (l.kind === 'bundle' && l.form === 'relative') {
        // Spec-valid, but this profile writes in-bundle links root-relative. In a 0.3 bundle a link
        // written the 0.2 way lands here too: name the file-relative form it meant.
        const asOld = lib.resolveHref(l.href, relPath, { ...linkOpts, legacy: true });
        const reach = asOld.form === 'legacy' ? lib.resolveOutside(asOld, workspaceRoot) : null;
        if (reach) errors.push(`${relPath}: link ${l.href} is read from this file's folder (OKF v0.3) -- write ${lib.linkTo(reach, relPath, linkOpts)}${l.href.replace(/^[^#?]*/, '')}`);
        else errors.push(`${relPath}: in-bundle link ${l.href} -- write it root-relative: ${l.path}`);
        continue;
      }
      if (l.kind === 'bundle') {
        const target = l.path;
        const first = target.split('/')[1];
        const rootFile = ['SCHEMA.md', 'index.md', 'log.md'].includes(first);
        if (!rootFile && !lib.DIR_TYPES[first]) {
          errors.push(`${relPath}: in-bundle link ${l.href} -- first segment "${first}" is not a bundle directory`);
          continue;
        }
        if (target.endsWith('.md') && !nodes.has(target)) errors.push(`${relPath}: broken in-bundle link ${l.href}`);
      } else if (l.kind === 'outside') {
        const isDirLink = l.path.endsWith('/');
        const exists = lib.resolveOutside(l, workspaceRoot) !== null;
        if (!exists && !lib.isGitIgnored(l.path, workspaceRoot)) {
          errors.push(`${relPath}: repo link ${l.href} -- ${isDirLink ? 'directory' : 'file'} not found`);
        }
      }
    }
  }

  const byKind = (type) => concepts.filter((c) => kindOf(c) === type);
  const frameworkFolders = lib.scanFrameworkFolders(workspaceRoot);
  const workflowFolderPaths = frameworkFolders.map((f) => f.path);
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
      if (w.fm && lib.stateOf(w.fm) === 'in-production') {
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
    const lobFolderRaw = lobNode && lobNode.fm && lobNode.fm.folder;
    const lobFolderLink = lobFolderRaw ? lib.resolveHref(String(lobFolderRaw), lobNode.relPath, linkOpts) : null;
    const lobFolder = lobFolderLink && lobFolderLink.kind === 'outside' ? lobFolderLink.path : lobFolderRaw;
    if (lobFolder && w.fm) {
      const folderPrefix = lobFolder.replace(/\/$/, '');
      for (const l of linksOf(w).links.filter((x) => x.kind === 'outside')) {
        // Shared layers: SOPs, a workflow's own output, and the framework folder's
        // workflow folders (framework/ on every platform; the legacy layout with
        // registry/ inside the framework folder still reads <slug>/; an old
        // relative link resolves through framework/).
        const h = reachOf(l);
        if (h.startsWith('sops/') || h.startsWith('outputs/') || h.startsWith('framework/')) continue;
        if (workflowFolderPaths.some((f) => h === f || h.startsWith(f + '/'))) continue;
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
  //    block's content and the derivable owners list is how stale/hand-edited
  //    content is caught -- see registry-lib.js's GENERATED-block comment).
  //    A content mismatch is only a WARNING: Phase 4 of scaffolding names
  //    Process owners before Phase 5's maintenance pass regenerates Owns,
  //    so a stale block is an expected mid-run state, not a lint blocker.
  //    Missing blocks, unterminated blocks, and missing markers stay errors.
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
      warnings.push(`${f.relPath}: GENERATED:owns content is stale -- run a maintenance pass to regenerate (does not match the derived owners list; Owns is hand-edited or stale)`);
    }
  }

  // 7. Orphan capabilities: skills/agents in the workspace referenced by no
  //    Workflow node. A single summary warning keeps lint scannable.
  const referencedCapabilities = new Set();
  for (const w of workflows) {
    for (const href of linksOf(w).repo) referencedCapabilities.add(href.replace(/\/$/, ''));
  }
  const orphanCaps = lib.scanCapabilities(workspaceRoot).filter((c) => !referencedCapabilities.has(c));
  if (orphanCaps.length) {
    warnings.push(`${orphanCaps.length} orphan skill(s)/agent(s) referenced by no Workflow node (${orphanCaps.join(', ')}) -- capture the workflow(s) that use them`);
  }

  // 8. Claims sweep: every SOP and workflow folder claimed by exactly one
  //    Workflow node's # Artifacts links; run-log evidence must not
  //    contradict status.
  const claims = new Map(); // repo path (no trailing slash) -> [workflow relPaths]
  for (const w of workflows) {
    // Dedupe per workflow first -- a workflow linking the same repo path
    // twice in its prose (e.g. once in `# Artifacts`, once in free text) is
    // one claim, not two, so it must never register as "claimed by 2
    // Workflow nodes" against itself.
    // An old relative link claims what it resolves to through framework/.
    const keysInThisWorkflow = new Set(linksOf(w).links.filter((l) => l.kind === 'outside')
      .map((l) => reachOf(l).replace(/\/$/, '')));
    for (const key of keysInThisWorkflow) {
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
  for (const folder of frameworkFolders) {
    const claimedByLink = [...claims.keys()].some((k) => k === folder.path || k.startsWith(folder.path + '/'));
    if (!claimedByLink && !wfSlugs.has(folder.slug)) {
      warnings.push(`${folder.path}/: framework folder not claimed by any Workflow node`);
    }
  }
  // Run log evidence must not contradict status. The run log lives where the workflow
  // runs, never in the framework folder; it is read through the node's "Run log" link,
  // and only where that link resolves inside the registry's parent folder. An external
  // or absent "Run log" link is skipped.
  for (const w of workflows) {
    const st = w.fm && lib.stateOf(w.fm);
    if (!st || st === 'in-production' || st === 'retired') continue;
    for (const l of lib.orderedLinks(w.sections['Artifacts'] || '')) {
      if (l.title.trim().toLowerCase() !== 'run log') continue;
      const r = lib.resolveHref(l.href, w.relPath, linkOpts);
      // Read only where the link reaches a file inside the working folder.
      if (r.kind !== 'outside' || r.path.split('/').includes('..')) continue;
      if (lib.runLogHasEntries(path.join(workspaceRoot, r.path))) {
        errors.push(`${w.relPath}: state "${st}" contradicts run log evidence (${l.href} has entries)`);
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
    const dueAt = w.fm.stale_after ? lib.toMillis(w.fm.stale_after) : null;
    if (dueAt !== null && now >= dueAt && lib.stateOf(w.fm) !== 'retired') warnings.push(`${w.relPath}: stale_after ${w.fm.stale_after} is past -- re-check due`);
    if (lib.stateOf(w.fm) === 'backlog') {
      const t = lib.lastChanged(w.fm);
      if (t) {
        const age = (Date.parse(today) - Date.parse(t)) / 86400000;
        if (age > 183) warnings.push(`${w.relPath}: backlog for ${Math.round(age)} days -- triage or retire`);
      }
    }
  }

  // 11b. Index frontmatter (OKF v0.3 §8, §8.1): only the bundle root's index.md carries any, and
  // only bundle metadata (okf_version, title, description, license) or an x- extension key.
  for (const idx of indexes) {
    if (!idx.fm) continue;
    if (idx.relPath !== '/index.md') { warnings.push(`${idx.relPath}: a subdirectory index.md carries no frontmatter (OKF v0.3 §8)`); continue; }
    for (const k of Object.keys(idx.fm)) {
      if (!['okf_version', 'title', 'description', 'license'].includes(k) && !k.startsWith('x-')) {
        warnings.push(`/index.md: frontmatter key "${k}" is not bundle metadata (okf_version, title, description, license, or an x- key; OKF v0.3 §8.1)`);
      }
    }
  }
  // 11c. log.md (OKF v0.3 §9): `## YYYY-MM-DD` headings, newest first, no frontmatter.
  const logNode = nodes.get('/log.md');
  if (logNode && !legacy) {
    const lines = logNode.raw.split('\n');
    const heads = lines.filter((l) => /^## /.test(l));
    const dates = heads.map((l) => (l.match(/^## (\d{4}-\d{2}-\d{2})\s*$/) || [])[1]);
    const ordered = dates.every((d, i) => d && (i === 0 || d <= dates[i - 1]));
    if (logNode.fm || lines.some((l) => /^\d{4}-\d{2}-\d{2}: /.test(l)) || !ordered) {
      warnings.push('/log.md: log.md is not in the OKF v0.3 §9 form (`## YYYY-MM-DD` headings, newest date first, entries as bullets) -- the upgrade (node tools/upgrade-registry.js) regroups it');
    }
  }

  // 12. Index coverage: every directory index.md links every concept file
  // (and every subdirectory index) in its directory; every directory that
  // holds concept nodes has an index.md.
  for (const idx of indexes) {
    const dirRel = path.posix.dirname(idx.relPath);
    const linked = new Set(linksOf(idx).inBundle);
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
      if (!lib.isConcept(nodes.get(target))) continue; // not a page (no frontmatter): needs no index entry
      if (!linked.has(target)) errors.push(`${idx.relPath}: index coverage -- missing link to ${name}`);
    }
  }
  const dirsWithConcepts = new Set(concepts.map((c) => path.posix.dirname(c.relPath)));
  for (const d of dirsWithConcepts) {
    if (!nodes.has(path.posix.join(d, 'index.md'))) errors.push(`${d}: missing index.md (index coverage)`);
  }

  // Notes linking no bundle node are probably misfiled.
  for (const n of notes) {
    if (linksOf(n).inBundle.length === 0) warnings.push(`${n.relPath}: Note links no bundle nodes -- probably misfiled`);
  }

  return { errors, warnings };
}

if (require.main === module) {
  const bundleDir = process.argv[2] || 'registry';
  const { errors, warnings } = lint(bundleDir);
  for (const w of warnings) console.log(`WARN  ${w}`);
  for (const e of errors) console.log(`ERROR ${e}`);
  // On GitHub Actions, also post each error as an annotation: the run's summary page then
  // names the file and rule, so a student never has to search the log.
  if (process.env.GITHUB_ACTIONS === 'true') {
    const esc = (s) => s.replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A');
    for (const e of errors) console.log(`::error title=Registry check::${esc(e)}`);
  }
  console.log(`lint-registry: ${errors.length} error(s), ${warnings.length} warning(s)`);
  process.exit(errors.length ? 1 : 0);
}

module.exports = { lint };
