---
title: How to Discover Your Best Agent Skills
description: Use this guided process to identify your highest-value agent skill candidates by analyzing your work patterns, scoring candidates on three dimensions, and choosing the right approach — skill, workspace, or prompt. Works in Claude, ChatGPT, Copilot, Gemini, Cursor, and Codex.
---

:::note[Doing this live or want a faster path?]
This page is the worksheet version — ten questions you answer in a text editor before pasting into your AI tool. For a quicker, conversational version where the AI interviews you directly, try [Find Your Skill Candidates (Quick Prompt)](/agentic-building-blocks/skills/find-skill-candidates/).
:::

## Why This Matters

Agent skills make an AI assistant specific to YOUR work — not generic, but tuned to your tasks, your standards, and your formats. The best skills don't come from tasks you invent. They come from tasks you already do — the repetitive, structured work where you follow the same steps every time but the content changes.

This guide walks you through discovering those tasks, analyzing them, and evaluating which ones are worth building into skills. You'll walk away with 3-5 evaluated skill candidates ranked by value, with your #1 pick ready to build.

This page covers **discovery and evaluation only** — helping you identify what to build. A separate lesson covers the actual skill-building process.

:::note[Works in any AI tool]
[Agent Skills are an open standard](/agentic-building-blocks/skills/) — the same `SKILL.md` format runs in Claude, ChatGPT, Microsoft 365 Copilot, Cursor, OpenAI Codex, Gemini CLI, and VS Code Copilot. This process works in any of them. Where a step depends on something not every tool has — persistent memory, or skills that can reach your local files — it's called out inline.
:::

## Before You Start

- **An AI tool you can paste a long prompt into** — Claude, ChatGPT, Microsoft 365 Copilot, Gemini, Cursor, or OpenAI Codex all work. A paid tier usually gives you longer context and file attachments, both of which help.
- **A text editor for your answers** — Word, Google Docs, Apple Notes, Notepad — anything you can type in. You'll build up your answers across all three steps in this document, so keep it open throughout.
- **Some history helps, but only in tools that have it** — where your tool remembers past conversations, it can spot patterns you haven't noticed yourself. Many tools have no memory at all, and a fresh chat or a CLI session starts blank. That's fine: the ten questions carry the process on their own, and attaching your SOPs or templates does the same job as memory.

---

## Step 1 — Speed Round

The goal of this step is to produce a written list of 10 answers you'll feed to the AI in Step 2. You're not using AI yet — this is just you, thinking about your own work.

**What to do:**

1. Copy the 10 questions below into your text editor (use the copy button in the top-right corner of the code block)
2. Write your answer directly below each question — keep the question text there so the AI can see which question you're answering in Step 2
3. For each answer, give it a short label (2-5 words) followed by a one-sentence description
4. If a question doesn't apply to you, write "N/A" below it and move on

**The 10 questions — copy this entire block:**

```text
1. What task do you do weekly that follows the same steps every time?

2. What output do you produce repeatedly where the format stays the same but the content changes?

3. What task do you give the AI the same context or instructions for every conversation?

4. What task takes you 15-30 minutes but only 2-3 minutes of actual thinking — the rest is mechanical?

5. What do you copy-paste between documents or apps regularly?

6. What task would you delegate to a smart intern — straightforward judgment, tedious execution?

7. What recurring task involves reading something long and producing something short?

8. What process have you already built your own template, checklist, or SOP for?

9. What task drops in quality when you're tired — where consistency matters more than creativity?

10. What task do you use AI for conversationally but wish it just "knew how" to do?
```

:::tip[Your first instinct is usually right]
Don't try to think of the "best" answer. The point is to surface real work, not impressive-sounding work. If your answer is "formatting invoices" — that's a great candidate.
:::
**Here's what your finished answers should look like.** Notice the question stays — you type your answer on the line below it:

> 1. What task do you do weekly that follows the same steps every time?
> **Weekly status report** — Every Monday I gather updates from Slack, email, and our project board, then write a summary for my manager in the same format.
>
> 2. What output do you produce repeatedly where the format stays the same but the content changes?
> **Client proposal intro sections** — Same structure every time: who we are, what we understand about their problem, proposed approach. Only the client details change.
>
> 3. What task do you give the AI the same context or instructions for every conversation?
> **Meeting notes cleanup** — I paste raw meeting notes and ask the AI to extract action items, decisions, and owners. Same instructions every time.
>
> 4. What task takes you 15-30 minutes but only 2-3 minutes of actual thinking — the rest is mechanical?
> N/A
>
> *(…and so on for all 10 questions)*

Once you have all 10 answered in your text editor, move to Step 2.

---

## Step 2 — Analyze Your Answers

Now you'll hand your answers to the AI and let it do the analysis. Here's exactly what to do:

1. Open a new conversation in your AI tool
2. Copy the entire prompt below (use the copy button in the top-right corner of the code block)
3. **Before you send it:** fill in the `My AI tool:` line at the top, then scroll to the bottom of the prompt and find the line that says `[PASTE YOUR 10 ANSWERS HERE]` — delete that line and paste in your questions and answers from Step 1 (the whole block — questions included)
4. Send the prompt

```text
You are a Skills Discovery Analyst. Your job is to analyze my work patterns and identify my strongest agent skill candidates — tasks that are repeatable, structured, and would benefit from being encoded as a reusable skill rather than re-prompted every time.

My AI tool: [Replace this with the tool I'll build in — e.g. Claude, ChatGPT, Microsoft 365 Copilot, Gemini, Cursor, OpenAI Codex, VS Code Copilot.]

I've answered 10 discovery questions below. Use them as your primary input.

ALSO DO THIS, but only where you genuinely can:
- If you can see my earlier conversations, scan them for recurring tasks, repeated instructions, or patterns I might not have mentioned.
- If you have saved memory, custom instructions, or project/workspace context about me, check it for stored preferences and workflows that suggest additional candidates.
- If I've attached documents, mine them for processes I follow.

Say up front, in one line, which of those you actually have access to. If the answer is none of them, say so and work from my 10 answers alone — that is a perfectly normal outcome in a fresh chat or a tool without memory. Do not invent history, do not describe patterns you cannot point to, and never present an inference about me as something you observed. A fabricated pattern will send me off to build the wrong skill.

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

If tables render poorly in this tool or on a narrow screen, use a numbered list instead with the same fields labelled on their own lines — do not drop any field.

### 2. Top 3 Deep Dive

For each of your top 3 candidates, explain:
- **Why it scored high** — what makes this a strong skill candidate
- **What the skill would do** — a 2-3 sentence description of the skill's function
- **Input → Output** — what goes in, what comes out

### 3. Tool Fit

For each of the top 3, say whether my tool can actually run it. If skills there execute in a cloud sandbox, they can only work on what I upload or paste into the conversation — flag any candidate that depends on reading my local files, my inbox, or a live system, and say what I'd need instead (a connector, or a tool that runs skills locally). If skills there run on my machine with filesystem access, say so and move on. If my tool has no native skill support, name the closest equivalent it does have — a project, a gem, custom instructions, a saved prompt — and what I lose by using it.

### 4. Patterns from History

Note what you found (if anything) from the sources you listed at the top. Be specific — "I noticed you've asked me to format meeting notes 12 times in the last month" is useful. "No additional patterns found" is fine if there aren't any, and "I have no access to prior conversations" is the right answer if that's the case.

---

## My Speed Round Answers

[PASTE YOUR 10 ANSWERS HERE]
```

:::tip[Attach your documents for richer results]
If you have SOPs, templates, checklists, or process docs related to your answers, attach them to the conversation before sending the prompt. The AI will use them to produce more specific and accurate candidates — and in a tool without memory, they're the only evidence it has beyond your ten answers.
:::
### What to Expect

The AI will return:

- A line stating **what it can actually see** — memory, prior conversations, attachments, or nothing
- A **table of 5-8 candidates** sorted by Skill Score (highest first)
- A **detailed breakdown of your top 3** — why they scored high, what the skill would do, and what goes in vs. comes out
- A **tool fit check** — whether your platform can actually run each one
- **Notes on patterns** it found in your history, if it has any to draw on

The whole analysis typically fits in one response. Once you have it, **copy the candidate table into your text editor** — you'll need it for Step 3.

---

## Step 3 — Evaluate Your Candidates

Don't build yet. Score each candidate first so you build the right one.

Copy the scoring table below into your text editor, underneath the analysis from Step 2. Fill in one row for each of your top candidates.

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
- **Below 9** — A persistent workspace with custom instructions (a Claude Project, or your tool's equivalent) is probably a better fit than a full skill.

Your top 1-2 candidates are what you'll build in the next lesson.

---

## Skill, Workspace, or Prompt?

Not everything should be a skill. Here's how to tell which approach fits best.

Walk through these four questions for any candidate you're considering:

1. **Do you do this more than once a month?**
    - NO → Just use a prompt. Write it well, save it somewhere, and reuse it when you need it.
    - YES → Continue to question 2.

2. **Do you follow the same steps each time?**
    - NO → Better as a **persistent workspace** with custom instructions. A workspace gives the AI ongoing context without rigid steps.
    - YES → Continue to question 3.

3. **Does it require specific formatting or standards the AI doesn't know by default?**
    - NO → A saved prompt template may be enough. Try that first.
    - YES → Continue to question 4.

4. **Do you give the AI the same instructions repeatedly for this task?**
    - YES → This is a strong **Skill** candidate. Build it.
    - NO → Revisit whether a workspace with good custom instructions would cover it.

### Comparison

| Approach | Best For | Example |
|----------|----------|---------|
| Prompt | One-off or infrequent tasks | "Summarize this PDF" |
| Workspace | Recurring context without rigid steps | Client research workspace |
| Skill | Repeatable process with consistent format and standards | Weekly status report generation |

:::note[What "workspace" means in your tool]
Different platforms name this differently — Claude calls them Projects, and other tools use their own equivalents. The idea is the same: a container that holds standing instructions and reference files across many conversations, without prescribing a fixed procedure.
:::

---

## Worked Example — Meeting Notes to Action Items

Here's the full journey for one candidate, so you can see what each step produces.

### Step 1 — Speed Round Answer

> **Meeting notes cleanup** — After every meeting, I paste raw notes into the AI and ask it to extract action items with owners, key decisions, and follow-ups. Same format every time, same instructions every time. I do this 4-5 times a week.

### Step 2 — What the Analysis Produced

| # | Candidate Name | What It Does | How Often | Skill Score |
|---|---------------|-------------|-----------|-------------|
| 1 | Meeting Notes → Action Items | Extracts structured action items, decisions, and follow-ups from raw meeting notes | 4-5x/week | 5 |

> **Why it scored high:** Daily frequency, identical instructions every time, clear input (raw notes) and output (formatted action items), almost entirely mechanical — the "thinking" is in the meeting, not in the extraction.
>
> **What the skill would do:** Accept raw meeting notes (pasted text or attached document), extract all action items with assigned owners and due dates, list key decisions made, flag open questions and follow-ups, and output everything in a consistent Markdown format.
>
> **Input → Output:** Raw meeting notes → Formatted document with Action Items table, Decisions list, and Follow-ups list.
>
> **Tool fit:** Runs anywhere. The notes arrive by paste or attachment, so this needs no local file access and no connector — it works the same in a cloud sandbox as it does in a local CLI.

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
3. Requires specific formatting the AI doesn't know? **Yes** (custom action item template with owner, due date, priority)
4. Same instructions repeatedly? **Yes** (identical prompt every time)

**Verdict:** Build it as a skill.

---

## Tips for Better Results

- **Be specific in your Speed Round** — "client onboarding emails" beats "email stuff"
- **Use real pain** — what actually frustrates you or eats your time, not what "should" be automated
- **Trust the patterns, but check them** — in a tool with memory, the AI spots repetition in your history that you don't consciously see. In a tool without memory, be sceptical of any "pattern" it claims to have noticed; ask it to point to the evidence.
- **Start with your highest-scoring candidate**, not your most ambitious idea
- **Iterate after you build** — v1.0 is always a draft. Use it a few times, then refine

## Next Steps

You now have evaluated skill candidates ranked by value. Here's what to do with them:

- **Take your #1 candidate** to the [Skills setup guide](/ai-workflow-framework/skills/) and turn it into a working skill on your platform
- **Save your candidate list** — you'll likely come back and build 3-5 of them over time
- **Re-run the discovery process** in a few weeks — as your work shifts, new patterns will emerge

## Related

- [Skills (Building Block)](/agentic-building-blocks/skills/) — What skills are and which platforms support them
- [Find Your Skill Candidates (Quick Prompt)](/agentic-building-blocks/skills/find-skill-candidates/) — The fast, conversational version of this process
- [Analyze AI Workflow Opportunities](/ai-workflow-framework/analyze/) — Analyze which workflows have the highest AI potential
- [Deconstruct Workflows](/ai-workflow-framework/deconstruct/) — Break down complex workflows into discrete, automatable steps
- [Write Custom Workspace Instructions](/agentic-building-blocks/projects/workspace-instructions-meta-prompt/) — Set up a workspace with tailored instructions
- [Claude Projects Setup](/platforms/claude/projects/claude-projects-setup/) — Set up Claude Projects for recurring work
