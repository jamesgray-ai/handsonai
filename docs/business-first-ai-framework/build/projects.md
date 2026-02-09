---
title: Projects
description: Set up a persistent workspace for your workflow — group context, prompts, and conversation history in one place.
---

# Projects

> **Part of:** [Build Workflows](index.md)

!!! tip "New to projects as a building block?"
    See [Agentic Building Blocks > Projects](../../agentic-building-blocks/projects/index.md) for definitions, examples, and cross-platform implementation details (Claude Projects, OpenAI Projects, Gemini Gems, M365 Copilot agents).

## What This Is

A project is a persistent workspace that groups your context, prompts, and conversation history. It's where your workflow lives and runs.

| | |
|---|---|
| **What you'll do** | Decide whether your workflow needs a project, then set one up if it does |
| **What you'll get** | A configured workspace with your context artifacts pre-loaded, ready for repeated workflow runs |
| **Time** | ~5-10 minutes |

## When to Use a Project vs. a Normal Chat

Not every workflow needs a project. Use the Execution Context recommendation from your AI Building Block Map as your starting point:

**Normal chat** — Best when:

- The workflow runs infrequently (monthly or less)
- Few or no context files needed (0-2 files)
- All context can be provided inline each time
- The workflow is a one-off or experimental process

**Project workspace** — Best when:

- The workflow runs frequently (weekly or more)
- Multiple context files needed (3+ files)
- The same reference materials are used every run
- Conversation memory across runs would be valuable
- Multiple people will run the same workflow

Many workflows start in normal chat and graduate to a project once they're proven and refined.

## Setting Up a Project for Your Workflow

1. **Create the project** — Name it after your workflow (e.g., "Lead Qualification," "Weekly Report Generation")
2. **Upload context artifacts** — Add the files you created in the [Context](context.md) step
3. **Add custom instructions** (optional) — A brief orientation for the AI about this workflow's purpose and domain. Keep this short — the prompt contains the workflow logic, not the project instructions.
4. **Run each workflow execution as a new conversation** within the project

## What Goes in the Project vs. the Prompt

This distinction matters:

**In the project:** Context — documents, data, rules, examples, and custom instructions. These persist across conversations and don't need to be re-provided each run.

**In the prompt:** Workflow logic, step sequencing, decision rules, human review gates. The prompt IS the workflow — always pasted fresh each run, never embedded in project instructions.

The prompt is self-contained. Someone could paste it into a normal chat with the context files attached and get the same result. The project provides convenience (pre-loaded files, conversation memory), not workflow logic.

## What's Next

With your workspace ready, build the [Prompt](prompt.md) that drives your workflow.
