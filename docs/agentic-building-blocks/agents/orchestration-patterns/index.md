---
title: Agent Orchestration Patterns
description: Eight coordination topologies for multi-agent systems — from linear pipelines to decentralized swarms — with a selection guide for choosing the right pattern
---

# Agent Orchestration Patterns

Orchestration patterns describe how multiple agents coordinate to accomplish a task. While [capability patterns](../capability-patterns/index.md) define what individual agents can *do* (reflect, use tools, plan), orchestration patterns define how agents *work together* — who talks to whom, who decides what, and how results flow between agents.

These eight patterns are drawn from research and production systems across Anthropic, Google, OpenAI, Microsoft, CrewAI, LangGraph, and others. They're platform-agnostic — the coordination topology is independent of which LLM or framework you use.

!!! info "How This Section Relates to Others"

    Three sections in the Cookbook cover different lenses on agent systems:

    | Section | Lens | Question It Answers |
    |---------|------|---------------------|
    | [Capability Patterns](../capability-patterns/index.md) | What agents can **do** | "What abilities does an agent need?" |
    | **Orchestration Patterns** (this section) | How agents **coordinate** | "How do multiple agents work together?" |
    | [Workflow Architecture](../../../patterns/workflow-architecture/index.md) | How to **structure LLM calls** | "What's the right architecture for my workflow?" |

    Capability patterns are about individual agent abilities. Orchestration patterns are about multi-agent coordination. Workflow architecture patterns are about the overall structure of LLM calls in a system — including single-agent systems.

## Pattern Catalog

### Structured Topologies

Predictable coordination with defined communication paths.

| Pattern | Core Idea | Best For |
|---------|-----------|----------|
| [Sequential](sequential.md) | Agents execute in linear order; each output feeds the next | Multi-stage pipelines with clear handoff points |
| [Parallel](parallel.md) | Multiple agents work simultaneously; results are aggregated | Independent subtasks that benefit from speed or diversity |
| [Router](router.md) | Classifier inspects input and dispatches to the right specialist | Varied inputs that require different handling |

### Coordinated Topologies

Dynamic coordination with a central authority or peer-to-peer transfers.

| Pattern | Core Idea | Best For |
|---------|-----------|----------|
| [Hierarchical](hierarchical.md) | Coordinator decomposes tasks, delegates to specialists, synthesizes results | Complex tasks requiring dynamic decomposition |
| [Handoff](handoff.md) | Responsibility transfers between peer agents as context evolves | Conversational flows where expertise shifts mid-task |
| [Evaluator-Optimizer](evaluator-optimizer.md) | Generator + evaluator iterate until quality criteria are met | Output that requires measurable quality improvement |

### Emergent Topologies

Flexible coordination where behavior emerges from agent interactions.

| Pattern | Core Idea | Best For |
|---------|-----------|----------|
| [Group Chat](group-chat.md) | Agents converse in shared context; a moderator may synthesize | Problems benefiting from debate or multiple perspectives |
| [Decentralized](decentralized.md) | No master agent; peers coordinate through shared state or messaging | Highly dynamic tasks where no single agent can plan ahead |

## Selection Guide

Three questions to narrow your choice:

**1. Is the task structure known in advance?**

- **Yes, fixed steps** → Structured topology (Sequential, Parallel, or Router)
- **Yes, but steps are dynamic** → Coordinated topology (Hierarchical, Handoff, or Evaluator-Optimizer)
- **No, emergent** → Emergent topology (Group Chat or Decentralized)

**2. How do agents need to communicate?**

- **One-directional (output → input)** → Sequential or Parallel
- **Hub-and-spoke (coordinator ↔ workers)** → Router or Hierarchical
- **Peer-to-peer (agent ↔ agent)** → Handoff, Group Chat, or Decentralized
- **Loop (generate → evaluate → revise)** → Evaluator-Optimizer

**3. What's the coordination overhead tolerance?**

- **Minimal** → Sequential or Parallel (simplest to implement and debug)
- **Moderate** → Router, Hierarchical, or Handoff
- **High (justified by task complexity)** → Group Chat or Decentralized

### Decision Tree

```
Start: Is the task structure known in advance?
│
├── YES, fixed steps
│   ├── Steps are independent → Parallel
│   ├── Steps must happen in order → Sequential
│   └── Input determines which path → Router
│
├── YES, but steps are dynamic
│   ├── One agent should plan and delegate → Hierarchical
│   ├── Agents hand off to each other → Handoff
│   └── Output needs iterative refinement → Evaluator-Optimizer
│
└── NO, emergent
    ├── Agents benefit from debating → Group Chat
    └── No single agent can plan the whole task → Decentralized
```

## Where to Start

**Business leaders evaluating architectures?** Start with [Sequential](sequential.md) and [Hierarchical](hierarchical.md) — they map most naturally to how human teams work.

**Builders designing your first multi-agent system?** Start with [Sequential](sequential.md) — it's the simplest to implement and debug. Add complexity only when you hit limits.

**Exploring advanced coordination?** [Handoff](handoff.md) and [Evaluator-Optimizer](evaluator-optimizer.md) solve real production problems that simpler patterns can't handle.

## Sources

These patterns are synthesized from multiple authoritative sources:

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- Google Cloud — [Choose a Design Pattern for Agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
- Google ADK — [Developer's Guide to Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- OpenAI — [A Practical Guide to Building AI Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- OpenAI Agents SDK — [Multi-Agent Patterns](https://openai.github.io/openai-agents-python/multi_agent/)
- Microsoft Azure — [AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- Andrew Ng — [Agentic Design Patterns](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/)
- CrewAI — [Framework Documentation](https://docs.crewai.com/)
- LangGraph — [Multi-Agent Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent)

## Related

- [Agent Capability Patterns](../capability-patterns/index.md) — what individual agents can do
- [Multi-Agent Collaboration](../capability-patterns/multi-agent-collaboration.md) — the capability pattern for agent teamwork
- [Workflow Architecture Patterns](../../../patterns/workflow-architecture/index.md) — how to structure LLM calls in a system
- [Agents Overview](../index.md) — the Agents building block
- [Agents Resources](../resources.md) — recommended reading on agents
