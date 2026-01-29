---
title: Plugin Marketplace
description: Pre-built Claude Code plugins with agents and skills you can install in one command
---

# Plugin Marketplace

Pre-built Claude Code agents and skills, bundled by theme. Install a plugin and get a complete toolkit for that workflow.

## Add This Marketplace

Run this once to register the Hands-on AI marketplace with your Claude Code installation:

```bash
/plugin marketplace add jamesgray-ai/handsonai
```

Then install any plugin below with a single command.

---

## :material-clipboard-check: Course Examples

Working examples of agents and skills from the Hands-on AI cohort courses.

```bash
/plugin install course-examples@handsonai
```

??? agents "Agents included"

    | Agent | What it does |
    |-------|-------------|
    | [`tech-executive-writer`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/tech-executive-writer.md) | Writes business-focused content about AI and technology. LinkedIn posts, magazine articles, executive briefs, and thought leadership pieces. Translates complex technical concepts for non-technical audiences. |
    | [`hbr-editor`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/hbr-editor.md) | Reviews drafts against HBR editorial standards. Provides prescriptive feedback on structure, evidence quality, voice, and argument strength. |
    | [`hbr-publisher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/hbr-publisher.md) | Formats finalized articles for web publication and PDF distribution. Handles SEO metadata, social snippets, and professional layout. |
    | [`ai-news-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/ai-news-researcher.md) | Scans news outlets, blogs, YouTube channels, podcasts, and communities for the latest AI developments. Categorizes findings by product releases, research, company updates, and community highlights. |
    | [`ai-productivity-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/ai-productivity-researcher.md) | Finds documented case studies of companies using AI for productivity gains. Prioritizes HBR-caliber sources with quantified outcomes. Outputs structured case study briefs. |
    | [`claude-research-daily`](https://github.com/jamesgray-ai/handsonai/blob/main/plugins/course-examples/agents/claude-research-daily.md) | Produces a daily brief on Anthropic, Claude, Claude Code, and Cowork. Covers official announcements, tech news, video content, tutorials, and community discussions from the last 24 hours. |

??? skills "Skills included"

    | Skill | What it does |
    |-------|-------------|
    | [`editing-hbr-articles`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/course-examples/skills/editing-hbr-articles/) | Loads HBR editorial criteria for article editing. Used by the `hbr-editor` agent to apply specific standards for openings, evidence, voice, and length. Includes a reference file with cut/replace patterns and source quality hierarchy. |

??? usage "Example usage"

    ```
    "Write a LinkedIn article about how RAG is changing enterprise search"
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
    ```

---

## :material-clipboard-text-outline: AI Operations Registry

Document, name, register, and sync AI operational workflows and skills.

```bash
/plugin install ai-operations-registry@handsonai
```

??? skills "Skills included"

    | Skill | What it does |
    |-------|-------------|
    | [`naming-workflows`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-operations-registry/skills/naming-workflows/) | Generates consistent, outcome-focused names and descriptions for business workflows. Follows domain-specific naming patterns (Sales, Marketing, Product, etc.) and creates entries in the Notion Workflows database. |
    | [`writing-workflow-sops`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-operations-registry/skills/writing-workflow-sops/) | Writes Standard Operating Procedure documentation for workflows. Adapts SOP templates for Manual, Augmented, and Automated workflow types. Saves SOPs to Notion workflow page bodies. |
    | [`writing-process-guides`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-operations-registry/skills/writing-process-guides/) | Writes Business Process Guide documentation explaining when, why, and how to execute a complete business process with its component workflows. Covers strategic context while linking to individual SOPs for tactical details. |
    | [`registering-skills`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-operations-registry/skills/registering-skills/) | Registers or updates Claude Skills in the Notion AI Assets database. Extracts metadata from SKILL.md frontmatter, generates Quick Start Prompts, and handles duplicate detection. |
    | [`syncing-skills-to-github`](https://github.com/jamesgray-ai/handsonai/tree/main/plugins/ai-operations-registry/skills/syncing-skills-to-github/) | Syncs skills from `~/.claude/skills/` to a GitHub repository. Detects changes, generates semantic commit messages, pushes to remote, and updates Notion AI Assets with GitHub URLs. |

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

| Plugin | Agents | Skills | Install command |
|--------|--------|--------|----------------|
| `course-examples` | 6 | 1 | `/plugin install course-examples@handsonai` |
| `ai-operations-registry` | 0 | 5 | `/plugin install ai-operations-registry@handsonai` |

All plugins are maintained in the [handsonai GitHub repository](https://github.com/jamesgray-ai/handsonai).
