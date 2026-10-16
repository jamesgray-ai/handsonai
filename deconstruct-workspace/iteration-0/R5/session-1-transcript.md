## Student

Run the build skill.

## AI

Phase 1 of 5 in this fix pass: spec and requirements loaded.

- **Workflow:** Weekly Status Report (`registry/workflows/weekly-status-report.md`, in production)
- **Mechanism:** Skill. **Involvement:** Augmented. **Platform:** Claude (code mode). **Packaging:** Standalone Skill, one zip per skill.
- **Counts:** 4 steps, 2 skills (S1 orchestrator `weekly-status-report`, S2 `status-report-drafting`), 0 agents, 1 integration (HubSpot, read-only)
- Spec is `spec_version: 3.0` and `approved: true`. The Workflow Requirements file (`framework/weekly-status-report/requirements.md`) is loaded.

**Phase 2 of 5: what I'm fixing.** The 2026-07-10 round finished as `not-ready`. Improve set that verdict on purpose: all 39 lines were met, and the round exists so this fix can run. The Issues table names one change. Maya added a **Risks** section by hand on 2026-06-26 and again on 2026-07-03, so the report the workflow drafts is one section short of the one she sends. I'll update the template (C2), the tone guide (C3), S2's section list and the orchestrator's format instruction. Everything else stays as it is: the HubSpot connector, Steps 1 and 4, both gates and the run logging. This is the first not-ready round since the Ready round on 2026-06-08, so there's no reason to go back to Design.

I'm not re-running platform research. Both skills already exist in the right format, and only their body text changes.

## Phase 3 of 5: context (C2 and C3 only)

| ID | Artifact | Outcome | What happens | Read-back |
|---|---|---|---|---|
| C2 | Past reports (the template) | **Provide it** | Add Maya's 2026-07-03 report, with its Risks section, to `context/past-reports/` | pending: needs your OK (below) |
| C3 | Tone guide | **Build it in**, as an edit to an existing file | Change the section order line in `context/tone-guide.md` | pending: needs your OK (below) |

**C2: one file to confirm.** The 07-03 report isn't in this workspace. I found it at `~/Downloads/weekly-status-report/outputs/weekly-status-report/status-report-2026-07-03.md`, and an identical copy is in the handsonai `examples/` folder. That Downloads folder is a separate, older copy of this workflow, so please confirm it's the report Maya actually sent.

- **Read-back from that report:** Risks is the **fifth section, after Next Week**. It has one line per risk and no owner. The 06-26 report has the same layout. Correct?
- **Strip a note?** Its Risks line ends with "— added by hand, second week." That reads like Maya's note to herself, not report text. I'd remove that phrase from the copy so the drafter doesn't learn to write it. OK?

**C3: proposed edit to `context/tone-guide.md`.** I won't overwrite this file without your OK.

```diff
- - Under 400 words. Four sections in this order: Wins, In Progress, Blockers, Next Week.
+ - Under 400 words. Five sections in this order: Wins, In Progress, Blockers, Next Week, Risks.
+ - Risks: what could slip but hasn't yet, one line each, taken only from this week's updates and comments. "None this week" when nothing points to one — never speculate.
```

The second bullet is my draft. It applies R2 ("never invent") to the new section. Correct it if Maya means something else by a risk.

## What I'll regenerate once you confirm (Phase 4)

- **S2 `status-report-drafting`:** the section list goes from four to five, with Risks last. It gets the Risks rule above, plus a quiet-week rule that Risks says "None this week" when there are none. The Output line names the five headings. The 400-word cap stays.
- **S1 `weekly-status-report` (orchestrator):** the Step 2 format instruction and the report outline gain `## Risks` / `- one line per risk` after Next Week. Nothing else changes.

Then Phase 5: the reconciliation table, rebuilding the two zips (`weekly-status-report.zip` and `status-report-drafting.zip`), and steps for Maya to re-save both skills in Claude (Customize → Skills).

**One more item, outside Build's scope:** improvement-plan item 3. AC2 and Step 2's Outputs in `requirements.md` still list four sections, so Test would grade the new report against the old shape. Do you want me to update those two lines to the five sections too?

**Reply with:**
1. Yes or no on the C2 file (and on stripping the note)
2. Approve or correct the C3 edit
3. Yes or no on updating AC2

Then I'll regenerate and package.
