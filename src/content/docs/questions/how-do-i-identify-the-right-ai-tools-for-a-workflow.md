---
question: "How do I identify the right AI tools for a workflow?"
short_answer: "Define the work first, then choose the tools. Deconstruct captures the goal, what every output must get right, the rules and the checkpoints without naming any tool; Design then picks the platform and the building block — prompt, skill, agent, or connector — for each step."
platforms: [openai, claude, gemini]
topic: strategy
date: 2026-02-02
author: James Gray
title: "How do I identify the right AI tools for a workflow?"
description: "Define the work first in Deconstruct, then let Design choose the platform and the building block — prompt, skill, agent, or connector — for each step."
---

**Short answer:** Define the work first, then choose the tools. Deconstruct captures the goal, what every output must get right, the rules and the checkpoints without naming any tool; Design then picks the platform and the building block — prompt, skill, agent, or connector — for each step.

## The Full Answer

You can't choose the right AI tools for a workflow you don't fully understand. The [AI Workflow Framework](/ai-workflow-framework/) separates the two questions on purpose: [Deconstruct](/ai-workflow-framework/deconstruct/) defines *what* the work is, and [Design](/ai-workflow-framework/design/) decides *how* AI delivers it.

Most people jump straight to tool selection — "Should I use an agent? Do I need an API?" — before they've worked out what the workflow actually involves. The result is over-engineered solutions for simple problems, or under-powered tools for complex ones.

**Deconstruct first.** The Deconstruct skill starts with the outcome: what the workflow produces and what every output must get right. Then it records how the work gets done, the rules it follows, where a person checks before it goes on (checkpoints), and a few practice inputs from your real work. No tool, platform, or autonomy level is chosen here. The result is your Workflow Requirements: a description of the work.

**Then design.** Design reads those requirements and makes the mechanism decisions: which platform, whether the workflow runs as a skill or an agent, how much the AI decides on its own (autonomy), and whether a person takes part while it runs (involvement). It then maps each step to the building block that delivers it:

| Layer | Building Block | What It Is | When to Use It |
|-------|---------------|------------|----------------|
| **Intelligence** | **Model** | The AI engine that processes inputs and generates outputs | When the task requires specific capabilities (reasoning, multimodal, speed) |
| | **Context** | Background information, reference docs, or examples | Steps that need domain knowledge or specific data |
| | **Memory** | Persistent knowledge that carries across conversations | Steps that need to recall prior interactions or accumulated knowledge |
| | **Project** | A persistent workspace grouping prompts, context, skills, and agents | Organizing everything for a specific workflow |
| **Orchestration** | **Prompt** | A well-crafted instruction that tells the model what to do | Single-step tasks with clear inputs and outputs |
| | **Skill** | A reusable routine — give it inputs, it follows a defined process, it produces consistent outputs | Repeatable tasks you'll run many times |
| | **Agent** | An autonomous AI that plans, uses tools, and executes multi-step work | Complex steps requiring judgment and tool use |
| | **Harness** | The software around a model that turns it into a working agent | Always present — the choice is which one fits the work |
| **Integration** | **MCP** | A connector via Model Context Protocol to external tools or databases | Steps that need to read from or write to external systems |
| | **API** | A programmatic interface to external services | Steps that need direct, structured access to external capabilities |
| | **SDK** | A development framework for building custom AI applications | Steps requiring custom code to orchestrate AI capabilities |
| | **CLI** | A command-line interface for interacting with AI tools | Steps executed via terminal commands or automated scripts |
| **Governance** | **Registry** | A catalog of your AI workflows, the processes they serve, and the skills and agents behind them | As soon as you rely on more than a handful of workflows |
| | **Observability** | Seeing what an AI system is doing, why, and how well | Workflows that run unattended or that others depend on |
| | **Evaluation** | Repeatable measurement of whether output is good enough | Every workflow — the framework's Test step is built on it |

Not every step needs AI. Design can assign a step to a person, and the checkpoints from Deconstruct stay in place whatever tools are chosen.

## How to Get Started

Both steps are skills in the Hands-on AI plugin — see [Install the Hands-on AI Plugin](/ai-workflow-framework/skills/) for your platform.

1. **Deconstruct** — say *"run the deconstruct skill"* and describe the workflow. It produces the workflow's requirements.
2. **Design** — say *"run the design skill"*. It reads those requirements and produces a Design Plan naming the platform, whether each part is a skill or an agent, and what it connects to, ending in a task list.

:::tip[Start with a workflow you actually do]
Real workflows produce the best requirements. Deconstruct is designed to work with rough, incomplete descriptions — don't over-prepare. Even "I onboard new clients and it takes forever" is enough to start. The model will find the hidden steps and assumptions you've internalized.
:::

## Key Takeaways

- Define the work before choosing tools — Deconstruct captures what the workflow does without naming any tool
- Deconstruct starts with the outcome, then captures the rules, the checkpoints and practice inputs from your real work
- Design chooses the platform, the mechanism (skill or agent), the autonomy level, and the involvement mode, then maps each step to one of the 15 AI building blocks across four layers — Intelligence, Orchestration, Integration, Governance
- Not every step needs AI — Design can leave a step with a person, and checkpoints stay in place

## Related Questions

- [How do I find workflows worth applying AI to?](/questions/how-do-i-find-workflows-worth-applying-ai-to/)
- [What is a system prompt?](/questions/what-is-a-system-prompt/)
