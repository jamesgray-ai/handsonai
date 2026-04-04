---
date: 2026-03-17
authors:
  - jamesgray
categories:
  - New Content
  - Plugins
description: "CLI joins as the 11th agentic building block, and the Construct step now discovers creation tools automatically."
title: "CLI Building Block and Smarter Construct"
---Two updates this week: a new building block and a smarter Build phase.

<!-- more -->

**CLI is now the 11th agentic building block.** Terminal-native AI tools — Claude Code, Codex CLI, Gemini CLI, GitHub Copilot CLI — have earned their own spot in the [Integration layer](../../agentic-building-blocks/cli/index.md) alongside MCP, API, and SDK. The new page covers interactive and headless modes, tool use, MCP integration, and project memory. Cross-references updated across all Integration layer siblings.

**Construct (Step 3.2) now discovers creation tools automatically.** The `constructing-workflows` skill no longer hardcodes which tools to use for building skills and agents. Instead, it [scans your environment at runtime](../../business-first-ai-framework/build/index.mdx#how-creation-tools-are-discovered) to find whatever creation skills you have installed — then delegates to them or generates inline. Works across Claude Code, Cursor, Codex CLI, Gemini CLI, and VS Code Copilot. Business-First AI Framework plugin updated to v6.0.3.
