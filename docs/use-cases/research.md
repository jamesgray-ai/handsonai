---
title: Research
description: AI use cases for searching, synthesizing, and structuring information from multiple sources
---

# Research

## What Research Is

Research use cases have AI search, synthesize, and structure information from multiple sources. Instead of spending hours reading, comparing, and summarizing, you direct the AI on what to investigate and it handles the collection and organization — you focus on interpretation and decisions.

This primitive covers any workflow where the primary output is structured knowledge: competitive analysis, market research, literature reviews, due diligence reports, vendor comparisons, and internal knowledge synthesis. The AI gathers information, identifies patterns, and presents findings in a format you specify.

Research becomes particularly powerful when paired with MCP connections to your actual data sources — the AI can pull from your CRM, project management tools, internal wikis, and external databases rather than relying solely on web search or uploaded documents.

*Research is one of six use case primitives identified in OpenAI's [Identifying and Scaling AI Use Cases](../resources/openai-use-cases-report.md) guide. The examples here are adapted to be platform-agnostic and mapped to [Agentic Building Blocks](../agentic-building-blocks/index.md).*

## Key Characteristics

- **Output is structured knowledge** — findings, summaries, comparisons, or recommendations derived from multiple sources
- **Source quality matters** — the value of research depends on what sources the AI can access and how well it evaluates them
- **Synthesis is the differentiator** — the hard part isn't finding information, it's combining insights from multiple sources into something actionable
- **Benefits from iteration** — initial research reveals new questions worth investigating, making multi-turn conversations more effective than single prompts
- **Scales with tool access** — research that connects to live data sources (via MCP or agents) is vastly more useful than research limited to the model's training data

## When to Apply This Primitive

**Use Research when:**

- You need to gather and compare information from multiple sources
- The deliverable is a summary, analysis, or structured set of findings
- You're making a decision that requires understanding a landscape (vendors, competitors, options)
- You need to monitor ongoing changes in a domain (market shifts, regulatory updates, competitive moves)

**NOT the right primitive when:**

- The main output is a written piece for an audience (that's [Content Creation](content-creation.md))
- You're exploring ideas and strategies rather than gathering facts (that's [Ideation & Strategy](ideation-and-strategy.md))
- You're analyzing structured numerical data (that's [Data Analysis](data-analysis.md))

## Department Examples

| Department | Use Case | What AI Does | Typical Building Blocks |
|-----------|----------|-------------|------------------------|
| Marketing | Competitive analysis | Monitors competitor websites, press releases, and social media for positioning changes | Agent, MCP, Skill |
| Product | User research synthesis | Aggregates feedback from support tickets, surveys, and reviews into themed summaries | Prompt, Context, Agent |
| Sales | Account research | Compiles prospect background, recent news, financial data, and mutual connections before calls | Agent, MCP, Skill |
| Legal | Regulatory monitoring | Tracks regulatory changes relevant to the business and flags items requiring review | Agent, MCP |
| Finance | Market intelligence | Synthesizes analyst reports, earnings calls, and market data into briefings | Prompt, Context, Agent |
| IT/Operations | Vendor evaluation | Compares vendor capabilities, pricing, and reviews against requirements | Prompt, Context, Project |

## Building Block Patterns

| Complexity | Building Blocks | Example |
|-----------|----------------|---------|
| **Simple** | Prompt + Context | Upload three analyst reports and ask AI to compare their conclusions on a specific topic |
| **Intermediate** | Project + Agent | A research project where an agent searches the web, reads sources, and produces a structured brief |
| **Advanced** | Agent + MCP + Skill | An agent that monitors competitor websites via MCP, synthesizes changes weekly, and produces a formatted intelligence report using a skill |

## Use Cases

| | |
|---|---|
| **Department** | Sales |
| **Autonomy level** | Autonomous |
| **Building blocks** | Agent, MCP, Skill |
| **Problem** | Reps spend 30+ minutes researching each prospect before calls — manually checking LinkedIn, news, company website, and CRM history — and still miss relevant context |
| **Solution** | An agent that takes a prospect name and company, searches multiple sources (LinkedIn, news, CRM via MCP), and produces a structured one-page brief with company overview, recent events, mutual connections, and suggested talking points |

| | |
|---|---|
| **Department** | Marketing |
| **Autonomy level** | Autonomous |
| **Building blocks** | Agent, MCP, Skill |
| **Problem** | Competitive intelligence is always stale — the team only updates competitive positioning quarterly, missing real-time changes in competitor messaging, pricing, and features |
| **Solution** | A scheduled agent monitors competitor websites and social channels weekly via MCP, compares changes against the previous snapshot, and produces a delta report highlighting what changed and why it matters |

| | |
|---|---|
| **Department** | Product |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Agent |
| **Problem** | User feedback is scattered across support tickets, NPS surveys, app reviews, and Slack channels — synthesizing it into actionable themes takes days of manual review |
| **Solution** | An agent ingests feedback from multiple sources, categorizes it by theme and sentiment, and produces a prioritized summary with representative quotes and frequency data for each theme |

## Common Mistakes

**Treating AI research as authoritative without verification.** AI can synthesize information effectively, but it can also miss nuance, misinterpret sources, or lack access to the most current data. Use AI research as a starting point for human analysis, not a replacement.

**Asking for research without specifying the decision it supports.** "Research our competitors" produces generic results. "Compare our top three competitors' pricing models so we can decide whether to offer a free tier" produces actionable analysis. Frame research around the decision you need to make.

**Ignoring source limitations.** AI can only research what it can access. If your research requires proprietary databases, paywalled content, or internal systems, you need MCP connections or uploaded documents — not just a prompt asking the AI to "look into it."

## Related

- [AI Use Cases Overview](index.md) — all six primitives at a glance
- [Agents](../agentic-building-blocks/agents/index.md) — autonomous AI that can plan and execute multi-step research
- [MCP](../agentic-building-blocks/mcp/index.md) — connecting AI to external data sources for live research
- [Context](../agentic-building-blocks/context/index.md) — providing source documents and background knowledge
- [Automation](automation.md) — running research workflows on a schedule
- [Research Resources](research-resources.md) — curated reports, guides, and references
