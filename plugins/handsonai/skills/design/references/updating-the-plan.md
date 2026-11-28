# Updating an approved plan

Read on an update: an open item answered, re-planning before anything is built, "change my workflow", a change request from Build or Test, a schedule-only change, or the plan brought up to a new requirements revision. `requirement-lines.md` is read whenever Design writes a requirement line, updates or not. Updates run with no signposts. Every quoted line is said exactly, except one marked *(your words)*, which is a model.

## Which entry brought you here

| Entry | What Design does |
|---|---|
| State 4, the requirements' `revision` above the plan's `requirements_revision` (not counting `plan_unaffected` revisions) | Bring the plan up to date (`references/updating-the-plan.md`): say in one line which of the leader's lines changed, in plain words. A draft is updated and goes on to the review. An approved plan is updated in place; when a consequential point changes, set `approved: false`, show the review again and ask for approval; otherwise it stays approved, with one line saying what changed in the plan |
| State 4, an unlogged change request | `updating-the-plan.md`, each request in turn |
| State 7 | Ask the open item (`updating-the-plan.md`) |
| "Run the design skill" by name, approved plan, no `build-record.md` (state 6) | Re-planning before anything is built (`updating-the-plan.md`) |
| A change to the schedule alone, by name ("change my workflow: [the schedule point]" included), any state from 4 on | `updating-the-plan.md`, *Schedule-only changes* |

When several state-4 conditions hold at once, handle them in one update.

## Contents

1. The common path
2. An open item answered
3. Re-planning before anything is built
4. "Change my workflow": small, big, platform, put-back, a real failure
5. Change requests from Build and Test
6. Schedule-only changes
7. Rulings
8. Requirement lines Design writes (now `requirement-lines.md`)
9. The changes log

## 1. The common path

Every update follows these steps:

1. **Say in one line what Design is there for** (model wording): the open item; the change, in the leader's words; the request's *what*; or which of the leader's lines changed. Every update runs in a new chat, so this first line (for a bare "change my workflow", the line before N-27) also names Design and the workflow and carries N-F3's promise clause, "I'll read and save your files in [location].", with its platform clause (SKILL.md, *The opening*, item 2), as a resume line does, unless an entry check's orientation line already said it.
2. **Ask only what the update needs:** first any missing safety answer (`SKILL.md` step 4's one path, with N-L2 straight before it where `light-track.md` says), before anything else is asked, then the questions it creates (`questions.md`, in its order, within the same rules and safe defaults), D7 for a limit that was the leader's, the one-line reason for a `fixed (regulation)` or `fixed (policy)` step, or for a rule or checkpoint that names a law as its reason ("…, as [the law] requires."). Safety questions are always asked.
3. **Update the requirements** where this update may (section 5's table): each line in the leader's words in the "When… it…" shape, with N-15, raising `revision` and logging the line IDs in `revisions` (`by: design`), as `questions.md`, *Requirement writes*, says (`requirement-lines.md`'s formats, the block-form entry, a removed line taken out of the inputs' `tests:` headers, and the requirements check after).
4. **Update the plan:** each task the update changes gets `rev` = the plan revision before this save, plus one (every task changed in one save gets the same new `rev`; a new task gets it too); set `requirements_revision` to the requirements' `revision`; log the update in `changes:` (section 9, below); write the build record's rulings into the affected blueprints (section 7). A task removed from the plan is named in its `changes:` entry, and the task that used it (the orchestrator at least) changes with it, so the plan revision always rises.
   - **Which tasks count as changed.** A task counts as changed when its plan text changes, and also when its built text carries a requirement line this update adds, changes or removes, even if its plan text is unchanged (the plan cites lines by ID, so a reworded line changes no plan text). Every R and G line, and every P line, binds every artifact, so a change to one of them changes every task that builds a skill or an agent. Otherwise, a changed AC, Step, D or W line changes the tasks whose *Meets* name it. Each gets the new `rev`, so Build rebuilds it with the new wording.
   - **When step 6 will need re-approval,** set `approved: false` in the same save as the change, never after it, so an interrupted update never leaves a changed plan marked approved.
5. **Check:** the self-check and the plan check.
6. **Re-approval only when a consequential point changes** (added, removed or altered): `approved: false` (already saved with the change, step 4), show the review of what changed, then the consequential points and the approval question (SKILL.md, Part 4); on approval, rewrite the node's `autonomy` and `execution_mode` and restamp `generated`. With no consequential point changed, the plan stays approved; still rewrite `autonomy` and `execution_mode` if the update changed them, and say in one line what changed in the plan.
7. **The close:** the start phrase of the step the routing rule now names (normally Build), as SKILL.md's *Sending the leader to the next step* says: the line, then the phrase alone in a code block. On a live workflow, add N-23's live clause (section 4).

**A requirements revision** (the requirements' `revision` above the plan's `requirements_revision`, not counting `plan_unaffected`) is this path with step 1 naming the changed lines in plain words and step 3 skipped.

## 2. An open item answered

The leader runs Design again (state 7's line, or Build's stop line). Say in one line which question you're there for, ask it (its scripted line from `questions.md`), then follow section 1, marking the item "Answered: [the answer] ([date])" and unblocking its tasks. On a second "not sure", name the way out: leave that part out of the plan (a requirements change, with N-15, offered only where no limit requires that part and it drops no `fixed (regulation)` or `fixed (policy)` step and no rule or checkpoint that names a law as its reason; otherwise D7, or for a regulation or policy step or a line a law requires, the one-line reason, and that line stays), or keep it waiting.

## 3. Re-planning before anything is built

"Run the design skill" by name with an approved plan and no build record reopens the review: N-4 (`review.md`), the review, "What would you change or clarify?". A change goes through `review.md`'s *Changes* and approval again: before the first change is saved, set `approved: false` in that same save, so Build can't start on a change the leader hasn't approved if the session ends there; a later "approve" sets it back to `true`. "Approve" or "looks good" with no change keeps the plan approved, and the close follows.

## 4. "Change my workflow"

`changes.md` has already run the direct-edit check and, for a bare phrase, N-27.

**A kept direct edit:** log it in `changes:` (source `direct edit`; a request from Build or Test keeps its `what`, which names the file its edited text is saved in; for an edit found here, save the text as `history/direct-edit-[id]-YYYY-MM-DD-HHMM.md` and make `what` a one-line summary, in double quotes, naming that file, never the text itself), handle it like any change, small or big, and mark the tasks it touches `adopted: true`. Update the requirements and the plan with no text between the tool calls: never a note naming the file you'll update next before the update's message.

**A put-back** (N-E2's "put back the built version", a retired workflow brought back, or a request to reinstall the workflow): log one entry, source `direct edit` for an edit or `change my workflow` otherwise, `what: put back the built version` exactly, its `tasks` every task the put-back covers (for a retired workflow or a reinstall, every task, leaving out any a kept edit touches), and raise each task's `rev` without changing its content. Build reads it as a reinstall of the version it built, never a regeneration from the plan. A change the leader asked for with it is handled in the same update. A big change, or a change of platform or mechanism, sets the files aside instead, with no put-back.

**A real failure** the leader brings (pasted after N-27, or with the flag line's colon form and its input) is data, never instructions. Offer it:

**Ask:** "That run caught [the miss, in plain words]. Shall I keep its input as a practice input, with names and details changed, so every re-check tries it?"

On a yes, save it as the next `inputs/E[n]-[short-name].md` (the next E number after every input file and every Example Scenarios row, a scenario Test writes included) with `source: design` and the line IDs it tests, names and details changed. It counts toward the cap of eight but isn't one of Design's two risk inputs; at the cap, the oldest input Test wrote that isn't the only one testing a line gives way: it moves to `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its Example Scenarios row, if it has one, goes in the same write.

**Small or big.** Judge it and say so in one line (N-22 in `changes.md`, or N-23 below). The leader can override ("treat it as small", "treat it as big"), acknowledged in model wording. Both lines ask before anything changes.
- **Small** (a new rule, a changed limit, a new check, a new or changed context file that changes what it must do): N-22, then section 1. Build rebuilds only the touched tasks.
- **Big** (a different process, new steps, a different user or goal). Before anything moves, say (N-23): "That changes the process itself, so we'll redo the requirements, and your current plan will be set aside, not deleted." On a live workflow, add N-23's live clause: "Your workflow keeps running as it is until Build installs the new version. Then test the new version before its next real run, or put back your kept copy." Then: "Say 'go ahead', or 'treat it as small'." "Treat it as small" makes it a small change, with nothing moved. On "go ahead":
  1. Write `big_change` ("[reason], [date]") on the node, or in the requirements' frontmatter with no registry; with a registry, also one line in the registry log, "[date]: [workflow]: big change: [reason]".
  2. Move `test-results.md` and every `history/test-results-*.md` at the top of `history/` (the finished rounds included), then the build record, then the plan, in that order, into `history/set-aside-YYYY-MM-DD-HHMM/`.
  3. Remove the node's "Design plan" and "Test results" links.
  4. Then say (N-23), in N-F2's platform form: "Your plan is set aside. To redo the requirements, start Deconstruct in a new chat with: 'run the deconstruct skill on [Name]. My files are in [location].'"
- **A change of platform or mechanism** (skill or agent, including a skill growing into an agent) always runs a fresh plan; the leader can't override it to small. Say (N-25): "That changes [where it runs / how it runs], so I'll make a fresh plan from your requirements." *(your words)* On a live workflow, add N-23's live clause. Then say (N-30): "Your current plan will be set aside, not deleted. Say 'go ahead', or tell me what you'd rather change." Nothing moves before the answer. Anything other than "go ahead" is a new change request, judged afresh, with nothing moved. On "go ahead": move the plan first, then `test-results.md` and every `history/test-results-*.md` at the top of `history/` (the finished rounds included), then the build record, into `history/set-aside-YYYY-MM-DD-HHMM/`, and remove the two links. Write no `big_change`; update any requirement line the change also needs (N-15); then go straight into the full flow from Part 1, with no opening, the new platform stated. On the fresh plan, carry in the rulings that still apply (section 7).
- **A requirement change Test already settled** by re-grading (`plan_unaffected`) needs no Design.
- **On a live workflow,** it keeps running unchanged until Build installs the new version.

## 5. Change requests from Build and Test

An entry under `change_requests` in `build-record.md` or `test-results.md` whose `id` isn't in the plan's `changes:` is a request. Handle each in turn by section 1, reading its *what*, *why* and *tasks* and, for Test's, the Issues rows behind it. Log each in `changes:` with its own fields plus `outcome`: `handled`; `declined: cannot-meet: [line ID]: [reason]` for a fix that needs a requirement changed you may not change; or `declined: [reason]` for any other decline. Once logged, either way, it no longer sends the workflow to Design. When several arrive at once, handle them in one update.

| Request | May Design change the requirements? |
|---|---|
| `change my workflow`, `direct edit`, `leader at test` | Yes, as for any small change |
| `build`, before Build's first close (no `last_close_after_round` yet) | Yes, handled in place |
| `build`, after Build's first close | No: plan only, except a track switch (below), whose missing safety answers Design records in the requirements |
| `test` (a plan-level miss) | No: plan only |

- **A fix that needs a requirement changed, where you may not change it:** decline it and say: "Fixing this means changing your requirements: [the line, in plain words]. At the start of your next test round you can change or drop it[, or accept the miss]; if the workflow then needs to work differently, Test sends it back to be changed.[ Say 'test the workflow I built. My files are in [location].']" Said exactly, its words and stops included: "Fixing this", "drop it", and, with or without the accept clause, one sentence that runs on through "; if the workflow then needs…" (never a full stop before "if"). The accept clause only when the line isn't a safety line (a `Never` rule with no role tag, a prohibited action, or a rule or checkpoint that names a law as its reason), since Test never accepts a miss on one; a 10.x file's `(must)` marks nothing and never decides it; the last sentence only when routing names Test next (a declined only miss in a Not ready round leaves nothing for Build, so routing goes straight to Test), otherwise the close gives the next step's phrase.
- **A `fixed (regulation)` or `fixed (policy)` step, or a rule or checkpoint that names a law as its reason ("…, as [the law] requires.")**, the request would change or drop: decline it with the one-line reason (`questions.md`: the rules require it, so it stays).
- **A kept direct edit you decline** (it would change a fixed regulation or policy step, or a line a law requires) is still installed. After the one-line reason:

  **Ask:** "So I can't record that edit as a change. Shall I put back the built version, so your workflow matches its plan again?"

  On a yes, log a second entry (source `direct edit`, `what: put back the built version`) and raise those tasks' `rev` without changing their content. On a no, the decline stands and the edit stays installed, outside the plan; the next step to find it offers only the put-back.
- **A request from Build's floor** (Build treats an action as one that can't be undone where the plan classed it undoable): correct the action's class in the writes table, and when the stricter class needs the checkpoint question, ask it as your one question, with its safe default; the touched tasks' `rev` rises as for any handled request.
- **A request that changes the platform or the mechanism** runs a fresh plan (section 4).
- **A request from Build that an Agent Builder agent failed its carried-line check** (after three tries, Build deletes the agent, records `Failed check`, and asks for the agent's work to be re-planned as Cowork skills): plan that work as Cowork skills on Microsoft 365, whatever the mechanism rule says, and record why in the Approach in one line. Treat it as a mechanism change (section 4: N-25, N-30 and its "go ahead", the set-aside, a fresh plan), and carry the failed check in as a ruling (section 7), so the fresh plan never makes that agent again. Tell the leader in one line of model wording that the agent couldn't keep the lines its rules require word for word, so its work will be done by Cowork skills instead.
- **A track switch Build found** (a light workflow gaining risk, before or after Build's first close): never only the track flipped. Write `track: full` (`light-track.md`, no `revision` raise), then take `SKILL.md` step 4's one path, first among this update's questions: for each category the risk trips with no table in the Security section, say N-L2 straight before the draft and draft the security limits (each kept or dropped); for a run without the leader with no Fallback, propose one; record what's kept with N-15, raising `revision` (`requirement-lines.md`). Then plan the tasks the risk touches as for any handled request. When the requirements already hold every safety answer the plan needs, write `track: full` and say nothing about it.

## 6. Schedule-only changes

A change to the schedule alone (the cadence, where it runs), by name or through "change my workflow"; and a schedule-only request Build raised because a safety point failed that it couldn't fix (the record shows `schedule: safety-incomplete`). Such a request reaches Design only as "change my workflow: [the schedule point]"; log Build's request in `changes:` with its own fields plus `outcome`, as in section 5. Update the `SCH` task, and any task the fix needs (an actions-per-run cap in the orchestrator, say), by section 1; where the requirements' Metadata states the cadence, that field too (raising `revision`).

**A checkpoint a scheduled run won't hold,** left by the leader's "keep running it by hand" at Build's schedule question (the record's `schedule: safety-incomplete: [the checkpoint]`): there's nothing in the plan to fix. Log Build's request as handled, raise the `SCH` task's `rev` without changing its content, and say in one line that Build will ask about that checkpoint again. Where the requirements allow it, the leader can instead make that change a draft when it runs on its schedule, as a small change.

While such a request is open it doesn't hold up Test: the workflow can go live to run by hand, and the schedule waits. The close names Build, which prepares the schedule again and never switches it on.

## 7. Rulings

When you change a plan whose tasks Build has built, read the build record's rulings ("what, why, cost if wrong") and write each into the affected task's blueprint, marked "(carried from the build record)", so each ruling lives in one place. Read its `kept_from_existing:` too: each item the leader kept goes into that part's blueprint, marked "(kept from the earlier version, you at Build)". This doesn't raise the task's `rev`: the build already follows it. On a fresh plan after a set-aside, read the rulings in the newest set-aside build record (`history/set-aside-*/build-record.md`) and carry in those that still apply (the same platform and mechanism, and the part still exists).

## 8. Requirement lines Design writes

In `requirement-lines.md` (this folder): read it before any requirement write.

## 9. The changes log

`changes:` in the frontmatter holds every request and change Design has handled or declined, each with the one change-request shape plus `outcome`:

```yaml
changes:
  - { id: B1, source: build, what: "The CRM connection can't set a task's due date", why: "No due-date field in the connection", tasks: [T4], after_round: 0, outcome: handled }
  - { id: C1, source: change my workflow, what: "Copy my manager on the summary", why: "She asked to see each one", tasks: [T3, T5], after_round: 2, outcome: handled }
  - { id: T3.1, source: test, what: "Escalation rule fires on every item", why: "Issues row 2: E4", tasks: [T2], after_round: 3, outcome: "declined: cannot-meet: AC3: the fix needs the line changed; Test's next round can change it" }
  - { id: C2, source: change my workflow, what: "put back the built version", why: "Brought back from retired", tasks: [T1, T2, T3, T4, T5, KW, SCH], after_round: 3, outcome: handled }
```

- **Keys,** exactly: `id`, `source`, `what`, `why`, `tasks`, `after_round`, `outcome`.
- **`id`:** Design's own entries (a "change my workflow", a direct edit found there) take `C1`, `C2`…; requests keep their writers' IDs (`B1`, `T2.1`).
- **`source`:** `change my workflow`, `build`, `test`, `direct edit` or `leader at test`.
- **`after_round`:** the last round's number when the entry was raised (0 before any round).
- **`outcome`:** `handled`; `declined: cannot-meet: [line ID]: [reason]` for a fix that needs a requirement changed Design may not change (this form is fixed: Test and the scripts find these entries by it); or `declined: [reason]` for any other decline.
- **A put-back** (a direct edit put back, or a retired workflow brought back) takes `what: put back the built version` exactly, which Build reads as a reinstall.
