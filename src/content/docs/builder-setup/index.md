---
title: Builder Tools Setup Guide
description: What each builder tool is and why it matters — your AI platform's desktop app and the Hands-on AI Skills, plus optional tools for power users
---

This page explains what each tool is and why you'd want it. To set up for a course, follow the [Tools Setup Checklist](/courses/tools-setup-checklist/): it has the steps and how to tell each one is done.

There are three parts:

1. **What you need:** your AI platform's desktop app and the Hands-on AI Skills.
2. **For power users:** optional tools that work alongside your AI platform.
3. **Your AI Registry:** the home for every workflow you build. In a course, we set it up together in Session 1.

## Why These Tools Matter

### Part 1 — What You Need

| Tool | What it is | Why it matters to you |
|---|---|---|
| **Your AI platform's desktop app** | The Claude, ChatGPT or Microsoft 365 Copilot app on your computer. Gemini Enterprise runs in your browser. | It's where you work. In Claude, the **Code** tab works with the files in a folder on your computer; in ChatGPT, the **Codex** tab does the same. You don't write code in either. |
| **[Hands-on AI Skills](../ai-workflow-framework/skills/)** | Skills that walk you through the [AI Workflow Framework](../ai-workflow-framework/) | Step-by-step guidance from "I think AI could help with this" to a tested, live workflow, right inside your AI tool |

Personalization, memory and connections make your AI more useful over time. The courses cover them in Session 2; your platform's Getting Started guide has the steps whenever you want them: [Claude](../platforms/claude/getting-started/) · [OpenAI](../platforms/openai/getting-started/) · [Gemini](../platforms/google-gemini/getting-started/) · [Microsoft 365 Copilot](../platforms/m365-copilot/getting-started/)

### Part 2 — For Power Users

Optional tools for building and managing your [AI building blocks](../agentic-building-blocks/) (prompts, skills, agents and more) as files you can version, back up and share. The desktop apps are enough for the courses; add these when you want what they do.

| Tool | What it is | Install this if you want to… | Requires |
|---|---|---|---|
| [Code Editor + Extensions](editor-setup/) | Cursor or VS Code, with AI extensions | Browse and edit your files in a second window, alongside the desktop app | Nothing |
| [GitHub Account](github-setup/) | Cloud storage for your files, set up in your browser | Have a place in the cloud for your building blocks | Nothing |
| [Git](git-install/) | Tracks every change to every file | Keep a full version history of your building blocks automatically | Nothing |
| [GitHub CLI](github-cli-setup/) | A small program that logs Git and your AI tools in to GitHub as you | Sync files to GitHub without passwords | GitHub Account + Git |
| [Create & Clone Your First Repository](repo-creation-and-cloning/) | Your first private repository, copied to your computer | Prove the three pieces above work together, and get a folder to build in | GitHub CLI |
| [Voice to Text](voice-to-text-setup/) | Built-in dictation, or a tool such as Wispr Flow | Talk instead of type when writing prompts | Nothing |
| [Knowledge Graph](knowledge-graph-setup/) | A folder of pages about your work (clients, offerings, processes) that your AI keeps current | Give your AI context it reads before answering | Your AI platform + a folder |

The GitHub Account, Git, GitHub CLI and repository rows are one sequence: do them in order.

#### Git & GitHub at a glance

Those first three are separate prerequisites. Here's how you know each one is done:

| Prerequisite | Done when |
|---|---|
| **1. GitHub account** | You can sign in at github.com, there is no "verify your email" banner, and **Settings → Password and authentication** shows two-factor authentication **Enabled** |
| **2. Git installed** | `git --version` prints a version number, and `git config --global user.name` and `git config --global user.email` each print back the value you set |
| **3. GitHub CLI installed and logged in** | `gh --version` prints a version number, and `gh auth status` prints `✓ Logged in to github.com account <your-username>` |

**End-to-end proof (optional):** create a private repository, clone it, `cd` into it, run `git status` → `On branch main`. That's the [Repository Creation & Cloning guide](/builder-setup/repo-creation-and-cloning/).

:::note[New to Markdown?]
Everything you build here (skills, prompts, context files, your registry) is stored as Markdown. If that word is unfamiliar, read [Markdown Basics](markdown-basics/) first. It's short and needs nothing installed.
:::

:::note[New to the terminal?]
Some power-user tools (Editor, Git, GitHub CLI) involve running commands in the terminal. If that's unfamiliar, skim [Terminal Basics](terminal-basics/) first. It's a short primer, not a setup step.
:::

### Part 3 — Your AI Registry

| Tool | What it is | Why it matters to you |
|---|---|---|
| [AI Registry](ai-registry-setup/) | An inventory of your workflows, processes and insights: Markdown in your workspace, kept up to date by your AI | The single source of truth for what you've built, who's using it, and how it all connects |

In a Hands-on AI course, skip this until Session 1: we set it up together there. Working through the framework on your own? Set it up before you run Analyze, which reads it and registers your candidates. There's nothing to install beyond the Hands-on AI Skills.

## What's Next?

With your builder tools in place, you're ready to start building with AI.

| Next Step | What it is |
|---|---|
| [**Learn the Building Blocks** →](../agentic-building-blocks/) | The fifteen components of every AI workflow, in four layers — models, prompts, context, skills, agents, connections, registry, evaluation, and more |
| [**Install Plugins** →](../use-the-playbook/build/) | Pre-built Claude Code agents and skills you can install in one command |
| [**Take a Course** →](../courses/) | Structured learning that walks you through building with AI step by step |
