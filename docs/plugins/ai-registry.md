---
title: AI Registry
description: Document, name, register, and sync AI operational workflows and skills in Notion
---

# AI Registry

Skills for building a structured registry of your AI workflows and skills. This plugin gives Claude the conventions for naming workflows, writing documentation (SOPs and process guides), registering skills in Notion, and syncing everything to GitHub. Use it to build an organized, searchable inventory of your AI operations.

!!! note "Prerequisites"
    This plugin requires a **Notion account** and the **Notion MCP connector**. Without it, Claude can follow the naming and documentation conventions but cannot save entries to Notion. See [Notion Registry Setup](../builder-setup/notion-registry-setup.md) for configuration instructions.

## Install

```bash
/plugin install ai-registry@handsonai
```

## Components

### Skills

---

#### `naming-workflows`

**What it does:** Generates consistent, outcome-focused names and descriptions for business workflows, then creates entries in your Notion Workflows database. Follows domain-specific naming patterns so your registry stays organized as it grows.

**When to use it:** Use this when you have a new workflow to document, need to standardize existing workflow names, or want to add a workflow entry to Notion. Also useful when you're not sure what to call a workflow.

**How it works:**

1. You describe the workflow (what it does, what domain it's in)
2. Claude identifies the domain (Sales, Marketing, Product, Education, Operations, etc.)
3. Claude generates 2-3 name options following the naming pattern for that domain
4. Claude writes a 1-2 sentence description (action + outcome) and suggests a process outcome (the concrete deliverable)
5. Claude searches your Notion Business Processes database to suggest where the workflow fits
6. After you confirm, Claude creates the entry in Notion with all properties filled in

**Naming conventions:**

| Domain | Pattern | Examples |
|--------|---------|----------|
| Sales | [Prospect Type] [Action] | Student Enrollment, Lead Qualification |
| Marketing | [Content Type] [Action/Purpose] | Newsletter Distribution, Content Repurposing |
| Product | [Deliverable] [Action] | Lesson Content Creation, Exercise Development |
| Education | [Student/Cohort] [Activity] | Student Onboarding, Live Session Delivery |
| Operations | [Function] [Process] | Email Response Drafting, Calendar Management |

Names are always 2-4 words, noun phrases (not verb phrases), in Title Case.

**Example prompts:**

    "Name a workflow for drafting email responses"
    → Suggests options like "Email Response Drafting" with description
      and process outcome, then creates the Notion entry

    "I need to name a workflow for turning lesson recordings into
    social media content"
    → Suggests "Content Repurposing" (Marketing pattern), writes the
      description, and creates the entry

**What you'll get:** A named workflow entry in your Notion Workflows database with: name, description, process outcome, business process link, sequence number, status, type, and trigger.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003; (Notion MCP required)

---

#### `writing-workflow-sops`

**What it does:** Writes Standard Operating Procedure documentation for workflows and saves it directly to the Notion workflow page body. Adapts the SOP template based on whether the workflow is Manual, Augmented, or Automated.

**When to use it:** Use this when you have a workflow entry in Notion and need to document how it's actually executed — step-by-step procedures, prerequisites, quality checks, and troubleshooting guidance.

**How it works:**

1. Claude fetches the workflow from Notion to get context (name, description, type, trigger, apps, assets used)
2. Claude asks clarifying questions about the procedure details
3. Claude writes the SOP using a template adapted for the workflow type:
    - **Manual**: Detailed human steps with time estimates and exact UI paths
    - **Augmented**: Steps marked as (AI) or (Human) with clear handoff points
    - **Automated**: Focus on monitoring, intervention points, and error handling
4. After your review and approval, Claude updates the workflow page body in Notion

**SOP sections:**

| Section | Purpose |
|---------|---------|
| Overview | 1-2 sentence summary |
| Prerequisites | Access, data, and tools needed |
| Trigger | When and how the workflow starts |
| Procedure | Step-by-step instructions (action verbs, one action per step) |
| Outputs | Deliverables with destinations |
| Quality Checks | How to verify success |
| Troubleshooting | Common problems and fixes |
| Automation Notes | For Augmented/Automated types only |

**Example prompts:**

    "Write an SOP for the Email Response Drafting workflow"
    → Fetches the workflow from Notion, asks about procedure details,
      produces a complete SOP, and saves it to the workflow page

    "Document how the Student Onboarding workflow works"
    → Walks through the SOP writing process, produces Manual-type
      documentation with detailed steps and time estimates

**What you'll get:** A complete SOP saved directly to your Notion workflow page body, with all sections filled in and adapted for the workflow type.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003; (Notion MCP required)

---

#### `writing-process-guides`

**What it does:** Writes Business Process Guide documentation that explains the strategic context and rhythm of a complete business process — when to execute it, why it matters, and how its component workflows fit together. This is the strategic companion to the tactical SOPs.

**When to use it:** Use this when you need to document how multiple workflows connect into a larger business process. Process guides answer "when, why, and what order" while SOPs answer "how."

**How it works:**

1. Claude fetches the business process from Notion to get context and linked workflows
2. Claude fetches each linked workflow for sequence and trigger details
3. Claude asks clarifying questions about timing and decision points
4. Claude writes the Process Guide using a structured template
5. After your review, Claude updates the business process page body in Notion

**Process Guide sections:**

| Section | Purpose |
|---------|---------|
| Purpose | Why this process exists and its business impact |
| When to Execute | Triggers, frequency, timing |
| Process Overview | Visual flow of workflows in sequence |
| Workflow Sequence | Each workflow with trigger, duration, and output |
| Decision Points | Key choices during the process |
| Success Criteria | How to know the process worked |
| Common Pitfalls | What typically goes wrong |

**Example prompts:**

    "Write a process guide for the Email Management business process"
    → Fetches the process and its workflows from Notion, documents
      the end-to-end flow, decision points, and success criteria

    "How do the Student Enrollment and Student Onboarding workflows
    connect? Document the full process."
    → Creates a process guide showing the workflow sequence,
      handoffs, and timing

**What you'll get:** A complete Business Process Guide saved to your Notion business process page body. Scannable in 2 minutes, focused on the strategic "when/why/what order" rather than tactical how-to details.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003; (Notion MCP required)

---

#### `registering-skills`

**What it does:** Registers or updates Claude Skills in your Notion AI Assets database. Extracts metadata from the skill's SKILL.md file, generates a Quick Start Prompt, checks for duplicates, and creates or updates the registry entry.

**When to use it:** Use this immediately after creating, packaging, or updating any Claude Skill to keep your AI Assets database current. Also useful for batch-registering multiple skills at once.

**How it works:**

1. Claude reads the SKILL.md frontmatter to extract the skill name and description
2. Claude generates a Quick Start Prompt — a single, copy-paste-ready sentence that demonstrates the skill's primary use case
3. Claude searches your Notion AI Assets database for an existing entry with the exact same name (to prevent duplicates)
4. If found: updates the existing entry with the latest description and Quick Start Prompt
5. If not found: creates a new entry with name, description, asset type (Skill), platform (Claude), and Quick Start Prompt

For batch registration, Claude searches for each skill individually first, builds separate update and create lists, then processes them.

**Example prompts:**

    "Register the email-response-drafting skill in Notion"
    → Reads the SKILL.md, generates a Quick Start Prompt, checks for
      duplicates, and creates or updates the AI Assets entry

    "Register all skills in the ~/.claude/skills/ directory"
    → Batch processes every skill, reporting X created and Y updated

**What you'll get:** An entry (or updated entry) in your Notion AI Assets database with: name, description, asset type, platform, Quick Start Prompt, and GitHub URL (if applicable).

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003; (Notion MCP required)

---

#### `syncing-skills-to-github`

**What it does:** Syncs Claude Skills from your local `~/.claude/skills/` directory to a GitHub repository. Detects changes, generates semantic commit messages, pushes to remote, and updates Notion AI Assets with GitHub URLs.

**When to use it:** Use this after creating or updating skills locally, after exporting skills from cloud to local, or as part of a weekly batch sync. This is Part 2 of the export-to-sync workflow (Part 1 is exporting skills from the cloud to your local machine).

**How it works:**

1. **Detect** changes in `~/.claude/skills/` using git status
2. **Review** what changed — new files, modifications, deletions
3. **Identify** which skill directories are affected
4. **Generate** semantic commit messages with prefixes: `[CREATE]`, `[UPDATE]`, `[FIX]`, `[SYNC]`, `[RETIRE]`
5. **Commit** changes to the local git repository
6. **Push** to GitHub remote
7. **Update** Notion AI Assets database with GitHub URLs and set status to "Deployed"
8. **Regenerate** the README.md skill index

**Three usage modes:**

- **Single skill sync** — "Sync the writing-linkedin-posts skill to GitHub" — commits and pushes just that skill
- **Batch sync** — "Sync all changed skills to GitHub" — detects all changes, commits everything, updates Notion for each
- **Dry run** — "Show what would sync to GitHub" — previews changes and commit message without actually committing

**Example prompts:**

    "Sync all changed skills to GitHub"
    → Detects 3 changes (1 new, 2 modified), generates a batch
      commit message, pushes, updates Notion for all 3 skills,
      and regenerates the README

    "Show what would sync to GitHub"
    → Previews the changes and generated commit message, asks for
      confirmation before proceeding

**What you'll get:** Skills committed and pushed to GitHub with descriptive commit messages, Notion AI Assets entries updated with GitHub URLs, and an auto-generated README index.

**Platform compatibility:** Claude Code &#10003; (requires terminal access and git credentials)

---

## Recommended Workflow

These skills work best in sequence, building from naming through to version control:

1. **Name your workflow** — Use `naming-workflows` to create a consistent entry in Notion
2. **Document the procedure** — Use `writing-workflow-sops` to write the SOP for the workflow
3. **Connect workflows** — Use `writing-process-guides` to document how workflows fit together in a business process
4. **Register your skills** — Use `registering-skills` to track Claude Skills in the AI Assets database
5. **Version control everything** — Use `syncing-skills-to-github` to push skills to GitHub with Notion tracking

## FAQ

**Do I need all five skills?**
No. Each skill works independently. Start with `naming-workflows` if you're building a registry from scratch, or `registering-skills` if you just want to track your existing Claude Skills.

**What if I don't have Notion set up?**
Claude will still follow the naming conventions, SOP templates, and documentation patterns — it just won't save to Notion. See [Notion Registry Setup](../builder-setup/notion-registry-setup.md) to configure the MCP connector.

**What's the difference between a Process Guide and an SOP?**
A Process Guide is strategic: when to execute, why it matters, what order the workflows go in. An SOP is tactical: step-by-step instructions for executing a single workflow. Think of the Process Guide as the playbook and SOPs as the play pages.
