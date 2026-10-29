---
title: Building Agents on M365 Copilot
description: How to build agents on Microsoft 365 Copilot — Agent Builder from Copilot Chat, declarative agents in Copilot Studio, and custom engine agents for developers.
---

> **Part of:** [Microsoft 365 Copilot](../../)

Microsoft 365 Copilot extends its built-in capabilities through agents — specialized AI assistants tailored to specific domains. Agents can retrieve information, summarize data, and take actions like sending emails or updating records, all within the Microsoft 365 apps where you already work.

**Official docs:** [Agents for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview)

There are two approaches to building agents, depending on how much control you need.

| Approach | Best for | Complexity |
|----------|----------|------------|
| [Declarative agents](#declarative-agents) | Business users and developers who want agents within Copilot's orchestration | Low to moderate — no-code (Agent Builder, the quickest way and the one the framework uses, or Copilot Studio) or pro-code (Agents Toolkit) |
| [Custom engine agents](#custom-engine-agents) | Developers who need custom orchestration, models, or external integrations | Higher — bring your own orchestrator and models |

## Build an agent with Agent Builder

When the [AI Workflow Framework](/ai-workflow-framework/) builds an agent on Microsoft 365 Copilot, it uses Agent Builder (verified 2026-10-24). Skills are made in [Copilot Cowork](/platforms/m365-copilot/skills/); agents are made here.

1. Open **Copilot › Chat › Agents › New agent**. Use the **Message Agent Builder** box. If Agent Builder asks you anything, paste its question into Build's chat. The ordinary Copilot Chat can read your plan and describe an agent, but it can't create one.
2. Paste the build prompt the [Build](/ai-workflow-framework/build/) step wrote for you. It names your plan, your requirements and their OneDrive folder, so Agent Builder fills in the name, description and instructions itself. You don't copy anything into the form.
3. Add each context file the agent reads under **Knowledge**, from the copy Build saved in the workflow's own folder, and check that Knowledge lists only the files Build named, removing anything else. Don't use Agent Builder's offer to attach a file: it may pick the copy in your working folder instead.
4. Check **Work content**. Each agent has its own switches (Cloud files, Outlook, Teams, Copilot connectors, web search), and Microsoft's default lets an agent reach everything Copilot can. Leave on only what the workflow uses, and switch the rest off.
5. Choose **Create**.
6. Paste the agent's instructions back into Build's chat, so Build can check them.

Build can't open the agent itself on Microsoft 365, so the framework's [Test](/ai-workflow-framework/test/) step proves the agent with practice runs. A fix goes back the same way: Build writes a fix prompt. For now, Agent Builder can't change an agent in place, so you make a new agent from the fix prompt in Agent Builder and delete the old one, then paste the new agent's instructions back for Build to check.

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
| **Agent Builder** (in Copilot Chat) | Everyone — the quickest way to make a declarative agent, and the one the AI Workflow Framework uses |
| **Copilot Studio** | Low-code — business users and citizen developers |
| **Microsoft 365 Agents Toolkit** (Visual Studio / VS Code) | Pro-code — developers who want more control |

### Where they run

Declarative agents run within Microsoft 365 Copilot and Microsoft 365 apps — Teams, Word, Excel, Outlook, and SharePoint. Users invoke them via @mentions or in business chats.

### When to use declarative agents

- You want agents within Copilot's orchestration with built-in security and compliance
- Your users work within Microsoft 365 apps and want agents in that context
- You want faster implementation with no-code or low-code tools
- You don't need custom AI models or external hosting

### Mapping an agent you design yourself

The AI Workflow Framework builds agents in Agent Builder only ([above](#build-an-agent-with-agent-builder)). Use this mapping for agents you build by hand in Copilot Studio or the Agents Toolkit.

| Your agent design | Declarative agent |
|-----------------|-------------------|
| **Name** | Agent name in Copilot Studio or Agents Toolkit |
| **Description** | Agent purpose and scenario description |
| **Instructions** | Custom instructions that shape Copilot's responses |
| **Model** | Copilot's built-in foundation models (not configurable) |
| **Tools** | Custom actions (API integrations) + custom knowledge (Microsoft 365 data sources, connectors) |

### Example: Building it by hand (Copilot Studio)

Here's how a research analyst agent you designed yourself maps to Copilot Studio's visual builder:

1. **Name** → Enter `Research Analyst` as the agent name when creating a new declarative agent
2. **Description** → Add the agent's scenario description: "Researches companies and produces structured briefs for the team"
3. **Instructions** → In the **Instructions** section, paste your agent instructions: "You are a research analyst who investigates companies and produces structured briefs. When asked about a company, search for information and summarize findings with sections for: company overview, key products/services, recent news, and relevant insights."
4. **Model** → Copilot's built-in foundation models are used automatically — no model selection needed
5. **Tools** → In the **Actions** section, add connectors: enable **Web Search** for research, add **SharePoint** knowledge sources for internal data, or configure **API plugins** for external system access

### Example: Building it by hand (JSON manifest)

For developers using the Microsoft 365 Agents Toolkit, the same agent is defined as a declarative JSON manifest:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json",
  "name": "Research Analyst",
  "description": "Researches companies and produces structured briefs",
  "instructions": "You are a research analyst who investigates companies and produces structured briefs. When asked about a company, search for information and summarize findings with sections for: company overview, key products/services, recent news, and relevant insights.",
  "capabilities": [
    { "name": "WebSearch" }
  ],
  "conversation_starters": [
    { "text": "Research Acme Corp and write a brief" },
    { "text": "What can you tell me about Contoso Ltd?" }
  ]
}
```

To add knowledge sources (SharePoint, OneDrive) or API actions, add them to the manifest's `capabilities` and `actions` arrays. See the [Agents Toolkit documentation](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-toolkit-overview) for the full schema.

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

### Mapping an agent you design yourself

The AI Workflow Framework builds agents in Agent Builder only ([above](#build-an-agent-with-agent-builder)). Use this mapping for custom engine agents you build by hand.

| Your agent design | Custom engine agent |
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

- [Build Your AI Workflow](../../../../ai-workflow-framework/build/) — how the framework builds and installs a workflow
- [Design Your AI Workflow](../../../../ai-workflow-framework/design/) — decides whether a workflow needs an agent at all
