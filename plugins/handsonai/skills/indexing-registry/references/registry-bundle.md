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
log · 8. Lint rule list · 9. Closing step

---

## 1. Where the registry is

| Where the leader works | Registry | Its parent folder |
|---|---|---|
| Claude Code, Codex | `registry/` in the workspace | the workspace, which also holds `framework/` |
| Claude desktop with a working folder | `registry/` inside the framework folder the leader added | the framework folder |
| Claude on the web, ChatGPT, Microsoft 365 Copilot (Cowork) | `Framework/registry/` in the leader's Google Drive or OneDrive, read and written through the platform's connection | `Framework/`, the framework folder |

A workflow's registry entry is its **Workflow concept node**, `registry/workflows/<slug>.md`, where
`<slug>` is the workflow's kebab-case ID, the same name as its folder in the framework folder. The
node is YAML frontmatter plus Markdown body sections, held inside an
[OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
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
2. **Stamp `generated` on every write.** Every node write (create or update) carries:

   ```yaml
   generated: { by: process:<skill-name>, at: <YYYY-MM-DDTHH:MM:SSZ> }
   ```

   `<skill-name>` is the writing skill's own name (`process:deconstruct`); `at` is the moment of
   the write as a UTC instant, such as `2026-10-24T15:04:05Z`. The lint accepts a bare
   `YYYY-MM-DD` on an older node; never write one.
3. **Never edit between GENERATED markers.** Content between `<!-- GENERATED:<name> -->` and
   `<!-- /GENERATED -->` is machine-owned: write around it, never inside it, and never leave a
   marker pair unterminated.
4. **Link discriminator, exact:**
   - Leading `/`: bundle-root-relative, resolved from `registry/` (`/processes/new-business.md`).
     The first path segment must be one of the bundle's directories or a root file.
   - No leading slash, not a URL: relative to the registry's parent folder (section 1), never
     `../`. On Claude Code and Codex that is the workspace (`framework/<slug>/requirements.md`);
     on the web and Claude desktop it is the framework folder (`<slug>/requirements.md`). The lint
     resolves both the same way.
   - A full URL: external.
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
8. **Saving on a drive.** Where the connection can update a file in place, it does. Where it can
   only create files but can move and rename them, before each save the current file moves into
   the framework folder's `history/`, under its registry path and renamed `[file]-YYYY-MM-DD-HHMM.md`
   (`history/registry/workflows/<slug>-2026-10-24-1504.md`), and the new file is
   created under its own name; such a step saves at the end of a part or a batch, not after every
   node. Nothing in the registry is ever shared, trashed or deleted on a drive.
9. **Print-to-save, only as the fallback.** With no files and no drive connection that can write,
   every write in this contract becomes: give the file complete, with its exact location, and say
   plainly that the leader must save it. Never report a file as written that you only gave. At
   the end of the step, list every file the leader needs to save.

**Bundle-wide anchors (consistency-check anchors, restated here on purpose):**

- The bundle root `index.md` declares `okf_version: "0.2"` in its frontmatter: the one index
  permitted a frontmatter block.
- Full enum block, all values, lint-enforced:
  - Workflow `status`: `backlog` | `under-development` | `in-production` | `retired`
  - `execution_mode`: `manual` | `augmented` | `automated`
  - `autonomy`: `deterministic` | `guided` | `autonomous`
  - `definition_type`: `step-driven` | `goal-driven`. No step writes it any more: it is
    tolerated on older nodes, with the legacy spellings `step-decomposed` and `outcome-driven`.
- `big_change`: free text, `"[reason], [date]"`, present only while a redo is pending.
- `stale_after`: a calendar date, `YYYY-MM-DD`.

---

## 3. Field ownership

| Skill | Writes |
|---|---|
| `analyze` | A Workflow node stub per registered candidate: `title`, `description` (outcome-first), `status: backlog`, `trigger` (provisional); its line in the confirmed Process's `# Workflows` list; `# Artifacts` → Opportunity report (`framework/ai-opportunity-report.md` on Claude Code and Codex, `ai-opportunity-report.md` on the web and Claude desktop). Work the leader already runs: `status: in-production` and its `# Skills` / `# Agents` entry (a link when the file is in the workspace, otherwise its name as plain text). A new process follows the same owning-function rule as `naming-workflows`. |
| `naming-workflows` | A Workflow node stub: `title`, `description` (outcome-first), `status: backlog`, `trigger`; its line in the chosen Process's `# Workflows` list. **A new process → asks which function owns it** and writes a complete minimal Process node (owner required). |
| `deconstruct` | `status`: `backlog` to `under-development` only (it never resets another status, on a re-run, a redo or running work brought in, which stays `in-production`); the refined `trigger`; the `description` the leader accepted, word for word; `# Artifacts` → Requirements; `big_change` removed when a redo is saved (the registry-log line stays). A cold-entry workflow with no node gets a new one in `naming-workflows`' stub format with `status: under-development`, listed in its Process's `# Workflows`. Finishing a set-aside that stopped partway, it removes any "Design plan" or "Test results" link still there; calling a big change off, it restores those links for the files moved back, each only if absent. |
| `design` | `execution_mode`, `autonomy`, on approval; `# Artifacts` → Design plan. A big change: `big_change` and one registry-log line (section 7). A set-aside (a big change, or a change of platform or mechanism, which writes no `big_change`): removes the "Design plan" and "Test results" links; finishing a set-aside that stopped partway, before a fresh plan, it removes any of those links still there. A retired workflow brought back by "change my workflow": `retired` to `under-development`. |
| `build` | `# Skills` / `# Agents` links for every skill and agent it built or reused, at its close. The build record has no link: it is found by its path, `[framework folder]/<slug>/build-record.md`. |
| `test` | `# Artifacts` → Test results, when a round closes. At go-live: `status: in-production`, `stale_after` three months on, and the go-live log line. At a passing re-check: `stale_after` reset three months on, and its log line. A changed version or a re-check not ready: its log line, `status` kept. A **Note node** on the leader's yes when a round surfaced a lasting insight, linked to the Workflow. |
| `writing-workflow-sops` | `# Artifacts` → SOP |
| `writing-process-guides` | Process node `guide:` frontmatter |
| The leader | `status: retired`, when they retire a workflow |

Every writer restamps `generated` (rule 2). `scaffolding-registry` writes no Workflow node; it
writes the bundle's skeleton and its founding log entry. Only `status` is schema-required on a
Workflow node, so a backlog stub lints clean without `execution_mode` or `autonomy`: `design`
writes both once the plan is approved, and nothing writes them earlier. A stub's `trigger` is
provisional: `deconstruct` may replace it; the never-overwrite rule protects values a leader set
through a framework step, not a stub-time guess. `scaffolding-registry` may set a Process node's
`guide:` when the leader's documents already include a process guide for it;
`writing-process-guides` owns the field thereafter.

---

## 4. Artifact links

Each `# Artifacts` entry is a plain bulleted link whose link text is the label itself
(`- [Requirements](framework/client-follow-up/requirements.md)`), because the lint and compose read
the label from the link text. Links follow rule 4's form.

| Label | Written by | Points at |
|---|---|---|
| Opportunity report | Analyze | `ai-opportunity-report.md` in the framework folder |
| Requirements | Deconstruct | `<slug>/requirements.md` in the framework folder |
| Design plan | Design | `<slug>/design-plan.md` |
| Test results | Test | `<slug>/test-results.md` |
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

**On the leader-facing views** (the dashboard and `REGISTRY.md`), fields show under these labels.
None shows a step number.

| Field | Label | Shown as |
|---|---|---|
| progress | Progress | the routing state's name |
| `stale_after` | Re-check by | the date |
| `autonomy` | How it decides | `deterministic`: "Deterministic: follows your instructions"; `guided`: "Guided: makes bounded decisions with your method"; `autonomous`: "Autonomous: works toward a goal you set" |
| `execution_mode` | Runs with you / Runs without you | `manual` and `augmented`: "Runs with you"; `automated`: "Runs without you" |

---

## 6. The re-check date

The re-check date is `stale_after`, a Workflow node field holding a date (`YYYY-MM-DD`). A live
workflow is **due for a re-check** when today is on or after it. Test owns the field: it sets it
three months after go-live, resets it three months on at each passing re-check, and writes the same
date into the run log's header as `recheck_after`, where the workflow keeps a run log. No other
skill writes it.

`next_review` does not exist. It is a retired field: banned, never written, and named in this
bundle and in every skill only as something that is gone.

---

## 7. The registry log

`registry/log.md` is append-only: no skill removes or rewrites a line in it. It holds:

- **Setup decisions and schema changes,** each as a dated `## <YYYY-MM-DD> — <title>` entry:
  `scaffolding-registry`'s founding entry, and later changes to `SCHEMA.md`.
- **The dashboard's Claude Artifact link,** as a `Dashboard Artifact: <link>` entry; the latest
  entry wins.
- **One line per workflow event,** written by the step that makes it, each on its own line, with
  the date as `YYYY-MM-DD` and the workflow by its title:

| Event | Written by | Line |
|---|---|---|
| A big change | Design, on "go ahead" | `[date]: [workflow]: big change: [reason]` |
| Go-live | Test | `[date]: [workflow] went live after test round [n]` |
| A re-check that passes | Test | `[date]: [workflow]: re-checked, ready` |
| A re-check not ready | Test | `[date]: [workflow]: re-check not ready` |
| A changed version not ready | Test | `[date]: [workflow]: changed version not ready` |

The big-change line is the record of why a workflow was redesigned. When Deconstruct saves the
redo it removes `big_change` from the node, never the log line. (With no registry, the reason is
kept in the old requirements' dated copy in `history/`.)

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
- Banned fields present (event facts and derived fields: `lob`/`sequence`/`process` anywhere,
  `owner` on Workflow, legacy `timestamp:`)
- Broken link targets (links resolved from the registry's parent folder, rule 4)
- In-bundle link whose first segment is not a bundle directory or root file
- Curated-list violations (a node in zero or 2+ parent lists; an in-production Workflow in no
  Process list)
- Process `owner:` missing or matching no Function file
- Function node missing its GENERATED `# Owns` marker block
- Unterminated GENERATED block
- A concept file missing from its directory index, or a typed directory missing its `index.md`
  (index coverage)
- **Claims sweep:** an SOP claimed by no Workflow node's `# Artifacts` (or by more than one)
- SOP `workflow:` back-pointer disagreeing with the claiming node
- Run log evidence contradicting status: the workflow's run log has rows but the node is neither
  `in-production` nor `retired`. Checked only where the run log is readable inside the workspace; an external
  or absent "Run log" link is skipped

**Warnings:**

- Malformed `generated.by` actor string (not `process:<name>` or `human:<id>`)
- `stale_after` overdue (shown to the leader as a re-check due)
- Backlog staleness (backlog node untouched more than six months: "triage or retire")
- Workflow in no Process list (not in production)
- A Note linking no bundle node ("probably misfiled")
- A workflow folder in the framework folder claimed by no Workflow node (`framework/<slug>/` on
  Claude Code and Codex; `<slug>/` beside `registry/` on the web and Claude desktop; `history/`
  and `registry/` are never workflow folders)
- **Orphan capabilities:** skills or agents in the workspace referenced by no Workflow node
  ("capture the workflow")
- Stale GENERATED content: regenerate (a Function `# Owns` block whose content no longer matches
  the derived owners list; hand-editing between the markers is still prohibited, but a stale
  block is a maintenance-pass warning, never a lint blocker)

**Gitignore tolerance:** links into gitignored paths (such as a folder where the workflow's own
output lands) are declarations, not guarantees: existence-checked locally when the target is
present, skipped in CI via `git check-ignore`.

All lint messages are plain-language and name the file; fixes are offered, never silently
applied: the lint never repairs meaning on its own.

---

## 9. Closing step

After your skill's fields are written, invoke the `indexing-registry` skill for a maintenance pass.
It is **best-effort**: a failed refresh never fails your step. Do not restate the maintenance pass
inline; point here. On the web, the pass writes in `Framework/registry/` through the connection.
Only on print-to-save does it give the updated `REGISTRY.md` with its location instead, for the
leader to save, and say so.
