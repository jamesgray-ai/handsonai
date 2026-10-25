---
title: "Example: Content Calendar Planning"
description: "An earlier-version example of the framework's deliverables (requirements, a Design Spec and a workflow prompt) for a real weekly content calendar planning workflow."
---

:::note[An earlier-version example]
These files were made with an earlier version of the [AI Workflow Framework](/ai-workflow-framework/), when it had seven steps and Design wrote a Design Spec. They're kept because the workflow is a good one to learn from, but they aren't in the current format: the framework's skills treat files like these as an earlier version, and Deconstruct offers what they say as something already written down when you start the workflow again. Each step's page ([Deconstruct](../../deconstruct/), [Design](../../design/), [Build](../../build/), [Test](../../test/)) describes the file it writes today.
:::

This page walks through the output of running a real workflow through the framework. The workflow is **Content Calendar Planning**: a weekly process for planning and sequencing content across LinkedIn, Substack, X and YouTube.

Analyze, Deconstruct, Design and Build produced three deliverables for this workflow. Each one is a detailed Markdown document. This page summarizes what's in each and why it matters, then links to the full file on GitHub, where you can read every table, every decision point and every failure mode at full width.

---

## The Deliverables

### 1. Workflow Requirements (Deconstruct)

[GitHub View full Workflow Requirements on GitHub](https://github.com/jamesgray-ai/handsonai/blob/main/examples/content-calendar-planning/requirements.md)

The Workflow Requirements are what [Deconstruct](../../deconstruct/) produces. What started as "I plan content on Sundays" became **10 refined steps across four phases**.

**What's inside:**

- **Metadata:** workflow name, trigger, owner and business objective
- **The steps,** each with its sub-steps, decision points, data in and out, and failure modes
- **Context:** the artifacts the workflow needs, with whether each exists and whether AI can reach it
- **What good output looks like,** and where a person reviews it

**Key insight:** Each step records not just what to do, but what to do when things go wrong. Step 1 has a fallback for when no metrics data exists. Step 2 detects an empty backlog and raises the importance of Step 3. Step 9 limits refinement to three rounds to prevent endless iteration. Capturing edge cases as requirements is what makes the workflow robust enough for AI to run. (The step numbers here are the workflow's own steps.)

---

### 2. Design Spec (Design)

[GitHub View full Design Spec on GitHub](https://github.com/jamesgray-ai/handsonai/blob/main/examples/content-calendar-planning/design-spec.md)

The Design Spec is what [Design](../../design/) produced from the requirements in the earlier version; today it writes a Design Plan. It classifies each step by autonomy level and identifies which steps should become reusable skills.

**What's inside:**

- **Why a Skill was chosen over an Agent:** the creative middle steps benefit from human judgment
- **A step-by-step decomposition table:** each step classified by phase, autonomy level, building blocks, skill candidacy, and whether a person reviews it
- **The autonomy summary:** Deterministic (4 steps), Guided (4 steps), Human (2 steps); the workflow is Guided and Augmented
- **4 skill candidates,** each with its purpose, inputs, outputs, decision logic and failure modes

**Key insight:** Autonomy is about what decides the next step. Steps 1, 2, 4 and 10 are fixed data operations, so they're Deterministic. In Steps 5–8 the AI makes bounded decisions by James's method (which ideas to select, which channel each goes to, how to sequence the plan), and those selections decide what happens next, so they're Guided. James approving them is involvement (Augmented), not lower autonomy.

---

### 3. Workflow Prompt (Build)

[GitHub View full Workflow Prompt on GitHub](https://github.com/jamesgray-ai/handsonai/blob/main/examples/content-calendar-planning/baseline-prompt.md)

The workflow prompt is one of the artifacts [Build](../../build/) can produce: a ready-to-run prompt you paste into any AI tool to run the workflow.

**What's inside:**

- **The full 10-step sequence:** the AI knows what to do at each step, what to present, and when to stop for input
- **Embedded context:** channel cadence targets, channel-format fit rules and content pillar definitions are written into the prompt, so no external documents are needed
- **Inputs and outputs:** what the user provides (fresh ideas, calendar context, theme selection, approvals) and what the workflow produces (an input summary, a draft plan, the final plan, and the database entries)

**Key insight:** The prompt reads like a conversation script. At each step, the AI knows whether to act, propose and wait, or ask for input. The points where a person decides (Steps 3, 5, 6 and 9) are explicit: the AI won't go on without approval there.

---

## What to Notice

- **The expansion.** "I plan content on Sundays" became 10 steps across 4 phases, with decision logic and failure modes. That expansion is what makes the workflow something AI can run.
- **Platform-agnostic.** The requirements and the design work with any AI tool. The skills and connections vary by platform, but the logic underneath is the same everywhere.

---

## Try It on Your Own Workflow

Ready to run your own workflow through the framework? It has five steps:

- **[Analyze](../../analyze/)**: find opportunities to create more value with AI in your work
- **[Deconstruct](../../deconstruct/)**: pin down what your chosen workflow must produce, its rules and where it asks first
- **[Design](../../design/)**: plan how it's built and how much the AI decides
- **[Build](../../build/)**: build it, check it and install it
- **[Test](../../test/)**: run it on practice inputs, grade the results, and take it live

Or start from the [AI Workflow Framework overview](/ai-workflow-framework/) for the full method.
