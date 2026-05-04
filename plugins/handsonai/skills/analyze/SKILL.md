---
name: analyze
description: >
  This skill should be used when the user wants to analyze AI workflow opportunities,
  run a workflow audit, find automation candidates, or says "where can AI help".
  Scans memory and conversation history, interviews the user about their work,
  then produces a prioritized opportunity report with structured workflow
  candidates ready for the Deconstruct step. This is Step 1 of the Business-First AI Framework.
user-invocable: true
---

# Analyze Workflows

Analyze concrete opportunities where AI can improve your workflows. Produces a categorized opportunity report with a summary table, detailed opportunity cards, and a structured workflow candidate list.

## Workflow

### Fast Path

If the user arrives with pre-identified workflows (e.g., "I already know I want to automate X, Y, and Z"), skip Steps 1-2. Infer the lens from what they describe — individual tasks (personal reporting, email triage) = Individual lens; multi-role or business-objective workflows (customer onboarding, sales pipeline) = Organizational lens. Confirm the inferred lens with the user. Go straight to Step 3 (Opportunity Analysis & Report) using what they've provided, then Step 4 (Workflow Candidate Summary).

### Standard Path

Work through four steps in order:

#### Step 1 — Memory & History Scan

Before asking any questions, review everything you already know about the user from conversation history, memory, project files, or any other available context.

Identify and list:
- Their role, responsibilities, and domain
- Recurring tasks or requests they perform
- Pain points, frustrations, or bottlenecks they've mentioned
- Workflows or processes they've described or demonstrated
- Tools and platforms they use regularly
- Any goals or priorities they've shared

Present your findings as a brief summary so the user can confirm or correct them before continuing. If you have no prior context, say so and move directly to Step 2.

#### Step 1.5 — Lens Selection

After presenting the memory scan summary (or noting no prior context), ask the user which lens to use:

> **Individual lens** — Workflows you personally perform in your role (reporting, email triage, content creation, etc.)
>
> **Organizational lens** — Workflows critical to delivering on your business outcomes — your value chain, cross-functional processes, and strategic operations (customer onboarding, sales pipeline, product delivery, etc.)
>
> Which lens should we start with?

**Inference rule:** If user context makes the answer obvious (e.g., "I want to improve our company's onboarding"), infer and confirm rather than asking: "Based on what you've described, the organizational lens fits best — we'll focus on your business's value chain processes. Sound right?"

#### Step 2 — Targeted Discovery Interview

Based on gaps in your understanding (or starting from scratch), ask focused questions to build a complete picture. Use the question set for the user's chosen lens.

**Individual Lens — Discovery Questions**

1. **Role & responsibilities** — What is your role? What are you accountable for?
2. **Repetitive tasks** — What tasks do you perform daily or weekly that feel repetitive, tedious, or low-value?
3. **Information synthesis** — Where do you spend time gathering, combining, or making sense of information from multiple sources?
4. **Multi-step processes** — What workflows involve multiple handoffs, approvals, or sequential steps?
5. **Quality & consistency** — Where do errors, inconsistencies, or quality issues tend to creep in?
6. **Communication overhead** — What recurring communications (status updates, reports, summaries) take more time than they should?
7. **Decision-making** — What decisions require you to weigh multiple factors or reference past precedents?

**Organizational Lens — Discovery Questions**

1. **Business objectives & outcomes** — What are your top 2-3 business objectives or OKRs? What outcomes drive success?
2. **Value chain & core processes** — What are the key end-to-end processes that deliver on those outcomes? (lead-to-close, hire-to-onboard, order-to-fulfill, etc.)
3. **Cross-functional handoffs** — Where do processes cross team boundaries? Where do things fall through cracks?
4. **Bottlenecks & cycle time** — Which processes take too long? Where do things stall waiting on people, approvals, or information?
5. **Consistency & quality risk** — Where do different people handle the same process differently? Where does inconsistency create risk?
6. **Visibility & measurement gaps** — Which processes lack metrics on performance, cycle time, or quality?
7. **Scale constraints** — Which processes break when volume increases? What works for 10 customers but not 100?

**Adaptive ordering:** Start with the areas where Step 1 revealed the least. Skip areas already well-covered by the memory scan — no need to re-ask what you already know.

Ask these questions **one at a time** — not as a list. Use the user's answers to ask smart follow-up questions. Probe for concrete examples: "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."

**Handling vague answers:** If the user gives vague responses after 2-3 probes on a topic, move on. If answers are vague across all areas, shift to hypothesis mode. For the individual lens: "Based on your role, I'd guess you spend time on X — is that right?" For the organizational lens: "For a [size] [industry] company, the value chain processes that typically benefit most from AI are X, Y, Z — do any of those resonate?"

**Transition signal:** When you've identified 3+ concrete opportunities, tell the user: "I've identified [N] opportunities so far. I have enough to put together the report — do you want to add anything else, or should I go ahead?" Let them add more or confirm before proceeding.

Continue until you can identify at least 3 concrete opportunities — typically 5-10 questions, fewer if the memory scan provided strong context.

#### Step 3 — Opportunity Analysis & Report

Once you can identify at least 3 concrete, specific opportunities with enough detail to fill the card format below, produce the structured report.

#### Step 4 — Workflow Candidate Summary

After presenting the full report, ask the user to pick their top workflow candidates — the ones they want to build. Once they've chosen, produce a **Workflow Candidate Summary** with structured metadata for each candidate:

For each candidate:

| Field | Content |
|-------|---------|
| **Workflow** | 2-4 word noun phrase, Title Case |
| **Description** | One sentence describing what this workflow does |
| **Trigger** | What kicks off this workflow — an event, schedule, or request |
| **Deliverable** | The tangible output — what gets produced, sent, or decided |
| **Autonomy** | Deterministic / Guided / Autonomous |
| **Involvement** | Augmented / Automated |
| **Pain point** | What's slow, error-prone, or manual today |
| **AI opportunity** | Specific description of what AI would do |
| **Frequency** | Daily / Weekly / Monthly / Ad-hoc |
| **Priority** | High / Medium / Low |
| **Reasoning** | Why this priority level — based on impact, frequency, and feasibility |
| **Lens** | Individual / Organizational |
| **Business Objective** | (Organizational only) Which strategic objective this workflow supports |
| **Stakeholders** | (Organizational only) Roles/teams involved |
| **Success Metrics** | (Organizational only) KPIs for measuring improvement |

Append this summary to the output file under a `## Workflow Candidate Summary` heading. Recommend which candidate to deconstruct first, with reasoning.

#### Step 5 — Second Lens Follow-Up

After completing the report and candidate selection for the first lens:

> "We've identified [N] workflow candidates from an [individual/organizational] perspective. Would you also like to explore the [other] lens?"

**If individual first:** "...the organizational lens looks at your business value chain — the cross-functional processes that deliver on strategic objectives like revenue growth or customer satisfaction."

**If organizational first:** "...the individual lens looks at your personal workflows — the repetitive tasks in your day-to-day role where AI could save you time or improve quality."

If user accepts, run discovery questions for the second lens. Append new candidates to the same report, tagged with their lens. Update the report header Lens field to "Individual + Organizational." Then proceed to candidate selection across both sets.

If user declines, proceed to next framework step.

## Output

Write the report to `outputs/ai-opportunity-report.md`. Create the `outputs/` directory if it doesn't exist. If the file already exists, rename the existing file to `ai-opportunity-report-YYYY-MM-DD.md` (using today's date) before writing the new one.

The report must include (in this order):

### Report Header

| | |
|---|---|
| **Name** | [User's name if known, otherwise omit row] |
| **Role** | [Role and domain] |
| **Date** | [YYYY-MM-DD] |
| **Lens** | Individual / Organizational / Individual + Organizational |
| **Opportunities identified** | [count] |
| **Top recommendation** | [#1 priority opportunity + one-sentence reason] |

### Summary Table

| # | Opportunity | Autonomy | Involvement | Impact |
|---|------------|----------|-------------|--------|
| 1 | [Name] | Deterministic / Guided / Autonomous | Augmented / Automated | High / Medium / Low |

### Top Recommendations

List the top 3 opportunities in priority order with a one-sentence rationale for each.

### Detailed Opportunity Cards

Group cards by autonomy level (Deterministic → Guided → Autonomous). Within each group, order from highest to lowest impact.

For each opportunity:

---

**[#] [Opportunity Name]**

**Autonomy:** Deterministic | Guided | Autonomous
**Involvement:** Augmented | Automated

**Why it's a good candidate:**
[What characteristics make this well-suited for AI — repetitive, pattern-based, language-heavy, clear inputs/outputs, etc.]

**Current pain point:**
[What's slow, error-prone, inconsistent, or draining about how this is done today]

**How AI helps:**
[Specific, concrete description — what AI takes as input, what it produces, how it fits into the workflow]

**Getting started:**
[A practical, low-effort first step achievable this week]

**Business Objective:** [Organizational lens only — which strategic objective this workflow supports]
**Stakeholders:** [Organizational lens only — roles/teams involved (process owner + participants)]
**Success Metrics:** [Organizational lens only — KPIs for measuring improvement]

---

### Workflow Candidate Summary

(Appended after user selects candidates — see Step 4 format above)

### Appendix: Classification Definitions

Use these definitions when classifying opportunities:

**Autonomy — How much decision-making does the AI have?**

- **Deterministic**: AI follows fixed rules — no decisions, no judgment. Same input produces same output every time. Examples: formatting reports, processing forms, data extraction, template-driven research.
- **Guided**: AI makes bounded decisions within guardrails. The human sets direction; AI chooses how to accomplish the task within those bounds. Examples: drafting emails, researching a topic, brainstorming, co-writing, data analysis.
- **Autonomous**: AI plans, decides, and adapts independently. It determines what to do, uses tools, and adjusts its approach based on what it finds. Examples: competitor monitoring, research → analysis → report pipelines, intake → triage → routing systems.

**Human Involvement — Is a human in the loop during execution?**

- **Augmented**: Human participates during the workflow run — reviews, steers, or decides at key points. AI and human collaborate in real time.
- **Automated**: AI runs solo — executes end-to-end without human intervention during the run. Human reviews only the final output.

## Guidelines

- Ask one question at a time — never present a wall of questions
- Use a conversational flow — let answers guide follow-up questions naturally
- Push for concrete examples over vague descriptions
- Be specific in recommendations: "AI could draft the weekly status email from your Jira board data" beats "AI could help with reporting"
- **Individual lens:** Scope each workflow candidate to one person's trigger-to-deliverable flow. If a workflow spans multiple people, note the cross-team dependencies in the opportunity card but keep the candidate focused on a single owner's scope.
- **Organizational lens:** Scope each workflow candidate to one trigger-to-deliverable flow, even if it spans multiple roles. Identify the process owner (accountable for the end-to-end outcome) and list participating roles.
- After writing the report, ask the user to pick their candidates for Step 4. Once they've chosen, append the Workflow Candidate Summary and tell the user: "Opportunity report and workflow candidates saved to `outputs/ai-opportunity-report.md`. Pick a candidate and start the Deconstruct step to break it down."
