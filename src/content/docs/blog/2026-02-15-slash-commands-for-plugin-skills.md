---
date: 2026-02-15
authors:
  - jamesgray
categories:
  - Plugins
description: "All 10 plugin skills now have slash commands — invoke any skill directly instead of relying on auto-triggering."
title: "Slash Commands for All Plugin Skills"
---Both marketplace plugins — **Business-First AI** and **AI Registry** — now support direct slash command invocation for every skill. Instead of describing what you need and hoping Claude triggers the right skill, you can invoke it directly with a `/` command in Claude Code.

<!-- more -->

All 10 skills across both plugins now include `user_invocable: true` and a `command:` field in their frontmatter. This means you can type `/business-first-ai:analyze` to start a workflow audit, `/ai-registry:workflow-sop` to write an SOP, or any of the other 8 commands listed below — no prompt engineering required.

Slash commands work everywhere Claude Code runs: terminal, VS Code, JetBrains, the Code tab in the desktop app, and Claude Code on the web.

**Business-First AI commands** (v2.1.0):

- `/business-first-ai:analyze` — run a workflow audit (Step 1)
- `/business-first-ai:deconstruct` — break down a workflow (Step 2)
- `/business-first-ai:build-workflow` — design and build (Step 3)
- `/business-first-ai:edit-article` — edit to HBR quality
- `/business-first-ai:meeting-prep` — research before a meeting

**AI Registry commands** (v3.1.0):

- `/ai-registry:name-workflow` — name and register a workflow
- `/ai-registry:workflow-sop` — write an SOP
- `/ai-registry:process-guide` — write a process guide
- `/ai-registry:register-block` — register a building block in Notion
- `/ai-registry:sync-skills` — sync skills to GitHub

Skills still auto-trigger from natural language prompts — the slash commands are an additional way to invoke them directly. See the updated [Business-First AI](../../business-first-ai-framework/skills.mdx) and [AI Registry](../../use-the-playbook/build/ai-registry.mdx) plugin pages for details.
