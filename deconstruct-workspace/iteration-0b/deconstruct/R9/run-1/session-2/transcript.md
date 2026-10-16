## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I haven't started the interview, because **Weekly Status Report has already been through Deconstruct and Design.** Running Deconstruct again would redo finished work, so I've left everything as it is.

Here's what's in `framework/weekly-status-report/`:

- **`requirements.md` (Step 2):** complete. It covers 4 steps, 3 context items (C1–C3), acceptance criteria AC1–AC3, rules R1–R5, human gates G1 and G2, and test scenarios E1–E3.
- **`inputs/`:** the three scenario input files are all there.
- **`design-spec.md` (Step 3):** approved (`approved: true`). It sets up two skills: `weekly-status-report`, which runs the whole thing, and `status-report-drafting`, which writes the report. It connects to HubSpot read-only.
- **Nothing for Build yet:** there's no `skills/` folder and no skill packages.

**You've completed through Step 3 (Design). Next is Step 4 (Build).**

There's one small inconsistency. The requirements and the design spec both list the tone guide (C3) as `Needs Creation`, but `context/tone-guide.md` already exists and covers the voice rules. Build can use it as it is, so that's one less thing to create.

There's also no AI Registry in this workspace yet, so this workflow isn't recorded on a dashboard. If you want one, say "run the scaffolding-registry skill."

How do you want to go on?

1. **Continue to Build:** say "run the build skill" (recommended).
2. **Redo Deconstruct anyway:** for example, if the process has changed since June. I'd keep the current file as `requirements-2026-10-16.md` before writing a new one. The approved design spec was built from the old requirements, so it would need another pass through Design afterwards.
3. **Deconstruct a different workflow** from your opportunity report: Program Risk Register, Stakeholder Meeting Prep, or Onboarding Checklist Drafting.

## Student

no

## AI

Understood, I won't do any of those. All your files are as they were.

When you want to pick it back up, say "continue my workflow" and I'll start from Step 4 (Build).
