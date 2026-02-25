---
title: Handoff
description: How responsibility transfers between peer agents as context evolves — no central coordinator, just agents passing the baton when another agent is better suited.
---

# Handoff

## What It Is

The handoff pattern transfers responsibility from one agent to another when the conversation or task context shifts to a domain where a different agent is better suited. There's no central coordinator deciding who does what — the currently active agent recognizes when it's out of its depth and passes the baton to the right peer.

Think of it like a relay race. Each runner carries the baton through their leg of the race, then hands it off to the next runner. The key difference from a [sequential pipeline](sequential.md) is that handoffs aren't predetermined — the active agent decides *when* and *to whom* to hand off based on real-time context.

## Why It Matters

Many tasks evolve unpredictably as they unfold. A customer starts with a billing question, then mentions a technical issue, then asks about returning the product. A rigid pipeline can't handle these shifts — it would need to predict the conversation path in advance.

Handoffs let the system adapt fluidly. Each agent carries full conversation context when it takes over, so the customer never repeats themselves. And because the handoff decision is made by the active agent (not a central router), it can be more nuanced — based on conversation signals rather than a single classification.

## How It Works

```text
┌─────────┐  handoff  ┌─────────┐  handoff  ┌─────────┐
│ Agent A  │─────────▸│ Agent B  │─────────▸│ Agent C  │
│ (active) │          │ (active) │          │ (active) │
└─────────┘          └─────────┘          └─────────┘
    Billing              Technical            Returns
```

1. **Agent A** is active and handling the task or conversation.
2. **Trigger** — Agent A recognizes that the context has shifted to another agent's expertise. Triggers can be explicit ("I need help with a return") or implicit (the agent detects a topic shift).
3. **Transfer** — Agent A hands off to Agent B, passing along the full conversation context and any relevant state.
4. **Agent B** takes over as the active agent. It has the full context and can continue seamlessly.
5. **Repeat** — Agent B may later hand off to Agent C, or even back to Agent A.

Handoffs can be **one-way** (Agent A → Agent B, done) or **bidirectional** (agents pass the baton back and forth). The critical design decision is what triggers a handoff — too sensitive and agents ping-pong between each other; too conservative and agents handle tasks they're not suited for.

## Example

### Customer support conversation

A customer contacts support:

1. **Triage Agent** — Greets the customer, asks how it can help. Customer says "I was charged twice for my order."
2. **→ Handoff to Billing Agent** — Triage detects a billing issue. Passes full context.
3. **Billing Agent** — Looks up the order, confirms the double charge, processes a refund. Customer then asks "Also, the product I received doesn't work."
4. **→ Handoff to Technical Agent** — Billing detects a product issue outside its scope. Passes context including the refund resolution.
5. **Technical Agent** — Has the full conversation history. Troubleshoots the product issue without asking the customer to repeat anything.

### Software development workflow

A coding assistant with specialized agents:

1. **Planner Agent** — Receives a feature request, breaks it into implementation steps, writes the plan. Hands off to the implementer.
2. **→ Handoff to Coder Agent** — The coder builds the feature following the plan. Encounters a test failure it can't resolve.
3. **→ Handoff to Debugger Agent** — The debugger diagnoses the failure, fixes the bug, and hands back.
4. **→ Handoff to Coder Agent** — The coder continues building the rest of the feature.

## When to Use It

- Conversational flows where the topic shifts unpredictably
- Tasks where different phases require different expertise, but the transition points aren't predictable
- Systems where agents need full conversation context when they take over
- Multi-turn interactions where a central router can't see the whole picture
- The active agent is best positioned to decide when to hand off (it has the most context)

## When NOT to Use It

- The task decomposition is known in advance — use [Sequential](sequential.md) or [Hierarchical](hierarchical.md)
- You need a central authority tracking all agents' work — use [Hierarchical](hierarchical.md)
- Agents need to collaborate simultaneously on the same task — use [Group Chat](group-chat.md)
- Handoff triggers are unreliable, causing agents to ping-pong — simplify to fewer agents or add a [Router](router.md)

## Related Patterns

- [Router](router.md) — centralized dispatch at the start vs. peer-to-peer handoff mid-task
- [Hierarchical](hierarchical.md) — coordinator-managed delegation vs. autonomous handoff
- [Sequential](sequential.md) — predetermined pipeline vs. dynamic handoff based on context
- [Multi-Agent Collaboration](../capability-patterns/multi-agent-collaboration.md) — the capability pattern for agent teamwork
- [Orchestration Patterns Overview](index.md)

## Further Reading

- OpenAI Agents SDK — [Multi-Agent Patterns](https://openai.github.io/openai-agents-python/multi_agent/) — handoff pattern
- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — agent delegation patterns
- LangGraph — [Multi-Agent Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent) — handoff strategies
