---
title: Workflow Deconstruction
description: Deconstruct business workflows into AI building blocks with guided discovery, analysis, and output generation
---

# Workflow Deconstruction

Deconstruct any business workflow into AI building blocks. This plugin walks you through a three-step process — discovery, analysis, and output generation — that turns a verbal description of how you work into a structured blueprint, an AI readiness analysis, and a ready-to-use prompt with skill recommendations. Use it when you want to figure out which parts of a workflow can be automated, augmented, or left as-is.

## Install

```bash
/plugin install workflow-deconstruction@handsonai
```

## Components

### Agents

---

#### `workflow-deconstructor`

**What it does:** Orchestrates the full three-step workflow deconstruction process. Runs discovery, analysis, and output generation sequentially, with file-based handoffs between stages so you can also run each step individually in separate conversations.

**When to use it:** Use this when you want to go through the entire deconstruction process in one session. The agent manages the flow between steps, saves intermediate files, and keeps you involved at each stage. If you prefer to work step-by-step across separate conversations, invoke the individual skills instead.

**How it works:** The agent runs three skills in sequence:

1. **Discovery** (`workflow-discovery`) — Interactive conversation where you describe your workflow. The agent probes for missing steps, decision points, data flows, and failure modes. Produces a Workflow Blueprint.
2. **Analysis** (`workflow-analysis`) — Reads the Blueprint, classifies each step on an autonomy spectrum (Human → AI-Deterministic → AI-Semi-Autonomous → AI-Autonomous), and maps to AI building blocks. Produces a Workflow Analysis Document.
3. **Output Generation** (`workflow-output-generation`) — Reads the Analysis Document and generates a ready-to-use prompt plus recommendations for which steps should become dedicated skills. Produces the Baseline Prompt and Skill Recommendations.

Files are saved to `outputs/` using kebab-case workflow names (e.g., `outputs/lead-qualification-blueprint.md`).

**Example prompts:**

    "I want to deconstruct my client onboarding workflow"
    → Walks you through all three steps, asking questions during
      discovery, presenting the analysis for review, and generating
      the final deliverables

    "People keep dropping off during enrollment. Help me build
    a workflow for that."
    → Starts from a problem description, proposes a candidate
      workflow, then deconstructs it into building blocks

    "Help me figure out which parts of my weekly reporting process
    could be automated with AI"
    → Decomposes the reporting process, classifies each step by
      autonomy level, and identifies quick wins vs. complex
      automation opportunities

**What you'll get:** Four files in `outputs/`:

1. **Workflow Blueprint** — `[name]-blueprint.md` — structured decomposition of every step
2. **Workflow Analysis Document** — `[name]-analysis.md` — autonomy classification and AI building block mapping
3. **Baseline Workflow Prompt** — `[name]-prompt.md` — ready-to-use prompt with numbered steps
4. **Skill Build Recommendations** — `[name]-skill-recs.md` — specs for which steps should become dedicated skills

---

### Skills

---

#### `workflow-discovery`

**What it does:** Interactively discovers and decomposes a business workflow into a structured Workflow Blueprint. This is Step 1 of 3 in the workflow deconstruction series.

**When to use it:** Use this when you want to thoroughly document a workflow before analyzing it for AI readiness. Also useful standalone when you just need a structured breakdown of a complex process — even without planning to automate it.

**How it works:**

1. **Scenario discovery** — Claude asks about the business scenario, objective, high-level steps, and ownership. One question at a time. If you describe a problem instead of a workflow, Claude proposes a candidate workflow for you to react to.
2. **Scope check** — Claude assesses whether this is one workflow or multiple bundled together. If multiple, it recommends splitting and asks which to start with.
3. **Name the workflow** — Claude presents 2-3 name options (2-4 word noun phrases, Title Case) and confirms name, description, outcome, trigger, and type.
4. **Deep dive** — For each step, Claude probes five dimensions:
    - Discrete steps (is this actually multiple steps?)
    - Decision points (if/then branches, quality gates)
    - Data flows (inputs, outputs, sources, destinations)
    - Context needs (specific documents, files, reference materials)
    - Failure modes (what happens when this step fails)
5. **Propose and react** — From step 4 onward, Claude proposes a hypothesis across all five dimensions and asks "What's right, what's wrong, what am I missing?"
6. **Map sequence** — Claude identifies sequential vs. parallel steps and the critical path
7. **Consolidate context** — Claude presents a rolled-up "context shopping list" of every artifact the workflow needs
8. **Generate Blueprint** — Claude writes the structured Blueprint to the output file

**Example prompts:**

    "Use workflow-discovery to break down my expense reporting process"
    → Interactive discovery session producing
      outputs/expense-reporting-blueprint.md

    "I need to document how our team handles customer escalations"
    → Walks through the discovery process, probing for hidden steps
      and decision points

**What you'll get:** A Workflow Blueprint file (`outputs/[name]-blueprint.md`) containing: scenario metadata, refined steps (with sub-steps, decision points, data flows, context needs, and failure modes for each), step sequence and dependencies, and a context shopping list.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

#### `workflow-analysis`

**What it does:** Classifies workflow steps on the autonomy spectrum, maps them to AI building blocks, and produces a Workflow Analysis Document. This is Step 2 of 3 in the workflow deconstruction series.

**When to use it:** Use this when you have a Workflow Blueprint (from Step 1) and want to analyze which steps can be automated, which need human oversight, and what AI tools are required.

**How it works:**

1. **Load Blueprint** — Claude reads the Blueprint file from `outputs/`
2. **Confirm understanding** — Claude summarizes the workflow and asks you to confirm before proceeding
3. **Classify each step** — For every step, Claude determines:
    - **Autonomy level**: Human / AI-Deterministic / AI-Semi-Autonomous / AI-Autonomous
    - **AI building block(s)**: Prompt, Context, Skill, Agent, MCP, Project
    - **Tools and connectors**: External tools, APIs, and integrations needed
    - **Human-in-the-loop gates**: Where human review is recommended
4. **Present mapping** — Claude shows the classification as a table and walks through reasoning for non-obvious decisions. You can adjust classifications.
5. **Generate Analysis Document** — After your confirmation, Claude produces the complete document

**Autonomy spectrum:**

| Level | Description |
|-------|-------------|
| Human | Must be done by a person — judgment, relationship, creativity |
| AI-Deterministic | Follows fixed rules — template filling, data lookups, formatting |
| AI-Semi-Autonomous | AI does most work, human reviews before final output |
| AI-Autonomous | AI handles end-to-end without human intervention |

**Example prompts:**

    "Use workflow-analysis on my blueprint"
    → Reads the most recent Blueprint, classifies each step, presents
      the mapping table, and generates the Analysis Document

    "Analyze the lead-qualification blueprint for AI readiness"
    → Reads outputs/lead-qualification-blueprint.md and produces
      the analysis

**What you'll get:** A Workflow Analysis Document (`outputs/[name]-analysis.md`) containing: scenario summary, step-by-step decomposition table (with autonomy level and AI building blocks for each step), autonomy spectrum summary, step sequence and dependencies, prerequisites, context inventory, tools and connectors required, and recommended implementation order (quick wins first).

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

#### `workflow-output-generation`

**What it does:** Generates a ready-to-use Baseline Workflow Prompt and Skill Build Recommendations from a Workflow Analysis Document. This is Step 3 of 3 in the workflow deconstruction series.

**When to use it:** Use this when you have a completed Analysis Document (from Step 2) and want the final, actionable deliverables — a prompt you can run immediately and specs for which steps should become dedicated skills.

**How it works:**

1. **Load Analysis Document** — Claude reads the Analysis Document from `outputs/`
2. **Confirm understanding** — Claude summarizes the workflow, step count, AI-eligible steps, and implementation order. You confirm before proceeding.
3. **Generate Baseline Workflow Prompt** — A self-contained, ready-to-use prompt with:
    - Title, purpose, and when to use it
    - Numbered steps, each labeled (AI) or (Human)
    - Input requirements with format specifications
    - Context requirements (what to attach when running the prompt)
    - Output format with structure specifications
4. **Generate Skill Build Recommendations** — For each step that should become a dedicated skill:
    - Skill name, purpose, inputs, outputs
    - Which baseline prompt steps it replaces
    - Integration points (external tools, APIs, MCP servers)
    - Priority level (High / Medium / Low)
    - Quick Start Prompt for invoking the skill

**Example prompts:**

    "Use workflow-output-generation on my analysis"
    → Reads the most recent Analysis Document, generates the prompt
      and skill recommendations

    "Generate the deliverables for expense-reporting"
    → Reads outputs/expense-reporting-analysis.md and produces both
      output files

**What you'll get:** Two files:

1. **Baseline Workflow Prompt** (`outputs/[name]-prompt.md`) — A self-contained prompt you can run immediately. Steps are labeled (AI) or (Human), includes all input/context/output requirements.
2. **Skill Build Recommendations** (`outputs/[name]-skill-recs.md`) — Specs for each recommended skill, in priority order, with Quick Start Prompts.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

## Recommended Workflow

The three skills form a pipeline, each building on the previous step's output:

1. **Discover** — Run `workflow-discovery` to interactively decompose your workflow into a Blueprint
2. **Analyze** — Run `workflow-analysis` to classify each step and map AI building blocks
3. **Generate** — Run `workflow-output-generation` to produce your ready-to-use prompt and skill specs

Use the `workflow-deconstructor` agent to run all three in one session, or invoke each skill individually across separate conversations — the file-based handoffs work either way.

**After deconstruction:**

- Start by running the Baseline Workflow Prompt on a real scenario
- Build skills in priority order from the recommendations
- Each skill you build replaces steps in the baseline prompt, making the workflow progressively more automated

## FAQ

**Can I start from a problem instead of a workflow?**
Yes. Tell the `workflow-deconstructor` agent about your problem (e.g., "people keep dropping off during enrollment") and it will propose a candidate workflow for you to refine during discovery.

**What if I lose context mid-conversation?**
The file-based handoffs mean you can continue in a new conversation. Just invoke the next skill and point it at the file from the previous step (e.g., "Use workflow-analysis on outputs/lead-qualification-blueprint.md").

**What are AI building blocks?**
The categories used during analysis: Prompt (single instruction), Context (reference material), Skill (multi-step workflow), Agent (autonomous personality), MCP (external tool connection), and Project (workspace configuration). Each step gets mapped to one or more of these.

**How long does the full process take?**
Discovery is the longest phase — typically 15-30 minutes of interactive conversation depending on workflow complexity. Analysis and output generation are faster since they work from the written Blueprint. The full process usually takes 30-45 minutes.
