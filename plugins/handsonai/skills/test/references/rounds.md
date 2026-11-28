# Rounds

Read when you open a round after the first, re-check a live workflow, or find a round left behind or waiting on access. A round is one pass of Test: open, run, verdict, and go live when it's ready. One round, one results file.

**Contents:** 1. Finding the earlier rounds · 2. Which kind of round · 3. Carried results · 4. Re-checking a live workflow · 5. A round that pauses, is set aside or waits on the policy check

## 1. Finding the earlier rounds

Read `test-results.md` and `history/test-results-round-*.md`, by round number. Skip everything under `history/set-aside-*/` and `history/earlier-version-*/`, and any round marked `round_status: abandoned`, whenever you look for the last round, the last Ready round or an earlier round, so a round set aside before it ran anything leaves the next round's kind as it would have been. The same listing of `history/` shows whether an `earlier-version-*` folder is newer than the last go-live (`going-live.md`).

## 2. Which kind of round

Set the kind when the round opens, checking in this order:

| Kind | When | What runs | Compared with |
|---|---|---|---|
| `first` | No earlier round outside set-aside and earlier-version folders: the first test after Build, or after a big change or a change of platform or mechanism | Every practice input, the flag input, and the new input | Nothing |
| `after-fix` | The last round was Not ready (and Build has closed since, or nothing in it was Build's); or it was Waiting on access and Build has closed since | The inputs that failed; the inputs graded on any line a task Build redid *Meets* (for an agent on Microsoft 365 that Build redid, every input that uses it); the new input; the rest carried. "Run them all" on request | The previous round |
| `after-change` | The plan has changed since the last Ready round (a `changes:` entry with `after_round` at or after that round's number), other than a put-back of the built version | The inputs graded on any line a changed task *Meets*; an input for any new line, written by you if none exists; the new input; the rest carried from the last Ready round. "Run them all" on request | The last Ready round |
| `regression` | Nothing in the plan has changed since the last Ready round, or the only change is a put-back (`what: put back the built version`): a live workflow re-checked; the built version reinstalled after an undone direct edit; a retired workflow brought back and reinstalled | Every practice input, the flag input, flags offered from the run log, and the new input | The last Ready round |

- **A leader's change:** in the round after one, each `leader's change` Issues row from the round before is graded as a line of its own (the change, in plain words: "no booking link in the email") on every input it touches, and every one of those inputs runs; the grading names it once for all of them (SKILL.md, *One grading message*). Once the round is Ready, the change folds into the check it belongs to, so later rounds keep checking it.
- **The round's opening says plainly what runs again** *(your words)*, by count and why: "the fix changed the skill every input uses, so all 6 earlier inputs run again, plus a new one". Never a muddle such as "all the ones your fix could affect, which is every one of them".
- **A task Build redid:** its built rev or "Last built after round" in the build record changed since the previous round.
- **A changed task:** its plan `rev` rose since the comparison round.
- **The comparison:** at the verdict, say in model wording any line met in the comparison round that misses now. A Ready round of a live workflow becomes the comparison point for later re-checks.

## 3. Carried results

An input's result carries from the round it last ran in only when every line graded on it there (Met or Not met) is met by tasks that haven't changed since: the same built rev, and not rebuilt after that round. A line graded on it that has changed wording since means the input runs again. Carried results are copied into the round's file, marked "carried from round [n]", and count toward Ready like any other.

## 4. Re-checking a live workflow

"Test the workflow I built" on a live workflow opens a `regression` round, or an `after-change` round after a small change. `status` stays `in-production` throughout.

- **A cloud routine on Claude Code** keeps its run log in the remote repository. Before the opening, say in your own words that its scheduled runs keep their run log in the remote repository, so pull it into this folder first ([steps]), and say 'done' when it's pulled (N-T57, *your words*), and wait for "done", so the opening and the flags read the routine's runs.
- **A team workflow** (the requirements' lens is Organizational): before the opening, as its own message, **Ask:** "Is the team using it, and is anyone stuck?" (N-T35, *your words*) "Stuck": the SOP offer comes at a Ready round's close (Part 4, `going-live.md` section 4); a round that isn't Ready makes no SOP offer. "Not using it": give "change my workflow" with the location in N-F2's form (model wording), and carry on with the re-check unless the leader stops it.
- **The opening** (the re-check form, or the after-change form after a change) shows the Target again when there is one, and how it's doing only where there's a run log (its runs since the comparison round, the time saved only where the built workflow has the time-saved line (an older file's known Baseline), its flags). When the Target is "—", the Target sentence is left out and the run-log sentence stays.
- **Flags from the run log** are offered as practice inputs (N-T49, *your words*, in SKILL.md).
- **On Claude Code,** a round on a live workflow where the AI runs the inputs adds the wrapper's allow back at the start of Part 2, with N-T47, and removes it at its close; when the leader runs them (release check 6 open, or N-T42), nothing is allowed and N-T47 isn't asked (`claude-code-runs.md`, section 1).
- **Ready:** `going-live.md` section 4. **Not ready:** SKILL.md's live verdict lines.

## 5. A round that pauses, is set aside or waits on the policy check

- **Set aside.** A round `in-progress` whose `plan_revision` isn't the current plan revision (the plan changed mid-round: a kept direct edit, a requirement change the plan had to catch up with, "change my workflow"), or whose number is at or below the build record's `last_close_after_round` (Build closed while it was open, as after a direct edit undone at Test): move it to `history/test-results-round-[n].md` with `round_status: abandoned`, and open a fresh round as round n+1, its kind by section 2. On Claude Code, clear its practice folder and run folders as at any close. So a Build close only ever follows a finished round.
- **Waiting on access** is a pause, not an end. When the connection passes its read check, the same round goes back to `round_status: in-progress`, keeps its number and its results, and runs only the inputs that couldn't run. If Build closed in the meantime, the round isn't reopened: an `after-fix` round opens instead. After a fix to a permission, rewrite the build record's "What it can access" for that connection.
- **The return visit after a policy wait is not a new round.** When the last round's only blocker was the policy wait (Verdict reason "Waiting on the policy check ([value])"), the requirements still read `Policy check: Not sure — to check` or `Policy check: No — not live until approved`, and nothing else changed since that round (its `plan_revision` is the plan's current one, no Build close since it, no other requirement revision since it): open no round, write no new results file, re-run nothing. Open with one line naming the workflow and where it stands (model wording, with N-F3's promise clause), then the policy confirm question, in the same message. On a yes: *Changing a requirement* step 7 (`requirement-lines.md`), then rewrite the last round's results to Ready, `readiness: ready` and `go_live: pending`, its Verdict reason replaced with "Policy check confirmed on [date]" (`results-template.md` section 2). The plan is unchanged and the revision is `plan_unaffected: true`, so routing returns state 10. Then N-T34's Ready form with "Take it live?"; a no or a stop leaves the round Ready, and the next entry is state 10. With no yes, the policy Not-ready line again, and stop; a "no" takes the "no" route (SKILL.md, the verdict). If anything else changed, the visit is an ordinary round of the kind section 2 sets, with the confirm question last.
- **After a policy "no":** while the last round's Verdict reason is "The policy check came back no" and the requirements haven't changed since, say that round's "no" line again and stop, with no confirm question. Once the requirements change, the next round is an ordinary one.
- **A requirement change in Part 1 that the plan must catch up with:** no round file is written; the change is in the requirements' `revisions:`, and the next round's file copies it under Requirement changes.

## The opening of a round after the first

In SKILL.md's *The opening*, item 3, these take the place of the `first` round's row. Each is said in your own words, with every fact it carries, ending with the ask for the round's new input.

| Round | Opening |
|---|---|
| `after-fix` | "This round re-runs [n] inputs: the ones that failed, the ones your fix could affect, and one new one. The others passed and nothing they use changed. To start, give me one more real example, or say 'write one for me'. You can also say 'use the newest', and it reads the newest [input] since [the last round's date] from [source] without changing anything." (the "use the newest" sentence only when the input comes through a connection) |
| `after-change` | "This round checks what your change could affect: [n] inputs[, including one for [the new rule in plain words]], and one new one. The rest passed on [date] and nothing they use changed.[ You set [the Target].][ How it's doing: it has run [n] times since[, saving about [hours]][, and flagged [n] things it wasn't designed for].] To start, give me one real example from your recent work, or say 'write one for me'. You can also say 'use the newest', and it reads the newest [input] since [the last round's date] from [source] without changing anything." (the Target sentence on a live workflow with a Target, never when it's "—"; the how-it's-doing sentence only where there's a run log, its saving clause only where the built workflow has the time-saved line; the "use the newest" sentence only when the input comes through a connection) |
| Re-check of a live workflow (`regression`) | "This re-checks your live workflow against what it did on [date].[ You set [the Target].][ Since then it has run [n] times[, saving about [hours]][, and flagged [n] things it wasn't designed for].] To start, give me one real example from your recent work, or say 'write one for me'. You can also say 'use the newest', and it reads the newest [input] since [the last round's date] from [source] without changing anything." (the same conditions as the after-change opening). A team workflow (the requirements' lens is Organizational) first gets N-T35 as its own message, and a Claude Code cloud routine N-T57 before the opening (`references/rounds.md`) |

A `regression` round on a workflow that isn't live now (a retired workflow brought back, or the built version put back before any go-live) takes the re-check opening (N-T26, *your words*) too, since every input runs again against the last round that passed, in its non-live form, in your own words: "This re-checks your workflow against what it did on [date].[ You set [the Target].][ Since then it has run [n] times[, saving about [hours]][, and flagged [n] things it wasn't designed for].] To start, give me one real example from your recent work, or say 'write one for me'. You can also say 'use the newest', and it reads the newest [input] since [the last round's date] from [source] without changing anything." (the same conditions as the live form)

