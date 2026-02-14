---
title: Data Analysis
description: AI use cases for harmonizing data from multiple sources, identifying trends, and producing visualizations and insights
---

# Data Analysis

## What Data Analysis Is

Data analysis use cases have AI harmonize data from multiple sources, identify trends and patterns, and produce visualizations and insights. The AI handles the tedious work — cleaning, formatting, merging, and pattern recognition — while you direct the analysis and interpret the results.

This primitive covers any workflow where the primary output is an insight derived from data: trend reports, anomaly detection, forecasting, benchmarking, and exploratory analysis. The data can come from spreadsheets, databases, APIs, or documents — the AI adapts to whatever format you provide.

Data analysis is often the highest-value primitive for teams that have data but lack the time or technical skills to extract meaning from it. AI dramatically lowers the barrier to working with data, letting anyone ask questions of their datasets in plain language.

*Data Analysis is one of six use case primitives identified in OpenAI's [Identifying and Scaling AI Use Cases](../resources/openai-use-cases-report.md) guide. The examples here are adapted to be platform-agnostic and mapped to [Agentic Building Blocks](../agentic-building-blocks/index.md).*

## Key Characteristics

- **Output is insights, not raw data** — the deliverable is an interpretation, trend, pattern, or recommendation based on data
- **Source data quality is everything** — AI can't fix garbage data, but it can identify inconsistencies and suggest cleanup steps
- **Exploratory by nature** — the best data analysis is iterative: initial findings suggest new questions worth investigating
- **Visual outputs are powerful** — charts, graphs, and dashboards often communicate insights more effectively than text summaries
- **Combines well with other primitives** — data analysis frequently feeds into content creation (reports), ideation (strategy), and automation (alerting)

## When to Apply This Primitive

**Use Data Analysis when:**

- You have data and need to extract meaning, patterns, or trends from it
- You need to harmonize data from multiple sources into a single view
- The deliverable is a chart, dashboard, trend report, or data-driven recommendation
- You want to explore a dataset to find what's interesting before deciding what to investigate further

**NOT the right primitive when:**

- The main output is code or a reusable tool for analyzing data (that's [Coding](coding.md))
- You're gathering qualitative information from documents and sources (that's [Research](research.md))
- You're running a data pipeline on a schedule without human involvement (that's [Automation](automation.md))

## Department Examples

| Department | Use Case | What AI Does | Typical Building Blocks |
|-----------|----------|-------------|------------------------|
| Finance | Expense analysis | Harmonizes expense data from multiple systems, categorizes spending, and identifies anomalies | Prompt, Context, Skill |
| Marketing | Campaign performance | Combines data from ad platforms, web analytics, and CRM to show what's working and what isn't | Prompt, Context, Agent |
| Sales | Pipeline analysis | Analyzes deal stage durations, conversion rates, and win/loss patterns across the pipeline | Prompt, Context, Skill |
| HR | Workforce analytics | Identifies retention patterns, compensation benchmarks, and headcount trends from HR data | Prompt, Context |
| Product | Usage analytics | Analyzes product usage data to identify adoption patterns, feature engagement, and churn indicators | Prompt, Context, Agent |
| Operations | Process efficiency | Measures cycle times, bottlenecks, and throughput across operational workflows | Prompt, Context, Skill |

## Building Block Patterns

| Complexity | Building Blocks | Example |
|-----------|----------------|---------|
| **Simple** | Prompt + Context | Upload a CSV and ask AI to identify the top trends, outliers, and patterns |
| **Intermediate** | Skill + Context | A skill that takes monthly sales data, compares to previous periods, and produces a formatted performance report with charts |
| **Advanced** | Agent + MCP + Skill | An agent that pulls data from multiple sources via MCP, harmonizes it, runs analysis, and produces a dashboard with commentary |

## Use Cases

| | |
|---|---|
| **Department** | Finance |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Skill |
| **Problem** | Monthly expense reporting requires manually downloading data from three systems, reformatting columns, reconciling categories, and producing summary charts — a full day of work that delays month-end close |
| **Solution** | A skill that takes the three data exports as input, harmonizes column names and categories, flags discrepancies, and produces a summary report with breakdowns by department, category, and variance from budget |

| | |
|---|---|
| **Department** | Marketing |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Agent |
| **Problem** | Campaign performance data lives in five different platforms (Google Ads, Meta, LinkedIn, HubSpot, GA4), making cross-channel comparison a manual spreadsheet exercise that's always out of date |
| **Solution** | An agent that ingests data exports from each platform, normalizes metrics (impressions, clicks, conversions, cost), and produces a unified performance view with channel comparison and recommendations for budget reallocation |

| | |
|---|---|
| **Department** | HR |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context |
| **Problem** | Leadership wants quarterly retention and compensation insights but the HR team spends weeks pulling data, anonymizing it, and creating visualizations — by the time it's ready, the data is already old |
| **Solution** | Upload anonymized HR data and ask AI to analyze retention patterns by department, tenure, and compensation band. AI identifies at-risk segments, produces visualizations, and suggests areas for deeper investigation |

## Common Mistakes

**Uploading data without explaining what it is.** A CSV with columns "A, B, C, D" gives the AI nothing to work with. Provide column descriptions, units, time periods, and what questions you want answered. The better you describe your data, the better the analysis.

**Expecting AI to validate its own analysis.** AI can identify patterns, but it can't tell you whether those patterns are meaningful in your business context. A correlation in the data might be a real signal or a coincidence — that judgment requires your domain expertise.

**Skipping data cleaning.** AI can work with messy data, but inconsistent formats, missing values, and duplicate records will produce unreliable results. Ask AI to identify data quality issues first, fix them, then run the analysis.

## Related

- [AI Use Cases Overview](index.md) — all six primitives at a glance
- [Context](../agentic-building-blocks/context/index.md) — providing datasets and domain knowledge
- [Skills](../agentic-building-blocks/skills/index.md) — packaging analysis workflows for repeatable use
- [Coding](coding.md) — when the goal is the analysis tool itself, not the insight
- [Automation](automation.md) — running analysis workflows on a schedule
- [Data Analysis Resources](data-analysis-resources.md) — curated reports, guides, and references
