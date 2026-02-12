---
name: deconstructing-workflows
description: >
  Interactively deconstruct a business workflow into a structured Workflow Definition. Use when
  the user wants to break down a workflow, decompose a business process, or deeply analyze a
  workflow's steps, decisions, data flows, and failure modes. This is the Deconstruct step.
---

# Workflow Deconstruction

Interactively discover a business workflow and decompose every step into a structured Workflow Definition using the 5-question framework.

## Workflow

1. **Scenario discovery** — Ask about the business scenario, objective, high-level steps, and ownership. One question at a time. If the user describes a problem instead of a workflow, propose a candidate workflow for them to react to.
2. **Scope check — one trigger, one deliverable** — A workflow has exactly one trigger (what kicks it off) and one deliverable (the tangible output). Test for multiple workflows by checking:
   - **Triggers**: Multiple independent starting points? (e.g., "when a lead comes in" vs. "end of each week") → separate workflows
   - **Deliverables**: Distinct outputs at different points? If someone receives a deliverable midway and the process continues toward a different output → workflow boundary
   - **Timeframes**: Parts run on different schedules (daily vs. weekly), or significant waits between phases → likely separate workflows
   - **Step count**: Would this expand to 15+ refined steps? → may be multiple workflows
   If multiple workflows are detected: map out each one (working name, trigger, deliverable), present the breakdown, confirm boundaries with the user, and ask which to deconstruct first. Proceed with only the chosen workflow.
3. **Name the workflow** — Present 2-3 name options following naming conventions (2-4 word noun phrase, Title Case). Confirm name, description, outcome, trigger, and type.
4. **Register to Workflows database (if Notion is available)** — After naming is confirmed, check if the Notion MCP server is accessible. If so, create a row in the Workflows database with: Name, Description, Process Outcome, Type, Trigger, Status = "Under Development". Ask the user which Business Process domain this belongs to (or leave blank). If Notion is not available, skip this step silently and continue to the deep dive.
5. **Deep dive** — Work through each step using the 5-question framework:
   - Discrete steps (is this actually multiple steps?)
   - Decision points (if/then branches, quality gates)
   - Data flows (inputs, outputs, sources, destinations)
   - Context needs (specific documents, files, reference materials)
   - Failure modes (what happens when this step fails)
   When probing context needs, push beyond vague answers — identify the specific artifact. For any step where AI is already being used, ask specifically for existing prompt instructions, project instructions, or system prompts — these contain workflow logic that must be included in the Baseline Prompt.
6. **Propose and react** — For steps 4+, propose a hypothesis across all 5 dimensions and ask "What's right, what's wrong, what am I missing?" instead of asking each question individually.
7. **Map sequence** — After all steps, identify sequential vs. parallel steps and the critical path.
8. **Consolidate context** — Present a rolled-up "context shopping list" of every piece of context the workflow needs — documents, data, rules, examples, and any other knowledge from the user's domain that the model doesn't have.
9. **Generate Workflow Definition** — Produce the structured Workflow Definition and write it to the output file.

## Output

Write the Workflow Definition to `outputs/[workflow-name]-definition.md` where `[workflow-name]` is the kebab-case workflow name (e.g., `lead-qualification`).

The Workflow Definition must include:

### Scenario Metadata
- Workflow name, description, outcome, trigger, type, business objective, current owner(s)

### Refined Steps
For each step: number, name, action, sub-steps, decision points, data in/out, context needs, failure modes

### Step Sequence and Dependencies
- Sequential steps, parallel steps, critical path, dependency map

### Context Shopping List
For each artifact: name, description, used by steps, status (Exists/Needs Creation), key contents

## Guidelines

- Ask one question at a time — never present a wall of questions
- Probe for missing steps — most people undercount by 30-50%
- Surface hidden assumptions ("How do you decide when X is good enough?")
- Use plain language; avoid jargon unless the user introduced it
- Push beyond vague context answers like "domain knowledge" — identify the specific artifact
- After writing the Workflow Definition file, tell the user: "Workflow Definition saved to `outputs/[name]-definition.md`. Ready for Step 3 — Build."
