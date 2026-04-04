---
title: "Step 2: Deconstruct Workflows into Structured Specifications"
description: Interactively break down any business workflow into discrete steps, surfacing decision points, data flows, context needs, and failure modes.
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What This Is

An interactive deep-dive that breaks down a business workflow into discrete steps — surfacing every hidden sub-step, decision point, data handoff, context requirement, and failure mode. Works with both individual workflows (one person's tasks) and organizational workflows (multi-role value chain processes), adding role transitions as an additional dimension for organizational workflows.

| | |
|---|---|
| **What you'll do** | Describe your workflow (or problem) and work through a guided conversation that probes each step for sub-steps, decision points, data flows, context needs, and failure modes |
| **What you'll get** | A **Workflow Definition** — a structured Markdown file capturing every step in detail |
| **Time** | ~15-25 minutes of interactive conversation |

## Why This Matters

You can't operationalize AI on a process you don't understand. Before you can build an AI-powered workflow, you need to break it down into discrete steps, identify the decision points and data flows, and understand what context each step needs and what happens when things go wrong.

The skill walks you through that deconstruction interactively. You provide the business scenario and rough steps — and the model either applies the 6-question framework to every step (step-decomposed path) or captures your goal, constraints, quality criteria, and capability domains (outcome-driven path). The deliverable:

- A **Workflow Definition** — the structured breakdown of your workflow into refined steps, with decision points, data flows, context needs, and failure modes captured for every step

The context needs and failure modes captured here directly inform design decisions in the next step — they tell you what context to create, what tools to connect, and where human review gates are needed.

This builds directly on the concepts of workflow deconstruction. If terms like the "6-question framework" or "AI building blocks" are new to you, review the [Key Concepts section of the Business-First AI Framework](../index.md#key-concepts) for quick definitions before starting.

## How to Use This

This step is facilitated by the **`deconstruct`** Business-First AI Framework Skill. How you get it depends on your platform — see [Get the Skills](../skills.mdx) for installation instructions.

**Start with this prompt:**

```
I need to deconstruct my [workflow name] workflow.
```

The skill runs an interactive deep dive — interviewing you about your scenario, refining your steps, then probing each step for sub-steps, decisions, data flows, context needs, and failure modes. It produces a structured Workflow Definition file.

:::tip[If your AI tool doesn't support skills]
Download the skill file from [GitHub](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins/business-first-ai/skills/deconstruct) and paste it into your system prompt or project instructions.
:::
### Example: What the first exchange looks like

After you start the conversation, the model will ask about your scenario. Here's what a typical opening looks like:

> **Model:** Let's start by understanding the workflow you want to deconstruct. First — what's the business scenario? What's the objective of this workflow, and why does it matter?
>
> **You:** I research LinkedIn prospects before sales outreach. The goal is to find people who'd be a good fit for our AI training programs, understand their background, and write personalized outreach messages. Right now it takes me about 45 minutes per prospect and I do maybe 10 a week.
>
> **Model:** Got it — LinkedIn prospect research for personalized sales outreach, with the goal of identifying fit and crafting tailored messages. That's a great workflow to deconstruct. Now, can you walk me through the high-level steps? Don't worry about being complete or precise — just describe what you typically do from start to finish, and we'll refine it together.
>
> **You:** I guess I start by finding people on LinkedIn, then I look at their profile, check their company, see if they've posted anything relevant, then I write the message. There's probably more to it but that's the gist.

From there, the model takes your rough steps and systematically breaks each one down — uncovering the sub-steps, decisions, data, and context you didn't think to mention.

### Example: Starting with a problem instead of a workflow

You don't need an existing process. If you have a gap or pain point, describe that — the model will help you design a workflow from scratch:

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

### Example: Defining an outcome for an agent system

When you know what you want produced but don't want to prescribe how the AI gets there, choose the outcome-driven path:

> **Model:** How would you like to approach this?
> (a) Deconstruct a known process — you can describe the steps and I'll interview you to surface hidden details
> (b) Start from a problem — you know what's broken; I'll propose a workflow and we refine it together
> (c) Define an outcome — you know what you want produced but want an agent system to figure out the approach
>
> **You:** (c) — I want a competitive analysis report produced weekly, but I don't want to prescribe how the agent researches or structures it.
>
> **Model:** Got it — outcome-driven. Let's define what the agent system needs to know. First: what does a successful run produce? Describe the deliverable.
>
> **You:** A 2-3 page report covering our top 5 competitors — what they shipped, pricing changes, new messaging, and any strategic moves. Formatted as a markdown doc with an executive summary at the top.
>
> **Model:** Clear. Now, what does the agent system receive to start? What triggers the work, and what materials does it have access to?
>
> **You:** It runs every Monday morning. It has access to our competitor list (a shared doc with URLs), our product positioning doc, and the web.

From there, the model continues through constraints, quality criteria, capability domains, tools/data, and human gates — building an outcome-driven Workflow Definition without decomposing into fixed steps.

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
- **Competitive analysis pipeline** (outcome-driven) — you know what the deliverable looks like but want an agent system to determine the research approach

You don't need to know all the steps before you start — that's what the skill helps you figure out. Even "I onboard new clients and it takes forever" is enough to begin. You can also start with a problem instead of a workflow — "People drop off during enrollment and I have no way to follow up" is a perfectly valid starting point.

## What the Skill Produces

The **Workflow Definition** captures one of two formats, depending on the path you chose:

**Step-decomposed** (paths a and b):

- **Scenario metadata** — name, description, outcome, trigger, type, objective, owners, definition type
- **Refined step-by-step breakdown** — each step with action, sub-steps, decision points, data in/out, context needs, failure modes
- **Step sequence and dependencies** — what's sequential, what's parallel, where the critical path is
- **Context shopping list** — every artifact the workflow needs, with status, key contents, AI accessibility, and readiness notes
- **Optimization summary** (if optimizations were applied) — what changed from the original process and why, including any optimizations declined and the reasoning

Most workflows expand from 5-8 rough steps to 12-20 refined steps after the deep dive.

**Outcome-driven** (path c):

- **Scenario metadata** — name, description, outcome, trigger, type, objective, owners, definition type
- **Goal** — what a successful run produces
- **Inputs** — what the agent system receives to start
- **Expected outputs** — format, structure, and quality expectations
- **Constraints** — boundaries and guardrails
- **Quality criteria** — evaluation dimensions (feeds directly into Test)
- **Capability domains** — what the agent system needs to be good at (research, analysis, writing, etc.)
- **Tools and data sources** — external systems with data readiness assessment
- **Human gates** — where human review is expected

Both formats are the input for the [Design phase](../design.md) in Step 3 — Design. Step-decomposed definitions go through per-step classification and building block mapping. Outcome-driven definitions go through capability domain mapping with pre-determined Autonomous autonomy and Agent orchestration.

### Process optimization

For step-decomposed workflows, the skill includes an **Optimize for AI** pass after the deep dive. Once the full process is mapped, the model steps back and challenges it — looking for steps that exist only because a human was doing the work (an integration eliminates the manual transfer), steps that can be collapsed (AI drafts and formats in one pass), steps that can be parallelized (no data dependency), handoffs that can be simplified, and new steps needed for the AI version. These are presented as recommendations for you to accept or reject — you may have good reasons to keep steps as-is (compliance, audit trail, stakeholder expectations). The Workflow Definition records what changed and why.

## Tips for Better Results

- **Start with workflows you actually do.** Real processes have real complexity that produces useful analysis. Hypothetical workflows tend to be too clean.
- **Include the messy details.** "Sometimes I skip this step if the client is a repeat customer" is exactly the kind of decision logic the model needs to capture.
- **Don't over-prepare your steps.** The model is designed to work with rough, incomplete descriptions. Let it do the work of refining and organizing.
- **Gather your context resources early.** The model will identify specific resources the workflow needs — documents like buyer personas and style guides, but also spreadsheets, databases, CRM access, application credentials, and sample data. If you already have these, have them ready. If you don't, the analysis will tell you exactly what to create or set up and what each resource should contain.

:::tip[Register your workflow in the AI Registry]
If you're using the [AI Registry](../../use-the-playbook/build/ai-registry.mdx) Notion database, register your workflow as soon as naming is confirmed — the skill walks you through it. This creates a record of the workflow with its name, description, trigger, outcome, and type. You'll update this entry as you move through Build. Even if you're not using Notion, save the metadata somewhere — it's the first entry in your workflow inventory. See [Builder Tools Setup](../../builder-setup/notion-registry-setup.md) if you haven't set up the AI Registry yet.
:::
## Related

- **Previous step:** Not sure which workflow to deconstruct? Start with [Analyze Workflows](../analyze.md) (Step 1) to identify your best candidates.
- **Next step:** Ready to design? Go to [Design Your AI Workflow](../design.md) (Step 3) — assess autonomy, choose an orchestration mechanism, and map building blocks.
- [Business-First AI Framework](../index.md) — the full seven-step methodology
- [Prompts](../../agentic-building-blocks/prompts/index.md)
- [Agents](../../agentic-building-blocks/agents/index.md)
