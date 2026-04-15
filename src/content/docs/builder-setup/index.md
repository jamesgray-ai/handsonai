---
title: Builder Tools Setup Guide
description: Two-part setup guide — your AI platform with Hands-on AI add-ons, plus optional advanced tools for power users
---

Two parts. **Part 1** is everything you need to start getting real value — your AI platform plus two add-ons that live inside it. **Part 2** is optional, for power users who want advanced capabilities (local files, version control, voice input, a workflow registry) that work alongside their AI platform.

:::note[Already have an AI platform set up?]
If you've already completed your platform's Getting Started checklist, skip straight to [Hands-on AI Skills](#part-1--what-you-need-60-min) below. If not, pick one:

[→ Claude](../platforms/claude/getting-started/) · [→ OpenAI](../platforms/openai/getting-started/) · [→ Gemini](../platforms/google-gemini/getting-started/) · [→ M365 Copilot](../platforms/m365-copilot/getting-started/)
:::

## Why These Tools Matter

Real AI workflows — the kind that save time, ship work, and scale beyond one-off chats — need more than a chatbot. Two parts: **Part 1** is what you need to start getting real value — your AI platform plus two add-ons that live inside it. **Part 2** is for power users who want advanced capabilities that work in collaboration with their AI platform.

Each tool below was chosen intentionally. Here's what each one unlocks for you.

### Part 1 — What You Need

Your AI platform is the reasoning engine that powers every workflow you build — one account is enough. Two add-ons then run inside it: one gives you step-by-step framework guidance, the other makes the Hands-on AI playbook searchable from your AI tool.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **Account + Apps** | A paid subscription (Claude, ChatGPT, Gemini, or Copilot) plus the web, desktop, and mobile apps | Paid plans unlock the features you'll use here — longer conversations, file uploads, connectors, and stronger reasoning models |
| **Personalization** | Custom instructions that tell the AI about your role, industry, and style | Every conversation starts with context — you stop re-introducing yourself and answers arrive tailored from message one |
| **Memory** | The AI remembers facts about you and your work across conversations | Your AI becomes a returning assistant who knows your projects, not a stranger every time you open a new chat |
| **Connections** | Links your AI to apps you already use (Google Docs, Slack, Notion, GitHub, etc.) | AI can read and write inside your real systems — no more copy-paste between tools |
| **Hands-on AI Skills** | Skills that walk you through the [Business-First AI Framework](../business-first-ai-framework/skills/) for building AI workflows | Learn how to go from "I think AI could help with this" to a shipped, improving workflow — with step-by-step guidance at every stage |
| **Hands-on AI Knowledge Base** | The Hands-on AI playbook, connected to your AI tool as a live reference | Ask questions and get answers right inside the AI tool where you're already doing your work — no switching tabs or searching the website |

### Part 2 — For Power Users

Optional tools that work in collaboration with your AI platform to build and manage your [AI building blocks](../agentic-building-blocks/) — prompts, skills, agents, and more — as files you can version, back up, and share. Pick any combination; you can come back and add more later.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **Code Editor** | Cursor or VS Code, with AI extensions installed | An organized home for every building block you create — browse them in folders, edit them in place, and let the built-in AI assistants read and update them directly as you work |
| **Git** | Automatically tracks every change to every file | You'll constantly create and refine your building blocks — Git keeps the full history for you, so you never have to manage versions manually, and it connects to GitHub so everything gets backed up in the cloud |
| **GitHub** | Cloud storage and backup for your files, built on top of Git | Your work is safe, versioned, accessible from any machine, and easy to share |
| **Voice to Text** | Dictation software (Wispr Flow or your system's built-in voice input) | Talk instead of type — faster for long prompts and more natural when you're thinking out loud |
| **AI Registry (Notion)** | A structured Notion workspace for your workflows, AI building blocks, and connected apps | The single source of truth for what you've built, who's using it, and how it all connects — essential once you're scaling beyond one-off experiments |

## Setup Order

Start with Part 1 and complete the steps in order. Part 2 is optional — pick any combination of tools when you need them. Each link opens the full setup guide with step-by-step instructions and verification criteria. For students working through a course, the [Tools Setup Checklist](/courses/tools-setup-checklist/) adds per-step "Done when" criteria and troubleshooting prompts.

### Part 1 — What You Need (~60 min)

| # | Tool | Time | Status | Why it matters |
|---|---|---|---|---|
| 1 | AI Platform (see [Platforms](../platforms/)) | ~45 min | Required | The reasoning engine that powers every workflow — one account is enough |
| 2 | [Hands-on AI Skills](../business-first-ai-framework/skills/) | ~10 min | Recommended | Step-by-step guidance for building AI workflows, right inside your AI tool |
| 3 | [Hands-on AI Knowledge Base](../mcp-server/) | ~5 min | Recommended | Ask the Hands-on AI playbook questions without leaving your AI tool |

### Part 2 — For Power Users (~70 min total)

Pick any combination — each row names the specific capability it unlocks.

| # | Tool | Time | Requires | Install this if you want to… |
|---|---|---|---|---|
| 4 | [AI Code Editor + Extensions](editor-setup/) | ~15 min | Nothing | Store building blocks as files on your computer and edit them with AI assistance |
| 5 | [Git](git-install/) | ~10 min | Editor | Keep a full version history of your building blocks automatically |
| 6 | [GitHub](github-setup/) | ~15 min | Editor + Git | Back up your building blocks to the cloud and share them across machines |
| 7 | [Voice to Text](voice-to-text-setup/) | ~10 min | Nothing | Talk instead of type when writing prompts |
| 8 | [AI Registry (Notion)](notion-registry-setup/) | ~20 min | AI platform | Track every workflow, building block, and connected app in one workspace |

:::note[New to the terminal?]
Some Power User tools (Editor, Git, GitHub) involve running commands in the terminal. If that's unfamiliar, skim [Terminal Basics](terminal-basics/) first — it's a ~15-minute fluency primer, not a setup step.
:::

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
