---
title: Getting Started with Gemini
description: Set up Gemini for your account type — personal, Workspace, or Enterprise — plus optional developer tools like Antigravity IDE, Gemini CLI, and Vertex AI
---Google offers three distinct Gemini products with different setup flows. Find yours below and follow the steps.

**Time:** ~20 minutes for Part 1, ~10 minutes for Part 2
**Requires:** A Google account

---

## Part 1 — Gemini Setup

### Which Gemini Do You Have?

| | **Gemini (Personal)** | **Gemini in Workspace** | **Gemini Enterprise** |
|---|---|---|---|
| **Who it's for** | Anyone with a personal Google account | Organizations on Google Workspace | Large enterprises on Google Cloud |
| **How you get it** | Sign up at [gemini.google.com](https://gemini.google.com) | Admin enables it for your Workspace org | Admin provisions through Google Cloud |
| **Plans** | Free → Google AI Plus → Google AI Pro ($19.99/mo) → Google AI Ultra ($249.99/mo) | Bundled with Workspace Business, Enterprise, or Education plans | Separate Google Cloud product |
| **App** | Gemini app (web + mobile) | Same Gemini app (sign in with work account) | Separate standalone app |
| **Key features** | Full conversational AI, extensions, Gems, CLI | AI features in Gmail, Docs, Sheets, Slides, Meet | Custom agents, enterprise search, third-party connectors |

:::tip[Not sure?]
If you signed up yourself with a personal Gmail → **Personal**.
If your company uses Google Workspace and you see Gemini in Gmail/Docs → **Workspace**.
If your company uses Google Cloud and you have a separate "Gemini Enterprise" app → **Enterprise**.
:::
---

## Gemini (Personal Account)

The full Gemini experience for individual users. Free tier available; paid plans unlock longer context, more models, and advanced features.

### 1. Create Your Account

1. Go to [gemini.google/subscriptions](https://gemini.google/subscriptions/) and sign in with your Google account
2. Choose a plan — **Google AI Pro** ($19.99/mo) is recommended for the full feature set

The free tier works for exploration, but paid plans unlock advanced models (Gemini 2.5 Pro), longer conversations, and Gems (custom AI personas).

**Official docs:** [Gemini Help Center](https://support.google.com/gemini)

### 2. Install Apps

- **Web:** Go to [gemini.google.com](https://gemini.google.com) in your browser
- **iOS:** [App Store](https://apps.apple.com/app/google-gemini/id6477141240)
- **Android:** [Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.bard)

Sign in with the same Google account you used to subscribe.

### 3. Configure Personalization

1. Go to [gemini.google.com](https://gemini.google.com) → click your profile picture → **Settings**
2. Find **Personalization** and review your preferences
3. Gemini automatically builds a profile from your conversations over time

**Starter template** — paste this into your first conversation to set your preferences:

> I'm a [your role] in [your industry]. I'm learning to build AI-powered workflows and agents. I prefer concise answers with practical examples. When I ask about technical concepts, explain them in business terms first, then provide the technical details. Please remember this for future conversations.

**Official docs:** [Gemini Help — Personalization](https://support.google.com/gemini/answer/15637730)

### 4. Enable Memory

1. Go to **Settings** (gear icon or profile menu)
2. Look for **Saved Info** and enable it
3. Review what Gemini has remembered periodically

Gemini builds memory from your conversations over time. You can also explicitly say "remember that I prefer..." to save specific preferences.

**Official docs:** [Gemini Help — Personalization and memory](https://support.google.com/gemini/answer/15637730)

### 5. Enable Extensions

Extensions connect Gemini to Google services and third-party tools.

1. Go to **Settings** → **Extensions**
2. Enable the extensions you want — Google Workspace, Maps, YouTube, Flights, Hotels
3. Some extensions are on by default for paid plan users

**Official docs:** [Gemini Help — Extensions](https://support.google.com/gemini/answer/13695044)

### You're Done When

- [ ] Google account created and plan selected
- [ ] Gemini accessible on web and mobile
- [ ] Personalization configured with your role and preferences
- [ ] Saved Info / memory enabled
- [ ] At least one extension enabled

---

## Gemini in Google Workspace

AI features embedded across Google Workspace apps — Gmail, Docs, Sheets, Slides, and Meet. Your Workspace admin controls availability. Optional **AI Expanded Access** add-on provides higher usage limits.

### 1. Verify Access

1. Check with your IT admin to confirm Gemini is enabled for your organization
2. Look for the Gemini icon (sparkle/star) in the side panel of Gmail, Docs, Sheets, or Slides
3. If you don't see it, ask your admin about your organization's Workspace plan and Gemini settings

**Official docs:** [Google Workspace Admin Help — Gemini](https://support.google.com/a/answer/13623623)

### 2. Access Gemini

Workspace users use the **same Gemini app** as personal users — just sign in with your work account.

- **Web:** Go to [gemini.google.com](https://gemini.google.com) and sign in with your work email
- **Mobile:** Download the Gemini app ([iOS](https://apps.apple.com/app/google-gemini/id6477141240) / [Android](https://play.google.com/store/apps/details?id=com.google.android.apps.bard)) and sign in with your work account

### 3. Explore AI Features in Workspace Apps

Gemini appears as a side panel or inline suggestion across Workspace:

| App | What Gemini does |
|-----|------------------|
| **Gmail** | Draft replies, summarize threads, find information across emails |
| **Docs** | Write drafts, rewrite sections, summarize documents |
| **Sheets** | Generate formulas, organize data, create summaries |
| **Slides** | Generate slide content, create images, suggest layouts |
| **Meet** | Real-time captions, meeting summaries, note-taking |

Look for the Gemini icon in the side panel or toolbar of each app.

**Official docs:** [Get started with Gemini in Workspace](https://support.google.com/mail/answer/13952129)

### 4. Configure Personalization

Personalization on Workspace accounts is admin-controlled — your options may be limited compared to personal accounts.

1. Go to [gemini.google.com](https://gemini.google.com) → **Settings**
2. Look for **Profile** — set your preferred name, job title, and industry if available
3. If your admin has enabled it, you can connect additional data sources

Automated memory may not be available on Workspace accounts. You can manually set preferences by telling Gemini "remember that I prefer..." in conversation.

### You're Done When

- [ ] Confirmed Gemini is enabled for your Workspace account
- [ ] Gemini accessible via web and mobile with your work account
- [ ] Explored Gemini features in at least one Workspace app (Gmail, Docs, Sheets, etc.)
- [ ] Profile / personalization configured (if available)

---

## Gemini Enterprise

A separate Google Cloud product (formerly Google Agentspace) with enterprise search, custom agent builder, and third-party data connectors. Has its own standalone app — separate from the standard Gemini app.

### 1. Get Access

Gemini Enterprise is provisioned through Google Cloud by your organization's admin.

1. Check with your IT admin to confirm your organization has Gemini Enterprise
2. Request access if you don't have it — provisioning is done through the [Google Cloud Console](https://console.cloud.google.com/)

Gemini Enterprise is currently invite-only for the standalone app experience.

**Official docs:** [Gemini Enterprise](https://cloud.google.com/gemini-enterprise) | [Compare editions](https://docs.cloud.google.com/gemini/enterprise/docs/editions)

### 2. Install the Gemini Enterprise App

Gemini Enterprise has its **own standalone app**, separate from the standard Gemini app.

- **Web:** Access through your Google Cloud Console or the enterprise portal your admin provides
- **iOS / Android:** Download the Gemini Enterprise app (separate from the standard Gemini app) — your admin will provide installation instructions

:::note
The Gemini Enterprise mobile app is a different app than the standard Gemini app used by personal and Workspace users.
:::
### 3. Connect Data Sources

Gemini Enterprise connects to your organization's tools and knowledge bases:

| Connector | What it connects |
|-----------|-----------------|
| **Google Workspace** | Drive, Gmail, Calendar, Sites |
| **Confluence** | Wiki pages and spaces |
| **Jira** | Issues, projects, and boards |
| **SharePoint** | Documents and sites |
| **ServiceNow** | Knowledge articles and incidents |

Your admin configures which connectors are available. Once connected, Gemini Enterprise can search across all your organization's data from a single interface.

### 4. Explore Agents

Gemini Enterprise includes an agent platform:

- **Pre-built agents** — Ready-to-use agents for common enterprise tasks (IT help desk, HR FAQ, etc.)
- **No-code agent builder** — Create custom agents that combine your data sources with Gemini's capabilities
- **Enterprise search** — Search across all connected data sources from one place

### You're Done When

- [ ] Access provisioned by your Google Cloud admin
- [ ] Gemini Enterprise app installed (web and/or mobile)
- [ ] At least one data source connected (admin-configured)
- [ ] Explored pre-built agents or the agent builder

---

## Part 2 — Google Cloud & Developer Tools

Developer tools for building with Gemini models. These are optional — if you only need Gemini for conversations, you're done after Part 1.

:::note[This part is optional]
Come back to Part 2 when you're ready to build software with Gemini-powered tools or deploy Gemini models via Google Cloud.
:::
### 1. Install Antigravity IDE

[Antigravity](https://antigravity.google/) is Google's AI-powered IDE — a VS Code fork built around an agent-first development workflow. Powered by Gemini, it features autonomous coding agents, parallel workspaces, and artifact-based transparency (task lists, plans, screenshots) so you can verify what agents are doing.

1. Download from [antigravity.google/download](https://antigravity.google/download) — available for macOS, Windows, and Linux
2. Install and sign in with your Google account

Free during public preview with generous Gemini rate limits.

**Official docs:** [Getting Started with Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity) · [Antigravity Developer Blog](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)

---

### 2. IDE Extension — Gemini Code Assist

Use Gemini inside VS Code or Cursor. See [AI Code Editor Setup](../../../builder-setup/editor-setup.md#gemini-code-assist) for installation instructions.

---

### 3. Install Gemini CLI

Google's command-line AI assistant. Works directly with your files and terminal — useful for coding tasks, file operations, and automation. Requires [Node.js](https://nodejs.org/) 18+ and a Google account.

**Install:**

```bash
npm install -g @google/gemini-cli
```

**Verify:**

```bash
gemini --version
```

**Official docs:** [Gemini CLI documentation](https://github.com/google-gemini/gemini-cli)

---

### 4. Add Skills (Gemini CLI)

After adding skills, you can say "edit this article for HBR quality" and Gemini CLI applies professional editorial standards automatically — no re-explaining your requirements each time.

Download skill folders from [GitHub](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins) and place them in `.gemini/skills/` or `.agents/skills/` in your project root. Gemini CLI discovers them automatically.

[→ How to Add Skills to Your Platform](../../../agentic-building-blocks/skills/index.mdx#how-to-add-skills-to-your-platform)

---

### 5. Google Cloud & Vertex AI (Optional)

[Google Cloud](https://cloud.google.com/) is the platform for deploying Gemini models at scale. [Vertex AI](https://cloud.google.com/vertex-ai) is the ML platform within Google Cloud for training, tuning, and serving Gemini models via API — used for production workloads, custom model tuning, and enterprise integrations.

1. Go to [console.cloud.google.com](https://console.cloud.google.com/) and create a project (or use an existing one)
2. Enable the Vertex AI API in your project
3. Try the [Vertex AI quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start) to send your first API request

Most people don't need this — Antigravity and Gemini CLI authenticate directly through your Google account.

**Official docs:** [Vertex AI documentation](https://docs.cloud.google.com/vertex-ai/docs) · [Google Cloud getting started](https://docs.cloud.google.com/vertex-ai/docs/start/cloud-environment)

---

### You're Done When

**Part 2 — Developer Tools:**

- [ ] Antigravity IDE installed and signed in (optional)
- [ ] Gemini Code Assist IDE extension installed in VS Code or Cursor (optional)
- [ ] Gemini CLI installed — `gemini --version` prints a version number (optional)
- [ ] At least one skill installed or added via Gemini CLI (optional)
- [ ] Google Cloud project created with Vertex AI API enabled (optional — for cloud workloads)
