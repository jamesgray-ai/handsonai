# The results file

Read when you write the round's file (Part 1) and at every later write to it. `test-results.md` in the workflow folder holds the current round. Only Test writes it; Build (fix mode), Design (change requests) and routing read it, so its frontmatter keys, headings and table columns are written exactly as below.

**Contents:** 1. The template · 2. Frontmatter values · 3. The sections · 4. Counts · 5. When each part is written

## 1. The template

```markdown
---
workflow: [workflow-slug]
round: [n]
plan_revision: [the plan revision this round tests]
date: [YYYY-MM-DD, the day the round opened]
environment: "[platform and account]; [where the runs happened and who ran them][; Claude Code: practice folder: [path]]"
round_status: in-progress
round_kind: [first | after-fix | after-change | regression]
readiness: [ready | not-ready | waiting-on-access; omitted until the verdict]
go_live: [pending | done; omitted until a Ready verdict]
change_requests: []
results:
  E1: { runs: 2, run1: { AC1: met, AC2: met, R1: met, G1: met, W1: met }, run2: { AC1: met, AC2: met, R1: met, G1: met, W1: met }, edits: none }
  E2: { runs: 1, run1: { AC1: met, AC2: not-met, R1: met }, edits: minor, carried: round 1 }
  E5: { runs: 1, run1: { KW: met, R3: met } }
  new: { runs: 1, run1: { AC1: met, AC2: met, R1: met, G1: met, W1: met }, edits: none }
---

# [Workflow name] — Test Results, round [n]

## Check list
| Line | Kind | Must-have |
|---|---|---|
| [ID]: [the line, in plain words] | output | yes |
| [ID]: [a rule tagged · (you)] | carried out by you, not graded | — |
| [ID]: [a safety must-have: a `Never` rule with no role tag, or a prohibited action] | path | yes (safety) |
| [ID]: [a D line] | path, graded against expect: | no |
| KW: the flag line | path | no |
| Policy check: [the line's value] | not graded: the confirm question | — |

## Coverage
| Line | Tested by | Presented by |
|---|---|---|
| [ID] | [E number, or new] | — |
| [ID of a safety must-have] | [E number] | [the E number of the input that presents its temptation] |
| [ID] | accepted as untested: [the leader's reason] | — |
| [ID] | untested: the cap of 8 was full | — |
| [ID] | not shown: [why no run can show where content went or who can see it] | — |

## Inputs
| Input | Came from | Ran by | Runs | Carried from | Saved as |
|---|---|---|---|---|---|
| E1 | Deconstruct | the AI | 2 | — | — |
| new | your real example ([a few words]) | you | 1 | — | [not saved / E[n]] |

## Report card

**[Input]**
| Line | Result | Evidence |
|---|---|---|
| [ID] | Met / Not met (run 1, run 2) | [a count, a phrase, a missing element] |

## Not run
| Input | Line | Reason |
|---|---|---|

## Environment
[Platform and account; where the runs happened; connections; for the AI's runs, that the start-up check passed and each run folder; memory notes; on Claude Code, the practice folder's path, created with its marker file.]

## Issues identified
| Input | Line | Level | Cause | Task | What to change |
|---|---|---|---|---|---|

## Accepted misses
| Line | Input | Your reason |
|---|---|---|

## Requirement changes
| Revision | Lines | What changed | Settled by |
|---|---|---|---|

## Verdict
[Ready / Not ready / Waiting on access]. [n] of [m] lines met across [k] inputs. [The policy reason, where there is one.] [What's next.] [For a later round: what changed since the comparison round.] [To check once it's live: each rule no run could show.]
```

An empty table keeps its header, or reads "None." under the heading.

## 2. Frontmatter values

The keys above and no others, plus `direct_edit: undo` only in the round Test opened when it found an edit the leader wants undone, and `old_platform_off: [set-aside folder name]` only in the round whose go-live had the leader switch off the version on the old platform (N-T56 answered; `going-live.md` section 2).
- **A file opened only to hold a direct-edit record** (SKILL.md entry check 2): the required keys (`workflow`, `round` the next number, `plan_revision`, `date`, `environment`, `round_status: in-progress`, and `round_kind` as `rounds.md` section 2 would set it) and `change_requests` with the one request (or `direct_edit: undo`); no `results`, and the sections' tables empty, until the round really opens (SKILL.md, state 8), when the rest is written in.
- **`round_status`:** `in-progress`, `complete`, or `abandoned` (a round set aside).
- **`results`:** per input, `{ runs: 1 | 2, run1: { [line]: met | not-met | not-run }, run2: {…}, edits: none | minor | major, carried: round [n] }`. Keys are E numbers, and `new` for the round's new input (if it's saved later, the Inputs section gives its E number). A practice input you write takes the next E number when it's written, as its key here, whether it's saved at once (Claude Code) or held in the Inputs section until the close (elsewhere); one held and then dropped keeps its row in Inputs, marked "not saved", and its number isn't reused. The flag input has no `edits`. With two runs, `run2` is there and the edits word is for the weaker run.
- **`change_requests`:** in the one shape, each with exactly `id` (`T[round].[n]`), `source` (`test` for a plan-level miss; `direct edit`, the edited text saved as `history/direct-edit-[id]-YYYY-MM-DD-HHMM.md` and `what` a one-line summary, in double quotes, naming that file; `leader at test` for a what-change at the real example), `what`, `why`, `tasks`, `after_round` (this round's number).
- **`environment`:** the platform and account, where the runs happened, who ran them, and on Claude Code the practice folder's path.
- **`readiness` and `go_live` on the return visit** after a policy wait: on the leader's yes, rewrite the last round's file in place, with no re-run and no new round: `readiness: ready`, `go_live: pending` (written as on any Ready round), and the Verdict reason "Waiting on the policy check ([value])" replaced with "Policy check confirmed on [date]". No other key changes, and no key is added, so routing reaches state 10 (`rounds.md` section 5).

## 3. The sections

In this order, and no others: Check list, Coverage, Inputs, Report card, Not run, Environment, Issues identified, Accepted misses, Requirement changes, Verdict.
- **Check list:** each line in plain words with its ID, kind (output or path) and must-have (a safety must-have marked "yes (safety)"); `D` lines as path lines graded against `expect:`; rules tagged `· (you)` listed as carried out by the leader; the policy row while `Policy check:` waits on the leader's confirmation.
- **Coverage:** each line, the input that tests it, and, for a safety must-have, the input that presents its temptation (Presented by; "—" for every other line); lines accepted as untested, with the reason; lines left untested because the cap of 8 was full; Boundaries and Access lines no run can show.
- **Check list and Coverage, the security lines:** every `P` line under Prohibited actions and Traceability, the per-run record regulated Autonomous work must keep, and every `P` line under Boundaries and Access, each a path line. A Boundaries or Access line no run can show is "not shown" in Coverage, never graded and never counted as met.
- **Inputs:** where each came from (Deconstruct, Design's risk input, written by Test, your real example, the flag input, a safety input, a flagged run), who ran it, runs, carried from, saved as. The text of an input Test wrote sits here until it's saved or dropped; the real example is named in a few words only, never its text.
- **Report card:** per input, output lines first, then path lines; the golden-example comparison where there is one; carried results marked "carried from round [n]".
- **Issues identified:** Level is `build`, `plan` or `requirement`; Cause from SKILL.md's list; Task is the plan task that *Meets* the line.
- **Verdict:** opens with Ready, Not ready or Waiting on access, then "[n] of [m] lines met across [k] inputs"; then the policy reason where there is one, as fixed text: "Waiting on the policy check ([value])", "The policy check came back no", or "Policy check confirmed on [date]" (which replaces the first on the return visit's yes); ends with each Boundaries or Access line Coverage records as not shown, as something to check once it's live (it never changes the verdict).

## 4. Counts

Worked out from `results`, never stored: the lines graded Met or Not met across every input, carried ones included; not-run lines are left out. With two runs, a line counts once and is met only when both runs met it. The Verdict's "[n] of [m] lines met" is this count.

## 5. When each part is written

| Part | Written |
|---|---|
| Frontmatter, Check list, Coverage, Inputs | Part 1, once the passing rule is confirmed; Coverage again after any requirement change and at the verdict |
| Report card, Not run | As each input is graded |
| Environment | Part 1 and Part 2 |
| Issues identified, Accepted misses, Verdict | Part 3 |
| Requirement changes | When a change is made |
| `round_status: complete`, `readiness`, `go_live` | At the round's close and at go-live; `readiness` and `go_live` also on the return visit's yes, with the Verdict's policy reason |

A finished round stays as `test-results.md` until the next round opens, then moves to `history/test-results-round-[n].md`. Nothing in `history/` is deleted.
