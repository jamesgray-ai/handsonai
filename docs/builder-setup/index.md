---
title: Builder Stack Setup Guide
description: Step-by-step checklist for setting up your complete AI builder toolkit — terminal, editor, Git, GitHub, AI coding CLIs, and more
---

# Builder Stack Setup Guide

This page walks you through every tool you need for an AI builder workflow. Later steps depend on earlier ones, so work through them in order. Budget about **75 minutes** to complete the required steps (longer if you include the optional ones).

Use the checkboxes to track your progress as you go.

## At a Glance

| Step | Tool | Time | Status |
|------|------|------|--------|
| 1 | Terminal Basics | ~15 min | Required |
| 2 | AI Code Editor + Extensions | ~15 min | Required |
| 3 | Git | ~10 min | Required |
| 4 | GitHub | ~15 min | Required |
| 5 | AI Coding CLIs (Command-Line Tools) | ~15 min | Required (Claude Code); Optional (Codex, Gemini) |
| 6 | AI Registry + Plugins | ~20 min | Optional |
| 7 | Voice to Text | ~10 min | Optional |

---

## Step 1: Terminal Basics

**What:** Learn to navigate your computer's command line.
**Time:** ~15 minutes
**Requires:** Nothing — this is where you start.

Every tool in this stack runs through the terminal. You don't need to be an expert — just comfortable opening it, navigating folders, and running commands.

[:octicons-arrow-right-24: Go to Terminal Basics guide](terminal-basics.md)

**You're done when:** You can open a terminal, run `pwd`, and navigate to a folder with `cd`.

- [ ] Terminal Basics — complete

---

## Step 2: AI Code Editor + Extensions

**What:** Install a code editor and add AI coding extensions.
**Time:** ~15 minutes
**Requires:** Step 1 (Terminal Basics)

Your editor is where you'll read, write, and edit code. This guide covers Cursor (has AI built in) and VS Code (free), plus AI extensions for Claude Code, OpenAI Codex, and Gemini Code Assist.

[:octicons-arrow-right-24: Go to Editor Setup guide](editor-setup.md)

**You're done when:** You can open your editor, navigate files and folders, and see the Claude Code extension installed.

- [ ] AI Code Editor — installed
- [ ] AI extensions — installed

---

## Step 3: Git

**What:** Install Git for version control.
**Time:** ~10 minutes
**Requires:** Step 1 (Terminal Basics)

Git tracks changes to your files and lets you collaborate on code. Claude Code and GitHub both depend on it.

[:octicons-arrow-right-24: Go to Git Installation guide](git-install.md)

**You're done when:** Opening your terminal and typing `git --version` prints a version number.

- [ ] Git — installed

---

## Step 4: GitHub

**What:** Create a GitHub account and connect it to your editor.
**Time:** ~15 minutes
**Requires:** Steps 2 (Editor) and 3 (Git)

GitHub hosts your projects (called *repositories*) in the cloud. You'll use it to download projects, upload your changes, and collaborate.

[:octicons-arrow-right-24: Go to GitHub Setup guide](github-setup.md)

**You're done when:** You can download (clone) a project from GitHub into your editor.

- [ ] GitHub — account created and connected

---

## Step 5: AI Coding CLIs

**What:** Install Claude Code and (optionally) other AI coding CLIs — command-line tools that let you use AI directly from your terminal.
**Time:** ~15 minutes
**Requires:** Steps 2 (Editor) and 3 (Git)

Claude Code is the primary AI coding CLI used throughout this cookbook. The guide also covers OpenAI Codex CLI and Gemini CLI as optional alternatives.

[:octicons-arrow-right-24: Go to AI Coding CLIs guide](claude-code-install.md)

**You're done when:** Running `claude --version` prints a version number, and typing `claude` starts a conversation with Claude in your terminal.

- [ ] Claude Code CLI — installed and authenticated
- [ ] OpenAI Codex CLI — installed (optional)
- [ ] Gemini CLI — installed (optional)

---

## Step 6: AI Registry + Plugins

**What:** Add the Hands-on AI plugin marketplace, set up the AI Registry, and install plugins.
**Time:** ~20 minutes
**Requires:** Step 5 (AI Coding CLIs) — plugin commands run inside Claude Code

This step has three parts:

!!! tip "These commands run inside Claude Code"
    The `/plugin` commands below are typed inside a Claude Code session, not in a regular terminal. Start Claude Code first by typing `claude` in your terminal, then run the `/plugin` commands.

**1. Add the plugin marketplace.** Register the Hands-on AI marketplace so Claude Code knows where to find plugins. You only need to do this once:

```bash
/plugin marketplace add jamesgray-ai/handsonai
```

See the [Getting Started with Plugins](../plugins/getting-started.md) guide for the full walkthrough.

**2. Set up the AI Registry.** The AI Registry is a Notion workspace template that gives you a structured system for tracking your workflows, AI building blocks, and connected applications. Once it's connected, Claude can name workflows, write SOPs (Standard Operating Procedures), and register skills directly in Notion.

[:octicons-arrow-right-24: Go to AI Registry Setup guide](notion-registry-setup.md)

**3. Install plugins.** With the marketplace added, install plugins to give Claude domain expertise:

```bash
/plugin install business-first-ai@handsonai
/plugin install ai-registry@handsonai
```

The **Business-First AI** plugin is required for a guided experience on the Claude platform using skills — it includes agents and skills for discovering AI opportunities, deconstructing workflows, and building with AI. The **AI Registry** plugin is required for Claude users who want to integrate seamlessly with the Notion registry — it lets Claude name workflows, write SOPs, and register building blocks directly in your workspace.

Browse all available plugins on the [Plugin Marketplace](../plugins/index.md).

!!! info "Using skills in Claude.ai (web)"
    After installing plugins, agents and skills work automatically in **Claude Code** and **Cowork**. However, if you want to use skills in **Claude.ai** (the web interface), there's an extra step: you need to zip each skill folder and upload it manually through Settings > Capabilities > Upload skill. See the [Using Skills in Claude.ai](../plugins/using-plugins.md#using-skills-in-claudeai-web) guide for step-by-step instructions.

**You're done when:** You've completed the parts above that apply to your workflow.

- [ ] Plugin marketplace — registered
- [ ] AI Registry — Notion template duplicated and connected (optional)
- [ ] AI Registry plugin — installed (optional)
- [ ] Business-First AI plugin — installed (optional)

---

## Step 7: Voice to Text

**What:** Set up voice dictation for faster input.
**Time:** ~10 minutes
**Requires:** Nothing — this step is fully independent.

Voice input can speed up how you write prompts, notes, and messages. This is optional but useful for anyone who thinks faster than they type.

[:octicons-arrow-right-24: Go to Voice to Text Setup guide](voice-to-text-setup.md)

**You're done when:** You can dictate text into any input field on your computer.

- [ ] Voice to Text — set up (optional)

---

## What's Next?

With your builder stack in place, you're ready to start building with AI.

<div class="grid cards" markdown>

-   :material-lightbulb:{ .lg .middle } **Learn the Building Blocks**

    ---

    Understand the six components of every AI workflow — prompts, context, projects, skills, agents, and MCP (connections to external tools).

    [:octicons-arrow-right-24: Agentic Building Blocks](../agentic-building-blocks/index.md)

-   :material-puzzle-outline:{ .lg .middle } **Install Plugins**

    ---

    Pre-built Claude Code agents and skills you can install in one command.

    [:octicons-arrow-right-24: Plugin Marketplace](../plugins/index.md)

-   :material-school:{ .lg .middle } **Take a Course**

    ---

    Structured learning that walks you through building with AI step by step.

    [:octicons-arrow-right-24: Browse Courses](../courses/index.md)

</div>
