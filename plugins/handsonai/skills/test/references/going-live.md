# Going live

Read for Part 4: on the leader's yes to "Take it live?", at state 10 when a go-live was interrupted (finish the remaining steps without asking again), and on every Ready round of a live workflow (section 4). Only the leader switches a schedule on, off or back on, or switches a version off: give the steps, wait for their word, and never say you did it.

**Contents:** 1. Going live for the first time · 2. Replacing another version · 3. The go-live message · 4. A re-check or change that passes · 5. The registry's log lines · 6. What Test doesn't do

## 1. Going live for the first time

In this order:

1. **The registry,** where there is one (on the web, `Framework/registry/`), as the indexing-registry skill's `registry-bundle.md` says: the node's `status: in-production`; `stale_after` three months on; the "Test results" link, in SKILL.md's form; one log line (section 5); `generated` restamped (`by: process:test`, `at` a UTC instant); then the indexing-registry maintenance pass (a pass that fails never stops the go-live), all with no text of its own, never a line on what you're writing, stamping or refreshing (a failed refresh, if you tell the leader, gets the 'update my registry' phrase with the location, as SKILL.md's *Close the round* gives it). With no registry, the build record's "Live since" line is the live marker.
2. **The build record's top section,** under "What was built": "Live since YYYY-MM-DD" (the date in that form, which routing reads; for a retired workflow brought back, rewritten with this date) and "How to switch it off: [steps for this platform: the schedule, then the skill or plugin]"; and `schedule:` (`none`; `not-on` once Build's switch-on steps are given; a `safety-incomplete` value left as Build wrote it).
3. **The run log,** only where the workflow writes one: `runs.md` (or `runs-[workflow-slug].md`) started where Build installed the workflow, header only, with `recheck_after` (the same date as `stale_after`; with no registry, three months on) and `first_time` (section 3's first-time items). For a retired workflow brought back that already has one, update its header. Never start one anywhere else, and never ask the leader to keep one.
4. **Nothing left switched on** (Claude Code): any block lifted, and the wrapper's allow removed (`claude-code-runs.md` section 7), then the settings read back.
5. **Replacing another version** (section 2), as its own message, before the go-live message.
6. **The go-live message** (section 3), once item 5 is answered.
7. **A team workflow:** the SOP offer (N-T52, in SKILL.md).
8. **A lasting insight** from the round, where there's a registry: **Ask:** "This round showed [the insight]. Shall I keep that as a note in your registry, for future workflows?" (N-T53) On a yes, write a Note node linked to the Workflow. The reply to the answer, when nothing else is left (no SOP, no Git save point), is the last message: a few words of acknowledgement (on a yes, that the note is saved), then, as its next action, model wording such as "Re-check it any time with 'test the workflow I built. My files are in [location].'"; never a summary of the round, of what you saved or of the registry, and never again that it's live or passed. That reply is one text, and the turn ends on it.
9. **The results:** `go_live: done`, the last write, made once nothing of the go-live is left to answer, as the last tool call of the turn whose message ends the go-live, just before that message (the go-live message when no question follows it; otherwise item 8's reply, or the SOP's close), never after it: so a go-live that stops before it (at a replacement question, the SOP or the note) still reads as state 10, and the next entry finishes what's left (SKILL.md, state 10).
10. **The Git save point,** where the folder is a repository (SKILL.md). On Claude Code with a schedule, the go-live message says to switch the schedule on after this save; for a cloud routine, Build's switch-on steps include the leader pushing it.

## 2. Replacing another version

Each question is its own message, before the go-live message, so the leader never reads "It's live" or switch-on steps while the older version is still set up: the first such question follows Part 4's signpost with nothing between them (the writes in section 1 aren't announced). Wait for the leader's word before going on. In N-T48's running-work form, the bracket is a phrase that follows "set up" directly, with no colon ("in Zapier, as the zap "Follow-up drafter", paused on 18 October"; "as a Claude Code desktop task that started the old skill every evening"), and the steps are a numbered list.

- **An earlier version of the framework** (the listing of `history/` shows an `earlier-version-*` folder newer than the build record's "Live since" date; a record without that line counts as never gone live): say exactly "Your earlier version of [workflow] may still have a schedule. Switch it off for good: [steps]. Say 'done', or 'no schedule'."
- **Running work brought in** (the requirements' `Runs today` row, and no "Live since" line in the build record), when the row says it was set up somewhere or ran on a schedule; and **an older version the leader told Build about** (the build record's older-version line names where it's set up, and what's still set up): say exactly "The way you ran [workflow] before is still set up [where its `Runs today` row places it, or what the build record's older-version line says is still set up]. Switch it off for good, so only the new version runs: [steps]. Say 'done', or 'already off'." After the line's replaced form, name only what it says is still set up (such as a schedule that called the replaced skill), never the new part: the steps find it by where it is and when it runs ("the task that runs every evening"), never by the skill it starts, whose name is now the new version's; when it names nothing, ask nothing. On "done" or "already off", rewrite the older-version line: "An older version: [where]; you switched it off on [date]." Work done by hand has nothing to switch off: ask nothing.
- **"An older version: none that you know of."** Ask nothing; the go-live message carries the reminder (section 3).
- **After a platform change** (the plan's `platform` differs from the newest set-aside plan's), at a live Ready round, **only until it's answered**: say exactly "Your earlier version of [workflow] still runs on [the old platform]. Switch it off for good: [its 'How to switch it off' steps]. Say 'done' when it's off." using the steps Build carried over from the set-aside record, wait for "done", then rewrite "How to switch it off" for the new platform and mark it answered: `old_platform_off: [that set-aside folder's name]` in this round's results. It's asked only when no results file (`test-results.md`, or `history/test-results-round-*.md`) already records that folder's name there, so a later re-check never asks it again; a newer platform change, with a newer set-aside folder, asks it once more.

After either N-T48 form, write "Live since" and "How to switch it off" (section 1 item 2) if they aren't there, so the question isn't asked again, and read `schedule: paused` as `none`: the paused schedule was the old version's, now switched off for good, so the new version's schedule comes as at a first go-live, never the switch-back form, and no second switch-off question.

## 3. The go-live message

Said exactly, with its parts chosen from the files, in this order, and nothing else: the message opens with "It's live." (or its by-hand form) and ends with its last part. Each part is said whole as one piece, as written: never split into two sentences, reworded around its quoted phrase, or turned into bullets or headings, and nothing of your own goes before, between or after the parts (wrong: "…My files are in [location].' That way the schedule is checked before it runs without you."; wrong: "Right now it runs only when you start it." before the schedule's line; wrong: "Client Follow-Up is now live. It passed its test on 20 October." in place of "It's live."; wrong: a list of what was saved, recorded or checked, a re-check date, or how to use or remove it). The re-check part's 'test the workflow I built' is said there exactly as written; in any line of your own it carries the location (SKILL.md, *Another step's start phrase*).

- **It's live:** "It's live." Where the schedule can't go on yet (`schedule: safety-incomplete`, or a schedule-only request waiting): "It's live to run by hand."
- **The first real run:** "Your first real run [does these for the first time: …]; check that each one works." The items: the real target, the first real changes, any action whose quick real check was declined, skipped or not yet made, and, when Test ran in a different account than Build (this round's `environment` names a different account from the build record's place and quick real checks), every kind of change. Each item is named from its `W` line's own system and action ("creates a draft in Gmail Drafts"), never with a verb or a reach the line doesn't have (wrong: "sends a draft to a real client" for a W line that creates a draft). The same items go in the run log's `first_time` header.
- **No older version the leader knows of** (the record's older-version line says "none that you know of"): "If an older version of [workflow] still runs anywhere, switch it off, so only this one runs."
- **The schedule** (the plan's `SCH` task):
  - Build wrote switch-on steps: "Run it by hand once on real work; when it's right, switch the schedule on: [steps][, after the save below]." ("after the save below" on Claude Code, where the Git save point follows.) Then write `schedule: not-on`.
  - Waiting on a safety fix or a schedule-only request: "Its schedule waits until [the point] is fixed: say 'change my workflow: [the schedule point]. My files are in [location].'"
  - The leader chose at Build to keep running it by hand (the schedule's safety record says so): "It runs by hand, as you chose. To put it on its schedule later, say 'change my workflow: [the schedule point]. My files are in [location].'"
  - No schedule in its plan: "To run it on a schedule later, say 'change my workflow: run it on a schedule. My files are in [location].', so the schedule is checked before it runs without you."
- **Other workflows paused for a shared skill** (the build record's "Also" lists "Paused for the shared skill [skill]: [workflow]"), at the first Ready round after the build that paused them, naming each, said exactly (N-T58): "You can switch [workflows] back on now; they use [skill], which just passed its test."
- **A schedule, and no run log:** "Check its run history now and then for anything it flags."
- **Re-check, and how to change it:** "Re-check it any time with 'test the workflow I built', especially if you find yourself editing more than you used to. To change it, say 'change my workflow. My files are in [location].'"
- **Time saved:** where the workflow writes a run log and the Baseline is still Unknown: "To see time saved later, note how long it takes you by hand next time and tell me with 'change my workflow. My files are in [location].'"

## 4. A re-check or change that passes

On a Ready round of a live workflow (a re-check, a change, or a fix after either), with no "Take it live?":

1. **Reset** `stale_after` (three months on) and the run log's `recheck_after`, and add the registry log line (section 5). This round becomes the comparison point. The round closed with `go_live: pending`; `go_live: done` is written last, once item 2 is answered and item 4 isn't waiting on an answer, as the last tool call before the message that ends the go-live (section 1, item 9).
2. **Replacing another version first,** where it applies (section 2): a live earlier-version workflow redone, or running work brought in, at its first Ready round; an older version still set up; a platform change.
3. **The live form of the go-live message** (N-T34's live form was already said in the verdict; it isn't said again), chosen by the build record's `schedule:` and the plan's `SCH` task, said exactly:
   - **Something new for the next real run** (a kind of change a task changed since the comparison round makes, a W line in its *Meets*; a quick real check now declined, skipped or not yet made for one; or every first-time item after a `first` round on a live workflow): "Your next real run [does these for the first time: …]; check that each one works." and update the run log's `first_time` header.
   - **`paused`, with Build's switch-on steps:** "Your [changed / fixed] version can go back to work: run it by hand once on real work; when it's right, switch its schedule back on: [steps]." Then write `schedule: not-on`.
   - **`paused`, and the current plan has no `SCH` task** (a schedule the leader made by hand and paused at Build, or one a fresh plan dropped): "Its plan doesn't run it on a schedule, so switch off the schedule you paused, and run it by hand. To run it on a schedule, say 'change my workflow: run it on a schedule. My files are in [location].'" Then write `schedule: none`.
   - **`safety-incomplete`:** "Its schedule stays paused until [the point] is fixed: say 'change my workflow: [the schedule point]. My files are in [location].'" Or, where the leader chose at Build to keep running it by hand: "Its schedule stays paused, and it runs by hand, as you chose. To put it back on its schedule, say 'change my workflow: [the schedule point]. My files are in [location].'" The value stays as Build wrote it.
   - **`not-on` and `none`:** nothing about the schedule.
   - **After N-T48** (section 2), `paused` reads as `none`: the first go-live's schedule sentence (or its no-schedule line), and write `not-on` where switch-on steps were given.
   - **Other workflows paused for a shared skill:** N-T58, as in section 3.
   - Then: "To change it, say 'change my workflow. My files are in [location].'"
4. **A team workflow** whose team question got "stuck": the SOP offer (N-T52, in SKILL.md).
5. Lift the settings (Claude Code), write `go_live: done`, and offer the Git save point, as at a first go-live.

**Running work brought in** counts as live throughout (its node is `in-production`), so its first Ready round, after a `first` round, takes this live form: N-T48's running-work form first where the work was set up somewhere or scheduled, then "Live since" and "How to switch it off" written, and every first-time item named.

## 5. The registry's log lines

One line each, in the registry log (`registry/log.md`):

| When | Line |
|---|---|
| A first go-live | `[date]: [workflow] went live after test round [n]` |
| A re-check or change that passes | `[date]: [workflow]: re-checked, ready` |
| A re-check not ready | `[date]: [workflow]: re-check not ready` |
| A changed version not ready | `[date]: [workflow]: changed version not ready` |

## 6. What Test doesn't do

- It never switches a schedule on or back on: it gives Build's steps.
- It doesn't check the first real run: the go-live message and the run log's first row cover it.
- There are no test records to clean up: Test never makes a real change. Build's quick real checks stay listed in the build record.
