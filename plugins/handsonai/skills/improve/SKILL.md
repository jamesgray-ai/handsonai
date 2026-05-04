---
name: improve
description: >
  Evaluate a running AI workflow for quality, relevance, and evolution opportunities.
  Use when the user wants to review how a deployed workflow is performing, check if it needs
  tuning, or assess whether it should graduate to a more capable orchestration mechanism.
  This is Step 7 (Improve) of the Business-First AI Framework.
user-invocable: true
---

# Improve Workflow

Evaluate and evolve running AI workflows. Review how a deployed workflow is performing against its original baseline, identify degradation or growth signals, and recommend whether to tune, redesign, or evolve the orchestration mechanism.

## Workflow

### 1. Load workflow context

Read the Building Block Spec (including Evaluation Criteria), Run Guide, and original Test Results (baseline scores). Understand what was built, how it was designed to work, and what quality bar was established.

### 2. Current state assessment

Interview the user with concrete questions:

- How often are you running this workflow?
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

- **Prompt → Skill-Powered Prompt** — if repeatable sub-routines have emerged that deserve codification
- **Skill-Powered Prompt → Agent** — if AI needs to make sequencing decisions rather than follow a fixed order
- **Single Agent → Multi-Agent** — if complexity has grown to require specialized sub-agents

Only recommend graduation when there's a concrete capability gap, not just because "it could be more sophisticated."

### 5. Regression evaluation

Re-run the eval suite from Step 5 (Test):

- Run the same test scenarios from the original baseline
- Score on the same dimensions
- Compare to baseline scores
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
- **Tune** — specific building blocks to adjust (identify which ones and what to change) → loop back to Build (Step 4) and Test (Step 5)
- **Redesign** — requirements have changed enough that the workflow structure needs rethinking → loop back to Design (Step 3)
- **Evolve** — graduate to a more capable orchestration mechanism → loop back to Design (Step 3) with an explicit graduation recommendation

## Output

Write results to `outputs/[workflow-name]-improvement-plan.md`.

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
