---
title: Context Engineering
description: The practice of designing and optimizing the entire context window — system prompts, instructions, tools, memory, and state — for AI systems
---

# Context Engineering

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What Context Engineering Is

**Context engineering** is the practice of designing and optimizing everything an AI model sees when it generates a response. This goes well beyond writing a good prompt — it includes system prompts, instructions, user input handling, tool integrations, retrieved knowledge, memory, and state management.

The term emerged as the industry recognized that a well-structured context makes even a simple prompt produce excellent results, while a perfectly crafted prompt with poor context still produces poor results. The focus shifted from *how you ask* to *what information the model sees*.

## How It Extends Prompt Engineering

**Prompt engineering** focuses on crafting the input text — choosing the right words, structure, and examples to get better outputs from a model. It's an important skill, but it's one component of a larger system.

**Context engineering** takes a holistic view of the entire context window. It treats all the elements that influence a model's behavior as interconnected components that need to be designed together:

| Component | Prompt Engineering | Context Engineering |
|-----------|-------------------|-------------------|
| **Scope** | The text of the prompt itself | Everything the model sees: system prompt, instructions, user input, tools, retrieved data, memory, state |
| **Focus** | Word choice, structure, examples | Architecture of the information environment |
| **Optimization** | Iterate on prompt wording | Design how components work together |
| **Persistence** | Per-conversation | Across sessions, users, and workflows |

Prompt engineering is a subset of context engineering — an essential one, but not the whole picture.

## The Components

Context engineering orchestrates multiple components that together shape model behavior. Each maps to one or more [building blocks](../agentic-building-blocks/index.md):

### System Prompts

The foundational layer that establishes the AI's role, capabilities, and behavioral parameters. System prompts define *who the AI is* for a given workflow — its expertise, tone, boundaries, and default behaviors.

Effective system prompts include role definition, behavioral guidelines, and capability boundaries. They can incorporate conditional behavior (adapting based on context), persona switching, and output formatting standards.

**Building blocks:** [Prompts](../agentic-building-blocks/prompts/index.md), [Projects](../agentic-building-blocks/projects/index.md)

### Instructions

Specific guidance for how the AI handles different types of tasks. While system prompts set the overall character, instructions direct behavior for particular scenarios — analysis tasks, creative work, technical tasks, and more.

Well-designed instructions include priority hierarchies (what takes precedence when guidance conflicts), escalation procedures (what to do when the AI can't complete a request), and dynamic adaptation (adjusting depth based on user responses).

**Building blocks:** [Prompts](../agentic-building-blocks/prompts/index.md), [Skills](../agentic-building-blocks/skills/index.md)

### User Input Processing

How the system interprets and enriches what users provide. This includes intent recognition (identifying what the user actually wants), context extraction (pulling implicit information from messages), and ambiguity resolution (strategies for handling unclear requests).

**Building blocks:** [Prompts](../agentic-building-blocks/prompts/index.md)

### Structured Inputs and Outputs

Defining precise formats for complex requests and responses. JSON schemas, templates, and metadata structures make interactions more predictable and consistent. On the output side, standardized formats and progressive disclosure (layered detail levels) improve usability.

**Building blocks:** [Prompts](../agentic-building-blocks/prompts/index.md), [Skills](../agentic-building-blocks/skills/index.md)

### Tools

Integrations that extend AI capabilities beyond text generation. Context engineering considers which tools are available, how they're described to the model, and how their outputs are integrated back into the context. Tool categories include information retrieval, computation, communication, and content creation.

**Building blocks:** [MCP](../agentic-building-blocks/mcp/index.md), [Agents](../agentic-building-blocks/agents/index.md)

### RAG and Memory

Systems for accessing external knowledge and maintaining information across interactions. **Retrieval-Augmented Generation (RAG)** — retrieving relevant documents from a database and injecting them into the prompt — is one approach. Memory systems add persistence: short-term memory within a conversation, and long-term memory across sessions.

This includes decisions about what to retrieve, how to rank results, and what to remember versus forget.

**Building blocks:** [Context](../agentic-building-blocks/context/index.md), [Projects](../agentic-building-blocks/projects/index.md)

### State and Historical Context

Tracking the current status of interactions and learning from past ones. Conversation state (current topic, goals, progress), user state (expertise level, preferences), and task state (completed steps, blockers) all shape how the AI responds.

Historical context adds pattern recognition — identifying recurring themes, successful approaches, and seasonal patterns that inform future interactions.

**Building blocks:** [Context](../agentic-building-blocks/context/index.md), [Projects](../agentic-building-blocks/projects/index.md), [Agents](../agentic-building-blocks/agents/index.md)

## Why Context Engineering Matters

Context engineering addresses what happens when AI moves from simple chat interactions to production systems:

- **Consistency** — Designed context produces reliable, repeatable results across users and sessions
- **Scalability** — Systems that assemble context programmatically scale in ways that manual prompt crafting cannot
- **Maintainability** — Separating components (system prompt, instructions, tools, memory) makes systems easier to update and debug
- **Quality ceiling** — The upper bound of AI output quality is set by the context, not the prompt. Better context engineering raises that ceiling.

## Relationship to Context Graphs

[Context graphs](../agentic-building-blocks/context/context-graphs.md) are a specific technique *within* context engineering. Where context engineering is the overall discipline of designing what the model sees, context graphs are a structured approach to organizing relationships, decisions, and reasoning chains in that context.

Think of it this way: context engineering is the practice; context graphs are one of the more advanced tools in that practice.

## Further Reading

- [Context Engineering Guide](https://claude.ai/public/artifacts/f498a4cc-4c45-481c-a6dd-8e1d196dadb0) — comprehensive guide to context engineering components and techniques
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic
- [Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/) — LangChain
- [Context is the Next Data Platform](https://www.glean.com/blog/context-data-platform) — Glean

## Related

- [AI Engineering](index.md) — the parent discipline
- [Agentic Building Blocks](../agentic-building-blocks/index.md) — the seven components context engineering operates on
- [Prompts](../agentic-building-blocks/prompts/index.md) — the most fundamental building block, and a key component of context engineering
- [Context](../agentic-building-blocks/context/index.md) — the data and knowledge component
- [Context Graphs](../agentic-building-blocks/context/context-graphs.md) — structured reasoning graphs, an advanced technique within context engineering
- [Patterns](../patterns/index.md) — reusable approaches across building blocks
