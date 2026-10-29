# Hand-written eval fixtures

Each folder here is a whole student workspace, copied as is into an eval run with `"fixture": "dir:<path>"` (the path is relative to the evals.json that names it). They are fixed inputs: Design, Build, Test, Run, Improve and indexing-registry evals read them, so they don't change when a Deconstruct round changes.

## New format (`new-format/`)

`requirements.md` follows section 4a of `deconstruct-redesign.md`: the 12 sections in order, no YAML, step lines, D/I/W/R/G labels, the `Runs:` line, and `Governing regime:` before `### Writes`.

| Folder | Shape | Used by |
|---|---|---|
| `sales/` | Sales Pre-Call Brief (I1's facts); node `under-development`, Requirements only. I2 is `Status: not available yet` | D1a, D1b |
| `expenses/` | Expense Report Approval (I2's facts, regulated: two `fixed (regulation)` steps, D1 `· value read by AI`, W1, `Runs: with you`) | base for the variants |
| `expenses-regime-not-sure/` | `expenses/` with `Governing regime: Not sure — to check` | D2b |
| `expenses-without-you/` | `Runs: without you`, the analyst gate and step removed, fallback "do its best and flag it"; the controller gate stays | D2a |
| `sales-plan-draft/` | `sales/` plus `design-plan.md` at `approved: false`; no node link | B1-unapproved, IR1 |
| `sales-plan-approved/` | `approved: true`, node link "Design plan", `autonomy`, `execution_mode` | B1-approved |
| `expenses-plan-approved/` | `expenses/` plus an approved `design-plan.md` | B2 |
| `expenses-built/` | plus the built skill at `.claude/skills/expense-report-approval/SKILL.md` (where Build installs on Claude Code) and the node's `# Skills` link | T1 |
| `sales-tested/` | approved plan, built skill, `test-results.md` at `readiness: ready` | RN1 |

**Refresh after Task 7 and Task 8.** The `design-plan.md` files are written by hand from the spec's description of the Design Plan (`plan_version: 4.0`, `autonomy:`, `decomposition:`, a coverage table). Task 7 Step 5 refreshes every one of them to match `plan-template.md` once it exists, and the built skills (`.claude/skills/*/SKILL.md`) are refreshed after Task 8 to match what Build produces.

## Moved (T15)

`expenses-in-production/`, `expenses-regression-done/` and `sales-stale-tools/` moved to `framework-fixtures/seeds/`, and `../old-format/` to `framework-fixtures/earlier-version/old-format/`, where their README lines now live. `../upgrade-9x/` and `../upgrade-9x-generated/` were dropped.

