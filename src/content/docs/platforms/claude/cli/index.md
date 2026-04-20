---
title: Claude Code
description: Anthropic's terminal-native AI coding assistant — install, configure, and use Claude Code with skills, plugins, hooks, and MCP
---

**Claude Code** is Anthropic's terminal-native AI coding assistant. It runs interactive sessions and headless jobs, reads and writes files in your project, runs shell commands, and supports the full stack of Claude building blocks — [skills](../skills/installing-skills/), plugins, hooks, subagents, MCP, and `CLAUDE.md` project memory.

## Install

Follow the official install instructions, which stay current as Anthropic updates the recommended method:

→ <a href="https://docs.anthropic.com/en/docs/claude-code/setup" target="_blank">Claude Code setup (official docs)</a>

For the broader Claude onboarding (account, plan, apps), see [Getting Started with Claude](../getting-started/).

## What you can do with it

- **Interactive coding** — refactor, debug, write tests, explore a codebase with the AI navigating files and running commands
- **Headless automation** — `claude -p "prompt" --dangerously-skip-permissions` in CI/CD or scheduled jobs
- **Extend with skills and plugins** — install from [handsonai-plugins](https://github.com/jamesgray-ai/handsonai-plugins) or write your own
- **Connect to external systems** — MCP servers give Claude Code access to databases, APIs, and project tooling
- **Project memory** — `CLAUDE.md` persists conventions and context across sessions

## Related

- [CLI building block](../../../agentic-building-blocks/cli/) — how CLIs fit alongside APIs, SDKs, and agents
- [Installing Skills on Claude](../skills/installing-skills/) — native skill support in Claude Code
- [Building Agents on Claude](../agents/building-agents/) — subagents, orchestration, and scheduled work
- [Scheduling Subagents](../subagents/scheduling-subagents/) — run Claude Code on a schedule
- <a href="https://docs.anthropic.com/en/docs/claude-code" target="_blank">Official Claude Code docs</a>
