---
name: improve
description: >
  Evaluate a running AI workflow for quality, relevance, and evolution opportunities.
  Use when the user wants to review how a deployed workflow is performing, check if it needs
  tuning, or assess whether it should graduate to a more capable orchestration mechanism.
  Also use when the user says "continue my workflow" and the workflow manifest shows Step 7 (Improve) is next, or the manifest next_review date has arrived.
  This is Step 7 (Improve) of the AI Workflow Framework.
user-invocable: true
---

# Improve Workflow

Evaluate and evolve running AI workflows. Review how a deployed workflow is performing against its original baseline, identify degradation or growth signals, and recommend whether to tune, redesign, or evolve the orchestration mechanism.

## Workflow

### 1. Load workflow context

Read the workflow's manifest (`outputs/[workflow-name]/workflow.yaml`) and load the artifacts it registers: the Design Spec, Run Guide, original Test Results (the baseline), and the **run log** (`runs.md`) if one exists. **Resume orientation:** if the user arrived via "continue my workflow" or with no stated workflow, first list the workflow folders under `outputs/` (if several) and orient from the manifest before proceeding. If no manifest exists but legacy flat files (`outputs/[name]-*.md`) do, use those paths. If this environment has no persistent workspace and the files aren't present, ask the user to re-upload them (manifest, test results, run log) instead of failing.

**Confirm the artifacts belong to the same workflow** — check that the `workflow` field in the Test Results frontmatter matches the manifest before treating its scores as this workflow's baseline. Parse the baseline scores from the Test Results frontmatter (`scores` and `averages`) — that's the regression reference.

**Check the review schedule.** If the manifest has a `next_review` date, compare it to today: if overdue, note it plainly ("This review was due [date] — good timing") and, at the end of this run, agree a fresh `next_review` date. If the user arrived well before the date, ask what prompted the early check — that signal (quality slipped, requirements changed) often points straight at the diagnosis.

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
| Output quality inconsistent | Prompt or context needs tuning |
| User adding steps manually | Workflow scope has grown beyond original design |

### 4. Graduation assessment

Should the orchestration mechanism evolve?

- **Prompt → Skill-Powered Workflow** — if repeatable sub-routines have emerged that deserve codification
- **Skill-Powered Workflow → Agent** — if AI needs to make sequencing decisions rather than follow a fixed order

(Older Design Specs use the legacy mechanism value `Skill-Powered Prompt` — treat it as `Skill-Powered Workflow`.)
- **Single Agent → Multi-Agent** — if complexity has grown to require specialized sub-agents

Only recommend graduation when there's a concrete capability gap, not just because "it could be more sophisticated."

### 5. Regression evaluation

Re-run the eval suite from Step 5 (Test):

- Run the same test scenarios (E1, E2, …) from the original baseline, scoring the same dimensions the same way Test does (AI-graded against Acceptance Criteria and Golden Examples first, user confirms)
- **Diff against the baseline mechanically**: compare the new per-scenario scores against the `scores` block parsed from the original Test Results frontmatter, and present a delta table (scenario × dimension, baseline → current, flagging any drop ≥1 point)
- **Compare like-for-like**: check the baseline's `environment` field — if an integration was simulated then and is live now (or vice versa), say so; a score change caused by an integration being fixed is not the workflow getting better or worse
- Identify areas of degradation or improvement
- Determine if the eval criteria themselves need updating (requirements may have shifted)

### 6. Operationalization review (organizational workflows)

For workflows used by teams (not just individuals), assess:

- **Adoption** — Is the team actually using it? What's the usage frequency?
- **Training** — Do new team members know how to use it?
- **Governance** — Are outputs being reviewed appropriately? Are there quality controls?

Skip this step for individual/personal workflows.

### 7. Recommendation

Produce one of the following:

- **No changes needed** — workflow is performing at or above baseline, requirements haven't shifted
- **Tune** — specific building blocks to adjust (identify which ones and what to change) → loop back to the `build` skill (Step 4) and `test` skill (Step 5)
- **Redesign** — requirements have changed enough that the workflow structure needs rethinking → loop back to the `design` skill (Step 3)
- **Evolve** — graduate to a more capable orchestration mechanism → loop back to the `design` skill (Step 3) with an explicit graduation recommendation

## Output

Write results to `outputs/[workflow-name]/improvement-plan.md`. If a plan already exists from a previous review cycle, rename it with a date suffix first. Then update the workflow manifest: set `current_step: 7`, `last_updated`, add `improvement_plan` under `artifacts`, and record `next_review: YYYY-MM-DD` (agree the date with the user — monthly is a good default for high-frequency workflows, quarterly for occasional ones). Also update the registry field `health` to reflect the diagnosis (`working`, `needs-attention`, or `broken`), then refresh `REGISTRY.md` at the workspace root per the `indexing-registry` skill (best-effort — a failed refresh never fails this step).

Include:

- **Current performance summary** — how the workflow is being used and performing
- **Regression scores** — comparison table of baseline vs. current scores
- **Issues identified** — specific problems with diagnosed root causes
- **Recommendation** — No changes / Tune / Redesign / Evolve, with rationale
- **Action items** — concrete next steps if changes are recommended

## Guidelines

- Don't prompt for information the user can't answer. If they don't track usage metrics, work with qualitative signals instead.
- Focus on concrete signals, not abstract evaluation. "Your context file references Q3 goals but it's Q1" beats "your context may be stale."
- This step is typically invoked weeks or months after initial deployment, in a separate conversation from the original build.
- Not every workflow needs improvement. If it's working, say so and move on.
