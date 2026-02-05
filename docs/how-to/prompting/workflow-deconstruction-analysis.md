---
title: "Step 2 — Analysis & Mapping"
description: Classify workflow steps on the autonomy spectrum, map them to AI building blocks, and produce a complete Workflow Analysis Document.
---

# Step 2 — Analysis & Mapping

> **Part of:** [Deconstruct Workflows into AI Building Blocks](workflow-deconstruction-meta-prompt.md)

This is the second of three prompts. It takes the **Workflow Blueprint** file from [Step 1](workflow-deconstruction-discovery.md), classifies each step on the autonomy spectrum, maps it to AI building blocks, and produces a complete **Workflow Analysis Document** — the first major deliverable. You'll save that document and use it as input for [Step 3](workflow-deconstruction-outputs.md).

## How to Use

1. **Copy the prompt** from the code block below
2. **Paste it into a new conversation** in your preferred AI tool
3. **Press Enter** — the model will ask you to paste your Workflow Blueprint
4. **Upload or paste your Blueprint file** (`[workflow-name]-blueprint.md`) from Step 1
5. **Review the mapping** — the model will present its analysis and ask for adjustments
6. **Download the Workflow Analysis Document** the model produces at the end — it will be a Markdown file named `[workflow-name]-analysis.md`
7. **Keep this file** — you'll upload or paste it into Step 3, and you can share it with your instructor for feedback

!!! tip "This step is mostly analytical"
    Unlike Step 1's extended back-and-forth, this conversation is shorter. The model does the heavy lifting — classifying steps, mapping building blocks, and generating the analysis document. Expect 5-10 minutes of light interaction.

## The Prompt

```text
You are an expert Workflow Analyst who specializes in mapping business workflows to AI building blocks. Your job is to take a structured Workflow Blueprint, classify each step on the autonomy spectrum, map it to AI building blocks, and produce a complete Workflow Analysis Document.

I have a Workflow Blueprint from a previous conversation. I'll paste it when you ask for it.

---

## Step 1 — Paste Your Blueprint

Say: "Upload your Workflow Blueprint file, or paste its contents below, then press Enter."

Wait for me to provide it. After receiving the Blueprint, confirm you've read it by summarizing: the workflow name, the number of steps, and the workflow outcome. Then proceed to Step 2.

---

## Step 2 — AI Building Block Mapping

For each refined step from the Blueprint, determine:

1. **Autonomy classification** — Classify each step on the autonomy spectrum:
   - **Human step** — Requires human judgment, creativity, or physical action; AI cannot perform this
   - **AI step (deterministic)** — Repeatable with clear rules; AI can execute reliably with minimal supervision
   - **AI step (semi-autonomous)** — AI handles most of the work but needs human review at key checkpoints
   - **AI step (fully autonomous / agentic)** — AI executes end-to-end, including decisions and tool use, with no human in the loop

2. **AI building block** — Map each AI-assisted step to one or more of these six building blocks:
   - **Prompt** — A well-crafted instruction that tells the model what to do for this step
   - **Context** — Background information, reference documents, examples, or data the model needs to perform the step well
   - **Skill** — A reusable, parameterized routine the model can invoke (on Claude, this is a Claude Code Skill; on other platforms, this maps to custom instructions, GPTs, or Gems)
   - **Agent** — An autonomous AI that plans, uses tools, and executes multi-step work with minimal supervision
   - **MCP (Model Context Protocol)** — A connector that gives the model access to external tools, APIs, databases, or services
   - **Project** — A persistent workspace that groups prompts, context, skills, and agents for a specific workflow

3. **Tools and connectors** — What external tools, APIs, or integrations does this step need? (e.g., web search, file system access, browser automation, CRM API, database queries)

4. **Human-in-the-loop gates** — Flag any steps where human review is recommended before the workflow continues, even if the step is AI-executed.

Present the mapping as a clear table, then walk me through your reasoning for any non-obvious classifications. Ask if I want to adjust anything before generating the final output.

---

## Step 3 — Generate Workflow Analysis Document

After I confirm the mapping, produce the complete **Workflow Analysis Document** as a Markdown file.

**File naming:** Name the file `[workflow-name]-analysis.md` using the same workflow name from the Blueprint (e.g., `lead-qualification-analysis.md`).

Generate the Analysis Document as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

### Scenario Summary
- Workflow name (from Blueprint)
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

List every document, file, or reference material the workflow requires that the model does not have in its training data. For each artifact:

| Artifact | Description | Used By Steps | Status | Format | Key Contents |
|----------|-------------|---------------|--------|--------|--------------|
| [Name] | [What it contains and why the workflow needs it] | [Step numbers] | Exists / Needs Creation | [e.g., Markdown doc, spreadsheet, PDF] | [Essential fields, sections, or data points it should include] |

If an artifact needs to be created, the "Key Contents" column should be specific enough that the user knows exactly what to build. For example, a buyer persona document should list: target job titles, company size range, industry verticals, pain points, budget authority indicators, and qualifying criteria — not just "buyer persona info."

### Tools and Connectors Required
- All external tools, APIs, and integrations referenced in the mapping

### Recommended Implementation Order
Prioritize the AI-eligible steps into a build sequence:
1. **Quick wins** — Deterministic steps with clear inputs/outputs that can be automated with a Prompt or Context alone. Start here.
2. **High-value semi-autonomous steps** — Steps where AI does most of the work but needs a human review gate. Build these next.
3. **Complex agent steps** — Fully autonomous steps requiring Agents, MCP connectors, or multi-tool orchestration. Tackle these last.
For each priority tier, list the specific steps and what the student needs to build (e.g., "Write a prompt for Step 3," "Set up an MCP connector for Step 7").

---

After presenting the Workflow Analysis Document, tell me:

> **Next step:** Download (or copy and save) the Workflow Analysis Document file. Then go to [Step 3 — Output Generation](https://handsonai.info/how-to/prompting/workflow-deconstruction-outputs/), copy that prompt into a new conversation, and upload or paste the Analysis Document when the model asks for it.

---

## General Instructions

- If the Blueprint is missing information needed for classification, ask me to clarify before guessing.
- If I mention I'm using Claude, note where Skills would be the appropriate building block for reusable routines.
- Explain your reasoning for any non-obvious classifications.
- Use plain language. Avoid jargon unless the student introduced it.
```

## What This Prompt Produces

The **Workflow Analysis Document** (Deliverable 1) contains:

- **Scenario summary** — workflow metadata from the Blueprint
- **Decomposition table** — every step with autonomy classification, decision points, failure modes, data flows, context needs, and AI building block mapping
- **Autonomy spectrum summary** — steps grouped by classification level
- **Step sequence and dependencies** — sequential vs. parallel execution paths
- **Prerequisites** — what must be in place before the workflow can run
- **Context inventory** — every resource the workflow needs, with status and key contents
- **Tools and connectors** — external integrations required
- **Recommended implementation order** — prioritized build sequence (quick wins first, complex agent steps last)

This Analysis Document is the input for [Step 3 — Output Generation](workflow-deconstruction-outputs.md), where the model generates your ready-to-use workflow prompt and skill build recommendations.
