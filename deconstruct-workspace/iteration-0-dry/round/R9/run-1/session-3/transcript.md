## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't start a new Deconstruct session. Step 2 (Deconstruct) is already done for this workflow, and it has moved past it.

You don't have a registry yet, so this workflow's requirements live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill."

**Where Weekly Status Report stands:**

- **Step 2, Deconstruct (done):** `framework/weekly-status-report/requirements.md` holds 4 steps, 3 context items, 3 acceptance criteria and 3 test inputs.
- **Step 3, Design (done and approved):** `design-spec.md` describes two skills, the HubSpot connector (read-only), and a pause for your review before anything is saved.
- **Step 5, Test (latest round 2026-07-10):** all 39 checks passed. Step 7 (Improve) still marked it **Not ready** because of one change, listed in `test-results.md`: the drafts have no **Risks** section, but the report you actually send does. The fix is to add that section to the template (C2), the tone guide (C3), and both skills.

**Next is Step 4, Build, to make that fix.** Running Deconstruct again would redo work that's finished.

**One gap in the requirements:** AC2 in `requirements.md` still says the report has exactly four sections (Wins, In Progress, Blockers, Next Week). Step 2's output says the same. If Build adds Risks and these stay as they are, the next Test round will fail on the new section.

**Also:** some files the records refer to aren't in this folder:
- the skill files Design planned under `framework/weekly-status-report/skills/`
- `runs.md`, the run log
- the `test-runs/` folder

They may be installed or saved somewhere else. Build will need to find them.

**How do you want to go on?**

1. **(Recommended)** I make a small change to the requirements: add Risks to AC2 and to Step 2's output. Where does Risks go in the order, for example between Blockers and Next Week? Then you say "run the build skill" to make the fix.
2. **Go straight to Build** and leave the requirements as they are.
3. **Redo Deconstruct from scratch.** I'd rename the current file to `requirements-2026-10-16.md` first, so nothing is lost. That's only worth it if the workflow itself has changed, not just the format.
