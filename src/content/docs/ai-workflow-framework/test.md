---
title: Test Your AI Workflow
description: "Test runs your workflow cold on practice inputs and one new input, checks every requirement with proof, and takes it live when you say yes."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Test proves the workflow does what your requirements say before you rely on it. It runs the workflow cold, in fresh chats kept apart from your requirements and plan, on practice inputs and one new input the workflow hasn't seen (ideally a real one from your recent work). It refuses any run that shows signs of drawing on your framework files. It checks every requirement with proof, and you decide what to fix or accept. When it's ready, Test takes it live.

## How the Skill Works

Test works in four parts. Practice runs show each change instead of making it:

1. **Open the round** — you give one real example the workflow hasn't seen, point Test to this week's through a connection, or ask Test to write one. Test makes sure every requirement has a practice input that tests it, and you confirm what counts as ready.
2. **Run it** — you run the practice inputs in one new chat and the new input in another, each started from one block you paste, and copy one block back. Test checks each requirement against what the workflow produced, with the proof, and you agree or not and say how much you'd edit it.
3. **The verdict** — each miss is sorted for Build or Design, you decide anything only you can decide, and the round is Ready, Not ready, or waiting on a connection's access.
4. **Go live** — when Test asks whether to take it live and you say yes, it first asks you to switch off any older version still set up, then marks the workflow live, writes down how to switch it off, tells you what the first real run does for the first time (run it by hand before any schedule goes on), and sets a date to re-check it.

## What You Get

Your **test results**, saved as `test-results.md` in the workflow's folder, with earlier rounds kept in its `history/` folder. On your yes, the workflow is live.

## How to Start

Say **"test the workflow I built"** with where your files are, for example "test the workflow I built. My files are in Google Drive, in Framework/weekly-status-report." On Claude Code you can also type `/handsonai:test`. Say the same phrase any time to re-check a live workflow.

## Worth Knowing

- **Test grades what the workflow produced, never what it says it did.** In one of my own tests, an agent I built in Microsoft 365 Copilot ended its run with the summary "Staples added: Bananas, Bread, Milk". The list it made had no Milk. The summary sounded right; the output was wrong. Test checks the output itself, so a miss like that is caught and goes back to Build to fix.
- **Practice runs are built never to send or change anything.** Every practice run opens by saying that nothing will be sent or changed; if a run doesn't, stop it. If your platform itself asks you to approve sending, posting or changing something during a practice run, choose Deny and tell Test. Answer the workflow's own questions as you would at work.

**Next:** once it's live, see [Keeping It Working](../#keeping-it-working) for the flag line, re-checks and "change my workflow".
