---
title: AI Registry Setup in Notion
description: Set up the Notion AI Registry template to track business processes, workflows, and AI assets
schema_type: HowTo
howto_steps:
  - name: Get Notion
    text: Sign up for a free Notion account at notion.so if you don't already have one.
  - name: Open the template
    text: Click the AI Registry template link to view the pre-built workspace structure.
  - name: Duplicate the template
    text: Click the Duplicate button in the top-right corner to copy the template to your workspace.
  - name: Review sample entries
    text: Explore the four databases (Business Processes, Workflows, AI Assets, Apps) to understand the structure.
  - name: Customize databases
    text: Edit select fields in each database to match your business areas, workflow categories, and asset types.
  - name: Connect your AI tools
    text: Add the Notion connector from your AI tool's account settings under Connected Apps.
---

# AI Registry Setup

The AI Registry is a Notion workspace template that gives you a structured system for tracking your business processes, workflows, AI assets, and connected applications. It serves as the central hub for your AI operations — a single place to document what you're building, how it works, and what tools are involved.

This registry is also the foundation for the [AI Registry plugin](../../plugins/index.md#ai-registry), a set of Claude Code skills that can read from and write to your registry automatically. Once your registry is set up and connected, Claude can name workflows, write SOPs, register skills, and keep everything in sync — anywhere on the Claude platform.

!!! note "Platform support"
    The AI Registry plugin is powered by Claude Agent skills, which are currently only supported on the **Claude** platform. Agent skills are an open standard, and many companies are already working to adopt them — as support broadens, the same skills will work across tools. The Notion connector ([Step 7](#step-7-connect-your-ai-tools)) works on both Claude and ChatGPT for basic read/write access.

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

**[AI Registry - Template](https://www.notion.so/2f3edcfdb924813f86f3eacca6b836bb)**

### Step 3: Click Duplicate

In the top-right corner of the template page, click the **"Duplicate"** button. If you're not signed in to Notion, you'll be prompted to log in first.

### Step 4: Copy to Your Workspace

Select the workspace you want to copy the template into. The entire page — including all four databases, sample entries, and relations between them — will be duplicated into your workspace.

### Step 5: Review Sample Entries

The template includes sample entries in each database so you can see how they work together. Explore a few entries to understand the structure:

- Click into a **Business Process** to see its linked workflows
- Click into a **Workflow** to see its linked AI assets and apps
- Notice how relations connect everything together

When you're ready, delete the sample entries and start adding your own.

### Step 6: Customize Databases and Properties

Tailor the registry to your business. Each database comes with sensible defaults, but you'll want to adjust them:

- **Business Processes** — Edit the **Domain** select field to match your business areas (Sales, Marketing, Product, Operations, etc.)
- **Workflows** — Update **Status** and **Type** options to fit your workflow categories
- **AI Assets** — Customize **Asset Type** options (Skill, Prompt, Agent, Project, Context MD, etc.)
- **Apps** — Configure **Type** options for your integration patterns (API, MCP Server, Native Integration, Webhook, etc.)

To edit a select field: click any cell with that property, then click **"Edit property"** to add, rename, or remove options.

### Step 7: Connect Your AI Tools

To let your AI tools read and update the registry, connect Notion using the built-in integrations available on each platform:

- **Claude** — Add the Notion connector from your Claude account settings under Connected Apps
- **ChatGPT** — Add the Notion connection from Connected Apps in your settings

Once connected, your AI tool can search, read, and update your registry databases directly. No custom configuration or API keys required.

!!! info "Plugin automation requires Claude"
    The Notion connector above gives both Claude and ChatGPT basic access to your registry. However, the [AI Registry plugin](#using-the-ai-registry-plugin) — which automates naming workflows, writing SOPs, registering skills, and more — is powered by Claude Agent skills, which are currently only supported on the **Claude** platform.

    Agent skills are an open standard, and many companies are already working to adopt them into their AI platforms. As support broadens, the same skills will work across tools without needing to be rewritten.

## Understanding the Registry Structure

### The Four Databases

| Database | Purpose | Key Fields |
|----------|---------|------------|
| **Business Processes** | High-level business functions and their domains | Domain, LOB, Description |
| **Workflows** | Specific workflows within each process | Status, Type, Trigger, Process Outcome |
| **AI Assets** | Skills, prompts, agents, and other AI components | Asset Type, Platform, Status, Dependencies |
| **Apps** | Connected applications and integrations | Type, Auth Type, Connection Status |

### How Relations Work

The databases are linked to show how your operations connect:

```
Business Process → Workflows → AI Assets
                            ↘ Apps
```

- Each **Business Process** contains multiple **Workflows**
- Each **Workflow** can use multiple **AI Assets** and **Apps**
- Changes propagate automatically through relations

## Using the AI Registry Plugin

Once your registry is connected via MCP, install the companion plugin to let Claude work with it directly:

```bash
/plugin install ai-registry@handsonai
```

The plugin includes five skills that automate common registry tasks:

| Skill | What it does |
|-------|-------------|
| `naming-workflows` | Generates consistent, outcome-focused workflow names and creates entries in the Workflows database |
| `writing-workflow-sops` | Writes Standard Operating Procedure documentation for each workflow |
| `writing-process-guides` | Documents how workflows fit together within a business process |
| `registering-skills` | Registers Claude skills in the AI Assets database with metadata |
| `syncing-skills-to-github` | Commits skills to GitHub and updates Notion with repository URLs |

### Recommended workflow

1. **Name** — Ask Claude to name a workflow and it creates a Notion entry
2. **Document** — Ask Claude to write the SOP for that workflow
3. **Connect** — Ask Claude to write a process guide linking workflows together
4. **Register** — Ask Claude to register any skills you've built in the AI Assets database
5. **Sync** — Ask Claude to push skills to GitHub with version tracking

See the [AI Registry plugin page](../../plugins/index.md#ai-registry) for full details and usage examples.

## Troubleshooting

**Relations not copying correctly?**

- This is rare with Notion duplicates. Try duplicating again.
- Ensure you're duplicating the entire page, not individual databases.

**Can't find the template?**

- The template must be shared publicly. Contact the course instructor if the link doesn't work.

**AI tool can't see your registry?**

- Confirm the Notion connector is enabled in your AI tool's settings
- Make sure you've granted access to the workspace containing your registry
- Try disconnecting and reconnecting the Notion integration

**Need to start over?**

- Delete your copy and duplicate the template again.

## Next Steps

- **Add your first process** — Start with one business domain you know well
- **Document existing workflows** — Capture what you're already doing before adding AI
- **Find AI opportunities** — Use the [AI Workflow Opportunity Finder](../../how-to/prompting/ai-workflow-opportunity-finder.md) to identify where AI can add value
- **Deconstruct workflows** — Break workflows into AI building blocks with the [Workflow Deconstruction Meta-Prompt](../../how-to/prompting/workflow-deconstruction-meta-prompt.md)
- **Install the plugin** — Set up the [AI Registry plugin](../../plugins/index.md#ai-registry) to automate registry updates
- **Explore other setup guides** — Continue with [Claude Code Installation](claude-code-install.md) if you haven't already

