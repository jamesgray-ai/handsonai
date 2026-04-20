---
title: Gemini CLI
description: Google's terminal-native AI assistant — install, authenticate, and use Gemini CLI with skills and MCP
---

**Gemini CLI** is Google's open-source command-line AI assistant. It works directly with your files and terminal for coding, file operations, and automation, and supports the same building blocks as Claude Code and Codex CLI — [skills](../skills/), MCP, and project memory (`GEMINI.md`).

## Install

Requires [Node.js](https://nodejs.org/) 18+ and a Google account.

```bash
npm install -g @google/gemini-cli
```

Verify:

```bash
gemini --version
```

Full walk-through: [Getting Started with Gemini → Install Gemini CLI](../getting-started/#3-install-gemini-cli).

## Authenticate

Gemini CLI authenticates directly through your Google account — no separate Vertex AI setup needed for most users. On first run, `gemini` will open a browser to sign you in.

## Add Skills

Place skill folders in `.gemini/skills/` (or `.agents/skills/`) at your project root. Gemini CLI discovers them automatically.

See [Skills on Google Gemini](../skills/) for the full pattern, or download ready-made skills from [handsonai-plugins](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins).

## Related

- [CLI building block](../../../agentic-building-blocks/cli/) — how CLIs fit alongside APIs, SDKs, and agents
- [Skills on Google Gemini](../skills/) — native skill support in Gemini CLI and Antigravity
- [Antigravity IDE](../getting-started/#1-install-antigravity-ide) — Google's agent-first IDE, also powered by Gemini
- <a href="https://github.com/google-gemini/gemini-cli" target="_blank">Gemini CLI on GitHub</a> · <a href="https://geminicli.com/docs/" target="_blank">Official docs</a>
