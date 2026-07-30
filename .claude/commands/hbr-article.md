---
description: Produce a business article through automatic delegation — you choose which specialist agents to use and when
argument-hint: "[topic] (optional — defaults to companies successfully applying AI agents)"
---

## Goal

Produce a Harvard Business Review–style article, for a senior business leadership
audience, on: **$1**

If `$1` is empty, the topic is: *companies that have successfully deployed AI agents in
their business, and what separated them from the ones still running pilots.*

**Done means two files exist on disk:** the article as markdown, and the article as a
Word document. Publication quality, and defensible — every factual claim traceable to a
credible, cited source.

## How to approach this

**You have specialist subagents available, and you decide which to use and when.** This
is deliberate: read the available agent descriptions, work out which specialists this
goal calls for, and delegate to them in whatever order the work requires. Nobody is
handing you a sequence.

Three rules constrain *how* you delegate, not *what* you choose:

1. **Do not do a specialist's work yourself.** If a specialist exists for a part of this
   goal, dispatch it rather than doing that part in your own context. This is the whole
   point — you are coordinating experts, not doing the job with help. Notably: do not
   research the case studies yourself, and do not write or edit the prose yourself.
2. **Every handoff goes through a file, and every subagent gets the absolute workspace
   path.** Subagents cannot see your context or each other's. If you don't tell an agent
   where to read from and write to, the chain breaks.
3. **Keep your own context clean.** Subagents return short summaries plus paths by
   design. Don't pull whole dossiers or drafts into your context; read a specific file
   only when you need a specific passage.

## Workspace

1. Choose a short kebab-case slug for the topic. Create `outputs/articles/<slug>/`.
2. Write this brief, with the resolved topic, to `<workspace>/00-goal.md`.
3. Arm the quality gates:
   ```bash
   echo "outputs/articles/<slug>" > outputs/articles/.active-run
   ```
   The hooks are inert until this flag exists. **Remove it when the run ends, including
   if you abandon the run.**

Use these filenames so the gates can find your work:

| File | Contents |
|---|---|
| `01-research.md` | the research dossier |
| `02-draft.md` | the first full draft |
| `03-edited.md` | the publication-ready revision |
| `03-editorial-memo.md` | what the editor changed and why |
| `04-article.md` | deliverable 1 |
| `04-article.docx` | deliverable 2 |

## Quality bar

Pass these on to the specialists you dispatch — they cannot see this brief:

- **Evidence** — at least 5 named companies with quantified outcomes, from Tier 1–2
  sources published within 24 months. Every claim carries a link. No invented numbers, no
  unsourced assertions. Single-source claims flagged as such.
- **Article** — 2,000–2,500 words, one clear big idea an executive could act on Monday,
  every factual claim traceable to the dossier. Frontmatter (`title`, `subtitle`,
  `author: James Gray`, `date`), a `## Sources` section, and an `## Assumptions` section
  recording judgment calls.
- **Editing** — the edited file must be the finished article with changes already
  applied, not a critique. Commentary goes in the memo. Citations must survive editing.

## The human gate — before publishing

**A human must approve the article before it is published.** This is enforced by the
harness, not left to your judgment: a `PreToolUse` hook blocks the publishing agent from
being dispatched at all until an approval marker exists. If you try to publish first, you
will be stopped and told to come back here.

When the article is ready for a decision:

1. Use `AskUserQuestion` to ask the human whether to publish. Show them, in the question
   or immediately before it:
   - the three or four most significant editorial changes
   - the article's title and opening paragraph
   - the full paths to the edited draft and the memo, so they can open them
2. **If they approve**, record it, then dispatch the publisher:
   ```bash
   echo "approved by human at $(date -u '+%Y-%m-%dT%H:%M:%SZ')" > <workspace>/APPROVED
   ```
3. **If they decline**, capture their notes, send the article back for revision, and ask
   again. Maximum two revision rounds, then stop and report where things stand. Never
   create the approval marker on the human's behalf, and never publish without it.

## Closing out

1. Confirm both deliverables exist and report their paths, the word count, and the page
   count.
2. Remove the activation flag: `rm outputs/articles/.active-run`
3. Show the human `<workspace>/run-log.md` — the gates' audit trail of which stages
   passed and when.

## If a gate blocks a subagent

The gate tells that agent exactly what to fix, and it will retry. Report the block to the
human rather than working around it, and never satisfy a gate by doing the agent's work
yourself.
