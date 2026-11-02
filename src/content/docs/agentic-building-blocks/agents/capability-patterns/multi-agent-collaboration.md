---
title: Multi-Agent Collaboration
description: "How multiple specialized AI agents divide and coordinate work to solve problems too complex for one agent — roles, handoffs, and when the pattern pays off."
last_reviewed: 2026-10-24
---

## What It Is

Multi-agent collaboration is a pattern where multiple AI agents — each with different roles, tools, or expertise — work together to accomplish a task. Instead of one general-purpose agent doing everything, the work is divided among specialists that communicate, delegate, and coordinate.

Think of it like a team at a company: a researcher gathers information, an analyst processes it, a writer drafts the report, and an editor reviews it. Each agent focuses on what it does best, and the combined output is better than any single agent could produce alone.

## Why It Matters

Single agents hit a complexity ceiling. As tasks grow more complex, a single agent's context window fills up, its instructions become contradictory, and its performance degrades. Multi-agent systems solve this by decomposing the problem across agents that each operate with focused context and clear responsibilities.

Multi-agent collaboration also enables **separation of concerns** — a safety-critical agent can enforce policies while a creative agent generates content, without either interfering with the other's role.

## How It Works

```text
┌──────────────┐
│  Orchestrator │
│  (coordinator)│
└──┬───┬───┬───┘
   │   │   │
   ▼   ▼   ▼
┌────┐┌────┐┌────┐
│ A1 ││ A2 ││ A3 │
│    ││    ││    │
└────┘└────┘└────┘
Researcher  Analyst  Writer
```

Common ways to arrange the team, each with its own page in the [Workflow Architecture Patterns](../../../../patterns/workflow-architecture/) catalogue:

- [Orchestrator-Workers](../../../../patterns/workflow-architecture/orchestrator-workers/) — a central agent assigns tasks to specialist agents, collects results, and synthesizes the final output.
- [Prompt Chaining](../../../../patterns/workflow-architecture/prompt-chaining/) — agents in a sequence, where each agent's output becomes the next agent's input (researcher → analyst → writer).
- [Group Chat](../../../../patterns/workflow-architecture/group-chat/) — agents argue different perspectives in a shared conversation, and a moderator synthesizes the result.
- [Swarm](../../../../patterns/workflow-architecture/swarm/) — agents work as peers with no lead, each contributing to a shared workspace.

The catalogue also covers [Handoff](../../../../patterns/workflow-architecture/handoff/), [Parallelization](../../../../patterns/workflow-architecture/parallelization/) and the rest, maps each pattern to an autonomy level, and has a decision tree for choosing one.

The key design decisions are:

1. **How many agents?** — Use the minimum number needed. More agents means more coordination overhead: in Anthropic's own data, a multi-agent system used about 15 times the tokens of a chat, against about 4 times for a single agent ([How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system), June 13, 2025).
2. **How do they communicate?** — Through shared context, message passing, or a shared workspace.
3. **Who decides what?** — An orchestrator, a round-robin, or autonomous negotiation.

## Example

### Customer exchange scenario

A customer exchange can be handled by a team of agents:

- **Triage Agent** — Reads the customer's request, classifies it as "exchange," and routes it to the right specialist.
- **Order Agent** — Looks up the order, verifies return eligibility, and handles the logistics.
- **Inventory Agent** — Checks stock levels and finds the best warehouse to ship from.
- **Communications Agent** — Drafts the customer-facing email with exchange details and return instructions.

Each agent has access only to the tools it needs — the Communications Agent can't process payments, and the Order Agent can't send emails. This limits the blast radius of any single agent's mistakes.

### Content production

A marketing team's content pipeline as a multi-agent system:

- **Research Agent** — Gathers data, competitor analysis, and market trends
- **Writer Agent** — Produces a draft based on the research brief
- **Editor Agent** — Reviews for clarity, accuracy, and brand voice
- **SEO Agent** — Optimizes headlines, metadata, and keyword placement

The Writer Agent never sees raw data — it receives a structured brief from the Research Agent. The Editor Agent doesn't know about SEO — it focuses purely on quality. The separation keeps each agent's instructions and context on one concern, instead of one agent juggling all four.

## When to Use It

- Tasks that require multiple distinct skill sets (research + writing + analysis)
- Workflows where separation of concerns improves quality or safety
- Problems where debate or multiple perspectives lead to better answers
- Systems that need to scale — adding a new capability means adding a new agent, not rewriting the existing one
- Production systems where different agents need different permission levels

## Related Patterns

- [Planning](../planning/) — An orchestrator agent often uses planning to coordinate the team
- [Tool Use](../tool-use/) — Each agent typically has its own set of tools
- [Reflection](../reflection/) — A critic agent reviewing another agent's work is multi-agent reflection
- [Guardrails](../guardrails/) — Each agent can have its own guardrails, limiting what it can do
- [Agent Capability Patterns](../)

## Further Reading

- Andrew Ng — [Agentic Design Patterns Part 5, Multi-Agent Collaboration](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration) (*The Batch*, April 17, 2024) — the last of his four patterns
- Wu et al. — [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) (arXiv, August 16, 2023)
- Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) (June 13, 2025)
- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024)
- CrewAI — [Processes](https://docs.crewai.com/v1.15.30/en/concepts/processes) (v1.15.30 docs, accessed 2026-10-24) — sequential and hierarchical crews
