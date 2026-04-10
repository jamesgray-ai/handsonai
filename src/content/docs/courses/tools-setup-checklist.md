---
title: Tools Setup Checklist
description: Complete setup guide for Hands-on AI courses — AI platform accounts, developer tools, and workflow management
---

Everything you need to set up before Session 1. Work through the steps in order — later steps build on earlier ones. Budget **2–3 hours** total, split across two sittings if you prefer. Times are estimates — it's normal for some steps to take longer, especially if the tools are new to you.

:::tip[Track your progress]
The checkboxes below are visual markers — they won't save on the web. Use **Cmd + P** (Mac) or **Ctrl + P** (Windows) to print this page and check off steps by hand, or track progress in a notes app.
:::
## At a Glance

### Part 1: AI Platform Setup (~45 min)

| Step | What | Time | Status |
|------|------|------|--------|
| 1 | [AI Platform Account + Apps](#step-1-ai-platform-account--apps) | ~15 min | Required |
| 2 | [Personalization / Custom Instructions](#step-2-personalization--custom-instructions) | ~15 min | Recommended |
| 3 | [Memory](#step-3-memory) | ~10 min | Recommended |
| 4 | [Connections (MCP / Integrations)](#step-4-connections-mcp--integrations) | ~15 min | Recommended |

### Part 2: Builder Tools (~90 min)

| Step | What | Time | Status |
|------|------|------|--------|
| 5 | [Terminal Basics](#step-5-terminal-basics) | ~15 min | Required |
| 6 | [Code Editor + Extensions](#step-6-code-editor--extensions) | ~15 min | Required |
| 7 | [Git](#step-7-git) | ~10 min | Required |
| 8 | [GitHub](#step-8-github) | ~15 min | Required |
| 9 | [Voice to Text](#step-9-voice-to-text) | ~10 min | Recommended |
| 10 | [Hands-on AI Skills](#step-10-hands-on-ai-skills) | ~10 min | Recommended |
| 11 | [Connect the Course Knowledge Base](#step-11-connect-the-course-knowledge-base) | ~5 min | Recommended |

### Part 3: AI Workflow Management (~20 min)

| Step | What | Time | Status |
|------|------|------|--------|
| 12 | [AI Registry Setup](#step-12-ai-registry-setup) | ~20 min | Recommended |

---

## Part 1 — AI Platform Setup

These steps set up your AI platform accounts and configure them for the best experience in the course. You only need **one** platform set up — use whichever you prefer. Each platform has a Getting Started checklist that covers all four steps below:

| Platform | Getting Started Guide |
|----------|----------------------|
| Claude (Anthropic) | [Getting Started with Claude](/platforms/claude/getting-started/) |
| OpenAI (ChatGPT + Codex) | [Getting Started with OpenAI](/platforms/openai/getting-started/) |
| Gemini (Google) | [Getting Started with Gemini](/platforms/google-gemini/getting-started/) |
| M365 Copilot (Microsoft) | [Getting Started with M365 Copilot](/platforms/m365-copilot/getting-started/) |

Pick your platform(s), open the Getting Started guide, and work through the steps below. Each guide has the platform-specific instructions.

### Step 1: AI Platform Account + Apps

**What:** Create an account with a paid subscription and install all available apps (web, desktop, mobile). The course requires a paid plan (e.g., ChatGPT Plus, Claude Pro, Gemini Advanced) — free tiers don't support features you'll need. Your Getting Started guide has pricing details.

- [ ] I have a paid AI platform account and can start conversations
- [ ] I've installed the desktop and mobile apps for my platform(s)

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to sign up for [Claude / ChatGPT / Gemini / Copilot] and running into this issue: [describe what's happening]. What should I try?

Still stuck? Check your platform's [Getting Started guide](#part-1--ai-platform-setup) or bring your question to Session 1.

</details>
---

### Step 2: Personalization / Custom Instructions

**What:** Tell your AI platform about yourself so every conversation starts with context about your role, industry, and preferences.

- [ ] I've added personalization / custom instructions to my AI platform

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to set up custom instructions in [ChatGPT / Claude / Gemini] and can't find the setting. I'm on [web / desktop / mobile]. Where do I go?

Still stuck? Check your platform's [Getting Started guide](#part-1--ai-platform-setup) or bring your question to Session 1.

</details>
---

### Step 3: Memory

**What:** Enable memory so your AI platform remembers context across conversations.

- [ ] Memory is enabled on my AI platform

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to enable memory in [ChatGPT / Claude / Gemini] but can't find the toggle. I'm on [web / desktop / mobile] with a [Free / Plus / Pro] plan. Where do I look?

Still stuck? Check your platform's [Getting Started guide](#part-1--ai-platform-setup) or bring your question to Session 1.

</details>
---

### Step 4: Connections (MCP / Integrations)

**What:** Connect your AI platform to external tools and data sources so it can read from and write to apps you already use — like Google Docs, Slack, or your company's knowledge base. Each platform calls these something different (MCP servers, connectors, extensions, or connected apps).

You can skip this for now — you'll set up specific connections later in the course when you need them.

- [ ] I've connected at least one external tool or data source (optional — can do later)

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to connect [tool name] to [ChatGPT / Claude / Gemini] and running into this issue: [describe what's happening]. What should I check?

Still stuck? Check your platform's [Getting Started guide](#part-1--ai-platform-setup) or bring your question to Session 1.

</details>
---

## Part 2 — Builder Tools

Your AI platform is ready. Next, you'll set up the developer tools that let you build with AI.

These steps install the developer tools you'll use throughout the course. Each step has a detailed guide — follow the link, complete the setup, then come back here and check the box.

### Step 5: Terminal Basics

**What:** Familiarize yourself with the basics of the terminal on Mac and PowerShell on Windows.

[→ Go to Terminal Basics guide](/builder-setup/terminal-basics/)

- [ ] I can open a terminal and see a prompt (`$`, `%`, or `>`)
- [ ] Running `pwd` (Mac) or `Get-Location` (Windows) shows my current directory

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm learning to use the terminal on [Mac / Windows] and ran into this issue: [describe what happened]. What does this mean and what should I try?

</details>
---

### Step 6: Code Editor + Extensions

**What:** Install and configure Cursor or VS Code with AI model integration (Claude, ChatGPT Codex, Gemini Code Assist, or similar).

[→ Go to Editor Setup guide](/builder-setup/editor-setup/)

- [ ] I can open my editor and see the welcome screen or an empty workspace
- [ ] At least one AI extension installed for a platform I have a paid subscription to

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Cursor / VS Code] on [Mac / Windows] and running into this issue: [describe what's happening]. What should I try next?

</details>
---

### Step 7: Git

**What:** Install Git — a version control tool that tracks the changes you make to your AI building blocks. Git ensures you never lose them — every version is saved, and you can always recover or refine what you've built.

[→ Go to Git Installation guide](/builder-setup/git-install/)

- [ ] Running `git --version` in my terminal shows a version number

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to install Git on [Mac / Windows] and getting this error: [paste error]. What should I try next?

</details>
---

### Step 8: GitHub

**What:** Create an account, enable 2FA, and create a repository for your coursework. GitHub is where your files live in the cloud — backed up, versioned, and accessible from any machine.

[→ Go to GitHub Setup guide](/builder-setup/github-setup/)

- [ ] I have a GitHub account
- [ ] I can clone a repository and see the files in my editor
- [ ] In my terminal, I can navigate to the cloned folder (`cd my-repo-name`) and run `git status` — it shows `On branch main`

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to clone a GitHub repository in [Cursor / VS Code] on [Mac / Windows] and getting this error: [paste error]. What should I try?

</details>
---

### Step 9: Voice to Text

**What:** Configure system voice input or install a dedicated voice-to-text tool (Wispr Flow recommended).

[→ Go to Voice to Text Setup guide](/builder-setup/voice-to-text-setup/)

- [ ] I can dictate text into any input field on my computer

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Wispr Flow / Claude Desktop Quick Entry] on [Mac / Windows] for voice-to-text and running into this issue: [describe what's happening]. What should I check?

</details>
---

### Step 10: Hands-on AI Skills

**What:** Skills are reusable instructions that teach your AI tool how to do specific tasks your way — like editing to publication standards or generating meeting briefs. You'll use these throughout the course.

[→ How to Add Skills to Your Platform](/agentic-building-blocks/skills/#how-to-add-skills-to-your-platform)

- [ ] At least one skill installed or added to your platform
- [ ] Skill verified — invoked it in your AI tool and got a response

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to add a skill to [your platform] and it's not working. What should I check?

</details>
---

### Step 11: Connect the Course Knowledge Base

**What:** Connect the Hands-on AI knowledge base to your AI tool so you can search course content, building blocks, and reference material right where you work.

[→ Go to MCP Server Connection Guide](/mcp-server/)

- [ ] Hands-on AI MCP server connected to my AI platform

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to connect the Hands-on AI MCP server to [Claude / ChatGPT / Cursor] and running into this issue: [describe what's happening]. What should I check?

</details>
---

## Part 3 — AI Workflow Management

Your toolkit is complete. One last step to set up your workflow management system.

Keeping track of your workflows and the AI building blocks that power them is essential to change management and scaling your operations.

### Step 12: AI Registry Setup

**What:** Get a free Notion account, duplicate the AI Registry template, and connect Notion to your AI tool.

[→ Go to AI Registry Setup guide](/builder-setup/notion-registry-setup/)

- [ ] Notion AI Registry template duplicated to my workspace
- [ ] AI Registry plugin installed (`/plugin install ai-registry@handsonai`)

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up the AI Registry in Notion and running into this issue: [describe what's happening]. What should I check?

</details>
---

## What's Next?

You're all set for the course — nice work getting through the setup!

- **Quick test:** Open your AI tool and ask: "What tools and connections do I have set up?" — this confirms everything is working together
- **Bookmark this page** — come back to finish any steps you skipped
- **Start Session 1** — you'll put these tools to work right away

Having trouble with any step? Bring your questions to the first session — we'll troubleshoot together.

[→ Back to courses overview](/courses/)
