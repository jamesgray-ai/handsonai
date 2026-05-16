---
title: Example Gallery
description: A library of example agents, skills, and prompts to copy and customize. Templates for research, writing, editorial review, and meeting prep — adapt any of them to your own workflow.
---

The Hands-on AI plugin gives you the **methodology** for building AI workflows (Analyze → Improve) plus the **registry tools** for documenting them. Once you've designed your own workflow, you'll often want to start from a working example rather than a blank slate.

This gallery preserves a set of agents, skills, and prompts that were originally bundled in the marketplace. They're scoped to specific personas (an HBR-style editor, an Anthropic-focused researcher) and use cases (executive writing, meeting prep, LinkedIn prospecting), so they don't ship as installable tools — but they're a useful **starting point** when you're building something similar.

## How to use the gallery

1. Find the example closest to your need.
2. Copy the file from [the GitHub repo](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery).
3. Replace persona-specific framing, source lists, and output formats with your own.
4. Drop the file into your own plugin, your `~/.claude/agents/` folder, or upload to Claude.ai or Cowork.

Every file is plain Markdown — no compiled code. Everything is MIT-licensed.

---

## Agents

### Writing & Editorial

**[`tech-executive-writer`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/tech-executive-writer.md)** — Persona: a 20-year tech executive who writes for HBR, MIT Sloan, and Forbes. Translates technical AI and data topics for non-technical business audiences. *Adapt by:* changing the persona to match your industry, replacing the publication list with your own outlets.

**[`hbr-editor`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/hbr-editor.md)** — Persona: a senior HBR editor with strict standards on the "Big Idea" test, evidence quality, and prose style. Pairs with the `editing-hbr-articles` skill for detailed editorial criteria. *Adapt by:* swapping HBR for your target publication or internal style guide.

**[`hbr-publisher`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/hbr-publisher.md)** — Formats finalized articles for both web publication and PDF distribution, with metadata, social snippets, and quality checks. *Adapt by:* updating the brand identity and replacing HBR-specific formatting with your own.

### Research

**[`ai-news-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/ai-news-researcher.md)** — Daily AI industry news scan across major vendors (OpenAI, Anthropic, Google, Meta), newsletters, communities, and YouTube. Saves a dated brief to `ai-news-reports/`. *Adapt by:* swapping the vendor and source list for whatever industry you track.

**[`ai-productivity-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/ai-productivity-researcher.md)** — Researches HBR-tier case studies of enterprise AI adoption, with a strict source-tier hierarchy and structured output format. *Adapt by:* changing the topic from "AI productivity" to whatever case studies you're hunting; adjust the source tiers.

**[`claude-research-daily`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/claude-research-daily.md)** — Vendor-specific daily brief — Anthropic, Claude, Claude Code, and Cowork only. Last 24 hours, no padding. *Adapt by:* replacing the vendor focus with whatever single product or company you want to track.

**[`meeting-prep-researcher`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/agents/meeting-prep-researcher.md)** — Researches attendees, companies, and topics before a meeting. Produces a structured prep brief with conversation starters, suggested talking points, and questions to ask. *Adapt by:* tweaking the brief format to match how you actually run meetings.

---

## Skills

**[`editing-hbr-articles`](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery/skills/editing-hbr-articles)** — Editorial criteria for HBR-grade business writing: opening hooks, evidence quality, voice, length guidelines. Used standalone or via the `hbr-editor` agent. *Adapt by:* replacing the HBR criteria with your own publication's style guide.

**[`preparing-meeting-briefs`](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery/skills/preparing-meeting-briefs)** — Structured format for meeting prep briefs. Pairs with `meeting-prep-researcher` or runs standalone. *Adapt by:* tuning the brief format to your meeting types (sales calls, interviews, partnership talks).

**[`drafting-linkedin-posts`](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery/skills/drafting-linkedin-posts)** — LinkedIn post structure: hook, body, CTA, hashtags. *Adapt by:* changing voice and target audience; pair with `extracting-article-insights` to repurpose existing content.

**[`extracting-article-insights`](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery/skills/extracting-article-insights)** — Pulls key insights, themes, and quotable points from a source article for content repurposing. *Adapt by:* changing the output format to match your downstream channels (newsletter, podcast, video script).

**[`syncing-skills-to-github`](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery/skills/syncing-skills-to-github)** — Operational skill for syncing a Notion-based skill registry to a GitHub repo. *Adapt by:* changing the registry source (Airtable, a Google Sheet, your CMS) and the destination repo conventions.

---

## Portable Prompts

These three prompts work in any AI tool that supports a chat interface — Claude.ai, ChatGPT, Gemini, M365 Copilot, Cursor, etc. Copy the prompt, fill in the blanks, run.

**[`buyer-persona-revenue-leader-rachel`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/prompts/buyer-persona-revenue-leader-rachel.md)** — A complete example of a buyer persona document — demographics, role, pain points, trigger events, exclusion criteria. *Adapt by:* using as a template and rewriting for your own ideal customer.

**[`linkedin-prospect-research`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/prompts/linkedin-prospect-research.md)** — Workflow prompt that takes a buyer persona, finds 5 matching LinkedIn prospects, and produces engagement recommendations. Requires a buyer persona file as input. *Adapt by:* tuning the prospect criteria to match your sales motion.

**[`meeting-prep-quick`](https://github.com/jamesgray-ai/handsonai/blob/main/examples/agent-gallery/prompts/meeting-prep-quick.md)** — Single-shot meeting prep prompt for any AI tool. The portable counterpart to the `meeting-prep-researcher` agent. *Adapt by:* shortening, lengthening, or restructuring the brief format.

---

## What's in the production plugin?

The [`handsonai` plugin](/use-the-playbook/build/handsonai/) ships only broadly applicable, customizable tools: the 7-step AI Workflow Framework, the AI Registry skills, and feature-spec writing skills. Everything else lives here as study material.

If you want one of these gallery components installed locally as an agent or skill, copy the file from GitHub into your own plugin or your `~/.claude/agents/` folder.
