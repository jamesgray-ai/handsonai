---
title: Competitive Intelligence Brief — Workflow Definition
workflow: Competitive Intelligence Brief
lob: learning
category: teaching-example
owner: James Gray
last_reviewed: 2026-05-11
notion_workflow_url:
framework_phase: deconstruct
definition_type: step-decomposed
---

# Competitive Intelligence Brief — Workflow Definition

## Scenario Metadata

| Field | Value |
|---|---|
| **Workflow Name** | Competitive Intelligence Brief |
| **Description** | Given a competitor name, research the competitor's recent moves and produce a structured brief — positioning, product moves, hiring signals, public commentary — then write findings to a structured context file. Run repeatedly, the workflow's outputs accrete into a self-improving knowledge base for that competitor. |
| **Outcome** | A publish-ready structured brief on the competitor's recent moves, plus an updated `knowledge/competitors/{name}.md` file with new findings appended (date-stamped, source-linked). |
| **Trigger** | Manual on demand, or scheduled per competitor on a cadence (e.g., weekly for top 3 competitors, monthly for second tier). |
| **Type** | Recurring / scheduled, with context that compounds across runs. |
| **Business Objective** | Stay current on competitor moves without paying the daily attention tax. Turn one-off research effort into an institutional asset that survives team turnover. |
| **Current Owner** | Workflow operator (the person tracking the competitor); knowledge base is shared with their team. |
| **Lens** | Individual or team. |
| **Definition Type** | Step-Decomposed. |

---

## How to Invoke

**Required input**: Competitor name (e.g., `Acme Corp`). The workflow resolves the knowledge file path as `knowledge/competitors/<kebab-cased-name>.md`.

**Optional inputs** (provided at invocation; each has a defined fallback if omitted):

| Input | Type | Used By | Fallback if omitted |
|---|---|---|---|
| `cadence_window` | Text (e.g., "last 30 days") | Step 2 (scoping searches) | Derived from `last_updated` in the existing knowledge file; "since project inception" on first run. |
| `competitor_aliases` | List of strings (known product/exec names) | Step 2 (broadening search) | Search uses competitor name only on first run. Aliases are expected to accrete in the knowledge file over time and be loaded by Step 1. |
| `output_path` | Path | Step 3 (where the brief is saved) | `briefs/{competitor}/{date}.md` |

---

## Refined Steps

### Step 1 — Load existing competitor knowledge

- **Action**: Read the competitor's existing knowledge file if it exists, or recognize that this is the first run.
- **Sub-steps**:
  1. Check whether `knowledge/competitors/<competitor-name>.md` exists.
  2. If yes, parse the file's structured sections; capture the `last_updated` date.
  3. If no, prepare to create the file from scratch in Step 4.
- **Decision Points**:
  - File exists and is fresh (updated within the last cadence window) → load and proceed.
  - File exists but is stale → load, proceed, but flag the staleness in the digest.
  - File does not exist → first-run path; the workflow will create it in Step 4.
  - File exists but cannot be parsed → notify the operator; do not overwrite.
- **Data In**: Competitor name; `knowledge/competitors/` folder.
- **Data Out**: The existing knowledge for the competitor (the file's contents and a `last_updated` reference, plus a flag for whether this is a first run).
- **Context Needs**:
  - A schema convention for the knowledge file (how its sections are organized so the workflow knows what to read and where to write).
  - The `knowledge/competitors/` folder structure.
- **Failure Modes**:
  - File schema mismatch (someone hand-edited it into an inconsistent state) — notify the operator; skip the run rather than overwrite.
  - Folder doesn't exist yet on first ever run — create it.

### Step 2 — Research the competitor's recent moves

- **Action**: Use web search to gather signals about the competitor's recent activity, scoped to the cadence window — "what's new since the last update."
- **Sub-steps**:
  1. Search for product launches and announcements (company blog, press releases, product pages).
  2. Search for hiring signals (open roles, leadership announcements, public LinkedIn changes for known executives).
  3. Search for public commentary (analyst reports, exec interviews, podcast appearances, customer case studies).
  4. Cross-reference findings against the existing knowledge from Step 1 to identify what's genuinely new vs. a restatement of what's already known.
- **Decision Points**:
  - No new findings since last run → skip the update; produce a "no change" digest.
  - A new finding contradicts something already in the knowledge file → produce the brief AND flag the conflict for human review.
  - Single-source claims → mark as lower-confidence (not authoritative) regardless of plausibility.
- **Data In**: Competitor name; existing knowledge and `last_updated` from Step 1; access to web search; optional `competitor_aliases`.
- **Data Out**: Raw research findings — a list of claims grouped by category (product, hiring, commentary), each carrying a source URL and a confidence level, with conflicts against existing knowledge flagged.
- **Context Needs**:
  - A web search capability.
  - Optional: per-competitor search hints (aliases, product names, exec names) — accrete in the knowledge file over time.
- **Failure Modes**:
  - Web search timeout or rate limit — the workflow may produce a partial run; surface this in the digest.
  - Hallucinated findings — every claim must carry a source URL; claims without sources should be dropped.
  - Paywalled sources — note the paywall in the source reference; do not invent the content behind it.

### Step 3 — Synthesize the structured brief

- **Action**: Turn the raw research findings into a structured brief in a defined format.
- **Sub-steps**:
  1. Categorize findings into the brief's sections: positioning, product moves, hiring signals, public commentary, open questions.
  2. Draft each section using the findings; cite sources inline.
  3. Add a "what changed since last run" summary at the top.
  4. Format output as markdown with consistent section headings.
- **Decision Points**:
  - Findings too thin to populate all sections → produce a partial brief; explicitly mark empty sections rather than padding.
  - Existing schema doesn't fit (e.g., competitor pivots to a fundamentally new business model) → produce the brief in the existing schema AND flag that the schema may need to evolve (an Improve-step signal).
- **Data In**: Step 2 findings; Step 1 existing knowledge.
- **Data Out**: Markdown brief — full document, brand-neutral, ready to share with the team.
- **Context Needs**:
  - A brief template (section structure, length norms).
  - Optional: examples of well-structured competitor briefs for voice anchoring.
- **Failure Modes**:
  - Generic "they announced a new feature" content with no analysis — each section should call out the *implication*, not just the fact.
  - Capability/scenario mismatch — the brief mentions a capability the cited source doesn't actually support.
  - Brief duplicates the previous run's brief — should be prevented by the Step 2 "what's genuinely new" cross-reference; if not, flag for review.

### Step 4 — Update the knowledge file

- **Action**: Write the workflow's findings back to the competitor's structured context file. This is the step that turns a one-off workflow into a self-improving knowledge base.
- **Sub-steps**:
  1. **First-run path** (file doesn't exist): create `knowledge/competitors/<competitor-name>.md` with the schema header; seed it from Step 1's initial context and Step 2's highest-confidence findings; set `last_updated`.
  2. **Update path** (file exists): append new findings with date stamps and source links; do not overwrite previously confirmed content; if a finding conflicts with existing content, append it AND add a flag note for a later reconciliation pass.
  3. Update `last_updated` date.
- **Decision Points**:
  - First run vs. update — branches based on whether the file existed in Step 1.
  - Conflict with existing content → append as a new finding + flag; never silently overwrite.
- **Data In**: Step 3 brief; Step 2 raw findings; Step 1 existing knowledge.
- **Data Out**: Updated `knowledge/competitors/<competitor-name>.md`.
- **Context Needs**: The schema convention for the knowledge file — what each section is for and how new findings should be added. (This convention is what Session 10's self-improvement work will formalize.)
- **Failure Modes**:
  - File write conflict (concurrent runs could collide) — flag for Design to resolve.
  - Malformed markdown output — risk to flag for Design; mitigation strategy (template, validator, both) is a Design decision.
  - Findings explosion (every run adds many low-signal items, bloating the file) — flag for Design; bounding logic is a Design decision.

### Step 5 — Output the digest

- **Action**: Produce a short digest summarizing what changed and where to read more.
- **Sub-steps**:
  1. Summarize 3–5 highest-signal findings as bullet points.
  2. Link to the full brief from Step 3 and the updated knowledge file from Step 4.
  3. Surface any flagged conflicts or schema-evolution signals for human attention.
- **Data In**: Step 3 brief; Step 4 update result; any flags raised in earlier steps.
- **Data Out**: Markdown digest — short enough to skim in 30 seconds.
- **Context Needs**: None beyond what's already produced.
- **Failure Modes**: None significant; the digest is the easiest step.

## Optimization Summary

Changes applied to a naive "search → write a brief" version:

- **Added** Step 1 (load existing knowledge) as a distinct step. Reason: the whole point of this workflow is that it compounds — without reading existing context, every run starts from scratch.
- **Flagged** Step 2's three searches (product, hiring, commentary) as having no data dependency on each other. Reason: they're a parallelism opportunity; how (or whether) to exploit that is a Design decision.
- **Required** every Step 2 claim to carry a source URL. Reason: the #1 failure mode for research workflows is hallucinated findings.
- **Branched** Step 4 into first-run and update paths. Reason: the workflow needs to bootstrap the knowledge file on first run and grow it on subsequent runs without conflating the two.
- **Added** explicit conflict handling (new finding contradicts existing content). Reason: this is the most informative signal the workflow produces — both about the competitor and about whether the schema is still serving you (an Improve-step trigger).
- **Eliminations**: none — every step earns its place.
- **Optimizations declined**: a human review checkpoint between Step 2 and Step 3 (would slow the workflow without materially improving output for a well-tuned brief template).

## Step Sequence and Dependencies

- **Sequential critical path**: Step 1 → Step 2 → Step 3 → Step 4 → Step 5.
- **Within Step 2**: the three searches (product, hiring, commentary) have no data dependency; the cross-reference sub-step (4) depends on all three. Whether to run them concurrently is a Design decision.
- **Single owner**: workflow operator. No role transitions during a single run.
- **Cross-run dependency**: every run depends on the previous run's Step 4 output (the updated knowledge file). This is the compounding mechanism.

## Context Shopping List

| Artifact | Description | Used By Steps | Status | Key Contents | AI Accessible? | Readiness Notes |
|---|---|---|---|---|---|---|
| `knowledge/competitors/{name}.md` | The competitor's structured context file | 1, 4 | Created on first run | Schema-structured competitor knowledge | Yes | Created by the workflow on first run; subsequently read AND written every run. |
| Schema convention for the knowledge file | Explains how the file's sections are organized and how new findings should be added | 1, 4 | Needs definition | Section conventions, append/reconcile rules | Yes | The convention is introduced in Session 9 and formalized in Session 10's self-improvement work. |
| Web search capability | Source of competitor signals | 2 | Available on platform | Web search results | Yes | Treat as a platform capability to be selected in Design. |
| Brief template | Section structure for the synthesized brief | 3 | Needs creation | Section headings, length norms | Yes | Lightweight; can live inline in the workflow's prompt or as a separate template file — Design decides. |
| Per-competitor search hints (optional) | Aliases, product names, exec names | 2 | Optional; accretes over time | Search-term hints | Yes | Lives inside the per-competitor knowledge file. |
| Output location for briefs | Where the rendered brief is saved (separate from the knowledge file) | 3 | Pre-built / configurable | — | Yes | Default `briefs/{competitor}/{date}.md`; the knowledge file is the persistent companion. |

### Out of Scope (separate workflows)

- A periodic **reconciliation cycle** that resolves flagged conflicts and surfaces stale claims — extended into the workflow itself during Session 10's self-improvement work.
- A **digest aggregator** that rolls up all competitor digests into a weekly newsletter — downstream workflow.
- **First-time competitor onboarding** (writing the initial high-confidence context from scratch based on prior knowledge) — handled out-of-band; the workflow seeds the file conservatively on first run and expects high-confidence content to be hand-curated over time.

---

**Workflow Definition complete. Ready for Session 9's live Design step — turning this into a Building Block Spec.**
