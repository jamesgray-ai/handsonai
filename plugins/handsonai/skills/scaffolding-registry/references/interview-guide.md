# Scaffolding Interview Guide

Six phases (0–5), about 25 minutes total. Run them in order. Each phase has a timebox —
treat it as a budget, not a target to fill.

**Pacing rule:** If a phase overruns its box, write what you have, mark the
gap in the close-out summary, and move on — missing nodes are homework;
fictional nodes are never a fallback.

---

## Phase 0 — Home and sources (4 min)

**First, detect — don't ask.** Can you create and edit files in the folder
the student has open? (A file the student would have to download does not count — that is print-and-save mode.)

- **Yes → write mode.** The registry goes at the root of that folder. It
  does not matter whether the folder is local, a synced cloud-drive folder,
  or a Git repository — the bundle is plain Markdown with relative links.
  Confirm in one sentence: "I'll create `registry/` inside `<folder name>` —
  OK?"
- **No → print-and-save mode.** Say once, up front: "I can't save files
  here, so for each file I'll print its full contents and exactly where to
  save it. Where will you keep them — a GitHub repository, a folder on your
  computer, or a synced cloud-drive folder? GitHub is the easiest if you
  already have an account." Then, on **every** file,
  restate the location and remind them to save it as plain `.md`. Never say
  "I've created" for a file you only printed.

**Follow-ups (both modes):**
- "Do you already have the empty registry skeleton — from the template
  repository or its Download ZIP?" If yes, do not reprint or recreate
  `SCHEMA.md`, `index.md`, `log.md`, or the typed `index.md` stubs.
- "Do you already have a `registry/` folder, or a `workflow.yaml` /
  `outputs/<name>-requirements.md` setup from an earlier version of this
  framework?" In write mode, look rather than ask. In print-and-save mode
  you cannot look — ask the student to paste a listing of their `outputs/`
  folder, or to say "nothing there".

**Then, in this order:**

1. **Persona.** "Who is this registry for — a business you own, a company or
   unit you lead, your role inside an organization, or your personal life?"
   Open `personas.md` and use that persona's openings for Phases 1–4. For
   the personal persona, add its privacy line now.
2. **Scan (write mode only).** Look for `knowledge/`, `sops/`,
   `process-guides/`, `CLAUDE.md` or `AGENTS.md`,
   `outputs/ai-opportunity-report*.md`, and any loose documents sitting in
   the folder (a pasted org chart, a services page). Report in one short
   list what you found and what each could pre-fill, or say "nothing here
   to pre-fill from" in one line. Never write to `knowledge/`.
3. **Documents.** "Do you have anything that already describes [the
   business / your team / the areas you want to run]? Paste or upload it
   now and I'll draft the nodes for you to confirm. If not, we'll build it
   together." Name the examples for the student's persona from
   `personas.md` § Documents to ask for. Map each with `intake-sources.md`.
   An answer the student gives here in words ("the areas are household,
   money, and the kids") counts as a source for the phase it covers: open
   that phase with the draft, still in phase order.
4. **The rule, once.** "I'll propose, you confirm. Nothing from these gets
   written until you say so, and I'll name functions for the area or role,
   never for the person, unless you ask."

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
skeleton plus a GitHub Action that publishes the dashboard, and is optional.

**Legacy-detection trigger:** In write mode: if `outputs/*/workflow.yaml` exists anywhere in
the workspace, or an `outputs/<name>-requirements.md` file exists with no
matching folder (flat layout), stop and offer the migration path from
`migrating-legacy-workspaces.md` before continuing the interview. A student
migrating does not repeat Phases 1–4 for businesses, lines of business,
functions, or processes the migration already covers. In print-and-save mode, rely on what the student told you in the follow-up above.

**Fast path:** if the student already has a full `registry/` bundle from a
prior scaffolding run, skip straight to gap-filling — re-run only the phases
that produced missing or incomplete nodes.

---

## Phase 1 — Business (3 min)

**Opening question:** "What's the name of the business or team this registry
is for, and what does it do in one sentence?"

**Persona wording:** use the opening for the student's persona from
`personas.md`; the question above is the founder form.

**If a Phase 0 source covers this phase:** open with the draft instead —
"From your [source], here's what I'd write: [show the node body]. Anything
wrong or missing?" Write only what the student confirms.

**Follow-ups:**
- "Is it active, still incubating, or dormant right now?"
- "Is there a URL you'd like on the dashboard?"
- "What are the two or three outcomes that matter most this year?"

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

**Opening question:** "Does this business have distinct lines of business, or
is it really one thing end to end?"

**Persona wording:** use the opening for the student's persona from
`personas.md`; the question above is the founder form.

**If a Phase 0 source covers this phase:** open with the draft instead —
"From your [source], here's what I'd write: [show the node body]. Anything
wrong or missing?" Write only what the student confirms.

**Follow-ups:**
- "If there's more than one, what order should they show up in — the order that matters most to you?"
- "Any of these dormant or just getting started?"

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

**Opening question:** "Who owns the work day to day? I'll suggest a starter
set and you can trim or rename it."

**Persona wording:** use the opening for the student's persona from
`personas.md`; the question above is the founder form.

**If a Phase 0 source covers this phase:** open with the draft instead —
"From your [source], here's what I'd write: [show the node body]. Anything
wrong or missing?" Write only what the student confirms.

**Follow-ups:**
- "Any of these unstaffed right now — no single owner?"
- "Anything missing from this list for how you're actually organized?"

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

**Opening question:** "For each line of business, what are the three to five
processes that deliver it — where the time, money, and customer outcomes
actually flow? Rank them by how much they matter to the business. Analyze
will decide where AI fits; right now we just want the map."

**Persona wording:** use the opening for the student's persona from
`personas.md`; the question above is the founder form.

**If a Phase 0 source covers this phase:** open with the draft instead —
"From your [source], here's what I'd write: [show the node body]. Anything
wrong or missing?" Write only what the student confirms.

**Follow-ups:**
- "Who owns each of these — which function (or, for a personal registry,
  which role)?" When the student answers with shorthand ("training"),
  say which Function you read it as before writing the slug.
- "Is there an existing guide or SOP for any of them?"
- Once the processes are named, one message covering every Function left
  without a process: "[Function] from the starter set has no process yet —
  does it own one of these, or shall we drop it?" Functions have no
  `status`, so dropping one means deleting the node and its index line at
  Close.

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

**Opening question:** "Is there anything you already know about how this
business runs — a process quirk, a constraint, a lesson learned — that's
worth capturing as a note before we wrap up?"

**Follow-ups:**
- "Anything that surprised you or changed how you'd do this next time?"

**Example to show:** the Note node from `example-registry.md`
(`registry/notes/2026-08-status-report-timing.md`).

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
1 `REGISTRY.md`, and offer the Tier 2 dashboard. The lab should end with
something visual on screen. In print-and-save mode there is no
maintenance hand-off: print the `log.md` entry, every typed `index.md` you
updated, and a complete `REGISTRY.md` composed per `indexing-registry`'s
rules, each with its location, say the set is complete, and then make the
same Analyze offer. In both modes, offer Analyze: "Your registry has [N]
processes and no workflows yet. Analyze finds the workflows: it walks each
of these processes asking where the friction is, and registers the ones
worth building. About 15 to 20 minutes. Run it now, or later?" On yes,
invoke the `analyze` skill.

**Fast path:** if no insight surfaced, skip the Note entirely — an absent
Note is not a gap to flag; a forced one is worse than none.
