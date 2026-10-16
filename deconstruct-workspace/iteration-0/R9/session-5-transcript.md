## Student

Run the deconstruct skill for Weekly Status Report.

## AI

Weekly Status Report has already been deconstructed, so I haven't started the interview or changed any files.

**Where it stands:**
- **Step 2 (Deconstruct):** done. The requirements are in `framework/weekly-status-report/requirements.md`. They describe a step-driven workflow with 4 steps, 3 context items, 3 acceptance criteria (AC1–AC3) and 3 saved test inputs (E1–E3).
- **Step 3 (Design):** done and approved (`design-spec.md`).
- **Step 5 (Test):** the 2026-07-10 retest passed all 39 checks, but the workflow is still marked **not ready**. A review of real runs from 2026-06-26 and 2026-07-03 found that the reports you actually send have a **Risks** section, and the workflow doesn't produce one.

**Why this affects the requirements:** they also say the report has exactly four sections. AC2 requires "Wins, In Progress, Blockers, Next Week" in that order, and Step 2 and R4 say the same. Your three past reports, which are the reference for the format, have those four headings and no Risks. The planned fix only updates the template, the tone guide and the two skills. If only those change, the requirements would contradict the new report, and the next test would mark the Risks section as off-format.

**Options:**
1. **Update the requirements for the Risks section (recommended, about 10 minutes).** I'd save the current file as `requirements-2026-10-15.md` and then update Step 2's output, AC2, R4, and the template entry (C2). I'd also add a test input with a risk in it, plus a recent report that includes Risks to use as the reference example. After that, the fix gets built against requirements that agree with it.
2. **Run the full Deconstruct again from scratch (45–60 minutes).** This only makes sense if more than this one section has changed.
3. **Skip the requirements and go straight to the Build fix.** This leaves the contradiction above in place.

If you choose option 1, I'll need:
- Where Risks goes in the order (after Blockers?) and what each risk entry must state (owner, likelihood/impact, mitigation?).
- Whether risks come from the same HubSpot tracker comments or somewhere else.
- A recent report you sent that includes Risks, with any confidential details changed. I'll use it as the new reference example.

**Also worth knowing:**
- You don't have a registry yet, so this workflow's requirements live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill".
- The design spec and test results refer to files that aren't in this folder: `skills/`, `test-runs/` and `runs.md`. They may live in another working folder. Check before the Build fix.
