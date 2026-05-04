---
name: writing-workflow-sops
description: Write Standard Operating Procedure documentation for workflows and save as markdown files. Selects full or lightweight SOP template based on autonomy level (deterministic vs. guided/autonomous), then adapts for workflow type (Manual, Augmented, Automated). Use when the user asks to write an SOP, document a workflow, create procedure documentation, or capture how a workflow is executed. Triggers on "write an SOP", "document this workflow", "create operating instructions", "how is this workflow executed".
user-invocable: true
---

# Writing Workflow SOPs

Write SOP documentation for workflows and save as markdown files, with optional linking to a workflow tracker (Notion, Airtable, etc.).

## Two-Axis Workflow Model

Every workflow has two independent characteristics that determine how its SOP should be written:

### Axis 1 — Workflow Type (who does the work)

| Type | Definition |
|------|-----------|
| Manual | Human does all steps |
| Augmented | Human + AI collaborate |
| Automated | System does all steps, human monitors |

### Axis 2 — Autonomy Level (where on the spectrum)

The Business-First AI Framework defines a single autonomy spectrum used at both the per-step and whole-workflow level:

```
Deterministic ———————— Guided ———————— Autonomous
(fixed path)       (bounded decisions)     (context-driven path)
```

For SOP template selection, the spectrum maps to a binary choice:

| Autonomy Level | SOP Weight |
|---------------|------------|
| **Deterministic** | **Full SOP** — documents every step, branch, and decision point |
| **Guided or Autonomous** | **Lightweight SOP** — documents how to invoke, human checkpoints, inputs/outputs |

**The key test:** Can the executor change its path at runtime based on what it encounters? If yes (guided or autonomous) → lightweight SOP. If no (deterministic) → full SOP.

An agent can orchestrate at any autonomy level. An agent that runs a fixed script (step 1 → step 2 → step 3, no branching) is still deterministic and gets a full SOP. An agent that backtracks, re-invokes skills based on feedback, or adapts its sequence is guided or autonomous and gets a lightweight SOP.

### Examples across the matrix

| | Deterministic | Guided / Autonomous |
|---|---|---|
| **Manual** | Invoicing — same steps every time | — |
| **Augmented** | Launch email sequence — fixed skill order, human reviews each | Course concept development — agent backtracks and re-invokes skills based on instructor feedback (autonomous) |
| **Automated** | Student enrollment provisioning — webhook triggers fixed pipeline | (future) Self-healing deployment monitor (autonomous) |

## Process

1. **Load workflow context** — Determine how the user is arriving:
   - **From framework artifacts** (primary path): Read the Workflow Definition (`outputs/<name>-definition.md`) and Building Block Spec (`outputs/<name>-building-block-spec.md`). Extract name, description, trigger, type, execution mode, autonomy level, refined steps, skill candidates, agent config, and failure modes.
   - **From Notion or another tracker** (if available): Fetch the workflow record for supplementary metadata (name, description, type, trigger, apps, assets used).
   - **From conversation**: If no artifacts exist, gather workflow details interactively (name, purpose, trigger, type, steps, etc.)
2. **Classify on both axes** — Determine execution mode (augmented / automated / manual) and autonomy level (deterministic / guided / autonomous / n/a). If loaded from a Building Block Spec, these are already defined — confirm with user rather than re-assessing from scratch. Autonomy level determines full vs. lightweight SOP template.
3. **Gather any missing details** — Adapted to autonomy level: for deterministic, confirm procedure steps; for guided/autonomous, confirm human checkpoints and inputs/outputs
4. **Write SOP** using the appropriate template adapted for workflow type. Set `execution_mode` and `autonomy_level` in frontmatter, and include the taxonomy pair in the relevant section:
   - **Full SOPs** → add `**Execution Model:** <Mode> + <Level>` as the first line of the Automation Notes section
   - **Lightweight SOPs** → use `**<Mode> + <Level>**` as the bold label in the Execution Pattern section
5. **Write SOP markdown file** to the user's repo with YAML frontmatter. Default path: `sops/<workflow-name>-sop.md`. Ask the user where SOPs live in their repo if their project has a different convention.
6. **Optionally update workflow tracker** — If the user tracks workflows in Notion, Airtable, or another tool, update the workflow's SOP link to point to the markdown file after writing it.

## Template Selection

See `references/sop-template.md` for full template structures.

### Full SOP (Deterministic autonomy level)

Used when the workflow follows a fixed sequence regardless of context. The SOP *is* the process definition.

| Section | Purpose |
|---------|---------|
| Overview | 1-2 sentence summary |
| Prerequisites | Access, data, tools needed |
| Trigger | When/how workflow starts |
| Procedure | Step-by-step instructions |
| Outputs | Deliverables with destinations |
| Quality Checks | Success verification |
| Troubleshooting | Common problems + fixes |
| Automation Notes | For Augmented/Automated only |

Then apply **type adaptations**:
- **Manual**: Detailed human steps, time estimates, exact UI paths
- **Augmented**: Mark steps as (AI) or (Human), include handoff points
- **Automated**: Focus on monitoring, intervention points, error handling

### Lightweight SOP (Guided or Autonomous autonomy level)

Used when the executor adapts its path at runtime. The agent's system prompt *is* the process definition — the SOP documents the human interface.

| Section | Purpose |
|---------|---------|
| Overview | 1-2 sentence summary + key principle |
| Execution Pattern | Names the agent + describes the division of labor |
| How to Start | Invocation command + what to have ready |
| Your Role at Each Checkpoint | Human decision points only — not the full step sequence |
| Outputs | Deliverables with destinations |
| When to Skip the Agent | When to run individual skills/steps directly |
| Related | Links to agent file, upstream/downstream workflows |

**Why lightweight?** The agent definition owns the step sequence, skill invocations, and constraints. Duplicating that logic in the SOP creates drift. The SOP's job is to tell a human how to *work with* the agent — not to re-describe what the agent does internally.

### YAML Frontmatter

```yaml
---
title: "<Workflow Name>"
owner: "<Your Name>"
last_reviewed: "YYYY-MM-DD"
execution_mode: augmented   # augmented | automated | manual
autonomy_level: guided      # deterministic | guided | autonomous | n/a
notion_workflow_url: ""      # optional — Notion page URL if you use the AI Registry
---
```

## Writing Guidelines

- Start procedure steps with action verbs
- One action per step (no "and then")
- Include decision points as explicit branches
- Add tips only for non-obvious gotchas
- Keep troubleshooting to common issues only

## Workflow Tracker Integration (Optional)

If you use Notion, Airtable, or another tool to track workflows, update the workflow's SOP link property to point to the markdown file after writing it. This keeps your tracker in sync with the source-of-truth markdown files.

For Notion users with the AI Registry template: update the "SOP" URL property on the workflow's page to point to your markdown file's URL (e.g., GitHub, GitLab, or local path).

## Interaction Pattern

### From framework artifacts (primary path)
1. Read the Workflow Definition and Building Block Spec from the `outputs/` folder
2. Confirm classification (execution mode + autonomy level) with user
3. Fill any gaps not covered by the artifacts
4. Draft SOP using the appropriate template and present for review
5. Write markdown file after user approval
6. Optionally update workflow tracker link

### From Notion or another tracker
1. Fetch workflow record for context (name, type, trigger, etc.)
2. Classify on both axes — determine full vs. lightweight template
3. Gather procedure details or checkpoint details from user
4. Draft SOP and present for review
5. Write markdown file and update tracker link after approval

### From scratch
1. Gather workflow details conversationally (name, purpose, trigger, type, steps)
2. Classify on both axes
3. Draft SOP using the appropriate template
4. Write markdown file after approval
