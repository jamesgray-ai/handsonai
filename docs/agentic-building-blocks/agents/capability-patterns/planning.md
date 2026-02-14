---
title: Planning
description: How AI agents break complex goals into a sequence of steps, deciding what to do and in what order before taking action.
---

# Planning

## What It Is

Planning is a pattern where an agent decomposes a complex goal into a sequence of smaller, manageable steps — then executes them in order. Instead of attempting to solve a problem in a single response, the agent first creates a plan, then follows it step by step, adapting as needed based on intermediate results.

This is what separates an agent from a simple chatbot. A chatbot responds to a single prompt. An agent with planning capability can take a high-level objective ("process this customer's exchange") and autonomously determine the sequence of actions required to achieve it.

## Why It Matters

Real-world tasks are rarely single-step. Processing an exchange requires verifying the order, checking return eligibility, confirming inventory, processing payment, and sending confirmation. A planning agent handles this entire workflow without requiring the user to specify each step.

Andrew Ng has noted that planning is the least mature of the four core agentic patterns — it works well for well-defined workflows but remains challenging for open-ended, ambiguous goals. This makes it both the most powerful pattern (when it works) and the one that most benefits from [guardrails](guardrails.md) and [human oversight](human-in-the-loop.md).

## How It Works

```text
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Goal     │────▸│  Plan         │────▸│  Execute      │
│  (input)  │     │  (decompose)  │     │  (step by    │
│           │     │               │     │   step)       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                                      Replan if needed
```

1. **Receive goal** — The agent receives a high-level objective.
2. **Decompose** — The agent breaks the goal into an ordered sequence of sub-tasks.
3. **Execute** — The agent works through each sub-task, using [tool calls](tool-use.md) and [reflection](reflection.md) as needed.
4. **Monitor** — After each step, the agent checks whether the result changes the remaining plan.
5. **Replan** — If a step fails or produces unexpected results, the agent revises the remaining plan rather than blindly continuing.

Advanced planning approaches include:

- **Chain-of-thought planning** — The agent reasons through the plan in natural language before executing.
- **Tree-of-thought** — The agent explores multiple possible plans and selects the best one (Yao et al. 2023).
- **Hierarchical planning** — High-level plans are broken into sub-plans, each with their own steps.

## Example

### Customer exchange scenario

**Goal:** "Process customer Jane Smith's exchange — return Blue Widget, ship Red Widget."

**Agent's plan:**

1. Look up Jane Smith's order history → find order #ORD-5678
2. Verify return eligibility → check if Blue Widget is within the 30-day return window
3. Check Red Widget inventory → confirm availability in the nearest warehouse
4. Calculate price difference → Blue Widget was $29.99, Red Widget is $34.99, difference is $5.00
5. Process return for Blue Widget → generate prepaid return label
6. Charge $5.00 price difference → process payment
7. Place order for Red Widget → create new shipment
8. Send confirmation email → include return label, new order details, and timeline

**Replanning example:** At step 3, the Red Widget is out of stock. The agent replans: offer the customer the Green Widget as an alternative, or place the Red Widget on backorder with an estimated date.

### Research task

**Goal:** "Write a competitive analysis of our top 3 competitors."

**Agent's plan:**

1. Identify the top 3 competitors from the company's CRM data
2. For each competitor, gather recent news, product launches, and pricing
3. Analyze strengths and weaknesses relative to our product
4. Draft a comparison table
5. Write executive summary with recommendations
6. Review and refine the full document

## When to Use It

- Multi-step workflows with dependencies between steps (step 3 depends on step 2's output)
- Tasks where the sequence of actions matters
- Goals that are too complex to accomplish in a single tool call
- Workflows where failure at one step should change the approach for subsequent steps

## Related Patterns

- [Tool Use](tool-use.md) — Planning determines which tools to call and in what order
- [Reflection](reflection.md) — The agent can reflect on its plan before and during execution
- [Multi-Agent Collaboration](multi-agent-collaboration.md) — A planning agent can delegate sub-tasks to specialized agents
- [Human-in-the-Loop](human-in-the-loop.md) — Humans can approve the plan before execution begins
- [Agent Capability Patterns](index.md)

## Further Reading

- Yao et al. 2023 — *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* — [arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)
- Huang et al. 2024 — *Understanding the Planning of LLM Agents: A Survey* — [arxiv.org/abs/2402.02716](https://arxiv.org/abs/2402.02716)
- Andrew Ng — *Agentic Design Patterns Part 4: Planning* — [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-4-planning/)
- Anthropic — *Building Effective Agents* — [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)
