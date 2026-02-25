---
title: Decentralized (Swarm)
description: How peer agents coordinate without a central controller — communicating through shared state or message passing to handle highly dynamic tasks.
---

# Decentralized (Swarm)

## What It Is

The decentralized pattern (sometimes called "swarm") organizes agents as peers with no master coordinator. Instead of a central agent planning and delegating, each agent independently decides what to do based on the current shared state — a shared workspace, message queue, or task board. Agents pick up work, contribute results, and react to each other's outputs autonomously.

Think of it like an ant colony. No single ant directs the colony — each ant follows simple rules (find food, follow pheromone trails, bring food back) and the collective behavior emerges from many independent agents reacting to shared signals.

## Why It Matters

Some tasks are too dynamic for any single agent to plan ahead. In highly fluid situations — real-time monitoring, exploratory research, open-ended problem solving — the "right" next step depends on what just happened, and changes too fast for a central coordinator to keep up.

Decentralized systems are also **resilient**. If one agent fails, the others continue working. There's no single point of failure, and the system degrades gracefully rather than halting entirely.

This is the most advanced orchestration pattern and carries the highest coordination overhead. Use it only when simpler patterns can't handle the task's dynamism.

## How It Works

```text
┌──────────────────────────────────┐
│         Shared State             │
│  (task board / message queue /   │
│   shared workspace)              │
└──┬────┬────┬────┬────┬──────────┘
   │    │    │    │    │
   ▼    ▼    ▼    ▼    ▼
 ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
 │A1│ │A2│ │A3│ │A4│ │A5│
 └──┘ └──┘ └──┘ └──┘ └──┘
  (all agents are peers)
```

1. **Shared state** — A central data structure (task board, message queue, shared document, or blackboard) holds the current state of the task. All agents can read from and write to it.
2. **Observe** — Each agent independently reads the shared state to understand what's been done and what needs doing.
3. **Decide** — Based on its capabilities and the current state, each agent decides whether to act and what to do. Simple rules prevent conflicts (e.g., claim a task before starting it).
4. **Act** — The agent performs its work and writes results back to the shared state.
5. **React** — Other agents observe the updated state and may take new actions in response.

Coordination happens through the shared state, not through direct agent-to-agent communication. This is what makes the system decentralized — agents don't need to know about each other, only about the shared state.

## Example

### Research exploration

An open-ended research task: "Map the competitive landscape for AI code assistants."

- **Shared state** — A research board with columns: `to-research`, `in-progress`, `completed`, `insights`.
- **Agent 1** — Claims "GitHub Copilot" from the to-research queue. Researches pricing, features, market share. Posts findings and adds "Copilot vs Cursor comparison" to the to-research queue.
- **Agent 2** — Claims "Cursor" and researches it independently.
- **Agent 3** — Sees the comparison task appear. Claims it. Uses Agent 1 and Agent 2's completed findings to write the comparison.
- **Agent 4** — Monitors the insights column. When enough data accumulates, synthesizes a landscape summary.

No agent planned the full research sequence. The work emerged from agents reacting to the evolving shared state.

### Incident response

A production incident triggers multiple monitoring agents:

- **Log Agent** — Notices error spike in logs, posts findings to the incident board.
- **Metrics Agent** — Detects latency increase, correlates with the log agent's findings.
- **Deployment Agent** — Checks recent deployments, finds a deploy that correlates with the incident timing.
- **Remediation Agent** — Sees the correlated deployment, triggers a rollback.

Each agent acts independently based on shared signals. The incident response emerges from their collective behavior.

## When to Use It

- Tasks are highly dynamic — the next step depends on what was just discovered
- No single agent can plan the entire task in advance
- Resilience matters — the system should degrade gracefully if agents fail
- The task naturally decomposes into many small, independent contributions
- Exploration is more important than efficiency (research, monitoring, discovery)

## When NOT to Use It

- The task has a predictable structure — use [Sequential](sequential.md), [Parallel](parallel.md), or [Hierarchical](hierarchical.md)
- Coordination overhead exceeds the benefit — simpler patterns are almost always better when they fit
- You need guaranteed output quality — decentralized systems are harder to quality-control than centrally coordinated ones
- The task requires a single coherent narrative or tightly integrated output — use [Hierarchical](hierarchical.md) with a synthesizing coordinator
- You can't afford the complexity of shared state management, conflict resolution, and deadlock prevention

## Related Patterns

- [Hierarchical](hierarchical.md) — centralized coordination; decentralized removes the coordinator
- [Group Chat](group-chat.md) — agents also coordinate as peers, but through conversation rather than shared state
- [Parallel](parallel.md) — agents work independently, but with a predetermined fan-out rather than emergent task selection
- [Handoff](handoff.md) — peer-to-peer transfers, but sequential rather than concurrent
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Google ADK — [Developer's Guide to Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — decentralized orchestration
- Google Cloud — [Choose a Design Pattern for Agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — swarm pattern
- OpenAI — [Swarm Framework](https://github.com/openai/swarm) — experimental decentralized agent framework
