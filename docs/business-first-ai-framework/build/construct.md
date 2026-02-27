---
title: "3.2: Construct"
description: The model executes the plan from Design to build your workflow's building blocks — prompts, context, skills, agents, MCP connections, and projects — in whatever format your platform requires.
---

# 3.2: Construct

> **Part of:** [Build Workflows](index.md)

## What This Is

In [Design (3.1)](design.md), you worked with the model in two phases — first collaborating on architecture decisions and execution pattern (normal conversation), then activating plan mode so the model could plan the full AI Building Block Spec. You reviewed and approved that spec.

Now the model shifts from planning to execution. **Exit plan mode** — the model takes the approved spec and builds the actual building blocks your workflow needs, in whatever format your platform requires.

| | |
|---|---|
| **What happens** | The model reads your approved AI Building Block Spec and generates your building blocks — prompts, context files, skills, agents, MCP connections, and project configurations |
| **Your role** | Review what the model produces, provide business-specific materials when prompted, and approve each building block |
| **What you get** | Working building blocks ready to run, plus a **Run Guide** with setup instructions |

!!! warning "Exit plan mode before starting Construct"
    If you used plan mode during Design, switch back to normal mode now. Construct is execution — the model needs to create files, run web searches, and generate building blocks, which requires normal mode.

    | Platform | How to exit plan mode |
    |---|---|
    | **Claude Code** | Press `Escape`, or press `Shift+Tab` to cycle back to normal mode |
    | **Cursor** | Switch composer mode back to normal |
    | **Codex CLI** | Run without the `--plan` flag |
    | **Other AI tools** | Simply continue the conversation — tell the model to start building |

This step is facilitated by the **`building-workflows`** Business-First AI Framework Skill — the same skill that ran Design. After you approve the AI Building Block Spec, the model transitions into Construct and begins generating building blocks.

If you're starting Construct separately (e.g., in a new conversation), provide the AI Building Block Spec:

```
Build the workflow from my AI Building Block Spec.
```

Upload or paste your `[workflow-name]-building-block-spec.md` file when prompted.

!!! tip "If your AI tool doesn't support skills"
    Use this page as a conversation guide — walk through each section in order with your AI tool. Ask it to generate each building block based on what your spec requires.

## What Construct Produces

By the end of this step, you'll have two things:

**Your building blocks** — the prompts, skills, agents, context files, and configurations your workflow needs, generated in whatever format your platform requires. The model only builds the building blocks your execution pattern calls for — a Prompt pattern doesn't get agent files, and a Single Agent pattern doesn't get multi-agent orchestration.

**Run Guide** (`[name]-run-guide.md`) — a plain-language walkthrough tailored to your platform and technical comfort level:

1. **What was built** — every building block listed with what it does and where it lives
2. **Setup steps** — numbered instructions for getting each artifact into the right place on your platform
3. **First run** — a guided test with sample input, expected behavior, and common first-run issues
4. **What to do next** — how to run it again, share with teammates, and when to revisit

The Run Guide is your bridge from Construct to [Run (3.3)](run.md) — follow it to get your workflow running.

## What Gets Built

The model constructs from the ten AI building blocks — but only the ones your workflow needs:

| Building Block | What the model generates | When it's needed |
|---|---|---|
| **[Prompt](../../agentic-building-blocks/prompts/index.md)** | A structured prompt with step-by-step instructions, input requirements, and output format | Every pattern |
| **[Context](../../agentic-building-blocks/context/index.md)** | Reference documents, style guides, examples, or data files the workflow needs | When steps require domain-specific knowledge |
| **[Skill](../../agentic-building-blocks/skills/index.md)** | Reusable routines with defined inputs, process, and outputs | When the spec tags steps as skill candidates |
| **[Agent](../../agentic-building-blocks/agents/index.md)** | Agent definitions with instructions, tools, and goals | Single Agent and Multi-Agent patterns |
| **[MCP](../../agentic-building-blocks/mcp/index.md)** | Tool connections to external services, APIs, or databases | When steps need to read from or write to external systems |
| **[Project](../../agentic-building-blocks/projects/index.md)** | Workspace configuration grouping the workflow's artifacts | When the workflow runs frequently with the same context |
| **[Memory](../../agentic-building-blocks/memory/index.md)** | Memory configuration or persistence notes (e.g., CLAUDE.md conventions, memory prompts) | When the workflow benefits from carrying preferences or decisions across runs |
| **[API](../../agentic-building-blocks/api/index.md)** | API call scripts, authentication setup, request/response handling | When the architecture approach is code-first and steps need programmatic model access |
| **[SDK](../../agentic-building-blocks/sdk/index.md)** | Agent project scaffolding, tool definitions, orchestration code | When the architecture approach is code-first and steps need agent frameworks |
| **Model** | Model selection recommendations based on step requirements | When steps need specific capabilities (reasoning, speed, multimodal) |

## How the Model Builds for Your Platform

The model generates building blocks in whatever format your platform requires — but it doesn't guess. It follows a two-step research process:

1. **Start with curated platform documentation.** The cookbook maintains [platform reference pages](../../platforms/claude/index.md) for Claude, OpenAI, Google Gemini, and M365 Copilot — each with links to official documentation, SDK references, and setup guides. The model reads the reference page for your platform first.
2. **Verify and supplement via web search.** The model then uses web search to confirm the documentation is still current and to find any newer resources. This catches renamed APIs, deprecated SDKs, and newly released tools.

This hybrid approach anchors the model in authoritative sources while ensuring it stays current as platforms evolve. The model provides the implementation (how to build it on your platform); the AI Building Block Spec provides the specs (what each building block should do).

## Pattern-Specific Build Paths

Your execution pattern (chosen in Design) determines which building blocks get built. The model works through only the steps that apply:

=== "Prompt"

    1. **Create context** — Build the context artifacts from your spec's Context Inventory
    2. **Set up project workspace** (optional) — If the spec recommends a project
    3. **Generate the prompt** — The model generates the workflow prompt for your platform
    4. **Generate the Run Guide**

=== "Skill-Powered Prompt"

    1. **Create context** — Build the context artifacts from your spec's Context Inventory
    2. **Set up project workspace** (optional) — If the spec recommends a project
    3. **Build skills** — The model generates skills for the steps tagged as skill candidates
    4. **Generate the prompt** — The model generates the workflow prompt, referencing the skills
    5. **Generate the Run Guide**

=== "Single Agent"

    1. **Create context** — Build the context artifacts from your spec's Context Inventory
    2. **Build skills** — The model generates skills for tagged candidates
    3. **Connect tools** — Wire external tools from the spec's Tools and Connectors section
    4. **Build the agent** — The model generates the agent definition for your platform
    5. **Generate the Run Guide**

=== "Multi-Agent"

    1. **Create context** — Build the context artifacts from your spec's Context Inventory
    2. **Build skills** — The model generates skills for tagged candidates
    3. **Connect tools** — Wire external tools from the spec's Tools and Connectors section
    4. **Build each specialist agent** — The model generates agent definitions for each role
    5. **Build the orchestrator** — The model generates the coordination layer
    6. **Generate the Run Guide**

### Code-First Build Paths

When your architecture approach is **code-first**, the same four execution patterns apply — but the implementation uses APIs and SDKs instead of platform UIs. The model generates code artifacts instead of platform configurations.

=== "Prompt (code-first)"

    1. **Create context** — Build context artifacts as files (Markdown, JSON, or data exports)
    2. **Set up API credentials** — Configure authentication for your chosen API (API key, environment variables)
    3. **Generate the API call script** — The model generates a script that sends the prompt with context to the API and handles the response
    4. **Test locally** — Run the script and verify the output
    5. **Generate the Run Guide**

=== "Skill-Powered Prompt (code-first)"

    1. **Create context** — Build context artifacts as files
    2. **Set up API credentials** — Configure authentication
    3. **Build reusable functions** — The model generates functions for each skill candidate, encapsulating the logic as callable code
    4. **Generate the main script** — The model generates a script that composes the functions with the prompt and context
    5. **Test locally** — Run the script and verify the output
    6. **Generate the Run Guide**

=== "Single Agent (code-first)"

    1. **Create context** — Build context artifacts as files
    2. **Initialize SDK project** — Set up the project structure for your chosen SDK (e.g., `pip install anthropic-agent-sdk`, `npm init`)
    3. **Define tools** — The model generates tool definitions that the agent can call
    4. **Build the agent** — The model generates the agent with instructions, tools, and orchestration logic
    5. **Test locally** — Run the agent and verify tool use and output
    6. **Generate the Run Guide**

=== "Multi-Agent (code-first)"

    1. **Create context** — Build context artifacts as files
    2. **Initialize SDK project** — Set up the project structure for your chosen SDK
    3. **Build specialist agents** — The model generates each specialist agent with its tools and instructions
    4. **Define handoffs** — The model generates the handoff logic between agents (what each passes to the next)
    5. **Build the orchestrator** — The model generates the coordination layer that routes work between agents
    6. **Test locally** — Run the full pipeline and verify agent coordination
    7. **Generate the Run Guide**

The Run Guide for code-first workflows includes additional setup details:

- **Dependency installation** — `pip install`, `npm install`, or equivalent for your SDK
- **Environment variable setup** — API keys, configuration values, and how to set them
- **How to run locally** — `python main.py`, `npx tsx agent.ts`, or equivalent
- **Deployment options** — Docker, cloud services, CI/CD pipelines (when applicable)

## Your Role During Construct

The model does the heavy lifting — reading your spec, researching your platform, and generating artifacts. But a few things require your direct involvement because the model can't do them on its own.

### Context — gather your business-specific materials

The model generates prompts, skills, and agents, but it can't create *your* business knowledge. You need to provide the context artifacts that make the workflow specific to your organization.

1. **Open the Context Inventory** from your AI Building Block Spec
2. **Focus on "Needs Creation" items** — these are gaps you need to fill
3. **Start with rules and criteria** — scoring rubrics, qualification criteria, and decision logic are often required for the workflow to function correctly. Without them, the model guesses instead of following your standards.
4. **Use the "Key Contents" column as your drafting checklist** — the spec already identified what each artifact should contain
5. **Create each artifact** as a standalone Markdown file or data export (e.g., `buyer-persona.md`, `scoring-rubric.md`)
6. **The model will tell you what it needs and when** — if you're using the `building-workflows` skill, it prompts you for each context artifact at the right point in the build

### MCP — configure external tool connections

If your Building Block Spec lists external tools in the **Tools and Connectors Required** section, you'll need to set up those connections. Most workflows don't need this — only when live data or external actions are required.

Connecting an external tool works like connecting an app to your phone — set it up once, authorize access, then it's available whenever you need it:

1. **Get access credentials** — Most tools require an API key. Create this in the external tool's settings, usually under "Integrations" or "Developer."
2. **Add the connection to your AI tool** — Tell your AI tool where to find the external service and how to authenticate.
3. **Test it** — Ask the AI to do something simple with the connected tool to verify the connection works.

How different platforms handle external connections:

| Platform | What it's called | How to set it up |
|----------|-----------------|-----------------|
| **Claude Code / Desktop** | MCP servers | Add server configuration to your project's settings file |
| **ChatGPT** | Actions (in Custom GPTs) | Define the external API endpoint and authentication in the GPT builder |
| **Gemini** | Extensions | Enable built-in extensions in settings, or connect custom services via the API |
| **M365 Copilot** | Connectors + Power Platform | Configure in Copilot Studio or through the Microsoft 365 admin center |

### Agents — build on your platform

When the model generates agent blueprints (for Single Agent and Multi-Agent patterns), how you operationalize them depends on your platform. Agent platforms fall into two categories:

**Builder/GUI platforms** — You take the agent details from your AI Building Block Spec (name, instructions, tools, model) and manually configure them through the platform's visual interface. This is point-and-click — paste the instructions, select the tools, and configure settings.

**Code-based platforms** — Your AI Building Block Spec gives you the *what* (agent role, instructions, tools, goals), but you'll need to translate that into code using the platform's SDK or framework. Refer to the platform's documentation for how to operationalize the agent configuration — defining tools, setting up orchestration, and deploying.

| Platform | Approach | Agent guide |
|---|---|---|
| Claude Code | Code-based — Markdown agent files | [Building Agents on Claude](../../platforms/claude/agents/building-agents.md) |
| OpenAI (ChatGPT) | Builder — configure in ChatGPT's agent interface | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents.md) |
| OpenAI (AgentKit) | Builder — visual canvas for agent workflows | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents.md) |
| OpenAI (Agents SDK) | Code-based — Python/TypeScript SDK | [Building Agents on OpenAI](../../platforms/openai/agents/building-agents.md) |
| Google Enterprise | Builder — no-code visual interface | [Building Agents on Google](../../platforms/google-gemini/agents/building-agents.md) |
| Google (ADK) | Code-based — open-source framework | [Building Agents on Google](../../platforms/google-gemini/agents/building-agents.md) |
| M365 Copilot | Builder — configure in Copilot Studio | [Building Agents on M365 Copilot](../../platforms/m365-copilot/agents/building-agents.md) |
