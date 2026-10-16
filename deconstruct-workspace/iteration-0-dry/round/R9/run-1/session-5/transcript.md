## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I checked the workspace before starting. Weekly Status Report has already been through Step 2, so I've stopped to ask before re-running it.

**Where the workflow is now**
- **Step 2 (Deconstruct):** finished. `framework/weekly-status-report/requirements.md` has 4 steps, 3 context items, 3 acceptance criteria and 3 test inputs.
- **Step 3 (Design):** finished. `design-spec.md` exists.
- **Step 5 (Test):** a regression round on 2026-07-10 passed 39 of 39 checks. Improve still marked it **Not ready** because of one open issue: the report Maya actually sends has a **Risks** section that the workflow doesn't produce.

That open issue is a gap in the requirements themselves. AC2, R4, the template and past reports (C2), and the tone guide (C3) all say "four sections: Wins, In Progress, Blockers, Next Week."

**Your options**
1. **Update the requirements for the Risks section (my recommendation).** This takes about 10 minutes. I'd ask where Risks goes in the order, what belongs in it (and how it differs from Blockers), and what to write in a week with no risks. Then I'd update AC2, R4, C2/C3 and add a test input for a week with risks. I'll save the current file as `requirements-2026-10-16.md` first. Then **Build** can make the fix.
2. **Skip the requirements and fix the build.** Improve has already routed this to Build's fix mode, and its Issues table names what to change. The downside is that the requirements would still say four sections, so Test would grade against the old format.
3. **Redo Step 2 from scratch.** This is the full 45–60 minute session, and the current file gets saved with a date. It's only worth it if the workflow has changed a lot since June.

**Also worth knowing**
- **No registry yet:** these requirements live in the workflow's folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill."
- **Missing test outputs:** `test-results.md` says three test outputs were saved under `framework/weekly-status-report/test-runs/`, but that folder doesn't exist. The next Test round should regenerate them.
- **Other candidates:** your opportunity report has three more: Program Risk Register, Stakeholder Meeting Prep and Onboarding Checklist Drafting. If you meant to start a new workflow, I can map one of those.

Which would you like: 1, 2, 3, or a different workflow?
