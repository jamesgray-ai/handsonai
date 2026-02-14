---
title: Agent Capability Patterns
description: Seven architectural patterns that make AI agents effective — from self-reflection to multi-agent collaboration, plus safety and control mechanisms
---

# Agent Capability Patterns

Capability patterns are the architectural building blocks that make AI agents powerful. While a basic LLM generates text in a single pass, an *agentic* system combines multiple patterns — reflection, tool use, planning, collaboration, and memory — to tackle complex, multi-step tasks autonomously.

These patterns were popularized by Andrew Ng in his 2024 writing on agentic design patterns (*The Batch*, DeepLearning.AI), building on research from Google, Stanford, Princeton, and others. The patterns are platform-agnostic — they apply whether you're building with Claude, ChatGPT, Gemini, or any other LLM.

## Pattern Catalog

### Capability Patterns

These five patterns define *what agents can do*.

| Pattern | What It Does | Key Benefit |
|---------|-------------|-------------|
| [Reflection](reflection.md) | Agent reviews and critiques its own output, then improves it | Higher-quality results through self-correction |
| [Tool Use](tool-use.md) | Agent calls external tools, APIs, and data sources | Extends capabilities beyond text generation |
| [Planning](planning.md) | Agent breaks complex goals into a sequence of steps | Handles multi-step tasks that require strategy |
| [Multi-Agent Collaboration](multi-agent-collaboration.md) | Multiple specialized agents work together on a task | Tackles problems too complex for a single agent |
| [Memory](memory.md) | Agent stores and retrieves information across interactions | Learns from experience and maintains context |

### Safety & Control

These two patterns define *how agents stay safe and aligned*.

| Pattern | What It Does | Key Benefit |
|---------|-------------|-------------|
| [Guardrails](guardrails.md) | Automated rules that constrain agent behavior | Prevents harmful or off-topic outputs without human intervention |
| [Human-in-the-Loop](human-in-the-loop.md) | Human checkpoints at key decision points | Keeps humans in control of high-stakes actions |

## How Patterns Work Together

Consider a customer exchange request — a customer wants to return a product and exchange it for a different item. A capable agent doesn't just use one pattern; it combines several:

1. **Planning** — The agent breaks the exchange into steps: verify the order, check return eligibility, find the replacement item, process the return, place the new order.
2. **Tool Use** — At each step, the agent calls the order management API, inventory system, and payment processor.
3. **Reflection** — Before confirming the exchange, the agent reviews its work: "Did I verify the return window? Is the replacement item in stock? Are the prices correct?"
4. **Guardrails** — Automated rules prevent the agent from issuing refunds above a threshold or processing exchanges for final-sale items.
5. **Human-in-the-Loop** — If the exchange involves an exception (expired return window, high-value item), the agent escalates to a human agent for approval.
6. **Memory** — The agent remembers this customer's preferences and past interactions, personalizing future service.

No single pattern makes this workflow possible. Their combination is what turns a basic chatbot into a capable agent.

## Where to Start

**Understanding agent concepts?** Start with [Reflection](reflection.md) — it's the simplest pattern to grasp and demonstrates the core idea of iterative improvement.

**Building your first agent?** [Tool Use](tool-use.md) is the most immediately practical pattern — it's how agents interact with the real world.

**Designing a production system?** Read [Guardrails](guardrails.md) and [Human-in-the-Loop](human-in-the-loop.md) first — safety and control should be designed in from the start, not bolted on later.

## Related

- [Agents](../index.md) — The Agents building block overview
- [Agents Resources](../resources.md) — Recommended reading on agents
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic's guide to agent architecture
- [Prompt Engineering](../../prompts/prompt-engineering/index.md) — Techniques for the prompts that drive agent behavior
- [Automation Use Cases](../../../use-cases/automation.md) — Real-world applications of agentic systems
