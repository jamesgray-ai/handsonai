---
title: Orchestrator-Workers
description: A central orchestrator dynamically breaks down tasks and delegates to specialized workers for flexible handling of complex, unpredictable problems
---

# Orchestrator-Workers

The **orchestrator-workers** pattern handles complex tasks where subtasks can't be defined in advance. A central orchestrator dynamically breaks down a task, delegates subtasks to specialized workers, and synthesizes their outputs into a final result.

This pattern differs from [parallelization](parallelization.md) because it emphasizes **flexibility and adaptability** — the orchestrator determines what needs to be done at runtime rather than following a predefined plan.

## Why It Matters

- **Flexibility for unknowns** — Adapts dynamically to varying task requirements, ideal for unstructured or evolving problems
- **Specialization** — The orchestrator ensures each subtask goes to the most suitable worker
- **Efficiency in complexity** — Complex tasks are broken into manageable components and results are synthesized
- **Scalability** — Dynamic task assignment allows systems to scale for diverse and large workloads

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Orchestrator** | Analyzes input, determines required subtasks, assigns them to appropriate workers | Divides a customer query into legal, financial, and technical subtasks |
| **Workers (LLM Calls)** | Specialized models or systems that process each subtask | Worker 1: legal analysis, Worker 2: financial evaluation, Worker 3: technical feasibility |
| **Synthesizer** | Combines worker outputs into a coherent final result | Merges legal, financial, and technical findings into actionable recommendations |
| **Input/Output** | The original task in, the synthesized result out | Input: multi-faceted customer request → Output: structured report addressing all aspects |

## Predefined vs. Dynamic Workers

The orchestrator can work with both:

- **Predefined workers** — Specialized for known task types (e.g., financial analysis, image recognition). The orchestrator routes to the right one.
- **Dynamic workers** — For tasks with unknown subtasks, the orchestrator creates workers on the fly:
    1. **Dynamic configuration** — Tailors a general-purpose LLM with specific prompts to temporarily specialize it
    2. **Tool integration** — Activates external tools or APIs to augment the worker's capabilities
    3. **On-the-fly instantiation** — In advanced systems, generates new worker instances adapted to the task

Dynamic worker creation ensures the system handles unexpected inputs without needing pre-configured workflows for every scenario.

## When to Use It

- **Unstructured tasks** — When subtasks can't be predicted or defined in advance
- **Multi-domain expertise** — When the task spans areas requiring different specialized knowledge
- **Dynamic workloads** — When new subtask types may emerge that weren't anticipated

## Example: Comprehensive Market Research

A company entering a new market needs analysis across competitor strategy, customer segmentation, and regulatory compliance:

1. **Orchestrator** breaks the task into three subtasks and assigns workers
2. **Worker 1** — Scans competitor pricing, products, and strategies
3. **Worker 2** — Processes demographic and survey data to generate customer segments
4. **Worker 3** — Reviews regulatory documents and flags compliance risks
5. **Synthesizer** — Combines outputs into a unified market research report

If a new subtask emerges (e.g., evaluating environmental impact), the orchestrator dynamically assigns or creates a new worker.

**Results:**

- **Speed** — All subtasks processed simultaneously
- **Specialization** — Each domain handled by a focused worker
- **Flexibility** — New subtasks addressed without restructuring the workflow

## How to Implement

1. **Design the orchestrator** — Build the logic that analyzes inputs and determines subtask breakdown
2. **Define worker capabilities** — Establish predefined workers for known task types and rules for dynamic creation
3. **Build the synthesizer** — Define how worker outputs combine into a coherent final result
4. **Test with varied inputs** — Ensure the orchestrator correctly identifies subtasks and routes to appropriate workers

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Workflow Architecture Patterns Overview](index.md)
- [Parallelization](parallelization.md) — similar structure but with predefined subtasks
- [Autonomous Agents](autonomous-agents.md) — the next step in autonomy
- [Agents](../../agentic-building-blocks/agents/index.md) — concepts for building AI agents
- [Build > Design Your AI Workflow](../../business-first-ai-framework/build/design.md)
