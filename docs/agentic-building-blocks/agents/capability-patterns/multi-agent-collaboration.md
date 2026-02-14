---
title: Multi-Agent Collaboration
description: How multiple specialized AI agents work together to solve problems that are too complex for a single agent.
---

# Multi-Agent Collaboration

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

Common architectures:

- **Orchestrator pattern** — A central agent assigns tasks to specialist agents, collects results, and synthesizes the final output.
- **Pipeline pattern** — Agents are arranged in a sequence where each agent's output becomes the next agent's input (researcher → analyst → writer).
- **Debate pattern** — Two or more agents argue different perspectives, and a judge agent selects or synthesizes the best answer.
- **Peer collaboration** — Agents communicate as equals, each contributing their expertise to a shared workspace.

The key design decisions are:

1. **How many agents?** — Use the minimum number needed. More agents means more coordination overhead.
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

The Writer Agent never sees raw data — it receives a structured brief from the Research Agent. The Editor Agent doesn't know about SEO — it focuses purely on quality. This separation produces better results than a single agent trying to juggle all four concerns.

## When to Use It

- Tasks that require multiple distinct skill sets (research + writing + analysis)
- Workflows where separation of concerns improves quality or safety
- Problems where debate or multiple perspectives lead to better answers
- Systems that need to scale — adding a new capability means adding a new agent, not rewriting the existing one
- Production systems where different agents need different permission levels

## Related Patterns

- [Planning](planning.md) — An orchestrator agent often uses planning to coordinate the team
- [Tool Use](tool-use.md) — Each agent typically has its own set of tools
- [Reflection](reflection.md) — A critic agent reviewing another agent's work is multi-agent reflection
- [Guardrails](guardrails.md) — Each agent can have its own guardrails, limiting what it can do
- [Agent Capability Patterns](index.md)

## Further Reading

- Wu et al. 2023 — *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation* — [arxiv.org/abs/2308.08155](https://arxiv.org/abs/2308.08155)
- Andrew Ng — *Agentic Design Patterns Part 5: Multi-Agent Collaboration* — [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-5-multi-agent-collaboration/)
- Anthropic — *Building Effective Agents* — [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)
- CrewAI — *Multi-Agent Framework Documentation* — [docs.crewai.com](https://docs.crewai.com/)
