---
title: Hierarchical (Coordinator / Manager)
description: How a central coordinator agent decomposes complex tasks, delegates to specialist agents, and synthesizes their results into a coherent output.
---

# Hierarchical (Coordinator / Manager)

## What It Is

The hierarchical pattern uses a central coordinator agent that dynamically decomposes a task into subtasks, delegates each subtask to the most appropriate specialist agent, collects their results, and synthesizes a final output. Unlike the [router](router.md) (which just classifies and dispatches), the coordinator actively plans, manages, and combines the work.

Think of it like a project manager leading a cross-functional team. The PM breaks the project into work packages, assigns each to the right team member, tracks progress, handles dependencies, and assembles the final deliverable. The team members focus on execution; the PM handles coordination.

## Why It Matters

Many real tasks can't be decomposed in advance — the subtasks depend on what the coordinator discovers during execution. A user asks "Plan a week-long trip to Japan" and the coordinator needs to dynamically decide: research destinations, check flight availability, find hotels, plan daily itineraries, and estimate budget. The number and sequence of subtasks emerge from the task itself.

Hierarchical coordination also provides **accountability** — one agent is responsible for the overall plan and output quality, while specialists focus on their domain without needing to understand the big picture.

## How It Works

```text
              ┌──────────────────┐
              │   Coordinator    │
              │  (plan, assign,  │
              │   synthesize)    │
              └──┬────┬────┬────┘
                 │    │    │
                 ▼    ▼    ▼
           ┌────┐ ┌────┐ ┌────┐
           │ S1 │ │ S2 │ │ S3 │
           └──┬─┘ └──┬─┘ └──┬─┘
              │      │      │
              ▼      ▼      ▼
              └──────┴──────┘
                     │
              ┌──────▼──────┐
              │ Coordinator  │
              │ (synthesize) │
              └─────────────┘
```

1. **Plan** — The coordinator analyzes the task and breaks it into subtasks. This plan may be explicit (a list of steps) or implicit (dynamically deciding what to do next).
2. **Delegate** — The coordinator assigns each subtask to a specialist agent, providing focused context and instructions.
3. **Execute** — Specialist agents complete their subtasks and return results. They may run sequentially, in parallel, or a mix.
4. **Synthesize** — The coordinator collects all results, resolves conflicts, fills gaps, and produces the final output.
5. **Iterate** — If results are incomplete or contradictory, the coordinator may assign additional subtasks or ask specialists to revise.

## Example

### Trip planning

A user asks: "Plan a 5-day trip to Tokyo for two people with a $3,000 budget."

- **Coordinator** — Decomposes: flights, hotels, daily activities, restaurant reservations, budget tracking. Decides to research flights and hotels first (they constrain the budget for activities).
- **Flight Agent** — Searches for roundtrip flights within the date range and budget. Returns top 3 options.
- **Hotel Agent** — Searches for accommodations near key areas. Returns 3 options with pricing.
- **Coordinator** — Selects flight + hotel combo that leaves the most activity budget. Calculates remaining budget.
- **Activities Agent** — Plans 5 days of activities within the remaining budget, considering location proximity.
- **Coordinator** — Assembles the complete itinerary with day-by-day schedule, budget breakdown, and booking links.

### Research report generation

A manager asks: "Write a competitive analysis of our three main competitors."

- **Coordinator** — Identifies the three competitors, plans the research dimensions (product, pricing, market share, customer sentiment), and assigns per-competitor research.
- **Research Agent A** — Deep-dives into Competitor 1
- **Research Agent B** — Deep-dives into Competitor 2
- **Research Agent C** — Deep-dives into Competitor 3
- **Coordinator** — Synthesizes the three research reports into a unified comparative analysis with a recommendation section.

## When to Use It

- The task requires dynamic decomposition — you can't define all subtasks in advance
- Multiple specialist agents need to contribute to a single coherent output
- Results from one subtask may influence which subtasks come next
- You need one agent to be accountable for the overall plan and output quality
- The final output requires synthesis across multiple sources, not just concatenation

## When NOT to Use It

- Subtasks are known in advance and don't change — use [Sequential](sequential.md) or [Parallel](parallel.md)
- The task is just classification and dispatch — use [Router](router.md) instead
- The coordinator becomes a bottleneck processing every message — consider [Handoff](handoff.md) or [Decentralized](decentralized.md)
- The overhead of coordinator reasoning exceeds the benefit of delegation

## Related Patterns

- [Router](router.md) — classifies and dispatches but doesn't plan or synthesize
- [Sequential](sequential.md) — fixed pipeline; hierarchical is a dynamic pipeline
- [Parallel](parallel.md) — the coordinator often fans out subtasks in parallel
- [Handoff](handoff.md) — peer-to-peer transfers instead of hub-and-spoke delegation
- [Planning](../capability-patterns/planning.md) — the capability pattern the coordinator uses internally
- [Orchestrator-Workers](../../../patterns/workflow-architecture/orchestrator-workers.md) — the workflow architecture equivalent
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "orchestrator-workers" section
- Google Cloud — [Choose a Design Pattern for Agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — hierarchical pattern
- CrewAI — [Hierarchical Process](https://docs.crewai.com/) — framework implementation
