---
title: Claude Cowork
description: How to give Cowork the persistent context it needs by writing a CLAUDE.md file.
---

Cowork is what Anthropic calls Claude when you point it at a folder and hand it a goal, instead of driving it turn-by-turn in chat. Cowork reads the files in that folder, works through the steps, and often runs while you're doing something else.

The catch: every session starts cold. Whatever Claude needs to know about you, your folder, and how you work has to live in a file Cowork can read. That file is `CLAUDE.md`.

## Why CLAUDE.md matters in Cowork

In chat, you can correct Claude in real time. In Cowork, you often aren't watching. Anything you'd otherwise re-type — your role, your working style, how the folder is organized, the rules Claude should never break — belongs in the folder's `CLAUDE.md`. If it's not in the file, it's not in the room.

## The one thing to know about CLAUDE.md

Cowork looks for a `CLAUDE.md` file inside the folder you've pointed it at. That file is plain markdown. You create it, you edit it, you keep it current. There's no special syntax, no separate config screen, no slash command to manage it — it's just a markdown file in the folder, loaded at the start of every Cowork session there.

## Best practices

1. **Keep it short.** Aim for under 200 lines. The whole file loads into Claude's working context at the start of every session, and a bloated file gets followed less reliably than a focused one.
2. **Be concrete.** "Save new meeting notes to `Clients/<slug>/notes/YYYY-MM-DD.md`" beats "stay organized." Claude can only follow rules it can actually verify.
3. **Structure with headings.** Claude scans markdown the way a person does. Short sections with clear headers beat walls of paragraph text.
4. **Write what you'd otherwise re-type.** If you've corrected Claude on the same thing twice, that correction belongs in `CLAUDE.md`.
5. **Don't contradict yourself.** If two instructions conflict, Claude will pick one of them more or less arbitrarily. Read the file end to end occasionally to weed those out.
6. **Move long procedures out.** A multi-step workflow isn't a `CLAUDE.md` entry — it's a skill. See [Skills](/agentic-building-blocks/skills/).

## Example CLAUDE.md

Here's a complete, realistic `CLAUDE.md` for a consultant's main Cowork folder. Copy it, edit it for your own work, and drop it into the folder you point Cowork at.

````markdown
# Working with Me

## About me

I'm an independent strategy consultant. My clients are mid-stage B2B SaaS companies, mostly Series B–D. I get hired to do go-to-market diagnostics, pricing work, and the occasional board-prep sprint. The output I produce is almost always one of three things: a short memo (1–3 pages), a deck (10–20 slides), or a working session agenda.

I am not a developer. Don't suggest code or terminal commands unless I ask.

## How I work

- Write in plain, direct language. Short sentences. No marketing voice, no hype words ("leverage", "unlock", "transform"), no em dashes.
- Default to short. If a memo can be one page, make it one page.
- Lead with the answer. Recommendation first, reasoning second, supporting detail third.
- When you draft something for a client, give me the draft to review before doing anything with it. Never send a draft directly to a client.
- If I ask a question and the honest answer is "I don't know" or "I'd need to check X," say so. Don't fabricate.

## Folder layout

- `Clients/<client-slug>/` — one folder per active engagement. Inside each: `notes/`, `drafts/`, `final/`, `meetings/`.
- `Drafts/` — work in progress that isn't tied to a specific client yet (talks, articles, frameworks).
- `Admin/` — invoices, contracts, expense receipts.
- `Archive/` — anything from a closed engagement. Don't put new work here.

## Standing rules

- Date format: `YYYY-MM-DD`. Use it in filenames and inside documents.
- New meeting notes go to `Clients/<client-slug>/meetings/YYYY-MM-DD-<topic>.md`.
- New client deliverables go to `Clients/<client-slug>/drafts/` first. When I approve, move to `final/`.
- Never delete a file without asking me first. If you think something should go, propose it and wait.
- Never move files between client folders without confirming. Cross-contamination of client material is the one thing I cannot have happen.

## Default tools and formats

- Save documents as Markdown (`.md`) unless I ask for Word or PDF.
- For decks, draft the outline and slide-by-slide content in Markdown first. I'll handle layout in Keynote.
- Spreadsheets: CSV by default, Excel if I ask.
- When researching online, give me the sources alongside the summary, not at the end.
````

That's ~60 lines, which is well within the limit and leaves plenty of room to add your own rules as they come up.

## Keeping CLAUDE.md current

Open the file and edit it whenever you notice yourself correcting Claude on the same thing more than once. There's no special UI for managing it — it's a file in your folder, like any other. Reopen it when your role changes, your folder layout changes, or you adopt a new working preference you want Claude to honor from then on.

## A quick mental model

`CLAUDE.md` is the briefing document you hand Cowork at the start of every shift. Keep it focused on the slow-changing facts: who you are, how you work, where things live, what's off-limits. Update it when those facts change. Everything else is conversation.

## Related

- [Getting Started with Claude](/platforms/claude/getting-started/) — set up your Claude account and apps before using Cowork.
- [Claude Projects Setup Guide](/platforms/claude/projects/claude-projects-setup/) — the chat-side Projects feature, for contrast with how Cowork uses folders.
- [Skills](/agentic-building-blocks/skills/) — when a procedure outgrows `CLAUDE.md` and should become a reusable skill.
