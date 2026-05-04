---
name: writing-process-guides
description: Write Business Process Guide documentation that explains when, why, and how to execute a complete business process with its component workflows, and save as markdown files. Use when documenting a business process end-to-end, creating playbooks, or explaining how multiple workflows fit together. Triggers on "write process guide", "document this process", "create a playbook for", "how do these workflows connect".
user-invocable: true
---

# Writing Business Process Guides

Write comprehensive Business Process Guide documentation and save as markdown files, with optional linking to a process tracker (Notion, Airtable, etc.). Process guides explain the strategic context and rhythm of a complete business process, while individual workflow SOPs handle the tactical execution details.

## Process Guide vs Workflow SOP

| Aspect | Process Guide | Workflow SOP |
|--------|---------------|--------------|
| Level | Strategic | Tactical |
| Scope | Multiple workflows | Single workflow |
| Answers | When/Why/What order | How (step-by-step) |
| Audience | Decision-maker | Executor |
| Length | 1-2 pages | Detailed steps |

## Process

1. **Load process context** — Determine how the user is arriving:
   - **From framework artifacts** (primary path): Read the Workflow Definitions for each component workflow (`outputs/<name>-definition.md`). If Building Block Specs and SOPs exist, read those too for sequencing, autonomy levels, and cross-references.
   - **From Notion or another tracker** (if available): Fetch the business process record and its linked workflows for supplementary metadata (name, domain, description, linked workflows).
   - **From conversation**: If no artifacts exist, gather process details interactively (name, component workflows, sequence, triggers).
2. **Gather strategic context** from user — frequency, timing, decision points between workflows, success criteria
3. **Write Process Guide** using template
4. **Write process guide markdown file** to user's repo with YAML frontmatter. Default path: `process-guides/<name>.md`. Ask the user where process guides live if their project has a different convention.
5. **Optionally update process tracker** — If the user tracks business processes in Notion, Airtable, or another tool, update the process's guide link to point to the markdown file after writing it.

## Template Overview

See `references/process-guide-template.md` for full template structure. Core sections:

| Section | Purpose |
|---------|---------|
| Purpose | Why this process exists and business impact |
| When to Execute | Triggers, frequency, timing |
| Process Overview | Visual flow of workflows |
| Workflow Sequence | Each workflow with trigger, duration, output |
| Decision Points | Key choices during the process |
| Success Criteria | How to know the process worked |
| Common Pitfalls | What typically goes wrong |
| Orchestrator Agent (optional) | If an agent exists that runs this process end-to-end, name it and describe how to invoke it |

### YAML Frontmatter

```yaml
---
title: "<Process Name>"
owner: "<Your Name>"
last_reviewed: "YYYY-MM-DD"
notion_process_url: ""   # optional — Notion page URL if you use the AI Registry
---
```

## SOP Cross-References

In the Workflow Sequence section, SOP links should use **relative repo paths** pointing to the SOP markdown files:

```markdown
> SOP: [<Workflow Name> SOP](../sops/<workflow-name>-sop.md)
```

If the SOP file doesn't exist yet, note it as pending:

```markdown
> SOP: _Not yet documented — [Workflow Name] SOP will be written separately_
```

## Writing Guidelines

- Focus on the "why" and "when", not the "how" (that's in the SOPs)
- Include time estimates for the overall process
- Highlight decision points and branching logic
- Connect to business outcomes and metrics
- Keep it scannable - someone should grasp the process in 2 minutes
- If the process has an orchestrator agent, include a "How to Run" section that names the agent, shows the invocation, and explains that the agent handles sequencing, progress tracking, and skill invocation

## Process Tracker Integration (Optional)

If you use Notion, Airtable, or another tool to track business processes, update the process's guide link property to point to the markdown file after writing it. This keeps your tracker in sync with the source-of-truth markdown files.

For Notion users with the AI Registry template: update the "Guide" URL property on the business process page to point to your markdown file's URL.

## Interaction Pattern

### From framework artifacts (primary path)
1. Read Workflow Definitions (and SOPs/Building Block Specs if they exist) for each component workflow
2. Gather strategic context from user (frequency, timing, decision points)
3. Draft Process Guide and present for review
4. Write markdown file after user approval
5. Optionally update process tracker link

### From Notion or another tracker
1. Fetch business process record and linked workflows for context
2. Fetch each linked workflow for sequence/trigger details
3. Ask clarifying questions about timing and decision points
4. Draft Process Guide and present for review
5. Write markdown file and update tracker link after approval

### From scratch
1. Gather process details conversationally (name, component workflows, sequence, triggers)
2. Gather strategic context (frequency, timing, decision points)
3. Draft Process Guide using template
4. Write markdown file after approval

### When workflows don't have SOPs yet
1. Note which workflows need SOPs
2. Recommend writing SOPs first or in parallel
3. Process Guide uses relative path placeholders: `../sops/<workflow-name>-sop.md`
4. Pending SOPs noted as: `_Not yet documented — [Workflow Name] SOP will be written separately_`
