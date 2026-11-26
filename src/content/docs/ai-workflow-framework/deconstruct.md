---
title: Deconstruct Workflows into Requirements
description: "Deconstruct turns one workflow into Workflow Requirements: the goal, what it produces, the checks every output must pass, the rules it follows, and where you check."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Deconstruct turns one workflow into a clear, testable description of what it must do. Everything built later comes from what it captures.

If you've worked with product teams, this is the PRD for your workflow: what it must do, not how it's built. Your Workflow Requirements are the spec in spec-driven development.

## How the Skill Works

You choose a workflow, then work through one interview in which Deconstruct drafts each part and you correct it. The outcome comes first, so every workflow has a clear goal, a defined output and checks before anything else is written. Deconstruct tells you at the start about how many replies it takes, and nothing your Analyze report or registry already recorded is asked again: it's drafted for you to correct.

1. **Choose the workflow** — pick one from your backlog, or name any other workflow. Bring anything you already have written down (an SOP, a checklist, a past example, notes), and Deconstruct drafts from it.
2. **The interview** — a name and description to confirm; then, each drafted for you to correct, the goal and what it produces; the checks every output must pass, with the one question only you can answer (what a draft could get wrong that only you would notice); what it works from; its rules and safety limits; where you check its work; and two or three practice runs. It states what it already knows, asks only what's open, and fills in the rest with defaults you can change. Every workflow also gets a short set of safety limits for you to keep or change: what it must never do, and, when it sends or changes something, runs without you, or reads confidential or outside content, where its data may go, who sees it and what it records. Where your answers call for it, it adds a few more questions: whether a law applies, when the work touches health data, money advice, records about individual customers or staff, or a regulated industry; if one does, which one, what it requires every time and which decisions a person must make or approve, each recorded as a rule or checkpoint that names the law; whether your company's rules and client agreements allow confidential details to go into an AI tool; and what it must remember between runs when it runs on a schedule or in batches.
3. **Generate Workflow Requirements** — you see a one-screen summary, then Deconstruct saves the requirements, updates your registry and gives you the exact words to start Design in a new chat.

## What You Get

Your **Workflow Requirements**, saved as `requirements.md` in `framework/<workflow>/` inside your working folder, with the context files the workflow reads in `context/` (and any real practice input you gave in `inputs/`). Its requirement lines are the [three kinds of line](../#how-it-fits-together): the checks every output must pass (each saying where its information comes from), the rules it follows, and where a person checks. Alongside them sit the goal, the output (what it is, who it's for, its form, voice and structure), why it matters, the sources it uses and its safety limits. It doesn't break the work into steps: [Design](../design/) plans how the work gets done.

## How to Start

Say **"run the deconstruct skill"**, or **"run the deconstruct skill on [workflow]"** to name one. Add where your files are, for example "My files are in Google Drive, in ai-workspace." On Claude Code you can also type `/handsonai:deconstruct`.

## Worth Knowing

- **"Not sure" is always a fine answer.** Deconstruct explains the questions that need it, says what a "not sure" will record, and drafts what it can for you to keep or change.
- **Stopping early is safe.** Once the workflow has a name, progress is saved as you go, so you pick up where you left off.
- **Every check is required, and anything it must never do has no exceptions.** At Test, a miss on a check is yours to fix or accept; a miss on something it must never do always sends it back.
- **The data question is asked before it's built.** If your company's rules or client agreements may not allow some details in an AI tool, Deconstruct offers to leave the source out, add a step where someone removes those details first, or keep the workflow from going live until you've checked. Test asks you to confirm before it goes live.
- **Practice runs are described from your real work.** Deconstruct drafts two or three practice runs, including your typical case and tricky ones drawn from your own rules, each with what should happen, for you to change or drop. Test writes each practice input from them, plus the rest it needs, and shows you every input before it's used; you can give it a real one then instead, with names and details swapped for made-up ones.

**Next:** [Design](../design/) reads your requirements and plans how AI will do the work.
