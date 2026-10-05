---
title: AI Workflow Design Matrix
description: "A 3x2 matrix combining autonomy (who decides the steps: Deterministic, Guided, Autonomous) with human involvement (Augmented, Automated) for any AI workflow."
---Every AI workflow can be described by two dimensions: **who decides the steps** and **whether a human is in the loop during execution**. These two dimensions combine into a 3x2 matrix of six workflow archetypes — a shared vocabulary for classifying, comparing, and designing AI workflows.

A third dimension — **Lens** — determines the scope of your analysis:

- **Individual** — Workflows scoped to one person's trigger-to-deliverable flow. Focus: personal productivity, task automation, quality improvement.
- **Organizational** — Workflows scoped to an end-to-end business process, potentially spanning multiple roles. Focus: value chain optimization, cross-functional efficiency, strategic outcomes.

The lens doesn't change the matrix — it changes what you're analyzing. An individual-lens audit surfaces your personal pain points; an organizational-lens audit surfaces value chain processes tied to business objectives. Both produce candidates classified on the same Autonomy x Involvement matrix.

## Two Dimensions Define Every AI Workflow

### Dimension 1: Autonomy — How Much Does the AI Decide on Its Own?

**Autonomy level: how much does the AI decide on its own? Tell by looking at who decides the steps.** This is about who sets the path through the work, not how much writing or thinking the AI does inside a step.

| Level | Who decides the steps | Test | Example |
|-------|----------------------|------|---------|
| **Deterministic** | You set the steps, their order, and the tool each one uses. The path is the same every run. The AI may still write, summarize, or analyze inside a step. | Could you draw the whole flow in advance, with no "it depends" arrows? | Pull this week's project updates, have the AI draft a status report, save it to the shared folder |
| **Guided** | You set the structure. The AI makes bounded choices about the path within limits you define: which tool to use, which branch to take, whether to retry or skip a step, or how to navigate a system. | Is there a choice point where the AI, not you, picks the next move from options you allowed? | Sort incoming support emails by category, send each to the right queue, and escalate the unclear ones; a browser assistant that works out how to navigate a website to find what you asked for |
| **Autonomous** | The AI plans its own steps toward a goal and changes course based on what it finds. | Could you only describe the goal, not the steps? | Research agents that decide what to investigate, follow what they find, and write an article |

**Tiebreak — path or content?** If the AI's choice changes which step runs next or which tool is used, it is a path decision and counts toward Guided. If it only changes what a step produces (the wording, what to include, the summary), it does not count.

A branch that your own rule decides is still yours. A fixed threshold ("flag anything under 80% confidence") or a pass/fail check where the AI grades the output against your criteria, and your rule says pass continues and fail stops, does not make a workflow Guided. It turns Guided when the AI picks among next moves you allowed: which queue, which tool, retry or skip.

**Autonomy is not about content risk.** Whether a person should check what the AI produced is answered by the involvement mode (Augmented puts a person in the run) and by evaluation in [Test](../test/), not by the autonomy level. A Deterministic workflow can write a client email that a person must approve; that makes it Deterministic + Augmented, not Guided.

### Dimension 2: Human Involvement — Is a Human in the Loop During Execution?

Human involvement describes whether a human participates while the workflow is running — not before (design) or after (review), but during.

| Mode | Human's Role | What It Looks Like | Example |
|------|-------------|-------------------|---------|
| **Augmented** | Human is in the loop — reviews, steers, or decides at key points | AI pauses for human input, feedback, or approval before continuing. Human and AI collaborate in real time. | Co-writing a document, reviewing AI research before it continues |
| **Automated** | AI runs solo — human reviews only the final output | Workflow executes end-to-end without human intervention during the run. May be triggered manually or on a schedule. | Weekly report generated overnight, prospect list compiled on a schedule |

**Key question:** *Does a human participate during the workflow run, or only see the final result?*

## The Matrix

Combining these two dimensions produces six distinct workflow archetypes:

| | **Augmented** (human in the loop) | **Automated** (AI runs solo) |
|---|---|---|
| **Deterministic** | You set every step and its tool; the AI writes or analyzes inside the steps; a person checks or approves at a pause before the result is used. | You set every step and its tool; the run goes start to finish on a trigger or schedule with no person in it. |
| **Guided** | You set the structure; the AI picks the next move at choice points you allowed (tool, branch, retry, navigation); a person reviews during the run. | You set the structure; the AI makes the same bounded path choices unattended. A person sees only the result, or the cases it escalates. |
| **Autonomous** | The AI plans its own steps toward a goal and changes course as it goes; a person approves at a gate before the workflow continues. | The AI plans and adapts end-to-end, with no person in the run until the deliverable is complete. |

### The Six Archetypes

| Archetype | Autonomy | Involvement | Description | Example |
|-----------|----------|-------------|-------------|---------|
| **Deterministic + Augmented** | Deterministic | Augmented | Fixed path; a person reviews or approves during the run | Weekly status report: pull updates, the AI drafts, you review, then it saves |
| **Deterministic + Automated** | Deterministic | Automated | Fixed path that runs unattended on a trigger or schedule | Three agents that draft, check, and publish answers every hour in a fixed order |
| **Guided + Augmented** | Guided | Augmented | The AI makes bounded path choices; a person reviews during the run | A browser assistant finds five LinkedIn prospects, working out its own navigation; you review the list |
| **Guided + Automated** | Guided | Automated | The AI makes bounded path choices unattended | Support emails sorted by category and routed to the right queue, unclear ones escalated, no one watching |
| **Autonomous + Augmented** | Autonomous | Augmented | The AI plans its own steps; a person approves at a gate | Research agents plan and write an article; you approve it before it publishes |
| **Autonomous + Automated** | Autonomous | Automated | The AI plans its own steps end-to-end with no person in the run | A monitoring agent that decides what to investigate when something changes, and alerts you |

### Worked Examples

These worked examples illustrate different matrix positions:

| Example | Archetype | Why |
|---------|-----------|-----|
| [Guided Prospect Research](../examples/deterministic-automation/) | **Guided + Augmented** | The criteria and report template are fixed, but the AI works out how to navigate LinkedIn to find matches — a path choice. You start the run and review the report. |
| [AI Collaborative](../examples/ai-collaborative/) | **Deterministic + Augmented** | The steps are fixed (research the people, research the company, draft the brief); the AI's judgment shapes what the brief says, not which step runs. You review and refine it. |
| [Autonomous Agent](../examples/autonomous-agent/) | **Autonomous + Augmented** | The orchestrator chooses which specialist agents to run and when; you only state the goal. One human approval gate before publishing. |

## Choosing Your Archetype

### Two Questions

1. **Who decides the steps — you, the AI at choice points you allowed, or the AI from a goal?** → Determines your autonomy level (Deterministic / Guided / Autonomous)
2. **Does a human need to be involved during the run?** → Determines your involvement mode (Augmented / Automated)

*(A fourth autonomy value, **Human**, exists only when classifying individual steps during Design — a step a person performs with no AI. It never appears at the whole-workflow level, which is what this matrix classifies.)*

### Common Progressions

Most workflows evolve along predictable paths as you build confidence:

- **Deterministic + Augmented → Deterministic + Automated** — You start by running the process and reviewing output. Once you trust it, you schedule it to run unattended.
- **Guided + Augmented → Guided + Automated** — You watch the AI make its choices at each choice point. Once those choices prove reliable, you let it run unattended and review only the result, or the cases it escalates.
- **Guided + Augmented → Autonomous + Augmented** — The work outgrows a fixed structure: you can describe the goal but no longer the steps. The AI plans them, and you keep a human review gate for high-stakes output.

:::tip[Start simple, upgrade when needed]
If you're new to AI workflows, start with **Deterministic + Augmented** — the lowest-risk archetype. Move to **Deterministic + Automated** once you trust the process. Explore **Guided** and **Autonomous** levels when you're ready to let the AI choose more of the path.
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
