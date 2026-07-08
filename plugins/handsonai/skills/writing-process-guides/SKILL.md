---
name: writing-process-guides
description: Write Business Process Guide documentation that explains when, why, and how to execute a complete business process with its component workflows, and save as markdown files. Use when documenting a business process end-to-end, creating playbooks, or explaining how multiple workflows fit together. Triggers on "write process guide", "document this process", "create a playbook for", "how do these workflows connect".
user-invocable: true
---

# Writing Business Process Guides

Write comprehensive Business Process Guide documentation and save as markdown files. The guide file **is** the business process's AI Registry record — the generated `REGISTRY.md` groups workflows under processes using the guide's frontmatter. Mirroring to an external tracker (Notion, Airtable, etc.) is optional. Process guides explain the strategic context and rhythm of a complete business process, while individual workflow SOPs handle the tactical execution details.

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
   - **From the AI Registry** (primary path): Find the process's workflows by scanning `outputs/*/workflow.yaml` manifests for matching `business_process` values (or read the Workflows section of `REGISTRY.md`). Read each workflow's manifest for sequence, trigger, and status, plus its Workflow Requirements, Design Spec, and SOP where they exist.
   - **From an external tracker** (only if the user keeps one): Fetch the business process record and its linked workflows for supplementary metadata — but prefer manifests when both exist.
   - **From conversation**: If no artifacts exist, gather process details interactively (name, component workflows, sequence, triggers).
2. **Gather strategic context** from user — frequency, timing, decision points between workflows, success criteria
3. **Write Process Guide** using template
4. **Write process guide markdown file** to user's repo with YAML frontmatter. Default path: `process-guides/<name>.md`. Ask the user where process guides live if their project has a different convention.
5. **Create or update `REGISTRY.md`** at the workspace root so the process appears with its workflows — follow the `indexing-registry` procedure if available, otherwise update its tables directly from the guide and manifests (skip only if the root isn't writable, and say so — never silently). If the user mirrors to the Notion AI Registry, update the Processes database entry's Guide property (see the `indexing-registry` skill's `references/notion-mirror.md`); for other trackers, optionally update their guide link too.

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
domain: "<Sales | Marketing | Product | Education | Consulting | Operations | Finance>"
owner: "<Your Name>"
last_reviewed: "YYYY-MM-DD"
workflows: []            # optional — kebab-case workflow IDs, for explicit ordering
notion_process_url: ""   # optional — Notion page URL if you mirror to Notion
---
```

The `title` is the join key: workflows belong to this process when their manifest's `business_process` matches it. `domain` classifies the process in the AI Registry. `workflows` is only needed when explicit ordering matters beyond the manifests' `sequence` numbers.

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

## External Tracker Mirror (Optional)

The AI Registry (guide frontmatter + generated `REGISTRY.md`) is the primary record. If the user mirrors to the Notion AI Registry, the guide maps to the Processes database — update its Guide property to point to the markdown file (see the `indexing-registry` skill's `references/notion-mirror.md`). For Airtable or other trackers, update that tracker's guide link property. Either way, the Markdown files remain the source of truth.

## Interaction Pattern

### From the AI Registry (primary path)
1. Find the process's workflows via manifests / `REGISTRY.md`; read Workflow Requirements (and SOPs/Design Specs if they exist) for each
2. Gather strategic context from user (frequency, timing, decision points)
3. Draft Process Guide and present for review
4. Write markdown file after user approval
5. Refresh `REGISTRY.md`; optionally update an external tracker link

### From an external tracker
1. Fetch business process record and linked workflows for context
2. Fetch each linked workflow for sequence/trigger details
3. Ask clarifying questions about timing and decision points
4. Draft Process Guide and present for review
5. Write markdown file, refresh `REGISTRY.md`, and update the tracker link after approval

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
