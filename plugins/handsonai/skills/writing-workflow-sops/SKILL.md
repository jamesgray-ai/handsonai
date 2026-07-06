---
name: writing-workflow-sops
description: Write Standard Operating Procedure documentation for workflows and save as markdown files. Selects full or lightweight SOP template based on autonomy level (deterministic vs. guided/autonomous), then adapts for workflow type (Manual, Augmented, Automated). Use when the user asks to write an SOP, document a workflow, create procedure documentation, or capture how a workflow is executed. Triggers on "write an SOP", "document this workflow", "create operating instructions", "how is this workflow executed".
user-invocable: true
---

# Writing Workflow SOPs

Write SOP documentation for workflows and save as markdown files, recording the SOP path in the workflow's `workflow.yaml` manifest (its AI Registry entry). Mirroring to an external tracker (Notion, Airtable, etc.) is optional.

## Two-Axis Workflow Model

Every workflow has two independent characteristics that determine how its SOP should be written:

### Axis 1 — Workflow Type (who does the work)

| Type | Definition |
|------|-----------|
| Manual | Human does all steps |
| Augmented | Human + AI collaborate |
| Automated | System does all steps, human monitors |

### Axis 2 — Autonomy Level (where on the spectrum)

The AI Workflow Framework defines a single autonomy spectrum used at both the per-step and whole-workflow level:

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
   - **From framework artifacts** (primary path): Read the workflow's manifest (`outputs/<name>/workflow.yaml`) for registry metadata (display name, description, type, autonomy, owner, trigger, apps), then the Workflow Requirements (`outputs/<name>/requirements.md`) and Design Spec (`outputs/<name>/design-spec.md`) — or the legacy flat paths (`outputs/<name>-requirements.md`, `outputs/<name>-design-spec.md`) if no workflow folder exists. Extract refined steps, skill candidates, agent config, and failure modes from the documents.
   - **From an external tracker** (only if the user keeps one): Fetch the workflow record for supplementary metadata — but prefer the manifest when both exist; it is the source of truth.
   - **From conversation**: If no artifacts exist, gather workflow details interactively (name, purpose, trigger, type, steps, etc.)
2. **Classify on both axes** — Determine execution mode (augmented / automated / manual) and autonomy level (deterministic / guided / autonomous / n/a). If loaded from a Design Spec, these are already defined — confirm with user rather than re-assessing from scratch. Autonomy level determines full vs. lightweight SOP template.
3. **Gather any missing details** — Adapted to autonomy level: for deterministic, confirm procedure steps; for guided/autonomous, confirm human checkpoints and inputs/outputs
4. **Write SOP** using the appropriate template adapted for workflow type. Set `execution_mode` and `autonomy_level` in frontmatter, and include the taxonomy pair in the relevant section:
   - **Full SOPs** → add `**Execution Model:** <Mode> + <Level>` as the first line of the Automation Notes section
   - **Lightweight SOPs** → use `**<Mode> + <Level>**` as the bold label in the Execution Pattern section
5. **Write SOP markdown file** to the user's repo with YAML frontmatter. Default path: `sops/<workflow-name>-sop.md`. Ask the user where SOPs live in their repo if their project has a different convention.
6. **Update the manifest** — set `artifacts.sop` in `outputs/<name>/workflow.yaml` to the SOP path, then refresh `REGISTRY.md` using the procedure in the `indexing-registry` skill (best-effort — never fail the step over it). If the manifest has a `notion_url`, also update the Notion Workflow row's SOP property (repo URL preferred) per the `indexing-registry` skill's `references/notion-mirror.md` (best-effort); for other external trackers, optionally update their SOP link too.

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
workflow: "<kebab-case-id>"  # back-pointer to outputs/<id>/workflow.yaml (omit for standalone SOPs)
owner: "<Your Name>"
last_reviewed: "YYYY-MM-DD"
execution_mode: augmented   # augmented | automated | manual
autonomy_level: guided      # deterministic | guided | autonomous | n/a
notion_workflow_url: ""      # optional — Notion page URL if you mirror to Notion
---
```

When a manifest exists, it is the source of truth for `owner`, `execution_mode`, and `autonomy_level` — copy those values from the manifest at write time rather than re-deriving them. Standalone SOPs (no manifest) carry them independently; the AI Registry index picks such SOPs up via this frontmatter.

## Writing Guidelines

- Start procedure steps with action verbs
- One action per step (no "and then")
- Include decision points as explicit branches
- Add tips only for non-obvious gotchas
- Keep troubleshooting to common issues only

## External Tracker Mirror (Optional)

The AI Registry (manifest + generated `REGISTRY.md`) is the primary record. If the user mirrors to the Notion AI Registry, the SOP link lands in the Workflow entry's SOP property (repo URL preferred — see the `indexing-registry` skill's `references/notion-mirror.md`). For Airtable or other trackers, update that tracker's SOP link property to point to the markdown file after writing it. Either way, the Markdown files remain the source of truth.

## Interaction Pattern

### From framework artifacts (primary path)
1. Read the manifest, Workflow Requirements, and Design Spec from the `outputs/` folder
2. Confirm classification (execution mode + autonomy level) with user
3. Fill any gaps not covered by the artifacts
4. Draft SOP using the appropriate template and present for review
5. Write markdown file after user approval
6. Update `artifacts.sop` in the manifest and refresh `REGISTRY.md`; optionally update an external tracker link

### From an external tracker
1. Fetch workflow record for context (name, type, trigger, etc.)
2. Classify on both axes — determine full vs. lightweight template
3. Gather procedure details or checkpoint details from user
4. Draft SOP and present for review
5. Write markdown file; update the manifest if one exists (or offer to create one) and refresh `REGISTRY.md`

### From scratch
1. Gather workflow details conversationally (name, purpose, trigger, type, steps)
2. Classify on both axes
3. Draft SOP using the appropriate template
4. Write markdown file after approval
