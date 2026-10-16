## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't start the interview, because Weekly Status Report has already been through Deconstruct. In fact it's through Step 6 (Run). Here's what `framework/weekly-status-report/` already holds:

- **`requirements.md`**: the Step 2 output, with 4 steps, the value case, acceptance criteria and rules.
- **`inputs/`**: the three test inputs (a typical week, a week with lots of blockers, and a quiet week).
- **`design-spec.md`**: Step 3, approved. It builds the workflow as a skill that drafts the report and pauses for your review.
- **`run-guide.md`**: the Step 6 run instructions. The first real run was on 2026-06-12.

So the next step is **Step 7 (Improve)**. The run guide set the first review for **2026-07-10**, and that date passed three months ago.

Two problems turned up while I was checking:

- **The run log is missing.** The run guide says every run adds a row to `framework/weekly-status-report/runs.md`, but that file doesn't exist. That leaves no record of past runs or of your timings. The Baseline is still "Unknown", and that log was meant to fill it in.
- **You don't have a registry.** There's no `registry/` folder, so this workflow has no registry entry and progress isn't tracked there.

How do you want to go on?

1. **Run the Improve step (recommended).** Say *"run the improve skill on weekly status report."* The missing run log will be the first thing to sort out there.
2. **Redo the requirements anyway.** This is the right choice if the work itself has changed, for example a new data source or a different report format. I'd keep the current file as `requirements-2026-10-16.md` before writing anything. The approved design and what you built would then be out of date, so Design and Build would need another pass.
3. **Map a different workflow.** Your opportunity report has three that haven't been started: Program Risk Register, Stakeholder Meeting Prep and Onboarding Checklist Drafting.

You can also say *"run the scaffolding-registry skill"* at any point to set up the registry.
