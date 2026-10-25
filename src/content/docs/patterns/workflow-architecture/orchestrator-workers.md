---
title: Orchestrator-Workers
description: "The orchestrator-workers pattern: a lead splits the work at runtime, hands subtasks to worker LLM calls or agents, and combines their results into one."
last_reviewed: 2026-10-24
---

**Level:** Guided when the planning is bounded; Autonomous when it's open-ended. See [How Much It Decides](#how-much-it-decides) and [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** manager (OpenAI), hierarchical, supervisor, coordinator (Google), agents-as-tools.

The **orchestrator-workers** pattern uses a central orchestrator that breaks a task down at runtime, delegates subtasks to specialized workers, and synthesizes their outputs into a final result. The workers can be LLM calls or full agents.

Think of it like a project manager leading a cross-functional team. The manager breaks the project into work packages, assigns each to the right team member, tracks progress, handles dependencies, and assembles the final deliverable. The team members focus on execution; the manager handles coordination.

This pattern differs from [parallelization](../parallelization/) because the orchestrator decides the subtasks for each input rather than following a fixed split. It differs from [routing](../routing/) because the orchestrator doesn't just classify and dispatch: it plans, manages, and combines the work.

## Why It Matters

- **Flexibility** — Adapts to varying task requirements, ideal for problems whose parts differ from one input to the next
- **Specialization** — The orchestrator ensures each subtask goes to the most suitable worker
- **Accountability** — One orchestrator is responsible for the overall plan and output quality, while workers focus on their part without needing the big picture
- **Synthesis** — The final output combines the workers' findings into one coherent result, not just a stack of reports

## How It Works

```text
              ┌──────────────────┐
              │   Orchestrator   │
              │  (plan, assign,  │
              │   synthesize)    │
              └──┬────┬────┬────┘
                 │    │    │
                 ▼    ▼    ▼
           ┌────┐ ┌────┐ ┌────┐
           │ W1 │ │ W2 │ │ W3 │
           └──┬─┘ └──┬─┘ └──┬─┘
              │      │      │
              ▼      ▼      ▼
              └──────┴──────┘
                     │
              ┌──────▼──────┐
              │ Orchestrator │
              │ (synthesize) │
              └─────────────┘
```

1. **Plan** — The orchestrator analyzes the task and breaks it into subtasks. This plan may be explicit (a list of steps) or implicit (deciding what to do next as it goes).
2. **Delegate** — The orchestrator assigns each subtask to a worker, giving it focused context and instructions.
3. **Execute** — Workers complete their subtasks and return results. They may run one after another, in parallel, or a mix.
4. **Synthesize** — The orchestrator collects all results, resolves conflicts, fills gaps, and produces the final output.
5. **Iterate** — If results are incomplete or contradictory, the orchestrator may assign more subtasks or ask workers to revise, within its cap on rounds.

## How Much It Decides

The same shape can sit at two levels. What decides the next step is the test:

- **Guided** — The orchestrator splits the work into a known kind of subtasks, using your criteria, with a cap on workers and rounds. For example: one research worker per competitor on your list, each covering the dimensions you set, and one round of follow-up at most. The AI's judgment decides the details, but by your method and within your limits.
- **Autonomous** — The orchestrator decides for itself which subtasks the goal needs, and keeps adding them until it judges the goal met. You can describe the goal, but not the steps.

The number of workers doesn't change the level in either case. Anthropic counts orchestrator-workers as a *workflow* in [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents), which matches the bounded case; the open-ended case behaves like an agent.

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Orchestrator** | Analyzes input, determines required subtasks, assigns them to appropriate workers | Divides a customer query into legal, financial, and technical subtasks |
| **Workers** | Specialized LLM calls or agents that process each subtask | Worker 1: legal analysis, Worker 2: financial evaluation, Worker 3: technical feasibility |
| **Synthesizer** | Combines worker outputs into a coherent final result (often the orchestrator itself) | Merges legal, financial, and technical findings into actionable recommendations |
| **Input/Output** | The original task in, the synthesized result out | Input: multi-faceted customer request → Output: structured report addressing all aspects |

## Predefined vs. Dynamic Workers

The orchestrator can work with both:

- **Predefined workers** — Specialized for known task types (e.g., financial analysis, image recognition). The orchestrator assigns each subtask to the right one.
- **Dynamic workers** — For subtasks nobody anticipated, the orchestrator configures workers on the fly:
    1. **Dynamic configuration** — Tailors a general-purpose LLM with specific prompts to temporarily specialize it
    2. **Tool integration** — Activates external tools or APIs to augment the worker's capabilities
    3. **On-the-fly instantiation** — In advanced systems, generates new worker instances adapted to the task

Dynamic workers point to the Autonomous end; a fixed set of predefined workers with a cap points to the Guided end.

## When to Use It

- **Work that splits differently each time** — When the subtasks depend on the input and can't be fixed in advance
- **Multi-domain expertise** — When the task spans areas requiring different specialized knowledge
- **One coherent output** — When several workers contribute to a single result that needs synthesis, not just concatenation
- **Dependent subtasks** — When results from one subtask may influence which subtasks come next

## When Not to Use It

- Subtasks are known in advance and don't change — use [Prompt Chaining](../prompt-chaining/) or [Parallelization](../parallelization/)
- The task is just classification and dispatch — use [Routing](../routing/) instead
- The orchestrator becomes a bottleneck processing every message — consider [Handoff](../handoff/) or [Swarm](../swarm/)
- The overhead of the orchestrator's reasoning exceeds the benefit of delegation
- One agent could do the job — split the work only for a named reason

## Examples

### Competitive analysis (Guided)

A manager asks: "Write a competitive analysis of our three main competitors."

- **Orchestrator** — Takes the three competitors from your list and the research dimensions you set (product, pricing, market share, customer sentiment), and assigns one worker per competitor.
- **Research Worker A** — Deep-dives into Competitor 1
- **Research Worker B** — Deep-dives into Competitor 2
- **Research Worker C** — Deep-dives into Competitor 3
- **Orchestrator** — Synthesizes the three reports into a unified comparative analysis with a recommendation section.

The kind of subtask is known (one per competitor, your dimensions) and capped, so this is Guided.

### Market research for a new market

A company entering a new market needs analysis across competitor strategy, customer segmentation, and regulatory compliance:

1. **Orchestrator** breaks the task into three subtasks and assigns workers
2. **Worker 1** — Scans competitor pricing, products, and strategies
3. **Worker 2** — Processes demographic and survey data to generate customer segments
4. **Worker 3** — Reviews regulatory documents and flags compliance risks
5. **Synthesizer** — Combines outputs into a unified market research report

If the orchestrator decides a new subtask is needed (e.g., evaluating environmental impact) and creates a worker for it, it's planning toward a goal: Autonomous.

### Trip planning (Autonomous)

A user asks: "Plan a 5-day trip to Tokyo for two people with a $3,000 budget."

- **Orchestrator** — Decomposes: flights, hotels, daily activities, restaurant reservations, budget tracking. Decides to research flights and hotels first (they constrain the budget for activities).
- **Flight Worker** — Searches for roundtrip flights within the date range and budget. Returns top 3 options.
- **Hotel Worker** — Searches for accommodations near key areas. Returns 3 options with pricing.
- **Orchestrator** — Selects the flight and hotel combination that leaves the most activity budget. Calculates the remaining budget.
- **Activities Worker** — Plans 5 days of activities within the remaining budget, considering location proximity.
- **Orchestrator** — Assembles the complete itinerary with a day-by-day schedule, budget breakdown, and booking links.

The number and order of subtasks emerge from the task itself.

## How to Implement

1. **Design the orchestrator** — Build the logic that analyzes inputs and decides the subtask breakdown
2. **Decide how much it decides** — Fix the kinds of subtasks and set caps on workers and rounds (Guided), or let it plan toward the goal (Autonomous)
3. **Define worker capabilities** — Establish predefined workers for known task types and, if needed, rules for dynamic creation
4. **Build the synthesizer** — Define how worker outputs combine into a coherent final result
5. **Test with varied inputs** — Ensure the orchestrator correctly identifies subtasks and assigns them to appropriate workers

## Sources

- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024) — "Workflow: Orchestrator-workers": "the key difference from parallelization is its flexibility—subtasks aren't pre-defined"
- Google Cloud — [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (last reviewed May 28, 2026) — the coordinator and hierarchical task decomposition patterns
- OpenAI — [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF, April 2025) — the manager pattern ("agents as tools")
- OpenAI Agents SDK — [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) (accessed 2026-10-24) — a manager agent calling specialists with `Agent.as_tool()`
- CrewAI — [Processes](https://docs.crewai.com/v1.15.30/en/concepts/processes) (v1.15.30 docs, accessed 2026-10-24) — the hierarchical process, with a manager agent that plans, delegates and validates

## Related

- [Workflow Architecture Patterns Overview](../)
- [Routing](../routing/) — classifies and dispatches but doesn't plan or synthesize
- [Parallelization](../parallelization/) — a similar shape with a fixed split; the orchestrator often fans out subtasks in parallel
- [Prompt Chaining](../prompt-chaining/) — a fixed sequence of steps
- [Handoff](../handoff/) — peer-to-peer transfers instead of hub-and-spoke delegation
- [Planning](../../../agentic-building-blocks/agents/capability-patterns/planning/) — the capability the orchestrator uses to break the work down
- [Autonomous Agents](../autonomous-agents/) — one agent planning its own steps toward a goal
- [Agents](../../../agentic-building-blocks/agents/) — concepts for building AI agents
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
