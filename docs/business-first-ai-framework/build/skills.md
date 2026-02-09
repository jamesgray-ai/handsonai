---
title: Skills
description: Build reusable skills that codify expertise for specific workflow steps — making your prompt shorter, more reliable, and more consistent.
---

# Skills

> **Part of:** [Build Workflows](index.md)

!!! tip "New to skills as a building block?"
    See [Agentic Building Blocks > Skills](../../agentic-building-blocks/skills/index.md) for definitions, examples, and cross-platform implementation details.

## What This Is

A skill codifies deep expertise for a specific workflow step. Give it inputs, it follows a defined process, it produces consistent outputs. Skills make your workflow shorter, more reliable, and more reusable.

| | |
|---|---|
| **What you'll do** | Review your Skill Specs, decide which skills to build, then turn the highest-priority spec into a working skill |
| **What you'll get** | Reusable skills that replace step sections in your baseline prompt |
| **Time** | 15-30 minutes per skill |

## When to Build Skills vs. When a Prompt Section Is Enough

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

Your Skill Specs (from the Build step) already recommend which steps should become skills and in what priority order. Start with the highest-priority recommendation.

## From Skill Spec to Working Skill

Your Build outputs include Skill Specs for each recommended skill. To turn a spec into a working skill:

1. **Start with the highest-priority spec** — Build what creates the most value first
2. **Use the spec's Purpose, Inputs, Outputs as the skeleton** — These define what the skill does and what it produces
3. **Write the Workflow section** — The step-by-step process the skill follows. Be specific — this is where domain expertise lives.
4. **Add Guidelines** — Edge cases, quality standards, things to watch for
5. **Test with real data from your workflow** — Run the skill on actual inputs and compare to what you'd produce manually

## How Skills Integrate with Your Prompt

A skill replaces specific step numbers in your baseline prompt. Instead of the prompt spelling out every instruction for that step, it invokes the skill:

**Before (inline in prompt):**
> Step 5: Extract key findings from the research. For each finding, identify the source, the claim, the supporting evidence, and the confidence level. Format as a structured table...

**After (with skill):**
> Step 5: Use the `finding-extraction` skill on the research output.

The skill handles the complexity. The prompt stays clean and focused on workflow sequencing.

## What's Next

If your workflow includes steps tagged with "Agent" in the Building Block Map, see [Agents](agents.md) to decide whether you need autonomous execution. Otherwise, test your baseline prompt on a real scenario and build skills incrementally from your Skill Specs.
