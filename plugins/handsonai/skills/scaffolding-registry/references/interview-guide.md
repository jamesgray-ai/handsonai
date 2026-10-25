# Scaffolding Interview Guide

Six phases (0–5), run in order. Keep each phase brief: sources shorten
them, and the student never hears how long anything takes.

**Pacing rule:** If a phase stalls, write what the student has confirmed,
mark the gap in the close-out summary, and move on — missing nodes are
homework; unconfirmed or fictional nodes are never a fallback.

**Question blocks.** Questions the student hears are marked **Ask:**. A
question with a *Why*, *Example*, and *Not sure?* gets all three in the same
message: the *Why* always, the *Example* and *Not sure?* unless the student
said "skip the explanations". If the student works in the field an
*Example* comes from, skip that *Example* and go straight to *Not sure?*.
One question per message. **Exact wording:** say each definition, each
**Ask:** line, and each *Why*, *Example*, and *Not sure?* line exactly as
written here (or as the persona wording in `personas.md` gives it) — don't
paraphrase them and don't add your own reassurance. The outline is exact
too. Only the opening and playbacks may be put in your own words, as long as
every part is there. When a question opens with a draft built from the
student's own source or earlier answers, leave out its *Example* — the draft
already shows the shape; the *Example* is for the blank-page path.
**Persona wording** (`personas.md`) works in two ways, on every path:
(1) its definitions and its name and description questions replace the
guide's; its other questions replace the guide's blank-page question only —
when a draft is on screen, ask the guide's question about the draft;
(2) its nouns replace the guide's nouns everywhere, including draft
questions, playback labels, and *Why* / *Not sure?* lines — for example
"team" and "services" for a professional, "areas", "routines", and "roles"
for personal life (the list is in `personas.md` § Nouns). Apart from those
nouns and the few words around them that grammar needs, the wording stays exact.
Wherever a phase says **Example to show**, describe that example node in plain words (its name, what it covers, who owns it); never paste the file.

**The opening (first message, before anything else but the storage
question):** when the storage question (N-F1, or N-F12 on Claude desktop) is
needed, it comes first, as SKILL.md's *Where the files live* says, and the
opening follows the student's answer. Otherwise the first thing the student
hears is this opening — nothing before it about refreshing, maintenance,
checks, or what the folder is missing.

> "This sets up your **registry**: a structured record of your business — what you offer, how it's organized, and the processes that deliver it. Every step of the framework uses it: Analyze walks your processes to find where AI can help, and each workflow you build is recorded here. By the end you'll have a `registry` folder describing your business, its lines of business, who does the work, and your key processes. It runs in four parts: (1) your business, (2) how it's organized, (3) who does the work, and (4) the processes that deliver it. I'll draft from anything you already have, like your website, and you confirm or correct. Stopping early is safe — progress is saved."
>
> "I'll explain each question as I ask it, and 'not sure' is always a fine answer. If you've done this before, say 'skip the explanations'."

Leave out "Stopping early is safe — progress is saved." on print-to-save,
where a new chat can't read the files.

In the same first message, confirm where the files go in one line (N-F3):
model wording carrying the promise clause "I'll read and save your files in
[location]." — locally the workspace (Claude Code, Codex) or the framework
folder the student added (Claude desktop); on the web and in Cowork, the
`Framework` folder in their drive. On the web and in Cowork, add: "When
[platform] asks to save to your drive here, choose Always allow for this
chat; I'll only save inside your framework folder." (in Cowork, [platform] is
"Cowork"). On Claude Code, add: "When Claude Code asks before I save a file,
you can allow edits for this session; I'll only change the files this step
needs." On Codex, add: "When Codex asks before I save a file, you can allow
it for this session; I'll only change the files this step needs." On
print-to-save, say N-F6 in its place (below).

**The outline (right after the persona answer),** in that persona's words
from `personas.md` § Outline wording — the founder form. Show it as this
nested list, never as an arrow chain (functions don't sit inside lines of
business; they own processes across all of them):

> "Here's the map of your business we'll build, top to bottom:
> - **Business** — the whole of what you run
>   - **Lines of business** — what you offer
>     - **Processes** — how each line gets delivered
> - **Functions** — who does the work. Each process is owned by one function, and a function can own processes in any line of business.
>
> Workflows come later, when Analyze finds them inside your processes."
---

## Phase 0 — Home and sources

**First, detect — don't ask.** Where the files go was settled before the
opening (SKILL.md, *Where the files live*):

- **Locally (Claude Code, Codex, Claude desktop with a folder added):** the
  registry goes at `registry/` in the workspace, or inside the framework
  folder the student added. Don't ask the student to approve the path.
- **On the web and in Cowork:** the registry goes in `Framework/registry/`
  in the student's drive, written through the connection.
- **No files and no connection that can save → print-to-save.** Say N-F6
  once, up front: "I can't save files here, so I'll give you the files to
  save as we go. Keep them together in one folder, and paste or attach them
  when you start the next step." Then, on **every** file, give its location
  inside that folder (`registry/…`) and remind them to save it as plain
  `.md`. Never say "I've created" for a file you only gave. (A file the
  student would have to download does not count as saved.)

**Follow-up (print-to-save only — otherwise, look instead of asking):**
- "Do you already have the empty registry skeleton — from the template
  repository or its Download ZIP?" If yes, do not give again or recreate
  `SCHEMA.md`, `index.md`, `log.md`, or the typed `index.md` stubs.

**Then, in this order:**

1. **Persona.**
   **Ask:** "Who is this registry for — a business you own, a company or unit you lead, your role inside an organization, or your personal life?"
   - *Why:* your answer sets the words I use for every question that follows, and how Analyze looks at your work later.
   - *Example:* a hospital operations manager might say "my role inside an organization — the patient scheduling team I run."
   - *Not sure?* Pick the one you'd use to describe your work to a stranger. If it turns out not to fit, just tell me and I'll switch.

   Open `personas.md` and use that persona's openings for Phases 1–4. For
   the personal persona, add its privacy line now.
2. **Scan (wherever you can read the files).** Look for `knowledge/`,
   `sops/`, `process-guides/`, `CLAUDE.md` or `AGENTS.md`, a prior
   opportunity report (`framework/ai-opportunity-report*.md` locally,
   `ai-opportunity-report*.md` in the framework folder on a drive), and any
   loose documents sitting in the folder (a pasted org chart, a services
   page). If you found something
   you will draft from, say so in one plain sentence ("I found your services
   page and will draft from it"). If you found nothing, say nothing — never
   list folders that aren't there. Never write to `knowledge/`.
3. **Documents.**
   **Ask:** "Do you have anything that already describes [the business / your team / the areas you want to run] — [the persona's examples from `personas.md` § Documents to ask for]? Paste it, upload it, or give me a link, and I'll draft from it for you to confirm."
   - *Why:* drafting from something you already have is faster than starting from a blank page, and you only have to correct it.
   - *Example:* a property manager might share the company website's "Services" page and a one-page team list.
   - *Not sure?* A website link is enough. If you have nothing, we'll build it together from your answers.

   Map each source with `intake-sources.md`.
   An answer the student gives here in words ("the areas are household,
   money, and the kids") counts as a source for the phase it covers: open
   that phase with the draft, still in phase order.
4. **The rule, once.** "I'll propose, you confirm. Nothing about your
   business gets saved until you confirm it."

**Then write the skeleton** — after the four steps above and before Phase 1.

**Example to show:** none — this phase is about the student's environment,
not the registry's content.

**What to write:** nothing until the steps above are done. Then, before
Phase 1, create `registry/` + `SCHEMA.md` + `index.md` +
`log.md` + the six typed directories with stub `index.md` files (each stub
is its heading, a blank line, and `_No entries yet — your AI assistant fills this index as nodes are added._` — the exact empty body compose
writes), unless they already exist. The root `index.md` and `log.md` have
fixed bodies — lint requires the root index to link every typed index and
to carry the two GENERATED inventory blocks compose fills. Write them
exactly as the template repository ships them:

```markdown
---
okf_version: "0.2"
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

Setup decisions, schema changes, the dashboard's Claude Artifact link, and one line per workflow event (a big change and its reason, go-live, re-checks) — routine regeneration is not logged.
```

On print-to-save with no skeleton yet, give those same files first, in that
order. If the student
asks "where's the template repo?", the URL is
`https://github.com/jamesgray-ai/ai-registry-template` — it ships this same
skeleton plus a GitHub Action that checks the registry on every save, and is optional.

**Fast path:** if the student already has a full `registry/` bundle from a
prior scaffolding run, skip straight to gap-filling — re-run only the phases
that produced missing or incomplete nodes.

---

## Phase 1 — Business

**Signpost:** "Part 1 of 4 — Your business."

**If a Phase 0 source covers this phase:** play the draft back in plain
words, labeled — never the file:

> **Name:** … · **What it does:** … · **Website:** … (add **Goals for this year:** … only when the source actually states goals — never draft goals from a website)

then ask the questions below one at a time, starting from the draft. Write
only what the student confirms.

**Ask (name):** "What do you call your business day to day — the name you'd want at the top of your dashboard?" (persona wording from `personas.md`)
- *Why:* this name labels everything the registry records about your business.
- *Example:* a family-run garden center might say "Hillside Gardens", not the legal entity "Hillside Horticultural Holdings Ltd".
- *Not sure?* Use the name your customers know you by. When a source offers several (brand, personal name, legal entity), list them and suggest the customer-facing one.

**Ask (what it does):** "Here's one sentence on what it does: '[draft]'. Does that sound like you?" (Ask "What does it do, in one sentence?" when there's no source.)
- *Why:* this sentence sits at the top of your dashboard and tells anyone reading it what the business is for.

**Ask (goals for this year):** "What are the two or three goals that matter most for the business this year?"
- *Why:* Analyze uses these to suggest where to look first and to tie each workflow it finds to a goal, so you won't be asked for them again.
- *Example:* a dental practice might say "fill the new evening clinic" and "cut no-shows by half".
- *Not sure?* Think about what would make this a good year for the business. Write that down in your own words; it doesn't need to be a target or a number.

Record what the student says as separate goals; if one answer could be two
goals or three, ask. Then play back the complete entry once, before writing
anything:

> **Name:** … · **What it does:** … · **Website:** … · **Goals for this year:** (each goal)
> "Shall I save your business entry like this?"

Write the Business node only on yes. The same applies to every phase:
confirm the whole entry (or list) once, then save it. When the student
changes something (merges two lines, renames a process, answers a status
question), play back the updated entry or list once more and save on yes —
never save an edit straight from the answer. Set `status` to `active` without asking
unless the student described something not yet launched or winding down.
Use the website from the source as `url`; ask for one only when there's no
source.

**Example to show:** the Business node from `example-registry.md`
(`registry/businesses/brightwork-consulting.md`).

**What to write:** one `registry/businesses/<slug>.md` node — required
frontmatter plus `status` and optional `url`, one identity sentence in the
body, a `## Objectives` prose list of those outcomes placed after the
identity sentence and before `# Lines of Business` (omit the block if the
student has none — never invent one), and an empty `# Lines of Business`
list (Phase 2 fills it).

**Fast path:** one business per registry is the default — do not offer
multi-business setup unless the student volunteers that they run more than
one.

---

## Phase 2 — Lines of Business

**Signpost:** "Part 2 of 4 — How it's organized: your lines of business."

**Define it first:** "A **line of business** is something distinct the
business offers — like a product line, a service, or a training
program. Some businesses have one; some have several."

**If a Phase 0 source covers this phase:** draft the lines from it, ordered
by the student's goals, each with a one-line description, and say why you
grouped anything together or left anything out.

**Ask:** "Does this grouping match how you think about the business? Merge, split, rename, or move any of them." (Without a source: "Does the business have distinct lines of business, or is it one thing end to end?" — persona wording from `personas.md`.)
- *Why:* each line becomes a section of your dashboard, and every process you name later sits under one of them.
- *Example:* a veterinary clinic might keep "Pet care" and "Grooming" separate but fold "Retail" into Pet care.
- *Not sure?* Keep my draft. You can reshape it any time by asking.

Don't ask a separate question about the order — the student can move lines
in their answer above. Set each line's `status` to `active` unless a source
suggests it is new or paused; only then ask about that line, before the
final playback:

**Ask:** "Is [line] something you're offering now, or just starting or paused?"
- *Why:* so your map shows what's running today.

**Example to show:** the two LineOfBusiness nodes from `example-registry.md`
(`advisory.md` and `training.md`) — Advisory shows a populated
`# Processes` list, Training shows the allowed-empty
`_No processes captured yet._` form.

**What to write:** one `registry/lines-of-business/<slug>.md` node per line,
each with `status` and a prose sentence, plus an entry in the Business
node's curated `# Lines of Business` list in the order given.

**Fast path (solo consultant / single-line business):** write one default
LOB named after the business itself and move on — don't force an artificial
split.

---

## Phase 3 — Functions

**Signpost:** "Part 3 of 4 — Who does the work: your functions."

**Define it first** (persona wording in `personas.md`; this is the founder
form): "A **function** is a team or department in your
organization — Marketing, Sales, Finance — that owns a kind of work across
every line of business. Your lines of business are *what you offer*; your
functions are *who does the work*. If you work alone, each function is one
of the hats you wear."

**Show the starter set (or the drafted list) as a table** — Function · What
it would own — with the second column filled in from the student's own
business.

**Ask:** "Would you rename, drop, or add any of these? A partner, contractor, or assistant who owns a piece of the work counts too — named by their role, not their name."
- *Why:* every process you name next gets one of these as its owner, so the dashboard shows who is responsible for what.
- *Example:* a small law firm might rename "Product" to "Practice Development" and add "Paralegal Support".
- *Not sure?* Keep the starter set. Any function that ends up owning no process, I'll ask about at the end.

Whatever the student keeps or drops here stands: don't raise a kept
function as a problem later unless it ends up owning no process.

**Starter set (verbatim):** Marketing, Sales, Service Delivery, Operations,
Product, Customer Success, IT/Engineering. Offer it only when no Phase 0
source covers Functions — a drafted list from an org chart replaces it.
Offer it as-is to founders and leaders; reframe as "who you hand work to
and receive it from" for the professional persona; do not offer it to the
personal persona — they name roles or helpers instead, at least one. A
Function is named for the area or role ("Client Delivery", "Partner"),
never for the person; the person, if the student wants them recorded, goes
in `lead:`.

**Example to show:** the Function node from `example-registry.md`
(`registry/functions/service-delivery.md`) — note the empty GENERATED
`# Owns` block written at creation time.

**What to write:** one `registry/functions/<slug>.md` node per function the
student keeps, `lead:` filled in or left empty — an empty value or an
omitted key both read as unstaffed, an insight not an error — and every node written **with** its empty GENERATED
`# Owns` marker block — the reference lints an error on a Function missing
that block ("compose can't fill what doesn't exist").

**Fast path (founder/leader, and only when no source covered Functions):** offer the starter set as-is; most students accept it with one
or two renames rather than building from scratch — then, once Phase 4 has
named the processes, drop the functions that own none (Close checks this).

---

## Phase 4 — Processes

**Signpost:** "Part 4 of 4 — The processes that deliver it."

**Define it first:** "A **process** is a set of related work that delivers
part of a line of business — like enrolling students or delivering a
workshop. Each one sits under one line of business and is owned by one
function. Later, Analyze finds the specific **workflows** inside each
process: the repeatable pieces of work that AI can help with."

**Draft three to five processes per line of business**, ordered yourself
(value-chain order, then the student's goals). Each process sits under
exactly one line; a shared one (a newsletter, invoicing) goes under the line
it serves most — say so in those words, never "under the schema". Play it
back in this layout, which labels each level so a student can't confuse
them: say they're suggestions, give a count line when there are ten or more
processes, keep each description to one short phrase, and put the owner
last. The names below only show the shape — fill every line from the
student's own registry, never reuse these:

> "Here are my suggested processes, drafted from [the source — your website, your org chart, or your answers so far]. You decide what stays." (With ten or more: "14 processes across 4 lines of business.")

```
**Line of business: Cohort Courses**
- **Process:** Cohort Delivery — running live sessions week to week. **Owner:** Service Delivery
- **Process:** Cohort Launch & Enrollment — launch plan, promotion, waitlist, filling seats. **Owner:** Marketing

**Line of business: Corporate Training**
- **Process:** Corporate Lead to Proposal — inquiry, qualification, scoping, proposal. **Owner:** Sales
```

**Ask:** "What would you add, remove, rename, or move? Each line of business only needs its main processes for now."
- *Why:* Analyze looks for work worth improving inside these processes, so anything missing here won't come up.
- *Not sure?* Keep the draft. Analyze adds processes later when it finds work that doesn't fit.

Never ask the student to rank processes — order them yourself; Analyze asks
which matter most before it looks at them. When the student names an owner in
shorthand ("training"), say which function you read it as before writing.
Don't ask for SOPs or guides; set `guide:` only when a Phase 0 document
turned one up.

Then check every function against the confirmed processes. Only if some
truly own none, ask once, naming them:

**Ask:** "[Function] has no process yet. Add one, or drop it for now? You can add it back any time."
- *Why:* every function in your registry should own some of the work, so the dashboard shows who's responsible for what.

Functions have no `status`, so dropping one means deleting the node and its
index line at Close. This is the only time the question is asked.

**Example to show:** the Process node from `example-registry.md`
(`registry/processes/client-delivery.md`).

**What to write:** one `registry/processes/<slug>.md` node per process, each
with a title, a description, required `owner:` (a function slug from Phase
3), optional `guide:`, a `# Workflows` list that starts as
`_No workflows captured yet._` (Analyze replaces it), and an entry added to
its LOB's curated `# Processes` list.

**Fast path:** three to five processes per LOB is enough for the lab —
remind the student that Analyze decides where AI fits and grows this list
later; don't try to be exhaustive here.

---

## Phase 5 — Close

**No new questions.** Don't prompt for a Note. Write one only if the
student volunteered an insight during the interview (a constraint, a lesson
learned) — and ask before saving it.

**Example to show (only when writing a volunteered Note):** the Note node
from `example-registry.md` (`registry/notes/2026-08-status-report-timing.md`).

**What to write:**
- an optional `registry/notes/<slug>.md` node — only if a real insight
  surfaced during the interview, never a manufactured one
- a founding `registry/log.md` entry describing the scaffolding run — say
  in plain words who the registry is for (the Phase 0 persona answer: "set
  up for a business the owner runs" / "for the team the owner works in" /
  "for the owner's personal life"), because `analyze` reads that line to
  infer the lens; the log is not a concept node, so no schema is touched
- directory `index.md` stubs for every typed directory that still has no
  nodes, with the standard empty body (heading, blank line, `_No entries yet — your AI assistant fills this index as nodes are added._`)
- `registry/workflows/index.md` with that same empty body — the directory
  must have an index even when empty, and Analyze replaces the placeholder
  line with its first entry
- every Function owns at least one process: delete any that owns none
  (the node and its index line — Functions have no `status` to retire
  into) or assign it a process the student names — the lint warning `function owns no processes` must not appear on
  a fresh scaffold

Hand off to
`indexing-registry` for the first maintenance pass: lint, generate the Tier
1 `REGISTRY.md`, and **always** generate the Tier 2 dashboard
(`registry-dashboard.html`) — never offer it as an option. On the web the
pass saves through the drive connection. On print-to-save there is no
maintenance hand-off: give the `log.md` entry, every typed `index.md` you
updated, and a complete `REGISTRY.md` composed per `indexing-registry`'s
rules, each with its location, and say the set is complete.

**The close (last message) — files saved (locally or in the drive):**

> "Your registry is set up in [where it's saved: locally the folder's name; in a drive, "your Google Drive, in [framework folder]/registry" or "your OneDrive, in [framework folder]/registry", with the framework folder's own name, Framework unless the leader chose another]. It holds [1 business], [N lines of business], [N functions], and [N processes] — no workflows yet; Analyze adds those."
>
> "Two files give you a view of it. **`registry-dashboard.html`** is your visual dashboard: double-click it to open it in your browser (in a drive, download it first), and click any line of business or process to see its details. **`REGISTRY.md`** is a one-page text summary of the same registry; it's refreshed after every step, and it's what your AI reads to catch up on your business."
>
> "You can reshape this any time — rename, merge, or move things — just ask, for example 'move [one of their processes] under [another of their lines of business]'." (Fill the example from the student's own registry.)
>
> "Next is Analyze. With your permission, it starts from what your AI already knows about your work, then looks for opportunities to create more value in your processes and adds every workflow it finds to your backlog. You can look at one process or all of them. When you're ready, say 'run the analyze skill. My files are in [location].' (in Claude Code, you can also type `/analyze` and pick it from the list). Want to run it now?"

That last paragraph is N-A7: say it exactly. [location] is the framework
folder, as Analyze's start phrase names it: "Google Drive, in Framework" or
"OneDrive, in Framework" in a drive (with the folder's own name when the
leader chose another folder at the storage question); on Claude desktop, the
folder's own name (such as "Framework"); on Claude Code and Codex,
"framework". Leave out the
`/analyze` clause anywhere but Claude Code.

**The close — print-to-save:** the same four parts, with two changes.
Say where the files go: "Save each file I gave you into your `registry`
folder, at the location shown above it." And for the dashboard, which can't
be given usefully as text: "Your visual dashboard is created as soon as your files
are in a folder I can save to. Then say 'generate my visual dashboard'."

Say nothing about lint, checks, or GENERATED blocks. The close ends on the
Analyze question. Once the student answers it, make these offers one per
message, each answered before the next, and only where it applies; then
act on the Analyze answer:

- **On Claude:** "Want your dashboard as a **Claude Artifact**? It's a private page you can open from Claude any time, and share with a link if you want to." On print-to-save on Claude, this is the way to see the dashboard now, so offer it in place of "created as soon as your files are in a folder I can save to". This close is the only place the Artifact is offered; `indexing-registry` doesn't repeat it here. On yes, publish it and append a `registry/log.md` entry, `Dashboard Artifact: <link>`, so every later step can update the same page in any conversation. On print-to-save, give that one line and say: "Add this line to the end of your `registry/log.md`, so later steps can keep this page up to date."
- **Only when the folder is a git repository** — locally, with a shell, `git rev-parse --show-toplevel` returns the workspace folder; never ask on the web or in a connected drive: "Your folder keeps a history of its changes (it's a Git repository). Want me to save this point in that history, so you can come back to it later? It stays on your computer — nothing is shared." On yes, commit locally; don't push as part of this offer (a student who asks to push or back up to GitHub gets that separately).

After the offers, on "now" to Analyze, invoke the `analyze` skill.

**Fast path:** if no insight surfaced, skip the Note entirely and don't
mention it — an absent Note is not a gap to flag; a forced one is worse than
none.
