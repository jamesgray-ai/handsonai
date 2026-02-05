---
name: workflow-output-generation
description: >
  Generate a Baseline Workflow Prompt and Skill Build Recommendations from a Workflow Analysis
  Document. Use when the user has a completed Analysis Document and wants the final deliverables.
  This is Step 3 of 3 in the workflow deconstruction series.
---

# Workflow Output Generation

Take a Workflow Analysis Document and produce two deliverables: a Baseline Workflow Prompt and Skill Build Recommendations.

## Workflow

1. **Load Analysis Document** — Read the Analysis Document from `outputs/[workflow-name]-analysis.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Analysis Document in `outputs/`.
2. **Confirm understanding** — Summarize the workflow name, step count, how many are AI-eligible, and the recommended implementation order. Ask the user to confirm before proceeding.
3. **Clarify if needed** — If anything in the Analysis Document is ambiguous, ask before generating. Maximum 1-2 clarifying questions.
4. **Generate Baseline Workflow Prompt** — Produce a ready-to-use prompt and write it to the output file.
5. **Generate Skill Build Recommendations** — Produce skill specs and write them to the output file.

## Outputs

Write two files:

### `outputs/[workflow-name]-prompt.md` — Baseline Workflow Prompt

Structure:
- **Title and Purpose** — Workflow name, description, outcome, when to use
- **Instructions** — Numbered steps, each labeled (AI) or (Human). AI steps get direct commands. Human steps describe what the human does and hands back. Include branching logic.
- **Input Requirements** — What the user provides when running the prompt, with format specs
- **Context Requirements** — Reference materials, files, or data to attach
- **Output Format** — What the prompt produces, with structure specs

The prompt must be: self-contained, specific, version-control ready, team-adoption ready.

### `outputs/[workflow-name]-skill-recs.md` — Skill Build Recommendations

For each recommended skill:
- **Skill Name** — 2-4 words, lowercase with hyphens
- **Purpose** — What it does, when to invoke it
- **Inputs** — What it needs, format requirements
- **Outputs** — What it produces, structure and format
- **Workflow Steps** — Specific steps it executes
- **Replaces Steps** — Which baseline prompt step numbers it replaces, how the invocation changes
- **Integration Points** — External tools, APIs, MCP servers
- **Priority** — High / Medium / Low
- **Quick Start Prompt** — One-sentence invocation

Present skills in priority order. If no steps qualify as good skill candidates, explain why.

## Guidelines

- If the user mentions Claude, note where Claude Code Skills are the appropriate implementation
- Use plain language; avoid jargon unless the user introduced it
- After writing both files, tell the user: "Outputs saved to `outputs/[name]-prompt.md` and `outputs/[name]-skill-recs.md`. Your workflow deconstruction is complete."
- Summarize the three files produced across all three steps so the user has a clear inventory of their deliverables
