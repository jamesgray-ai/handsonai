# Build Spec — what Phase 5 writes

Read `types.md` at the project root. Fetch the latest OKF spec (https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md). If it is unreachable, use § OKF rules below. Then write everything in § The graph, § The standing rules, and § The two skills, in that order. Stamp every **concept page** you create with `generated: { by: process:building-knowledge-graph, at: <now as YYYY-MM-DDTHH:MM:SSZ> }` — that means `SCHEMA.md`, `overview.md`, and every page inside a type folder. `index.md`, `log.md`, `.gitkeep`, the standing-rules file, and the two `SKILL.md` files are not concepts and carry no `generated` key.

## OKF rules (distilled fallback; the fetched spec wins where they differ)

- A bundle is a folder of markdown files. Every `.md` in it except `index.md` and `log.md` is a concept and MUST have YAML frontmatter with a non-empty `type`. `title` and `description` are recommended on every concept. Type names are not registered anywhere; the user chooses them.
- Links between concepts are ordinary markdown links. Bundle-absolute form, starting with `/` at the bundle root (`/clients/acme.md`), is recommended. A link asserts a relationship; its kind is conveyed by the surrounding prose (for us: the section heading), not by the link. A link to a page that does not exist yet is legitimate, not an error.
- `index.md` may appear in any folder and lists contents for progressive disclosure: sections with `* [Title](link) - description` lines. The bundle-root `index.md` may carry one frontmatter key, `okf_version`.
- `log.md` is a flat list of date-grouped entries, newest first: `## YYYY-MM-DD` headings with `* **Word**: prose` bullets. The bold word (Creation, Update, Ingest, Query, Lint, Deprecation) is a convention.
- Provenance: `sources` is a list; each entry has a required `resource` (a URL, a bundle-relative path, a relative path, or a plain descriptor), an optional stable `id`, and an optional `title`. A claim in the body is attributed with a footnote whose label equals a `sources[].id`: `…sharded daily.[^acme-msa-2026]` and `[^acme-msa-2026]: Master services agreement`.
- Trust: `generated: { by, at }` records who wrote the current content and when. `verified: { by, at }` (or a list of them) records who confirmed it. Actors: `human:<id>` for people, `process:<id>` for automated processes, `<producer>/<version>` for agents. Trust tier is derived: no `verified` = unverified; non-human verifiers = machine-confirmed; a `human:` verifier = human-reviewed.
- Lifecycle: `status: draft | stable | deprecated` (absent = stable). `stale_after: <instant>`: stale when now ≥ that instant.
- Every timestamp is ISO 8601 with an explicit UTC offset: `2026-09-21T14:00:00Z`.
- `resource` (top-level) is the canonical URI of the thing a concept describes (a tool's site, a client's site). It is a different field from `sources[].resource`, which is provenance. Never put a source in the top-level `resource`.

## The graph — `knowledge/`

### `knowledge/SCHEMA.md`

Frontmatter first (it is a concept too), then the rulebook. Fill from `types.md`; the example below shows the shape with the worked example's types. **Replace every Acme-flavoured value with the user's.**

```markdown
---
type: Schema
title: <Scope> Knowledge Graph Schema
description: The types, relationships, and conventions for this knowledge graph. Read before creating or changing any file in knowledge/.
generated: { by: process:building-knowledge-graph, at: 2026-09-21T14:00:00Z }
---
# Knowledge Graph — SCHEMA

This bundle follows the Open Knowledge Format (read the latest version at
https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
before setting up or checking this graph). Built to OKF <version the fetched spec declares>.
Scope: the work of <person | team | company: name>.

## Types

### Client
An organization we do paid work for.
Folder:        /clients/
Frontmatter:   type, title, description, generated; sources and stale_after
               where the facts have a shelf life; resource for their website
Body:          who they are, what they buy, commercial terms, who we deal
               with, what I would tell a colleague joining the account
Relationships: `# Engagements` — links to each Engagement, ordered by start
               date, oldest first (order matters)
Examples:      Acme Manufacturing, Bowman Foods, Reston Health

### Engagement
One piece of contracted work, for one client.
Folder:        /engagements/
Frontmatter:   type, title, description, generated, status (draft | stable | deprecated)
Body:          scope, dates, what we promised, where it stands now
Relationships: `# Client` — link to its Client (reciprocal of Client's
               `# Engagements`); `# Playbooks used` — links to Playbooks
               (no order)
Examples:      Acme AI Roadmap, Acme Pilot, Bowman Data Review

### Playbook
A repeatable way we do something.
Folder:        /playbooks/
Frontmatter:   type, title, description, generated
Body:          when to use it, the steps, what good looks like
Relationships: `# Used in` — links to Engagements (reciprocal of Engagement's
               `# Playbooks used`)
Examples:      Kickoff Checklist, Discovery Interview, Handover Pack

### Note
Anything learned that has no other home yet, and answers worth keeping.
Folder:        /notes/
Frontmatter:   type, title, description, generated, sources
Body:          the note; if it is a filed answer, the question it answered
Relationships: links to whatever pages it is about, in prose
Examples:      none at build. Exempt from the three-examples rule and from
               lint's lonely-folder check.

### Overview
The single page you would hand a new hire. Exactly one, at the bundle root.
Folder:        none — exactly one file at the bundle root (overview.md),
               not inside a type folder
Body:          scope, what the work is, and links to the key pages of each type

## Relationships

Declared relationships are recorded on BOTH pages, under the headings above.
Lint reports a declared link with no reciprocal. Where order matters, the
list order is the order. A link inside ordinary prose is a mention, not a
declared relationship, and may be one-way.

## Conventions

- One concept per file. Filenames lowercase with hyphens: acme-ai-roadmap.md.
- Links between concepts are bundle-absolute: /clients/acme.md, never ../clients/acme.md.
- Every concept carries type, title, description, and generated.
  generated.at and stale_after are full instants: YYYY-MM-DDTHH:MM:SSZ.
- One index.md at the bundle root lists every page, sectioned by type, with
  bundle-absolute links. No per-folder indexes. log.md records what changed
  and when, newest first, in OKF §9 form.
- Where a page's claims come from a document, that document is listed in
  sources with an id (kebab-case, from the filename: acme-msa-2026), a
  resource path RELATIVE to the bundle pointing into the project's raw/
  folder (../raw/acme-msa-2026.pdf), and a title. Each claim taken from it
  carries a footnote [^acme-msa-2026]. Knowledge dictated in conversation
  gets a sources entry whose resource describes the occasion
  ("Call with Dana, 8 August 2026") and whose id is a slug of it
  (call-dana-2026-08-08).
- stale_after only when a fact has a real expiry: a contract end, a rate
  lock, a renewal.
- verified is added only when a person confirms a page. Never self-stamped.
- Deprecate, don't delete: a page nothing should use any more gets
  status: deprecated and stays, so links keep resolving.
- `index.md`, `log.md`, and `.gitkeep` are reserved — skip all concept
  checks on them. `index.md` carries only `okf_version`; `log.md` carries
  no frontmatter at all. Never propose adding `type` or other concept
  frontmatter to a reserved file.
- A fact belongs in this knowledge graph if it would need correcting when
  it changes. If it is a record of something that happened, it belongs in
  the system that already keeps it (calendar, inbox, invoices, raw/).
- No personal data about identifiable people: no payroll, health, or
  individual HR records.
```

### Concept pages

One folder per type inside `knowledge/`, folder name the plural slug of the type (`clients/`, `engagements/`, `playbooks/`, `notes/`) — except `Overview`, which has no folder (see above). Seed every named example from `types.md` as a page. Body sections come from the type's `Body:` line; relationship sections from `Relationships:`; keep a section even when it is empty (`_None yet._`). Shape:

```markdown
---
type: Client
title: Acme Manufacturing
description: Mid-market logistics manufacturer, client since 2024.
generated: { by: process:building-knowledge-graph, at: 2026-09-21T14:00:00Z }
resource: https://example.com # canonical site, only when one exists
---
# Who they are
Family-owned, 400 staff, three factories. (Only what the user told you.)

# What they buy
_Fill from the first ingest._

# Commercial terms
_None yet._

# Who we deal with
_None yet._

# What I would tell a colleague
_None yet._

# Engagements
1. [Acme AI Roadmap](/engagements/acme-ai-roadmap.md)
2. [Acme Pilot](/engagements/acme-pilot.md)
```

Write only what the user actually said. A seeded page with empty sections is correct; a seeded page with invented detail is a defect.

`notes/` is created with an empty `.gitkeep` file and no pages.

### `knowledge/overview.md`

```markdown
---
type: Overview
title: <Scope name> — Overview
description: What this work is, who it serves, and where to start reading.
generated: { by: process:building-knowledge-graph, at: 2026-09-21T14:00:00Z }
---
# Scope
This graph covers <the work you do | your team's work | the whole company>: <one sentence from the interview>.

# What the work is
<Two to four short paragraphs from the interview: what is delivered, to whom, what repeats. Only what the user said.>

# Where to start
- Clients: [Acme Manufacturing](/clients/acme-manufacturing.md), [Bowman Foods](/clients/bowman-foods.md)
- Engagements: [Acme AI Roadmap](/engagements/acme-ai-roadmap.md)
- Playbooks: [Kickoff Checklist](/playbooks/kickoff-checklist.md)
```

### `knowledge/index.md`

```markdown
---
okf_version: "0.2"
---
# Knowledge Graph Index

# Overview
* [Overview](/overview.md) - What this work is, who it serves, and where to start reading.

# Clients
* [Acme Manufacturing](/clients/acme-manufacturing.md) - Mid-market logistics manufacturer, client since 2024.
* [Bowman Foods](/clients/bowman-foods.md) - …

# Engagements
* …

# Playbooks
* …

# Notes
_None yet._

# Schema
* [Schema](/SCHEMA.md) - The types, relationships, and conventions for this knowledge graph.
```

Set `okf_version` to the version the fetched spec declares; `"0.2"` if unreachable. One line per page, description copied from its frontmatter.

### `knowledge/log.md`

```markdown
# Knowledge Graph Log

## 2026-09-21
* **Creation**: Built the graph from types.md — 4 types (Client, Engagement, Playbook, Note), 9 seeded pages, overview, index, schema. Standing rules written to CLAUDE.md; ingest and lint skills written to .claude/skills/.
```

Newest date first. Entries are prose; the bold word is Creation, Update, Ingest, Query, Lint, or Deprecation.

## The standing rules — `CLAUDE.md` or `AGENTS.md` at the project root

About thirty lines. If the file already exists (a course workspace often has one), **append** this block under a heading `# Knowledge graph` rather than overwriting.

```markdown
# Knowledge graph

`knowledge/` holds the knowledge graph for <scope>: markdown concept pages
about the work itself, one concept per file, following the Open Knowledge
Format. `knowledge/SCHEMA.md` is the rulebook. `raw/` at the project root
holds source documents: read them, never edit them. `types.md` is the
original blueprint; when it and SCHEMA.md disagree, SCHEMA.md wins.

I am `human:<id>`.

## Rules
- Read `knowledge/SCHEMA.md` before creating or changing any file in `knowledge/`.
- Everything in `knowledge/` is markdown. Never put tool configuration there.
- Never edit anything in `raw/`.
- Stamp `generated` on every page you write, with `by: process:ingest`, `process:lint`, or `process:building-knowledge-graph`, whichever wrote the page. Add `verified: { by: human:<id>, at: <instant> }` only when I confirm a page is right, never on your own.

## Answering my questions
When I ask a question ABOUT THE WORK (clients, offerings, processes, people, tools, policies):
1. Read `knowledge/index.md` first, then open only the pages that could hold the answer.
2. Answer from those pages only. Cite each page you used by path.
3. If the answer is not in the graph, say so plainly. Do not fill the gap from general knowledge.
4. If the answer is worth keeping, offer to file it as a Note in `knowledge/notes/`.
Questions about anything else in this project are answered normally.

## Skills in this project
- `ingest`: fold a document from `raw/`, or something I tell you, into the pages it affects. Proposes first, writes after I say yes.
- `lint`: sweep every page against `SCHEMA.md` and report; fixes only what I approve.
```

## The two skills — in the platform's skills folder at the project root

### `<skills folder>/ingest/SKILL.md`

```markdown
---
name: ingest
description: Fold a new source into the knowledge graph. Use when the user says "ingest", names a document in raw/, pastes something to add, or tells you a fact about the work to record. Proposes the changes first, writes after approval, reports every file changed.
---
# Ingest

1. Read `knowledge/log.md` to see what has already been folded in, so nothing is ingested twice. Read `knowledge/SCHEMA.md` and `knowledge/index.md`, so the question you ask of the source is "which of these types and pages does it touch", not "what is in here".
2. Identify the source: the document the user named in `raw/`; or everything in `raw/` the log does not account for, if they named none; or the text they pasted or said.
3. **Propose before writing.** List the pages that would change (existing and new) and, under each, the claims that would land there in one line each. Ask: "Shall I write these?" Change nothing until the user says yes. Steering such as "focus on the commercial terms" is welcome.
4. Write. For each affected page: update what is now out of date, add what is new, leave the rest. Record the source in the page's `sources` with an `id` (kebab-case from the filename, e.g. `acme-msa-2026`; for spoken knowledge, from the occasion, e.g. `call-dana-2026-08-08`), a `resource` (`../raw/<file>`, or a plain description of the occasion), and a `title`. Footnote each claim you added with `[^<id>]` and add the matching `[^<id>]: <title>` line at the end of the body. Set `stale_after` when the source gives a fact a real expiry. If the source reveals a declared relationship, add the link on BOTH pages under their agreed headings. Stamp `generated: { by: process:ingest, at: <instant> }` on every page you touch.
5. Update `knowledge/index.md` for any new page and append an `**Ingest**` entry to `knowledge/log.md`.
6. Report every file changed and why, one line each.

Rules: never edit `raw/`. Never invent. A twelve-page contract may produce four sentences across two pages; that is correct. Distil, don't extract. If this skill is run unattended (a scheduled sweep), stop at step 3: write the proposal to `knowledge/log.md` under `**Ingest (proposed)**` and change no pages.
```

### `<skills folder>/lint/SKILL.md`

```markdown
---
name: lint
description: Health-check the knowledge graph. Use when the user says "lint", asks to check the graph, or after any change to types or relationships. Reads the OKF spec and SCHEMA.md, sweeps every page, reports; fixes only what the user approves.
---
# Lint

1. Fetch the latest OKF spec (https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md) if reachable. Read `knowledge/SCHEMA.md`. Read every file under `knowledge/`. `index.md`, `log.md`, and `.gitkeep` are reserved — skip all concept checks on them; never propose "fixing" them by adding `type` or other concept frontmatter.
2. Report, grouped, naming specific files:
   - **Rule violations**: a page missing `type`, `title`, `description`, or `generated`; a page in the wrong folder for its type; a relative link between concepts; a bare-date timestamp; tool configuration inside `knowledge/`. (Not reserved files — see step 1.)
   - **Contradictions**: two pages that disagree about a fact.
   - **Out of date**: any page whose `stale_after` has passed; claims a newer source superseded.
   - **Broken structure**: orphan pages nothing links to; a declared relationship with no reciprocal on the other page; links into `status: deprecated` pages; pages missing from `index.md`.
   - **Trust picture**: how many pages are unverified, machine-confirmed, and human-reviewed.
   - **Pages worth writing** (not errors): concepts mentioned on several pages that have no page of their own; links to pages that do not exist yet. Exempt `notes/` from any lonely-folder observation.
3. Ask which fixes to apply. Apply only those, stamping `generated: { by: process:lint, at: <instant> }` on any page you fix. Append a `**Lint**` entry to `knowledge/log.md` with what was found and what was fixed.
```
