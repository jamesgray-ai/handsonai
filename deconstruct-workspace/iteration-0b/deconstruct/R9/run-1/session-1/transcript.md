## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't start a new interview: Weekly Status Report has already been through Deconstruct, and Design is finished too.

- **Step 2 (Deconstruct):** `framework/weekly-status-report/requirements.md` is complete. It has 4 steps, 3 context items (C1–C3), 3 acceptance criteria (AC1–AC3), 5 rules (R1–R5), 2 human gates (G1–G2), and 3 test scenarios (E1–E3). The input files for those three scenarios are saved in `inputs/`.
- **Step 3 (Design):** `framework/weekly-status-report/design-spec.md` is marked approved. It packages the workflow as a standalone Claude skill that you start yourself on Friday mornings.

**Next is Step 4, Build.** Running Deconstruct again would just ask you questions you've already answered.

One thing has changed since the requirements were written. They list the tone guide (C3) as "Needs Creation", but `context/tone-guide.md` now exists. Build will pick it up, or I can update the row to "Exists" first.

Separately, you don't have a registry yet, so this workflow's records live only in its folder. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill".

How do you want to continue?

1. **Go to Build:** say "run the build skill".
2. **Redo Deconstruct for Weekly Status Report:** for example, if the process has changed. I'd rename the current file to `requirements-2026-10-16.md` before writing a new one. The approved design spec was built from the old requirements, so Design would need to run again afterwards.
3. **Deconstruct a different workflow from your report:**

   **Process:** Program Delivery
   1. Program Risk Register: about two hours at month end
   2. Stakeholder Meeting Prep: 30–40 minutes per stakeholder meeting
   3. Onboarding Checklist Drafting: not sized yet

## Student

yes

## AI

"Yes" could mean a few things here, and they lead to different work. Which did you mean?

1. **Update the tone guide row (C3) to "Exists"** in the requirements, and then go to Build.
2. **Go straight to Build** and leave the requirements as they are.
3. **Redo Deconstruct for Weekly Status Report.** I'd keep the current file as a dated copy, and you'd need to run Design again afterwards.
4. **Deconstruct a different workflow:** Program Risk Register, Stakeholder Meeting Prep, or Onboarding Checklist Drafting.

If you're not sure, I'd go with 1.
