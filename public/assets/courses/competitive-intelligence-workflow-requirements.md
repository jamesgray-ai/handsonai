# Competitive Intelligence Brief — Workflow Requirements

## Goal
Given a competitor name, research the competitor's recent moves and produce a publish-ready structured brief — positioning, product moves, hiring signals, public commentary — plus an updated `knowledge/competitors/{name}.md` file with new findings appended, date-stamped and source-linked. The workflow runs on demand or on a per-competitor schedule; run repeatedly, its outputs accrete into a compounding knowledge base for that competitor. The brief and digest are consumed by the workflow operator and shared with their team.

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Competitive Intelligence Brief |
| Description | Research a competitor's recent moves and produce a structured brief plus an updated competitor knowledge file |
| Trigger | Manual on demand, or scheduled per competitor (e.g., weekly for top-tier competitors, monthly for second tier) |
| Owner | Workflow operator (the person tracking the competitor) |
| Lens | Individual |
| Definition Type | Step-Decomposed |
| Business Objective | Stay current on competitor moves without paying the daily attention tax; turn one-off research effort into an institutional asset that survives team turnover |

---

## Steps Overview

1. Load existing competitor knowledge — read the competitor's knowledge file, or recognize a first run
2. Research recent moves — search product, hiring, and commentary signals scoped to the window since the last update
3. Synthesize the brief — turn raw findings into a structured, source-cited brief
4. Update the knowledge file — append new findings, date-stamped and source-linked
5. Output the digest — summarize what changed and where to read more

## Step Details

### Step 1 — Load Existing Competitor Knowledge
- **Goal:** Load the competitor's existing knowledge file and determine whether this is a first run.
- **Inputs:** Competitor name (required invocation input); competitor knowledge file (C1); knowledge file schema convention (C2).
- **Outputs:** Existing knowledge contents and its `last_updated` date; a first-run flag when no file exists.
- **Rules & Edge Cases:**
  - Resolve the file path as `knowledge/competitors/<kebab-cased-name>.md`.
  - File exists and is fresh (updated within the cadence window) — load and proceed.
  - File exists but is stale — load and proceed, and flag the staleness so it surfaces in the digest.
  - File does not exist — take the first-run path; Step 4 creates the file.
  - File exists but cannot be parsed against the schema convention (e.g., hand-edited into an inconsistent state) — notify the operator and stop the run; never overwrite.
  - `knowledge/competitors/` folder missing on the first ever run — create it.
- **Context Needed:** C1, C2

### Step 2 — Research Recent Moves
- **Goal:** Gather sourced signals about the competitor's activity since the last update, across product, hiring, and public commentary.
- **Inputs:** Competitor name; existing knowledge and `last_updated` from Step 1; web search capability (C3); per-competitor search hints from the knowledge file (C1) when available; optional cadence-window override (e.g., "last 30 days") provided at invocation.
- **Outputs:** Raw research findings — claims grouped by category (product, hiring, commentary), each carrying a source URL and a confidence level, with conflicts against existing knowledge flagged.
- **Rules & Edge Cases:**
  - Scope searches to the window since `last_updated`; an invocation-time cadence-window override takes precedence; on a first run, search since project inception.
  - Cover three signal categories: product launches and announcements (company blog, press releases, product pages); hiring signals (open roles, leadership announcements, public LinkedIn changes for known executives); public commentary (analyst reports, exec interviews, podcast appearances, customer case studies).
  - Broaden searches with aliases, product names, and exec names from the knowledge file when available; on a first run, search on the competitor name only.
  - Cross-reference findings against existing knowledge — only genuinely new findings count; restatements of what is already known are excluded.
  - Every claim must carry a source URL; drop claims without sources.
  - Single-source claims are marked lower-confidence regardless of plausibility.
  - A new finding that contradicts existing knowledge is kept AND flagged as a conflict for human review.
  - No new findings — proceed with an empty finding set; Steps 3–5 produce a "no change" result rather than padding.
  - Search timeout or rate limit — a partial run is acceptable; record the gap so it surfaces in the digest.
  - Paywalled source — note the paywall in the source reference; never invent the content behind it.
- **Context Needed:** C1, C3

### Step 3 — Synthesize the Brief
- **Goal:** Turn the raw findings into a structured, publish-ready brief.
- **Inputs:** Step 2 findings; Step 1 existing knowledge; brief template (C4); optional output-path override provided at invocation.
- **Outputs:** Markdown brief — sections for positioning, product moves, hiring signals, public commentary, and open questions, with inline source citations and a "what changed since last run" summary at the top — saved to `briefs/{competitor}/{date}.md` unless an output-path override is provided.
- **Rules & Edge Cases:**
  - Each section states the implication of a finding, not just the fact — no generic "they announced a new feature" content without analysis.
  - Never attribute a capability the cited source does not actually support.
  - Findings too thin to populate all sections — produce a partial brief and mark empty sections explicitly; never pad.
  - No new findings — the brief is a short, honest "no change" note.
  - The competitor pivots so the template no longer fits — produce the brief in the existing template AND flag that the template may need to evolve (an Improve-step signal).
- **Context Needed:** C4

### Step 4 — Update the Knowledge File
- **Goal:** Write the run's findings back to the competitor's knowledge file — the step that turns a one-off workflow into a compounding knowledge base.
- **Inputs:** Step 3 brief; Step 2 raw findings; Step 1 existing knowledge and first-run flag; knowledge file schema convention (C2).
- **Outputs:** Created or updated `knowledge/competitors/<competitor-name>.md` with `last_updated` set to the run date.
- **Rules & Edge Cases:**
  - First run — create the file with the schema header and seed it from the highest-confidence Step 2 findings.
  - Update run — append new findings with date stamps and source links; never overwrite previously confirmed content.
  - A finding conflicts with existing content — append it as a new finding plus a reconciliation flag; never silently overwrite.
  - Concurrent runs could collide on the file — the safeguard (locking, queueing, or a single-runner constraint) is a Design decision.
  - Malformed markdown output would corrupt the file — the mitigation (template, validator, or both) is a Design decision.
  - Many low-signal findings could bloat the file across runs — the bounding logic is a Design decision.
- **Context Needed:** C2

### Step 5 — Output the Digest
- **Goal:** Give the operator a 30-second summary of what changed and where to read more.
- **Inputs:** Step 3 brief; Step 4 update result; any flags raised in earlier steps.
- **Outputs:** Short markdown digest — the 3–5 highest-signal findings as bullets, links to the full brief and the updated knowledge file, and any flags.
- **Rules & Edge Cases:**
  - No new findings — produce a "no change" digest.
  - Flags (staleness, conflicts, partial run, template-evolution signals) always surface here, even when the finding list is empty.
- **Context Needed:** —

## Sequence

- **Sequential steps:** 1 → 2 → 3 → 4 → 5
- **Parallel steps:** Within Step 2, the three search categories (product, hiring, commentary) have no data dependency on each other and could run in parallel; the cross-reference against existing knowledge depends on all three. Whether to parallelize is a Design decision.
- **Critical path:** All five steps.
- **Cross-run dependency:** Every run depends on the previous run's Step 4 output (the updated knowledge file). This is the compounding mechanism.

---

## Context Inventory

| ID | Artifact | Used By | Status | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|
| C1 | Competitor knowledge file | 1, 2, 4 | Needs Creation | Yes | Create as `knowledge/competitors/<competitor-name>.md` — created by the workflow itself on first run | Schema-structured competitor knowledge; `last_updated` date; per-competitor search hints (aliases, product names, exec names) that accrete over time |
| C2 | Knowledge file schema convention | 1, 4 | Needs Creation | Yes | Create during Design/Build — inline in the workflow artifacts or as `knowledge/competitors/README.md` | Section conventions; append and reconcile rules for new findings |
| C3 | Web search capability | 2 | Exists | Yes | Platform capability — specific tool selected in Design | Web search results |
| C4 | Brief template | 3 | Needs Creation | Yes | Create during Design/Build — inline in the workflow's prompt or skill, or as a separate template file (Design decides) | Section headings (positioning, product moves, hiring signals, public commentary, open questions); length norms |

## Acceptance Criteria

### What good output looks like
The brief reads like analysis, not a link dump: every claim carries an inline source link, each section calls out what the finding means for us, and the "what changed since last run" summary at the top can be skimmed in under a minute. The knowledge file grows by appending — nothing previously confirmed is overwritten, and every conflict is visible as a flag rather than silently resolved. The digest tells the operator in 30 seconds whether anything needs their attention.

### Dimensions that matter
- **Source fidelity** — every claim has a working source URL; nothing is attributed beyond what the source supports
- **Novelty** — findings are genuinely new since the last run, not restatements of what the knowledge file already holds
- **Analysis depth** — sections state implications, not just facts
- **Knowledge-file integrity** — appends only; date stamps and source links on every new entry; conflicts flagged, never silently overwritten
- **Digest brevity** — skimmable in 30 seconds; flags impossible to miss

### Minimum bar
Source fidelity and knowledge-file integrity must be right — an unsourced claim or a silent overwrite is a failed run. Thin sections are acceptable if explicitly marked as thin; a "no change" result is acceptable when the window is genuinely quiet.

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Typical run | Established knowledge file; 4–8 genuinely new findings across categories | All brief sections populated with sourced, implication-focused entries; "what changed" summary leads; knowledge file gains date-stamped entries | Inline: "**What changed:** Acme shipped usage-based pricing ([acme.com/blog](https://acme.com/blog)) — undercuts our enterprise tier and signals a move down-market." |
| E2 | First run | Competitor name only; no knowledge file exists | File created with schema header, seeded from highest-confidence findings; brief produced; digest notes the bootstrap | — |
| E3 | Quiet window | Established knowledge file; no new findings since last run | Short "no change" digest and brief note; no padding or invented activity; knowledge file untouched except `last_updated` | — |
| E4 | Conflicting finding | New finding contradicts an entry in the knowledge file | Brief includes the finding; conflict appended to the knowledge file with a reconciliation flag; digest surfaces the conflict for review | — |

## Human Gates

| Where | What requires human input |
|---|---|
| Step 1 | Knowledge file cannot be parsed — the operator is notified and the run stops rather than overwrite |
| Step 5 | Flagged conflicts and template-evolution signals are surfaced in the digest for operator review and later reconciliation |

## Optimization Notes

Changes applied to a naive "search, then write a brief" version:

- **Added** Step 1 (load existing knowledge) as a distinct step — the whole point of this workflow is that it compounds; without reading existing context, every run starts from scratch.
- **Flagged** Step 2's three searches (product, hiring, commentary) as a parallelism opportunity with no data dependency — whether to exploit it is a Design decision.
- **Required** every Step 2 claim to carry a source URL — the top failure mode for research workflows is hallucinated findings.
- **Branched** Step 4 into first-run and update paths — the workflow bootstraps the knowledge file on first run and grows it on subsequent runs without conflating the two.
- **Added** explicit conflict handling (a new finding contradicts existing content) — the most informative signal the workflow produces, both about the competitor and about whether the schema still serves you (an Improve-step trigger).
- **Eliminations:** none — every step earns its place.
- **Optimizations declined:** a human review checkpoint between Step 2 and Step 3 — it would slow the workflow without materially improving output once the brief template is well tuned.

Deliberately out of scope (candidates for separate workflows or later Improve-step evolution): a periodic reconciliation cycle that resolves flagged conflicts and retires stale claims; a digest aggregator that rolls all competitor digests into a weekly newsletter; hand-curated first-time competitor onboarding (the workflow seeds the file conservatively on first run and expects high-confidence content to be curated over time).
