---
title: Chain-of-Thought Prompting
description: "Chain-of-thought prompting — improve LLM reasoning by asking the model to show its work step by step before answering, with examples and when to use it."
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What It Is

Chain-of-Thought (CoT) prompting asks the model to work through a problem step by step before giving a final answer. Instead of jumping straight to a conclusion, the model shows its reasoning — making it more likely to arrive at a correct answer and allowing you to verify the logic along the way.

## Why It Works

When an LLM (large language model) generates intermediate reasoning steps, each step provides context for the next. This breaks complex problems into simpler sub-problems the model can handle more reliably. Without CoT, the model attempts to compute the answer in a single forward pass — essentially trying to "think" the entire solution at once — which fails for multi-step reasoning tasks like math, logic, and comparative analysis.

## When to Use It

- Math and numerical reasoning
- Multi-step logic problems
- Comparing options with tradeoffs
- Debugging and root cause analysis
- Any task where the reasoning matters as much as the answer

## The Pattern

```text
{Problem statement}

Think through this step by step:
1. First, {identify/analyze the key elements}
2. Then, {work through the logic}
3. Finally, {arrive at your conclusion}

Show your reasoning before giving your final answer.
```

**Zero-Shot CoT variation** — just append this to any prompt:

```text
Let's think step by step.
```

This simple addition can dramatically improve reasoning performance without any examples (Kojima et al. 2022).

**Filled-in example:**

```text
A company has 150 employees. 40% are remote, 30% are hybrid, and the rest
are in-office. Hybrid workers share desks at a 3:1 ratio (3 hybrid workers
per desk). How many desks does the office need?

Think through this step by step. Show your reasoning before giving your
final answer.
```

## Examples in Practice

### Business decision

**Context:** Your team is evaluating CRM vendors and needs a structured comparison that accounts for multiple constraints.

```text
We're choosing between three vendors for our CRM migration:
- Vendor A: $50K cost, 6-month timeline
- Vendor B: $35K cost, 12-month timeline
- Vendor C: $45K cost, 4-month timeline

Our current CRM contract expires in 8 months. We have a $48K budget.

Think through the tradeoffs step by step, considering cost, timeline risk,
and transition complexity. Then recommend the best option with your reasoning.
```

**Why this works:** It forces the model to weigh multiple factors systematically rather than jumping to the cheapest or fastest option.

### Debugging

**Context:** Your engineering team noticed a performance regression after a deployment and needs to narrow down the cause.

```text
Our API response times increased from 200ms to 800ms after last week's
deployment. The deployment included: a database schema migration, an upgrade
to the authentication library, and a new logging middleware.

Walk through potential causes step by step, starting with the most likely.
For each cause, explain how we could verify or rule it out.
```

**Why this works:** Debugging requires sequential elimination of hypotheses. CoT prevents the model from fixating on one cause and ignoring others.

### Math with multiple calculations

**Context:** You need to calculate office space requirements based on employee work patterns.

```text
A company has 150 employees. 40% are remote, 30% are hybrid, and the rest
are in-office. Hybrid workers share desks at a 3:1 ratio (3 hybrid workers
per 1 desk). In-office workers each need their own desk.

How many desks does the office need? Show your work.
```

**Why this works:** The model needs to track multiple calculations — percentages, different desk ratios for different groups, then a final total. Showing work prevents arithmetic errors that commonly occur when the model tries to compute everything at once.

:::tip[Platform tip]

Claude's extended thinking mode is essentially automated Chain-of-Thought — the model reasons internally before responding. OpenAI's o1/o3 model family does this natively. Enable these features when tackling complex reasoning tasks, especially math and multi-step analysis.
:::
## Common Pitfalls

:::caution[Using CoT for simple tasks]

**Problem:** "What is the capital of France? Let's think step by step." wastes tokens and adds no value. CoT is overhead for tasks that don't involve multi-step reasoning.

**Fix:** Reserve CoT for problems that actually require working through multiple steps — math, comparisons, debugging, planning. For simple factual questions, use [zero-shot prompting](../zero-shot-prompting/).
:::
:::caution[Not verifying the reasoning]

**Problem:** The model's intermediate steps can look logical and well-structured but still contain errors — especially in arithmetic or when applying domain-specific rules.

**Fix:** Read the intermediate steps, not just the final answer. If the reasoning is wrong at step 2, the final answer will be wrong too. This is the whole point of CoT: it makes errors visible and auditable.
:::
:::caution[Confusing CoT with Self-Consistency]

**Problem:** A single CoT trace shows one reasoning path. If that path happens to go wrong, you get a confidently wrong answer. Self-Consistency (Wang et al. 2022) is a separate technique that samples multiple reasoning paths and takes the majority answer.

**Fix:** For high-stakes decisions, consider asking the model for multiple approaches: "Solve this problem using two different methods, then compare your answers." See [Self-Consistency and Reflection](../self-consistency-and-reflection/).
:::
## Related Techniques

- [Zero-Shot Prompting](../zero-shot-prompting/) — Zero-Shot CoT ("Let's think step by step") bridges these two techniques
- [Self-Consistency and Reflection](../self-consistency-and-reflection/) — sample multiple reasoning paths for higher accuracy
- [Direct Instruction](../direct-instruction/) — combine with CoT by explicitly specifying the reasoning steps
- [Prompt Engineering Overview](../)
- [Research use case](../../../../use-cases/research/)

## Further Reading

- Wei et al. 2022 — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* — [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Kojima et al. 2022 — *Large Language Models are Zero-Shot Reasoners* — [arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916)
- Wang et al. 2022 — *Self-Consistency Improves Chain of Thought Reasoning in Language Models* — [arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)
- Yao et al. 2023 — *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* — [arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)
