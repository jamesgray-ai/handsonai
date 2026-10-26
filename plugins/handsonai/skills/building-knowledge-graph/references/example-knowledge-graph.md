# Example Knowledge Graph — a consulting practice (FICTIONAL)

Worked example for the interview and build. **Never copy these pages into the user's graph.** Show them as the shape to imitate, then write the user's real work instead. The finished graph must contain no Acme residue.

## The interview, condensed

Scope: the work I do (a solo AI consultant). Named things: Acme Manufacturing, Bowman Foods, Reston Health, the AI Roadmap engagement, the Acme pilot, the kickoff checklist, the discovery interview, Notion, HubSpot. Who for: mid-market operations leaders. Delivered: roadmaps and pilots. Repeats: kickoffs, weekly client check-ins, monthly invoicing. Look up: what we promised each client and when it ends. Systems: HubSpot keeps each client's deals, contacts, and invoices, and is updated whenever one changes.

## `types.md`

```markdown
# The types

## Client
An organization we do paid work for.
System of record: HubSpot (deals, contacts and their details, invoices)
Examples: Acme Manufacturing, Bowman Foods, Reston Health

## Engagement
One piece of contracted work, for one client.
System of record: none
Examples: Acme AI Roadmap, Acme Pilot, Bowman Data Review

## Playbook
A repeatable way we do something.
System of record: none
Examples: Kickoff Checklist, Discovery Interview, Handover Pack

## Note
Anything learned that has no other home yet, and answers worth keeping.
System of record: none
Examples: none yet

# How they connect

- A Client has Engagements. Heading: `# Engagements` on the Client page, `# Client` on the Engagement page. Order: by start date, oldest first.
- An Engagement uses Playbooks. Heading: `# Playbooks used` on the Engagement page, `# Used in` on the Playbook page. Order: no.
```

Tool and Contact were proposed and dropped. Two tools do not earn a type; they are lines on the pages that use them. Contacts did not pass the test: HubSpot already holds them and is updated when one changes, so the Client type declares HubSpot as its system of record and each client page links to its HubSpot record instead of listing contacts.

## The folder after `build`

```
my-business/
├── .claude/skills/ingest/SKILL.md
├── .claude/skills/lint/SKILL.md
├── raw/
├── knowledge/
│   ├── clients/acme-manufacturing.md, bowman-foods.md, reston-health.md
│   ├── engagements/acme-ai-roadmap.md, acme-pilot.md, bowman-data-review.md
│   ├── playbooks/kickoff-checklist.md, discovery-interview.md, handover-pack.md
│   ├── notes/.gitkeep
│   ├── overview.md
│   ├── index.md
│   ├── log.md
│   └── SCHEMA.md
├── CLAUDE.md
└── types.md
```

## A client page after one ingest and one verification

`knowledge/clients/acme-manufacturing.md`, after ingesting `raw/acme-msa-2026.pdf` and the user confirming the page:

```markdown
---
type: Client
title: Acme Manufacturing
description: Mid-market logistics manufacturer, client since 2024.
records: { hubspot: https://app.hubspot.com/contacts/00000000/record/0-2/12345678 }
generated: { by: process:ingest, at: 2026-09-21T15:10:00Z }
verified: { by: human:jamesgray, at: 2026-09-21T15:20:00Z }
stale_after: 2027-03-31T00:00:00Z
sources:
  - id: acme-msa-2026
    resource: ../raw/acme-msa-2026.pdf
    title: Master services agreement, signed March 2026
  - id: call-dana-2026-08-08
    resource: "Call with Dana, 8 August 2026"
---

# Who they are
Family-owned, 400 staff, three factories. Bought by a private equity
firm in 2025, which is why the pace changed.

# What they buy
Two engagements so far: /engagements/acme-ai-roadmap.md and
/engagements/acme-pilot.md. Both fixed-fee.

# How the commercials work
Rates are locked until the agreement renews,[^acme-msa-2026] so any price change waits
for the renewal conversation. They always pay about two weeks late;
plan cash around it.

# Who really decides
Priya Raman is the only real sponsor; nothing moves without her. Dana
Whitlock introduced us and is still a friendly voice, but no longer
has a say.[^call-dana-2026-08-08]

# What I would tell a colleague
They buy on speed, not on price. Do not send a 40-page deck.

# Engagements
1. [Acme AI Roadmap](/engagements/acme-ai-roadmap.md)
2. [Acme Pilot](/engagements/acme-pilot.md)

[^acme-msa-2026]: Master services agreement, signed March 2026
[^call-dana-2026-08-08]: Call with Dana, 8 August 2026
```

Read what that buys: the rates claim traces to a document in `raw/`; the judgment that Dana no longer has a say traces to a conversation and says so; the page announces its own expiry, because the rate lock ends when the agreement renews; and a person has confirmed it, so its trust tier is human-reviewed. What it leaves out matters too: contract dates and amounts, invoices, and contacts' details and roles stay in HubSpot, behind the `records:` link, where they are updated anyway.

## A traversal query

*"Which playbooks have we used with Acme?"* → read `index.md`, open `/clients/acme-manufacturing.md`, follow `# Engagements` to both engagement pages, read each `# Playbooks used`. Answer: the Kickoff Checklist (Acme AI Roadmap, Acme Pilot) and the Discovery Interview (Acme AI Roadmap). Cited: three pages. Offer to file the answer as `/notes/playbooks-used-with-acme.md`.
