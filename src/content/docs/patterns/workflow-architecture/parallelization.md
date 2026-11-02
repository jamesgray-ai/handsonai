---
title: Parallelization
description: "The parallelization pattern — run independent subtasks simultaneously and aggregate the results for faster, more reliable AI workflows, with examples."
last_reviewed: 2026-10-24
---

**Level:** Deterministic when the split is fixed; Guided if the AI judges the vote. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** parallel, fan-out / fan-in, sectioning, voting.

**Parallelization** divides subtasks of a larger problem and processes them simultaneously through separate LLM calls or agents. The outputs are then aggregated to produce the final result.

Think of it like a newsroom editor assigning different sections of a story to different reporters. Each reporter works independently on their section, and the editor assembles the final piece from all the contributions.

This pattern has two primary variations:

- **Sectioning** — Breaking a task into independent subtasks, each processed in parallel
- **Voting** — Running the same task multiple times to generate diverse perspectives, then aggregating for higher confidence

## Why It Matters

- **Increased speed** — Independent subtasks finish in about the time of the slowest one, not the sum of all of them
- **Enhanced reliability** — Multiple evaluations or diverse subtasks processed in parallel produce higher-confidence results
- **Focused task management** — Specialized LLM calls handle each subtask, improving accuracy through focused attention
- **Scalability** — Larger datasets or more complex workflows are handled without bottlenecking a single model

Anthropic names both reasons: parallelization is effective "when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results". Other sources lean one way or the other. Name the one you're after, because it decides how you combine the results.

## How It Works

```text
                ┌─────────┐
           ┌───▸│ Call A   │───┐
           │    └─────────┘   │
┌────────┐ │    ┌─────────┐   │  ┌────────────┐
│  Input  │─┼───▸│ Call B   │───┼─▸│ Aggregator │
└────────┘ │    └─────────┘   │  └────────────┘
           │    ┌─────────┐   │
           └───▸│ Call C   │───┘
                └─────────┘
```

1. **Fan-out** — The work is sent to several LLM calls or agents at once. This can be the same task (for diversity) or different subtasks (for speed).
2. **Execute** — Each one works independently and concurrently. They don't communicate with each other.
3. **Fan-in** — The aggregator collects all results and combines them. There are four ways to combine:
    - **Merge** — combine all outputs into one (e.g., assembling report sections)
    - **Vote** — take the majority answer (e.g., classification confidence)
    - **Select** — pick the best output based on a quality criterion
    - **Synthesize** — produce a new output informed by all results

The split and the combining rule set the level. A fixed split whose results are merged or tallied by your rules is Deterministic. When the AI judges the vote, or selects the best output by your criteria, its judgment decides what happens next: Guided.

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Parallel LLM Calls** | Each handles a different subtask (sectioning) or repeats the same task (voting) | One call evaluates content for tone, another for factual accuracy, another for compliance |
| **Aggregator** | Combines parallel outputs into a unified result (merging, voting, selecting, or synthesizing) | Merges flagged issues from parallel code reviews into a comprehensive report |
| **Input/Output** | Input initiates all parallel processes; output delivers aggregated results | Input: a large dataset → Output: a combined analysis report |

## When to Use It

- **Independent subtasks** — Subtasks don't depend on each other's output
- **Speed-intensive tasks** — Time-sensitive workflows requiring simultaneous processing
- **Tasks with multiple dimensions** — Multiple independent considerations that can be evaluated separately
- **Higher confidence needs** — Outputs requiring validation through multiple attempts or perspectives
- **Straightforward aggregation** — Merging sections, picking the best, or tallying votes

## When Not to Use It

- Subtasks depend on each other's output — use [Prompt Chaining](../prompt-chaining/) instead
- You need agents to discuss and build on each other's ideas — use [Group Chat](../group-chat/) instead
- The number of subtasks isn't known until runtime — use [Orchestrator-Workers](../orchestrator-workers/) instead
- Running several calls or agents costs more than the speed or quality benefit justifies

## Examples

### Market research analysis

A company needs comprehensive market analysis for a product launch covering competitor analysis, consumer trends, and regional insights:

**Sectioning approach:**

1. **Parallel Call 1** — Evaluates competitors' pricing and positioning
2. **Parallel Call 2** — Analyzes customer preferences and behaviors
3. **Parallel Call 3** — Studies market potential across regions
4. **Aggregator** — Combines all findings into one comprehensive report and resolves any contradictions

**Voting approach (for uncertain predictions):**

1. Multiple models independently predict regional sales figures
2. The aggregator evaluates and combines predictions for a well-rounded decision

### Code review with voting

Three reviewers independently review the same pull request:

- **Reviewer 1** — Focuses on correctness and logic errors
- **Reviewer 2** — Focuses on security vulnerabilities
- **Reviewer 3** — Focuses on performance and readability

If two or more reviewers flag the same issue, it's high-confidence. Issues flagged by only one reviewer get a lower priority.

## How to Implement

1. **Identify subtasks** — Break the problem into components that can be processed independently
2. **Determine parallelization type** — Sectioning (dividing tasks) or voting (repeating with different approaches)
3. **Set up aggregation rules** — Define how outputs combine (merge, vote, select, synthesize)
4. **Test and optimize** — Ensure efficient operation and consistent, high-quality outputs

## Sources

- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024) — "Workflow: Parallelization", with its two variations, sectioning and voting
- Google Cloud — [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (last reviewed May 28, 2026) — the multi-agent parallel pattern
- Microsoft — [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), Azure Architecture Center (accessed 2026-10-24) — "Concurrent orchestration", also known as parallel, fan-out/fan-in, scatter-gather or map-reduce

## Related

- [Workflow Architecture Patterns Overview](../)
- [Prompt Chaining](../prompt-chaining/) — for dependent stages that must happen in order
- [Routing](../routing/) — directs to one specialized path; parallelization runs multiple paths simultaneously
- [Orchestrator-Workers](../orchestrator-workers/) — a similar shape, but the lead decides the subtasks at runtime
- [Group Chat](../group-chat/) — agents interact with each other instead of working independently
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
