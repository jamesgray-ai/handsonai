---
title: "Analyze Examples — Sample AI Opportunity Reports"
description: Three complete AI Opportunity Report examples showing what the Analyze step produces — a Marketing Operations Manager, an AI Instructor, and a VP of Operations.
---

These are three synthetic AI Opportunity Reports showing what the Analyze step produces. Use them as a reference for format, level of detail, and how each opportunity's process, value lever, and size are stated.

- **Example 1** — Marketing Operations Manager at a B2B SaaS company (Individual lens, 7 opportunities)
- **Example 2** — AI Instructor running courses and maintaining a knowledge base (Individual lens, 7 opportunities)
- **Example 3** — VP of Operations at a logistics company (Organizational lens, 5 opportunities)

Examples 1 and 2 use the **individual lens** — analyzing one person's workflows. Example 3 uses the **organizational lens** — analyzing value chain processes tied to business objectives. Each opportunity carries one value lever (see the [value lever definitions](#appendix-value-lever-definitions)): Streamline when the work still happens the same way with fewer steps, Automate when a person stops doing it, Accelerate when the outcome arrives sooner, Create value when something becomes possible that wasn't done before. All three include every section the Analyze step produces: report header, summary table, detailed opportunity cards grouped by process, a workflow candidate summary that covers every opportunity, and value lever definitions. Each card states its size in the person's own numbers, or says it isn't sized yet. Nothing is ranked: choosing which workflow to build is the first move in [Deconstruct](../deconstruct/). Organizational-lens cards include three additional fields: Business Objective, Stakeholders, and Success Metrics. How much the AI decides and who takes part while it runs are assessed later, in [Design](../design/), once the steps are known.

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
| **Lens** | Individual |
| **Opportunities identified** | 7                                                                                                                       |

The Organizational lens hasn't been run yet.

### Summary Table

| # | Opportunity | Process | Value lever | Size |
|---|------------|---------|-------------|------|
| 1 | Campaign Performance Reporting | Campaign Reporting | Automate | 3-4 hours every Monday |
| 2 | Lead Data Enrichment | Lead Operations | Automate | 10-15 minutes per lead, 50+ leads a week |
| 3 | Lead Scoring Model Tuning | Lead Operations | Create value | Not sized yet |
| 4 | Content Brief Generation | Content Production | Accelerate | About 90 minutes per brief, 8-10 briefs a month |
| 5 | Competitive Content Monitoring | Content Production | Create value | Not sized yet |
| 6 | Email Sequence Optimization | Marketing Analytics | Accelerate | A full day each month across 12 sequences |
| 7 | Campaign Budget Reallocation | Marketing Analytics | Accelerate | Half a day each month |

### Detailed Opportunity Cards

#### Campaign Reporting

---

**#1 Campaign Performance Reporting**

**Why it's a good candidate:**
The same steps every week: gather last week's metrics from the same three sources, calculate the changes, fill the fixed template, send the summary. The inputs are known, the output format never varies, and nothing about the work needs a judgment call.

**Current pain point:**
Every Monday morning, Sarah spends 3-4 hours pulling data from three ad platforms, copying numbers into a Google Sheet, calculating WoW changes, formatting a slide deck, and emailing it to the VP of Marketing. The process is tedious and error-prone — last month a copy-paste error overstated LinkedIn ROAS by 40%, which wasn't caught until the executive review.

**How AI helps:**
Takes in last week's campaign metrics from the three sources Sarah uses today and the standing slide template; produces the completed weekly deck with period-over-period changes and a short written summary, ready to send.

**Value lever:** Automate — Sarah stops doing the Monday pull entirely; the deck exists before she sits down.

**Size:** 3-4 hours every Monday.

**What changes for the business:**
The VP of Marketing gets the report first thing Monday instead of mid-morning, the numbers are calculated the same way every week, and the 3-4 hours return to campaign work. The copy-paste error class disappears.

**Systems involved today:** the three ad platforms, the Google Sheet, the slide deck, email.


#### Lead Operations

---

**#2 Lead Data Enrichment**

**Why it's a good candidate:**
Enrichment follows clear rules: look up the company, match it to a firmographic record, fill in the missing fields (industry, employee count, revenue range). No ambiguity in what "correct" looks like — either the data matches or it doesn't. The one branch, flagging low-confidence matches for a person to check, uses a confidence score the data source supplies.

**Current pain point:**
New leads arrive from webinars and content downloads with incomplete data — often just name and email. Sarah's team manually researches each company on LinkedIn and Crunchbase to fill in firmographic fields before leads can be scored and routed. This takes 10-15 minutes per lead, and with 50+ new leads per week, it's a significant time drain that delays sales follow-up.

**How AI helps:**
Takes in each new lead as it arrives, with whatever fields it came with; produces the same lead with industry, employee count, and revenue range filled in from an agreed firmographic source, plus a short list of leads whose match was too uncertain to trust, set aside for a person.

**Value lever:** Automate — the team stops researching companies by hand; the record is complete before anyone looks at it.

**Size:** 10-15 minutes per lead, 50+ leads a week.

**What changes for the business:**
Sales follow-up starts the same day a lead arrives instead of days later, scoring and routing run on complete records, and the team recovers roughly 10 hours a week of lookup work.

**Systems involved today:** the CRM, the webinar and content-download forms, LinkedIn and Crunchbase for lookups.


---

**#3 Lead Scoring Model Tuning**

**Why it's a good candidate:**
The analysis follows the same steps every time: take the closed deals, test which attributes correlate with conversion, propose new weights. The business logic of what makes a "sales-ready" lead needs domain expertise and sales team input, so Sarah reviews the proposal with the sales team before anything changes.

**Current pain point:**
The current lead scoring model in HubSpot was set up 18 months ago and hasn't been recalibrated. Sarah suspects the weights are off — the sales team complains that "hot" leads often aren't ready to buy, while some "warm" leads convert quickly. Recalibrating requires exporting data, running correlation analysis, and proposing new weights, which keeps getting deprioritized.

**How AI helps:**
Takes in the last 12 months of lead-to-close history with each lead's attributes and score at handoff; produces a short analysis of which attributes (job title, company size, content engagement, page visits) actually predicted conversion, and a proposed set of scoring weights with the evidence behind each. Sarah reviews the proposal with the sales team and decides what changes.

**Value lever:** Create value — there is no today version of this analysis: no recalibration has been done in 18 months, so there is nothing to compare against.

**Size:** Not sized yet — you can add today's number when the requirements are written.

**What changes for the business:**
"Hot" leads start meaning what sales expects them to mean, the handoff conversation between marketing and sales moves from complaints to evidence, and the model gets reviewed on a schedule instead of never.

**Systems involved today:** the CRM's lead scoring and opportunity history.


#### Content Production

---

**#4 Content Brief Generation**

**Why it's a good candidate:**
Content briefs follow a consistent structure (target audience, keywords, competitor angles, outline) and a set research sequence: keyword research, top-ranking competitor articles, customer quotes from recent calls, then the brief. Every brief goes through the same steps; Sarah reviews, adjusts the angle, and approves the draft before it goes to a writer.

**Current pain point:**
The content team produces 8-10 blog posts per month. Each brief takes Sarah or her content strategist ~90 minutes: researching keywords in Ahrefs, reviewing top-ranking competitor articles, pulling relevant customer quotes from Gong, and structuring the brief. The research portion is 70% of the time, and the quality varies depending on who writes the brief.

**How AI helps:**
Takes in a topic and target keyword; produces a structured brief in the team's standard shape — search intent, the gaps in top-ranking articles, relevant customer quotes, and an outline. Sarah reviews it, adjusts the angle or emphasis, and approves — turning a 90-minute task into a 15-minute review.

**Value lever:** Accelerate — a brief that took 90 minutes is ready for review in minutes, so the calendar stops waiting on research.

**Size:** About 90 minutes per brief, 8-10 briefs a month.

**What changes for the business:**
Eight to ten briefs a month reach writers earlier and in the same shape every time, the strategist's time moves from compiling research to choosing the angle, and brief quality stops depending on who wrote it.

**Systems involved today:** the keyword research tool, competitor blogs, call recordings.


---

**#5 Competitive Content Monitoring**

**Why it's a good candidate:**
The goal is clear — catch competitor positioning changes before sales hears about them on a call — and the work is research: when something new appears, check the pricing page, the docs, job postings, and press coverage until the change can be explained. The inputs are public and the output is a digest.

**Current pain point:**
Sarah tries to keep tabs on 5 key competitors' content and messaging, but it's inconsistent — she checks their blogs when she remembers, usually before quarterly planning. The team often learns about competitor positioning changes reactively (from sales call objections) rather than proactively.

**How AI helps:**
Takes in the five competitors' public presence — their blogs, release notes, and social accounts — each week; produces a digest of the 3-5 most notable changes with what each means for Sarah's content strategy. Where it finds a change it cannot yet explain, it keeps investigating until it can.

**Value lever:** Create value — there is no monitoring process today, only occasional glances before planning; a weekly digest is new work, not faster work.

**Size:** Not sized yet — you can add today's number when the requirements are written.

**What changes for the business:**
Sales hears about competitor positioning shifts from marketing before hearing them as objections on calls, and quarterly planning starts from a record of what changed rather than from memory.


#### Marketing Analytics

---

**#6 Email Sequence Optimization**

**Why it's a good candidate:**
The steps are set: pull the metrics, rank the sequences by open, click, and reply rates, diagnose the weakest emails, draft variants. The ranking is a metric sort. Brand voice, compliance, and which variants to test need a person, so Sarah reviews before anything goes out.

**Current pain point:**
Sarah manages 12 active email nurture sequences. Reviewing performance, identifying underperforming emails, and writing A/B test variants is a monthly task that takes a full day. She often defaults to tweaking subject lines because rewriting full emails is too time-consuming, leaving bigger optimization opportunities on the table.

**How AI helps:**
Takes in the month's open, click, and reply rates for all twelve sequences along with the email copy; produces a ranked list of the weakest emails, a likely diagnosis for each (subject line, length, call-to-action placement, send time), and two or three rewritten variants per email for testing. Sarah reviews, picks what to test, and adjusts copy to brand voice.

**Value lever:** Accelerate — a full day of monthly review becomes a two-hour pass, so whole-email rewrites get tested instead of only subject lines.

**Size:** A full day each month across 12 sequences.

**What changes for the business:**
Underperforming sequences get fixed in the month they underperform, the team tests bigger changes than it had time for, and nurture performance is reviewed on a steady monthly rhythm.

**Systems involved today:** the email automation platform's sequence reports.


---

**#7 Campaign Budget Reallocation**

**Why it's a good candidate:**
You set the structure and the method: the metrics and thresholds that define "off target", and how to model a reallocation. The AI uses your method to judge when a channel warrants a recommendation and which scenarios to model. Budget moves have direct financial impact, so Sarah approves every recommendation before any money moves.

**Current pain point:**
Campaign budgets are set quarterly and adjusted monthly based on performance. Sarah spends half a day each month analyzing cost-per-lead and ROAS across channels, modeling "what if" scenarios in a spreadsheet, and proposing reallocations to the VP. The analysis is always backward-looking, and by the time changes are implemented, market conditions have shifted.

**How AI helps:**
Takes in current campaign performance against the targets and thresholds Sarah sets; produces, whenever a channel runs significantly over or under target, a recommended budget shift with the supporting numbers and the projected effect. Sarah approves or adjusts before any money moves.

**Value lever:** Accelerate — the gain is measured in days between a channel drifting and the budget moving, down from a month.

**Size:** Half a day each month.

**What changes for the business:**
Budget moves within days of a channel drifting instead of at month end, every move comes with a stated rationale and projection, and the VP sees proposals continuously rather than in one monthly batch.

**Systems involved today:** the ad platforms' performance reports, the planning spreadsheet.

---

### Workflow Candidate Summary

#### Candidate 1: Campaign Performance Reporting

| Field | Content |
|-------|---------|
| **Workflow** | Campaign Performance Reporting |
| **Process** | Campaign Reporting |
| **Description** | Aggregates weekly campaign metrics from three ad platforms into a formatted slide deck and email summary |
| **Trigger** | Scheduled — every Monday at 7:00 AM |
| **Deliverable** | Google Slides deck + email summary sent to VP of Marketing |
| **Value lever** | Automate |
| **Pain point** | 3-4 hours of manual data pulling and formatting every Monday, with copy-paste errors that erode trust in the numbers |
| **AI opportunity** | Gather the week's metrics from the three sources, calculate WoW changes, fill the slide template, and send the summary |
| **Frequency** | Weekly |
| **Size** | 3-4 hours every Monday |

#### Candidate 2: Lead Data Enrichment

| Field | Content |
|-------|---------|
| **Workflow** | Lead Data Enrichment |
| **Process** | Lead Operations |
| **Description** | Completes each new inbound lead's firmographic fields from an agreed data source |
| **Trigger** | Event — new lead created in the CRM |
| **Deliverable** | Enriched lead record with firmographic fields populated in the CRM |
| **Value lever** | Automate |
| **Pain point** | 10-15 minutes of manual research per lead, 50+ leads/week, delays sales follow-up |
| **AI opportunity** | Identify the company from the lead, fill the standard firmographic fields, and set aside low-confidence matches for a person |
| **Frequency** | Daily (triggered per lead) |
| **Size** | 10-15 minutes per lead, 50+ leads a week |

#### Candidate 3: Lead Scoring Model Tuning

| Field | Content |
|-------|---------|
| **Workflow** | Lead Scoring Model Tuning |
| **Process** | Lead Operations |
| **Description** | Analyzes the last 12 months of lead-to-close history and proposes recalibrated lead scoring weights |
| **Trigger** | Request — Sarah starts a recalibration review |
| **Deliverable** | Analysis of which attributes predicted conversion, with proposed scoring weights and the evidence behind each |
| **Value lever** | Create value |
| **Pain point** | The scoring model hasn't been recalibrated in 18 months; sales says "hot" leads often aren't ready to buy, and the analysis keeps getting deprioritized |
| **AI opportunity** | Test which lead attributes predicted conversion and propose new weights with the evidence; Sarah reviews the proposal with the sales team |
| **Frequency** | Ad-hoc |
| **Size** | Not sized yet |

#### Candidate 4: Content Brief Generation

| Field | Content |
|-------|---------|
| **Workflow** | Content Brief Generation |
| **Process** | Content Production |
| **Description** | Researches and drafts structured content briefs for the blog editorial calendar |
| **Trigger** | Request — content strategist submits a topic and target keyword |
| **Deliverable** | Structured content brief (audience, keywords, competitor analysis, outline, key points) |
| **Value lever** | Accelerate |
| **Pain point** | 90 minutes per brief, mostly spent on repetitive research; quality varies by author |
| **AI opportunity** | AI handles keyword research, competitor article analysis, and brief drafting; human refines strategic angle and approves |
| **Frequency** | Weekly (8-10 per month) |
| **Size** | About 90 minutes per brief, 8-10 briefs a month |

#### Candidate 5: Competitive Content Monitoring

| Field | Content |
|-------|---------|
| **Workflow** | Competitive Content Monitoring |
| **Process** | Content Production |
| **Description** | Produces a weekly digest of the most notable changes in five competitors' public content and positioning |
| **Trigger** | Scheduled — weekly |
| **Deliverable** | Weekly digest of the 3-5 most notable competitor changes, with what each means for the content strategy |
| **Value lever** | Create value |
| **Pain point** | Competitor checks happen only when Sarah remembers, usually before quarterly planning; the team learns about positioning changes from sales call objections |
| **AI opportunity** | Review the five competitors' public presence each week, keep investigating a change until it can be explained, and summarize the most notable ones |
| **Frequency** | Weekly |
| **Size** | Not sized yet |

#### Candidate 6: Email Sequence Optimization

| Field | Content |
|-------|---------|
| **Workflow** | Email Sequence Optimization |
| **Process** | Marketing Analytics |
| **Description** | Reviews the performance of the 12 active nurture sequences and drafts test variants for the weakest emails |
| **Trigger** | Scheduled — monthly performance review |
| **Deliverable** | List of the weakest emails, each with a likely diagnosis and two or three rewritten variants for testing |
| **Value lever** | Accelerate |
| **Pain point** | A full day each month to review 12 sequences; whole-email rewrites get skipped in favor of subject-line tweaks |
| **AI opportunity** | Sort the sequences by open, click, and reply rates, diagnose the weakest emails, and draft variants; Sarah picks what to test and adjusts the copy to brand voice |
| **Frequency** | Monthly |
| **Size** | A full day each month across 12 sequences |

#### Candidate 7: Campaign Budget Reallocation

| Field | Content |
|-------|---------|
| **Workflow** | Campaign Budget Reallocation |
| **Process** | Marketing Analytics |
| **Description** | Recommends a budget shift whenever a channel runs significantly over or under target, with the supporting numbers and projected effect |
| **Trigger** | Event — a channel runs significantly over or under its target |
| **Deliverable** | Recommended budget shift with supporting numbers and the projected effect, for Sarah's approval |
| **Value lever** | Accelerate |
| **Pain point** | Half a day each month of backward-looking analysis; by the time changes are made, market conditions have shifted |
| **AI opportunity** | Compare channel performance with Sarah's targets and thresholds and model a reallocation when a channel drifts; Sarah approves before any money moves |
| **Frequency** | Ad-hoc (whenever a channel drifts off target) |
| **Size** | Half a day each month |

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
| **Lens** | Individual |
| **Opportunities identified** | 7                                                                                                        |

The Organizational lens hasn't been run yet.

### Summary Table

| # | Opportunity | Process | Value lever | Size |
|---|------------|---------|-------------|------|
| 1 | Post-Class Summary Generation | Teaching | Automate | 20-30 minutes per session |
| 2 | Assignment Feedback Drafting | Teaching | Accelerate | 10-15 minutes per submission, 4-6 hours per round of feedback |
| 3 | Course Content Updates | Content Creation | Streamline | A full day to audit 30+ pages |
| 4 | Lesson Slide Formatting | Content Creation | Automate | 30-45 minutes per lesson |
| 5 | Newsletter Curation | Content Creation | Streamline | 1-2 hours per edition |
| 6 | Student Q&A Research | Student Support | Accelerate | 15-30 minutes per question, 10-15 questions a week |
| 7 | Meeting Prep Briefs | Client and Partner Meetings | Create value | 15-20 minutes per meeting, 5-8 meetings a week |

### Detailed Opportunity Cards

#### Teaching

---

**#1 Post-Class Summary Generation**

**Why it's a good candidate:**
Class summaries follow a fixed structure: topics covered, key takeaways, action items, links to resources mentioned. The input (class recording transcript + lesson plan) is well-defined, and the output format doesn't vary. The AI writes the summary and the email goes out the same way every time.

**Current pain point:**
After each live session, James writes a summary email to students recapping what was covered, highlighting key concepts, and listing homework or next steps. This takes 20-30 minutes per session, and it's always the first thing that gets skipped when time is tight — meaning students miss the reinforcement.

**How AI helps:**
Takes in the session transcript and the lesson plan; produces the standard summary email — topics actually covered, key takeaways, action items, and the resources mentioned — ready to go out within an hour of class ending.

**Value lever:** Automate — the summary that gets skipped when time is tight now goes out every time without James writing it.

**Size:** 20-30 minutes per session.

**What changes for the business:**
Every student gets the reinforcement email after every session, not only the sessions with a quiet evening after them, and homework and next steps are stated the same way each week.

**Systems involved today:** the meeting recording and transcript, the lesson plan, email.


---

**#2 Assignment Feedback Drafting**

**Why it's a good candidate:**
Every submission goes through the same steps: read it against the rubric and assignment prompt, note strengths and gaps, draft feedback with references to course material. Every draft goes to James, who adds the coaching touch and approves it before it's sent.

**Current pain point:**
James reviews 15-25 student assignments per cohort. Each piece of feedback takes 10-15 minutes: reading the submission, checking it against the rubric, identifying strengths and areas for improvement, and writing personalized comments. A full round of feedback takes 4-6 hours, and the turnaround time directly affects student momentum.

**How AI helps:**
Takes in each submission, the rubric, and the assignment prompt; produces a draft of specific, constructive feedback — what was done well, where the gaps or misunderstandings are, and which course material to revisit. James reviews each draft, adds personal observations, adjusts tone, and approves before sending.

**Value lever:** Accelerate — a round of feedback that took 4-6 hours is reviewed in one, so students hear back in a day instead of a week.

**Size:** 10-15 minutes per submission, 4-6 hours per round of feedback.

**What changes for the business:**
Students get feedback while the assignment is still fresh, every submission is measured against the same rubric, and James's time goes to the coaching comments only he can write.

**Systems involved today:** the course platform's submissions, the rubric document.


#### Content Creation

---

**#3 Course Content Updates**

**Why it's a good candidate:**
AI platforms release updates frequently, and checking whether course content is still accurate means comparing current docs against existing lesson material — a tedious but critical task. The comparison runs the same way each time: you hand the AI the lesson page and the matching documentation, and it lists discrepancies and drafts edits. James decides which edits are worth making.

**Current pain point:**
Platform updates (new Claude features, changed OpenAI pricing, deprecated Gemini APIs) can make course material outdated overnight. James periodically audits lessons against current documentation, but it's reactive — he often discovers outdated content when a student flags it in class. A full content audit across 30+ pages takes a full day.

**How AI helps:**
Takes in a lesson page and the current official documentation it describes; produces a list of every discrepancy — changed features, stale screenshot references, deprecated terminology, new capabilities worth a mention — each with a suggested edit and the reason. James decides which updates are worth making now and applies them.

**Value lever:** Streamline — the audit still happens, but a day of page-by-page comparison becomes a review of a discrepancy list.

**Size:** A full day to audit 30+ pages.

**What changes for the business:**
Outdated content is found by the audit rather than by a student in class, and a full-course audit fits into a morning, so it happens after every major platform release instead of once a quarter.

**Systems involved today:** the course pages, the platforms' official documentation.


---

**#4 Lesson Slide Formatting**

**Why it's a good candidate:**
Slide formatting follows strict rules — heading hierarchy, font sizes, code block styling, brand colors. The steps are fixed: parse the Markdown, map each block to a slide template, apply the formatting rules. The content is already decided; this is pure template application.

**Current pain point:**
After writing lesson content in Markdown, James spends 30-45 minutes per lesson manually formatting slides — adjusting font sizes, adding code syntax highlighting, ensuring consistent spacing, and applying the course brand template. With 12+ lessons per course and multiple courses, this adds up to full days of formatting work per quarter.

**How AI helps:**
Takes in the finished lesson text and the course's formatting rules; produces the formatted slide deck — title, content, code, and exercise slides — with the brand template applied. Same rules every time.

**Value lever:** Automate — James stops formatting slides; the deck is ready when the lesson text is.

**Size:** 30-45 minutes per lesson.

**What changes for the business:**
Full days of quarterly formatting return to lesson design, every deck looks the same, and a last-minute content change no longer means an hour of reformatting.

**Systems involved today:** the lesson files, the slide tool, the brand template.


---

**#5 Newsletter Curation**

**Why it's a good candidate:**
The sources are configured in advance and the structure is set: check each source, judge each item's relevance to practical AI adoption, summarize the top items. The relevance judgment, made by James's criteria, decides which items make the digest. James reviews it, removes items, and adds commentary before he publishes.

**Current pain point:**
James curates a periodic newsletter of AI developments relevant to his students and audience. Scanning RSS feeds, Twitter/X, AI news sites, and research papers takes 1-2 hours per edition. The inconsistency of the publishing schedule (sometimes biweekly, sometimes monthly) reflects the time pressure — it's always the lowest-priority task.

**How AI helps:**
Takes in the sources James already follows and his relevance criteria; produces a weekly digest of the 5-7 items most relevant to practical AI adoption, each with a one-paragraph summary. James removes what doesn't belong, adds his commentary, and publishes.

**Value lever:** Streamline — the curation still happens, with the scanning done and the shortlist waiting, so the edition takes 30 minutes instead of two hours.

**Size:** 1-2 hours per edition.

**What changes for the business:**
The newsletter goes out on a steady schedule instead of when time allows, and James's effort goes into commentary rather than scanning.

**Systems involved today:** news feeds, social accounts, research preprint listings, the newsletter platform.


#### Student Support

---

**#6 Student Q&A Research**

**Why it's a good candidate:**
Student questions vary, so for each one the AI works out which of the allowed sources to check — the playbook, the official documentation, or the open web — and whether a quick example is needed. The answer also needs to be pedagogically appropriate (right level of detail, connected to course concepts), so James reviews the draft before posting.

**Current pain point:**
Students ask questions via Slack, email, and in class that go beyond the prepared material — "How does this work in Gemini?", "What's the difference between X and Y?", "Can you show an example of Z?" James spends 15-30 minutes per question researching current docs, testing examples, and crafting a thoughtful answer. With 10-15 questions per week across cohorts, this is 3-5 hours of reactive work.

**How AI helps:**
Takes in a student's question and the course's level; produces a sourced draft answer with a practical example, pitched for that course. James reviews, adjusts the pedagogical framing, and posts it. The answer is also kept for the playbook, so the next student with the same question finds it already written.

**Value lever:** Accelerate — a 15-30 minute research cycle becomes a five-minute review, so questions are answered the same day.

**Size:** 15-30 minutes per question, 10-15 questions a week.

**What changes for the business:**
Students get thorough, sourced answers quickly instead of waiting on James's calendar, 3-5 hours a week of reactive research return to teaching, and every answer becomes reusable content.

**Systems involved today:** the course chat, email, the playbook, the platforms' documentation.


#### Client and Partner Meetings

---

**#7 Meeting Prep Briefs**

**Why it's a good candidate:**
The goal is clear — a brief that tells James who he's meeting and why it matters — and each meeting is different: what to search for each attendee depends on what turns up (a thin public profile sends the research to company press or past talks). The brief is read as-is before the meeting.

**Current pain point:**
James has 5-8 external meetings per week — prospective clients, conference organizers, partnership discussions, guest lecturers. Before each meeting, he spends 15-20 minutes researching the person and company on LinkedIn, their website, and recent news. Some meetings get thorough prep; others get none because of time pressure, leading to missed context.

**How AI helps:**
Takes in the meeting title and attendee names two hours before each external meeting; produces a structured brief — who each person is, what their company does, any relevant connection to AI education, and any previous interaction — that James reads on the way in.

**Value lever:** Create value — there is no prep process today, only what time allows; a brief for every meeting is new output, not a faster version of existing work.

**Size:** 15-20 minutes per meeting, 5-8 meetings a week.

**What changes for the business:**
Every external meeting starts with context instead of a cold open, and the 15-20 minutes per meeting that sometimes happened and sometimes didn't is no longer James's to find.

**Systems involved today:** the calendar, professional profiles, company websites, past email.

---

### Workflow Candidate Summary

#### Candidate 1: Post-Class Summary Generation

| Field | Content |
|-------|---------|
| **Workflow** | Post-Class Summary Generation |
| **Process** | Teaching |
| **Description** | Writes the summary email to students after each live session from the transcript and lesson plan |
| **Trigger** | Event — a live session ends |
| **Deliverable** | Summary email with the topics covered, key takeaways, action items, and resources mentioned, sent to students |
| **Value lever** | Automate |
| **Pain point** | 20-30 minutes per session, and the first thing skipped when time is tight, so students miss the reinforcement |
| **AI opportunity** | Write the standard summary from the session transcript and lesson plan and send it within an hour of class ending |
| **Frequency** | Weekly (after each live session) |
| **Size** | 20-30 minutes per session |

#### Candidate 2: Assignment Feedback Drafting

| Field | Content |
|-------|---------|
| **Workflow** | Assignment Feedback Drafting |
| **Process** | Teaching |
| **Description** | Drafts personalized assignment feedback based on rubric criteria and submission content |
| **Trigger** | Event — assignment submission deadline passes |
| **Deliverable** | Draft feedback for each submission, ready for instructor review and delivery |
| **Value lever** | Accelerate |
| **Pain point** | 10-15 minutes per submission, 15-25 per cohort — slow turnaround affects student momentum |
| **AI opportunity** | AI reads submissions against rubric, identifies strengths and gaps, drafts specific constructive feedback with course material references |
| **Frequency** | Weekly (during active cohorts) |
| **Size** | 10-15 minutes per submission, 4-6 hours per round of feedback |

#### Candidate 3: Course Content Updates

| Field | Content |
|-------|---------|
| **Workflow** | Course Content Updates |
| **Process** | Content Creation |
| **Description** | Compares lesson pages against current platform documentation and drafts edits for anything out of date |
| **Trigger** | Event — a major platform release |
| **Deliverable** | Discrepancy list for each lesson page, each item with a suggested edit and the reason |
| **Value lever** | Streamline |
| **Pain point** | A full day to audit 30+ pages, so audits are reactive; outdated content is often found when a student flags it in class |
| **AI opportunity** | Compare each lesson page with the documentation it describes and list every discrepancy with a suggested edit; James decides which edits to make |
| **Frequency** | Ad-hoc (after each major platform release) |
| **Size** | A full day to audit 30+ pages |

#### Candidate 4: Lesson Slide Formatting

| Field | Content |
|-------|---------|
| **Workflow** | Lesson Slide Formatting |
| **Process** | Content Creation |
| **Description** | Turns finished lesson text into a formatted slide deck with the course brand template applied |
| **Trigger** | Event — the lesson text is finished |
| **Deliverable** | Formatted slide deck — title, content, code, and exercise slides |
| **Value lever** | Automate |
| **Pain point** | 30-45 minutes of manual formatting per lesson, adding up to full days per quarter |
| **AI opportunity** | Apply the course's formatting rules to the lesson text and produce the deck, the same way every time |
| **Frequency** | Ad-hoc (12+ lessons per course) |
| **Size** | 30-45 minutes per lesson |

#### Candidate 5: Newsletter Curation

| Field | Content |
|-------|---------|
| **Workflow** | Newsletter Curation |
| **Process** | Content Creation |
| **Description** | Scans the sources James follows and drafts a digest of the AI developments most relevant to practical adoption |
| **Trigger** | Scheduled — weekly |
| **Deliverable** | Digest of 5-7 items, each with a one-paragraph summary, ready for James's commentary |
| **Value lever** | Streamline |
| **Pain point** | 1-2 hours of scanning per edition; the schedule slips because it is always the lowest-priority task |
| **AI opportunity** | Check each source against James's relevance criteria and summarize the top items; James removes items, adds commentary, and publishes |
| **Frequency** | Weekly |
| **Size** | 1-2 hours per edition |

#### Candidate 6: Student Q&A Research

| Field | Content |
|-------|---------|
| **Workflow** | Student Q&A Research |
| **Process** | Student Support |
| **Description** | Researches student questions and drafts sourced, pedagogically appropriate answers |
| **Trigger** | Request — student posts a question in the course chat or by email |
| **Deliverable** | Draft answer with sources and examples, ready for instructor review and posting |
| **Value lever** | Accelerate |
| **Pain point** | 15-30 minutes per question, 10-15 questions/week — reactive research that fragments focused work time |
| **AI opportunity** | AI researches docs, finds examples, and drafts an answer at the right course level; instructor reviews and adjusts before posting |
| **Frequency** | Daily |
| **Size** | 15-30 minutes per question, 10-15 questions a week |

#### Candidate 7: Meeting Prep Briefs

| Field | Content |
|-------|---------|
| **Workflow** | Meeting Prep Briefs |
| **Process** | Client and Partner Meetings |
| **Description** | Researches attendees and produces a structured prep brief before each external meeting |
| **Trigger** | Scheduled — 2 hours before each external calendar event |
| **Deliverable** | Structured meeting brief, delivered where James reads before meetings |
| **Value lever** | Create value |
| **Pain point** | 15-20 minutes per meeting, 5-8 meetings/week — inconsistent prep quality due to time pressure |
| **AI opportunity** | AI researches attendees, identifies relevant context, and delivers a ready-to-read brief before the meeting |
| **Frequency** | Daily |
| **Size** | 15-20 minutes per meeting, 5-8 meetings a week |

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

The Individual lens hasn't been run yet.

### Summary Table

| # | Opportunity | Process | Value lever | Size |
|---|------------|---------|-------------|------|
| 1 | Demand Forecasting | Warehouse Operations | Create value | Not sized yet |
| 2 | Fleet Maintenance Scheduling | Fleet Management | Automate | Unplanned breakdowns cost 3-5x a scheduled service |
| 3 | Order Fulfillment Tracking | Customer Fulfillment | Automate | 3-4 hours a day of reactive status checks |
| 4 | Customer Onboarding | Customer Onboarding | Accelerate | 2-3 weeks per new customer, 3-5 new customers a month |
| 5 | Carrier Rate Negotiation Prep | Carrier Management | Accelerate | 2-3 days of prep each quarter |

### Detailed Opportunity Cards

#### Warehouse Operations

---

**#1 Demand Forecasting**

**Why it's a good candidate:**
The forecast follows the same steps every month: analyze shipment history, find seasonal patterns and growth trends per customer, add known upcoming events, produce a 90-day forecast. Maria adds market intuition and customer-specific knowledge before approving the capacity plan.

**Current pain point:**
Monthly capacity planning relies on the VP's experience and a basic spreadsheet model. Seasonal demand shifts, new customer ramp-ups, and one-time events aren't systematically factored in. Over-forecasting wastes warehouse labor; under-forecasting creates overtime costs and missed SLAs.

**How AI helps:**
Takes in 24 months of shipment history by customer and the known upcoming events (new customer launches, holiday peaks); produces a 90-day demand forecast with confidence ranges and the seasonal patterns behind it. Maria adjusts for what the history cannot show — a large customer hinting at a contract change — and approves the capacity plan.

**Value lever:** Create value — a customer-by-customer statistical forecast with confidence ranges does not exist today; the spreadsheet is a staffing guess, not a forecast to compare against.

**Size:** Not sized yet — you can add today's number when the requirements are written.

**What changes for the business:**
Warehouse staffing is planned against a stated forecast rather than a feel for the month, over- and under-staffing both shrink, and the forecast's accuracy can be measured and improved quarter by quarter.

**Systems involved today:** the shipment history in the warehouse system, the planning spreadsheet.

**Business Objective:** Optimize warehouse labor costs while maintaining SLA compliance
**Stakeholders:** VP Operations (approval), Warehouse Manager (staffing), Finance (labor budget)
**Success Metrics:** Forecast accuracy (MAPE), labor cost variance, SLA compliance rate


#### Fleet Management

---

**#2 Fleet Maintenance Scheduling**

**Why it's a good candidate:**
You set the structure and the rules: service intervals, delivery commitments, and how to weigh uptime against maintenance. For each vehicle the AI uses those rules to decide whether to book service now or defer it, and which low-utilization window to use. The constraints are clear enough to book directly from the rules.

**Current pain point:**
Fleet maintenance is tracked in a spreadsheet. The fleet manager checks mileage and schedules services based on manufacturer intervals, but competing delivery commitments mean vehicles often run past due. Unplanned breakdowns cost 3-5x more than scheduled maintenance and disrupt delivery schedules.

**How AI helps:**
Takes in each vehicle's mileage, engine hours, and fault codes alongside the service intervals and the upcoming delivery commitments; produces a maintenance booking in the lowest-utilization window for each vehicle that needs one, the work order for the shop, and the delivery-schedule adjustment around the downtime.

**Value lever:** Automate — the fleet manager stops reconciling the spreadsheet against the delivery board; vehicles are booked before they run past due.

**Size:** Unplanned breakdowns cost 3-5x a scheduled service.

**What changes for the business:**
Unplanned breakdowns, which cost 3-5x a scheduled service, become rare, deliveries are planned around downtime instead of disrupted by it, and the fleet manager's week is spent on exceptions rather than scheduling.

**Systems involved today:** the fleet maintenance spreadsheet, vehicle telematics, the dispatch schedule.

**Business Objective:** Reduce unplanned vehicle downtime by 50%
**Stakeholders:** Fleet Manager (scheduling), Maintenance Shop (execution), Dispatch (route adjustment)
**Success Metrics:** Planned vs. unplanned maintenance ratio, average vehicle uptime %, maintenance cost per mile


#### Customer Fulfillment

---

**#3 Order Fulfillment Tracking**

**Why it's a good candidate:**
Status tracking follows fixed rules: order received → picked → packed → shipped → delivered. Each stage transition is a recorded event in the systems the warehouse and transport teams already run, and every alert fires on a timing threshold you set. Just monitoring, matching, and alerting.

**Current pain point:**
Customer service reps manually check order status across the WMS and TMS when customers call. Exception detection (delayed shipments, partial picks, missed delivery windows) relies on someone noticing — there's no proactive alerting. The team spends 3-4 hours daily on reactive status checks, and customers often know about problems before the ops team does.

**How AI helps:**
Takes in each order's stage events as they are recorded and the timing thresholds the ops team sets; produces a live status view of every open order and an alert the moment an order misses a threshold (a pick not started within two hours of receipt, a shipment not scanned inside its delivery window). Fixed rules, fixed thresholds, fixed notifications.

**Value lever:** Automate — reps stop checking status by hand; exceptions find the team instead of the other way round.

**Size:** 3-4 hours a day of reactive status checks.

**What changes for the business:**
The ops team knows about a late order before the customer does, customer service answers from a live view instead of two system lookups, and 3-4 hours a day of reactive checking return to resolving exceptions.

**Systems involved today:** the warehouse management system, the transport management system, the customer service phone queue.

**Business Objective:** Achieve 98% on-time delivery rate (currently 94%)
**Stakeholders:** Warehouse Manager (pick/pack), Logistics Coordinator (shipping), Customer Service (communication)
**Success Metrics:** Exception detection time, proactive alert rate, customer inquiry volume reduction


#### Customer Onboarding

---

**#4 Customer Onboarding**

**Why it's a good candidate:**
Onboarding follows a structured sequence (account setup, system configuration, initial shipment planning, training), and at several points the AI makes bounded decisions by your method: which warehouse to assign based on the customer's shipping patterns, which carrier mix to propose, which training schedule fits. The account manager reviews and approves the key decisions along the way.

**Current pain point:**
New customer onboarding takes 2-3 weeks and involves sales, operations, and account management. Each team owns different steps, and handoffs are where things break — incomplete information passes between teams, setup tasks get missed, and the customer's first shipment experience sets the tone for the relationship. There's no single owner for the end-to-end outcome.

**How AI helps:**
Takes in the signed contract and the customer's expected shipping patterns; produces the account setup draft, a recommended warehouse assignment and carrier mix, a proposed training schedule, and a running view of which team has completed which step. The account manager approves the key decisions along the way.

**Value lever:** Accelerate — the gain is cycle time: time-to-first-shipment drops from weeks to days because the handoffs no longer wait on people reconstructing information.

**Size:** 2-3 weeks per new customer, 3-5 new customers a month.

**What changes for the business:**
A new customer's first shipment goes out in days rather than weeks, nothing falls between teams because one view shows what is done, and the customer's first impression stops depending on which account manager they drew.

**Systems involved today:** the CRM where contracts land, the warehouse and transport systems, the training calendar.

**Business Objective:** Improve customer retention rate from 85% to 92%
**Stakeholders:** Sales (handoff), Operations (setup), Account Management (relationship owner)
**Success Metrics:** Time-to-first-shipment, onboarding completion rate, 90-day customer satisfaction score


#### Carrier Management

---

**#5 Carrier Rate Negotiation Prep**

**Why it's a good candidate:**
Rate negotiation prep is research-heavy but follows the same steps every quarter: pull shipment volumes by lane, pull carrier on-time performance, benchmark against published rate indices, write the negotiation brief. The negotiation strategy needs human judgment, so the logistics manager reviews the brief before using it.

**Current pain point:**
Quarterly carrier negotiations require 2-3 days of prep. The logistics manager pulls shipment data from the TMS, calculates lane-by-lane volumes, reviews carrier scorecards, researches competitor rate benchmarks, and assembles a briefing document. By the time the brief is ready, some of the market data is already stale.

**How AI helps:**
Takes in the quarter's shipment volumes by lane, each carrier's on-time performance, and published rate benchmarks; produces a negotiation brief that names the lanes priced above market, recommends a target rate for each, and shows the evidence. The logistics manager adjusts for relationship factors and walks in prepared.

**Value lever:** Accelerate — 2-3 days of prep becomes an afternoon of review, so the brief is built on this week's market data rather than last month's.

**Size:** 2-3 days of prep each quarter.

**What changes for the business:**
Negotiations start from current numbers, every lane gets analyzed instead of only the largest, and the logistics manager's time goes to strategy and relationships rather than spreadsheets.

**Systems involved today:** the transport management system, carrier scorecards, published rate indices.

**Business Objective:** Reduce transportation costs by 8% through better carrier rate management
**Stakeholders:** Logistics Manager (prep + negotiation), VP Operations (approval), Finance (budget impact)
**Success Metrics:** Average rate reduction per lane, negotiation prep time, rate variance vs. market benchmark

---

### Workflow Candidate Summary

#### Candidate 1: Demand Forecasting

| Field | Content |
|-------|---------|
| **Workflow** | Demand Forecasting |
| **Process** | Warehouse Operations |
| **Description** | Produces a 90-day demand forecast by customer from shipment history and known upcoming events |
| **Trigger** | Scheduled — monthly capacity planning |
| **Deliverable** | 90-day demand forecast with confidence ranges and the seasonal patterns behind it, for Maria's approval |
| **Value lever** | Create value |
| **Pain point** | Capacity planning relies on experience and a basic spreadsheet; over-forecasting wastes warehouse labor and under-forecasting creates overtime and missed SLAs |
| **AI opportunity** | Find seasonal patterns and growth trends per customer in 24 months of history, add known events, and forecast 90 days ahead; Maria adjusts and approves the capacity plan |
| **Frequency** | Monthly |
| **Size** | Not sized yet |
| **Lens** | Organizational |
| **Business Objective** | Optimize warehouse labor costs while maintaining SLA compliance |
| **Stakeholders** | VP Operations, Warehouse Manager, Finance |
| **Success Metrics** | Forecast accuracy (MAPE), labor cost variance, SLA compliance rate |

#### Candidate 2: Fleet Maintenance Scheduling

| Field | Content |
|-------|---------|
| **Workflow** | Fleet Maintenance Scheduling |
| **Process** | Fleet Management |
| **Description** | Books maintenance for each vehicle that needs it in its lowest-utilization window, around delivery commitments |
| **Trigger** | Event — a vehicle's mileage, engine hours, or fault codes show it needs service |
| **Deliverable** | Maintenance booking, the work order for the shop, and the delivery-schedule adjustment around the downtime |
| **Value lever** | Automate |
| **Pain point** | Maintenance is tracked by hand and competing delivery commitments push vehicles past due; unplanned breakdowns cost 3-5x more than scheduled maintenance |
| **AI opportunity** | Weigh each vehicle's service needs against delivery commitments by the set rules and book service in the lowest-utilization window |
| **Frequency** | Ad-hoc (as each vehicle comes due) |
| **Size** | Unplanned breakdowns cost 3-5x a scheduled service |
| **Lens** | Organizational |
| **Business Objective** | Reduce unplanned vehicle downtime by 50% |
| **Stakeholders** | Fleet Manager, Maintenance Shop, Dispatch |
| **Success Metrics** | Planned vs. unplanned maintenance ratio, average vehicle uptime %, maintenance cost per mile |

#### Candidate 3: Order Fulfillment Tracking

| Field | Content |
|-------|---------|
| **Workflow** | Order Fulfillment Tracking |
| **Process** | Customer Fulfillment |
| **Description** | Monitors order lifecycle from receipt through delivery and proactively alerts on exceptions |
| **Trigger** | Event — new order created in the warehouse system |
| **Deliverable** | Real-time order status view + exception alerts |
| **Value lever** | Automate |
| **Pain point** | 3-4 hours daily of reactive status checks; customers learn about problems before the ops team |
| **AI opportunity** | Watch each order's stage events against set thresholds and alert the moment one is missed |
| **Frequency** | Continuous (hundreds of orders daily) |
| **Size** | 3-4 hours a day of reactive status checks |
| **Lens** | Organizational |
| **Business Objective** | Achieve 98% on-time delivery rate |
| **Stakeholders** | Warehouse, Logistics, Customer Service |
| **Success Metrics** | Exception detection time, proactive alert rate, customer inquiry volume |

#### Candidate 4: Customer Onboarding

| Field | Content |
|-------|---------|
| **Workflow** | Customer Onboarding |
| **Process** | Customer Onboarding |
| **Description** | Orchestrates the end-to-end process of setting up new customers from signed contract through first successful shipment |
| **Trigger** | Event — new customer contract signed in CRM |
| **Deliverable** | Fully configured customer account with completed first shipment and satisfaction survey |
| **Value lever** | Accelerate |
| **Pain point** | 2-3 week onboarding with frequent handoff failures between sales, ops, and account management — leading to poor first impressions and early churn |
| **AI opportunity** | Draft the account setup, recommend warehouse and carrier assignments, carry the handoffs between teams, and flag delays |
| **Frequency** | Weekly (3-5 new customers per month) |
| **Size** | 2-3 weeks per new customer, 3-5 new customers a month |
| **Lens** | Organizational |
| **Business Objective** | Improve customer retention rate from 85% to 92% |
| **Stakeholders** | Sales, Operations, Account Management |
| **Success Metrics** | Time-to-first-shipment, onboarding completion rate, 90-day CSAT |

#### Candidate 5: Carrier Rate Negotiation Prep

| Field | Content |
|-------|---------|
| **Workflow** | Carrier Rate Negotiation Prep |
| **Process** | Carrier Management |
| **Description** | Synthesizes shipment data, carrier performance, and market rates into a negotiation-ready brief |
| **Trigger** | Scheduled — 3 weeks before quarterly carrier review |
| **Deliverable** | Negotiation brief with lane-by-lane analysis, rate benchmarks, and recommended targets |
| **Value lever** | Accelerate |
| **Pain point** | 2-3 days of manual data gathering and analysis per quarter; market data goes stale during prep |
| **AI opportunity** | Analyze shipment and carrier history against market benchmarks and produce a draft brief — logistics manager refines strategy and enters negotiations prepared |
| **Frequency** | Quarterly |
| **Size** | 2-3 days of prep each quarter |
| **Lens** | Organizational |
| **Business Objective** | Reduce transportation costs by 8% |
| **Stakeholders** | Logistics Manager, VP Operations, Finance |
| **Success Metrics** | Average rate reduction, prep time, rate vs. market benchmark |

---

## Appendix: Value Lever Definitions

**Value lever — what kind of value does AI create here?** One per opportunity, the dominant one.

- **Streamline** — the work still happens the same way, with fewer steps, handoffs, or reformatting. Test: would the person still do it, just faster and cleaner?
- **Automate** — work a person does today runs without them. Test: does a person stop doing something they do now?
- **Accelerate** — the outcome arrives sooner, or more of it arrives in the same time. Test: is the gain measured in cycle time or throughput rather than effort?
- **Create value** — something becomes possible that was not done at all before. Test: is there no "today" version of this work to compare against?
