# Framework fixtures

Hand-authored workspaces in the 10.0.0 file formats (rules 4.2 and 6), one per routing state and per edge case in rules 14's routing bullet. They are fixed inputs for `framework-state` (T13), `requirements-check` (T14), the shared eval harness (T18) and the registry tests (T34). Hand-written now; regenerated from real runs of the finished skills in T45 and T71.

## Layout

- `<group>/<fixture>/README.md`: one line naming the state and the facts that put it there.
- `<group>/<fixture>/with-registry/` and `<group>/<fixture>/no-registry/`: each a whole Claude Code workspace (`framework/<slug>/`, `.claude/skills/` once built, and `registry/` in the first). Point an eval at the variant folder (`dir:<path>`). The README sits above the workspaces so no eval run can read its answer.
- `expected.json`: the same table, machine-readable, for T13's tests. `self` marks a fixture that is itself one workspace.
- With a registry, the bundle's derived index views were composed with `registry-template/tools/compose-registry.js`; the root `REGISTRY.md` is left out until T33's compose shows state names instead of step counts.
- Workflows: `client-follow-up` (Client Follow-Up: drafts a follow-up email in Gmail Drafts after each client call) and, in multi-workflow fixtures, `weekly-pipeline-summary` (Weekly Pipeline Summary: reads HubSpot, writes nothing). Both run on Claude Code as one skill.
- With no registry, "live" is the build record's "Live since" line (or the newest set-aside record's), `big_change` sits in the requirements' frontmatter, and nothing records retiring or running work, so those fixtures' no-registry variants route differently, as the table says.

Expected values are the routing rule's (rules 4.2): the state number and its owner. For the `continue/` fixtures, the result of "continue my workflow" said in any step.

## States 0 to 11

| Fixture | With a registry | No registry |
|---|---|---|
| `states/s00-retired/` | 0 · no owner: retired line | 11 · Test |
| `states/s00-running-work/` | 0 · no owner: running-work message | 3 · Deconstruct |
| `states/s02-redo-pending/` | 2 · Deconstruct | 2 · Deconstruct |
| `states/s03-requirements-needed/` | 3 · Deconstruct | 3 · Deconstruct |
| `states/s04-plan-needed/` | 4 · Design | 4 · Design |
| `states/s05-plan-to-approve/` | 5 · Design | 5 · Design |
| `states/s06-build-needed/` | 6 · Build | 6 · Build |
| `states/s07-waiting-on-open-item/` | 7 · Design | 7 · Design |
| `states/s08-test-needed/` | 8 · Test | 8 · Test |
| `states/s09-waiting-on-access/` | 9 · Test | 9 · Test |
| `states/s10-ready-to-go-live/` | 10 · Test | 10 · Test |
| `states/s11-live/` | 11 · Test | 11 · Test |

## Edge cases (rules 14's routing bullet)

| Fixture | With a registry | No registry |
|---|---|---|
| `edge/e-platform-change/` | 4 · Design | 4 · Design |
| `edge/e-platform-change-stopped-after-plan/` | 4 · Design | 4 · Design |
| `edge/e-big-change-stopped-partway/` | 2 · Deconstruct | 2 · Deconstruct |
| `edge/e-direct-edit-undo/` | 6 · Build | 6 · Build |
| `edge/e-round-left-behind/` | 8 · Test | 8 · Test |
| `edge/e-build-saved-never-closed/` | 6 · Build | 6 · Build |
| `edge/e-three-not-ready-rounds/` | 6 · Build | 6 · Build |
| `edge/e-requirements-revision-above-plan/` | 4 · Design | 4 · Design |
| `edge/e-plan-unaffected-revision/` | 10 · Test | 10 · Test |
| `edge/e-unlogged-change-request/` | 4 · Design | 4 · Design |
| `edge/e-schedule-only-request/` | 8 · Test | 8 · Test |
| `edge/e-declined-only-miss/` | 8 · Test | 8 · Test |
| `edge/e-known-miss-after-first-close/` | 8 · Test | 8 · Test |
| `edge/e-go-live-interrupted/` | 10 · Test | 10 · Test |
| `edge/e-change-after-ready-not-live/` | 8 · Test | 8 · Test |
| `edge/e-retired-brought-back/` | 6 · Build | 6 · Build |
| `edge/e-interrupted-redo-with-progress/` | 3 · Deconstruct | 3 · Deconstruct |
| `edge/e-interrupted-redo-no-progress/` | 3 · Deconstruct | 3 · Deconstruct |
| `edge/e-run-guide-not-a-sign/` | 11 · Test | 11 · Test |

## State 1: earlier versions

| Fixture | With a registry | No registry |
|---|---|---|
| `earlier-version/v1-requirements-no-revision/` | 1 · Deconstruct · no N-B44 | 1 · Deconstruct · no N-B44 |
| `earlier-version/v1-design-spec/` | 1 · Design · no N-B44 | 1 · Design · no N-B44 |
| `earlier-version/v1-plan-no-requirements-revision/` | 1 · Design · no N-B44 | 1 · Design · no N-B44 |
| `earlier-version/v1-results-no-record/` | 1 · Build · N-B44 | 1 · Build · N-B44 |
| `earlier-version/v1-results-no-round/` | 1 · Test · N-B44 | 1 · Test · N-B44 |
| `earlier-version/v1-run-guide-built/` | 1 · Deconstruct · N-B44 | 1 · Deconstruct · N-B44 |
| `earlier-version/v1-progress-no-track/` | 3 · Deconstruct | 3 · Deconstruct |
| `earlier-version/old-format/*` (six, moved from `deconstruct-workspace/evals/fixtures/old-format/`; each folder is one workspace with a registry; see its README) | 1 · Deconstruct · no N-B44 | — |

## "Continue my workflow"

| Fixture | With a registry | No registry |
|---|---|---|
| `continue/c-analyze-unfinished-alone/` | Analyze resumes | Analyze resumes |
| `continue/c-analyze-unfinished-beside-workflow/` | N-F9 lists client-follow-up and the unfinished Analyze session | N-F9 lists client-follow-up and the unfinished Analyze session |
| `continue/c-only-backlog/` | Deconstruct's start phrase | Deconstruct's start phrase |
| `continue/c-nothing/` | nothing to continue yet; Analyze's start phrase | nothing to continue yet; Analyze's start phrase |
| `continue/c-retired-beside-in-progress/` | picks weekly-pipeline-summary (state 6, Build) | picks weekly-pipeline-summary (state 6, Build) |
| `continue/c-only-retired/` | nothing to continue yet; Analyze's start phrase | picks client-follow-up (state 11, Test), N-T19 |
| `continue/c-several-in-progress/` | N-F9 lists client-follow-up and weekly-pipeline-summary | N-F9 lists client-follow-up and weekly-pipeline-summary |
| `continue/c-one-live/` | picks client-follow-up (state 11, Test), N-T19 | picks client-follow-up (state 11, Test), N-T19 |
| `continue/c-live-changing-beside-live/` | picks client-follow-up (state 6, Build) | picks client-follow-up (state 6, Build) |
| `continue/c-live-changing-beside-not-live/` | N-F9 lists client-follow-up and weekly-pipeline-summary | N-F9 lists client-follow-up and weekly-pipeline-summary |

## Seeds

Moved unchanged from `deconstruct-workspace/evals/fixtures/new-format/` for regeneration; pre-10.0 format, so each reads as state 1 today. See `seeds/README.md`.

| Seed | For | Today |
|---|---|---|
| `seeds/expenses-in-production/` | T25 | 1 · Deconstruct · N-B44 |
| `seeds/expenses-regression-done/` | T25 | 1 · Deconstruct · N-B44 |
| `seeds/sales-stale-tools/` | T31 | 1 · Deconstruct (both workflows) |

## Notes

- Four registry fixtures don't lint clean on purpose: `edge/e-big-change-stopped-partway` and `edge/e-platform-change-stopped-after-plan` keep a link to a file the interrupted set-aside already moved (an error), `edge/e-build-saved-never-closed` has a skill no node links yet (Build links it at its close; a warning), and `earlier-version/v1-run-guide-built` is past its `stale_after` (a warning).
- Replays of real calls never land here; `.gitignore` keeps any `post-call-*/` folder out.
