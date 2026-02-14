---
title: Prompt Chaining
description: Break complex tasks into sequential steps with validation gates between each step for structured, reliable AI workflows
---

# Prompt Chaining

**Prompt chaining** breaks a complex task into a sequence of smaller steps. Each step (LLM call) builds on the output of the previous one, with intermediate **gates** that validate quality before proceeding. If an output fails validation, the process can exit early to prevent error propagation.

Think of it as an assembly line where each station contributes a specific part to the final product.

## Why It Matters

- **Increased accuracy** — Each LLM call focuses on a specific goal, reducing errors and improving overall quality
- **Modularity** — You can inspect and debug intermediate steps, making the workflow easier to adapt and refine
- **Enhanced reliability** — Programmatic gates catch errors early, increasing confidence in the final output
- **Efficiency trade-off** — This workflow trades some latency (multiple steps) for more robust, higher-quality outputs

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **LLM Call 1** | Handles the initial step and produces the first output | Generate a document outline based on user input |
| **Gate** | Validates the output of the previous call; continues or exits | Check if the outline contains all necessary sections |
| **LLM Call 2** | Processes the validated output from the previous step | Expand the approved outline into a detailed draft |
| **LLM Call 3** | Finalizes the task by refining or transforming the output | Translate the draft or format it for publication |
| **Exit** | Ends the workflow early if validation fails | Stop if the outline doesn't meet quality standards |
| **Output** | Delivers the final product after all steps complete successfully | A polished, translated document ready for publication |

## When to Use It

- **Multi-step processes** — Tasks that naturally decompose into sequential steps (generate, validate, refine)
- **Tasks requiring validation** — When intermediate outputs need quality checks before proceeding
- **Complex workflows** — When different steps benefit from different prompts, models, or configurations

## Example: Generating Marketing Materials

A company needs product launch copy translated into multiple languages with consistent tone:

1. **LLM Call 1** — Generate initial marketing copy from product details and target audience
2. **Gate** — Validate against tone guide and campaign goals
3. **LLM Call 2** — Translate the validated copy into multiple languages
4. **Gate** — Ensure translations retain tone and key messages
5. **LLM Call 3** — Format translated copy for each platform (email, social media, website)
6. **Output** — Finalized, multilingual marketing materials ready for deployment

## How to Implement

1. **Decompose the task** — Identify the logical subtasks that make up the overall goal
2. **Define validation criteria** — Establish clear checkpoints (gates) to evaluate outputs after each step
3. **Connect steps programmatically** — Design the workflow so outputs from one step feed into the next
4. **Test and refine** — Ensure each step performs as intended and adjust based on intermediate results

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Workflow Architecture Patterns Overview](index.md)
- [Augmented LLM](augmented-llm.md) — the foundation this pattern builds on
- [Routing](routing.md) — another structured workflow for branching paths
- [Evaluator-Optimizer](evaluator-optimizer.md) — iterative refinement with feedback loops
- [Build > Design Your AI Workflow](../../business-first-ai-framework/build/design.md)
