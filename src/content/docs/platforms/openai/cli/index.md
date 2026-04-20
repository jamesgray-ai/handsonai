---
title: Codex CLI
description: OpenAI's terminal-native AI coding agent — install, authenticate, and use Codex CLI for coding, file operations, and automation
---

**Codex CLI** is OpenAI's terminal-native AI coding agent. It works with your files and shell, is sandboxed by default, and supports both interactive and headless modes. Codex is included with ChatGPT Plus, Pro, Business, Enterprise, and Edu plans.

## Install

Requires [Node.js](https://nodejs.org/) 22+. Works on macOS, Windows, and Linux.

```bash
npm install -g @openai/codex
```

Run `codex` and sign in with your ChatGPT account when prompted:

```bash
codex
```

Verify:

```bash
codex --version
```

Full walk-through: [Getting Started with OpenAI → Install Codex](../getting-started/#1-install-codex). The Codex section also covers the **Codex app** and **IDE extension** options.

## What you can do with it

- **Interactive coding** — refactor, debug, explore a codebase with Codex reading files, running commands, and iterating
- **Sandboxed execution** — Codex runs in a sandbox by default, so it won't touch files outside your project without approval
- **Headless automation** — pass a prompt as an argument for CI/CD pipelines and scheduled jobs
- **Multiple surfaces** — same Codex logic across the CLI, desktop app, and IDE extension

## Related

- [CLI building block](../../../agentic-building-blocks/cli/) — how CLIs fit alongside APIs, SDKs, and agents
- [Skills on OpenAI](../skills/) — skills support in Codex
- [Building Agents on OpenAI](../agents/building-agents/) — Codex, Agents SDK, and orchestration patterns
- <a href="https://developers.openai.com/codex/cli" target="_blank">Official Codex CLI docs</a> · <a href="https://github.com/openai/codex" target="_blank">GitHub</a>
