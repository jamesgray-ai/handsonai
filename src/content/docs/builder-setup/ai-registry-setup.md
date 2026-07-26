---
title: AI Registry Setup
description: Set up your Markdown-based AI Registry to track workflows, skills, agents, and connected apps — no external tools required
schema_type: HowTo
howto_steps:
  - name: Pick your AI workspace
    text: Choose one folder (ideally a GitHub repository) as the home for all your AI workflows, skills, and agents.
  - name: Use the framework
    text: Run the AI Workflow Framework skills — the registry creates and updates itself as you name, deconstruct, design, build, and run workflows.
  - name: Open REGISTRY.md
    text: Review the generated REGISTRY.md file at the root of your workspace — it lists your skills, agents, workflows, business processes, and apps.
  - name: Refresh anytime
    text: Ask Claude to "update my registry" to regenerate the index after adding assets outside the framework.
---The **AI Registry** is your inventory of everything you build with AI: workflows, skills, agents, business processes, and the apps they connect to. It lives entirely in your workspace as Markdown files — no database, no external account, nothing extra to maintain.

New to Markdown? It's plain text with a few formatting marks — see [Markdown Basics](../markdown-basics/) for a ten-minute primer.

The registry has one simple principle: **the file is the record.**

- Every **skill** and **agent** already describes itself in its own file (the `name` and `description` at the top).
- Every **workflow** gets a small `workflow.yaml` file that the [AI Workflow Framework](../../ai-workflow-framework/) creates and updates automatically as you work through the steps.
- Every **business process** is described by its process guide file.
- The **apps** a workflow uses are listed right in that workflow's `workflow.yaml`.

On top of those files sits one generated index: **`REGISTRY.md`**, at the root of your workspace. It's your at-a-glance dashboard — which workflows exist, who owns them, whether they're healthy, when they last ran, and which skills, agents, and apps they use. You never edit `REGISTRY.md` by hand; Claude regenerates it from the source files.

:::note[Coming from the Notion registry?]
Earlier versions of this playbook used a Notion template as the AI Registry. That still works as an optional mirror — see [Optional: Mirror to Notion](#optional-mirror-to-notion) below. If you want to move your Notion registry into Markdown, ask Claude: *"Migrate my Notion AI Registry into my workspace using the indexing-registry skill."*
:::

## Prerequisites

- A folder for your AI work — ideally a GitHub repository (see [Git](../git-install/) and [GitHub](../github-setup/) setup), but any folder works
- Claude with the [Hands-on AI plugin](../../use-the-playbook/build/) installed (Claude Code or Cowork), or the individual framework skills added to your Claude project

## Setup Steps

### Step 1: Pick Your AI Workspace

Choose **one folder** as the home for all your AI workflows, skills, and agents. This is your *AI workspace*. The registry lives at its root, next to the folders the framework creates:

```
my-ai-workspace/
├── REGISTRY.md          ← generated index (your dashboard)
├── outputs/             ← one folder per workflow (with workflow.yaml)
├── sops/                ← standard operating procedures
├── process-guides/      ← business process guides
└── .claude/
    ├── skills/          ← your skills
    └── agents/          ← your agents
```

**One workspace = one registry.** If you work in multiple Cowork project folders, each gets its own registry scoped to that folder. To see everything in one place, keep all your AI work in a single workspace folder or repository.

### Step 2: Use the Framework — the Registry Builds Itself

There is no separate registry setup. The first time you name or deconstruct a workflow, Claude creates **two files** for you:

1. **`outputs/<workflow-name>/workflow.yaml`** — the workflow's record. A small text file holding everything the registry knows about that one workflow: its name, description, status, trigger, owner, and (as you progress) which apps, skills, and agents it uses.
2. **`REGISTRY.md`** — the index at your workspace root. Claude reads all your workflow records, skills, and agents and renders them as tables you can scan.

After your first workflow finishes the Build step, `REGISTRY.md` looks something like this:

```markdown
# AI Registry

## Workflows
| Workflow | Business Process | Owner | Status | Health | Last Run |
|---|---|---|---|---|---|
| Pipeline Hygiene Review | Sales Pipeline | James | Under Development | — | — |

## Skills
| Skill | Description | Location |
|---|---|---|
| scoring-deal-health | Scores deals against a staleness rubric… | outputs/…/SKILL.md |

## Agents
| Agent | Description | Location |
|---|---|---|
| unlisted-deal-scanner | Finds deals in email that aren't in the CRM… | outputs/…/agents/… |
```

You never fill any of this in yourself. Each framework step adds what it just learned to the workflow's record, then refreshes the index:

| When you… | The registry records… |
|-----------|----------------------|
| Name a workflow (`naming-workflows`) | Name, description, business process, status, trigger |
| Deconstruct it (Step 2) | Owner, requirements link |
| Design it (Step 3) | Type (augmented/automated/manual), autonomy level |
| Build it (Step 4) | Apps used, skills/agents used, platform |
| Test it (Step 5) | Health (working / needs attention) |
| Run it (Step 6) | Status → in production, last run date |
| Improve it (Step 7) | Updated health, next review date |
| Write an SOP or process guide | Links joining workflows to their docs and processes |

If a step ever can't write the file (for example, a read-only folder), Claude tells you it skipped the refresh — you can always catch up later with *"update my AI Registry."*

### Step 3: Open REGISTRY.md

After your first workflow, open `REGISTRY.md` at your workspace root. You'll see tables for:

- **Skills** and **Agents** — everything you've built, with a copy-paste Quick Start Prompt for each
- **Workflows** — the operational dashboard: owner, status, health, last run, plus links to each workflow's SOP, requirements, and design spec
- **Business Processes** — your workflows grouped by process
- **Apps** — which integrations each workflow depends on

### Step 4: Refresh Anytime

The framework refreshes the index automatically after every step. But if you add skills or agents outside the framework — or the index ever looks stale or missing — you can refresh it yourself at any time. The skill that does this is called **`indexing-registry`**, and you can invoke it two ways:

1. **Just ask** (works everywhere — Claude Code, Cowork, claude.ai):

   > "Update my AI Registry"

2. **Run the slash command** (Claude Code):

   ```
   /handsonai:indexing-registry
   ```

Either way, Claude rescans your workspace — every `workflow.yaml`, skill, agent, SOP, and process guide — and regenerates `REGISTRY.md` from scratch. Because it's a generated file, it's always safe to rebuild, and you never lose anything: the source files are the record; the index is just the view.

## Verify Setup

- [ ] `REGISTRY.md` exists at your workspace root after naming or deconstructing your first workflow
- [ ] Your workflow appears in the Workflows table with its status and business process
- [ ] Your skills and agents appear with descriptions and Quick Start Prompts
- [ ] Asking *"What have I built?"* gets an answer grounded in your registry

## Troubleshooting

**REGISTRY.md wasn't created?**

- Make sure you're working inside your AI workspace folder (Claude can only write where it has access)
- Ask directly: *"Update my AI Registry using the indexing-registry skill"*

**A workflow is missing from the index?**

- Check that it has a `workflow.yaml` in its `outputs/<workflow-name>/` folder — older workflows with flat files (e.g., `outputs/my-workflow-requirements.md`) show as "legacy"; re-running the `deconstruct` skill offers to migrate them

**Working in claude.ai without a project folder?**

- Claude generates `REGISTRY.md` as a downloadable file — keep it in your Project knowledge and re-upload it (along with `workflow.yaml`) when you continue work

## Optional: Mirror to Notion

If you work across multiple machines and tools — or just like having a visual database view — you can keep the [Notion AI Registry template](https://jamesgray007.notion.site/AI-Operations-Registry-Template-2f3edcfdb924813f86f3eacca6b836bb) as a **mirror** of your Markdown registry. The template contains exactly four databases — one per core concept, nothing to configure or prune:

- **Workflows** — the operational dashboard: status, trigger, execution mode, autonomy level, and a link to each workflow's SOP
- **Processes** — your workflows grouped by business process
- **Skills** and **Agents** — everything you've built, with descriptions, GitHub links, and clickable relations to the workflows that use them

To set it up:

1. Duplicate the template into your Notion workspace
2. Connect the Notion connector in your Claude settings (Settings → Connectors)
3. After regenerating your registry, ask Claude: *"Mirror my AI Registry to Notion"*

Claude copies your registry entries into the Notion databases and remembers the connection (each workflow's `workflow.yaml` records its Notion page). From then on, the framework keeps the mirror current automatically as you work through the steps — Build adds your new skills and agents with their workflow relations, and Run updates status and health.

You can also work with single entries using plain commands — *"register this skill in Notion"*, *"add this workflow to my Notion registry"*, *"what's in my Notion registry?"* — no setup beyond the two steps above, and nothing to configure inside the skill.

The Markdown files in your workspace remain the source of truth — the mirror is one-way, and you never need Notion for the framework to work.

## Next Steps

- **Find AI opportunities** — Use the [Analyze](../../ai-workflow-framework/analyze/) guide to identify where AI can add value
- **Deconstruct your first workflow** — Follow the [Deconstruct](../../ai-workflow-framework/deconstruct/) guide; the registry starts itself
- **Document workflows** — Ask Claude to write SOPs (`writing-workflow-sops`) and process guides (`writing-process-guides`)
- **Explore the plugin** — See the [Hands-on AI plugin page](../../use-the-playbook/build/) for all registry-related skills
