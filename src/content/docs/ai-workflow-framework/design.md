---
title: Design Your AI Workflow
description: "Design reads your Workflow Requirements, drafts the whole plan for how AI will do the work, and asks you only what only you can decide."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Design decides how the workflow will be built, before anything is built. It reads your Workflow Requirements, researches your platform, and drafts the whole plan on its own: how much the AI decides at each step, which parts are skills or agents, where a person checks, what it connects to, and how each part will be checked.

## How the Skill Works

Design works in four parts:

1. **Where it runs** — Design plans for the platform you're running it in, so run Design where the workflow will run (you can name another platform instead). It also confirms where your files are.
2. **The plan** — Design drafts the whole plan from your requirements, then checks it a second time, the way a stranger would read it (on Claude Code, in a separate session), for anything that would break a requirement, a rule or checkpoint, safety, or the build.
3. **A few questions for you** — only the questions Design couldn't settle itself, one at a time, with a recommendation and its reason wherever there's an option to choose.
4. **Review and approve** — you read the plan in plain words and approve it. It ends in the task list Build follows.

## What You Get

An approved **Design Plan**, saved as `design-plan.md` in the workflow's folder. It refers to your requirements rather than copying them, so each fact lives in one place.

## How to Start

Say **"run the design skill"** with where your files are, for example "run the design skill. My files are in Google Drive, in Framework/weekly-status-report." On Claude Code you can also type `/handsonai:design`.

Design is also where changes start. To change a workflow that's planned, built or live, say **"change my workflow"** and what should change.

## Worth Knowing

- **Few questions, and safety comes first.** Design asks at most five questions (three on the light track). Safety questions come first, are never dropped, and are asked even past that limit. Over that limit, Design takes the safe or recommended answer and lists it in the review as an assumption you can change. A fact nobody can answer yet, such as where a write should go, becomes a named open item, and only the tasks it blocks wait.
- **Simple first.** Design starts with the simplest thing that works: one agent before several, a limit on every loop, and a person before any change that can't be undone, unless you choose to accept that risk. The plan names the design pattern it uses, with the playbook page and its original source.

**Next:** [Build](../build/) builds the workflow from your approved plan, task by task.
