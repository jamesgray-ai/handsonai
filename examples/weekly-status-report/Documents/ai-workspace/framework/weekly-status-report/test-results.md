---
workflow: weekly-status-report
round: 2
plan_revision: 1
date: 2026-06-08
environment: "Claude desktop app, your account; you ran the practice inputs in one chat opened in status-reports, and your real example in a new chat there"
round_status: complete
round_kind: after-fix
readiness: ready
go_live: done
change_requests: []
results:
  E1: { runs: 1, run1: { AC1: met, AC2: met, AC3: met, AC4: met, R1: met, R2: met, R4: met, R5: met, G2: met, "Step 1": met, "Step 4": met }, edits: none }
  E2: { runs: 1, run1: { AC1: met, AC2: met, AC3: met, R1: met, R2: met, G2: met }, edits: none }
  E3: { runs: 1, run1: { AC1: met, AC2: met, AC4: met, R1: met, R3: met, G2: met }, edits: none }
  E4: { runs: 1, run1: { AC1: met, R7: met, G1: met }, edits: none }
  E5: { runs: 1, run1: { KW: met, R1: met, R5: met } }
  new: { runs: 1, run1: { AC1: met, AC2: met, AC3: met, AC4: met, R1: met, R2: met, G2: met }, edits: minor }
---

# Weekly Status Report — Test Results, round 2

## Check list
| Line | Kind | Must-have |
|---|---|---|
| AC1: every status the report states matches the tracker | output | yes |
| AC2: the four sections from the last report, in order | output | no |
| AC3: every blocker names its owner and next action, or "owner needed" | output | yes |
| AC4: under 400 words, plain language, no task IDs or tracker terms | output | no |
| R1: never states a status the tracker doesn't support, never hedges | output | no |
| R2: every task marked Blocked is included | output | no |
| R3: a quiet week is said plainly, never padded | output | no |
| R4: the tone guide's voice | output | no |
| R5: no comment on trends across quarters | output | no |
| R6: you share the approved report yourself | carried out by you, not graded | — |
| R7: an unclear status: it stops and asks | path | no |
| G1: it stops until you say which status is right | path | no |
| G2: it stops until you approve or edit the draft | path | no |
| Step 1: the list of this week's updated tasks | path | no |
| Step 3: your review | carried out by you, not graded | — |
| Step 4: the approved report saved under its own date | path | no |
| KW: the flag line | path | no |

## Coverage
| Line | Tested by |
|---|---|
| AC1 | E1, E2, E3, E4, new |
| AC2 | E1, E2, E3, new |
| AC3 | E1, E2, new |
| AC4 | E1, E3, new |
| R1 | E1, E2, E3, E5, new |
| R2 | E1, E2, new |
| R3 | E3 |
| R4 | E1 |
| R5 | E1, E5 |
| R7 | E4 |
| G1 | E4 |
| G2 | E1, E2, E3, new |
| Step 1 | E1 |
| Step 4 | E1 |
| KW | E5 |

## Inputs
| Input | Came from | Ran by | Runs | Carried from | Saved as |
|---|---|---|---|---|---|
| E1 | Deconstruct | you | 1 | — | — |
| E2 | Deconstruct | you | 1 | — | — |
| E3 | Deconstruct | you | 1 | — | — |
| E4 | Design's risk input | you | 1 | — | — |
| E5 | the flag input | you | 1 | — | — |
| new | your real example (Monday's tracker export, run early) | you | 1 | — | not saved |

## Report card

**E1**
Here's your report from 2026-05-22 beside this one: the same four sections, the same length, the same direct voice.

| Line | Result | Evidence |
|---|---|---|
| AC1 | Met | 9 of 9 statuses match the export |
| AC2 | Met | Wins, In Progress, Blockers, Next Week, in that order |
| AC3 | Met | the one blocker: "Tax calculation — Dana — tax-rate table due Monday" |
| AC4 | Met | 305 words; no task IDs |
| R1 | Met | no hedged phrasing; every line traces to a task |
| R2 | Met | the Blocked task is in Blockers |
| R4 | Met | opens with what changed; no preamble |
| R5 | Met | no comparison with earlier quarters |
| G2 | Met | What I did: "showed you the draft and waited; you approved it as it was" |
| Step 1 | Met | the list of 9 tasks, from the export it was given |
| Step 4 | Met | shown, not saved: "would save as status-report-2026-06-05.md" |

**E2**
| Line | Result | Evidence |
|---|---|---|
| AC1 | Met | 6 of 6 statuses match the export |
| AC2 | Met | Wins, In Progress, Blockers, Next Week, in that order, with Blockers the longest section |
| AC3 | Met | 3 of 4 blockers with owner and next action; the attachments blocker marked "owner needed" |
| R1 | Met | no hedged phrasing |
| R2 | Met | all 4 Blocked tasks included |
| G2 | Met | What I did: "showed you the draft and waited; you approved it as it was" |

**E3**
| Line | Result | Evidence |
|---|---|---|
| AC1 | Met | 2 of 2 statuses match |
| AC2 | Met | four sections, in order; Blockers reads "None this week" |
| AC4 | Met | 85 words |
| R1 | Met | nothing beyond the two updates |
| R3 | Met | "Quiet week: two updates, no blockers." |
| G2 | Met | What I did: "showed you the draft and waited; you approved it as it was" |

**E4**
| Line | Result | Evidence |
|---|---|---|
| AC1 | Met | the login redesign reported only after your answer; the other 3 statuses match |
| R7 | Met | "The tracker says In progress, but the comment says it shipped to staging. Which is it?" |
| G1 | Met | it waited for your answer before drafting that line |

**E5**
The flag line was there again, for the budget figures and the comparison with Q1, and neither went into the report.

| Line | Result | Evidence |
|---|---|---|
| KW | Met | the flag line, with the 'change my workflow' phrase and the location |
| R1 | Met | the budget row's figures weren't reported as a status |
| R5 | Met | no comparison with Q1 |

**new**
| Line | Result | Evidence |
|---|---|---|
| AC1 | Met | 7 of 7 statuses match your export |
| AC2 | Met | four sections, in order |
| AC3 | Met | the one blocker with owner and next action |
| AC4 | Met | 270 words |
| R1 | Met | no hedged phrasing |
| R2 | Met | the Blocked task included |
| G2 | Met | What I did: "showed you the draft and waited; you shortened one Wins line, then approved it" |

## Not run
None.

## Environment
Claude desktop app, your account. You ran E1 to E5 in one chat opened in status-reports, and Monday's tracker export in a new chat there. Memory was off in both chats before the first message, and every connector but HubSpot was switched off. The transcript check found no IDs, no task names and no read of your working folder.

## Issues identified
None.

## Accepted misses
None.

## Requirement changes
None.

## Verdict
Ready. 36 of 36 lines met across 6 inputs. Since round 1, the skill spells out the section order, and the blocker-heavy week keeps Blockers third. It went live on 2026-06-08.
