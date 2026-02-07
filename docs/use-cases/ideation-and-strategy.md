---
title: Ideation & Strategy
description: AI use cases for brainstorming, planning, providing feedback, and running scenario analysis
---

# Ideation & Strategy

## What Ideation & Strategy Is

Ideation and strategy use cases have AI serve as a thinking partner — brainstorming ideas, planning approaches, providing structured feedback, and running scenario analysis. This is the most collaborative primitive. Rather than producing a finished deliverable, the AI helps you think through problems, explore possibilities, and stress-test your plans.

This primitive covers any workflow where the primary output is a set of ideas, a plan, a recommendation, or an evaluation: campaign brainstorming, product roadmap planning, risk analysis, decision frameworks, and structured feedback on drafts or proposals.

Unlike the other primitives where AI executes work, ideation and strategy is about augmenting your thinking. The AI brings breadth (more options than you'd generate alone), structure (frameworks and evaluation criteria), and perspective (challenging assumptions you didn't realize you were making).

*Ideation & Strategy is one of six use case primitives identified in OpenAI's [Identifying and Scaling AI Use Cases](https://cdn.openai.com/business-guides-and-resources/identifying-and-scaling-ai-use-cases.pdf) guide. The examples here are adapted to be platform-agnostic and mapped to [Agentic Building Blocks](../agentic-building-blocks/index.md).*

## Key Characteristics

- **Output is ideas, plans, or evaluations** — the deliverable is thinking, not execution
- **Highly interactive** — the best results come from multi-turn conversations where you refine direction as ideas develop
- **Benefits from constraints** — "brainstorm marketing ideas" produces generic results; "brainstorm marketing ideas for a B2B SaaS launch with a $5K budget targeting enterprise CFOs" produces actionable ones
- **Persistent context is key** — the more the AI knows about your goals, constraints, past decisions, and domain, the more relevant its suggestions become
- **Pairs with every other primitive** — ideation often precedes content creation, research, coding, or data analysis

## When to Apply This Primitive

**Use Ideation & Strategy when:**

- You need to generate options, alternatives, or creative approaches
- You want structured feedback on a plan, draft, or proposal
- You're making a decision that requires weighing multiple factors
- You need to explore scenarios (what if X happens? what are the risks of Y?)

**NOT the right primitive when:**

- You need to find facts or gather information (that's [Research](research.md))
- The deliverable is a finished document for an audience (that's [Content Creation](content-creation.md))
- You're analyzing numerical data to find patterns (that's [Data Analysis](data-analysis.md))

## Department Examples

| Department | Use Case | What AI Does | Typical Building Blocks |
|-----------|----------|-------------|------------------------|
| Marketing | Campaign ideation | Brainstorms campaign concepts within budget, audience, and brand constraints | Prompt, Context, Project |
| Product | Feature prioritization | Evaluates proposed features against a scoring framework (impact, effort, alignment) | Prompt, Context, Project |
| Sales | Objection handling | Generates responses to common objections, tailored to specific deal contexts | Prompt, Context, Skill |
| Finance | Scenario modeling | Explores what-if scenarios for budget decisions, investments, or pricing changes | Prompt, Context, Project |
| Engineering | Architecture reviews | Evaluates proposed system designs against quality attributes (scalability, security, maintainability) | Prompt, Context |
| HR | Program design | Brainstorms engagement initiatives, training programs, or policy changes with trade-off analysis | Prompt, Context, Project |

## Building Block Patterns

| Complexity | Building Blocks | Example |
|-----------|----------------|---------|
| **Simple** | Prompt + Context | Share a project brief and ask AI to brainstorm 10 approaches with pros and cons for each |
| **Intermediate** | Project + Context | A strategy project with company goals, competitive landscape, and past decisions as persistent context — every brainstorming session builds on shared knowledge |
| **Advanced** | Project + Agent + Context | A strategy project with a feedback agent that evaluates proposals against a scoring rubric, challenges assumptions, and suggests improvements |

## Use Cases

| | |
|---|---|
| **Department** | Marketing |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Project |
| **Problem** | Campaign brainstorming sessions produce safe, repetitive ideas because the team defaults to what worked before — there's no structured way to explore new directions while staying within brand and budget constraints |
| **Solution** | A strategy project loaded with brand guidelines, past campaign performance data, and audience research. Team members brainstorm with AI that suggests unexpected angles, challenges assumptions, and evaluates ideas against the constraints — producing a wider range of options than group brainstorming alone |

| | |
|---|---|
| **Department** | Product |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Project |
| **Problem** | Feature prioritization decisions are driven by the loudest voice in the room rather than structured analysis — the team lacks a consistent framework for evaluating trade-offs |
| **Solution** | A project workspace with the product roadmap, OKRs, user research, and a prioritization framework (RICE, value/effort, or custom). For each proposed feature, AI evaluates it against the framework, identifies risks, and compares it to alternatives — giving the team data-informed starting points for discussion |

| | |
|---|---|
| **Department** | Finance |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Project |
| **Problem** | Budget planning is a linear process — the team builds one plan and defends it, rather than exploring multiple scenarios and understanding the trade-offs between them |
| **Solution** | A project with financial data, company goals, and market assumptions as context. AI generates multiple budget scenarios (aggressive growth, conservative, balanced), identifies the key trade-offs between them, and highlights the assumptions each scenario depends on |

## Common Mistakes

**Under-constraining the brainstorm.** "Give me ideas" produces generic output. The more specific your constraints — budget, timeline, audience, brand, past failures to avoid — the more creative and useful the AI's suggestions become. Constraints don't limit creativity; they focus it.

**Treating AI suggestions as decisions.** AI is a brainstorming partner, not a decision-maker. It generates options and analysis, but the judgment about which option to pursue requires your understanding of politics, relationships, timing, and context that the AI doesn't have.

**Forgetting to share context about past decisions.** AI will suggest things you've already tried and rejected if it doesn't know your history. Use project workspaces with persistent context so the AI builds on your past thinking rather than starting from scratch every time.

## Related

- [AI Use Cases Overview](index.md) — all six primitives at a glance
- [Projects](../agentic-building-blocks/projects/index.md) — persistent workspaces for ongoing strategic work
- [Context](../agentic-building-blocks/context/index.md) — providing goals, constraints, and history
- [Prompts](../agentic-building-blocks/prompts/index.md) — crafting effective brainstorming and evaluation prompts
- [Phase 1 — Discover](../business-first-ai-framework/discover.md) — using ideation to find AI opportunities
