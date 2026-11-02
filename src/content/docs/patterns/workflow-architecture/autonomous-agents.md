---
title: Autonomous Agents
description: "The autonomous agent pattern: an LLM with tools, memory and planning that works toward a goal through a think-act-observe loop until it's done or hits a cap."
last_reviewed: 2026-10-24
---

**Level:** Autonomous. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** agent loop, gather–act–verify.

An **autonomous agent** is an LLM equipped with tools, memory, and planning logic that can interpret a high-level goal, break it into steps, execute actions in an external environment, evaluate feedback, and iterate until it finishes or hits a stop condition.

Unlike the patterns where you define the steps, an agent decides **in real time** which tools to call and how many iterations it needs. This gives it flexibility for open-ended, non-deterministic tasks.

## Why It Matters

| Benefit | Impact |
|---------|--------|
| **Flexibility** | Handles tasks where steps can't be pre-coded — multistep research, dynamic troubleshooting |
| **Ground-truth feedback** | Checks its progress against real tool outputs or API responses at each step, rather than its own guesses |
| **Human-like autonomy** | Mirrors expert work patterns (plan, do, check) and scales them across domains |
| **Rapid iteration** | Adds, repeats, or skips steps until quality criteria or iteration/time limits are hit |

## Key Components: The Agent Loop

| Element | Purpose | Example |
|---------|---------|---------|
| **Human** | Issues the initial goal or provides feedback | "Draft a competitive analysis of ACME vs. BetaCo." |
| **LLM Call (Brain)** | Parses the goal, reasons, and chooses the next action | *Thought:* "I should collect market-share data." |
| **Action** | Invokes one or more tools (API, code, web search) | Calls a market data API for ACME and BetaCo |
| **Environment** | The external system the action touches | Market-data service returns JSON |
| **Feedback** | The result sent back to the LLM for reflection | *Observation:* market-share figures for both companies |
| **Stop** | Task complete or iteration/time cap reached | "Report ready — exit loop." |

The agent cycles through **think → act → observe** until the task is complete or a stop condition is met.

## When to Use It

| Use an Agent When... | Use a Workflow When... |
|---------------------|----------------------|
| Steps are unknown until runtime (open-ended research, debugging) | Steps are fixed and predictable (ETL, translation) |
| Tool selection depends on intermediate results | A single LLM call plus retrieval suffices |
| Human oversight is only needed at checkpoints | Tight latency or cost constraints dominate |

## Example: Autonomous Customer Support Agent

A SaaS company wants an agent that triages inquiries, pulls user data, suggests answers, and closes tickets automatically when confident:

| Loop Phase | What Happens |
|-----------|-------------|
| **Goal** | "Resolve Tier-1 tickets under 3 min average." |
| **Think** | Parse ticket, decide next action |
| **Act** | CRM API → fetch account history. KB search → retrieve relevant article. |
| **Observe** | CRM returns premium plan; KB returns refund policy article |
| **Think** | Compose personalized answer; confidence 0.92 |
| **Act** | Send reply + mark ticket solved |
| **Stop** | Confidence above 0.9 OR max 5 iterations |

What to measure once it runs: the share of tickets it closes without a person, the handle time, and how often a closed ticket is reopened. The agent doesn't retrain on new knowledge-base articles; it finds them through search, so keeping the knowledge base current keeps its answers current.

## How to Implement

1. **Define clear success criteria** — Accuracy, format, KPIs that tell the agent when it's done
2. **Expose the right tools** — Provide tools with explicit documentation and guardrails
3. **Set iteration/time caps** — Prevent runaway loops with maximum iteration counts or time limits
4. **Test in a sandbox** — Measure cost vs. quality, then graduate to production

## Sources

- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024) — the "Agents" section: agents suit "open-ended problems where it's difficult or impossible to predict the required number of steps", gain "ground truth" from the environment at each step, can "pause for human feedback at checkpoints", and commonly have "stopping conditions (such as a maximum number of iterations)"

## Related

- [Workflow Architecture Patterns Overview](../)
- [Orchestrator-Workers](../orchestrator-workers/) — a lead that delegates subtasks to workers; Autonomous when its planning is open-ended
- [Evaluator-Optimizer](../evaluator-optimizer/) — iterative refinement with structured feedback
- [Agents](../../../agentic-building-blocks/agents/) — concepts for building AI agents
- [Planning](../../../agentic-building-blocks/agents/capability-patterns/planning/) — the capability an agent uses to break a goal into steps
- [Group Chat](../group-chat/) and [Swarm](../swarm/) — several agents working toward a goal together
- [Agent Capability Patterns](../../../agentic-building-blocks/agents/capability-patterns/) — behavioral patterns (reflection, tool use, planning, etc.)
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
