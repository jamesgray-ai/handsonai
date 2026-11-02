---
name: expense-report-approval
description: This skill should be used when Northbank's Finance Operations team wants a submitted expense report checked against the expense policy and routed for approval. It matches every receipt to its line, checks policy limits, routes by the report total, writes the decision note, pauses for the analyst's review and posts the decision to Concur.
disable-model-invocation: true
---

# Expense Report Approval

Built from the approved Design Plan (`framework/expense-report-approval/design-plan.md`) and the Workflow Requirements (`framework/expense-report-approval/requirements.md`). Follow the steps in order. Steps 1 and 4 are required by regulation (SOX): follow them exactly, every time.

## Test runs

If the request says "test run", work only from the pasted report and receipts instead of Concur, post nothing, save the decision note under `framework/expense-report-approval/test-runs/` as `E<n>-YYYY-MM-DD.md`, and log nothing. The person replying plays the analyst and, when needed, the controller.

## Steps

1. **Match each receipt to its line item** (I1, I2). Every receipt matches a line; a receipt with no line, or a line with no receipt, is a mismatch. Do this before the policy-limit check (R1). Read each amount from the receipt itself and show the amount you read, converting foreign currency at the rate on the receipt date.
2. **Check amounts against the policy limits** in `framework/expense-report-approval/context/C1-expense-policy.md`. Check every hotel bill for a minibar line (R2).
3. **Route by report total (D1).** Over $5,000 → Step 4; otherwise the analyst approves at Step 6.
4. **Controller approval (G2).** For a report over $5,000, ask the controller to approve or return it, and wait, before writing the note.
5. **Write the decision note**: one paragraph, approved or returned, with a reason the employee can act on and the policy-limit check for each line.
6. **Analyst review (G1).** Show the decision and the note; wait for the analyst to approve or change it.
7. **Post the decision to Concur (W1)** only after G1. Never send emails.

When a case can't be handled confidently, stop and ask the analyst (G3).

## What I did

End every run with a **What I did** list: the steps in order, each amount read from a receipt, the route taken at D1, each gate where you paused and what was decided, what was posted (or, in a test run, where the note was saved).
