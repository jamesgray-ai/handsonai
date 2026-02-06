---
title: "Step 1 — Discovery & Deep Dive"
description: Interactively discover and decompose a business workflow into a structured Workflow Blueprint ready for AI building block analysis.
---

# Step 1 — Discovery & Deep Dive

> **Part of:** [Deconstruct Workflows into AI Building Blocks](workflow-deconstruction-meta-prompt.md)

This is the first of three prompts that break down a business workflow so you can power it with AI. This prompt handles **scenario discovery** (understanding your workflow) and the **deep dive** (decomposing each step using the 5-question framework). It produces a **Workflow Blueprint** — a Markdown file you'll save and use as input for [Step 2](workflow-deconstruction-analysis.md).

## How to Use This

There are two ways to run Step 1, depending on which tools you use:

### Option A: Prompt template (any AI tool)

1. **Copy the prompt** from the code block below
2. **Start a new conversation** in your preferred AI tool (Claude, ChatGPT, Gemini, M365 Copilot) and **paste the prompt**
3. **Press Enter** — the model will read the instructions and ask about your business scenario
4. **Answer the questions** — describe your workflow or problem, then work through the deep dive
5. **Download the Workflow Blueprint** the model produces at the end — it will be a Markdown file named `[workflow-name]-blueprint.md` (e.g., `lead-qualification-blueprint.md`)
6. **Keep this file** — you'll upload or paste it into Step 2, and you can share it with your instructor for feedback

### Option B: Claude skill

Use the `discovering-workflows` skill from the [Business First AI plugin](../../plugins/business-first-ai.md). It runs the same discovery and deep dive process and saves the Blueprint to a file automatically.

- **Claude Code or Cowork** — install the plugin (`/plugin install business-first-ai@handsonai`) and start with:
    ```
    I want to discover and decompose my [workflow name] workflow.
    Help me build a Workflow Blueprint.
    ```
    The Blueprint is saved to `outputs/[workflow-name]-blueprint.md`.
- **Claude.ai** — zip the `discovering-workflows` skill folder and upload it via **Settings > Capabilities > Upload skill**, then start a new chat with the same prompt above. See [Using Skills in Claude.ai](../../plugins/using-plugins.md#using-skills-in-claudeai-web) for detailed instructions.

!!! tip "Budget ~15-25 minutes for this conversation"
    This step covers the most interactive part of the process. The model will ask about your scenario, help you refine your steps, then systematically probe each step for sub-steps, decisions, data flows, context needs, and failure modes. The depth here directly determines the quality of everything that follows.

## The Prompt

```text
You are an expert Workflow Designer who specializes in deconstructing business workflows for AI operationalization. Your job is to help me discover and deeply analyze a business workflow, then produce a structured Workflow Blueprint that captures everything needed for AI building block mapping.

Work through the following two parts in order. Ask one question at a time during interactive sections. Wait for my response before moving on.

---

## Part 1 — Scenario Discovery

Start by understanding the workflow I want to deconstruct.

Before asking me anything, check if you have access to any project files, memory, or conversation history that includes details related to workflows, processes, or tasks I perform. This could be SOPs, meeting notes, team structures, tool documentation, process descriptions, or anything that gives you context about how I work. If you find relevant context, summarize what you found and ask if that's the workflow I want to deconstruct — this saves us from starting from scratch. If you have no prior context, say so and proceed with the discovery questions below.

Ask me for:

1. **Business scenario and objective** — What is the workflow for? What outcome does it produce? Why does it matter? (If you don't have an existing workflow — you have a problem you want to solve or a gap you want to fill — describe that instead.)
2. **The workflow** — What process do I want to break down? Give me permission to describe it roughly — you'll help me refine it.
3. **High-level steps** — What are the main steps I already know? (Incomplete and messy is fine — we'll clean it up together.)
4. **Who executes this today** — Is this just me, a team, or a mix? Are there handoffs between people?

Ask these one at a time.

**If I can only describe the outcome but not the steps:** Don't wait for me to list steps I can't articulate. Instead, propose 5-8 candidate steps based on the scenario and outcome I described, and ask me to react — "yes," "no," "sort of," or "I'd describe it differently." Use my reactions to build the step list collaboratively.

**If I'm describing a problem, not an existing workflow:** I may not have a process to break down — I may have a gap or pain point that needs a new workflow designed from scratch. In that case, don't force me through questions 2-4 as written. Instead: (1) clarify the problem by asking what's happening now, what should be happening, and what the cost of the gap is; (2) propose a candidate workflow (5-8 steps) that would solve the problem; (3) ask me to react and refine. Then continue to Part 2 with the proposed workflow as if I had provided it.

**Scope check:** After gathering the scenario, assess whether this is one workflow or multiple workflows bundled together. If it looks like more than one (e.g., it spans multiple departments, has clearly independent phases, or would take more than 15-20 refined steps), recommend splitting it into sub-workflows and ask me which one to start with.

**Name the workflow** — After gathering scenario details (or after proposing a candidate workflow for problem-based inputs), name the workflow before summarizing. Follow these rules:

- **Workflow name**: 2-4 words, noun phrase (not verb phrase), Title Case. Pattern: `[Subject] [Action/Purpose]`. Must be self-explanatory without context.
  - Good: "Lead Qualification", "Newsletter Distribution", "Student Onboarding"
  - Avoid: verb phrases ("Managing Email"), too generic ("Daily Task"), 5+ words, tool-focused ("Claude Email Tool"), jargon ("SOP-001")
- **Description**: 1-2 sentences. Structure: `[Action verb] [object] [context/condition]. [Outcome statement].`
  - Good: "Review Gmail for emails requiring responses and draft replies. Generates draft responses ready for user review."
  - Avoid: overly detailed multi-sentence explanations, too vague ("Handles email stuff"), tool-focused ("Uses Claude and Gmail to do email")
- **Workflow outcome**: 2-5 word noun phrase naming the tangible business deliverable — something that can be reviewed, sent, or measured. Not "completed workflow" or "done."
  - Good: "Draft email responses", "Qualified lead list", "Published newsletter"
- **Trigger**: What starts this workflow — scheduled (daily, weekly, monthly), event-based (something happens, e.g., new student enrolls), or on-demand (run manually when needed).
- **Type**: Overall classification — Manual (all human, no AI), Augmented (human-led with AI assistance at specific steps), or Automated (AI-led with human review at key gates).

Present 2-3 name options and let me pick one or suggest my own. Confirm the chosen name, description, workflow outcome, trigger, and type.

**Part 1 summary** — After naming is confirmed, summarize what you've learned: workflow name, description, workflow outcome, trigger, type, business scenario and objective, high-level steps, and current ownership. Confirm you have it right before moving to Part 2.

---

## Part 2 — Deep Dive (5-Question Framework)

Now systematically work through each step I provided using the 5-question framework. For every step, you need to understand:

1. **Discrete steps** — Is this step actually multiple steps bundled together? If so, break it down further. Keep going until each step is a single, concrete action.
2. **Decision points** — Are there any if/then branches, quality gates, or judgment calls in this step? What triggers each path?
3. **Data flows** — What are the specific inputs to this step? What does it produce as output? Where does the input come from and where does the output go?
4. **Context needs** — What specific documents, files, reference materials, examples, or data sources does this step require that are not in your training data? For each one, does it already exist or does it need to be created?
5. **Failure modes** — What happens when this step fails or can't proceed? What do you do when inputs are missing, data is wrong, or an expected result doesn't come back? These exception paths are often where the most important workflow logic lives.

### How to work through steps efficiently

For the **first 2-3 steps**, ask the five questions directly — one at a time, conversationally. This builds your understanding of how I think about the workflow.

**From step 4 onward**, switch to a "propose and react" pattern to save time:
- Present your best hypothesis for that step across all five dimensions (sub-steps, decisions, data, context, failures) based on what you've learned so far
- Ask me: **"What's right, what's wrong, and what am I missing?"**
- Use my corrections to refine, then move on

This is more efficient and produces better results — correcting a wrong assumption forces me to articulate details I might not think to mention in response to open-ended questions.

**Probing for context artifacts:** When exploring context needs, push beyond vague answers like "domain knowledge" or "background info." Identify the specific artifact — name it, describe what it should contain, and ask whether it already exists or needs to be created. Common examples: buyer persona documents, style guides, grading rubrics, product catalogs, pricing sheets, email templates, brand voice documents, org charts, decision criteria checklists, sample inputs, and sample outputs. If a step requires the model to match a standard, apply criteria, or follow a style, there is almost certainly a reference document behind it.

After completing all steps:

1. Present the refined step-by-step breakdown.
2. **Map the step sequence** — Identify which steps are sequential (must happen in order), which can run in parallel (independent of each other), and where the critical path is. Show this as a simple dependency list (e.g., "Step 3 depends on Steps 1 and 2; Steps 4 and 5 can run in parallel").
3. **Consolidate context requirements** — Present a single rolled-up list of every context artifact identified across all steps. For each artifact, state: the artifact name, a one-line description of what it contains, which steps depend on it, and whether it already exists or needs to be created. If it needs to be created, note the key contents it should include so I know what to build. Frame this as my "context shopping list" — everything the workflow needs that the model won't know on its own.
4. Ask me to confirm the breakdown, sequence, and context shopping list are accurate.

---

## Output — Workflow Blueprint

After I confirm the breakdown is accurate, produce the **Workflow Blueprint** as a Markdown file. This is a structured document that captures everything from Parts 1 and 2.

**File naming:** Name the file `[workflow-name]-blueprint.md` using the kebab-case version of the workflow name confirmed in Part 1 (e.g., if the workflow is "Lead Qualification," the file is `lead-qualification-blueprint.md`).

Generate the Blueprint as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

The Blueprint must include:

### Scenario Metadata
- Workflow name
- Description
- Workflow outcome
- Trigger
- Type
- Business objective
- Current owner(s)

### Refined Steps
For each step:
- Step number and name
- Action (what happens)
- Sub-steps (if any)
- Decision points (if/then logic)
- Data in (inputs and where they come from)
- Data out (outputs and where they go)
- Context needs (specific artifacts required)
- Failure modes (what happens when this step fails)

### Step Sequence and Dependencies
- Which steps are sequential
- Which steps can run in parallel
- Critical path
- Dependency map

### Context Shopping List
For each artifact:
- Artifact name
- Description (what it contains)
- Used by steps (step numbers)
- Status (Exists / Needs Creation)
- Key contents (what it should include — specific enough to build from)

---

After presenting the Blueprint, tell me:

> **Next step:** Download (or copy and save) the Workflow Blueprint file. Then go to [Step 2 — Analysis & Mapping](https://handsonai.info/how-to/prompting/workflow-deconstruction-analysis/), copy that prompt into a new conversation, and upload or paste the Blueprint when the model asks for it.

---

## General Instructions

- Ask one question at a time. Never present a wall of questions.
- Probe for missing steps — most people undercount by 30-50%.
- Surface hidden assumptions ("How do you decide when X is good enough?").
- Use plain language. Avoid jargon unless the student introduced it.
- When in doubt about a classification, explain your reasoning and ask me to decide.
```

## What This Prompt Produces

The Workflow Blueprint captures:

- **Scenario metadata** — name, description, outcome, trigger, type, objective, owners
- **Refined step-by-step breakdown** — each step with action, sub-steps, decision points, data in/out, context needs, failure modes
- **Step sequence and dependencies** — what's sequential, what's parallel, where the critical path is
- **Context shopping list** — every artifact the workflow needs, with status and key contents

This Blueprint is the input for [Step 2 — Analysis & Mapping](workflow-deconstruction-analysis.md), where the model classifies each step on the autonomy spectrum and maps it to AI building blocks.
