# Weekly Status Report — Run Card

## Your first real run

Friday 2026-06-12, on the live tracker: 11 updated tasks and 2 blockers. The skill
pulled the week, drafted, paused at the review gate, and saved
`status-report-2026-06-12.md` after Maya approved it with no edits — then logged the
run itself. Next Friday looks exactly like this.

## How to start it

Open a new chat **inside this project** in Cowork and say:
**"Run my weekly status report."** Give it nothing else — it pulls the week itself.
If someone else takes the Friday report over: they add both skills under
**Customize → Skills**, join the project, and use the same sentence.

This runs when you start it. If you later want it on a schedule, come back to this
step and we'll set that up.

## What to have ready

- **HubSpot connector authorized in the account that runs it**, with the
  "Q2 Delivery Tracker" list visible. Authorization does not carry over from another
  project, another session, or another person's account — this is the one that breaks.
- **Both skills installed in that account:** `weekly-status-report` and
  `status-report-drafting` under Customize → Skills. A fresh chat does not inherit a
  session's setup; this list is what it needs.
- `context/tone-guide.md` and `context/past-reports/` present in the project files
  panel (the tone guide is what keeps the draft from sounding generic).

## What to check before you act on the output

- **G1 — the review gate.** The skill stops and shows you the full draft before
  anything is saved or shared. You are deciding whether this is the report you would
  send: approve as-is, or edit and then approve. It does not proceed on silence.
- **G2 — ambiguous status.** If the skill asks which status a task really has, answer
  from the tracker, not from memory; it will not guess.
- **The (must) line:** every status in the report matches the tracker (AC1). Skim the
  blockers against the tracker — a mismatch there is a stop, not an edit.
- Also worth a glance: the four sections are in template order (AC2), and every blocker
  names an owner and a next action (R1).

## Log the run

One row per run in `outputs/weekly-status-report/runs.md` — date, input, result,
edits needed, notes. The orchestrator appends it at the end of every production run;
it did on today's, which is how we know that part works. Fill the notes cell yourself
with the minutes door to door — the Baseline is `Unknown` until four runs are timed. If a row is ever missing, the fix is
in the orchestrator skill, not the log — add the step back and re-run. Ten seconds a
week, and it is the evidence Step 7 reads instead of memory.

## Your first review

**2026-07-10** — monthly, as the skill sets for a weekly workflow, recorded as `stale_after`
on the workflow node. It is also when the Baseline becomes readable: the requirements
said four runs would establish the number that is missing today. When it arrives, or sooner if you find yourself editing every draft the same
way, start a new conversation and say: *"Run the improve skill on weekly status
report."* Bring nothing — the node, the test results, and the run log carry it.
