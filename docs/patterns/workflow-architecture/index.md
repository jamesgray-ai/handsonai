---
title: Workflow Architecture Patterns
description: Seven architectural patterns for AI workflows — from augmented LLMs to autonomous agents — with a selection framework for choosing the right pattern
---

# Workflow Architecture Patterns

Every AI workflow falls somewhere on an autonomy spectrum. These seven patterns — drawn from Anthropic's research — provide a common vocabulary for describing how AI systems are structured, from simple tool-augmented models to fully autonomous agents.

The right pattern depends on what your workflow actually needs, not on how sophisticated you want it to be. Start simple, upgrade when you hit limits.

## The Autonomy Spectrum

The patterns are organized into three tiers of increasing autonomy:

### Foundation

| Pattern | Description |
|---------|-------------|
| [Augmented LLM](augmented-llm.md) | An LLM enhanced with retrieval, tools, and memory — the building block for all other patterns |

### Structured Workflows

| Pattern | Description |
|---------|-------------|
| [Prompt Chaining](prompt-chaining.md) | Break a task into sequential steps, with validation gates between each step |
| [Routing](routing.md) | Classify input and direct it to a specialized follow-up process |
| [Parallelization](parallelization.md) | Run subtasks simultaneously and aggregate the results |
| [Orchestrator-Workers](orchestrator-workers.md) | A central orchestrator dynamically breaks down tasks and delegates to specialized workers |
| [Evaluator-Optimizer](evaluator-optimizer.md) | Generate output, evaluate it against criteria, and refine iteratively until it meets quality standards |

### Autonomous

| Pattern | Description |
|---------|-------------|
| [Autonomous Agents](autonomous-agents.md) | An LLM with tools, memory, and planning that independently executes multi-step tasks through a think-act-observe loop |

## Pattern Selection Framework

Use these three questions to identify which pattern your workflow needs:

**1. Is the task predictable or open-ended?**

- **Predictable** (you can define the steps in advance) → Use a structured workflow pattern
- **Open-ended** (steps depend on what the AI discovers) → Consider an autonomous agent

**2. How many steps are involved?**

- **Single step** → Augmented LLM
- **Sequential steps** → Prompt Chaining
- **Branching paths** → Routing
- **Independent parallel steps** → Parallelization
- **Dynamic subtasks** → Orchestrator-Workers

**3. Does the output need iterative refinement?**

- **Yes, with clear quality criteria** → Evaluator-Optimizer
- **Yes, with open-ended exploration** → Autonomous Agent

### Decision Flow

```
Start here: Can you define all the steps in advance?
│
├── YES → How many steps?
│   ├── One step → Augmented LLM
│   ├── Sequential steps with validation → Prompt Chaining
│   ├── Input determines the path → Routing
│   ├── Independent steps that can run simultaneously → Parallelization
│   └── Steps need dynamic decomposition → Orchestrator-Workers
│
├── PARTIALLY → Does output need iterative refinement?
│   └── YES → Evaluator-Optimizer
│
└── NO → Steps are unknown until runtime
    └── Autonomous Agent
```

!!! tip "Start simple, upgrade when needed"
    Most workflows start as a single Augmented LLM or Prompt Chain. Only add complexity when you hit a concrete limitation — not because the problem *seems* complex.

## How These Patterns Relate to the Framework

The [Build > Design](../../business-first-ai-framework/build/design.md) phase of the Business-First AI Framework uses an Execution Pattern Spectrum (Prompt → Skill-Powered Prompt → Single Agent → Multi-Agent) to classify workflows at a higher level. These seven architecture patterns provide the detailed implementation blueprints within that spectrum:

| Framework Execution Pattern | Architecture Patterns |
|---------------------------|----------------------|
| Prompt | Augmented LLM |
| Skill-Powered Prompt | Prompt Chaining, Routing |
| Single Agent | Parallelization, Orchestrator-Workers, Evaluator-Optimizer |
| Multi-Agent | Orchestrator-Workers (multi-agent), Autonomous Agents |

## Credit

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Build > Design Your AI Workflow](../../business-first-ai-framework/build/design.md) — choose an execution pattern for your workflow
- [Agents](../../agentic-building-blocks/agents/index.md) — concepts for building AI agents
- [Agent Capability Patterns](../../agentic-building-blocks/agents/capability-patterns/index.md) — behavioral patterns (reflection, tool use, planning, etc.)
- [Patterns Overview](../index.md)
