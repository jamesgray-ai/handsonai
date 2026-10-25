---
title: Agents
description: "The Agent building block — how AI agents plan, call tools, and loop until a task is done, with the capability and orchestration patterns for building them."
last_reviewed: 2026-10-24
---

Concepts for building AI agents and implementing tool use.

## Agents by Platform

Each platform has its own agent system. These guides show how to build agents on each one — from no-code options for business users to full developer frameworks.

| Platform | Approach | Description | Guide |
|----------|----------|-------------|-------|
| **Claude** | <a href="https://code.claude.com/docs/en/sub-agents" target="_blank">Subagents</a> | Build and activate subagents via natural language | [Building Agents on Claude](../../platforms/claude/agents/building-agents/) |
| **Claude** | <a href="https://code.claude.com/docs/en/agent-teams" target="_blank">Agent Teams</a> | Code-first multi-agent coordination | ↑ |
| **Claude** | <a href="https://claude.com/claude-in-chrome" target="_blank">Claude in Chrome</a> | Chrome browser orchestration (macOS only) | ↑ |
| **Claude** | <a href="https://code.claude.com/docs/en/agent-sdk/overview" target="_blank">Agents SDK</a> | Code-first approach in Python with SDK | ↑ |
| **OpenAI** | <a href="https://chatgpt.com/features/agent/" target="_blank">ChatGPT Agent Mode</a> | Single-agent orchestration in ChatGPT | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents/) |
| **OpenAI** | <a href="https://openai.com/index/introducing-chatgpt-atlas/" target="_blank">Atlas Browser</a> | Browser orchestration (macOS only) | ↑ |
| **OpenAI** | <a href="https://developers.openai.com/api/docs/guides/agents" target="_blank">AgentKit</a> | Visual builder for conversational agents | ↑ |
| **OpenAI** | <a href="https://openai.github.io/openai-agents-python/" target="_blank">Agents SDK</a> | Code-first approach with Python | ↑ |
| **OpenAI** | <a href="https://openai.com/business/frontier/" target="_blank">Frontier</a> | Enterprises orchestrating custom, OpenAI, and third-party agents | ↑ |
| **Google** | <a href="https://workspace.google.com/studio/" target="_blank">Workspace Studio</a> | Simple agent flows for Workspace apps | [Building Agents on Google](../../platforms/google-gemini/agents/building-agents/) |
| **Google** | <a href="https://docs.cloud.google.com/gemini/enterprise/docs/agents-overview" target="_blank">Gemini Enterprise Agent Designer</a> | Build agents and workflows visually — enterprise offering | ↑ |
| **Google** | <a href="https://gemini.google/overview/gemini-in-chrome/" target="_blank">Gemini in Chrome</a> | AI-powered browser workflows | ↑ |
| **Google** | <a href="https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk" target="_blank">Vertex AI & ADK</a> | Code-first approach in Python | ↑ |
| **M365 Copilot** | <a href="https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agents-overview" target="_blank">Copilot & Copilot Studio</a> | Build agents visually and deploy to M365 surfaces | [Building Agents on M365 Copilot](../../platforms/m365-copilot/agents/building-agents/) |

For guidance on deciding *whether* your workflow needs an agent, see [Build Workflows > Agents](../../ai-workflow-framework/build/).

## Topics

- [SDK Building Block](../sdk/) — Frameworks and toolkits for building agents and AI workflows in code (Claude Agent SDK, OpenAI Agents SDK, Google ADK, LangGraph, and more)
- [Agent Capability Patterns](./capability-patterns/) — What one agent can do: Andrew Ng's four agentic design patterns (Reflection, Tool Use, Planning, Multi-Agent Collaboration), plus Memory and two safety patterns, Guardrails and Human Checkpoint
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/) — How the work is structured, for one agent or several: Prompt Chaining, Routing, Parallelization, Evaluator-Optimizer, Orchestrator-Workers, Handoff, Group Chat, Swarm, and more, each mapped to an autonomy level

## Key Concepts

- **Function Calling** - Enabling models to call external functions
- **Tool Use** - Defining and executing tools
- **Agent Loops** - Iterative reasoning and action
- **ReAct Pattern** - Reasoning and acting
- **State Management** - Tracking conversation and tool state
- **Error Handling** - Graceful failure and recovery

## Related

- [Agentic Building Blocks](../)
- [SDK](../sdk/) — frameworks for building agents in code
- [API](../api/) — programmatic interfaces agents call under the hood
- [AI Use Cases](../../use-cases/) — what teams build with agents, organized by six primitives
- [Automation Use Cases](../../use-cases/automation/) — the highest-autonomy use cases powered by agents
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/) — the one catalogue of patterns, from a single augmented LLM call to autonomous agents, each mapped to an autonomy level
- [Patterns](../../patterns/)
