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

1. **Choose the workflow** — pick one from your backlog, or describe it. Bring anything you already have written down (an SOP, a checklist, a past example, notes), and Deconstruct drafts from it. It also proposes the light or full track here.
2. **What this is worth** — what gets better and for whom, what you'd measure, and today's number.
3. **Scope and a name** — one trigger and one deliverable, a clear name and description, and whether a law or regulation applies.
4. **The outcome** — say it, sharpen it, make it checkable: a one-sentence goal, then yes-or-no checks for what every output must get right, with the must-haves marked.
5. **How the work gets done** — whether it should go the same way every time or the AI can work out how each time; what must stay fixed; where you review or approve; and the decisions and what settles them.
6. **Rules, sources and practice runs** — the rules it follows, the sources it uses, and practice inputs taken from your real work, drafted for you to correct.
7. **Generate Workflow Requirements** — you see a preview, then Deconstruct saves the requirements and updates your registry.

## What You Get

Your **Workflow Requirements**, saved as `requirements.md` in the workflow's own folder inside your Framework folder, with practice inputs in `inputs/` and the context files the steps read in `context/`. Each requirement is one of [three kinds of line](../#how-it-fits-together): what it must get right, the rules it follows, and where a person checks.

## How to Start

Say **"run the deconstruct skill"**, or **"run the deconstruct skill on [workflow]"** to name one. Add where your files are, for example "My files are in Google Drive, in Framework." On Claude Code you can also type `/handsonai:deconstruct`.

## Worth Knowing

- **"Not sure" is always a fine answer.** Deconstruct explains the questions that need it, recommends an answer wherever you're choosing, and drafts what it can for you to keep or change.
- **Practice inputs come from your real work.** Bring two or three realistic examples, with names and details changed where they need to be. Test runs the workflow on them later, so the closer they are to your real work, the more the test tells you.

**Next:** [Design](../design/) reads your requirements and plans how AI will do the work.
