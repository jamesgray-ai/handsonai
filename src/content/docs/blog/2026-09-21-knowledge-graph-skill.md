---
date: 2026-09-21
authors:
  - jamesgray
tags:
  - Plugins
  - Knowledge Graph
  - Platform Updates
description: "A new skill builds your business knowledge graph from an interview: types, their connections, a rulebook, and ingest/lint skills, in the Open Knowledge Format."
title: "Build your knowledge graph with one sentence: the building-knowledge-graph skill"
---

The Hands-on AI plugin now includes `building-knowledge-graph`. Open a folder in Claude Code, Cowork, or the ChatGPT desktop app, say *build my knowledge graph*, and the skill looks at what is already there, interviews you about the work a person, team, or company does, and proposes the four to seven kinds of things it runs on and the sentences that connect them. When you approve the list and send the word **build**, it writes a `knowledge/` folder in the [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md), a standing-rules file, and two local skills, `ingest` and `lint`, that keep the graph current. The [Knowledge Graph Setup](/builder-setup/knowledge-graph-setup/) page has everything you need.

<!-- more -->

## What changed

- **New skill: `building-knowledge-graph`** (plugin 7.2.0). It replaces a long pasted prompt from the Claude Builders and Agentic AI for Leaders courses. The interview now starts by reading your folder and your documents, asks concrete questions before abstract ones, and asks for relationships as sentences using your real examples. Nothing is built until you send one word.
- **A Knowledge Graph Setup page** under Builder Setup, beside AI Registry Setup, with the plugin path and both skill ZIPs for tools that take skills as files.
- **The AI Registry and the knowledge graph are now clearly two things.** The registry records what you build with AI; the knowledge graph records what your business knows. `scaffolding-registry` no longer answers to "stand up my knowledge base", and each skill points at the other. Both bundles sit side by side in your folder.
- **OKF links updated.** Google moved the specification to `GoogleCloudPlatform/open-knowledge-format`; every link on the playbook and in the plugin now points there.

## What the build writes

`SCHEMA.md` with your types, their relationships, and the conventions; one folder per type with a page per real thing; an `overview.md` you would hand a new hire; `index.md` and `log.md`; a `notes/` folder for filed answers; and `raw/` beside the bundle for the documents your AI reads and never edits. Every page carries who wrote it and when, and gains a `verified` stamp when you confirm it. Each claim taken from a document carries a footnote back to that document.

Requires a tool that writes files on your computer. A browser chat window cannot build one, and the skill says so.
