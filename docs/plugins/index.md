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

## :material-clipboard-check: Course Examples

Working examples of agents and skills from the Hands-on AI cohort courses.

```bash
/plugin install course-examples@handsonai
```

???+ agents "Agents included"

    | Agent | What it does |
    |-------|-------------|
    | [`tech-executive-writer`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/tech-executive-writer.md) | Writes business-focused content about AI and technology. LinkedIn posts, magazine articles, executive briefs, and thought leadership pieces. Translates complex technical concepts for non-technical audiences. |
    | [`hbr-editor`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/hbr-editor.md) | Reviews drafts against HBR editorial standards. Provides prescriptive feedback on structure, evidence quality, voice, and argument strength. |
    | [`hbr-publisher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/hbr-publisher.md) | Formats finalized articles for web publication and PDF distribution. Handles SEO metadata, social snippets, and professional layout. |
    | [`ai-news-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/ai-news-researcher.md) | Scans news outlets, blogs, YouTube channels, podcasts, and communities for the latest AI developments. Categorizes findings by product releases, research, company updates, and community highlights. |
    | [`ai-productivity-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/ai-productivity-researcher.md) | Finds documented case studies of companies using AI for productivity gains. Prioritizes HBR-caliber sources with quantified outcomes. Outputs structured case study briefs. |
    | [`claude-research-daily`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/claude-research-daily.md) | Produces a daily brief on Anthropic, Claude, Claude Code, and Cowork. Covers official announcements, tech news, video content, tutorials, and community discussions from the last 24 hours. |
    | [`meeting-prep-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/meeting-prep-researcher.md) | Researches meeting attendees and companies, then produces a structured prep brief with profiles, talking points, and suggested questions. |

???+ skills "Skills included"

    | Skill | What it does |
    |-------|-------------|
    | [`editing-hbr-articles`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/course-examples/skills/editing-hbr-articles/) | Loads HBR editorial criteria for article editing. Used by the `hbr-editor` agent to apply specific standards for openings, evidence, voice, and length. Includes a reference file with cut/replace patterns and source quality hierarchy. |
    | [`meeting-prep-research`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/course-examples/skills/meeting-prep-research/) | Step-by-step research workflow for meeting preparation. Guides the meeting-prep-researcher agent through attendee research, company analysis, and prep brief generation. |

???+ usage "Example usage"

    ```
    "Write a LinkedIn post about how RAG is transforming enterprise search"
    → tech-executive-writer drafts the article

    "Review this article for HBR quality"
    → hbr-editor provides structured editorial feedback

    "Prepare the article for publication"
    → hbr-publisher formats for web + PDF

    "What's new in AI today?"
    → ai-news-researcher scans sources and produces a categorized briefing

    "Find case studies of companies using AI agents for customer support"
    → ai-productivity-researcher gathers quantified examples from tier-1 sources

    "What's the latest news about Claude?"
    → claude-research-daily produces a 24-hour brief on all things Claude

    "I have a meeting with Sarah Chen from Acme Corp tomorrow. Help me prepare."
    → meeting-prep-researcher researches the attendee and company, produces a prep brief
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
    | [`naming-workflows`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-registry/skills/naming-workflows/) | Generates consistent, outcome-focused names and descriptions for business workflows. Follows domain-specific naming patterns (Sales, Marketing, Product, etc.) and creates entries in the Notion Workflows database. |
    | [`writing-workflow-sops`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-registry/skills/writing-workflow-sops/) | Writes Standard Operating Procedure documentation for workflows. Adapts SOP templates for Manual, Augmented, and Automated workflow types. Saves SOPs to Notion workflow page bodies. |
    | [`writing-process-guides`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-registry/skills/writing-process-guides/) | Writes Business Process Guide documentation explaining when, why, and how to execute a complete business process with its component workflows. Covers strategic context while linking to individual SOPs for tactical details. |
    | [`registering-skills`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-registry/skills/registering-skills/) | Registers or updates Claude Skills in the Notion AI Assets database. Extracts metadata from SKILL.md frontmatter, generates Quick Start Prompts, and handles duplicate detection. |
    | [`syncing-skills-to-github`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-registry/skills/syncing-skills-to-github/) | Syncs skills from `~/.claude/skills/` to a GitHub repository. Detects changes, generates semantic commit messages, pushes to remote, and updates Notion AI Assets with GitHub URLs. |

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

## :material-sitemap: Workflow Deconstruction

Deconstruct business workflows into AI building blocks. Includes an orchestrator agent and a three-skill chain that walks you through discovery, analysis, and output generation — producing a Workflow Blueprint, Analysis Document, Baseline Prompt, and Skill Recommendations.

```bash
/plugin install workflow-deconstruction@handsonai
```

???+ agents "Agents included"

    | Agent | What it does |
    |-------|-------------|
    | [`workflow-deconstructor`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/workflow-deconstruction/agents/workflow-deconstructor.md) | Orchestrates the full three-step workflow deconstruction process. Runs discovery, analysis, and output generation sequentially with file-based handoffs between stages. |

???+ skills "Skills included"

    | Skill | What it does |
    |-------|-------------|
    | [`workflow-discovery`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/workflow-deconstruction/skills/workflow-discovery/) | Interactively discovers and decomposes a business workflow into a structured Workflow Blueprint using the 4-question framework + failure modes. |
    | [`workflow-analysis`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/workflow-deconstruction/skills/workflow-analysis/) | Classifies workflow steps on the autonomy spectrum, maps them to AI building blocks, and produces a Workflow Analysis Document. |
    | [`workflow-output-generation`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/workflow-deconstruction/skills/workflow-output-generation/) | Generates a ready-to-use Baseline Workflow Prompt and Skill Build Recommendations from a Workflow Analysis Document. |

???+ usage "Example usage"

    ```
    "I want to deconstruct my client onboarding workflow"
    → workflow-deconstructor walks you through the full process

    "Help me figure out which parts of my reporting process could be automated with AI"
    → workflow-deconstructor decomposes the process and maps AI building blocks

    "People keep dropping off during enrollment. Help me build a workflow for that."
    → workflow-deconstructor designs a workflow from the problem and produces deliverables
    ```

    You can also invoke skills individually if you prefer to work step-by-step across separate conversations:

    ```
    "Use workflow-discovery to break down my expense reporting process"
    → Produces outputs/expense-reporting-blueprint.md

    "Use workflow-analysis on my blueprint"
    → Reads the blueprint, produces outputs/expense-reporting-analysis.md

    "Use workflow-output-generation on my analysis"
    → Produces the baseline prompt and skill recommendations
    ```

---

## Quick Reference

| Plugin | Agents | Skills | Install command |
|--------|--------|--------|----------------|
| `course-examples` | 7 | 2 | `/plugin install course-examples@handsonai` |
| `ai-registry` | 0 | 5 | `/plugin install ai-registry@handsonai` |
| `workflow-deconstruction` | 1 | 3 | `/plugin install workflow-deconstruction@handsonai` |

All plugins are maintained in the [handsonai GitHub repository](https://github.com/jamesgray-ai/handsonai).
