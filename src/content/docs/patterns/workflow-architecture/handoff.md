---
title: Handoff
description: "The handoff pattern: the active agent passes the task, with full context, to a better-suited specialist as the task shifts, with no central coordinator."
---

**Level:** Guided. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** OpenAI's "decentralized" pattern. OpenAI uses "decentralized" for agents handing work to one another; this catalogue calls that Handoff, and keeps [Swarm](../swarm/) for peers working from shared state.

The **handoff** pattern transfers responsibility from one agent to another when the conversation or task shifts to a domain where a different agent is better suited. There's no central coordinator deciding who does what — the currently active agent recognizes when the work has moved outside its area and passes the baton to the right peer.

Think of it like a relay race. Each runner carries the baton through their leg of the race, then hands it to the next runner. The difference from [prompt chaining](../prompt-chaining/) is that handoffs aren't predetermined — the active agent decides *when* and *to whom* to hand off based on what's happening.

The active agent judges when to hand off, but only among the specialists you defined and by the triggers you set. That makes this pattern Guided.

## Why It Matters

Many tasks shift as they unfold. A customer starts with a billing question, then mentions a technical issue, then asks about returning the product. A fixed chain of steps can't handle these shifts — it would need to predict the conversation path in advance.

Handoffs let the system adapt. Each agent carries the full conversation context when it takes over, so the customer never repeats themselves. And because the handoff decision is made by the active agent (not a router at the start), it can respond to signals that only appear partway through.

## How It Works

```text
┌─────────┐  handoff  ┌─────────┐  handoff  ┌─────────┐
│ Agent A  │─────────▸│ Agent B  │─────────▸│ Agent C  │
│ (active) │          │ (active) │          │ (active) │
└─────────┘          └─────────┘          └─────────┘
    Billing              Technical            Returns
```

1. **Agent A** is active and handling the task or conversation.
2. **Trigger** — Agent A recognizes that the context has shifted to another agent's area. Triggers can be explicit ("I need help with a return") or implicit (the agent detects a topic shift).
3. **Transfer** — Agent A hands off to Agent B, passing along the full conversation context and any relevant state.
4. **Agent B** takes over as the active agent. It has the full context and can continue seamlessly.
5. **Repeat** — Agent B may later hand off to Agent C, or back to Agent A.

Handoffs can be **one-way** (Agent A → Agent B, done) or **two-way** (agents pass the baton back and forth). The critical design decision is what triggers a handoff — too sensitive and agents ping-pong between each other; too conservative and agents handle tasks they're not suited for. Put a cap on the number of handoffs in one run.

## When to Use It

- Conversational flows where the topic shifts unpredictably
- Tasks where different phases require different expertise, but the transition points aren't predictable
- Systems where agents need full conversation context when they take over
- Multi-turn interactions where a router at the start can't see the whole picture
- The active agent is best positioned to decide when to hand off (it has the most context)

## When Not to Use It

- The task breakdown is known in advance — use [Prompt Chaining](../prompt-chaining/) or [Orchestrator-Workers](../orchestrator-workers/)
- You need a central authority tracking all agents' work — use [Orchestrator-Workers](../orchestrator-workers/)
- Agents need to collaborate simultaneously on the same task — use [Group Chat](../group-chat/)
- Handoff triggers are unreliable, causing agents to ping-pong — simplify to fewer agents or add [Routing](../routing/)

## Examples

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

## Sources

- OpenAI Agents SDK — [Multi-Agent Patterns](https://openai.github.io/openai-agents-python/multi_agent/) — handoff pattern
- OpenAI — [A Practical Guide to Building AI Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) — decentralized pattern
- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — agent delegation patterns
- LangGraph — [Multi-Agent Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent) — handoff strategies

## Related

- [Workflow Architecture Patterns Overview](../)
- [Routing](../routing/) — central dispatch at the start vs. peer-to-peer handoff mid-task
- [Orchestrator-Workers](../orchestrator-workers/) — a lead manages delegation vs. agents handing off to each other
- [Prompt Chaining](../prompt-chaining/) — a predetermined sequence vs. handoffs decided by context
- [Swarm](../swarm/) — peers working from shared state rather than passing the task along
- [Multi-Agent Collaboration](../../../agentic-building-blocks/agents/capability-patterns/multi-agent-collaboration/) — the capability pattern for agent teamwork
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
