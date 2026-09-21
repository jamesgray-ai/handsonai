---
title: Knowledge Graph Setup
description: Build your business knowledge graph — a Markdown knowledge bundle about the work you do, written and maintained by your AI assistant from an interview
schema_type: HowTo
howto_steps:
  - name: Open your project folder in a tool that writes files
    text: Claude Code, Cowork, or the ChatGPT desktop app's Codex view. Open the folder that will hold your knowledge graph. A browser chat window cannot build one.
  - name: Say "Build my knowledge graph."
    text: Your assistant confirms the folder, looks at what is already there, makes a raw/ folder for your documents, and interviews you (about 30 minutes) about the work you, your team, or your company does.
  - name: Approve the type list, then send the word build
    text: Your assistant proposes four to seven kinds of things and the sentences that connect them, writes them to types.md when you approve, and builds the knowledge/ folder only when you send the single word "build".
  - name: Run the loop once
    text: Ingest one document, ask one question across a connection, run lint, and confirm one page. Then seed the graph on your real material.
---

Your **knowledge graph** is what your AI reads before it answers a question about your work: your clients, offerings, processes, people, tools, and policies, one Markdown page per concept, linked to each other, written and kept current by your AI assistant. It lives in a `knowledge/` folder on your computer, in an open format called the [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md), so it opens in any editor and moves to any tool.

The pattern comes from [Andrej Karpathy's LLM wiki note](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): raw sources you never edit, a wiki of pages the AI maintains, and a schema that disciplines how it maintains them, with three operations — ingest, query, lint — that keep it alive.

New to Markdown? See [Markdown Basics](../markdown-basics/).

## What Your Knowledge Graph Is

A folder that looks like this once the build has run (Claude Code names; in the ChatGPT app `.claude/` is `.agents/` and `CLAUDE.md` is `AGENTS.md`):

```
my-business/                     ← you open your AI here
├── .claude/skills/              ← two procedures the build writes for you
│   ├── ingest/SKILL.md             fold a document into the pages it affects
│   └── lint/SKILL.md               sweep every page against the rulebook
├── raw/                         ← your documents, exactly as they arrived; read, never edited
├── knowledge/                   ← the graph itself
│   ├── clients/                    one folder per kind of thing
│   │   ├── acme.md                 one page per real one
│   │   └── bowman.md
│   ├── engagements/
│   ├── playbooks/
│   ├── notes/                      answers worth keeping, and knowledge with no other home yet
│   ├── overview.md                 the page you would hand a new hire
│   ├── index.md                    every page, one line each
│   ├── log.md                      what changed, and when
│   └── SCHEMA.md                   the rulebook: your kinds, how they connect, the conventions
├── CLAUDE.md                    ← standing rules your AI reads every session
└── types.md                     ← the blueprint you approved before the build
```

`raw/` is what you received; `knowledge/` is what you learned. The build keeps them apart on purpose.

## Not the AI Registry

The [AI Registry](../ai-registry-setup/) records what you build *with* AI: your workflows, the skills and agents that power them, the processes they serve. The knowledge graph records what your business *knows*: clients, offerings, how the work is done. Both are Open Knowledge Format bundles. They live side by side in the same folder, `registry/` and `knowledge/`, and never merge. If you already have a registry, the knowledge graph build leaves it untouched.

## Before You Start

1. **The Hands-on AI skills are in your AI tool.** The build is run by a skill called `building-knowledge-graph`. If you installed the Hands-on AI plugin (Claude or ChatGPT), you already have it. If you add skills by uploading ZIP files (Cursor, Codex CLI, Gemini CLI, or a plan that blocks plugins), upload one of these:
   - [building-knowledge-graph.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/building-knowledge-graph.zip) — skill folder at the root
   - [building-knowledge-graph-flat.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/building-knowledge-graph-flat.zip) — `SKILL.md` at the root, for tools that ask for that

   Haven't set up the skills yet? Follow [Set Up the Skills](../../ai-workflow-framework/skills/) for your tool, then come back here.
2. **A folder for your project.** Any folder works: on your computer, a synced cloud-drive folder, or a clone of a GitHub repository. Open your AI at that folder's root, not inside `knowledge/`. If you made a `my-business` repository for the course, use that.
3. **Two or three real documents about your work** handy: a proposal, a client summary, a process doc, a team charter. The skill asks where they are and makes the `raw/` folder for them. Leave out anything with personal data about identifiable people: payroll, health, individual HR records.
4. **A jotted list** of the five to ten most important named things in your work: clients, products, projects, tools, policies, teams. The interview starts there.

## What You Need

A tool that opens a folder on your computer and writes files into it: **Claude Code**, **Cowork**, or the **ChatGPT desktop app's Codex view**. Cursor, Codex CLI, and Gemini CLI also work with the ZIP. A browser chat window (claude.ai, ChatGPT on the web, Gemini, Microsoft 365 Copilot) cannot build a knowledge graph; the skill will say so and stop.

- **Claude Code:** open Terminal, type `cd ` (with a space), drag your folder into the Terminal window, press Enter, then type `claude` and press Enter. Or open the folder in the desktop app.
- **Cowork:** choose the folder as your working folder when you start.
- **ChatGPT desktop:** in the **Codex** view, create a project, **Edit project → Add folder**, choose your folder, and **Make primary**.

## Build It

Say: *"Build my knowledge graph."*

Your assistant works in phases and never moves on until you say so. Nothing is built until you send one word.

| Phase | What your assistant does | What you do | You know it worked when |
|---|---|---|---|
| **Home** | States the folder it is in, your platform, and what is already there (a registry, an earlier graph, a saved type list) | Confirm the folder; give the name it should record you as | It asked a question and created nothing |
| **Look around** | Makes `raw/`, scans your folder, asks where your documents are, reports what it found | Point it at your documents, or say skip | It said what it found and what it did not, in plain words |
| **Interview** | Asks which work we are mapping (you, your team, the company), then the named things, who you serve, what repeats, what you look up | Answer as you would to a new hire | Every question was answered or skipped for a stated reason |
| **Propose types** | Proposes four to seven kinds of things, each with three real examples, and argues with you | Rename, merge, delete. Push back | You argued with it at least once and the list uses your words |
| **Connect them** | Proposes the sentences between the kinds, using your real examples, and asks what you would look up by following each | Confirm, correct, or strike each sentence | Every kept connection has a heading you chose |
| **Approve** | Writes exactly one file, `types.md`, and stops | Say the list is right | One file exists; nothing else has been created |
| **build** | Constructs `knowledge/`, the rules file, and the two skills | Send **`build`** as its own message | The folder above exists; the report lists graph, rules, skills |
| **Run the loop** | Guides one ingest, one question, one lint, one confirmed page | Drop a document in `raw/`; ask; approve fixes; confirm a page | A page changed with a cited claim; the answer named files; the lint report named files; a page shows `verified` |

While it interviews you, your assistant may show a worked example from a fictional consulting practice. It illustrates the shape of a good answer and is never copied into your graph.

## Keep It Alive

Three operations, all already in your folder:

- **Ingest.** Drop a document in `raw/` and say *ingest it*, or just tell your assistant something you know. It proposes which pages would change and what would land on each, writes after you say yes, and reports every file it touched. Each claim carries a footnote back to its source.
- **Query.** Ask a question about your work. Your assistant reads `index.md` first, opens only the pages that could hold the answer, answers from those pages only, and cites them. If the answer is worth keeping, it offers to file it as a Note.
- **Lint.** Say *lint*. Your assistant reads the rulebook and sweeps every page: contradictions, claims past their date, orphans, connections missing their other side, and pages worth writing. It reports first and fixes only what you approve. Safe to schedule; ingest is not, because it writes.

To see the graph drawn: install [Obsidian](https://obsidian.md), choose **Open folder as vault**, pick `knowledge/`, and click the graph icon.
