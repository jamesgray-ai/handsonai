---
name: workflow-analysis
description: >
  Classify workflow steps on the autonomy spectrum, map them to AI building blocks, and produce
  a Workflow Analysis Document. Use when the user has a Workflow Blueprint and wants to analyze
  it for AI operationalization. This is Step 2 of 3 in the workflow deconstruction series.
---

# Workflow Analysis

Take a Workflow Blueprint, classify each step on the autonomy spectrum, map to AI building blocks, and produce a complete Workflow Analysis Document.

## Workflow

1. **Load Blueprint** — Read the Blueprint file from `outputs/[workflow-name]-blueprint.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Blueprint in `outputs/`.
2. **Confirm understanding** — Summarize the workflow name, step count, and outcome. Ask the user to confirm before proceeding.
3. **Classify each step** — For every refined step, determine:
   - **Autonomy level**: Human / AI-Deterministic / AI-Semi-Autonomous / AI-Autonomous
   - **AI building block(s)**: Prompt, Context, Skill, Agent, MCP, Project
   - **Tools and connectors**: External tools, APIs, integrations needed
   - **Human-in-the-loop gates**: Where human review is recommended
4. **Present mapping** — Show the classification as a clear table. Walk through reasoning for non-obvious classifications. Ask the user if they want to adjust anything.
5. **Generate Analysis Document** — After confirmation, produce the complete Workflow Analysis Document and write it to the output file.

## Output

Write the Workflow Analysis Document to `outputs/[workflow-name]-analysis.md` using the same workflow name from the Blueprint.

The Analysis Document must include:

### Scenario Summary
- Workflow name, description, outcome, trigger, type, business objective, current owner(s)

### Step-by-Step Decomposition Table

| # | Step | Action | Type | Decision Points | Failure Mode | Data In | Data Out | Context Needed | AI Building Block(s) |
|---|------|--------|------|----------------|-------------|---------|----------|----------------|---------------------|

### Autonomy Spectrum Summary
- Human steps, deterministic AI steps, semi-autonomous AI steps (with review gates), fully autonomous AI steps

### Step Sequence and Dependencies
- Sequential steps, parallel steps, critical path, dependency map

### Prerequisites
- What must be in place before the workflow can run
- External dependencies (accounts, access, data sources)

### Context Inventory

| Artifact | Description | Used By Steps | Status | Format | Key Contents |
|----------|-------------|---------------|--------|--------|--------------|

### Tools and Connectors Required

### Recommended Implementation Order
1. **Quick wins** — Deterministic steps automatable with Prompt or Context alone
2. **High-value semi-autonomous steps** — AI does most work, human review gate
3. **Complex agent steps** — Fully autonomous, requiring Agents/MCP/multi-tool orchestration

## Guidelines

- If the Blueprint is missing information needed for classification, ask the user to clarify
- If the user mentions they're using Claude, note where Skills are the appropriate building block
- Explain reasoning for non-obvious classifications
- After writing the Analysis Document, tell the user: "Analysis saved to `outputs/[name]-analysis.md`. Ready for Step 3 — Output Generation."
