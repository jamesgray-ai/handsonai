# Scaffolding Interview Guide

Six phases, ~30 minutes total. Run them in order. Each phase has a timebox —
treat it as a budget, not a target to fill.

**Pacing rule:** If a phase overruns its box, write what you have, mark the
gap in the close-out summary, and move on — missing nodes are homework;
fictional nodes are never a fallback.

---

## Phase 0 — Home (2 min)

**Opening question:** "Where should your registry live — a new repo from the
template, inside a workspace you already have, or should I generate it here
and you commit it yourself?"

**Follow-ups:**
- "Do you already have a `registry/` folder, or a `workflow.yaml` / `outputs/<name>-requirements.md` setup from an earlier version of this framework?"
- "Is this a GitHub repo you can clone locally, or are we working entirely in this chat?"

**Example to show:** none — this phase is about the student's environment,
not the registry's content.

**What to write:** nothing yet. Record which of the three homes applies:
(a) template repo — `https://github.com/jamesgray-ai/ai-registry-template` —
via *Use this template* (arrives with the skeleton + Tier 3 machinery already
in place); if the student asks "where's the template repo?", this is the
URL; (b) scaffold into an existing repo/workspace
(create `registry/` + `SCHEMA.md` + `index.md` + `log.md` + the six typed
directories with stub `index.md` files); (c) cloud generate-and-commit
fallback (produce the files in chat; the student commits them by hand).

**Legacy-detection trigger:** if `outputs/*/workflow.yaml` exists anywhere in
the workspace, or an `outputs/<name>-requirements.md` file exists with no
matching folder (flat layout), stop and offer the migration path from
`migrating-legacy-workspaces.md` before continuing the interview. A student
migrating does not repeat Phases 1–5 for workflows the migration already
covers.

**Fast path:** if the student already has a full `registry/` bundle from a
prior scaffolding run, skip straight to gap-filling — re-run only the phases
that produced missing or incomplete nodes.

---

## Phase 1 — Business (3 min)

**Opening question:** "What's the name of the business or team this registry
is for, and what does it do in one sentence?"

**Follow-ups:**
- "Is it active, still incubating, or dormant right now?"
- "Is there a URL you'd like on the dashboard?"

**Example to show:** the Business node from `example-registry.md`
(`registry/businesses/brightwork-consulting.md`).

**What to write:** one `registry/businesses/<slug>.md` node — required
frontmatter plus `status` and optional `url`, one identity sentence in the
body, and an empty `# Lines of Business` list (Phase 2 fills it).

**Fast path:** one business per registry is the default — do not offer
multi-business setup unless the student volunteers that they run more than
one.

---

## Phase 2 — Lines of Business (4 min)

**Opening question:** "Does this business have distinct lines of business, or
is it really one thing end to end?"

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

**Follow-ups:**
- "Any of these unstaffed right now — no single owner?"
- "Anything missing from this list for how you're actually organized?"

**Starter set (verbatim):** Marketing, Sales, Service Delivery, Operations,
Product, Customer Success, IT/Engineering.

**Example to show:** the Function node from `example-registry.md`
(`registry/functions/service-delivery.md`) — note the empty GENERATED
`# Owns` block written at creation time.

**What to write:** one `registry/functions/<slug>.md` node per function the
student keeps, `lead:` filled in or left blank (blank = unstaffed, an
insight not an error), and every node written **with** its empty GENERATED
`# Owns` marker block — the reference lints an error on a Function missing
that block ("compose can't fill what doesn't exist").

**Fast path:** offer the starter set as-is; most students accept it with one
or two renames rather than building from scratch.

---

## Phase 4 — Processes (8 min)

**Opening question:** "For each line of business, what are the two or three
processes where AI could help the most right now? Not everything you do —
just the highest-value candidates."

**Follow-ups:**
- "Who owns each of these — which function?"
- "Is there an existing guide or SOP for any of them?"

**Example to show:** the Process node from `example-registry.md`
(`registry/processes/client-delivery.md`).

**What to write:** one `registry/processes/<slug>.md` node per process, each
with a title, a description, required `owner:` (a function slug from Phase
3), optional `guide:`, and an entry added to its LOB's curated
`# Processes` list.

**Fast path:** two or three processes per LOB is enough for the lab —
remind the student that Analyze (Step 1 of the framework) grows this list
later; don't try to be exhaustive here.

---

## Phase 5 — First Workflow (7 min)

**Opening question:** "Which single workflow are you going to take through
the framework first? Walk me through what happens, start to finish."

**Follow-ups:**
- "What triggers it — a schedule, an event, a request?"
- "Do you already have any requirements, SOP, or other artifacts for it?"

**Example to show:** the Workflow node from `example-registry.md`
(`registry/workflows/client-status-reporting.md`) — the full frontmatter
set, the `# Artifacts` and `# Skills` link sections, and the empty
GENERATED `# Insights` block.

**What to write:** one `registry/workflows/<slug>.md` node with `status`,
`definition_type`, `execution_mode`, `autonomy`, `trigger`, optional
`stale_after`, two sentences of body prose describing what the workflow
does, `# Artifacts` links to any existing requirements/SOP/other files,
`# Skills` / `# Agents` links to any existing capabilities, an empty
GENERATED `# Insights` block, and an entry added to its Process's curated
`# Workflows` list.

**Fast path:** if the student has no artifacts yet, write the node with
empty `# Artifacts` / `# Skills` sections rather than waiting — the
framework's later steps fill them in.

---

## Phase 6 — Close (3 min)

**Opening question:** "Is there anything you already know from running this
workflow that's worth capturing as a note — before we wrap up?"

**Follow-ups:**
- "Anything that surprised you or changed how you'd do this next time?"

**Example to show:** the Note node from `example-registry.md`
(`registry/notes/2026-08-status-report-timing.md`).

**What to write:** an optional `registry/notes/<slug>.md` node — only if a
real insight surfaced during the interview, never a manufactured one — plus
a founding `registry/log.md` entry describing the scaffolding run, and
directory `index.md` stubs for every typed directory. Hand off to
`indexing-registry` for the first maintenance pass: lint, generate the Tier
1 `REGISTRY.md`, and offer the Tier 2 dashboard. The lab should end with
something visual on screen.

**Fast path:** if no insight surfaced, skip the Note entirely — an absent
Note is not a gap to flag; a forced one is worse than none.
