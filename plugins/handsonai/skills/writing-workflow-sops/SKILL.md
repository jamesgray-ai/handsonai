---
name: writing-workflow-sops
description: Write Standard Operating Procedure documentation for workflows and save as markdown files. Selects full or lightweight SOP template based on autonomy level (deterministic vs. guided/autonomous), then adapts for workflow type (Manual, Augmented, Automated). Use when the user asks to write an SOP, document a workflow, create procedure documentation, or capture how a workflow is executed. Triggers on "write an SOP", "document this workflow", "create operating instructions", "how is this workflow executed".
user-invocable: true
---

# Writing Workflow SOPs

Write SOP documentation for workflows and save as markdown files, recording the SOP path in the workflow's Workflow node. External trackers are out of scope.

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

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
   - **From framework artifacts** (primary path): Read the workflow's Workflow node (`registry/workflows/<slug>.md`) for registry metadata (title, description, execution_mode, autonomy, trigger) and its `# Artifacts` links, then follow those links to the Workflow Requirements and Design Spec (normally `outputs/<name>/requirements.md` and `outputs/<name>/design-spec.md`) — or the legacy flat paths (`outputs/<name>-requirements.md`, `outputs/<name>-design-spec.md`) if no workflow folder exists. Extract refined steps, skill candidates, agent config, and failure modes from the documents.
   - **From conversation**: If no artifacts exist, gather workflow details interactively (name, purpose, trigger, type, steps, etc.)
2. **Classify on both axes** — Determine execution mode (augmented / automated / manual) and autonomy level (deterministic / guided / autonomous / n/a). If loaded from a Design Spec, these are already defined — confirm with user rather than re-assessing from scratch. Autonomy level determines full vs. lightweight SOP template.
3. **Gather any missing details** — Adapted to autonomy level: for deterministic, confirm procedure steps; for guided/autonomous, confirm human checkpoints and inputs/outputs
4. **Write SOP** using the appropriate template adapted for workflow type. Set `execution_mode` and `autonomy_level` in frontmatter, and include the taxonomy pair in the relevant section:
   - **Full SOPs** → add `**Execution Model:** <Mode> + <Level>` as the first line of the Automation Notes section
   - **Lightweight SOPs** → use `**<Mode> + <Level>**` as the bold label in the Execution Pattern section
5. **Write SOP markdown file** to the user's repo with YAML frontmatter. Default path: `sops/<workflow-name>-sop.md`. Ask the user where SOPs live in their repo if their project has a different convention.
6. **Update the Workflow node** — set the SOP link in the node's `# Artifacts` (label `SOP`) to the SOP path, then **create or update `REGISTRY.md`** at the workspace root (follow the `indexing-registry` procedure if available, otherwise update its tables directly from the registry data; skip only if the root isn't writable, and say so — never silently). Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step).

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
workflow: "<kebab-case-id>"  # back-pointer to the Workflow node's slug (omit for standalone SOPs)
owner: "<Your Name>"
last_reviewed: "YYYY-MM-DD"
execution_mode: augmented   # augmented | automated | manual
autonomy_level: guided      # deterministic | guided | autonomous | n/a
---
```

When a Workflow node exists, it is the source of truth for `execution_mode` and `autonomy`; `owner` resolves workflow → process → owning Function → `lead:` if set, else the Function's title (a snapshot, refreshed on regeneration) — copy those values at write time rather than re-deriving them. Standalone SOPs (no Workflow node) carry them independently; the AI Registry index picks such SOPs up via this frontmatter.

## Writing Guidelines

- Start procedure steps with action verbs
- One action per step (no "and then")
- Include decision points as explicit branches
- Add tips only for non-obvious gotchas
- Keep troubleshooting to common issues only

## Interaction Pattern

### From framework artifacts (primary path)
1. Read the Workflow node, Workflow Requirements, and Design Spec from the `outputs/` folder
2. Confirm classification (execution mode + autonomy level) with user
3. Fill any gaps not covered by the artifacts
4. Draft SOP using the appropriate template and present for review
5. Write markdown file after user approval
6. Set the SOP link in the Workflow node's `# Artifacts` and refresh `REGISTRY.md`; then invoke `indexing-registry` for a maintenance pass

### From scratch
1. Gather workflow details conversationally (name, purpose, trigger, type, steps)
2. Classify on both axes
3. Draft SOP using the appropriate template
4. Write markdown file after approval
