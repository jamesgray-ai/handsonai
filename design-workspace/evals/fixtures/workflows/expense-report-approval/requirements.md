---
revision: 1
track: full
revisions: []
---

# Expense Report Approval — Workflow Requirements

## Goal
For each submitted expense report, an approve-or-return recommendation for the controller, ready before the weekly close.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Close the books on time every week |
| Desired Outcome | Every expense report is checked against the expense policy before the controller signs it off |
| Measure | Minutes per expense report |
| Baseline | 15 minutes per report · Estimated |
| Target | 4 minutes per report, including the controller's review |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Expense Report Approval |
| Description | Checks each submitted expense report against the expense policy and recommends approve or return, for the controller to sign off. |
| Trigger | An employee submits an expense report |
| Owner | Finance operations lead |
| Lens | Organizational |
| Stakeholders | Employees who submit reports; the controller; finance operations |

## Path

Method preference: same way every time

- Step 1 — Check every receipt is attached · produces a list of missing receipts · uses C1 · fixed (regulation)
- Step 2 — Check each line against the policy · produces a list of out-of-policy lines · uses C1 · flexible
- Step 3 — Recommend approve or return · produces an approve-or-return recommendation · fixed (policy)
- Step 4 — Controller signs off · produces a signed-off report · fixed (regulation) · (controller)
- Step 5 — Post the approved report · produces a posted expense report in NetSuite · fixed (policy) · writes W1

### Decisions

- D1 (Step 3): When any receipt is missing or any line is out of policy, it recommends return · settled by: a rule on a value · value read by AI

### Step 2 — Check each line against the policy
**Rule:** Use the policy's limits for meals, travel and lodging.
**Expertise:** A hotel's resort fee counts as lodging, not as a separate line.

## Inputs

- I1 · the submitted expense report with its receipts · from the expense inbox · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Expense policy | Step 1, Step 2 | Exists | Internal | Authored | Yes | `context/C1-expense-policy.md` | Limits per category and the receipt rules |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The recommendation lists every missing receipt.
2. **AC2 (must)** — The recommendation lists every out-of-policy line with the limit it breaks.
3. **AC3** — The recommendation says approve or return in its first line.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Clean trip report (real) | `inputs/E1-clean-trip-report.md` — a three-day trip with every receipt attached | Approve, with nothing listed | — |
| E2 | Missing hotel receipt (proposed, hard) | `inputs/E2-missing-hotel-receipt.md` — a report missing one receipt, with one dinner over the limit | Return, naming the receipt and the dinner | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never recommends approving a report with a missing receipt. |
| R2 | Always | It always names the policy limit for each out-of-policy line. |
| R3 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 4 | When the recommendation is ready, it stops until the controller signs it off. · (controller) |

## Security, Privacy & Safety

*Scope: writes to a live system; handles data you'd be uncomfortable seeing outside the company*

### Boundaries
| ID | Constraint | Source |
|---|---|---|
| P1 | Expense reports and receipts stay inside the finance team's systems. | Finance policy FIN-07 |

### Access
| ID | Constraint | Source |
|---|---|---|
| P2 | Only finance operations and the controller see the recommendation. | Finance policy FIN-07 |

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P3 | Each posted report records who signed it off and when. | SOX control 4.2 |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P4 | It never posts a report the controller hasn't signed off, whoever asks. | SOX control 4.2 |

Governing regime: Sarbanes-Oxley (SOX) internal controls

### Writes
- W1 · NetSuite · post the approved expense report · Step 5
