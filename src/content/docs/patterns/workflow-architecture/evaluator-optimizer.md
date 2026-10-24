---
title: Evaluator-Optimizer
description: "The evaluator-optimizer pattern: a generator drafts, an evaluator grades the draft against clear criteria and sends it back, until it passes or hits a cap."
---

**Level:** Guided. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** review loop, generator–critic, maker-checker, iterative refinement.

The **evaluator-optimizer** pattern uses iterative refinement through two components: a **generator** that produces output and an **evaluator** that assesses it against predefined criteria and gives specific feedback. The workflow cycles between generation and evaluation until the output meets the quality bar or a maximum number of rounds is reached.

Think of it like a writer and editor working together. The writer produces a draft, the editor marks it up with specific feedback ("this paragraph is unclear," "this claim needs a citation"), and the writer revises. They go back and forth until the piece is ready.

The evaluator's grade decides what happens next (accept, or send back), and it grades by your criteria. That makes this pattern Guided.

## Why It Matters

- **High-quality outputs** — The evaluator catches and refines suboptimal results before delivery
- **Measurable improvement** — Each round either raises the score or the loop ends
- **Adaptable to complex tasks** — Ideal for nuanced or multi-faceted outputs that benefit from incremental improvement
- **Checks the generator can't make** — The evaluator can run tests, validate against a schema, or compare against reference examples

A separate evaluator is usually stronger than self-critique. In [Reflection](../../../agentic-building-blocks/agents/capability-patterns/reflection/), one agent reviews its own work. A separate evaluator, with its own instructions and tools, judges work it didn't write, so it's less likely to share the generator's blind spots.

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

1. **Generate** — The generator produces an initial output from the task input.
2. **Evaluate** — The evaluator scores the output against defined criteria and gives specific, actionable feedback.
3. **Check** — If the score meets the threshold, or the round cap is reached, output the final version. Otherwise, continue.
4. **Revise** — The generator receives the feedback and produces an improved version.
5. **Repeat** — Steps 2–4 loop until the quality bar is met or the cap stops the loop.

**Feedback must be specific.** Not "this needs improvement" but "paragraph 3 contradicts the data in paragraph 1; the conclusion doesn't follow from the evidence presented." The more specific the feedback, the better the revision.

**Every loop needs a cap.** Set a maximum number of rounds, and decide what happens when the cap is reached before the output passes (deliver the best version with a note, or hand it to a person).

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Generator** | Produces an initial solution or response | Drafts a marketing tagline for a product |
| **Evaluator** | Reviews output against evaluation criteria and provides actionable feedback | Assesses whether the tagline aligns with brand voice and audience preferences |
| **Feedback Loop** | Iteratively refines output until it meets criteria | If the tagline misses brand guidelines, the evaluator provides specific improvement guidance |
| **Accepted Output** | Delivers the finalized result once criteria are satisfied | A polished tagline ready for the campaign |

## When to Use It

- **Clear evaluation criteria** — When you can define measurable standards for what "good" looks like (test pass rate, rubric score, schema compliance)
- **High-stakes outputs** — When accuracy and quality are critical (legal documents, strategic reports)
- **Worth the extra rounds** — When the cost of iteration is lower than the cost of a wrong first answer
- **A natural stopping point** — When you can define a termination condition (score threshold or round cap)

## When Not to Use It

- Quality criteria are subjective or undefined — the evaluator can't provide useful feedback without clear criteria
- The task is simple enough that single-pass generation is sufficient
- Iteration costs (tokens, time, API calls) aren't justified by the quality improvement
- The generator can't meaningfully improve from the feedback (if the feedback is "this is wrong" without specifics)
- No natural termination condition — the loop may never converge

## Examples

### Refining a marketing campaign

A company needs compelling marketing content (taglines, ad copy, social posts) that must reflect brand tone, resonate with the audience, and meet platform guidelines:

1. **Generator** — Produces initial drafts of taglines, ad copy, and social media posts
2. **Evaluator** — Reviews drafts against brand tone, audience fit, and platform requirements; provides actionable feedback ("Make the tagline more emotionally engaging for the target audience")
3. **Feedback Loop** — Refines outputs until all criteria are met, or three rounds have run
4. **Accepted Output** — Polished, ready-to-use marketing content aligned with campaign goals

### API documentation

A documentation system for API references:

- **Generator** — Writes endpoint documentation from the source code and inline comments.
- **Evaluator** — Checks against a rubric: (1) all parameters documented, (2) request/response examples included, (3) error codes listed, (4) description matches actual behavior. Scores 0–4.
- **Loop** — The generator revises until the evaluator scores 4/4, with a cap on rounds.

### Code generation

A coding assistant producing a function to specification:

- **Generator** — Writes the function based on the requirements and type signatures.
- **Evaluator** — Runs the test suite, checks type safety, measures code complexity. Returns: tests passed (8/10), type errors (1), complexity score (acceptable).
- **Loop** — The generator fixes the 2 failing tests and 1 type error. Next round: 10/10 tests pass, 0 type errors. Done.

The evaluator has a concrete advantage here — it can actually *run* the code, something the generator can't do while writing it.

## How to Implement

1. **Define evaluation criteria** — Establish clear, measurable standards (quality, alignment, tone)
2. **Set up the feedback loop** — Pass the evaluator's specific feedback back to the generator for each revision
3. **Set iteration limits** — Prevent infinite loops by capping the number of refinement cycles, and decide what happens at the cap
4. **Test the workflow** — Validate that evaluator feedback effectively guides the generator toward desired outcomes

## Sources

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "evaluator-optimizer" section
- Andrew Ng — [Agentic Design Patterns Part 2: Reflection](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/) — iterative refinement concepts

## Related

- [Workflow Architecture Patterns Overview](../)
- [Reflection](../../../agentic-building-blocks/agents/capability-patterns/reflection/) — single-agent self-critique; evaluator-optimizer uses a separate evaluator
- [Prompt Chaining](../prompt-chaining/) — sequential steps with gates (one pass, not iterative)
- [Orchestrator-Workers](../orchestrator-workers/) — the lead may use a review loop for quality-sensitive subtasks
- [Autonomous Agents](../autonomous-agents/) — agents with built-in evaluation through the think-act-observe loop
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
