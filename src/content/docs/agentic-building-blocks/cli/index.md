---
title: CLI
description: The CLI building block — terminal-native interfaces for interacting with AI, from interactive coding sessions to scriptable automation
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What a CLI Is

A **CLI** (Command-Line Interface) is a terminal-native interface for interacting with AI. Instead of using a chat window in a browser or calling an API from code, you work with AI directly from your terminal — the same environment where you already run commands, manage files, and write code.

Where [APIs](../api/index.md) let your code call AI and [SDKs](../sdk/index.md) let you build agent systems, CLIs let *you* interact with AI as a human (or script) from the command line. They combine the power of programmatic access with the immediacy of conversation.

## Key Characteristics

- **Terminal-native** — runs where you already work; no browser or IDE required
- **File-system aware** — can read, write, and navigate your project files directly
- **Tool-using** — can run shell commands, edit files, search code, and use MCP servers
- **Scriptable** — supports headless mode for automation, CI/CD pipelines, and scheduled tasks
- **Extensible** — supports plugins, skills, agents, hooks, and MCP server connections

## When to Use It

Use CLIs when:

- You're working with AI in the terminal and want a conversational, hands-on experience
- You need AI assistance while coding — refactoring, debugging, writing tests, exploring a codebase
- You want to automate AI tasks via shell scripts, CI pipelines, or scheduled jobs (headless mode)
- You need file-system-aware AI that understands your project structure, not just a chat window
- You're building workflows that combine AI with existing command-line tools

## Example

Using Claude Code to refactor a module — it reads the existing code, proposes changes across multiple files, runs the test suite to verify nothing breaks, and commits the result. The entire workflow happens in the terminal with the AI navigating the file system, using tools, and iterating based on test results.

Or running a CLI in headless mode as part of a CI pipeline — on every push, it generates release notes from the git history, creates a summary, and posts it as a GitHub release. No human interaction needed; the CLI runs unattended with a prompt passed via command-line arguments.

## CLI Tools

| Tool | Provider | Platforms | Links |
|------|----------|-----------|-------|
| **Claude Code** | Anthropic | macOS, Linux, Windows (WSL) | [Getting started](../../platforms/claude/getting-started/index.md#3-install-claude-code) · <a href="https://docs.anthropic.com/en/docs/claude-code" target="_blank">Docs</a> |
| **Codex CLI** | OpenAI | macOS, Linux, Windows (WSL) | <a href="https://github.com/openai/codex" target="_blank">GitHub</a> |
| **Gemini CLI** | Google | macOS, Linux, Windows | <a href="https://github.com/google-gemini/gemini-cli" target="_blank">GitHub</a> |
| **GitHub Copilot CLI** | Microsoft | macOS, Linux, Windows | <a href="https://docs.github.com/en/copilot/github-copilot-in-the-cli" target="_blank">Docs</a> |
| **gws** | Google Workspace | macOS, Linux, Windows | <a href="https://github.com/googleworkspace/cli" target="_blank">GitHub</a> |

## Key Concepts

**Interactive mode** — The default experience: you launch the CLI, type prompts, and the AI responds in a conversational loop. You can refine, iterate, and direct the AI in real time — similar to a chat UI but in the terminal with full file-system access.

**Headless mode** — Run the CLI non-interactively by passing a prompt as an argument. The AI executes the task and exits. This enables automation: shell scripts, CI pipelines, scheduled jobs, and any workflow where a human isn't sitting at the keyboard.

**Tool use** — CLI tools can execute shell commands, read and write files, search code, run tests, and interact with external systems. The AI decides which tools to use based on the task, just like an agent.

**Skills and plugins** — Extend the CLI with reusable routines (skills) and bundled toolkits (plugins) that add domain-specific capabilities — from code review to workflow automation.

**MCP integration** — Connect the CLI to external systems via MCP servers, giving it access to databases, APIs, project management tools, and more — the same MCP servers that work with chat UIs.

**Project memory** — Files like `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` give the CLI persistent context about your project — coding conventions, architecture decisions, and workflow preferences that persist across sessions.

## Platform Implementations

| Platform | CLI Tool | Key Features |
|----------|----------|-------------|
| **Claude** | Claude Code | Interactive + headless modes, tool use, skills, plugins, hooks, MCP integration, CLAUDE.md project memory |
| **OpenAI** | Codex CLI | Interactive + headless modes, file editing, command execution, sandboxed by default |
| **Google** | Gemini CLI | Interactive mode, Google Cloud integrations, MCP support, GEMINI.md project context |
| **Microsoft** | GitHub Copilot CLI | Command suggestions, shell integration, explain and suggest modes |

## Relationship to Other Blocks

CLI is the terminal-native interaction layer:

- **Model** is what CLIs call — they send your prompts to the model and stream back responses
- **Prompt** is how you communicate with the CLI — typing instructions in the terminal or passing them as arguments
- **Context** is loaded automatically from project files, or attached via CLI flags and MCP connections
- **Project** memory files (CLAUDE.md, etc.) give the CLI persistent project-specific instructions
- **Memory** lets the CLI accumulate preferences and patterns across sessions
- **Skills** extend the CLI with reusable routines invoked via slash commands
- **Agents** are what CLIs become in complex workflows — tool-using, multi-step, autonomous execution
- **MCP** connects the CLI to external systems, giving it the same integrations available in chat UIs
- **API** is what CLI tools call under the hood — they abstract the raw API into a conversational interface
- **SDK** provides the framework for building the CLI's agent capabilities — tool orchestration, memory, and handoffs

## Related

- [Agentic Building Blocks](../index.md) — CLI in the context of all building blocks
- [API](../api/index.md) — the programmatic interfaces that CLIs abstract over
- [SDK](../sdk/index.md) — frameworks that power CLI agent capabilities
- [MCP](../mcp/index.md) — the protocol that connects CLIs to external systems
- [Agents](../agents/index.md) — the autonomous capabilities CLIs enable
- [Skills](../skills/index.mdx) — reusable routines that extend CLI functionality
- [AI Use Cases](../../use-cases/index.md) — what teams build with these blocks
- [Coding Use Cases](../../use-cases/coding/index.md) — the primary use case for CLI tools
- [Agentic Coding](../../use-cases/coding/agentic-coding.mdx) — the coding workflow that CLI tools enable
- [Editor Setup](../../builder-setup/editor-setup.md) — AI coding extensions including Claude Code
- [Platforms](../../platforms/index.md) — platform-specific CLI guides
