---
title: Antigravity CLI
description: "Antigravity CLI (agy), Google's terminal AI assistant and the successor to Gemini CLI: install it, sign in, and use it with Agent Skills and MCP servers."
---

**Antigravity CLI** (the `agy` command) is Google's command-line AI assistant, powered by Gemini. It works directly with your files and terminal for coding, file operations, and automation, and supports the same building blocks as Claude Code and Codex CLI: [skills](../skills/), MCP servers, and project rules (`AGENTS.md`).

It replaces Gemini CLI for free and Google AI Pro / Ultra users. Google moved those users to Antigravity CLI on June 18, 2026.

## Install

Open a terminal and run the line for your computer.

**macOS or Linux:**

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

**Windows (PowerShell):**

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

Close the terminal, open a new one, and check it worked:

```bash
agy --version
```

You should see a version number. Full instructions, including Windows Command Prompt: [Antigravity CLI getting started](https://antigravity.google/docs/getting-started?tab=cli).

## Sign in

Type `agy` and press Enter. The first time, it asks a few setup questions (colors, display, and whether you trust the folder), then opens your browser to sign in.

- **Personal Google account:** choose **Google OAuth**.
- **Work account with Gemini Enterprise:** choose **Use a Google Cloud project**.

Antigravity plans (Free, Google AI Plus, Pro, and Ultra) are for personal Google accounts; Google Workspace plans don't include them. See [Authenticate](https://antigravity.google/docs/install?tab=cli) and [Plans](https://antigravity.google/docs/plans/).

## Add Skills

Place skill folders in `.agents/skills/` at your project root. Antigravity CLI finds them when it starts, and each skill becomes a slash command (`/ingest`). If you add one while `agy` is running, type `/skills reload`.

Project rules go in `AGENTS.md` (or `GEMINI.md`) in the folder where you start `agy`.

See [Skills on Google Gemini](../skills/) for the full pattern, or download ready-made skills from the [skill downloads](../../../ai-workflow-framework/skills/#download-the-skill-zips).

## Moving from Gemini CLI

Google's [Migrating from Gemini CLI](https://antigravity.google/docs/cli/gcli-migration) guide covers it. In short: your `AGENTS.md` and `GEMINI.md` work as they are, project skills move from `.gemini/skills/` to `.agents/skills/`, and MCP servers move to `.agents/mcp_config.json` (or `~/.gemini/config/mcp_config.json` for every project).

Gemini CLI itself still exists for organizations on Gemini Code Assist Standard or Enterprise. If that's you, keep using it: [Gemini CLI on GitHub](https://github.com/google-gemini/gemini-cli).

## Related

- [CLI building block](../../../agentic-building-blocks/cli/): how CLIs fit alongside APIs, SDKs, and agents
- [Skills on Google Gemini](../skills/): native skill support in Antigravity
- [Antigravity IDE](../getting-started/#1-install-antigravity-ide): Google's agent-first IDE, from the same team
- <a href="https://antigravity.google/product/antigravity-cli" target="_blank">Antigravity CLI</a> · <a href="https://antigravity.google/docs/getting-started?tab=cli" target="_blank">Official docs</a>
