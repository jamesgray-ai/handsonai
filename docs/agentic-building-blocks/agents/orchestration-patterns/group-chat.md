---
title: Group Chat (Debate)
description: How multiple agents converse in a shared context, contributing different perspectives — with an optional moderator to synthesize or direct the discussion.
---

# Group Chat (Debate)

## What It Is

The group chat pattern places multiple agents in a shared conversation where they can see and respond to each other's messages. Agents take turns contributing their perspective, building on or challenging what others have said. An optional moderator agent manages turn-taking and synthesizes the discussion into a final output.

Think of it like a panel discussion. Each panelist has a different expertise, and they react to each other's points — agreeing, disagreeing, adding nuance, or redirecting. A moderator keeps the discussion on track and summarizes the key takeaways at the end.

## Why It Matters

Some problems are best solved through deliberation. When a task has no single correct answer — strategic planning, ethical analysis, creative brainstorming — getting multiple agents to argue different positions produces richer, more nuanced results than any single agent could.

Group chat also enables **adversarial verification**. A "devil's advocate" agent can challenge every claim, forcing other agents to defend their reasoning. Research shows that debate between LLMs can surface flaws that neither model would catch on its own.

## How It Works

```text
┌───────────────────────────────┐
│        Shared Context          │
│                                │
│  ┌────┐  ┌────┐  ┌────┐      │
│  │ A1 │  │ A2 │  │ A3 │      │
│  └──┬─┘  └──┬─┘  └──┬─┘      │
│     │       │       │         │
│     └───────┼───────┘         │
│             │                 │
│       ┌─────▼─────┐          │
│       │ Moderator │          │
│       └───────────┘          │
└───────────────────────────────┘
```

1. **Setup** — Each agent is assigned a role, perspective, or expertise area. The shared context (a conversation transcript or workspace) is initialized with the task.
2. **Discussion** — Agents take turns contributing. Turn order can be round-robin, moderator-directed, or self-selected (any agent can speak when it has something to add).
3. **Interaction** — Agents respond to each other — agreeing, challenging, refining, or extending previous contributions. This is what distinguishes group chat from [parallel](parallel.md) execution, where agents work independently.
4. **Moderation** — A moderator agent (optional but recommended) manages the discussion: directing questions to specific agents, preventing circular arguments, and deciding when the discussion has converged.
5. **Synthesis** — The moderator (or a dedicated summarizer) distills the discussion into a final output, capturing areas of agreement, resolved disagreements, and remaining open questions.

## Example

### Strategic decision-making

A company is deciding whether to enter a new market:

- **Market Analyst Agent** — Presents market size data, growth trends, and competitive landscape.
- **Financial Agent** — Models the investment required, projected returns, and risk scenarios.
- **Devil's Advocate Agent** — Challenges every optimistic assumption. "Your growth projection assumes 15% adoption — what's the evidence for that?"
- **Moderator** — Steers the discussion through key decision points, ensures the financial model addresses the devil's advocate's concerns, and produces a recommendation with caveats.

The back-and-forth produces a more rigorous analysis than parallel reports — the devil's advocate forces the other agents to tighten their reasoning.

### Content editorial review

A publishing team reviews an article through multi-perspective discussion:

- **Subject Expert Agent** — Evaluates technical accuracy and depth
- **Audience Agent** — Evaluates clarity and accessibility for the target reader
- **Brand Agent** — Evaluates alignment with editorial voice and guidelines
- **Moderator** — Identifies conflicts between agents ("the expert wants more detail, but the audience agent says it's already too technical"), facilitates resolution, and produces final editorial guidance.

## When to Use It

- The task benefits from multiple perspectives or adversarial analysis
- Agents need to react to and build on each other's ideas (not just work independently)
- Strategic, creative, or evaluative tasks where deliberation improves quality
- You want adversarial verification — agents challenging each other's reasoning
- The output should reflect nuance, trade-offs, and areas of (dis)agreement

## When NOT to Use It

- The task has a single correct answer that doesn't benefit from debate — use [Sequential](sequential.md) or [Parallel](parallel.md)
- Agents don't need to interact — independent parallel execution is simpler and faster
- The discussion could loop indefinitely without converging — always include a turn limit and a moderator
- Token costs from the shared conversation context are prohibitive (each agent sees the full transcript)
- The task is execution-oriented (build this, process that) rather than deliberation-oriented

## Related Patterns

- [Parallel](parallel.md) — agents work independently; group chat adds interaction between agents
- [Evaluator-Optimizer](evaluator-optimizer.md) — structured two-agent feedback loop; group chat is more free-form multi-agent discussion
- [Hierarchical](hierarchical.md) — coordinator directs workers; group chat is more peer-based
- [Decentralized](decentralized.md) — agents also coordinate without a master, but through shared state rather than conversation
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Microsoft Azure — [AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — group chat pattern
- CrewAI — [Framework Documentation](https://docs.crewai.com/) — crew-based multi-agent discussions
- Google ADK — [Developer's Guide to Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — collaborative agent models
