# Workflow Manifest Schema (`workflow.yaml`)

The manifest at `outputs/<workflow-name>/workflow.yaml` is both the framework's state file **and** the workflow's AI Registry entry — the single source of truth for all workflow-level registry metadata. Framework skills read it on load and update it after writing their outputs. The generated `REGISTRY.md` is built from these files.

Every field except `workflow` is optional. Skills fill in what they know at their step and leave the rest; the index renders missing values as `—`.

```yaml
# Identity ─ set by naming-workflows or deconstruct
workflow: lead-qualification      # kebab-case ID — names the folder and all artifacts (required)
display_name: Lead Qualification
description: >-                   # 1-2 sentence outcome-focused description
  Qualifies inbound leads against the ICP and produces a ranked list.
process_outcome: Ranked qualified-lead list   # the tangible deliverable

# Classification ─ set by naming-workflows / deconstruct / design
business_process: Sales Pipeline  # which business process this workflow belongs to
sequence: 10                      # order within the process (multiples of 10)
status: under-development         # backlog | under-development | in-production
type: augmented                   # augmented | automated | manual
autonomy: guided                  # deterministic | guided | autonomous (set by design)
trigger: "New lead in CRM"        # what kicks the workflow off
owner: "Jane Doe"                 # accountable person or role

# Operations ─ set by build / test / run / improve
platform: claude-code             # claude-code | cowork | claude-ai | scheduled-agent
health: working                   # working | needs-attention | broken
last_run: 2026-07-01              # date of most recent run
apps: [Gmail, HubSpot]            # integrations the workflow uses
assets_used: [drafting-outreach]  # skills/agents used, by frontmatter name

# Framework state ─ maintained by every step
definition_type: Step-Decomposed  # or Goal-Driven (legacy "Outcome-Driven" = Goal-Driven)
current_step: 4                   # last completed framework step (1-7); 0 = named only
last_updated: 2026-07-01
next_review: 2026-08-01           # set by run/improve
artifacts:
  requirements: outputs/lead-qualification/requirements.md
  sop: sops/lead-qualification-sop.md
  design_spec: outputs/lead-qualification/design-spec.md
  platform_artifacts:
    - outputs/lead-qualification/artifacts/drafting-outreach/SKILL.md
  test_results: outputs/lead-qualification/test-results.md
  run_guide: outputs/lead-qualification/run-guide.md
  run_log: outputs/lead-qualification/runs.md
  improvement_plan: outputs/lead-qualification/improvement-plan.md

# Optional mirror
notion_url: ""                    # back-pointer if the user mirrors to Notion
```

## Which skill writes which fields

| Skill | Writes |
|---|---|
| `naming-workflows` | `workflow`, `display_name`, `description`, `process_outcome`, `business_process`, `sequence`, `status`, `type`, `trigger` (creates a stub with `current_step: 0` when run before deconstruct) |
| `deconstruct` | `display_name`, `description`, `trigger`, `owner`, `status: under-development`, `definition_type`, `artifacts.requirements` — merging into any existing stub, never overwriting set fields |
| `design` | `type`, `autonomy`, `artifacts.design_spec` |
| `build` | `apps`, `assets_used`, `platform`, `artifacts.platform_artifacts` |
| `test` | initial `health`, `artifacts.test_results` |
| `run` | `status: in-production`, `health`, `last_run`, `next_review`, `artifacts.run_guide`, `artifacts.run_log` |
| `improve` | `health`, `artifacts.improvement_plan` |
| `writing-workflow-sops` | `artifacts.sop` |

Every skill also sets `current_step` and `last_updated` after writing its output, then refreshes `REGISTRY.md` (best-effort — see the main SKILL.md).

## Related frontmatter

**SOP files** (`sops/<name>-sop.md`) carry `workflow: <kebab-id>` as a back-pointer. When a manifest exists it is the source of truth for `owner`, `autonomy_level`, and `execution_mode` — the SOP-writing skill copies those values from the manifest at write time. Standalone SOPs (no manifest) may carry them independently.

**Process guides** (`process-guides/<name>.md`) carry `domain:` (Sales, Marketing, Operations, …) and optionally `workflows: [kebab-ids]`. The guide file is the record for the business process; workflows join to it via their `business_process` field matching the guide's `title`.
