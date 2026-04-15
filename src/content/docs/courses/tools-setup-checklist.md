---
title: Tools Setup Checklist
description: Complete setup guide for Hands-on AI courses — AI platform, in-platform add-ons, and advanced tools for power users
---

Everything you need to set up before Session 1. Work through the steps in order — later steps build on earlier ones. Budget **1–3 hours** total depending on how far you go. Times are estimates — it's normal for some steps to take longer, especially if the tools are new to you.

:::note[New to these tools?]
Before diving in, skim [Why These Tools Matter](/builder-setup/#why-these-tools-matter) (~2 minutes). It explains what each tool is and why we use it — the context that makes the rest of this checklist click.
:::

## At a Glance

### Part 1: What You Need for the Course (~60 min)

Your AI platform plus two add-ons that run entirely inside it. This is the baseline every student needs to get real value from the course.

| Step | What | Time | Status |
|------|------|------|--------|
| 1 | [AI Platform Setup](#step-1-ai-platform-setup) | ~45 min | Required |
| 2 | [Hands-on AI Skills](#step-2-hands-on-ai-skills) | ~10 min | Recommended |
| 3 | [Hands-on AI Knowledge Base](#step-3-hands-on-ai-knowledge-base) | ~5 min | Recommended |

### Part 2: For Power Users (~70 min)

More advanced tools that work in collaboration with your AI platform. Pick any combination — each unlocks a specific capability. Optional, and you can come back and add more later.

| Step | What | Time | Status |
|------|------|------|--------|
| 4 | [Code Editor + Extensions](#step-4-code-editor--extensions) | ~15 min | Optional |
| 5 | [Git](#step-5-git) | ~10 min | Optional |
| 6 | [GitHub](#step-6-github) | ~15 min | Optional |
| 7 | [Voice to Text](#step-7-voice-to-text) | ~10 min | Optional |
| 8 | [AI Registry (Notion)](#step-8-ai-registry-notion) | ~20 min | Optional |

---

## Part 1 — What You Need for the Course

Your AI platform plus two add-ons that live inside it. Most students only need Part 1 to start getting real value from the course.

### Choose Your AI Platform

You need at least one AI platform set up before starting anything else. Pick whichever you prefer — you only need one. Each platform has a Getting Started guide that walks you through everything in one place.

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

### Step 2: Hands-on AI Skills

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

### Step 3: Hands-on AI Knowledge Base

**What:** Connect the Hands-on AI Knowledge Base to your AI tool so you can search course content, building blocks, and reference material right where you work. Your AI tool may call this an "MCP server" or "MCP connector" — that's the underlying technology.

**Action:** [Follow the Knowledge Base connection guide →](/mcp-server/)

**Done when:**

- The Hands-on AI Knowledge Base is connected to your AI platform

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to connect the Hands-on AI MCP server to [Claude / ChatGPT / Cursor] and running into this issue: [describe what's happening]. What should I check?

</details>
---

## Part 2 — For Power Users

Optional tools that work in collaboration with your AI platform. Pick any combination — you don't need all of them, and you can come back and add more later as your workflows grow.

:::note[New to the terminal?]
Some steps below (Code Editor, Git, GitHub) involve running commands in the terminal. If that's unfamiliar, skim [Terminal Basics](/builder-setup/terminal-basics/) first — it's a ~15-minute fluency primer, not a setup step.
:::

### Step 4: Code Editor + Extensions

**What:** Install and configure Cursor or VS Code with AI model integration (Claude, ChatGPT Codex, Gemini Code Assist, or similar). Unlocks the ability to store your building blocks as files on your computer and edit them with AI assistance.

**Action:** [Follow the Code Editor setup guide →](/builder-setup/editor-setup/)

**Done when:**

- You can open your editor and see the welcome screen or an empty workspace
- At least one AI extension is installed for a platform you have a paid subscription to

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Cursor / VS Code] on [Mac / Windows] and running into this issue: [describe what's happening]. What should I try next?

</details>
---

### Step 5: Git

**What:** Install Git and configure your name and email so it can sign your commits. Keeps a full version history of your building blocks automatically.

**Action:** [Follow the Git installation guide →](/builder-setup/git-install/)

**Done when:**

- Running `git --version` in your terminal shows a version number

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to install Git on [Mac / Windows] and getting this error: [paste error]. What should I try next?

</details>
---

### Step 6: GitHub

**What:** Create an account, enable two-factor authentication (2FA), install the GitHub CLI, and create a repository for your coursework. Backs your building blocks up to the cloud and makes them accessible from any machine.

**Action:** [Follow the GitHub setup guide →](/builder-setup/github-setup/)

**Done when:**

- You have a GitHub account
- `gh auth status` shows you are logged in to `github.com`
- You can clone a repository and see the files in your editor (or in the Claude Desktop Code tab)
- In your terminal, you can navigate to the cloned folder (`cd my-repo-name`) and run `git status` — it shows `On branch main`

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to clone a GitHub repository in [Cursor / VS Code] on [Mac / Windows] and getting this error: [paste error]. What should I try?

</details>
---

### Step 7: Voice to Text

**What:** Configure system voice input or install a dedicated voice-to-text tool (Wispr Flow recommended). Lets you talk instead of type — faster for long prompts and more natural when you're thinking out loud.

**Action:** [Follow the Voice to Text setup guide →](/builder-setup/voice-to-text-setup/)

**Done when:**

- You can dictate text into any input field on your computer

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Wispr Flow / Claude Desktop Quick Entry] on [Mac / Windows] for voice-to-text and running into this issue: [describe what's happening]. What should I check?

</details>
---

### Step 8: AI Registry (Notion)

**What:** Get a free Notion account, duplicate the AI Registry template, and connect Notion to your AI tool. Tracks every workflow, building block, and connected app in one workspace — essential once you're scaling beyond one-off experiments.

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
