---
title: "Step 3 — Prompt & Skill Specs"
description: Generate a ready-to-use Baseline Workflow Prompt and Skill Specs from your AI Building Block Map.
---

# Step 3 — Prompt & Skill Specs

> **Part of:** [Deconstruct Workflows](index.md)

## What This Is

The final step that turns your analysis into action. AI reads your AI Building Block Map and generates two ready-to-use deliverables: a prompt you can paste into any AI tool to execute the workflow today, and a set of skill specs for reusable skills to build over time.

| | |
|---|---|
| **What you'll do** | Upload your AI Building Block Map from Step 2, answer 1–2 clarifying questions, then review the generated outputs |
| **What you'll get** | A **Baseline Workflow Prompt** (ready to paste and run) and **Skill Specs** (what to build next and in what order) |
| **Time** | ~5–10 minutes (mostly generative — the AI does the heavy lifting) |

## Why This Matters

Analysis without action is just documentation. The Baseline Workflow Prompt gives you something you can use immediately — paste it into any AI tool and run your workflow. It works on day one, on any platform.

The Skill Specs show you how to evolve that prompt over time. Each skill you build replaces a section of the baseline prompt, making the workflow shorter, more reliable, and more reusable. You get a clear path from "working but manual" to "automated and refined" — with specific priorities so you know what to build first.

## How to Use This

There are two ways to run Step 3, depending on which tools you use:

### Option A: Prompt template (any AI tool)

1. **Copy the prompt** from the code block below
2. **Paste it into a new conversation** in your preferred AI tool
3. **Press Enter** — the model will ask you to upload or paste your AI Building Block Map
4. **Upload or paste your AI Building Block Map file** (`[workflow-name]-building-blocks.md`) from Step 2
5. **Review the outputs** — the model may ask 1-2 clarifying questions, then generates both deliverables
6. **Download both files** — the Baseline Workflow Prompt and Skill Specs

### Option B: Claude skill

Use the `generating-workflow-outputs` skill from the [Business-First AI plugin](../../plugins/business-first-ai.md). It reads the AI Building Block Map from Step 2 and generates both deliverables automatically.

- **Claude Code or Cowork** — install the plugin (`/plugin install business-first-ai@handsonai`) and start with:
    ```
    Generate the Baseline Workflow Prompt and Skill Specs
    from the AI Building Block Map in outputs/[workflow-name]-building-blocks.md.
    ```
    Both deliverables are saved to the `outputs/` directory.
- **Claude.ai** — zip the `generating-workflow-outputs` skill folder and upload it via **Settings > Capabilities > Upload skill**, then start a new chat with: "Generate a Baseline Workflow Prompt and Skill Specs from this AI Building Block Map." Upload or paste your AI Building Block Map when prompted. See [Using Skills in Claude.ai](../../plugins/using-plugins.md#using-skills-in-claudeai-web) for detailed instructions.

!!! tip "This step is mostly generative"
    The heavy analytical work is done. The model reads your AI Building Block Map and produces two structured outputs with minimal interaction. Expect 5-10 minutes.

## The Prompt

```text
You are an expert Prompt Engineer who writes clear, precise instructions that language models can execute reliably. Your job is to take an AI Building Block Map and produce two deliverables: a Baseline Workflow Prompt and Skill Specs.

I have an AI Building Block Map from a previous conversation. I'll paste it when you ask for it.

---

## Part 1 — Paste Your AI Building Block Map

Say: "Upload your AI Building Block Map file, or paste its contents below, then press Enter."

Wait for me to provide it. After receiving the document, confirm you've read it by summarizing: the workflow name, the number of steps, how many are AI-eligible, and the recommended implementation order. Then proceed to Part 2.

If anything in the AI Building Block Map is ambiguous or seems incomplete, ask me to clarify before generating outputs. Do not guess at missing information.

---

## Part 2 — Generate Baseline Workflow Prompt

Generate a ready-to-use Markdown prompt that someone could paste into any AI tool to execute this workflow. This is the **baseline version** — it spells out every step in full so it works on any platform (Claude, ChatGPT, Gemini, M365 Copilot). As the user builds skills from the recommendations below, they'll update this prompt to invoke those skills instead of repeating the logic inline.

**Before generating the prompt, check the Context Inventory for any artifacts typed as "Executable Instructions."** These contain workflow logic that must be included in the Baseline Prompt — not referenced, but actually included. If the AI Building Block Map indicates executable instructions exist (e.g., existing project instructions, system prompts, or custom assistant configurations) but their content is not in the AI Building Block Map, ask the user to paste or upload those instructions now. The Baseline Prompt cannot reference external systems for its core logic — it must be self-contained.

Structure it as:

**Title and Purpose**
- Workflow name and description (from the AI Building Block Map)
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

**Self-contained means:** The prompt contains every instruction the model needs to execute the workflow. It never says "open this project" or "follow those instructions" or "refer to the project instructions." If existing AI instructions drive a step, those instructions are written into the prompt. A reader who has never seen the AI Building Block Map or Workflow Definition can execute this prompt successfully.

**Execution Context**
- Where to run this prompt (normal chat vs. project), based on the AI Building Block Map's recommendation
- If normal chat: which files to attach when pasting the prompt
- If project: how to set up the project (name, which files to pre-load, any general project-level settings), then paste this prompt into a conversation within the project
- Decision criteria summary so the user understands why this recommendation was made

Note: The prompt instructions above are the same regardless of execution context. The project provides file staging convenience — the prompt provides the workflow logic.

**File naming:** Name the file `[workflow-name]-prompt.md` using the same workflow name from the AI Building Block Map (e.g., `lead-qualification-prompt.md`).

Generate the prompt as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

---

## Part 3 — Generate Skill Specs

Based on the AI Building Block Map, recommend which reusable skills I should build. Focus on steps that are:
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

**File naming:** Name the file `[workflow-name]-skill-specs.md` using the same workflow name (e.g., `lead-qualification-skill-specs.md`).

Generate the recommendations as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

---

After presenting both files, summarize what I now have:

> **Workflow deconstruction complete.** You now have four files:
>
> 1. `[workflow-name]-definition.md` — your Workflow Definition (from Step 1)
> 2. `[workflow-name]-building-blocks.md` — your AI Building Block Map (from Step 2)
> 3. `[workflow-name]-prompt.md` — your Baseline Workflow Prompt (ready to use)
> 4. `[workflow-name]-skill-specs.md` — your Skill Specs (what to build next)
>
> Start by running the baseline prompt on a real scenario. Then build skills in priority order from the recommendations.

**Write workflow SOP (Claude users, optional):** If you registered this workflow to the AI Registry in Step 1, you can now generate a Standard Operating Procedure and save it to the workflow's Notion page. Use the `writing-workflow-sops` skill from the AI Registry plugin — it reads the workflow entry from Notion, uses the Baseline Prompt's procedure steps as input, and writes a formatted SOP (overview, prerequisites, trigger, step-by-step procedure, outputs, quality checks, troubleshooting) directly to the page body. This gives your workflow a complete home in Notion: metadata in the properties, SOP in the page content, and deliverable files in your local folder.

---

## General Instructions

- If I mention I'm using Claude, note where Claude Code Skills are the appropriate implementation. On other platforms, map to custom instructions, GPTs, or Gems.
- Use plain language. Avoid jargon unless the student introduced it.
- If anything is ambiguous in the AI Building Block Map, ask me before generating.
```

## What This Prompt Produces

### Baseline Workflow Prompt

A ready-to-paste prompt that works on any AI platform. Every step is spelled out in full — no skills or shortcuts required. This is your starting point. As you build skills from the recommendations, you'll update this prompt to call those skills instead of repeating the logic inline.

### Skill Specs

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
| `[name]-definition.md` | Workflow Definition (Step 1) | Reference — the raw decomposition you can revisit |
| `[name]-building-blocks.md` | AI Building Block Map (Step 2) | Reference — the full analysis with building block mapping |
| `[name]-prompt.md` | Baseline Workflow Prompt (Step 3) | **Use this** — paste it into a new conversation to run the workflow |
| `[name]-skill-specs.md` | Skill Specs (Step 3) | **Build from this** — your roadmap for reusable skills |

Start by running the baseline prompt on a real scenario. See what works, refine what doesn't, then build skills in priority order. Each skill you build makes the baseline prompt shorter and more reliable.

Keep all four files together — in a folder, a repo, or wherever you store your workflow documentation. You can share any of these with your instructor or team for feedback.

For more on building skills and agents, see [Agents](../../agentic-building-blocks/agents/index.md).
