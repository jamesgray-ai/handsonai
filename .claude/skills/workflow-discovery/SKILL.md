---
name: workflow-discovery
description: >
  Interactively discover and decompose a business workflow into a structured Workflow Blueprint.
  Use when the user wants to deconstruct a workflow, break down a business process, or start
  the workflow deconstruction process. This is Step 1 of 3 in the workflow deconstruction series.
---

# Workflow Discovery

Interactively discover a business workflow and decompose every step into a structured Workflow Blueprint using the 4-question framework + failure modes.

## Workflow

1. **Scenario discovery** — Ask about the business scenario, objective, high-level steps, and ownership. One question at a time. If the user describes a problem instead of a workflow, propose a candidate workflow for them to react to.
2. **Scope check** — Assess whether this is one workflow or multiple bundled together. If multiple, recommend splitting and ask which to start with.
3. **Name the workflow** — Present 2-3 name options following naming conventions (2-4 word noun phrase, Title Case). Confirm name, description, outcome, trigger, and type.
4. **Deep dive** — Work through each step using the 4-question framework + failure modes:
   - Discrete steps (is this actually multiple steps?)
   - Decision points (if/then branches, quality gates)
   - Data flows (inputs, outputs, sources, destinations)
   - Context needs (specific documents, files, reference materials)
   - Failure modes (what happens when this step fails)
5. **Propose and react** — For steps 4+, propose a hypothesis across all 5 dimensions and ask "What's right, what's wrong, what am I missing?" instead of asking each question individually.
6. **Map sequence** — After all steps, identify sequential vs. parallel steps and the critical path.
7. **Consolidate context** — Present a rolled-up "context shopping list" of every artifact the workflow needs.
8. **Generate Blueprint** — Produce the structured Workflow Blueprint and write it to the output file.

## Output

Write the Workflow Blueprint to `outputs/[workflow-name]-blueprint.md` where `[workflow-name]` is the kebab-case workflow name (e.g., `lead-qualification`).

The Blueprint must include:

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
- After writing the Blueprint file, tell the user: "Blueprint saved to `outputs/[name]-blueprint.md`. Ready for Step 2 — Analysis & Mapping."
