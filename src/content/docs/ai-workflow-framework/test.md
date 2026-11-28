---
title: Test Your AI Workflow
description: "Test runs your workflow cold on practice inputs and one new input, checks every requirement with proof, and takes it live when you say yes."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Test proves the workflow does what your requirements say before you rely on it. It runs the workflow cold, in one practice chat kept apart from your requirements and plan, on practice inputs and one new input the workflow hasn't seen (ideally a real one from your recent work). It refuses any run that shows signs it saw your framework files. It checks every check, rule and limit with proof; a miss is yours to fix or accept, except anything it must never do, which always sends it back. When it's ready, Test takes it live.

## How the Skill Works

Test works in four parts. Practice runs show each change instead of making it:

1. **Open the round** — you give one real example the workflow hasn't seen, point Test to this week's through a connection, or ask Test to write one. Test writes the practice inputs Deconstruct described, makes sure every check has an input that tests it (in a first round it also writes an empty input, except on a small, low-risk workflow, and, when the workflow reads outside content, one carrying an instruction aimed at the AI), and that each thing it must never do is tempted by an input. You see each input Test writes as one line, with what it should do, and can ask to see any in full before it's used.
2. **Run it** — Test gives you one message: a few numbered steps to set up a new chat, then the box to paste into it, last. You run every input in that one practice chat and copy its whole last reply back. On Claude desktop, that's an incognito chat when the workflow doesn't read files from its own folder; other platforms use a new chat in the workflow's Project or folder, with memory off where that's one click, so the run shows what the workflow does on its own, as it would for anyone you share it with. Nothing else is switched off: your plugins and connections stay on, so if your platform asks to approve sending or changing something, you choose Deny. The one exception: when your files are in Google Drive or OneDrive and the workflow doesn't use that drive, you switch that drive off for the chat. Test reads which skills the run used and tells you about any it didn't expect. It grades every input in one message: a headline, one row per input with anything worth a look, and one question, how much you'd edit each draft, so you know whether it's good enough to use as well as whether it does what you wrote down.
3. **The verdict** — a short verdict line, then a scorecard showing every check against every input, each miss is sorted for Build or Design, you decide anything only you can decide, and the round is Ready, Not ready, or waiting on a connection's access. When it's not ready, Test says what passed, what's left and which step makes the fix, gives you that step's phrase to copy, and tells you to come back for a short second round, which checks the change on every input it touches. A miss on anything it must never do always sends it back. When Deconstruct recorded that the data it uses still needs your check against your company's rules, Test asks you last, once everything else would be Ready; if you haven't checked yet, the round waits, and next time Test opens with where the workflow stands and asks again, with no re-run.
4. **Go live** — when Test asks whether to take it live and you say yes, it asks you to switch off any older version it knows is still set up, then marks the workflow live, writes down how to switch it off, tells you how to use it and what the first real run does for the first time (run it by hand before any schedule goes on), gives you the phrases to re-check or change it, each ready to copy, and sets a date to re-check it. Your registry dashboard shows the last round's scorecard.

## What You Get

Your **test results**, saved as `test-results.md` in `framework/<workflow>/` in your working folder, with earlier rounds kept in its `history/` folder. On your yes, the workflow is live.

## How to Start

Say **"test the workflow I built"** with where your files are, for example "test the workflow I built. My files are in Google Drive, in ai-workspace/framework/weekly-status-report." On Claude Code you can also type `/handsonai:test`. Say the same phrase any time to re-check a live workflow.

## Worth Knowing

- **Test grades what the workflow produced, never what it says it did.** In one of my own tests, an agent I built in Microsoft 365 Copilot ended its run with the summary "Staples added: Bananas, Bread, Milk". The list it made had no Milk. The summary sounded right; the output was wrong. Test checks the output itself, so a miss like that is caught and goes back to Build to fix.
- **Practice runs never touch your real records.** When the workflow remembers earlier runs (which items it already handled), a practice run works on a copy of what it remembers, never the real one: on Claude Code, Test makes the copy in the run's practice folder; elsewhere, it asks you to point the run at a test copy.
- **Practice runs are built never to send or change anything.** Every practice run says that nothing will be sent or changed before it produces anything; if a run shows a draft or asks a question first, stop it. If your platform itself asks you to approve sending, posting or changing something during a practice run, choose Deny (in Copilot Cowork, Cancel) and tell Test. Answer the workflow's own questions as you would at work.

**Next:** once it's live, see [Keeping It Working](../#keeping-it-working) for the flag line, re-checks and "change my workflow".
