# Scaffolding Interview Guide

Six phases (0–5), about 25 minutes total. Run them in order. Each phase has a timebox —
treat it as a budget, not a target to fill.

**Pacing rule:** If a phase overruns its box, write what you have, mark the
gap in the close-out summary, and move on — missing nodes are homework;
fictional nodes are never a fallback.

**Question blocks.** Questions the student hears are marked **Ask:**. A
question with a *Why*, *Example*, and *Not sure?* gets all three in the same
message: the *Why* always, the *Example* and *Not sure?* unless the student
said "skip the explanations". If the student works in the field an
*Example* comes from, skip that *Example* and go straight to *Not sure?*.
One question per message. Wherever a phase says **Example to show**, describe that example node in plain words (its name, what it covers, who owns it); never paste the file.

**The opening (first message, before anything else):**

> "This step sets up your **registry**: a structured record of your business — what you offer, how it's organized, and the processes that deliver it. Every later step uses it: Analyze walks your processes to find where AI can help, and each workflow you build is recorded here. By the end you'll have a `registry` folder describing your business, its lines of business, who does the work, and your key processes. It takes about 25 minutes, in four parts: (1) your business, (2) how it's organized, (3) who does the work, and (4) the processes that deliver it. I'll draft from anything you already have, like your website, and you confirm or correct. Stopping early is safe — progress is saved."
>
> "I'll explain each question as I ask it, and 'not sure' is always a fine answer. If you've done this before, say 'skip the explanations'."

In the same first message, add one sentence on where the files go: in write mode, "I'll save it in
`<folder name>`." In print-and-save mode, the print-and-save line below.

**The outline (right after the persona answer),** in that persona's words
from `personas.md` § Outline wording — the founder form:

> "Here's the outline we'll fill in, top to bottom: **Business** → **Lines of business** (what you offer) → **Functions** (who does the work) → **Processes** (how each line gets delivered). Workflows come later, when Analyze finds them inside your processes."
---

## Phase 0 — Home and sources (4 min)

**First, detect — don't ask.** Can you create and edit files in the folder
the student has open? (A file the student would have to download does not count — that is print-and-save mode.)

- **Yes → write mode.** The registry goes at the root of that folder. It
  does not matter whether the folder is local, a synced cloud-drive folder,
  or a Git repository — the bundle is plain Markdown with relative links.
  State it in one sentence: "I'll save your registry in `<folder name>`."
  Don't ask the student to approve the path.
- **No → print-and-save mode.** Say once, up front: "I can't save files
  here, so for each file I'll print its full contents and exactly where to
  save it. Where will you keep them — a GitHub repository, a folder on your
  computer, or a synced cloud-drive folder? GitHub is the easiest if you
  already have an account." Then, on **every** file,
  restate the location and remind them to save it as plain `.md`. Never say
  "I've created" for a file you only printed.

**Follow-ups (print-and-save mode only — in write mode, look instead of asking):**
- "Do you already have the empty registry skeleton — from the template
  repository or its Download ZIP?" If yes, do not reprint or recreate
  `SCHEMA.md`, `index.md`, `log.md`, or the typed `index.md` stubs.
- "Have you used an earlier version of this framework in this folder? If
  so, paste a listing of its `outputs/` folder; otherwise say 'nothing
  there'."

**Then, in this order:**

1. **Persona.**
   **Ask:** "Who is this registry for — a business you own, a company or unit you lead, your role inside an organization, or your personal life?"
   - *Why:* your answer sets the words I use for every question that follows, and how Analyze looks at your work later.
   - *Example:* a hospital operations manager might say "my role inside an organization — the patient scheduling team I run."
   - *Not sure?* Pick the one you'd use to describe your work to a stranger. You can't pick wrong; it only changes the wording.

   Open `personas.md` and use that persona's openings for Phases 1–4. For
   the personal persona, add its privacy line now.
2. **Scan (write mode only).** Look for `knowledge/`, `sops/`,
   `process-guides/`, `CLAUDE.md` or `AGENTS.md`,
   `framework/ai-opportunity-report*.md` (or, from before 9.0,
   `outputs/ai-opportunity-report*.md`), and any loose documents sitting in
   the folder (a pasted org chart, a services page). If you found something
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
Phase 1, in write mode create `registry/` + `SCHEMA.md` + `index.md` +
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

Migrations and schema changes only — routine regeneration is not logged.
```

In print-and-save mode and no skeleton yet, print those same files first,
in that order. If the student
asks "where's the template repo?", the URL is
`https://github.com/jamesgray-ai/ai-registry-template` — it ships this same
skeleton plus a GitHub Action that checks the registry on every save, and is optional.

**Legacy-detection trigger:** In write mode: if `outputs/*/workflow.yaml` exists anywhere in
the workspace, or an `outputs/<name>-requirements.md` file exists with no
matching folder (flat layout), or an `outputs/<slug>/` folder holds any of `requirements.md`,
`design-spec.md`, `runs.md`, or a `test-runs/` folder (the pre-9.0 outputs layout), stop and offer the migration path from
`migrating-legacy-workspaces.md` before continuing the interview. A student
migrating does not repeat Phases 1–4 for businesses, lines of business,
functions, or processes the migration already covers. In print-and-save mode, rely on what the student told you in the follow-up above.

**Fast path:** if the student already has a full `registry/` bundle from a
prior scaffolding run, skip straight to gap-filling — re-run only the phases
that produced missing or incomplete nodes.

---

## Phase 1 — Business (3 min)

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
- *Why:* Analyze uses these to judge which work is most worth improving, so you won't be asked for them again.
- *Example:* a dental practice might say "fill the new evening clinic" and "cut no-shows by half".
- *Not sure?* Think about what would make this a good year for the business. Write that down in your own words; it doesn't need to be a target or a number.

Record what the student says as separate goals; if one answer could be two
goals or three, ask before writing. Set `status` to `active` without asking
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

## Phase 2 — Lines of Business (4 min)

**Signpost:** "Part 2 of 4 — How it's organized: your lines of business."

**Define it first:** "A **line of business** is something distinct the
business sells or delivers — like a product line, a service, or a training
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
suggests it is new or paused; only then ask about that line:

**Ask:** "Is [line] something you're selling now, or just starting or paused?"
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

## Phase 3 — Functions (3 min)

**Signpost:** "Part 3 of 4 — Who does the work: your functions."

**Define it first** (persona wording in `personas.md`; this is the founder
form): "A **function** is a team or department in your
organization — Marketing, Sales, Finance — that owns a kind of work across
every line of business. Your lines of business are *what you sell*; your
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

## Phase 4 — Processes (8 min)

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
them. The names below only show the shape — fill every line from the
student's own registry, never reuse these:

```
**Line of business: Cohort Courses**
- **Process:** Cohort Launch & Enrollment — owned by Marketing. Launch plan, promotion, waitlist, filling seats.
- **Process:** Cohort Delivery — owned by Service Delivery. Running live sessions week to week.

**Line of business: Corporate Training**
- **Process:** Corporate Lead to Proposal — owned by Sales. Inquiry, qualification, scoping, proposal.
```

**Ask:** "What would you add, remove, rename, or move? Each line of business only needs its main processes for now."
- *Why:* Analyze looks for work worth improving inside these processes, so anything missing here won't come up.
- *Example:* an accounting firm might add "Tax Filing" under Individual Clients and drop "Office Supplies" as too small.
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
remind the student that Analyze (Step 1 of the framework) decides where AI
fits and grows this list later; don't try to be exhaustive here.

---

## Phase 5 — Close (3 min)

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
(`registry-dashboard.html`) — never offer it as an option. In print-and-save
mode there is no maintenance hand-off: print the `log.md` entry, every typed
`index.md` you updated, and a complete `REGISTRY.md` composed per
`indexing-registry`'s rules, each with its location, and say the set is
complete.

**The close (last message) — write mode:**

> "Your registry is set up in `<folder name>`. It holds [1 business], [N lines of business], [N functions], and [N processes] — no workflows yet; Analyze adds those."
>
> "Two files give you a view of it. **`registry-dashboard.html`** is your visual dashboard: double-click it to open it in your browser, and click any line of business or process to see its details. **`REGISTRY.md`** is a one-page text summary of the same registry; it's refreshed after every step, and it's what your AI reads to catch up on your business."
>
> "You can reshape this any time — rename, merge, or move things — just ask, for example 'move [one of their processes] under [another of their lines of business]'." (Fill the example from the student's own registry.)
>
> "Next is Analyze. It asks which of your processes matter most right now, then looks inside them for work that's slow or repetitive, and registers the workflows worth building. About 15 to 20 minutes. Run it now, or later? When you're ready, say 'run the analyze skill'."

**The close — print-and-save mode:** the same four parts, with two changes.
Say where the files go: "Save each file I printed into your `registry`
folder, at the location shown above it." And for the dashboard, which can't
be printed usefully: "Your visual dashboard is created as soon as your files
are in a folder I can save to. Then say 'generate my visual dashboard'."

Say nothing about lint, checks, or GENERATED blocks. If the folder is a git
repository, you may add one line: "Want me to save a version of this?" On
Claude, after the close, you may add: "Want to share the dashboard with
someone? I can publish it as a private link." On yes to Analyze, invoke the
`analyze` skill.

**Fast path:** if no insight surfaced, skip the Note entirely and don't
mention it — an absent Note is not a gap to flag; a forced one is worse than
none.
