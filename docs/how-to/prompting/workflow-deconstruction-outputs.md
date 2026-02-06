---
title: "Step 3 — Output Generation"
description: Generate a ready-to-use Baseline Workflow Prompt and Skill Build Recommendations from your Workflow Analysis Document.
---

# Step 3 — Output Generation

> **Part of:** [Deconstruct Workflows into AI Building Blocks](workflow-deconstruction-meta-prompt.md)

This is the final prompt in the three-part series. It takes the **Workflow Analysis Document** from [Step 2](workflow-deconstruction-analysis.md) and produces your two remaining deliverables: a **Baseline Workflow Prompt** you can paste into any AI tool to run the workflow, and **Skill Build Recommendations** showing which reusable skills to build and what they replace.

## How to Use This

There are two ways to run Step 3, depending on which tools you use:

### Option A: Prompt template (any AI tool)

1. **Copy the prompt** from the code block below
2. **Paste it into a new conversation** in your preferred AI tool
3. **Press Enter** — the model will ask you to upload or paste your Workflow Analysis Document
4. **Upload or paste your Analysis Document file** (`[workflow-name]-analysis.md`) from Step 2
5. **Review the outputs** — the model may ask 1-2 clarifying questions, then generates both deliverables
6. **Download both files** — the Baseline Workflow Prompt and Skill Build Recommendations

### Option B: Claude skill

Use the `generating-workflow-outputs` skill from the [Business First AI plugin](../../plugins/business-first-ai.md). It reads the Analysis Document from Step 2 and generates both deliverables automatically.

- **Claude Code or Cowork** — install the plugin (`/plugin install business-first-ai@handsonai`) and start with:
    ```
    Generate the Baseline Workflow Prompt and Skill Build Recommendations
    from the analysis in outputs/[workflow-name]-analysis.md.
    ```
    Both deliverables are saved to the `outputs/` directory.
- **Claude.ai** — zip the `generating-workflow-outputs` skill folder and upload it via **Settings > Capabilities > Upload skill**, then start a new chat with: "Generate a Baseline Workflow Prompt and Skill Build Recommendations from this analysis." Upload or paste your Analysis Document when prompted. See [Using Skills in Claude.ai](../../plugins/using-plugins.md#using-skills-in-claudeai-web) for detailed instructions.

!!! tip "This step is mostly generative"
    The heavy analytical work is done. The model reads your Analysis Document and produces two structured outputs with minimal interaction. Expect 5-10 minutes.

## The Prompt

```text
You are an expert Prompt Engineer who writes clear, precise instructions that language models can execute reliably. Your job is to take a Workflow Analysis Document and produce two deliverables: a Baseline Workflow Prompt and Skill Build Recommendations.

I have a Workflow Analysis Document from a previous conversation. I'll paste it when you ask for it.

---

## Part 1 — Paste Your Analysis Document

Say: "Upload your Workflow Analysis Document file, or paste its contents below, then press Enter."

Wait for me to provide it. After receiving the document, confirm you've read it by summarizing: the workflow name, the number of steps, how many are AI-eligible, and the recommended implementation order. Then proceed to Part 2.

If anything in the Analysis Document is ambiguous or seems incomplete, ask me to clarify before generating outputs. Do not guess at missing information.

---

## Part 2 — Generate Baseline Workflow Prompt

Generate a ready-to-use Markdown prompt that someone could paste into any AI tool to execute this workflow. This is the **baseline version** — it spells out every step in full so it works on any platform (Claude, ChatGPT, Gemini, M365 Copilot). As the user builds skills from the recommendations below, they'll update this prompt to invoke those skills instead of repeating the logic inline.

Structure it as:

**Title and Purpose**
- Workflow name and description (from the Analysis Document)
- Workflow outcome — what this workflow produces
- When to use it

**Instructions**
- Numbered steps, each clearly labeled as (AI) or (Human)
- For each AI step: specific instructions the model should follow, written as direct commands
- For each Human step: clear description of what the human does and what they hand back to the model
- Include the decision logic for any branching steps

**Input Requirements**
- What the user needs to provide when they run this prompt
- Format specifications for each input

**Context Requirements**
- What reference materials, files, or data should be attached or available
- Where to find them, or what to include if creating them from scratch

**Output Format**
- Exactly what the prompt should produce
- Structure and format specifications

The prompt should be:
- Self-contained (someone unfamiliar with the analysis can use it)
- Specific enough to produce consistent results
- Ready for version control (clean Markdown, no ambiguity)
- Ready for team adoption (clear enough that a colleague could run it)

**File naming:** Name the file `[workflow-name]-prompt.md` using the same workflow name from the Analysis Document (e.g., `lead-qualification-prompt.md`).

Generate the prompt as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

---

## Part 3 — Generate Skill Build Recommendations

Based on the Workflow Analysis Document, recommend which reusable skills I should build. Focus on steps that are:
- Repeatable (executed frequently with similar patterns)
- Mechanical (follow clear rules, not creative judgment)
- Consistent (should produce the same output structure every time)

For each recommended skill, provide:

**Skill Name**
- A short, action-oriented name (2-4 words, lowercase with hyphens)

**Purpose**
- What this skill does in 1-2 sentences
- When to invoke it (trigger scenarios)

**Inputs**
- What information the skill needs to run
- Format requirements

**Outputs**
- What the skill produces
- Structure and format

**Workflow Steps**
- The specific steps the skill executes (derived from the workflow analysis)

**Replaces Steps**
- Which step numbers from the Baseline Workflow Prompt this skill will replace (e.g., "Steps 3-5")
- Brief note on how the prompt invocation changes (e.g., "Replace steps 3-5 with: /validate-prospect-fit")

**Integration Points**
- External tools, databases, or APIs the skill connects to
- MCP servers it would use (if any)

**Priority**
- High / Medium / Low based on frequency of use and automation value

**Quick Start Prompt**
- A one-sentence prompt the user could paste to invoke this skill

Present skills in priority order (highest value first). If no steps qualify as good skill candidates, explain why and note that the workflow may be better served by a single prompt or agent rather than reusable skills.

**File naming:** Name the file `[workflow-name]-skill-recs.md` using the same workflow name (e.g., `lead-qualification-skill-recs.md`).

Generate the recommendations as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

---

After presenting both files, summarize what I now have:

> **Workflow deconstruction complete.** You now have four files:
>
> 1. `[workflow-name]-blueprint.md` — your Workflow Blueprint (from Step 1)
> 2. `[workflow-name]-analysis.md` — your Workflow Analysis Document (from Step 2)
> 3. `[workflow-name]-prompt.md` — your Baseline Workflow Prompt (ready to use)
> 4. `[workflow-name]-skill-recs.md` — your Skill Build Recommendations (what to build next)
>
> Start by running the baseline prompt on a real scenario. Then build skills in priority order from the recommendations.

---

## General Instructions

- If I mention I'm using Claude, note where Claude Code Skills are the appropriate implementation. On other platforms, map to custom instructions, GPTs, or Gems.
- Use plain language. Avoid jargon unless the student introduced it.
- If anything is ambiguous in the Analysis Document, ask me before generating.
```

## What This Prompt Produces

### Baseline Workflow Prompt (Deliverable 2)

A ready-to-paste prompt that works on any AI platform. Every step is spelled out in full — no skills or shortcuts required. This is your starting point. As you build skills from the recommendations, you'll update this prompt to call those skills instead of repeating the logic inline.

### Skill Build Recommendations (Deliverable 3)

Actionable specs for each recommended skill, including:

- **Name and purpose** — what the skill does and when to use it
- **Inputs and outputs** — what goes in, what comes out
- **Which steps it replaces** — exactly which parts of the baseline prompt each skill absorbs
- **Integration points** — external tools and connectors needed
- **Priority** — what to build first based on frequency and automation value
- **Quick start prompt** — a one-liner to invoke the skill

## What's Next

You now have four Markdown files from the full workflow deconstruction:

| File | What it is | What to do with it |
|------|-----------|-------------------|
| `[name]-blueprint.md` | Workflow Blueprint (Step 1) | Reference — the raw decomposition you can revisit |
| `[name]-analysis.md` | Workflow Analysis Document (Step 2) | Reference — the full analysis with building block mapping |
| `[name]-prompt.md` | Baseline Workflow Prompt (Step 3) | **Use this** — paste it into a new conversation to run the workflow |
| `[name]-skill-recs.md` | Skill Build Recommendations (Step 3) | **Build from this** — your roadmap for reusable skills |

Start by running the baseline prompt on a real scenario. See what works, refine what doesn't, then build skills in priority order. Each skill you build makes the baseline prompt shorter and more reliable.

Keep all four files together — in a folder, a repo, or wherever you store your workflow documentation. You can share any of these with your instructor or team for feedback.

For more on building skills and agents, see [Agents & Tools Overview](../../fundamentals/agents-and-tools/README.md).
