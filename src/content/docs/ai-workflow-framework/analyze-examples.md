---
title: "Analyze Examples — Sample AI Opportunity Reports"
description: Three complete AI Opportunity Report examples showing what the Analyze step produces — a Marketing Operations Manager, an AI Instructor, and a VP of Operations.
---

These are three synthetic AI Opportunity Reports showing what the Analyze step produces. Use them as a reference for format, level of detail, and how opportunities are classified on the [AI Workflow Design Matrix](../workflow-design-matrix/).

- **Example 1** — Marketing Operations Manager at a B2B SaaS company (Individual lens, 7 opportunities)
- **Example 2** — AI Instructor running courses and maintaining a knowledge base (Individual lens, 7 opportunities)
- **Example 3** — VP of Operations at a logistics company (Organizational lens, 5 opportunities)

Examples 1 and 2 use the **individual lens** — analyzing one person's workflows. Example 3 uses the **organizational lens** — analyzing value chain processes tied to business objectives. Autonomy is classified by what decides the next step (see the [classification definitions](#appendix-classification-definitions)): an opportunity where the AI drafts or analyzes inside steps you set is Deterministic, one where the AI's judgment by your rubric or criteria decides what happens next is Guided, and a person taking part along the way makes it Augmented. All three include every section the Analyze step produces: report header, summary table, top 3 recommendations, detailed opportunity cards grouped by autonomy level, workflow candidate summary, and classification definitions. Organizational-lens cards include three additional fields: Business Objective, Stakeholders, and Success Metrics.

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

| # | Opportunity | Autonomy | Involvement | Value lever | Impact |
|---|------------|----------|-------------|-------------|--------|
| 1 | Campaign Performance Reporting | Deterministic | Automated | Automate | High |
| 2 | Lead Data Enrichment | Deterministic | Automated | Automate | High |
| 3 | Content Brief Generation | Deterministic | Augmented | Accelerate | High |
| 4 | Lead Scoring Model Tuning | Deterministic | Augmented | Create value | Medium |
| 5 | Email Sequence Optimization | Deterministic | Augmented | Accelerate | Medium |
| 6 | Campaign Budget Reallocation | Guided | Augmented | Accelerate | Low |
| 7 | Competitive Content Monitoring | Autonomous | Automated | Create value | Medium |

### Top Recommendations

1. **Campaign Performance Reporting** — Eliminates 4+ hours of weekly manual data pulling and formatting across three platforms, with the same steps every week.
2. **Lead Data Enrichment** — Standardizes and enriches messy CRM records at scale, directly improving lead routing accuracy and sales handoff quality.
3. **Content Brief Generation** — Cuts content brief creation from 90 minutes to 15 minutes per brief, freeing the team to focus on creative strategy instead of research compilation.

### Detailed Opportunity Cards

#### Deterministic

---

**#1 Campaign Performance Reporting**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
You give the AI instructions for every step: gather last week's metrics from the same three sources, calculate the changes, fill the fixed template, send the summary. Nothing the AI produces changes what happens next, and the output format never varies. Classic automation candidate.

**Current pain point:**
Every Monday morning, Sarah spends 3-4 hours pulling data from three ad platforms, copying numbers into a Google Sheet, calculating WoW changes, formatting a slide deck, and emailing it to the VP of Marketing. The process is tedious and error-prone — last month a copy-paste error overstated LinkedIn ROAS by 40%, which wasn't caught until the executive review.

**How AI helps:**
Takes in last week's campaign metrics from the three sources Sarah uses today and the standing slide template; produces the completed weekly deck with period-over-period changes and a short written summary, ready to send. Same path every week.

**Value lever:** Automate — Sarah stops doing the Monday pull entirely; the deck exists before she sits down.

**What changes for the business:**
The VP of Marketing gets the report first thing Monday instead of mid-morning, the numbers are calculated the same way every week, and the 3-4 hours return to campaign work. The copy-paste error class disappears.

**Systems involved today:** the three ad platforms, the Google Sheet, the slide deck, email.


---

**#2 Lead Data Enrichment**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Enrichment follows clear rules: look up the company, match it to a firmographic record, fill in the missing fields (industry, employee count, revenue range). No ambiguity in what "correct" looks like — either the data matches or it doesn't. The one branch, flagging low-confidence matches for manual review, uses a confidence score the data source supplies, not an AI judgment, so the work follows the same path whatever the AI produces.

**Current pain point:**
New leads arrive from webinars and content downloads with incomplete data — often just name and email. Sarah's team manually researches each company on LinkedIn and Crunchbase to fill in firmographic fields before leads can be scored and routed. This takes 10-15 minutes per lead, and with 50+ new leads per week, it's a significant time drain that delays sales follow-up.

**How AI helps:**
Takes in each new lead as it arrives, with whatever fields it came with; produces the same lead with industry, employee count, and revenue range filled in from an agreed firmographic source, plus a short list of leads whose match was too uncertain to trust, set aside for a person.

**Value lever:** Automate — the team stops researching companies by hand; the record is complete before anyone looks at it.

**What changes for the business:**
Sales follow-up starts the same day a lead arrives instead of days later, scoring and routing run on complete records, and the team recovers roughly 10 hours a week of lookup work.

**Systems involved today:** the CRM, the webinar and content-download forms, LinkedIn and Crunchbase for lookups.


---

**#3 Content Brief Generation**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
Content briefs follow a consistent structure (target audience, keywords, competitor angles, outline) and a set research sequence: keyword research, top-ranking competitor articles, customer quotes from recent calls, then the brief. The AI's judgment about messaging angle shapes what the brief says, but every brief goes through the same steps, so it's Deterministic. Sarah reviews, adjusts the angle, and approves the draft along the way — that's what makes it Augmented.

**Current pain point:**
The content team produces 8-10 blog posts per month. Each brief takes Sarah or her content strategist ~90 minutes: researching keywords in Ahrefs, reviewing top-ranking competitor articles, pulling relevant customer quotes from Gong, and structuring the brief. The research portion is 70% of the time, and the quality varies depending on who writes the brief.

**How AI helps:**
Takes in a topic and target keyword; produces a structured brief in the team's standard shape — search intent, the gaps in top-ranking articles, relevant customer quotes, and an outline. Sarah reviews it, adjusts the angle or emphasis, and approves — turning a 90-minute task into a 15-minute review.

**Value lever:** Accelerate — a brief that took 90 minutes is ready for review in minutes, so the calendar stops waiting on research.

**What changes for the business:**
Eight to ten briefs a month reach writers earlier and in the same shape every time, the strategist's time moves from compiling research to choosing the angle, and brief quality stops depending on who wrote it.

**Systems involved today:** the keyword research tool, competitor blogs, call recordings.


---

**#4 Lead Scoring Model Tuning**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
The analysis follows the same steps every time: take the closed deals, test which attributes correlate with conversion, propose new weights. The AI's analysis shapes what it recommends, but never what happens next, so it's Deterministic. The business logic of what makes a "sales-ready" lead needs domain expertise and sales team input, so Sarah reviews the proposal with the sales team before anything changes (Augmented).

**Current pain point:**
The current lead scoring model in HubSpot was set up 18 months ago and hasn't been recalibrated. Sarah suspects the weights are off — the sales team complains that "hot" leads often aren't ready to buy, while some "warm" leads convert quickly. Recalibrating requires exporting data, running correlation analysis, and proposing new weights, which keeps getting deprioritized.

**How AI helps:**
Takes in the last 12 months of lead-to-close history with each lead's attributes and score at handoff; produces a short analysis of which attributes (job title, company size, content engagement, page visits) actually predicted conversion, and a proposed set of scoring weights with the evidence behind each. Sarah reviews the proposal with the sales team and decides what changes.

**Value lever:** Create value — there is no today version of this analysis: no recalibration has been done in 18 months, so there is nothing to compare against.

**What changes for the business:**
"Hot" leads start meaning what sales expects them to mean, the handoff conversation between marketing and sales moves from complaints to evidence, and the model gets reviewed on a schedule instead of never.

**Systems involved today:** the CRM's lead scoring and opportunity history.


---

**#5 Email Sequence Optimization**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
The steps are set: pull the metrics, rank the sequences by open, click, and reply rates, diagnose the weakest emails, draft variants. The ranking is a metric sort, and the AI's diagnosis and copywriting happen inside those steps without changing what happens next, so it's Deterministic. Brand voice, compliance, and which variants to test need a person, so Sarah reviews before anything goes out (Augmented).

**Current pain point:**
Sarah manages 12 active email nurture sequences. Reviewing performance, identifying underperforming emails, and writing A/B test variants is a monthly task that takes a full day. She often defaults to tweaking subject lines because rewriting full emails is too time-consuming, leaving bigger optimization opportunities on the table.

**How AI helps:**
Takes in the month's open, click, and reply rates for all twelve sequences along with the email copy; produces a ranked list of the weakest emails, a likely diagnosis for each (subject line, length, call-to-action placement, send time), and two or three rewritten variants per email for testing. Sarah reviews, picks what to test, and adjusts copy to brand voice.

**Value lever:** Accelerate — a full day of monthly review becomes a two-hour pass, so whole-email rewrites get tested instead of only subject lines.

**What changes for the business:**
Underperforming sequences get fixed in the month they underperform, the team tests bigger changes than it had time for, and nurture performance is reviewed on a steady monthly rhythm.

**Systems involved today:** the email automation platform's sequence reports.


---

#### Guided

---

**#6 Campaign Budget Reallocation**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
You set the structure and the method: the metrics and thresholds that define "off target", and how to model a reallocation. The AI uses your method to judge when a channel warrants a recommendation and which scenarios to model — its judgment, made by your rules, decides what happens next, so it's Guided. It isn't planning the work from an open-ended goal, so it isn't Autonomous. Budget moves have direct financial impact, so Sarah approves every recommendation before any money moves (Augmented).

**Current pain point:**
Campaign budgets are set quarterly and adjusted monthly based on performance. Sarah spends half a day each month analyzing cost-per-lead and ROAS across channels, modeling "what if" scenarios in a spreadsheet, and proposing reallocations to the VP. The analysis is always backward-looking, and by the time changes are implemented, market conditions have shifted.

**How AI helps:**
Takes in current campaign performance against the targets and thresholds Sarah sets; produces, whenever a channel runs significantly over or under target, a recommended budget shift with the supporting numbers and the projected effect. Sarah approves or adjusts before any money moves.

**Value lever:** Accelerate — the gain is measured in days between a channel drifting and the budget moving, down from a month.

**What changes for the business:**
Budget moves within days of a channel drifting instead of at month end, every move comes with a stated rationale and projection, and the VP sees proposals continuously rather than in one monthly batch.

**Systems involved today:** the ad platforms' performance reports, the planning spreadsheet.


---

#### Autonomous

---

**#7 Competitive Content Monitoring**

**Autonomy:** Autonomous
**Involvement:** Automated

**Why it's a good candidate:**
You can describe the goal — catch competitor positioning changes before sales hears about them on a call — but not the steps. When the AI spots something new, it decides what to do next at each turn (check the pricing page, the docs, job postings, press coverage) and keeps going until it can explain the change. That open-ended decision-making is what makes it Autonomous. The inputs are public and the output is a digest, so no one takes part until it's done.

**Current pain point:**
Sarah tries to keep tabs on 5 key competitors' content and messaging, but it's inconsistent — she checks their blogs when she remembers, usually before quarterly planning. The team often learns about competitor positioning changes reactively (from sales call objections) rather than proactively.

**How AI helps:**
Takes in the five competitors' public presence — their blogs, release notes, and social accounts — each week; produces a digest of the 3-5 most notable changes with what each means for Sarah's content strategy. Where it finds a change it cannot yet explain, it keeps investigating until it can.

A note on how the level climbs: a first version that checks the same sources and summarizes anything new is Deterministic (fixed sources, fixed steps). It becomes Guided if the AI picks the 3-5 most notable changes by criteria you write, and Autonomous when you let it decide where to dig after it spots a change.

**Value lever:** Create value — there is no monitoring process today, only occasional glances before planning; a weekly digest is new work, not faster work.

**What changes for the business:**
Sales hears about competitor positioning shifts from marketing before hearing them as objections on calls, and quarterly planning starts from a record of what changed rather than from memory.


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
| **Value lever** | Automate |
| **Pain point** | 3-4 hours of manual data pulling and formatting every Monday, with copy-paste errors that erode trust in the numbers |
| **AI opportunity** | Gather the week's metrics from the three sources, calculate WoW changes, fill the slide template, and send the summary — no human steps during execution |
| **Frequency** | Weekly |
| **Priority** | High |
| **Reasoning** | Highest time savings (4 hrs/week), zero ambiguity in logic, and directly addresses a reliability issue that affects executive trust |

#### Candidate 2: Lead Data Enrichment

| Field | Content |
|-------|---------|
| **Workflow** | Lead Data Enrichment |
| **Description** | Completes each new inbound lead's firmographic fields from an agreed data source |
| **Trigger** | Event — new lead created in the CRM |
| **Deliverable** | Enriched lead record with firmographic fields populated in the CRM |
| **Autonomy** | Deterministic |
| **Involvement** | Automated |
| **Value lever** | Automate |
| **Pain point** | 10-15 minutes of manual research per lead, 50+ leads/week, delays sales follow-up |
| **AI opportunity** | Identify the company from the lead, fill the standard firmographic fields, and set aside low-confidence matches for a person |
| **Frequency** | Daily (triggered per lead) |
| **Priority** | High |
| **Reasoning** | High volume, direct impact on sales velocity, and the rules are unambiguous |

#### Candidate 3: Content Brief Generation

| Field | Content |
|-------|---------|
| **Workflow** | Content Brief Generation |
| **Description** | Researches and drafts structured content briefs for the blog editorial calendar |
| **Trigger** | Request — content strategist submits a topic and target keyword |
| **Deliverable** | Structured content brief (audience, keywords, competitor analysis, outline, key points) |
| **Autonomy** | Deterministic |
| **Involvement** | Augmented |
| **Value lever** | Accelerate |
| **Pain point** | 90 minutes per brief, mostly spent on repetitive research; quality varies by author |
| **AI opportunity** | AI handles keyword research, competitor article analysis, and brief drafting; human refines strategic angle and approves |
| **Frequency** | Weekly (8-10 per month) |
| **Priority** | High |
| **Reasoning** | Large time savings per brief (75 min), high frequency, and directly improves content quality consistency |

**Recommendation:** Start with **Campaign Performance Reporting**. It's the simplest to build (deterministic, well-defined inputs/outputs), delivers immediate visible value to leadership, and builds confidence in AI workflows before tackling candidates where the AI decides more of what happens next.

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

| # | Opportunity | Autonomy | Involvement | Value lever | Impact |
|---|------------|----------|-------------|-------------|--------|
| 1 | Assignment Feedback Drafting | Deterministic | Augmented | Accelerate | High |
| 2 | Lesson Slide Formatting | Deterministic | Automated | Automate | Medium |
| 3 | Post-Class Summary Generation | Deterministic | Automated | Automate | Medium |
| 4 | Course Content Updates | Deterministic | Augmented | Streamline | Medium |
| 5 | Student Q&A Research | Guided | Augmented | Accelerate | High |
| 6 | Newsletter Curation | Guided | Augmented | Streamline | Low |
| 7 | Meeting Prep Briefs | Autonomous | Automated | Create value | Medium |

### Top Recommendations

1. **Student Q&A Research** — Turns ad-hoc student questions into well-sourced, reusable answers, building the playbook's knowledge base while improving response quality and speed.
2. **Assignment Feedback Drafting** — Scales personalized, actionable feedback across cohorts without sacrificing quality — the highest-leverage activity for student outcomes.
3. **Lesson Slide Formatting** — Eliminates the tedious formatting step between content creation and delivery, freeing time for higher-value lesson design.

### Detailed Opportunity Cards

#### Deterministic

---

**#1 Assignment Feedback Drafting**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
Every submission goes through the same steps: read it against the rubric and assignment prompt, note strengths and gaps, draft feedback with references to course material. The AI uses the rubric to write the feedback, not to decide what happens next — every draft goes to James — so it's Deterministic. James adds the coaching touch and approves each draft before it's sent; that's the Augmented part, not more autonomy.

**Current pain point:**
James reviews 15-25 student assignments per cohort. Each piece of feedback takes 10-15 minutes: reading the submission, checking it against the rubric, identifying strengths and areas for improvement, and writing personalized comments. A full round of feedback takes 4-6 hours, and the turnaround time directly affects student momentum.

**How AI helps:**
Takes in each submission, the rubric, and the assignment prompt; produces a draft of specific, constructive feedback — what was done well, where the gaps or misunderstandings are, and which course material to revisit. James reviews each draft, adds personal observations, adjusts tone, and approves before sending.

**Value lever:** Accelerate — a round of feedback that took 4-6 hours is reviewed in one, so students hear back in a day instead of a week.

**What changes for the business:**
Students get feedback while the assignment is still fresh, every submission is measured against the same rubric, and James's time goes to the coaching comments only he can write.

**Systems involved today:** the course platform's submissions, the rubric document.



---

**#2 Lesson Slide Formatting**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Slide formatting follows strict rules — heading hierarchy, font sizes, code block styling, brand colors. You give instructions for every step: parse the markdown, map each block to a slide template, apply the formatting rules. The content is already decided, and the work follows the same path every time. It's pure template application.

**Current pain point:**
After writing lesson content in markdown, James spends 30-45 minutes per lesson manually formatting slides — adjusting font sizes, adding code syntax highlighting, ensuring consistent spacing, and applying the course brand template. With 12+ lessons per course and multiple courses, this adds up to full days of formatting work per quarter.

**How AI helps:**
Takes in the finished lesson text and the course's formatting rules; produces the formatted slide deck — title, content, code, and exercise slides — with the brand template applied. Same rules every time.

**Value lever:** Automate — James stops formatting slides; the deck is ready when the lesson text is.

**What changes for the business:**
Full days of quarterly formatting return to lesson design, every deck looks the same, and a last-minute content change no longer means an hour of reformatting.

**Systems involved today:** the lesson files, the slide tool, the brand template.



---

**#3 Post-Class Summary Generation**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Class summaries follow a fixed structure: topics covered, key takeaways, action items, links to resources mentioned. The input (class recording transcript + lesson plan) is well-defined, and the output format doesn't vary. The AI writes the summary, but writing inside a step never makes a workflow Guided — the email goes out the same way whatever it says.

**Current pain point:**
After each live session, James writes a summary email to students recapping what was covered, highlighting key concepts, and listing homework or next steps. This takes 20-30 minutes per session, and it's always the first thing that gets skipped when time is tight — meaning students miss the reinforcement.

**How AI helps:**
Takes in the session transcript and the lesson plan; produces the standard summary email — topics actually covered, key takeaways, action items, and the resources mentioned — ready to go out within an hour of class ending.

**Value lever:** Automate — the summary that gets skipped when time is tight now goes out every time without James writing it.

**What changes for the business:**
Every student gets the reinforcement email after every session, not only the sessions with a quiet evening after them, and homework and next steps are stated the same way each week.

**Systems involved today:** the meeting recording and transcript, the lesson plan, email.



---

**#4 Course Content Updates**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
AI platforms release updates frequently, and checking whether course content is still accurate means comparing current docs against existing lesson material — a tedious but critical task. The comparison runs the same way each time: you hand the AI the lesson page and the matching documentation, and it lists discrepancies and drafts edits. Its findings change what the suggestions say, not what happens next, so it's Deterministic. James decides which edits are worth making (Augmented).

**Current pain point:**
Platform updates (new Claude features, changed OpenAI pricing, deprecated Gemini APIs) can make course material outdated overnight. James periodically audits lessons against current documentation, but it's reactive — he often discovers outdated content when a student flags it in class. A full content audit across 30+ pages takes a full day.

**How AI helps:**
Takes in a lesson page and the current official documentation it describes; produces a list of every discrepancy — changed features, stale screenshot references, deprecated terminology, new capabilities worth a mention — each with a suggested edit and the reason. James decides which updates are worth making now and applies them.

**Value lever:** Streamline — the audit still happens, but a day of page-by-page comparison becomes a review of a discrepancy list.

**What changes for the business:**
Outdated content is found by the audit rather than by a student in class, and a full-course audit fits into a morning, so it happens after every major platform release instead of once a quarter.

**Systems involved today:** the course pages, the platforms' official documentation.



---

#### Guided

---

**#5 Student Q&A Research**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Student questions vary, and the AI makes bounded decisions by your method for each one: it chooses which of the sources you allow to check — the playbook, the official documentation, or the open web — and whether a quick example is needed. Choosing the source decides what happens next, so it's Guided. The answer also needs to be pedagogically appropriate (right level of detail, connected to course concepts), so James reviews the draft before posting (Augmented).

**Current pain point:**
Students ask questions via Slack, email, and in class that go beyond the prepared material — "How does this work in Gemini?", "What's the difference between X and Y?", "Can you show an example of Z?" James spends 15-30 minutes per question researching current docs, testing examples, and crafting a thoughtful answer. With 10-15 questions per week across cohorts, this is 3-5 hours of reactive work.

**How AI helps:**
Takes in a student's question and the course's level; produces a sourced draft answer with a practical example, pitched for that course. James reviews, adjusts the pedagogical framing, and posts it. The answer is also kept for the playbook, so the next student with the same question finds it already written.

**Value lever:** Accelerate — a 15-30 minute research cycle becomes a five-minute review, so questions are answered the same day.

**What changes for the business:**
Students get thorough, sourced answers quickly instead of waiting on James's calendar, 3-5 hours a week of reactive research return to teaching, and every answer becomes reusable content.

**Systems involved today:** the course chat, email, the playbook, the platforms' documentation.



---

**#6 Newsletter Curation**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
The sources are configured in advance and the structure is set: check each source, judge each item's relevance to practical AI adoption, summarize the top items. The relevance judgment, made by your criteria, decides which items advance to the digest and which are dropped — the AI's judgment decides what happens next for each item, so it's Guided. James reviews the digest, removes items, and adds commentary before he publishes (Augmented).

**Current pain point:**
James curates a periodic newsletter of AI developments relevant to his students and audience. Scanning RSS feeds, Twitter/X, AI news sites, and research papers takes 1-2 hours per edition. The inconsistency of the publishing schedule (sometimes biweekly, sometimes monthly) reflects the time pressure — it's always the lowest-priority task.

**How AI helps:**
Takes in the sources James already follows and his relevance criteria; produces a weekly digest of the 5-7 items most relevant to practical AI adoption, each with a one-paragraph summary. James removes what doesn't belong, adds his commentary, and publishes.

**Value lever:** Streamline — the curation still happens, with the scanning done and the shortlist waiting, so the edition takes 30 minutes instead of two hours.

**What changes for the business:**
The newsletter goes out on a steady schedule instead of when time allows, and James's effort goes into commentary rather than scanning.

**Systems involved today:** news feeds, social accounts, research preprint listings, the newsletter platform.



---

#### Autonomous

---

**#7 Meeting Prep Briefs**

**Autonomy:** Autonomous
**Involvement:** Automated

**Why it's a good candidate:**
You can describe the goal — a brief that tells James who he's meeting and why it matters — but not the steps. Each meeting is different: the AI decides what to search for each attendee and what to do next at each turn based on what it finds (a thin public profile sends it to company press or past talks), and keeps going until the brief is complete. That open-ended decision-making makes it Autonomous. The brief is read as-is before the meeting, so no one takes part until it's done.

**Current pain point:**
James has 5-8 external meetings per week — prospective clients, conference organizers, partnership discussions, guest lecturers. Before each meeting, he spends 15-20 minutes researching the person and company on LinkedIn, their website, and recent news. Some meetings get thorough prep; others get none because of time pressure, leading to missed context.

**How AI helps:**
Takes in the meeting title and attendee names two hours before each external meeting; produces a structured brief — who each person is, what their company does, any relevant connection to AI education, and any previous interaction — that James reads on the way in.

**Value lever:** Create value — there is no prep process today, only what time allows; a brief for every meeting is new output, not a faster version of existing work.

**What changes for the business:**
Every external meeting starts with context instead of a cold open, and the 15-20 minutes per meeting that sometimes happened and sometimes didn't is no longer James's to find.

**Systems involved today:** the calendar, professional profiles, company websites, past email.



---

### Workflow Candidate Summary

Based on impact, frequency, and feasibility, the following three candidates are recommended for the Deconstruct step:

#### Candidate 1: Student Q&A Research

| Field              | Content                                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **Workflow**       | Student Q&A Research                                                                                                              |
| **Description**    | Researches student questions and drafts sourced, pedagogically appropriate answers                                                |
| **Trigger**        | Request — student posts a question in the course chat or by email                                                                 |
| **Deliverable**    | Draft answer with sources and examples, ready for instructor review and posting                                                   |
| **Autonomy**       | Guided                                                                                                                            |
| **Involvement**    | Augmented                                                                                                                         |
| **Value lever**    | Accelerate                                                                                                                        |
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
| **Autonomy**       | Deterministic                                                                                                                             |
| **Involvement**    | Augmented                                                                                                                                 |
| **Value lever**    | Accelerate                                                                                                                                |
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
| **Deliverable**    | Structured meeting brief, delivered where James reads before meetings                                                                                              |
| **Autonomy**       | Autonomous                                                                                                                                                         |
| **Involvement**    | Automated                                                                                                                                                          |
| **Value lever**    | Create value                                                                                                                                                       |
| **Pain point**     | 15-20 minutes per meeting, 5-8 meetings/week — inconsistent prep quality due to time pressure                                                                      |
| **AI opportunity** | AI independently researches attendees, identifies relevant context, and delivers a ready-to-read brief with no human steps during execution                        |
| **Frequency**      | Daily                                                                                                                                                              |
| **Priority**       | Medium                                                                                                                                                             |
| **Reasoning**      | High frequency and fully automatable — moderate impact per meeting but compounds across 5-8 weekly meetings; also a good proof-of-concept for autonomous workflows |

**Recommendation:** Start with **Student Q&A Research**. It's the highest-frequency opportunity, directly improves the core teaching experience, and produces a tangible artifact (the answer) that compounds in value as it builds the playbook's knowledge base. It's also the workflow whose inputs James already has to hand: the questions arrive daily, and the sources to answer them from are known.

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

| # | Opportunity | Autonomy | Involvement | Value lever | Impact |
|---|------------|----------|-------------|-------------|--------|
| 1 | Order Fulfillment Tracking | Deterministic | Automated | Automate | High |
| 2 | Carrier Rate Negotiation Prep | Deterministic | Augmented | Accelerate | Medium |
| 3 | Demand Forecasting | Deterministic | Augmented | Create value | Medium |
| 4 | Customer Onboarding | Guided | Augmented | Accelerate | High |
| 5 | Fleet Maintenance Scheduling | Guided | Automated | Automate | Medium |

### Top Recommendations

1. **Customer Onboarding** — A cross-functional process spanning sales, ops, and account management that directly impacts customer retention (the #1 business objective). Inconsistent execution leads to early churn.
2. **Order Fulfillment Tracking** — End-to-end visibility from order receipt through delivery confirmation. Currently manual status checks create delays in exception handling.
3. **Carrier Rate Negotiation Prep** — Quarterly process that requires synthesizing shipment volume data, carrier performance metrics, and market rate benchmarks — highly data-intensive research that AI can accelerate.

### Detailed Opportunity Cards

#### Deterministic

---

**#1 Order Fulfillment Tracking**

**Autonomy:** Deterministic
**Involvement:** Automated

**Why it's a good candidate:**
Status tracking follows fixed rules: order received → picked → packed → shipped → delivered. Each stage transition is a recorded event in the systems the warehouse and transport teams already run, and every alert fires on a timing threshold you set — no AI judgment decides what happens next. Just monitoring, matching, and alerting.

**Current pain point:**
Customer service reps manually check order status across the WMS and TMS when customers call. Exception detection (delayed shipments, partial picks, missed delivery windows) relies on someone noticing — there's no proactive alerting. The team spends 3-4 hours daily on reactive status checks, and customers often know about problems before the ops team does.

**How AI helps:**
Takes in each order's stage events as they are recorded and the timing thresholds the ops team sets; produces a live status view of every open order and an alert the moment an order misses a threshold (a pick not started within two hours of receipt, a shipment not scanned inside its delivery window). Fixed rules, fixed thresholds, fixed notifications — the same path every run.

**Value lever:** Automate — reps stop checking status by hand; exceptions find the team instead of the other way round.

**What changes for the business:**
The ops team knows about a late order before the customer does, customer service answers from a live view instead of two system lookups, and 3-4 hours a day of reactive checking return to resolving exceptions.

**Systems involved today:** the warehouse management system, the transport management system, the customer service phone queue.

**Business Objective:** Achieve 98% on-time delivery rate (currently 94%)
**Stakeholders:** Warehouse Manager (pick/pack), Logistics Coordinator (shipping), Customer Service (communication)
**Success Metrics:** Exception detection time, proactive alert rate, customer inquiry volume reduction


---

**#2 Carrier Rate Negotiation Prep**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
Rate negotiation prep is research-heavy but follows the same steps every quarter: pull shipment volumes by lane, pull carrier on-time performance, benchmark against published rate indices, write the negotiation brief. The AI's analysis shapes what the brief recommends, not what happens next, so it's Deterministic. The negotiation strategy needs human judgment, so the logistics manager reviews the brief before using it (Augmented).

**Current pain point:**
Quarterly carrier negotiations require 2-3 days of prep. The logistics manager pulls shipment data from the TMS, calculates lane-by-lane volumes, reviews carrier scorecards, researches competitor rate benchmarks, and assembles a briefing document. By the time the brief is ready, some of the market data is already stale.

**How AI helps:**
Takes in the quarter's shipment volumes by lane, each carrier's on-time performance, and published rate benchmarks; produces a negotiation brief that names the lanes priced above market, recommends a target rate for each, and shows the evidence. The logistics manager adjusts for relationship factors and walks in prepared.

**Value lever:** Accelerate — 2-3 days of prep becomes an afternoon of review, so the brief is built on this week's market data rather than last month's.

**What changes for the business:**
Negotiations start from current numbers, every lane gets analyzed instead of only the largest, and the logistics manager's time goes to strategy and relationships rather than spreadsheets.

**Systems involved today:** the transport management system, carrier scorecards, published rate indices.

**Business Objective:** Reduce transportation costs by 8% through better carrier rate management
**Stakeholders:** Logistics Manager (prep + negotiation), VP Operations (approval), Finance (budget impact)
**Success Metrics:** Average rate reduction per lane, negotiation prep time, rate variance vs. market benchmark


---

**#3 Demand Forecasting**

**Autonomy:** Deterministic
**Involvement:** Augmented

**Why it's a good candidate:**
The forecast follows the same steps every month: analyze shipment history, find seasonal patterns and growth trends per customer, add known upcoming events, produce a 90-day forecast. The AI's modeling changes what the forecast says, not what happens next, so it's Deterministic. Maria adds market intuition and customer-specific knowledge before approving the capacity plan, so a person takes part along the way (Augmented).

**Current pain point:**
Monthly capacity planning relies on the VP's experience and a basic spreadsheet model. Seasonal demand shifts, new customer ramp-ups, and one-time events aren't systematically factored in. Over-forecasting wastes warehouse labor; under-forecasting creates overtime costs and missed SLAs.

**How AI helps:**
Takes in 24 months of shipment history by customer and the known upcoming events (new customer launches, holiday peaks); produces a 90-day demand forecast with confidence ranges and the seasonal patterns behind it. Maria adjusts for what the history cannot show — a large customer hinting at a contract change — and approves the capacity plan.

**Value lever:** Create value — a customer-by-customer statistical forecast with confidence ranges does not exist today; the spreadsheet is a staffing guess, not a forecast to compare against.

**What changes for the business:**
Warehouse staffing is planned against a stated forecast rather than a feel for the month, over- and under-staffing both shrink, and the forecast's accuracy can be measured and improved quarter by quarter.

**Systems involved today:** the shipment history in the warehouse system, the planning spreadsheet.

**Business Objective:** Optimize warehouse labor costs while maintaining SLA compliance
**Stakeholders:** VP Operations (approval), Warehouse Manager (staffing), Finance (labor budget)
**Success Metrics:** Forecast accuracy (MAPE), labor cost variance, SLA compliance rate


---

#### Guided

---

**#4 Customer Onboarding**

**Autonomy:** Guided
**Involvement:** Augmented

**Why it's a good candidate:**
Onboarding follows a structured sequence (account setup, system configuration, initial shipment planning, training), and at several points the AI makes bounded decisions by your method: which warehouse to assign based on the customer's shipping patterns, which carrier mix to propose, which training schedule fits. Those selections decide what happens next in the setup, so it's Guided. The account manager reviews and approves the key decisions along the way — that's involvement (Augmented), and it doesn't lower the autonomy level.

**Current pain point:**
New customer onboarding takes 2-3 weeks and involves sales, operations, and account management. Each team owns different steps, and handoffs are where things break — incomplete information passes between teams, setup tasks get missed, and the customer's first shipment experience sets the tone for the relationship. There's no single owner for the end-to-end outcome.

**How AI helps:**
Takes in the signed contract and the customer's expected shipping patterns; produces the account setup draft, a recommended warehouse assignment and carrier mix, a proposed training schedule, and a running view of which team has completed which step. The account manager approves the key decisions along the way.

**Value lever:** Accelerate — the gain is cycle time: time-to-first-shipment drops from weeks to days because the handoffs no longer wait on people reconstructing information.

**What changes for the business:**
A new customer's first shipment goes out in days rather than weeks, nothing falls between teams because one view shows what is done, and the customer's first impression stops depending on which account manager they drew.

**Systems involved today:** the CRM where contracts land, the warehouse and transport systems, the training calendar.

**Business Objective:** Improve customer retention rate from 85% to 92%
**Stakeholders:** Sales (handoff), Operations (setup), Account Management (relationship owner)
**Success Metrics:** Time-to-first-shipment, onboarding completion rate, 90-day customer satisfaction score


---

**#5 Fleet Maintenance Scheduling**

**Autonomy:** Guided
**Involvement:** Automated

**Why it's a good candidate:**
You set the structure and the rules: service intervals, delivery commitments, and how to weigh uptime against maintenance. For each vehicle the AI uses those rules to decide whether to book service now or defer it, and which low-utilization window to use. That judgment decides what happens next — a work order or not, a delivery-schedule change or not — so it's Guided. It isn't planning open-endedly toward a goal, so it isn't Autonomous. The constraints are clear enough for no one to take part until it's done (Automated).

**Current pain point:**
Fleet maintenance is tracked in a spreadsheet. The fleet manager checks mileage and schedules services based on manufacturer intervals, but competing delivery commitments mean vehicles often run past due. Unplanned breakdowns cost 3-5x more than scheduled maintenance and disrupt delivery schedules.

**How AI helps:**
Takes in each vehicle's mileage, engine hours, and fault codes alongside the service intervals and the upcoming delivery commitments; produces a maintenance booking in the lowest-utilization window for each vehicle that needs one, the work order for the shop, and the delivery-schedule adjustment around the downtime.

**Value lever:** Automate — the fleet manager stops reconciling the spreadsheet against the delivery board; vehicles are booked before they run past due.

**What changes for the business:**
Unplanned breakdowns, which cost 3-5x a scheduled service, become rare, deliveries are planned around downtime instead of disrupted by it, and the fleet manager's week is spent on exceptions rather than scheduling.

**Systems involved today:** the fleet maintenance spreadsheet, vehicle telematics, the dispatch schedule.

**Business Objective:** Reduce unplanned vehicle downtime by 50%
**Stakeholders:** Fleet Manager (scheduling), Maintenance Shop (execution), Dispatch (route adjustment)
**Success Metrics:** Planned vs. unplanned maintenance ratio, average vehicle uptime %, maintenance cost per mile


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
| **Value lever** | Accelerate |
| **Pain point** | 2-3 week onboarding with frequent handoff failures between sales, ops, and account management — leading to poor first impressions and early churn |
| **AI opportunity** | Draft the account setup, recommend warehouse and carrier assignments, carry the handoffs between teams, and flag delays |
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
| **Trigger** | Event — new order created in the warehouse system |
| **Deliverable** | Real-time order status view + automated exception alerts |
| **Autonomy** | Deterministic |
| **Involvement** | Automated |
| **Value lever** | Automate |
| **Pain point** | 3-4 hours daily of reactive status checks; customers learn about problems before the ops team |
| **AI opportunity** | Watch each order's stage events against set thresholds and alert the moment one is missed — no human involvement during execution |
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
| **Autonomy** | Deterministic |
| **Involvement** | Augmented |
| **Value lever** | Accelerate |
| **Pain point** | 2-3 days of manual data gathering and analysis per quarter; market data goes stale during prep |
| **AI opportunity** | Analyze shipment and carrier history against market benchmarks and produce a draft brief — logistics manager refines strategy and enters negotiations prepared |
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

**Autonomy — How much does the AI decide on its own? Look at what decides the next step.**

- **Deterministic** — you give instructions. You set every step, and the AI carries each one out. It may write or summarize inside a step, but its output never changes what happens next. Test: does the work follow the same path whatever the AI produces? Examples: formatting reports, drafting a status report from fixed sources, drafting feedback against a rubric for a person to review.
- **Guided** — you give bounded decisions, with your method. You set the structure and the methodology (a rubric, criteria, a process); the AI uses it to make decisions on your behalf: route an item, choose a tool, judge quality and send work back. Its decisions are bounded (within your structure, by your rules), not open-ended. Test: does the AI's judgment, made by your rules, decide what happens next? Examples: routing support emails by category, scoring items against a rubric and advancing only those that pass, choosing which source to search for each question.
- **Autonomous** — you give a goal. The AI plans its own steps, decides what to do next at each turn, and keeps going until the goal is met. Its decision-making is open-ended. Test: could you only describe the goal, not the steps? Examples: research agents that plan and write an article, a monitoring agent that decides where to dig when something changes.

Writing or summarizing inside a step never makes a workflow Guided, and the number of agents doesn't set the level. A branch on a value the AI didn't judge — an API's score, a timer, a field value — is still an instruction: Deterministic. A person approving the AI's decisions doesn't lower the level: if the AI proposes selections by your method and you approve them, it's Guided + Augmented.

**Human Involvement — Does a person take part while it runs?**

- **Augmented**: A person is in the workflow along the way, guiding, engaging, or collaborating with the AI while it runs.
- **Automated**: No one takes part until it's done. Starting a run by hand doesn't make it Augmented.

**Value lever — what kind of value does AI create here?** One per opportunity, the dominant one.

- **Streamline** — the work still happens the same way, with fewer steps, handoffs, or reformatting. Test: would the person still do it, just faster and cleaner?
- **Automate** — work a person does today runs without them. Test: does a person stop doing something they do now?
- **Accelerate** — the outcome arrives sooner, or more of it arrives in the same time. Test: is the gain measured in cycle time or throughput rather than effort?
- **Create value** — something becomes possible that was not done at all before. Test: is there no "today" version of this work to compare against?
