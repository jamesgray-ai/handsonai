## Student

Run the deconstruct skill. Continue my workflow.

## AI

Your one workflow in progress is **Weekly Status Report**, and it's already past Deconstruct. You've finished through **Step 4 (Build)**. **Step 5 (Test)** is next, and you've done part of it.

- Requirements, design spec and both skills are all in place.
- Your test results (`framework/weekly-status-report/test-results.md`) show **E1 (Typical week) graded on 2026-06-05, with every line Met**. The round is still marked in progress.
- **E2 (Blocked-heavy week)** and **E3 (Quiet week)** haven't been run yet. Their input files are ready under `framework/weekly-status-report/inputs/`.

Running Deconstruct again would redo work you've already finished, so I've stopped here instead.

Two other things I noticed:
- Your registry has a note from **2026-07-10** saying leadership started asking for a **risks** section, and you added it to the report by hand twice. If you want that section built into the workflow, the requirements need updating first. That would be a real reason to go back to Deconstruct for this workflow.
- Your opportunity report lists **3 more workflows** that haven't been mapped or added to your registry: **Program Risk Register**, **Stakeholder Meeting Prep** and **Onboarding Checklist Drafting**.

**Which do you want to do?**
1. **Continue Step 5 (Test)** on Weekly Status Report by running E2 and E3. This is the next step in your workflow.
2. **Update Weekly Status Report's requirements** to add the risks section (this skill).
3. **Map a new workflow** from your report (this skill). Tell me which one, or say "not sure" and I'll suggest one.

## Student

Yes, run the test skill.

## AI

You've graded 1 of 3 scenarios so far, so **run E2 (Blocked-heavy week) in a new chat next.**

E2 is a made-up week with four blocked tasks, one of which has no owner. It mainly checks that every blocker names an owner and a next action, and how the report handles the blocker with no owner. There's no past report to compare it against.

**Input to paste** (from `framework/weekly-status-report/inputs/E2-blocked-heavy-week.md`):

```
# Tracker export — constructed scenario E2 (blocked-heavy week)

Source: constructed input for testing; mirrors the HubSpot export format.

| Task | Status | Owner | Updated | Comment |
|---|---|---|---|---|
| Billing API — tax calculation | Blocked | Tomás | 2026-06-04 | Tax-rate table still outstanding — Dana to deliver by Wednesday |
| Billing API — payment retries | Blocked | Tomás | 2026-06-03 | Needs a decision on retry policy from product — Sam to decide this week |
| Customer portal — SSO | Blocked | Priya | 2026-06-02 | Identity provider contract not signed — Legal owns, no date yet |
| Data migration — attachments | Blocked |  | 2026-06-04 | Storage quota exceeded; nobody assigned to raise it |
| Mobile app — offline mode | In progress | Marcus | 2026-06-02 | Week 1 of 3 |
| Reporting — leadership dashboard | Done | Maya | 2026-06-04 | Published |
```

**How to start it:**
1. Open a new chat in the Claude desktop app, pointed at this same workspace folder. That's how it reaches the installed skill and your results file.
2. Before you start, don't open or discuss the requirements, the design spec or the skill's source files in that chat. The installed skill itself is fine.
3. Say **"run my weekly status report as a test run"** and paste the input above under it.
4. When it pauses for your review, decide as you would on a real Friday.
5. When it finishes, say **test this** in that chat. I'll grade it there and add the results to `test-results.md`, then give you E3.

## Student

END
