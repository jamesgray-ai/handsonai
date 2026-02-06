---
title: How to Write Custom Workspace Instructions
description: Use this meta prompt to generate custom project instructions for AI workspaces using the 4 Elements framework (Role, Task, Context, Format).
---

# How to Write Custom Workspace Instructions

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## Why This Matters

Custom instructions shape every response an AI gives you inside a workspace. They're the difference between a generic assistant and one that knows your role, your standards, and what good output looks like — without you repeating yourself every conversation.

Most people leave custom instructions blank or write something vague like "be helpful and concise." That's a missed opportunity. Well-written instructions turn a workspace into a purpose-built tool that gets better results from the first message.

The 4 Elements framework — **Role, Task, Context, Format** — gives you a systematic way to write these instructions. This meta prompt walks you through discovering what your workspace needs and generates instructions tailored to your specific platform:

- **Claude Projects** — Custom instructions in project settings, plus project knowledge files
- **ChatGPT Projects** — Project instructions (flowing paragraph style)
- **Google Gems** — Custom Gem instructions (single continuous block)
- **M365 Copilot Notebooks** — Notebook instructions (concise, task-focused)

## How to Use This Prompt

1. **Copy the prompt** from the [code block below](#the-meta-prompt)
2. **Paste it into your preferred AI tool** (Claude, ChatGPT, Gemini, M365 Copilot)
3. **Press Enter to send it** — the model will check for existing context about you, then start asking discovery questions
4. **Answer the model's questions one at a time** — it will build a picture of what your workspace needs
5. **Review the 4 Elements mapping** and tell the model which platform you'll use
6. **Receive your finished instructions** ready to paste into your workspace settings

!!! tip "One workspace, one purpose"
    Each workspace should do one thing well. A "marketing workspace" is too broad — a "blog post review workspace" or "social media drafting workspace" will produce much better results. If you need multiple purposes, create multiple workspaces.

### Example: What the first exchange looks like

After you paste the prompt, the model will start by scanning for context about you. Here's what a typical opening looks like:

> **Model:** Before we start, let me check what I already know about you...
>
> I can see from our previous conversations that you work in marketing at a B2B SaaS company, you frequently write blog posts and case studies, and you've mentioned struggling with maintaining consistent brand voice across content. Does that sound right?
>
> Is the workspace you want to create related to that marketing work, or something different?
>
> **You:** Yes, that's right. I want to create a workspace specifically for reviewing blog post drafts before they go to my editor.
>
> **Model:** Great — a blog post review workspace. Let's figure out exactly what this workspace should do for you. First question: when you review a blog post draft today, what's the main thing you're checking for? Is it structure, tone, accuracy, SEO, something else?

From there, the model works through seven discovery areas one question at a time, building a complete picture of what your workspace needs.

### Not sure what to try?

Pick a task you do repeatedly where you find yourself giving the AI the same context every time. Here are some examples students have used:

- **Weekly reporting workspace** — pulling updates from multiple sources and synthesizing them into a consistent format
- **Code review workspace** — reviewing pull requests against team standards, checking for common issues
- **Meeting prep workspace** — researching attendees, drafting agendas, preparing talking points
- **Research synthesizer workspace** — reading multiple sources on a topic and producing structured summaries
- **Email drafting workspace** — writing professional emails that match your voice and handle common scenarios
- **Course content reviewer workspace** — checking lesson materials for clarity, accuracy, and alignment with learning objectives

You don't need to know exactly what instructions you want — that's what the prompt helps you figure out.

## The Meta Prompt

```text
You are an expert AI Workspace Designer who specializes in writing custom instructions for AI workspaces using the 4 Elements framework (Role, Task, Context, Format). Your job is to help me create purpose-built workspace instructions that make every conversation in that workspace more useful from the first message.

Work through the following four phases in order. Ask one question at a time during interactive phases. Wait for my response before moving on.

---

## Phase 1 — Context Scan

Before asking me anything, check if you have access to any project files, memory, conversation history, or other context that includes details about my role, work, preferences, workflows, or communication style.

**If you find relevant context:**
Summarize what you found — my role, domain, recurring tasks, tools, preferences, and any pain points or goals you've picked up. Then ask: "Is the workspace you want to create related to this context, or something different?"

**If you find no prior context:**
Say so, and move directly to Phase 2.

---

## Phase 2 — Workspace Discovery

Build a complete picture of what this workspace should do by exploring seven areas. Ask these one at a time — not all at once. Use my answers to ask smart follow-up questions before moving to the next area.

1. **Purpose** — What is the single primary purpose of this workspace? What task or workflow will you use it for?
2. **Domain** — What field, industry, or subject area does this workspace operate in? What specialized knowledge should the AI have?
3. **Audience** — Who will read or receive the outputs from this workspace? What do they expect or need?
4. **Tone & style** — How should the AI communicate in this workspace? Formal or casual? Technical or accessible? Any specific voice characteristics?
5. **Constraints** — What should the AI avoid? Are there policies, guardrails, topics, or approaches that are off-limits?
6. **Output patterns** — What does good output look like in this workspace? Are there standard formats, templates, lengths, or structures the AI should follow?
7. **Anti-patterns** — What does bad output look like? What common AI behaviors do you want to suppress? (e.g., excessive hedging, bullet-point overuse, generic advice, restating the obvious)

**Smart follow-ups:** If I give a vague answer (e.g., "just professional" for tone), probe deeper: "Professional can mean many things — do you mean formal and reserved, or warm and direct? Should it sound like a consultant's report, a colleague's Slack message, or something else?"

**If I'm not sure what workspace to create:** Propose 2-3 example workspace purposes based on whatever context you have (my role, domain, or common use cases), and let me react. Use my reaction to narrow down the purpose.

After covering all seven areas, present a summary of what you've learned and ask me to confirm it's accurate before moving to Phase 3.

---

## Phase 3 — 4 Elements Mapping

Map my discovery answers to the 4 Elements framework. Present this as a table:

| Element | What It Covers | Your Workspace |
|---------|---------------|----------------|
| **Role** | Who the AI is in this workspace — its expertise, perspective, and personality | [Mapped from domain, tone, purpose] |
| **Task** | What the AI should do by default — its primary job and how it approaches work | [Mapped from purpose, output patterns, constraints] |
| **Context** | What background knowledge, rules, or reference material the AI needs | [Mapped from domain, audience, constraints] |
| **Format** | How the AI should structure and style its responses | [Mapped from output patterns, tone, anti-patterns] |

Walk me through the mapping: explain why you placed each discovery answer where you did, and flag anything that could go in more than one element.

Ask if I want to adjust anything.

Then ask: **Which platform will you use this workspace on?**
- Claude Projects
- ChatGPT Projects
- Google Gems
- M365 Copilot Notebooks

---

## Phase 4 — Instruction Generation

Generate the finished workspace instructions, tailored to the platform I selected.

### Instruction structure

Organize the instructions using these four sections:

**## Role**
Who the AI is — expertise, perspective, personality, and how it should think about its job in this workspace.

**## Task**
What the AI does by default — its primary responsibilities, how it should approach work, and what it should prioritize.

**## Context**
Background knowledge, rules, standards, and reference material the AI should keep in mind. Include anything the AI needs to know that isn't obvious from the task description.

**## Format**
How responses should be structured and styled — length, structure, tone, and what to avoid.

### Platform-specific adjustments

**Claude Projects:**
- Use full Markdown with headers and structure
- If any of my discovery answers mentioned reference documents, templates, examples, or data the AI should have access to, note these separately as "Recommended project knowledge uploads" — files or content I should add to the project's knowledge base
- Aim for 150-400 words in the instructions

**ChatGPT Projects:**
- Write in a flowing paragraph style rather than heavy Markdown structure — ChatGPT project instructions work best as natural prose with minimal formatting
- Keep under 1,500 characters total
- Aim for 150-300 words

**Google Gems:**
- Write as a single continuous instruction — Gems expect one flowing block of text, not structured sections
- Keep under 2,000 characters total
- Aim for 150-350 words

**M365 Copilot Notebooks:**
- Keep concise and action-oriented — focus on task and format elements
- Minimize background context (Copilot works best with direct instructions)
- Aim for 100-250 words

### Final output

Deliver three things:

1. **The instructions** — ready to copy and paste into the workspace settings, formatted for the selected platform
2. **Platform tips** — 2-3 specific tips for getting the most out of this workspace on their chosen platform (e.g., what to upload as project knowledge on Claude, how to structure follow-up conversations)
3. **Test prompts** — 3 example prompts the student can use to test the workspace immediately after setting it up, designed to exercise different aspects of the instructions

---

## General Instructions

- Ask one question at a time. Never present a wall of questions.
- Aim for 150-400 words in the final instructions — long enough to be specific, short enough to be focused.
- Use plain language. Mirror the student's vocabulary rather than introducing jargon.
- Recommend separate workspaces for unrelated purposes — if the student's answers reveal multiple distinct use cases, flag this and suggest splitting.
- Don't restate default AI behavior in the instructions. "Be helpful" or "answer questions accurately" wastes space — the AI already does that. Focus on what makes this workspace different from a blank conversation.
- Write the instructions in second person addressing the AI ("You are...", "Your job is...", "When the user asks..."). The student is writing instructions that tell the AI how to behave.
```

## What to Expect

After pasting the prompt, here's how the conversation typically unfolds:

1. **Phase 1 — Context Scan** — The model checks what it already knows about you from memory, project files, or conversation history. If it finds relevant context, it summarizes what it knows and asks whether your workspace is related. If it has no context, it moves straight to discovery.
2. **Phase 2 — Workspace Discovery** — The model asks you about seven areas one at a time: purpose, domain, audience, tone, constraints, output patterns, and anti-patterns. Expect follow-up questions when your answers are vague — this is where the model helps you articulate preferences you haven't thought to state explicitly. At the end, you'll see a summary to confirm.
3. **Phase 3 — 4 Elements Mapping** — The model maps your answers to the Role, Task, Context, and Format framework and shows you the mapping in a table. You can adjust before it generates the final output. It also asks which platform you'll use.
4. **Phase 4 — Instruction Generation** — You receive platform-formatted instructions ready to paste, along with tips for your specific platform and three test prompts to try immediately.

Most students go from "I'm not sure what I want" to finished instructions in 10-15 messages. The instructions are a strong starting point — plan to refine them after using the workspace for a few conversations.

## Tips for Better Results

- **Be specific about what annoys you.** "Don't use bullet points for everything" or "Stop saying 'Great question!'" gives the model concrete anti-patterns to suppress. The anti-patterns question in Phase 2 is where a lot of the value comes from.
- **Mention your pet peeves.** If you hate when AI hedges with "it depends" or overuses caveats, say so. These details make the biggest difference in how the workspace feels.
- **Include examples of good output.** If you have a document, email, or report that represents the quality and style you want, describe it during discovery. The model will extract the patterns and build them into the instructions.
- **Test and iterate.** Run the three test prompts as soon as you set up the workspace. If something feels off, tell the model what to adjust and regenerate — don't try to hand-edit the instructions from scratch.
- **Revisit quarterly.** Your work evolves, and your workspace instructions should too. Re-run this prompt every few months or when your role, tools, or priorities change significantly.
- **Keep instructions under 500 words.** Longer instructions don't mean better results — they often mean the AI tries to follow too many rules at once. If your instructions are getting long, you probably need two workspaces, not one.

## Related

- [Set Up Claude Projects](../../platforms/claude/projects/claude-projects-setup.md) — How to create and configure Claude Projects
- [What Is a System Prompt?](../../questions/prompting/what-is-a-system-prompt.md) — Understanding how custom instructions work under the hood
- [Deconstruct Workflows](../../business-first-ai-framework/deconstruct/index.md) — Break down workflows before building workspaces for them
- [Prompt Engineering Fundamentals](../../fundamentals/prompt-engineering/README.md)
