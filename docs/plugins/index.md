---
title: Plugin Marketplace
description: Pre-built Claude Code plugins with agents and skills you can install in one command
---

# Plugin Marketplace

## Why Plugins?

Out of the box, Claude is a generalist. It can write, research, and analyze — but it doesn't know your standards, your workflows, or your preferred formats. Every time you start a new conversation, you'd need to re-explain how you want things done.

**Plugins solve this.** Each plugin packages domain expertise — writing standards, naming conventions, research processes, editorial criteria — into a format Claude can use automatically. Install a plugin once and Claude gains that expertise across every session.

A plugin can bundle several types of components:

- **Agents** — Expert personalities that Claude activates automatically. Ask for a LinkedIn post and Claude brings in a writing specialist. Ask for an AI news briefing and a research specialist takes over.
- **Skills** — Step-by-step workflows that teach Claude specific tasks. A skill might encode your editorial standards, your workflow naming conventions, or your documentation templates.
- **Commands** — Slash commands that trigger specific actions (like `/commit` for git workflows).
- **Hooks** — Automations that run in response to events (e.g., running a linter after every file edit).
- **MCP servers** — Connections to external tools and services (e.g., Notion, GitHub, Slack).

The plugins in this marketplace currently focus on **agents** and **skills**. For the full plugin format, see the official [Plugin structure overview](https://code.claude.com/docs/en/plugins#plugin-structure-overview).

**The result:** Instead of writing long prompts to explain what you want, you describe your goal in plain language and Claude applies the right expertise automatically.

New to plugins? Start with the [Getting Started guide](getting-started.md) for a step-by-step walkthrough, or browse the available plugins below.

## Add This Marketplace

In your Claude Code session, type this once to register the Hands-on AI marketplace:

```bash
/plugin marketplace add jamesgray-ai/handsonai
```

Then install any plugin below with a single command. All `/plugin` commands are typed inside Claude Code, not in a regular terminal.

For the full details on how marketplaces and plugin installation work, see the official [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins) documentation.

---

## :material-rocket-launch: Business First AI

The [Business-First AI Framework](../business-first-ai-framework.md) as executable Claude Code skills. Discover AI workflow opportunities (Phase 1), deconstruct workflows into AI building blocks (Phase 2), and build with worked examples across the autonomy spectrum (Phase 3).

```bash
/plugin install business-first-ai@handsonai
```

???+ agents "Agents included (8)"

    | Agent | Phase | What it does |
    |-------|-------|-------------|
    | [`workflow-deconstructor`](business-first-ai.md#workflow-deconstructor) | 2 | Orchestrates the full three-step workflow deconstruction process. Runs discovery, analysis, and output generation sequentially with file-based handoffs between stages. |
    | [`tech-executive-writer`](business-first-ai.md#tech-executive-writer) | 3 | Writes business-focused content about AI and technology. LinkedIn posts, magazine articles, executive briefs, and thought leadership pieces. |
    | [`hbr-editor`](business-first-ai.md#hbr-editor) | 3 | Reviews drafts against HBR editorial standards. Provides prescriptive feedback on structure, evidence quality, voice, and argument strength. |
    | [`hbr-publisher`](business-first-ai.md#hbr-publisher) | 3 | Formats finalized articles for web publication and PDF distribution. Handles SEO metadata, social snippets, and professional layout. |
    | [`ai-productivity-researcher`](business-first-ai.md#ai-productivity-researcher) | 3 | Finds documented case studies of companies using AI for productivity gains. Prioritizes HBR-caliber sources with quantified outcomes. |
    | [`meeting-prep-researcher`](business-first-ai.md#meeting-prep-researcher) | 3 | Researches meeting attendees and companies, then produces a structured prep brief with profiles, talking points, and suggested questions. |
    | [`ai-news-researcher`](business-first-ai.md#ai-news-researcher) | Utility | Scans news outlets, blogs, YouTube channels, podcasts, and communities for the latest AI developments. |
    | [`claude-research-daily`](business-first-ai.md#claude-research-daily) | Utility | Produces a daily brief on Anthropic, Claude, Claude Code, and Cowork from the last 24 hours. |

???+ skills "Skills included (6)"

    | Skill | Phase | What it does |
    |-------|-------|-------------|
    | [`finding-ai-opportunities`](business-first-ai.md#finding-ai-opportunities) | 1 | Structured audit of your workflows to discover where AI can help. Produces a categorized opportunity report. |
    | [`discovering-workflows`](business-first-ai.md#discovering-workflows) | 2 | Interactively discovers and decomposes a business workflow into a structured Workflow Blueprint. |
    | [`analyzing-workflows`](business-first-ai.md#analyzing-workflows) | 2 | Classifies workflow steps on the autonomy spectrum, maps them to AI building blocks, and produces a Workflow Analysis Document. |
    | [`generating-workflow-outputs`](business-first-ai.md#generating-workflow-outputs) | 2 | Generates a ready-to-use Baseline Workflow Prompt and Skill Build Recommendations from a Workflow Analysis Document. |
    | [`editing-hbr-articles`](business-first-ai.md#editing-hbr-articles) | 3 | HBR editorial criteria for article editing. Used by the `hbr-editor` agent. |
    | [`preparing-meeting-briefs`](business-first-ai.md#preparing-meeting-briefs) | 3 | Structured research workflow for meeting preparation. Used by the `meeting-prep-researcher` agent. |

???+ prompts "Prompts included (3)"

    | Prompt | What it does |
    |--------|-------------|
    | [`linkedin-prospect-research`](business-first-ai.md#linkedin-prospect-research) | Deterministic prospecting prompt — finds and qualifies LinkedIn prospects against a buyer persona. |
    | [`buyer-persona-revenue-leader-rachel`](business-first-ai.md#buyer-persona-revenue-leader-rachel) | Example buyer persona used as input to the prospect research workflow. |
    | [`meeting-prep-quick`](business-first-ai.md#meeting-prep-quick) | Portable one-shot meeting prep prompt for any AI tool. |

???+ usage "Example usage"

    ```
    "Help me find where AI can improve my workflows"
    → finding-ai-opportunities runs a structured audit and produces an opportunity report

    "I want to deconstruct my client onboarding workflow"
    → workflow-deconstructor walks you through the full deconstruction process

    "Write a LinkedIn post about how RAG is transforming enterprise search"
    → tech-executive-writer drafts the article

    "Review this article for HBR quality"
    → hbr-editor provides structured editorial feedback

    "I have a meeting with Sarah Chen from Acme Corp tomorrow. Help me prepare."
    → meeting-prep-researcher researches the attendee and company, produces a prep brief

    "What's new in AI today?"
    → ai-news-researcher scans sources and produces a categorized briefing
    ```

---

## :material-clipboard-text-outline: AI Registry

Document, name, register, and sync AI operational workflows and skills.

!!! note
    This plugin requires a Notion account and the [Notion MCP connector](../fundamentals/developer-setup/notion-registry-setup.md). Without it, Claude can follow the naming and writing conventions but cannot save entries to Notion.

```bash
/plugin install ai-registry@handsonai
```

??? skills "Skills included"

    | Skill | What it does |
    |-------|-------------|
    | [`naming-workflows`](ai-registry.md#naming-workflows) | Generates consistent, outcome-focused names and descriptions for business workflows. Follows domain-specific naming patterns (Sales, Marketing, Product, etc.) and creates entries in the Notion Workflows database. |
    | [`writing-workflow-sops`](ai-registry.md#writing-workflow-sops) | Writes Standard Operating Procedure documentation for workflows. Adapts SOP templates for Manual, Augmented, and Automated workflow types. Saves SOPs to Notion workflow page bodies. |
    | [`writing-process-guides`](ai-registry.md#writing-process-guides) | Writes Business Process Guide documentation explaining when, why, and how to execute a complete business process with its component workflows. Covers strategic context while linking to individual SOPs for tactical details. |
    | [`registering-skills`](ai-registry.md#registering-skills) | Registers or updates Claude Skills in the Notion AI Assets database. Extracts metadata from SKILL.md frontmatter, generates Quick Start Prompts, and handles duplicate detection. |
    | [`syncing-skills-to-github`](ai-registry.md#syncing-skills-to-github) | Syncs skills from `~/.claude/skills/` to a GitHub repository. Detects changes, generates semantic commit messages, pushes to remote, and updates Notion AI Assets with GitHub URLs. |

??? workflow "Recommended workflow"

    1. **Name** — Use `naming-workflows` to create a consistent workflow entry in Notion
    2. **Document** — Use `writing-workflow-sops` to write the SOP for each workflow
    3. **Connect** — Use `writing-process-guides` to document how workflows fit together in a business process
    4. **Register** — Use `registering-skills` to track skills in Notion AI Assets
    5. **Sync** — Use `syncing-skills-to-github` to version-control everything in GitHub

    ```
    "Name a workflow for drafting email responses"
    → naming-workflows generates options and creates a Notion entry

    "Write an SOP for the Email Response Drafting workflow"
    → writing-workflow-sops produces a complete SOP in Notion

    "Write a process guide for the Email Management business process"
    → writing-process-guides documents the end-to-end process

    "Register the email-response-drafting skill in Notion"
    → registering-skills adds it to the AI Assets database

    "Sync all changed skills to GitHub"
    → syncing-skills-to-github commits and pushes with Notion tracking
    ```

---

## Quick Reference

| Plugin | Agents | Skills | Prompts | Install command |
|--------|--------|--------|---------|----------------|
| `business-first-ai` | 8 | 6 | 3 | `/plugin install business-first-ai@handsonai` |
| `ai-registry` | 0 | 5 | 0 | `/plugin install ai-registry@handsonai` |

All plugins are maintained in the [handsonai GitHub repository](https://github.com/jamesgray-ai/handsonai).
