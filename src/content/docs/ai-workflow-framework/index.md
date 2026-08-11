---
title: AI Workflow Framework
description: A seven-step methodology — Analyze, Deconstruct, Design, Build, Test, Run, Improve — for identifying AI opportunities in your workflows, breaking them into building blocks, and constructing working AI-powered workflows.
---

## The Problem

Most AI adoption starts with the technology — "we have ChatGPT, where should we use it?" This leads to shallow adoption and misses the workflows where AI creates real leverage. And even when people identify the right workflow, there's a gap between the idea and making it real — without a repeatable process to follow, they get stuck and stop. The AI Workflow Framework closes that gap: audit your workflows, identify where AI creates the most value, deconstruct those workflows into building blocks, design the architecture, build the components, test them, deploy, and improve over time.

## How It Works

The framework is facilitated by **seven skills** — reusable AI routines that guide you through each step interactively. You don't need to figure out the right questions to ask or remember the methodology — the skill drives the conversation, probes for details, and produces structured outputs you carry to the next step. You bring the domain knowledge about your work; the AI handles the process.

| Step | Skill | What it guides you through |
|------|-------|---------------------------|
| 1.&nbsp;Analyze | `analyze` | Identify and prioritize the workflows worth reimagining with AI |
| 2.&nbsp;Deconstruct | `deconstruct` | Map the workflow’s process — or define the goal for an agent system |
| 3.&nbsp;Design | `design` | Architect how AI building blocks will power your workflow |
| 4.&nbsp;Build | `build` | Build the AI building blocks your design specifies |
| 5.&nbsp;Test | `test` | Test your workflow's output quality and fix what's not working |
| 6.&nbsp;Run | `run` | Deploy and operationalize your workflow |
| 7.&nbsp;Improve | `improve` | Monitor quality and innovate your workflow over time |

**Get the skills:** See [Set Up the Skills](skills/) for installation instructions across Claude Code, Claude Cowork, Claude.ai, M365 Copilot (Cowork), Cursor, Codex CLI, Gemini CLI, and VS Code Copilot. The plugin name is `handsonai`.

## Run It All at Once: framework-agent

You can run all seven skills step-by-step in separate conversations, or use the **`framework-agent`** to orchestrate the full lifecycle end-to-end in a single session.

**What it does:** Runs the seven skills sequentially — Analyze, Deconstruct, Design, Build, Test, Run, Improve — with file-based handoffs between stages. The agent manages the flow between steps, saves intermediate files to `outputs/`, and keeps you involved at each stage.

**When to use it:** Use the agent when you want to go through the entire process in one session. If you prefer to work step-by-step across separate conversations — or want to run a single step standalone (e.g., just Deconstruct, just Improve) — invoke the individual skills instead. Both styles produce the same artifacts.

**Example prompts:**

```
"I want to deconstruct my client onboarding workflow"
→ Walks you through all seven steps, asking questions during
  discovery, presenting the analysis for review, and generating
  the build deliverables

"People keep dropping off during enrollment. Help me build
a workflow for that."
→ Starts from a problem description, proposes a candidate
  workflow, then deconstructs and designs it

"Help me figure out which parts of my weekly reporting process
could be automated with AI"
→ Decomposes the reporting process, assesses autonomy, chooses
  an orchestration mechanism, and identifies quick wins
```

**What you'll get** — each workflow gets its own folder under `outputs/`, named with the workflow name in lowercase using hyphens (for example, `outputs/client-onboarding/`). Each workflow gets a Workflow node in your `registry/` bundle — status, mode, and review date in one place — so any session can resume mid-framework by reading the node and seeing which artifacts already exist:

1. **Opportunity Report** — `outputs/ai-opportunity-report.md` (before a workflow is named)
2. **Workflow Requirements** — `[name]/requirements.md`
3. **Design Spec** — `[name]/design-spec.md`
4. **Platform Artifacts** — prompts, skills, agents, and configs in the format your platform requires
5. **Test Results** — `[name]/test-results.md`
6. **Run Guide** — `[name]/run-guide.md`, plus a run log at `[name]/runs.md`
7. **Improvement Plan** — `[name]/improvement-plan.md` (when running Improve)

## The Framework

Seven steps, each building on the last:

### Step 1: Analyze Workflows

Find which workflows are candidates for AI.

Before you can apply AI to anything, you need to know *where* it fits. Step 1 is a structured audit of your workflows that produces a prioritized list of opportunities classified on two dimensions:

- **Autonomy** — How much decision-making does the AI have? **Deterministic** (follows fixed rules), **Guided** (makes bounded decisions within guardrails), or **Autonomous** (plans and adapts independently)
- **Human Involvement** — Is a human in the loop during execution? **Augmented** (human reviews and steers) or **Automated** (AI runs solo)

The audit starts by determining which lens to use — individual or organizational — then scans what AI already knows about your work, interviews you with lens-specific questions to fill gaps, and produces a classified report with specific opportunities and actionable first steps.

**Deliverable:** **Opportunity Report** (`outputs/ai-opportunity-report.md`) — prioritized opportunities with a Workflow Candidate Summary listing the workflows you've chosen to pursue.

**Facilitated by the `analyze` skill.** See [Analyze Workflows](analyze/) for details and [Set Up the Skills](skills/) for installation on any supported platform.

---

### Step 2: Deconstruct Workflows

Define *what* the business process does — every step, decision, and handoff — before deciding *how* to implement it with AI.

Step 2 is the **Product Requirements Document (PRD) for your workflow** — clear requirements, decision rules, and edge cases that feed directly into Design. There are two paths, chosen by one question at the start: *do you know the steps, or just the goal?*

- **Step-driven** — You can describe how the work gets done. The model interviews you to refine the steps and surface decision rules, edge cases, and the context each step needs. Each step is captured as Goal / Inputs / Outputs / Rules & Edge Cases / Context.
- **Goal-driven** — You know what "done" looks like, but the work takes different steps depending on what comes in, so you give an agent system a goal and let it figure out the steps at runtime. The model captures the goal, inputs, acceptance criteria, rules, and constraints — without prescribing steps.

Don't have either yet? Describe the problem you're trying to solve. The model proposes a candidate workflow and routes you into one of the two paths above.

For step-driven workflows, the model uses the **six-question framework** as the interview structure to identify what belongs in each step's requirements block:

1. Is this step actually multiple steps bundled together?
2. Are there decision points, branches, or quality gates?
3. What data flows in and out?
4. What context, documents, or reference materials does this step need?
5. What happens when this step fails?
6. Can the AI access, interpret, and persist the data this step needs?

Two questions run alongside the mapping, whichever path you took:

- **What is this worth, and how would you know?** The business objective it supports, the outcome that changes, what you'd count, and what that number is today. Without today's number there is nothing to compare the improvement against — and if nobody knows it, the requirements say so plainly rather than guessing.
- **What must it protect?** Where data may travel, who may see the output, what has to be recorded, what the workflow must never do, and which regulation applies. Most workflows need none of this and finish the section in a line; the skill works out which case you're in from what it already knows about your context, rather than making you fill in a form.

This is purely the *what* — the workflow's requirements, with no prescription of how AI will handle it. The *how* comes in Step 3 (Design).

**Deliverable:** **Workflow Requirements** (`outputs/[name]/requirements.md`) — a PRD-style document. Every Workflow Requirements file contains: Goal, Value & Measurement, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Rules & Constraints, Human Gates, and Security, Privacy & Safety. Step-driven workflows add a Steps Overview with per-step requirements; goal-driven workflows add Inputs.

**Facilitated by the `deconstruct` skill.** See [Deconstruct Workflows](deconstruct/) for details and [Set Up the Skills](skills/) for installation on any supported platform.

---

### Step 3: Design Your AI Workflow

Decide *how* the workflow should be built — before you build it.

The Design step takes your Workflow Requirements and produces a complete blueprint for your AI workflow. The skill works through three layers of decisions:

- **Architecture** — confirm your platform, assess the workflow's autonomy level (Deterministic, Guided, or Autonomous), and recommend an orchestration mechanism (Prompt, Skill-Powered Workflow, or Agent) with an involvement mode (Augmented or Automated).
- **Decomposition** — classify each step on the autonomy spectrum, map AI building blocks, and identify which steps become reusable skills.
- **Component blueprints** — document the field-level specs for each new skill and agent.

The spec must be approved before moving to Build.

**Deliverable:** **Design Spec** (`outputs/[name]/design-spec.md`) — architecture decisions, autonomy assessment, orchestration mechanism, per-step classifications, skill candidates, agent blueprints, integration options, model recommendation, Data Readiness Summary, implementation order, and a Constraint Conformance table showing, for each protection named in Deconstruct, where the design meets it. References the Workflow Requirements rather than restating it.

**Facilitated by the `design` skill.** See [Design Your AI Workflow](design/) for the full guide with autonomy assessment, orchestration mechanism decision flow, and output format.

---

### Step 4: Build the Components

Generate platform-appropriate artifacts from the approved spec.

The Build step starts with a **Prepare Context** phase — systematically resolving the context needs identified during Deconstruct and Design. Then the model researches your platform using a curated platform registry, integration registries, and web search to generate the actual artifacts — context, skills, prompts, agents, MCP connections — in whatever format your platform requires. Only the components your orchestration mechanism needs are built.

**Deliverable:** **Platform artifacts** — prompts, skills, agents, and configs generated for your specific platform, plus resolved context artifacts (style guides, reference materials, examples).

**Facilitated by the `build` skill.** See [Build](build/) for mechanism-specific build paths and platform research details.

---

### Step 5: Test the Workflow

Structured testing against the Acceptance Criteria and Example Scenarios captured in the Workflow Requirements.

Your first run is a test, not a deployment. The Test step walks you through a quick smoke test (does it run at all?), then a full eval suite where you run each Example Scenario from the Workflow Requirements and score the output against the Acceptance Criteria dimensions. You also test individual building blocks in isolation and establish a baseline for future comparison.

Most workflows need 2-4 iterations between Build and Test before they produce reliably good output. When something is off, the skill helps you diagnose which building block to fix and sends you back to Build with a clear target.

**Deliverable:** **Test Results** (`outputs/[name]/test-results.md`) — eval scorecard with scores per scenario and dimension, baseline averages, diagnosed issues, and a readiness assessment.

**Facilitated by the `test` skill.** See [Test](test/) for the full evaluation process and troubleshooting guide.

---

### Step 6: Run the Workflow

Deploy and operate your tested workflow.

Once your workflow passes testing, Run helps you put it into production. The skill produces a Run Guide tailored to your platform and technical comfort level, then helps you choose the right run pattern — from simple paste-and-run to fully automated schedules. For organizational workflows, Run also covers sharing with your team and setting up ongoing operations.

**Deliverable:** **Run Guide** (`outputs/[name]/run-guide.md`) — artifact inventory, setup steps, first production run instructions, run pattern, and operationalization guidance.

**Facilitated by the `run` skill.** See [Run](run/) for run patterns, deployment options, and operationalization guidance.

---

### Step 7: Improve Over Time

Evaluate and evolve running workflows.

Workflows are not something you set up once and forget. Over time, business context changes, new tools become available, and output quality can drift. The Improve step teaches you when and how to revisit a running workflow — watch for quality signals, re-run your eval suite to catch regressions, and assess whether the workflow should graduate to a more capable orchestration mechanism. Four outcomes: no changes needed, tune it, redesign it, or evolve it.

**Deliverable:** **Improvement Plan** (`outputs/[name]/improvement-plan.md`) — current vs. baseline scores, quality signals, graduation assessment, decision outcome, and specific next actions.

**Facilitated by the `improve` skill.** See [Improve](improve/) for the full evaluation and graduation framework.

---

## Key Concepts

Quick reference for the framework's vocabulary:

### AI Workflow Design Matrix

Every AI workflow is classified on two dimensions — autonomy and human involvement — producing six archetypes. See the [AI Workflow Design Matrix](workflow-design-matrix/) for the full 3x2 matrix with descriptions, examples, and guidance on choosing the right archetype.

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

Used to decompose each step in a step-driven workflow:

1. **Discrete steps** — Is this one step or multiple bundled together?
2. **Decision points** — Any if/then branches, quality gates, or judgment calls?
3. **Data flows** — What goes in? What comes out? Where from and where to?
4. **Context needs** — What documents, files, or reference materials are required?
5. **Failure modes** — What happens when this step fails?
6. **Data readiness** — Can the AI access, interpret, and persist the data this step needs?

### AI Building Blocks

Each workflow step gets mapped to one or more building blocks across three layers — **Intelligence** (Model, Context, Memory, Project), **Orchestration** (Prompt, Skill, Agent), and **Integration** (MCP, API, SDK, CLI). See [Agentic Building Blocks](../agentic-building-blocks/) for definitions, examples, and cross-platform comparisons.

### Six Use Case Primitives

When classifying opportunities from Step 1, it helps to know what **type** of AI work each one involves. The [six use case primitives](../use-cases/) — Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, and Automation — provide a classification system for the opportunities you identify.

### Autonomy Spectrum

Used to classify each workflow step during [Design](design/):

| Level | Description |
|-------|-------------|
| **Human** | Requires human judgment, creativity, or physical action |
| **Deterministic** | Follows fixed rules; AI executes reliably with no decisions |
| **Guided** | AI makes bounded decisions within guardrails; human reviews at key checkpoints |
| **Autonomous** | AI plans and executes end-to-end, including decisions and tool use |

The same scale describes the **whole workflow** during Design's autonomy assessment — with one difference: **Human appears only at the step level** (a whole workflow that's entirely human needs no AI design), so the workflow-level scale runs Deterministic → Guided → Autonomous.

### Orchestration Mechanism

The orchestration mechanism answers: **who drives the workflow?** The right mechanism depends on the workflow's autonomy level and what it actually needs:

| Mechanism | Description | Signals |
|-----------|-------------|---------|
| **Prompt** | Human follows structured instructions step by step, all logic inline | Sequential steps, human provides inputs and makes decisions |
| **Skill-Powered Workflow** | Human invokes reusable skills in a defined sequence | Repeatable sub-routines, moderate complexity |
| **Agent** | Agent orchestrates the flow, invoking skills and making sequencing decisions | Tool use required, autonomous decisions, multi-step reasoning |

Single-agent vs. multi-agent is an architecture detail decided during agent configuration — not a top-level choice.

## Getting Started

:::tip[Get guided help]

- **MCP Server** — [Connect the MCP server](../mcp-server/) and ask your AI to walk you through the framework step by step.
- **Skills** — Install the [AI Workflow Framework skills](skills/) for interactive guidance through all seven steps.
:::
1. **[Analyze Workflows](analyze/)** — identify your best AI candidates
2. **[Deconstruct the workflow](deconstruct/)** — break it into discrete steps
3. **[Design](design/)** your AI workflow — assess autonomy, choose an orchestration mechanism, classify steps, map building blocks
4. **[Build](build/)** the components your orchestration mechanism requires
5. **[Test](test/)** your workflow against evaluation criteria and establish a quality baseline
6. **[Run](run/)** — deploy, choose a run pattern, and operationalize
7. **[Improve](improve/)** — periodically evaluate, catch regressions, and evolve

:::tip[Before you start]
- **See the destination first.** The [worked example](examples/worked-example/) shows every file a complete run produces — the whole project folder for one small workflow taken through all seven steps.
- **Start small.** Make your first workflow starter-sized: 3–5 steps, one tool connection, triggered manually. Build your big opportunity second, once you've been through the loop.
- **Pausing is safe.** Every step saves progress to files. In any later session, just say **"continue my workflow"** — the framework reads its tracking file and picks up at the right step.
:::

## FAQ

**Which step should I start with?**
Start with Step 1 ([Analyze](analyze/)) if you're not sure where AI fits in your work. Browse [AI Use Cases](../use-cases/) to see what types of work AI handles — content creation, research, coding, data analysis, ideation, and automation. Start with Step 2 ([Deconstruct](deconstruct/)) if you already know which workflow you want to automate.

**Can I start from a problem instead of a workflow?**
Yes. Tell the [`framework-agent`](#run-it-all-at-once-framework-agent) about your problem (e.g., "people keep dropping off during enrollment") and it will propose a candidate workflow for you to refine during discovery. The individual `deconstruct` skill can do the same.

**How many iterations of Build-Test should I expect?**
Most workflows need 2–4 rounds of Build and Test before they produce reliably good output. Each iteration should be targeted — fix a specific building block, re-test, and measure improvement. If you have been through four iterations and scores are not improving, return to [Design (Step 3)](design/) to re-examine your architecture decisions.

**Where are the example agents and prompts?**
They're in the [AI Workflow Examples](../use-the-playbook/build/ai-workflow-examples/) collection — agents for executive writing, editorial review, research, meeting prep, and AI news.

For setup-specific questions (which platforms support the skills, how to handle losing context mid-conversation), see the [FAQ on the Set Up the Skills page](skills/#faq).
