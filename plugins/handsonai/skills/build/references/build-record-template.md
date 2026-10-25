# The build record

Read at the first entry and at every record write. `build-record.md` sits in the workflow folder, beside the plan. Only Build writes it, except Test's go-live lines ("Live since", "How to switch it off", the rewritten older-version line), `schedule:`, and `write_block`, which Test sets to `off` when it lifts a block it took over from Build. Later steps and scripts parse its frontmatter keys, headings and table columns, so they're written exactly as below.

**Contents:** 1. When it's written · 2. The template · 3. Frontmatter values · 4. The table · 5. The two sections for people · 6. The older-version line · 7. Also in the record · 8. The Claude Code profile · 9. Never in the record

## 1. When it's written

- Created at your first entry, before the first task, even when every task waits on an open item.
- Each row written straight after its task's check; frontmatter values updated as they change.
- `plan_revision` and `last_close_after_round` set only at a close, never at a stop or a pause.
- "What was built" and "What it can access" written at every close, and "What it can access" again whenever a connection or permission changes.
- Saved after each task (local files, a drive that updates in place); at each part's end, after each main skill's task, and at every pause and stop on a drive that can only create files (the current file moved into `history/build-record-YYYY-MM-DD-HHMM.md` first); given to the leader on print-to-save.

## 2. The template

```markdown
---
plan_revision: [the plan revision at your last close; omitted until the first close]
last_close_after_round: [the last round's number at your last close, 0 before any round; omitted until the first close]
live_checks:
  [kind of change]: "done: [the place it landed]"
skills_on: yes
write_block: "off"
schedule: none
fingerprints:
  wrapper: sha256:[64 hex characters]
  [installed skill or agent, by its path]: sha256:[hex]
  [runtime context copy, by its path]: sha256:[hex]
bare_run:
  [main skill]: done
run_folders: []
change_requests: []
---

# [Workflow name] — Build Record

## What was built
[Live since YYYY-MM-DD. — Test's line, kept; the date in that form, which routing reads]
[How to switch it off: [steps] — Test's line, kept]

- [Each part and what it does, in plain words; where it lives; how to start it, and "practice run" to try it with nothing sent or changed.]
- [What's still waiting.]
- [Where the kept copy is.]
- An older version: [the line, section 6]

## What it can access
**[Connection] ([the account]).** [What it reads.] [What it can change, and which of those changes can't be undone.] [Each tool's class: a read only where it can't change anything.] [The permissions left off on purpose.] [What it never does.] [The checkpoints before a change.] [Anything under Work content that won't switch off, as reachable.]

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | [the Project / folder / workspace] | [where] | Created | yes | — | — | [memory switch confirmed] | — |

## Also
- Practice-run instruction: [its text, with its cue "practice run"]
- Places a dry run confirmed: [each place]
- Quick real checks: [each, where it landed, and every real change it made with its undo status: undone, left, or the leader's to remove; permanent ones marked]
- Bare run: [what the plain model handled, per main skill]
- [An agent on Microsoft 365: the instructions the leader last pasted back]
- Schedule: [the five points, one by one; any risk accepted, naming the change and the checkpoint; a checkpoint the leader chose to keep running by hand; the switch-on steps, withheld while incomplete]
- Put back the kept copy: [the steps]
- Remaining manual steps and prerequisites: [each]
- The package, for sharing: [where]

## Claude Code profile
[Claude Code only: the one framework-profile block, section 8]
```

## 3. Frontmatter values

The keys above and no others, in that order:
- **`live_checks`:** per kind of change, `done: [the place it landed]`, `declined`, `skipped` or `not yet`.
- **`skills_on`:** `yes` once checked.
- **`write_block`** (Claude Code): `off`, or a mapping with `on:` (this workflow's own deny rules, a rule another workflow also lists included), `leader_rules:` (deny rules the leader already had, never removed) and `leader_allow:` (the leader's allow rules when the block went on), as `claude-code-block.md` section 4 shows. Elsewhere, `off`.
- **`schedule`:** `none` with no `SCH` task (a first build with no set-aside); carried over from a set-aside record (missing there, or no record in the set-aside folder, counts as not `none`); `not-on` once every safety point passes; `safety-incomplete: [points]` when one fails, including a checkpoint the leader chose to keep running by hand; `paused` when the leader confirms a pause. There is no value for "on".
- **`fingerprints`:** at install, one per installed skill and agent (none for an agent Agent Builder made on Microsoft 365), one per runtime context copy you can read back, and on Claude Code `wrapper: sha256:<64 hex>` for `framework/.bin/test-run.sh`. Where no code can run, a part's size and date.
- **`bare_run`:** per main skill, `done` or `skipped: [why]`.
- **`run_folders`** (Claude Code): each fresh folder made for a check or a bare run, until it's cleared; `[]` otherwise.
- **`change_requests`:** in the one shape, each with exactly `id` (`B1`, `B2`…; never left out), `source` (`build`; `direct edit` for an edit the leader keeps, its edited text saved as `history/direct-edit-[id]-YYYY-MM-DD-HHMM.md` and `what` a one-line summary, in double quotes, naming that file, never the text itself), `what`, `why`, `tasks`, `after_round` (a number, 0 before any round). The track switch goes here too.

## 4. The table

One row per task, `KW` and `SCH` included, its Task cell the plan's task ID exactly (`T3`, `KW`, `SCH`, never "T3 (S2)"): a task with no row, or with another Task cell, reads as not built. Plus the orchestrator, each connection, each context item (its runtime copy), and the workflow's place. For example:

```markdown
| T3 | New skill: S2 | C1 | follow-up-drafter | package/skills/follow-up-drafter/ | Created | yes | 2 | 1 | E2: AC1–AC4 met | — |
```
- **Status:** `Created`, `Reused`, `Extended` or `Installed by you`, for what was made; `Built, misses [line]`, for a task finished with a known miss; `Waiting on [the open item]`, `Waiting on change request [id]`, `Failed check`, `Not built yet` or `Removed from the plan`, for what wasn't. The `SCH` row is `Created` with `schedule: safety-incomplete` too.
- **Saved:** `yes` once the part is kept where a later session can find it (installed, or staged in `package/`); on print-to-save, once the leader has the text; otherwise `no`.
- **Path or location:** `package/…` while a part is staged; its installed place once Part 3 installs it.
- **Built rev:** the task's `rev` when built. **Last built after round:** the last round's number when you last built or rebuilt it (0 before any round).
- **Check:** the result in one line ("E2: AC1–AC4 met"; "dry run confirmed: #sales-updates"; "read-back: 3 open deals"; for an agent that failed its paste-back, "Failed check, deleted" or "Failed check, not deleted").
- **Ruling:** "what, why, cost if wrong", or "—".

## 5. The two sections for people

In plain words, with no IDs; anyone the leader shows it to (IT, security, a manager) can see what the workflow can read and change.
- **What was built:** each part and what it does ("a skill that reads your open deals and drafts the Friday summary"); where it lives; how to start it (under its different name, where one was used), and "practice run" to try it with nothing sent or changed, and, on Microsoft 365 while release check 32 hasn't passed, attaching its context files from `Documents/Cowork/[workflow-slug]` each time; what's still waiting; where the kept copy is; and the older-version line. Keep Test's "Live since" and "How to switch it off" lines and the older-version line whenever you rewrite it.
- **What it can access,** one block per connection: the account; what it reads; what it can change, and which of those changes can't be undone; each tool's class; the permissions left off on purpose; what it never does (from the requirements' "It never…" rules and Prohibited actions); the checkpoints before a change.

## 6. The older-version line

Once N-B51 is answered, one line in "What was built", in one of these forms:
- **A yes:** "An older version: [where it's set up]; you paused it on [date] (a skill: you switched it off on [date]; or: it runs only when you start it)[; your copy is [in [place] / where you kept it / in your version history]][; the new one went in as [new name], so nothing was overwritten]. Switch it off for good when this one goes live." (the copy clause only where the new version is saved over the old one; the new-name clause where no copy could be kept).
- **A no or "not sure":** "An older version: none that you know of."
- **A part installed over it** (Part 2 on a first build on Claude Code and Codex, Part 3 elsewhere), rewritten: "An older version: [where]; this one replaced it when it was installed on [date]; your copy is [in [place] / where you kept it / in your version history].[ Still set up: [what of it you didn't install over, such as its schedule, paused on [date]]. Switch that off for good when this one goes live.]" It never names the new part's place as the older version's.
- **After go-live,** Test writes: "An older version: [where]; you switched it off on [date]."

The line is kept whenever the section is rewritten, and carried over a set-aside.

## 7. Also in the record

Under `## Also`: the places a dry run confirmed; the quick real checks and where they landed; every real change a quick real check made, with its undo status; the practice-run instruction's text; for an agent on Microsoft 365, the instructions the leader last pasted back; what the plain model handled in each bare run; the schedule's safety record and switch-on steps (withheld while incomplete); "Put back the kept copy"; the remaining manual steps and prerequisites; where the package is kept for sharing.

## 8. The Claude Code profile

On Claude Code only: the one block the wrapper builds every headless session from, under its own `## Claude Code profile` heading, in a fence opened with ` ```framework-profile `. Its grammar is in `claude-code-block.md` section 3. Write it at the block, and rewrite it whenever a connection, tool list, skill, agent or context file changes. It names an environment variable, never a secret's value. Elsewhere the heading and block are left out.

## 9. Never in the record

Copies of plan text or requirement wording, quoted update lines, `changed:` markers, or any check for a stale copy. The revision numbers and one current file per name make them unnecessary.
