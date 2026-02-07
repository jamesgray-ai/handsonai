---
name: finding-ai-opportunities
description: >
  Discover where AI can improve your workflows through a structured audit.
  Produces a prioritized report of opportunities across three categories:
  Deterministic Workflows, Collaborative AI, and Autonomous Agents.
  This is Phase 1 of the Business-First AI Framework.
---

# Finding AI Opportunities

Discover concrete opportunities where AI can improve your workflows. Produces a categorized report with a summary table and detailed opportunity cards.

## Workflow

Work through four steps in order:

### Step 1 — Memory & History Scan

Before asking any questions, review everything you already know about the user from conversation history, memory, project files, or any other available context.

Identify and list:
- Their role, responsibilities, and domain
- Recurring tasks or requests they perform
- Pain points, frustrations, or bottlenecks they've mentioned
- Workflows or processes they've described or demonstrated
- Tools and platforms they use regularly
- Any goals or priorities they've shared

Present your findings as a brief summary so the user can confirm or correct them before continuing. If you have no prior context, say so and move directly to Step 2.

### Step 2 — Targeted Discovery Interview

Based on gaps in your understanding (or starting from scratch), ask focused questions to build a complete picture. Cover these areas:

1. **Role & responsibilities** — What is your role? What are you accountable for?
2. **Repetitive tasks** — What tasks do you perform daily or weekly that feel repetitive, tedious, or low-value?
3. **Information synthesis** — Where do you spend time gathering, combining, or making sense of information from multiple sources?
4. **Multi-step processes** — What workflows involve multiple handoffs, approvals, or sequential steps?
5. **Quality & consistency** — Where do errors, inconsistencies, or quality issues tend to creep in?
6. **Communication overhead** — What recurring communications (status updates, reports, summaries) take more time than they should?
7. **Decision-making** — What decisions require you to weigh multiple factors or reference past precedents?

Ask these questions **one at a time** — not as a list. Use the user's answers to ask smart follow-up questions. Probe for concrete examples: "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting." Continue until you can identify at least 3 concrete opportunities — typically 5-10 questions, fewer if the memory scan provided strong context.

### Step 3 — Opportunity Analysis & Report

Once you can identify at least 3 concrete, specific opportunities with enough detail to fill the card format below, produce the structured report.

### Step 4 — Workflow Candidate Summary

After presenting the full report, ask the user to pick ONE opportunity from each category that they want to build during the course. Once they've chosen, produce a **Workflow Candidate Summary** in this exact format:

```markdown
- **Workflow:** [name]
- **Type:** Deterministic
- **Pain point:** [1 sentence]
- **AI opportunity:** [1 sentence]

- **Workflow:** [name]
- **Type:** Collaborative AI
- **Pain point:** [1 sentence]
- **AI opportunity:** [1 sentence]

- **Workflow:** [name]
- **Type:** Autonomous Agent
- **Pain point:** [1 sentence]
- **AI opportunity:** [1 sentence]
```

Append this summary to the output file under a `## Workflow Candidate Summary` heading.

## Output

Write the report to `outputs/ai-opportunity-report.md`. Create the `outputs/` directory if it doesn't exist.

The report must include:

### Summary Table

| # | Opportunity | Category | Impact |
|---|------------|----------|--------|
| 1 | [Name] | Deterministic Workflow / Collaborative AI / Autonomous Agent | High / Medium / Low |

### Detailed Opportunity Cards

Group cards by category. Within each category, order from highest to lowest impact.

For each opportunity:

---

**[#] [Opportunity Name]**

**Category:** Deterministic Workflow | Collaborative AI | Autonomous Agent

**Why it's a good candidate:**
[What characteristics make this well-suited for AI — repetitive, pattern-based, language-heavy, clear inputs/outputs, etc.]

**Current pain point:**
[What's slow, error-prone, inconsistent, or draining about how this is done today]

**How AI helps:**
[Specific, concrete description — what AI takes as input, what it produces, how it fits into the workflow]

**Getting started:**
[A practical, low-effort first step achievable this week]

---

### Category Definitions

Use these definitions when categorizing:

- **Deterministic Workflow**: A repeatable process with clear inputs, rules, and outputs that AI can execute reliably with minimal supervision. Examples: formatting reports, processing forms, generating routine communications, data transformation.
- **Collaborative AI**: Human and AI work together in real time. The human drives the process; AI contributes suggestions, drafts, analysis, or feedback. Examples: co-writing, brainstorming, code review, data analysis.
- **Autonomous Agent**: A goal-driven workflow where AI plans and executes steps autonomously. The agent reasons about what to do, calls tools as needed, and adapts its approach. Ranges from a single agent handling a complex task to multi-agent systems where specialized agents coordinate across steps. Examples: competitor monitoring and alerting, research → analysis → report pipelines, intake → triage → routing systems.

## Guidelines

- Ask one question at a time — never present a wall of questions
- Use a conversational flow — let answers guide follow-up questions naturally
- Push for concrete examples over vague descriptions
- Be specific in recommendations: "AI could draft the weekly status email from your Jira board data" beats "AI could help with reporting"
- After writing the report, ask the user to pick their three candidates (one per category) for Step 4. Once they've chosen, append the Workflow Candidate Summary to the output file and tell the user: "Opportunity report and Workflow Candidate Summary saved to `outputs/ai-opportunity-report.md`. Your candidate summary is ready to copy into your course assignment."
