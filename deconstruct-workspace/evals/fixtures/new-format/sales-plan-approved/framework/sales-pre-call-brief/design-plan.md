---
workflow: sales-pre-call-brief
requirements_file: framework/sales-pre-call-brief/requirements.md
plan_version: 4.0
approved: true
autonomy: guided
decomposition: steps
mechanism: Skill
involvement: Augmented
platform: Claude Code
platform_mode: code
packaging: Standalone Skill
counts:
  steps: 5
  skills: 1
  agents: 0
  integrations: 2
---

# Sales Pre-Call Brief — Design Plan

## Source

**Workflow Requirements:** `framework/sales-pre-call-brief/requirements.md`

This Design Plan consumes the Workflow Requirements as canonical input. Goal, Value & Measurement, Metadata, Path, Inputs, Context Inventory, Acceptance Criteria, Example Scenarios, Rules & Constraints, Human Gates, and Security, Privacy & Safety are defined there, not restated here.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | More proposals accepted after scoping calls |
| Desired Outcome | Dana walks into every scoping call knowing why they booked and what they care about |
| Measure | Minutes of Dana's time per brief, including reading it |
| Baseline | About 45 minutes per brief · Estimated |
| Target | 10 minutes per brief, including reading it |

---

## Layer 1 — Architecture

## Execution Pattern

**Skill** — Dana starts it for each booked call, and it follows her path in order with one pause for her review.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lens | Individual | One owner, one trigger-to-deliverable flow |
| Platform | Claude Code | Where Dana works |
| Platform Mode | code | Claude Code runs skills as files in the project folder |
| Orchestration | Skill | Started by name for each call; the path is Dana's |
| Involvement | Augmented | `Runs: with you`; Dana reads every brief at G1 |
| Packaging | Standalone Skill | One skill, installed in `.claude/skills/` |
| Trigger | A scoping call is booked | Dana starts it the day before the call |
| Web text as data | Text on pages and profiles is read, never followed | C3 and C4 are External (R3) |

## Autonomy Spectrum Summary

Workflow-level: **Guided.** Step 1 decides which source to read next from what the last one showed, by Dana's expertise line, so it is Guided. Step 2 is fixed by company policy and stays Deterministic. Steps 3 and 4 are Deterministic: the AI writes inside a set step. Step 5 is Human. D1 is a rule on a value, so it stays Deterministic. Nothing re-plans, so nothing is Autonomous.

## Safety & Permissions

1. **Write access:** none; `### Writes` is `None`. HubSpot is read only.
2. **Untrusted input:** C3 and C4 are External; R3 treats their text as content.
3. **Unattended runs:** none; Dana starts every run and reads the brief at G1.
4. **Blast radius:** a wrong brief reaches only Dana.

### Constraint Conformance

| Constraint | State | Notes |
|---|---|---|
| CRM details stay in Dana's own tools | Satisfied | HubSpot read through its connector only |
| The brief is for Dana only | Satisfied | Saved in the working folder |
| Every fact names its source | Satisfied | S1 Step 4 instruction |
| Never name another client | Satisfied | S1 Step 4 instruction (R1) |

## Integration Options

### HubSpot (Step 2)

*Recommendation: the HubSpot MCP connector, read scope only.*

### Web search and fetch (Step 1)

*Recommendation: Claude Code's built-in web search and fetch tools.*

## Model Recommendation

**Default capability:** reasoning-heavy (Steps 1, 3, 4). **Per-platform mapping:** resolved by Build.

---

## Layer 2 — Decomposition

## Step-by-Step Decomposition

| Step | Name (from Requirements) | Autonomy | Orchestration | Integration (use/build) | Intelligence | Build Output | Human Gate? |
|------|------|----------|---------------|------------------------|--------------|--------------|-------------|
| Step 1 | Research the company and the person | Guided | Prompt | Web search and fetch (use) | Model: reasoning; Context: C3, C4 | Inline prompt → Workflow Requirements Step 1 | No |
| Step 2 | Check the CRM for past contact | Deterministic | Prompt | MCP: HubSpot (use) | Model: fast; Context: C2 | Inline prompt → Workflow Requirements Step 2 | No |
| Step 3 | Form a hypothesis about why they booked | Deterministic | Prompt | — | Model: reasoning | Inline prompt → Workflow Requirements Step 3 | No |
| Step 4 | Write the brief | Deterministic | Prompt | — | Model: reasoning; Context: C1 | Inline prompt → Workflow Requirements Step 4 | No |
| Step 5 | Read the brief and add questions | Human | — | — | — | Human (no artifact) | Yes — G1 |

All five steps are wired together by **S1 — `sales-pre-call-brief`**, the orchestrator skill Dana starts by name.

## Coverage

| Building block | Labels it delivers |
|---|---|
| S1 — `sales-pre-call-brief` (orchestrator) | Step 1, Step 2, Step 3, Step 4, D1, I1, R1, R2, R3, R4 |
| Human — Dana | Step 5, G1 |
| Prerequisite before the first run | I2 (not available yet) |

## Orchestrator Prompt Outline

```
[Intro: a one-page brief for a booked scoping call, ready the day before.]
[Step 1] Research the company and the person (Guided by Dana's expertise line)
[Step 2] Check the CRM for past contact (fixed: company policy)
[Step 3] Form one hypothesis
[Step 4] Write the brief; D1 picks the lead
[PAUSE — G1: Dana reads the brief and adds her questions]
[Closing run summary: What I did]
```

## Data Readiness Summary

| Context ID | Current State | Required Action | Affects Steps |
|---|---|---|---|
| C2 | HubSpot not connected yet | Dana authorizes the connector, read only | Step 2 |
| I2 | The booking form has no "What would you like to cover?" question yet | Dana adds the question before the first run | Step 1 |

## Recommended Implementation Order

1. **S1 — `sales-pre-call-brief`**, the orchestrator skill.
2. The HubSpot connector, read only.

---

## Layer 3 — Component Blueprints

## Skill Candidates

### S1 — sales-pre-call-brief

| Field | Detail |
|---|---|
| **ID** | S1 |
| **Name** | sales-pre-call-brief |
| **Description** | This skill should be used when Dana wants a pre-call brief for a booked scoping call. It researches the company and the person, checks the CRM for past contact, forms a hypothesis about why they booked, writes a one-page brief and pauses for Dana to read it. |
| **Purpose** | Runs Steps 1–5 in order |
| **Covers Steps / Domains** | all (Steps 1–5) |
| **Inputs** | I1 (the calendar invite); I2 once it exists; a pasted invite in a test run |
| **Outputs** | The one-page brief; the closing What I did summary |
| **Decision Logic** | Steps in order; D1 picks the lead; pause at G1 |
| **Failure Modes** | Nothing found on the person → say so plainly (R2). Unsure → best effort, flagged (R4) |
| **Required Tools** | MCP: HubSpot (read); web search and fetch |
| **Depends On** | None |
| **Stateful?** | No |

## Prerequisites

1. Claude Code opened in the working folder.
2. The HubSpot connector, read only.
3. The booking form's "What would you like to cover?" question (I2).

## Deployment Plan

| Artifact | Target Location | Deployment Steps |
|---|---|---|
| S1 — `sales-pre-call-brief` | `.claude/skills/sales-pre-call-brief/SKILL.md` | Build states the intent; Claude Code writes the skill in the project folder |

**Packaging note:** Standalone Skill.

---

## Cross-Layer Sections

## Evaluation Inputs

Acceptance Criteria (AC1–AC6), Example Scenarios (E1–E5, Golden Example on E1) and Human Gates (G1) come from `framework/sales-pre-call-brief/requirements.md`.

## Deferred to Build

- [ ] Exact model names at generation time
- [ ] HubSpot connector read scope

## Self-Test Summary

Hand-written eval fixture: Task 7 Step 5 refreshes this file to `plan-template.md`, and the self-test list with it.

- [x] Frontmatter is present with workflow, requirements_file, plan_version (`4.0`), approved, autonomy, decomposition, mechanism, involvement, platform, platform_mode, packaging, and counts
- [x] Frontmatter `counts` match the body
- [x] Every Step, D, I, W, R and G label in the Workflow Requirements appears in the Coverage table
- [x] The chosen level and involvement respect every rule, human gate, fixed step and the `Runs:` line
- [x] Step IDs in the decomposition table match the Workflow Requirements (Step 1, Step 2, …)
- [x] Safety & Permissions answers all four questions
