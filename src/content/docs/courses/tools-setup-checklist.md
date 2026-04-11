---
title: Tools Setup Checklist
description: Complete setup guide for Hands-on AI courses — AI platform accounts, developer tools, and workflow management
---

Everything you need to set up before Session 1. Work through the steps in order — later steps build on earlier ones. Budget **2–3 hours** total, split across two sittings if you prefer. Times are estimates — it's normal for some steps to take longer, especially if the tools are new to you.

:::note[New to these tools?]
Before diving in, skim [Why These Tools Matter](/builder-setup/#why-these-tools-matter) (~2 minutes). It explains what each tool is and why we use it — the context that makes the rest of this checklist click.
:::

## At a Glance

### Part 1: AI Platform Setup (~45 min)

| Step | What | Time | Status |
|------|------|------|--------|
| 1 | [AI Platform Setup](#step-1-ai-platform-setup) | ~45 min | Required |

### Part 2: Builder Tools (~90 min)

| Step | What | Time | Status |
|------|------|------|--------|
| 2 | [Terminal Basics](#step-2-terminal-basics) | ~15 min | Required |
| 3 | [Code Editor + Extensions](#step-3-code-editor--extensions) | ~15 min | Required |
| 4 | [Git](#step-4-git) | ~10 min | Required |
| 5 | [GitHub](#step-5-github) | ~15 min | Required |
| 6 | [Voice to Text](#step-6-voice-to-text) | ~10 min | Recommended |
| 7 | [Hands-on AI Skills](#step-7-hands-on-ai-skills) | ~10 min | Recommended |
| 8 | [Hands-on AI Knowledge Base](#step-8-hands-on-ai-knowledge-base) | ~5 min | Recommended |

### Part 3: AI Workflow Management (~20 min)

| Step | What | Time | Status |
|------|------|------|--------|
| 9 | [AI Registry Setup](#step-9-ai-registry-setup) | ~20 min | Recommended |

---

## Part 1 — AI Platform Setup

You need at least one AI platform set up before starting on builder tools. Pick whichever you prefer — you only need one. Each platform has a Getting Started guide that walks you through everything in one place.

| Platform | Getting Started Guide |
|----------|----------------------|
| Claude (Anthropic) | [Getting Started with Claude](/platforms/claude/getting-started/) |
| OpenAI (ChatGPT + Codex) | [Getting Started with OpenAI](/platforms/openai/getting-started/) |
| Gemini (Google) | [Getting Started with Gemini](/platforms/google-gemini/getting-started/) |
| M365 Copilot (Microsoft) | [Getting Started with M365 Copilot](/platforms/m365-copilot/getting-started/) |

### Step 1: AI Platform Setup

**What:** Create a paid AI platform account, configure it for your work, and connect it to the apps you already use. Your platform's Getting Started guide walks you through all of this in one place — account creation, apps, personalization, memory, and connections.

**Action:** Follow your platform's Getting Started guide from the table above.

**Done when:**

- You have a paid AI platform account and can start conversations (Claude Pro, ChatGPT Plus, Gemini Advanced, or Copilot Pro)
- You've installed the desktop and mobile apps for your platform
- You've added personalization / custom instructions so the AI knows about your role and work
- Memory is enabled so the AI remembers context across conversations
- You've connected at least one external tool or data source (Google Docs, Slack, Notion, etc.)

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Claude / ChatGPT / Gemini / Copilot] and running into this issue: [describe what's happening]. What should I try?

Still stuck? Bring your question to Session 1.

</details>
---

## Part 2 — Builder Tools

Your AI platform is ready. Next, you'll set up the developer tools you'll use throughout the course. For each step, follow the Action link to the setup guide, complete the setup, then come back here and confirm the "Done when" criteria before moving on.

### Step 2: Terminal Basics

**What:** Learn to open the terminal, see where you are, and navigate between folders — on Mac (Terminal) and Windows (PowerShell). You don't need to be an expert.

**Action:** [Follow the Terminal Basics setup guide →](/builder-setup/terminal-basics/)

**Done when:**

- You can open a terminal and see a prompt (`$`, `%`, or `>`)
- Running `pwd` (Mac) or `Get-Location` (Windows) shows your current directory

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm learning to use the terminal on [Mac / Windows] and ran into this issue: [describe what happened]. What does this mean and what should I try?

</details>
---

### Step 3: Code Editor + Extensions

**What:** Install and configure Cursor or VS Code with AI model integration (Claude, ChatGPT Codex, Gemini Code Assist, or similar).

**Action:** [Follow the Code Editor setup guide →](/builder-setup/editor-setup/)

**Done when:**

- You can open your editor and see the welcome screen or an empty workspace
- At least one AI extension is installed for a platform you have a paid subscription to

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Cursor / VS Code] on [Mac / Windows] and running into this issue: [describe what's happening]. What should I try next?

</details>
---

### Step 4: Git

**What:** Install Git and configure your name and email so it can sign your commits.

**Action:** [Follow the Git installation guide →](/builder-setup/git-install/)

**Done when:**

- Running `git --version` in your terminal shows a version number

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to install Git on [Mac / Windows] and getting this error: [paste error]. What should I try next?

</details>
---

### Step 5: GitHub

**What:** Create an account, enable two-factor authentication (2FA), and create a repository for your coursework.

**Action:** [Follow the GitHub setup guide →](/builder-setup/github-setup/)

**Done when:**

- You have a GitHub account
- You can clone a repository and see the files in your editor
- In your terminal, you can navigate to the cloned folder (`cd my-repo-name`) and run `git status` — it shows `On branch main`

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to clone a GitHub repository in [Cursor / VS Code] on [Mac / Windows] and getting this error: [paste error]. What should I try?

</details>
---

### Step 6: Voice to Text

**What:** Configure system voice input or install a dedicated voice-to-text tool (Wispr Flow recommended).

**Action:** [Follow the Voice to Text setup guide →](/builder-setup/voice-to-text-setup/)

**Done when:**

- You can dictate text into any input field on your computer

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Wispr Flow / Claude Desktop Quick Entry] on [Mac / Windows] for voice-to-text and running into this issue: [describe what's happening]. What should I check?

</details>
---

### Step 7: Hands-on AI Skills

**What:** Install the Hands-on AI skills that walk you through the Business-First AI Framework — analyze, deconstruct, design, build, test, run, improve. These are the step-by-step guides you'll use throughout the course to take a workflow from "I think AI could help with this" to shipped and improving.

**Action:** [Follow the Framework Skills setup guide →](/business-first-ai-framework/skills/)

**Done when:**

- At least one skill is installed or added to your platform
- You've invoked a skill in your AI tool and received a response

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to add a skill to [your AI tool] on [Mac / Windows] and running into this issue: [describe what's happening]. What should I check?

</details>
---

### Step 8: Hands-on AI Knowledge Base

**What:** Connect the Hands-on AI Knowledge Base to your AI tool so you can search course content, building blocks, and reference material right where you work. Your AI tool may call this an "MCP server" or "MCP connector" — that's the underlying technology.

**Action:** [Follow the Knowledge Base connection guide →](/mcp-server/)

**Done when:**

- The Hands-on AI Knowledge Base is connected to your AI platform

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to connect the Hands-on AI MCP server to [Claude / ChatGPT / Cursor] and running into this issue: [describe what's happening]. What should I check?

</details>
---

## Part 3 — AI Workflow Management

Your toolkit is complete. One last step to set up your workflow management system.

Keeping track of your workflows and the AI building blocks that power them is essential to change management and scaling your operations.

### Step 9: AI Registry Setup

**What:** Get a free Notion account, duplicate the AI Registry template, and connect Notion to your AI tool.

**Action:** [Follow the AI Registry setup guide →](/builder-setup/notion-registry-setup/)

**Done when:**

- The Notion AI Registry template is duplicated to your workspace
- The AI Registry plugin is installed (`/plugin install ai-registry@handsonai`)

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up the AI Registry in Notion and running into this issue: [describe what's happening]. What should I check?

</details>
---

## What's Next?

You're all set for the course — nice work getting through the setup!

- **Quick test:** Open your AI tool and ask: "What tools and connections do I have set up?" — this confirms everything is working together
- **Bookmark this page** — it's your ongoing reference for the tool setup
- **Start Session 1** — you'll put these tools to work right away

Having trouble with any step? Bring your questions to the first session — we'll troubleshoot together.

[→ Back to courses overview](/courses/)
