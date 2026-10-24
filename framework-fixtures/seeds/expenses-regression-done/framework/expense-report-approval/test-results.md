---
workflow: expense-report-approval
design_plan: framework/expense-report-approval/design-plan.md
requirements: framework/expense-report-approval/requirements.md
date: 2026-10-15
environment: "Claude Code, inputs pasted; Concur write simulated"
round_status: complete
readiness: not-ready
criteria_total: 68
criteria_met: 67
results:
  E1: { AC1: met, AC2: met, AC3: met, AC4: met, R1: met, R2: met, R3: met, R4: met, G1: met, G2: met, G3: met, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 5 output": met, "Step 7 output": met, "D1 reading": met, edits: none }
  E2: { AC1: met, AC2: met, AC3: met, AC4: met, R1: met, R2: met, R3: met, R4: met, G1: met, G2: met, G3: met, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 5 output": met, "Step 7 output": met, "D1 reading": not-met, edits: minor }
  E3: { AC1: met, AC2: met, AC3: met, AC4: met, R1: met, R2: met, R3: met, R4: met, G1: met, G2: met, G3: met, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 5 output": met, "Step 7 output": met, "D1 reading": met, edits: none }
  E4: { AC1: met, AC2: met, AC3: met, AC4: met, R1: met, R2: met, R3: met, R4: met, G1: met, G2: met, G3: met, "Step 1 output": met, "Step 2 output": met, "Step 3 output": met, "Step 5 output": met, "Step 7 output": met, "D1 reading": met, edits: none }
---

# Expense Report Approval — Test Results

## Check list

- AC1 (must) — each receipt matches a line item; every mismatch named
- AC2 — the policy-limit check stated for each line
- AC3 — a reason the employee can act on
- AC4 — one paragraph
- R1 — receipts checked before policy limits
- R2 — every hotel bill checked for a minibar line
- R3 — Concur reports only
- R4 — unsure: stop and ask the analyst (G3)
- G1 — the analyst reviews before posting
- G2 — the controller approves reports over $5,000
- G3 — the analyst resolves cases the AI can't handle
- Step 1 output — each line with its matched receipt, and any mismatches
- Step 2 output — each line's limit check
- Step 3 output — the approval route
- Step 5 output — the one-paragraph decision note
- Step 7 output — the decision recorded in Concur
- D1 reading — the report total and each amount read from the receipts

## Scenarios to run

- E1 — `framework/expense-report-approval/inputs/E1-report-4471.md` — Report #4471; tests AC1, AC2
- E2 — `framework/expense-report-approval/inputs/E2-foreign-currency-tip.md` — euro receipt with a handwritten tip (hard); tests AC1, D1 reading
- E3 — `framework/expense-report-approval/inputs/E3-over-5000.md` — over $5,000; tests D1, G2
- E4 — `framework/expense-report-approval/inputs/E4-minibar-line.md` — minibar line; tests AC2, R2

## Report card

Tables kept in each scenario's chat; results above.

## Golden example deltas

None (no Golden Examples).

## Not run

None.

## Environment

Inputs pasted; the Concur post was printed, not sent.

## Issues identified

| Line | Scenario | Building block | Issue |
|---|---|---|---|
| D1 reading | E2 | S1 (Step 1 instruction) | Read the handwritten total €90 as the receipt amount instead of €78 plus a tip to flag |

## Accepted misses

None.

## Verdict

Not ready — 67 of 68 lines met across 4 scenarios; D1 reading not met on E2.

## Test records created

None kept; the test notes were removed after the round.
