---
title: How to Discover Your Best Claude Skills
description: Use this guided process to identify your highest-value Claude Skill candidates by analyzing your work patterns, scoring candidates on three dimensions, and choosing the right approach — skill, project, or prompt.
---

# How to Discover Your Best Claude Skills

## Why This Matters

Claude Skills make Claude specific to YOUR work — not generic, but tuned to your tasks, your standards, and your formats. The best skills don't come from tasks you invent. They come from tasks you already do — the repetitive, structured work where you follow the same steps every time but the content changes.

This guide walks you through discovering those tasks, analyzing them, and evaluating which ones are worth building into skills. You'll walk away with 3-5 evaluated skill candidates ranked by value, with your #1 pick ready to build.

This page covers **discovery and evaluation only** — helping you identify what to build. A separate lesson covers the actual skill-building process.

## Before You Start

- **Claude Pro subscription** (or higher) — you'll paste a prompt into Claude to run the analysis in Step 2
- **A text editor for your answers** — Word, Google Docs, Apple Notes, Notepad — anything you can type in. You'll build up your answers across all three steps in this document, so keep it open throughout.
- **Some conversation history helps** — Claude can scan your past conversations and memory for patterns you haven't noticed. The more history you have, the richer the analysis. If you're new to Claude, that's fine — the process still works.

---

## Step 1 — Speed Round

The goal of this step is to produce a written list of 10 answers you'll feed to Claude in Step 2. You're not using Claude yet — this is just you, thinking about your own work.

**What to do:**

1. Copy the 10 questions below into your text editor (use the copy button in the top-right corner of the code block)
2. Write your answer directly below each question — keep the question text there so Claude can see which question you're answering in Step 2
3. For each answer, give it a short label (2-5 words) followed by a one-sentence description
4. If a question doesn't apply to you, write "N/A" below it and move on

**The 10 questions — copy this entire block:**

```text
1. What task do you do weekly that follows the same steps every time?

2. What output do you produce repeatedly where the format stays the same but the content changes?

3. What task do you give Claude the same context or instructions for every conversation?

4. What task takes you 15-30 minutes but only 2-3 minutes of actual thinking — the rest is mechanical?

5. What do you copy-paste between documents or apps regularly?

6. What task would you delegate to a smart intern — straightforward judgment, tedious execution?

7. What recurring task involves reading something long and producing something short?

8. What process have you already built your own template, checklist, or SOP for?

9. What task drops in quality when you're tired — where consistency matters more than creativity?

10. What task do you use Claude for conversationally but wish it just "knew how" to do?
```

!!! tip "Your first instinct is usually right"
    Don't try to think of the "best" answer. The point is to surface real work, not impressive-sounding work. If your answer is "formatting invoices" — that's a great candidate.

**Here's what your finished answers should look like.** Notice the question stays — you type your answer on the line below it:

> 1. What task do you do weekly that follows the same steps every time?
> **Weekly status report** — Every Monday I gather updates from Slack, email, and our project board, then write a summary for my manager in the same format.
>
> 2. What output do you produce repeatedly where the format stays the same but the content changes?
> **Client proposal intro sections** — Same structure every time: who we are, what we understand about their problem, proposed approach. Only the client details change.
>
> 3. What task do you give Claude the same context or instructions for every conversation?
> **Meeting notes cleanup** — I paste raw meeting notes and ask Claude to extract action items, decisions, and owners. Same instructions every time.
>
> 4. What task takes you 15-30 minutes but only 2-3 minutes of actual thinking — the rest is mechanical?
> N/A
>
> *(…and so on for all 10 questions)*

Once you have all 10 answered in your text editor, move to Step 2.

---

## Step 2 — Analyze Your Answers

Now you'll hand your answers to Claude and let it do the analysis. Here's exactly what to do:

1. Open a new conversation in Claude
2. Copy the entire prompt below (use the copy button in the top-right corner of the code block)
3. **Before you send it:** scroll to the bottom of the prompt and find the line that says `[PASTE YOUR 10 ANSWERS HERE]` — delete that line and paste in your questions and answers from Step 1 (the whole block — questions included)
4. Send the prompt

```text
You are a Skills Discovery Analyst. Your job is to analyze my work patterns and identify my strongest Claude Skill candidates — tasks that are repeatable, structured, and would benefit from being encoded as a reusable skill rather than re-prompted every time.

I've answered 10 discovery questions below. Use them as your primary input.

ALSO DO THIS (mandatory):
- Scan my conversation history for recurring tasks, repeated instructions, or patterns I might not have mentioned.
- Check my memory for stored preferences, workflows, or context that suggests additional candidates.
- If you find relevant patterns from history or memory, include them in your analysis and note where they came from.

## Your Analysis

Produce the following:

### 1. Candidate Table

A table of 5-8 skill candidates, ranked by Skill Score (highest first):

| # | Candidate Name | What It Does | How Often | Skill Score (1-5) |
|---|---------------|-------------|-----------|-------------------|

Skill Score criteria:
- **5** — Daily/weekly, identical steps every time, highly mechanical, clear input→output
- **4** — Weekly, mostly identical steps, some minor variation, clear format
- **3** — Weekly/biweekly, consistent structure but moderate judgment needed
- **2** — Monthly or variable frequency, some structure but significant judgment
- **1** — Infrequent, loosely structured, mostly creative/judgment work

### 2. Top 3 Deep Dive

For each of your top 3 candidates, explain:
- **Why it scored high** — what makes this a strong skill candidate
- **What the skill would do** — a 2-3 sentence description of the skill's function
- **Input → Output** — what goes in, what comes out

### 3. Patterns from History

Note what you found (if anything) from scanning my conversation history and memory. Be specific — "I noticed you've asked me to format meeting notes 12 times in the last month" is useful. "No additional patterns found" is fine if there aren't any.

---

## My Speed Round Answers

[PASTE YOUR 10 ANSWERS HERE]
```

!!! tip "Attach your documents for richer results"
    If you have SOPs, templates, checklists, or process docs related to your answers, attach them to the conversation before sending the prompt. Claude will use them to produce more specific and accurate candidates.

### What to Expect

Claude will return:

- A **table of 5-8 candidates** sorted by Skill Score (highest first)
- A **detailed breakdown of your top 3** — why they scored high, what the skill would do, and what goes in vs. comes out
- **Notes on patterns** it found in your conversation history (if any)

The whole analysis typically fits in one response. Once you have it, **copy Claude's candidate table into your text editor** — you'll need it for Step 3.

---

## Step 3 — Evaluate Your Candidates

Don't build yet. Score each candidate first so you build the right one.

Copy the scoring table below into your text editor, underneath Claude's analysis from Step 2. Fill in one row for each of your top candidates.

**Scoring dimensions** (score each 1-5):

| Dimension | 1 (Low) | 5 (High) |
|-----------|---------|----------|
| **Repeatability** | Rarely, unpredictable timing | Daily or weekly, like clockwork |
| **Consistency Need** | Quality can vary, no one notices | Must be the same quality every time, regardless of your energy |
| **Mechanical vs. Judgment** | Mostly creative thinking, unique decisions each time | Mostly following steps, filling in templates, applying rules |

**Scoring table** — copy this into your text editor and fill it in:

```text
Candidate               | Repeatability (1-5) | Consistency (1-5) | Mechanical (1-5) | Total (/15)
----------------------- | ------------------- | ----------------- | ----------------- | -----------
                        |                     |                   |                   |
                        |                     |                   |                   |
                        |                     |                   |                   |
                        |                     |                   |                   |
```

**How to read your scores:**

- **12-15** — Strong skill candidate. Build it.
- **9-11** — Decent candidate. Could be a skill, but check the decision framework below to confirm.
- **Below 9** — A Claude Project with custom instructions is probably a better fit than a full skill.

Your top 1-2 candidates are what you'll build in the next lesson.

---

## Skill, Project, or Prompt?

Not everything should be a skill. Here's how to tell which approach fits best.

Walk through these four questions for any candidate you're considering:

1. **Do you do this more than once a month?**
    - NO → Just use a prompt. Write it well, save it somewhere, and reuse it when you need it.
    - YES → Continue to question 2.

2. **Do you follow the same steps each time?**
    - NO → Better as a **Project** with custom instructions. Projects give Claude ongoing context without rigid steps.
    - YES → Continue to question 3.

3. **Does it require specific formatting or standards Claude doesn't know by default?**
    - NO → A saved prompt template may be enough. Try that first.
    - YES → Continue to question 4.

4. **Do you give Claude the same instructions repeatedly for this task?**
    - YES → This is a strong **Skill** candidate. Build it.
    - NO → Revisit whether a Project with good custom instructions would cover it.

### Comparison

| Approach | Best For | Example |
|----------|----------|---------|
| Prompt | One-off or infrequent tasks | "Summarize this PDF" |
| Project | Recurring context without rigid steps | Client research workspace |
| Skill | Repeatable process with consistent format and standards | Weekly status report generation |

---

## Worked Example — Meeting Notes to Action Items

Here's the full journey for one candidate, so you can see what each step produces.

### Step 1 — Speed Round Answer

> **Meeting notes cleanup** — After every meeting, I paste raw notes into Claude and ask it to extract action items with owners, key decisions, and follow-ups. Same format every time, same instructions every time. I do this 4-5 times a week.

### Step 2 — What Claude's Analysis Produced

| # | Candidate Name | What It Does | How Often | Skill Score |
|---|---------------|-------------|-----------|-------------|
| 1 | Meeting Notes → Action Items | Extracts structured action items, decisions, and follow-ups from raw meeting notes | 4-5x/week | 5 |

> **Why it scored high:** Daily frequency, identical instructions every time, clear input (raw notes) and output (formatted action items), almost entirely mechanical — the "thinking" is in the meeting, not in the extraction.
>
> **What the skill would do:** Accept raw meeting notes (pasted text or attached document), extract all action items with assigned owners and due dates, list key decisions made, flag open questions and follow-ups, and output everything in a consistent Markdown format.
>
> **Input → Output:** Raw meeting notes → Formatted document with Action Items table, Decisions list, and Follow-ups list.

### Step 3 — Evaluation Scores

```text
Candidate                    | Repeatability | Consistency | Mechanical | Total
---------------------------- | ------------- | ----------- | ---------- | -----
Meeting Notes → Action Items | 5             | 5           | 4          | 14/15
```

- **Repeatability: 5** — 4-5 times per week, every week
- **Consistency Need: 5** — Team depends on the same format; inconsistency causes confusion about who owns what
- **Mechanical: 4** — Almost entirely pattern extraction. The only judgment is occasionally deciding if something is an "action item" or just a "discussion point" — but even that follows a rule (does it have an owner and a deadline?)

### Decision Framework Check

1. More than once a month? **Yes** (4-5x/week)
2. Same steps each time? **Yes** (paste notes, extract items, format output)
3. Requires specific formatting Claude doesn't know? **Yes** (custom action item template with owner, due date, priority)
4. Same instructions repeatedly? **Yes** (identical prompt every time)

**Verdict:** Build it as a skill.

---

## Tips for Better Results

- **Be specific in your Speed Round** — "client onboarding emails" beats "email stuff"
- **Use real pain** — what actually frustrates you or eats your time, not what "should" be automated
- **Trust the patterns** — Claude spots repetition in your conversation history that you don't consciously see
- **Start with your highest-scoring candidate**, not your most ambitious idea
- **Iterate after you build** — v1.0 is always a draft. Use it a few times, then refine

## Next Steps

You now have evaluated skill candidates ranked by value. Here's what to do with them:

- **Take your #1 candidate** to the skill-building lesson and turn it into a working Claude Skill
- **Save your candidate list** — you'll likely come back and build 3-5 of them over time
- **Re-run the discovery process** in a few weeks — as you use Claude more, new patterns will emerge

## Related

- [Discover AI Workflow Opportunities](../../../business-first-ai-framework/discover.md) — Discover which workflows have the highest AI potential
- [Deconstruct Workflows](../../../business-first-ai-framework/deconstruct/index.md) — Break down complex workflows into discrete, automatable steps
- [Write Custom Workspace Instructions](../../../how-to/prompting/workspace-instructions-meta-prompt.md) — Set up Claude Projects with tailored instructions
- [Claude Projects Setup](../projects/claude-projects-setup.md) — Set up Claude Projects for recurring work
