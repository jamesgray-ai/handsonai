---
title: Find Your Skill Candidates (Quick Prompt)
description: A single copy-paste prompt that interviews you, reviews whatever your AI already knows about your work, and ranks your best agent skill candidates. Works in Claude, ChatGPT, Copilot, Gemini, Cursor, and Codex.
---

## Why This Matters

The best agent skills come from work you already do repeatedly — not ideas you brainstorm on the spot. This prompt puts the AI in the analyst seat: it reviews whatever it already knows about you, interviews you about your recurring work, and returns a ranked table of skill candidates with the single best one to build first.

Use this when you want a fast, conversational discovery in one chat — ideal for live sessions or when you want the AI to do the heavy lifting. Prefer a worksheet you can fill out on your own time? → [How to Discover Your Best Agent Skills (Worksheet)](/agentic-building-blocks/skills/skills-discovery-meta-prompt/).

:::note[Works in any AI tool]
[Agent Skills are an open standard](/agentic-building-blocks/skills/) — the same `SKILL.md` format runs in Claude, ChatGPT, Microsoft 365 Copilot, Cursor, OpenAI Codex, Gemini CLI, and VS Code Copilot. This prompt is written to run in any of them. It adapts to what your tool can actually do, including whether it has memory of your past conversations and whether skills run locally or in a cloud sandbox.
:::

## How to Use This Prompt

1. **Copy the prompt** from the [code block below](#the-prompt) using the copy button in the top-right of the block
2. **Fill in the "My AI tool" line** at the top — this is the one edit you need to make. It tells the AI what it can realistically recommend.
3. **Open a new conversation** in that tool and paste the prompt
4. **Read the capability line it returns first** — it will tell you whether it has memory or stored context to work from. If it has none, it skips straight to the interview. That's expected, not a failure.
5. **Answer one question at a time** during Phase 2 — be specific about real work, not ideal work
6. **Review the ranked table** in Phase 3 and pick the top candidate to build

:::tip[Attach your SOPs for sharper results]
If you have templates, checklists, or process docs, attach them before sending. The AI will use them to produce more accurate candidates — and this matters most in tools with no memory, where attached files are the only evidence of how you actually work.
:::

## The Prompt

```text
You are an AI workflow analyst helping me identify the best candidates to package as agent skills — reusable bundles of instructions, context, and reference material that an AI assistant loads on demand to handle a repeatable task consistently.

My AI tool: [Replace this with the tool I'll build in — e.g. Claude, ChatGPT, Microsoft 365 Copilot, Gemini, Cursor, OpenAI Codex, VS Code Copilot. If I left this blank, ask me before you do anything else.]

Before Phase 1, state in one or two lines what you can actually draw on to analyze my work. Choose honestly from: saved memory about me, custom instructions or project/workspace context, earlier messages in this conversation, files I have attached, or none of the above.

Do not invent or infer details about me. If you have no stored information about my work, say so plainly in one line and go straight to Phase 2. Never present a guess as something you remember — a fabricated profile will corrupt every ranking that follows.

What qualifies as a skill candidate — any ONE of these is enough:
- A **repeatable task** I do more than once, with a recognizable trigger ("every Monday", "whenever a new X arrives", "before every client call") and a stable output shape
- **Reused context or reference material** I paste into the AI over and over — brand guidelines, voice rules, product facts, glossaries, policy docs, SOPs, templates, style guides, example outputs, frameworks, rubrics
- **Standing instructions** I find myself re-typing into prompts ("always do X", "never do Y", "structure it like Z", "use this tone", "follow this checklist")
- Any combination of the above — most real skills bundle a repeatable task WITH the context and instructions it needs

What does NOT qualify (exclude these):
- One-off creative work with no repeat pattern
- Tasks requiring live access to systems or data the AI cannot reach, unless a connector or integration for it already exists in my tool
- Pure judgment calls with no underlying rubric
- Things better solved by a macro, a script, or a full agent rather than a skill

We'll work through this in three phases.

---

Phase 1 — Context Review

Using only the sources you listed above, review what you already know about my work: role, tools, recurring workflows, tasks I've asked for help with repeatedly, documents I've had you draft, and patterns in how I work.

List the candidate tasks you can actually evidence. For each, include:
- The task in one line
- Why it stood out (frequency, consistent pattern, same tools/inputs, same output shape)
- Where the evidence came from (a memory entry, a prior session, an attached file, an earlier message in this chat)

If you have nothing usable, say so in one line and move to Phase 2. Do not pad this phase.

---

Phase 2 — Discovery Interview

Ask me exactly ONE question per message. Do not batch questions, do not number a list of questions, and do not move on until I have answered. After each answer, probe deeper on that answer before advancing.

Cover these areas, adapting order to what I reveal:

1. Tasks I do weekly or more often
2. Work that pulls information from multiple apps, docs, or people
3. Work that produces a consistent output shape (report, email, summary, update, ticket, post)
4. Decisions I make by following a pattern or checklist rather than gut
5. Tasks I dread or delay because they're tedious, not hard
6. **Context I paste into the AI over and over** — brand/voice guides, product info, glossaries, customer data, framework definitions, style rules, reference docs, example outputs
7. **Standing instructions I repeat** — "always include X", "never do Y", "format like Z", "match this tone" — things I catch myself re-typing
8. Templates, rubrics, checklists, or "the way I do X" knowledge that lives in my head or in scattered docs

Continue until we have at least 6 distinct tasks (Phase 1 + interview combined). Then move to Phase 3.

---

Phase 3 — Ranked Output

Produce a ranked table:

| Rank | Task | Trigger | Frequency | Time/Instance | Inputs | Output | Source | Potential | Why |

- Source: Memory/Context, Interview, or Both
- Potential:
  - 🟢 High — clear trigger, predictable inputs/output, procedural logic I could describe in a checklist
  - 🟡 Medium — mostly structured but needs occasional judgment or missing context
  - 🔴 Low — too creative, relational, or context-dependent to package as a skill today

Rank highest to lowest potential. If tables render poorly in this tool or on a narrow screen, use a numbered list instead with the same fields labelled on their own lines — do not drop any field.

Judge Potential against what my tool can actually do. If skills there run in a cloud sandbox, they can only work on what I upload or paste into the conversation — a task that depends on reading my local files, my inbox, or a live system is at best 🟡 and you should say why. If skills there run on my machine with filesystem and command access, that constraint doesn't apply.

After the table, provide:
1. The single best candidate to build first and why it delivers the biggest leverage (frequency × time saved × consistency gain)
2. What the skill would need to contain — instructions, templates, examples, reference files, tool or connector requirements
3. Any borderline candidates better served by something other than a skill — a full agent, a connector or integration to a live system, or a plain saved prompt
4. If my tool does not support agent skills natively, name the closest equivalent it does support (project, gem, custom instructions, saved prompt) and say what I lose by using it instead

---

Start now: state your available sources, then begin Phase 1.
```

## What to Expect

- **Sources line** — Before anything else, the AI states what it can draw on. In a tool with memory, that's your history. In a fresh chat or a CLI, it should say it has nothing and move on. If it claims to remember things you never told it, stop and start over — you're in a tool without memory and it's confabulating.
- **Phase 1** — Evidenced candidates only. Skipped entirely when there's no stored context.
- **Phase 2** — One question at a time. Expect 6–10 exchanges. Answer with specifics ("Monday status update for my manager"), not categories ("status stuff").
- **Phase 3** — A ranked table plus a recommendation for the first skill to build, what to put in it, whether your tool can actually run it, and which candidates are better suited to an agent, a connector, or a saved prompt.

## Next Steps

- Take your #1 candidate to the [Skills setup guide](/ai-workflow-framework/skills/) and install it in your platform — or, if you're on Claude, [Installing Skills on Claude](/platforms/claude/skills/installing-skills/)
- Re-run this prompt in a few weeks as new patterns emerge in your work
- Browse [Skills Resources](/platforms/claude/skills/resources/) for examples and deeper reference material

## Related

- [Skills (Building Block)](/agentic-building-blocks/skills/) — What skills are and which platforms support them
- [How to Discover Your Best Agent Skills](/agentic-building-blocks/skills/skills-discovery-meta-prompt/) — The full worksheet-driven version of this process
- [Write Custom Workspace Instructions](/agentic-building-blocks/projects/workspace-instructions-meta-prompt/) — Companion meta prompt for Claude Projects
- [Analyze AI Workflow Opportunities](/ai-workflow-framework/analyze/) — Broader workflow audit across your whole role
