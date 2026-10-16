## Student

Run the build skill.

## AI

I've loaded the spec and the requirements.

- **Workflow:** Weekly Status Report. It uses a Skill mechanism, Augmented involvement, runs on Claude (code mode) and ships as standalone skills.
- **Counts:** 4 steps, 2 skills (S1 is the orchestrator `weekly-status-report`, S2 is `status-report-drafting`), 0 agents, 1 integration (HubSpot, read-only).
- **Approval:** the spec is approved (spec v3.0). The requirements file `framework/weekly-status-report/requirements.md` is loaded.

Phase 2 of 5 in this fix pass: deciding what to fix.

The latest `test-results.md` has a finished round marked **not ready**. The Improve review set that on 2026-07-10 so this fix pass could run. This is the first not-ready round since the Ready round on 2026-06-08, so we're well short of the "go back to Design" limit.

What I'm fixing, from the Issues identified table: on 2026-06-26 and 2026-07-03 you added a Risks section to the report by hand. The workflow's report is one section short of what you actually send. Four pieces change:

- **C2:** the report template, which is the layout your past reports share
- **C3:** the section order in `context/tone-guide.md`
- **S2:** the section list in `status-report-drafting`
- **Orchestrator:** the format block in `weekly-status-report`

Nothing else gets regenerated. The HubSpot connection, the inputs and both review gates stay as they are.

Phase 3 of 5: preparing the context, for C2 and C3 only.

| ID | Artifact | Outcome | Who does what | Read-back |
|---|---|---|---|---|
| C2 | Report template (`context/past-reports/`) | **Provide it** | You add the 2026-07-03 report you sent, with its Risks section, as `context/past-reports/2026-07-03.md` | pending |
| C3 | Tone guide | **Build it in** (update) | I change the section-order line from four sections to five | pending, waiting on C2 |

**I need one thing from you before I change anything:** the report you sent leadership on 2026-07-03, with the Risks section you added. Paste it here or save it to `context/past-reports/2026-07-03.md`. It isn't in the workspace yet, and I searched for it.

Your real report settles three things I'd otherwise have to guess:

1. **Where Risks sits.** My guess is between Blockers and Next Week, but your report decides it.
2. **What one risk line looks like.** For example, it might be risk, then owner, then mitigation, like the blocker lines, or something else.
3. **Where risks come from.** If they're tracker items, such as tasks or comments that mention a risk, the skills will pull them. If they're your own judgment, the draft needs to leave a marked spot for you to fill in at review. Otherwise it would make up risks, which breaks R2 (never invent).

Once I have the report, I'll show you a read-back of the section order and the risk-line format. Then I'll update the tone guide and the two skills, rebuild the two skill zips for you to re-save in Claude, and give you the reconciliation table.

One note for later: AC2 in the requirements still names four sections. Changing it to five is a requirements change, so I'll leave that file alone and flag it for Test to pick up.
