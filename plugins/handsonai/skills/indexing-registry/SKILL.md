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
user-invocable: true
---

# Maintaining the AI Registry

The **AI Registry** is the `registry/` knowledge bundle at the workspace root, plus everything derived from it: directory indexes, GENERATED blocks inside individual nodes, the `REGISTRY.md` dashboard, and — on request — the visual HTML dashboard.

**The registry is derived-state doctrine.** The bundle's node files (under `registry/`) are the source of truth. Every dashboard, index, and summary is generated from them. **Edit sources, regenerate — never hand-edit a derived view.** If a derived view looks wrong, that's a signal to fix the source node and regenerate, not to patch the view directly.

For how nodes are resolved, written, and owned — resolution rules, write rules, the field-ownership table, framework-progress inference, review scheduling, and the full lint rule list — see `references/registry-bundle.md`. This skill assumes that contract; it doesn't restate it.

## Location & Scope

**One workspace = one registry.** The bundle lives at `registry/` off the root of the folder the framework operates in — beside `outputs/`, `sops/`, and `process-guides/`. Where that root is, and how bytes get read and written there, depends on the platform — see the platform matrix in the framework's cross-platform delivery documentation. Claude Code and Cowork read and write the bundle directly; claude.ai and other connector-based platforms generate and commit through their connector, with anything unwritten stated explicitly.

> **Terminology:** "AI Registry" always means the `registry/` bundle and the views generated from it. It is unrelated to the framework's *platform registry* (`registries/platform-registry.json`), which catalogs platforms and integrations for the Design and Build skills.

## The maintenance pass

Run all five jobs for a full pass, or just the one the user asked for. Other framework skills invoke this skill from their closing step for the same pass — see **Best-effort rule** below.

### 1. Lint

Read every node against the workspace's `registry/SCHEMA.md` and the rule list in `references/registry-bundle.md` (§6) — that file is the single source; do not duplicate its rule list here. Report findings in plain language, named by file. **Offer fixes; never silently repair meaning** — a lint pass corrects mechanical issues (formatting, missing index entries) only with the user's confirmation, and never reinterprets or rewrites a node's content on its own judgment.

### 2. Refresh indexes

Regenerate the typed-directory `index.md` files and the bundle-root inventories (Skills and Agents, each with a "used by" column derived from which Workflow nodes link them).

**Quick Start Prompts** are retained from the prior version of this skill. A Quick Start Prompt is a single copy-paste-ready prompt demonstrating an asset's primary use case. When an asset has no `quick_start_prompt` frontmatter field, generate one and **offer to write it back into the asset's frontmatter** (with the user's confirmation — this is the only write this skill makes outside the bundle and its derived views). Until it's written back, show the generated prompt in the index but note it's unsaved.

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
- Within each, one subsection per process, each holding a workflow table in value-chain order with status, execution mode, autonomy, and review-by date
- A **Review dates** section, sorted ascending
- An **Unassigned** section for anything the bundle can't place
- A **Skills** inventory and an **Agents** inventory, each with description and "used by"

No Health, Last Run, or Step columns — framework step is inferred from artifact presence (`references/registry-bundle.md` §4), not stored. No generation-date line — the file's content is the only thing that changes, so a timestamp footer would just create diff noise.

**Tier 2 — `registry-dashboard.html` (on request: "generate my dashboard").** Read the bundle, build a data island matching `references/data-island.schema.json`, and inject it as the **only** change into `references/dashboard-template.html`'s `<script type="application/json" id="data">` element — never touch the renderer around it. Save the result as `registry-dashboard.html` at the workspace root.

*Claude platforms:* after generating `registry-dashboard.html`, offer to publish it as an Artifact.

### 5. Append `log.md`

Record schema changes and migrations only — not routine content edits. Routine node writes don't need a log entry.

## Refusal + self-healing rule

Refuses to regenerate derived views while lint reports errors — with the reference's self-healing exception: broken-link errors that point at derived content the pass is about to rewrite (stale links left in GENERATED views by renames/retirements) do not block emission; a post-emit lint is the backstop. Without this exception, a rename deadlocks the composer on the very files whose regeneration would clear the error.

## Workspace-generator precedence

If the workspace contains `tools/compose-registry.js`, run `node tools/lint-registry.js && node tools/compose-registry.js` instead of assembling the dashboards by hand — the workspace's own generator is authoritative.

## Best-effort rule

A failed refresh must never fail the step that requested it. If the environment can't write to the workspace root, say so and continue.
