# Expense Report Approval — Run Card

## Your first real run
On 2026-09-15 the workflow checked Report #4588 and the analyst approved the note before it posted to Concur. Expect the same pause at every run.

## How to start it
Open a new Claude Code session in this folder and type `/expense-report-approval`, then paste the report number.

## What to have ready
The report number. The Concur connector authorized in the account that runs it. The expense policy at `framework/expense-report-approval/context/C1-expense-policy.md`. The `expense-report-approval` skill in `.claude/skills/`.

## What to check before you act on the output
The workflow pauses for the analyst before anything posts (G1), and for the controller on any report over $5,000 (G2). Must: every receipt matches a line, and every mismatch is named.

## Log the run
One line per run in `framework/expense-report-approval/runs.md`: date, input, result, edits needed, notes.

## Your first review
2026-10-15. Say: "Run the improve skill on Expense Report Approval." Bring nothing; the registry node, test results and run log carry it.
