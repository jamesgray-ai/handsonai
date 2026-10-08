# Weekly Status Report — Improvement Plan

**Review date:** 2026-07-10 (on schedule)

## Current performance summary

5 runs since deployment (run log). Zero failed runs; edits needed on 3 of 5 — one
reworded blocker, and a risk section added by hand on two separate Fridays, which the
log's own note flags as the second time. Door-to-door time, from the notes column, averaged 21 minutes across the five runs —
the Baseline the requirements left `Unknown` is now measured, and the under-25-minute
Target is met.

## Regression

Baseline: `test-results-2026-06-08.md` (2026-06-08) — the round that produced the Ready verdict.

No line flipped: 18 of 18 met at baseline, 18 of 18 met now.

| Scenario | Line | Baseline | Now | Evidence |
|---|---|---|---|---|
| *(no flipped lines)* | | | | |

Edits trend: per scenario unchanged from baseline (E1 none, E2 minor, E3 none); in the
run log, edits appear on 3 of 5 rows, two of them the same hand-added section — the
earliest drift signal, and the one this review acts on.

Environment like-for-like: same (Cowork, HubSpot connector live).

## Issues identified

| Scenario | Line | Building block | What to change |
|---|---|---|---|
| Run log 2026-06-26, 2026-07-03 | AC2 (scope) | C2, S2, orchestrator | The report the workflow produces is a section short of the report Maya actually sends: add a Risks section to the template (C2), to S2's section list, and to the orchestrator's format instruction |

## Recommendation

**Tune** — add a Risks section to the report template (C2), to S2's section list, and
to the orchestrator's format instruction; re-run E1, E2, and E3.

Nothing regressed, so this is not a repair. Maya has added the same section by hand two
weeks running, which is the workflow's scope growing past the four sections it was
built for — cheaper to teach the template the shape she keeps adding than to keep
adding it.

## Action items

1. Add a **Risks** section to the report template in `context/past-reports/` (C2)
2. Update S2's section list and the orchestrator's format instruction to produce it —
   Build's fix mode, C2, S2, and the orchestrator only; the regression round's `test-results.md` is now
   `readiness: not-ready` with the Issues identified table above, which is what fix
   mode reads
3. Update AC2 in the requirements to name the five sections in order, then re-run E1,
   E2, and E3 in Test
4. Workflow node: `# Artifacts` gains the Improvement plan link; `stale_after` reset to
   2026-08-14; the scope-growth insight recorded as a Note linked to the workflow
