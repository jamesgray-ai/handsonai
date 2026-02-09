---
title: Agents
description: Decide when your workflow needs autonomous AI execution — and when a prompt is enough.
---

# Agents

> **Part of:** [Build Workflows](index.md)

!!! tip "New to agents as a building block?"
    See [Agentic Building Blocks > Agents](../../agentic-building-blocks/agents/index.md) for definitions, examples, and cross-platform implementation details.

## What This Is

The agent decision framework. Not every workflow needs an agent — many work perfectly as a prompt you paste and run. This page helps you decide when autonomous execution is worth the investment, and how to build your first agent when it is.

| | |
|---|---|
| **What you'll do** | Review your Building Block Map for steps tagged "Agent," decide whether to build agents, then design the first one |
| **What you'll get** | A clear decision on agent vs. prompt for each workflow step, and agent definitions for steps that need autonomous execution |
| **Time** | 15-30 minutes per agent |

## The Agent Decision Framework

**Not every workflow needs an agent.** Many workflows work perfectly as a prompt — paste it in, run it, get results. That's a feature, not a limitation.

### When a prompt is enough

- All steps can be completed in a single conversation
- No tool use needed (no web browsing, no file access, no API calls)
- Human provides all inputs and reviews all outputs
- Steps are sequential and straightforward

### When you need an agent

- The step requires **tool use** — browsing the web, reading/writing files, calling APIs
- The step requires **autonomous execution** — the AI needs to make decisions and take actions without asking you at each step
- The step requires **multi-step reasoning with memory** — the AI needs to plan, execute, and adjust based on results
- The step spans **multiple conversations** or needs to **persist state** across sessions

### When to use multiple agents

- Different steps require different domain expertise (researcher vs. writer vs. editor)
- Steps can run independently (parallel execution)
- You want human review gates between phases

The [Autonomous Agent](autonomous-agent.md) worked example shows a multi-agent pipeline with 4 specialized agents.

## Building Your First Agent

1. **Look at your Building Block Map** for steps tagged with "Agent"
2. **Group related steps** — Contiguous steps with the same expertise domain become one agent
3. **Write the agent's system prompt** using those steps — describe the agent's role, what it knows, and what it does
4. **Define human review gates** — Where should the agent pause for your approval?
5. **Test with a real scenario** — Run the agent on actual inputs and evaluate the output

## Agent Anatomy

What an agent definition contains:

- **Name** — What the agent is called (e.g., `meeting-prep-researcher`)
- **Description** — When to activate this agent and what it does
- **Model** — Which AI model to use (affects capability and cost)
- **System prompt** — The agent's role, expertise, process, and constraints

For platform-specific implementation details, see [Agentic Building Blocks > Agents](../../agentic-building-blocks/agents/index.md).

## What's Next

If your workflow requires external tool access (databases, APIs, browsers), see [MCP](mcp.md) for connecting AI to your tools. Otherwise, test your baseline prompt and build incrementally.
