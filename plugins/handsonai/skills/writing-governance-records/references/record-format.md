# The Governance Record File

One Markdown file per workflow: `framework/[slug]/governance-record.md`, or `governance-records/[slug].md` in the working folder when the workflow has no framework folder. A later update and the company's policy reviews read it back, so keep this shape exactly.

## Shape

1. **Frontmatter:** `title` (`[Workflow name] — Governance Record`), `workflow` (the slug), `written` (`YYYY-MM-DD`), `in_place`, `partly` and `gaps` (counts, adding up to 8).
2. **One intro line:** what the workflow does (its registry description, or the user's words) and whether it's live.
3. **`## Practices`:** one table with the header exactly `| # | Practice | Status | Evidence | Follow-up |`.
   - Eight rows, in order: 1 Name and description, 2 Ownership, 3 Process, 4 Building blocks, 5 Evaluations, 6 SOP, 7 Operations, 8 Change management.
   - `Status` is exactly `In place`, `Partly` or `Gap`.
   - `Evidence` names where it came from in plain words: "registry entry", "build record", "test results, 2026-11-05", "you said".
   - `Follow-up` is the action that closes the gap, or `—` when the practice is in place. Two actions are separated by `; `. A gap the framework follow-up will close says `Finish the framework steps`.
4. **`## Follow-up actions`:** a numbered list, one action per line: first the one framework follow-up when there's unfinished framework work ("Finish the framework steps: in a new chat, say 'continue my workflow. My files are in [workflow folder].'"), then every other `Follow-up` from the table in practice order, one action per line, each listed once. Any start phrase in a follow-up carries the location.
5. **`## Policy`:** only when the working folder has `policies/ai-governance-policy.md`: one line per policy rule this workflow doesn't meet yet, as "[rule ID]: [the rule], [why not yet]", or the line "Meets every rule in the policy." Leave the section out when there's no policy.

## Sample

```
---
title: Weekly Status Report — Governance Record
workflow: weekly-status-report
written: 2026-11-05
in_place: 5
partly: 1
gaps: 2
---

Drafts the weekly status report from the week's notes for review before it's sent. Live since 2026-06-08.

## Practices

| # | Practice | Status | Evidence | Follow-up |
|---|---|---|---|---|
| 1 | Name and description | In place | registry entry | — |
| 2 | Ownership | In place | registry entry: Client Services | — |
| 3 | Process | In place | registry entry: Client Reporting | — |
| 4 | Building blocks | In place | build record | — |
| 5 | Evaluations | Partly | test results, 2026-06-08, the workflow end to end; no tests of the skill itself | Add tests for the report-drafting skill |
| 6 | SOP | Gap | no SOP found | Write the SOP: in a new chat, say "write an SOP for weekly status report. My files are in framework/weekly-status-report." |
| 7 | Operations | In place | registry entry and build record: Fridays, you start it | — |
| 8 | Change management | Gap | you said: nobody reviews a change | Name a second person to review changes before release |

## Follow-up actions

1. Add tests for the report-drafting skill
2. Write the SOP: in a new chat, say "write an SOP for weekly status report. My files are in framework/weekly-status-report."
3. Name a second person to review changes before release
```

## Before saving

- The table header matches the exact string above, with eight rows in order.
- Every `Status` is `In place`, `Partly` or `Gap`; the frontmatter counts match the table and add up to 8.
- Every `Partly` or `Gap` row has a `Follow-up`, and every follow-up is in the numbered list.
- Nothing is `In place` without evidence from a file or the user.
- Dates are `YYYY-MM-DD`.
