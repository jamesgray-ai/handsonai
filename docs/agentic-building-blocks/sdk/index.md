---
title: SDK
description: The SDK building block — frameworks and toolkits for building AI workflows in code, from agent orchestration to multi-agent pipelines
---

# SDK

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What an SDK Is

An **SDK** (Software Development Kit) is a framework or toolkit that provides abstractions for building AI workflows in code. Where [APIs](../api/index.md) give you raw access to models and services, SDKs give you patterns and structure — handling orchestration logic, tool use, memory management, and multi-agent coordination so you don't wire everything from scratch.

Think of it this way: an API lets you call a model. An SDK lets you build an agent that calls models, uses tools, manages state, and coordinates with other agents — with the plumbing handled for you.

## Key Characteristics

- **Higher-level abstractions** — wrap raw API calls with patterns for tool use, memory, multi-turn conversations, and agent loops
- **Handle orchestration logic** — manage the planning, routing, and error recovery that make agents work reliably
- **Opinionated about patterns** — provide built-in support for agent loops, handoffs between agents, guardrails, and structured outputs
- **Multi-language support** — most SDKs offer Python as a primary language, with TypeScript/JavaScript as a secondary option

## When to Use It

Use SDKs when:

- You're building agents or multi-step workflows in code and want established patterns rather than building from scratch
- You need tool use orchestration — the SDK handles the loop of "model decides to call a tool → tool executes → result goes back to model"
- You're coordinating multiple agents that need to hand off work to each other
- You want guardrails, memory management, or structured output validation built into the framework
- You're moving beyond a single API call into workflows that require state, iteration, and decision-making

## Example

Using the Claude Agent SDK to build a research agent that takes a topic, searches the web, reads relevant pages, evaluates source quality, and produces a structured report — the SDK handles the agent loop (plan → act → observe → repeat), tool execution, and conversation state, while you define the tools and instructions.

Or using LangGraph to orchestrate a content pipeline where a research agent hands off findings to a writing agent, which hands off a draft to an editing agent — each with different tools and instructions, coordinated through a graph-based workflow.

## Frameworks

| Framework | Provider | Languages | Links |
|-----------|----------|-----------|-------|
| **Claude Agent SDK** | Anthropic | Python, TypeScript | [Cookbook guide](../../platforms/claude/agents/building-agents.md) · <a href="https://platform.claude.com/docs/en/agent-sdk/overview" target="_blank">Docs</a> |
| **OpenAI Agents SDK** | OpenAI | Python, TypeScript | [Cookbook guide](../../platforms/openai/agents/building-agents.md) · <a href="https://developers.openai.com/api/docs/guides/agents-sdk" target="_blank">Docs</a> |
| **Google Agent Development Kit (ADK)** | Google | Python | [Cookbook guide](../../platforms/google-gemini/agents/building-agents.md) · <a href="https://docs.cloud.google.com/agent-builder/agent-development-kit/overview" target="_blank">Docs</a> |
| **LangGraph** | LangChain | Python, JavaScript | <a href="https://www.langchain.com/langgraph" target="_blank">langchain.com/langgraph</a> |
| **Microsoft Agent Framework** | Microsoft | Python, .NET (C#) | <a href="https://github.com/microsoft/agent-framework" target="_blank">GitHub</a> |
| **Microsoft 365 Agents SDK** | Microsoft | .NET, Python, TypeScript | [Cookbook guide](../../platforms/m365-copilot/agents/building-agents.md) · <a href="https://github.com/microsoft/Agents" target="_blank">GitHub</a> · <a href="https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/m365-agents-sdk" target="_blank">Docs</a> |
| **CrewAI** | CrewAI | Python | <a href="https://www.crewai.com/" target="_blank">crewai.com</a> |

## Agent-to-Agent (A2A) Protocol

The <a href="https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/" target="_blank">Agent-to-Agent (A2A) protocol</a> is an open standard for agent interoperability. It defines how agents built with different frameworks can discover each other, negotiate capabilities, and collaborate on tasks — regardless of which SDK or platform they were built on.

A2A complements MCP: where [MCP](../mcp/index.md) connects agents to **tools and data**, A2A connects **agents to other agents**.

<a href="https://google.github.io/A2A/" target="_blank">A2A specification and documentation</a>

## Key Concepts

**Agent loop** — The core pattern in most SDKs: the model receives a goal, decides what to do, calls tools, observes results, and repeats until the goal is met or a stop condition is reached.

**Tool definition** — SDKs provide structured ways to define tools the agent can call — functions, APIs, file operations, web search — with schemas that tell the model what each tool does and what parameters it accepts.

**Handoffs** — In multi-agent workflows, one agent passes control (and context) to another. SDKs formalize this with handoff protocols that manage what information transfers between agents.

**Guardrails** — Built-in safety checks that validate inputs and outputs at each step. SDKs let you define rules (content filters, output validators, scope limiters) that run automatically during agent execution.

**Memory and state** — SDKs manage conversation history, tool call results, and workflow state so the agent can reference prior steps. Some support persistent memory across sessions.

**Structured outputs** — Many SDKs integrate schema validation so agent responses conform to expected formats — critical for pipelines where one agent's output feeds into the next.

## Platform Implementations

| Platform | How It Works | SDK Reference |
|----------|-------------|---------------|
| **Claude (Agent SDK)** | Python and TypeScript SDK for building agents with tool use, handoffs, and guardrails; integrates with MCP servers | <a href="https://platform.claude.com/docs/en/agent-sdk/overview" target="_blank">Docs</a> · <a href="https://github.com/anthropics/anthropic-sdk-python" target="_blank">Python SDK</a> · <a href="https://github.com/anthropics/anthropic-sdk-typescript" target="_blank">TypeScript SDK</a> |
| **OpenAI (Agents SDK)** | Python and TypeScript SDK for building agents with function calling, handoffs, and tracing; includes built-in guardrails | <a href="https://developers.openai.com/api/docs/guides/agents-sdk" target="_blank">Docs</a> · <a href="https://github.com/openai/openai-agents-python" target="_blank">Python SDK</a> · <a href="https://github.com/openai/openai-agents-js" target="_blank">TypeScript SDK</a> |
| **Google (ADK)** | Python SDK for building agents on Vertex AI; supports tool use, multi-agent orchestration, and Google Cloud integrations | <a href="https://docs.cloud.google.com/agent-builder/agent-development-kit/overview" target="_blank">Docs</a> · <a href="https://github.com/google/adk-python" target="_blank">Python SDK</a> |
| **Microsoft (M365 Agents SDK)** | .NET, Python, and TypeScript SDK for building agents that deploy to Microsoft 365 surfaces; integrates with Copilot | <a href="https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/m365-agents-sdk" target="_blank">Docs</a> · <a href="https://github.com/microsoft/Agents" target="_blank">GitHub</a> |

## Relationship to Other Blocks

SDK is the code-first orchestration layer:

- **Model** is what SDKs orchestrate — they manage the model's decision-making loop
- **API** is what SDKs call under the hood — they abstract raw API calls into higher-level patterns
- **Prompts** are embedded in SDK agent definitions as system instructions and tool descriptions
- **Context** is managed by the SDK through memory, conversation history, and tool results
- **Skills** are conceptually similar to SDK tool definitions — both package capabilities for the agent to invoke
- **Agents** are what SDKs build — the agent concept comes to life through SDK code
- **MCP** servers are a common tool type in SDKs — agents use MCP to connect to external systems

## Related

- [Agentic Building Blocks](../index.md) — SDK in the context of all ten building blocks
- [API](../api/index.md) — the raw programmatic interfaces that SDKs abstract over
- [Agents](../agents/index.md) — the building block that SDKs implement in code
- [Agent Capability Patterns](../agents/capability-patterns/index.md) — architectural patterns that SDKs help implement
- [Multi-Agent Collaboration](../agents/capability-patterns/multi-agent-collaboration.md) — patterns for coordinating multiple agents
- [MCP](../mcp/index.md) — the protocol that connects SDK-built agents to tools and data
- [AI Use Cases](../../use-cases/index.md) — what teams build with these blocks
- [Coding Use Cases](../../use-cases/coding/index.md) — code-first AI workflows
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/index.md) — architectural patterns from augmented LLMs to autonomous agents
- [Platforms](../../platforms/index.md) — platform-specific SDK guides
