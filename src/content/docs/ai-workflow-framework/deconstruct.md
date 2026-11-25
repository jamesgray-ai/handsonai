---
title: Deconstruct Workflows into Requirements
description: "Deconstruct turns one workflow into Workflow Requirements: the goal, what every output must get right, the rules it follows, and where you check."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Deconstruct turns one workflow into a clear, testable description of what it must do. Everything built later comes from what it captures.

If you've worked with product teams, this is the PRD for your workflow: what it must do, not how it's built. Your Workflow Requirements are the spec in spec-driven development.

## How the Skill Works

You choose a workflow, then answer one interview. The outcome comes first, so every workflow has a clear goal and checks before anything else is written. Deconstruct tells you at the start about how many questions there are, and nothing your Analyze report already recorded is asked again: it's played back once for you to correct.

1. **Choose the workflow** — pick one from your backlog, or describe it. Bring anything you already have written down (an SOP, a checklist, a past example, notes), and Deconstruct drafts from it.
2. **The interview** — a name and description to confirm; three safety questions (what it may send or change, whether you take part while it runs, and whether a law or regulation applies); then what it's for, what every output must get right, what it works from, its rules, and two or three practice runs. Deconstruct drafts most of it for you to correct and fills in the rest with defaults you can change. Every workflow also gets a short set of safety limits for you to keep or change: what it must never do, and, when it sends or changes something, runs without you, or reads confidential or outside content, where its data may go, who sees it and what it records. Where your answers call for it, it adds a few more questions: when a law applies, which one, what it requires every time and which decisions a person must make or approve, each recorded as a rule or checkpoint that names the law; whether your company's rules and client agreements allow confidential details to go into an AI tool; and what it must remember between runs when it runs on a schedule or in batches.
3. **Generate Workflow Requirements** — you see a preview, then Deconstruct saves the requirements and updates your registry.

## What You Get

Your **Workflow Requirements**, saved as `requirements.md` in `framework/<workflow>/` inside your working folder, with practice inputs in `inputs/` and the context files the workflow reads in `context/`. Its requirement lines are the [three kinds of line](../#how-it-fits-together): what it must get right, the rules it follows, and where a person checks. Alongside them sit the goal, the sources it uses and its safety limits. It doesn't break the work into steps: [Design](../design/) plans how the work gets done.

## How to Start

Say **"run the deconstruct skill"**, or **"run the deconstruct skill on [workflow]"** to name one. Add where your files are, for example "My files are in Google Drive, in ai-workspace." On Claude Code you can also type `/handsonai:deconstruct`.

## Worth Knowing

- **"Not sure" is always a fine answer.** Deconstruct explains the questions that need it, says what a "not sure" will record, and drafts what it can for you to keep or change.
- **Stopping early is safe.** Once the workflow has a name, progress is saved as you go, so you pick up where you left off.
- **Anything it must never do counts like a must-have.** One miss on it at Test always sends the workflow back; it can't be accepted.
- **The data question is asked before it's built.** If your company's rules or client agreements may not allow some details in an AI tool, Deconstruct offers to leave the source out, add a step where someone removes those details first, or keep the workflow from going live until you've checked. Test asks you to confirm before it goes live.
- **Practice runs are drafted from your real work.** Deconstruct drafts two or three practice runs, including your typical case, each with what should happen, for you to change or drop. Test adds the rest it needs, such as an empty input and one carrying an instruction aimed at the AI. You see every input either one writes before it's used. For each real one, paste the input you'd start from, with names and details swapped for made-up ones, or ask it to draft a made-up input in the same shape. Test runs the workflow on them later, so the closer they are to your real work, the more the test tells you.

**Next:** [Design](../design/) reads your requirements and plans how AI will do the work.
