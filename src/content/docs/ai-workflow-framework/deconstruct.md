---
title: Deconstruct Workflows into Requirements
description: "Deconstruct turns one workflow into Workflow Requirements: the goal, what every output must get right, the rules it follows, and where you check."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Deconstruct turns one workflow into a clear, testable description of what it must do. Everything built later comes from what it captures, so it's the most thorough conversation in the framework.

If you've worked with product teams, this is the PRD for your workflow: what it must do, not how it's built. Your Workflow Requirements are the spec in spec-driven development.

## How the Skill Works

You choose a workflow, then work through five parts. The outcome comes before the steps, so every workflow has a clear goal and checks before anything else is written.

On the light track, a shorter version replaces the five parts: a name, the goal, what it must get right, what it works from, the rules and two or three practice runs, then three safety questions; Deconstruct fills in the rest with defaults you can correct. Any sign of risk switches it to the full version.

1. **Choose the workflow** — pick one from your backlog, or describe it. Bring anything you already have written down (an SOP, a checklist, a past example, notes), and Deconstruct drafts from it. It also proposes the light or full track here.
2. **What this is worth** — what gets better and for whom, what you'd measure, and today's number.
3. **Scope and a name** — one trigger and one deliverable, a clear name and description, and whether a law or regulation applies.
4. **The outcome** — say it, sharpen it, make it checkable: a one-sentence goal, then yes-or-no checks for what every output must get right, with the must-haves marked.
5. **How the work gets done** — whether it should go the same way every time, the AI can work out how each time, or some of each; what must stay fixed; where you review or approve; and the decisions and what settles them.
6. **Rules, sources and practice runs** — the rules it follows, the sources it uses, and practice runs based on your real work, drafted for you to correct; then three questions it always asks: what it may send or change, whether you take part while it runs, and what it does when it's unsure.
7. **Generate Workflow Requirements** — you see a preview, then Deconstruct saves the requirements and updates your registry.

## What You Get

Your **Workflow Requirements**, saved as `requirements.md` in `framework/<workflow>/` inside your working folder, with practice inputs in `inputs/` and the context files the steps read in `context/`. Its requirement lines are the [three kinds of line](../#how-it-fits-together): what it must get right, the rules it follows, and where a person checks. Alongside them sit the goal, what it's worth, the sources it uses and its safety limits.

## How to Start

Say **"run the deconstruct skill"**, or **"run the deconstruct skill on [workflow]"** to name one. Add where your files are, for example "My files are in Google Drive, in ai-workspace." On Claude Code you can also type `/handsonai:deconstruct`.

## Worth Knowing

- **"Not sure" is always a fine answer.** Deconstruct explains the questions that need it, says what a "not sure" will record, and drafts what it can for you to keep or change.
- **Practice runs are drafted from your real work.** Deconstruct drafts three to five practice runs (two or three on the light track), including your typical case and a tricky one, for you to change or drop. For each real one, paste the input you'd start from, with names and details swapped for made-up ones, or ask it to draft a made-up input in the same shape. Test runs the workflow on them later, so the closer they are to your real work, the more the test tells you.

**Next:** [Design](../design/) reads your requirements and plans how AI will do the work.
