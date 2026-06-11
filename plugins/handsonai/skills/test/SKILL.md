---
name: test
description: >
  Guide structured testing of AI workflow artifacts, evaluate output quality, identify which building blocks need adjustment, and determine readiness for deployment. Use when the user has built workflow artifacts and needs to test them. This is Step 5 (Test) of the AI Workflow Framework.
user-invocable: true
---

# Test Workflow

Structured testing and evaluation of AI workflow artifacts. Walk the user through running their workflow against real scenarios, scoring output quality, diagnosing issues back to specific building blocks, and deciding whether the workflow is ready for deployment.

## Workflow

### 1. Load context

Read the workflow's manifest (`outputs/[workflow-name]/workflow.yaml`) to locate the artifacts, then read the Design Spec and the Workflow Requirements it references (the requirements own the Acceptance Criteria, Example Scenarios, and Golden Examples). If no manifest exists but legacy flat files (`outputs/[name]-*.md`) do, use those paths. Verify both files exist before proceeding — if either is missing, stop and say which.

From these, identify:
- The test scenarios (E1, E2, …) and what to look for in each output
- The scoring dimensions from the Acceptance Criteria
- Any **Golden Examples** — known-good outputs (or excerpts) attached to scenarios. These are the strongest evaluation tool you have: scoring becomes "compare against this reference" instead of "how does it feel?"

### 2. Quick smoke test

One representative input, manual check: does the workflow run end-to-end and produce something reasonable? This is a sanity check before systematic evaluation — catch showstoppers early.

### 2.5 Integration pre-flight (enables partial testing)

Before the eval suite, check each integration the scenarios will exercise for the access it needs (read vs. write). Connectors are often **read-only** or unauthorized, which would block steps like creating a draft, writing a CRM row, or sending a message.

- If everything needed is available → run the full eval suite (Step 3).
- If any **write path is blocked** → **don't abort.** Switch to **partial test**: run and score every step that *can* run (classification, content generation, any readable/writable integrations), and **simulate** the blocked steps (produce the would-be output without performing the live action). Clearly mark which steps were **simulated/skipped and why**, and report the result as *"logic verified; deployment blocked on [integration] write access"* rather than a pass or a fail.

This distinguishes "the workflow logic is wrong" from "an integration isn't authorized yet" — two very different fixes.

### 3. Run eval suite

Execute each test scenario — sourced from the Acceptance Criteria and Example Scenarios sections of the Workflow Requirements (loaded in Step 1). For each scenario:

- Run the workflow with the scenario's input (full or partial per the pre-flight above)
- Score output on each eval dimension (1–5 scale); score only the steps that actually ran
- Note specific issues with concrete examples
- Note any steps that were **simulated/skipped** (don't let a simulated step count as a pass)

**Live-system test data caution.** A real test writes real artifacts to the user's accounts (rows, drafts, events). Prefer a clearly-marked test record, tell the user exactly what was created and where, and offer to clean it up afterward.

**Score each scenario two ways, then reconcile:**

1. **AI-graded first.** Before asking the user anything, evaluate the output yourself against the Acceptance Criteria — and against the scenario's Golden Example if one exists. Propose a score per dimension with a one-line justification quoting the specific evidence ("Accuracy 4/5 — matches the golden example's structure, but the deal value is stated as monthly where the reference uses annual"). Comparing against a golden example, check: what's missing, what's extra, what's different in substance (not just wording).
2. **User confirms or adjusts.** Present your proposed scores and ask the user to confirm or correct them with plain-language prompts:
   - "I scored **accuracy** 4/5 because [evidence]. Does that match your read, or would you move it?"
   - "On **tone/style**, does this sound like it came from you? 1 means completely off, 5 means indistinguishable."

The AI grade gives every scenario a consistent, evidence-based starting point (and makes future regression runs comparable); the user's confirmation keeps the human as the final judge of quality. Record the **confirmed** score. Adapt the dimension names to whatever eval dimensions were defined in the Acceptance Criteria.

### 4. Building block evals

Test individual skills and prompts in isolation — not just end-to-end. For each skill or prompt in the workflow:

- Run it with a known input
- Check: did this specific building block produce the right output?
- Isolating components helps pinpoint where problems originate vs. where they cascade

### 5. Establish baseline

Record the eval scores as the reference point for future regression testing in Step 7 (Improve). This baseline captures:

- Scores per scenario per dimension
- Overall averages
- Known limitations and accepted tradeoffs

### 6. Diagnose issues

For each problem identified in the eval, map it to which building block to adjust:

| Symptom | Building Block to Adjust |
|---------|--------------------------|
| Generic output | Add more **Context** (examples, style guides, reference materials) |
| Steps skipped or misunderstood | Refine the **Prompt** (more explicit instructions) |
| Missing expertise | Build a **Skill** for that step (codify domain knowledge) |
| Unpredictable decisions | Convert to **Agent** (let AI plan its approach) |

### 7. Readiness decision

Based on eval scores across all scenarios:

- **Ready** — scores meet the minimum bar from the Workflow Requirements' Acceptance Criteria → proceed to the `run` skill (Step 6)
- **Logic-ready, deploy-blocked** — the logic passes in partial testing but one or more write integrations are unauthorized. Name the blocker and what to authorize; the user fixes access, then re-runs the blocked steps before going to Run. (Not a code defect — don't loop back to Build for it.)
- **Not ready** — document specific adjustments needed, return to the `build` skill (Step 4), then re-test

## Output

Write results to `outputs/[workflow-name]/test-results.md`. If a results file already exists from a previous round, rename it with a date suffix (e.g., `test-results-2026-06-10.md`) first — earlier rounds are useful history, not waste. Then update the workflow manifest (`outputs/[workflow-name]/workflow.yaml`): set `current_step: 5`, `last_updated`, and add `test_results` under `artifacts`.

**Open the file with YAML frontmatter** so Improve (Step 7) can diff regression runs mechanically instead of re-reading prose:

```yaml
---
workflow: [kebab-case name]
design_spec: outputs/[workflow-name]/design-spec.md
requirements: outputs/[workflow-name]/requirements.md
date: YYYY-MM-DD
environment: [platform + notable conditions, e.g., "Claude.ai, Gmail connector live, Notion simulated"]
readiness: ready | not-ready | logic-ready-deploy-blocked
scores:
  E1: { accuracy: 4, completeness: 5, tone: 3 }   # confirmed scores, one line per scenario
  E2: { accuracy: 5, completeness: 4, tone: 4 }
averages: { accuracy: 4.5, completeness: 4.5, tone: 3.5 }
---
```

Use the actual scenario IDs and dimension names from the Workflow Requirements. Below the frontmatter, include an eval scorecard with this format:

- **Scenarios tested** — list each scenario with its input description
- **Scores per dimension** — table of scenario × dimension scores (1–5), noting where a Golden Example was used as the reference
- **Golden Example deltas** — for scenarios with a golden example, the specific differences found (missing / extra / substantively different)
- **Steps simulated/skipped (and why)** — any steps not run live (e.g., blocked integration), so a partial test is never mistaken for a full pass
- **Integration / environment status** — which integrations were live vs. simulated, and the environment tested in (so a later Improve regression compares like-for-like and doesn't read "an integration got fixed" as "the workflow improved")
- **Issues identified** — specific problems with concrete examples and diagnosed building block
- **Baseline established** — summary scores to use as regression reference in Step 7
- **Overall readiness assessment** — Ready / Not Ready / **Logic-ready, deploy-blocked** (with the blocking integration named), with rationale

## Guidelines

- 2–4 testing iterations is normal before reaching readiness. Don't treat the first round of issues as failure — it's expected.
- Use plain-language scoring guidance. Never say "write an eval" — instead say "rate your output across real scenarios."
- Keep the user focused on concrete examples, not abstract quality judgments. "Show me the sentence that's wrong" beats "was it good?"
- If the Workflow Requirements has no Acceptance Criteria or Example Scenarios, help the user create them now — and note this as a gap to fix by re-running the Deconstruct step for future workflows.
