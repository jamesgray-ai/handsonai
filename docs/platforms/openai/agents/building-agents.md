---
title: Building Agents on OpenAI
description: How to build agents on OpenAI's platform — ChatGPT Agent Mode for simple tasks, AgentKit for visual workflows, Agents SDK for custom development, and Frontier for enterprise orchestration.
---

# Building Agents on OpenAI

> **Part of:** [Build Workflows > Agents](../../../business-first-ai-framework/build/agents.md)

OpenAI offers four approaches to building agents, ranging from no-code chat interactions to full programmatic control.

| Approach | Best for | Complexity |
|----------|----------|------------|
| [ChatGPT Agent Mode](#chatgpt-agent-mode) | Non-technical users running single-agent tasks in ChatGPT | Low — conversational, no setup required |
| [AgentKit](#agentkit) | Business users building agent workflows with a visual canvas | Low to moderate — no-code visual builder |
| [Agents SDK](#agents-sdk) | Developers building custom agents with Python or TypeScript | Higher — full programmatic control |
| [Frontier](#frontier) | Enterprises orchestrating custom, OpenAI, and third-party agents | Enterprise — managed platform (limited availability) |

## ChatGPT Agent Mode

Agent Mode is available directly in ChatGPT. It lets ChatGPT autonomously browse the web, run code, analyze files, and take multi-step actions to complete a task — all from a single conversation.

**Official docs:** [ChatGPT Agent Mode](https://chatgpt.com/features/agent/)

### When to use it

- You want a quick, single-agent approach with no setup
- The task can be completed in one conversation with web browsing, code execution, or file analysis
- You don't need custom tools, integrations, or multi-agent coordination

### Mapping your Design blueprint

| Design blueprint | ChatGPT Agent Mode |
|-----------------|-------------------|
| **Instructions** | Your message describing what you want done |
| **Tools** | Built-in capabilities (web browsing, code interpreter, file analysis) |

Agent Mode is best suited for the **Prompt** execution pattern — paste your instructions, let ChatGPT execute autonomously, review the output.

## AgentKit

AgentKit is OpenAI's modular toolkit for creating, deploying, and refining agent systems using a visual canvas. Agent Builder — the core creation interface — lets you design agent workflows by connecting pre-built components without writing code.

**Official docs:** [AgentKit guide](https://developers.openai.com/api/docs/guides/agents)

### Key capabilities

- **Build** — visual workflow design with integrated models, tools, and logic nodes
- **Deploy** — embed agents into applications using ChatKit
- **Optimize** — evaluation platform for monitoring and improving agent performance

### Who it's for

Business-oriented users who want to create agent workflows visually. AgentKit bridges the gap between no-code simplicity and the flexibility needed for production agent systems.

### Mapping your Design blueprint

| Design blueprint | AgentKit |
|-----------------|----------|
| **Name** | Agent name in the Builder interface |
| **Description** | Agent purpose and activation context |
| **Instructions** | Agent instructions configured in the visual canvas |
| **Model** | Model selection in the Builder |
| **Tools** | Tool nodes connected in the visual workflow |

## Agents SDK

The Agents SDK is a developer library for building agentic applications with full programmatic control. Agents can use tools, hand off to other specialized agents, stream partial results, and maintain execution traces.

**Official docs:** [Agents SDK guide](https://developers.openai.com/api/docs/guides/agents-sdk)

### Language support

| Language | Repository |
|----------|-----------|
| Python | [openai-agents-python](https://github.com/openai/openai-agents-python) |
| TypeScript/JavaScript | [openai-agents-js](https://openai.github.io/openai-agents-js) |

### Key features

- **Tool integration** — connect agents to external services and data sources
- **Agent-to-agent handoffs** — specialized agents delegate to each other
- **Streaming** — stream intermediate results as the agent works
- **Execution tracing** — full trace of what happened for debugging and monitoring
- **Safety guardrails** — built-in patterns for safe agent behavior

### Mapping your Design blueprint

| Design blueprint | Agents SDK |
|-----------------|-----------|
| **Name** | Agent name in your code |
| **Description** | Agent description and metadata |
| **Instructions** | System prompt and instructions defined programmatically |
| **Model** | Model parameter in agent configuration |
| **Tools** | Tool definitions and integrations |

For multi-agent workflows, the SDK's handoff mechanism maps directly to the agent handoffs defined in your Design blueprint.

## Frontier

OpenAI Frontier is an enterprise platform for orchestrating AI agents at scale. It brings together custom agents, OpenAI-built agents, and third-party agents into a unified management layer.

**Official docs:** [OpenAI Frontier](https://openai.com/business/frontier/)

!!! note "Limited availability"
    Frontier is currently available to select enterprise customers. Broader availability is expected in the coming months.

### What it includes

- **Custom agents** — agents you build using the Agents SDK or AgentKit
- **OpenAI agents** — pre-built agents from OpenAI for common enterprise tasks
- **Third-party agents** — agents from partner ecosystems integrated into the platform

### When to use it

- You need enterprise-grade agent orchestration with governance and compliance
- Your organization runs multiple agent types (custom, OpenAI, third-party) that need unified management
- You want a managed platform for deploying and monitoring agents at scale

### Mapping your Design blueprint

For multi-agent workflows, Frontier provides the orchestration layer:

| Design blueprint | Frontier |
|-----------------|----------|
| **Specialist agents** | Custom, OpenAI, or third-party agents configured on the platform |
| **Orchestrator** | Frontier's agent orchestration and management layer |
| **Human review gates** | Enterprise governance and approval workflows |

## What's Next

- [Agents overview](../../../business-first-ai-framework/build/agents.md) — the platform-agnostic agent decision framework
- [Design Your AI Workflow](../../../business-first-ai-framework/build/design.md) — produce the agent blueprint that feeds into these implementations
