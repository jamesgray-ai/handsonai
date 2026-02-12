---
title: "Step 3: Build Workflows"
description: Design your AI workflow, construct it with the right building blocks, and run it — from execution pattern selection through prompts, skills, agents, and MCP connections.
---

# Step 3: Build Workflows

## Where You Are

You've just finished [Deconstructing](../deconstruct/index.md) your workflow. You should have:

- **Workflow Definition** (`[name]-definition.md`) — every step in your workflow broken down with decision points, data flows, context needs, and failure modes

This file is your input. Build has three parts: **Design** your AI implementation, **Construct** the components, and **Run** the workflow.

## 3.1: Design

Before building anything, decide *how* the workflow should be built. The Design phase takes your Workflow Definition and produces an **AI Building Block Spec** — a complete blueprint that tells you exactly what to build.

Design covers:

1. **Execution pattern** — Choose from four patterns based on what your workflow needs:

    | Pattern | When to use |
    |---------|-------------|
    | **Prompt** | Sequential steps, human drives the process and provides all inputs |
    | **Skill-Powered Prompt** | Steps with repeatable sub-routines or moderate complexity |
    | **Single Agent** | Tool use required, autonomous decisions, multi-step reasoning |
    | **Multi-Agent** | Multiple expertise domains, parallel execution, review gates |

2. **Autonomy classification** — Classify each step (Human → Deterministic → Semi-Autonomous → Autonomous)
3. **Building block mapping** — Map each step to AI building blocks (Prompt, Context, Skill, Agent, MCP, Project)
4. **Skill candidates** — Tag steps that should become reusable skills, with generation-ready detail
5. **Agent configuration** (when applicable) — Platform-agnostic blueprint for each agent (name, description, instructions, model, tools, context, goal)

**[Design Your AI Workflow](design.md)** — the full Design guide with prompt template, execution pattern decision flow, and output format

**Produces:** `[name]-building-block-spec.md` — your AI Building Block Spec with execution pattern, step classifications, skill candidates, agent configurations (when applicable), and implementation order.

## 3.2: Construct

The AI Building Block Spec tells you exactly what to build — and the execution pattern determines which steps you follow. Work through **only** the steps that apply to your pattern:

=== "Prompt"

    1. **[Create context](context.md)** — Build the context artifacts listed in your Building Block Spec's Context Inventory
    2. **[Set up project workspace](projects.md)** (optional) — If the Building Block Spec's Where to Run recommends a project
    3. **[Generate prompt](prompt.md)** — Paste the prompt template with your Building Block Spec to generate the Baseline Workflow Prompt
    4. **[Run](run.md)** → 3.3

=== "Skill-Powered Prompt"

    1. **[Create context](context.md)** — Build the context artifacts listed in your Building Block Spec's Context Inventory
    2. **[Set up project workspace](projects.md)** (optional) — If the Building Block Spec's Where to Run recommends a project
    3. **[Build skills](skills.md)** — Build skills for the steps tagged as skill candidates in your Building Block Spec. On Claude, auto-generate `SKILL.md` files from the Design output. On other platforms, create custom instructions, GPTs, or Gems using the skill candidate specs.
    4. **[Generate prompt](prompt.md)** — Generate a prompt that references your skills instead of spelling out those steps
    5. **[Run](run.md)** → 3.3

=== "Single Agent"

    1. **[Create context](context.md)** — Build the context artifacts listed in your Building Block Spec's Context Inventory
    2. **[Build skills](skills.md)** — Build skills for tagged candidates
    3. **[Connect MCP](mcp.md)** — Wire external tools from the Tools and Connectors section of your Building Block Spec
    4. **[Build agent](agents.md)** — On Claude, auto-generate the agent `.md` file from the Design phase's agent configuration. On other platforms, configure the agent using the blueprint.
    5. **[Run](run.md)** → 3.3

=== "Multi-Agent"

    1. **[Create context](context.md)** — Build the context artifacts listed in your Building Block Spec's Context Inventory
    2. **[Build skills](skills.md)** — Build skills for tagged candidates
    3. **[Connect MCP](mcp.md)** — Wire external tools from the Tools and Connectors section of your Building Block Spec
    4. **[Build specialist agents](agents.md)** — On Claude, auto-generate agent `.md` files from the Design phase's agent configurations. On other platforms, configure each agent using the blueprint.
    5. **Build orchestrator** — On Claude, auto-generate an orchestrator agent that coordinates the pipeline. On other platforms, configure the orchestration layer.
    6. **[Run](run.md)** → 3.3

Each guide page covers one building block in depth. You only visit the pages your pattern requires — no "skip if not needed."

## 3.3: Run

Take your constructed workflow and run it on a real scenario.

1. **Open a new conversation** in your AI tool (or open your project workspace)
2. **Paste the contents of `[name]-prompt.md`** and press Enter (or invoke the agent for agent-based patterns)
3. **Attach any context files** listed in the prompt's Context Requirements section
4. **Provide the inputs** the prompt asks for
5. **Review the output**

**The first run is a test, not a final product.** Expect to run, evaluate, go back to 3.2 Construct to adjust, and run again. This cycle is normal — most workflows need 2-4 iterations before they produce reliably good output.

You're evaluating: Did the output match what you expected? Were any steps skipped? Was the output specific to your business, or generic?

**[Run guide](run.md)** — how to choose between a normal chat and a project, and how to troubleshoot first-run issues

### Test, iterate, repeat

Each time you run, you're testing. When something is off, go back to 3.2 Construct, adjust the relevant building block, and run again:

| What went wrong | Go back to 3.2 and... |
|---|---|
| Output is generic or off-brand | Add more **context** — examples, style guides, reference materials |
| Steps were skipped or misunderstood | Refine the **prompt** — make the instructions more explicit |
| A step needs expertise the AI doesn't have | Build a **skill** for that step — codify the expertise |
| The AI needs to make decisions you can't predict | Convert from prompt to **agent** — let the AI plan its approach |

The workflow is ready when you can run it on a new scenario and trust the output without heavy editing. Until then, keep iterating.

**[Run guide > Iterating](run.md#test-iterate-repeat)** — detailed troubleshooting for common first-run issues

---

**Your deliverables across Build:**

| File | From | What it is |
|------|------|-----------|
| `[name]-definition.md` | Deconstruct | Your Workflow Definition — the raw decomposition |
| `[name]-building-block-spec.md` | Build: 3.1 Design | Your AI Building Block Spec — execution pattern, classifications, skill candidates, agent configs |
| `[name]-prompt.md` | Build: 3.2 Construct | Your Baseline Workflow Prompt — **paste this to run the workflow** |

These three files are your core deliverables on any platform. On the **Claude platform**, the Construct step can also auto-generate:

| File | When | What it is |
|------|------|-----------|
| `.claude/skills/[skill]/SKILL.md` | Skill-Powered Prompt, Single Agent, Multi-Agent | Reusable skill definitions — one per skill candidate tagged in the AI Building Block Spec |
| `.claude/agents/[agent].md` | Single Agent, Multi-Agent | Agent configurations — auto-generated from the Design blueprint |

Plus any context artifacts and MCP connections you set up along the way.

Many workflows stay at the prompt-plus-context level permanently — pasted into a chat whenever you need it. That's a feature, not a limitation.

## Track and Version Your Work

As you build, two background practices keep your work organized and recoverable:

**Register building blocks in your AI Registry.** Each time you create a skill, prompt, or agent, register it in your [AI Registry](../../plugins/ai-registry.md) Notion database — name, type, description, and which workflow it belongs to. If you registered the workflow during Deconstruct, these building blocks link back to it. This gives you a searchable inventory of everything you've built, and makes it easy for your team to discover and reuse building blocks across workflows.

**Commit source files to GitHub.** The `.md` files for your skills, agents, and prompts are source code — they should live in version control, not just on your local machine. After creating or updating a building block, commit it to your GitHub repository. This gives you a history of changes, makes it easy to share with collaborators, and protects against losing work.

These aren't separate steps — they're part of the rhythm of building. Each time you finish a building block in 3.2 Construct: **test it, register it, commit it.**

!!! tip "Need to set up these tools?"
    The [Builder Stack Setup](../../builder-setup/index.md) guide walks you through everything you need — an AI code editor ([Step 2](../../builder-setup/editor-setup.md)), Git ([Step 3](../../builder-setup/git-install.md)), GitHub ([Step 4](../../builder-setup/github-setup.md)), and the AI Registry ([Step 6](../../builder-setup/notion-registry-setup.md)). If you haven't set these up yet, that guide has you covered.

## Quick Reference

| | Guide | When to use |
|-------|-------|-------------|
| 3.1 | [Design Your AI Workflow](design.md) | Always — produces your AI Building Block Spec |
| 3.2 | [Context](context.md) | Always |
| 3.2 | [Projects](projects.md) | When Where to Run recommends a project workspace |
| 3.2 | [Skills](skills.md) | When Building Block Spec tags steps as skill candidates |
| 3.2 | [Prompt](prompt.md) | For Prompt and Skill-Powered Prompt patterns |
| 3.2 | [Agents](agents.md) | For Single Agent and Multi-Agent patterns |
| 3.2 | [MCP](mcp.md) | When Building Block Spec lists external tools or connectors |
| 3.3 | [Run](run.md) | Always |

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
- [Deconstruct Workflows](../deconstruct/index.md) — break down workflows into structured definitions
- [Plugin Marketplace](../../plugins/index.md) — browse all available plugins
