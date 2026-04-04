---
title: Builder Tools Setup Guide
description: Step-by-step checklist for setting up your developer toolkit — terminal, editor, Git, CLIs, and workflow management
---Building with AI means more than using a chatbot — you'll read code, modify files, run commands, and connect AI tools to real workflows. This guide sets up the developer tools and workflow management you need.

:::note[AI platform setup is in the Platforms section]
Before starting here, make sure you've set up at least one AI platform — account, apps, personalization, memory, and connections. Each platform has its own Getting Started checklist:

[→ Claude](../platforms/claude/getting-started/index.md) · [→ OpenAI](../platforms/openai/getting-started/index.mdx) · [→ Gemini](../platforms/google-gemini/getting-started/index.md) · [→ M365 Copilot](../platforms/m365-copilot/getting-started/index.md)
:::
## At a Glance

### Builder Tools (~90 min)

| What | Time | Status |
|------|------|--------|
| [Terminal Basics](#terminal-basics) | ~15 min | Required |
| [AI Code Editor + Extensions](#ai-code-editor-extensions) | ~15 min | Required |
| [Git](#git) | ~10 min | Required |
| [GitHub](#github) | ~15 min | Required |
| [Voice to Text](#voice-to-text) | ~10 min | Recommended |
| [Hands-on AI Skills](#hands-on-ai-skills) | ~10 min | Recommended |
| [Hands-on AI MCP Server](#hands-on-ai-mcp-server) | ~5 min | Recommended |

### AI Workflow Management (~20 min)

| What | Time | Status |
|------|------|--------|
| [AI Registry Setup](#ai-registry-setup) | ~20 min | Recommended |

---

## Builder Tools

## Terminal Basics

**What:** Learn to navigate your computer's command line — Terminal on Mac, PowerShell on Windows.
**Time:** ~15 minutes
**Requires:** Nothing — this is where you start.

Every tool in this stack runs through the terminal. You don't need to be an expert — just comfortable opening it, navigating folders, and running commands.

[→ Go to Terminal Basics guide](terminal-basics.mdx)

**You're done when:** You can open a terminal, run `pwd`, and navigate to a folder with `cd`.

- [ ] Terminal Basics — complete

---

## AI Code Editor + Extensions

**What:** Install and configure Cursor or VS Code with AI model integration.
**Time:** ~15 minutes
**Requires:** Terminal Basics

Your editor is where you'll read, write, and edit code. This guide covers Cursor (has AI built in) and VS Code (free), plus AI extensions for Claude Code, OpenAI Codex, and Gemini Code Assist.

[→ Go to Editor Setup guide](editor-setup.md)

**You're done when:** You can open your editor, navigate files and folders, and see at least one AI extension installed.

- [ ] AI Code Editor — installed
- [ ] AI extensions — installed

---

## Git

**What:** Install Git — a version control tool that tracks the changes you make to your AI building blocks.
**Time:** ~10 minutes
**Requires:** Terminal Basics

Git ensures you never lose your work — every version is saved, and you can always recover or refine what you've built.

[→ Go to Git Installation guide](git-install.md)

**You're done when:** Opening your terminal and typing `git --version` prints a version number.

- [ ] Git — installed

---

## GitHub

**What:** Create a GitHub account, enable 2FA, and create a repository for your work.
**Time:** ~15 minutes
**Requires:** Editor and Git

GitHub is where your files live in the cloud — backed up, versioned, and accessible from any machine.

[→ Go to GitHub Setup guide](github-setup.md)

**You're done when:** You can download (clone) a project from GitHub into your editor.

- [ ] GitHub — account created and connected

---

## Voice to Text

**What:** Configure system voice input or install a dedicated voice-to-text tool (Wispr Flow recommended).
**Time:** ~10 minutes
**Requires:** Nothing — this step is fully independent.

Voice input can speed up how you write prompts, notes, and messages. This is recommended for anyone who thinks faster than they type.

[→ Go to Voice to Text Setup guide](voice-to-text-setup.md)

**You're done when:** You can dictate text into any input field on your computer.

- [ ] Voice to Text — set up

---

## Hands-on AI Skills

**What:** Skills teach your AI tool specific tasks — like editing to publication standards, naming workflows consistently, or generating meeting briefs — so you describe your goal and the AI follows your standards automatically.
**Time:** ~10 minutes
**Requires:** At least one AI platform set up

Skills work across platforms — Claude Code, Claude.ai, Cowork, Cursor, Codex CLI, Gemini CLI, VS Code Copilot, and any tool that supports the skill format.

For step-by-step install instructions for your platform:

[→ How to Add Skills to Your Platform](../agentic-building-blocks/skills/index.mdx#how-to-add-skills-to-your-platform)

Browse all available plugins on the [Agents & Skills Marketplace](../use-the-playbook/build/index.md).

**You're done when:** At least one skill is installed or added to your platform.

- [ ] At least one skill — installed or added to your platform

---

## Hands-on AI MCP Server

**What:** Access the Hands-on AI knowledge base where you do your work by adding a connector in your AI tool.
**Time:** ~5 minutes
**Requires:** An AI platform account

The Hands-on AI MCP server gives your AI platform access to the playbook's reference material — building blocks, patterns, use cases, and more — right inside your conversations.

[→ Go to MCP Server Connection Guide](../mcp-server/index.md)

**You're done when:** You can ask your AI platform a question about the playbook and get an answer from the MCP server.

- [ ] Hands-on AI MCP server — connected

---

## AI Workflow Management

Keeping track of your workflows and the AI building blocks that power them is essential to change management and scaling your operations.

## AI Registry Setup

**What:** Get a free Notion account (or other database system), duplicate the AI Registry template, and connect Notion to your AI tool.
**Time:** ~20 minutes
**Requires:** An AI platform account

The AI Registry is a Notion workspace template that gives you a structured system for tracking your workflows, AI building blocks, and connected applications. Once it's connected, Claude can name workflows, write SOPs (Standard Operating Procedures), and register skills directly in Notion.

[→ Go to AI Registry Setup guide](notion-registry-setup.md)

After setting up the registry, install the AI Registry plugin so Claude can read from and write to your Notion workspace:

```bash
/plugin install ai-registry@handsonai
```

**You're done when:** You've duplicated the template and connected Notion to your AI tool.

- [ ] AI Registry — Notion template duplicated and connected
- [ ] AI Registry plugin — installed

---

## What's Next?

With your builder tools in place, you're ready to start building with AI.

<div class="grid cards" markdown>

-   💡 **Learn the Building Blocks**

    ---

    Understand the seven components of every AI workflow — models, prompts, context, projects, skills, agents, and MCP (connections to external tools).

    [→ Agentic Building Blocks](../agentic-building-blocks/index.md)

-   🧩 **Install Plugins**

    ---

    Pre-built Claude Code agents and skills you can install in one command.

    [→ Plugin Marketplace](../use-the-playbook/build/index.md)

-   🎓 **Take a Course**

    ---

    Structured learning that walks you through building with AI step by step.

    [→ Learn with James](../courses/index.md)

</div>
