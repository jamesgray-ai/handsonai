---
question: "How do I identify the right AI tools for a workflow?"
short_answer: "Break your workflow into discrete steps using the 6-question framework (steps, decisions, data flows, context needs, failure modes, data readiness), then map each step to AI building blocks like prompts, skills, agents, and connectors to see exactly what to build."
platforms: [openai, claude, gemini]
topic: strategy
date: 2026-02-02
author: James Gray
title: "How do I identify the right AI tools for a workflow?"
---**Short answer:** Break your workflow into discrete steps using the 6-question framework (steps, decisions, data flows, context needs, failure modes, data readiness), then map each step to AI building blocks like prompts, skills, agents, and connectors to see exactly what to build.

## The Full Answer

You can't choose the right AI tools for a workflow you don't fully understand. The [AI Workflow Framework](/ai-workflow-framework/) addresses this with a structured approach: discover opportunities first, then deconstruct workflows into building blocks before selecting tools.

Most people jump straight to tool selection — "Should I use an agent? Do I need an API?" — before they've properly decomposed what the workflow actually involves. The result is over-engineered solutions for simple problems, or under-powered tools for complex ones.

The right approach is to **deconstruct first, then map**. Start by breaking your workflow into discrete steps using the 6-question framework: What are the individual steps? Where are the decision points? What data flows in and out? What context does each step need? What happens when this step fails? Is the data AI-accessible? That last question — data readiness — surfaces gaps where data needs to be reorganized, reformatted, or migrated before AI can reliably use it.

Once you have the refined step-by-step breakdown, map each step to one or more of the AI building blocks:

| Layer | Building Block | What It Is | When to Use It |
|-------|---------------|------------|----------------|
| **Intelligence** | **Model** | The AI engine that processes inputs and generates outputs | When the task requires specific capabilities (reasoning, multimodal, speed) |
| | **Context** | Background information, reference docs, or examples | Steps that need domain knowledge or specific data |
| | **Memory** | Persistent knowledge that carries across conversations | Steps that need to recall prior interactions or accumulated knowledge |
| | **Project** | A persistent workspace grouping prompts, context, skills, and agents | Organizing everything for a specific workflow |
| **Orchestration** | **Prompt** | A well-crafted instruction that tells the model what to do | Single-step tasks with clear inputs and outputs |
| | **Skill** | A reusable routine — give it inputs, it follows a defined process, it produces consistent outputs | Repeatable tasks you'll run many times |
| | **Agent** | An autonomous AI that plans, uses tools, and executes multi-step work | Complex steps requiring judgment and tool use |
| **Integration** | **MCP** | A connector via Model Context Protocol to external tools or databases | Steps that need to read from or write to external systems |
| | **API** | A programmatic interface to external services | Steps that need direct, structured access to external capabilities |
| | **SDK** | A development framework for building custom AI applications | Steps requiring custom code to orchestrate AI capabilities |
| | **CLI** | A command-line interface for interacting with AI tools | Steps executed via terminal commands or automated scripts |

Not every step needs AI. The deconstruction also classifies each step on an autonomy spectrum — from fully human to fully autonomous — so you can see which steps are candidates for AI and which should stay manual.

## How to Get Started

Use the [Deconstruct Workflows](/ai-workflow-framework/deconstruct/) to run through this process interactively. Paste it into any AI tool and it will:

1. **Analyze your scenario** — understand the workflow objective and rough steps
2. **Deep dive into each step** — apply the 6-question framework
3. **Map to building blocks** — classify each step and recommend the right AI tools
4. **Generate deliverables** — produce a workflow analysis document and an executable prompt you can save and reuse

:::tip[Start with a workflow you actually do]
Real workflows produce the best analysis. The meta prompt is designed to work with rough, incomplete descriptions — don't over-prepare. Even "I onboard new clients and it takes forever" is enough to start. The model will find the hidden steps and assumptions you've internalized.
:::
## Key Takeaways

- Deconstruct the workflow before choosing tools — you can't pick the right AI building blocks for a process you don't fully understand
- Use the 6-question framework: discrete steps, decision points, data flows, context needs, failure modes, and data readiness
- Map each step to one or more of the 11 AI building blocks across three layers — Intelligence (Model, Context, Memory, Project), Orchestration (Prompt, Skill, Agent), Integration (MCP, API, SDK, CLI)
- Not every step needs AI — the autonomy classification helps you see which steps are candidates and which should stay manual
- Use the [Deconstruct Workflows](/ai-workflow-framework/deconstruct/) to run through this process interactively

## Related Questions

- [How do I find workflows worth applying AI to?](/questions/how-do-i-find-workflows-worth-applying-ai-to/)
- [What is a system prompt?](/questions/what-is-a-system-prompt/)
