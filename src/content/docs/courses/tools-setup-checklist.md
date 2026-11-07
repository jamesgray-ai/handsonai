---
title: Tools Setup Checklist
description: Set up for a Hands-on AI course — your AI platform's desktop app and basic settings, plus the Hands-on AI plugin. Power-user tools are optional.
---

Two steps get you ready for Session 1: set up your AI platform, then install the Hands-on AI plugin. Everything after Part 1 is optional. You don't need any of it for the course.

## At a Glance

### Part 1: What You Need for the Course

| Step | What | Status |
|------|------|--------|
| 1 | [AI Platform Setup](#step-1-ai-platform-setup) | Required |
| 2 | [Hands-on AI Skills](#step-2-hands-on-ai-skills) | Required |

### Part 2: For Power Users

Optional tools for going further. The desktop apps are all the course needs, so add these only when you want what they do. Steps 4–7 are one sequence: do them in order.

| Step | What | Status |
|------|------|--------|
| 3 | [Code Editor + Extensions](#step-3-code-editor--extensions) | Optional |
| 4 | [GitHub Account](#step-4-github-account) | Optional |
| 5 | [Git](#step-5-git) | Optional |
| 6 | [GitHub CLI](#step-6-github-cli) | Optional |
| 7 | [Create & Clone Your First Repository](#step-7-create--clone-your-first-repository) | Optional |
| 8 | [Voice to Text](#step-8-voice-to-text) | Optional |

### Part 3: Your AI Registry

The home for every workflow you build. **In a Hands-on AI course? Skip it. We set it up together in Session 1.** Working through the framework on your own? Set it up before you run Analyze.

| Step | What | Status |
|------|------|--------|
| 9 | [AI Registry](#step-9-ai-registry) | In a course: done live in Session 1 |

---

## Part 1 — What You Need for the Course

### Step 1: AI Platform Setup

You need one AI platform, on a paid plan: for example Claude Pro or above, ChatGPT Plus or above, a Microsoft 365 Copilot license, or Gemini Enterprise. Use the one you'll build in.

**1. Get the desktop app.** The live sessions use it, and it's where you'll work during the course.

| Platform | Desktop app | Where you'll work in the course |
|----------|-------------|---------------------------------|
| Claude | [claude.ai/download](https://claude.ai/download) (Mac, Windows) | The **Code** tab |
| ChatGPT | [openai.com/chatgpt/desktop](https://openai.com/chatgpt/desktop/) (Mac, Windows) | The **Codex** tab |
| Microsoft 365 Copilot | The Microsoft 365 Copilot app, or [copilot.cloud.microsoft](https://copilot.cloud.microsoft) in your browser: either works | **Copilot Cowork** |
| Gemini | No app needed: it runs in your browser | Gemini Enterprise (work account) or [gemini.google.com](https://gemini.google.com) (personal account) |

The Code tab and the Codex tab aren't for programming. They're where the AI works with the files in a folder on your computer: reading them, writing them, and running your skills. You won't write code in the course.

**2. Check your settings and privacy.**

- **Claude:** in **Settings → Capabilities**, turn on **Code execution and file creation**; skills need it. In **Settings → Privacy**, choose whether your chats can be used to improve Claude. (On Team and Enterprise plans, your company's settings apply.)
- **ChatGPT:** in **Settings → Data controls**, choose whether **Improve the model for everyone** is on. On a personal plan it covers your Codex tasks too. (Business and Enterprise workspaces aren't used for training.)
- **Microsoft 365 Copilot:** sign in with your work account. Check that **Cowork** appears next to **Chat**; if it doesn't, ask your IT team to turn on Copilot Cowork.
- **Gemini Enterprise:** sign in with your work account. Check that **Skills** appears in the left navigation; if it doesn't, ask your admin.
- **Gemini app (personal account):** turn on **Keep Activity**; skills need it.

**3. Using Claude or ChatGPT in a browser instead of the desktop app?** Connect your Google Drive (in Claude, **Settings → Connectors**; in ChatGPT, **Settings → Apps**) so your work has somewhere to be saved. In the desktop app, your files live in a folder on your computer, so there's nothing to connect. Microsoft 365 Copilot saves to your OneDrive on its own.

Personalization, memory and connections to your other apps come later: you set them up in Session 2.

**Done when:**

- You're signed in to your platform on a paid plan, in its desktop app or your browser
- Your settings and privacy choices are made
- Using Claude or ChatGPT in a browser: your Google Drive is connected

Want the full tour of your platform? Its Getting Started guide covers everything else, and none of it is needed before Session 1: [Claude](/platforms/claude/getting-started/) · [OpenAI](/platforms/openai/getting-started/) · [Gemini](/platforms/google-gemini/getting-started/) · [Microsoft 365 Copilot](/platforms/m365-copilot/getting-started/)

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Claude / ChatGPT / Gemini Enterprise / Microsoft 365 Copilot] and running into this issue: [describe what's happening]. What should I try?

Still stuck? Bring your question to Session 1.

</details>

---

### Step 2: Hands-on AI Skills

**What:** Install the Hands-on AI plugin. It holds every Hands-on AI skill: the guides you'll use throughout the course to take a workflow from "I think AI could help with this" to tested and live. One install covers everything, and in Claude and ChatGPT it works in the Code tab and the Codex tab too.

**Action:** [Follow the plugin setup guide →](/ai-workflow-framework/skills/)

**Done when:**

- The Hands-on AI plugin is installed. On Claude, ChatGPT and Microsoft 365 Copilot, that's the whole plugin, from the marketplace or by uploading the plugin file. On Gemini, which takes skills one at a time, upload **analyze**, **scaffolding-registry** and **indexing-registry** before Session 1.
- You start a new conversation, type *"Help me analyze AI workflow opportunities"*, and Analyze starts instead of giving a generic answer. (In ChatGPT, switch to **Work** or the **Codex** tab and pick the skill with `@analyze` first.)

Seeing Analyze's first question means it worked. You can close the conversation: we start here together in Session 1.

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to add a skill to [your AI tool] on [Mac / Windows] and running into this issue: [describe what's happening]. What should I check?

</details>

---

## Part 2 — For Power Users

All optional. You don't need any of these for the course: the Code tab in Claude and the Codex tab in ChatGPT already work with the files on your computer. Add them when you want what they do.

:::note[New to the terminal?]
Some steps below (Code Editor, Git, GitHub CLI) involve running commands in the terminal. If that's unfamiliar, skim [Terminal Basics](/builder-setup/terminal-basics/) first. It's a short primer, not a setup step.
:::

### Step 3: Code Editor + Extensions

**What:** Install and configure Cursor or VS Code with AI model integration (Claude, ChatGPT Codex, Gemini Code Assist, or similar). A second window for browsing and editing the files in your folder. Optional: the Code tab in Claude and the Codex tab in ChatGPT already work with those files.

**Action:** [Follow the Code Editor setup guide →](/builder-setup/editor-setup/)

**Done when:**

- You can open your editor and see the welcome screen or an empty workspace
- At least one AI extension is installed for a platform you have a paid subscription to

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [Cursor / VS Code] on [Mac / Windows] and running into this issue: [describe what's happening]. What should I try next?

</details>

---

### Step 4: GitHub Account

**What:** Create your GitHub account and turn on two-factor authentication. Entirely in your browser — nothing to install. This is the first of three prerequisites (Steps 4–6) that together back your building blocks up to the cloud.

**Action:** [Follow the GitHub Account setup guide →](/builder-setup/github-setup/)

**Done when:**

| Prerequisite | Done when |
|---|---|
| **1. GitHub account** | You can sign in at github.com, there is no "verify your email" banner, and **Settings → Password and authentication** shows two-factor authentication **Enabled** |

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm creating a GitHub account and turning on two-factor authentication, and I'm getting this error: [paste error]. What should I try?

</details>

---

### Step 5: Git

**What:** Install Git and tell it your name and the email on your GitHub account. Keeps a full version history of your building blocks automatically.

**Action:** [Follow the Git installation guide →](/builder-setup/git-install/)

**Done when:**

| Prerequisite | Done when |
|---|---|
| **2. Git installed** | `git --version` prints a version number, and `git config --global user.name` and `git config --global user.email` each print back the value you set |

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to install Git on [Mac / Windows] and getting this error: [paste error]. What should I try next?

</details>

---

### Step 6: GitHub CLI

**What:** Install the GitHub CLI (`gh`) and log in once, so Git and the AI tools on your computer can reach GitHub as you.

**Action:** [Follow the GitHub CLI setup guide →](/builder-setup/github-cli-setup/)

**Done when:**

| Prerequisite | Done when |
|---|---|
| **3. GitHub CLI installed and logged in** | `gh --version` prints a version number, and `gh auth status` prints `✓ Logged in to github.com account <your-username>` |

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm installing the GitHub CLI (`gh`) on [Mac / Windows] and logging in with `gh auth login`, and I'm getting this error: [paste error]. What should I try?

</details>

---

### Step 7: Create & Clone Your First Repository

**What:** Create a private repository on GitHub and clone it to your computer. This is the end-to-end proof that Steps 4–6 work together — and it gives you the folder you'll build in.

**Action:** [Follow the Repository Creation and Cloning guide →](/builder-setup/repo-creation-and-cloning/)

**Done when:**

- You can see the cloned repository's files in the Code tab in Claude, the Codex tab in ChatGPT, or your editor
- In your terminal, you can navigate to the cloned folder (`cd my-repo-name`) and run `git status` — it shows `On branch main`

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm trying to clone a GitHub repository in [the Claude Code tab / the ChatGPT Codex tab / Cursor / VS Code] on [Mac / Windows] and getting this error: [paste error]. What should I try?

</details>

---

### Step 8: Voice to Text

**What:** Turn on your computer's built-in dictation, or install a dedicated voice-to-text tool such as Wispr Flow. Lets you talk instead of type — faster for long prompts and more natural when you're thinking out loud.

**Action:** [Follow the Voice to Text setup guide →](/builder-setup/voice-to-text-setup/)

**Done when:**

- You can dictate text into any input field on your computer

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up [built-in dictation / Wispr Flow / Claude Quick Entry] on [Mac / Windows] for voice-to-text and running into this issue: [describe what's happening]. What should I check?

</details>

---

## Part 3 — Your AI Registry

**In a Hands-on AI course? Skip this part. We set your registry up together in Session 1.** Already set it up? Bring it; the setup skill fills gaps rather than starting over.

### Step 9: AI Registry

**What:** Set up your Markdown-based AI Registry — a generated `REGISTRY.md` index that tracks every workflow, skill, agent, and connected app in your workspace. No external accounts needed. The AI Workflow Framework's Analyze step reads it, and every step writes to it — set it up before you run Analyze.

**Action:** [Follow the AI Registry setup guide →](/builder-setup/ai-registry-setup/)

**What to bring (optional, saves time):** something that lists what you offer, something that shows who does the work (an org chart or team list — roles are enough), something that says what matters this year, and optionally a process inventory or SOP folder. One shortens the interview; three turn it into confirmation.

**Done when:**

- You have one folder for your registry — on your computer, in a GitHub repository, or `ai-workspace/registry/` in your Google Drive (Claude, ChatGPT) or OneDrive (Microsoft 365 Copilot) through your AI tool's drive connection
- The Hands-on AI skills from Step 2 are in your AI tool (if you added skills one at a time, that includes `scaffolding-registry` and `indexing-registry`)
- `registry/` exists with `SCHEMA.md` inside, and `registry/workflows/index.md` exists (empty is correct — Analyze fills it)
- You can see your dashboard — `REGISTRY.md` next to your `registry/` folder — listing your business, lines of business, functions, and processes

<details>
<summary>Stuck? Ask AI for help</summary>

> I'm setting up my Markdown-based AI Registry (a `registry/` bundle in my workspace) and running into this issue: [describe what's happening]. What should I check?

</details>

---

## What's Next?

With Steps 1 and 2 done, you're ready for the course.

- **Have these handy for Session 1 (optional, it saves time):** a services page, an org chart or team list, this year's plan, and any process inventory or SOP folder. We use them to set up your AI Registry.
- **Bookmark this page.** Come back to it when you want a power-user tool.
- **Start Session 1.** You'll put your platform and the skills to work right away.

Having trouble with any step? Bring your questions to the first session — we'll troubleshoot together.

[→ Back to courses overview](/courses/)
