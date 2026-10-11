---
title: Find Your Skill Candidates (Quick Prompt)
description: "A copy-paste prompt that reviews your recent work and what your AI already knows about you, asks a few questions, and recommends the task skill and reference skill to build first, on any platform."
---

## Why This Matters

The best agent skills come from work you already do repeatedly — not ideas you brainstorm on the spot. This prompt puts the AI in the analyst seat: it reviews whatever it can see of your work — your calendar, email, and recent files where it's connected to them, plus its memory of you and your past conversations — then asks you a few questions to fill the gaps. It returns a ranked table of skill candidates and recommends a pair to build first: a task skill and the reference skill it applies.

Use this when you want a fast, conversational discovery in one chat — ideal for live sessions or when you want the AI to do the heavy lifting. Prefer a worksheet you can fill out on your own time? → [How to Discover Your Best Agent Skills (Worksheet)](/agentic-building-blocks/skills/skills-discovery-meta-prompt/).

:::note[Works in any AI tool]
[Agent Skills are an open standard](/agentic-building-blocks/skills/) — the same `SKILL.md` format runs in Claude, ChatGPT, Microsoft 365 Copilot, Cursor, OpenAI Codex, Gemini CLI, and VS Code Copilot. This prompt is written to run in any of them. It adapts to what your tool can actually do, including whether it can see your calendar and email, whether it has memory of your past conversations, and whether skills run locally or in a cloud sandbox.
:::

## How to Use This Prompt

1. **Copy the prompt** from the [code block below](#the-prompt) using the copy button in the top-right of the block
2. **Fill in the "My AI tool" line** at the top. It tells the AI what it can realistically recommend.
3. **Check the "Sources you may use" line.** By default the AI may look at your calendar, email, recent files, its memory of you, and your past conversations. Delete any you'd rather it didn't use; the prompt works with none of them.
4. **Open a new conversation** in that tool and paste the prompt
5. **Read the first line it returns.** It tells you which of your allowed sources it can actually reach. If it can reach none, it skips straight to the questions. That's expected, not a failure.
6. **Answer one question at a time** in Phase 2. Be specific about real work, not ideal work.
7. **Review the recommendations** in Phase 3: a ranked table, then one task skill and one reference skill to build first.

:::tip[Give it your real work for sharper results]
- **Connect your calendar and email first, if you're comfortable with it.** Two weeks of meetings and sent mail show what you actually repeat, not what you remember repeating. The AI is told to describe patterns, not quote your email. Deleting a source from the prompt is a request, not a switch: some tools (Microsoft 365 Copilot, for one) search everything you've connected and may still show meeting titles or file names as citations. If that matters, turn the connector off, and don't share your screen while it runs. Microsoft 365 Copilot can see them already; in Claude and ChatGPT, turn on their email and calendar connectors.
- **Attach your SOPs, templates, or checklists.** The AI uses them to produce more accurate candidates. This matters most in tools with no memory or connections, where attached files are the only evidence of how you actually work.
:::

## The Prompt

```text
You are an AI workflow analyst helping me find the best work to package as Agent Skills: reusable folders of instructions and reference material that an AI loads when a task needs them, so it handles that task the same way every time.

My AI tool: [Replace with the tool I'll build in, e.g. Claude, Claude Code, ChatGPT, Microsoft 365 Copilot, Gemini, Cursor, OpenAI Codex, VS Code Copilot. If I left this blank, ask me before doing anything else.]

Sources you may use: my calendar, my email, my recent files, your memory of me, and our past conversations. [Delete any you don't want the AI to use, then delete this note.]

Two kinds of skill matter here:
- A **reference skill** holds knowledge my work draws on: brand or voice guidelines, a style guide, product facts, a glossary, policies, templates, example outputs.
- A **task skill** holds the steps for one job I repeat, such as drafting a client email, writing a weekly update, or summarizing a meeting. It applies a reference skill when it needs one.

What makes a good candidate (any one is enough):
- Work I repeat, with a recognizable trigger ("every Monday", "after every client call") and output that looks the same each time
- Context I give the AI over and over: guidelines, background, examples
- Instructions I keep re-typing: "always include X", "never do Y", "use this tone"

Leave out: one-off creative work, pure judgment calls with no rubric, and work that needs systems my tool can't reach.

Rules:
- Use only the sources I allowed above, and only the ones you can actually reach.
- Never invent or guess details about me. If you have nothing to go on, say so in one line.
- Describe patterns, not private details: don't quote emails, names, figures, meeting titles, or file names, and skip anything that reaches you through a source I removed.
- If you don't know a value, write "?" rather than estimating.

We'll work in three phases.

---

Phase 1 — Review my work

First, in one or two lines, say which of my allowed sources you can actually reach (or say none).

If you can see my calendar, email, or recent files, look at the last two weeks for work I repeat: recurring meetings that lead to the same follow-up, emails I write the same way, documents I produce on a schedule. Then add what you already know about me from memory or past conversations.

List the candidates you can actually point to, one line each: the task, why it stood out, and where you saw it (calendar, email, a file, memory, a past conversation, or "you told me"). If you have nothing, say so and go to Phase 2.

---

Phase 2 — A few questions

Ask me one question per message, and wait for my answer before the next. Ask about whatever Phase 1 didn't cover:
- Work I do weekly or more often, what it produces, and roughly how long it takes
- Guidelines, background, or examples I give the AI every time
- Instructions I keep re-typing
- Tedious work I put off, or work with a checklist I follow

Keep it short: stop when we have at least five candidates, usually after three to five questions. If I say "keep going", ask more.

---

Phase 3 — Recommendations

Give me a ranked table:

| Rank | Task | How often | Time each time | Knowledge it draws on | Where you saw it | Potential |

Potential: 🟢 High (clear trigger, same steps, same output), 🟡 Medium (mostly structured, needs some judgment or missing context), 🔴 Low (too creative or one-off for a skill today). If tables display poorly here, use a numbered list with the same fields.

Judge against what my tool can do. If skills there run in the cloud, they work only on what I upload or paste in; a task that needs my local files, inbox, or a live system is at best 🟡, and say why.

Then recommend what to build first, as a pair:
1. **A task skill**: the one candidate to start with, usually your #1 (if not, say why). Prefer something small: a few steps, in order, that I could build together with its reference skill in about 25 minutes. Say why it pays off (how often × time saved × consistency).
2. **A reference skill** it should apply: the knowledge that task draws on. If nothing more specific stands out, suggest my brand or writing guidelines. If that knowledge is a long document, plan for me to upload it whole rather than condense it.
3. For each of the two, what to give the AI when I build it: the steps, the source documents, and one or two real examples.

Finally, name any candidate better served by something else (an agent, a connector, or a saved prompt), and if my tool doesn't support Agent Skills, name its closest equivalent. If you're not sure what my tool supports today, say so instead of guessing.

---

Start now with Phase 1.
```

## What to Expect

- **Sources line** — Before anything else, the AI says which of your allowed sources it can reach. With connectors, that includes your calendar, email, and files; in a tool with memory, your history. In a fresh chat or a CLI, it should say it has nothing and move on. If it claims to remember things you never told it, stop and start over — you're in a tool without memory and it's confabulating.
- **Phase 1** — Evidenced candidates only, each with where it came from. Skipped entirely when there's nothing to review.
- **Phase 2** — One question at a time. Expect three to five; say "keep going" for more. Answer with specifics ("Monday status update for my manager"), not categories ("status stuff").
- **Phase 3** — A ranked table, then a pair to build first: a task skill and the reference skill it applies, with what to give the AI for each. It also flags candidates better suited to an agent, a connector, or a saved prompt.

## Next Steps

- Take your #1 candidate to the [Skills setup guide](/ai-workflow-framework/skills/) and install it in your platform — or, if you're on Claude, [Installing Skills on Claude](/platforms/claude/skills/installing-skills/)
- Re-run this prompt in a few weeks as new patterns emerge in your work
- Browse [Claude Skills Resources](/platforms/claude/skills/resources/) for examples and deeper reference material — Claude-specific, but the structure and testing advice carries across platforms

## Related

- [Skills (Building Block)](/agentic-building-blocks/skills/) — What skills are and which platforms support them
- [How to Discover Your Best Agent Skills](/agentic-building-blocks/skills/skills-discovery-meta-prompt/) — The full worksheet-driven version of this process
- [Write Custom Workspace Instructions](/agentic-building-blocks/projects/workspace-instructions-meta-prompt/) — Companion meta prompt for Claude Projects
- [Analyze AI Workflow Opportunities](/ai-workflow-framework/analyze/) — Broader workflow audit across your whole role
