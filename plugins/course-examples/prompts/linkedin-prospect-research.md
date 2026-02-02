# LinkedIn Prospect Research Workflow

A portable workflow prompt that takes a buyer persona and identifies 5 matching LinkedIn prospects with engagement recommendations. Works with any AI tool that has web browsing capability — Claude, ChatGPT, Gemini, or M365 Copilot.

## How to Use

1. Copy the prompt below into any AI conversation (with web browsing enabled)
2. Attach or paste your buyer persona file as context
3. Receive a structured prospect research report with 5 qualified prospects

## The Prompt

```text
# LinkedIn Prospect Research Workflow

## Purpose
Identify and qualify 5 LinkedIn prospects that match a provided buyer persona, then output actionable engagement recommendations.

---

## Instructions

### Step 1: Analyze the Buyer Persona

Read the provided buyer persona markdown file completely. Extract and internalize:

- **Job titles/roles** the ideal prospect holds
- **Industry/vertical** they work in
- **Company size** (employees, revenue if specified)
- **Seniority level** (C-suite, VP, Director, Manager, etc.)
- **Geographic location** preferences
- **Key pain points** they likely experience
- **Trigger events** that indicate buying readiness
- **Any exclusion criteria** (companies/roles to avoid)

If the persona file is missing critical information, note what assumptions you're making based on common patterns for similar buyer profiles.

---

### Step 2: Access LinkedIn

1. Navigate to **linkedin.com**
2. Confirm you are logged into the authenticated account
3. If not logged in, stop and notify the user that authentication is required

---

### Step 3: Search for Matching Prospects

Use LinkedIn's search functionality strategically:

**Search approach:**
1. Start with **People search** using the primary job title(s) from the persona
2. Apply filters that match persona criteria:
   - Current company industry
   - Location/geography
   - Connections (2nd degree often best for warm outreach)
   - Company size if available
3. Review search results systematically

**For each potential prospect, evaluate:**
- Does their current role match the persona's target titles?
- Is their company in the right industry/size range?
- Do they show signals of relevance (posts about relevant topics, recent role changes, company growth)?
- Are there mutual connections or shared groups?

**Select exactly 5 prospects** that best match the persona criteria. Prioritize:
1. Strong title/role match
2. Company fit (industry, size)
3. Engagement signals (active on LinkedIn, posts about relevant topics)
4. Accessibility (2nd-degree connections, shared groups)

---

### Step 4: Document Each Prospect

For each of the 5 selected prospects, capture:

- **Full name**
- **LinkedIn profile URL**
- **Current job title**
- **Company name**
- **Why they match the persona** (2-3 specific reasons)
- **Engagement hook** (something specific from their profile to reference in outreach)

---

### Step 5: Generate Output File

Create a markdown file named `prospect-research-[DATE].md` with the following structure:

# Prospect Research Results

**Date:** [Current Date]
**Buyer Persona:** [Persona Name/Title from input file]
**Prospects Identified:** 5

---

## Prospect 1: [Full Name]

**LinkedIn:** [Profile URL]
**Title:** [Current Job Title]
**Company:** [Company Name]

**Persona Match:**
[2-3 bullet points explaining why this prospect fits the buyer persona]

**Recommended Engagement Approach:**
[Specific, actionable next step based on their profile - e.g., comment on a recent post, reference shared connection, mention specific content they've engaged with]

---

[Continue for all 5 prospects]

---

## Summary

**Selection Rationale:**
[Brief paragraph explaining the overall approach and why these 5 prospects represent strong opportunities]

**Common Themes:**
[Any patterns noticed across prospects that could inform messaging]

**Recommended Priority Order:**
1. [Name] - [One-line reason]
2. [Name] - [One-line reason]
3. [Name] - [One-line reason]
4. [Name] - [One-line reason]
5. [Name] - [One-line reason]

---

## Quality Criteria

Before completing, verify:

- [ ] All 5 prospects clearly match the buyer persona criteria
- [ ] Each LinkedIn URL is complete and accurate
- [ ] Engagement recommendations are specific (not generic)
- [ ] The summary explains selection logic clearly
- [ ] Output file is properly formatted markdown

---

## Error Handling

**If fewer than 5 matching prospects are found:**
- Document however many were found
- Note in the summary what criteria were relaxed or what limitations were encountered
- Suggest alternative search strategies

**If LinkedIn access is restricted:**
- Stop immediately and notify the user
- Do not attempt to bypass any LinkedIn limitations

**If persona file is incomplete:**
- Note missing information
- State assumptions made
- Proceed with best judgment based on available data
```

## What Makes This Deterministic

This workflow is deterministic — it follows a fixed sequence of steps, applies predefined evaluation criteria (from the buyer persona), and produces output in a rigid template. The rules for selecting and evaluating prospects are defined upfront, the output format never changes, and the quality checklist provides a binary pass/fail verification.

This makes it ideal for:

- **Delegation** — Anyone with the buyer persona file can run this workflow and get consistent results
- **Repeatability** — Run it weekly or monthly against the same persona to find fresh prospects
- **Consistency** — Every research report follows the same structure, making it easy to compare across runs
- **Handoff** — The structured output is immediately usable by a sales team without further formatting
