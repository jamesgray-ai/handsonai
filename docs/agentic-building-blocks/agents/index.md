---
title: Agents
description: Concepts for building AI agents including function calling, tool use, and agent loops
---

# Agents

Concepts for building AI agents and implementing tool use.

## Topics

- [Agent Capability Patterns](./capability-patterns/index.md) — Seven architectural patterns that make agents effective: Reflection, Tool Use, Planning, Multi-Agent Collaboration, Memory, Guardrails, and Human-in-the-Loop

## Key Concepts

- **Function Calling** - Enabling models to call external functions
- **Tool Use** - Defining and executing tools
- **Agent Loops** - Iterative reasoning and action
- **ReAct Pattern** - Reasoning and acting
- **State Management** - Tracking conversation and tool state
- **Error Handling** - Graceful failure and recovery

## Agents by Platform

Each platform has its own agent system. These guides show how to build agents on each one — from no-code options for business users to full developer frameworks.

| Platform | Approaches | Guide |
|----------|-----------|-------|
| **Claude** | Custom subagents (Markdown agent files), Agent teams (multi-agent coordination) | [Building Agents on Claude](../../platforms/claude/agents/building-agents.md) |
| **OpenAI** | ChatGPT Agent Mode, AgentKit (visual canvas), Agents SDK (Python/TypeScript), Frontier (enterprise) | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents.md) |
| **Google Gemini** | Agent Designer (no-code), Agent Development Kit (open-source framework) | [Building Agents on Google](../../platforms/google-gemini/agents/building-agents.md) |
| **M365 Copilot** | Declarative agents (no-code/low-code), Custom engine agents (bring your own models) | [Building Agents on M365 Copilot](../../platforms/m365-copilot/agents/building-agents.md) |

For guidance on deciding *whether* your workflow needs an agent, see [Build Workflows > Agents](../../business-first-ai-framework/build/agents.md).

## Related

- [Agentic Building Blocks](../index.md)
- [AI Use Cases](../../use-cases/index.md) — what teams build with agents, organized by six primitives
- [Automation Use Cases](../../use-cases/automation.md) — the highest-autonomy use cases powered by agents
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/index.md) — seven patterns from augmented LLMs to autonomous agents
- [Patterns](../../patterns/index.md)
