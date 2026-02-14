---
title: Business-First AI Framework
description: A three-step methodology for finding where AI fits in your business, deconstructing workflows into building blocks, and turning those outputs into working AI workflows
---

# Business-First AI Framework

## The Problem

Most AI adoption starts with the technology — "we have ChatGPT, where should we use it?" This leads to shallow adoption and misses the workflows where AI creates real leverage. And even when people identify the right workflow, there's a gap between the idea and making it real — without a repeatable process to follow, they get stuck and stop. The Business-First AI Framework closes that gap: audit your workflows, identify where AI creates the most value, deconstruct those workflows into building blocks, then build.

## The Framework

Three steps, each with a structured process:

### Step 1: Discover Workflows

Find which workflows are candidates for AI.

Before you can apply AI to anything, you need to know *where* it fits. Step 1 is a structured audit of your workflows that produces a prioritized list of opportunities across three categories:

- **Deterministic Workflows** — Repeatable processes with clear inputs and outputs that AI can execute reliably with little supervision
- **Collaborative AI** — Tasks where you and AI work together in real time (drafting, brainstorming, reviewing)
- **Autonomous Agents** — Goal-driven workflows where AI plans and executes steps autonomously

The audit uses a three-step process: scan what AI already knows about your work, interview you to fill gaps, then produce a categorized report with specific opportunities and actionable first steps.

**Two ways to run Step 1:**

- **Any AI tool** — Copy the [Discover AI Workflow Opportunities](discover.md) prompt into Claude, ChatGPT, Gemini, or M365 Copilot
- **Claude platform** — Use the `discovering-workflows` skill from the [Business-First AI plugin](../plugins/business-first-ai.md) in Claude Code, Claude.ai, or Cowork ([setup guide](../plugins/using-plugins.md))

---

### Step 2: Deconstruct Workflows

Give your workflow clear structure through deep decomposition.

Once you've identified a workflow worth automating, Step 2 deconstructs it so you understand every step, decision point, and dependency. You describe your workflow — rough and incomplete is fine — and the model interviews you to surface every hidden step, data handoff, and failure mode.

The deconstruction uses the **five-question framework** to break down each step:

1. Is this step actually multiple steps bundled together?
2. Are there decision points, branches, or quality gates?
3. What data flows in and out?
4. What context, documents, or reference materials does this step need?
5. What happens when this step fails?

The deliverable is a **Workflow Definition** — a structured breakdown of your workflow into refined steps, with decision points, data flows, context needs, and failure modes captured for every step. The context needs and failure modes captured here directly inform design decisions in Step 3.

**Two ways to run Step 2:**

- **Any AI tool** — Copy the [Deconstruct Workflows](deconstruct/index.md) prompt into Claude, ChatGPT, Gemini, or M365 Copilot
- **Claude platform** — Use the `workflow-deconstructor` agent or individual skills from the [Business-First AI plugin](../plugins/business-first-ai.md) in Claude Code, Claude.ai, or Cowork ([setup guide](../plugins/using-plugins.md))

---

### Step 3: Build Workflows

Design your AI implementation, construct the components, and run the workflow.

Step 2 produces a Workflow Definition — the analysis. Step 3 is where that analysis becomes a working AI workflow through three parts:

1. **3.1: Design** — Choose an execution pattern (Prompt → Skill-Powered Prompt → Single Agent → Multi-Agent), classify each step on the autonomy spectrum, map to AI building blocks, identify skill candidates, and configure agents when needed. Produces an AI Building Block Spec — a platform-agnostic blueprint.

2. **3.2: Construct** — Build only what your execution pattern requires. The AI Building Block Spec tells you exactly which components to create — context, skills, prompts, agents, MCP connections — and in what order.

3. **3.3: Run** — Execute the workflow on a real scenario, then iterate based on results.

The [Build Workflows](build/index.md) section includes:

- **3.1: Design** — execution pattern spectrum, autonomy classification, building block mapping, skill candidate identification, agent configuration
- **Pattern-specific Construct paths** — each execution pattern shows only the steps that apply
- **Six building block guides** — Context, Projects, Skills, Prompt, Agents, MCP
- **Three worked examples** across the autonomy spectrum — deterministic automation, collaborative workflows, and fully autonomous multi-agent pipelines

**[See Step 3 — Build Workflows](build/index.md)**

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

### Seven AI Building Blocks

| Block | What It Is |
|-------|-----------|
| **Model** | The AI engine that processes inputs and generates outputs |
| **Prompt** | A well-crafted instruction that tells the model what to do |
| **Context** | Background information, reference docs, or examples the model needs |
| **Skill** | A reusable routine the model can invoke — give it inputs, it follows a defined process, it produces consistent outputs |
| **Agent** | An autonomous AI that plans, uses tools, and executes multi-step work |
| **MCP (Model Context Protocol)** | A connector that lets AI access external tools, services, or databases on your behalf |
| **Project** | A persistent workspace grouping prompts, context, skills, and agents |

For detailed definitions and cross-platform examples, see [Agentic Building Blocks](../agentic-building-blocks/index.md).

### Six Use Case Primitives

When classifying opportunities from Step 1, it helps to know what **type** of AI work each one involves. The [six use case primitives](../use-cases/index.md) — Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, and Automation — provide a classification system for the opportunities you discover.

### Autonomy Spectrum

| Level | Description |
|-------|-------------|
| **Human** | Requires human judgment, creativity, or physical action |
| **Deterministic** | Follows fixed rules; AI executes reliably with minimal supervision |
| **Semi-Autonomous** | AI does most of the work; human reviews at key checkpoints |
| **Autonomous** | AI executes end-to-end, including decisions and tool use |

### Execution Pattern Spectrum

Every AI workflow falls somewhere on this spectrum. The right pattern depends on what your workflow actually needs:

| Pattern | Description | Signals |
|---------|-------------|---------|
| **Prompt** | Single self-contained prompt, all logic inline | Sequential steps, human drives the process and provides all inputs |
| **Skill-Powered Prompt** | Prompt invoking reusable skills | Repeatable sub-routines, moderate complexity |
| **Single Agent** | One autonomous agent with tool access | Tool use, autonomous decisions, multi-step reasoning |
| **Multi-Agent** | Specialized agents in a pipeline | Multiple expertise domains, parallel execution, review gates |

## Getting Started

1. **Start with the [Opportunity Finder](discover.md)** to identify your best candidates
2. **Pick your highest-impact opportunity** — don't try to pursue everything at once
3. **Run it through the [Deconstruction process](deconstruct/index.md)** to break it into discrete steps
4. **[Design](build/design.md)** your AI workflow — choose an execution pattern, classify steps, map building blocks
5. **[Build](build/index.md)** the components your execution pattern requires — context, skills, prompts, agents, MCP connections
6. **Test on a real scenario** — paste the generated prompt into any AI tool and run the workflow
7. **Iterate** — refine the prompt, build additional skills, or add agents based on what works

## Tools

For Claude platform users (Claude Code, Claude.ai, or Cowork), the [Business-First AI plugin](../plugins/business-first-ai.md) implements all three steps as executable skills you can run interactively:

```bash
/plugin install business-first-ai@handsonai
```
