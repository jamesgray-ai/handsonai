# Old-format fixtures (state 1 source)

Moved here unchanged from `deconstruct-workspace/evals/fixtures/old-format/` (T15). Each folder is itself a whole workspace with a registry, copied as is into an eval run, so its README line lives here, not inside it. Frozen: never refresh them to the new format.

| Fixture | State, and the facts that put it there |
|---|---|
| `step-driven-norow/` | State 1, owner Deconstruct, no N-B44: 9.1.0 requirements with `## Steps Overview` and no frontmatter (`revision:`), the `Definition Type` row removed; nothing built |
| `step-driven-approved/` | State 1, owner Deconstruct (the earliest old file), no N-B44: the same requirements plus an approved 9.x `design-spec.md` (`spec_version: 3.0`) and its "Design spec" link; nothing built |
| `goal-driven/` | State 1, owner Deconstruct, no N-B44: Partner Fit Research in the 9.x goal-driven shell (`Definition Type: Goal-Driven`, `## Inputs`, no `## Path`, no `revision:`) |
| `outcome-driven/` | State 1, owner Deconstruct, no N-B44: the same with the legacy `Outcome-Driven` value and `## Outcome` heading |
| `no-markers/` | State 1, owner Deconstruct, no N-B44: no `Definition Type` row and `## Inputs` renamed, but still no `revision:` frontmatter |
| `goal-driven-approved/` | State 1, owner Deconstruct, no N-B44: `goal-driven/` plus an approved 9.x goal-driven `design-spec.md` |

The two `step-driven-*` folders were first built from `make_fixture.py R10` (whose 9.1.0 source, `upgrade-9x/`, T15 deleted); their derived views were recomposed with `registry-template/tools/` so they lint clean.
