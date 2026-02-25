---
title: "Parallel (Fan-Out / Fan-In)"
description: How multiple agents work simultaneously on independent subtasks, with results aggregated by a coordinator — for speed, diversity, or reliability.
---

# Parallel (Fan-Out / Fan-In)

## What It Is

The parallel pattern sends the same input (or different subtasks) to multiple agents simultaneously, then aggregates their results. A coordinator fans out the work to agents running in parallel, waits for all of them to complete, and fans in the results into a single output.

Think of it like a newsroom editor assigning different sections of a story to different reporters. Each reporter works independently on their section, and the editor assembles the final piece from all the contributions.

## Why It Matters

Parallel execution solves two problems that sequential pipelines can't:

**Speed.** If three independent subtasks each take 30 seconds sequentially, that's 90 seconds. In parallel, it's 30 seconds.

**Diversity.** Running the same task through multiple agents (or the same agent with different prompts) produces varied perspectives. A coordinator can then select the best result, synthesize multiple viewpoints, or use majority voting to improve reliability.

## How It Works

```text
                ┌─────────┐
           ┌───▸│ Agent A  │───┐
           │    └─────────┘   │
┌────────┐ │    ┌─────────┐   │  ┌────────────┐
│  Input  │─┼───▸│ Agent B  │───┼─▸│ Aggregator │
└────────┘ │    └─────────┘   │  └────────────┘
           │    ┌─────────┐   │
           └───▸│ Agent C  │───┘
                └─────────┘
```

1. **Fan-out** — The coordinator distributes work to multiple agents. This can be the same task (for diversity) or different subtasks (for speed).
2. **Execute** — Each agent works independently and concurrently. They don't communicate with each other.
3. **Fan-in** — The aggregator collects all results and combines them. Aggregation strategies include:
    - **Merge** — combine all outputs into one (e.g., assembling report sections)
    - **Vote** — take the majority answer (e.g., classification confidence)
    - **Select** — pick the best output based on a quality criterion
    - **Synthesize** — produce a new output informed by all results

## Example

### Market research report

A strategy team needs a competitive landscape analysis:

- **Agent A** — Researches competitor pricing and positioning
- **Agent B** — Analyzes market trends and growth projections
- **Agent C** — Reviews customer sentiment and product reviews
- **Aggregator** — Synthesizes all three into a unified market research report

Each agent works with different data sources and produces a different section. The aggregator assembles the report and resolves any contradictions.

### Code review with voting

Three reviewer agents independently review the same pull request:

- **Reviewer 1** — Focuses on correctness and logic errors
- **Reviewer 2** — Focuses on security vulnerabilities
- **Reviewer 3** — Focuses on performance and readability

If two or more reviewers flag the same issue, it's high-confidence. Issues flagged by only one reviewer get a lower priority. This voting approach catches more bugs than any single reviewer.

## When to Use It

- Subtasks are independent and don't depend on each other's output
- Speed is important — parallel execution reduces total wall-clock time
- You want diverse perspectives on the same input (multiple reviewers, varied creative approaches)
- Reliability matters — voting or consensus improves accuracy over a single agent
- The aggregation logic is straightforward (merge sections, pick best, tally votes)

## When NOT to Use It

- Subtasks depend on each other's output — use [Sequential](sequential.md) instead
- You need agents to discuss and build on each other's ideas — use [Group Chat](group-chat.md) instead
- The number of subtasks isn't known until runtime — use [Hierarchical](hierarchical.md) instead
- Running multiple agents costs more than the speed or quality benefit justifies

## Related Patterns

- [Sequential](sequential.md) — for dependent stages that must happen in order
- [Hierarchical](hierarchical.md) — the coordinator dynamically decides what to parallelize
- [Group Chat](group-chat.md) — agents interact with each other instead of working independently
- [Parallelization](../../../patterns/workflow-architecture/parallelization.md) — the workflow architecture equivalent
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "parallelization" section (sectioning and voting)
- Google Cloud — [Choose a Design Pattern for Agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — parallel pattern
- Microsoft Azure — [AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — parallel execution
