## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I haven't started the interview. Weekly Status Report already finished Step 2, and running it again from scratch would overwrite work you've already done and tested.

**Where the workflow stands now:**
- **Step 2 (Deconstruct):** done. The requirements file `framework/weekly-status-report/requirements.md` has 4 steps, 3 context items, 3 acceptance criteria, 3 test inputs and 2 human gates.
- **Step 3 (Design):** done. The design spec was approved (a standalone skill, with Maya in the loop).
- **Step 5 (Test):** done. All 39 checks were met on 2026-07-10.
- **Step 7 (Improve):** this sent it back. It's marked **not ready** because the report is a section short of what Maya actually sends: it has no **Risks** section. Improve gave the fix to **Build's fix mode** (Step 4), not to Deconstruct.

**One reason to touch the requirements anyway:** they spell out the sections. **AC2** says "uses the *four* sections from C2 in order: Wins, In Progress, Blockers, Next Week", and Step 2's output says the same. If Build adds Risks, AC2 will fail every run until it's updated. Two other questions also belong here:
- Where does Risks go in the section order?
- Does the 400-word limit (R4) still hold with a fifth section?

**Options:**
1. **Update the requirements for Risks, then go to Build (my recommendation).** It's a short change, a few questions rather than the full 45–60 minute interview:
   - where the Risks section goes;
   - what counts as a risk, and where it comes from in the tracker;
   - whether the word limit changes;
   - one new test input for a week with risks.

   I'd keep the current file as `requirements-2026-10-16.md` first, so nothing is lost. After that, run the build skill in fix mode.
2. **Go straight to Build's fix mode** and leave the requirements alone. It's quicker, but AC2 will then conflict with the new template.
3. **Redo Deconstruct from scratch.** Only worth it if the workflow itself has changed a lot since June, beyond the Risks section.

You don't have a registry yet, so this workflow's records live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill".

Which option do you want?
