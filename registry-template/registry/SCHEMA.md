---
type: Schema
title: "AI Registry Bundle Schema"
description: "Types, link rules, derived views, and maintenance rules for your AI registry bundle."
generated: { by: process:ai-registry-template, at: 2026-08-10 }
---
# AI Registry Bundle — SCHEMA

This bundle is an [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
knowledge bundle holding **operations knowledge**: how your business runs — its lines of business,
processes, workflows, and the durable insights their runs produce. The bundle root declares
`okf_version: "0.2"` in `index.md`'s frontmatter (spec §12: the one index permitted a frontmatter
block).

**Before changing this schema or the bundle's structure** (concept types, frontmatter fields,
links, indexes, directory layout, or the rules below), **consult the OKF spec first**
([spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) ·
[raw SPEC.md](https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md)).
This SCHEMA is a **stricter producer profile** on top of OKF: it requires `title`/`description`/
`generated`, enforces directory↔type agreement and enum values, and errors on broken links, index
gaps, and unclaimed operational artifacts — all OKF-permitted.

> `SCHEMA.md` itself is a **reserved file**: your AI assistant's lint pass treats `SCHEMA.md`,
> `log.md`, and every `index.md` as reserved and skips all concept checks on them (that's why this
> file carries `type: Schema` — deliberately outside the six-type table below, and never
> directory-checked).

# Types and directories

Plural directories, singular `type` values. Directory↔type agreement is lint-enforced.

| Directory | type | Frontmatter beyond required | Body sections |
|---|---|---|---|
| `businesses/` | Business | `status` (`active \| incubating \| dormant`), optional `url` | identity prose · curated ordered `# Lines of Business` list |
| `lines-of-business/` | LineOfBusiness | `status` (same enum), optional `folder:` | prose · curated ordered `# Processes` list |
| `processes/` | Process | `owner` (required — a function slug), optional `guide:` | prose · curated ordered `# Workflows` list (the edge AND the value-chain order) |
| `workflows/` | Workflow | `status` (required), `definition_type`, `execution_mode`, `autonomy`, `trigger`, optional `stale_after` | prose · `# Artifacts` labeled links · `# Skills` · `# Agents` · GENERATED `# Insights` |
| `notes/` | Note | — | free body; its links to Workflow/Process nodes are the single source of the insight edge |
| `functions/` | Function | optional `lead:` (free text; blank = unstaffed) | charter prose · required GENERATED `# Owns` block (write it empty at creation) |

# Enums

Lint-enforced:
- Workflow `status`: `backlog` | `under-development` | `in-production` | `retired`
- `definition_type`: `step-driven` | `goal-driven` (readers tolerate the legacy spellings
  `step-decomposed` and `outcome-driven` from earlier registry versions — never write them into a
  new node)
- `execution_mode`: `manual` | `augmented` | `automated`
- `autonomy`: `deterministic` | `guided` | `autonomous`

# Deliberately not concept types

**Skills, agents, SOPs, process guides, runbooks, prompts, and apps stay in their existing
homes** — this bundle links to them and never duplicates their content. Skills and agents are
sourced from your assistant's own skill/agent files; SOPs, guides, and prompts live wherever your
workflow outputs put them. A Workflow node's `# Skills`, `# Agents`, and `# Artifacts` links are
how the bundle points at them.

**Event-fact fields are banned from nodes**: `current_step`, `health`, `last_run`, `run_count`
(and any run-counter field), `next_review`, `notion_url`, `timestamp`, `lob`, `sequence`,
`process` (banned on any node), `owner` (banned on Workflow nodes — it lives on Process) — those
are raw-source-layer or retired-manifest concerns, not registry state. `stale_after` (a date — a
workflow is stale when today ≥ `stale_after`) is permitted because a dashboard roll-up and a lint
warning give it teeth.

**Layered model.** `outputs/<slug>/` is the **raw-source layer** — the system of record for what a
workflow produces and experiences (run logs, generated outputs, framework documents). Event-facts
stay there. Only **synthesized insight** crosses into this bundle, as `Note` concepts.

# Frontmatter

**Single-line YAML values only** — no `>-`/`|` folded or literal blocks, no inline `#` comments,
no multi-line values of any kind. Required on every concept node: `type`, `title`, `description`,
`generated` — a single-line flow map, `generated: { by: process:ai-registry-template, at:
2026-08-10 }`, carrying who/what produced the file (`by`) and when (`at`, `YYYY-MM-DD`). `by`
follows the OKF actor convention: `human:<id>` or `process:<skill-name>`.

**Reserved files are exempt.** `SCHEMA.md`, `log.md`, and every `index.md` carry no required
concept frontmatter. The sole exception is the bundle root `index.md`, which carries exactly one
frontmatter key: `okf_version`.

**Banned fields** (never write these into a node): `current_step`, `health`, `last_run`,
`run_count` (and any run-counter field), `next_review`, `notion_url`, `timestamp`, `lob`,
`sequence`, `process` (banned on any node), `owner` (banned on Workflow nodes — it lives on
Process) — see "Deliberately not concept types" above for why.

**`stale_after`** is permitted on Workflow nodes: a date, `YYYY-MM-DD`; the workflow is stale when
today ≥ `stale_after`.

Optional standard fields: `verified: { by, at }` (same flow-map shape as `generated`, stamped
after a deliberate human review pass — absent means unverified) and `tags: [a, b]`.

# Recorded deviations from OKF v0.2

- **`status` enums.** OKF v0.2 standardizes `status` as a lifecycle enum (`draft | stable |
  deprecated`, absent ⇒ stable). This bundle overrides `status` with domain-state enums per type
  instead — a producer-profile deviation the spec permits (consumers MUST tolerate unknown values
  per §11). This bundle's `retired` corresponds to spec `deprecated`.
- **`generated.at` is required and date-only.** The spec requires only `generated.by`; this
  profile also requires `at`, and keeps it a plain `YYYY-MM-DD` date where the spec's own examples
  show datetimes.

# Relationships — stored once, everything else derived

**One rule at every level: the parent's curated ordered list is both the edge and the sequence;
children carry no pointer.** A Business orders its Lines of Business, a Line of Business orders
its Processes, a Process orders its Workflows. To re-sequence a value chain, reorder the lines in
the parent — nothing on the child changes.

| Edge | Single home | Derived views |
|---|---|---|
| LOB → Business | the Business node's curated `# Lines of Business` list | dashboard header + LOB ordering |
| Process → LOB | the LOB node's curated `# Processes` list | dashboard grouping |
| Workflow → Process | the Process node's curated `# Workflows` list | dashboard tables in value-chain order; workflow's LOB (via chain) |
| Workflow → Skill/Agent | the Workflow node's `# Skills` / `# Agents` body links | per-skill/agent used-by in generated inventories |
| Insight → Workflow/Process | the Note's body links | Workflow `# Insights` GENERATED block |
| Workflow → operational files | the Workflow node's `# Artifacts` labeled links | claims sweep (every SOP/`outputs/<slug>/` folder must be claimed) |

**Process → Function (ownership)** is the one attribute-reference edge: the Process's `owner:`
frontmatter holds a function slug. Deliberately not a curated parent list — ownership is
cross-cutting, many-to-one, with no sequence. The Function's `# Owns` block is the GENERATED
reverse view. **Workflows inherit their process's owner and LOB — never stored on the workflow
itself.** A Function with no `lead:` is *unstaffed* — a derived insight, not an error. A Workflow
listed in no Process's curated list renders under "Unassigned" on the dashboard (error if
`in-production`, warning otherwise).

# Links

Discriminator, exact:
- **Leading `/`** = bundle-root-relative, resolved from `registry/` (e.g.
  `/processes/course-improvement.md`). The first path segment MUST be one of this bundle's
  directories or a root file — lint errors otherwise.
- **No leading slash, not a URL** = workspace/repo-root-relative (e.g.
  `outputs/course-improvement/sop.md`). A trailing `/` marks a directory target.
- **Full URLs** = external.

Links into gitignored paths (e.g. `outputs/`) are declarations, not guarantees: lint checks them
when the target is present and skips them otherwise.

# Naming

Kebab-case slug from title at creation (`&` → `and`, strip punctuation). Slugs are STABLE — title
edits never rename files. A Workflow's slug matches its `outputs/<slug>/` folder where one exists.

# Artifact labels

`# Artifacts` links on a Workflow node use these labels: Raw source, Run log, Output, SOP,
Requirements, Design spec, Test results, Run guide, Improvement plan.

# Derived views & maintenance

Derived views are: the root dashboard (`REGISTRY.md`), an optional `registry-dashboard.html`,
each directory's `index.md`, and GENERATED blocks inside nodes — hash-less paired markers
(`<!-- GENERATED:<name> -->` … `<!-- /GENERATED -->`); never hand-edit content between the
markers.

These views are regenerated, and this bundle is linted, **by your AI assistant reading the bundle
against this SCHEMA** — there is no separate compose or lint program to run. The rules it checks:
required frontmatter present · single-line values · directory↔type agreement · enum values ·
banned fields absent · link targets resolve · curated-list membership (exactly one parent per
child) · owner validity (Process `owner:` names a real Function) · Function `# Owns` block
present · GENERATED markers intact and terminated · every directory `index.md` covers its nodes ·
claims sweep (every SOP and `outputs/<slug>/` folder claimed by exactly one Workflow; an SOP's
`workflow:` back-pointer must agree with the claiming node; run-log evidence must not contradict
`status`). Warnings (not errors): overdue `stale_after`, a `backlog` workflow older than six
months, a Note linking no node, uncaptured skills/agents, a malformed `generated.by` actor string,
an artifact link pointing outside the workflow's derived LOB `folder:` when one is set, and stale
Function `# Owns` content (present but no longer matching the derived owners list — regenerate via
a maintenance pass; hand-editing between the markers is still prohibited, but staleness alone never
blocks regeneration).

Regeneration is refused while lint reports errors, with one exception: broken links inside
derived content that the regeneration pass itself rewrites.

Repos created from this template also get these checks wired as CI (the `tools/` scripts plus a
GitHub Action) — you never run them yourself; your AI assistant and CI do.

# Lifecycle

Removed workflows or processes become `status: retired` — kept, and linked from an explaining
Note — never deleted. `log.md` records migrations and schema changes only, not routine
regenerations.
