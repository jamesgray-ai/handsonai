# Registry Bundle — the Shared Contract

Every framework skill treats the **AI registry bundle** as the single source of truth for
workflow registry metadata. This document defines how any skill *resolves* the bundle, *writes*
to it, *owns* particular fields, infers framework progress from artifacts, schedules review, and
lints the result — so the rules are stated once instead of per-skill. Every dispatch blockquote
in the ten framework skills points here rather than restating any of this.

---

## 1. Resolution

A workflow's registry entry is the **Workflow concept node**:

```
registry/workflows/<slug>.md
```

where `<slug>` is the workflow's kebab-case ID. The node is YAML frontmatter plus markdown body
sections, held inside an [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
knowledge bundle rooted at `registry/`.

The workspace's own `registry/SCHEMA.md` is **authoritative** for node structure, enums, and
lint rules. Read it before the first node write of any session, and defer to it if it ever
differs from anything restated here.

**If `registry/SCHEMA.md` does not exist**, the workspace has no bundle yet. Offer the
`scaffolding-registry` skill — it creates a new bundle, or migrates any legacy `workflow.yaml`
manifest or flat (non-bundle) layout it finds. Do not write registry entries of any kind until
the bundle exists.

---

## 2. Write rules

1. **Single-line frontmatter only.** No `>-`/`|` block scalars, no inline `#` comments, no
   multi-line values of any kind. If a description is long, shorten it — never wrap it in a
   block scalar.
2. **Stamp `generated` on every write.** Every node write (create or update) carries:

   ```yaml
   generated: { by: process:<skill-name>, at: <YYYY-MM-DD> }
   ```

   `<skill-name>` is the writing skill's own name (e.g. `process:deconstruct`); `<date>` is the
   write date.
3. **Never edit between GENERATED markers.** Content between `<!-- GENERATED:<name> -->` and
   `<!-- /GENERATED -->` is machine-owned — write around it, never inside it, and never leave a
   marker pair unterminated.
4. **Link discriminator, exact:**
   - Leading `/` — bundle-root-relative, resolved from `registry/` (e.g.
     `/processes/course-improvement.md`). The first path segment must be one of the bundle's
     directories or a root file.
   - No leading slash, not a URL — workspace/repo-root-relative (e.g.
     `outputs/course-improvement/sop.md`).
   - A full URL — external.
5. **A workflow joins exactly one Process** via that Process's curated ordered `# Workflows`
   list (`registry/processes/<process-slug>.md`) — the list is both the Workflow→Process edge
   and the value-chain sequence. Append at the end if the position is unknown. **Never write**
   `process:`, `owner:`, `lob:`, or `sequence:` on the Workflow node — the process membership,
   ownership, and line-of-business all derive from the parent list, never from a pointer stored
   on the child.
6. **Banned fields** — never write these into any node:

   `current_step`, `health`, `last_run`, `run_count` (and any run-counter field), `next_review`,
   `notion_url`, `timestamp`, `lob`, `sequence`, `process` (banned on any node), `owner` (banned
   on Workflow nodes — it lives on Process).

**Bundle-wide anchors (consistency-check anchors — restated here on purpose):**

- The bundle root `index.md` declares `okf_version: "0.2"` in its frontmatter — the one index
  permitted a frontmatter block.
- Full enum block, all values, lint-enforced:
  - Workflow `status`: `backlog` | `under-development` | `in-production` | `retired`
  - `definition_type`: `step-driven` | `goal-driven` (readers tolerate the legacy spellings
    `step-decomposed` and `outcome-driven` from earlier registry versions — never write either
    into a new node)
  - `execution_mode`: `manual` | `augmented` | `automated`
  - `autonomy`: `deterministic` | `guided` | `autonomous`

---

## 3. Field ownership table

| Skill | Writes |
|---|---|
| `naming-workflows` | Workflow node stub: `title`, `description` (outcome-first), `status: backlog`, `trigger`, `execution_mode`; line in the chosen Process's `# Workflows` list. **New process → asks which function owns it** and writes a complete minimal Process node (owner required — no stub violates the schema). |
| `deconstruct` | `status: under-development`, `definition_type` (step-driven/goal-driven), `trigger`, description refinement; `# Artifacts` → Requirements. Merges into stubs; never overwrites set fields. |
| `design` | `execution_mode`, `autonomy`; `# Artifacts` → Design spec |
| `build` | `# Skills` / `# Agents` links; `# Artifacts` → platform artifacts |
| `test` | `# Artifacts` → Test results (health lives in test-results.md, not the node) |
| `run` | `status: in-production`, `stale_after`; `# Artifacts` → Run guide, Run log |
| `improve` | `stale_after`; `# Artifacts` → Improvement plan; **a Note node when the review yields a durable insight, linked to the Workflow** |
| `writing-workflow-sops` | `# Artifacts` → SOP |
| `writing-process-guides` | Process node `guide:` frontmatter |

`scaffolding-registry` also writes provisional values for the schema-required fields
`definition_type`, `execution_mode`, and `autonomy` at Phase 5, so the first Workflow node lints
clean before Deconstruct or Design ever run. `deconstruct` and `design` still own those fields
going forward and may overwrite scaffold's provisional values with better-informed ones — the
never-overwrite rule above protects values a student has deliberately set through a framework
step, not a scaffold-time guess made to satisfy the schema. Similarly, `scaffolding-registry` may
set a Process node's `guide:` at scaffold time when an SOP already exists for it;
`writing-process-guides` owns the field thereafter.

---

## 4. Framework progress (artifact-presence inference)

There is no `current_step` field. A skill that needs to know "what step is next" infers it from
which artifacts the Workflow node's `# Artifacts` section already links:

| Artifact present | Step completed |
|---|---|
| Requirements | 2 (Deconstruct) |
| Design spec | 3 (Design) |
| Platform artifacts (skills/agents) | 4 (Build) |
| Test results | 5 (Test) |
| Run guide | 6 (Run) |

---

## 5. Review scheduling

Review scheduling is `stale_after` — a Workflow node frontmatter field holding a date
(`YYYY-MM-DD`). A workflow is **stale** when today's date is on or after `stale_after`.

`run` sets `stale_after` on go-live; `improve` resets it at the close of each review. These are
the only two skills that own the field.

`next_review` does not exist. It is a retired field — banned, never written, and appears in this
bundle and in every skill only as something that is gone.

---

## 6. Lint rule list

The single source both linters implement — the AI-performed pass in `indexing-registry` and the
scripted Tier 3 pass in `tools/lint-registry.js` (or the template repo's compose/lint tooling).
The consistency suite asserts string agreement between the two.

**Errors:**

- Missing required frontmatter
- Multi-line/block-scalar values
- Directory↔type disagreement
- Invalid enum values
- Banned fields present (event-facts + derived: `lob`/`sequence`/`process` anywhere, `owner` on
  Workflow, legacy `timestamp:`)
- Broken link targets
- In-bundle link whose first segment is not a bundle directory or root file
- Curated-list violations (a node in zero or 2+ parent lists; in-production Workflow in no
  Process list)
- Process `owner:` missing or matching no Function file
- Function node missing its GENERATED `# Owns` marker block
- Unterminated GENERATED block
- A concept file missing from its directory index, or a typed directory missing its `index.md`
  (index coverage)
- **Claims sweep** — an SOP or `outputs/<slug>/` folder claimed by no Workflow node's
  `# Artifacts` (or by more than one)
- SOP `workflow:` back-pointer disagreeing with the claiming node
- Run-log evidence contradicting status (`runs.md` has entries but the node is not
  `in-production`)

**Warnings:**

- Malformed `generated.by` actor string
- `stale_after` overdue
- Backlog staleness (backlog node untouched > 6 months — "triage or retire")
- Workflow in no Process list (non-production)
- A Note linking no bundle node ("probably misfiled")
- **Orphan capabilities** — skills/agents in the workspace referenced by no Workflow node
  ("capture the workflow" — the single most useful maintenance signal for students)
- Stale GENERATED content — regenerate (a Function `# Owns` block whose content no longer
  matches the derived owners list; hand-editing between the markers is still prohibited by
  doctrine, but a stale block is a maintenance-pass warning, never a lint blocker — see
  `scaffolding-registry/SKILL.md`'s Phase 4/6 notes)

**Gitignore tolerance:** links into gitignored paths (the raw-source layer, e.g. `outputs/`) are
declarations, not guarantees — existence-checked locally when the target is present, skipped in
CI/Tier 3 via `git check-ignore`. Without this tolerance, every artifact link would fail a
student's first Action run.

All lint messages are plain-language and file-naming; fixes are offered, never silently
auto-applied — lint never repairs meaning on its own.

---

## 7. Closing step

After your skill's fields are written, invoke the `indexing-registry` skill for a maintenance
pass. This is **best-effort** — a failed refresh never fails your step. Do not restate the
maintenance pass inline; point here.
