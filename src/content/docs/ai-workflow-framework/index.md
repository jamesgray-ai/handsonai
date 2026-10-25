---
title: AI Workflow Framework
description: "Five steps that turn a piece of your real work into an AI workflow that is specified, planned, built, tested and running on the AI you already use."
---

The AI Workflow Framework turns a piece of your real work into an AI workflow that is specified, planned, built, tested and running on the AI platform you already use. You make every real choice; the AI does the design work, the building and the checking, and asks only what it needs you to decide.

Each step is a skill in the `handsonai` plugin. [Install the plugin](skills/) once, then work through the steps in order.

## The Five Steps

| Step | What it does | What you get |
|---|---|---|
| **[Analyze](analyze/)** | Looks across your work for the workflows worth handing to AI | A backlog of candidate workflows, each with the work, the pain and the value, plus an opportunity report |
| **[Deconstruct](deconstruct/)** | Turns one workflow into a clear, testable description of what it must do | Your Workflow Requirements, with practice inputs taken from your real work |
| **[Design](design/)** | Plans how AI will do the work, and asks you only what only you can decide | An approved Design Plan that ends in a task list |
| **[Build](build/)** | Builds the plan task by task and checks each task, without making any real change | Your workflow, installed where it runs, and a build record of what was built and what it can access |
| **[Test](test/)** | Runs the workflow on practice inputs and one real example it hasn't seen, and checks every requirement with proof | Your test results, your decision, and the workflow live |

## How It Fits Together

**Three kinds of line.** Your Workflow Requirements hold three kinds of line, and every later step works from them:

- **What it must get right:** yes-or-no checks that every output must pass, such as "Every update names an owner and a date."
- **The rules it follows:** "It always…", "It never…" and "When…, it…" sentences.
- **Where a person checks:** the checkpoints where the workflow stops and asks you first, such as before it sends anything.

Design plans against these lines, Build checks each task against them, and Test grades every one.

**Two tracks.** Small, low-risk workflows take the **light** track; everything else takes the **full** track. Both use the same five steps and the same files, and each step is shorter on the light track. Deconstruct proposes a track early and you can switch. Any sign of risk keeps a workflow on the full track: a change that can't be undone, a change to a system other people use, running without you, regulated work, or confidential or outside content such as inbound email.

**Three stages prove a workflow.**

1. **Build's quick real checks** prove each kind of change works, with one small real change somewhere only you can see.
2. **Test's practice runs** prove the workflow does what it must on realistic inputs. Nothing is sent or changed.
3. **Your first real run** proves it at the real destination, with you watching and its checkpoints in place. A schedule comes only after one run by hand.

## What You Need

- **The five skills** on your platform. See [Install the Hands-on AI Plugin](skills/).
- **A folder for your workflow files**, called Framework. On Claude on the web and ChatGPT, it lives in Google Drive, or OneDrive on a work or school account, through the platform's connection with writes turned on. On Microsoft 365 Copilot, it lives in OneDrive. On the Claude desktop app, it's a folder on your computer that you add to each framework chat. On Claude Code and Codex, it's `framework/` in your workspace. The first skill you run asks where to keep it.
- **An [AI Registry](../builder-setup/ai-registry-setup/)**, if you want one. Analyze reads it so you don't describe your business twice, and every step keeps the workflow's card up to date. Without one, Analyze keeps a backlog file in the Framework folder.

Your workflow itself runs somewhere else: its own Project or folder, holding only what the workflow reads. Build sets that up. Keeping the two apart is what lets Test run your workflow cold, the way it will run at work.

## Moving From Step to Step

Run each step in a new chat (a new session on Claude Code and Codex). Start a step with its phrase and where your files are:

> run the design skill. My files are in Google Drive, in Framework/weekly-status-report.

Or say **"continue my workflow"** in any step. The skill reads your files, works out where the workflow is, and picks up there. Every step ends by giving you the phrase that starts the next one, so you never need to remember the order. Stopping partway is safe: progress is saved as you go.

**Started a workflow with an earlier version of the framework?** The framework sends it back to the earliest step whose files are in the old format, usually Deconstruct. Deconstruct offers your old requirements as something you've already written down, so you don't start from a blank page. Your old files stay where they are.

## Keeping It Working

Keeping a workflow working is part of every workflow, not a step of its own:

- **The flag line.** Every run ends by flagging anything it wasn't designed for, such as a new kind of input or a checkpoint it had to guess at, and tells you how to fix it with "change my workflow".
- **Re-checks.** When Test takes a workflow live, it sets a date to re-check it, three months out. Say "test the workflow I built" any time to re-check it, especially if you find yourself editing its work more than you used to. A workflow that keeps a run log reminds you when the date comes.
- **"Change my workflow".** Say "change my workflow" and what should change, and Design picks it up. A small change updates the requirements and the plan, Build rebuilds only what the change touches, and Test re-checks it. A big change, such as a different process or a different goal, goes back to Deconstruct. Every change starts at the requirements.

## Where It Runs

The framework runs on **Claude** (web and desktop app), **ChatGPT**, **Microsoft 365 Copilot**, **Claude Code** and **Codex**. On Microsoft 365 Copilot there are two places to build: skills are made in **Copilot Cowork**, and agents in **Agent Builder** (Copilot › Chat › Agents › New agent). The framework's own steps run in Copilot Cowork. [Install the Hands-on AI Plugin](skills/) covers each platform.

## The Spec Behind It

If you've worked with product teams, this is the PRD for your workflow: what it must do, not how it's built. Your Workflow Requirements are the spec in spec-driven development.

Spec-driven development is how AI coding tools such as [GitHub Spec Kit](https://github.com/github/spec-kit) and [Kiro](https://kiro.dev/docs/specs/) build software (as of October 2026). You write the spec first: what the work must do, and how you'll know it's done. Then a plan for how, broken into tasks. Then the build, task by task. Then a check of the result against the spec. The framework follows the same order for business workflows: Deconstruct writes the spec, Design writes the plan and its tasks, Build carries them out, and Test checks the result against the spec. When something needs to change, the change starts at the spec.

## Go Deeper

- [Framework Glossary](glossary/): every term, in plain language
- [AI Workflow Design Matrix](workflow-design-matrix/): how much the AI decides on its own, and who takes part while it runs
- [Analyze example reports](analyze-examples/): three finished opportunity reports
- [Agentic Building Blocks](../agentic-building-blocks/): the skills, agents, connections and context a workflow is built from
- [MCP server](../mcp-server/): ask your AI about the framework while you work
