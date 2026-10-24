---
name: indexing-registry
description: >
  This skill should be used to maintain the user's AI Registry — the registry/
  knowledge bundle and its derived views (the REGISTRY.md dashboard, directory
  indexes, GENERATED blocks, and the visual HTML dashboard). Triggers: "update
  my registry", "refresh my registry", "lint my registry", "generate my
  dashboard", "what have I built", "show my AI inventory", after creating
  skills or agents, or when another framework skill's closing step calls for a
  maintenance pass. Also repairs stale or hand-edited derived views. If no
  registry/SCHEMA.md exists, route to the scaffolding-registry skill instead.
---

# Maintaining the AI Registry

The **AI Registry** is the `registry/` knowledge bundle plus everything derived from it: directory indexes, GENERATED blocks inside individual nodes, the `REGISTRY.md` dashboard, and the visual HTML dashboard (always generated at the end of registry setup; once it exists, refreshed on every pass).

**The registry is derived-state doctrine.** The bundle's node files (under `registry/`) are the source of truth. Every dashboard, index, and summary is generated from them. **Edit sources, regenerate — never hand-edit a derived view.** If a derived view looks wrong, fix the source node and regenerate; never patch the view.

For where the bundle is and how nodes are written and owned (resolution, write rules, the field-ownership table, the registry log, how progress and the re-check date are shown, and the full lint rule list), see `references/registry-bundle.md`. This skill assumes that contract; it doesn't restate it. A workflow's progress is never stored: it is read from the workflow's folder by the routing rule, through the `framework-state` script where code can run (`references/tier-2-island.md` has the by-hand reading). Its re-check date is Test's `stale_after`.

## Location & Scope

**One framework folder = one registry.** On Claude Code and Codex the bundle is `registry/` in the workspace, beside `framework/`, `sops/` and `process-guides/`. On Claude desktop it is `registry/` inside the framework folder the leader added. On the web (Claude, ChatGPT) and in Microsoft 365 Copilot it is `Framework/registry/` in the leader's Google Drive or OneDrive, read and written through the platform's connection, by the drive-saving rule in `references/registry-bundle.md`. `REGISTRY.md` and `registry-dashboard.html` sit beside `registry/`, in its parent folder. Only where there are no files and no drive connection that can write does the skill fall back to print-to-save: it gives each file complete with its location for the leader to save, and says plainly what is unsaved. The skill never assumes a Git repository.

> **Terminology:** "AI Registry" always means the `registry/` bundle and the views generated from it. It is unrelated to the framework's *platform registry* (`registries/platform-registry.json`), which catalogs platforms and integrations for the Design and Build skills.

## The maintenance pass

Run all five jobs for a full pass, or just the one the user asked for. Other framework skills invoke this skill from their closing step for the same pass — see **Best-effort rule** below.

### 1. Lint

Read every node against the bundle's `registry/SCHEMA.md` and the rule list in `references/registry-bundle.md` (§8) — that file is the single source; do not duplicate its rule list here. Report findings in plain language, named by file. On a pass called by another step, say nothing unless a fix needs the leader, and then name the workflow or process, never the file. **Offer fixes; never silently repair meaning** — a lint pass corrects mechanical issues (formatting, missing index entries) only with the user's confirmation, and never reinterprets or rewrites a node's content on its own judgment.

### 2. Refresh indexes

Regenerate the typed-directory `index.md` files and the bundle-root inventories (Skills and Agents, each with a "used by" column derived from which Workflow nodes link them).

**Quick Start Prompts.** A Quick Start Prompt is a single copy-paste-ready prompt demonstrating an asset's primary use case. When an asset has no `quick_start_prompt` frontmatter field, generate one and **offer to write it back into the asset's frontmatter** (with the user's confirmation — this is the only write this skill makes outside the bundle and its derived views). Until it's written back, show the generated prompt in the index but note it's unsaved.

**Guidelines:**
- One sentence that triggers the asset's main workflow
- Specific enough to be immediately useful
- Generic enough to work across different contexts
- Should produce a complete result, not just start a conversation

**Examples:**

| Type | Name | Quick Start Prompt |
|------|------|--------------------|
| Skill | reviewing-student-goals | "Review student learning goals from my course platform, update each student's record, and give me a cohort theme analysis." |
| Skill | writing-linkedin-posts | "Write a LinkedIn post about [topic] using my brand voice." |
| Agent | playbook-question-answerer | "Answer the question 'What are the six AI building blocks?' using the Hands-on AI site content." |
| Agent | hbr-editor | "Review this article for HBR publication quality and give me prescriptive feedback." |
| Prompt | meeting-prep-quick | "Prepare me for my meeting with [name] at [company] tomorrow." |

Context files typically don't need a Quick Start Prompt — use `—`. If unsure, ask the user rather than guessing.

### 3. Regenerate GENERATED blocks

Rewrite the content between `<!-- GENERATED:<name> -->` and `<!-- /GENERATED -->` markers: a Workflow node's `# Insights` block, and a Function node's `# Owns` block. Write only inside the markers, never outside them, and never leave a marker pair unterminated.

### 4. Regenerate dashboards

**Tier 1 — `REGISTRY.md` (always, on every pass).** Structure, fixed by the reference example:

- Business header (name, linked if a URL is set)
- One section per line of business, in curated order
- Within each, one subsection per process, each holding a workflow table in value-chain order with status, progress (the routing state's name), "How it decides", "Runs with you" or "Runs without you", and the "Re-check by" date, under the labels in `references/registry-bundle.md` §5
- A **Re-check dates** section, sorted ascending
- An **Unassigned** section for anything the bundle can't place
- A **Skills** inventory and an **Agents** inventory, each with description and "used by"

No step number, Health or Last Run column, and no raw `autonomy` or `execution_mode` value. Progress is read by the routing rule from the folder, never from which links a node has. No generation-date line — the file's content is the only thing that changes, so a timestamp footer would just create diff noise.

**Tier 2 — `registry-dashboard.html` (always at the end of `scaffolding-registry`; on every later pass once `registry-dashboard.html` exists or the leader has a dashboard Artifact — on print-to-save, build it only to republish the Artifact; otherwise on request: "generate my dashboard").** Read the bundle, build a data island matching `references/data-island.schema.json` by the derivation rules in `references/tier-2-island.md` (ids, `nodePath`/`nodeUrl`, traversal order, `state`, `usedBy`, skills and agents scan — the same rules compose follows), and inject it as the **only** change into `references/dashboard-template.html`'s `<script type="application/json" id="data">` element — never touch the renderer around it. Before injecting, replace every `<` in the serialized JSON with `\u003c`; an unescaped `<` in any description closes the script element and blanks the page. Save the result as `registry-dashboard.html` beside `registry/`.

**Telling the leader about `REGISTRY.md`.** When you mention it, say what it is in one plain sentence: "`REGISTRY.md` is a one-page text summary of your registry; it's refreshed after every step, and it's what your AI reads to catch up on your business." Mention it only when the leader asks about it or runs this skill directly. On a maintenance pass at the end of another step, never name it: the calling step's close names only the dashboard.

**Telling the leader about the dashboard.** On a maintenance pass at the end of another step, say nothing; that step's close mentions the dashboard. When the leader runs this skill directly or asks about the dashboard, in plain words: what it shows (lines of business, processes, owners, workflows and where each one is), why any section is empty, and how to open it — on their computer, "double-click `registry-dashboard.html` to open it in your browser; click any item to see its details"; in a drive, download it first, then open it the same way. Don't report the checks you ran, the template, the data block, or JSON. If you replace an earlier dashboard, just replace it; don't save a copy outside the framework's folders or point the leader at a session folder.

*Claude platforms:* when the leader asks for the dashboard directly ("generate my visual dashboard"), after they know how to open the file, offer on its own line: "Want your dashboard as a **Claude Artifact**? It's a private page you can open from Claude any time, and share with a link if you want to." At the end of registry setup, `scaffolding-registry`'s close makes this offer instead — don't repeat it. Never offer it on a routine maintenance pass at the end of another step. When the leader already has a dashboard Artifact (a `Dashboard Artifact: <link>` entry in `registry/log.md`, one published earlier in this conversation, or one they mention), republish it to the same link on every pass that refreshes the dashboard, without asking: the link doesn't change, and a stale copy is never what they want. Tell the calling step so its close can say the Claude page is updated. If republishing to the logged link fails (the platform can't update a page from another conversation), publish a new page, give the leader its link in one line ("Your dashboard's Claude page has a new link: [link]"), and append the new `Dashboard Artifact: <link>` entry. Never create one unasked. When you create one (on request), append a `registry/log.md` entry: `Dashboard Artifact: <link>`; if the leader later deletes it, remove nothing, and append a new entry when a new one is made — the latest entry wins.

### 5. Append `log.md`

`registry/log.md` is append-only (`references/registry-bundle.md` §7). This skill appends only the dashboard Artifact link and any schema change it makes. The workflow lines (go-live, a re-check, a changed version not ready, a big change and its reason) belong to the steps that write them. Never remove or rewrite a line, and never log routine node writes or regenerations.

## Refusal + self-healing rule

Refuses to regenerate derived views while lint reports errors — with the reference's self-healing exception: broken-link errors that point at derived content the pass is about to rewrite (stale links left in GENERATED views by renames/retirements) do not block emission; a post-emit lint is the backstop. Without this exception, a rename deadlocks the composer on the very files whose regeneration would clear the error.

## Workspace-generator precedence

If the workspace contains `tools/compose-registry.js`, run `node tools/lint-registry.js && node tools/compose-registry.js` instead of assembling the dashboards by hand — the workspace's own generator is authoritative. Compose only refreshes a `registry-dashboard.html` that already exists: when the Tier 2 dashboard is due and there is none beside `registry/`, first copy `tools/dashboard-template.html` to `registry-dashboard.html`, then run compose. A registry in a drive is never composed by script: build its views by hand, as above.

**Out-of-date tools.** Before running them, compare the `"version"` in the workspace's `tools/package.json` with the one in the plugin's `tools/` folder (where `framework-state.js` ships). If the workspace's is missing or lower, ask, word for word: "Your registry's tools are out of date. Update them now?" On a yes, copy the plugin's `compose-registry.js`, `lint-registry.js`, `registry-lib.js`, `package.json`, `framework-state.js` and `requirements-check.js` over `tools/`, plus `references/dashboard-template.html` and `references/data-island.schema.json`; then copy the new template over `registry-dashboard.html` before composing, since compose only injects data into an existing page. Leave the bundle's `registry/SCHEMA.md` as it is. On a no, compose with the tools as they are. A workspace with no `tools/` folder is unaffected.

## Best-effort rule

A failed refresh must never fail the step that requested it. On the web, write through the drive connection like any other save. Only on print-to-save, give the regenerated `REGISTRY.md` with its location for the leader to save, say so, and continue. The HTML dashboard is never printed; on print-to-save it is built only to republish an existing Artifact.
