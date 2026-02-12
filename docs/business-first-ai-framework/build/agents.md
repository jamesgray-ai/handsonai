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
| **What you'll do** | Review your Building Block Spec for steps tagged "Agent," decide whether to build agents, then design the first one |
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

1. **Look at your Building Block Spec** for steps tagged with "Agent"
2. **Group related steps** — Contiguous steps with the same expertise domain become one agent
3. **Write the agent's instructions** — Describe the agent's role, what it knows, and what it does. Think of it as writing a job description: "You are a researcher who finds case studies from business publications. You search for companies with quantified outcomes and produce structured briefs." Your Building Block Spec's Action, Decision Points, and Context Needed columns give you most of this.
4. **Define human review gates** — Where should the agent pause for your approval?
5. **Test with a real scenario** — Run the agent on actual inputs and evaluate the output
6. **Register and commit** — Add the agent to your [AI Registry](../../plugins/ai-registry.md) Notion database and commit the agent `.md` file to your GitHub repository


## Agent Anatomy

What an agent definition contains:

- **Name** — What the agent is called (e.g., `meeting-prep-researcher`)
- **Description** — When to activate this agent and what it does
- **Model** — Which AI model to use (affects capability and cost)
- **Instructions** (also called a "system prompt") — The agent's role, expertise, process, and constraints — written in plain language, just like you'd brief a new team member
- **Tools** — What the agent can interact with to carry out its work — web search, file access, APIs, databases, MCP servers, or other external services. Without tools, an agent is just a prompt. Tools are what give agents the ability to take action in the world.

## Build on Your Platform

The Design phase produced a platform-agnostic agent blueprint — name, description, instructions, model, and tools. How you build that agent depends on which platform you're using. Each platform has its own agent system with different capabilities and configuration approaches.

| Platform | Agent guide |
|---|---|
| Claude | [Building Agents on Claude](../../platforms/claude/agents/building-agents.md) |
| OpenAI | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents.md) |
| Google Gemini | [Building Agents on Google](../../platforms/google-gemini/agents/building-agents.md) |
| M365 Copilot | [Building Agents on M365 Copilot](../../platforms/m365-copilot/agents/building-agents.md) |

Each guide shows how to translate your Design blueprint into a working agent on that platform — where each component goes, what tools are available, and links to official documentation.

The [Autonomous Agent](autonomous-agent.md) worked example shows a complete multi-agent pipeline with 4 specialized agents, including the full instructions for each one.

## What's Next

If your workflow requires external tool access (databases, APIs, browsers), see [MCP](mcp.md) for connecting AI to your tools. Otherwise, [run your workflow](run.md) on a real scenario and build incrementally.
