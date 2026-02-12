---
title: Building Agents on M365 Copilot
description: How to build agents on Microsoft 365 Copilot — declarative agents for business users and custom engine agents for developers.
---

# Building Agents on M365 Copilot

> **Part of:** [Build Workflows > Agents](../../../business-first-ai-framework/build/agents.md)

Microsoft 365 Copilot extends its built-in capabilities through agents — specialized AI assistants tailored to specific domains. Agents can retrieve information, summarize data, and take actions like sending emails or updating records, all within the Microsoft 365 apps where you already work.

**Official docs:** [Agents for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview)

There are two approaches to building agents, depending on how much control you need.

| Approach | Best for | Complexity |
|----------|----------|------------|
| [Declarative agents](#declarative-agents) | Business users and developers who want agents within Copilot's orchestration | Low to moderate — no-code (Copilot Studio) or pro-code (Agents Toolkit) |
| [Custom engine agents](#custom-engine-agents) | Developers who need custom orchestration, models, or external integrations | Higher — bring your own orchestrator and models |

## Agent Core Components

All M365 Copilot agents share these building blocks:

- **Knowledge** — specialized instructions and data sources that shape the agent's responses
- **Actions** — triggers and workflows that automate business processes
- **Orchestrator** — the engine that manages how the agent interacts with knowledge and actions
- **Foundation models** — the AI models powering reasoning and language understanding
- **User experience layer** — how users interact with the agent across Microsoft 365 apps

## Declarative Agents

Declarative agents use Copilot's built-in AI infrastructure, model, and orchestrator. You configure them by adding custom instructions, knowledge, and actions — no hosting required. Because they run on Copilot's infrastructure, they inherit Microsoft 365 security, compliance, and Responsible AI standards.

### What you configure

- **Custom instructions** — shape Copilot's responses for your organization's workflows
- **Custom knowledge** — connect Microsoft 365 data sources (Teams, SharePoint, OneDrive) or external data via Copilot connectors
- **Custom actions** — integrate with APIs to interact with external systems in real-time

### How to build them

| Tool | Audience |
|------|----------|
| **Copilot Studio** | Low-code — business users and citizen developers |
| **Microsoft 365 Agents Toolkit** (Visual Studio / VS Code) | Pro-code — developers who want more control |

### Where they run

Declarative agents run within Microsoft 365 Copilot and Microsoft 365 apps — Teams, Word, Excel, Outlook, and SharePoint. Users invoke them via @mentions or in business chats.

### When to use declarative agents

- You want agents within Copilot's orchestration with built-in security and compliance
- Your users work within Microsoft 365 apps and want agents in that context
- You want faster implementation with no-code or low-code tools
- You don't need custom AI models or external hosting

### Mapping your Design blueprint

| Design blueprint | Declarative agent |
|-----------------|-------------------|
| **Name** | Agent name in Copilot Studio or Agents Toolkit |
| **Description** | Agent purpose and scenario description |
| **Instructions** | Custom instructions that shape Copilot's responses |
| **Model** | Copilot's built-in foundation models (not configurable) |
| **Tools** | Custom actions (API integrations) + custom knowledge (Microsoft 365 data sources, connectors) |

## Custom Engine Agents

Custom engine agents are fully customized AI assistants. You bring your own orchestrator, choose your own models, and host the agent outside of Microsoft 365. This gives you full control over workflows, business logic, and integrations — but you're responsible for compliance, security, and hosting.

### What you configure

- **Custom orchestration** — full control over workflows, with one or more language models
- **Custom models** — choose any model (foundation, fine-tuned, or industry-specific)
- **Autonomy** — agents can initiate workflows proactively, make decisions, and escalate tasks

### How to build them

| Tool | Audience |
|------|----------|
| **Copilot Studio** | Low-code — simpler custom engine setups |
| **Microsoft 365 Agents Toolkit** (Visual Studio / VS Code) | Pro-code — .NET, Python, JavaScript |
| **Frameworks** | Semantic Kernel, LangChain, or other orchestration frameworks |

### Where they run

Custom engine agents run in Microsoft 365 apps (Teams, Word, Outlook) **and** external apps and websites — customer service portals, internal dashboards, or any web application.

### When to use custom engine agents

- You need custom orchestration for complex workflows or specific business logic
- You want to use your own AI models (domain-specific, fine-tuned, or multimodal)
- You need group collaboration where multiple users interact with the same agent
- You want agents available outside Microsoft 365
- You need proactive messaging — agents that trigger actions without user input
- You're integrating an existing conversational assistant with Microsoft 365

### Mapping your Design blueprint

| Design blueprint | Custom engine agent |
|-----------------|---------------------|
| **Name** | Agent name in your code or Copilot Studio |
| **Description** | Agent purpose and scenario description |
| **Instructions** | Custom orchestration logic and agent behavior |
| **Model** | Your chosen model (Azure OpenAI, open-source, fine-tuned, etc.) |
| **Tools** | API integrations, Microsoft Graph, external system connections |

For multi-agent workflows, custom engine agents support agent-to-agent communication — agents can delegate tasks and coordinate workflows across your organization.

## Choosing Between Approaches

| Feature | Declarative agents | Custom engine agents |
|---------|-------------------|---------------------|
| **Hosting** | Hosted in Microsoft 365 — no additional infrastructure | Requires external hosting (Azure or other cloud) |
| **Models** | Copilot's built-in models | Any model you choose |
| **Customization** | Instructions, knowledge, and actions within Copilot's framework | Fully customizable orchestration, models, and logic |
| **Proactive actions** | User-initiated only | Can trigger actions automatically |
| **Where it runs** | Microsoft 365 apps only | Microsoft 365 apps + external apps and websites |
| **Compliance** | Inherits Microsoft 365 standards | You manage compliance and security |

**Start with declarative agents** if your workflow fits within Microsoft 365 and you want built-in security and faster setup. **Move to custom engine agents** when you need custom models, external integrations, or proactive behavior.

## What's Next

- [Agents overview](../../../business-first-ai-framework/build/agents.md) — the platform-agnostic agent decision framework
- [Design Your AI Workflow](../../../business-first-ai-framework/build/design.md) — produce the agent blueprint that feeds into these implementations
