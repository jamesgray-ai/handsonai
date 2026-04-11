---
title: Builder Tools Setup Guide
description: Step-by-step checklist for setting up your developer toolkit — terminal, editor, Git, GitHub, and workflow management
---

This guide sets up the developer tools and workflow management you need for building with AI.

:::note[AI platform setup is in the Platforms section]
Before starting here, make sure you've set up at least one AI platform — account, apps, personalization, memory, and connections. Each platform has its own Getting Started checklist:

[→ Claude](../platforms/claude/getting-started/) · [→ OpenAI](../platforms/openai/getting-started/) · [→ Gemini](../platforms/google-gemini/getting-started/) · [→ M365 Copilot](../platforms/m365-copilot/getting-started/)
:::

## Why These Tools Matter

Real AI workflows — the kind that save time, ship work, and scale beyond one-off chats — need more than a chatbot. You need an **AI platform** to think with, **builder tools** to build and manage your AI building blocks, and a **workflow registry** so you can track and reuse what you build.

Each tool below was chosen intentionally. Here's what each one unlocks for you.

### 1. AI Platform — the foundation

Everything else sits on top of this. Your AI platform is the reasoning engine that powers every workflow you build — pick whichever you prefer, one is enough.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **Account + Apps** | A paid subscription (Claude, ChatGPT, Gemini, or Copilot) plus the web, desktop, and mobile apps | Paid plans unlock the features you'll use here — longer conversations, file uploads, connectors, and stronger reasoning models |
| **Personalization** | Custom instructions that tell the AI about your role, industry, and style | Every conversation starts with context — you stop re-introducing yourself and answers arrive tailored from message one |
| **Memory** | The AI remembers facts about you and your work across conversations | Your AI becomes a returning assistant who knows your projects, not a stranger every time you open a new chat |
| **Connections** | Links your AI to apps you already use (Google Docs, Slack, Notion, GitHub, etc.) | AI can read and write inside your real systems — no more copy-paste between tools |

### 2. Builder Tools — build and manage your AI building blocks

These are the tools you use to build and manage your [AI building blocks](../agentic-building-blocks/) — prompts, skills, agents, and more — that power every AI workflow. Building a good one is just the start: like any asset that runs your business, they need to be refined, versioned, and shared over time. This toolkit handles all of that, whether your workflows run locally or in the cloud.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **Terminal** | The command-line interface built into your computer (Terminal on Mac, PowerShell on Windows) | Most AI developer tools run here — a little fluency unlocks everything else in this list |
| **Code Editor** | Cursor or VS Code, with AI extensions installed | An organized home for every building block you create — browse them in folders, edit them in place, and let the built-in AI assistants read and update them directly as you work |
| **Git** | Automatically tracks every change to every file | You'll constantly create and refine your building blocks — Git keeps the full history for you, so you never have to manage versions manually, and it connects to GitHub so everything gets backed up in the cloud |
| **GitHub** | Cloud storage and backup for your files, built on top of Git | Your work is safe, versioned, accessible from any machine, and easy to share |
| **Voice to Text** | Dictation software (Wispr Flow or your system's built-in voice input) | Talk instead of type — faster for long prompts and more natural when you're thinking out loud |
| **Hands-on AI Skills** | Skills that walk you through the [Business-First AI Framework](../business-first-ai-framework/skills/) for building AI workflows | Learn how to go from "I think AI could help with this" to a shipped, improving workflow — with step-by-step guidance at every stage |
| **Hands-on AI Knowledge Base** | The Hands-on AI playbook, connected to your AI tool as a live reference | Ask questions and get answers right inside the AI tool where you're already doing your work — no switching tabs or searching the website |

### 3. Workflow Registry — your system of record for AI workflows

Once you're building more than one workflow, you need a single place to track what they do, who uses them, and how they're built.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **AI Registry (Notion)** | A structured Notion workspace for your workflows, AI building blocks, and connected apps | The single source of truth for what you've built, who's using it, and how it all connects — essential once you're scaling beyond one-off experiments |

## Setup Order

Work through these in order — later steps build on earlier ones. Each link opens the full setup guide with step-by-step instructions and verification criteria.

### Builder Tools (~90 min)

| # | Tool | Time | Requires | Status |
|---|---|---|---|---|
| 1 | [Terminal Basics](terminal-basics/) | ~15 min | Nothing | Required |
| 2 | [AI Code Editor + Extensions](editor-setup/) | ~15 min | Terminal | Required |
| 3 | [Git](git-install/) | ~10 min | Terminal | Required |
| 4 | [GitHub](github-setup/) | ~15 min | Editor + Git | Required |
| 5 | [Voice to Text](voice-to-text-setup/) | ~10 min | Nothing | Recommended |
| 6 | [Hands-on AI Skills](../business-first-ai-framework/skills/) | ~10 min | AI platform | Recommended |
| 7 | [Hands-on AI Knowledge Base](../mcp-server/) | ~5 min | AI platform | Recommended |

### AI Workflow Management (~20 min)

| # | Tool | Time | Requires | Status |
|---|---|---|---|---|
| 8 | [AI Registry (Notion)](notion-registry-setup/) | ~20 min | AI platform | Recommended |

:::note[Heads up]
- **Hands-on AI Knowledge Base:** Your AI tool may call this an "MCP server" or "MCP connector" — that's the underlying technology.
- **AI Registry:** After setting up the Notion template, install the plugin so Claude can read from and write to your workspace: `/plugin install ai-registry@handsonai`
:::

---

## What's Next?

With your builder tools in place, you're ready to start building with AI.

| Next Step | What it is |
|---|---|
| [**Learn the Building Blocks** →](../agentic-building-blocks/) | The eleven components of every AI workflow — models, prompts, context, projects, skills, agents, and more |
| [**Install Plugins** →](../use-the-playbook/build/) | Pre-built Claude Code agents and skills you can install in one command |
| [**Take a Course** →](../courses/) | Structured learning that walks you through building with AI step by step |
