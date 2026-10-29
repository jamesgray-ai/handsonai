---
name: scaffolding-registry
description: >
  This skill should be used when the user wants to set up their AI Registry as a
  knowledge bundle — a registry/ folder with SCHEMA.md and concept nodes for the
  workflows, processes, and functions of their business. Triggers: "set up my
  registry", "set up my AI registry", "create my registry", "scaffold my
  registry", starting the registry lab, or when any framework skill finds no
  registry/SCHEMA.md where the leader keeps their framework files. NOT the
  business knowledge graph: for "build my knowledge graph" or a knowledge/
  folder about the work itself (clients, offerings, processes as knowledge),
  use building-knowledge-graph. Re-running on an existing bundle fills gaps; it
  never re-scaffolds.
---

# Scaffolding Registry

Stand up a leader's AI Registry as an [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) knowledge bundle: a `registry/` folder with a `SCHEMA.md` producer profile and concept nodes for their real business. This is the on-ramp: a guided interview that captures the leader's real business, lines of business, functions, and processes. It names no workflows: the `analyze` skill does that next, writing them into the backlog.

## What this builds

The registry lives in the **working folder**, the one folder that holds the leader's AI Registry (`registry/`), their workflows (`framework/`, the framework folder) and their knowledge graph (`knowledge/`). Where that folder is depends on where the leader works (see *Where the files live* below): on Claude Code and Codex it is the workspace; on the web (Claude, ChatGPT) and in Microsoft 365 Copilot (Cowork), a folder in the leader's Google Drive or OneDrive, `ai-workspace/` unless they keep another; on Claude desktop, the folder the leader selects in the prompt window. The layout inside it is the same everywhere:

```
<working folder>/            ← the workspace on Claude Code and Codex; ai-workspace/ (or the leader's own folder) elsewhere
├── REGISTRY.md              ← Tier 1 dashboard (derived, never hand-edited)
├── registry-dashboard.html  ← Tier 2 visual dashboard (derived; always generated at setup)
├── registry/                ← the OKF v0.2 bundle
│   ├── SCHEMA.md            ← producer profile (written by scaffolding-registry)
│   ├── index.md             ← bundle root; frontmatter okf_version: "0.2"
│   ├── log.md               ← setup decisions, schema changes, workflow events
│   ├── businesses/  lines-of-business/  functions/
│   ├── processes/   workflows/          notes/
│   │       (each typed directory has its own index.md)
├── framework/               ← the framework folder (made by the first step that saves a workflow, never by this skill)
│   └── <workflow>/          ← the workflow's record: requirements.md, design-plan.md,
│                              build-record.md, test-results.md, with inputs/, context/
│                              and history/
├── knowledge/               ← the knowledge graph, when the leader builds one (building-knowledge-graph)
├── sops/  process-guides/   ← unchanged homes; nodes link to them
```

A workflow's **run log** is never in the working folder: it lives where the workflow runs. Event facts stay in the workflow's record, never in registry nodes.

The registry is the structured record every framework skill reads and writes: `analyze` writes backlog Workflow nodes into it, `deconstruct` starts a workflow (`under-development`) and links its requirements, `design` records how the workflow decides and runs and links its plan, `build` links the skills and agents it built, and `test` links the test results and takes the workflow live (`in-production`). `registry/SCHEMA.md` is the contract that makes that possible: it defines the six concept types (Business, LineOfBusiness, Process, Workflow, Note, Function), their required frontmatter, and the rules (enum values, link discipline, banned fields) that every skill's writes and every maintenance pass's lint checks agree on. Write it once per registry, using `references/schema-template.md` verbatim; after that, the leader's own copy is authoritative and every skill re-reads it before writing.

## Platform & Workspace

The procedure below is identical everywhere: the same six phases (0–5), the same node shapes, the same SCHEMA.md. Platforms differ only in how the skill instructions arrive and how files get saved.

| Platform | Skill delivery | Where the registry lives | How files are saved |
|---|---|---|---|
| Claude Code | handsonai plugin | `registry/` in the workspace | directly |
| ChatGPT desktop (Codex) | same SKILL.md dirs at `~/.agents/skills/` (user-level default) or repo `.agents/skills/` (optional pin) | `registry/` in the workspace | directly |
| Claude desktop app | handsonai plugin (installed once, shared with Claude on the web) or skill ZIP | `registry/` inside the working folder the leader selects in the chat | directly |
| Claude on the web | handsonai plugin (paid plans; same install as the Claude desktop app) or skill ZIP (Releases channel) | `ai-workspace/registry/` (or the leader's own working folder) in Google Drive, or OneDrive on a work or school account | through the drive connection |
| ChatGPT web (paid plans) | handsonai plugin via Plugins > Add marketplace, or Personal Skill upload (same ZIP) | `ai-workspace/registry/` (or the leader's own working folder) in Google Drive, or OneDrive on a work or school account | through the drive connection |
| Microsoft 365 Copilot (Cowork) | Cowork skills (the plugin archive or a skill ZIP) | `ai-workspace/registry/` (or the leader's own working folder) in OneDrive, separate from Cowork's own folder | Cowork's own OneDrive edits |
| Gemini Spark / Gemini Enterprise | skill ZIP via Skills > Upload | wherever the leader saves | print-to-save |

A few rules follow from that table:

- **(a) Assistant-agnostic procedures.** Everything in this file (the phases, the write rules, the interview questions) is written for "your AI assistant" in general. Platforms differ only in delivery and saving, never in what gets written or asked.
- **(b) Save through the drive; print only as the fallback.** On the web and in Cowork, write every file through the drive connection into `registry/` in the working folder. Where a connection can only create files but can move and rename them, follow the drive-saving rule in the `indexing-registry` skill's `references/registry-bundle.md` (§2, rule 8). Only where there are no files and no connection that can save does the skill fall back to print-to-save: it gives each file complete, with its exact location, and says plainly what is unsaved — never "I've created" for a file it only gave, and never leave the leader assuming a file landed somewhere it didn't. A file the leader would have to download doesn't count as saved.
- **(c) Home: any folder; GitHub is optional.** A local folder, a drive folder, or a GitHub repository all work: the bundle is plain Markdown with relative links and never depends on Git. Never require GitHub; mention it only for what it adds (an in-browser editor, version history, and the template repo's automatic check on every save).
- **(d) One skill artifact, three channels.** The same agentskills.io-standard SKILL.md, packaged by `build-skill-zips.sh` in the handsonai-plugins repository, is what Codex desktop scans locally, what ChatGPT web's Personal Skills accepts as an upload, and what Claude and Cowork accept as an uploaded skill. There is no separate packaging for each.
- **(e) Repo-checked-in skills are optional, not the default.** Codex desktop can read `.agents/skills/` inside the leader's repo, but the default is a user-level install (`~/.agents/skills/`): checking a skill into every repo it's used in invites version drift between repos. Only pin a repo-local copy when the leader has a specific reason to.

**Platform note (Claude):** the closing step always generates the visual dashboard as a file that opens in any browser. On Claude, also offer it as a Claude Artifact — a private page the leader can open from Claude any time and share with a link — on its own line, using the interview guide's wording. The Artifact is in addition to the file, never instead of generating it — except on print-to-save on Claude, where no file can be generated and the Artifact is how the leader sees the dashboard.

## Where the files live

Settle this before anything else, because every later step reads and saves in the same place.

- **Claude Code and Codex:** the registry is `registry/` in the workspace. Nothing is asked.
- **Claude desktop:** the registry goes inside the working folder selected in this chat. When this is the leader's first framework skill and the chat has no folder selected, the first message is N-F12, said exactly, with its *Why* when the leader asks why:

  > "Your AI work lives in one working folder on your computer: your AI Registry, your workflows and your knowledge graph. Select your working folder in the prompt window. If you don't have one, make a folder called ai-workspace, for example in Documents, and select that. Open each step of the framework in a new chat with that folder selected. Say 'done' when it's selected[, or 'use my drive' to keep it in [Google Drive / OneDrive] instead]."
  >
  > *Why:* "Every step reads and saves these files, so a new chat needs to find them."

  If the leader can't find where to select a folder, say you couldn't verify the exact steps and that they can select it their own way (the platform registry's `claude` entry, `capabilities.desktop_add_folder`, holds what is verified); never make up a menu path. On "use my drive", continue as on the web. When the selected folder holds a lot besides AI work, the big-folder follow-up (below) comes first; on "go ahead", make `ai-workspace` inside it as the working folder and say in one line, in your own words, to select that folder in each later framework chat.
- **On the web and in Microsoft 365 Copilot (Cowork):** take the location from the start phrase ("set up my registry. My files are in Google Drive, in ai-workspace."), or find the working folder: a folder named ai-workspace in the drive; else a folder holding `registry/SCHEMA.md` or `framework/`, taken as the working folder once the leader confirms it in one line. When there's no working folder yet (this is the leader's first framework skill), ask the storage question as the first message, before the opening and before anything is read or written. Offer only a drive whose connection is on and can write. Say N-F1 exactly; in Cowork, its Microsoft 365 form:

  > "Where's your working folder? It's the one folder that holds your AI Registry, your workflows and your knowledge graph. If you already have one in your [Google Drive / OneDrive], tell me its name. If not, I'll make a private folder called ai-workspace there. The connection reaches your whole drive, but I'll only read and save inside your working folder, and never share or delete anything. Please run each step of the framework in a new chat that isn't inside one of your [Claude / ChatGPT] Projects. Say 'go ahead', or tell me your folder's name."

  Microsoft 365:

  > "Where's your working folder? It's the one folder that holds your AI Registry, your workflows and your knowledge graph. If you already have one in your OneDrive, tell me its name. If not, I'll make a folder called ai-workspace there, separate from Cowork's own folder. Cowork can see your whole OneDrive, but I'll only read and save inside your working folder, and never share or delete anything. Please run each step of the framework in a new Cowork chat. Say 'go ahead', or tell me your folder's name."
  >
  > *Why:* "Every step reads and saves these files, so a new chat needs to find them."

  Never assume the leader has a working folder, or that they don't. On "go ahead", make `ai-workspace/` with `registry/` inside it. When they name a folder, use it: first check it can be read (if it can't, say so in one line and ask for it again), then make `registry/` inside it. Never make `framework/`: the first step that saves a workflow makes it. Analyze and every later step take the location from the start phrase, so the storage question is never asked twice.
- **A folder that holds a lot besides AI work** (many files or folders that aren't `registry/`, `framework/` or `knowledge/`, such as a drive's top level or Documents): before saving anything, the big-folder follow-up, said exactly:

  > "That folder holds a lot besides your AI work. I'd suggest a new, clean folder called ai-workspace instead, so the framework only ever touches your AI work. Say 'go ahead', or 'use it anyway'."

  On "go ahead", make `ai-workspace` (on the web, in the drive; on Claude desktop, inside the selected folder) and use it as the working folder; on "use it anyway", use the folder they named or selected.
- **No files and no connection that can save** (Gemini, or a web chat with no drive connection on): print-to-save, with N-F6 in the opening.

Never ask the leader to approve a path; say where the registry is saved in the opening (see the interview guide).

## Before scaffolding

Before running the interview, check what's already in the working folder (locally, the workspace):

0. **A `knowledge/` folder exists** → leave it alone — never write to it or lint it; Phase 0 may read it as an intake source. It is the business knowledge graph, a different OKF bundle with its own `SCHEMA.md` and its own lint (built by `building-knowledge-graph`). Say so in one sentence and continue with the registry checks below.
1. **`registry/SCHEMA.md` exists** → this is **gap-filling mode**, not a fresh scaffold. List which concept types have zero nodes and which typed directories are missing their `index.md`, tell the leader what's missing, and offer to fill only those gaps. Never overwrite an existing node, and never rewrite `SCHEMA.md` once the leader has one — their copy is authoritative from here on.
2. **No `registry/SCHEMA.md`** → run the interview below from Phase 0. Files left by an earlier version of the framework are never read, moved or converted: the registry is set up fresh beside them.

## The interview

Six phases (0–5), run in order. Follow `references/interview-guide.md` for the exact opening, questions, follow-ups, worked examples, and fast paths for each phase — this section is the map; that file is the script.

**How the leader experiences it.** The leader hears an opening, then four parts, then the close — never phase numbers:

| Part (what the leader hears) | Phases | Level of the registry |
|---|---|---|
| — (opening and setup) | 0 | — |
| Part 1 of 4 — Your business | 1 | Business |
| Part 2 of 4 — How it's organized | 2 | Lines of Business |
| Part 3 of 4 — Who does the work | 3 | Functions |
| Part 4 of 4 — The processes that deliver it | 4 | Processes |
| — (close) | 5 | — |

Rules for every message in this interview:

- **One question per message.** Never number two or three questions in one message.
- **Signpost each part** in one line: "Part 2 of 4 — How it's organized: your lines of business."
- **Play back in plain words, never as a file.** Show a draft as labeled plain text (Name · What it does · Website · Goals for this year), never as raw frontmatter, Markdown headings, or file names. Write the file format behind it, and offer "Want to see the file itself?" once.
- **Confirm before writing.** Play back each complete entry (or list) once and write it only after the leader confirms. If you interpret an answer (two goals or three?), ask; don't write your reading and offer to fix it.
- **Never mention a check that found nothing**, a lint rule, or the maintenance pass as the reason for a question. Give the leader's reason instead.
- **Explain as you ask.** The interview guide's question blocks give each question's *Why*, *Example*, and *Not sure?*. If the leader says "skip the explanations", keep only the *Why*.
- **No time and no step numbers.** Never say how long the interview or any part takes, and never number the framework's steps: name the step ("Analyze").

**Phase 0 — Home and sources.** The storage question, when it's needed, comes first (*Where the files live*); then the opening. Detect, don't ask, how files are saved: locally the registry goes at `registry/` in the workspace (Claude Code, Codex) or inside the working folder selected in the chat (Claude desktop); on the web and in Cowork it goes in `registry/` in the working folder, through the connection; only with no files and no connection that can save is it print-to-save, said once with N-F6. The first message after the storage question is the opening — nothing before it about refreshing, maintenance, checks, or what the folder lacks. Open with the opening in `references/interview-guide.md` (what a registry is, the outline it builds, what the leader leaves with, its parts), and confirm where the registry will be saved in one sentence (N-F3's promise clause) — don't ask the leader to approve a folder path. Ask whether the empty skeleton already exists (template repo or Download ZIP) only on print-to-save, where you can't look; otherwise, look. Then, one message each: **ask who the registry is for** (a business you own, a company or unit you lead, your role inside an organization, or your personal life — `references/personas.md` sets the vocabulary for every later question and is never stored in a node); **scan the framework folder** (locally, the workspace) for `knowledge/`, `sops/`, `process-guides/`, `CLAUDE.md`/`AGENTS.md`, and a prior opportunity report, and mention the scan only if it found something you'll draft from (one plain sentence; never list what wasn't there); and **ask for documents** the leader can paste or upload — an org chart or team list, job descriptions, a strategy or OKR document, a services page, a process inventory. `references/intake-sources.md` maps each source to the nodes it drafts. Say once: "I'll propose, you confirm. Nothing about your business gets saved until you confirm it." (Name functions for the area or role, never for the person, unless the leader asks — but don't say "functions" before Part 3 defines it.) Then write the skeleton and begin Phase 1. The template repo (`https://github.com/jamesgray-ai/ai-registry-template`) is only the answer to "where's the template repo?" — never a prerequisite. Follow `references/interview-guide.md`.

**Phase 1 — Business.** One Business node: name, one-sentence identity, `status` (set it yourself — `active` for a business the leader runs; ask only if they describe something not yet launched or winding down), optional `url`, and the two or three outcomes that matter most this year, written as a bulleted list under a `## Objectives` heading in the body, below the identity sentence and above `# Lines of Business` (prose only; no frontmatter field; `analyze` reads it so the leader is never asked for objectives twice). Almost always exactly one business per registry; for a professional it is their team, for the personal persona it is the person or household. Follow `references/interview-guide.md`.

**Phase 2 — Lines of Business.** One or more LineOfBusiness nodes in a curated, ordered list under the Business node. Define the term before the first question. Order the draft yourself, following the leader's objectives; don't ask a separate ordering question — the leader can move lines when they confirm the grouping. Set each line's `status` yourself; ask about one only when a source suggests it is new or paused. Solo consultants get one default LOB named after the business — no artificial splitting. Follow `references/interview-guide.md`.

**Phase 3 — Functions.** Offer the starter set (Marketing, Sales, Service Delivery, Operations, Product, Customer Success, IT/Engineering) to founders and leaders, and only when no Phase 0 source covered Functions; the leader trims and renames it. Write only the functions that will own a process: a Function that owns none is a lint warning (`function owns no processes`), and a fresh registry must lint with no such warning — so once Phase 4 has named the processes, ask once about any that truly own none, and write the Function nodes only then, with the processes: a function the leader drops is never written (Functions have no `status`; nothing is deleted, and nothing is moved to any other folder). Professionals name the groups they hand work to; the personal persona names roles, never the starter set. Every Function node is written with its empty GENERATED `# Owns` block from the start. Define the term before the first question, using the persona's wording (`references/personas.md`): functions are the teams or departments that do the work — for a solo founder, the hats they wear — as distinct from lines of business, which are what the business offers. Carry the leader's answers forward: a function they chose to keep or drop stays that way in Phase 4 and Close. Follow `references/interview-guide.md`.

**Phase 4 — Processes.** Per LOB, the three to five processes that deliver it — where the time, money, and customer outcomes actually flow. Define the term before the first question. Order each line's processes yourself in the draft, by value-chain order and the leader's objectives; **never ask the leader to rank them** — they can't judge that yet, and Analyze asks which processes matter most before it walks them. Don't ask for SOPs or guides: fill `guide:` only when a Phase 0 document already turned one up. Play the draft back in the labeled layout in the interview guide. Map how the business delivers, never where AI might help: Analyze decides where AI fits and files each workflow it finds under one of these processes; right now you want the map, not a shortlist. Not exhaustive: Analyze grows this later. Each needs a required `owner:` function slug. Once Processes name their owners, the owning Functions' `# Owns` blocks written empty in Phase 3 are now stale — that's expected, not an error; the Phase 5 maintenance pass regenerates them, and lint only ever flags stale content as a warning, never a blocker. Follow `references/interview-guide.md`.

The Brightwork examples in `references/example-registry.md` are shown, never copied. Every node written is the leader's real business.

When Phase 0 surfaced a source that covers a phase, open that phase with the draft rather than the blank question — "From your [source], here's what I'd write … anything wrong or missing?" — and write only what the leader confirms. The blank-slate question remains for anyone with nothing to bring. Sources shorten the phases.

**Phase 5 — Close.** A Function the leader chose to drop at the end of Phase 4 (that is the only time the unowned-function question is asked) was never written, so there is nothing to delete — a Note only if the leader volunteered an insight during the interview (never prompt for one), the empty `registry/workflows/index.md` (Analyze fills the workflows in — this scaffold never names one), founding `log.md` entry, and hand-off — see Close below. Follow `references/interview-guide.md`.

If the leader can't finish a phase, write what they have confirmed, note the gap for the close-out summary, and move on — missing nodes are homework for later; fictional ones are never an acceptable substitute.

## Write rules

- **The leader's `registry/SCHEMA.md` is authoritative once it exists.** Re-read it immediately before every write in this skill, including during gap-filling — never write from memory of what the schema template said.
- **Stamp `generated: { by: process:scaffolding-registry, at: <YYYY-MM-DDTHH:MM:SSZ> }`** (single-line flow map; `at` is the moment of the write as a UTC instant, such as `2026-10-24T15:04:05Z`) on every node this skill creates or edits. Never write a bare date.
- **Function nodes are always written with their empty GENERATED `# Owns` block** at creation time — never deferred to a later maintenance pass. A Function missing that block is a lint error, because the maintenance pass has nothing to fill.
- **Slugs are plain ASCII kebab-case** — fold accents (`Café Orders` → `cafe-orders`), `&` → `and`, strip other punctuation — so filenames and links agree on every platform.
- **Every new node gets added to its typed directory's `index.md`.** A concept file with no entry in its directory index is a lint error; write or update the index in the same pass as the node. An index with no nodes yet has exactly this body — the heading, a blank line, and `_No entries yet — your AI assistant fills this index as nodes are added._` — which is the text compose writes, so a fresh scaffold composes with no file rewritten. Index entries use bundle-root-relative leading-slash links — `[Client Onboarding](/processes/client-onboarding.md)`, never a bare same-directory link like `[Client Onboarding](client-onboarding.md)`, which the schema's link discriminator resolves from the registry's parent folder and lint flags as broken.
- **On a drive,** every file is saved through the connection, by the drive-saving rule in the `indexing-registry` skill's `references/registry-bundle.md` (§2, rule 8). Nothing on a drive is ever shared, trashed or deleted.

## Close

End Phase 5 by writing a founding `registry/log.md` entry describing the scaffolding run (what was created), and making sure every typed directory has an `index.md`, even a stub one — including `registry/workflows/index.md`, which starts empty because this skill writes no Workflow node; the `analyze` skill adds the first ones.

Then invoke the `indexing-registry` skill for the first maintenance pass: it lints the new bundle, generates the Tier 1 `REGISTRY.md` — which is written in the registry's parent folder, next to `registry/` and not inside it — and **always** generates the Tier 2 visual dashboard, `registry-dashboard.html`. The dashboard is not an option at setup: it is the leader's window into the registry, and a leader offered it as one of "two options" skips it. On the web the pass saves through the drive connection, like every other save. This is a best-effort hand-off — if the maintenance pass can't run for some reason, say so plainly rather than leaving the leader assuming it happened. The lab should end with something visual on screen, not a blank terminal. On print-to-save the hand-off produces files to save rather than saved files: give the founding `log.md` entry, every typed `index.md` you updated, and a complete `REGISTRY.md` composed per `indexing-registry`'s rules, each with its exact location, and tell the leader the set is complete.

Then deliver the close exactly as the interview guide gives it (saved and print-to-save differ): what was made (counts), where it's saved, what `REGISTRY.md` and the dashboard are and how to open the dashboard, that the leader can reshape the registry any time by asking, and Analyze's paragraph (N-A7) with Analyze's start phrase and the location. Say nothing about lint results or GENERATED blocks; offer to save a version only when the folder is a git repository (detected with `git rev-parse --show-toplevel`), in the guide's plain wording; commit locally and don't push as part of that offer. If the leader says now, invoke the `analyze` skill; it knows the registry was built in this conversation, so it says its opening, skips the registry summary and goes to the lens, and asks no second storage question.
