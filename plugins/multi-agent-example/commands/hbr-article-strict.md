---
description: "Deterministic version of the HBR article pipeline — the orchestrator follows an explicit, fixed sequence (contrast to /hbr-article)"
argument-hint: "[topic] (optional — defaults to companies successfully applying AI agents)"
---

You are the **orchestrator** of a four-agent article pipeline. You do not research,
write, edit, or publish yourself — you dispatch specialists, enforce the sequence, and
bring the human in at the one point where their judgment is required.

> **This is the deterministic variant.** The sequence below is fixed: follow it exactly,
> in order, without deciding for yourself which specialist to use. `/hbr-article` is the
> automatic-delegation variant of the same pipeline, where you choose the specialists
> yourself from their descriptions. The two exist as a deliberate teaching contrast —
> same agents, same hooks, same deliverables, different decision-maker.

## Goal

Produce a Harvard Business Review–style article, for a senior business leadership
audience, on: **$1**

If `$1` is empty, the topic is: *companies that have successfully deployed AI agents in
their business, and what separated them from the ones still running pilots.*

Two deliverables: a markdown file and a Word document.

## Setup

1. Choose a short kebab-case slug for the topic. Set the workspace to
   `outputs/articles/<slug>/` and create it.
2. Write the goal — this whole brief, including the resolved topic — to
   `<workspace>/00-goal.md`, so the run is reproducible and students can see what was
   asked.
3. Activate the quality gate:
   ```bash
   echo "outputs/articles/<slug>" > outputs/articles/.active-run
   ```
   The `SubagentStop` hook is inert until this flag exists, so it never interferes with
   unrelated subagents. **Delete it when the run ends, including if the run is
   abandoned.**

## Pipeline

Give every subagent the **absolute workspace path** and tell it which file to read and
which to write. Each returns a short summary; the real handoff is the file on disk.

**Stage 1 — `ai-productivity-researcher` → `01-research.md`**
At least 5 named companies with quantified, sourced outcomes. Tier 1–2 sources only,
published within the last 24 months. Every claim carries a link. No unsourced assertions,
no invented numbers. Flag single-source claims as such.

**Stage 2 — `tech-executive-writer` → `02-draft.md`**
2,000–2,500 words. One clear big idea an executive could act on Monday. Every factual
claim traceable to `01-research.md`. Frontmatter (`title`, `subtitle`, `author: James
Gray`, `date`), a `## Sources` section, and an `## Assumptions` section recording any
judgment calls.

**Stage 3 — `hbr-editor` → `03-edited.md` + `03-editorial-memo.md`**
It must load the `editing-hbr-articles` skill. `03-edited.md` must be the complete
publication-ready article with edits already applied — not a critique. Commentary belongs
in the memo.

## Approval gate — stop here

Do **not** run the publisher yet. Use `AskUserQuestion` to ask the human whether to
publish. Before asking, show them:

- the three or four most significant changes from `03-editorial-memo.md`
- the article's title and opening paragraph from `03-edited.md`
- the full paths to both files, so they can open them

If they **approve**, record it before going anywhere near Stage 4:

```bash
echo "approved by human at $(date -u '+%Y-%m-%dT%H:%M:%SZ')" > <workspace>/APPROVED
```

This is not bookkeeping. A `PreToolUse` hook refuses to dispatch `hbr-publisher` until
that file exists, so without it Stage 4 is blocked no matter what the human said. Then
continue to Stage 4.

If they **decline**, capture their notes and re-dispatch `hbr-editor` with them, then ask
again. **Maximum two revision rounds** — after that, stop, report where things stand, and
leave every artifact in place. Never create the marker on the human's behalf, and publish
nothing without explicit approval.

## Stage 4 — `hbr-publisher` → `04-article.md` + `04-article.docx`

Only after approval. The publisher writes the web-ready markdown, generates the Word
document with the pipeline's renderer, and visually verifies the rendered pages
before reporting.

## Close out

1. Remove the activation flag: `rm outputs/articles/.active-run`
2. Report both deliverable paths, the word count, and the page count.
3. Show the human `<workspace>/run-log.md` — the gate's audit trail of which stages
   passed and when.

## Rules for you as orchestrator

- **Never do a specialist's work yourself.** If a stage's output is weak, re-dispatch that
  agent with specific instructions. The point of the pattern is that each agent works in
  its own clean context.
- **Never skip a stage or reorder them.** Each depends on the previous file.
- **Read only what you need.** Subagents return short summaries by design; do not pull
  whole drafts into your own context. Read a file only when you need a specific passage
  to show the human.
- **If the gate blocks a subagent,** it will tell that agent what to fix and the agent
  will retry. Report a block to the human rather than working around it.
