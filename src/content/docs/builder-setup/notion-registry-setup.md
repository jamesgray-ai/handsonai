---
title: AI Registry Setup in Notion
description: Set up the Notion AI Registry template to track business processes, workflows, and AI building blocks
schema_type: HowTo
howto_steps:
  - name: Get Notion
    text: Sign up for a free Notion account at notion.so if you don't already have one.
  - name: Open the template
    text: Click the AI Registry template link to view the pre-built workspace structure.
  - name: Duplicate the template
    text: Click the Duplicate button in the top-right corner to copy the template to your workspace.
  - name: Review sample entries
    text: Explore the four databases (Business Processes, Workflows, AI Building Blocks, Apps) to understand the structure.
  - name: Customize databases
    text: Edit select fields in each database to match your business areas, workflow categories, and asset types.
  - name: Connect your AI tools
    text: Add the Notion connector from your AI tool's account settings under Connected Apps.
---The AI Registry is a Notion workspace template that gives you a structured system for tracking your business processes, workflows, AI building blocks, and connected applications. It serves as the central hub for your AI operations — a single place to document what you're building, how it works, and what tools are involved.

This registry is also the foundation for the [AI Registry plugin](../../use-the-playbook/build/#ai-registry), a set of Claude Code skills that can read from and write to your registry automatically. Once your registry is set up and connected, Claude can name workflows, write SOPs (Standard Operating Procedures), register skills, and keep everything in sync — anywhere on the Claude platform.

:::note[Platform support]
The AI Registry plugin is powered by Claude Agent skills, which are currently only supported on the **Claude** platform. Agent skills are an open standard, and many companies are already working to adopt them — as support broadens, the same skills will work across tools. The Notion connector ([Step 7](#step-7-connect-your-ai-tools)) works on both Claude and ChatGPT for basic read/write access.
:::
## Prerequisites

- Notion account (free or paid) — [get Notion here](https://www.notion.so/product)
- Basic familiarity with Notion pages and databases

## Setup Steps

### Step 1: Get Notion

If you don't already have Notion, sign up at [notion.so](https://www.notion.so/product). Notion is available on:

- **Web** — works in any browser
- **Desktop** — macOS and Windows apps
- **Mobile** — iOS and Android

A free Notion account is all you need to use the registry.

### Step 2: Open the Template

Click this link to view the AI Registry template:

**<a href="https://jamesgray007.notion.site/AI-Operations-Registry-Template-2f3edcfdb924813f86f3eacca6b836bb" target="_blank">AI Registry - Template</a>**

### Step 3: Click Duplicate

In the top-right corner of the template page, click the **"Duplicate"** button. If you're not signed in to Notion, you'll be prompted to log in first.

### Step 4: Copy to Your Workspace

Select the workspace you want to copy the template into. The entire page — including all four databases, sample entries, and relations between them — will be duplicated into your workspace.

### Step 5: Review Sample Entries

The template includes sample entries in each database so you can see how they work together. Explore a few entries to understand the structure:

- Click into a **Business Process** to see its linked workflows
- Click into a **Workflow** to see its linked AI building blocks and apps
- Notice how relations connect everything together

When you're ready, delete the sample entries and start adding your own.

### Step 6: Customize Databases and Properties

Tailor the registry to your business. Each database comes with sensible defaults, but you'll want to adjust them:

- **Business Processes** — Edit the **Domain** select field to match your business areas (Sales, Marketing, Product, Operations, etc.)
- **Workflows** — Update **Status**, **Execution Mode** (Augmented, Automated, Manual), and **Autonomy Level** (Deterministic, Guided, Autonomous, N/A) options to fit your workflow categories
- **AI Building Blocks** — Customize **Asset Type** options (Skill, Prompt, Agent, Project, Context MD, etc.)
- **Apps** — Configure **Type** options for your integration patterns (API, MCP Server, Native Integration, Webhook, etc.)

To edit a select field: click any cell with that property, then click **"Edit property"** to add, rename, or remove options.

### Step 7: Connect Your AI Tools

To let your AI tools read and update the registry, connect Notion using the built-in integrations available on each platform:

- **Claude** — Add the Notion connector from your Claude account settings under Connected Apps
- **ChatGPT** — Add the Notion connection from Connected Apps in your settings

Once connected, your AI tool can search, read, and update your registry databases directly. No custom configuration or API keys required.

:::note[Plugin automation requires Claude]
The Notion connector above gives both Claude and ChatGPT basic access to your registry. However, the [AI Registry plugin](#using-the-ai-registry-plugin) — which automates naming workflows, writing SOPs, registering skills, and more — is powered by Claude Agent skills, which are currently only supported on the **Claude** platform.

Agent skills are an open standard, and many companies are already working to adopt them into their AI platforms. As support broadens, the same skills will work across tools without needing to be rewritten.
:::
## Understanding the Registry Structure

### The Four Databases

| Database | Purpose | Key Fields |
|----------|---------|------------|
| **Business Processes** | High-level business functions and their domains | Domain, LOB, Description, Guide (URL) |
| **Workflows** | Specific workflows within each process | Status, Execution Mode, Autonomy Level, Trigger, Process Outcome, SOP (URL), Workflow Requirements (URL), Design Spec (URL) |
| **AI Building Blocks** | Skills, prompts, agents, and other AI components | Asset Type, Platform, Status, Dependencies |
| **Apps** | Connected applications and integrations | Type, Auth Type, Connection Status |

### How Relations Work

The databases are linked to show how your operations connect:

```
Business Process → Workflows → AI Building Blocks
                            ↘ Apps
```

- Each **Business Process** contains multiple **Workflows**
- Each **Workflow** can use multiple **AI Building Blocks** and **Apps**
- Changes propagate automatically through relations

## Using the AI Registry Plugin

Once your registry is connected via the Notion connector, install the companion plugin to let Claude work with it directly:

```bash
/plugin install handsonai@handsonai
```

The plugin includes five skills that automate common registry tasks:

| Skill | What it does |
|-------|-------------|
| `naming-workflows` | Generates consistent, outcome-focused workflow names and creates entries in the Workflows database |
| `writing-workflow-sops` | Writes SOP markdown files for workflows and optionally links them from your tracker's SOP URL property |
| `writing-process-guides` | Writes process guide markdown files and optionally links them from your tracker's Guide URL property |
| `registering-building-blocks` | Registers AI building blocks (Skills, Agents, Prompts, Context MDs) in the AI Building Blocks database |
| `syncing-skills-to-github` | Commits skills to GitHub and updates Notion with repository URLs |

### Recommended workflow

1. **Name** — Ask Claude to name a workflow and it creates a Notion entry
2. **Document** — Ask Claude to write the SOP for that workflow
3. **Connect** — Ask Claude to write a process guide linking workflows together
4. **Register** — Ask Claude to register any skills you've built in the AI Building Blocks database
5. **Sync** — Ask Claude to push skills to GitHub with version tracking

See the [AI Registry plugin page](../../use-the-playbook/build/#ai-registry) for full details and usage examples.

## Verify Setup

After duplicating and customizing the template, confirm everything is working:

- [ ] You can see all **four databases** in your workspace (Business Processes, Workflows, AI Building Blocks, Apps)
- [ ] Clicking into a sample entry shows **relations** linking to other databases (e.g., a Workflow links to its Business Process)
- [ ] You can **create a new entry** in any database and fill in the fields
- [ ] If you connected an AI tool (Step 7), ask it: *"Search my Notion workspace for the AI Registry"* — it should find and describe your databases

## Troubleshooting

**Relations not copying correctly?**

- This is rare with Notion duplicates. Try duplicating again.
- Ensure you're duplicating the entire page, not individual databases.

**Can't find the template?**

- The template must be shared publicly. If the link doesn't work, check for updates on [GitHub](https://github.com/jamesgray-ai/handsonai/issues).

**AI tool can't see your registry?**

- Confirm the Notion connector is enabled in your AI tool's settings
- Make sure you've granted access to the workspace containing your registry
- Try disconnecting and reconnecting the Notion integration

**Need to start over?**

- Delete your copy and duplicate the template again.

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm setting up the AI Registry in Notion and running into this issue: [describe what's happening]. I duplicated the template and can see the databases. What should I check?

</details>
## Next Steps

- **Add your first process** — Start with one business domain you know well
- **Document existing workflows** — Capture what you're already doing before adding AI
- **Find AI opportunities** — Use the [Analyze AI Workflow Opportunities](../../ai-workflow-framework/analyze/) guide to identify where AI can add value
- **Deconstruct workflows** — Break workflows into AI building blocks with the [Deconstruct Workflows](../../ai-workflow-framework/deconstruct/) guide
- **Install the plugin** — Set up the [AI Registry plugin](../../use-the-playbook/build/#ai-registry) to automate registry updates
- **Explore other setup guides** — See [Platforms](../../platforms/) for platform-specific CLI tools

