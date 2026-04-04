---
title: Choosing the Right Building Block
description: Comparison matrix for the AI building blocks — quick reference tables by layer and a decision guide to help you pick the right block for your situation.
---Multiple building blocks, three layers — but which ones does your workflow actually need? This page gives you comparison tables to quickly differentiate the blocks and a decision guide to match your situation to the right starting point.

Most workflows need just two or three blocks. The goal isn't to use them all — it's to pick the right ones for the job.

:::tip[Start simple]
Begin with a **Prompt** and add blocks only when you hit a real limitation. If you're re-typing the same instructions, add a **Skill**. If you need external data, add **MCP**. If you need multi-step autonomy, add an **Agent**. Don't over-engineer — let the workflow tell you what it needs.
:::
## At a Glance

All blocks in one view — use this to quickly orient yourself, then drill into the layer tables below for full details.

| Block | Primary Job | Best For | Typical User |
|-------|------------|----------|--------------|
| **[Model](models/index.md)** | Process and generate | Choosing the right engine for speed, depth, or cost | Everyone |
| **[Context](context/index.md)** | Inform | Grounding the model in your specific domain knowledge | Everyone |
| **[Project](projects/index.md)** | Organize | Persisting instructions and context across conversations | Everyone |
| **[Memory](memory/index.md)** | Remember | Accumulating preferences and patterns over time | Everyone |
| **[Prompt](prompts/index.md)** | Instruct | One-off or conversational tasks with clear instructions | Everyone |
| **[Skill](skills/index.mdx)** | Standardize | Repeatable routines you run the same way every time | Everyone |
| **[Agent](agents/index.md)** | Execute autonomously | Multi-step workflows requiring planning and tool use | Power user |
| **[MCP](mcp/index.md)** | Connect | Bridging AI to external tools, data, and services | Power user |
| **[API](api/index.md)** | Integrate programmatically | Embedding AI in applications and automated pipelines | Developer |
| **[SDK](sdk/index.md)** | Orchestrate in code | Building agent systems with tool use, memory, and handoffs | Developer |
| **[CLI](cli/index.md)** | Interact from terminal | Working with AI in the terminal, scripting, and headless automation | Power user / Developer |

---

## Intelligence Layer

*The persistent foundation: engine, knowledge, and workspace powering every interaction.*

|  | **Model** | **Context** | **Project** | **Memory** |
|--|----------|------------|------------|-----------|
| **What it provides** | AI engine that processes inputs and generates outputs | Background knowledge the model doesn't have | Persistent workspace grouping instructions, context, and skills | Accumulated knowledge from past interactions |
| **Primary job** | Process and generate | Inform | Organize | Remember |
| **Persistence** | Always available (platform-managed) | Ephemeral (per-conversation) or attached to a project | Persistent across conversations | Persistent and growing across conversations |
| **Contains** | Trained weights, capability tiers, modality support | Files, docs, data, examples, reference material | Instructions, context files, conversation history, skills | Preferences, decisions, facts, learned patterns |
| **When it loads** | Selected before or during a conversation | Attached at conversation start or mid-conversation | Active when you open a conversation in the project | Retrieved automatically when relevant |
| **Can include code** | No (model selection, not authoring) | Yes (code files as reference material) | Yes (code in project knowledge or instructions) | No (system-managed, natural language) |
| **Best for** | Choosing the right engine for speed, depth, or cost | Grounding the model in your specific domain | Persisting setup so you don't re-upload every time | Adapting AI behavior over time without manual setup |
| **Who manages it** | Platform (you choose tier) | User-curated | User-curated | System-managed |
| **Requires external access** | No | No (you bring the files) | No | No |
| **Typical user** | Everyone | Everyone | Everyone | Everyone |

---

## Orchestration Layer

*The execution layer: instructions, routines, and autonomous agents that direct and do the work.*

|  | **Prompt** | **Skill** | **Agent** |
|--|-----------|----------|----------|
| **What it provides** | Natural language instructions to the model | Reusable routine with defined inputs and outputs | Autonomous AI that plans, uses tools, and executes multi-step work |
| **Primary job** | Instruct | Standardize | Execute autonomously |
| **Persistence** | Ephemeral (per-conversation) | Persistent (saved as files, reusable across conversations) | Ephemeral (runs for a session) or scheduled |
| **Contains** | Natural language instructions, examples, constraints | Instructions, reference files, output format specs | Goals, tool access, planning logic, decision-making |
| **When it loads** | When you type or send a message | Auto-triggered when relevant, or invoked via slash command | Launched explicitly or on a schedule |
| **Can include code** | No (natural language only) | Yes (scripts, templates, code references) | Yes (reads, writes, and runs code) |
| **Best for** | One-off or conversational tasks with clear instructions | Repeatable routines you run the same way every time | Multi-step workflows requiring planning and tool use |
| **Who manages it** | User (typed in the moment) | User-curated (packaged for reuse) | User-launched or developer-built |
| **Requires external access** | No | No (self-contained instructions) | Often yes (uses tools, files, MCP connections) |
| **Typical user** | Everyone | Everyone | Power user |

---

## Integration Layer

*The connection layer: protocols, interfaces, and frameworks that bridge AI to external systems and code.*

|  | **MCP** | **API** | **SDK** | **CLI** |
|--|--------|--------|--------|--------|
| **What it provides** | Connector to external tools, services, and databases | Programmatic interface for accessing AI models | Frameworks for building AI workflows in code | Terminal-native interface for interacting with AI |
| **Primary job** | Connect | Integrate programmatically | Orchestrate in code | Interact from terminal |
| **Persistence** | Persistent (configured once, available across conversations) | Stateless (each call is independent) | Persistent (code you deploy and maintain) | Persistent (project memory files, settings) |
| **Contains** | Server configs, tool definitions, authentication | API keys, endpoint URLs, request/response schemas | Libraries, agent loops, tool abstractions, patterns | Skills, plugins, hooks, MCP connections, project memory |
| **When it loads** | Connected at startup or configured in settings | Called on demand from code | Imported into your application code | Launched from the terminal interactively or via script |
| **Can include code** | Yes (server implementations) | Yes (code making HTTP requests) | Yes (the primary interface is code) | Yes (reads, writes, and runs code) |
| **Best for** | Bridging AI to external tools, data, and services | Embedding AI in applications and automated pipelines | Building agent systems with tool use, memory, and handoffs | Working with AI in the terminal, scripting, headless automation |
| **Who manages it** | User-configured or developer-built | Developer-owned | Developer-owned | User-launched or script-driven |
| **Requires external access** | Yes (bridges to external systems) | Yes (calls external APIs) | Yes (wraps APIs and external services) | Yes (calls APIs under the hood) |
| **Typical user** | Power user | Developer | Developer | Power user / Developer |

---

## Decision Guide: "I want to..."

Use this table to find your starting point. Most real workflows combine several blocks — this tells you where to begin.

| I want to... | Start with | Add when needed |
|-------------|-----------|----------------|
| Ask AI a question | **Prompt** | + **Context** if it needs your specific data |
| Get better answers about my domain | **Context** + **Prompt** | + **Project** to persist the setup |
| Stop re-uploading the same files | **Project** | + **Memory** to also retain learned preferences |
| Have AI remember how I like things done | **Memory** | Already persistent — just keep using it |
| Run the same workflow every week | **Skill** | + **MCP** if the skill needs external data |
| Pull live data into a conversation | **MCP** | + **Skill** to standardize what you do with the data |
| Automate a multi-step research task | **Agent** | + **MCP** for external sources, + **Skill** for sub-routines |
| Build AI into my app | **API** | + **SDK** for complex orchestration |
| Coordinate multiple agents in code | **SDK** | + **MCP** for external tool access |
| Work with AI in my terminal | **CLI** | + **Skills** for reusable routines, + **MCP** for external data |
| Automate AI in shell scripts or CI | **CLI** (headless mode) | + **MCP** for external system access |
| Get AI help while coding | **CLI** | + **Project** memory for persistent conventions |
| Choose between fast and deep AI | **Model** (select the right tier) | All other blocks work with any model |

---

## Related

- [Building Blocks Overview](index.md) — what each block is, with cross-platform implementations
- [Design Your AI Workflow](../business-first-ai-framework/design.md) — mapping workflow steps to building blocks
- [Business-First AI Framework](../business-first-ai-framework/index.md) — the full Analyze → Deconstruct → Build methodology
