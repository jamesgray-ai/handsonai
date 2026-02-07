---
title: Business-First AI Framework
description: A three-phase methodology for finding where AI fits in your business, deconstructing workflows into building blocks, and turning those outputs into working AI workflows
---

# Business-First AI Framework

## The Problem

Most AI adoption starts with the technology — "we have ChatGPT, where should we use it?" This leads to shallow adoption and misses the workflows where AI creates real leverage. And even when people identify the right workflow, there's a gap between the idea and making it real — without a repeatable process to follow, they get stuck and stop. The Business-First AI Framework closes that gap: audit your workflows, identify where AI creates the most value, deconstruct those workflows into building blocks, then build.

## The Framework

Three phases, each with a structured process:

### Phase 1: Discover

Find which workflows are candidates for AI.

Before you can apply AI to anything, you need to know *where* it fits. Phase 1 is a structured audit of your workflows that produces a prioritized list of opportunities across three categories:

- **Deterministic Workflows** — Repeatable processes with clear inputs and outputs that AI can execute reliably with little supervision
- **Collaborative AI** — Tasks where you and AI work together in real time (drafting, brainstorming, reviewing)
- **Autonomous Agents** — Goal-driven workflows where AI plans and executes steps autonomously

The audit uses a three-step process: scan what AI already knows about your work, interview you to fill gaps, then produce a categorized report with specific opportunities and actionable first steps.

**Two ways to run Phase 1:**

- **Any AI tool** — Copy the [Discover AI Workflow Opportunities](discover.md) prompt into Claude, ChatGPT, Gemini, or M365 Copilot
- **Claude platform** — Use the `finding-ai-opportunities` skill from the [Business-First AI plugin](../plugins/business-first-ai.md) in Claude Code, Claude.ai, or Cowork ([setup guide](../plugins/using-plugins.md))

---

### Phase 2: Deconstruct

Give your workflow clear structure — then identify the building blocks to turn it into a working AI workflow.

Once you've identified a workflow worth automating, Phase 2 deconstructs it so you understand every step, decision point, and dependency. With that structure in place, you map each step to the right AI building blocks. The three-step pipeline:

1. **Workflow Definition** — Interactively decompose the workflow into refined steps, surfacing hidden sub-steps, decision points, data flows, context needs, and failure modes
2. **AI Building Blocks** — Classify each step on the autonomy spectrum (Human → Deterministic → Semi-Autonomous → Autonomous) and map to AI building blocks
3. **Prompt & Skill Specs** — Generate a ready-to-use Baseline Workflow Prompt (a prompt you can paste into any AI tool to run the workflow) and Skill Specs

The deconstruction uses the **five-question framework** to break down each step:

1. Is this step actually multiple steps bundled together?
2. Are there decision points, branches, or quality gates?
3. What data flows in and out?
4. What context, documents, or reference materials does this step need?
5. What happens when this step fails?

Each step gets mapped to one or more of the **six AI building blocks**: Prompt, Context, Skill, Agent, MCP, or Project.

**Two ways to run Phase 2:**

- **Any AI tool** — Copy the [Deconstruct Workflows](deconstruct/index.md) prompts into Claude, ChatGPT, Gemini, or M365 Copilot
- **Claude platform** — Use the `workflow-deconstructor` agent or individual deconstruction skills from the [Business-First AI plugin](../plugins/business-first-ai.md) in Claude Code, Claude.ai, or Cowork ([setup guide](../plugins/using-plugins.md))

---

### Phase 3: Build

Turn your deconstruction outputs into working AI workflows.

Phase 2 produces two actionable deliverables: a Baseline Workflow Prompt you can run immediately, and Skill Specs that tell you what to build next. Phase 3 is where those become real.

The [Build Workflows](build/index.md) examples show three worked examples across the autonomy spectrum — from deterministic automation to collaborative workflows to fully autonomous multi-agent pipelines. Each includes working building blocks you can install and study.

This section will grow with guides on building prompts, skills, agents, and multi-agent workflows from deconstruction output.

**[See Phase 3 — Build Workflows](build/index.md)**

---

## Key Concepts

Quick reference for the framework's vocabulary:

### Three Opportunity Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Deterministic Workflow** | Repeatable process AI executes with minimal supervision | Formatting reports, processing forms |
| **Collaborative AI** | Human and AI work together in real time | Co-writing, brainstorming, code review |
| **Autonomous Agent** | AI plans and executes steps autonomously | Competitor monitoring, research → report pipelines |

### Five-Question Framework

Used to decompose each workflow step:

1. **Discrete steps** — Is this one step or multiple bundled together?
2. **Decision points** — Any if/then branches, quality gates, or judgment calls?
3. **Data flows** — What goes in? What comes out? Where from and where to?
4. **Context needs** — What documents, files, or reference materials are required?
5. **Failure modes** — What happens when this step fails?

### Six AI Building Blocks

| Block | What It Is |
|-------|-----------|
| **Prompt** | A well-crafted instruction that tells the model what to do |
| **Context** | Background information, reference docs, or examples the model needs |
| **Skill** | A reusable, parameterized routine the model can invoke |
| **Agent** | An autonomous AI that plans, uses tools, and executes multi-step work |
| **MCP (Model Context Protocol)** | A connector that lets AI access external tools, services, or databases on your behalf |
| **Project** | A persistent workspace grouping prompts, context, skills, and agents |

### Autonomy Spectrum

| Level | Description |
|-------|-------------|
| **Human** | Requires human judgment, creativity, or physical action |
| **Deterministic** | Follows fixed rules; AI executes reliably with minimal supervision |
| **Semi-Autonomous** | AI does most of the work; human reviews at key checkpoints |
| **Autonomous** | AI executes end-to-end, including decisions and tool use |

## Getting Started

1. **Start with the [Opportunity Finder](discover.md)** to identify your best candidates
2. **Pick your highest-impact opportunity** — don't try to pursue everything at once
3. **Run it through the [Deconstruction process](deconstruct/index.md)** to break it into AI building blocks
4. **Test the Baseline Prompt** on a real scenario — paste the generated prompt into any AI tool and run the workflow
5. **Build skills in priority order** from the Skill Specs — each skill you build replaces steps in the baseline prompt, making the workflow progressively more automated

## Tools

For Claude platform users (Claude Code, Claude.ai, or Cowork), the [Business-First AI plugin](../plugins/business-first-ai.md) implements all three phases as executable skills you can run interactively:

```bash
/plugin install business-first-ai@handsonai
```
