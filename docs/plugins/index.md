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

## Available Plugins

<div class="grid cards" markdown>

-   :material-pencil-outline:{ .lg .middle } **HBR Content Suite**

    ---

    Write, edit, and publish HBR-quality business articles with a complete content pipeline

    ```bash
    /plugin install hbr-content-suite@handsonai
    ```

-   :material-newspaper-variant-outline:{ .lg .middle } **AI Research Agents**

    ---

    Stay current on AI news, productivity case studies, and Claude/Anthropic developments

    ```bash
    /plugin install ai-research-agents@handsonai
    ```

</div>

---

## HBR Content Suite

??? info "Agents included"

    | Agent | What it does |
    |-------|-------------|
    | `tech-executive-writer` | Writes business-focused content about AI and technology. LinkedIn posts, magazine articles, executive briefs, and thought leadership pieces. Translates complex technical concepts for non-technical audiences. |
    | `hbr-editor` | Reviews drafts against HBR editorial standards. Provides prescriptive feedback on structure, evidence quality, voice, and argument strength. |
    | `hbr-publisher` | Formats finalized articles for web publication and PDF distribution. Handles SEO metadata, social snippets, and professional layout. |

??? info "Skills included"

    | Skill | What it does |
    |-------|-------------|
    | `editing-hbr-articles` | Loads HBR editorial criteria for article editing. Used by the `hbr-editor` agent to apply specific standards for openings, evidence, voice, and length. Includes a reference file with cut/replace patterns and source quality hierarchy. |

??? example "Recommended workflow"

    1. **Write** — Use `tech-executive-writer` to draft your article
    2. **Edit** — Use `hbr-editor` to review against HBR standards (automatically loads the `editing-hbr-articles` skill)
    3. **Revise** — Apply the editor's prescriptive feedback
    4. **Publish** — Use `hbr-publisher` to format for web and PDF

    ```
    "Write a LinkedIn article about how RAG is changing enterprise search"
    → tech-executive-writer drafts the article

    "Review this article for HBR quality"
    → hbr-editor provides structured editorial feedback

    "Prepare the article for publication"
    → hbr-publisher formats for web + PDF
    ```

---

## AI Research Agents

??? info "Agents included"

    | Agent | What it does |
    |-------|-------------|
    | `ai-news-researcher` | Scans news outlets, blogs, YouTube channels, podcasts, and communities for the latest AI developments. Categorizes findings by product releases, research, company updates, and community highlights. |
    | `ai-productivity-researcher` | Finds documented case studies of companies using AI for productivity gains. Prioritizes HBR-caliber sources with quantified outcomes. Outputs structured case study briefs. |
    | `claude-research-daily` | Produces a daily brief on Anthropic, Claude, Claude Code, and Cowork. Covers official announcements, tech news, video content, tutorials, and community discussions from the last 24 hours. |

??? example "Example usage"

    ```
    "What's new in AI today?"
    → ai-news-researcher scans sources and produces a categorized briefing

    "Find case studies of companies using AI agents for customer support"
    → ai-productivity-researcher gathers quantified examples from tier-1 sources

    "What's the latest news about Claude?"
    → claude-research-daily produces a 24-hour brief on all things Claude
    ```

---

## Quick Reference

| Plugin | Agents | Skills | Install command |
|--------|--------|--------|----------------|
| `hbr-content-suite` | 3 | 1 | `/plugin install hbr-content-suite@handsonai` |
| `ai-research-agents` | 3 | 0 | `/plugin install ai-research-agents@handsonai` |

All plugins are maintained in the [handsonai GitHub repository](https://github.com/jamesgray-ai/handsonai).
