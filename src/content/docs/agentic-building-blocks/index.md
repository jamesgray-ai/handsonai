---
title: Agentic AI Building Blocks
description: The eleven components of agentic AI workflows — Model, Prompt, Context, Project, Memory, Skill, Agent, MCP, API, SDK, and CLI
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## Overview

The AI building blocks are a shared vocabulary for describing the components of any AI workflow. Whether you're writing a single prompt, calling a model from code, or orchestrating a multi-agent pipeline, every AI workflow is assembled from some combination of these building blocks.

Three layers:

- **Intelligence** — Model, Context, Project, Memory
- **Orchestration** — Prompt, Skill, Agent
- **Integration** — MCP, API, SDK, CLI

These are platform-agnostic concepts. Every major AI platform implements them, though the names and interfaces differ. Understanding the blocks gives you a mental model that transfers across tools — you can evaluate any platform by asking "how does it handle models, prompts, context, projects, memory, skills, agents, external connections, APIs, development frameworks, and command-line interfaces?"

:::note[Which block should I use?]
Not sure where to start? The [Choosing the Right Building Block](comparison.md) page has comparison tables for all blocks and a "I want to..." decision guide.
:::
:::tip[Using building blocks for workflow analysis]
The [Business-First AI Framework](../business-first-ai-framework/index.md) uses these building blocks as the analysis tool in [Design Your AI Workflow](../business-first-ai-framework/design.md), where each step of a workflow gets mapped to the building blocks it needs.
:::
<div class="grid cards single-column" markdown>

-   🧠 **Intelligence**

    ---

    *The persistent foundation: engine, knowledge, and workspace powering every interaction.*

    - **[Model](models/index.md)** — The AI engine that processes inputs and generates outputs
    - **[Context](context/index.md)** — Background information and reference material
    - **[Project](projects/index.md)** — Persistent workspace grouping prompts, context, and skills
    - **[Memory](memory/index.md)** — Accumulated knowledge from past interactions

-    **Orchestration**

    ---

    *The execution layer: instructions, routines, and autonomous agents that direct and do the work.*

    - **[Prompt](prompts/index.md)** — Natural language instructions to the model
    - **[Skill](skills/index.mdx)** — Reusable routine with defined inputs and outputs
    - **[Agent](agents/index.md)** — Autonomous AI that plans, uses tools, and executes multi-step work

-    **Integration**

    ---

    *The connection layer: protocols, interfaces, and frameworks that bridge AI to external systems and code.*

    - **[MCP](mcp/index.md)** — Connector to external tools, services, and databases
    - **[API](api/index.md)** — Programmatic interface for accessing AI models
    - **[SDK](sdk/index.md)** — Frameworks and toolkits for building AI workflows in code
    - **[CLI](cli/index.md)** — Terminal-native interface for interacting with AI

</div>

## Intelligence

*The persistent foundation: engine, knowledge, and workspace powering every interaction.*

### Model

The AI engine that processes inputs and generates outputs. Models are trained on data and come in different capability tiers — from fast, lightweight models for simple tasks to deep reasoning models for complex analysis.

**Key characteristics:**

- The foundation all other blocks operate on — every AI interaction requires a model
- Come in capability tiers: fast models for speed, reasoning models for depth
- Have defined context windows and vary by modality (text, code, vision, audio)

**When to use it:** Every AI interaction uses a model. The key decision is choosing the *right* model — matching model capabilities to your task requirements.

**Example:** Using a fast model for high-volume email classification, and a reasoning model for complex strategy analysis that requires nuanced judgment.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Multiple model tiers (fast, balanced, reasoning); select via model picker or API |
| OpenAI (ChatGPT) | Multiple model tiers (fast, balanced, reasoning); select via model picker or API |
| Gemini | Multiple model tiers (fast, balanced); select via model picker or API |
| M365 Copilot | Models managed by Microsoft; limited user selection |

**Relationship to other blocks:** Model is the engine — prompts steer it, context informs it, skills package routines for it, agents orchestrate it, MCP connects it to external systems, APIs expose it to code, and SDKs provide frameworks for orchestrating it.

---

### Context

Unique knowledge (not in models) required by the agentic workflow for execution. These are information from sources such as docs, databases, and markdown files.

**Key characteristics:**

- Provides knowledge the model doesn't have — your data, your docs, your domain
- Can be inline (pasted into the conversation), attached as files, or pre-loaded in a project
- Improves output quality by grounding the model in your specific domain

**When to use it:** When the model needs information it wasn't trained on — your company's style guide, a product spec, customer data, or examples of desired output format.

**Example:** Attaching your brand voice guidelines and three sample blog posts before asking the model to draft a new one.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | File attachments, project knowledge base, conversation history |
| OpenAI (ChatGPT) | File uploads, Custom GPT knowledge files, conversation history |
| Gemini | File uploads, Google Drive integration, NotebookLM sources |
| M365 Copilot | Microsoft Graph (emails, files, meetings), attached documents |

**Relationship to other blocks:** Context makes prompts smarter. Projects organize context persistently so you don't re-upload it every time.

---

### Project

Self-contained workspaces with their own chat histories and knowledge bases that set custom instructions applying to all conversations within the project.

**Key characteristics:**

- Organizes related resources in one place so they persist across conversations
- Sets custom instructions that apply to every conversation in the project
- Reduces setup time: start a new conversation with everything already in place

**When to use it:** When you run the same type of workflow repeatedly and want to avoid re-uploading context and re-explaining instructions every time.

**Example:** A "Weekly Client Reports" project that contains your report template, client data, brand guidelines, and standing instructions for tone and format.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Claude Projects (with project knowledge and custom instructions) |
| OpenAI (ChatGPT) | Custom GPTs, or Projects in ChatGPT |
| Gemini | Gems (with custom instructions and uploaded context) |
| M365 Copilot | Copilot agents with knowledge sources and instructions |

**Relationship to other blocks:** Projects are containers — they hold the prompts, context, and skills a workflow needs, making the whole package reusable.

---

### Memory

Accumulated knowledge from past interactions — preferences, decisions, facts, and patterns that the AI retains and retrieves when relevant. Memory makes AI persistent rather than stateless.

**Key characteristics:**

- System-managed, not user-curated — the AI decides what to remember
- Persists across conversations — survives session boundaries
- Grows over time — more interactions produce richer memory

**When to use it:** When repeating context to the AI is friction — preferences, project conventions, communication style — or when the AI should adapt to how you work over time.

**Example:** After several conversations about a project, the AI remembers your preferred report format, the client's communication preferences, and that last week's deliverable was delayed — without you re-explaining any of it.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Claude memory, CLAUDE.md project memory, conversation continuity |
| OpenAI (ChatGPT) | ChatGPT Memory, custom instructions persistence |
| Gemini | Conversation memory, Gems with learned preferences |
| M365 Copilot | Microsoft Graph as implicit memory, organizational knowledge |

**Relationship to other blocks:** Memory complements context — context is knowledge you provide, memory is knowledge the AI accumulates. Projects organize context; memory adds learned persistence on top.

---

## Orchestration

*The execution layer: instructions, routines, and autonomous agents that direct and do the work.*

### Prompt

Instructions you provide to an AI in natural language during a conversation. Prompts are ephemeral, conversational, and reactive — you provide context and direction in the moment.

**Key characteristics:**

- The most fundamental building block — every AI interaction starts with a prompt
- Can range from a single sentence to a detailed multi-section instruction
- Ephemeral by default: conversational and reactive, used in the moment

**When to use it:** Any time you interact with an AI model. A good prompt is sufficient for many tasks without needing other blocks.

**Example:** "Summarize this quarterly sales report in three bullet points, highlighting the biggest change from last quarter."

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Message in conversation, system prompt, or project instructions |
| OpenAI (ChatGPT) | Message in conversation, system prompt, or Custom GPT instructions |
| Gemini | Message in conversation or Gem instructions |
| M365 Copilot | Message in chat, or prompt within a Copilot agent |

**Relationship to other blocks:** Prompts are the foundation — context enhances them, skills package them for reuse, and agents chain them together.

---

### Skill

Folders containing instructions, scripts, and resources that the AI discovers and loads dynamically when relevant to a task. Skills are now an open standard and being adopted broadly.

**Key characteristics:**

- Encapsulates a specific capability: instructions, context, and output format bundled together
- Invocable two ways: auto-triggered when relevant, or invoked directly with a slash command
- Reusable across conversations, shareable with others, and becoming an open standard

**When to use it:** When you find yourself writing the same prompt repeatedly, or when a workflow step is well-defined enough to package as a repeatable routine.

**Example:** A "Draft Meeting Recap" skill that takes meeting notes as input and produces a formatted summary with action items, decisions, and follow-ups — in your team's standard format every time.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Claude Code Skills (SKILL.md files with instructions and references) |
| OpenAI (ChatGPT) | Custom GPTs, or Actions within a GPT |
| Gemini | Gems with structured instructions |
| M365 Copilot | Copilot agent actions, Power Automate flows triggered by Copilot |

**Relationship to other blocks:** Skills are upgraded prompts — they package a prompt with its context into something reusable. Agents can invoke skills as part of multi-step workflows.

:::note[Skills vs. Agents]
A skill is a **routine** — it does one thing well when invoked. An agent is **autonomous** — it decides what to do, which tools to use, and when to invoke skills. Think of skills as tools in a toolbox and agents as the person using the toolbox.
:::
---

### Agent

A system where an LLM controls workflow execution to achieve a goal.

**Key characteristics:**

- Plans its own approach: breaks goals into steps and decides which tools to use
- Uses tools: can read files, search the web, run code, call APIs
- Iterates: evaluates its own output, handles errors, and adjusts course

**When to use it:** When a workflow requires multiple steps, tool use, or decision-making that would be tedious to manage manually through individual prompts.

**Example:** A research agent that takes a topic, searches multiple sources, synthesizes findings, fact-checks claims, and produces a structured report — deciding on its own which sources to consult and how deep to go.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Claude Code agents (autonomous tool-using sessions), Cowork agents |
| OpenAI (ChatGPT) | Custom GPTs with Actions, Assistants API with tools |
| Gemini | Gemini with extensions (Google Search, Workspace, Maps, etc.) |
| M365 Copilot | Copilot agents with plugins and connectors |

**Relationship to other blocks:** Agents orchestrate the other blocks — they use prompts, draw on context, invoke skills, and connect to external systems through MCP.

---

## Integration

*The connection layer: protocols, interfaces, and frameworks that bridge AI to external systems and code.*

### MCP (Model Context Protocol)

An open standard for connecting AI assistants to external systems where data lives — content repositories, business tools, databases, and development environments.

**Key characteristics:**

- Bridges the gap between the AI and the outside world where your data lives
- Open standard: one integration pattern that works across compatible platforms
- Enables read and write operations: the AI can both retrieve information and take actions

**When to use it:** When the AI needs to interact with external systems — reading from a database, posting to Slack, creating tasks in a project management tool, or accessing live data.

**Example:** An MCP connector to your CRM that lets the AI look up client history, check deal status, and log meeting notes — all within the conversation.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | MCP servers (local or remote) connected via Claude Code or Claude Desktop |
| OpenAI (ChatGPT) | Function calling, Actions in Custom GPTs, Assistants API tools |
| Gemini | Extensions and function calling |
| M365 Copilot | Connectors, plugins, Power Platform integrations |

**Relationship to other blocks:** MCP extends what agents and skills can do by connecting them to external systems. Without MCP, the AI is limited to what's in the conversation.

---

### API

Programmatic interfaces for accessing AI models and cloud services. The code-first way to interact with AI — send a request, get a response.

**Key characteristics:**

- Stateless request/response pattern — each call is independent
- Authentication via API keys with usage-based billing
- Platform-agnostic — any language that can make HTTP requests can call an API

**When to use it:** When you need to integrate AI into an application, automate workflows programmatically, or access model capabilities beyond what the chat UI provides.

**Example:** Calling the Claude API from a Python script to classify 1,000 customer support tickets overnight, or calling a search API to enrich an agent's research.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Anthropic REST API with Messages endpoint; Python and TypeScript SDKs |
| OpenAI (ChatGPT) | REST API with Chat Completions endpoint; Python and TypeScript SDKs |
| Gemini | REST API with generateContent endpoint; Python SDK; Vertex AI for enterprise |
| M365 Copilot | Azure AI Services REST APIs; .NET, Python, Java SDKs |

**Relationship to other blocks:** API is the programmatic bridge — it's how you call models from code, and SDKs abstract over it. MCP servers often wrap APIs to give agents standardized access.

---

### SDK

Frameworks and toolkits that provide abstractions for building AI workflows in code. Where APIs give you raw access, SDKs give you patterns and structure.

**Key characteristics:**

- Provide higher-level abstractions for tool use, memory, and multi-agent coordination
- Handle orchestration logic — planning, routing, error recovery
- Opinionated about patterns — agent loops, handoffs, guardrails

**When to use it:** When you're building agents or multi-step workflows in code and want established patterns for tool use, memory management, or multi-agent coordination rather than wiring everything from scratch.

**Example:** Using the Claude Agent SDK to build a research agent with tool use and memory, or LangGraph to orchestrate a multi-agent pipeline with handoffs.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Agent SDK (Python, TypeScript) for agents with tool use, handoffs, and guardrails |
| OpenAI (ChatGPT) | Agents SDK (Python, TypeScript) for agents with function calling, handoffs, and tracing |
| Gemini | Agent Development Kit (ADK) for agents on Vertex AI with Google Cloud integrations |
| M365 Copilot | M365 Agents SDK (.NET, Python, TypeScript) for agents deployed to Microsoft 365 surfaces |

**Relationship to other blocks:** SDKs orchestrate models, abstract over APIs, and implement the agent concept in code. They integrate with MCP for external system access and formalize patterns like tool use and handoffs.

---

### CLI

Terminal-native interfaces for interacting with AI. Instead of using a browser-based chat or calling an API from code, you work with AI directly from the command line — the same environment where you run commands, manage files, and write code.

**Key characteristics:**

- Terminal-native — runs where you already work, with full file-system access
- Scriptable — supports headless mode for automation, CI/CD, and scheduled tasks
- Extensible — supports plugins, skills, hooks, and MCP server connections

**When to use it:** When you're working with AI in the terminal — coding, debugging, automating tasks via shell scripts or CI pipelines, or running scheduled AI jobs without a chat window.

**Example:** Using Claude Code to refactor a module — it reads the code, proposes changes, runs tests, and commits the result. Or running a CLI in headless mode in CI to generate release notes from git history on every push.

**Cross-platform implementations:**

| Platform | How It Works |
|----------|-------------|
| Claude | Claude Code — interactive + headless modes, tool use, skills, plugins, MCP integration |
| OpenAI (ChatGPT) | Codex CLI — interactive + headless modes, file editing, sandboxed execution |
| Gemini | Gemini CLI — interactive mode, Google Cloud integrations, MCP support |
| M365 Copilot | GitHub Copilot CLI — command suggestions, shell integration |

**Relationship to other blocks:** CLIs are the terminal-native interaction layer — they abstract over APIs to give humans (and scripts) a conversational interface to AI, with file-system awareness, tool use, and MCP integration built in.

## How the Blocks Fit Together

The building blocks are composable — combine the ones your workflow needs. Here's how a typical workflow grows as you adopt more blocks:

1. **Choose a Model** — Select the right AI engine for your task (speed vs. depth, modality, cost)
2. **Start with a Prompt** — Write clear instructions for what you want done
3. **Add Context** — Attach reference materials so the model has what it needs
4. **Organize in a Project** — Group your prompt and context so they persist across conversations
5. **Build Memory** — Let the AI accumulate preferences, patterns, and knowledge across conversations
6. **Package as a Skill** — Turn the prompt + context into a reusable routine you can invoke with different inputs
7. **Connect with MCP** — Give the skill access to external data and tools
8. **Orchestrate with an Agent** — Let an autonomous AI run the skill, use MCP connections, and handle multi-step workflows
9. **Interact via CLI** — Use a terminal-native AI tool to work with code, automate tasks, and run headless AI jobs from the command line
10. **Call via API** — Integrate the workflow into an application or automated pipeline by calling the model programmatically
11. **Build with an SDK** — Use a framework to orchestrate agents, manage tool use, and coordinate multi-agent pipelines in code

### Worked example: Weekly Client Status Report

| Stage | What Changes |
|-------|-------------|
| **Prompt only** | You paste "Write a status report for Client X covering this week's deliverables..." into a chat every Monday |
| **+ Context** | You attach the client's project brief and last week's report so the model has history |
| **+ Project** | You create a "Client Reports" project with the brief, templates, and standing instructions pre-loaded |
| **+ Memory** | The project remembers your preferred report format, the client's communication preferences, and that last week's deliverable was delayed — no need to re-explain |
| **+ Skill** | You package "generate weekly status report" as a skill — now you just invoke it with this week's updates |
| **+ MCP** | The skill pulls this week's completed tasks from your project management tool and time entries from your time tracker |
| **+ Agent** | An agent runs every Monday: gathers data via MCP, generates the report using the skill, drafts an email, and flags anything that needs your review |
| **+ CLI** | You use a terminal-native AI tool to run the report workflow from the command line — interactively while refining, or headless on a schedule via cron |
| **+ API** | You call the model via API from a script that runs on a schedule, processing inputs from a database and writing results back — no chat window needed |
| **+ SDK** | You build the agent using a framework that handles tool orchestration, error recovery, and handoffs between a data-gathering agent and a report-writing agent |

**Not every workflow needs every block.** Many tasks are handled perfectly well with a prompt and some context. The blocks are a menu, not a checklist — use what the workflow actually requires.

## Platform Comparison

All building blocks across all four platforms in one view:

| Building Block | Claude | OpenAI (ChatGPT) | Gemini | M365 Copilot |
|---------------|--------|-------------------|--------|--------------|
| **Model** | Multiple tiers (fast, balanced, reasoning) | Multiple tiers (fast, balanced, reasoning) | Multiple tiers (fast, balanced) | Microsoft-managed |
| **Prompt** | Conversation messages, system prompts | Conversation messages, system prompts | Conversation messages | Chat messages |
| **Context** | File attachments, project knowledge | File uploads, GPT knowledge files | File uploads, Drive, NotebookLM | Microsoft Graph, documents |
| **Project** | Claude Projects | Custom GPTs, ChatGPT Projects | Gems | Copilot agents |
| **Memory** | Claude memory, CLAUDE.md | ChatGPT Memory | Conversation memory | Microsoft Graph |
| **Skill** | Claude Code Skills | Not yet available | Not yet available | Not yet available |
| **Agent** | Claude Code agents, Cowork | Assistants API, GPTs with Actions | Extensions | Copilot agents with plugins |
| **MCP** | MCP servers | Function calling, Actions | Extensions, function calling | Connectors, plugins |
| **API** | Anthropic REST API (Python, TypeScript SDKs) | OpenAI REST API (Python, TypeScript SDKs) | Gemini API, Vertex AI (Python SDK) | Azure AI Services (.NET, Python, Java) |
| **SDK** | Claude Agent SDK (Python, TypeScript) | OpenAI Agents SDK (Python, TypeScript) | Agent Development Kit (Python) | M365 Agents SDK (.NET, Python, TypeScript) |
| **CLI** | Claude Code | Codex CLI | Gemini CLI | GitHub Copilot CLI |

## Common Misconceptions

**"Skills and agents are the same thing."**
Skills are routines — they do one specific thing when invoked. Agents are autonomous — they decide what to do, plan steps, and invoke skills (among other tools) to accomplish goals. A skill is a tool; an agent is the one using the toolbox.

**"You need all blocks for every workflow."**
Most workflows need two or three blocks. A well-written prompt with good context handles many tasks. Only add blocks when the workflow genuinely requires them.

**"APIs and SDKs are the same thing."**
An API is a raw interface — you send a request, you get a response. An SDK is a framework that builds on APIs, adding patterns for orchestration, tool use, memory, and multi-agent coordination. You can use APIs without an SDK, but SDKs make complex workflows much easier to build.

**"Memory and context are the same thing."**
Context is knowledge you provide — files, docs, examples attached to a conversation. Memory is knowledge the AI accumulates — preferences, past decisions, and patterns learned over time. You curate context; the AI manages memory.

**"A project is just a folder."**
A project is an active workspace — it provides standing instructions, persistent context, and conversation continuity. It shapes how the AI behaves for every conversation within it, not just where files are stored.

## Related

**Comparison and decision guide:**

- [Choosing the Right Building Block](comparison.md) — comparison matrix and "I want to..." decision guide

**Framework and courses:**

- [Business-First AI Framework](../business-first-ai-framework/index.md) — applies building blocks to workflow analysis
- [Design Your AI Workflow](../business-first-ai-framework/design.md) — mapping workflow steps to building blocks
- [Agentic AI for Leaders](../courses/leaders/index.md) — course covering AI strategy and building blocks
- [Claude for Builders](../courses/builders/index.md) — hands-on course building with these blocks

**Fundamentals deep-dives:**

- [Model](models/index.md) — the AI engine that powers everything
- [Prompts](prompts/index.md) — the Prompt building block, with prompt engineering techniques
- [Context](context/index.md) — background information and reference materials
- [Projects](projects/index.md) — project workspaces with memory, knowledge bases, and custom instructions
- [Memory](memory/index.md) — accumulated knowledge from past interactions
- [Skills](skills/index.mdx) — reusable routines the AI invokes when relevant
- [Agents](agents/index.md) — concepts for the Agent building block
- [MCP](mcp/index.md) — connecting AI to external systems
- [API](api/index.md) — programmatic interfaces for accessing AI models and services
- [SDK](sdk/index.md) — frameworks and toolkits for building AI workflows in code
- [CLI](cli/index.md) — terminal-native interfaces for interacting with AI
- [AI Engineering](../ai-engineering/index.md) — practices for designing and optimizing AI systems, including context engineering
- [Patterns](../patterns/index.md) — reusable approaches across building blocks

**Use cases:**

- [AI Use Cases](../use-cases/index.md) — what teams build with these blocks, organized by six primitives

**Platform-specific guides:**

- [Claude Projects](../platforms/claude/projects/claude-projects-setup.md) — setting up the Project block on Claude
- [Claude Skills](../platforms/claude/skills/skills-discovery-meta-prompt.md) — discovering Skills on Claude
- [Claude Subagents](../platforms/claude/subagents/scheduling-subagents.mdx) — scheduling Agents on Claude
