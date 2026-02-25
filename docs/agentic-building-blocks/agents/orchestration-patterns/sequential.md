---
title: "Sequential (Pipeline)"
description: How agents execute in linear order — each agent's output becomes the next agent's input — creating reliable, debuggable multi-agent pipelines.
---

# Sequential (Pipeline)

## What It Is

The sequential pattern arranges agents in a linear chain where each agent's output becomes the next agent's input. Agent A completes its work, passes the result to Agent B, which passes its result to Agent C, and so on until the final agent produces the output.

Think of it like an assembly line in a factory. Each station performs one operation, inspects the result, and passes the workpiece to the next station. No station starts until it receives input from the one before it.

## Why It Matters

Sequential pipelines are the simplest multi-agent pattern to build, test, and debug. When something goes wrong, you can inspect the output at each stage to find exactly where the problem occurred. This makes them the default starting point for most multi-agent systems.

Sequential pipelines also enable **validation gates** — checkpoints between agents where the output is verified before the next agent begins. This catches errors early instead of letting them propagate through the entire chain.

## How It Works

```text
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Agent A  │────▸│ Agent B  │────▸│ Agent C  │────▸│  Output  │
│ Research │     │ Analyze  │     │  Write   │     │          │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │
  Gate 1          Gate 2          Gate 3
 (validate)      (validate)      (validate)
```

1. **Agent A** receives the initial input and produces its output.
2. **Gate 1** validates Agent A's output (optional but recommended). If it fails, Agent A retries or the pipeline halts.
3. **Agent B** receives Agent A's validated output and produces its own output.
4. The pattern repeats until the final agent delivers the result.

Each agent operates with focused context — it only sees what it needs from the previous stage, not the entire task history. This keeps prompts clean and reduces token costs.

## Example

### Content production pipeline

A marketing team's content workflow as a sequential pipeline:

1. **Research Agent** — Receives a topic brief, gathers data from web sources and internal docs, outputs a structured research summary.
2. **Writer Agent** — Receives the research summary, drafts an article following brand guidelines.
3. **Editor Agent** — Receives the draft, checks for clarity, accuracy, and tone. Outputs a revised version.
4. **SEO Agent** — Receives the edited article, optimizes headlines, metadata, and keyword placement. Outputs the final publish-ready piece.

Each agent is a specialist. The Writer never sees raw search results — it receives a clean brief from the Research Agent. The SEO Agent never rewrites for tone — that's already handled.

### Customer support triage

1. **Classifier Agent** — Reads the incoming support ticket, categorizes it (billing, technical, returns), and extracts key details.
2. **Policy Agent** — Looks up the relevant policy based on the classification and determines what actions are permitted.
3. **Response Agent** — Drafts a customer-facing response using the classification and policy constraints.
4. **Compliance Agent** — Reviews the draft for regulatory compliance before sending.

## When to Use It

- Tasks that naturally decompose into ordered stages (research → write → edit)
- Workflows where each stage requires different expertise or tools
- Pipelines where you need validation gates between steps
- Systems where debuggability matters — you need to trace where things went wrong
- Content workflows, data processing pipelines, and approval chains

## When NOT to Use It

- Stages are independent and could run simultaneously — use [Parallel](parallel.md) instead
- The number or order of stages isn't known until runtime — use [Hierarchical](hierarchical.md) instead
- The task requires iteration between stages (writer ↔ editor back-and-forth) — use [Evaluator-Optimizer](evaluator-optimizer.md) instead
- You only need one agent — adding a pipeline adds complexity without benefit

## Related Patterns

- [Parallel](parallel.md) — run independent stages simultaneously instead of sequentially
- [Evaluator-Optimizer](evaluator-optimizer.md) — adds a feedback loop between generator and evaluator
- [Hierarchical](hierarchical.md) — dynamic task decomposition when stages aren't fixed
- [Prompt Chaining](../../../patterns/workflow-architecture/prompt-chaining.md) — the single-agent equivalent (sequential LLM calls without separate agents)
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "prompt chaining" section
- Google Cloud — [Choose a Design Pattern for Agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — sequential pattern
- CrewAI — [Sequential Process](https://docs.crewai.com/) — framework implementation
