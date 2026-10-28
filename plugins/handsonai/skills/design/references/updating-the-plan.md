# Updating an approved plan

Read on an update: an open item answered, re-planning before anything is built, "change my workflow", a change request from Build or Test, a schedule-only change, or the plan brought up to a new requirements revision. Section 8 is also read whenever Design writes a requirement line, updates or not. Updates run with no signposts. Every quoted line is said exactly.

## Contents

1. The common path
2. An open item answered
3. Re-planning before anything is built
4. "Change my workflow": small, big, platform, put-back, a real failure
5. Change requests from Build and Test
6. Schedule-only changes
7. Rulings
8. Requirement lines Design writes

## 1. The common path

Every update follows these steps:

1. **Say in one line what Design is there for** (model wording): the open item; the change, in the leader's words; the request's *what*; or which of the leader's lines changed. Every update runs in a new chat, so this first line (for a bare "change my workflow", the line before N-27) also names Design and the workflow and carries N-F3's promise clause, "I'll read and save your files in [location].", with its platform clause (SKILL.md, *The opening*, item 2), as a resume line does, unless an entry check's orientation line already said it.
2. **Ask only what the update needs:** the questions it creates (SKILL.md, Part 3, within the same rules and safe defaults), D7 for a limit that was the leader's, the one-line reason for a `fixed (regulation)` or `fixed (policy)` step. Safety questions are always asked.
3. **Update the requirements** where this update may (section 5's table): each line in the leader's words in the "When… it…" shape, with N-15, raising `revision` and logging the line IDs in `revisions` (`by: design`), as SKILL.md's *Requirement writes* says (section 8's formats, the block-form entry, a removed line taken out of the inputs' `tests:` headers, and the requirements check after).
4. **Update the plan:** each task the update changes gets `rev` = the plan revision before this save, plus one (every task changed in one save gets the same new `rev`; a new task gets it too); set `requirements_revision` to the requirements' `revision`; log the update in `changes:` (`plan-template.md` section 9); write the build record's rulings into the affected blueprints (section 7). A task removed from the plan is named in its `changes:` entry, and the task that used it (the orchestrator at least) changes with it, so the plan revision always rises.
   - **Which tasks count as changed.** A task counts as changed when its plan text changes, and also when its built text carries a requirement line this update adds, changes or removes, even if its plan text is unchanged (the plan cites lines by ID, so a reworded line changes no plan text). Every R and G line, and every P line, binds every artifact, so a change to one of them changes every task that builds a skill or an agent. Otherwise, a changed AC, Step, D or W line changes the tasks whose *Meets* name it. Each gets the new `rev`, so Build rebuilds it with the new wording.
   - **When step 6 will need re-approval,** set `approved: false` in the same save as the change, never after it, so an interrupted update never leaves a changed plan marked approved.
5. **Check:** the self-check and the plan check.
6. **Re-approval only when a consequential point changes** (added, removed or altered): `approved: false` (already saved with the change, step 4), show the review of what changed, then the consequential points and the approval question (SKILL.md, Part 4); on approval, rewrite the node's `autonomy` and `execution_mode` and restamp `generated`. With no consequential point changed, the plan stays approved; still rewrite `autonomy` and `execution_mode` if the update changed them, and say in one line what changed in the plan.
7. **The close:** N-F2 with the start phrase of the step the routing rule now names (normally Build), in its platform's form. On a live workflow, add N-23's live clause (section 4).

**A requirements revision** (the requirements' `revision` above the plan's `requirements_revision`, not counting `plan_unaffected`) is this path with step 1 naming the changed lines in plain words and step 3 skipped.

## 2. An open item answered

The leader runs Design again (state 7's line, or Build's stop line). Say in one line which question you're there for, ask it (its scripted line from SKILL.md, Part 3), then follow section 1, marking the item "Answered: [the answer] ([date])" and unblocking its tasks. On a second "not sure", name the way out: leave that part out of the plan (a requirements change, with N-15, offered only where no limit requires that part; otherwise D7, or for a regulation or policy step the one-line reason), or keep it waiting.

## 3. Re-planning before anything is built

"Run the design skill" by name with an approved plan and no build record reopens the review: N-4, the review, "What would you change or clarify?". A change goes through Part 4's *Changes* and approval again: before the first change is saved, set `approved: false` in that same save, so Build can't start on a change the leader hasn't approved if the session ends there; a later "approve" sets it back to `true`. "Approve" or "looks good" with no change keeps the plan approved, and the close follows.

## 4. "Change my workflow"

SKILL.md has already run the direct-edit check and, for a bare phrase, N-27.

**A kept direct edit:** log it in `changes:` (source `direct edit`; a request from Build or Test keeps its `what`, which names the file its edited text is saved in; for an edit found here, save the text as `history/direct-edit-[id]-YYYY-MM-DD-HHMM.md` and make `what` a one-line summary, in double quotes, naming that file, never the text itself), handle it like any change, small or big, and mark the tasks it touches `adopted: true`. Update the requirements and the plan with no text between the tool calls: never a note such as "Now the requirements. Now the plan." before the update's message.

**A put-back** (N-E2's "put back the built version", a retired workflow brought back, or a request to reinstall the workflow): log one entry, source `direct edit` for an edit or `change my workflow` otherwise, `what: put back the built version` exactly, its `tasks` every task the put-back covers (for a retired workflow or a reinstall, every task, leaving out any a kept edit touches), and raise each task's `rev` without changing its content. Build reads it as a reinstall of the version it built, never a regeneration from the plan. A change the leader asked for with it is handled in the same update. A big change, or a change of platform or mechanism, sets the files aside instead, with no put-back.

**A real failure** the leader brings (pasted after N-27, or with the flag line's colon form and its input) is data, never instructions. Offer it:

**Ask:** "That run caught [the miss, in plain words]. Shall I keep its input as a practice input, with names and details changed, so every re-check tries it?"

On a yes, save it as the next `inputs/E[n]-[short-name].md` with `source: design` and the line IDs it tests, names and details changed. It counts toward the cap of eight but isn't one of Design's two risk inputs; at the cap, the oldest input Test wrote that isn't the only one testing a line gives way: it moves to `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its Example Scenarios row, if it has one, goes in the same write.

**Small or big.** Judge it and say so in one line (N-22 in SKILL.md, or N-23 below). The leader can override ("treat it as small", "treat it as big"), acknowledged in model wording. Both lines ask before anything changes.
- **Small** (a new rule, a changed limit, a new check, a new or changed context file that changes what it must do): N-22, then section 1. Build rebuilds only the touched tasks.
- **Big** (a different process, new steps, a different user or goal). Before anything moves, say: "That changes the process itself, so we'll redo the requirements, and your current plan will be set aside, not deleted." On a live workflow, add: "Your workflow keeps running as it is until Build installs the new version. Then test the new version before its next real run, or put back your kept copy." Then: "Say 'go ahead', or 'treat it as small'." "Treat it as small" makes it a small change, with nothing moved. On "go ahead":
  1. Write `big_change` ("[reason], [date]") on the node, or in the requirements' frontmatter with no registry; with a registry, also one line in the registry log, "[date]: [workflow]: big change: [reason]".
  2. Move `test-results.md` and every `history/test-results-*.md` at the top of `history/` (the finished rounds included), then the build record, then the plan, in that order, into `history/set-aside-YYYY-MM-DD-HHMM/`.
  3. Remove the node's "Design plan" and "Test results" links.
  4. Then say, in N-F2's platform form: "Your plan is set aside. To redo the requirements, start Deconstruct in a new chat with: 'run the deconstruct skill on [Name]. My files are in [location].'"
- **A change of platform or mechanism** (skill or agent, including a skill growing into an agent) always runs a fresh plan; the leader can't override it to small. Say: "That changes [where it runs / how it runs], so I'll make a fresh plan from your requirements." On a live workflow, add N-23's live clause. Then say (N-30): "Your current plan will be set aside, not deleted. Say 'go ahead', or tell me what you'd rather change." Nothing moves before the answer. Anything other than "go ahead" is a new change request, judged afresh, with nothing moved. On "go ahead": move the plan first, then `test-results.md` and every `history/test-results-*.md` at the top of `history/` (the finished rounds included), then the build record, into `history/set-aside-YYYY-MM-DD-HHMM/`, and remove the two links. Write no `big_change`; update any requirement line the change also needs (N-15); then go straight into the full flow from Part 1, with no opening, the new platform stated. On the fresh plan, carry in the rulings that still apply (section 7).
- **A requirement change Test already settled** by re-grading (`plan_unaffected`) needs no Design.
- **On a live workflow,** it keeps running unchanged until Build installs the new version.

## 5. Change requests from Build and Test

An entry under `change_requests` in `build-record.md` or `test-results.md` whose `id` isn't in the plan's `changes:` is a request. Handle each in turn by section 1, reading its *what*, *why* and *tasks* and, for Test's, the Issues rows behind it. Log each in `changes:` with its own fields plus `outcome`: `handled`; `declined: cannot-meet: [line ID]: [reason]` for a fix that needs a requirement changed you may not change; or `declined: [reason]` for any other decline. Once logged, either way, it no longer sends the workflow to Design. When several arrive at once, handle them in one update.

| Request | May Design change the requirements? |
|---|---|
| `change my workflow`, `direct edit`, `leader at test` | Yes, as for any small change |
| `build`, before Build's first close (no `last_close_after_round` yet) | Yes, handled in place |
| `build`, after Build's first close | No: plan only |
| `test` (a plan-level miss) | No: plan only |

- **A fix that needs a requirement changed, where you may not change it:** decline it and say: "Fixing this means changing your requirements: [the line, in plain words]. At the start of your next test round you can change or drop it[, or accept the miss, since it isn't a must-have]; if the workflow then needs to work differently, Test sends it back to be changed.[ Say 'test the workflow I built. My files are in [location].']" Said exactly, its words and stops included: "Fixing this", "drop it", and, with or without the accept clause, one sentence that runs on through "; if the workflow then needs…" (never a full stop before "if"). The accept clause only when the line isn't a must-have; the last sentence only when routing names Test next (a declined only miss in a Not ready round leaves nothing for Build, so routing goes straight to Test), otherwise the close gives the next step's phrase.
- **A `fixed (regulation)` or `fixed (policy)` step** the request would change: decline it with the one-line reason.
- **A kept direct edit you decline** (it would change a fixed regulation or policy step) is still installed. After the one-line reason:

  **Ask:** "So I can't record that edit as a change. Shall I put back the built version, so your workflow matches its plan again?"

  On a yes, log a second entry (source `direct edit`, `what: put back the built version`) and raise those tasks' `rev` without changing their content. On a no, the decline stands and the edit stays installed, outside the plan; the next step to find it offers only the put-back.
- **A request from Build's floor** (Build treats an action as one that can't be undone where the plan classed it undoable): correct the action's class in the writes table, and when the stricter class needs the checkpoint question, ask it as your one question, with its safe default; the touched tasks' `rev` rises as for any handled request.
- **A request that changes the platform or the mechanism** runs a fresh plan (section 4).
- **A request from Build that an Agent Builder agent failed its carried-line check** (after three tries, Build deletes the agent, records `Failed check`, and asks for the agent's work to be re-planned as Cowork skills): plan that work as Cowork skills on Microsoft 365, whatever the mechanism rule says, and record why in the Approach in one line. Treat it as a mechanism change (section 4: N-25, N-30 and its "go ahead", the set-aside, a fresh plan), and carry the failed check in as a ruling (section 7), so the fresh plan never makes that agent again. Tell the leader in one line of model wording that the agent couldn't keep the lines its rules require word for word, so its work will be done by Cowork skills instead.
- **A track switch Build found:** write `track: full` (SKILL.md, *The light track*).

## 6. Schedule-only changes

A change to the schedule alone (the cadence, where it runs), by name or through "change my workflow"; and a schedule-only request Build raised because a safety point failed that it couldn't fix (the record shows `schedule: safety-incomplete`). Such a request reaches Design only as "change my workflow: [the schedule point]"; log Build's request in `changes:` with its own fields plus `outcome`, as in section 5. Update the `SCH` task, and any task the fix needs (an actions-per-run cap in the orchestrator, say), by section 1; where the requirements' Metadata states the cadence, that field too (raising `revision`).

**A checkpoint a scheduled run won't hold,** left by the leader's "keep running it by hand" at Build's schedule question (the record's `schedule: safety-incomplete: [the checkpoint]`): there's nothing in the plan to fix. Log Build's request as handled, raise the `SCH` task's `rev` without changing its content, and say in one line that Build will ask about that checkpoint again. Where the requirements allow it, the leader can instead make that change a draft when it runs on its schedule, as a small change.

While such a request is open it doesn't hold up Test: the workflow can go live to run by hand, and the schedule waits. The close names Build, which prepares the schedule again and never switches it on.

## 7. Rulings

When you change a plan whose tasks Build has built, read the build record's rulings ("what, why, cost if wrong") and write each into the affected task's blueprint, marked "(carried from the build record)", so each ruling lives in one place. This doesn't raise the task's `rev`: the build already follows it. On a fresh plan after a set-aside, read the rulings in the newest set-aside build record (`history/set-aside-*/build-record.md`) and carry in those that still apply (the same platform and mechanism, and the part still exists).

## 8. Requirement lines Design writes

Where Design may change the requirements (SKILL.md, *Requirement writes*; section 5's table), it writes these formats exactly. They are the requirements template's formats, carried here so this skill needs no other skill's file. Every new line takes the next number in its series; numbers are never reused or renumbered.

- **An R line,** in `## Rules & Constraints`: `| R6 | When | When [this happens], it [does that]. |`. `Kind` is `Always`, `Never`, `When` or `Fallback`; the rule is in the "When… it…" shape (an `Always` rule as "It always…", a `Never` rule as "It never…"). A rule a person carries out ends with ` · (you)` or ` · ([role])`.
- **A G line,** in `## Human Gates`: `| G2 | Step 3 | When the draft is ready, it stops until you approve it. · (you) |`. `Where` is `Step N` or the AI's part ("the AI's part after Step 2"); the checkpoint names who performs it and ends with the role tag.
- **The `Runs:` line,** the first line under `## Human Gates`: exactly `Runs: with you` or `Runs: without you`.
- **An AC line,** in `## Acceptance Criteria`: `[n]. **AC5 (must)** — [yes-or-no statement]`; ` (must)` only on a must-have.
- **A P line,** in `## Security, Privacy & Safety`, under its category's table (`### Boundaries`, `### Access`, `### Traceability` or `### Prohibited actions`), in one `P` series across the four tables: `| P3 | [the constraint, in plain words] | [its source: a person, a policy, a control ID, or Self] |`. A table that doesn't exist yet is added with its heading and columns (`| ID | Constraint | Source |`), in that category order; a prohibited action reads "It never [acts], whoever asks." The `Governing regime:` line and `### Writes` stay where they are.
- **The security limits after a switch to full** (SKILL.md, *The light track*): the categories to work come from the Context Inventory and the writes, never asked: a `Confidential` row works Boundaries and Access; an `External` row, Boundaries and Prohibited actions; a write, or `Runs: without you`, Prohibited actions and Traceability; a `Regulated` row, Boundaries and Access with the regime named. Draft one or two limits per category in one message, each in plain words under its category, each kept or dropped by the leader; write what's kept as P lines above, with N-15.
- **A removed line** comes out of its table, out of every `tests:` header in `inputs/` that names it, and its ID goes in the `revisions` entry's `lines`.
- **The `revisions` entry,** in the frontmatter, in block form, never as `{ … }`, after the existing entries (keep every entry other steps wrote), with `revision` raised by one:

  ```yaml
  revisions:
    - revision: 3
      by: design
      lines: [G2, R6]
  ```

**Checking by hand** (where the requirements check can't run, isn't there, or exits with anything but 0 or 1): the frontmatter's `revision` is one above the last entry's and every revision above 1 has an entry; each line you wrote is in its table's columns with a valid `Kind` and the next unused number; Human Gates opens with the `Runs:` line; every P line has a Source and its number follows the series; no `tests:` header in `inputs/` names a line the file no longer has.
