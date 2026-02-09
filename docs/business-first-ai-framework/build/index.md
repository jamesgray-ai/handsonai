---
title: Build Workflows
description: Turn your AI Building Block Map into a working workflow — from context and skills through prompts, agents, and MCP connections.
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

The build process has seven steps. Your AI Building Block Map tells you which ones your workflow needs — work through each step that applies.

### 1. Create your context

Open your `[name]-building-blocks.md` file and find the **Context Inventory** table. It lists every piece of information your workflow needs — documents, data, rules, examples, and reference materials. Some of these already exist (your style guide, your CRM data, your buyer persona). Others are marked "Needs Creation" — you need to create those before the workflow can produce quality output.

Start with items marked "Needs Creation." The Context Inventory's "Key Contents" column tells you what each one should contain — use it as your drafting checklist. Most context artifacts are simple Markdown files (like `scoring-rubric.md` or `buyer-persona.md`).

**[Context guide](context.md)** — what context looks like, how to create what's missing, and where to store it

### 2. Set up a project workspace (if running frequently)

If your AI Building Block Map's Where to Run recommends a project workspace — typically when you run the workflow weekly or more and have 3+ context files — set one up now. A project pre-loads your context so you just paste the prompt and go, no re-attaching files every time.

Skip this step if the Where to Run recommends normal chat, or if you're not sure yet — you can always move to a project later.

**[Projects guide](projects.md)** — when to use a project vs. a normal chat, and how to set one up

### 3. Build your skills (recommended)

Your AI Building Block Map already identifies which steps should become reusable skills — and it contains everything you need to build them. The decomposition table has each step's purpose, inputs, outputs, decision logic, and failure modes — that's all the raw material a skill needs. You'll paste the Building Block Map into any AI tool that supports agent skills and ask it to build a skill for each candidate step.

Each skill you build makes the prompt you'll generate in the next step shorter and smarter — the prompt invokes your skills by name instead of spelling out every instruction.

Skip this step if your platform doesn't support agent skills or you want to start with a standalone prompt — the Prompt step generates the full baseline with every step spelled out.

**[Skills guide](skills.md)** — step-by-step instructions for identifying skill candidates, building them from your existing artifacts, and integrating them with your prompt

### 4. Generate your prompt

Paste the prompt template (from the Prompt page) into any AI tool along with your AI Building Block Map. If you built skills, list them when the AI asks — it generates a prompt that references your skills instead of spelling out those steps. If you didn't build skills, the AI generates the full baseline with every step spelled out. Save as `[name]-prompt.md`.

**[Prompt guide](prompt.md)** — the full prompt template, step-by-step instructions, and what the output contains

### 5. Build agents (if your Building Block Map calls for them)

Check your AI Building Block Map for steps tagged with "Agent" in the AI Building Blocks column. These are steps where the AI needs to plan its own approach, use tools, and adapt based on what it finds — more than a prompt can handle. If you have agent steps, build them now.

Skip this step if no steps are tagged with "Agent" in your Building Block Map.

**[Agents guide](agents.md)** — when you need an agent vs. when a prompt is enough

### 6. Connect external tools with MCP (if your workflow needs them)

Check the **Tools and Connectors Required** section of your AI Building Block Map. If your workflow needs to read from or write to external systems — databases, APIs, browsers, project management tools — you'll wire those connections using MCP (Model Context Protocol). Set up the MCP connections now so they're available when you run the workflow.

Skip this step if your Building Block Map doesn't list any external tools or connectors.

**[MCP guide](mcp.md)** — what MCP provides and how to connect your workflow to external tools

### 7. Run it on a real scenario

Now take the `[name]-prompt.md` file the AI generated for you. This is your workflow — ready to use.

1. **Open a new conversation** in your AI tool (or open your project workspace if you set one up in step 2)
2. **Paste the contents of `[name]-prompt.md`** and press Enter
3. **Attach any context files** listed in the prompt's Context Requirements section (these are the artifacts from step 1 — already pre-loaded if you're using a project)
4. **Provide the inputs** the prompt asks for — the Input Requirements section tells you exactly what's needed
5. **Review the output**

The first run is a test, not a final product. You're looking for: Did the output match what you expected? Were any steps skipped? Was the output specific to your business, or generic?

**[Run guide](run.md)** — how to choose between a normal chat and a project, and how to troubleshoot first-run issues

### After the first run: iterate

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

**You now have three core files:**

| File | From | What it is |
|------|------|-----------|
| `[name]-definition.md` | Deconstruct | Your Workflow Definition — the raw decomposition |
| `[name]-building-blocks.md` | Deconstruct | Your AI Building Block Map — the analysis and blueprint |
| `[name]-prompt.md` | Build | Your Baseline Workflow Prompt — **paste this to run the workflow** |

Plus any skills, agents, MCP connections, and context artifacts you built along the way.

Many workflows stay at the prompt-plus-context level permanently — pasted into a chat whenever you need it. That's a feature, not a limitation.

## Quick Reference

| Step | Guide | When to use |
|------|-------|-------------|
| 1 | [Context](context.md) | Always |
| 2 | [Projects](projects.md) | When Where to Run recommends a project workspace |
| 3 | [Skills](skills.md) | Recommended — when Building Block Map tags steps with "Skill" |
| 4 | [Prompt](prompt.md) | Always |
| 5 | [Agents](agents.md) | When Building Block Map tags steps with "Agent" |
| 6 | [MCP](mcp.md) | When Building Block Map lists external tools or connectors |
| 7 | [Run](run.md) | Always |

Each building block guide cross-references the corresponding [Agentic Building Blocks](../../agentic-building-blocks/index.md) page for platform-specific implementation details.

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
