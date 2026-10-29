---
title: Workflow Architecture Patterns
description: "The playbook's one catalogue of AI workflow patterns, each mapped to an autonomy level by what decides the next step, with a decision tree for choosing one."
last_reviewed: 2026-10-24
---

These patterns are the playbook's one catalogue of how AI work is laid out, from a single augmented LLM call to agents that plan their own steps. Most of the names come from Anthropic's [Building effective agents](https://www.anthropic.com/research/building-effective-agents); Handoff, Group Chat and Swarm come from the multi-agent guides by OpenAI, Microsoft and Google. Each page lists the other names vendors use.

The number of agents never changes the pattern. A prompt chain can be three LLM calls or three agents, and one page covers both.

The right pattern depends on what your workflow actually needs, not on how sophisticated you want it to be.

:::note[Capabilities and patterns]
The playbook looks at agent systems through two lenses:

| Lens | Question it answers |
|------|---------------------|
| [Agent Capability Patterns](../../agentic-building-blocks/agents/capability-patterns/) | What can one agent **do**? (reflect, use tools, plan, remember) |
| **Workflow Architecture Patterns** (this section) | How is the **work structured**? |

A capability can show up inside any pattern: an orchestrator uses planning, an evaluator is a form of reflection. When the framework's [Design](../../ai-workflow-framework/design/) step names a pattern in your plan, it uses the names in this catalogue.
:::

## Choose the Simplest Pattern That Works

Two principles come before any pattern:

1. **Start with the simplest thing that works,** and add complexity only when it measurably helps. Try a single [Augmented LLM](augmented-llm/) or a [Prompt Chain](prompt-chaining/) first, and move up only when it falls short. Anthropic recommends "finding the simplest solution possible, and only increasing complexity when needed" ([Building effective agents](https://www.anthropic.com/research/building-effective-agents)).
2. **One agent before several.** Split the work only for a named reason: protecting context, parallel coverage, specialization, or a security boundary. Coordination has a cost: Anthropic reports that in its own data a single agent used about 4 times the tokens of a chat, and a multi-agent system about 15 times ([How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system), June 13, 2025).

### Decision Tree

The tree asks the same question as the [AI Workflow Design Matrix](../../ai-workflow-framework/workflow-design-matrix/): **what decides the next step?**

```
What decides the next step?
│
├── Your instructions, every time ─────────────── Deterministic
│   ├── One pass ................................ Augmented LLM
│   ├── Ordered steps ........................... Prompt Chaining
│   └── Independent parts ....................... Parallelization
│
├── The AI's judgment, by your method ────────── Guided
│   ├── Sorting inputs into kinds ............... Routing
│   ├── Grading work and sending it back ........ Evaluator-Optimizer
│   ├── Several views to decide ................. Parallelization (voting)
│   ├── Passing to a specialist mid-task ........ Handoff
│   └── Splitting into a known kind of
│       subtasks, with a cap .................... Orchestrator-Workers
│
└── Only the goal can be described ───────────── Autonomous
    ├── One agent working it out ................ Autonomous Agents
    ├── Several workers on subtasks it invents .. Orchestrator-Workers
    ├── Deliberation ............................ Group Chat
    └── Peers refining together, with no lead ... Swarm
```

Then ask a separate question: **is there a high-risk action, or one that can't be undone?** If so, add a [Human Checkpoint](../../agentic-building-blocks/agents/capability-patterns/human-in-the-loop/) before it. A checkpoint sets how a person takes part (involvement); it never changes the level.

## The Patterns and Their Levels

Each pattern maps to an autonomy level by what decides the next step. Where a pattern can sit at two levels, the table says what tips it.

| Pattern | Use when | What decides the next step (level) | Also called |
|---------|----------|-------------------------------------|-------------|
| [Augmented LLM](augmented-llm/) | One call, with retrieval, tools or memory, does the job | **Deterministic** | single call |
| [Prompt Chaining](prompt-chaining/) | The work splits into ordered steps, each checked before the next | **Deterministic** with coded gates; **Guided** if the AI judges a gate | sequential pipeline |
| [Routing](routing/) | Inputs fall into kinds that each need different handling | **Guided** if the AI classifies; **Deterministic** if rules route | router, dispatcher, triage |
| [Parallelization](parallelization/) | Independent parts can run at once, or several attempts should vote | **Deterministic** when the split is fixed; **Guided** if the AI judges the vote | parallel, fan-out / fan-in, sectioning, voting |
| [Evaluator-Optimizer](evaluator-optimizer/) | Clear criteria can grade a draft and send it back | **Guided** | review loop, generator–critic, maker-checker, iterative refinement |
| [Orchestrator-Workers](orchestrator-workers/) | A lead splits the work, hands out subtasks and combines the results | **Guided** when the planning is bounded; **Autonomous** when it's open-ended | hierarchical, manager, supervisor, coordinator, agents-as-tools |
| [Handoff](handoff/) | The right specialist changes as a conversation or task unfolds | **Guided** | OpenAI's "decentralized" |
| [Group Chat](group-chat/) | The answer benefits from several agents debating | **Autonomous** | debate |
| [Swarm](swarm/) | Peers refine the work together with no lead, by messaging each other or through shared state | **Autonomous** | decentralized (the playbook's earlier name) |
| [Autonomous Agents](autonomous-agents/) | You can describe the goal, not the steps | **Autonomous** | agent loop, gather–act–verify |
| [Human Checkpoint](../../agentic-building-blocks/agents/capability-patterns/human-in-the-loop/) (cross-cutting) | A high-risk or irreversible action needs a person's approval | **No level.** It sets involvement (Augmented) | human-in-the-loop, approval gate |

A person's review never changes the level, and neither does the number of agents. The workflow's level is the highest level any of its AI steps reaches.

Whether the workflow runs as a Skill or an Agent is a separate choice. [Design](../../ai-workflow-framework/design/) makes it by how the workflow runs (whether it decides its path at runtime, uses tools on its own judgment, or runs unattended), never by the pattern.

## Sources

- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024). The post now carries a note that much of the tooling it describes has changed since then; the patterns this catalogue takes from it are still the ones it describes.
- Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) (June 13, 2025) — the token figures under principle 2
- OpenAI — [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF, April 2025) — the manager and decentralized patterns
- OpenAI Agents SDK — [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) (accessed 2026-10-24) — handoffs and agents as tools
- Google Cloud — [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (last reviewed May 28, 2026) — including the swarm pattern
- Microsoft — [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), Azure Architecture Center (accessed 2026-10-24) — including group chat and handoff orchestration

## Related

- [Design Your AI Workflow](../../ai-workflow-framework/design/) — assess autonomy and choose an orchestration mechanism for your workflow
- [AI Workflow Design Matrix](../../ai-workflow-framework/workflow-design-matrix/) — the autonomy levels and involvement modes these patterns map to
- [Agent Capability Patterns](../../agentic-building-blocks/agents/capability-patterns/) — what one agent can do (reflection, tool use, planning, and more)
- [Agents](../../agentic-building-blocks/agents/) — concepts for building AI agents
- [Patterns Overview](../)
