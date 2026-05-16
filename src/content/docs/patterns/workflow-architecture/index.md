---
title: Workflow Architecture Patterns
description: Seven architectural patterns for AI workflows — from augmented LLMs to autonomous agents — with a selection framework for choosing the right pattern
---Every AI workflow falls somewhere on an autonomy spectrum. These seven patterns — drawn from Anthropic's research — provide a common vocabulary for describing how AI systems are structured, from simple tool-augmented models to fully autonomous agents.

The right pattern depends on what your workflow actually needs, not on how sophisticated you want it to be. Start simple, upgrade when you hit limits.

## The Autonomy Spectrum

The patterns are organized into three tiers of increasing autonomy:

### Foundation

| Pattern | Description |
|---------|-------------|
| [Augmented LLM](augmented-llm/) | An LLM enhanced with retrieval, tools, and memory — the building block for all other patterns |

### Structured Workflows

| Pattern | Description |
|---------|-------------|
| [Prompt Chaining](prompt-chaining/) | Break a task into sequential steps, with validation gates between each step |
| [Routing](routing/) | Classify input and direct it to a specialized follow-up process |
| [Parallelization](parallelization/) | Run subtasks simultaneously and aggregate the results |
| [Orchestrator-Workers](orchestrator-workers/) | A central orchestrator dynamically breaks down tasks and delegates to specialized workers |
| [Evaluator-Optimizer](evaluator-optimizer/) | Generate output, evaluate it against criteria, and refine iteratively until it meets quality standards |

### Autonomous

| Pattern | Description |
|---------|-------------|
| [Autonomous Agents](autonomous-agents/) | An LLM with tools, memory, and planning that independently executes multi-step tasks through a think-act-observe loop |

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

:::tip[Start simple, upgrade when needed]
Most workflows start as a single Augmented LLM or Prompt Chain. Only add complexity when you hit a concrete limitation — not because the problem *seems* complex.
:::
## How These Patterns Relate to the Framework

The [Design](../../ai-workflow-framework/design/) phase of the AI Workflow Framework first assesses the workflow's autonomy level (Deterministic → Guided → Autonomous), then recommends an orchestration mechanism (Prompt → Skill-Powered Prompt → Agent). These seven architecture patterns provide the detailed implementation blueprints within that spectrum:

| Orchestration Mechanism | Architecture Patterns |
|------------------------|----------------------|
| Prompt | Augmented LLM |
| Skill-Powered Prompt | Prompt Chaining, Routing |
| Agent | Parallelization, Orchestrator-Workers, Evaluator-Optimizer, Autonomous Agents |

The [AI Workflow Design Matrix](../../ai-workflow-framework/workflow-design-matrix/) adds a second dimension — **human involvement** (Augmented vs. Automated) — to the autonomy spectrum. Architecture patterns map to the matrix's autonomy axis: Deterministic workflows typically use Augmented LLM or Prompt Chaining, Guided workflows use Routing or Evaluator-Optimizer, and Autonomous workflows use Orchestrator-Workers or Autonomous Agents.

## Credit

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Design Your AI Workflow](../../ai-workflow-framework/design/) — assess autonomy and choose an orchestration mechanism for your workflow
- [Agents](../../agentic-building-blocks/agents/) — concepts for building AI agents
- [Agent Capability Patterns](../../agentic-building-blocks/agents/capability-patterns/) — behavioral patterns (reflection, tool use, planning, etc.)
- [Agent Orchestration Patterns](../../agentic-building-blocks/agents/orchestration-patterns/) — multi-agent coordination topologies (sequential, parallel, hierarchical, etc.)
- [Patterns Overview](../)
