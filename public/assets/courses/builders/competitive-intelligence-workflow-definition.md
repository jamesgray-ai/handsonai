---
title: Competitive Intelligence Brief — Workflow Definition
workflow: Competitive Intelligence Brief
lob: learning
category: teaching-example
owner: James Gray
last_reviewed: 2026-05-10
notion_workflow_url:
framework_phase: deconstruct
definition_type: step-decomposed
---

# Competitive Intelligence Brief — Workflow Definition

> **About this file.** This is the workflow definition you'll work from in Session 9 — the Step 2 (Deconstruct) artifact you'd produce yourself if you deconstructed a competitive intelligence workflow from scratch. Pre-built so we can spend Session 9 running the rest of the framework end-to-end on it (`/design` → `/build` → `/test` → `/run`) and shipping a working `competitor-research` skill and `competitor-brief` agent. In Session 10, you'll evolve that workflow into a self-improving system by applying Karpathy's "LLM Wiki" pattern to its structured output.

## Scenario Metadata

- **Workflow Name**: Competitive Intelligence Brief
- **Description**: Given a competitor name, research the competitor's recent moves and produce a structured brief — positioning, product moves, hiring signals, public commentary — then write findings to a structured context file as Rules / Facts / Hypotheses. Run repeatedly, the workflow's outputs accrete into a self-improving knowledge base for that competitor.
- **Outcome**: A publish-ready structured brief on the competitor's recent moves, plus an updated `knowledge/competitors/{name}.md` file with new findings appended as Hypotheses (with date stamps and source links).
- **Trigger**: Manual on demand, or scheduled per competitor on a cadence (e.g., weekly for top 3 competitors, monthly for second tier).
- **Type**: Recurring / scheduled, with context that compounds across runs.
- **Business Objective**: Stay current on competitor moves without paying the daily attention tax. Turn one-off research effort into an institutional asset that survives team turnover.
- **Current Owner**: Workflow operator (the person tracking the competitor); knowledge base is shared with their team.
- **Lens**: Individual or team.
- **Definition Type**: Step-Decomposed.

## Refined Steps

### Step 1 — Load existing competitor knowledge

- **Action**: Read the competitor's existing knowledge file if it exists, or recognize that this is the first run.
- **Sub-steps**:
  1. Check whether `knowledge/competitors/<competitor-name>.md` exists.
  2. If yes, parse the Rules, Facts, and Hypotheses sections; capture `last_updated` date.
  3. If no, prepare to create the file from scratch in Step 4 with seeded Rules.
- **Decision Points**:
  - File exists and is fresh (updated within the last cadence window) → load and proceed.
  - File exists but is stale → load, proceed, but flag the staleness in the digest.
  - File does not exist → first-run path; the workflow will create it in Step 4.
  - File exists but is malformed (schema doesn't parse) → notify operator; do not overwrite.
- **Data In**: Competitor name; `knowledge/competitors/` folder.
- **Data Out**: Structured object — `{ exists: bool, rules: [...], facts: [...], hypotheses: [...], last_updated: date | null }`.
- **Context Needs**:
  - The Session-9-style schema doc that explains the Rules / Facts / Hypotheses convention.
  - The `knowledge/competitors/` folder structure.
- **Failure Modes**:
  - File schema mismatch (someone hand-edited it into an inconsistent state) — fall back to notify + skip the run.
  - Folder doesn't exist yet on first ever run — create it.

### Step 2 — Research the competitor's recent moves

- **Action**: Use web search to gather signals about the competitor's recent activity, scoped to "what's new since the last update."
- **Sub-steps** (2a, 2b, 2c run in parallel; 2d depends on all three):
  1. Search for product launches and announcements (company blog, press releases, product pages).
  2. Search for hiring signals (open roles, leadership announcements, LinkedIn changes for known executives).
  3. Search for public commentary (analyst reports, exec interviews, podcast appearances, customer case studies).
  4. Cross-reference findings against existing Facts from Step 1 to identify what's genuinely new vs. a restatement of what's already known.
- **Decision Points**:
  - No new findings since last run → skip the update; produce a "no change" digest.
  - Conflicting findings (e.g., new source contradicts an existing Fact) → produce the brief AND flag the conflict for human review.
  - Single-source claims → mark as Hypothesis (not Fact) regardless of plausibility.
- **Data In**: Competitor name; existing Facts and `last_updated` from Step 1; access to web search.
- **Data Out**: Raw research findings — list of `{ category, claim, source_url, confidence, conflicts_with_existing }`.
- **Context Needs**:
  - Web search tool (Cowork connector or skill).
  - Optional: a per-competitor search-terms list (handles known aliases, product names, exec names).
- **Failure Modes**:
  - Web search timeout or rate limit — retry once, then notify + partial-run.
  - Hallucinated findings — every claim must have a source URL; claims without sources get dropped.
  - Paywalled sources — note the paywall in the source field; do not invent the content behind it.

### Step 3 — Synthesize the structured brief

- **Action**: Turn the raw research findings into a structured brief in a defined format.
- **Sub-steps**:
  1. Categorize findings into the brief's sections: positioning, product moves, hiring signals, public commentary, open questions.
  2. Draft each section using the findings; cite sources inline.
  3. Add a "what changed since last run" summary at the top.
  4. Format output as markdown with consistent section headings.
- **Decision Points**:
  - Findings too thin to populate all sections → produce a partial brief; explicitly mark empty sections rather than padding.
  - Schema doesn't fit (e.g., competitor pivots to a fundamentally new business model) → produce the brief in the existing schema AND flag a Hypothesis that the schema may need to evolve (this is an Improve-step signal).
- **Data In**: Step 2 findings; Step 1 existing context.
- **Data Out**: Markdown brief — full document, brand-neutral, ready to share with the team.
- **Context Needs**:
  - Brief template (section structure, length norms).
  - Examples of well-structured competitor briefs (optional, for voice anchoring).
- **Failure Modes**:
  - Generic "they announced a new feature" content with no analysis — mitigated by requiring each section to call out the *implication*, not just the fact.
  - Capability/scenario mismatch — the brief mentions a capability the cited source doesn't actually support.
  - Brief duplicates the previous run's brief — caught by the Step 2 "what's genuinely new" cross-reference.

### Step 4 — Update the knowledge file

- **Action**: Write the workflow's findings back to the competitor's structured context file as Rules / Facts / Hypotheses. This is the step that turns a one-off workflow into a self-improving knowledge base.
- **Sub-steps**:
  1. **First-run path** (file doesn't exist): create `knowledge/competitors/{name}.md` with the schema header (Rules / Facts / Hypotheses sections); seed with one or two foundational Rules from Step 1; promote the highest-confidence findings from Step 2 as initial Hypotheses; set `last_updated`.
  2. **Update path** (file exists): append new findings as Hypotheses with date stamps and source links; do NOT overwrite existing Facts or Rules; if a finding conflicts with an existing Fact, append it as a Hypothesis AND add a flag note for the next lint pass.
  3. Update `last_updated` date.
- **Decision Points**:
  - First run vs. update — branches based on Step 1's `exists` flag.
  - Conflict with existing Fact → append as Hypothesis + flag for lint; never auto-demote a Fact.
- **Data In**: Step 3 brief; Step 2 raw findings; Step 1 existing context.
- **Data Out**: Updated `knowledge/competitors/<competitor-name>.md`.
- **Context Needs**: The schema doc (Rules / Facts / Hypotheses convention — introduced by this workflow's outputs in Session 9 and formalized in Session 10's self-improvement work).
- **Failure Modes**:
  - File write conflict (concurrent runs) — implement a lock or a single-runner constraint.
  - Malformed markdown — use a deterministic template, not free-form generation.
  - Hypothesis explosion (every run adds 10+ hypotheses) — bound the number of new hypotheses per run; surface lower-confidence ones in a "deferred" subsection.

### Step 5 — Output the digest

- **Action**: Produce a short digest summarizing what changed and where to read more.
- **Sub-steps**:
  1. Summarize 3–5 highest-signal findings as bullet points.
  2. Link to the full brief from Step 3 and the updated knowledge file from Step 4.
  3. Surface any flagged conflicts or schema-evolution Hypotheses for human attention.
- **Data In**: Step 3 brief; Step 4 update result; any flags raised in earlier steps.
- **Data Out**: Markdown digest — short enough to skim in 30 seconds.
- **Context Needs**: None beyond what's already produced.
- **Failure Modes**: None significant; the digest is the easiest step.

## Optimization Summary

Changes applied to a naive "search → write a brief" version:

- **Added** Step 1 (load existing knowledge) as a distinct, parallelizable step. Reason: the whole point of this workflow is that it compounds — without reading existing context, every run starts from scratch.
- **Parallelized** Step 2's three search sub-steps. Reason: no data dependency; substantial latency savings.
- **Required** every Step 2 claim to carry a source URL. Reason: the #1 failure mode for research workflows is hallucinated findings; the source-URL requirement is a deterministic guard.
- **Branched** Step 4 into first-run and update paths. Reason: the workflow needs to bootstrap the KB on first run and grow it on subsequent runs without conflating the two.
- **Bounded** the number of new Hypotheses per run. Reason: an unbounded write pattern produces hypothesis explosion; bounding it forces the workflow to prioritize signal.
- **Added** explicit conflict handling (new finding contradicts existing Fact). Reason: this is the most informative signal the workflow produces — both about the competitor and about whether the schema is still serving you (an Improve-step trigger).
- **Eliminations**: none — every step earns its place.
- **Optimizations declined**: human review checkpoint between Step 2 and Step 3 (would slow the workflow without materially improving output for a well-tuned brief template).

## Step Sequence and Dependencies

- **Sequential critical path**: Step 1 → Step 2 → Step 3 → Step 4 → Step 5.
- **Parallel within Step 2**: 2a (product), 2b (hiring), 2c (commentary) run concurrently; 2d (cross-reference with existing Facts) waits on all three.
- **Single owner**: workflow operator. No role transitions during a single run.
- **Cross-run dependency**: every run depends on the previous run's Step 4 output (the updated knowledge file). This is the compounding mechanism.

## Context Shopping List

| Artifact | Description | Used By Steps | Status | Key Contents | AI Accessible? | Readiness Notes |
|---|---|---|---|---|---|---|
| `knowledge/competitors/{name}.md` | The competitor's structured context file (Rules / Facts / Hypotheses) | 1, 4 | Created on first run | Schema-structured competitor knowledge | Yes | Created by the agent itself on first run; subsequently read AND written every run. |
| Schema doc | Explains the Rules / Facts / Hypotheses convention | 1, 4 | Created by the workflow's first run | Section conventions, promotion/demotion rules | Yes | The convention is introduced by this workflow's outputs in Session 9 and formalized in Session 10's self-improvement work. |
| Web search tool | Source of competitor signals | 2 | Exists | Web search results | Yes | Cowork web search connector or a research skill that wraps it. |
| Brief template | Section structure for the synthesized brief | 3 | Pre-built | Section headings, length norms | Yes | Lives in the `competitor-research` skill prompt. |
| Per-competitor search terms (optional) | Aliases, product names, exec names | 2 | Optional | Search-term hints | Yes | Lives as Rules in the per-competitor knowledge file. |
| Output location for briefs | Where the rendered brief is saved (separate from the KB file) | 3 | Pre-built | — | Yes | Suggest `briefs/{competitor}/{date}.md` for the dated brief; the KB file is the persistent companion. |

### Reuse Candidates (carry into Design)

- **Skills**: `competitor-research` (new — built live in the demo); the KB read/write conventions inform Step 1 and Step 4.
- **Agents**: `competitor-brief` agent (new — built live in the demo) orchestrates the five steps.
- **MCP servers / connectors**: web search (Cowork connector); filesystem (read/write knowledge files).
- **Patterns**: LLM Wiki pattern (Rules / Facts / Hypotheses + ingest / query / lint) — applied to this workflow's outputs in Session 10.

### Out of Scope (separate workflows)

- A periodic **lint cycle** that promotes Hypotheses → Facts when confirmed and surfaces contradictions — built into the workflow itself during Session 10's self-improvement work.
- A **digest aggregator** that rolls up all competitor digests into a weekly newsletter — downstream workflow.
- **First-time competitor onboarding** (writing the initial Rules from scratch based on prior knowledge) — handled out-of-band; the workflow seeds Rules conservatively on first run and expects them to be hand-curated over time.

---

**Workflow Definition complete. Ready for Session 9's live Design step — turning this into a Building Block Spec.**
