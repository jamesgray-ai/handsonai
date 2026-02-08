---
name: registering-building-blocks
description: Register or update AI building blocks (Skills, Agents, Prompts, Context MDs) in the Notion AI Assets database. Use this skill immediately after creating, packaging, or updating any Claude building block to add or update it in the AI Assets tracking database. Triggers after skill creation, agent creation, prompt authoring, context MD updates, or when user asks to register/add/track a building block in Notion.
---

# Registering AI Building Blocks

After creating, packaging, or updating any AI building block — Skill, Agent, Prompt, or Context MD — register or update it in the AI Assets database.

## Asset Type Resolution

Determine the asset type from the user's request before extracting metadata.

| Asset Type | Source Location | Identifier File | Name Source |
|-----------|----------------|-----------------|-------------|
| Skill | `~/.claude/skills/{name}/SKILL.md` | `SKILL.md` frontmatter `name` field | Frontmatter `name` |
| Agent | `.claude/agents/{name}.md` or `~/.claude/agents/{name}.md` | Agent `.md` file frontmatter or filename | Filename (without `.md`) or frontmatter |
| Prompt | User-specified file or inline text | N/A | User-provided name |
| Context MD | `CLAUDE.md` or user-specified file | N/A | User-provided name or filename |

**Resolution rules:**

1. **Keywords in the user request** — "register this skill", "add this agent", "track this prompt", "register this context MD"
2. **File path patterns** — `SKILL.md` → Skill; `.claude/agents/*.md` → Agent; `CLAUDE.md` → Context MD
3. **If ambiguous** — Ask the user which asset type to use

## Database Reference

- **Data Source ID**: `2d5edcfd-b924-80cf-a0a0-000ba0164e40`
- **Data Source URL**: `collection://2d5edcfd-b924-80cf-a0a0-000ba0164e40`

## Schema

| Property | Type | Purpose |
|----------|------|---------|
| Name | title | Building block name (from frontmatter, filename, or user input) |
| Description | text | Description (from frontmatter or user input — includes trigger phrases for skills) |
| Asset Type | select | "Skill", "Agent", "Prompt", or "Context MD" |
| Platform | select | Always "Claude" for Claude building blocks |
| Quick Start Prompt | text | Copy-paste prompt that demonstrates the building block |
| GitHub | url | Repository URL if applicable |

## Process

For **each building block** being registered:

### Step 1: Extract Metadata

Based on the resolved asset type, read metadata from the appropriate source:

- **Skill** — Read `SKILL.md` frontmatter for `name` and `description`
- **Agent** — Read the agent `.md` file for name (filename or frontmatter) and description (opening paragraph or frontmatter)
- **Prompt** — Get name and description from the user or from the prompt file's content
- **Context MD** — Get name and description from the user; optionally summarize the file's purpose

### Step 2: Generate Quick Start Prompt

Create a single, copy-paste-ready prompt that demonstrates the building block's primary use case.

**Guidelines for Quick Start Prompts:**
- One sentence that triggers the building block's main workflow
- Specific enough to be immediately useful
- Generic enough to work across different contexts
- Should produce a complete result, not just start a conversation

**Examples by asset type:**

| Type | Name | Quick Start Prompt |
|------|------|--------------------|
| Skill | reviewing-student-goals | "Navigate to my Maven course Reflect: Goals page and extract all student learning goals. Update each student's record in Notion and give me a cohort theme analysis." |
| Skill | writing-linkedin-posts | "Write a LinkedIn post about [topic] using my brand voice." |
| Agent | cookbook-question-answerer | "Answer the question 'What are the six AI building blocks?' using the Hands-on AI site content." |
| Agent | hbr-editor | "Review this article for HBR publication quality and give me prescriptive feedback." |
| Prompt | meeting-prep-quick | "Prepare me for my meeting with [name] at [company] tomorrow." |

**Context MDs** typically don't need a Quick Start Prompt — leave blank or ask the user.

**If unsure**: Ask James for the Quick Start Prompt rather than guessing.

### Step 3: Search for Existing Entry

Search the data source for the **exact building block name**:

```json
{
  "query": "<building-block-name>",
  "data_source_url": "collection://2d5edcfd-b924-80cf-a0a0-000ba0164e40"
}
```

**Critical**: Check search results carefully. A match exists only if a result has the **exact same title** as the building block name. Partial matches or similar names are NOT duplicates.

### Step 4: Create or Update

**If exact match found** → Update the existing page:

```json
{
  "data": {
    "page_id": "<page-id-from-search>",
    "command": "update_properties",
    "properties": {
      "Description": "<description>",
      "Quick Start Prompt": "<generated-quick-start-prompt>"
    }
  }
}
```

**If no exact match** → Create new entry:

```json
{
  "parent": {"data_source_id": "2d5edcfd-b924-80cf-a0a0-000ba0164e40"},
  "pages": [{
    "properties": {
      "Name": "<building-block-name>",
      "Description": "<description>",
      "Asset Type": "<Skill|Agent|Prompt|Context MD>",
      "Platform": "Claude",
      "Quick Start Prompt": "<generated-quick-start-prompt>"
    }
  }]
}
```

## Batch Registration

When registering multiple building blocks (which can mix asset types):
1. Search for **each building block individually** before any creates/updates
2. Build two lists: items to update (with page IDs) and items to create
3. For each item, generate or request a Quick Start Prompt
4. Perform updates first, then batch create new entries
5. Report results: X created, Y updated (broken down by asset type)

## Notes

- Always confirm registration with the user after modifying Notion
- If the building block has a GitHub repository, include the URL in the **GitHub** property
- Never create entries without first checking for duplicates
- If you can't determine an appropriate Quick Start Prompt, ask James for one
