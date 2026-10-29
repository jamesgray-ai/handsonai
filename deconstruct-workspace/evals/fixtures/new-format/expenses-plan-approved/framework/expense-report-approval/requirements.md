# Expense Report Approval — Workflow Requirements

## Goal

For each submitted expense report, a one-paragraph decision note for the employee and payroll, ready within two business days.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Fewer audit findings on expense reimbursements |
| Desired Outcome | Employees get a clear decision with the reason, reimbursements go out faster, and reimbursement errors stop turning into audit findings |
| Measure | Analyst hours a week spent checking expense reports |
| Baseline | About 12 hours a week across 3 analysts · Estimated |
| Target | 4 analyst hours a week |
| Readable When | After a quarter |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Expense Report Approval |
| Description | Checks each submitted expense report against policy and routes it for approval; out comes an approved or returned report |
| Trigger | An employee submits an expense report |
| Owner | Marcus Webb (Finance Operations manager) |
| Lens | Organizational |
| Stakeholders | Finance analysts, the controller, payroll, employees who submit reports |

## Path

- Step 1 — Match each receipt to its line item · produces each line item with its matched receipt, and any mismatches · uses C2 · fixed (regulation)
- Step 2 — Check amounts against the policy limits · produces each line's limit check, within or over · uses C1 · flexible
- Step 3 — Route by report total · produces the approval route: analyst or controller · flexible · proposed by AI
- Step 4 — Controller approval over $5,000 · produces the controller's approve-or-return decision · fixed (regulation) · (controller)
- Step 5 — Write the decision note · produces a one-paragraph decision note with the reason · flexible · proposed by AI
- Step 6 — Analyst review · produces the reviewed decision, ready to post · flexible · (finance analyst)
- Step 7 — Post the decision to Concur · produces the decision recorded on the report in Concur · uses C2 · flexible · writes W1 · proposed by AI

### Decisions

- D1 (Step 3): if the report total is over $5,000 → the controller approves (Step 4); otherwise the analyst approves · settled by: a rule on a value · value read by AI

### Step 1 — Match each receipt to its line item

**Rule:** Every receipt matches a line item; a receipt with no line, or a line with no receipt, is a mismatch.
**Check or handoff:** The receipt check happens before the policy-limit check.

### Step 2 — Check amounts against the policy limits

**Rule:** The limits in the expense policy (C1).
**Expertise:** Check every hotel bill for a minibar line before approving it.

### Step 4 — Controller approval over $5,000

**Check or handoff:** Reports over $5,000 go to the controller before the decision note is written.

## Inputs

- I1 · the submitted expense report with its line items · from Concur (C2) · Status: available
- I2 · the scanned receipt for each line · from Concur (C2) · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Expense policy (Expense Policy v7) | Step 2 | Exists | Internal | Authored | Yes | `framework/expense-report-approval/context/C1-expense-policy.md` | Per-category limits, receipt rules, approval thresholds |
| C2 | Concur expense system | Step 1, Step 7 | Exists | Confidential | Authored | No | Concur; the reports and receipts are uploaded by employees | Staff expense reports, scanned receipts, approval history |

## Acceptance Criteria

1. **AC1 (must)** — Each receipt matches a line item, and every mismatch is named.
2. **AC2** — The note states the policy-limit check for each line.
3. **AC3** — The decision has a reason the employee can act on.
4. **AC4** — Fits in one paragraph.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Six-line travel report (real) | `framework/expense-report-approval/inputs/E1-report-4471.md` — Report #4471: 6 lines, hotel $612, meals $148, taxi $56, total $816 | Every receipt matched, every line within its limit, approved with a reason; tests AC1, AC2 | — |
| E2 | Foreign-currency receipt with a handwritten tip (real, hard) | `framework/expense-report-approval/inputs/E2-foreign-currency-tip.md` — a dinner receipt in euros with a tip written in by hand | The amount is read and converted correctly, the handwritten tip is flagged; tests AC1, D1 reading | — |
| E3 | Report over $5,000 (proposed) | `framework/expense-report-approval/inputs/E3-over-5000.md` — a conference trip totalling $6,240 | Routed to the controller before any note is written; tests D1, G2 | — |
| E4 | Hotel bill with a minibar line (proposed) | `framework/expense-report-approval/inputs/E4-minibar-line.md` — a hotel bill whose minibar charge is folded into the room line | The minibar line is found and returned; tests AC2, R2 | — |

## Rules & Constraints

| ID | Type | Rule |
|---|---|---|
| R1 | Must do | Check every receipt against its line item before the policy-limit check |
| R2 | Must never do | Approve a hotel bill without checking it for a minibar line |
| R3 | Scope | Expense reports submitted through Concur only |
| R4 | Fallback | When it hits a case it can't confidently handle, stop and ask the analyst (also recorded as G3) |

## Human Gates

Runs: with you

| ID | Where | What requires human input |
|---|---|---|
| G1 | Step 6 | A finance analyst reviews each decision before it posts to Concur |
| G2 | Step 4 | The controller approves any report over $5,000 |
| G3 | Any step | The analyst resolves any case the AI can't confidently handle |

## Security, Privacy & Safety

*Scope: writes to a live system (Concur); handles confidential staff data; governed by a regulation.*

### Boundaries
| Constraint | Source |
|---|---|
| Staff expense data stays in Concur and the bank's approved tools | Northbank expense policy |

### Access
| Constraint | Source |
|---|---|
| Decision notes are visible only to the employee, payroll and Finance Operations | Northbank expense policy |

### Traceability
| Constraint | Source |
|---|---|
| Every decision records who approved it and which policy limit applied | SOX controls |

### Prohibited actions
| Constraint | Source |
|---|---|
| Never send emails | Marcus Webb |

Governing regime: SOX controls, and Northbank's internal expense policy that implements them

### Writes

- W1 · Concur · posts the decision on the expense report · Step 7
