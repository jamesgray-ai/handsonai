---
title: Evaluator-Optimizer
description: Generate output, evaluate it against criteria, and refine iteratively through a feedback loop until quality standards are met
---

# Evaluator-Optimizer

The **evaluator-optimizer** pattern uses iterative refinement through two components: a **generator** that produces output and an **evaluator** that assesses it against predefined criteria. The workflow cycles between generation and evaluation until the output meets quality standards.

This mirrors how humans refine their work — drafting, reviewing, and editing — to achieve optimal outcomes.

## Why It Matters

- **High-quality outputs** — The evaluator catches and refines suboptimal results before delivery
- **Adaptable to complex tasks** — Ideal for nuanced or multi-faceted outputs that benefit from incremental improvement
- **Human-like iteration** — Mimics the draft-review-revise cycle that produces polished work
- **Dynamic feedback** — The evaluator can provide domain-specific feedback or adapt criteria, making it versatile across use cases

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Generator (LLM Call)** | Produces an initial solution or response | Drafts a marketing tagline for a product |
| **Evaluator (LLM Call)** | Reviews output against evaluation criteria and provides actionable feedback | Assesses whether the tagline aligns with brand voice and audience preferences |
| **Feedback Loop** | Iteratively refines output until it meets criteria | If the tagline misses brand guidelines, the evaluator provides specific improvement guidance |
| **Accepted Output** | Delivers the finalized result once criteria are satisfied | A polished tagline ready for the campaign |

## When to Use It

- **Nuanced tasks** — When outputs require multiple layers of refinement (creative content, technical documentation)
- **High-stakes outputs** — When accuracy and quality are critical (legal documents, strategic reports)
- **Clear evaluation criteria** — When you can define measurable standards for what "good" looks like

## Example: Refining a Marketing Campaign

A company needs compelling marketing content (taglines, ad copy, social posts) that must reflect brand tone, resonate with the audience, and meet platform guidelines:

1. **Generator** — Produces initial drafts of taglines, ad copy, and social media posts
2. **Evaluator** — Reviews drafts against brand tone, audience fit, and platform requirements; provides actionable feedback ("Make the tagline more emotionally engaging for the target audience")
3. **Feedback Loop** — Refines outputs iteratively until all criteria are met
4. **Accepted Output** — Polished, ready-to-use marketing content aligned with campaign goals

**Results:**

- **Quality** — High-quality outputs aligned with brand and audience
- **Efficiency** — Reduces manual editing, saving time and resources
- **Consistency** — Uniform tone and style across campaign elements

## How to Implement

1. **Define evaluation criteria** — Establish clear, measurable standards (quality, alignment, tone)
2. **Set up the feedback loop** — Ensure seamless communication between generator and evaluator for iterative refinement
3. **Set iteration limits** — Prevent infinite loops by capping the number of refinement cycles
4. **Test the workflow** — Validate that evaluator feedback effectively guides the generator toward desired outcomes

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Workflow Architecture Patterns Overview](index.md)
- [Prompt Chaining](prompt-chaining.md) — sequential steps with gates (but not iterative)
- [Autonomous Agents](autonomous-agents.md) — agents with built-in evaluation through the think-act-observe loop
- [Build > Design Your AI Workflow](../../business-first-ai-framework/build/design.md)
