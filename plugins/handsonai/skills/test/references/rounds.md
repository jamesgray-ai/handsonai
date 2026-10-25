# Rounds

Read when you open a round after the first, re-check a live workflow, or find a round left behind or waiting on access. A round is one pass of Test: open, run, verdict, and go live when it's ready. One round, one results file.

**Contents:** 1. Finding the earlier rounds · 2. Which kind of round · 3. Carried results · 4. Re-checking a live workflow · 5. A round that pauses or is set aside

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

- **A task Build redid:** its built rev or "Last built after round" in the build record changed since the previous round.
- **A changed task:** its plan `rev` rose since the comparison round.
- **The comparison:** at the verdict, say in model wording any line met in the comparison round that misses now. A Ready round of a live workflow becomes the comparison point for later re-checks.

## 3. Carried results

An input's result carries from the round it last ran in only when every line graded on it there (Met or Not met) is met by tasks that haven't changed since: the same built rev, and not rebuilt after that round. A line graded on it that has changed wording since means the input runs again. Carried results are copied into the round's file, marked "carried from round [n]", and count toward Ready like any other.

## 4. Re-checking a live workflow

"Test the workflow I built" on a live workflow opens a `regression` round, or an `after-change` round after a small change. `status` stays `in-production` throughout.

- **A cloud routine on Claude Code** keeps its run log in the remote repository. Before the opening, say exactly "Your scheduled runs keep their run log in your remote repository. Pull it into this folder first: [steps]. Say 'done' when it's pulled." (N-T57) and wait for "done", so the opening and the flags read the routine's runs.
- **A team workflow** (the requirements' lens is Organizational): before the opening, as its own message, **Ask:** "Is the team using it, and is anyone stuck?" (N-T35) "Stuck": the SOP offer comes at the round's close. "Not using it": give "change my workflow" with the location in N-F2's form (model wording), and carry on with the re-check unless the leader stops it.
- **The opening** (the re-check form, or the after-change form after a change) shows the Target again when there is one, and how it's doing only where there's a run log (its runs since the comparison round, the time saved where the time-saved line applies, its flags). When the Target is "—", the Target sentence is left out and the run-log sentence stays.
- **Flags from the run log** are offered as practice inputs (N-T49, in SKILL.md).
- **On Claude Code,** every round on a live workflow adds the wrapper's allow back at the start of Part 2, with N-T47, and removes it at its close (`claude-code-runs.md`).
- **Ready:** `going-live.md` section 4. **Not ready:** SKILL.md's live verdict lines.

## 5. A round that pauses or is set aside

- **Set aside.** A round `in-progress` whose `plan_revision` isn't the current plan revision (the plan changed mid-round: a kept direct edit, a requirement change the plan had to catch up with, "change my workflow"), or whose number is at or below the build record's `last_close_after_round` (Build closed while it was open, as after a direct edit undone at Test): move it to `history/test-results-round-[n].md` with `round_status: abandoned`, and open a fresh round as round n+1, its kind by section 2. On Claude Code, clear its practice folder and run folders as at any close. So a Build close only ever follows a finished round.
- **Waiting on access** is a pause, not an end. When the connection passes its read check, the same round goes back to `round_status: in-progress`, keeps its number and its results, and runs only the inputs that couldn't run. If Build closed in the meantime, the round isn't reopened: an `after-fix` round opens instead. After a fix to a permission, rewrite the build record's "What it can access" for that connection.
- **A requirement change in Part 1 that the plan must catch up with:** no round file is written; the change is in the requirements' `revisions:`, and the next round's file copies it under Requirement changes.
