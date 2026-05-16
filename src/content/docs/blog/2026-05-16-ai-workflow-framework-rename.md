---
date: 2026-05-16
authors:
  - jamesgray
categories:
  - Framework
description: "The Business-First AI Framework is now the AI Workflow Framework. Same seven steps, same skills, same /handsonai:* commands — just a clearer name that says what it actually is."
title: "Renamed: AI Workflow Framework"
---

The Business-First AI Framework has a new name: **AI Workflow Framework**. This is purely a renaming — the seven steps, the skills, the slash commands, and the way you use it all stay the same.

<!-- more -->

## Why the rename

"Business-First AI" introduced a second brand sitting alongside "Hands-on AI" — and the framework was being mistaken for the whole site. It isn't. The framework is one major pillar on Hands-on AI, specifically: a guided methodology for the end-to-end **AI workflow lifecycle** (Analyze → Deconstruct → Design → Build → Test → Run → Improve).

The name now says what it is.

## What didn't change

- **The seven steps** are unchanged: Analyze, Deconstruct, Design, Build, Test, Run, Improve.
- **The skills** are unchanged: `analyze`, `deconstruct`, `design`, `build`, `test`, `run`, `improve`.
- **The slash commands** are unchanged: `/handsonai:analyze`, `/handsonai:deconstruct`, etc.
- **The plugin** is unchanged: still `handsonai`.
- **Old URLs redirect**: anything under `/business-first-ai-framework/*` now redirects to `/ai-workflow-framework/*`. Existing bookmarks keep working.

## What did change

- **URL path**: `/business-first-ai-framework/` → `/ai-workflow-framework/`.
- **Framework agent**: renamed from `framework-orchestrator` to `framework-agent` for consistency. If you're on manual install, download the new `framework-agent.zip` from the latest GitHub release.
- **Release artifact**: the GitHub release now bundles the framework agent as well as the skills, so manual-install users on ChatGPT, Gemini, M365 Copilot, and Cursor can grab the agent the same way they grab skills.
- **Plugin version**: bumped to `v1.0.2`. No functional changes — only descriptions and the agent rename.

## Do I need to do anything?

- **Cloud plugin users** (Claude Code, Cowork): your plugin will pick up the new descriptions on its next update. No action needed.
- **Manual install users**: re-download the skills you use from the [latest release](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest) if you want the updated descriptions, and grab the new `framework-agent.zip` if you use the orchestrator. Otherwise, the old files keep working.
