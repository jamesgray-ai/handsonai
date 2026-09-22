---
name: improve
description: >
  Evaluate a running AI workflow for quality and fit.
  Use when the user wants to review how a deployed workflow is performing, check if it needs
  tuning, or decide whether it should go back to Design (including graduating from a skill to an agent).
  Also use when the user says "continue my workflow" and the Workflow node's artifacts show Step 7 (Improve) is next, or its `stale_after` date has arrived.
  This is Step 7 (Improve) of the AI Workflow Framework.
user-invocable: true
---

# Improve Workflow

Evaluate running AI workflows and decide what, if anything, to change. Review how a deployed workflow is performing against its original baseline, identify degradation or growth signals, and recommend one of three outcomes: leave it, tune it, or go back to Design.

## Workflow

### 1. Load workflow context

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

Read the workflow's Workflow node (`registry/workflows/<slug>.md`) and load the artifacts it links: the Design Spec, Run Card, the Test Results that hold the baseline, and the **run log** (`runs.md`) if one exists. **Resume orientation:** if the user arrived via "continue my workflow" or with no stated workflow, check `registry/workflows/` for existing Workflow nodes (if several, list them) and orient from which artifacts each node's `# Artifacts` section already links before proceeding. If no Workflow node exists yet but legacy flat files (`outputs/[name]-*.md`) do, use those paths. If this environment has no persistent workspace and the files aren't present, ask the user to reconnect your registry repo via the GitHub connector, or re-upload the bundle folder, instead of failing.

The **baseline** is the report card of the round that produced the `Ready` verdict — the file named `test-results.md` when Run began — not the first attempt.

**Confirm the artifacts belong to the same workflow** — check that the `workflow` field in the Test Results frontmatter matches the Workflow node before treating its report card as this workflow's baseline. Parse the baseline from the Test Results frontmatter: the `results` block (per scenario, per criterion, `met` / `not-met`, plus `edits`). If the file has `scores` / `averages` instead, it predates the binary format: say so ("your baseline is from the older 1–5 format"), do not attempt a numeric comparison, and treat this review's report card as the new baseline.

**Check the review schedule.** If the Workflow node has a `stale_after` date, compare it to today: if overdue, note it plainly ("This review was due [date] — good timing") and, at the end of this run, agree a fresh `stale_after` date. If the user arrived well before the date, ask what prompted the early check — that signal (quality slipped, requirements changed) often points straight at the diagnosis.

Understand what was built, how it was designed to work, and what quality bar was established.

### 2. Current state assessment

**Start from the run log if one exists** — it's evidence, not recollection. Summarize what it shows (run frequency, recurring edits, failures, drift) and confirm the summary with the user rather than asking them to remember.

Then interview the user for what the log can't show:

- How often are you running this workflow? (skip if the run log answers this)
- How much manual editing does the output typically need?
- Have your requirements or business context changed?
- Are there new steps or decisions that have emerged since deployment?
- What's working well that you want to preserve?

### 3. Quality evaluation

Identify signals of degradation or opportunity:

| Signal | What It Means |
|--------|---------------|
| Increasing manual edits | Context may need updating (stale examples, changed standards) |
| New decision types appearing | May need additional skills or agent capabilities |
| Steps being skipped | Workflow coverage gap — missing steps need to be added |
| Report-card lines flipped between rounds | Orchestrator instructions or context need tuning |
| User adding steps manually | Workflow scope has grown beyond original design |

### 4. Graduation assessment

Has the workflow outgrown its mechanism?

- **Skill → Agent** — if the workflow now needs to make sequencing decisions or use tools rather than follow a fixed order
- **Single Agent → Multi-Agent** — if complexity has grown to require specialized sub-agents

Older Design Specs name the mechanism `Prompt`, `Skill-Powered Workflow`, or `Skill-Powered Prompt`. Read `Skill-Powered Workflow` and `Skill-Powered Prompt` as `Skill`. Read `Prompt` as a workflow that has not yet been packaged as a skill: its first graduation is **Prompt → Skill** (the same instructions saved as a skill the user invokes by name), and it is a Redesign outcome like the others.

Only recommend graduation when there's a concrete capability gap, not just because "it could be more sophisticated." Graduation is a Redesign outcome — it goes back to Design with the reason recorded.

### 5. Regression check

Re-run the same scenarios (`E1…`) the same way Test does — in a fresh conversation, graded here against the same check list, user confirms — and compare line by line:

- **Diff mechanically.** For every scenario × criterion, compare baseline to current. Present a table of every line that **flipped**: `Scenario | Line | Baseline | Now | Evidence`. A Met → Not met flip is a regression with a cause attached (the line names the step or rule); Not met → Met is an improvement.
- **Edits trend.** Compare `edits` per scenario, and the run log's "Edits needed" column over time — rising edit effort is the earliest drift signal, often before any line flips.
- **Like for like.** If a connector was simulated at baseline and is live now (or vice versa), say so — a flip caused by access changing is not the workflow changing.
- **Check the criteria themselves.** If the business has changed, some lines may be obsolete or missing; propose edits to the Requirements file, not to this review only.

Write this round's report card as a new dated `outputs/[workflow-name]/test-results.md` in Test's format (rename the previous one with a date suffix first). If the outcome is Tune, set `readiness: not-ready` and fill `## Issues identified` naming the building blocks — that file is what Build's fix mode reads.

### 6. Operationalization review (organizational workflows)

For workflows used by teams (not just individuals), assess:

- **Adoption** — Is the team actually using it? What's the usage frequency?
- **Training** — Do new team members know how to use it?
- **Governance** — Are outputs being reviewed appropriately? Are there quality controls?

Skip this step for individual/personal workflows.

### 7. Recommendation

Produce exactly one of three outcomes:

- **No changes needed** — no line regressed, edits are stable, requirements haven't shifted. Record it and set the next review date.
- **Tune** — specific building blocks to adjust (name them: S2, C3, orchestrator, connector) → the `build` skill regenerates only those (fix mode), then the `test` skill re-runs the affected scenarios.
- **Redesign** — the architecture no longer fits: requirements changed enough to restructure, or the workflow has outgrown its mechanism (a skill that now needs to make its own sequencing decisions, or an agent that should split into specialists). → the `design` skill, with the reason recorded in the Improvement Plan so Design starts from it.

## Output

Write results to `outputs/[workflow-name]/improvement-plan.md`. If a plan already exists from a previous review cycle, rename it with a date suffix first. Then update the Workflow node (`registry/workflows/<slug>.md`): reset `stale_after: YYYY-MM-DD` to the next agreed review date (monthly is a good default for high-frequency workflows, quarterly for occasional ones), and link the Improvement plan under `# Artifacts`. **If the review surfaced a durable insight, write it as a Note node in `registry/notes/` linking the Workflow** — insights are how learning enters your registry. See `indexing-registry/references/registry-bundle.md` for write rules and the full field-ownership table.

Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step).

Include:

- **Current performance summary** — how the workflow is being used and performing
- **Regression** — the flipped-lines table (scenario, line, baseline, now, evidence) and the edits trend
- **Issues identified** — specific problems with diagnosed root causes
- **Recommendation** — No changes / Tune / Redesign, with rationale
- **Action items** — concrete next steps if changes are recommended

## Guidelines

- Don't prompt for information the user can't answer. If they don't track usage metrics, work with qualitative signals instead.
- Focus on concrete signals, not abstract evaluation. "Your context file references Q3 goals but it's Q1" beats "your context may be stale."
- This step is typically invoked weeks or months after initial deployment, in a separate conversation from the original build.
- Not every workflow needs improvement. If it's working, say so and move on.
