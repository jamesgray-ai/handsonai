# Hand-written eval fixtures

Each folder here (and in `../old-format/`) is a whole student workspace, copied as is into an eval run with `"fixture": "dir:<path>"` (the path is relative to the evals.json that names it). They are fixed inputs: Design, Build, Test, Run, Improve and indexing-registry evals read them, so they don't change when a Deconstruct round changes.

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
| `expenses-in-production/` | built, baseline `test-results.md` (`readiness: ready`, a `D1 reading` key), Run Card, run log, `in-production` | IM1 session 1 |
| `expenses-regression-done/` | as above, with the baseline dated `test-results-2026-09-12.md` and a finished regression round in `test-results.md` (`D1 reading` not met on E2) | IM1 session 2 |
| `sales-stale-tools/` | `sales-plan-draft/` plus a `tools/` copied from `registry-template/tools/` before `TOOLS_VERSION` existed (each file carries a `stale-tools-9.1.0` or `stale-template-9.1.0` marker), a dashboard and `REGISTRY.md` composed by those tools, and a second workflow whose node links both "Design spec" and "Design plan" | IR1 |

**Refresh after Task 7 and Task 8.** The `design-plan.md` files are written by hand from the spec's description of the Design Plan (`plan_version: 4.0`, `autonomy:`, `decomposition:`, a coverage table). Task 7 Step 5 refreshes every one of them to match `plan-template.md` once it exists, and the built skills (`.claude/skills/*/SKILL.md`) are refreshed after Task 8 to match what Build produces.

## Old format (`old-format/`)

| Folder | Shape | Used by |
|---|---|---|
| `step-driven-norow/` | the frozen 9.1.0 worked example's requirements (`upgrade-9x/`, fixture `R10`) with the `Definition Type` row removed (a `## Steps Overview` file with no row) | D3-step-norow |
| `step-driven-approved/` | fixture `R10` plus the frozen approved `design-spec.md` (`spec_version: 3.0`) and its "Design spec" link; nothing built | B3 |
| `goal-driven/` | Partner Fit Research, written in the 9.x goal-driven shell (today's Deconstruct template: `Definition Type: Goal-Driven`, `## Inputs`, no `## Path`); node `definition_type: goal-driven` | D3-goal |
| `outcome-driven/` | the same with the legacy `Outcome-Driven` value and `## Outcome` heading | D3-goal-outcome |
| `no-markers/` | the same with no `Definition Type` row and `## Inputs` renamed, so none of the old markers is present | D3-nomarkers |
| `goal-driven-approved/` | `goal-driven/` plus an approved 9.x goal-driven `design-spec.md` (Capability Domain Mapping) | B4 |

The two `step-driven-*` folders were built from `make_fixture.py R10`, then their derived views (`registry/index.md`, `REGISTRY.md`) were recomposed with `registry-template/tools/` so they lint clean. Old-format folders are frozen: never refresh them to the new format.
