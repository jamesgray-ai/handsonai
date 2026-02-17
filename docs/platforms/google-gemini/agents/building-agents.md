---
title: Building Agents on Google
description: How to build agents on Google's Gemini platform — Workspace Studio for natural-language automation, Agent Designer for no-code workflows, and the Agent Development Kit for custom development.
---

# Building Agents on Google

> **Part of:** [Build Workflows > Agents](../../../business-first-ai-framework/build/agents.md)

Google offers three approaches to building agents on the Gemini platform, ranging from natural-language automation to full programmatic control.

| Approach | Best for | Complexity |
|----------|----------|------------|
| [Workspace Studio](#workspace-studio) | Non-technical users automating everyday work across Workspace apps | Lowest — describe what you want in natural language |
| [Agent Designer](#agent-designer) | Business users who want to build agents without writing code | Low — no-code/low-code visual interface |
| [Agent Development Kit (ADK)](#agent-development-kit-adk) | Developers building custom agents for deployment on Vertex AI | Higher — open-source framework, full programmatic control |

## Workspace Studio

Workspace Studio is Google's natural-language automation platform built into Workspace. It lets anyone create automated workflows across Gmail, Drive, Sheets, and other Workspace apps by describing what they want in plain language — no coding or visual builder required.

**Official docs:** [Workspace Studio](https://workspace.google.com/studio/)

### What you can build

- Automated workflows for everyday tasks — email triage, meeting summaries, cross-app data transfer, report generation
- Multi-step automations that connect Workspace apps with third-party services

### How it works

1. **Describe** — tell Gemini what you want to automate in natural language
2. **Generate** — Gemini creates a workflow from your description
3. **Refine** — adjust the flow using pre-configured steps and connectors
4. **Manage** — run, monitor, and edit workflows directly within Workspace apps

### Key capabilities

- Create automations using natural language — no code, no visual builder
- Pre-configured steps for common Workspace actions (send email, create doc, update sheet)
- Manage workflows in-app from Gmail, Chat, and Drive
- Third-party connectors for tools like Asana, Jira, Salesforce, and Mailchimp
- Included with Google Workspace Business and Enterprise plans

### Mapping your Design blueprint

| Design blueprint | Workspace Studio |
|-----------------|------------------|
| **Name** | Workflow name in Studio |
| **Description** | Natural language description of the automation |
| **Instructions** | The plain-language prompt that generates the workflow |
| **Model** | Gemini (built-in, not configurable) |
| **Tools** | Workspace app actions and third-party connectors |

### Example: Implementing your Design blueprint

Here's how a research analyst agent from the Design phase maps to Workspace Studio:

1. **Name** → Enter the workflow name (e.g., "Company Research Brief") when creating a new automation
2. **Description** → Describe what the automation does: "Researches a company and produces a structured brief in Google Docs"
3. **Instructions** → In the prompt field, describe the full workflow in natural language: "When I provide a company name, search for the company, find recent news and key products, then create a Google Doc with a structured brief containing: company overview, key products/services, recent news, and relevant insights."
4. **Model** → Gemini is built-in and not configurable — Workspace Studio uses the default Gemini model
5. **Tools** → Workspace Studio auto-connects Workspace apps. Add third-party connectors (Jira, Salesforce) from the connectors menu if your workflow needs them

Workspace Studio is best suited for the **Prompt** execution pattern — describe what you want, Gemini generates the automation, and you refine it conversationally.

## Agent Designer

Agent Designer is a no-code, low-code platform within Gemini Enterprise for building AI agents using natural language and a visual workflow editor.

**Official docs:** [Agent Designer](https://docs.cloud.google.com/gemini/enterprise/docs/agent-designer)

### What you can build

- **Single-step agents** — straightforward tasks with one action
- **Multi-step agents** — a primary agent coordinates with subagents on complex workflows

### How it works

The interface has two main sections:

- **Chat pane** — describe what you want the agent to do in natural language, and refine it conversationally
- **Designer pane** — visually edit agent workflows on an interactive canvas, plus schedule and test agents

### Key capabilities

- Create and preview agents using natural language prompts
- Visually edit agent workflows on an interactive canvas
- Connect to Google and third-party tools (Gmail, Drive, Jira)
- Schedule agent executions for recurring tasks
- No programming required for basic agent creation, with low-code options for more control

### Mapping your Design blueprint

| Design blueprint | Agent Designer |
|-----------------|----------------|
| **Name** | Agent name in the Designer interface |
| **Description** | Agent description and purpose |
| **Instructions** | Natural language instructions in the chat pane, refined conversationally |
| **Model** | Gemini model selection (configured in the Designer) |
| **Tools** | Google and third-party tool connections (Gmail, Drive, Jira, etc.) |

### Example: Implementing your Design blueprint

Here's how a research analyst agent from the Design phase maps to Agent Designer:

1. **Name** → Enter `research-analyst` as the agent name when creating a new agent
2. **Description** → Add the agent's purpose in the description field: "Researches companies and produces structured briefs"
3. **Instructions** → In the **Chat pane**, describe your agent: "You are a research analyst who investigates companies. Search for the company, visit key pages, and summarize findings with sections for company overview, key products/services, recent news, and relevant insights." Refine conversationally until the agent behavior matches your blueprint.
4. **Model** → Select the Gemini model version in the **Designer pane** settings (e.g., Gemini 2.0 Flash for speed, Gemini 2.5 Pro for complex reasoning)
5. **Tools** → In the **Designer pane**, connect tools — add Google Search for web research, Gmail for email actions, or Jira for issue tracking

For multi-agent workflows, create a primary agent and add subagents in the Designer pane. Each subagent gets its own name, instructions, and tools. The primary agent coordinates by delegating tasks to subagents based on your orchestration pattern.

## Agent Development Kit (ADK)

The Agent Development Kit is an open-source framework for developing and deploying AI agents. It's designed to make agent development feel like software development — model-agnostic, deployment-agnostic, and compatible with other frameworks.

**Official docs:** [Agent Development Kit overview](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) | [Gemini Enterprise Agents](https://cloud.google.com/gemini-enterprise/agents)

### Key features

- **Open-source** — flexible and extensible framework
- **Model-agnostic** — optimized for Gemini but works with other models
- **Deployment-agnostic** — deploy anywhere, with managed hosting on Vertex AI Agent Engine
- **Framework-compatible** — built for interoperability with other agent frameworks

### What you can build

- Custom agents with programmatic control over behavior and orchestration
- Multi-agent architectures with specialized agents coordinating on complex tasks
- Production agents deployed to Vertex AI Agent Engine (fully managed Google Cloud runtime)

### Tools and integrations

ADK agents can use:

- **Built-in tools** — core capabilities provided by the framework
- **Google Cloud tools** — access to Google Cloud services
- **MCP tools** — connect to external services via the Model Context Protocol
- **Ecosystem tools** — third-party integrations

### Getting started paths

| Path | Description |
|------|-------------|
| **Quickstart with Vertex AI Agent Engine** | Setup, development, deployment, and testing on Google Cloud |
| **Open-source quickstart** | Installation, basic agent setup with tools, local execution |
| **Agent Starter Pack** | Production-ready templates for Vertex AI Agent Engine |

### Mapping your Design blueprint

| Design blueprint | Agent Development Kit |
|-----------------|----------------------|
| **Name** | Agent name in your ADK configuration |
| **Description** | Agent description and metadata |
| **Instructions** | Agent instructions defined programmatically |
| **Model** | Model configuration (Gemini recommended, others supported) |
| **Tools** | Built-in tools, Google Cloud tools, MCP tools, or custom integrations |

### Example: Implementing your Design blueprint

Here's how a research analyst agent from the Design phase looks in the ADK:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

research_agent = Agent(
    name="research_analyst",
    model="gemini-2.0-flash",
    instruction=(  # Note: ADK uses "instruction" (singular), not "instructions"
        "You are a research analyst who investigates companies "
        "and produces structured briefs. Search for the company, "
        "visit key pages, and summarize findings with sections for: "
        "company overview, key products/services, recent news, "
        "and relevant insights."
    ),
    tools=[google_search],
)
```

!!! warning "ADK naming difference"
    ADK uses `instruction` (singular), not `instructions` (plural). This is a common source of errors when translating from other platforms.

For multi-agent workflows, use the `sub_agents` parameter:

```python
from google.adk.agents import Agent

writer_agent = Agent(
    name="brief_writer",
    model="gemini-2.0-flash",
    instruction="You write structured company briefs from research notes...",
)

research_agent = Agent(
    name="research_analyst",
    model="gemini-2.0-flash",
    instruction="You research companies. After gathering findings, delegate to the writer...",
    tools=[google_search],
    sub_agents=[writer_agent],
)
```

**Official reference:** [ADK quickstart](https://docs.cloud.google.com/agent-builder/agent-development-kit/quickstart)

## What's Next

- [Agents overview](../../../business-first-ai-framework/build/agents.md) — the platform-agnostic agent decision framework
- [Design Your AI Workflow](../../../business-first-ai-framework/build/design.md) — produce the agent blueprint that feeds into these implementations
