## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't start the interview, because Weekly Status Report has already been through Step 2. Running it from scratch would redo finished work and replace a requirements file that later steps depend on. I haven't changed any files.

**Where the workflow stands now (in `framework/weekly-status-report/`):**
- **Step 2, Deconstruct:** done. `requirements.md` has 4 steps, 3 acceptance criteria, 5 rules, 2 human gates and 3 test inputs.
- **Step 3, Design:** done (`design-spec.md`).
- **Steps 5–6, Test and Run:** done. The workflow went live and has runs logged for 2026-06-26 and 2026-07-03.
- **Step 7, Improve:** found one gap. The report the workflow produces is missing a **Risks** section that Maya adds before she sends it. Improve sent this back to Build to fix, and the last test round (2026-07-10) is marked **Not ready** until that's done.

**What this means for the requirements:** they still say the report has four sections (`requirements.md:101`, AC2: Wins, In Progress, Blockers, Next Week), and R4 says to use the template with those sections. If Build adds Risks without updating the requirements, Test will grade the next round against the old four-section list. So the requirements do need a small change, but only to the parts about Risks:
- update AC2 and R4 to include Risks, and decide where it goes in the section order
- decide what a Risks entry has to contain (for example, an owner and how it's being handled, like R1 does for blockers)
- check that the reports stay under 400 words with the extra section
- possibly add a test input with risks in it

I'd keep a copy of the current file as `requirements-2026-10-15.md` before changing it.

**Your options:**
1. **Update the requirements for Risks (recommended).** This is about 10 minutes. After that, Build makes the fix.
2. **Go straight to Build** and fix the template as Improve recorded it. You'd update the requirements afterwards.
3. **Redo the full Deconstruct** (45–60 minutes), if the workflow itself has changed more than this one section.

You don't have a registry yet, so this workflow's records live only in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill".

Which would you like?
