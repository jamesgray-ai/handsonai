---
date: 2026-05-04
authors:
  - jamesgray
categories:
  - Plugins
description: "Four plugins are now one. The handsonai plugin bundles the Business-First AI Framework, AI Registry, and Agentic Coding skills into a single install. Example agents move to a new gallery."
title: "One Plugin to Install: Hands-on AI Marketplace Consolidation"
---

The Hands-on AI plugin marketplace has been simplified from four plugins into one. The new `handsonai` plugin bundles the Business-First AI Framework, AI Registry, and Agentic Coding skills under a single install, single namespace, and single detail page.

<!-- more -->

## What changed

**Before:** Four separate plugins (`business-first-ai`, `ai-workflow-examples`, `ai-registry`, `agentic-coding`) — four install decisions, four namespaces, and a mix of production tools alongside narrowly-scoped example components.

**After:** One plugin — `handsonai` — with **1 agent** and **13 skills** scoped to a single coherent purpose: design, build, and document AI workflows.

```bash
/plugin marketplace add jamesgray-ai/handsonai-plugins
/plugin install handsonai@handsonai
```

See the new [plugin detail page](/use-the-playbook/build/handsonai/) for everything that's included.

## Why this is better

For non-technical students who are new to plugins, four installs felt fragmented. The four plugins didn't carve up the work in a way that mapped to anyone's mental model — they were a historical artifact of how the toolkit grew over time.

The consolidated plugin is shaped around a single question: *"What do I need to take an AI workflow from idea to documented production system?"* Everything in the plugin contributes to that. Everything that didn't is now in a separate gallery as study material.

## Where the example agents went

Specialized agents (executive writing, HBR-style editorial review, vendor-specific researchers, meeting prep) and the portable buyer-persona prompts have moved to the new [Example Gallery](/use-cases/example-gallery/). They live there as **templates to copy and customize** rather than installable defaults — adapt them to your industry, your sources, your output formats.

The gallery preserves: 7 agents (writing, editorial, research, meeting prep), 5 skills (HBR editing, meeting briefs, LinkedIn drafting, article insight extraction, GitHub skill sync), and 3 portable prompts.

## Migration for existing users

If you've installed any of the old plugins, here's the one-time migration:

```bash
/plugin uninstall business-first-ai@handsonai
/plugin uninstall ai-workflow-examples@handsonai
/plugin uninstall ai-registry@handsonai
/plugin uninstall agentic-coding@handsonai
/plugin install handsonai@handsonai
```

The skills you used (`analyze`, `naming-workflows`, `writing-feature-prds`, etc.) all still exist — only the namespace prefix changed. Your slash commands move from `/business-first-ai:analyze` to `/handsonai:analyze`, `/agentic-coding:writing-feature-prds` to `/handsonai:writing-feature-prds`, and so on.

**Cowork users:** Plugin updates require a remove-and-re-add (Cowork caches plugin versions at install time), so the migration commands above apply equally to Cowork.

## What didn't change

- The marketplace URL: `jamesgray-ai/handsonai-plugins`
- Component names: `analyze`, `framework-orchestrator`, `writing-feature-prds`, etc. are unchanged
- ZIP downloads for non-Claude-Code users (ChatGPT, M365 Copilot, Cursor, Codex CLI, Gemini CLI) — every skill is still available individually on [GitHub Releases](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest), now with all 13 skills covered (previously only 7)

## Why the consolidation is the right shape

A plugin's mental model for a student should be "tools I install to do work," not "a curated gallery of demos to study." Bundling worked examples alongside production tools dilutes what the plugin is *for*. Examples have a different job — they teach by showing — and they belong in docs and blog posts where you can read, copy, and adapt them.

If you want one of the gallery components installed locally as an agent or skill, the source files are in plain Markdown — copy from [the gallery on GitHub](https://github.com/jamesgray-ai/handsonai/tree/main/examples/agent-gallery) into your own plugin or `~/.claude/agents/` folder. Same files, different home.
