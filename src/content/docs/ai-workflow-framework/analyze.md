---
title: Analyze Workflows for AI Opportunity
description: "Analyze looks across your work for the workflows worth handing to AI, and saves each one to a backlog with the work, the pain and the value."
---

> **Part of:** [AI Workflow Framework](../)

## What It's For

Analyze finds where AI fits in your work before you build anything. It aims to find 3 to 5 **candidate workflows**: pieces of work worth building with AI, such as work that eats time or slips, or work you'd do more of if you had the time. It looks from your business's point of view (the **Organizational** lens) or your own (the **Individual** lens), and ties each candidate to the goal it serves.

## How the Skill Works

1. **Reading and the lens** — It starts from your registry. Analyze reads your processes and goals from your [AI Registry](../../builder-setup/ai-registry-setup/) and tells you which point of view it will take. To switch, just say so.
2. **The evidence pass** — It asks before it looks. With your permission, it looks through what you've already given your AI: the documents in your working folder (on Claude Code and Codex, your knowledge graph, SOPs and process guides), files you attach, folders you name, and your saved memory and past chats where your AI has them (on Claude Code, your memory files and the requests you've typed). It never reads the rest of your drive, your email or your calendar. It keeps only work that fits your business, and leaves out client names and confidential details. Then you choose from a short list: up to 5 pieces of work it found, grouped by process, each with where it saw it and a guess at the problem. You keep the ones worth working on, correct any guess it got wrong, and tell it if AI already does any of them. Work that already runs is recorded as running, not added as new.
3. **The open question and follow-ups** — Analyze always asks where your time went, or what slipped, over the last few weeks. Two or three answers is plenty, and "not sure" is fine.
4. **Enough to choose from** — If that still leaves fewer than 3 candidates, it offers to look at one process more closely.
5. **The list, the report and registering** — You confirm the list once. You see every candidate with its name, a one-line description and the kind of value it adds. Rename, reword, move or leave out any, then each one is saved to your backlog and written up in your report. Analyze doesn't ask you to size anything, and no later step does either.

## What You Get

- **A backlog of candidate workflows:** one card per workflow in your [AI Registry](../../builder-setup/ai-registry-setup/), or `framework/backlog.md` in your working folder if you don't have a registry.
- **An opportunity report:** `framework/ai-opportunity-report.md` in your working folder, with each candidate's problem, the value it adds and the goal it serves. See three [example reports](../analyze-examples/).

## How to Start

Say **"run the analyze skill"**. On Claude Code you can also type `/handsonai:analyze`.

If Analyze is the first framework skill you run, it first asks for your working folder: the one folder that holds your AI Registry, your workflows and your knowledge graph. On Claude on the web, ChatGPT or Copilot Cowork, name the folder in your drive if you have one; if not, it makes a folder called ai-workspace there. On the Claude desktop app, it asks you to select your working folder in the prompt window, or to make one called ai-workspace (for example in Documents) and select that.

## Worth Knowing

- **Run it again any time.** Each later run adds its candidates to the same report, so nothing found earlier is lost. It offers again only what's new: documents added or changed since the last run, and your memory and chats.
- **It stays strategic.** Analyze names the work, the pain and the value, never the tool or connection that would do it. [Design](../design/) picks the tools, once the work is clear.
- **It doesn't rank or choose.** Every candidate goes on the backlog. You choose which one to build when you start [Deconstruct](../deconstruct/), which explains what makes a good first one (a handful of steps, started when you decide, working from material you already have) and suggests one if you're not sure.

**Next:** [Deconstruct](../deconstruct/) turns one workflow from your backlog into Workflow Requirements.
