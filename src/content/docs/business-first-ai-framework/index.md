---
title: Business-First AI Framework
description: A seven-step methodology — Analyze, Deconstruct, Design, Build, Test, Run, Improve — for identifying AI opportunities in your workflows, breaking them into building blocks, and constructing working AI-powered workflows.
---## The Problem

Most AI adoption starts with the technology — "we have ChatGPT, where should we use it?" This leads to shallow adoption and misses the workflows where AI creates real leverage. And even when people identify the right workflow, there's a gap between the idea and making it real — without a repeatable process to follow, they get stuck and stop. The Business-First AI Framework closes that gap: audit your workflows, identify where AI creates the most value, deconstruct those workflows into building blocks, design the architecture, build the components, test them, deploy, and improve over time.

## How It Works

The framework is facilitated by **seven skills** — reusable AI routines that guide you through each step interactively. You don't need to figure out the right questions to ask or remember the methodology — the skill drives the conversation, probes for details, and produces structured outputs you carry to the next step. You bring the domain knowledge about your work; the AI handles the process.

<div class="framework-steps" markdown>

| Step | Skill | What it guides you through |
|------|-------|---------------------------|
| 1. Analyze | `analyze` | Identify and prioritize the workflows worth reimagining with AI |
| 2. Deconstruct | `deconstruct` | Map the workflow's process — or define the outcome it should produce |
| 3. Design | `design` | Architect how AI building blocks will power your workflow |
| 4. Build | `build` | Build the AI building blocks your design specifies |
| 5. Test | `test` | Test your workflow's output quality and fix what's not working |
| 6. Run | `run` | Deploy and operationalize your workflow |
| 7. Improve | `improve` | Monitor quality and innovate your workflow over time |

</div>

**Get the skills:** See [Get the Skills](skills.mdx) for installation instructions across Claude Code, Cowork, Claude.ai, Cursor, Codex CLI, Gemini CLI, and VS Code Copilot. The plugin name is `business-first-ai`.

## The Framework

Seven steps, each building on the last:

### Step 1: Analyze Workflows

Find which workflows are candidates for AI.

Before you can apply AI to anything, you need to know *where* it fits. Step 1 is a structured audit of your workflows that produces a prioritized list of opportunities classified on two dimensions:

- **Autonomy** — How much decision-making does the AI have? **Deterministic** (follows fixed rules), **Guided** (makes bounded decisions within guardrails), or **Autonomous** (plans and adapts independently)
- **Human Involvement** — Is a human in the loop during execution? **Augmented** (human reviews and steers) or **Automated** (AI runs solo)

The audit starts by determining which lens to use — individual or organizational — then scans what AI already knows about your work, interviews you with lens-specific questions to fill gaps, and produces a classified report with specific opportunities and actionable first steps.

**Deliverable:** **Opportunity Report** (`outputs/ai-opportunity-report.md`) — prioritized opportunities with a Workflow Candidate Summary listing the workflows you've chosen to pursue.

**Facilitated by the `analyze` skill.** See [Analyze Workflows](analyze.md) for details and [Get the Skills](skills.mdx) for installation on any supported platform.

---

### Step 2: Deconstruct Workflows

Define *what* the business process does — every step, decision, and handoff — before deciding *how* to implement it with AI.

How you enter depends on what you're starting with:

- **You know the process.** You can describe the steps, decisions, and handoffs — the model interviews you to surface hidden details and capture it all in a structured format. This is the most common path for workflows you already do manually.
- **You have a problem, not a process.** You know what's broken or slow, but there's no defined workflow yet. The model proposes a candidate workflow for you to react to, then decomposes it collaboratively.
- **You know the outcome, not the process.** You know what you want produced but don't want to prescribe how — the model captures your goal, constraints, quality criteria, and what the agent system needs to be good at, producing an outcome-driven definition that feeds into agent-oriented design.

For the first two paths, the model uses the **six-question framework** to break down each step:

1. Is this step actually multiple steps bundled together?
2. Are there decision points, branches, or quality gates?
3. What data flows in and out?
4. What context, documents, or reference materials does this step need?
5. What happens when this step fails?
6. Can the AI access, interpret, and persist the data this step needs?

This is purely the *what* — it captures the process without prescribing how AI will handle it. The *how* comes in Step 3 (Design), where the Workflow Definition becomes the input for architecture decisions.

**Deliverable:** **Workflow Definition** (`outputs/[name]-definition.md`) — either a step-decomposed breakdown (refined steps with decision points, data flows, context needs, failure modes, and a context shopping list) or an outcome-driven definition (goal, inputs, outputs, constraints, quality criteria, capability domains, and human gates).

**Facilitated by the `deconstruct` skill.** See [Deconstruct Workflows](deconstruct/index.md) for details and [Get the Skills](skills.mdx) for installation on any supported platform.

---

### Step 3: Design Your AI Workflow

Decide *how* the workflow should be built — before you build it.

The Design step takes your Workflow Definition and produces a complete blueprint for your AI workflow. The skill confirms your platform, extracts tool integrations and constraints from your Workflow Definition, assesses the workflow's autonomy level (Deterministic, Guided, or Autonomous), recommends an orchestration mechanism (Prompt, Skill-Powered Prompt, or Agent) and involvement mode, classifies each step on the autonomy spectrum, maps AI building blocks, identifies skill candidates, and documents agent blueprints when needed. The spec must be approved before moving to Build.

**Deliverable:** **AI Building Block Spec** (`outputs/[name]-building-block-spec.md`) — architecture decisions, autonomy assessment, orchestration mechanism, per-step classifications, skill candidates, agent blueprints, context inventory, and implementation order.

**Facilitated by the `design` skill.** See [Design Your AI Workflow](design.md) for the full guide with autonomy assessment, orchestration mechanism decision flow, and output format.

---

### Step 4: Build the Components

Generate platform-appropriate artifacts from the approved spec.

The Build step starts with a **Prepare Context** phase — systematically resolving the context needs identified during Deconstruct and Design. Then the model researches your platform using a curated platform registry, integration registries, and web search to generate the actual artifacts — context, skills, prompts, agents, MCP connections — in whatever format your platform requires. Only the components your orchestration mechanism needs are built.

**Deliverable:** **Platform artifacts** — prompts, skills, agents, and configs generated for your specific platform, plus resolved context artifacts (style guides, reference materials, examples).

**Facilitated by the `build` skill.** See [Build](build/index.mdx) for mechanism-specific build paths and platform research details.

---

### Step 5: Test the Workflow

Structured testing against the evaluation criteria from Design.

Your first run is a test, not a deployment. The Test step walks you through a quick smoke test (does it run at all?), then a full eval suite where you run each test scenario from the Building Block Spec and score the output on the quality dimensions defined during Design. You also test individual building blocks in isolation and establish a baseline for future comparison.

Most workflows need 2-4 iterations between Build and Test before they produce reliably good output. When something is off, the skill helps you diagnose which building block to fix and sends you back to Build with a clear target.

**Deliverable:** **Test Results** (`outputs/[name]-test-results.md`) — eval scorecard with scores per scenario and dimension, baseline averages, diagnosed issues, and a readiness assessment.

**Facilitated by the `test` skill.** See [Test](test.md) for the full evaluation process and troubleshooting guide.

---

### Step 6: Run the Workflow

Deploy and operate your tested workflow.

Once your workflow passes testing, Run helps you put it into production. The skill produces a Run Guide tailored to your platform and technical comfort level, then helps you choose the right run pattern — from simple paste-and-run to fully automated schedules. For organizational workflows, Run also covers sharing with your team and setting up ongoing operations.

**Deliverable:** **Run Guide** (`outputs/[name]-run-guide.md`) — artifact inventory, setup steps, first production run instructions, run pattern, and operationalization guidance.

**Facilitated by the `run` skill.** See [Run](run.md) for run patterns, deployment options, and operationalization guidance.

---

### Step 7: Improve Over Time

Evaluate and evolve running workflows.

Workflows are not set-and-forget. Over time, business context changes, new tools become available, and quality can drift. The Improve step teaches you when and how to revisit a running workflow — watch for quality signals, re-run your eval suite to catch regressions, and assess whether the workflow should graduate to a more capable orchestration mechanism. Four outcomes: no changes needed, tune it, redesign it, or evolve it.

**Deliverable:** **Improvement Plan** (`outputs/[name]-improvement-plan.md`) — current vs. baseline scores, quality signals, graduation assessment, decision outcome, and specific next actions.

**Facilitated by the `improve` skill.** See [Improve](improve.md) for the full evaluation and graduation framework.

---

## Key Concepts

Quick reference for the framework's vocabulary:

### AI Workflow Design Matrix

Every AI workflow is classified on two dimensions — autonomy and human involvement — producing six archetypes. See the [AI Workflow Design Matrix](workflow-design-matrix.md) for the full 3x2 matrix with descriptions, examples, and guidance on choosing the right archetype.

| Autonomy | Description | Example |
|----------|-------------|---------|
| **Deterministic** | AI follows fixed rules — no decisions, no judgment | Formatting reports, processing forms |
| **Guided** | AI makes bounded decisions within guardrails | Co-writing, brainstorming, research summaries |
| **Autonomous** | AI plans, decides, and adapts independently | Competitor monitoring, research → report pipelines |

| Involvement | Description |
|-------------|-------------|
| **Augmented** | Human is in the loop — reviews, steers, or decides at key points |
| **Automated** | AI runs solo — human reviews only the final output |

### Six-Question Framework

Used to decompose each step in a step-decomposed workflow:

1. **Discrete steps** — Is this one step or multiple bundled together?
2. **Decision points** — Any if/then branches, quality gates, or judgment calls?
3. **Data flows** — What goes in? What comes out? Where from and where to?
4. **Context needs** — What documents, files, or reference materials are required?
5. **Failure modes** — What happens when this step fails?
6. **Data readiness** — Can the AI access, interpret, and persist the data this step needs?

### AI Building Blocks

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

When classifying opportunities from Step 1, it helps to know what **type** of AI work each one involves. The [six use case primitives](../use-cases/index.md) — Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, and Automation — provide a classification system for the opportunities you identify.

### Autonomy Spectrum

Used to classify each workflow step during [Design](design.md):

| Level | Description |
|-------|-------------|
| **Human** | Requires human judgment, creativity, or physical action |
| **Deterministic** | Follows fixed rules; AI executes reliably with no decisions |
| **Guided** | AI makes bounded decisions within guardrails; human reviews at key checkpoints |
| **Autonomous** | AI plans and executes end-to-end, including decisions and tool use |

### Orchestration Mechanism

The orchestration mechanism answers: **who drives the workflow?** The right mechanism depends on the workflow's autonomy level and what it actually needs:

| Mechanism | Description | Signals |
|-----------|-------------|---------|
| **Prompt** | Human follows structured instructions step by step, all logic inline | Sequential steps, human provides inputs and makes decisions |
| **Skill-Powered Prompt** | Human invokes reusable skills in a defined sequence | Repeatable sub-routines, moderate complexity |
| **Agent** | Agent orchestrates the flow, invoking skills and making sequencing decisions | Tool use required, autonomous decisions, multi-step reasoning |

Single-agent vs. multi-agent is an architecture detail decided during agent configuration — not a top-level choice.

## Getting Started

:::tip[Get guided help]

- **MCP Server** — [Connect the MCP server](../mcp-server/index.md) and ask your AI to walk you through the framework step by step.
- **Skills** — Install the [Business-First AI skills](skills.mdx) for interactive guidance through all seven steps.
:::
1. **[Analyze Workflows](analyze.md)** — identify your best AI candidates
2. **[Deconstruct the workflow](deconstruct/index.md)** — break it into discrete steps
3. **[Design](design.md)** your AI workflow — assess autonomy, choose an orchestration mechanism, classify steps, map building blocks
4. **[Build](build/index.mdx)** the components your orchestration mechanism requires
5. **[Test](test.md)** your workflow against evaluation criteria and establish a quality baseline
6. **[Run](run.md)** — deploy, choose a run pattern, and operationalize
7. **[Improve](improve.md)** — periodically evaluate, catch regressions, and evolve
