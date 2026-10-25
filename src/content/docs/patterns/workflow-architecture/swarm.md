---
title: Swarm
description: "The swarm pattern: peer agents with no lead build on each other's work, by messaging each other or through shared state, until an exit condition is met."
last_reviewed: 2026-10-24
---

**Level:** Autonomous. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** decentralized (the playbook's earlier name for this page). Google names this pattern "swarm". Note that OpenAI uses "decentralized" for agents handing work to one another, which this catalogue calls [Handoff](../handoff/); OpenAI's experimental Swarm framework, despite its name, was also built on handoffs.

The **swarm** pattern organizes agents as peers with no lead. Instead of a central agent planning and delegating, each agent decides what to do next from what the others have done. Agents pick up work, contribute results, and react to each other's outputs, refining the answer over many rounds.

Think of it like an ant colony. No single ant directs the colony — each ant follows simple rules (find food, follow pheromone trails, bring food back) and the collective behavior emerges from many independent agents reacting to shared signals.

No one sets the steps: what gets done next emerges from the agents reacting to each other's work. That makes this pattern Autonomous.

## Why It Matters

Some tasks are too dynamic for any single agent to plan ahead. In highly fluid situations — real-time monitoring, exploratory research, open-ended problem solving — the right next step depends on what just happened, and changes too fast for a central coordinator to keep up.

A swarm can also be **resilient**. With no lead, one agent failing doesn't stop the others, so the system can degrade gracefully rather than halting entirely.

Google describes the swarm as the most complex and costly of its multi-agent patterns: many rounds of agent conversation add latency and cost, and without good control logic the agents can loop or fail to agree. Use it only when simpler patterns can't handle the task.

## How It Works

Peers coordinate in one of two ways:

- **By messaging each other.** In Google's description, each agent can talk to every other agent and hand the task to whichever is better suited for the next step. A dispatcher may route the first request in, but it doesn't direct the work.
- **Through shared state.** Agents read and write a shared task board, message queue or workspace (sometimes called a blackboard), and never message each other directly. The diagram and steps below show this version.

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

In this version, agents don't need to know about each other, only about the shared state. In either version, no one is in charge of stopping, so set an explicit exit condition that every agent respects: a cap on rounds or actions, a time limit, or a goal such as agreement on the answer.

## When to Use It

- Tasks are highly dynamic — the next step depends on what was just discovered
- The problem is ambiguous or highly complex and benefits from debate and repeated refinement (Google's example: agents weighing design trade-offs until they agree on a product specification)
- No single agent can plan the entire task in advance
- Resilience matters — the system should degrade gracefully if agents fail
- The task naturally breaks into many small, independent contributions
- Exploration is more important than efficiency (research, monitoring, discovery)

## When Not to Use It

- The task has a predictable structure — use [Prompt Chaining](../prompt-chaining/), [Parallelization](../parallelization/), or [Orchestrator-Workers](../orchestrator-workers/)
- Coordination overhead exceeds the benefit — a simpler pattern is the better choice whenever it fits
- You need guaranteed output quality — swarms are harder to quality-control than centrally coordinated systems
- The task requires a single coherent narrative or tightly integrated output — use [Orchestrator-Workers](../orchestrator-workers/) with a synthesizing lead
- You can't afford the complexity of shared state management, conflict resolution, and deadlock prevention

## Examples

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

- **Log Agent** — Notices an error spike in logs, posts findings to the incident board.
- **Metrics Agent** — Detects a latency increase, correlates it with the log agent's findings.
- **Deployment Agent** — Checks recent deployments, finds a deploy that correlates with the incident timing.
- **Remediation Agent** — Sees the correlated deployment and proposes a rollback.

Each agent acts independently based on shared signals. A rollback changes production, so it's the kind of action that belongs behind a [Human Checkpoint](../../../agentic-building-blocks/agents/capability-patterns/human-in-the-loop/).

## Sources

- Google Cloud — [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (last reviewed May 28, 2026) — the multi-agent swarm pattern: "all-to-all communication", no central supervisor, and "an explicit exit condition"
- OpenAI — [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF, April 2025) — "decentralized" for agents handing off to agents (this catalogue's Handoff)
- OpenAI Agents SDK — [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) (accessed 2026-10-24) — the successor to OpenAI's Swarm framework, whose README now says "Swarm is now replaced by the OpenAI Agents SDK"

## Related

- [Workflow Architecture Patterns Overview](../)
- [Orchestrator-Workers](../orchestrator-workers/) — central coordination; a swarm removes the lead
- [Group Chat](../group-chat/) — agents also coordinate as peers, but through conversation rather than shared state
- [Parallelization](../parallelization/) — agents work independently, but with a fixed fan-out rather than picking their own work
- [Handoff](../handoff/) — peer-to-peer transfers, but one agent at a time rather than all at once
- [Multi-Agent Collaboration](../../../agentic-building-blocks/agents/capability-patterns/multi-agent-collaboration/) — the capability pattern for agent teamwork
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
