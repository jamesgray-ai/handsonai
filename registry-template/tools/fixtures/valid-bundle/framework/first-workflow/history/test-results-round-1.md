---
workflow: first-workflow
round: 1
plan_revision: 1
date: 2026-06-24
environment: "Claude Code; the AI ran E1 to E3 headless through the wrapper; you ran the new input; practice folder: practice/"
round_status: complete
round_kind: first
readiness: not-ready
change_requests: []
results:
  E1: { runs: 2, run1: { AC1: met, AC2: met, R1: met }, run2: { AC1: met, AC2: met, R1: met }, edits: none }
  E2: { runs: 2, run1: { AC1: met, R1: not-met }, run2: { AC1: met, R1: met }, edits: major }
  E3: { runs: 2, run1: { KW: met, R1: met }, run2: { KW: met, R1: met } }
  new: { runs: 1, run1: { AC1: met, AC2: met, R1: met }, edits: none }
---

# First Workflow — Test Results, round 1

## Check list
| Line | Kind | Must-have |
|---|---|---|
| AC1 | output | yes |
| AC2 | output | no |
| R1 | output | no |
| G1 | path | no |
| KW | path | no |

## Coverage
| Line | Tested by |
|---|---|
| AC1 | E1, E2 |
| AC2 | E1 |
| R1 | E2 |
| G1 | E1 |
| KW | E3 |

## Inputs
| Input | Came from | Ran by | Runs | Carried from | Saved as |
|---|---|---|---|---|---|
| E1 | Deconstruct | the AI | 2 | — | — |
| E2 | Deconstruct | the AI | 2 | — | — |
| E3 | the flag input | the AI | 2 | — | — |
| new | your real example (a signing this week) | you | 1 | — | not saved |

## Report card
None.

## Not run
None.

## Environment
Claude Code in this workspace.

## Issues identified
| Input | Line | Level | Cause | Task | What to change |
|---|---|---|---|---|---|
| E2 | R1 | build | main skill | T1 | Say a missing date is still to be agreed, never guess one |

## Accepted misses
None.

## Requirement changes
None.

## Verdict
Not ready. 9 of 10 lines met across 4 inputs. Build fixes the missing-date case.
