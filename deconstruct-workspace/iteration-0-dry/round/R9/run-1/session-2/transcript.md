## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't start a new interview: **Weekly Status Report has already been through Step 2 (Deconstruct), and Step 3 (Design) is done too.** Running Deconstruct again would replace finished work, so here's where it stands.

**What's already in `framework/weekly-status-report/`:**
- `requirements.md` is complete. It covers the goal, value and measurement (baseline Unknown, target under 25 minutes), 4 steps, 3 context items, 3 acceptance criteria, 5 rules and 2 human gates.
- The three test inputs E1–E3 are saved under `inputs/`.
- `design-spec.md` is marked `approved: true`. It builds the workflow as a skill on Claude that you work alongside.

**You've completed through Step 3 (Design). Next is Step 4 (Build).** To pick up there, say "run the build skill" or "continue my workflow".

**One mismatch in the requirements:** C3, the tone guide, is listed as `Needs Creation` / AI Accessible `No`. But `context/tone-guide.md` now exists and covers the voice rules (direct, no hedging, blockers name an owner, under 400 words, four sections). Build should treat it as `Exists` / `Yes`. I can make that one-row fix if you want.

**You don't have a registry yet,** so this workflow's requirements live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill".

**Which do you want?**
1. **Go to Build** (recommended). I'll fix the C3 row first if you want.
2. **Redo Deconstruct anyway.** I'd keep the current file as `requirements-2026-10-16.md` and start the interview again. The approved design spec would then be out of date, and Design would need to run again.
3. **Deconstruct a different workflow from your report:** Program Risk Register (about two hours at month end), Stakeholder Meeting Prep (30–40 minutes per meeting) or Onboarding Checklist Drafting (not sized yet).

## Student

no

## AI

Okay, I won't change anything. Your requirements, design spec and test inputs stay exactly as they are.

I'm not sure what the "no" covers, so tell me if you meant one of these:
- **No to the C3 fix:** fine. I'd leave the tone-guide row as it is, and Build will simply find the file when it runs.
- **No to all three options:** we'll stop here. When you're ready, say "continue my workflow" and it'll pick up at Step 4 (Build).
- **You want something else from "deconstruct Weekly Status Report":** tell me what you had in mind, like reviewing or changing part of the requirements.
