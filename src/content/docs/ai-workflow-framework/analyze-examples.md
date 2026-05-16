---
title: "Analyze Examples — Sample AI Opportunity Reports"
description: Two complete AI Opportunity Report examples showing what the Analyze step produces — a Marketing Operations Manager and an AI Instructor.
---These are three synthetic AI Opportunity Reports showing what the Analyze step produces. Use them as a reference for format, level of detail, and how opportunities are classified on the [AI Workflow Design Matrix](../workflow-design-matrix/).

- **Example 1** — Marketing Operations Manager at a B2B SaaS company (Individual lens, 7 opportunities)
- **Example 2** — AI Instructor running courses and maintaining a knowledge base (Individual lens, 7 opportunities)
- **Example 3** — VP of Operations at a logistics company (Organizational lens, 5 opportunities)

Examples 1 and 2 use the **individual lens** — analyzing one person's workflows. Example 3 uses the **organizational lens** — analyzing value chain processes tied to business objectives. All three include every section the Analyze step produces: report header, summary table, top 3 recommendations, detailed opportunity cards grouped by autonomy level, workflow candidate summary, and classification definitions. Organizational-lens cards include three additional fields: Business Objective, Stakeholders, and Success Metrics.

---

## Example 1: Marketing Operations Manager

<details>
<summary>About this persona</summary>

Sarah Chen is a Marketing Operations Manager at a mid-size B2B SaaS company. She manages campaign reporting, lead operations, content production workflows, and marketing analytics. Her team uses HubSpot, Google Ads, LinkedIn Ads, Ahrefs, and Google Slides.

</details>
### Report Header

|                              |                                                                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Name**                     | Sarah Chen                                                                                                              |
| **Role**                     | Marketing Operations Manager, mid-size B2B SaaS company                                                                |
| **Date**                     | 2026-03-05                                                                                                              |
| **Opportunities identified** | 7                                                                                                                       |
| **Top recommendation**       | Campaign Performance Reporting — automates the most time-consuming weekly task with high reliability                    |

### Summary Table

| # | Opportunity | Autonomy | Involvement | Impact |
|---|------------|----------|-------------|--------|
| 1 | Campaign Performance Reporting | Deterministic | Automated | High |
| 2 | Lead Data Enrichment | Deterministic | Automated | High |
| 3 | Content Brief Generation | Guided | Augmented | High |
| 4 | Lead Scoring Model Tuning | Guided | Augmented | Medium |
| 5 | Email Sequence Optimization | Guided | Augmented | Medium |
| 6 | Competitive Content Monitoring | Autonomous | Automated | Medium |
| 7 | Campaign Budget Reallocation | Autonomous | Augmented | Low |

### Top Recommendations

1. **Campaign Performance Reporting** — Eliminates 4+ hours of weekly manual data pulling and formatting across three platforms, with zero judgment calls required.
2. **Lead Data Enrichment** — Standardizes and enriches messy CRM records at scale, directly improving lead routing accuracy and sales handoff quality.
3. **Content Brief Generation** — Cuts content brief creation from 90 minutes to 15 minutes per brief, freeing the team to focus on creative strategy instead of research compilation.

### Detailed Opportunity Cards

#### Deterministic

---

**#1 Campaign Performance Reporting**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
This is pure data aggregation and formatting — no judgment or creativity required. The inputs (HubSpot, Google Ads, LinkedIn Ads) are structured, the output format is fixed (weekly slide deck + email summary), and the logic is the same every week. Classic automation candidate.

**Current pain point:**
Every Monday morning, Sarah spends 3-4 hours pulling data from three ad platforms, copying numbers into a Google Sheet, calculating WoW changes, formatting a slide deck, and emailing it to the VP of Marketing. The process is tedious and error-prone — last month a copy-paste error overstated LinkedIn ROAS by 40%, which wasn't caught until the executive review.

**How AI helps:**
A deterministic workflow connects to HubSpot, Google Ads, and LinkedIn Ads APIs, pulls the previous week's campaign metrics, calculates period-over-period changes, populates a templated Google Slides deck, and emails the summary to stakeholders. Same logic every week, no decisions needed.

**Getting started:**
Start with one platform (Google Ads) and build a simple script that pulls last week's metrics and formats them into a markdown summary. Validate the numbers against a manual pull before expanding to all three sources.

---

**#2 Lead Data Enrichment**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Enrichment follows clear rules: look up company domain, match to firmographic database, fill in missing fields (industry, employee count, revenue range). No ambiguity in what "correct" looks like — either the data matches or it doesn't.

**Current pain point:**
New leads arrive from webinars and content downloads with incomplete data — often just name and email. Sarah's team manually researches each company on LinkedIn and Crunchbase to fill in firmographic fields before leads can be scored and routed. This takes 10-15 minutes per lead, and with 50+ new leads per week, it's a significant time drain that delays sales follow-up.

**How AI helps:**
An automated workflow triggers when a new lead enters HubSpot, extracts the email domain, queries enrichment APIs (Clearbit, Apollo) for firmographic data, fills in standardized fields, and flags any leads where enrichment confidence is below threshold for manual review.

**Getting started:**
Map the exact fields that need enrichment and the acceptable data sources. Test one enrichment API (like Clearbit) against 20 recent leads to measure match rate and data quality before building the full pipeline.

---

#### Guided

---

**#3 Content Brief Generation**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Content briefs follow a consistent structure (target audience, keywords, competitor angles, outline) but require judgment about messaging angle and competitive positioning. AI can do the research and draft; a human refines the strategic direction.

**Current pain point:**
The content team produces 8-10 blog posts per month. Each brief takes Sarah or her content strategist ~90 minutes: researching keywords in Ahrefs, reviewing top-ranking competitor articles, pulling relevant customer quotes from Gong, and structuring the brief. The research portion is 70% of the time, and the quality varies depending on who writes the brief.

**How AI helps:**
Given a topic and target keyword, AI researches search intent, analyzes top-ranking articles for gaps, pulls relevant data points from internal sources, and drafts a structured content brief. Sarah reviews the brief, adjusts the angle or emphasis, and approves it — turning a 90-minute task into a 15-minute review.

**Getting started:**
Take three recent content briefs that performed well and use them as examples. Prompt AI to generate a brief for next week's planned topic using the same structure, then compare the output to what the team would have written manually.

---

**#4 Lead Scoring Model Tuning**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Lead scoring requires analyzing conversion patterns across multiple attributes — something AI does well. But the business logic of what makes a "sales-ready" lead involves domain expertise and sales team input, making this a collaborative task.

**Current pain point:**
The current lead scoring model in HubSpot was set up 18 months ago and hasn't been recalibrated. Sarah suspects the weights are off — the sales team complains that "hot" leads often aren't ready to buy, while some "warm" leads convert quickly. Recalibrating requires exporting data, running correlation analysis, and proposing new weights, which keeps getting deprioritized.

**How AI helps:**
AI analyzes the last 12 months of lead-to-close data, identifies which attributes (job title, company size, content engagement, page visits) actually correlate with conversion, and proposes updated scoring weights with supporting evidence. Sarah reviews the recommendations with the sales team and decides which changes to implement.

**Getting started:**
Export the last 6 months of closed-won and closed-lost opportunities with their lead scores at time of handoff. Ask AI to identify the three attributes with the strongest correlation to conversion outcome.

---

**#5 Email Sequence Optimization**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Email optimization involves analyzing performance data and generating copy variations — AI excels at both pattern recognition in metrics and language generation. But brand voice, compliance, and strategic messaging decisions need human oversight.

**Current pain point:**
Sarah manages 12 active email nurture sequences. Reviewing performance, identifying underperforming emails, and writing A/B test variants is a monthly task that takes a full day. She often defaults to tweaking subject lines because rewriting full emails is too time-consuming, leaving bigger optimization opportunities on the table.

**How AI helps:**
AI analyzes open rates, click rates, and reply rates across all sequences, identifies the bottom performers, diagnoses likely issues (subject line, length, CTA placement, send time), and drafts optimized variants for A/B testing. Sarah reviews the analysis, selects which variants to test, and adjusts copy to match brand voice.

**Getting started:**
Pick the single worst-performing email sequence. Export its metrics and email copy, and ask AI to diagnose the weakest email and draft two alternative versions with different approaches.

---

#### Autonomous

---

**#6 Competitive Content Monitoring**

**Autonomy:** Autonomous
**Involvement:** Automated

**Why it's a good candidate:**
Monitoring competitors is an ongoing, open-ended research task where AI can independently decide what's worth flagging. The inputs are public (competitor blogs, social feeds, product pages) and the output is a curated digest — no human intervention needed during the monitoring itself.

**Current pain point:**
Sarah tries to keep tabs on 5 key competitors' content and messaging, but it's inconsistent — she checks their blogs when she remembers, usually before quarterly planning. The team often learns about competitor positioning changes reactively (from sales call objections) rather than proactively.

**How AI helps:**
An autonomous agent monitors competitor blogs, changelog pages, and social accounts on a weekly schedule. It identifies new content, detects messaging shifts or new feature announcements, and produces a weekly competitive digest with the 3-5 most notable changes and their implications for Sarah's content strategy.

**Getting started:**
List the 5 competitor blogs and their RSS feeds (or URLs to monitor). Set up a simple weekly prompt that checks each URL and summarizes anything new, delivered to a Slack channel.

---

**#7 Campaign Budget Reallocation**

**Autonomy:** Autonomous
**Involvement:** Augmented

**Why it's a good candidate:**
Budget optimization requires continuous analysis of spend vs. performance across channels — a data-heavy task where AI can independently model scenarios and propose reallocations. However, budget decisions have direct financial impact, so human approval is essential.

**Current pain point:**
Campaign budgets are set quarterly and adjusted monthly based on performance. Sarah spends half a day each month analyzing cost-per-lead and ROAS across channels, modeling "what if" scenarios in a spreadsheet, and proposing reallocations to the VP. The analysis is always backward-looking, and by the time changes are implemented, market conditions have shifted.

**How AI helps:**
An autonomous agent continuously monitors campaign performance against targets, models reallocation scenarios based on current trends, and proactively recommends budget shifts when it detects a channel significantly over- or under-performing. Sarah receives a notification with the recommended change, supporting data, and projected impact — she approves or adjusts before any budget moves.

**Getting started:**
Define the three key metrics and thresholds that should trigger a reallocation review (e.g., "CPL exceeds target by 20% for 5+ consecutive days"). Start with alerts only — no automated changes — to calibrate sensitivity.

---

### Workflow Candidate Summary

Based on impact, frequency, and feasibility, the following three candidates are recommended for the Deconstruct step:

#### Candidate 1: Campaign Performance Reporting

| Field | Content |
|-------|---------|
| **Workflow** | Campaign Performance Reporting |
| **Description** | Aggregates weekly campaign metrics from three ad platforms into a formatted slide deck and email summary |
| **Trigger** | Scheduled — every Monday at 7:00 AM |
| **Deliverable** | Google Slides deck + email summary sent to VP of Marketing |
| **Autonomy** | Deterministic |
| **Involvement** | Automated |
| **Pain point** | 3-4 hours of manual data pulling and formatting every Monday, with copy-paste errors that erode trust in the numbers |
| **AI opportunity** | Connect to platform APIs, pull metrics, calculate WoW changes, populate slide template, and send summary email — zero human steps during execution |
| **Frequency** | Weekly |
| **Priority** | High |
| **Reasoning** | Highest time savings (4 hrs/week), zero ambiguity in logic, and directly addresses a reliability issue that affects executive trust |

#### Candidate 2: Lead Data Enrichment

| Field | Content |
|-------|---------|
| **Workflow** | Lead Data Enrichment |
| **Description** | Automatically enriches new inbound leads with firmographic data from external APIs |
| **Trigger** | Event — new lead created in HubSpot |
| **Deliverable** | Enriched lead record with firmographic fields populated in HubSpot |
| **Autonomy** | Deterministic |
| **Involvement** | Automated |
| **Pain point** | 10-15 minutes of manual research per lead, 50+ leads/week, delays sales follow-up |
| **AI opportunity** | Extract email domain, query enrichment APIs, populate standardized CRM fields, flag low-confidence matches for review |
| **Frequency** | Daily (triggered per lead) |
| **Priority** | High |
| **Reasoning** | High volume, direct impact on sales velocity, and straightforward to implement with existing enrichment APIs |

#### Candidate 3: Content Brief Generation

| Field | Content |
|-------|---------|
| **Workflow** | Content Brief Generation |
| **Description** | Researches and drafts structured content briefs for the blog editorial calendar |
| **Trigger** | Request — content strategist submits a topic and target keyword |
| **Deliverable** | Structured content brief (audience, keywords, competitor analysis, outline, key points) |
| **Autonomy** | Guided |
| **Involvement** | Augmented |
| **Pain point** | 90 minutes per brief, mostly spent on repetitive research; quality varies by author |
| **AI opportunity** | AI handles keyword research, competitor article analysis, and brief drafting; human refines strategic angle and approves |
| **Frequency** | Weekly (8-10 per month) |
| **Priority** | High |
| **Reasoning** | Large time savings per brief (75 min), high frequency, and directly improves content quality consistency |

**Recommendation:** Start with **Campaign Performance Reporting**. It's the simplest to build (deterministic, well-defined inputs/outputs), delivers immediate visible value to leadership, and builds confidence in AI workflows before tackling the more nuanced guided and autonomous candidates.

---

## Example 2: AI Instructor

<details>
<summary>About this persona</summary>

James Gray is an AI Instructor who runs live cohort courses and maintains the Hands-on AI Playbook — a documentation site with setup guides, framework content, and an MCP server. His work spans teaching, content creation, student support, and meeting with prospective clients and partners.

</details>
### Report Header

|                              |                                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Name**                     | James Gray                                                                                               |
| **Role**                     | AI Instructor and course creator, Hands-on AI Playbook                                                   |
| **Date**                     | 2026-03-05                                                                                               |
| **Opportunities identified** | 7                                                                                                        |
| **Top recommendation**       | Student Q&A Research — directly improves the core teaching experience while saving significant prep time |

### Summary Table

| # | Opportunity | Autonomy | Involvement | Impact |
|---|------------|----------|-------------|--------|
| 1 | Lesson Slide Formatting | Deterministic | Automated | Medium |
| 2 | Post-Class Summary Generation | Deterministic | Automated | Medium |
| 3 | Student Q&A Research | Guided | Augmented | High |
| 4 | Assignment Feedback Drafting | Guided | Augmented | High |
| 5 | Course Content Updates | Guided | Augmented | Medium |
| 6 | Meeting Prep Briefs | Autonomous | Automated | Medium |
| 7 | Newsletter Curation | Autonomous | Augmented | Low |

### Top Recommendations

1. **Student Q&A Research** — Turns ad-hoc student questions into well-sourced, reusable answers, building the playbook's knowledge base while improving response quality and speed.
2. **Assignment Feedback Drafting** — Scales personalized, actionable feedback across cohorts without sacrificing quality — the highest-leverage activity for student outcomes.
3. **Lesson Slide Formatting** — Eliminates the tedious formatting step between content creation and delivery, freeing time for higher-value lesson design.

### Detailed Opportunity Cards

#### Deterministic

---

**#1 Lesson Slide Formatting**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Slide formatting follows strict rules — heading hierarchy, font sizes, code block styling, brand colors. There's no creative judgment in the formatting step itself; the content is already decided. It's pure template application.

**Current pain point:**
After writing lesson content in markdown, James spends 30-45 minutes per lesson manually formatting slides — adjusting font sizes, adding code syntax highlighting, ensuring consistent spacing, and applying the course brand template. With 12+ lessons per course and multiple courses, this adds up to full days of formatting work per quarter.

**How AI helps:**
A deterministic workflow takes the lesson markdown file, parses it by heading structure, maps content blocks to slide templates (title slides, content slides, code slides, exercise slides), applies consistent formatting rules, and outputs a formatted slide deck. Same rules every time.

**Getting started:**
Document the formatting rules for one slide type (e.g., code demonstration slides) and build a script that converts a markdown section into a properly formatted slide. Test against three recent lessons.

---

**#2 Post-Class Summary Generation**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Class summaries follow a fixed structure: topics covered, key takeaways, action items, links to resources mentioned. The input (class recording transcript + lesson plan) is well-defined, and the output format doesn't vary.

**Current pain point:**
After each live session, James writes a summary email to students recapping what was covered, highlighting key concepts, and listing homework or next steps. This takes 20-30 minutes per session, and it's always the first thing that gets skipped when time is tight — meaning students miss the reinforcement.

**How AI helps:**
An automated workflow ingests the class transcript (from Zoom or recording tool), cross-references it with the lesson plan, extracts the topics actually covered, identifies key discussion points, and generates a structured summary email in the standard format. Sent automatically within an hour of class ending.

**Getting started:**
Take a recent class recording transcript and the corresponding lesson plan. Prompt AI to generate a summary email following the standard format. Compare it to a manually-written summary to calibrate quality.

---

#### Guided

---

**#3 Student Q&A Research**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Student questions often require researching current documentation, comparing platform features, or synthesizing information across multiple sources — tasks where AI is fast and thorough. But the answer needs to be pedagogically appropriate (right level of detail, connected to course concepts), which requires instructor judgment.

**Current pain point:**
Students ask questions via Slack, email, and in class that go beyond the prepared material — "How does this work in Gemini?", "What's the difference between X and Y?", "Can you show an example of Z?" James spends 15-30 minutes per question researching current docs, testing examples, and crafting a thoughtful answer. With 10-15 questions per week across cohorts, this is 3-5 hours of reactive work.

**How AI helps:**
Given a student question, AI researches current documentation (via MCP server and web search), finds relevant examples, drafts an answer at the appropriate level for the course, and cites sources. James reviews the draft, adjusts the pedagogical framing, and posts the response. The answer is also saved to the playbook for future reference.

**Getting started:**
Collect the last 10 student questions from Slack. Run three of them through AI with the prompt: "Research this question for a student in an introductory AI course. Provide a clear answer with sources and a practical example." Evaluate whether the answers are accurate and at the right level.

---

**#4 Assignment Feedback Drafting**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Feedback benefits from pattern recognition (identifying common mistakes, referencing rubric criteria, suggesting specific improvements) combined with instructor perspective on what matters most for each student's growth. AI handles the analysis; the instructor adds the coaching touch.

**Current pain point:**
James reviews 15-25 student assignments per cohort. Each piece of feedback takes 10-15 minutes: reading the submission, checking it against the rubric, identifying strengths and areas for improvement, and writing personalized comments. A full round of feedback takes 4-6 hours, and the turnaround time directly affects student momentum.

**How AI helps:**
AI reads each submission alongside the rubric and assignment prompt, identifies what was done well, flags gaps or misunderstandings, and drafts specific, constructive feedback with references to relevant course material. James reviews each draft, adds personal observations, adjusts tone, and approves before sending.

**Getting started:**
Take three completed assignments from the last cohort along with the rubric. Have AI draft feedback for each, then compare the drafts to the feedback James actually gave. Note where AI feedback was on-target and where it missed the mark.

---

**#5 Course Content Updates**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
AI platforms release updates frequently, and checking whether course content is still accurate involves comparing current docs against existing lesson material — a tedious but critical task. AI can do the comparison; the instructor decides what's worth updating.

**Current pain point:**
Platform updates (new Claude features, changed OpenAI pricing, deprecated Gemini APIs) can make course material outdated overnight. James periodically audits lessons against current documentation, but it's reactive — he often discovers outdated content when a student flags it in class. A full content audit across 30+ pages takes a full day.

**How AI helps:**
Given a lesson page and the relevant platform documentation, AI compares the two and identifies discrepancies — changed features, outdated screenshots references, deprecated terminology, new capabilities worth mentioning. It drafts specific suggested edits with reasoning. James reviews, decides which updates are worth making now, and applies the changes.

**Getting started:**
Pick the three platform pages most likely to be outdated (e.g., Claude capabilities, OpenAI pricing, Gemini model list). Have AI compare each against current official documentation and list every discrepancy found.

---

#### Autonomous

---

**#6 Meeting Prep Briefs**

**Autonomy:** Autonomous
**Involvement:** Automated

**Why it's a good candidate:**
Meeting prep involves independently researching attendees, companies, and topics across multiple sources, then synthesizing findings into a structured brief. The AI needs to decide what's relevant and how deep to go — classic autonomous research pattern. The output is consumed as-is (read before the meeting), so no real-time collaboration is needed.

**Current pain point:**
James has 5-8 external meetings per week — prospective clients, conference organizers, partnership discussions, guest lecturers. Before each meeting, he spends 15-20 minutes researching the person and company on LinkedIn, their website, and recent news. Some meetings get thorough prep; others get none because of time pressure, leading to missed context.

**How AI helps:**
An autonomous agent triggers from the calendar 2 hours before each external meeting. It researches each attendee (LinkedIn, company website, recent publications), identifies relevant connections to the AI education space, notes any previous interactions, and delivers a structured brief to a designated channel. James reads it on the way to the meeting.

**Getting started:**
Take tomorrow's meetings and manually create the ideal prep brief for one of them. Then prompt AI to generate the same brief from just the meeting title and attendee names. Compare coverage and identify what sources AI needs access to.

---

**#7 Newsletter Curation**

**Autonomy:** Autonomous
**Involvement:** Augmented

**Why it's a good candidate:**
Newsletter curation requires scanning many sources, filtering for relevance, and organizing findings — a broad monitoring task well-suited to autonomous operation. But editorial judgment about what's actually interesting to the audience (and how to frame it) benefits from human review.

**Current pain point:**
James curates a periodic newsletter of AI developments relevant to his students and audience. Scanning RSS feeds, Twitter/X, AI news sites, and research papers takes 1-2 hours per edition. The inconsistency of the publishing schedule (sometimes biweekly, sometimes monthly) reflects the time pressure — it's always the lowest-priority task.

**How AI helps:**
An autonomous agent continuously monitors configured sources (RSS feeds, specific Twitter accounts, arXiv, AI news sites), filters for topics relevant to practical AI adoption, and compiles a weekly digest of the top 5-7 items with one-paragraph summaries. James reviews the digest, removes irrelevant items, adds personal commentary, and publishes.

**Getting started:**
List the 10 sources James checks most often for AI news. Set up a weekly prompt that checks each source and summarizes the top 3 items from each, then ask AI to select the overall top 7 most relevant to "business professionals learning to use AI tools."

---

### Workflow Candidate Summary

Based on impact, frequency, and feasibility, the following three candidates are recommended for the Deconstruct step:

#### Candidate 1: Student Q&A Research

| Field              | Content                                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Workflow**       | Student Q&A Research                                                                                                              |
| **Description**    | Researches student questions and drafts sourced, pedagogically appropriate answers                                                |
| **Trigger**        | Request — student posts a question in Slack or email                                                                              |
| **Deliverable**    | Draft answer with sources and examples, ready for instructor review and posting                                                   |
| **Autonomy**       | Guided                                                                                                                            |
| **Involvement**    | Augmented                                                                                                                         |
| **Pain point**     | 15-30 minutes per question, 10-15 questions/week — reactive research that fragments focused work time                             |
| **AI opportunity** | AI researches docs, finds examples, and drafts an answer at the right course level; instructor reviews and adjusts before posting |
| **Frequency**      | Daily                                                                                                                             |
| **Priority**       | High                                                                                                                              |
| **Reasoning**      | Highest frequency, directly improves the student experience, and each answer becomes reusable content in the playbook             |

#### Candidate 2: Assignment Feedback Drafting

| Field              | Content                                                                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Workflow**       | Assignment Feedback Drafting                                                                                                              |
| **Description**    | Drafts personalized assignment feedback based on rubric criteria and submission content                                                   |
| **Trigger**        | Event — assignment submission deadline passes                                                                                             |
| **Deliverable**    | Draft feedback for each submission, ready for instructor review and delivery                                                              |
| **Autonomy**       | Guided                                                                                                                                    |
| **Involvement**    | Augmented                                                                                                                                 |
| **Pain point**     | 10-15 minutes per submission, 15-25 per cohort — slow turnaround affects student momentum                                                 |
| **AI opportunity** | AI reads submissions against rubric, identifies strengths and gaps, drafts specific constructive feedback with course material references |
| **Frequency**      | Weekly (during active cohorts)                                                                                                            |
| **Priority**       | High                                                                                                                                      |
| **Reasoning**      | High impact on student outcomes, significant time savings (4-6 hrs per round), and faster turnaround improves the learning loop           |

#### Candidate 3: Meeting Prep Briefs

| Field              | Content                                                                                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Workflow**       | Meeting Prep Briefs                                                                                                                                                |
| **Description**    | Autonomously researches attendees and generates structured prep briefs before external meetings                                                                    |
| **Trigger**        | Scheduled — 2 hours before each external calendar event                                                                                                            |
| **Deliverable**    | Structured meeting brief delivered to a Slack channel or document                                                                                                  |
| **Autonomy**       | Autonomous                                                                                                                                                         |
| **Involvement**    | Automated                                                                                                                                                          |
| **Pain point**     | 15-20 minutes per meeting, 5-8 meetings/week — inconsistent prep quality due to time pressure                                                                      |
| **AI opportunity** | AI independently researches attendees, identifies relevant context, and delivers a ready-to-read brief with no human steps during execution                        |
| **Frequency**      | Daily                                                                                                                                                              |
| **Priority**       | Medium                                                                                                                                                             |
| **Reasoning**      | High frequency and fully automatable — moderate impact per meeting but compounds across 5-8 weekly meetings; also a good proof-of-concept for autonomous workflows |

**Recommendation:** Start with **Student Q&A Research**. It's the highest-frequency opportunity, directly improves the core teaching experience, and produces a tangible artifact (the answer) that compounds in value as it builds the playbook's knowledge base. It's also a natural fit for the tools already in place (MCP server, web search, markdown output).

---

## Example 3: VP of Operations (Organizational Lens)

<details>
<summary>About this persona</summary>

Maria Torres is VP of Operations at a 200-person logistics company. She oversees warehouse operations, fleet management, and customer fulfillment. She's looking at AI from an organizational perspective — identifying value chain processes where AI can improve outcomes tied to business objectives. This example demonstrates the **organizational lens**.

</details>
### Report Header

|                              |                                                                                                    |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| **Name**                     | Maria Torres                                                                                       |
| **Role**                     | VP of Operations, mid-size logistics company                                                       |
| **Date**                     | 2026-03-05                                                                                         |
| **Lens**                     | Organizational                                                                                     |
| **Opportunities identified** | 5                                                                                                  |
| **Top recommendation**       | Customer Onboarding — highest impact on customer retention, the company's top strategic objective   |

### Summary Table

| # | Opportunity | Autonomy | Involvement | Impact |
|---|------------|----------|-------------|--------|
| 1 | Customer Onboarding | Guided | Augmented | High |
| 2 | Order Fulfillment Tracking | Deterministic | Automated | High |
| 3 | Carrier Rate Negotiation Prep | Guided | Augmented | Medium |
| 4 | Fleet Maintenance Scheduling | Autonomous | Automated | Medium |
| 5 | Demand Forecasting | Autonomous | Augmented | Medium |

### Top Recommendations

1. **Customer Onboarding** — A cross-functional process spanning sales, ops, and account management that directly impacts customer retention (the #1 business objective). Inconsistent execution leads to early churn.
2. **Order Fulfillment Tracking** — End-to-end visibility from order receipt through delivery confirmation. Currently manual status checks create delays in exception handling.
3. **Carrier Rate Negotiation Prep** — Quarterly process that requires synthesizing shipment volume data, carrier performance metrics, and market rate benchmarks — highly data-intensive research that AI can accelerate.

### Detailed Opportunity Cards

#### Guided

---

**#1 Customer Onboarding**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Onboarding follows a structured sequence (account setup, system configuration, initial shipment planning, training) but requires judgment at multiple points — which service tier, which warehouse assignment, which carrier mix. AI can handle research, drafting, and coordination; humans make the key decisions.

**Current pain point:**
New customer onboarding takes 2-3 weeks and involves sales, operations, and account management. Each team owns different steps, and handoffs are where things break — incomplete information passes between teams, setup tasks get missed, and the customer's first shipment experience sets the tone for the relationship. There's no single owner for the end-to-end outcome.

**How AI helps:**
AI orchestrates the onboarding sequence: pre-populates account configuration from the signed contract, drafts a warehouse assignment recommendation based on the customer's shipping patterns, generates a carrier mix proposal, creates a personalized training schedule, and tracks completion across all teams. Account manager reviews and approves key decisions.

**Getting started:**
Map the current onboarding process across all three teams. Identify which handoff points have the highest failure rate and start by automating status tracking and notifications at those points.

**Business Objective:** Improve customer retention rate from 85% to 92%
**Stakeholders:** Sales (handoff), Operations (setup), Account Management (relationship owner)
**Success Metrics:** Time-to-first-shipment, onboarding completion rate, 90-day customer satisfaction score

---

**#3 Carrier Rate Negotiation Prep**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Rate negotiation prep is research-heavy: gathering shipment volumes by lane, analyzing carrier on-time performance, benchmarking against market rates, and preparing a negotiation brief. AI excels at data synthesis; the negotiation strategy requires human judgment.

**Current pain point:**
Quarterly carrier negotiations require 2-3 days of prep. The logistics manager pulls shipment data from the TMS, calculates lane-by-lane volumes, reviews carrier scorecards, researches competitor rate benchmarks, and assembles a briefing document. By the time the brief is ready, some of the market data is already stale.

**How AI helps:**
AI pulls shipment volume data and carrier performance metrics from the TMS, benchmarks against published rate indices, identifies lanes where current rates are above market, and produces a negotiation brief with recommended rate targets and supporting evidence. Logistics manager reviews the brief, adjusts strategy based on relationship factors, and enters negotiations prepared.

**Getting started:**
Export last quarter's shipment data by carrier and lane. Have AI analyze the top 10 lanes by volume and compare current rates to published benchmarks. Evaluate whether the analysis matches the logistics manager's intuition.

**Business Objective:** Reduce transportation costs by 8% through better carrier rate management
**Stakeholders:** Logistics Manager (prep + negotiation), VP Operations (approval), Finance (budget impact)
**Success Metrics:** Average rate reduction per lane, negotiation prep time, rate variance vs. market benchmark

---

#### Deterministic

---

**#2 Order Fulfillment Tracking**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Status tracking follows fixed rules: order received → picked → packed → shipped → delivered. Each stage transition is a data event from the WMS or TMS. No judgment needed — just monitoring, matching, and alerting.

**Current pain point:**
Customer service reps manually check order status across the WMS and TMS when customers call. Exception detection (delayed shipments, partial picks, missed delivery windows) relies on someone noticing — there's no proactive alerting. The team spends 3-4 hours daily on reactive status checks, and customers often know about problems before the ops team does.

**How AI helps:**
A deterministic workflow monitors order lifecycle events from the WMS and TMS, updates a real-time status dashboard, and triggers automated alerts when orders deviate from expected timelines (e.g., pick not started within 2 hours of order receipt, shipment not scanned within delivery window). No decisions needed — fixed rules, fixed thresholds, fixed notifications.

**Getting started:**
Define the 5 most common exception scenarios and their alert thresholds. Build a simple status check for one exception type (e.g., "shipment not departed within 4 hours of scheduled pickup") and validate against historical data.

**Business Objective:** Achieve 98% on-time delivery rate (currently 94%)
**Stakeholders:** Warehouse Manager (pick/pack), Logistics Coordinator (shipping), Customer Service (communication)
**Success Metrics:** Exception detection time, proactive alert rate, customer inquiry volume reduction

---

#### Autonomous

---

**#4 Fleet Maintenance Scheduling**

**Autonomy:** Autonomous
**Involvement:** Automated

**Why it's a good candidate:**
Maintenance scheduling requires analyzing multiple data streams (mileage, engine hours, maintenance history, upcoming delivery commitments) and making independent scheduling decisions that balance vehicle uptime with maintenance needs. The AI can plan autonomously because the constraints are clear and the decisions are bounded.

**Current pain point:**
Fleet maintenance is tracked in a spreadsheet. The fleet manager checks mileage and schedules services based on manufacturer intervals, but competing delivery commitments mean vehicles often run past due. Unplanned breakdowns cost 3-5x more than scheduled maintenance and disrupt delivery schedules.

**How AI helps:**
An autonomous agent continuously monitors vehicle telemetry (mileage, engine hours, diagnostic codes), cross-references against maintenance schedules and upcoming delivery commitments, and automatically schedules maintenance during low-utilization windows. Generates work orders for the maintenance shop and adjusts the delivery schedule around planned downtime.

**Getting started:**
Export the current fleet roster with last maintenance dates and mileage. Have AI identify the 5 vehicles most overdue for service and propose a maintenance schedule that minimizes delivery disruption for the next 30 days.

**Business Objective:** Reduce unplanned vehicle downtime by 50%
**Stakeholders:** Fleet Manager (scheduling), Maintenance Shop (execution), Dispatch (route adjustment)
**Success Metrics:** Planned vs. unplanned maintenance ratio, average vehicle uptime %, maintenance cost per mile

---

**#5 Demand Forecasting**

**Autonomy:** Autonomous
**Involvement:** Augmented

**Why it's a good candidate:**
Demand forecasting requires analyzing historical shipment patterns, seasonal trends, customer growth trajectories, and external signals (economic indicators, industry events). AI can independently model scenarios and generate forecasts; human review adds market intuition and customer-specific knowledge.

**Current pain point:**
Monthly capacity planning relies on the VP's experience and a basic spreadsheet model. Seasonal demand shifts, new customer ramp-ups, and one-time events aren't systematically factored in. Over-forecasting wastes warehouse labor; under-forecasting creates overtime costs and missed SLAs.

**How AI helps:**
An autonomous agent analyzes 24 months of shipment history, identifies seasonal patterns and growth trends per customer, incorporates known upcoming events (new customer launches, holiday peaks), and generates a 90-day demand forecast with confidence intervals. Maria reviews the forecast, adjusts for factors the model can't see (a large customer hinted at a contract change), and approves the capacity plan.

**Getting started:**
Export 12 months of daily shipment volumes by customer. Have AI identify the top 3 seasonal patterns and compare its next-month forecast against actual volumes from a previous period to calibrate accuracy.

**Business Objective:** Optimize warehouse labor costs while maintaining SLA compliance
**Stakeholders:** VP Operations (approval), Warehouse Manager (staffing), Finance (labor budget)
**Success Metrics:** Forecast accuracy (MAPE), labor cost variance, SLA compliance rate

---

### Workflow Candidate Summary

Based on strategic impact, cross-functional complexity, and feasibility, the following three candidates are recommended for the Deconstruct step:

#### Candidate 1: Customer Onboarding

| Field | Content |
|-------|---------|
| **Workflow** | Customer Onboarding |
| **Description** | Orchestrates the end-to-end process of setting up new customers from signed contract through first successful shipment |
| **Trigger** | Event — new customer contract signed in CRM |
| **Deliverable** | Fully configured customer account with completed first shipment and satisfaction survey |
| **Autonomy** | Guided |
| **Involvement** | Augmented |
| **Pain point** | 2-3 week onboarding with frequent handoff failures between sales, ops, and account management — leading to poor first impressions and early churn |
| **AI opportunity** | AI orchestrates the sequence, pre-populates configurations, recommends warehouse and carrier assignments, tracks cross-team completion, and alerts on delays |
| **Frequency** | Weekly (3-5 new customers per month) |
| **Priority** | High |
| **Reasoning** | Directly addresses the #1 business objective (customer retention), involves the most painful cross-functional handoffs, and improvements compound across every new customer |
| **Lens** | Organizational |
| **Business Objective** | Improve customer retention rate from 85% to 92% |
| **Stakeholders** | Sales, Operations, Account Management |
| **Success Metrics** | Time-to-first-shipment, onboarding completion rate, 90-day CSAT |

#### Candidate 2: Order Fulfillment Tracking

| Field | Content |
|-------|---------|
| **Workflow** | Order Fulfillment Tracking |
| **Description** | Monitors order lifecycle from receipt through delivery and proactively alerts on exceptions |
| **Trigger** | Event — new order created in WMS |
| **Deliverable** | Real-time order status dashboard + automated exception alerts |
| **Autonomy** | Deterministic |
| **Involvement** | Automated |
| **Pain point** | 3-4 hours daily of reactive status checks; customers learn about problems before the ops team |
| **AI opportunity** | Automated monitoring of WMS/TMS events with rule-based exception detection and proactive alerting — no human involvement during execution |
| **Frequency** | Continuous (hundreds of orders daily) |
| **Priority** | High |
| **Reasoning** | Highest volume, directly impacts on-time delivery (key SLA metric), and deterministic nature makes it straightforward to implement |
| **Lens** | Organizational |
| **Business Objective** | Achieve 98% on-time delivery rate |
| **Stakeholders** | Warehouse, Logistics, Customer Service |
| **Success Metrics** | Exception detection time, proactive alert rate, customer inquiry volume |

#### Candidate 3: Carrier Rate Negotiation Prep

| Field | Content |
|-------|---------|
| **Workflow** | Carrier Rate Negotiation Prep |
| **Description** | Synthesizes shipment data, carrier performance, and market rates into a negotiation-ready brief |
| **Trigger** | Scheduled — 3 weeks before quarterly carrier review |
| **Deliverable** | Negotiation brief with lane-by-lane analysis, rate benchmarks, and recommended targets |
| **Autonomy** | Guided |
| **Involvement** | Augmented |
| **Pain point** | 2-3 days of manual data gathering and analysis per quarter; market data goes stale during prep |
| **AI opportunity** | AI pulls and analyzes shipment/carrier data, benchmarks against market rates, and produces a draft brief — logistics manager refines strategy and enters negotiations prepared |
| **Frequency** | Quarterly |
| **Priority** | Medium |
| **Reasoning** | High financial impact per occurrence (rate negotiations affect millions in annual spend) but lower frequency; good candidate once higher-frequency workflows are running |
| **Lens** | Organizational |
| **Business Objective** | Reduce transportation costs by 8% |
| **Stakeholders** | Logistics Manager, VP Operations, Finance |
| **Success Metrics** | Average rate reduction, prep time, rate vs. market benchmark |

**Recommendation:** Start with **Customer Onboarding**. It's the highest-impact opportunity tied directly to the company's top strategic objective (customer retention). While it's more complex than Order Fulfillment Tracking, the cross-functional visibility and structured handoffs it creates will improve operations far beyond the onboarding process itself. Order Fulfillment Tracking is the natural second candidate — deterministic and automated, it provides quick wins while the onboarding workflow is being developed.

---

## Appendix: Classification Definitions

**Autonomy — How much decision-making does the AI have?**

- **Deterministic**: AI follows fixed rules — no decisions, no judgment. Same input produces same output every time. Examples: formatting reports, processing forms, data extraction, template-driven outputs.
- **Guided**: AI makes bounded decisions within guardrails. The human sets direction; AI chooses how to accomplish the task within those bounds. Examples: drafting emails, researching a topic, co-writing, data analysis.
- **Autonomous**: AI plans, decides, and adapts independently. It determines what to do, uses tools, and adjusts its approach based on what it finds. Examples: competitor monitoring, research-to-report pipelines, intake-to-triage systems.

**Human Involvement — Is a human in the loop during execution?**

- **Augmented**: Human participates during the workflow run — reviews, steers, or decides at key points. AI and human collaborate in real time.
- **Automated**: AI runs solo — executes end-to-end without human intervention during the run. Human reviews only the final output.
