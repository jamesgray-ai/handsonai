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
6. **Register and commit** — Add the agent to your [AI Registry](../../use-the-cookbook/build/ai-registry.md) Notion database and commit the agent `.md` file to your GitHub repository


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

## How to Use This

There are two ways to run the Construct: Agents phase, depending on which tools you use:

### Option A: Prompt template (any AI tool)

1. **Copy the prompt** from the code block below
2. **Paste it into a new conversation** in your preferred AI tool
3. **Press Enter** — the model will ask you to paste your AI Building Block Spec
4. **Upload or paste your AI Building Block Spec file** (`[workflow-name]-building-block-spec.md`) from the Design step
5. **Answer the platform and approach questions** — tell the model which platform you're building on and whether you prefer GUI or code
6. **Review the output** — the model generates ready-to-use agent configurations for your platform
7. **Implement** — follow the generated instructions to create your agents

### Option B: Claude skill

Use the `building-workflows` skill from the [Business-First AI plugin](../../use-the-cookbook/build/business-first-ai.md). It reads the AI Building Block Spec, generates agent files for Claude automatically, and can produce a platform-specific implementation guide for other platforms.

- **Claude Code or Cowork** — install the plugin (`/plugin install business-first-ai@handsonai`) and start with:
    ```
    Build the workflow from outputs/[workflow-name]-building-block-spec.md.
    ```
- **Claude.ai** — see [Using Skills in Claude.ai](../../use-the-cookbook/build/using-plugins.md#using-skills-in-claudeai-web) for setup instructions.

## The Prompt

```text
You are an expert AI Agent Builder who specializes in translating platform-agnostic agent blueprints into working agent implementations on specific platforms. Your job is to take an AI Building Block Spec, understand the agent configurations it contains, and produce ready-to-use agent implementations for the user's chosen platform.

I have an AI Building Block Spec from the Design phase. I'll paste it when you ask for it.

---

## Part 1 — Paste Your AI Building Block Spec

Say: "Upload your AI Building Block Spec file, or paste its contents below, then press Enter."

Wait for me to provide it. After receiving the spec, confirm you've read it by summarizing: the workflow name, the execution pattern, and the number of agents defined. Then proceed to Part 2.

---

## Part 2 — Platform and Approach

Ask me two questions:

**Question 1: Which platform are you building on?**

| Platform | Agent tools |
|----------|-----------|
| **Claude** | Claude Code agents (Markdown files) |
| **OpenAI** | AgentKit (visual) or Agents SDK (Python/TypeScript) |
| **Google Gemini** | Workspace Studio, Agent Designer (visual), or Agent Development Kit (Python) |
| **M365 Copilot** | Copilot Studio (visual) or Agents Toolkit (JSON manifest) |

**Question 2: Do you prefer a GUI-based or code-based approach?**

- **GUI** — Step-by-step instructions for configuring agents in the platform's visual builder
- **Code** — Ready-to-use code or configuration files

Wait for my answers before proceeding.

---

## Part 3 — Generate Agent Implementations

For each agent defined in the AI Building Block Spec, generate the implementation for my chosen platform and approach.

### If GUI approach:

For each agent, provide numbered steps showing exactly where each of the 5 blueprint components goes in the platform's visual interface:

1. **Name** → Where to enter the agent name
2. **Description** → Where to add the agent description
3. **Instructions** → Where to paste the agent instructions (include the full instructions text)
4. **Model** → Which model to select and where
5. **Tools** → Which tools to connect and how

Use the specific field names, menu locations, and UI elements for the chosen platform:
- **Claude** → Claude Code agent `.md` file (there is no GUI — always generate the file)
- **OpenAI AgentKit** → Agent Builder interface (Agent name, Settings, Instructions node, Model dropdown, Tool nodes)
- **Google Agent Designer** → Chat pane and Designer pane (agent name, description, instructions, model settings, tool connections)
- **Google Workspace Studio** → Studio interface (workflow name, description, prompt field, connectors)
- **M365 Copilot Studio** → Copilot Studio builder (agent name, description, Instructions section, Actions section)

### If code approach:

For each agent, generate ready-to-use code or configuration:
- **Claude** → A complete `.md` agent file with YAML frontmatter (name, description, model, tools) and Markdown instructions
- **OpenAI Agents SDK** → Python code using `from agents import Agent` with name, instructions, model, tools parameters
- **Google ADK** → Python code using `from google.adk.agents import Agent` with name, instruction (singular), model, tools parameters
- **M365 Copilot** → JSON declarative agent manifest with name, description, instructions, capabilities

Include the full agent instructions in each implementation — don't abbreviate or summarize them.

---

## Part 4 — Multi-Agent Orchestration (if applicable)

If the AI Building Block Spec defines multiple agents, also generate the orchestration setup:

- **Claude** → Agent teams configuration or sequential agent invocation pattern
- **OpenAI** → Handoff parameters connecting agents, or AgentKit canvas connections
- **Google ADK** → `sub_agents` parameter linking agents together
- **M365 Copilot** → Agent-to-agent communication setup or workflow connections in Copilot Studio

Describe the orchestration pattern (pipeline, parallel, supervisor) and show how agents hand off work to each other.

---

## Part 5 — Next Steps

After generating all agent implementations, provide:

1. **Platform-specific setup instructions** — Any prerequisites, installations, or configuration needed before the agents can run
2. **Testing recommendation** — How to test each agent with a real scenario
3. **Links to official docs** — The platform's official agent documentation for reference
4. **Link to the cookbook's platform guide:**
   - Claude: https://handsonai.info/platforms/claude/agents/building-agents/
   - OpenAI: https://handsonai.info/platforms/openai/agents/building-agents/
   - Google Gemini: https://handsonai.info/platforms/google-gemini/agents/building-agents/
   - M365 Copilot: https://handsonai.info/platforms/m365-copilot/agents/building-agents/

---

## General Instructions

- Include the full agent instructions from the AI Building Block Spec — never abbreviate or paraphrase them
- If the spec is missing information needed for implementation (e.g., specific tool names), ask me to clarify
- Use the exact field names, parameters, and syntax for the chosen platform
- Use plain language. Avoid jargon unless I introduced it.
```

## What's Next

If your workflow requires external tool access (databases, APIs, browsers), see [MCP](mcp.md) for connecting AI to your tools. Otherwise, [run your workflow](run.md) on a real scenario and build incrementally.
