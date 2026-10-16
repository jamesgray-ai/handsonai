## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't run Deconstruct again. Weekly Status Report finished that step a while ago, and running it again would just redo work you've already approved.

**Where the workflow stands**

- **Step 2, Deconstruct, is done.** `framework/weekly-status-report/requirements.md` covers 4 steps, 3 context items, 3 acceptance criteria and 3 saved test inputs.
- **Step 3, Design, is done.** `design-spec.md` is approved: a skill-based workflow with two skills and a read-only HubSpot connection.
- **Step 5, Test, is done.** The latest round (2026-07-10) met all 39 of its 39 lines.
- **Step 7, Improve, sent it back.** Your run logs from 2026-06-26 and 2026-07-03 show the report it produces is missing the **Risks** section you add before sending. Improve marked it *not ready* so Build can fix this.

**Next is Build, to fix the gap.** Say "run the build skill". It will add the Risks section to the report template, the tone guide, the drafting skill and the main skill.

**One thing Build won't fix:** the requirements still list four sections. AC2 says "Wins, In Progress, Blockers, Next Week" and Step 2's output says the same, while all three past reports in `context/past-reports/` only have those four headings. Once Risks is added, the next test would check against the old list. I'd update the requirements before Build runs, and keep the current file as `requirements-2026-10-15.md`. I need three answers from you to do that:
1. Where does Risks go in the order? After Blockers seems likely.
2. Should "under 400 words" stay the limit now that there's a fifth section?
3. Is there a report you've sent with a Risks section in it? That would replace the 2026-05-22 report as the example the criteria are checked against.

You don't have a registry yet, so this workflow's records live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill". The other three candidates in your opportunity report (Program Risk Register, Stakeholder Meeting Prep, Onboarding Checklist Drafting) haven't been started. Say "deconstruct" plus one of their names when you want to map one.

Shall I make the requirements update?
