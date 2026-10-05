---
title: AI Workflow Design Matrix
description: "A 3x2 matrix combining autonomy (what decides the next step: Deterministic, Guided, Autonomous) with human involvement (Augmented, Automated)."
---Every AI workflow can be described by two dimensions: **what decides the next step** and **whether a person takes part while it runs**. These two dimensions combine into a 3x2 matrix of six workflow archetypes — a shared vocabulary for classifying, comparing, and designing AI workflows.

A third dimension — **Lens** — determines the scope of your analysis:

- **Individual** — Workflows scoped to one person's trigger-to-deliverable flow. Focus: personal productivity, task automation, quality improvement.
- **Organizational** — Workflows scoped to an end-to-end business process, potentially spanning multiple roles. Focus: value chain optimization, cross-functional efficiency, strategic outcomes.

The lens doesn't change the matrix — it changes what you're analyzing. An individual-lens audit surfaces your personal pain points; an organizational-lens audit surfaces value chain processes tied to business objectives. Both produce candidates classified on the same Autonomy x Involvement matrix.

## Two Dimensions Define Every AI Workflow

### Dimension 1: Autonomy — How Much Does the AI Decide on Its Own?

**Autonomy level: how much does the AI decide on its own? Look at what decides the next step.**

| Level | What you give the AI | What It Looks Like | Test | Example |
|-------|---------------------|--------------------|------|---------|
| **Deterministic** | Instructions | You set every step, and the AI carries each one out. It may write or summarize inside a step, but its output never changes what happens next. | Does the work follow the same path whatever the AI produces? | Pull this week's project updates, have the AI draft a status report, save it to the shared folder |
| **Guided** | Bounded decisions, with your method | You set the structure and the methodology (a rubric, criteria, a process); the AI uses it to make decisions on your behalf: route an item, choose a tool, judge quality and send work back. Its decisions are bounded (within your structure, by your rules), not open-ended. | Does the AI's judgment, made by your rules, decide what happens next? | Sort support emails by category and route each to the right queue; score insights 1–10 against your rubric and draft posts only for those that score 7 or higher |
| **Autonomous** | A goal | The AI plans its own steps, decides what to do next at each turn, and keeps going until the goal is met. Its decision-making is open-ended. | Could you only describe the goal, not the steps? | Research agents that decide what to investigate, follow what they find, and write an article |

Two notes keep the classification honest:

- **Writing or summarizing inside a step never makes a workflow Guided.** A step that drafts a client email is Deterministic if the draft goes to the same next step whatever it says. It turns Guided when an AI judgment — a score, a pass/fail grade, a category — decides where the work goes next.
- **The number of agents doesn't set the level.** Three agents in a fixed chain can be Deterministic or Guided; a single agent working from a goal can be Autonomous. Look at what decides the next step, not at how many AI workers there are.

Whether a person should check what the AI produced is a separate question: it's answered by the involvement mode below and by evaluation in [Test](../test/), not by autonomy.

The line between Guided and Autonomous follows Anthropic's distinction in [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents): *workflows* are "orchestrated through predefined code paths" — including routing and evaluator-optimizer loops, which are Guided here because the AI's judgment picks the path within a structure you defined — while *agents* "dynamically direct their own processes and tool usage," which is Autonomous.

### Dimension 2: Human Involvement — Is a Person in the Workflow While It Runs?

Human involvement describes whether a person takes part while the workflow is running — not before (design) or after (using the result), but during.

| Mode | What It Means | What It Looks Like | Example |
|------|---------------|-------------------|---------|
| **Augmented** | A person is in the workflow along the way, guiding, engaging, or collaborating with the AI while it runs | The workflow pauses for a person's input, feedback, or approval before it continues, or the person works alongside it in the session | Reviewing a draft before it's saved, answering the AI's questions as it researches |
| **Automated** | No one takes part until it's done | The workflow runs end-to-end on its own and the person sees only the result. Starting it by hand doesn't change that — what counts is whether anyone takes part along the way. | Weekly report generated overnight, support emails routed as they arrive |

**Key question:** *Does a person take part along the way, or does no one take part until it's done?*

## The Matrix

Combining these two dimensions produces six distinct workflow archetypes:

| | **Augmented** (a person takes part along the way) | **Automated** (no one takes part until it's done) |
|---|---|---|
| **Deterministic** | You set every step and the AI carries each one out; a person reviews, guides, or approves during the run. | You set every step and the AI carries each one out, start to finish, with no one taking part. |
| **Guided** | The AI makes bounded decisions by your method (routing, choosing a tool, grading and sending work back); a person takes part during the run. | The AI makes the same bounded decisions with no one taking part until it's done — or until it escalates a case. |
| **Autonomous** | The AI plans its own steps toward a goal; a person approves at a gate or steers along the way. | The AI plans and keeps going until the goal is met, with no one taking part until the deliverable is complete. |

### The Six Archetypes

| Archetype | Autonomy | Involvement | Description | Example |
|-----------|----------|-------------|-------------|---------|
| **Deterministic + Augmented** | Deterministic | Augmented | Your steps; a person takes part along the way | Weekly status report: pull updates, the AI drafts, you review, then it saves |
| **Deterministic + Automated** | Deterministic | Automated | Your steps, run unattended | After each class, turn the transcript into a summary email and send it |
| **Guided + Augmented** | Guided | Augmented | Bounded AI decisions by your method; a person takes part | A browser assistant finds five LinkedIn prospects that fit your persona, working out how to navigate the site, while you stay in the session and review the list |
| **Guided + Automated** | Guided | Automated | Bounded AI decisions by your method, unattended | Support emails categorized and routed, unclear ones escalated; or three agents that draft playbook answers, grade them against your criteria, send failures back to be fixed, and publish the rest every hour |
| **Autonomous + Augmented** | Autonomous | Augmented | The AI plans its own steps; a person takes part | Research agents plan and write an article; you approve it before it publishes |
| **Autonomous + Automated** | Autonomous | Automated | The AI plans its own steps, with no one taking part | A monitoring agent that decides what to investigate when something changes, and alerts you |

### Worked Examples

These worked examples illustrate different matrix positions:

| Example | Archetype | Why |
|---------|-----------|-----|
| [Guided Prospect Research](../examples/deterministic-automation/) | **Guided + Augmented** | The AI judges each prospect against your persona criteria to decide who makes the list, and works out how to navigate LinkedIn to find them — decisions made by your method. You stay in the session and review the report. |
| [AI Collaborative](../examples/ai-collaborative/) | **Deterministic + Augmented** | Every run takes the same steps (research the people, research the company, draft the brief); the AI's research and writing shape what the brief says, never what happens next. You review and refine it along the way. |
| [Autonomous Agent](../examples/autonomous-agent/) | **Autonomous + Augmented** | You state the goal; the orchestrator decides which specialist agents to run and when. One human approval gate before publishing. |

## Choosing Your Archetype

### Two Questions

1. **What decides the next step — your instructions, the AI's judgment by your method, or the AI working from a goal?** → Determines your autonomy level (Deterministic / Guided / Autonomous)
2. **Does a person take part along the way, or does no one take part until it's done?** → Determines your involvement mode (Augmented / Automated)

*(A fourth autonomy value, **Human**, exists only when classifying individual steps during Design — a step a person performs with no AI. It never appears at the whole-workflow level, which is what this matrix classifies.)*

### Common Progressions

Most workflows evolve along predictable paths as you build confidence:

- **Deterministic + Augmented → Deterministic + Automated** — You start by running the process and reviewing output. Once you trust it, you schedule it to run unattended.
- **Guided + Augmented → Guided + Automated** — You watch the AI apply your method — routing, scoring, grading. Once its decisions prove reliable, you let it run with no one taking part, and review only the result or the cases it escalates.
- **Guided + Augmented → Autonomous + Augmented** — The work outgrows a fixed structure: you can describe the goal but no longer the steps. The AI plans them, and you keep a human review gate for high-stakes output.

:::tip[Start simple, upgrade when needed]
If you're new to AI workflows, start with **Deterministic + Augmented** — the lowest-risk archetype. Move to **Deterministic + Automated** once you trust the process. Explore **Guided** and **Autonomous** levels when you're ready to let the AI decide more of what happens next.
:::
## How This Maps to Framework Concepts

### Orchestration Mechanisms

The [orchestration mechanism](../design/#orchestration-mechanism) describes *who drives the workflow*. The matrix describes *how the AI and human interact*. They're complementary:

| Orchestration Mechanism | Typical Archetypes |
|------------------------|-------------------|
| Skill | Deterministic or Guided, either involvement mode |
| Agent | Guided or Autonomous, either involvement mode |

### Architecture Patterns

The seven [workflow architecture patterns](../../patterns/workflow-architecture/) provide implementation blueprints within each archetype:

| Archetype | Common Architecture Patterns |
|-----------|------------------------------|
| Deterministic | Augmented LLM, Prompt Chaining |
| Guided | Prompt Chaining, Routing, Evaluator-Optimizer |
| Autonomous | Orchestrator-Workers, Autonomous Agents |

## Related

- [AI Workflow Framework](../) — the full seven-step methodology
- [Design Your AI Workflow](../design/) — assess autonomy, choose an orchestration mechanism, and map building blocks
- [Build Workflows](../build/) — worked examples across the matrix
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/) — implementation blueprints for each pattern
