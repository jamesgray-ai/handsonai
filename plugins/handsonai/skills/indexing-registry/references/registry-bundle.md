# Registry Bundle — the Shared Contract

Every framework skill treats the **AI registry bundle** as the single source of truth for
workflow registry metadata. This document defines how any skill *finds* the bundle, *writes* to
it, which fields each skill *owns*, what goes in the *registry log*, how progress and the re-check
date are *shown*, and how the bundle is *linted*, so the rules are stated once instead of per skill.
Every registry note in the framework skills points here rather than restating any of this.

Progress is never stored in the registry: it is read from the workflow's folder by the routing
rule (each step skill's `references/routing.md`; the `framework-state` script where code can
run). The re-check date is Test's `stale_after`.

**Contents:** 1. Where the registry is · 2. Write rules · 3. Field ownership · 4. Artifact
links · 5. Progress and the leader-facing labels · 6. The re-check date · 7. The registry
log · 8. Lint rule list · 9. Closing step · 10. Upgrading a registry from OKF 0.2

---

## 1. Where the registry is

| Where the leader works | Registry | Its parent folder |
|---|---|---|
| Claude Code, Codex | `registry/` in the workspace | the workspace, the working folder, which also holds `framework/` |
| Claude desktop with a local working folder | `registry/` inside the working folder the leader selected | the working folder, which also holds `framework/` |
| Claude on the web, ChatGPT, Microsoft 365 Copilot (Cowork) | `registry/` in the working folder (`ai-workspace/`, or the leader's own folder) in the storage service it was set up in (Google Drive, OneDrive, Dropbox or another), read and written through the platform's connection | the working folder, which also holds `framework/` |

A workflow's registry entry is its **Workflow concept node**, `registry/workflows/<slug>.md`, where
`<slug>` is the workflow's kebab-case ID, the same name as its folder in the framework folder. The
node is YAML frontmatter plus Markdown body sections, held inside an
[OKF v0.3](https://github.com/open-knowledge-format/open-knowledge-format)
knowledge bundle rooted at `registry/`.

**The workflow's folder** is `[framework folder]/<slug>/`. It holds `requirements.md`,
`design-plan.md`, `build-record.md`, `test-results.md`, `inputs/`, `context/`, `package/` and
`history/` (plus `deconstruct-in-progress.md` while Deconstruct is unfinished, and a team
workflow's `<slug>-sop.md`). The run log is never there: it lives in the workflow's own place,
where the workflow runs. Nothing in `history/` is ever deleted, and no registry write reads it.

The bundle's own `registry/SCHEMA.md` is **authoritative** for node structure, enums and lint
rules. Read it before the first node write of any session, and defer to it if it ever differs from
anything restated here.

**With no registry** (`registry/SCHEMA.md` doesn't exist), write no registry entry of any kind.
The steps keep their no-registry markers instead: the backlog in `backlog.md`, `big_change` in the
requirements' frontmatter, and the build record's "Live since" line. The `scaffolding-registry`
skill sets a registry up when the leader wants one.

---

## 2. Write rules

1. **Single-line frontmatter only.** No `>-`/`|` block scalars, no inline `#` comments, no
   multi-line values of any kind. If a description is long, shorten it; never wrap it in a block
   scalar. Quote a value that holds `: ` or starts with a character YAML treats specially.
2. **Stamp `generated` when your step changes the content.** A write that creates a node, or
   changes what it says (a field value, a link added or removed, the description, a line added to
   or removed from its curated list, such as a Process's `# Workflows`), carries:

   ```yaml
   generated: { by: process:<skill-name>, at: <YYYY-MM-DDTHH:MM:SSZ> }
   ```

   `<skill-name>` is the writing skill's own name (`process:deconstruct`); `at` is the moment of
   the write as a UTC instant, such as `2026-10-24T15:04:05Z`. The lint accepts a bare
   `YYYY-MM-DD` on an older node; never write one. `generated` records how the current content was
   made (OKF v0.3 §5.2), so:
   - **A trivial edit leaves `by` and `at` as they are:** formatting, whitespace, a link or path
     repair, the upgrade to OKF v0.3, a regenerated derived view or GENERATED block, a `verified`
     check recorded.
   - **When the leader asks you to change a node outside any step,** the writer is you, in the
     agent form `<app>/<model id>` (`claude-code/claude-opus-5-5`, `claude-ai/claude-opus-5-5`;
     `<app>/unrecorded` when you don't know your model ID), with `at` now. A node the leader edited
     by hand is theirs: `human:<id>`.
3. **Never edit between GENERATED markers.** Content between `<!-- GENERATED:<name> -->` and
   `<!-- /GENERATED -->` is machine-owned: write around it, never inside it, and never leave a
   marker pair unterminated.
4. **Link discriminator, exact** (OKF v0.3 §6):
   - Leading `/`: bundle-root-relative, resolved from `registry/` (`/processes/new-business.md`).
     The first path segment must be one of the bundle's directories or a root file. Every link
     to another registry page is written this way.
   - No leading slash, not a URL: **file-relative**, resolved from the folder of the page the link
     is in. Use it for every file outside the registry. A node sits in a type folder
     (`registry/workflows/`), two levels below the working folder, so a workflow's files read
     `../../framework/<slug>/requirements.md` on every platform, an SOP `../../sops/<file>.md`, a
     skill `../../.claude/skills/<name>/SKILL.md`. From the root `registry/index.md`, one level
     down, the same skill is `../.claude/skills/<name>/SKILL.md`. The `guide:` and `folder:` fields
     resolve the same way (`guide: ../../process-guides/<file>.md`).
     *Worked example, by hand:* from `registry/workflows/client-follow-up.md`, the link
     `../../framework/client-follow-up/requirements.md` goes up from `workflows/` to `registry/`,
     up again to the working folder, then down into `framework/client-follow-up/`.
   - Never write a file-relative link to another registry page (`../processes/x.md`): use the
     `/` form.
   - A full URL: external.
   - **A registry still at OKF 0.2** (its root `index.md` says `okf_version: "0.2"`, or no
     version): its older links were written from the registry's parent folder (this profile's
     own 0.2 rule, not the spec's §12.1 fallback to the bundle root)
     (`framework/<slug>/requirements.md`), and one that doesn't resolve as written
     (`<slug>/requirements.md`) is valid when `framework/` plus the same path resolves. Read them
     that way, as the lint scripts do; never rewrite one outside the upgrade (section 10), never
     report it. Everything you write into such a registry uses the 0.3 forms of this contract.
5. **A workflow joins exactly one Process** through that Process's curated, ordered `# Workflows`
   list (`registry/processes/<process-slug>.md`); the list is both the Workflow→Process edge and
   the value-chain order. Append at the end if the position is unknown. **Never write**
   `process:`, `owner:`, `lob:` or `sequence:` on the Workflow node: membership, ownership and
   line of business all derive from the parent list.
6. **Banned fields:** never write these into any node:

   `current_step`, `health`, `last_run`, `run_count` (and any run-counter field), `next_review`,
   `notion_url`, `timestamp`, `lob`, `sequence`, `process` (banned on any node), `owner` (banned
   on Workflow nodes; it lives on Process).
7. **No link to a moved file.** A step that moves a linked file into `history/` removes that link
   in the same write, and a step that moves one back restores it only if it's absent (the
   set-aside rules in section 3). The same holds when an earlier version's files are moved into
   `history/earlier-version-[date]/`: their links, legacy labels included, come off the node.
8. **Saving on a drive.** How to save comes from the tools the connection gives you (`references/saving.md` in each skill that saves), and a page you'll save again is read as stored, never from a reformatted view. Where the connection can update a file in place, it does. Where it can
   only create files but can move and rename them, before each save the current file moves into
   the framework folder's `history/`, under its registry path and renamed `[file]-YYYY-MM-DD-HHMM.md`
   (`history/registry/workflows/<slug>-2026-10-24-1504.md`), and the new file is
   created under its own name; such a step saves at the end of a part or a batch, not after every
   node. Nothing in the registry is ever shared, trashed or deleted on a drive.
9. **Nothing that can save.** With no files and no connection that can save, nothing in this
   contract is written: N-F16, and wait (`references/saving.md`, rule 5).
10. **Keep what you don't own** (OKF v0.3 §4, §4.1). When you change a node, keep every key you
    don't own as it is (`verified`, `sources`, `tags`, any `x-` key, and fields another step
    owns), and leave the lines you didn't change as they were: never reorder, requote or reformat
    them.
11. **`verified` is the leader's, never yours.** Never write or change `verified` as part of a
    step. It is written only when the leader says they have read a page and it is right, by the
    `indexing-registry` skill (*Record a check*).

**Bundle-wide anchors (consistency-check anchors, restated here on purpose):**

- The bundle root `index.md` declares `okf_version: "0.3"` in its frontmatter: the one index
  permitted a frontmatter block (with the bundle's optional `title`, `description` and `license`).
- Domain state is `state`; `status` is only the lifecycle, `draft` | `stable` | `deprecated`
  (OKF v0.3 §5.4). A retired workflow says both `state: retired` and `status: deprecated`.
- Full enum block, all values, lint-enforced:
  - Workflow `state`: `backlog` | `under-development` | `in-production` | `retired`
  - Business and LineOfBusiness `state`: `active` | `incubating` | `dormant`
  - `execution_mode`: `manual` | `augmented` | `automated`
  - `autonomy`: `deterministic` | `guided` | `autonomous`
  - `definition_type`: `step-driven` | `goal-driven`. No step writes it any more: it is
    tolerated on older nodes, with the legacy spellings `step-decomposed` and `outcome-driven`.
- `big_change`: free text, `"[reason], [date]"`, present only while a redo is pending.
- `stale_after`: a calendar date, `YYYY-MM-DD` (the start of that UTC day).

---

## 3. Field ownership

| Skill | Writes |
|---|---|
| `analyze` | A Workflow node stub per registered candidate: `title`, `description` (outcome-first), `state: backlog`, `trigger` (provisional); its line in the confirmed Process's `# Workflows` list; `# Artifacts` → Opportunity report (`../../framework/ai-opportunity-report.md`, on every platform), and → SOP (`../../sops/<file>.md`) when the candidate came from the leader's own SOP that no other node claims. Work the leader already runs: `state: in-production` and its `# Skills` / `# Agents` entry (a link when the file is in the workspace, otherwise its name as plain text). A new process follows the same owning-function rule as `naming-workflows`. |
| `naming-workflows` | A Workflow node stub: `title`, `description` (outcome-first), `state: backlog`, `trigger`; its line in the chosen Process's `# Workflows` list. **A new process → asks which function owns it** and writes a complete minimal Process node (owner required). |
| `deconstruct` | `state`: `backlog` to `under-development` only (it never resets another state, on a re-run, a redo or running work brought in, which stays `in-production`); the refined `trigger`; the `description` the leader accepted, word for word; `# Artifacts` → Requirements; `big_change` removed when a redo is saved (the registry-log entry stays). A cold-entry workflow with no node gets a new one in `naming-workflows`' stub format with `state: under-development`, listed in its Process's `# Workflows`. Finishing a set-aside that stopped partway, it removes any "Design plan" or "Test results" link still there; calling a big change off, it restores those links for the files moved back, each only if absent. |
| `design` | `execution_mode`, `autonomy`, on approval; `# Artifacts` → Design plan. A big change: `big_change` and one registry-log entry (section 7). A set-aside (a big change, or a change of platform or mechanism, which writes no `big_change`): removes the "Design plan" and "Test results" links; finishing a set-aside that stopped partway, before a fresh plan, it removes any of those links still there. A retired workflow brought back by "change my workflow": `state` `retired` to `under-development`, and `status: deprecated` (with any `superseded_by`) removed. |
| `build` | `# Skills` / `# Agents` links for every skill and agent it built or reused, at its close. The build record has no link: it is found by its path, `[framework folder]/<slug>/build-record.md`. |
| `test` | `# Artifacts` → Test results, when a round closes. At go-live: `state: in-production`, `stale_after` three months on, and the go-live log entry. At a passing re-check: `stale_after` reset three months on, and its log entry. A changed version or a re-check not ready: its log entry, `state` kept. A **Note node** on the leader's yes when a round surfaced a lasting insight, linked to the Workflow. |
| `writing-workflow-sops` | `# Artifacts` → SOP |
| `writing-process-guides` | Process node `guide:` frontmatter |
| The leader | `state: retired` with `status: deprecated` (and `superseded_by: /workflows/<slug>.md` when another workflow took over), when they retire a workflow |

Every writer that changes a node's content restamps `generated` (rule 2). `scaffolding-registry` writes no Workflow node; it
writes the bundle's skeleton and its founding log entry. Only `state` is schema-required on a
Workflow node, so a backlog stub lints clean without `execution_mode` or `autonomy`: `design`
writes both once the plan is approved, and nothing writes them earlier. A stub's `trigger` is
provisional: `deconstruct` may replace it; the never-overwrite rule protects values a leader set
through a framework step, not a stub-time guess. `scaffolding-registry` may set a Process node's
`guide:` when the leader's documents already include a process guide for it;
`writing-process-guides` owns the field thereafter.

---

## 4. Artifact links

Each `# Artifacts` entry is a plain bulleted link whose link text is the label itself
(`- [Requirements](../../framework/client-follow-up/requirements.md)`), because the lint and compose
read the label from the link text. Links follow rule 4's form: file-relative from the node.

| Label | Written by | Points at |
|---|---|---|
| Opportunity report | Analyze | `ai-opportunity-report.md` in the framework folder (`../../framework/ai-opportunity-report.md`) |
| Requirements | Deconstruct | `<slug>/requirements.md` in the framework folder (`../../framework/<slug>/requirements.md`) |
| Design plan | Design | `../../framework/<slug>/design-plan.md` |
| Test results | Test | `../../framework/<slug>/test-results.md` |
| SOP | writing-workflow-sops | the SOP |
| Run log | no step | the workflow's run log, where one was linked: an external link, or none, when the workflow's place is outside the registry's reach; both are fine |
| Raw source, Output | the leader | their own files |

**Legacy labels** ("Design spec", "Run guide", "Improvement plan") are tolerated on older nodes so
the lint passes, and never written. They say nothing about progress.

---

## 5. Progress and the leader-facing labels

There is no progress field. **Progress is read by the routing rule from the workflow's folder,
never from which links a node has:** the `framework-state` script where code can run, otherwise the
routing table by hand. Its states, by name:

0 Not a framework workflow, or retired · 1 Earlier version · 2 Redo pending · 3 Requirements
needed · 4 Plan needed · 5 Plan to approve · 6 Build needed · 7 Waiting on an open item · 8 Test
needed · 9 Waiting on access · 10 Ready to go live · 11 Live

Only the name ever reaches the leader, never the number. A node that is `in-production` with no
workflow folder is work Analyze recorded as already running (state 0), not a framework record.
State 0's name covers two things, so the views split it: **Runs outside the framework** for that
running work, **Retired** for a retired workflow.

**On the leader-facing views** (the dashboard and `REGISTRY.md`), fields show under these labels.
None shows a step number.

| Field | Label | Shown as |
|---|---|---|
| progress | Progress | the routing state's name |
| the last test round | Last test (dashboard only) | "[met] of [total] checks met across [k] inputs", worked out by `framework-state` from `test-results.md`, never stored; left out before any round |
| `stale_after` | Re-check by | the date |
| `autonomy` | How it decides | `deterministic`: "Deterministic: follows your instructions"; `guided`: "Guided: makes bounded decisions with your method"; `autonomous`: "Autonomous: works toward a goal you set" |
| `execution_mode` | Runs with you / Runs without you | `manual` and `augmented`: "Runs with you"; `automated`: "Runs without you" |

---

## 6. The re-check date

The re-check date is `stale_after`, a Workflow node field holding a date (`YYYY-MM-DD`). A live
workflow is **due for a re-check** when today is on or after it (the date is the start of that UTC
day). Test owns the field: it sets it
three months after go-live, resets it three months on at each passing re-check, and writes the same
date into the run log's header as `recheck_after`, where the workflow keeps a run log. No other
skill writes it.

`next_review` does not exist. It is a retired field: banned, never written, and named in this
bundle and in every skill only as something that is gone.

---

## 7. The registry log

`registry/log.md` follows OKF v0.3 §9. It has no frontmatter. Below its title and one-line
description, entries are grouped under `## YYYY-MM-DD` headings, **newest date first**, and each
entry is one bullet, its kind in bold. To add an entry, put it at the end of today's heading, the
first heading below the description; when the first heading isn't today's, write a new
`## YYYY-MM-DD` heading there first, with a blank line on each side. Nothing already in the log is
reworded, moved or removed: no skill rewrites an entry. It holds:

- **Setup decisions and schema changes:** `scaffolding-registry`'s founding entry
  (`- **Registry scaffolded** — [the founding line]`), and later changes to `SCHEMA.md`
  (`- **Schema change** — [what changed]`).
- **The dashboard's Claude Artifact link,** as `- Dashboard Artifact: <link>`; the newest entry
  wins.
- **The leader's checker ID,** once, at their first check: `- **Checker** — [name] checks pages as
  human:[id]` (*Record a check* in the indexing-registry skill).
- **One entry per workflow event,** written by the step that makes it, the workflow by its title:

| Event | Written by | Entry |
|---|---|---|
| A big change | Design, on "go ahead" | `- **Big change** — [workflow]: [reason]` |
| Go-live | Test | `- **Go-live** — [workflow] went live after test round [n]` |
| A re-check or change that passes | Test | `- **Re-check** — [workflow]: re-checked, ready` |
| A re-check not ready | Test | `- **Re-check** — [workflow]: re-check not ready` |
| A changed version not ready | Test | `- **Changed version** — [workflow]: changed version not ready` |

The big-change entry is the record of why a workflow was redesigned. When Deconstruct saves the
redo it removes `big_change` from the node, never the log entry. (With no registry, the reason is
kept in the old requirements' dated copy in `history/`.)

A registry still at OKF 0.2 has its older entries in the earlier form (`## date — title` headings
and `[date]: …` lines, oldest first). Read them as they are; a new entry still goes in the form
above, at the top. The upgrade (section 10) regroups the old ones.

Routine node writes and regenerations get no log entry.

---

## 8. Lint rule list

The single source both linters implement: the AI-performed pass in `indexing-registry` and the
scripted pass in `tools/lint-registry.js`. The consistency suite asserts string agreement between
the two.

**Errors:**

- Missing required frontmatter, or a malformed `generated` stamp (not a single-line map with `by`
  and `at`; `at` neither a UTC instant nor, on an older node, a bare date)
- Multi-line/block-scalar values
- Directory↔type disagreement
- Invalid enum values
- **Domain state in the wrong key** (OKF 0.3 registry): a domain value (`backlog`, `active`, …) in
  `status`, which is only `draft` | `stable` | `deprecated`; `state` on a type that has none
  (anything but Workflow, Business, LineOfBusiness); `state: retired` without `status: deprecated`.
  A registry still at OKF 0.2 may keep domain values in `status`: not an error there
- `superseded_by` that reaches no registry page
- `stale_after` that is neither a date nor a UTC instant (never read as fresh)
- Banned fields present (event facts and derived fields: `lob`/`sequence`/`process` anywhere,
  `owner` on Workflow, legacy `timestamp:`)
- Broken link targets (links resolved from the page's own folder, rule 4; in a registry still at
  OKF 0.2, an older bare link from the registry's parent folder)
- In-bundle link whose first segment is not a bundle directory or root file
- A file-relative link that lands inside the registry (OKF 0.3 registry): name the form to write,
  `../../…` when the link was meant from the working folder, otherwise the `/` form
- Curated-list violations (a node in zero or 2+ parent lists; an in-production Workflow in no
  Process list)
- Process `owner:` missing or matching no Function file
- Function node missing its GENERATED `# Owns` marker block
- Unterminated GENERATED block
- A concept file missing from its directory index, or a typed directory missing its `index.md`
  (index coverage)
- **Claims sweep:** an SOP claimed by no Workflow node's `# Artifacts` (or by more than one)
- SOP `workflow:` back-pointer disagreeing with the claiming node
- Run log evidence contradicting state: the workflow's run log has rows but the node is neither
  `in-production` nor `retired`. Checked only where the run log is readable inside the workspace; an external
  or absent "Run log" link is skipped

**Warnings:**

- **A registry still at OKF 0.2** (once per registry): offer the upgrade (section 10)
- Malformed actor string in `generated.by` or `verified` (not `process:<name>`, `human:<id>`,
  another `scheme:id`, or the agent form `<app>/<model id>`)
- A `verified` event missing `by` or `at` (ignored); a check the content has outrun (every
  `verified` `at` earlier than `generated.at`: the page is unverified until checked again)
- `superseded_by` without `status: deprecated`
- Root `index.md` frontmatter beyond `okf_version`, `title`, `description`, `license` and `x-`
  keys; any frontmatter in a subdirectory `index.md`
- `log.md` out of the §9 form (OKF 0.3 registry)
- `stale_after` overdue (shown to the leader as a re-check due)
- Backlog staleness (backlog node untouched more than six months: "triage or retire")
- Workflow in no Process list (not in production)
- A Note linking no bundle node ("probably misfiled")
- A workflow folder in the framework folder claimed by no Workflow node (`framework/<slug>/`
  on every platform; `framework/history/` is never a workflow folder)
- **Orphan capabilities:** skills or agents in the workspace referenced by no Workflow node
  ("capture the workflow")
- Stale GENERATED content: regenerate (a Function `# Owns` block whose content no longer matches
  the derived owners list; hand-editing between the markers is still prohibited, but a stale
  block is a maintenance-pass warning, never a lint blocker). Writing the block in its derived
  form isn't hand-editing: a step that creates a Process writes it into its owner's `# Owns`
  block itself, in the form under the indexing-registry skill's *Regenerate GENERATED blocks*

**Gitignore tolerance:** links into gitignored paths (such as a folder where the workflow's own
output lands) are declarations, not guarantees: existence-checked locally when the target is
present, skipped in CI via `git check-ignore`.

All lint messages are plain-language and name the file; fixes are offered, never silently
applied: the lint never repairs meaning on its own.

---

## 9. Closing step

After your skill's fields are written, invoke the `indexing-registry` skill for a maintenance pass.
It is **best-effort**: a failed refresh never fails your step. Its check covers the pages your step
wrote or changed, plus the cross-page essentials (every Process's owner matches a Function, every page
is in exactly one parent list and in its folder's index, links into and out of those pages resolve),
claims no more, and says nothing when they pass. To the leader it is "checking your registry", the
files are "pages", and no "maintenance pass", lint, script or `tools/` name is said unless they ask. Do not restate the maintenance pass
inline; point here. On the web, the pass writes in `registry/` in the working folder, through the connection.

---

## 10. Upgrading a registry from OKF 0.2

A registry whose root `index.md` says `okf_version: "0.2"`, or declares no version, was set up
before OKF v0.3. It still works: the tools and the AI-performed check read its older forms. The
`indexing-registry` skill offers the upgrade when the leader says "upgrade my registry", or once,
in plain words, when a maintenance pass finds one (never in the middle of another step).

The upgrade changes the form, never the content, so it moves no page's `generated` line (rule 2) and
keeps every key the tool doesn't own (rule 10):

1. The root `index.md`: `okf_version: "0.3"`.
2. Workflow, Business and LineOfBusiness nodes: a domain value in `status` moves to `state`; a
   retired Workflow also says `status: deprecated`. A Process with `status: retired` says
   `status: deprecated`.
3. Each link and `guide:`/`folder:` value written from the registry's parent folder becomes
   file-relative from what it reaches: `framework/<slug>/requirements.md` →
   `../../framework/<slug>/requirements.md` in a node, `.claude/skills/<name>/SKILL.md` →
   `../.claude/skills/<name>/SKILL.md` in the root `index.md`, an older `<slug>/requirements.md`
   that only resolves through `framework/` → `../../framework/<slug>/requirements.md`. Links in
   code spans and fenced blocks stay as they are.
4. `log.md`: the older entries regrouped under `## YYYY-MM-DD` headings, newest date first, each a
   bullet, every word kept: a `## [date] — [title]` entry becomes `- **[title]** — [its first
   paragraph]` under its date, with any further paragraph or list line indented two spaces below
   it; a `[date]: [text]` line becomes `- [text]` under its date; a `Dashboard Artifact:` line
   stays a bullet of its own, under the date of the entry before it. The log's title and
   description stay at the top as they are.
5. `registry/SCHEMA.md` replaced with the current one (the scaffolding-registry skill's
   `references/schema-template.md`), copied as it ships, its own `generated` line included: the
   schema's content does change, so this is the one file whose stamp moves.

Where code can run, `node tools/upgrade-registry.js` (`--check` first, to see what it will
change) does 1 to 4. On a drive the same changes are made page by page, saved as rule 8 says (on a
connection that can only create files, the whole pass saves once, at the end). Then a maintenance
pass regenerates the views.
