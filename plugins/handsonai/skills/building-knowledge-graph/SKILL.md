---
name: building-knowledge-graph
description: >
  This skill should be used when the user wants to build their knowledge
  graph — a knowledge/ folder of markdown pages about the work a person,
  team, or company does (clients, offerings, processes, people, tools,
  policies) that the AI maintains, following the Open Knowledge Format.
  Triggers: "build my knowledge graph", "set up my knowledge graph", "create
  my knowledge graph", "start my knowledge graph", "set up my business
  knowledge base", starting the knowledge graph lab. NOT the AI Registry:
  for "set up my registry" or an inventory of workflows, skills, and agents,
  use scaffolding-registry. NOT step 4 of the AI Workflow Framework: for
  building a workflow's building blocks, use the build skill. Re-running on
  an existing knowledge/ bundle fills gaps; it never rebuilds.
user-invocable: true
---

# Building Knowledge Graph

Build the user's knowledge graph: a `knowledge/` folder of markdown concept pages about the work a person, a team, or a company does, that the AI maintains from now on. The pattern is Andrej Karpathy's LLM wiki (three layers: raw sources, the wiki, the schema; three operations: ingest, query, lint). The file format is Google's Open Knowledge Format (OKF). This is a ~30-minute guided build that ends with a small real graph and all three operations run once against it.

Ground yourself in two sources before Phase 5, and read the latest version of each rather than working from memory:

1. Karpathy's LLM-wiki note: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. The OKF specification: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md (raw: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md)

If a page cannot be fetched, work from the distilled rules in `references/build-spec.md`.

This file is the map. `references/interview-guide.md` is the script for Phases 0–4 and the Close; `references/build-spec.md` is the exact shape of everything Phase 5 writes; `references/example-knowledge-graph.md` is a worked example that is **shown to illustrate and never copied** into the user's graph.

## What this builds

```
<project folder>/                ← the user opens their AI here
├── .claude/skills/              ← Claude Code and Cowork (ChatGPT app: .agents/skills/)
│   ├── ingest/SKILL.md             fold a document into the pages it affects
│   └── lint/SKILL.md               sweep every page against SCHEMA.md
├── raw/                         ← source documents, read but never edited — OUTSIDE the bundle
├── knowledge/                   ← the OKF bundle
│   ├── <one folder per type>/
│   │   └── <one page per concept>.md
│   ├── notes/                      filed answers and knowledge with no other home
│   ├── overview.md                 the page you would hand a new hire
│   ├── index.md                    every page, one line each; okf_version in frontmatter
│   ├── log.md                      dated record of what changed
│   └── SCHEMA.md                   the rulebook: types, relationships, conventions
├── CLAUDE.md                    ← standing rules, read every session (ChatGPT app: AGENTS.md)
└── types.md                     ← the approved blueprint from Phase 4
```

## Platform and mode

**Write mode only.** This skill needs a tool that opens a folder on the user's machine and writes files into it: Claude Code, Cowork, the ChatGPT desktop app's Codex view, and also Cursor, Codex CLI, or Gemini CLI. If you cannot create files in the user's folder (claude.ai or ChatGPT in the browser, Gemini, Microsoft 365 Copilot), say so in two sentences in Phase 0, name those three desktop tools, and stop. There is no print-and-save fallback: a knowledge graph is dozens of files, and hand-saving printed files is not a realistic path.

Resolve platform names yourself; never ask the user:

| | Claude Code / Cowork | Codex (ChatGPT app) and Codex CLI |
|---|---|---|
| Standing-rules file, at the project root | `CLAUDE.md` | `AGENTS.md` |
| Skills folder, at the project root | `.claude/skills/` | `.agents/skills/` |

We work in phases with stop-gates. Announce each phase as you reach it. Never move to a later phase until the user says so, and build nothing until the user sends the single word **build** as its own message.

## Phase 0 — Home and boundaries (2 min). Create nothing.

1. State the full path of the folder you are working in and ask the user to confirm it is the **project folder**: the one that will hold the standing-rules file, the skills folder, `raw/`, and `knowledge/`. The graph goes in a `knowledge/` subfolder; the machinery goes at the root. If the user is inside a `knowledge/` folder already, tell them to reopen one level up.
2. State the platform and therefore which rules-file and skills-folder names apply.
3. Confirm write mode (see Platform and mode). If you cannot write files, stop here.
4. Report what already exists, explicitly:
   - `registry/` present → say in one sentence: *Your registry stays untouched; it records what you build with AI. This build models the work itself and goes in `knowledge/` beside it.*
   - `knowledge/SCHEMA.md` present → **gap-filling mode.** Read `SCHEMA.md`. List which types have no pages, which declared relationships have no reciprocal, and what is missing. Offer to fill only those gaps. Never rewrite `SCHEMA.md`, never rebuild. Run the relationships round of Phase 3 only for any new type.
   - `types.md` present but no `knowledge/` → **resume mode.** Show the list and offer to pick up at Phase 3 (revise) or Phase 5 (build).
   - None of these → fresh build from Phase 1.
5. Ask once how to record the user as an actor: `human:<name>`, for example `human:jamesgray`. Phase 5 writes it into the standing-rules file so every future session stamps `verified` with the same id.
6. Never invoke `scaffolding-registry` or `indexing-registry` from this skill; they belong to a different bundle.

Follow `references/interview-guide.md` § Phase 0.

## Phase 1 — Look around first (3 min)

1. State the privacy line once, before reading anything: *Nothing with personal data about identifiable people goes into the graph: no payroll, no health records, no individual HR files, whichever way it would arrive.*
2. **Create `raw/` at the project root now, automatically**, and say so in one line. This is the single exception to Phase 0's "create nothing", and it happens whether or not the user has documents yet.
3. Scan the whole project folder for anything readable about the work: README files, SOPs, process guides, proposals, requirements files from earlier framework steps, transcripts, spreadsheet names. Do not read `registry/` as evidence about the work; it is about AI builds.
4. Ask one question: *"Do you have two or three documents that describe your work — a proposal, a client summary, a process doc, a team charter? Tell me where they are, drop them into the `raw/` folder I just made, or say skip."* If your platform can reach other systems (a Drive or email connector, saved memory), offer to look there too, and never look without a yes.
5. Report in plain words: what the work appears to be, and which named things (clients, offerings, tools, processes, people, policies) appear and where. State honestly what was found and what was not. If nothing was found, say so in one line and go to Phase 2. Never present a guess as something you read. Never invent facts about the work.

Follow `references/interview-guide.md` § Phase 1.

## Phase 2 — Interview, concrete first (7 min)

One question at a time. Skip any question Phase 1 already answered, and say that you are skipping it and why. Wording is for someone who has never heard the word *graph*: say "kinds of things" before "types" and "the real ones" before "concepts". The interview must work for any role or industry: a fractional CFO, an HR lead, a product manager, a clinic operations lead, a nonprofit director, an e-commerce operator.

0. The sixty-second explainer, delivered proactively (many users will not have read the lesson).
1. **Scope:** the work *you* do, your *team's* work, or the *whole company's*?
2. The 5–10 most important named things in that work.
3. Who you do the work for, and what you deliver to them.
4. What work repeats in a typical week or month.
5. What you wish you could look up when making a decision.

The question *what lives only in your head or in scattered documents* is not a type-finder; it is asked at the Close, as the first knowledge to dictate into the graph.

Follow `references/interview-guide.md` § Phase 2, including the probe list and the six example type lists (shown, never copied).

## Phase 3 — Propose and iterate: types, then relationships (8 min)

**Types round (5 min).** Propose 4–7 types drawn from Phases 1 and 2. For each: a type name in the user's own words, a one-line definition, and 2–3 real named examples the user mentioned. Refine in rounds: the user renames, merges, deletes, and adds; you challenge. Push back if the user over-models: every type must earn its place with real examples, and a type that cannot name three real ones today is a field on some other type or a note. Flag anything from the interview that has no home on the list. Use the user's words, never consultant words. **`Note` is always on the list** and is exempt from the three-examples rule: it holds filed answers, syntheses, and knowledge that belongs to no other type yet. Create no files while iterating. Iterate until the user says the list is right.

**Relationships round (3 min).** Once the list is stable, propose the connections between types **as plain sentences using the user's real examples**: "Acme has two Engagements, the AI Roadmap and the Pilot." "The Kickoff Checklist was used in the Acme Pilot." No diagrams, no arrows; the words edge, direction, and cardinality never appear. The user confirms, corrects, or strikes each sentence. Each relationship earns its place with one question: *"What would you look up by following this link?"* No answer, no link. Keep one to three relationships per type. For each kept relationship, agree the heading it will live under on each side, in the user's words (`# Engagements` on a Client page, `# Client` on an Engagement page), and ask whether order matters ("the pilot came before the roadmap"; "these are the steps in order").

Follow `references/interview-guide.md` § Phase 3.

## Phase 4 — Approve (1 min)

When the user approves the list: write exactly ONE file, `types.md`, at the ROOT of the project (NOT inside `knowledge/`, which does not exist yet and will hold only knowledge pages). Two sections: `# The types` (each type with its one-line definition and the named examples agreed) and `# How they connect` (one line per declared relationship: the sentence, the heading on each side, and whether order matters). Replace any draft the user brought. Show it and stop. This file is the blueprint you build from.

Follow `references/interview-guide.md` § Phase 4.

## Phase 5 — Build (4 min)

ONLY when the user sends the word **build** as its own message. Construct the graph from `types.md`, following the latest OKF spec (fetch it now; fall back to `references/build-spec.md` § OKF rules if unreachable) and the exact shapes in `references/build-spec.md`:

(a) **The graph**, in `knowledge/`: `SCHEMA.md` with frontmatter (`type: Schema`); a folder per type; every named example seeded as a concept page with `type`, `title`, `description`, `generated`, its declared relationship sections, and bundle-absolute links; `notes/` (empty, with `.gitkeep`); `overview.md`; one `index.md` at the bundle root with `okf_version` as its only frontmatter; `log.md` in OKF §9 form. Confirm `raw/` exists at the project root (Phase 1 created it).

(b) **The standing rules**: about thirty lines at the project root under this platform's name, from the template in `references/build-spec.md`, including the user's actor id.

(c) **The two local skills**: `ingest/SKILL.md` and `lint/SKILL.md` in this platform's skills folder at the project root, from the templates in `references/build-spec.md`. They are multi-step procedures, which is why they are skills rather than standing-rules content.

Then report everything you built, grouped as **graph**, **rules**, and **skills**, and say where each thing is.

If the user says the build produced something they did not want and nothing of theirs is in `knowledge/` yet, offer to delete `knowledge/`, fix `types.md`, and build again. Once real content is in the graph, never rebuild; fix the specific thing.

## Close — run the loop once, guided (5 min)

Not numbered phases. Guide the user through each step and state what "worked" looks like:

1. **On Cowork only:** ask the user to type `/ingest` and confirm the skill fires. If it does not, walk them through adding `ingest/SKILL.md` and `lint/SKILL.md` as account skills in the Claude app (Customize → Skills), then continue.
2. **Ingest** one document from `raw/` (or one the user pastes) by running the `ingest` skill you wrote, not by working from this file, so the user sees the thing they will use from now on. Worked when: at least one *already existing* page changed and carries a footnoted claim and a `sources` entry.
3. **Query**: ask the user for one question that follows a relationship ("Which playbooks have we used with Acme?"). Answer from the graph only, reading `index.md` first, citing every page you used. Worked when: the answer names two or more pages and opening one confirms the claim. If the answer is worth keeping, offer to file it as a Note.
4. **Lint** by running the `lint` skill you wrote. Worked when: the report names specific files.
5. **Verify one page**: ask the user to read one seeded page and say whether it is right. When they confirm, add `verified: { by: human:<their id>, at: <now> }` to its frontmatter. Worked when: the page's frontmatter shows `verified`.
6. **Dictate**: ask *"What do you know that is in nobody's document? Tell me, the way you would tell a colleague, and I will put it on the pages it belongs to."* Fold it in through the ingest skill with a descriptive `sources` entry. Worked when: at least one page changed and its `sources` names the conversation.
7. Offer Obsidian's graph view: download Obsidian, **Open folder as vault** on `knowledge/`, click the graph icon.
8. Hand off: the graph is small and real. Seed to at least ten concepts across three types on real material, and run the loop again.

## Write rules

- Never invent facts about the user's work; ask.
- The user's words, not consultant words. When unsure, propose and ask.
- Once `knowledge/SCHEMA.md` exists it is authoritative; re-read it immediately before every write, including in gap-filling mode.
- `types.md` and `raw/` live at the project root, outside the bundle. `knowledge/` holds concept pages (including `overview.md` and `notes/`), `SCHEMA.md`, `index.md`, `log.md`, and nothing else. Never write tool configuration into it.
- Links between concepts are bundle-absolute (`/clients/acme.md`), never `../`. The one relative path in the bundle is `sources[].resource` pointing outside it (`../raw/<file>`).
- Every page carries `type`, `title`, `description`, `generated: { by: process:building-knowledge-graph, at: <instant> }`. `at` is a full ISO 8601 instant, `YYYY-MM-DDTHH:MM:SSZ`, never a bare date. `sources` (with `id`) and `stale_after` only where they mean something. `verified` only on a human's say-so, never self-stamped.
- Declared relationships are recorded on both pages under their agreed headings. Incidental mentions in prose are ordinary one-way links.
- Deprecate, don't delete, while anything links to a page (`status: deprecated`).
- The worked example in `references/example-knowledge-graph.md` is shown to illustrate, never copied. The finished graph must contain no Acme residue.
- If a phase runs over its timebox, write what has been gathered, say what is missing, and move on. Missing pages are homework; invented ones are never acceptable.
