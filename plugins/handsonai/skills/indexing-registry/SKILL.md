---
name: indexing-registry
description: >
  This skill should be used to maintain the user's AI Registry — the registry/
  knowledge bundle and its derived views (the REGISTRY.md dashboard, directory
  indexes, GENERATED blocks, and the visual HTML dashboard). Triggers: "update
  my registry", "check my AI registry", "refresh my registry", "lint my registry", "generate my
  dashboard", "what have I built", "show my AI inventory", after creating
  skills or agents, or when another framework skill's closing step calls for a
  maintenance pass. Also "upgrade my registry" (moves a registry set up before
  OKF 0.3 to the current format), and recording the user's own check of a page
  ("I've checked my registry", "mark [page] as checked"). Also repairs stale or
  hand-edited derived views. If no
  registry/SCHEMA.md exists, route to the scaffolding-registry skill instead.
---

# Maintaining the AI Registry

The **AI Registry** is the `registry/` knowledge bundle plus everything derived from it: directory indexes, GENERATED blocks inside individual nodes, the `REGISTRY.md` dashboard, and the visual HTML dashboard (always generated at the end of registry setup; once it exists, refreshed on every pass).

**The registry is derived-state doctrine.** The bundle's node files (under `registry/`) are the source of truth. Every dashboard, index, and summary is generated from them. **Edit sources, regenerate — never hand-edit a derived view.** If a derived view looks wrong, fix the source node and regenerate; never patch the view.

For where the bundle is and how nodes are written and owned (resolution, write rules, the field-ownership table, the registry log, how progress and the re-check date are shown, and the full lint rule list), see `references/registry-bundle.md`. This skill assumes that contract; it doesn't restate it. A workflow's progress is never stored: it is read from the workflow's folder by the routing rule, through the `framework-state` script where code can run (`references/tier-2-island.md` has the by-hand reading). Its re-check date is Test's `stale_after`.

## Location & Scope

**One working folder = one registry.** On Claude Code and Codex the bundle is `registry/` in the workspace, beside `framework/`, `sops/` and `process-guides/`. On Claude desktop it is `registry/` inside the working folder the leader selected, beside `framework/`. On the web (Claude, ChatGPT) and in Microsoft 365 Copilot it is `registry/` in the working folder (`ai-workspace/`, or the leader's own folder) in the storage service it was set up in (Google Drive, OneDrive, Dropbox or another; OneDrive in Microsoft 365), read and written through the platform's connection, saved the way `references/saving.md` decides from the connection's tools, by the drive-saving rule in `references/registry-bundle.md`. `REGISTRY.md` and `registry-dashboard.html` sit beside `registry/`, in its parent folder. Where there are no files and no connection that can save, nothing is written: N-F16, and wait (`references/saving.md`, rule 5). The skill never assumes a Git repository.

> **Terminology:** "AI Registry" always means the `registry/` bundle and the views generated from it. It is unrelated to `registries/platform-docs.json`, the list of platforms' documentation pages the framework's skills look things up in.

## The maintenance pass

Run all five jobs for a full pass, or just the one the user asked for. Other framework skills invoke this skill from their closing step for the same pass — see **Best-effort rule** below.

### 1. Check the registry (lint)

Check the pages against the bundle's `registry/SCHEMA.md` and the rule list in `references/registry-bundle.md` (§8) — that file is the single source; do not duplicate its rule list here. The scope:

- **At a framework step's close, and at `scaffolding-registry`'s:** the pages that step wrote or changed, plus the essentials that reach across pages: every Process has an `owner:` matching a Function, and each Function's `# Owns` block lists exactly the Processes it owns, in the form under *Regenerate GENERATED blocks*. A step that creates a Process writes it into its owner Function's `# Owns` block itself, when it writes the Process, so the check normally finds it current; a block still missing a Process or out of date is regenerated with the views (it is derived content, so this is regeneration, not a repair; a stale block is a warning, never an error); every page sits in exactly one parent list; every page is in its folder's `index.md`; links into and out of the changed pages resolve. Claim no more than that, and say nothing when it passes.
- **Every §8 rule only when the leader asks** ("check my AI registry", "update my AI registry", or this skill by name). End that check with one plain line saying what it covered, and, where it couldn't cover everything (a page it couldn't read, say), what it didn't: name the pages and the rules you checked, in plain words. Never imply more than you checked.
- **A workspace's own `tools/`,** where the leader already has one, is used as before (*Workspace-generator precedence*). This skill adds no scripts to the leader's folder; where the workspace has none, it runs the plugin's own copies (*Workspace-generator precedence*).

Report findings in plain language, named by page. On a pass called by another step, say nothing when every check passes, or when a finding needs nothing from the leader; when a fix needs the leader, name the workflow or process, never the file.

**Talking about the check.** To the leader it is "checking your registry", and the files are "pages", never nodes. Never name a skill or a hand-off between skills ("the scaffolding skill hands the pages to…"). Never say "maintenance pass", and never mention lint, compose, scripts, `tools/`, `lint-registry.js`, `compose-registry.js`, GitHub Actions or the template repository unless the leader asks about one of them, and never ask the leader to choose between them. Asked, give one short answer: "The checks run inside the skill. The template's scripts are an optional extra for people who keep their registry on GitHub." **Offer fixes; never silently repair meaning** — a lint pass corrects mechanical issues (formatting, missing index entries) only with the user's confirmation, and never reinterprets or rewrites a node's content on its own judgment. Regenerating GENERATED blocks (a Function's `# Owns`, a Workflow's `# Insights`) isn't such a fix: they are derived, and are rewritten with the views.

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

Rewrite the content between `<!-- GENERATED:<name> -->` and `<!-- /GENERATED -->` markers: a Workflow node's `# Insights` block, and a Function node's `# Owns` block. Write only inside the markers, never outside them, and never leave a marker pair unterminated. One exception: where a Function's `# Owns` heading sits inside the markers (an earlier form), move it above the opening marker; that is the only change made outside them. A Function's `# Owns` block, exactly (the heading stays above and outside the markers; inside, one bullet per Process whose `owner:` is this Function, in path order, and nothing else):

```markdown
# Owns

<!-- GENERATED:owns -->
- [Cohort Delivery](/processes/cohort-delivery.md)
- [Cohort Launch & Enrollment](/processes/cohort-launch-and-enrollment.md)
<!-- /GENERATED -->
```

### 4. Regenerate dashboards

**Tier 1 — `REGISTRY.md` (always, on every pass).** Structure, fixed by the reference example:

- Business header (name, linked if a URL is set)
- One section per line of business, in curated order
- Within each, one subsection per process, each holding a workflow table in value-chain order with its state (from `state`; the column is headed Status), progress (the routing state's name), "How it decides", "Runs with you" or "Runs without you", and the "Re-check by" date, under the labels in `references/registry-bundle.md` §5
- A **Re-check dates** section, sorted ascending
- An **Unassigned** section for anything the bundle can't place
- A **Skills** inventory and an **Agents** inventory, each with description and "used by"

No step number, Health or Last Run column, and no raw `autonomy` or `execution_mode` value. Progress is read by the routing rule from the folder, never from which links a node has. No generation-date line — the file's content is the only thing that changes, so a timestamp footer would just create diff noise.

**Tier 2 — `registry-dashboard.html` (always at the end of `scaffolding-registry`; on every later pass once `registry-dashboard.html` exists or the leader has a dashboard Artifact; otherwise on request: "generate my dashboard").** Read the bundle, build a data island matching `references/data-island.schema.json` by the derivation rules in `references/tier-2-island.md` (ids, `nodePath`/`nodeUrl`, traversal order, `state`, `usedBy`, skills and agents scan — the same rules compose follows), and inject it as the **only** change into `references/dashboard-template.html`'s `<script type="application/json" id="data">` element — never touch the renderer around it. Before injecting, replace every `<` in the serialized JSON with `\u003c`; an unescaped `<` in any description closes the script element and blanks the page. Save the result as `registry-dashboard.html` beside `registry/`.

**Telling the leader about `REGISTRY.md`.** When you mention it, say what it is in one plain sentence: "`REGISTRY.md` is a one-page text summary of your registry; it's refreshed after every step, and it's what your AI reads to catch up on your business." Mention it only when the leader asks about it or runs this skill directly. On a maintenance pass at the end of another step, never name it: the calling step's close names only the dashboard.

**Telling the leader about the dashboard.** On a maintenance pass at the end of another step, say nothing; that step's close mentions the dashboard. When the leader runs this skill directly or asks about the dashboard, in plain words: what it shows (lines of business, processes, owners, workflows and where each one is), why any section is empty, and how to open it — on Claude Code and Codex, offer to open it for them ("Say 'open my dashboard' and I'll open it in your browser."), and on that answer open it with the system's own command (`open` on macOS, `start ""` on Windows, `xdg-open` on Linux), or, if that fails, give its full path and say to double-click it; elsewhere on their computer, "double-click `registry-dashboard.html` to open it in your browser; click any item to see its details"; in a drive, download it first, then open it the same way; in a cloud session, where the file is in the repository on GitHub, say it's there to download and lead with the Claude Artifact offer, never "double-click it". Don't report the checks you ran, the template, the data block, or JSON. If you replace an earlier dashboard, just replace it; don't save a copy outside the framework's folders or point the leader at a session folder.

*Claude platforms:* when the leader asks for the dashboard directly ("generate my visual dashboard"), after they know how to open the file, offer on its own line: "Want your dashboard as a **Claude Artifact**? It's a private page you can open from Claude any time, and share with a link if you want to." At the end of registry setup, `scaffolding-registry`'s close makes this offer instead — don't repeat it. Never offer it on a routine maintenance pass at the end of another step. When the leader already has a dashboard Artifact (a `Dashboard Artifact: <link>` entry in `registry/log.md`, one published earlier in this conversation, or one they mention), republish it to the same link on every pass that refreshes the dashboard, without asking: the link doesn't change, and a stale copy is never what they want. Tell the calling step so its close can say the Claude page is updated. If republishing to the logged link fails (the platform can't update a page from another conversation), publish a new page, give the leader its link in one line ("Your dashboard's Claude page has a new link: [link]"), and add the new `- Dashboard Artifact: <link>` entry at the end of today's heading (`references/registry-bundle.md` §7). If the platform can't publish at all, leave the page as it is and say nothing about it: the file is current, and the page refreshes on the next pass that can publish. Never create one unasked. When you create one (on request), add a `registry/log.md` entry, `- Dashboard Artifact: <link>`, at the end of today's heading (`references/registry-bundle.md` §7); if the leader later deletes it, remove nothing, and add a new entry when a new one is made — the newest entry (the one under the latest date) wins.

### 5. Append `log.md`

`registry/log.md` keeps OKF v0.3's form: entries under `## YYYY-MM-DD` headings, newest date first, each a bullet; a new entry goes at the end of today's heading, the first below the log's description (`references/registry-bundle.md` §7). This skill adds only the dashboard Artifact link, any schema change it makes, and the leader's checker ID (*Record a check*). The workflow entries (go-live, a re-check, a changed version not ready, a big change and its reason) belong to the steps that write them. Never remove, reword or move an entry, and never log routine node writes or regenerations.

## Upgrade a registry from OKF 0.2

A registry whose root `index.md` says `okf_version: "0.2"`, or no version, was set up before OKF v0.3 (`references/registry-bundle.md` §10). It still works, and every step writes the new forms into it. On "upgrade my registry", or once when a pass the leader started finds one (never on a pass at another step's close), ask, word for word: "Your registry was set up with an earlier version of its file format. Updating it changes how the pages are written, never what they say. Update it now?" On a yes: where code can run on a local folder, `node [tools]/upgrade-registry.js registry` (the workspace's `tools/`, else the plugin's), then replace `registry/SCHEMA.md` with `scaffolding-registry`'s `references/schema-template.md`, then a full pass. Elsewhere, make §10's changes page by page by hand, saving as the drive rules say. Leave `generated` and `verified` as they are on every page. Then say in one line that the registry is on the current format; never list the pages.

## Record a check

`verified` is the leader's own check (`references/registry-bundle.md` rule 11), never yours. When the leader says they've read a page and it's right ("I've checked my registry", "mark [page] as checked"), record it on that page only, and on each page they name; "my registry" means the pages they say they read, so ask which when it isn't clear. The first time, ask in model wording what name to record their checks under; write it as `human:<id>` (lowercase, hyphens), and add `- **Checker** — [their name] checks pages as human:[id]` to `log.md`; later checks read the ID from there. Write `verified: { by: human:<id>, at: <now, UTC instant> }` on the line after `generated`; a page that already has one becomes a list with both events (`verified: [{ … }, { … }]`), the earlier kept. Nothing else on the page changes, `generated` included. Confirm in one line which pages are recorded as checked, and that a page counts as checked until its content next changes.

## Refusal + self-healing rule

Refuses to regenerate derived views while lint reports errors — with the reference's self-healing exception: broken-link errors that point at derived content the pass is about to rewrite (stale links left in GENERATED views by renames/retirements) do not block emission; a post-emit lint is the backstop. Without this exception, a rename deadlocks the composer on the very files whose regeneration would clear the error.

## Workspace-generator precedence

If the workspace contains `tools/compose-registry.js`, run `node tools/lint-registry.js && node tools/compose-registry.js` instead of assembling the dashboards by hand — the workspace's own generator is authoritative. Never name the scripts to the leader (*Talking about the check*). Compose only refreshes a `registry-dashboard.html` that already exists: when the Tier 2 dashboard is due and there is none beside `registry/`, first copy `tools/dashboard-template.html` to `registry-dashboard.html`, then run compose. **No `tools/` in the workspace:** where code can run and the registry is in a local folder, use the plugin's own copies instead of building the views by hand: `node [plugin root]/tools/lint-registry.js registry && node [plugin root]/tools/compose-registry.js registry`, run from the working folder (the plugin root is two folders above this skill's folder, where `framework-state.js` ships). When the Tier 2 dashboard is due and there is none beside `registry/`, first copy this skill's `references/dashboard-template.html` to `registry-dashboard.html`. Never copy the scripts into the leader's folder for this. Only when a script fails to run (it can't start or crashes), or where the plugin's `tools/` isn't there (a skill uploaded on its own), build the views by hand, as above. When lint reports errors, that is the refusal (*Refusal + self-healing rule*): build nothing by hand while the check fails, and the calling step's close says the dashboard wasn't refreshed (N-F20). Warnings (a stale `# Owns` block, say) never block the build. A registry in a drive is never composed by script: build its views by hand, as above.

**Out-of-date tools.** Before running them, compare the `"version"` in the workspace's `tools/package.json` with the one in the plugin's `tools/` folder (where `framework-state.js` ships). If the workspace's is missing or lower, ask, word for word: "Your registry's tools are out of date. Update them now?" On a yes, copy the plugin's `compose-registry.js`, `lint-registry.js`, `registry-lib.js`, `upgrade-registry.js`, `package.json`, `framework-state.js` and `requirements-check.js` over `tools/`, plus `references/dashboard-template.html` and `references/data-island.schema.json`; then copy the new template over `registry-dashboard.html` before composing, since compose only injects data into an existing page. Leave the bundle's `registry/SCHEMA.md` as it is. On a no, compose with the tools as they are. A workspace with no `tools/` folder is unaffected.

## Best-effort rule

A failed refresh must never fail the step that requested it. On the web, write through the drive connection like any other save.
