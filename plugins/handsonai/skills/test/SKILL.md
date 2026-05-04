---
name: test
description: >
  Guide structured testing of AI workflow artifacts, evaluate output quality, identify which building blocks need adjustment, and determine readiness for deployment. Use when the user has built workflow artifacts and needs to test them. This is Step 5 (Test) of the Business-First AI Framework.
user-invocable: true
---

# Test Workflow

Structured testing and evaluation of AI workflow artifacts. Walk the user through running their workflow against real scenarios, scoring output quality, diagnosing issues back to specific building blocks, and deciding whether the workflow is ready for deployment.

## Workflow

### 1. Load context

Read the Building Block Spec (including Evaluation Criteria) to understand what was built, expected behavior, and how to evaluate. Identify the test scenarios and scoring dimensions defined during Design.

### 2. Quick smoke test

One representative input, manual check: does the workflow run end-to-end and produce something reasonable? This is a sanity check before systematic evaluation — catch showstoppers early.

### 3. Run eval suite

Execute each test scenario from the Evaluation Criteria (defined in Design). For each scenario:

- Run the workflow with the scenario's input
- Score output on each eval dimension (1–5 scale)
- Note specific issues with concrete examples

Guide the user through scoring with plain-language prompts:

- "On **accuracy**, was this a 1 (not close), 3 (mostly right), or 5 (nailed it)?"
- "On **completeness**, did it cover everything you'd expect? 1 means major gaps, 5 means nothing missing."
- "On **tone/style**, does this sound like it came from you? 1 means completely off, 5 means indistinguishable."

Adapt the dimension names and prompts to match whatever eval dimensions were defined in the spec.

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

- **Ready** — scores meet the minimum quality bar defined in the spec → proceed to Step 6: Run
- **Not ready** — document specific adjustments needed, return to Step 4: Build, then re-test

## Output

Write results to `outputs/[workflow-name]-test-results.md`.

Include an eval scorecard with this format:

- **Scenarios tested** — list each scenario with its input description
- **Scores per dimension** — table of scenario × dimension scores (1–5)
- **Issues identified** — specific problems with concrete examples and diagnosed building block
- **Baseline established** — summary scores to use as regression reference in Step 7
- **Overall readiness assessment** — Ready or Not Ready, with rationale

## Guidelines

- 2–4 testing iterations is normal before reaching readiness. Don't treat the first round of issues as failure — it's expected.
- Use plain-language scoring guidance. Never say "write an eval" — instead say "rate your output across real scenarios."
- Keep the user focused on concrete examples, not abstract quality judgments. "Show me the sentence that's wrong" beats "was it good?"
- If no Evaluation Criteria were defined in the spec, help the user create them now — but note this as a gap to fix in the Design step for future workflows.
