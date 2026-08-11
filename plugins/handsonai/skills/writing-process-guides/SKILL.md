---
name: writing-process-guides
description: Write Business Process Guide documentation that explains when, why, and how to execute a complete business process with its component workflows, and save as markdown files. Use when documenting a business process end-to-end, creating playbooks, or explaining how multiple workflows fit together. Triggers on "write process guide", "document this process", "create a playbook for", "how do these workflows connect".
user-invocable: true
---

# Writing Business Process Guides

Write comprehensive Business Process Guide documentation and save as markdown files. The guide file **is** the business process's AI Registry record — the generated `REGISTRY.md` groups workflows under processes using the guide's frontmatter, and the guide's path is set as `guide:` frontmatter on the Process node itself. External trackers are out of scope. Process guides explain the strategic context and rhythm of a complete business process, while individual workflow SOPs handle the tactical execution details.

## Process Guide vs Workflow SOP

| Aspect | Process Guide | Workflow SOP |
|--------|---------------|--------------|
| Level | Strategic | Tactical |
| Scope | Multiple workflows | Single workflow |
| Answers | When/Why/What order | How (step-by-step) |
| Audience | Decision-maker | Executor |
| Length | 1-2 pages | Detailed steps |

## Process

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists. In addition, this skill's primary record is the Process node itself: set `guide:` frontmatter on `registry/processes/<slug>.md` pointing at the guide file.

1. **Load process context** — Determine how the user is arriving:
   - **From the AI Registry** (primary path): Read the Process node's (`registry/processes/<slug>.md`) curated `# Workflows` list for its component workflows. Read each linked Workflow node for trigger and status, plus its Workflow Requirements, Design Spec, and SOP where they exist (via the node's `# Artifacts` links).
   - **From conversation**: If no artifacts exist, gather process details interactively (name, component workflows, sequence, triggers).
2. **Gather strategic context** from user — frequency, timing, decision points between workflows, success criteria
3. **Write Process Guide** using template
4. **Write process guide markdown file** to user's repo with YAML frontmatter. Default path: `process-guides/<name>.md`. Ask the user where process guides live if their project has a different convention.
5. **Create or update `REGISTRY.md`** at the workspace root so the process appears with its workflows — follow the `indexing-registry` procedure if available, otherwise update its tables directly from the guide and registry data (skip only if the root isn't writable, and say so — never silently). Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step).

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
---
```

The `title` is the join key: it's the Process node's own title, and the Process node's curated `# Workflows` list — not this frontmatter — is what determines which workflows belong to it. Single-home rule: the Process node owns the workflow list (order and membership), and the owning Function (via the Process node's `owner:`) expresses domain — neither is duplicated here.

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

## Interaction Pattern

### From the AI Registry (primary path)
1. Find the process's workflows via the Process node's `# Workflows` list / `REGISTRY.md`; read Workflow Requirements (and SOPs/Design Specs if they exist) for each
2. Gather strategic context from user (frequency, timing, decision points)
3. Draft Process Guide and present for review
4. Write markdown file after user approval
5. Set `guide:` on the Process node, refresh `REGISTRY.md`, then invoke `indexing-registry` for a maintenance pass

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
