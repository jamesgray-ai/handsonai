---
type: Schema
title: "AI Registry Bundle Schema"
description: "Types, link rules, derived views, and maintenance rules for your AI registry bundle."
generated: { by: process:ai-registry-template, at: 2026-11-28T14:40:35Z }
---
# AI Registry Bundle — SCHEMA

This bundle is an [OKF v0.3](https://github.com/open-knowledge-format/open-knowledge-format)
knowledge bundle holding **operations knowledge**: how your business runs — its lines of business,
processes, workflows, and the durable insights their runs produce. The bundle root declares
`okf_version: "0.3"` in `index.md`'s frontmatter (spec §8.1: the bundle-root index is the one
index permitted a frontmatter block; it may also carry the bundle's `title`, `description` and
`license`).

**Before changing this schema or the bundle's structure** (concept types, frontmatter fields,
links, indexes, directory layout, or the rules below), **consult the OKF spec first**
([spec](https://github.com/open-knowledge-format/open-knowledge-format) ·
[raw SPEC.md](https://raw.githubusercontent.com/open-knowledge-format/open-knowledge-format/main/SPEC.md)).
This SCHEMA is a **stricter producer profile** on top of OKF: it requires `title`/`description`/
`generated`, enforces directory↔type agreement and enum values, and errors on broken links, index
gaps, and unclaimed operational artifacts — all OKF-permitted.

> `log.md` and every `index.md` are the spec's **reserved files** (§3.1): never concepts. This
> `SCHEMA.md` is a concept to the spec (it carries `type: Schema`); this profile exempts it from
> its concept checks, since it sits outside the six-type table below and is never
> directory-checked.

# Types and directories

Plural directories, singular `type` values. Directory↔type agreement is lint-enforced.

| Directory | type | Frontmatter beyond required | Body sections |
|---|---|---|---|
| `businesses/` | Business | `state` (`active \| incubating \| dormant`), optional `url` | identity prose · curated ordered `# Lines of Business` list |
| `lines-of-business/` | LineOfBusiness | `state` (same enum), optional `folder:` | prose · curated ordered `# Processes` list |
| `processes/` | Process | `owner` (required — a function slug), optional `guide:` | prose · curated ordered `# Workflows` list (the edge AND the value-chain order) |
| `workflows/` | Workflow | `state` (required), `execution_mode`, `autonomy`, `trigger`, optional `stale_after`, optional `big_change` (`definition_type` is tolerated on older nodes, never written) | prose · `# Artifacts` labeled links · `# Skills` · `# Agents` · GENERATED `# Insights` |
| `notes/` | Note | — | free body; its links to Workflow/Process nodes are the single source of the insight edge |
| `functions/` | Function | optional `lead:` (free text; blank = unstaffed) | charter prose · required GENERATED `# Owns` block (written current, listing the processes it owns, by the step that saves each process; the empty pair only while it owns none) |

# Enums

Lint-enforced:
- Workflow `state`: `backlog` | `under-development` | `in-production` | `retired`
- Business and LineOfBusiness `state`: `active` | `incubating` | `dormant`
- `status` (any node, optional): `draft` | `stable` | `deprecated` — the spec's lifecycle, never
  domain state (see *Domain state and lifecycle*)
- `definition_type`: `step-driven` | `goal-driven`. No framework step writes it any more; it is
  tolerated on older nodes, as are its legacy spellings `step-decomposed` and `outcome-driven`
- `execution_mode`: `manual` | `augmented` | `automated`
- `autonomy`: `deterministic` | `guided` | `autonomous`

# Domain state and lifecycle

OKF v0.3 §5.4 makes `status` the lifecycle only: absent means current (`stable`), `draft` not
finished, `deprecated` kept for links and history; any other value is read as not current.
**Domain state lives in `state`**, with the enums above, on Workflow, Business and LineOfBusiness
nodes only. A retired Workflow says both `state: retired` and `status: deprecated`, with
`superseded_by: /workflows/<slug>.md` when another workflow took over its work. A removed Process
says `status: deprecated` (a Process has no `state`). Lint errors on a domain value in `status`,
on `state` on any other type, and on `state: retired` without `status: deprecated`.

A registry written before OKF v0.3 (its root `index.md` declares `okf_version: "0.2"`, or no
version) keeps its domain state in `status` and its links in the 0.2 form; the tools read both
forms there, and lint gives one warning that offers the upgrade (*Upgrading from OKF v0.2* below).

# Deliberately not concept types

**Skills, agents, SOPs, process guides, runbooks, prompts, and apps stay in their existing
homes** — this bundle links to them and never duplicates their content. Skills and agents are
sourced from your assistant's own skill/agent files; SOPs, guides, and prompts live wherever your
workflow outputs put them. A Workflow node's `# Skills`, `# Agents`, and `# Artifacts` links are
how the bundle points at them.

**Event-fact fields are banned from nodes**: `current_step`, `health`, `last_run`, `run_count`
(and any run-counter field), `next_review`, `notion_url`, `timestamp`, `lob`, `sequence`,
`process` (banned on any node), `owner` (banned on Workflow nodes — it lives on Process) — those
are workflow-record concerns, not registry state. `stale_after` (the re-check date) is permitted
because a dashboard roll-up and a lint warning give it teeth.

**Layered model.** Each workflow has a folder in the **framework folder** — its **record**, what the
AI Workflow Framework produced while building and testing it: `requirements.md`, `design-plan.md`,
`build-record.md` and `test-results.md`, with `inputs/`, `context/`, `package/` and `history/`.
The framework folder is `framework/` in the leader's **working folder**, beside `registry/` and
`knowledge/`, so a workflow's folder is `framework/<slug>/` on every platform. The working folder is
`ai-workspace/` in the leader's drive on the web and in Microsoft 365 Copilot, the folder the leader
selects on Claude desktop, and the workspace on Claude Code and Codex. The workflow's **run log** and
its own output are not part of the record: they live in the workflow's own folder, where it runs,
outside the working folder. Event-facts stay in the
record. Only **synthesized insight** crosses into this bundle, as `Note` concepts. Links point one
way: the registry links into the workflow folders, and nothing in them links back to registry nodes.

**Progress** is never stored in this bundle. It is read by the framework's routing rule from the
workflow's folder, never from which links a node has, and the derived views show it as the routing
state's name, with no step number.

# Frontmatter

**Single-line YAML values only** — no `>-`/`|` folded or literal blocks, no inline `#` comments,
no multi-line values, with one exception: `verified` (and `sources`) may be a block list of one-line
maps (`  - { by: …, at: … }`). Required on every concept node: `type`, `title`, `description`,
`generated` — a single-line flow map, `generated: { by: process:<skill-name>, at:
2026-10-24T15:04:05Z }`, carrying who or what wrote the current content (`by`) and when (`at`, a
UTC instant, `YYYY-MM-DDTHH:MM:SSZ`). The lint accepts a bare `YYYY-MM-DD` date on an older node;
never write one.

**Who wrote it (`by`) and when (`at`)** (OKF v0.3 §5.2, §7). `generated` records how the *current
content* was made, so it moves only when the content does:
- **A skill's run changed the content**: `by: process:<skill-name>` (`process:deconstruct`), `at`
  the moment of the write.
- **The leader asked the AI to change it, with no skill running**: the agent form
  `<app>/<model id>` (`claude-code/claude-opus-5-5`; `<app>/unrecorded` when the model ID isn't
  known), `at` now.
- **The leader edited it by hand**: `human:<id>`, `at` now.
- **A trivial edit** — formatting, whitespace, a link or path repair, the upgrade to OKF v0.3,
  regenerating a derived view or a GENERATED block, recording a check in `verified` — changes
  neither `by` nor `at`.

**`verified`** (optional, OKF v0.3 §5.2–5.3) records a person's own check of the file against what
it describes: `verified: { by: human:<id>, at: <instant> }`, or a list of such events
(`verified: [{ … }, { … }]`; a block list of one-line maps reads the same). It is written
only when the leader says they have read the file and it is right — never on their behalf, and never
by a skill on its own. A check counts only while it is current (its `at` is on or after
`generated.at`): once the content changes, the file is unverified again until someone checks it
again, and lint warns. The leader's `<id>` is asked once, at their first check, and recorded in
`log.md`.

**Keys you don't own are kept.** A writer that changes a node keeps every key it doesn't own
(`verified`, `sources`, `tags`, and any `x-` key) and leaves the lines it didn't change as they
were (OKF v0.3 §4, §4.1).

**Write each key once** (OKF v0.3 §4); lint warns on a key written twice, and the last value is
read. **A `.md` file with no frontmatter isn't a page** (OKF v0.3 §3.2): a `README.md` in a
folder, say. Lint warns, and every check, index and view skips it.

**Reserved files are exempt.** `log.md` and every `index.md` carry no concept frontmatter. The
sole exception is the bundle root `index.md`, which carries the bundle's metadata: `okf_version`
(required), and optionally `title`, `description`, `license` and `x-` keys (§8.1). Lint warns on
any other key there, and on frontmatter in a subdirectory `index.md`.

**Banned fields** (never write these into a node): `current_step`, `health`, `last_run`,
`run_count` (and any run-counter field), `next_review`, `notion_url`, `timestamp`, `lob`,
`sequence`, `process` (banned on any node), `owner` (banned on Workflow nodes — it lives on
Process) — see "Deliberately not concept types" above for why.

**`stale_after`** is permitted on Workflow nodes: the **re-check date**, `YYYY-MM-DD` (the start of
that UTC day, OKF v0.3 §5), set by Test at go-live and reset at each passing re-check. A workflow is
due for a re-check when now ≥ `stale_after`. A value that isn't a date or a UTC instant is a lint
error: it is never read as fresh (§5.5).

**`big_change`** is permitted on Workflow nodes: `"[reason], [date]"`, written by Design when it
sends a workflow back for a redesign, and removed by Deconstruct when the redo is saved. An empty
`big_change` reads as absent (OKF v0.3 §11.2). Design also
writes one entry in `log.md` with the reason, which stays.

Optional standard fields: `verified` (above), `tags: [a, b]`, and, on a deprecated node,
`superseded_by`.

# Where this profile is stricter than OKF v0.3

All OKF-permitted; recorded so a reader of the spec isn't surprised:
- **`generated.at` is required**, as a UTC instant (the spec requires only `generated.by`, and also
  admits a date or an offset). A bare date is accepted on nodes written before this profile asked
  for instants.
- **Single-line values**, except the `verified`/`sources` block list.
- **In-bundle links are root-relative** (`/processes/x.md`); the spec admits both forms.
- **This profile's own keys are unprefixed.** `state`, `execution_mode`, `autonomy`, `trigger`,
  `big_change`, `owner`, `lead`, `url`, `folder`, `guide` and `definition_type` predate the spec's
  advice to name producer keys `x-<producer>-<name>` (§4.1) and stay as they are: renaming them
  would break every registry. A future OKF version could define one of them; this schema would then
  record how it reads that key.
- **The root `index.md` must declare `okf_version`** (§8.1 makes it a SHOULD), and lint warns on
  any root-index key beyond `title`, `description`, `license` and `x-` keys (the spec permits any
  extension key there).
- **A 0.2 registry's bare links read from the registry's parent folder:** this profile's own
  rule from before v0.3, not the spec's §12.1 fallback to the bundle root.
- **The registry's own tools read files outside the bundle.** To a generic OKF consumer a link
  that leaves the bundle is external and never read (§6, §11.2). Lint and compose read the SOPs,
  workflow folders, run logs, skills and agents a node links (to check they exist, and for the
  claims sweep and the dashboard): the one place they go beyond a generic consumer.

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
| Workflow → operational files | the Workflow node's `# Artifacts` labeled links | claims sweep (every SOP and every workflow folder, `framework/<slug>/`, must be claimed) |

**Process → Function (ownership)** is the one attribute-reference edge: the Process's `owner:`
frontmatter holds a function slug. Deliberately not a curated parent list — ownership is
cross-cutting, many-to-one, with no sequence. The Function's `# Owns` block is the GENERATED
reverse view. **Workflows inherit their process's owner and LOB — never stored on the workflow
itself.** A Function with no `lead:` is *unstaffed* — a derived insight, not an error. A Workflow
listed in no Process's curated list renders under "Unassigned" on the dashboard (error if
`in-production`, warning otherwise).

# Links

OKF v0.3 §6, exact:
- **Leading `/`** = in-bundle, resolved from `registry/` (e.g. `/processes/course-improvement.md`).
  The first path segment MUST be one of this bundle's directories or a root file — lint errors
  otherwise. Every in-bundle link is written this way.
- **No leading slash, not a URL** = **file-relative**: resolved from the folder of the file the
  link is in. Use it for files outside the bundle. From a node (`workflows/x.md`, or any type
  directory) the working folder is two levels up, so a workflow's requirements are
  `../../framework/course-improvement/requirements.md`, an SOP `../../sops/x-sop.md`, a skill
  `../../.claude/skills/<name>/SKILL.md`; from the root `index.md` it is one level up
  (`../.claude/skills/<name>/SKILL.md`). The `guide:` and `folder:` path fields and
  `superseded_by` resolve the same way. A trailing `/` marks a directory target. Lint errors on a
  link of this form that lands inside the bundle, and names the form to write instead.
- **Full URLs** = external.
- **Code is not a link** (OKF v0.3 §6.1): text in inline code or a fenced block that looks like a
  link (an example of the form) is never read as one, so it is never checked or counted.

Links into gitignored paths (e.g. `outputs/`, where a workflow's own output may land) are
declarations, not guarantees: lint checks them when the target is present and skips them otherwise.

In a registry still at OKF 0.2, a bare link is read from the registry's parent folder
(`framework/course-improvement/requirements.md`), and an older one that doesn't resolve as written
(`course-improvement/requirements.md`) is still valid when `framework/` plus the same path does.

# Naming

Kebab-case slug from title at creation (`&` → `and`, strip punctuation). Slugs are STABLE — title
edits never rename files. A Workflow's slug matches its folder in the framework folder where one
exists.

# Artifact labels

`# Artifacts` links on a Workflow node use these labels: Raw source, Run log, Output, SOP,
Opportunity report, Requirements, Design plan, Test results. Each is a plain bulleted link whose
link text is the label itself (link text `Requirements`, not a bold `Requirements:` prefix before
the link), because lint and compose read the label from the link text. The build record has no
label: it is found by its path, beside the requirements. A "Run log" link may point outside the
registry's reach (an external link), or be absent.

Labels from earlier versions of the framework ("Design spec", "Run guide", "Improvement plan") are
tolerated on older nodes — those whose `generated.at` is a bare date — and never written; a node
stamped with a UTC instant that carries one is a lint error.

# Derived views & maintenance

Derived views are: the root dashboard (`REGISTRY.md`), `registry-dashboard.html` (generated at the end of setup, refreshed on every maintenance pass once it exists),
each directory's `index.md` (one entry per page: its root-relative link, then ` — ` and the
page's `description`, on one line; OKF v0.3 §8), and GENERATED blocks inside nodes — hash-less paired markers
(`<!-- GENERATED:<name> -->` … `<!-- /GENERATED -->`); never hand-edit content between the
markers. Regenerating `index.md` keeps the root index's frontmatter (§8.1).

These views are regenerated, and this bundle is linted, **by your AI assistant reading the bundle
against this SCHEMA**, or, where code can run, by the framework's own compose and lint scripts,
which follow these same rules. The rules it checks:
required frontmatter present on every page (a `.md` with no frontmatter isn't a page: a warning) · single-line values · directory↔type agreement · enum values ·
domain state in `state`, `status` the lifecycle only, a retired Workflow also `status: deprecated` ·
banned fields absent · link targets resolve, in-bundle links root-relative · `superseded_by` reaches
a concept · `stale_after` a date or a UTC instant · curated-list membership (exactly one parent per
child) · owner validity (Process `owner:` names a real Function) · Function `# Owns` block
present · GENERATED markers intact and terminated · every directory `index.md` covers its nodes ·
claims sweep (every SOP claimed by exactly one Workflow; an SOP's `workflow:` back-pointer must
agree with the claiming node; run-log evidence must not contradict `state`, checked only where the
node's "Run log" link is readable inside the registry's parent folder — an external or absent link
is skipped) · legacy artifact labels only on older nodes. Warnings (not errors): a registry still at
OKF 0.2 (the upgrade offer), a workflow folder in the framework folder claimed by no Workflow, a
re-check overdue (now ≥ `stale_after`), a `backlog` workflow older than six months, a Note linking
no node, uncaptured skills/agents, a malformed actor string in `generated.by` or `verified`, a
`verified` event missing `by` or `at`, a check the content has outrun, a frontmatter key written
twice, a `.md` with no frontmatter, `superseded_by` without
`status: deprecated`, frontmatter in the wrong
`index.md`, a `log.md` out of the §9 form, an artifact link pointing outside the workflow's derived
LOB `folder:` when one is set, and stale Function `# Owns` content (present but no longer matching the derived owners list — regenerate via
a maintenance pass; hand-editing between the markers is still prohibited, but staleness alone never
blocks regeneration).

Regeneration is refused while lint reports errors, with one exception: broken links inside
derived content that the regeneration pass itself rewrites.

On the derived views, a workflow's progress shows as the routing state's name, `stale_after` as
"Re-check by", `autonomy` as "How it decides" (the level's name with its plain meaning), and
`execution_mode` as "Runs with you" (`manual`, `augmented`) or "Runs without you" (`automated`).

Repos created from this template also get these checks wired as CI (the `tools/` scripts plus a
GitHub Action) — you never run them yourself; your AI assistant and CI do.

# Upgrading from OKF v0.2

A registry set up before OKF v0.3 says `okf_version: "0.2"` (or no version) in `index.md`. The
upgrade changes only the form, never the content, so no page's `generated` line moves (the
replaced `SCHEMA.md` brings its own): the root index
declares `"0.3"`; on Workflow, Business and LineOfBusiness nodes a domain value in `status` moves
to `state` (a retired Workflow also gets `status: deprecated`; a retired Process becomes
`status: deprecated`); each link and `guide:`/`folder:` value written from the registry's parent
folder becomes file-relative from what it reaches; `log.md` is regrouped into the §9 form; and this
`SCHEMA.md` is replaced with the current one. Where code can run, `node tools/upgrade-registry.js`
does all but the schema (`--check` shows what it would change).

# Lifecycle

Removed workflows become `state: retired` with `status: deprecated` (and `superseded_by` when
another workflow took over), and removed processes `status: deprecated` — kept, and linked from an
explaining Note — never deleted.

`log.md` follows OKF v0.3 §9: no frontmatter; entries grouped under `## YYYY-MM-DD` headings,
newest date first; each entry a bullet, its kind in bold where it has one
(`- **Go-live** — Client Follow-Up went live after test round 1`). A new entry goes at the end of
today's heading, the first heading below the log's title, which it creates when it isn't there; nothing already in the log is reworded,
moved or removed. It records setup decisions (such as the dashboard's Claude Artifact link), schema
changes, the leader's checker ID, and one entry per workflow event, written by the step that makes
it: a big change and its reason, go-live, a re-check, a changed version not ready. It never records
routine regenerations.
