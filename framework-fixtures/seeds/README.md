# Seeds (pre-10.0 format)

Moved here unchanged from `deconstruct-workspace/evals/fixtures/new-format/` (T15) for the tasks that regenerate them in this release's format. Each folder is itself a whole workspace with a registry, copied as is into an eval run, so its README line lives here. Until regenerated, each reads as an earlier version: none of their `requirements.md` files has `revision:` frontmatter.

| Seed | For | State today, and the facts that put it there |
|---|---|---|
| `expenses-in-production/` | T25 (Improve's IM1 session 1, re-homed in Test) | State 1, owner Deconstruct, N-B44 first: requirements with no `revision:`; node `in-production`, a Run Card (`run-guide.md`), a run log and a baseline `test-results.md` |
| `expenses-regression-done/` | T25 (IM1 session 2) | State 1, owner Deconstruct, N-B44 first: as above, with a finished regression round in `test-results.md` and the baseline as `test-results-2026-09-12.md` |
| `sales-stale-tools/` | T31 (indexing-registry's IR1) | State 1, owner Deconstruct, for both workflows (no `revision:`); `client-follow-up` has results, so N-B44 first; `tools/` copied before `TOOLS_VERSION` existed, with a dashboard and `REGISTRY.md` those tools composed |
