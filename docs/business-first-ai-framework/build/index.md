---
title: Build Workflows
description: Turn your AI Building Block Map into a working workflow — from context and prompts through skills, agents, and MCP connections.
---

# Build Workflows

!!! info "Business-First AI Framework — Step 3: Build Workflows"
    This is **Step 3** of the [Business-First AI Framework](../index.md). You've deconstructed your workflow and mapped it to building blocks. Now build it.

## Where You Are

You've just finished [Deconstructing](../deconstruct/index.md) your workflow. You should have two files:

1. **Workflow Definition** (`[name]-definition.md`) — every step in your workflow broken down with decision points, data flows, context needs, and failure modes
2. **AI Building Block Map** (`[name]-building-blocks.md`) — each step classified by how much AI can handle, mapped to specific AI building blocks, plus a **Context Inventory** listing every document, data source, and resource the workflow needs

These two files are your blueprint. The AI Building Block Map tells you *exactly* what to build — and this page walks you through building it.

## What You'll Do Next

For most workflows, the build process is four actions. You can complete it in an afternoon.

### 1. Create your context

Open your `[name]-building-blocks.md` file and find the **Context Inventory** table. It lists every piece of information your workflow needs — documents, data, rules, examples, and reference materials. Some of these already exist (your style guide, your CRM data, your buyer persona). Others are marked "Needs Creation" — you need to create those before the workflow can produce quality output.

Start with items marked "Needs Creation." The Context Inventory's "Key Contents" column tells you what each one should contain — use it as your drafting checklist. Most context artifacts are simple Markdown files (like `scoring-rubric.md` or `buyer-persona.md`).

**[Context guide](context.md)** — what context looks like, how to create what's missing, and where to store it

### 2. Generate your prompt

This is the core action. You'll use AI to turn your `[name]-building-blocks.md` file into two new deliverables:

- A **Baseline Workflow Prompt** (`[name]-prompt.md`) — a ready-to-use prompt with numbered steps, each labeled as AI or Human. This IS your workflow. Paste it into any AI tool and it runs.
- **Skill Specs** (`[name]-skill-specs.md`) — recommendations for which steps could become reusable skills (optional — you can build these later or not at all)

Here's exactly how:

1. Go to the **[Prompt](prompt.md)** page
2. **Copy the prompt** from the code block on that page
3. **Open a new conversation** in any AI tool — Claude, ChatGPT, Gemini, or M365 Copilot
4. **Paste the prompt** you copied and press Enter
5. The AI will ask you for your AI Building Block Map — **upload or paste your `[name]-building-blocks.md` file**
6. The AI reads your file, may ask 1-2 clarifying questions, then **generates both deliverables**
7. **Save both files** — download them or copy the output and save as `[name]-prompt.md` and `[name]-skill-specs.md`

**[Prompt guide](prompt.md)** — the full prompt template, step-by-step instructions, and what the outputs contain

### 3. Run it on a real scenario

Now take the `[name]-prompt.md` file the AI just generated for you. This is your workflow — ready to use.

1. **Open a new conversation** in your AI tool
2. **Paste the contents of `[name]-prompt.md`** and press Enter
3. **Attach any context files** listed in the prompt's Context Requirements section (these are the artifacts from action 1)
4. **Provide the inputs** the prompt asks for — the Input Requirements section tells you exactly what's needed
5. **Review the output**

The first run is a test, not a final product. You're looking for: Did the output match what you expected? Were any steps skipped? Was the output specific to your business, or generic?

**[Run guide](run.md)** — how to choose between a normal chat and a project, and how to troubleshoot first-run issues

### 4. Iterate based on what you see

After your first run, you'll know what works and what doesn't. The most common issue is generic output — the AI didn't have enough context about your specific business. The fix is usually adding more context files (reference materials, examples of good output, or rules the AI should follow).

Use this table to figure out what to adjust:

| What went wrong | What to fix |
|---|---|
| Output is generic or off-brand | Add more **context** — examples, style guides, reference materials |
| Steps were skipped or misunderstood | Refine the **prompt** — make the instructions in `[name]-prompt.md` more explicit |
| A step needs expertise the AI doesn't have | Build a **skill** for that step — codify the expertise |
| The AI needs to make decisions you can't predict | Convert from prompt to **agent** — let the AI plan its approach |

**[Run guide > Iterating](run.md#iterating-after-the-first-run)** — detailed troubleshooting for common first-run issues

---

**That's it for most workflows.** These four actions get you from "I have these Markdown files" to "I have a working AI workflow." You now have four files:

| File | From | What it is |
|------|------|-----------|
| `[name]-definition.md` | Deconstruct | Your Workflow Definition — the raw decomposition |
| `[name]-building-blocks.md` | Deconstruct | Your AI Building Block Map — the analysis and blueprint |
| `[name]-prompt.md` | Build | Your Baseline Workflow Prompt — **paste this to run the workflow** |
| `[name]-skill-specs.md` | Build | Your Skill Specs — what to build next and in what order |

Many workflows stay at this level permanently — a prompt plus context, pasted into a chat whenever you need it. That's a feature, not a limitation.

If your workflow needs more — a persistent workspace, reusable skills, autonomous agents, or connections to external tools — keep reading.

## Going Further

### Setting up a project workspace

If you run this workflow frequently (weekly or more) and you're attaching the same context files every time, move it into a project. A project pre-loads your context so you just paste the prompt and go — no re-attaching files.

**[Projects guide](projects.md)** — when to use a project vs. a normal chat, and how to set one up

### Building skills

Your Build outputs include Skill Specs — recommendations for which workflow steps could become reusable skills. A skill codifies expertise for a specific step so the prompt can invoke it by name instead of re-explaining the process every time. You don't need to build skills right away — start with the prompt, and add skills later for steps where you want more consistent, expert-level output.

**[Skills guide](skills.md)** — when to build skills and how to turn a Skill Spec into a working skill

### Using agents

Some workflow steps need more than a script to follow — they need the AI to plan its own approach, use tools, and adapt based on what it finds. If your AI Building Block Map tags steps with "Agent," those steps are candidates for autonomous execution. Agents are the most advanced building block and are optional for most workflows.

**[Agents guide](agents.md)** — when you need an agent vs. when a prompt is enough

### Connecting to external tools with MCP

If your workflow needs to read from or write to external systems — databases, APIs, browsers, project management tools — you'll wire those connections using MCP (Model Context Protocol). MCP is the bridge between AI and your tools. Check the "Tools and Connectors Required" section of your AI Building Block Map to see if you need it.

**[MCP guide](mcp.md)** — what MCP provides and how to connect your workflow to external tools

## The Full Build Process

Here's the complete picture — all seven steps. Most workflows only need steps 1, 2, 3, and 7. Work through whichever steps your Building Block Map calls for:

| Step | What | What you'll do | When to use |
|------|------|---------------|-------------|
| 1 | [Context](context.md) | Create the context your workflow needs — documents, data, rules, and examples | Always — every workflow benefits from explicit context |
| 2 | [Projects](projects.md) | Set up a persistent workspace with pre-loaded context | When running the workflow frequently (weekly+) with 3+ context files |
| 3 | [Prompt](prompt.md) | Generate a self-contained Baseline Workflow Prompt and Skill Specs | Always — the prompt is your workflow |
| 4 | [Skills](skills.md) | Build reusable routines for steps requiring domain expertise | When your Skill Specs recommend skill candidates |
| 5 | [Agents](agents.md) | Build autonomous agents for steps that need planning and adaptive execution | When your Building Block Map tags steps with "Agent" |
| 6 | [MCP](mcp.md) | Connect AI to external tools, databases, and services | When steps require external tool access |
| 7 | [Run](run.md) | Execute the workflow — paste and run, run in a project, command an agent, or automate on a schedule | Always — this is where you test and iterate |

Each building block page cross-references the corresponding [Agentic Building Blocks](../../agentic-building-blocks/index.md) page for platform-specific implementation details.

## Worked Examples

These three examples show complete AI-powered workflows at different levels of the autonomy spectrum — from deterministic automation to collaborative workflows to fully autonomous multi-agent pipelines. Each includes working building blocks you can install and study.

| Type | AI Involvement | When to Use | Example |
|------|---------------|-------------|---------|
| [Deterministic Automation](deterministic-automation.md) | AI follows fixed rules — criteria from input, output from template | Prospecting, recurring reports, template-driven research | LinkedIn prospect research |
| [AI Collaborative](ai-collaborative.md) | AI researches and drafts; human steers and decides | Meeting prep, competitive analysis, proposal drafting | Meeting prep researcher |
| [Autonomous Agent](autonomous-agent.md) | Multiple agents execute a full pipeline; human reviews at one gate | Research-driven content, multi-step pipelines, specialist roles | HBR article pipeline |

### All Building Blocks

These are the working building blocks included across all three examples. Each one links to its source on GitHub — read the full definition, understand how it works, and adapt it for your own workflows.

| Building Block | Type | Workflow | Description | Source |
|-------|------|----------|-------------|--------|
| `linkedin-prospect-research` | Prompt | Deterministic | Finds and qualifies 5 LinkedIn prospects against a buyer persona | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/prompts/linkedin-prospect-research.md) |
| `buyer-persona-revenue-leader-rachel` | Prompt | Deterministic | Example buyer persona used as input to the research workflow | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/prompts/buyer-persona-revenue-leader-rachel.md) |
| `meeting-prep-researcher` | Agent | Collaborative | Researches attendees and companies for meeting prep | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/agents/meeting-prep-researcher.md) |
| `preparing-meeting-briefs` | Skill | Collaborative | Step-by-step research workflow for the agent | [View](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/business-first-ai/skills/preparing-meeting-briefs/) |
| `meeting-prep-quick` | Prompt | Collaborative | Portable one-shot meeting prep prompt | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/prompts/meeting-prep-quick.md) |
| `ai-productivity-researcher` | Agent | Autonomous | Finds case studies of companies using AI with quantified outcomes | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/agents/ai-productivity-researcher.md) |
| `tech-executive-writer` | Agent | Autonomous | Writes articles for business leadership audiences | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/agents/tech-executive-writer.md) |
| `hbr-editor` | Agent | Autonomous | Edits drafts against HBR editorial standards | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/agents/hbr-editor.md) |
| `editing-hbr-articles` | Skill | Autonomous | Editorial criteria and cut/replace patterns for the editor | [View](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/business-first-ai/skills/editing-hbr-articles/) |
| `hbr-publisher` | Agent | Autonomous | Formats approved articles as PDF + markdown with SEO metadata | [View](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/business-first-ai/agents/hbr-publisher.md) |

## How to Use These Examples

=== "Any AI Tool"

    Every example includes at least one **standalone prompt** — a text template you can copy and paste into Claude, ChatGPT, Gemini, M365 Copilot, or any other AI tool. Click the "View" links in the table above to read the prompt source on GitHub.

    Prompts are the most portable building block type. They work everywhere, require no setup, and can be shared with anyone on your team.

=== "Claude Code"

    All building blocks — agents, skills, and prompts — are bundled in the `business-first-ai` plugin. Install it once and the agents activate automatically when you describe a matching task.

    ```bash
    # Add the Hands-on AI marketplace (one time)
    /plugin marketplace add jamesgray-ai/handsonai

    # Install the business-first-ai plugin
    /plugin install business-first-ai@handsonai
    ```

    Then describe what you need in natural language:

    - *"Run the LinkedIn prospect research workflow using the Revenue Leader Rachel persona"* — executes the deterministic prospecting workflow
    - *"Prepare me for my meeting with Sarah Chen at Acme Corp"* — activates the meeting prep researcher agent
    - *"Write an HBR-style article about companies successfully using AI agents"* — triggers the full multi-agent research → write → edit → publish pipeline

## Related

- [AI Use Cases](../../use-cases/index.md) — browse use cases by type (content creation, research, coding, data analysis, ideation, automation)
- [Discover AI Workflow Opportunities](../discover.md) — discover which of your workflows are candidates for AI
- [Deconstruct Workflows](../deconstruct/index.md) — break down workflows into automatable steps
- [Plugin Marketplace](../../plugins/index.md) — browse all available plugins
