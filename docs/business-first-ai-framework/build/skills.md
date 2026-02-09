---
title: Skills
description: Build reusable skills before generating your prompt — so the prompt can reference them instead of spelling out every step.
---

# Skills

> **Part of:** [Build Workflows](index.md)

!!! tip "New to skills as a building block?"
    See [Agentic Building Blocks > Skills](../../agentic-building-blocks/skills/index.md) for definitions, examples, and cross-platform implementation details.

## What This Is

Build reusable skills before generating your prompt, so the prompt can reference them instead of spelling out every step. Skills codify deep expertise for specific workflow steps — give a skill inputs, it follows a defined process, it produces consistent outputs. When you generate your prompt in the next step, list the skills you built and the AI generates a shorter, smarter prompt that invokes them by name.

| | |
|---|---|
| **What you'll do** | Identify skill candidates from your AI Building Block Map, then build each one by giving Claude your Deconstruct artifacts — the analysis you've already done provides everything it needs |
| **What you'll get** | Reusable skills that your Baseline Workflow Prompt can invoke instead of spelling out every step |
| **Time** | ~10-15 minutes per skill (the heavy analysis is already in your artifacts) |

## Identify Skill Candidates

Open your AI Building Block Map (`[name]-building-blocks.md`) and scan the step table. Look for steps that meet these criteria:

- **Repeatable** — the step runs frequently with similar patterns
- **Requires domain expertise** — getting it right depends on specialized knowledge (scoring rubrics, extraction frameworks, editorial criteria)
- **Benefits from consistency** — the step should produce the same output structure every time

Good candidates are typically steps tagged with "Skill" in the AI Building Blocks column, or steps classified as "AI – Semi-Autonomous" that have complex logic. If a step is simple and deterministic — a few sentences of instruction — it's better left inline in the prompt.

**Don't overthink this.** If you're not sure whether a step needs a skill, skip it for now. You can always extract it into a skill later after running the prompt a few times and seeing where quality varies.

## When to Build a Skill vs. Keep It in the Prompt

Not every step needs a dedicated skill:

**Build a skill when:**

- The step requires domain expertise that's hard to get right every time
- You'll run this step across multiple workflows
- You want consistent quality without re-explaining the process each run
- The step has complex logic worth codifying (scoring rubrics, extraction frameworks, editorial criteria)

**Keep it in the prompt when:**

- The step is simple or deterministic
- It's unique to this workflow
- The instructions are short (a few sentences)
- Getting it right doesn't require specialized knowledge

## Build Your First Skill

Your Deconstruct artifacts already contain everything a skill needs. You spent 20-30 minutes producing a rich Workflow Definition and AI Building Block Map — building a skill is just giving Claude that context and asking it to create the skill.

### How to build a skill

1. **Pick your highest-priority skill candidate** — Open your AI Building Block Map (`[name]-building-blocks.md`) and find the steps tagged with "Skill" in the AI Building Blocks column. Start with the one in the highest priority tier from the Recommended Implementation Order.
2. **Ask Claude to create a skill** — Claude's built-in skill creation process will guide you through it. When you start, paste or upload your AI Building Block Map and Workflow Definition — they contain everything Claude needs.
3. **Point Claude at the right step** — Tell it which step to build: *"Create a skill for Step 4 — Score and Qualify Prospects. Here's my AI Building Block Map and Workflow Definition from the Deconstruct step."*
4. **Let your artifacts do the work** — Claude will ask questions as it builds the skill. Most answers are already in your files:

    | When Claude asks about... | Paste or point to... |
    |---|---|
    | What the skill does | Step name + Action column in your Building Block Map |
    | Inputs and format | Data In column |
    | Expected outputs | Data Out column |
    | Step-by-step process | Action + Decision Points columns, plus the detailed sub-steps in your Workflow Definition |
    | Edge cases and failure handling | Failure Mode column |
    | Reference materials needed | Context Needed column + Context Inventory table |
    | External tools or connections | Tools and Connectors Required section |

5. **Test with real data** — run the skill on actual inputs from your workflow and compare to what you'd produce manually. Refine until the output matches your standards.
6. **Repeat** for additional skill candidates — focus on the top 1-3. You can always build more later.

!!! tip "Paste the whole file"
    You don't have to extract individual columns. Paste your entire AI Building Block Map when you start — Claude will pull what it needs. Add the Workflow Definition too if the step has complex sub-steps or exception paths.

## How Skills Integrate with Your Prompt

When you generate your prompt in the next step ([Prompt](prompt.md)), list the skills you built. The AI generates a prompt that invokes your skills by name instead of spelling out those steps in full.

**Before (inline in prompt):**
> Step 5: Extract key findings from the research. For each finding, identify the source, the claim, the supporting evidence, and the confidence level. Format as a structured table...

**After (with skill):**
> Step 5: Extract key findings from the research output.

The skill handles the complexity. The prompt stays clean and focused on workflow sequencing. Each skill you build makes the prompt shorter and more maintainable.

## What's Next

Generate your Baseline Workflow Prompt — [Prompt](prompt.md). When the AI asks, list the skills you built and it generates a prompt that references them instead of spelling out those steps.

If you skipped building skills (or your platform doesn't support them), the Prompt step generates the full baseline with every step spelled out. You can always extract skills later.
