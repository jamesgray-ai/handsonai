---
title: Builder Tools Setup Guide
description: Two-part setup guide — your AI platform with Hands-on AI add-ons, plus optional advanced tools for power users
---

Two parts. **Part 1** is everything you need to start getting real value — your AI platform plus one add-on that lives inside it. **Part 2** is optional, for power users who want advanced capabilities (local files, version control, voice input, a workflow registry) that work alongside their AI platform.

:::note[Already have an AI platform set up?]
If you've already completed your platform's Getting Started checklist, skip straight to [Hands-on AI Skills](#part-1--what-you-need-55-min) below. If not, pick one:

[→ Claude](../platforms/claude/getting-started/) · [→ OpenAI](../platforms/openai/getting-started/) · [→ Gemini](../platforms/google-gemini/getting-started/) · [→ M365 Copilot](../platforms/m365-copilot/getting-started/)
:::

## Why These Tools Matter

Real AI workflows — the kind that save time, ship work, and scale beyond one-off chats — need more than a chatbot. Two parts: **Part 1** is what you need to start getting real value — your AI platform plus one add-on that lives inside it. **Part 2** is for power users who want advanced capabilities that work in collaboration with their AI platform.

Each tool below was chosen intentionally. Here's what each one unlocks for you.

### Part 1 — What You Need

Your AI platform is the reasoning engine that powers every workflow you build — one account is enough. One add-on then runs inside it: the Hands-on AI skills, which give you step-by-step framework guidance.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **Account + Apps** | A paid subscription (Claude, ChatGPT, Gemini, or Copilot) plus the web, desktop, and mobile apps | Paid plans unlock the features you'll use here — longer conversations, file uploads, connectors, and stronger reasoning models |
| **Personalization** | Custom instructions that tell the AI about your role, industry, and style | Every conversation starts with context — you stop re-introducing yourself and answers arrive tailored from message one |
| **Memory** | The AI remembers facts about you and your work across conversations | Your AI becomes a returning assistant who knows your projects, not a stranger every time you open a new chat |
| **Connections** | Links your AI to apps you already use (Google Docs, Slack, Notion, GitHub, etc.) | AI can read and write inside your real systems — no more copy-paste between tools |
| **Hands-on AI Skills** | Skills that walk you through the [AI Workflow Framework](../ai-workflow-framework/skills/) for building AI workflows | Learn how to go from "I think AI could help with this" to a shipped, improving workflow — with step-by-step guidance at every stage |

### Part 2 — For Power Users

Optional tools that work in collaboration with your AI platform to build and manage your [AI building blocks](../agentic-building-blocks/) — prompts, skills, agents, and more — as files you can version, back up, and share. Pick any combination; you can come back and add more later.

| Capability | What it is | Why it matters to you |
|---|---|---|
| **Code Editor** | Cursor or VS Code, with AI extensions installed | An organized home for every building block you create — browse them in folders, edit them in place, and let the built-in AI assistants read and update them directly as you work |
| **Git** | Automatically tracks every change to every file | You'll constantly create and refine your building blocks — Git keeps the full history for you, so you never have to manage versions manually, and it connects to GitHub so everything gets backed up in the cloud |
| **GitHub** | Cloud storage and backup for your files, built on top of Git. Two pieces: a GitHub *account* (in your browser) and the GitHub *CLI* (a small program on your computer that logs Git and your AI tools in as you) | Your work is safe, versioned, accessible from any machine, and easy to share |
| **Voice to Text** | Dictation software (Wispr Flow or your system's built-in voice input) | Talk instead of type — faster for long prompts and more natural when you're thinking out loud |
| **AI Registry** | A knowledge-bundle inventory of your workflows, processes, and insights — Markdown in your workspace, maintained by your AI assistant | The single source of truth for what you've built, who's using it, and how it all connects — essential once you're scaling beyond one-off experiments |

## Setup Order

Start with Part 1 and complete the steps in order. Part 2 is optional — pick any combination of tools when you need them. Each link opens the full setup guide with step-by-step instructions and verification criteria. For students working through a course, the [Tools Setup Checklist](/courses/tools-setup-checklist/) adds per-step "Done when" criteria and troubleshooting prompts.

### Part 1 — What You Need (~55 min)

| # | Tool | Time | Status | Why it matters |
|---|---|---|---|---|
| 1 | AI Platform (see [Platforms](../platforms/)) | ~45 min | Required | The reasoning engine that powers every workflow — one account is enough |
| 2 | [Hands-on AI Skills](../ai-workflow-framework/skills/) | ~10 min | Recommended | Step-by-step guidance for building AI workflows, right inside your AI tool |

### Part 2 — For Power Users (~70 min total)

Pick any combination — each row names the specific capability it unlocks. Rows 4–7 are one sequence: do them in order.

| # | Tool | Time | Requires | Install this if you want to… |
|---|---|---|---|---|
| 3 | [AI Code Editor + Extensions](editor-setup/) | ~15 min | Nothing | Store building blocks as files on your computer and edit them with AI assistance |
| 4 | [GitHub Account](github-setup/) | ~10 min | Nothing | Have a place in the cloud for your building blocks — done entirely in your browser |
| 5 | [Git](git-install/) | ~10 min (Mac: up to 30 while Apple's tools download) | Nothing | Keep a full version history of your building blocks automatically |
| 6 | [GitHub CLI](github-cli-setup/) | ~10 min | GitHub Account + Git | Log your computer and AI tools in to GitHub once, so files sync without passwords |
| 7 | [Create & Clone Your First Repository](repo-creation-and-cloning/) | ~5 min | Editor + GitHub CLI | Prove the three pieces above work together, and get a folder to build in |
| 8 | [Voice to Text](voice-to-text-setup/) | ~10 min | Nothing | Talk instead of type when writing prompts |
| 9 | [AI Registry](ai-registry-setup/) | ~10 min | AI platform | Track every workflow, skill, agent, and connected app in your workspace — pure Markdown, no external tools |
| 10 | [Knowledge Graph](knowledge-graph-setup/) | ~40 min | AI platform + a folder | Give your AI a knowledge graph of your work — clients, offerings, processes — that it reads before answering and keeps current for you |

#### Git & GitHub at a glance

Steps 4–6 are three separate prerequisites. Here's how you know each one is done:

| Prerequisite | Done when |
|---|---|
| **1. GitHub account** | You can sign in at github.com, there is no "verify your email" banner, and **Settings → Password and authentication** shows two-factor authentication **Enabled** |
| **2. Git installed** | `git --version` prints a version number, and `git config --global user.name` and `git config --global user.email` each print back the value you set |
| **3. GitHub CLI installed and logged in** | `gh --version` prints a version number, and `gh auth status` prints `✓ Logged in to github.com account <your-username>` |

**End-to-end proof (optional, ~3 min):** create a private repository, clone it, `cd` into it, run `git status` → `On branch main`. That's the [Repository Creation & Cloning guide](/builder-setup/repo-creation-and-cloning/).

:::note[New to Markdown?]
Everything you build here — skills, prompts, context files, your registry — is stored as Markdown. If that word is unfamiliar, read [Markdown Basics](markdown-basics/) first. It takes about ten minutes and requires nothing installed.
:::

:::note[New to the terminal?]
Some Power User tools (Editor, Git, GitHub CLI) involve running commands in the terminal. If that's unfamiliar, skim [Terminal Basics](terminal-basics/) first — it's a ~15-minute fluency primer, not a setup step.
:::

:::note[Heads up]
- **AI Registry:** The registry lives in your workspace as Markdown — there's nothing extra to install beyond the Hands-on AI skills from step 2 (see the [AI Registry setup guide](ai-registry-setup/)).
- **Knowledge Graph:** Also pure Markdown, built by the Hands-on AI skills from step 2, but it needs a tool that writes files on your computer (see the [Knowledge Graph setup guide](knowledge-graph-setup/)).
:::

---

## What's Next?

With your builder tools in place, you're ready to start building with AI.

| Next Step | What it is |
|---|---|
| [**Learn the Building Blocks** →](../agentic-building-blocks/) | The eleven components of every AI workflow — models, prompts, context, projects, skills, agents, and more |
| [**Install Plugins** →](../use-the-playbook/build/) | Pre-built Claude Code agents and skills you can install in one command |
| [**Take a Course** →](../courses/) | Structured learning that walks you through building with AI step by step |
