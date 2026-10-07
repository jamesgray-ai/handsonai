# Migrating Legacy Workspaces

Two legacy shapes feed into the same registry bundle: a `workflow.yaml`
manifest layout, and an older flat layout with no manifest at all. Both
migrations write the same kind of node — a `registry/workflows/<slug>.md`
file that lints clean against the student's `SCHEMA.md`.

## Detection

A workspace needs migration when either of these is true:

- `outputs/*/workflow.yaml` exists — the manifest layout.
- `outputs/<name>-requirements.md` exists with **no** matching
  `outputs/<name>/` folder — the flat layout (requirements files sitting
  directly in `outputs/`, not inside a per-workflow folder).

Run this check at Phase 0 of the scaffolding interview, before asking any
content questions. If either shape is found, offer the migration path
described here instead of (or before) a fresh scaffold.

## Procedure

**Prerequisite:** a migrated Workflow node only lints clean once its Business,
LineOfBusiness, Function, and Process nodes exist — scaffold those first.
Ask the student where the workflow belongs (which Process, which Function
owns it); the legacy manifest rarely says.

1. **Scaffold the bundle first if it doesn't exist yet** — `registry/` +
   `SCHEMA.md` + `index.md` + `log.md` + the six typed directories with stub
   `index.md` files (standard empty body — see the interview guide, Phase
   1). Migration writes nodes into this bundle; it never
   invents its own structure.
2. **Per workflow found:**
   a. Create the Workflow node — `registry/workflows/<slug>.md` — from the
      manifest (or, for flat layout, from the requirements doc; see below).
   b. Apply the disposition table below field by field.
   c. Delete the `workflow.yaml` only after its node lints clean against
      `SCHEMA.md` — never delete before verifying. If the environment will
      not let you delete, leave the file and say so in the `log.md` entry
      ("legacy manifest pending deletion") so the student removes it.
   d. Append one `log.md` entry for the whole migration run, naming every
      workflow migrated in that run (not one entry per workflow).
3. Slot each new Workflow node into its owning Process's curated
   `# Workflows` list, and its Process into the right LineOfBusiness — ask
   the student where a workflow belongs if the manifest doesn't say. When
   migrating a subset of a legacy manifest's workflows, order the
   `# Workflows` list by the legacy `sequence` values and write it as the
   usual unnumbered list — position is the sequence; the legacy numbers
   themselves (which may have gaps) are never written.

## Disposition table

| workflow.yaml field | Disposition |
|---|---|
| `workflow` | filename slug `registry/workflows/<slug>.md` |
| `display_name` | `title` |
| `description` | `description` (written outcome-first) |
| `process_outcome` | retired into outcome-first `description` (recorded, not lost) |
| `business_process`, `sequence` | line + position in the Process node's `# Workflows` list |
| `status` | `status`, kebab-case (`Archived` → `retired`) |
| `type` | `execution_mode` |
| `autonomy`, `trigger`, `definition_type` | same-named frontmatter |
| `owner` | derived: process → owning Function — use the legacy value to match (or name) that Function node, then drop the field |
| `platform` | dropped — the run guide usually names it; if no artifact does, carry it into the node's prose ("Runs on Claude Code.") rather than reviving a field |
| `health`, `last_run`, `current_step` | dropped (event-facts; step inferred from artifacts) |
| `last_updated` | `generated.at` (never the legacy `timestamp:` field the old manifest layout mapped to — `timestamp:` is a lint error; migration converts any encountered) |
| `next_review` | `stale_after` |
| `apps` | derived on demand from linked skills/agents (no maintained record); if neither a skill nor an agent resolves, carry the app names into the node's prose ("Uses Notion and Slack.") so they are not lost |
| `assets_used` | `# Skills` body links |
| `platform_artifacts` | `# Agents` body links |
| `artifacts:` map | `# Artifacts` labeled links |
| sibling `sops/<slug>-sop.md` (no legacy field) | `# Artifacts` link `- [SOP](sops/<slug>-sop.md)` — lint requires every SOP to be claimed by exactly one Workflow node |
| `notion_url` | dropped |

Field-level notes worth calling out during migration:

- **`definition_type` normalization.** Legacy manifests may carry
  `Step-Driven`, `Goal-Driven`, the retired `Outcome-Driven` spelling, or the
  retired `Step-Decomposed` spelling (in any casing). Normalize all of these
  to the current enum values — `step-driven` or `goal-driven` — on write.
  Never carry a legacy spelling into a new node.
- **`status` normalization.** Legacy manifests may use Title Case
  (`Backlog`, `Under Development`, `In Production`, `Archived`). Map to the
  kebab-case enum: `Archived` maps to `retired`, not to a status of its own
  — there is no legacy-to-new 1:1 for every value, so `Archived` is the one
  that changes meaning as well as case.
- **Unresolved `assets_used` / `platform_artifacts` names.** If a name in
  either legacy field resolves to no file on disk, record it as a
  plain-text entry (no link) under `# Skills` / `# Agents` — never fabricate
  a path to make a link work, and never drop the name just because it
  doesn't resolve.
- **`last_updated` → `generated.at` reconciliation.** A migrated node keeps
  the legacy `last_updated` date in `generated.at` — that's provenance, not
  a fresh write, so don't stamp today's date over it. A flat-layout
  migration has no `last_updated`: use the requirements file's own
  modification date, and today's date only if it cannot be read. `generated.by` is
  still `process:scaffolding-registry`. The stamp-today rule in this
  skill's Write rules applies to newly created nodes, not migrated ones.

## Flat layout

When there's no `workflow.yaml`, mint the node directly from what's on disk:

- Frontmatter comes from the requirements doc's own frontmatter where
  present, filled out from its filename otherwise (`<name>` from
  `outputs/<name>-requirements.md` becomes the slug and, title-cased, the
  `title`). `description` is required and no flat doc carries one: write it
  outcome-first from the doc's Goal or Outcome section and read it back to
  the student to confirm.
- `status: under-development` — a flat-layout workflow has requirements but
  no confirmed production status, so this is the honest default rather than
  a guess.
- Link the requirements file itself in `# Artifacts`:
  `- [Requirements](outputs/<name>-requirements.md)` (label as the link text —
  compose reads the framework step from it).
- All other frontmatter (`definition_type`, `execution_mode`, `autonomy`,
  `trigger`) comes from the doc where it states one (a `## Trigger` section,
  a stated path) — confirm it with the student — and from a short
  conversation otherwise; a flat requirements doc rarely states them all.

## Post-migration check

After every workflow in the run has a node:

1. Grep the migrated nodes for every banned field, scoped as
   `lint-registry.js` scopes it: the node files under `registry/*/`,
   excluding each directory's `index.md` (the root-level `SCHEMA.md`, which
   documents the banned list, and `log.md`, which records what was dropped,
   fall outside that glob already). The banned items are frontmatter *keys*, so grep for them at
   the start of a line (`^process:`, `^owner:`) — the strings `process` and
   `owner` also appear legitimately in every node's `generated: { by:
   process:… }` and in the required `owner:` on Process nodes:
   `current_step`, `health`, `last_run`, any run-counter key (`run_count`,
   `runs`, `total_runs`), `next_review`, `notion_url`, `timestamp`, `lob`,
   `sequence`, `process` (on any node), `owner` (on Workflow nodes) — and
   every other legacy key
   from the disposition table's left column that was renamed or dropped
   (`workflow`, `display_name`, `process_outcome`, `business_process`,
   `type`, `platform`, `last_updated`, `apps`, `assets_used`,
   `platform_artifacts`, `artifacts`). Expect zero matches — if
   anything turns up, it means a disposition step above was skipped or a
   legacy `timestamp:` field slipped through instead of being converted to
   `generated.at`.
2. **Claims sweep.** Every sibling SOP under `sops/` and every
   `outputs/<slug>/` folder must be linked from its owning Workflow node's
   `# Artifacts` section — lint errors on any SOP or outputs folder claimed
   by zero (or more than one) Workflow node. Fix the links before moving on.
3. Run a full maintenance pass (`indexing-registry`) so lint, directory
   indexes, and the Tier 1 dashboard reflect the migrated workflows before
   calling the migration done.
