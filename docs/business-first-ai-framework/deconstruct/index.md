---
title: "Step 2: Deconstruct Workflows"
description: Interactively break down any business workflow into discrete steps, surfacing decision points, data flows, context needs, and failure modes.
---

# Step 2: Deconstruct Workflows

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What This Is

An interactive deep-dive that breaks down a business workflow into discrete steps — surfacing every hidden sub-step, decision point, data handoff, context requirement, and failure mode.

| | |
|---|---|
| **What you'll do** | Describe your workflow (or problem) and work through a guided conversation that probes each step for sub-steps, decision points, data flows, context needs, and failure modes |
| **What you'll get** | A **Workflow Definition** — a structured Markdown file capturing every step in detail |
| **Time** | ~15-25 minutes of interactive conversation |

## Why This Matters

You can't operationalize AI on a process you don't understand. Before you can build an AI-powered workflow, you need to break it down into discrete steps, identify the decision points and data flows, and understand what context each step needs and what happens when things go wrong.

This prompt walks you through that deconstruction interactively. You provide the business scenario and rough steps — the model handles the structured analysis, applying the 5-question framework (discrete steps, decision points, data flows, context needs, failure modes) to every step. The deliverable:

- A **Workflow Definition** — the structured breakdown of your workflow into refined steps, with decision points, data flows, context needs, and failure modes captured for every step

The context needs and failure modes captured here directly inform design decisions in the next step — they tell you what context to create, what tools to connect, and where human review gates are needed.

This builds directly on the concepts of workflow deconstruction. If terms like the "5-question framework" or "seven building blocks" are new to you, review the [Key Concepts section of the Business-First AI Framework](../index.md#key-concepts) for quick definitions before starting.

## How to Use This

There are two ways to run this: as a **prompt** in any AI tool, or with the **Claude platform** plugin.

=== "Any AI Tool"

    Works with ChatGPT, Gemini, M365 Copilot, Claude, or any AI chat tool.

    1. **Go to [Break Down Your Workflow](workflow-definition.md)** — Copy the prompt, start a new conversation, paste the prompt, and describe your workflow
    2. **Save the Workflow Definition** — Download the `.md` file the model produces (or copy the output and save it as `[workflow-name]-definition.md`)
    3. **Go to [Build Workflows](../build/index.md)** — Start with the Design phase to choose your execution pattern and map building blocks

=== "Claude Platform"

    Install the [Business-First AI plugin](../../plugins/business-first-ai.md) and the `workflow-deconstructor` agent orchestrates the full process — running discovery, deconstruction, design, and build in sequence with file-based handoffs between stages.

    **Install the plugin:**

    ```bash
    /plugin install business-first-ai@handsonai
    ```

    **Start with this prompt:**

    ```
    I want to deconstruct my [workflow name] workflow.
    Walk me through the full process.
    ```

    **Review the outputs** — deliverables are saved to the `outputs/` directory. You can also run individual steps using the skills directly: `discovering-workflows` (Discover), `deconstructing-workflows` (Deconstruct), `building-workflows` (Build).

    The plugin works on three Claude interfaces:

    | Interface | How to install | Notes |
    |-----------|---------------|-------|
    | **Claude Code** | Run `/plugin install` in the terminal | Full agent + skill support |
    | **Cowork** | Click **+** > **Add plugins...** > upload the plugin ZIP | Same capabilities, visual interface |
    | **Claude.ai** | Upload skill ZIPs under **Settings > Capabilities > Upload skill** | Skills only — the orchestrator agent doesn't work in Claude.ai, so you run skills individually with manual handoffs ([details](../../plugins/using-plugins.md#using-skills-in-claudeai-web)) |

    For setup details, see [Using Plugins](../../plugins/using-plugins.md).

Both options follow the same process and produce the same deliverable.

!!! tip "Start with a workflow you actually do"
    Real workflows produce the best results. The model will surface hidden steps and assumptions you've internalized — that's much harder with hypothetical processes. If you don't have an existing workflow but have a clear problem to solve, that works too — the model will help you design one.

!!! tip "Register your workflow in the AI Registry"
    If you're using the [AI Registry](../../plugins/ai-registry.md) Notion database, register your workflow as soon as naming is confirmed — the prompt walks you through it. This creates a record of the workflow with its name, description, trigger, outcome, and type. You'll update this entry as you move through Build. Even if you're not using Notion, save the metadata somewhere — it's the first entry in your workflow inventory. See [Builder Stack Setup — Step 6](../../builder-setup/notion-registry-setup.md) if you haven't set up the AI Registry yet.

!!! tip "Keep your files together"
    By the end of the full process you'll have several Markdown files: `[name]-definition.md` (from Deconstruct), `[name]-building-block-spec.md` (from Build: Design), and `[name]-prompt.md` (from Build: Construct), plus any skills you built. Keep them in a single folder — they form a complete record of your workflow deconstruction. You can share any of these files with your team for feedback, put them in version control, or hand them to a colleague.

!!! tip "Markdown renders as formatted text"
    Markdown (`.md`) files are plain text with lightweight formatting — headings, bold, lists, tables. Many tools render them automatically: GitHub, Notion, VS Code, and most code editors show the formatted version when you open the file. You can also paste Markdown into Google Docs or Notion and it converts on the fly.

    If you'd prefer a polished document, ask your AI tool: "Convert this to a Word document" or "Reformat this as a PDF." The content is the same — Markdown is just the most portable starting format because it works everywhere and is easy to version-control.

### Example: What the first exchange looks like

After you paste the prompt, the model will ask about your scenario. Here's what a typical opening looks like:

> **Model:** Let's start by understanding the workflow you want to deconstruct. First — what's the business scenario? What's the objective of this workflow, and why does it matter?
>
> **You:** I research LinkedIn prospects before sales outreach. The goal is to find people who'd be a good fit for our AI training programs, understand their background, and write personalized outreach messages. Right now it takes me about 45 minutes per prospect and I do maybe 10 a week.
>
> **Model:** Got it — LinkedIn prospect research for personalized sales outreach, with the goal of identifying fit and crafting tailored messages. That's a great workflow to deconstruct. Now, can you walk me through the high-level steps? Don't worry about being complete or precise — just describe what you typically do from start to finish, and we'll refine it together.
>
> **You:** I guess I start by finding people on LinkedIn, then I look at their profile, check their company, see if they've posted anything relevant, then I write the message. There's probably more to it but that's the gist.

From there, the model takes your rough steps and systematically breaks each one down — uncovering the sub-steps, decisions, data, and context you didn't think to mention.

### Example: Starting with a problem instead of a workflow

You don't need an existing process to use this prompt. If you have a gap or pain point, describe that — the model will help you design a workflow from scratch:

> **Model:** Let's start by understanding the workflow you want to deconstruct. First — what's the business scenario? What's the objective of this workflow, and why does it matter?
>
> **You:** I don't really have a workflow for this — it's more of a problem. People sign up for my online course but a lot of them never finish. I have no way to know who's dropping off, when they stop engaging, or how to follow up. I'm just losing students and I don't find out until it's too late.
>
> **Model:** Got it — so this isn't an existing process to break down, it's a gap you need to fill. Let me make sure I understand the problem before we design a solution. A few questions: What does "signing up" look like — is there a registration step, a payment, or both? And when you say people don't finish, do you have any data on where they tend to drop off, or is that part of the problem — you just don't know?
>
> **You:** They register and pay through my course platform. I can see completion rates in the dashboard but I don't check it regularly, and there's no alert or trigger when someone stops. I only notice if I happen to look.
>
> **Model:** That's clear. So the core gap is: no systematic way to detect drop-offs and no follow-up process when they happen. Let me propose a candidate workflow that would solve this, and you can tell me what fits and what doesn't.

From there, the model proposes a step-by-step workflow to address the problem, asks you to react and refine, and then continues into the deep dive just like any other workflow.

### Not sure which workflow to try?

Browse the [AI Use Cases](../../use-cases/index.md) section for inspiration — it organizes examples by type (content creation, research, coding, data analysis, ideation, and automation) with department-specific scenarios.

Or pick something you do regularly and could describe to a colleague over coffee. Here are some examples students have used:

- **Weekly team status reporting** — gathering updates from multiple sources, synthesizing, and distributing a summary
- **New client onboarding** — intake, account setup, kickoff scheduling, and initial deliverables
- **Processing expense reports** — collecting receipts, validating against policy, approving, and submitting for reimbursement
- **Content publishing pipeline** — drafting, editing, formatting, scheduling, and distributing across channels
- **Candidate screening** — reviewing applications, initial outreach, scheduling interviews, and tracking status
- **Vendor evaluation** — gathering proposals, comparing against criteria, scoring, and recommending a decision
- **Course enrollment follow-up** — people start signing up but don't finish, and there's no process to detect drop-offs or send reminders

You don't need to know all the steps before you start — that's what the prompt helps you figure out. Even "I onboard new clients and it takes forever" is enough to begin. You can also start with a problem instead of a workflow — "People drop off during enrollment and I have no way to follow up" is a perfectly valid starting point.

## What to Expect

**[Break Down Your Workflow](workflow-definition.md)** (~15-25 minutes) — The model asks about your business scenario, objective, steps, and who's involved. Then it works through each step one by one, asking about sub-steps, decision points, data flows, context needs, and failure modes. For later steps, it switches to a "propose and react" pattern — presenting hypotheses for you to correct, which is faster and surfaces more detail. Produces a **Workflow Definition**.

Most workflows expand from 5-8 rough steps to 12-20 refined steps after the deep dive. After the Workflow Definition is complete, take it to [Step 3 — Build Workflows](../build/index.md). The Build step starts with a Design phase where you choose your execution pattern and map each step to AI building blocks.

## Tips for Better Results

- **Start with workflows you actually do.** Real processes have real complexity that produces useful analysis. Hypothetical workflows tend to be too clean.
- **Include the messy details.** "Sometimes I skip this step if the client is a repeat customer" is exactly the kind of decision logic the model needs to capture.
- **Don't over-prepare your steps.** The model is designed to work with rough, incomplete descriptions. Let it do the work of refining and organizing.
- **Gather your context resources early.** The model will identify specific resources the workflow needs — documents like buyer personas and style guides, but also spreadsheets, databases, CRM access, application credentials, and sample data. If you already have these, have them ready. If you don't, the analysis will tell you exactly what to create or set up and what each resource should contain.
- **Save your files.** The Workflow Definition is your reference material. Keep it in a folder or version control — you'll use it throughout the Build step.
- **Iterate the executable prompt.** Once you generate it in Build, run it once, see what works and what doesn't, then refine. The first version is a strong draft, not a final product.

## Related

- **Previous step:** Not sure which workflow to deconstruct? Start with [Discover Workflows](../discover.md) (Step 1) to identify your best candidates.
- **Next step:** Ready to build? Go to [Build Workflows](../build/index.md) (Step 3) — starting with the Design phase to choose your execution pattern and map building blocks.
- [Business-First AI Framework](../index.md) — the full three-step methodology
- [Prompts](../../agentic-building-blocks/prompts/index.md)
- [Agents](../../agentic-building-blocks/agents/index.md)
