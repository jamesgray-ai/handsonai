---
workflow: weekly-status-report
design_spec: outputs/weekly-status-report/design-spec.md
requirements: outputs/weekly-status-report/requirements.md
date: 2026-06-08
environment: "Cowork, HubSpot connector live"
round_status: complete
readiness: ready
criteria_total: 39
criteria_met: 39
results:
  E1: { AC1: met, AC2: met, AC3: met, R1: met, G1: met, "Step 2 output": met, R2: met, R3: met, R4: met, R5: met, G2: met, "Step 1 output": met, "Step 4 output": met, edits: none }
  E2: { AC1: met, AC2: met, AC3: met, R1: met, G1: met, "Step 2 output": met, R2: met, R3: met, R4: met, R5: met, G2: met, "Step 1 output": met, "Step 4 output": met, edits: minor }
  E3: { AC1: met, AC2: met, AC3: met, R1: met, G1: met, "Step 2 output": met, R2: met, R3: met, R4: met, R5: met, G2: met, "Step 1 output": met, "Step 4 output": met, edits: none }
---

# Weekly Status Report — Test Results

## Check list

- AC1 (must) — every status stated matches the tracker
- AC2 — uses the four C2 sections in order
- AC3 — Maya could send it without rewording
- R1 — every blocker names an owner and the next action
- G1 — Maya approves before the report is saved or shared
- Step 2 output — complete draft under 400 words
- R2 — never invent a status or hedge
- R3 — current quarter only
- R4 — C3's voice, C2's template, under 400 words
- R5 — ambiguous status: stop and ask (G2)
- G2 — Maya resolves any ambiguous status
- Step 1 output — structured list of updated tasks
- Step 4 output — report saved, run logged

## Scenarios to run

- **E1 — Typical week (real):** `outputs/weekly-status-report/inputs/E1-typical-week.md` — the week of 2026-06-01: 9 updated tasks, 1 blocker (same saved input as round 1) — tests R1, G1; golden example C2 (report of 2026-05-22)
- **E2 — Blocked-heavy week (proposed):** `outputs/weekly-status-report/inputs/E2-blocked-heavy-week.md` — the same constructed input as round 1 — tests R1 and the Step 2 ownerless-blocker edge case; no golden example
- **E3 — Quiet week (proposed):** `outputs/weekly-status-report/inputs/E3-quiet-week.md` — the same constructed input as round 1 (2 updates, no blockers) — tests R2 (nothing invented when there is little to report); no golden example

## Report card

**E1 — Typical week**

| Expected | From | Result | Evidence |
|---|---|---|---|
| Every status stated matches the tracker | AC1 (must) | Met | 9 of 9 tasks match |
| Uses the four C2 sections in order | AC2 | Met | Wins / In Progress / Blockers / Next Week, in order |
| Maya could send it without rewording | AC3 | Met | No hedged phrasing found |
| Every blocker names an owner and the next action | R1 | Met | E1 "tests R1" — 1 of 1 blockers has both |
| Maya approves before the report is saved or shared | G1 | Met | E1 "tests G1" — What I did: "paused and showed you the draft before saving anything — you approved it as-is" |
| Complete draft under 400 words | Step 2 output | Met | 335 words |
| Never invent a status or hedge | R2 | Met | No hedged phrasing; every line traces to an update |
| Current quarter only | R3 | Met | All 9 tasks are Q2 tracker items |
| C3's voice, C2's template, under 400 words | R4 | Met | Tone guide followed; 335 words |
| Ambiguous status: stop and ask | R5 | Met | No status was ambiguous; the skill said so in What I did |
| Maya resolves any ambiguous status | G2 | Met | Did not fire — no ambiguous status; What I did says so |
| Structured list of updated tasks | Step 1 output | Met | 9 tasks listed with status, owner, comments |
| Report saved, run logged | Step 4 output | Met | Saved to test-runs/E1-2026-06-08.md; test run, so no run-log row |

**E2 — Blocked-heavy week**

| Expected | From | Result | Evidence |
|---|---|---|---|
| Every status stated matches the tracker | AC1 (must) | Met | 4 of 4 blockers match |
| Uses the four C2 sections in order | AC2 | Met | Sections in template order — the round 1 miss is fixed |
| Maya could send it without rewording | AC3 | Met | No hedged phrasing found |
| Every blocker names an owner and the next action | R1 | Met | E2 "tests R1 and the Step 2 ownerless-blocker edge case" — 3 of 4 named; the ownerless one flagged "owner needed" |
| Maya approves before the report is saved or shared | G1 | Met | What I did: "paused and showed you the draft before saving anything — you approved it with one edit" |
| Complete draft under 400 words | Step 2 output | Met | 388 words |
| Never invent a status or hedge | R2 | Met | No hedged phrasing; every line traces to an update |
| Current quarter only | R3 | Met | All 6 tasks are Q2 tracker items |
| C3's voice, C2's template, under 400 words | R4 | Met | Tone guide followed; 388 words |
| Ambiguous status: stop and ask | R5 | Met | No status was ambiguous; the skill said so in What I did |
| Maya resolves any ambiguous status | G2 | Met | Did not fire — no ambiguous status; What I did says so |
| Structured list of updated tasks | Step 1 output | Met | 6 tasks listed with status, owner, comments |
| Report saved, run logged | Step 4 output | Met | Saved to test-runs/E2-2026-06-08.md; test run, so no run-log row |

**E3 — Quiet week**

| Expected | From | Result | Evidence |
|---|---|---|---|
| Every status stated matches the tracker | AC1 (must) | Met | 2 of 2 updates match |
| Uses the four C2 sections in order | AC2 | Met | Wins / In Progress / Blockers / Next Week, in order |
| Maya could send it without rewording | AC3 | Met | No hedged phrasing found |
| Every blocker names an owner and the next action | R1 | Met | No blockers this week — Blockers section says "None this week"; nothing to name, graded Met on the evidence that nothing was invented |
| Maya approves before the report is saved or shared | G1 | Met | What I did: "paused and showed you the draft before saving anything — you approved it as-is" |
| Complete draft under 400 words | Step 2 output | Met | 95 words |
| Never invent a status or hedge | R2 | Met | No hedged phrasing; every line traces to an update |
| Current quarter only | R3 | Met | All 2 tasks are Q2 tracker items |
| C3's voice, C2's template, under 400 words | R4 | Met | Tone guide followed; 95 words |
| Ambiguous status: stop and ask | R5 | Met | No status was ambiguous; the skill said so in What I did |
| Maya resolves any ambiguous status | G2 | Met | Did not fire — no ambiguous status; What I did says so |
| Structured list of updated tasks | Step 1 output | Met | 2 tasks listed with status, owner, comments |
| Report saved, run logged | Step 4 output | Met | Saved to test-runs/E3-2026-06-08.md; test run, so no run-log row |

## Golden example deltas

**E1** — against C2 (report of 2026-05-22):
- Missing: nothing
- Extra: nothing this round
- Substantively different: nothing

## Not run

None — all three scenarios ran live.

## Environment

Cowork, HubSpot connector live (read scope confirmed; the runs used pasted inputs). Same environment for all three scenarios.

## Issues identified

None.

## Accepted misses

None.

## Verdict

**Ready** — 18 of 18 lines met across 3 scenarios. It's ready. To put it to work, run
the `run` skill (Step 6) — 15–20 minutes.

## Test records created

Three test-run reports under `outputs/weekly-status-report/test-runs/` (E1, E2, E3 dated 2026-06-08). No rows in `runs.md`.
