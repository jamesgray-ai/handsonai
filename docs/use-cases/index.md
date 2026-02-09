---
title: AI Use Cases
description: Six use case primitives that cover what teams actually build with AI — content creation, research, coding, data analysis, ideation and strategy, and automation
---

# AI Use Cases

OpenAI's analysis of over 600 enterprise AI deployments found that nearly all use cases fall into six primitives. These primitives describe the **type of work** AI does, not the tools or platforms involved. Understanding them helps you classify your own workflows and find the right building blocks faster.

*The six primitives and department examples in this section are adapted from OpenAI's [Identifying and Scaling AI Use Cases: How Early Adopters Focus Their AI Efforts](https://cdn.openai.com/business-guides-and-resources/identifying-and-scaling-ai-use-cases.pdf) and made platform-agnostic.*

!!! tip "Connecting to the Framework"
    The [Business-First AI Framework](../business-first-ai-framework/index.md) helps you **find** opportunities (Step 1 — Discover) and **deconstruct** them into building blocks (Step 2). Use these six primitives to **classify** the opportunities you find — they tell you what type of AI work each opportunity involves, which makes choosing the right building blocks easier.

## The Six Primitives

| Primitive | What AI Does | Typical Building Blocks | Example |
|-----------|-------------|------------------------|---------|
| [**Content Creation**](content-creation.md) | Drafts, edits, translates, repurposes | Prompt, Context, Skill, Project | First-draft blog posts in brand voice |
| [**Research**](research.md) | Searches, synthesizes, structures information | Prompt, Context, Agent, MCP | Multi-source competitive analysis |
| [**Coding**](coding.md) | Generates, debugs, ports, explains code | Prompt, Context, Agent | Python scripts for non-coders |
| [**Data Analysis**](data-analysis.md) | Harmonizes data, identifies trends, visualizes | Prompt, Context, Skill | Expense analysis across sources |
| [**Ideation & Strategy**](ideation-and-strategy.md) | Brainstorms, plans, gives feedback, models scenarios | Prompt, Context, Project | Campaign ideation with constraints |
| [**Automation**](automation.md) | Executes repeatable routine tasks with minimal human involvement | Skill, Agent, MCP | Weekly competitive update pipeline |

## Content Creation

AI drafts, edits, translates, and repurposes content across formats. This is the most common entry point for teams adopting AI — nearly every department produces written content, and AI can handle first drafts, formatting, and adaptation between audiences.

Content creation works best when you provide context (brand voice, style guides, examples) so the AI produces output that matches your standards rather than generic copy.

[:octicons-arrow-right-24: Content Creation detail](content-creation.md)

---

## Research

AI searches, synthesizes, and structures information from multiple sources. Research use cases replace the hours spent gathering, reading, and summarizing — the AI handles the collection while you focus on judgment and decision-making.

Research primitives are particularly powerful when combined with MCP connections to external data sources, letting the AI pull from your actual tools rather than just web search.

[:octicons-arrow-right-24: Research detail](research.md)

---

## Coding

AI generates, debugs, ports, and explains code. This primitive isn't limited to software engineers — it extends to anyone who needs to create scripts, formulas, queries, or technical artifacts as part of their work.

Coding use cases range from simple formula generation (Excel, SQL) to full application development with agents that plan, write, test, and iterate autonomously.

[:octicons-arrow-right-24: Coding detail](coding.md)

---

## Data Analysis

AI harmonizes data from multiple sources, identifies trends, and produces visualizations. Data analysis use cases turn raw information into structured insights — the AI handles cleaning, formatting, and pattern recognition while you direct the analysis.

This primitive often pairs with coding (generating analysis scripts) and research (interpreting results in context).

[:octicons-arrow-right-24: Data Analysis detail](data-analysis.md)

---

## Ideation & Strategy

AI brainstorms ideas, plans approaches, provides feedback, and runs scenario analysis. This is the most collaborative primitive — AI serves as a thinking partner rather than an executor, helping you explore possibilities you wouldn't consider alone.

Ideation works best in project workspaces where the AI has persistent context about your goals, constraints, and past decisions.

[:octicons-arrow-right-24: Ideation & Strategy detail](ideation-and-strategy.md)

---

## Automation

AI executes repeatable routine tasks with minimal human involvement. Automation is the highest-autonomy primitive — once configured, these workflows run on schedule or in response to triggers, producing consistent results without manual intervention.

Automation typically builds on the other primitives. A content creation workflow becomes automation when it runs on a schedule. A research workflow becomes automation when it monitors sources continuously.

[:octicons-arrow-right-24: Automation detail](automation.md)

## Classifying Your Use Cases

When a use case seems to span multiple primitives, identify the **primary output** to pick the right one:

| If the main output is... | The primary primitive is... | Even though it also involves... |
|--------------------------|----------------------------|-------------------------------|
| A written document | Content Creation | Research to gather source material |
| A structured summary of findings | Research | Content creation to format the report |
| A working script or application | Coding | Research to find the right approach |
| Charts, trends, or insights from data | Data Analysis | Coding to build the analysis |
| A plan, list of options, or recommendation | Ideation & Strategy | Research to inform the strategy |
| A pipeline that runs without you | Automation | Any of the above as individual steps |

Most real workflows combine two or three primitives. The classification helps you find the right starting point and examples — not a rigid box.

## Primitives vs. Building Blocks

These are different lenses on the same work:

| Concept | What it answers | Where to learn more |
|---------|----------------|-------------------|
| **Primitives** (this section) | **What** type of work is AI doing? | You're here |
| **Building Blocks** | **How** do you implement it? | [Agentic Building Blocks](../agentic-building-blocks/index.md) |
| **Autonomy Levels** | **How much** AI involvement? | [Business-First AI Framework](../business-first-ai-framework/index.md) |

Primitives help you browse use cases by category. Building blocks help you assemble the implementation. Autonomy levels help you decide how much control to hand over. All three work together.

## Related

- [Business-First AI Framework](../business-first-ai-framework/index.md) — find and prioritize AI opportunities
- [Discover Workflows](../business-first-ai-framework/discover.md) — structured audit to surface workflow candidates
- [Agentic Building Blocks](../agentic-building-blocks/index.md) — the six components for implementing AI workflows
- [Build Workflows](../business-first-ai-framework/build/index.md) — worked examples across the autonomy spectrum
- [Plugin Marketplace](../plugins/index.md) — pre-built agents and skills you can install
