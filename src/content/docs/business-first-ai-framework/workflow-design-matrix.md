---
title: AI Workflow Design Matrix
description: A 3x2 matrix combining autonomy level (Deterministic, Guided, Autonomous) with human involvement (Augmented, Automated) to define six workflow archetypes — use it to classify any AI workflow and choose the right design.
---Every AI workflow can be described by two dimensions: **how much decision-making the AI has** and **whether a human is in the loop during execution**. These two dimensions combine into a 3x2 matrix of six workflow archetypes — a shared vocabulary for classifying, comparing, and designing AI workflows.

A third dimension — **Lens** — determines the scope of your analysis:

- **Individual** — Workflows scoped to one person's trigger-to-deliverable flow. Focus: personal productivity, task automation, quality improvement.
- **Organizational** — Workflows scoped to an end-to-end business process, potentially spanning multiple roles. Focus: value chain optimization, cross-functional efficiency, strategic outcomes.

The lens doesn't change the matrix — it changes what you're analyzing. An individual-lens audit surfaces your personal pain points; an organizational-lens audit surfaces value chain processes tied to business objectives. Both produce candidates classified on the same Autonomy x Involvement matrix.

## Two Dimensions Define Every AI Workflow

### Dimension 1: Autonomy — How Much Decision-Making Does the AI Have?

Autonomy describes how much latitude the AI has to make decisions during execution. This is about the AI's role, not the human's.

| Level | AI's Role | What It Looks Like | Example |
|-------|-----------|-------------------|---------|
| **Deterministic** | Follows fixed rules — no decisions, no judgment | Input → predefined steps → structured output. Same input produces same output every time. | Format a report from a template, extract data from a form |
| **Guided** | Makes bounded decisions within guardrails | AI chooses *how* to accomplish a step, but the human sets direction and reviews output. | Draft an email based on meeting notes, research a topic and summarize findings |
| **Autonomous** | Plans, decides, and adapts independently | AI determines what to do, uses tools, adjusts its approach based on what it finds. | Research agent that finds sources, evaluates quality, and produces a report end-to-end |

**Key question:** *How much does the AI decide on its own?*

- **Deterministic** — nothing; it follows your script exactly
- **Guided** — some; it makes choices within boundaries you set
- **Autonomous** — a lot; it plans its own approach and adapts

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
| **Deterministic** | Human triggers a fixed sequence and reviews output before it's used. AI follows rules; human confirms results. | Fixed sequence runs on a schedule or trigger with no human involvement. Same input → same output, every time. |
| **Guided** | Human and AI collaborate — AI researches, drafts, or analyzes; human steers, refines, and decides. | AI handles research, drafting, or analysis on its own, applying bounded judgment. Human reviews only the final output. |
| **Autonomous** | AI plans and executes multi-step work; human reviews at defined checkpoints before the workflow continues. | AI runs a full pipeline end-to-end — plans, executes, adapts — with no human intervention until the deliverable is complete. |

### The Six Archetypes

| Archetype | Autonomy | Involvement | Description | Example |
|-----------|----------|-------------|-------------|---------|
| **Deterministic + Augmented** | Deterministic | Augmented | Human triggers a rules-based process and confirms results before use | Run a data extraction template, review output, then forward |
| **Deterministic + Automated** | Deterministic | Automated | Rules-based process runs unattended on a trigger or schedule | Nightly report formatting, scheduled form processing |
| **Guided + Augmented** | Guided | Augmented | AI drafts, researches, or analyzes; human steers and decides in real time | Meeting prep research, co-writing, competitive analysis |
| **Guided + Automated** | Guided | Automated | AI applies bounded judgment independently; human reviews the final output | Draft personalized outreach emails overnight for morning review |
| **Autonomous + Augmented** | Autonomous | Augmented | AI executes a multi-step pipeline with human approval gates | Multi-agent research → write → edit pipeline with a review checkpoint |
| **Autonomous + Automated** | Autonomous | Automated | AI runs a full autonomous pipeline end-to-end without human involvement | Continuous monitoring agent that detects, analyzes, and alerts |

### Worked Examples

These three worked examples from the [Build](build/index.mdx) section illustrate different matrix positions:

| Example | Archetype | Why |
|---------|-----------|-----|
| [Deterministic Automation](examples/deterministic-automation.mdx) | **Deterministic + Automated** | Fixed rules, structured input/output, runs the same way every time with no human steering |
| [AI Collaborative](examples/ai-collaborative.mdx) | **Guided + Augmented** | AI researches and drafts; human reviews, refines, and decides what to use |
| [Autonomous Agent](examples/autonomous-agent.mdx) | **Autonomous + Augmented** | Multi-agent pipeline executes autonomously with one human review gate before publishing |

## Choosing Your Archetype

### Two Questions

1. **How much should the AI decide on its own?** → Determines your autonomy level (Deterministic / Guided / Autonomous)
2. **Does a human need to be involved during the run?** → Determines your involvement mode (Augmented / Automated)

### Common Progressions

Most workflows evolve along predictable paths as you build confidence:

- **Deterministic + Augmented → Deterministic + Automated** — You start by running the process and reviewing output. Once you trust it, you schedule it to run unattended.
- **Guided + Augmented → Guided + Automated** — You collaborate with AI on drafts and research. Once the AI consistently produces good output, you let it run independently and review only the final result.
- **Guided + Augmented → Autonomous + Augmented** — The workflow grows more complex. You add tool access and multi-step reasoning, but keep a human review gate for high-stakes output.

:::tip[Start simple, upgrade when needed]
If you're new to AI workflows, start with **Deterministic + Augmented** — the lowest-risk archetype. Move to **Deterministic + Automated** once you trust the process. Explore **Guided** and **Autonomous** levels when you're ready for more AI decision-making.
:::
## How This Maps to Framework Concepts

### Orchestration Mechanisms

The [orchestration mechanism](design.md#orchestration-mechanism) describes *who drives the workflow*. The matrix describes *how the AI and human interact*. They're complementary:

| Orchestration Mechanism | Typical Archetypes |
|------------------------|-------------------|
| Prompt | Deterministic + Augmented, Deterministic + Automated |
| Skill-Powered Prompt | Deterministic or Guided, either involvement mode |
| Agent | Guided or Autonomous, either involvement mode |

### Architecture Patterns

The seven [workflow architecture patterns](../patterns/workflow-architecture/index.md) provide implementation blueprints within each archetype:

| Archetype | Common Architecture Patterns |
|-----------|------------------------------|
| Deterministic | Augmented LLM, Prompt Chaining |
| Guided | Prompt Chaining, Routing, Evaluator-Optimizer |
| Autonomous | Orchestrator-Workers, Autonomous Agents |

## Related

- [Business-First AI Framework](index.md) — the full seven-step methodology
- [Design Your AI Workflow](design.md) — assess autonomy, choose an orchestration mechanism, and map building blocks
- [Build Workflows](build/index.mdx) — worked examples across the matrix
- [Workflow Architecture Patterns](../patterns/workflow-architecture/index.md) — implementation blueprints for each pattern
