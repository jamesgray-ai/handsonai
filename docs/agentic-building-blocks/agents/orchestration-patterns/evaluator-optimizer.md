---
title: Evaluator-Optimizer (Review Loop)
description: How a generator agent and an evaluator agent iterate on output until it meets defined quality criteria — producing measurably better results than single-pass generation.
---

# Evaluator-Optimizer (Review Loop)

## What It Is

The evaluator-optimizer pattern pairs a generator agent with an evaluator agent in a feedback loop. The generator produces output, the evaluator scores it against defined criteria and provides specific feedback, and the generator revises its output based on that feedback. This loop repeats until the output meets a quality threshold or a maximum iteration count is reached.

Think of it like a writer and editor working together. The writer produces a draft, the editor marks it up with specific feedback ("this paragraph is unclear," "this claim needs a citation"), and the writer revises. They go back and forth until the piece is publication-ready.

## Why It Matters

Single-pass generation rarely produces the best possible output for complex tasks. The evaluator-optimizer pattern provides **measurable quality improvement** — each iteration either raises the score or the loop terminates. Unlike simple [reflection](../capability-patterns/reflection.md) (where one agent self-critiques), using a separate evaluator agent avoids confirmation bias and produces more rigorous feedback.

This pattern is especially valuable when you have clear, objective quality criteria — factual accuracy, format compliance, code correctness, or rubric-based scoring. The evaluator can check things the generator can't: running tests, validating against a schema, or comparing against reference examples.

## How It Works

```text
┌───────────┐      output      ┌───────────┐
│ Generator │─────────────────▸│ Evaluator  │
│           │◂─────────────────│            │
└───────────┘    feedback +    └───────────┘
                  score              │
    ▲                                │
    │         score ≥ threshold?     │
    │         ├── YES → final output │
    │         └── NO → loop back ────┘
    └────────────────────────────────┘
```

1. **Generate** — The generator agent produces an initial output based on the task input.
2. **Evaluate** — The evaluator agent scores the output against defined criteria and provides specific, actionable feedback.
3. **Check** — If the score meets the threshold (or max iterations reached), output the final version. Otherwise, continue.
4. **Revise** — The generator receives the evaluator's feedback and produces an improved version.
5. **Repeat** — Steps 2–4 loop until the quality bar is met.

The evaluator's feedback should be **specific and actionable** — not "this needs improvement" but "paragraph 3 contradicts the data in paragraph 1; the conclusion doesn't follow from the evidence presented." The more specific the feedback, the better the revision.

## Example

### Technical writing

A documentation system for API references:

- **Generator** — Writes API endpoint documentation from the source code and inline comments.
- **Evaluator** — Checks against a rubric: (1) all parameters documented, (2) request/response examples included, (3) error codes listed, (4) description matches actual behavior. Scores 0–4.
- **Loop** — The generator revises until the evaluator scores 4/4. Typically converges in 2–3 iterations.

### Code generation

A coding assistant producing a function to specification:

- **Generator** — Writes the function based on the requirements and type signatures.
- **Evaluator** — Runs the test suite, checks type safety, measures code complexity. Returns: tests passed (8/10), type errors (1), complexity score (acceptable).
- **Loop** — The generator fixes the 2 failing tests and 1 type error. Next iteration: 10/10 tests pass, 0 type errors. Done.

The evaluator has a concrete advantage here — it can actually *run* the code, something the generator can't do during generation.

## When to Use It

- Output quality has clear, measurable criteria (test pass rate, rubric score, schema compliance)
- The cost of iteration is lower than the cost of a wrong first answer
- The evaluator can check things the generator can't (run tests, validate against external data, check compliance)
- Single-pass quality isn't sufficient for the use case
- You can define a termination condition (score threshold or max iterations)

## When NOT to Use It

- Quality criteria are subjective or undefined — the evaluator can't provide useful feedback without clear criteria
- The task is simple enough that single-pass generation is sufficient
- Iteration costs (tokens, time, API calls) aren't justified by the quality improvement
- The generator can't meaningfully improve from the evaluator's feedback (if the feedback is "this is wrong" without specifics)
- No natural termination condition — the loop may never converge

## Related Patterns

- [Reflection](../capability-patterns/reflection.md) — single-agent self-critique; evaluator-optimizer uses a separate evaluator for less bias
- [Sequential](sequential.md) — one-pass pipeline vs. iterative refinement loop
- [Hierarchical](hierarchical.md) — the coordinator may use evaluator-optimizer internally for quality-sensitive subtasks
- [Evaluator-Optimizer (Workflow Architecture)](../../../patterns/workflow-architecture/evaluator-optimizer.md) — the single-agent workflow architecture equivalent
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "evaluator-optimizer" section
- Andrew Ng — [Agentic Design Patterns Part 2: Reflection](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/) — iterative refinement concepts
