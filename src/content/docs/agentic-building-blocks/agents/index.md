---
title: Agents
description: Concepts for building AI agents including function calling, tool use, and agent loops
---Concepts for building AI agents and implementing tool use.

## Agents by Platform

Each platform has its own agent system. These guides show how to build agents on each one — from no-code options for business users to full developer frameworks.

| Platform | Approach | Description | Guide |
|----------|----------|-------------|-------|
| **Claude** | <a href="https://code.claude.com/docs/en/sub-agents" target="_blank">Subagents</a> | Build and activate subagents via natural language | [Building Agents on Claude](../../platforms/claude/agents/building-agents.mdx) |
| **Claude** | <a href="https://code.claude.com/docs/en/agent-teams" target="_blank">Agent Teams</a> | Code-first multi-agent coordination | ↑ |
| **Claude** | <a href="https://claude.com/chrome" target="_blank">Claude in Chrome</a> | Chrome browser orchestration (macOS only) | ↑ |
| **Claude** | <a href="https://platform.claude.com/docs/en/agent-sdk/overview" target="_blank">Agents SDK</a> | Code-first approach in Python with SDK | ↑ |
| **OpenAI** | <a href="https://chatgpt.com/features/agent/" target="_blank">ChatGPT Agent Mode</a> | Single-agent orchestration in ChatGPT | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents.md) |
| **OpenAI** | <a href="https://openai.com/index/introducing-chatgpt-atlas/" target="_blank">Atlas Browser</a> | Browser orchestration (macOS only) | ↑ |
| **OpenAI** | <a href="https://developers.openai.com/api/docs/guides/agents" target="_blank">AgentKit</a> | Visual builder for conversational agents | ↑ |
| **OpenAI** | <a href="https://developers.openai.com/api/docs/guides/agents-sdk" target="_blank">Agents SDK</a> | Code-first approach with Python | ↑ |
| **OpenAI** | <a href="https://openai.com/business/frontier/" target="_blank">Frontier</a> | Enterprises orchestrating custom, OpenAI, and third-party agents | ↑ |
| **Google** | <a href="https://workspace.google.com/studio/" target="_blank">Workspace Studio</a> | Simple agent flows for Workspace apps | [Building Agents on Google](../../platforms/google-gemini/agents/building-agents.md) |
| **Google** | <a href="https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview" target="_blank">Gemini Enterprise Agent Designer</a> | Build agents and workflows visually — enterprise offering | ↑ |
| **Google** | <a href="https://gemini.google/overview/gemini-in-chrome/" target="_blank">Gemini in Chrome</a> | AI-powered browser workflows | ↑ |
| **Google** | <a href="https://docs.cloud.google.com/agent-builder/agent-development-kit/overview" target="_blank">Vertex AI & ADK</a> | Code-first approach in Python | ↑ |
| **M365 Copilot** | <a href="https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview" target="_blank">Copilot & Copilot Studio</a> | Build agents visually and deploy to M365 surfaces | [Building Agents on M365 Copilot](../../platforms/m365-copilot/agents/building-agents.md) |

For guidance on deciding *whether* your workflow needs an agent, see [Build Workflows > Agents](../../business-first-ai-framework/build/index.mdx).

## Topics

- [SDK Building Block](../sdk/index.md) — Frameworks and toolkits for building agents and AI workflows in code (Claude Agent SDK, OpenAI Agents SDK, Google ADK, LangGraph, and more)
- [Agent Capability Patterns](./capability-patterns/index.md) — Seven architectural patterns that make agents effective: Reflection, Tool Use, Planning, Multi-Agent Collaboration, Memory, Guardrails, and Human-in-the-Loop
- [Agent Orchestration Patterns](./orchestration-patterns/index.md) — Eight coordination topologies for multi-agent systems: Sequential, Parallel, Router, Hierarchical, Handoff, Evaluator-Optimizer, Group Chat, and Decentralized

## Key Concepts

- **Function Calling** - Enabling models to call external functions
- **Tool Use** - Defining and executing tools
- **Agent Loops** - Iterative reasoning and action
- **ReAct Pattern** - Reasoning and acting
- **State Management** - Tracking conversation and tool state
- **Error Handling** - Graceful failure and recovery

## Related

- [Agentic Building Blocks](../index.md)
- [SDK](../sdk/index.md) — frameworks for building agents in code
- [API](../api/index.md) — programmatic interfaces agents call under the hood
- [AI Use Cases](../../use-cases/index.md) — what teams build with agents, organized by six primitives
- [Automation Use Cases](../../use-cases/automation/index.md) — the highest-autonomy use cases powered by agents
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/index.md) — seven patterns from augmented LLMs to autonomous agents
- [Patterns](../../patterns/index.md)
