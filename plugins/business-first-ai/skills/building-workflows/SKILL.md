---
name: building-workflows
description: >
  Turn your AI Building Block Map into a Baseline Workflow Prompt and build guidance. If the user
  has already built skills, generates a skill-aware prompt that references them instead of spelling
  out those steps inline. Use when the user has a completed AI Building Block Map and wants to
  generate the prompt. This is the Build step in the workflow deconstruction series.
---

# Workflow Build

Take an AI Building Block Map and produce the Build deliverable: a Baseline Workflow Prompt with Recommended Implementation Order and Where to Run. If the user has already built skills, the prompt references them instead of spelling out those steps inline.

## Workflow

1. **Load AI Building Block Map** — Read the AI Building Block Map from `outputs/[workflow-name]-building-blocks.md`. If the user specifies a file path, use that. Otherwise, look for the most recent AI Building Block Map in `outputs/`.
2. **Confirm understanding** — Summarize the workflow name, step count, how many are AI-eligible, and the building blocks identified. Ask the user to confirm before proceeding.
3. **Clarify if needed** — If anything in the AI Building Block Map is ambiguous, ask before generating. Maximum 1-2 clarifying questions.
3b. **Check for existing skills** — Ask: "Did you build any skills for this workflow? If yes, list each skill name and which steps it covers." If skills exist, note them for prompt generation — replace covered steps with skill invocations instead of inline instructions.
4. **Check for existing AI instructions** — Before generating, check the Context Inventory for any artifacts that contain existing prompt instructions, project instructions, or system prompts from AI tools the user already uses for this workflow. These contain workflow logic that must be included in the Baseline Prompt — not referenced, but actually included. If such artifacts exist but their content is not in the AI Building Block Map, ask the user to paste or upload them.
5. **Generate Baseline Workflow Prompt** — Produce a ready-to-use, self-contained prompt and write it to the output file. Include a Where to Run section advising where to run the prompt (normal chat vs. project). For any step covered by a skill the user provided, replace the inline instructions with a brief description of the task (the skill handles the details automatically). Keep full instructions only for steps NOT covered by a skill.
6. **Write SOP to Notion (if available)** — After the prompt is generated, check if the Notion MCP server is accessible AND this workflow was registered in the Discover step. If so, offer to write the workflow SOP to the Notion page using the `writing-workflow-sops` approach: pass the workflow name to locate the page, use the Baseline Prompt's procedure steps as the primary input, and write the formatted SOP to the page body. If Notion is not available or the workflow was not registered, skip this step.

## Outputs

Write one file:

### `outputs/[workflow-name]-prompt.md` — Baseline Workflow Prompt

Structure:
- **Title and Purpose** — Workflow name, description, outcome, when to use
- **Instructions** — Numbered steps, each labeled (AI) or (Human). AI steps get direct commands. Human steps describe what the human does and hands back. Include branching logic.
- **Input Requirements** — What the user provides when running the prompt, with format specs
- **Context Requirements** — Reference materials, files, or data to attach
- **Output Format** — What the prompt produces, with structure specs

The prompt must be: self-contained, specific, version-control ready, team-adoption ready.

**Self-contained means:** The prompt contains every instruction the model needs to execute the workflow. It never says "open this project" or "follow those instructions." If existing AI instructions drive a step, those instructions are written into the prompt.

**Where to Run** — Include a section advising where to run the prompt (normal chat vs. project), which files to attach or pre-load, and why. The prompt instructions are the same regardless of where you run it — the project provides file staging convenience, not workflow logic.

Recommend where the Baseline Workflow Prompt should be run:

- **Normal chat** — recommended when the workflow runs infrequently (monthly or less), few or no context files are needed (0-2 files), all context can be provided inline each time, or the workflow is a one-off or experimental process.
- **Project workspace** — recommended when the workflow runs frequently (weekly or more), multiple context files are needed (3+ files), the same reference materials are used every run, conversation memory across runs would be valuable, or multiple people will run the same workflow.

State the recommendation, the reasoning, and list the specific context files to attach (chat) or pre-load in the project.

**Important:** The Baseline Workflow Prompt is always self-contained — it contains all workflow logic regardless of where you run it. A project provides pre-loaded context and conversation memory, but never contains the workflow logic. The prompt IS the workflow.

### Recommended Implementation Order

Include in the prompt output file:

1. **Quick wins** — Deterministic steps with clear inputs/outputs that can be automated with a Prompt or Context alone. Start here.
2. **High-value semi-autonomous steps** — Steps where AI does most of the work but needs a human review gate. Build these next.
3. **Complex agent steps** — Fully autonomous steps requiring Agents, MCP connectors, or multi-tool orchestration. Tackle these last.

For each priority tier, list the specific steps and what needs to be built (e.g., "Write a prompt for Step 3," "Set up an MCP connector for Step 7").

## Guidelines

- If the user mentions Claude, note where Claude Code Skills are the appropriate implementation
- Use plain language; avoid jargon unless the user introduced it
- After writing the file, tell the user: "Output saved to `outputs/[name]-prompt.md`. Your Baseline Workflow Prompt is ready."
- Summarize the three files produced across Deconstruct and Build so the user has a clear inventory of their deliverables
