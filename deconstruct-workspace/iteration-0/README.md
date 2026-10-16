# Iteration 0: baseline against today's Deconstruct (before the rewrite)

Run 2026-10-15 on branch `deconstruct-build1` at `16b67cdbb` (plugin 9.1.0, unchanged skills), with `evals/run_eval.py` and graded by `evals/grade_eval.py`. Each folder holds the eval, the transcripts and the grading; the workspaces are not kept.

| Eval | Result | Notes |
|---|---|---|
| I1 sales pre-call brief | 2 of 23 | Capped at 12 AI turns (a baseline only needs to show the failures). Today's opening, "Shall we go step-driven?", several questions per message, no law question in Part 2, no recipe. Most file checks not reached. |
| R5 renamed resume (walk e) | 1 of 4 | Build ignores the progress file and starts a fix pass on another workflow. Deconstruct gives the full opening and the backlog choice, no resume line. Design already points to the unfinished Deconstruct (it reads the folder), so session 2 passes today. |
| R9 no registry, built (walk i) | 1 of 6 | No R9-3 question; the AI offers its own three-option menus and never uses the R10-2 message for any `test-results.md` state. |

Expected: the rewrite (Task 3) turns I1, R5 session 3 and R9 green; R5 session 1 needs Task 8 (Build's resume scan).
