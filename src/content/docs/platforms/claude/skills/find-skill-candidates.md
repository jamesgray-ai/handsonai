---
title: Find Your Skill Candidates (Quick Prompt)
description: A single copy-paste prompt that interviews you, reviews your Claude memory, and ranks your best agent skill candidates.
---

## Why This Matters

The best Claude Skills come from work you already do repeatedly — not ideas you brainstorm on the spot. This prompt puts Claude in the analyst seat: it reviews what it already knows about you from memory, interviews you about your recurring work, and returns a ranked table of skill candidates with the single best one to build first.

Use this when you want a fast, conversational discovery in one Claude chat — ideal for live sessions or when you want Claude to do the heavy lifting. Prefer a worksheet you can fill out on your own time? → [Discover Your Best Claude Skills (Worksheet)](./skills-discovery-meta-prompt.md).

## How to Use This Prompt

1. **Copy the prompt** from the [code block below](#the-prompt) using the copy button in the top-right of the block
2. **Open a new conversation** in Claude (Pro or higher — memory access helps but isn't required)
3. **Paste and send** — Claude will start with Phase 1 (memory review)
4. **Answer one question at a time** during Phase 2 — be specific about real work, not ideal work
5. **Review the ranked table** in Phase 3 and pick the top candidate to build

:::tip[Attach your SOPs for sharper results]
If you have templates, checklists, or process docs, attach them before sending. Claude will use them to produce more accurate candidates.
:::

## The Prompt

```text
You are an AI workflow analyst helping me identify the best candidates to package as Claude agent skills — reusable bundles of instructions, context, and reference material that Claude loads on demand to handle a repeatable task consistently.

What qualifies as a skill candidate — any ONE of these is enough:
- A **repeatable task** I do more than once, with a recognizable trigger ("every Monday", "whenever a new X arrives", "before every client call") and a stable output shape
- **Reused context or reference material** I paste into Claude over and over — brand guidelines, voice rules, product facts, glossaries, policy docs, SOPs, templates, style guides, example outputs, frameworks, rubrics
- **Standing instructions** I find myself re-typing into prompts ("always do X", "never do Y", "structure it like Z", "use this tone", "follow this checklist")
- Any combination of the above — most real skills bundle a repeatable task WITH the context and instructions it needs

What does NOT qualify (exclude these):
- One-off creative work with no repeat pattern
- Tasks requiring real-time access to systems Claude can't reach (unless an MCP or tool already exists)
- Pure judgment calls with no underlying rubric
- Things better solved by a macro, script, or a full agent rather than a skill

We'll work through this in three phases.

---

Phase 1 — Memory Review

Before asking me anything, review everything you know about me from memory: role, tools, recurring workflows, tasks I've asked for help with repeatedly, documents I've had you draft, and patterns in how I work.

List the candidate tasks you've already observed. For each, include:
- The task in one line
- Why it stood out (frequency, consistent pattern, same tools/inputs, same output shape)
- What memory entries or prior sessions it came from

If you find nothing usable, say so and skip to Phase 2.

---

Phase 2 — Discovery Interview

Ask me focused questions one at a time. After each answer, probe deeper before moving on. Cover these areas, adapting order to what I reveal:

1. Tasks I do weekly or more often
2. Work that pulls information from multiple apps, docs, or people
3. Work that produces a consistent output shape (report, email, summary, update, ticket, post)
4. Decisions I make by following a pattern or checklist rather than gut
5. Tasks I dread or delay because they're tedious, not hard
6. **Context I paste into Claude over and over** — brand/voice guides, product info, glossaries, customer data, framework definitions, style rules, reference docs, example outputs
7. **Standing instructions I repeat** — "always include X", "never do Y", "format like Z", "match this tone" — things I catch myself re-typing
8. Templates, rubrics, checklists, or "the way I do X" knowledge that lives in my head or in scattered docs

Continue until we have at least 6 distinct tasks (memory + interview combined). Then move to Phase 3.

---

Phase 3 — Ranked Output

Produce a ranked table:

| Rank | Task | Trigger | Frequency | Time/Instance | Inputs | Output | Source | Potential | Why |

- Source: 🧠 Memory, 🗣️ Interview, or Both
- Potential:
  - 🟢 High — clear trigger, predictable inputs/output, procedural logic I could describe in a checklist
  - 🟡 Medium — mostly structured but needs occasional judgment or missing context
  - 🔴 Low — too creative, relational, or context-dependent to package as a skill today

Rank highest to lowest potential.

After the table, provide:
1. The single best candidate to build first and why it delivers the biggest leverage (frequency × time saved × consistency gain)
2. What the skill would need to contain — instructions, templates, examples, reference files, tool requirements
3. Any borderline candidates that might be better as a full agent, an MCP connection, or a simple prompt template instead

---

Start with Phase 1 now.
```

## What to Expect

- **Phase 1** — Claude reports what it already sees in memory. If the account is new, it skips to Phase 2.
- **Phase 2** — One question at a time. Expect 6–10 exchanges. Answer with specifics ("Monday status update for my manager"), not categories ("status stuff").
- **Phase 3** — A ranked table plus a recommendation for the first skill to build, what to put in it, and which candidates are actually better suited to an agent, MCP connection, or saved prompt.

## Next Steps

- Take your #1 candidate to [Installing Skills on Claude](./installing-skills.md) and build it
- Re-run this prompt in a few weeks as new patterns emerge in your Claude memory
- Browse [Skills Resources](./resources.md) for examples and deeper reference material

## Related

- [Discover Your Best Claude Skills](./skills-discovery-meta-prompt.md) — The full worksheet-driven version of this process
- [Write Custom Workspace Instructions](../../../agentic-building-blocks/projects/workspace-instructions-meta-prompt.md) — Companion meta prompt for Claude Projects
- [Analyze AI Workflow Opportunities](../../../business-first-ai-framework/analyze/) — Broader workflow audit across your whole role
