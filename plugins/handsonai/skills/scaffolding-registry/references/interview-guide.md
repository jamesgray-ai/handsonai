# Scaffolding Interview Guide

Four phases (0–3), run in order. The student hears an opening with one open
question, one card to confirm, one message per line of business for its
processes, and the close. Sources shorten it further, and the student never
hears how long anything takes.

**Pacing rule:** if the student stops or can't answer, write what they have
confirmed, mark the gap in the close-out summary, and move on: missing pages
are homework; unconfirmed or fictional ones are never a fallback.

**Question blocks.** Questions the student hears are marked **Ask:**. Each
has a one-line *Why*, said with the question every time. An *Example* or
*Not sure?* line, where a question has one, is said only when the student
says "not sure", asks what is meant, or gives an answer that shows the
question wasn't clear. If the student says "skip the explanations", drop the
*Why* too. Save confirmations (N-SR6, "Shall I save this?", "Shall I save these?") carry no *Why*: the card or list above them is the reason. One question per message. **Exact wording:** say each definition,
each **Ask:** line and each *Why*, *Example* and *Not sure?* line exactly as
written here (or as `personas.md` gives it), with only its [brackets] filled;
don't paraphrase them and don't add your own reassurance. Only playbacks and
the card's contents are in your own words, as long as every part is there.
**Persona nouns** (`personas.md` § Nouns) replace the guide's nouns
everywhere once the persona is known: in the card, the process messages, the
*Why* lines and the close. Apart from those nouns and the few words around
them that grammar needs, the wording stays exact.

**The example business** (`example-registry.md`, Brightwork) is shown only
when the student says "not sure", asks for an example, or asks what a page
looks like: describe the page in plain words (its name, what it covers, who
owns it), as formatted text in the chat; never paste the file, never use a
code block, and never copy it into the student's registry.

---

## Phase 0 — Opening and the first question

**Where the files go was settled before this** (SKILL.md, *Where the files
live*): the storage question (N-F1, N-F12 or N-F16), when it's needed, comes
first, and the opening follows the student's answer. With a registry already
there, N-SR2 comes first instead (SKILL.md, *Before scaffolding*). Detect,
don't ask, how files are saved:

- **Locally (Claude Code, Codex, Claude desktop with a folder selected):** the
  registry goes at `registry/` in the workspace, or inside the working folder
  the student selected. Don't ask the student to approve the path.
- **On the web and in Cowork:** the registry goes in `registry/` in the
  working folder in the student's drive, written through the connection.
- **No files and no connection that can save (Gemini, or on the web with no
  drive that can save):** N-F16, and wait; nothing is written until a place
  that can save is added (`references/saving.md`, rule 5).

**Scan first, silently (wherever you can read the files).** Before the
opening, look for `knowledge/`, `sops/`, `process-guides/`, `CLAUDE.md` or
`AGENTS.md`, a prior opportunity report (`framework/ai-opportunity-report*.md`
in the working folder), and any loose documents in the folder (a pasted org
chart, a services page). Map what you find with `intake-sources.md`. Never
write to `knowledge/`. Never list folders that aren't there.

**The opening (the first message after the storage question).** Nothing
before it about refreshing, maintenance, checks, or what the folder is
missing. It is N-SR4, then N-SR1, then the save line, then the first
question, all in one message:

> "This sets up your registry: a map of what your business offers and the processes that deliver it. Every step of the framework builds on it. I'll draft it from what you tell me, and nothing is saved until you confirm it. Stopping early is safe. Progress is saved."

Then confirm where the files go in one line (N-F3): model wording carrying
the promise clause "I'll read and save your files in [location]." — locally
the workspace (Claude Code, Codex) or the working folder the student selected
(Claude desktop); on the web and in Cowork, the working folder in their drive
(`ai-workspace` unless they keep another). On the web and in Cowork, add:
"When [platform] asks to save to your drive here, choose Always allow for
this chat; I'll only read and save inside your working folder." (in Cowork,
[platform] is "Cowork"). On Claude Code, add: "When Claude Code asks before I
save a file, you can allow edits for this session; I'll only change the files
this step needs." On Codex, add: "When Codex asks before I save a file, you
can allow it for this session; I'll only change the files this step needs."

Then the first question, N-SR5:

**Ask (blank page):** "To start, tell me about the work this registry is for, whether that's a business you own, a company or team you lead or work in, or your personal life. In a few sentences: what it offers, who does the work (just you, or which roles), and the two or three goals that matter most this year. Or paste your website's About or Services text, and I'll draft from that."
- *Why:* I'll draft your whole map from this, so you only have to correct it.
- *Not sure?* Say it the way you'd tell a new client. I'll ask about anything I need.

**When the scan found a source** that covers part of this, open with it
instead, in your own words: "From your [source], I can see [what it covers,
in one short sentence]." Then ask the blank-page question for only what the
source lacks (for example, only who does the work and the goals), keeping the
*Why*. Never draft goals from a website or a services page.

**A link you can't open:** say so in one line and ask them to paste the key
text or answer in their own words; never propose changing the environment,
network, permissions or credentials.

**Read the answer for the persona** (`personas.md` § Working out who it's
for). When the signals are clear, carry the persona into the card without
asking. When they conflict or are missing, ask one follow-up:

**Ask (only when unclear):** "Is this registry for a business you own, a whole company or division you run, a team you lead or work in inside a larger organization, or your personal life?"
- *Why:* it sets the words I use from here on, and how Analyze looks at your work later.

For the personal-life persona, say its privacy line (`personas.md`) before
the card, so it comes before anything is saved.

**Follow up only on gaps,** one question per message, in this order, and
only for what the answer left out:

**Ask (what it offers, only if missing):** "What does [the business] offer, in a sentence or two?"
- *Why:* each thing you offer becomes a section of your dashboard, and every process sits under one.

**Ask (goals, only if missing):** "What are the two or three goals that matter most for [the business] this year?"
- *Why:* Analyze uses these to suggest where to look first and to tie each workflow it finds to a goal, so you won't be asked for them again.
- *Example:* a dental practice might say "fill the new evening clinic" and "cut no-shows by half".
- *Not sure?* Think about what would make this a good year for the business. Write that down in your own words; it doesn't need to be a target or a number.

Goals are asked at most once. Record what the student says as separate
goals; if one answer could be two goals or three, ask. **Never invent goals,**
even when asked to draft every part from what you know: with none given,
record none and say N-SR3, "Your goals for this year aren't recorded yet; tell me them any time."

Who does the work, if missing, isn't asked here: draft the owners in Phase 2
from what you know, and the student corrects them there.

**Then write the skeleton** (it holds nothing about the business yet, so it
needs no confirmation): `registry/` + `SCHEMA.md` + `index.md` + `log.md` +
the six typed directories with stub `index.md` files (each stub is its
heading, a blank line, and `_No entries yet — your AI assistant fills this index as nodes are added._` — the exact empty body compose writes),
unless they already exist. The root
`index.md` and `log.md` have fixed bodies — lint requires the root index to
link every typed index and to carry the two GENERATED inventory blocks
compose fills. Write them exactly as the template repository ships them:

```markdown
---
okf_version: "0.3"
---
# AI Registry

Your operations knowledge bundle: how your business runs. See [SCHEMA](/SCHEMA.md) for types and rules.
The dashboard view is the generated root `REGISTRY.md`.

## Concepts

- [Businesses](/businesses/index.md) — the traversal root: identity + curated line-of-business order
- [Lines of Business](/lines-of-business/index.md) — each orders its processes in value-chain order
- [Functions](/functions/index.md) — cross-cutting ownership areas processes map into
- [Processes](/processes/index.md) — business processes grouping workflows
- [Workflows](/workflows/index.md) — the hub: one node per business workflow
- [Notes](/notes/index.md) — synthesized operational insights

<!-- GENERATED:skills -->
## Skills inventory (0)
<!-- /GENERATED -->

<!-- GENERATED:agents -->
## Agents inventory (0)
<!-- /GENERATED -->
```

```markdown
# Registry Log

Setup decisions, schema changes, the dashboard's Claude Artifact link, and one entry per workflow event (a big change and its reason, go-live, re-checks), grouped by date with the newest first — routine regeneration is not logged.
```

If the student asks "where's the template repo?", the URL is
`https://github.com/jamesgray-ai/ai-registry-template` — it ships this same
skeleton plus a GitHub Action that checks the registry on every save, and is
optional. Give this only when asked; never offer it, and never ask the
student to choose between it and the skill's own check.

---

## Phase 1 — The card: your business and what it offers

One message: the card, then N-SR6. Show it as labeled plain text, never as
the file, in the persona's nouns:

> **For:** [a business you own / a company or unit you lead / your team, which you lead / a team you work in / your personal life] · **Name:** … · **What it does:** [one sentence] · **Website:** … (only when given) · **Goals for this year:** (each goal, or "none yet")
>
> **Lines of business** (each one is something distinct you offer), in this order:
> - **[Line]** — [one-line description]
> - …
>
> "Shall I save this? Change anything first."

How to draft the card:
- **Name:** the name customers know the business by. When the answer or a
  source gives several (brand, personal name, legal entity), use the
  customer-facing one and show the others in brackets so the student can
  pick.
- **What it does:** one sentence, drafted from the answer.
- **Lines of business:** one per distinct offering, each with a one-line
  description, ordered yourself by the student's goals. A shared offering (a
  newsletter) goes under the line it serves most. Don't ask a separate
  ordering question: the student can move lines in their answer. Decide the
  number of lines by how many distinct things the business offers, never by
  how many people do the work: a solo consultant with three offerings gets
  three lines. **One offering:** one line named after the business, with no
  split forced.
- **State:** set `state: active` yourself for the business and each line; ask only
  when the student described something not yet launched, paused or winding
  down: "Is [line] something you're offering now, or just starting or paused?"
  (*Why:* so your map shows what's running today.)

When the student changes anything, play back only what changed, then
"Shall I save this?" again; never save an edit straight from the answer.
**Save on yes:** the Business page and one page per line of business, with
their index entries.

---

## Phase 2 — Processes and their owners, one line of business at a time

One message per line of business, in the card's order. **With four or more
lines, show two lines per message** (Lines 1 and 2 of 6), so a big business
gets no more than three or four of these messages; never more than ten
processes in one message.

**Draft three to five processes per line** (fewer when one person does all of
a line's work as one piece of work: never split one person's single piece of
work in two to reach three), ordered yourself (value-chain
order, then the student's goals). Each sits under exactly one line; a shared
one goes under the line it serves most — say so in those words, never "under
the schema". Map how the business delivers, never where AI might help:
Analyze decides that later. Each description is one short phrase, and the
owner comes last.

**Draft each owner** from what the student said about who does the work
(`personas.md` § Owners):
- **Working alone:** three or four broad hats, named for the area of work
  (for example Sales, Delivery, Marketing, Operations). Use only the hats that
  own a process.
- **A team or company:** each role or team the student named becomes the
  owner of the work it does ("two analysts" → Analytics; "a deal desk lead"
  → Deal Desk), plus the groups the team hands work to or receives it from
  (Sales, Finance). A process no named role does goes to the named role whose
  work is closest; use the area of work only when none is close. Never merge the named
  roles into one owner for the whole team. Named for the area or role, never
  the person.
- Reuse the same owner names across lines, so one owner can own processes in
  several lines.

**The first of these messages,** N-SR7, in the founder form (persona nouns
elsewhere), with the list shown as a formatted list in the chat, never in a
code block:

> "Line 1 of [N]: [line]. A **process** is a set of related work that delivers part of a line of business, and its **owner** is who does it (for you, the hat you wear). Here's what I'd suggest, in the order the work flows:"
>
> - **Process:** [name] — [short phrase]. **Owner:** [owner]
> - …
>
> "Anything to add, remove, rename, or change the owner?"
> - *Why:* Analyze looks for work worth improving inside these processes, so anything missing here won't come up.

With two lines in one message (four or more lines of business), the first
message is N-SR7's two-line form, with a labeled list for each line:

> "Lines 1 and 2 of [N]: [line] and [line]. A **process** is a set of related work that delivers part of a line of business, and its **owner** is who does it (for you, the hat you wear). Here's what I'd suggest for each, in the order the work flows:"

and each later one "Lines [k] and [k+1] of [N]: [line] and [line]. Here's
what I'd suggest for each, in the order the work flows:" (with an odd number
of lines, the last message has one). Say "(for you, the hat you wear)" only to
someone working alone; for a team, leave it out. **Each later message** is the shorter form: "Line [k] of [N]:
[line]. Here's what I'd suggest, in the order the work flows:" then the list,
then "Anything to add, remove, rename, or change the owner?" with the *Why*.

- *Not sure?* (on "not sure" only) Keep the draft. Analyze adds processes later when it finds work that doesn't fit.

Never ask the student to rank processes. When the student names an owner in
shorthand ("training"), say which owner you read it as. Don't ask for SOPs or
guides; set `guide:` only when a source turned one up. When the student
changes something, play back only what changed, then "Shall I save these?";
save on yes.

**Save each line on yes:** one `registry/processes/<slug>.md` per process
(title, description, required `owner:` naming a Function slug, optional
`guide:`, a `# Workflows` list starting `_No workflows captured yet._`), an
entry in its line's curated `# Processes` list, and the index entries. **The
functions are the owners:** the first time an owner is used, write its
Function page in the same save (named for the area or role, one sentence of
what it takes care of, `lead:` only if the student asked for a person to be
recorded, and its empty GENERATED `# Owns` block), with its index entry. A
Function is never written before a process uses it, so none owns nothing and
there is no question about unused ones. An owner the student renames or
removes before saving is never written.

---

## Phase 3 — Close

**No new questions,** except the close's one, below. A Note is never its own
question and is never prompted for: when the student volunteers an insight (a
constraint, a lesson learned), add one line to the next confirmation ("I'll
also save your note that [insight].") and save it with that yes; volunteered
after the last confirmation, leave it out and say nothing.

**What to write:**
- a founding `registry/log.md` entry describing the setup run, below the
  log's description under today's `## YYYY-MM-DD` heading, as one bullet
  starting `- **Registry scaffolded** — `, saying who the
  registry is for in exactly one of the fixed forms in `personas.md` (*The
  founding log line*), such as "set up for a business the owner runs alone",
  because `analyze` and `deconstruct` read that line (the lens, and
  personal-life wording); never reword it. For a team, it ends with
  "; the team's own functions: [names]" (`personas.md`)
- directory `index.md` stubs for every typed directory that still has no
  pages, with the standard empty body, including `registry/workflows/index.md`
  (Analyze replaces the placeholder line with its first entry)

Then the check and the views (SKILL.md, *Close*).

Before the check, if you say anything, say only this, word for word: "Now
I'll check your registry and build your dashboard." Never a longer or more
technical version: that sentence or nothing. Say nothing about the check when
it passes, or about GENERATED blocks. Call the files pages, never nodes, and
never say "maintenance pass" or name lint, compose, scripts, `tools/`, GitHub
Actions or the template repository unless the student asks.

**The close (last message):**

> "Your registry is set up in [where it's saved: on Claude Code and Codex, "this project's folder"; on Claude desktop, the folder's name; in a drive, "your Google Drive, in [working folder]/registry" or "your OneDrive, in [working folder]/registry", with the storage service's own name, with the working folder's own name, ai-workspace unless the leader chose another]. It holds your [business], [N lines of business] and [N processes], each with its owner — no workflows yet; Analyze adds those."
>
> [The dashboard, for this platform — below.]
>
> "You can reshape this any time — rename, merge, or move things — just ask, for example 'move [one of their processes] under [another of their lines of business]'." (Fill the example from the student's own registry; with one line of business, use a rename instead.)
>
> "Next is Analyze. With your permission, it looks through what you've given your AI and what it already knows about your work, asks you a few questions, and aims to save 3 to 5 workflows worth building to your backlog. When you're ready, say 'run the analyze skill. My files are in [location].'"

**The dashboard paragraph, by platform.** The close names the dashboard only,
never `REGISTRY.md` (unless the student asks what it is: `indexing-registry`,
*Telling the leader about `REGISTRY.md`*).
- **Claude Code and Codex (a shell that can open files):** "Your visual dashboard is ready: click any line of business or process in it to see its details." Then N-SR8: "Say 'open my dashboard' and I'll open it in your browser[, or 'make it a Claude page' for a private link you can open any time]." Include the bracketed clause only where this session can publish a Claude Artifact. On "open my dashboard", open `registry-dashboard.html` with the system's own command (`open` on macOS, `start ""` on Windows, `xdg-open` on Linux); once it's open, say "It's open in your browser."; if that fails, give the file's full path in one line and say to double-click it. On "make it a Claude page", publish it as the Claude Artifact offer below does on yes.
- **Claude desktop:** "Your visual dashboard is `registry-dashboard.html`, in your [folder] folder: double-click it to open it in your browser, and click any line of business or process to see its details."
- **In a drive:** "Your visual dashboard is `registry-dashboard.html`, in your [storage service], in [working folder]: download it, then double-click it to open it in your browser, and click any line of business or process to see its details."
- **In a cloud session:** it's in the repository on GitHub to download; never "double-click it". The Claude Artifact offer then leads, as the one question.

That last paragraph of the close is N-A7: say it exactly, and say Analyze's
start phrase word for word ("run the analyze skill", never "Run Analyze").
[location] is the working folder, as Analyze's start phrase names it: "Google
Drive, in ai-workspace" or "OneDrive, in ai-workspace" in a drive (the
storage service by its own name; the folder's own name when the leader chose
another folder at the storage question); on Claude desktop, the folder's own
name (such as "ai-workspace"). On Claude Code and Codex the workspace is the
working folder, so the phrase carries no location. On Claude Code, say N-A7's
Claude Code form, "Next is Analyze. With your permission, it looks through what you've given your AI and what it already knows about your work, asks you a few questions, and aims to save 3 to 5 workflows worth building to your backlog. When you're ready, say 'run the analyze skill.' (in Claude Code, you can also type `/analyze` and pick it from the list)". On Codex (and the Work tab in a local folder, treated
as Codex), say its Codex form, which ends at "'run the analyze skill.'": "Next is Analyze. With your permission, it looks through what you've given your AI and what it already knows about your work, asks you a few questions, and aims to save 3 to 5 workflows worth building to your backlog. When you're ready, say 'run the analyze skill.'" Leave out the
`/analyze` clause anywhere but Claude Code.

**In a cloud session** (*Where the files live*, in `SKILL.md`): commit and
push the registry's files yourself first, name the repository, never a path
on the machine ("Your registry is set up in your [repository] repository on
GitHub"), and say N-F18 where the branch isn't the default.

**One question at most.** N-A7 gives Analyze's start phrase as the next step;
it asks nothing. Then the close's one question, where it applies, as its last
line:

- **On Claude on the web, Claude desktop, and in a cloud session:** "Want your dashboard as a **Claude Artifact**? It's a private page you can open from Claude any time, and share with a link if you want to." On Claude Code (not a cloud session), N-SR8's bracketed clause makes this offer instead, as a choice rather than a question. This close is the only place the Artifact is offered; `indexing-registry` doesn't repeat it here. On yes, publish it and add a `registry/log.md` entry, `- Dashboard Artifact: <link>`, at the end of today's heading, so every later step can update the same page in any conversation.
- **Elsewhere (Codex, or Claude Code where no Claude page can be published), only when the folder is a git repository** — locally, with a shell, `git rev-parse --show-toplevel` returns the workspace folder; never on the web or in a connected drive: "Your folder keeps a history of its changes (it's a Git repository). Want me to save this point in that history, so you can come back to it later? It stays on your computer — nothing is shared." On yes, commit locally; don't push as part of this offer (a student who asks to push or back up to GitHub gets that separately).

With neither, the close ends on N-A7. When the leader then says Analyze's
start phrase, or asks to run it here, invoke the `analyze` skill.
