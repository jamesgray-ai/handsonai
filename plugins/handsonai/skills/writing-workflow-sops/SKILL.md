---
name: writing-workflow-sops
description: >-
  Write Standard Operating Procedure documentation for workflows and save it as a Markdown file.
  Selects a full or lightweight SOP template by autonomy level (deterministic vs. guided or
  autonomous), then adapts it for workflow type (Manual, Augmented, Automated). Use when the
  user asks to write an SOP, document a workflow, create procedure documentation, or capture how
  a workflow is executed, and when the test skill offers a team workflow's SOP at go-live and the
  user says yes. Triggers on "write an SOP", "document this workflow", "create operating
  instructions", "how is this workflow executed".
---

# Writing Workflow SOPs

Write SOP documentation for workflows and save it as Markdown, recording the SOP path in the workflow's Workflow node where there's a registry. External trackers are out of scope.

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the registry bundle (`registry/` in the workspace on Claude Code and Codex; `registry/` inside the framework folder on Claude desktop; `Framework/registry/` in the user's drive on the web and in Microsoft 365, written through the connection) — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. With no `registry/SCHEMA.md`, write no registry entry: save the SOP anyway. When the user came on their own (not from the test skill's offer), mention once that the `scaffolding-registry` skill sets a registry up.

> **Arriving from the test skill.** For a team workflow, the test skill offers an SOP at go-live (and at a re-check where someone on the team is stuck), tells the user where it will be saved, and on a yes runs this skill. The user has already agreed and heard the location, so don't ask where SOPs live, and don't ask the user to confirm the execution mode or autonomy level: the Design Plan and the Workflow node settle both. Read the workflow's files (step 1), draft the SOP, show it, and save it as `[workflow-slug]-sop.md` in the workflow's folder in the framework folder (step 5) once the user is happy with it. Never save it in the workflow's own place, where the workflow runs.
>
> **From Test, the SOP the user sees and saves uses only plain words.** Keep `execution_mode` and `autonomy_level` in its frontmatter, but put no taxonomy label in the body: leave out step 4's `**Execution Model:** <Mode> + <Level>` line and use "How it runs" as the Execution Pattern section's label, never `**<Mode> + <Level>**`; never write "Augmented", "Automated", "autonomy", "deterministic" or "guided", a requirement or task ID, or a framework step number. Give no time estimates, for a Manual SOP either. Skip step 6 (no SOP link on the Workflow node and no registry refresh: the framework's node links don't include one). When it's saved, say so in one line and hand back: the test skill carries on with its next go-live step.

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
(you give instructions)  (bounded decisions, your method)  (you give a goal)
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
| **Augmented** | Launch email sequence — fixed skill order, human reviews each | Course concept development — agent decides which skill to re-run based on instructor feedback, by the process you set (guided) |
| **Automated** | Student enrollment provisioning — webhook triggers fixed pipeline | (future) Self-healing deployment monitor (autonomous) |

## Process

1. **Load workflow context** — Determine how the user is arriving:
   - **From framework files** (primary path): Where there's a registry, read the workflow's Workflow node (`registry/workflows/<slug>.md`) for its title, description, `execution_mode`, `autonomy` and `trigger`. Then read three files in the workflow's folder in the framework folder (`framework/<slug>/` on Claude Code and Codex; `<slug>/` in the framework folder the user added on Claude desktop; `Framework/<slug>/` in the user's drive on the web and in Microsoft 365, through the connection):
     - `requirements.md` (the node's "Requirements" link): the steps, the rules it follows ("It always…", "It never…", the R lines), the checkpoints where it asks first (the G lines), its inputs and what it must get right.
     - `design-plan.md` (the node's "Design plan" link): the tasks, and the component blueprints (which skill or agent does what, and how they hand work on). The plan refers to requirement lines by ID and copies nothing, so take each rule's or checkpoint's wording from `requirements.md`.
     - `build-record.md` (found by its path; it has no link): from its top section, what was built and where it lives, how to start it, what it can access and what it never does, and, once it's live, "Live since" and "How to switch it off".

     Never read a `design-spec.md`, or anything in the folder's `history/`: those are earlier versions and earlier copies. If the folder holds no `design-plan.md` or no `build-record.md` yet, write from what's there and gather the rest from the user.
   - **From conversation**: If no artifacts exist, gather workflow details interactively (name, purpose, trigger, type, steps, etc.)
2. **Classify on both axes** — Determine execution mode (augmented / automated / manual) and autonomy level (deterministic / guided / autonomous / n/a). If loaded from a Design Plan, these are already defined: the plan's `autonomy` (and the Workflow node's `autonomy` and `execution_mode`, which Design sets on approval); with no registry, the requirements' `Runs:` line gives the mode (`Runs: without you` is automated; `Runs: with you` is manual or augmented). Use them rather than re-assessing from scratch, and confirm them with the user only when the user came on their own. Autonomy level determines full vs. lightweight SOP template.
3. **Gather any missing details** — Adapted to autonomy level: for deterministic, confirm procedure steps; for guided/autonomous, confirm human checkpoints and inputs/outputs
4. **Write SOP** using the appropriate template adapted for workflow type (from the test skill, the plain-words rule above overrides this step's labels). Set `execution_mode` and `autonomy_level` in frontmatter, and include the taxonomy pair in the relevant section:
   - **Full SOPs** → add `**Execution Model:** <Mode> + <Level>` as the first line of the Automation Notes section
   - **Lightweight SOPs** → use `**<Mode> + <Level>**` as the bold label in the Execution Pattern section
5. **Save the SOP** as Markdown with YAML frontmatter:
   - **A workflow with a framework folder** (always, when the test skill hands over): `[workflow-slug]-sop.md` in the workflow's folder in the framework folder, beside its `requirements.md` (`framework/<slug>/<slug>-sop.md` on Claude Code and Codex; `<slug>/<slug>-sop.md` in the framework folder on Claude desktop; `Framework/<slug>/<slug>-sop.md` on the web and in Microsoft 365, written through the drive connection). Never in the workflow's own place.
   - **Any other workflow:** default path `sops/<workflow-name>-sop.md`. Ask the user where SOPs live if their project has a different convention.
   - **On a drive** that can only create files, follow the drive-saving rule in `indexing-registry/references/registry-bundle.md` (section 2, rule 8). **With no files and no drive connection that can write,** give the SOP complete, with its location, and say plainly that the user must save it; never say it's saved when you only gave it.
6. **Update the Workflow node** (only where there's a registry, and never when the test skill handed over) — set the SOP link in the node's `# Artifacts` (label `SOP`), relative to the registry's parent folder as the bundle's link rule says (`framework/<slug>/<slug>-sop.md` on Claude Code and Codex; `<slug>/<slug>-sop.md` on the web and Claude desktop), and restamp `generated` (`by: process:writing-workflow-sops`, `at` a UTC instant, `YYYY-MM-DDTHH:MM:SSZ`). Then **create or update `REGISTRY.md`** beside `registry/`, in its parent folder (follow the `indexing-registry` procedure if available, otherwise update its tables directly from the registry data; on print-to-save, give it with its location, and say so — never silently). Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step).

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
- **Manual**: Detailed human steps, time estimates (never from the test skill), exact UI paths
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
- Write for the team in plain words: no requirement or task IDs (AC1, R3, G2, T4), and no framework step numbers

## Interaction Pattern

### From framework artifacts (primary path)
1. Read the Workflow node (where there's a registry), the Workflow Requirements, the Design Plan and the build record from the workflow's folder in the framework folder
2. Confirm classification (execution mode + autonomy level) with the user — skipped when the test skill handed over
3. Fill any gaps not covered by the files
4. Draft SOP using the appropriate template and present for review
5. Save it as `[workflow-slug]-sop.md` in the workflow's folder after user approval
6. Where there's a registry, set the SOP link in the Workflow node's `# Artifacts` and refresh `REGISTRY.md`; then invoke `indexing-registry` for a maintenance pass

### From scratch
1. Gather workflow details conversationally (name, purpose, trigger, type, steps)
2. Classify on both axes
3. Draft SOP using the appropriate template
4. Write markdown file after approval
