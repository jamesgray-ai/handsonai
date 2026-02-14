---
title: Coding
description: AI use cases for generating, debugging, porting, and explaining code — from spreadsheet formulas to full applications
---

# Coding

## What Coding Is

Coding use cases have AI generate, debug, port, refactor, and explain code. This primitive extends far beyond traditional software engineering — it includes anyone who needs to create scripts, formulas, queries, macros, or technical artifacts as part of their work.

A marketing manager writing an Excel formula, a data analyst creating a SQL query, an operations lead building a Google Apps Script, and a software engineer writing a microservice — all of these are coding use cases. The AI handles the translation from intent to working technical implementation.

Coding is the primitive where AI agents are most mature. Modern AI coding agents can plan an approach, write code, run tests, debug failures, and iterate — handling multi-file changes across entire projects with minimal human guidance.

*Coding is one of six use case primitives identified in OpenAI's [Identifying and Scaling AI Use Cases](../resources/openai-use-cases-report.md) guide. The examples here are adapted to be platform-agnostic and mapped to [Agentic Building Blocks](../agentic-building-blocks/index.md).*

## Key Characteristics

- **Output is executable** — the deliverable is code, scripts, formulas, or queries that run and produce results
- **Testable and verifiable** — unlike content or research, code either works or it doesn't, making quality assessment straightforward
- **Amplifies non-technical users** — people who understand what they need but can't write code can now create technical solutions
- **Benefits from iteration** — AI can write, run, see errors, and fix them in a loop, converging on working solutions
- **Context accelerates quality** — existing codebase, documentation, and examples help AI produce code that fits your patterns and standards

## When to Apply This Primitive

**Use Coding when:**

- The deliverable is something that executes — code, scripts, formulas, queries, or macros
- You need to translate a business requirement into a technical implementation
- You're debugging, refactoring, or porting existing code
- Non-technical team members need technical artifacts (Excel formulas, SQL queries, simple scripts)

**NOT the right primitive when:**

- The main output is a written document (that's [Content Creation](content-creation.md))
- You're analyzing data and the insight is the deliverable, not the analysis code (that's [Data Analysis](data-analysis.md))
- You're creating a pipeline that runs autonomously (that's [Automation](automation.md) — though coding may be a step within it)

## Department Examples

| Department | Use Case | What AI Does | Typical Building Blocks |
|-----------|----------|-------------|------------------------|
| Engineering | Feature development | Plans, writes, tests, and debugs features across multiple files | Agent, Context, MCP |
| Marketing | Dashboard formulas | Creates complex spreadsheet formulas and Google Sheets scripts from plain-language descriptions | Prompt, Context |
| Finance | Financial models | Builds Excel models and Python scripts for scenario analysis | Prompt, Context, Skill |
| Sales | CRM automation scripts | Writes scripts to automate CRM data entry, lead scoring, and pipeline management | Prompt, Context, Agent |
| HR | Workflow automation | Creates Google Apps Scripts or Power Automate flows for approval processes | Prompt, Context |
| IT/Operations | Infrastructure scripts | Generates deployment scripts, monitoring configurations, and automation tooling | Agent, Context, MCP |

## Building Block Patterns

| Complexity | Building Blocks | Example |
|-----------|----------------|---------|
| **Simple** | Prompt + Context | Ask AI to write a VLOOKUP formula, providing the spreadsheet structure as context |
| **Intermediate** | Agent + Context | An AI agent that reads your codebase, writes a new feature, runs the tests, and iterates until they pass |
| **Advanced** | Agent + MCP + Context | An agent connected to your repository (via MCP) that handles pull requests end-to-end — writing code, running CI, addressing review comments |

## Use Cases

| | |
|---|---|
| **Department** | Finance |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context |
| **Problem** | Building financial models in Excel takes hours of formula debugging — nested IF statements, VLOOKUP chains, and array formulas are error-prone and hard to verify |
| **Solution** | Describe the model logic in plain language with sample data as context. AI generates the formulas, explains each step, and troubleshoots errors when the results don't match expectations |

| | |
|---|---|
| **Department** | Engineering |
| **Autonomy level** | Autonomous |
| **Building blocks** | Agent, Context, MCP |
| **Problem** | Routine development tasks (bug fixes, test writing, dependency updates, small features) consume senior engineer time that should go to architecture and design |
| **Solution** | An AI coding agent reads the issue, explores the codebase, writes the implementation, runs tests, and creates a pull request. Senior engineers review the output rather than writing it themselves |

| | |
|---|---|
| **Department** | Marketing |
| **Autonomy level** | Collaborative |
| **Building blocks** | Prompt, Context, Skill |
| **Problem** | The marketing team needs data pulled from multiple spreadsheets and combined into reports, but they depend on engineering for any formula or script work — creating a bottleneck |
| **Solution** | A skill that takes a plain-language description of what data to combine and how, generates the appropriate Google Sheets formulas or Apps Script, and explains how to use it. Marketing becomes self-sufficient for routine data tasks |

## Common Mistakes

**Accepting code without testing it.** AI-generated code often works but may have subtle bugs, security issues, or edge cases. Always run the code, verify the output, and test edge cases before deploying — especially for code that handles sensitive data or runs in production.

**Providing requirements without examples.** "Build a script that processes our invoices" is vague. "Build a script that reads CSV files with columns [date, vendor, amount, category], groups by category, and outputs a summary with totals — here's a sample file" produces working code on the first try.

**Confusing coding with data analysis.** If the goal is the insight (what are our spending trends?), the primitive is [Data Analysis](data-analysis.md). If the goal is the tool (build me a script that analyzes spending), the primitive is Coding. The distinction matters because it changes how you evaluate the output.

## Related

- [AI Use Cases Overview](index.md) — all six primitives at a glance
- [Agents](../agentic-building-blocks/agents/index.md) — autonomous coding agents that plan, write, test, and iterate
- [Context](../agentic-building-blocks/context/index.md) — providing codebases, documentation, and examples
- [Data Analysis](data-analysis.md) — when the insight is the goal, not the code
- [Automation](automation.md) — when code runs as part of an unattended pipeline
- [Coding Resources](coding-resources.md) — curated reports, guides, and references
