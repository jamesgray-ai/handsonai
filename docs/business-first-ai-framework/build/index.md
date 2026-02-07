---
title: Build Workflows
description: Three worked examples showing the spectrum of AI involvement in workflows — from deterministic automation to fully autonomous agents.
---

# Build Workflows

!!! info "Business-First AI Framework — Phase 3: Build"
    These examples are **Phase 3** of the [Business-First AI Framework](../index.md) — building AI workflows from your deconstruction outputs. More build guides are coming — this section will grow with content on building prompts, skills, agents, and multi-agent workflows.

Not all AI workflows are created equal. The right level of AI involvement depends on the task — some workflows need rigid, repeatable automation; others need AI that can research, reason, and iterate with a human; and some work best when an agent handles everything end-to-end.

These three examples show the spectrum in practice. Each includes a real-world scenario, working building blocks you can install and use, and guidance on when to apply the pattern to your own work.

## What This Is

Worked examples showing complete AI-powered workflows at three levels of the autonomy spectrum — deterministic automation, AI collaborative, and autonomous agent.

| | |
|---|---|
| **What you'll find** | Three fully built workflow examples, each showing the complete set of building blocks (prompts, context, skills, agents, MCP connectors) that make it work |
| **What you'll do** | Study these examples to understand how the building blocks from Phase 2 come together, then use them as templates for building your own workflows |
| **Time** | Self-paced reference (no guided conversation) |

## Why This Matters

Most people start using AI the same way: paste something into a chat, get a response, use it or don't. That works for simple tasks, but it misses the bigger picture. AI can operate at different levels of autonomy, and matching the right level to the right task is what separates "I use ChatGPT sometimes" from "AI is integrated into how I work."

Understanding the spectrum helps you:

- **Avoid over-engineering** — not every task needs an autonomous agent
- **Avoid under-utilizing** — some tasks deserve more than a copy-paste prompt
- **Build incrementally** — start with deterministic automation, graduate to collaborative, then autonomous as you gain confidence

## The Spectrum

| Type | AI Involvement | When to Use | Example |
|------|---------------|-------------|---------|
| [Deterministic Automation](./deterministic-automation.md) | AI follows fixed rules — criteria from input, output from template | Prospecting, recurring reports, template-driven research | LinkedIn prospect research |
| [AI Collaborative](./ai-collaborative.md) | AI researches and drafts; human steers and decides | Meeting prep, competitive analysis, proposal drafting | Meeting prep researcher |
| [Autonomous Agent](./autonomous-agent.md) | Multiple agents execute a full pipeline; human reviews at one gate | Research-driven content, multi-step pipelines, specialist roles | HBR article pipeline |

## All Building Blocks

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
