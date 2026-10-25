---
title: Reflection
description: How AI agents improve their output by reviewing, critiquing and revising their own work, alone or with a critic agent, before delivering a final result.
last_reviewed: 2026-10-24
---

## What It Is

Reflection is a pattern where an agent reviews its own output, identifies flaws or gaps, and revises its work before presenting a final result. Instead of delivering the first response it generates, the agent runs an internal feedback loop — acting as both creator and critic.

In its simplest form, the agent generates an output, then prompts itself (or a second "critic" agent) to evaluate that output against criteria like accuracy, completeness, and tone. The feedback is fed back into the generation step, producing an improved version.

## Why It Matters

LLMs generate text in a single forward pass — essentially thinking the entire answer at once. For simple tasks, this works fine. But for complex tasks (writing, analysis, code generation), the first draft is rarely the best draft. Reflection mimics the human process of drafting, reviewing, and revising.

Two 2023 studies measured the gain, without any model fine-tuning. In Self-Refine, a model that critiqued and revised its own output improved by about 20% (absolute) on average across seven tasks, compared with answering in one step ([Madaan et al., 2023](https://arxiv.org/abs/2303.17651)). In Reflexion, an agent that reflected on feedback from earlier attempts reached 91% pass@1 on the HumanEval coding benchmark, against 80% for GPT-4, the previous best ([Shinn et al., 2023](https://arxiv.org/abs/2303.11366)).

## How It Works

```text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Generator   │────▸│   Critic     │────▸│  Revised     │
│  (Draft)     │     │  (Evaluate)  │     │  Output      │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    Feedback loop
                    (repeat if needed)
```

1. **Generate** — The agent produces an initial output.
2. **Evaluate** — The agent (or a separate critic) reviews the output against defined criteria.
3. **Revise** — The agent incorporates the feedback and produces an improved version.
4. **Repeat** — Steps 2–3 can loop multiple times until the output meets quality thresholds or a maximum iteration count is reached.

The critic can be the same LLM with a different prompt ("Review this for accuracy and completeness") or a separate agent entirely. Andrew Ng writes that he has found it convenient to create two agents, one prompted to generate good outputs and the other to criticize them. A separate critic, with its own instructions, is less likely to share the generator's blind spots; the [Evaluator-Optimizer](../../../../patterns/workflow-architecture/evaluator-optimizer/) pattern builds on that.

## Example

### Customer exchange scenario

An agent is drafting a response to a customer requesting a product exchange:

**First draft:**
> "Your exchange has been processed. The new item will ship in 3-5 business days."

**Critic feedback:**
> "The response doesn't confirm which item is being exchanged, doesn't mention the return process for the original item, and doesn't provide a tracking or confirmation number."

**Revised response:**
> "I've processed your exchange of the Blue Widget (Order #4521) for the Red Widget. Please return the Blue Widget using the prepaid label sent to your email within 14 days. Your Red Widget will ship within 3–5 business days once we receive the return. Your exchange confirmation number is EX-78234."

### Code generation

An agent writes a Python function, then reviews it:

**Critic feedback:**
> "The function doesn't handle the edge case where the input list is empty. It also uses a variable name `l` which is hard to distinguish from `1`."

The agent revises the function to add an empty-list check and renames the variable to `items`.

## When to Use It

- Writing tasks where quality matters (reports, emails, documentation)
- Code generation — catching bugs, edge cases, and style issues before delivery
- Analysis tasks where accuracy is critical
- Any task where the cost of iteration is lower than the cost of a wrong first answer

## Related Patterns

- [Planning](../planning/) — Reflection can evaluate whether a plan is complete before execution begins
- [Multi-Agent Collaboration](../multi-agent-collaboration/) — A dedicated critic agent is a form of multi-agent collaboration
- [Guardrails](../guardrails/) — Guardrails enforce hard constraints; reflection handles softer quality improvements
- [Evaluator-Optimizer](../../../../patterns/workflow-architecture/evaluator-optimizer/) — the workflow pattern that puts the critique in a separate evaluator
- [Agent Capability Patterns](../)

## Further Reading

- Andrew Ng — [Agentic Design Patterns Part 2, Reflection](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection) (*The Batch*, March 27, 2024)
- Shinn et al. — [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) (arXiv, March 20, 2023) — the 91% HumanEval figure
- Madaan et al. — [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) (arXiv, March 30, 2023) — the ~20% average improvement
- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024)
