---
title: Group Chat
description: "The group chat pattern: several agents with different roles discuss a task in a shared conversation, with a moderator who steers the debate and sums it up."
---

**Level:** Autonomous. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** debate.

The **group chat** pattern places multiple agents in a shared conversation where they can see and respond to each other's messages. Agents take turns contributing their perspective, building on or challenging what others have said. A moderator agent manages turn-taking and synthesizes the discussion into a final output.

Think of it like a panel discussion. Each panelist has a different expertise, and they react to each other's points — agreeing, disagreeing, adding nuance, or redirecting. A moderator keeps the discussion on track and summarizes the key takeaways at the end.

Where the discussion goes, and when it has reached an answer, emerges from the agents' exchange rather than from steps you set. That makes this pattern Autonomous.

## Why It Matters

Some problems are best solved through deliberation. When a task has no single correct answer — strategic planning, ethical analysis, creative brainstorming — getting multiple agents to argue different positions can produce richer, more nuanced results than any single agent could.

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

1. **Setup** — Each agent is assigned a role, perspective, or area of expertise. The shared context (a conversation transcript or workspace) is initialized with the task.
2. **Discussion** — Agents take turns contributing. Turn order can be round-robin, moderator-directed, or self-selected (any agent can speak when it has something to add).
3. **Interaction** — Agents respond to each other — agreeing, challenging, refining, or extending previous contributions. This is what distinguishes group chat from [parallelization](../parallelization/), where agents work independently.
4. **Moderation** — A moderator agent (optional but recommended) manages the discussion: directing questions to specific agents, preventing circular arguments, and deciding when the discussion has converged.
5. **Synthesis** — The moderator (or a dedicated summarizer) distills the discussion into a final output, capturing areas of agreement, resolved disagreements, and remaining open questions.

Always set a turn limit. Without one, a discussion can loop indefinitely without converging.

## When to Use It

- The task benefits from multiple perspectives or adversarial analysis
- Agents need to react to and build on each other's ideas (not just work independently)
- Strategic, creative, or evaluative tasks where deliberation improves quality
- You want adversarial verification — agents challenging each other's reasoning
- The output should reflect nuance, trade-offs, and areas of (dis)agreement

## When Not to Use It

- The task has a single correct answer that doesn't benefit from debate — use [Prompt Chaining](../prompt-chaining/) or [Parallelization](../parallelization/)
- Agents don't need to interact — independent parallel work is simpler and faster
- You can't set a turn limit and a moderator — the discussion could loop indefinitely without converging
- Token costs from the shared conversation context are prohibitive (each agent sees the full transcript)
- The task is execution-oriented (build this, process that) rather than deliberation-oriented

## Examples

### Strategic decision-making

A company is deciding whether to enter a new market:

- **Market Analyst Agent** — Presents market size data, growth trends, and competitive landscape.
- **Financial Agent** — Models the investment required, projected returns, and risk scenarios.
- **Devil's Advocate Agent** — Challenges every optimistic assumption. "Your growth projection assumes 15% adoption — what's the evidence for that?"
- **Moderator** — Steers the discussion through key decision points, ensures the financial model addresses the devil's advocate's concerns, and produces a recommendation with caveats.

The back-and-forth tests each agent's reasoning in a way separate parallel reports don't.

### Content editorial review

A publishing team reviews an article through multi-perspective discussion:

- **Subject Expert Agent** — Evaluates technical accuracy and depth
- **Audience Agent** — Evaluates clarity and accessibility for the target reader
- **Brand Agent** — Evaluates alignment with editorial voice and guidelines
- **Moderator** — Identifies conflicts between agents ("the expert wants more detail, but the audience agent says it's already too technical"), facilitates resolution, and produces final editorial guidance.

## Sources

- Microsoft Azure — [AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — group chat pattern
- CrewAI — [Framework Documentation](https://docs.crewai.com/) — crew-based multi-agent discussions
- Google ADK — [Developer's Guide to Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — collaborative agent models

## Related

- [Workflow Architecture Patterns Overview](../)
- [Parallelization](../parallelization/) — agents work independently; group chat adds interaction between agents
- [Evaluator-Optimizer](../evaluator-optimizer/) — a structured two-part feedback loop; group chat is a freer multi-agent discussion
- [Orchestrator-Workers](../orchestrator-workers/) — a lead directs workers; group chat is more peer-based
- [Swarm](../swarm/) — agents also coordinate without a lead, but through shared state rather than conversation
- [Multi-Agent Collaboration](../../../agentic-building-blocks/agents/capability-patterns/multi-agent-collaboration/) — the capability pattern for agent teamwork
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
