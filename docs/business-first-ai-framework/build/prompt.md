---
title: Prompt
description: Turn your AI Building Block Spec into a ready-to-use Baseline Workflow Prompt.
---

# Prompt

> **Part of:** [Build Workflows](index.md)

!!! tip "New to prompts as a building block?"
    See [Agentic Building Blocks > Prompts](../../agentic-building-blocks/prompts/index.md) for prompt engineering guidance and cross-platform techniques.

## What This Is

The step that turns your analysis into action. AI reads your AI Building Block Spec and generates a ready-to-use prompt you can paste into any AI tool to execute the workflow today. If you built skills in the previous step, the prompt references them — making it shorter and more maintainable.

| | |
|---|---|
| **What you'll do** | Upload your AI Building Block Spec from the Design phase, answer 1-2 clarifying questions, then review the generated prompt |
| **What you'll get** | A **Baseline Workflow Prompt** (ready to paste and run). If you built skills, the prompt invokes them by name instead of spelling out those steps. |
| **Time** | ~5-10 minutes (mostly generative — the AI does the heavy lifting) |

## Why This Matters

Analysis without action is just documentation. The Baseline Workflow Prompt gives you something you can use immediately — paste it into any AI tool and run your workflow. It works on day one, on any platform.

If you built skills in the previous step, this prompt references them — each skill invocation replaces what would otherwise be a long block of inline instructions. If you didn't build skills, the prompt spells out every step in full so it still works standalone.

## How to Use This

There are two ways to generate your prompt, depending on which tools you use:

### Option A: Prompt template (any AI tool)

1. **Copy the prompt** from the code block below
2. **Paste it into a new conversation** in your preferred AI tool
3. **Press Enter** — the model will ask you to upload or paste your AI Building Block Spec
4. **Upload or paste your AI Building Block Spec file** (`[workflow-name]-building-block-spec.md`) from the Design phase
5. **If you built skills**, list them when the AI asks — it generates a prompt that references your skills instead of spelling out those steps
6. **Review the output** — the model may ask 1-2 clarifying questions, then generates the Baseline Workflow Prompt
7. **Download the file** — save as `[name]-prompt.md`

### Option B: Claude skill (`building-workflows`)

Use the `building-workflows` skill from the [Business-First AI plugin](../../plugins/business-first-ai.md). You still need to provide your AI Building Block Spec — the skill guides the conversation but doesn't have your file until you upload it.

=== "Claude Code or Cowork"

    1. **Install the plugin** (one time): `/plugin install business-first-ai@handsonai`
    2. **Start a new conversation** and say:
        ```
        Generate the Baseline Workflow Prompt
        from the AI Building Block Spec in outputs/[workflow-name]-building-block-spec.md.
        ```
    3. **Claude reads your file** from the path you specified and summarizes what it found — confirm before proceeding
    4. **If you built skills**, list them when Claude asks — it generates a prompt that references your skills instead of spelling out those steps
    5. **Review the output** — Claude may ask 1-2 clarifying questions, then generates the Baseline Workflow Prompt
    6. **Claude saves the file** to `outputs/[workflow-name]-prompt.md`

=== "Claude.ai"

    1. **Install the skill** — zip the `building-workflows` skill folder and upload it via **Settings > Capabilities > Upload skill** (see [Using Skills in Claude.ai](../../plugins/using-plugins.md#using-skills-in-claudeai-web) for detailed instructions)
    2. **Start a new chat** and say: "Generate a Baseline Workflow Prompt from this AI Building Block Spec."
    3. **Upload or paste your AI Building Block Spec file** (`[workflow-name]-building-block-spec.md`) when prompted
    4. **If you built skills**, list them when Claude asks — it generates a prompt that references your skills instead of spelling out those steps
    5. **Review the output** — Claude may ask 1-2 clarifying questions, then generates the Baseline Workflow Prompt
    6. **Download the file** — save as `[workflow-name]-prompt.md`

!!! tip "This step is mostly generative"
    The heavy analytical work is done. The model reads your AI Building Block Spec and produces a structured prompt with minimal interaction. Expect 5-10 minutes.

!!! tip "Register and commit"
    After generating your Baseline Workflow Prompt, register it in your [AI Registry](../../plugins/ai-registry.md) Notion database and commit the `[name]-prompt.md` file to your GitHub repository. This applies to all building blocks you create — prompts, skills, and agents.

## The Prompt

```text
You are an expert Prompt Engineer who writes clear, precise instructions that language models can execute reliably. Your job is to take an AI Building Block Spec and produce a Baseline Workflow Prompt.

I have an AI Building Block Spec from a previous conversation. I'll paste it when you ask for it.

---

## Part 1 — Paste Your AI Building Block Spec

Say: "Upload your AI Building Block Spec file, or paste its contents below, then press Enter."

Wait for me to provide it. After receiving the document, confirm you've read it by summarizing: the workflow name, the number of steps, how many are AI-eligible, and the AI building blocks identified. Then proceed to Part 1b.

If anything in the AI Building Block Spec is ambiguous or seems incomplete, ask me to clarify before generating outputs. Do not guess at missing information.

---

## Part 1b — Check for Skills

Ask: "Did you build any skills for this workflow? If yes, list each skill name and which workflow steps it covers. If no, I'll generate the full baseline prompt with all steps spelled out."

If the user provides skills: note which steps are covered. In Part 2, replace those steps with skill invocations instead of spelling out the full logic.

If the user says no: proceed to Part 2 and spell out every step in full.

---

## Part 2 — Generate Baseline Workflow Prompt

Generate a ready-to-use Markdown prompt that someone could paste into any AI tool to execute this workflow. For any step covered by a skill the user provided, replace the detailed inline instructions with a brief description of the task — the skill handles the details automatically on platforms that support it. Keep full instructions only for steps NOT covered by a skill. If no skills were provided, spell out every step in full — this is the baseline version that works on any platform (Claude, ChatGPT, Gemini, M365 Copilot).

**Before generating the prompt, check the Context Inventory for any artifacts that contain existing AI instructions** — prompts, project instructions, system prompts, or custom assistant configurations the user already has. These contain workflow logic that must be included in the Baseline Prompt — not referenced, but actually included. If such artifacts exist but their content is not in the AI Building Block Spec, ask the user to paste or upload them now. The Baseline Prompt cannot reference external systems for its core logic — it must be self-contained.

Structure it as:

**Title and Purpose**
- Workflow name and description (from the AI Building Block Spec)
- Workflow outcome — what this workflow produces
- When to use it

**Instructions**
- Numbered steps, each clearly labeled as (AI) or (Human)
- For each AI step: specific instructions the model should follow, written as direct commands
- For each Human step: clear description of what the human does and what they hand back to the model
- Include the decision logic for any branching steps
- For any step covered by a user-provided skill: describe the task briefly instead of repeating the full logic inline (the skill handles the details automatically)

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

**Self-contained means:** The prompt contains every instruction the model needs to execute the workflow. It never says "open this project" or "follow those instructions" or "refer to the project instructions." If existing AI instructions drive a step, those instructions are written into the prompt. A reader who has never seen the AI Building Block Spec or Workflow Definition can execute this prompt successfully. (Exception: steps covered by a named skill — the skill handles those instructions.)

**Recommended Implementation Order**
Prioritize the AI-eligible steps into a build sequence:
1. **Quick wins** — Deterministic steps with clear inputs/outputs that can be automated with a Prompt or Context alone. Start here.
2. **High-value semi-autonomous steps** — Steps where AI does most of the work but needs a human review gate. Build these next.
3. **Complex agent steps** — Fully autonomous steps requiring Agents, MCP connectors, or multi-tool orchestration. Tackle these last.
For each priority tier, list the specific steps and what to build.

**Where to Run**
- Where to run this prompt (normal chat vs. project), based on the AI Building Block Spec's recommendation
- If normal chat: which files to attach when pasting the prompt
- If project: how to set up the project (name, which files to pre-load, any general project-level settings), then paste this prompt into a conversation within the project
- Decision criteria summary so the user understands why this recommendation was made

Note: The prompt instructions above are the same regardless of where you run it. The project provides file staging convenience — the prompt provides the workflow logic.

**File naming:** Name the file `[workflow-name]-prompt.md` using the same workflow name from the AI Building Block Spec (e.g., `lead-qualification-prompt.md`).

Generate the prompt as a downloadable Markdown file. If your platform doesn't support file downloads, format it inside a single Markdown code block so I can copy and save it manually.

---

After presenting the file, summarize what the user now has:

> **Build complete.** You now have your Baseline Workflow Prompt (`[workflow-name]-prompt.md`). Paste it into any AI tool to run the workflow.

If skills were provided, also note: "Your prompt references [N] skills — those steps are invoked by name instead of spelled out inline."

> Your three core deliverables:
>
> 1. `[workflow-name]-definition.md` — your Workflow Definition (from Deconstruct)
> 2. `[workflow-name]-building-block-spec.md` — your AI Building Block Spec (from Design)
> 3. `[workflow-name]-prompt.md` — your Baseline Workflow Prompt (ready to use)
>
> Start by running the baseline prompt on a real scenario.

**Write workflow SOP (Claude users, optional):** If you registered this workflow to the AI Registry during the Deconstruct step, you can now generate a Standard Operating Procedure and save it to the workflow's Notion page. Use the `writing-workflow-sops` skill from the AI Registry plugin — it reads the workflow entry from Notion, uses the Baseline Prompt's procedure steps as input, and writes a formatted SOP (overview, prerequisites, trigger, step-by-step procedure, outputs, quality checks, troubleshooting) directly to the page body. This gives your workflow a complete home in Notion: metadata in the properties, SOP in the page content, and deliverable files in your local folder.

---

## General Instructions

- If I mention I'm using Claude, note where Claude Code Skills are the appropriate implementation. On other platforms, map to custom instructions, GPTs, or Gems.
- Use plain language. Avoid jargon unless I introduced it.
- If anything is ambiguous in the AI Building Block Spec, ask me before generating.
```

## What This Prompt Produces

### Baseline Workflow Prompt

A ready-to-paste prompt that works on any AI platform. If you built skills, the prompt references them — those steps are invoked by name instead of spelled out inline, making the prompt shorter and more maintainable. If you didn't build skills, every step is spelled out in full so it works standalone.

## What's Next

You now have three core Markdown files from the full workflow deconstruction and build:

| File | What it is | What to do with it |
|------|-----------|-------------------|
| `[name]-definition.md` | Workflow Definition (Deconstruct) | Reference — the raw decomposition you can revisit |
| `[name]-building-block-spec.md` | AI Building Block Spec (Design) | Reference — the full analysis with building block mapping |
| `[name]-prompt.md` | Baseline Workflow Prompt (Build) | **Use this** — paste it into a new conversation to run the workflow |

Your prompt is ready. Test it on a real scenario — [Run](run.md).

Keep all three files together — in a folder, a repo, or wherever you store your workflow documentation. You can share any of these with your team for feedback.

For next steps on building agents or connecting external tools, see [Agents](agents.md) and [MCP](mcp.md).
