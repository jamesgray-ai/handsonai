---
name: run
description: >
  This skill should be used when the user has built and tested workflow artifacts and wants a Run Guide
  for deploying and operating their AI workflow. It generates a plain-language guide
  with setup steps, deployment patterns, and sharing instructions — tailored to the user's platform and
  build path. This is Step 6 (Run) of the Business-First AI Framework.
user-invocable: true
---

# Workflow Run Guide

Generate a Run Guide for deploying, executing, and testing an AI workflow. The Run Guide bridges the gap between "artifacts exist" and "workflow is running."

**Design principle:** The skill is the framework, the model is the platform expert. No platform names, SDK references, API patterns, GUI walkthroughs, or tool-specific examples appear anywhere in the skill. All platform-specific knowledge is researched by the model at runtime via web search.

**Role:** You are an **Agentic AI Architect**. Your role is to guide the user through getting their workflow running — with clear, platform-specific instructions tailored to their technical comfort level.

## Workflow

#### Step 1 — Determine Build Path and Load Context

Determine which build path the user followed:

- **Path 1 (Model-built):** The model generated platform artifacts during the Build phase. Look for generated artifacts in the working directory and load the Building Block Spec from `outputs/[workflow-name]-building-block-spec.md`.
- **Path 2 (Manual build):** The user chose to build artifacts themselves using the spec as a guide. Load the Building Block Spec from `outputs/[workflow-name]-building-block-spec.md`.
- **Path 3 (Guided-mode):** The model generated GUI instruction documents during the Build phase (for guided-mode platforms like Copilot Studio, Workspace Studio, ChatGPT Agent Mode). The `mode` field in the Building Block Spec indicates `guided`.

If the user specifies a file path, use that. Otherwise, look for the most recent Building Block Spec in `outputs/` and check conversation context for which path was chosen.

If unclear, ask: "Did the model generate your workflow artifacts (Path 1), are you building them yourself from the spec (Path 2), or did the model produce GUI instruction documents for a guided-mode platform (Path 3)?"

#### Step 2 — Generate Run Guide

Generate the Run Guide based on the build path.

**Variant A: Model-built artifacts (Path 1)**

Walk the user through getting the workflow running. Use the platform and code comfort (resolved during artifact generation) to tailor every instruction to their specific setup. Use web search to verify current platform steps. Write in plain language — assume no technical background unless code comfort was confirmed.

The Run Guide covers four sections:

**A. What was built** — List every artifact produced, what it does, and where it was saved. Use a simple table:

| Artifact | What it does | Location |
|----------|-------------|----------|

**B. Setup steps** — Numbered, platform-specific instructions for getting each artifact into the right place. Research the platform's current UI/workflow via web search. For each step:
- Tell the user exactly where to go (menu paths, button names, URLs)
- Tell them exactly what to do (paste, upload, configure, connect)
- Tell them what they should see when it's working (confirmation messages, visual indicators)
- If a step requires technical knowledge beyond the user's code comfort level, flag it and offer to walk through it interactively

**C. First run** — A guided test run:
- Provide a sample input the user can try (based on the workflow's Input Requirements from the spec)
- Walk through what should happen at each step
- Explain what good output looks like
- List common first-run issues and how to fix them

**D. What to do next** — Brief guidance on:
- How to run the workflow again in the future (the repeatable trigger)
- How to share it with team members (if shareability was confirmed during Build)
- When to revisit and improve (signs the workflow needs updating)
- For organizational workflows: **Change management** — who needs training, what communication is needed, and **Rollout plan** — pilot first or full rollout?

**Variant B: Manual build (Path 2)**

Provide a Construction Guide instead of setup instructions. The user will build the artifacts themselves.

**A. What to build** — List every artifact from the spec, what it does, and the recommended file format for the user's platform. Use a table:

| Artifact | Purpose | Format | Priority |
|----------|---------|--------|----------|

**B. Build sequence** — Ordered implementation steps following the spec's recommended implementation order. For each artifact:
- What to create (from the spec's generation-ready detail)
- Platform-specific format guidance (file type, frontmatter requirements, directory conventions)
- Key content to include (inputs, outputs, decision logic from the spec)
- How to test it in isolation before connecting to other artifacts

**C. First run** — Same as Variant A: guided test run with sample input.

**D. What to do next** — Same as Variant A: repeatable trigger, sharing, iteration guidance.

**Variant C: Guided-mode platforms (Path 3)**

The Build phase produced GUI instruction documents rather than deployable code artifacts. The Run Guide walks the user through following these instructions.

**A. What was built** — List the instruction documents produced, what each covers, and which platform screens they reference. Use a table:

| Document | What it covers | Platform area |
|----------|---------------|---------------|

**B. Setup steps** — Walk through following the GUI instructions in order:
- Which platform screen to open first
- What to configure at each step (referencing the instruction document)
- What to verify after each configuration step (confirmation messages, visual indicators)
- If a step requires permissions or admin access the user may not have, flag it

**C. First run** — Same as Variant A: guided test with sample input, expected behavior at each step, what good output looks like, common first-run issues.

**D. What to do next** — How to modify the configuration later, share with team members (if the platform supports it), when to revisit and update, change management notes for organizational workflows.

Present the Run Guide directly in the conversation. Also save it to `outputs/[workflow-name]-run-guide.md` so the user has a reference they can follow later or share with teammates.

## Outputs

### `outputs/[workflow-name]-run-guide.md` — Run Guide

Plain-language guide for getting the workflow running. Three variants:
- **Model-built:** Artifact inventory, step-by-step setup instructions tailored to the user's platform, a guided first-run test with sample input, and next steps for ongoing use and team sharing.
- **Manual build:** Construction Guide with artifact list, build sequence with platform-specific format guidance, first-run test, and next steps.
- **Guided-mode:** Instruction walkthrough, step-by-step GUI setup guide, first-run test, and next steps.

## Guidelines

- Use plain language; avoid jargon unless the user introduced it
- After writing the Run Guide, tell the user: "Run Guide saved to `outputs/[name]-run-guide.md`."
- Summarize all deliverables at the end so the user has a clear inventory of everything produced across Steps 3-6 (Design, Build, Test, and Run)
- After the summary, prompt for SOP creation: "To document this workflow as a Standard Operating Procedure (SOP) for your team, run `/ai-registry:writing-sops`. The SOP captures what the workflow does, when to trigger it, what inputs it needs, and who's responsible — useful for onboarding teammates and maintaining the workflow over time."
- Use web search to verify current platform setup steps — platform UIs change frequently
