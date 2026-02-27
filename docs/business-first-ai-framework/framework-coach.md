---
title: Framework Coach Guide
description: A structured guide for AI tools to coach users through the Business-First AI Framework — compact methodology overview with links to detailed documentation.
---

# Business-First AI Framework — Coach Guide

This document is designed for AI tools (Claude, ChatGPT, Gemini, M365 Copilot) to use as a coaching reference when guiding users through the Business-First AI Framework. It provides the methodology overview, decision trees, and links to detailed documentation in raw Markdown format.

For the coaching prompt and setup instructions, see [Use AI as Your Coach](coach.md).

---

## Framework Overview

The Business-First AI Framework is a three-step methodology for finding where AI fits in your business, breaking down workflows into structured components, and building working AI workflows.

```
Step 1: Analyze → Step 2: Deconstruct → Step 3: Build (3.1 Design → 3.2 Construct → 3.3 Run)
```

Each step produces a specific deliverable that feeds into the next:

| Step | What happens | Deliverable | File |
|------|-------------|-------------|------|
| **1. Analyze** | Audit workflows, identify AI opportunities | Opportunity Report + Workflow Candidates | `ai-opportunity-report.md` |
| **2. Deconstruct** | Deep-dive a specific workflow using the 5-question framework | Workflow Definition | `[name]-definition.md` |
| **3.1 Design** | Choose execution pattern, classify steps, map building blocks | AI Building Block Spec | `[name]-building-block-spec.md` |
| **3.2 Construct** | Build the components your pattern requires | Platform artifacts + Run Guide | Context, skills, agents, API/SDK code, configs |
| **3.3 Run** | Get the workflow running, test on a real scenario, iterate | Refined workflow | `[name]-run-guide.md` |

---

## Step 1: Analyze Workflows

**Purpose:** Find which of your workflows are candidates for AI automation.

**Process:** The AI scans what it knows about the user, interviews them about their work (role, repetitive tasks, pain points, multi-step processes), then produces a categorized opportunity report.

**Three opportunity categories:**

| Category | Description | Example |
|----------|-------------|---------|
| **Deterministic Workflow** | Repeatable process AI executes with minimal supervision | Formatting reports, processing forms |
| **Collaborative AI** | Human and AI work together in real time | Co-writing, brainstorming, code review |
| **Autonomous Agent** | AI plans and executes steps autonomously | Research pipelines, monitoring systems |

**Output:** An opportunity report with a report header, summary table, top recommendations, detailed cards for each opportunity, and a workflow candidate summary with structured metadata (name, description, trigger, deliverable, category, priority, reasoning).

**Coaching guidance:**

- If the user doesn't know where to start, run Step 1 first
- If they already know which workflow to work on, skip to Step 2
- Encourage them to pick one workflow from each category to start
- Start with Collaborative AI if they're new to AI (lowest risk, easiest to try)

---

## Step 2: Deconstruct Workflows

**Purpose:** Break down a specific workflow into discrete steps with full detail on decision points, data flows, context needs, and failure modes.

**Process:** Interactive deep-dive using the 5-question framework applied to every step:

1. **Discrete steps** — Is this actually multiple steps bundled together?
2. **Decision points** — Any if/then branches, quality gates, or judgment calls?
3. **Data flows** — What goes in? What comes out? Where from and where to?
4. **Context needs** — What documents, files, or reference materials are required?
5. **Failure modes** — What happens when this step fails?

**Scope check (critical):** Before starting the deep dive, verify the workflow has exactly one trigger and one deliverable. Test with four diagnostic questions:

1. Does it have multiple independent starting points? → Separate workflows
2. Does it produce distinct outputs at different points? → Workflow boundary
3. Do parts run on different schedules? → Likely separate workflows
4. Would it expand to 15+ refined steps? → May be multiple workflows

If multiple workflows are detected, help the user identify and separate them, then pick one to deconstruct.

**Output:** A Workflow Definition with scenario metadata, refined steps (each with action, sub-steps, decision points, data in/out, context needs, failure modes), step sequence/dependencies, and a context shopping list.

**Coaching guidance:**

- Most workflows expand from 5-8 rough steps to 12-20 refined steps
- Encourage messy, incomplete descriptions — the process refines them
- Push for specific context artifacts, not vague "domain knowledge"
- Ask for existing AI instructions if AI is already being used at any step
- The Workflow Definition should be saved as `[name]-definition.md`
- After completing, register the workflow in the AI Registry if using Notion

---

## Step 3: Build Workflows

Build has three parts: **3.1 Design**, **3.2 Construct**, and **3.3 Run**.

### 3.1: Design

**Purpose:** Decide *how* the workflow should be built before building it.

**Process:** Take the Workflow Definition and make five design decisions:

1. **Architecture approach** — No-code (build in a platform UI) or Code-first (build with APIs and SDKs). Recommended based on integration needs, deployment requirements, and technical comfort.
2. **Architecture decisions** — Confirm the platform, then extract tool integrations, trigger/schedule, and constraints from the Workflow Definition. One question, then a confirmation block.
3. **Execution pattern** — How complex does the AI implementation need to be?
4. **Autonomy classification** — How much AI assistance does each step need?
5. **Building block mapping** — What specific AI components does each step require?

**Execution Pattern Spectrum:**

| Pattern | Description | Signals |
|---------|-------------|---------|
| **Prompt** | Single self-contained prompt, all logic inline | Sequential steps, human drives the process and provides all inputs |
| **Skill-Powered Prompt** | Prompt invoking reusable skills | Repeatable sub-routines, moderate complexity |
| **Single Agent** | One autonomous agent with tool access | Tool use, autonomous decisions, multi-step reasoning |
| **Multi-Agent** | Specialized agents in a pipeline | Multiple expertise domains, parallel execution, review gates |

**Five decision questions for choosing a pattern:**

1. Does the workflow require tool use? (web, files, APIs) → If yes, need at least Single Agent
2. Does it require autonomous decision-making? → If yes, need at least Single Agent
3. Are there steps with complex, reusable logic? → Skill candidates
4. Does it span multiple expertise domains? → Consider Multi-Agent
5. Would it benefit from parallel execution or review gates? → Multi-Agent

**Autonomy spectrum for each step:**

| Level | Description |
|-------|-------------|
| **Human** | Requires human judgment, creativity, or physical action |
| **Deterministic** | Follows fixed rules; AI executes reliably with minimal supervision |
| **Semi-Autonomous** | AI does most of the work; human reviews at key checkpoints |
| **Autonomous** | AI executes end-to-end, including decisions and tool use |

**Ten AI Building Blocks:**

| Block | What It Is |
|-------|-----------|
| **Model** | The AI engine that processes inputs and generates outputs |
| **Prompt** | A well-crafted instruction that tells the model what to do |
| **Context** | Background information, reference docs, or examples the model needs |
| **Project** | A persistent workspace grouping prompts, context, skills, and agents |
| **Memory** | Accumulated knowledge from past interactions — preferences, decisions, and patterns the AI retains |
| **Skill** | A reusable routine — give it inputs, it follows a defined process, produces consistent outputs |
| **Agent** | An autonomous AI that plans, uses tools, and executes multi-step work |
| **MCP** | A connector giving AI access to external tools, APIs, databases |
| **API** | Programmatic interfaces for accessing AI models and cloud services |
| **SDK** | Frameworks and toolkits for building AI workflows in code |

**Output:** An AI Building Block Spec with execution pattern, autonomy classifications, building block mapping, skill candidates (with generation-ready detail), agent configurations (when applicable), context inventory, and implementation order.

**Two phases, two modes:** Design has two distinct phases:

1. **Collaborative decisions (normal conversation)** — The model confirms the platform, extracts architecture decisions from the Workflow Definition, presents a confirmation block, then recommends an execution pattern and interaction mode. This is back-and-forth.
2. **Plan the spec (plan mode)** — Once architecture decisions and execution pattern are locked in, the user activates plan mode. The model then plans the full AI Building Block Spec — classifying steps, mapping building blocks, identifying skill candidates, and documenting agent blueprints.

After the model produces the spec, the user reviews and approves the AI Building Block Spec before moving to Construct.

**Coaching guidance:**

- Most workflows start as Prompt or Skill-Powered Prompt — start simple
- The AI Building Block Spec is platform-agnostic — it works on any AI platform
- Implementation order: quick wins first, complex agent steps last
- After confirming architecture decisions and execution pattern, prompt the user to activate plan mode before the model proceeds to classify steps and map building blocks
- After the user approves the AI Building Block Spec, prompt them to exit plan mode before starting Construct

### 3.2: Construct

**Purpose:** Build only what your execution pattern requires.

Each pattern has a specific build path — users follow only the steps that apply to their pattern:

| Pattern | Build steps |
|---------|-------------|
| **Prompt** | Create context → Set up project (optional) → Generate prompt → Run |
| **Skill-Powered Prompt** | Create context → Set up project (optional) → Build skills → Generate prompt → Run |
| **Single Agent** | Create context → Build skills → Connect MCP → Build agent → Run |
| **Multi-Agent** | Create context → Build skills → Connect MCP → Build agents → Build orchestrator → Run |

**Building blocks:** See [3.2: Construct](https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/construct.md) for the full guide — covers all building blocks (Context, Projects, Skills, Prompt, Agents, MCP) and what the user needs to do themselves (gathering context, configuring MCP connections, operationalizing agents on their platform).

**Operational rhythm:** After creating each building block: **test it, register it** (in the AI Registry), **commit it** (to GitHub).

**Coaching guidance:**

- Point users to the specific build path for their execution pattern
- Don't overwhelm with all options — show only what applies
- Skills: build only for steps with complex, reusable logic
- Generated prompts should be self-contained — paste and run on any AI platform

### 3.3: Run

**Purpose:** Test the workflow on a real scenario and iterate.

**Process:** Run → evaluate → adjust → run again. Most workflows need 2-4 iterations.

**What to evaluate:**

- Did the output match expectations?
- Were any steps skipped or misunderstood?
- Was the output specific to the business or generic?

**Troubleshooting:**

| Problem | Fix |
|---------|-----|
| Generic output | Add more context (reference materials, examples, style guides) |
| Steps skipped or wrong | Refine the prompt (more explicit instructions) |
| Step needs domain expertise | Build a skill for that step |
| AI needs to make unpredictable decisions | Convert from prompt to agent |

**Coaching guidance:**

- The first run is always a test, not production
- Set expectations: 2-4 iterations is normal
- The workflow is ready when you can run it on a new scenario and trust the output

---

## Common Questions

**"Where do I start?"**
If you know which workflow to work on → Step 2 (Deconstruct). If you need to figure out where AI fits → Step 1 (Analyze).

**"Do I need agents?"**
Most workflows work as a prompt or skill-powered prompt. You need agents only when the workflow requires tool use (web, files, APIs) or autonomous decision-making. Start simple.

**"What if my workflow is too big?"**
Apply the scope check: one trigger, one deliverable. If it has multiple triggers or produces distinct outputs at different points, split it into separate workflows.

**"How long does this take?"**
Step 1: ~20-30 min. Step 2: ~15-25 min. Step 3 Design: ~10-15 min. Step 3 Construct: ~5-15 min per building block. First run + iteration: varies.

**"Can I skip steps?"**
You can skip Step 1 if you already know your workflow. You should not skip Step 2 (Deconstruct) or Step 3.1 (Design) — they prevent building the wrong thing.

---

## Detailed Documentation Index

When the user needs more depth on a specific topic, fetch the raw Markdown from the URLs below. Each URL points to the full documentation page.

### Framework Pages

| Topic | Description | Raw Markdown URL |
|-------|-------------|-----------------|
| Framework overview | Full methodology, key concepts, vocabulary | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/index.md` |
| Step 1: Analyze | Opportunity finder prompt template and instructions | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/analyze.md` |
| Step 2: Deconstruct | How Deconstruct works, examples, tips, and what the skill produces | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/deconstruct/index.md` |
| Step 3: Build overview | The three parts (Design, Construct, Run) and pattern-specific paths | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/index.md` |
| 3.1: Design | Execution pattern spectrum, autonomy classification, the Design prompt template | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/design.md` |
| 3.2: Construct | How the model builds your workflow's building blocks, plus what you need to do yourself | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/construct.md` |
| 3.3: Run | Executing, testing, and iterating your workflow | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/run.md` |

### Worked Examples

| Example | Type | Raw Markdown URL |
|---------|------|-----------------|
| LinkedIn prospect research | Deterministic automation | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/deterministic-automation.md` |
| Meeting prep researcher | AI collaborative | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/ai-collaborative.md` |
| HBR article pipeline | Autonomous multi-agent | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/build/autonomous-agent.md` |

### Supporting References

| Topic | Description | Raw Markdown URL |
|-------|-------------|-----------------|
| Agentic Building Blocks | Definitions and cross-platform details for all ten blocks | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/agentic-building-blocks/index.md` |
| AI Use Cases | Six use case primitives with examples | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/use-cases/index.md` |
| Agents by platform | Platform-specific agent building guides | `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/agentic-building-blocks/agents/index.md` |
