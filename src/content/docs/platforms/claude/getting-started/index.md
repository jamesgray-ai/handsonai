---
title: Getting Started with Claude
description: Set up your Claude account, install all apps, configure personalization and memory, and connect MCP servers — plus optional developer platform access
---Complete setup checklist for Anthropic's Claude platform. Work through each section in order — later steps build on earlier ones.

**Time:** ~30 minutes for Part 1, ~5 minutes for Part 2
**Requires:** Nothing — this is where you start.

---

## Part 1 — Claude

Set up your account, install all apps, configure Claude for the best experience, and connect your tools.

### 1. Create Your Account

Sign up and choose a subscription that gives you the full feature set.

1. Go to [claude.ai](https://claude.ai) and sign up (or sign in)
2. Upgrade to **Claude Pro** ($20/month) or **Claude Max** for extended usage

**Official docs:** [Claude Support — Getting started](https://support.claude.com)

---

### 2. Install Claude Desktop

The desktop app gives you quick access to Claude outside the browser, plus support for local MCP servers and file system access.

1. Download from [claude.ai/download](https://claude.ai/download) — available for macOS and Windows
2. Sign in with your Claude account

**Official docs:** [Claude Support — Desktop app](https://support.claude.com)

---

### 3. Install Claude Code

Claude Code is Anthropic's AI coding CLI — it works directly with your files and terminal. This is the primary development tool used throughout the playbook.

Follow the official installation guide for your operating system — install commands change occasionally, and the official docs are always current:

**Official install guide:** [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)

:::caution[Don't skip the post-install steps]
After the installer finishes (on both macOS and Windows), it prints a few **post-installation steps** in the terminal — most importantly, adding `claude` to your system **PATH** so you can run it from any terminal window.

**Most people scroll past this and then can't figure out why `claude` doesn't work.** Read the final output of the installer carefully and follow each step it lists before closing the terminal. If you miss it, the easiest fix is to run the installer again and watch the end of the output.
:::

Once installed and on your PATH, open a terminal and run `claude` to start it. The first time you launch, Claude Code walks you through a few setup screens — pick your theme, accept the terms, and **connect to your Claude.ai account** when prompted (this signs you in with your existing subscription so you don't need a separate API key).

---

### 4. Claude Office Add-ins

Use Claude inside Microsoft Excel and PowerPoint.

- **Excel:** [Claude in Excel](https://claude.com/claude-in-excel)
- **PowerPoint:** [Claude in PowerPoint](https://claude.com/claude-in-powerpoint)

For Google Workspace (Gmail, Calendar, Docs), connect via **Settings → Connectors** in Claude — covered in [Step 8 below](#8-connect-mcp-servers-connectors).

---

### 5. Install Mobile Apps

Access Claude on the go for quick questions, voice conversations, and image analysis.

- **iOS:** [App Store](https://apps.apple.com/app/claude-by-anthropic/id6473753684)
- **Android:** [Google Play](https://play.google.com/store/apps/details?id=com.anthropic.claude)

Sign in with your Claude account on each device.

---

### 6. Configure Personalization

Tell Claude about yourself so every conversation starts with context about your role, industry, and preferences.

1. Click your initials (lower-left) → **Settings**
2. Find **Instructions for Claude**
3. Enter your preferences and click **Save**

**Starter template:**

> I'm a [your role] in [your industry]. I'm learning to build AI-powered workflows and agents. I prefer concise answers with practical examples. When I ask about technical concepts, explain them in business terms first, then provide the technical details.

**Official docs:** [Claude Support — Personalization features](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features)

---

### 7. Enable Memory

Memory lets Claude remember context across conversations — preferences, project details, and key facts — so each conversation picks up where the last left off.

1. Go to **Settings → Capabilities**
2. Toggle **Memory** on
3. Grant any permissions if prompted
4. Click **View and manage memory** to review or edit what Claude remembers about you

Memory works both in standalone chats and per-project. Each project has its own separate memory space.

**Official docs:** [Claude Support — Memory and chat search](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context)

---

### 8. Connect MCP Servers & Connectors

MCP (Model Context Protocol) lets Claude read from and write to external tools — giving it access to your actual work environment.

**Claude.ai (web):** Connect remote MCP servers and 50+ built-in connectors (Slack, Notion, Google Drive, etc.).

1. Go to **Settings → Connectors**
2. Browse the connector directory or click **Add custom connector** to enter a remote MCP server URL
3. Enable connectors per conversation via the **+** button → **Connectors**

**Claude Desktop:** Supports both the web connectors and local MCP servers running on your machine.

**Cowork:** Accesses your connectors, local MCP servers, and file system automatically — no extra setup needed.

Connect the Hands-on AI Playbook MCP server for reference material:

[→ MCP Server Connection Guide](../../../mcp-server/)

**Official docs:**

- [Custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Local MCP servers on Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Getting started with Cowork](https://support.claude.com/en/articles/13345190-getting-started-with-cowork)

---

## Part 2 — Anthropic Developer Platform (Advanced / Optional)

:::caution[Most people can skip this entire section]
Part 2 is **only** for technical users who plan to build applications with the Anthropic API, write code against Claude programmatically, or manage API keys for tools like Claude Code's API-based access.

**If you just want to use Claude for chat, projects, Claude Desktop, or Claude Code with your regular subscription — you're already done. Stop after Part 1.**

Come back here only when you have a specific reason to need API access.
:::

The Claude Developer Platform is where you manage API keys, monitor usage, and access developer documentation.
### 1. IDE Extension

Use Claude Code inside VS Code or Cursor. See [AI Code Editor Setup](../../../builder-setup/editor-setup/#claude-code) for installation instructions.

---

### 2. Create a Developer Platform Account

1. Go to [platform.claude.com](https://platform.claude.com) and sign in with your Anthropic account
2. Navigate to **API keys** to create a key if needed

Most people don't need this — Claude Code and Claude Desktop authenticate directly through your Claude subscription.

**Official docs:** [Claude Developer Platform](https://platform.claude.com/docs/en/home)

---

## You're Done When

**Part 1 — Claude:**

- [ ] Claude account created with Pro or Max subscription
- [ ] Claude Desktop installed and signed in
- [ ] Claude Code installed — `claude --version` prints a version number
- [ ] Mobile app installed on at least one device
- [ ] Personalization configured with your role and preferences
- [ ] Memory enabled in Settings → Capabilities
- [ ] At least one MCP connector or server connected (optional)

**Part 2 — Developer Platform:**

- [ ] Claude Code IDE extension installed in VS Code or Cursor (optional)
- [ ] Developer Platform account created at platform.claude.com (optional — for API access)
