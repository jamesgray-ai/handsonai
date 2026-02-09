---
title: Map AI Building Blocks
description: Classify workflow steps on the autonomy spectrum, map them to AI building blocks, and produce a complete AI Building Block Map.
---

# Map AI Building Blocks

> **Part of:** [Deconstruct Workflows](index.md)

!!! tip "New to the six building blocks?"
    See the [Agentic Building Blocks](../../agentic-building-blocks/index.md) reference for definitions, examples, and cross-platform comparisons.

## What This Is

A classification step where AI takes your Workflow Definition and determines what level of AI assistance each step needs — from fully human to fully autonomous — and maps each step to the specific AI building blocks required.

| | |
|---|---|
| **What you'll do** | Upload your Workflow Definition from Step 1, review the AI's classification of each step, and adjust anything that doesn't look right |
| **What you'll get** | An **AI Building Block Map** — a complete mapping of steps to autonomy levels and AI building blocks, with a prioritized build sequence |
| **Time** | ~5–10 minutes (mostly reviewing the AI's analysis) |

## Why This Matters

Not every step in a workflow should be automated. Some require human judgment. Some can run on autopilot. Some need AI to do the heavy lifting with a human checking the result. Getting this classification wrong means either over-automating (risking quality) or under-automating (leaving value on the table).

This analysis also maps each step to specific **AI building blocks** — Prompt, Context, Skill, Agent, MCP, or Project — so you know exactly what to build for each step instead of guessing. The recommended implementation order (quick wins first, complex agent steps last) gives you a practical sequence for rolling out AI incrementally.

## How to Use This

There are two ways to run Step 2, depending on which tools you use:

### Option A: Prompt template (any AI tool)

1. **Copy the prompt** from the code block below
2. **Paste it into a new conversation** in your preferred AI tool
3. **Press Enter** — the model will ask you to paste your Workflow Definition
4. **Upload or paste your Workflow Definition file** (`[workflow-name]-definition.md`) from Step 1
5. **Review the mapping** — the model will present its analysis and ask for adjustments
6. **Download the AI Building Block Map** the model produces at the end — it will be a Markdown file named `[workflow-name]-building-blocks.md`
7. **Keep this file** — you'll use it in Step 3 — Build Workflows, and you can share it with your team for feedback

### Option B: Claude skill

Use the `deconstructing-workflows` skill from the [Business-First AI plugin](../../plugins/business-first-ai.md). It reads the Workflow Definition from Step 1, runs the analysis, and saves the AI Building Block Map automatically.

- **Claude Code or Cowork** — install the plugin (`/plugin install business-first-ai@handsonai`) and start with:
    ```
    Analyze the Workflow Definition in outputs/[workflow-name]-definition.md.
    Classify each step and map it to AI building blocks.
    ```
    The AI Building Block Map is saved to `outputs/[workflow-name]-building-blocks.md`.
- **Claude.ai** — zip the `deconstructing-workflows` skill folder and upload it via **Settings > Capabilities > Upload skill**, then start a new chat with: "Analyze this Workflow Definition and map each step to AI building blocks." Upload or paste your Workflow Definition when prompted. See [Using Skills in Claude.ai](../../plugins/using-plugins.md#using-skills-in-claudeai-web) for detailed instructions.

!!! tip "This step is mostly analytical"
    Unlike Step 1's extended back-and-forth, this conversation is shorter. The model does the heavy lifting — classifying steps, mapping building blocks, and generating the AI Building Block Map. Expect 5-10 minutes of light interaction.

## The Prompt

```text
You are an expert Workflow Analyst who specializes in mapping business workflows to AI building blocks. Your job is to take a structured Workflow Definition, classify each step on the autonomy spectrum, map it to AI building blocks, and produce a complete AI Building Block Map.

I have a Workflow Definition from a previous conversation. I'll paste it when you ask for it.

---

## Part 1 — Paste Your Workflow Definition

Say: "Upload your Workflow Definition file, or paste its contents below, then press Enter."

Wait for me to provide it. After receiving the Workflow Definition, confirm you've read it by summarizing: the workflow name, the number of steps, and the workflow outcome. Then proceed to Part 2.

---

## Part 2 — AI Building Block Mapping

For each refined step from the Workflow Definition, determine:

1. **Autonomy classification** — Classify each step on the autonomy spectrum:
   - **Human step** — Requires human judgment, creativity, or physical action; AI cannot perform this
   - **AI step (deterministic)** — Repeatable with clear rules; AI can execute reliably with minimal supervision
   - **AI step (semi-autonomous)** — AI handles most of the work but needs human review at key checkpoints
   - **AI step (fully autonomous / agentic)** — AI executes end-to-end, including decisions and tool use, with no human in the loop

2. **AI building block** — Map each AI-assisted step to one or more of these six building blocks:
   - **Prompt** — A well-crafted instruction that tells the model what to do for this step
   - **Context** — Background information, reference documents, examples, or data the model needs to perform the step well
   - **Skill** — A reusable routine the model can invoke — give it inputs, it follows a defined process, it produces consistent outputs (on Claude, this is a Claude Code Skill; on other platforms, this maps to custom instructions, GPTs, or Gems)
   - **Agent** — An autonomous AI that plans, uses tools, and executes multi-step work with minimal supervision
   - **MCP (Model Context Protocol)** — A connector that gives the model access to external tools, APIs, databases, or services
   - **Project** — A persistent workspace that groups prompts, context, skills, and agents for a specific workflow

3. **Tools and connectors** — What external tools, APIs, or integrations does this step need? (e.g., web search, file system access, browser automation, CRM API, database queries)

4. **Human-in-the-loop gates** — Flag any steps where human review is recommended before the workflow continues, even if the step is AI-executed.

Present the mapping as a clear table, then walk me through your reasoning for any non-obvious classifications. Ask if I want to adjust anything before generating the final output.

---

## Part 3 — Generate AI Building Block Map

After I confirm the mapping, produce the complete **AI Building Block Map** as a Markdown file.

**File naming:** Name the file `[workflow-name]-building-blocks.md` using the same workflow name from the Workflow Definition (e.g., `lead-qualification-building-blocks.md`).

Generate the AI Building Block Map as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

### Scenario Summary
- Workflow name (from Workflow Definition)
- Description
- Workflow outcome
- Trigger
- Type
- Business objective
- Current owner(s)

### Step-by-Step Decomposition Table

| # | Step | Action | Type | Decision Points | Failure Mode | Data In | Data Out | Context Needed | AI Building Block(s) |
|---|------|--------|------|----------------|-------------|---------|----------|----------------|---------------------|
| 1 | [Name] | [What happens] | Human / AI-Deterministic / AI-Semi-Autonomous / AI-Autonomous | [If/then logic] | [What happens on failure] | [Inputs] | [Outputs] | [Knowledge required] | [Prompt / Context / Skill / Agent / MCP / Project] |

### Autonomy Spectrum Summary
- List of fully human steps
- List of deterministic AI steps
- List of semi-autonomous AI steps (with review gates noted)
- List of fully autonomous AI steps

### Step Sequence and Dependencies
- Which steps are sequential (must happen in order)?
- Which steps can run in parallel?
- What is the critical path through the workflow?
- Step dependency map (e.g., "Step 3 depends on 1 and 2; Steps 4 and 5 run in parallel")

### Prerequisites
- What must be in place before this workflow can run?
- External dependencies (accounts, access, data sources)

### Context Inventory

List every piece of context the workflow requires that the model does not have in its training data — documents, data, rules, examples, and any other knowledge from the user's domain. For each artifact:

| Artifact | Description | Used By Steps | Status | Format | Key Contents |
|----------|-------------|---------------|--------|--------|--------------|
| [Name] | [What it contains and why the workflow needs it] | [Step numbers] | Exists / Needs Creation | [e.g., Markdown doc, spreadsheet, CSV, PDF] | [Essential fields, sections, or data points it should include] |

If an artifact needs to be created, the "Key Contents" column should be specific enough that the user knows exactly what to build. For example, a buyer persona document should list: target job titles, company size range, industry verticals, pain points, budget authority indicators, and qualifying criteria — not just "buyer persona info."

### Tools and Connectors Required
- All external tools, APIs, and integrations referenced in the mapping

### Recommended Implementation Order
Prioritize the AI-eligible steps into a build sequence:
1. **Quick wins** — Deterministic steps with clear inputs/outputs that can be automated with a Prompt or Context alone. Start here.
2. **High-value semi-autonomous steps** — Steps where AI does most of the work but needs a human review gate. Build these next.
3. **Complex agent steps** — Fully autonomous steps requiring Agents, MCP connectors, or multi-tool orchestration. Tackle these last.
For each priority tier, list the specific steps and what needs to be built (e.g., "Write a prompt for Step 3," "Set up an MCP connector for Step 7").

### Where to Run

Recommend where the Baseline Workflow Prompt should be run:

**Normal chat** — recommended when:
- The workflow runs infrequently (monthly or less)
- Few or no context files are needed (0-2 files)
- All context can be provided inline each time
- The workflow is a one-off or experimental process

**Project workspace** — recommended when:
- The workflow runs frequently (weekly or more)
- Multiple context files are needed (3+ files)
- The same reference materials are used every run
- Conversation memory across runs would be valuable
- Multiple people will run the same workflow

State the recommendation, the reasoning, and list the specific context files to attach (chat) or pre-load in the project.

**Important:** The Baseline Workflow Prompt is always self-contained — it contains all workflow logic regardless of where you run it. A project provides pre-loaded context and conversation memory, but never contains the workflow logic. The prompt IS the workflow.

---

After presenting the AI Building Block Map, tell me:

> **Next step:** Download (or copy and save) the AI Building Block Map file. Then go to [Step 3 — Build Workflows](https://handsonai.info/business-first-ai-framework/build/) to build skills from your artifacts, generate your executable prompt, and everything else you need to run the workflow.

---

## General Instructions

- If the Workflow Definition is missing information needed for classification, ask me to clarify before guessing.
- If I mention I'm using Claude, note where Skills would be the appropriate building block for reusable routines.
- Explain your reasoning for any non-obvious classifications.
- Use plain language. Avoid jargon unless I introduced it.
```

## What This Prompt Produces

The **AI Building Block Map** contains:

- **Scenario summary** — workflow metadata from the Workflow Definition
- **Decomposition table** — every step with autonomy classification, decision points, failure modes, data flows, context needs, and AI building block mapping
- **Autonomy spectrum summary** — steps grouped by classification level
- **Step sequence and dependencies** — sequential vs. parallel execution paths
- **Prerequisites** — what must be in place before the workflow can run
- **Context inventory** — every piece of context the workflow needs, with status and key contents
- **Tools and connectors** — external integrations required

This AI Building Block Map is the input for [Step 3 — Build Workflows](../build/index.md), where you build skills, generate your Baseline Prompt, and everything else you need to run the workflow.
