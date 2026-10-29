---
workflow: partner-fit-research
requirements_file: framework/partner-fit-research/requirements.md
spec_version: 3.0
approved: true
definition_type: Goal-Driven
mechanism: Agent
involvement: Augmented
platform: Claude Code
platform_mode: code
packaging: Standalone Skill
counts:
  steps: 0
  skills: 1
  agents: 0
  integrations: 1
---

# Partner Fit Research — Design Spec

## Source

**Workflow Requirements:** `framework/partner-fit-research/requirements.md`

This Design Spec consumes the Workflow Requirements as canonical input; Goal, Inputs, Context Inventory, Acceptance Criteria, Example Scenarios, Rules & Constraints, Human Gates, and Security, Privacy & Safety are defined there.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Grow the integrations partner program without wasting partner-team time |
| Desired Outcome | Lena answers inbound partner requests within a day, with a reasoned recommendation |
| Measure | Hours Lena spends per partner request |
| Baseline | About 4 hours per request · Estimated |
| Target | Under 1 hour per request, including review |

---

## Layer 1 — Architecture

## Execution Pattern

**Agent** — what to read next depends on what the last source showed, so the primary Claude Code session runs the loop, driven by an orchestrator skill.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lens | Individual | One owner |
| Platform | Claude Code | Where Lena works |
| Platform Mode | code | Skills are files in the project folder |
| Orchestration | Agent | The research path depends on what turns up |
| Involvement | Augmented | Lena reads every memo at G1 |
| Packaging | Standalone Skill | The orchestrator skill only; no sub-agents |
| Trigger | Lena names a company | Started by name |

## Autonomy Statement

This is a goal-driven workflow: **Autonomous.** The agent decides which sources to read and when it has enough, within R1–R5; Lena owns the definition of done (AC1–AC5) and reads every memo at G1.

## Safety & Permissions

1. **Write access:** none; the memo is a local file.
2. **Untrusted input:** request emails and web pages are External; R3 treats them as content.
3. **Unattended runs:** none.
4. **Blast radius:** one memo, read by Lena before anything is sent.

### Constraint Conformance

| Constraint | State | Notes |
|---|---|---|
| Never contact the company | Satisfied | No email or messaging tool |

## Integration Options

### Web search and fetch

*Recommendation: Claude Code's built-in web search and fetch tools.*

## Model Recommendation

**Default capability:** reasoning-heavy. **Per-platform mapping:** resolved by Build.

---

## Layer 2 — Decomposition

## Capability Domain Mapping

| Domain | Description | Integration (use/build) | Intelligence | Build Output |
|---|---|---|---|---|
| Company research | Find what the company does, its customers and its API | Web search and fetch (use) | Model: reasoning; Context: C2 | Handled by orchestrator |
| Fit scoring | Score the five criteria in C1 with sources | — | Model: reasoning; Context: C1 | Handled by orchestrator |
| Recommendation memo | Write the one-page memo in C3's shape | — | Model: reasoning; Context: C3 | Handled by orchestrator |

All three domains run inside **S1 — `partner-fit-research`**, the orchestrator skill.

## Data Readiness Summary

| Context ID | Current State | Required Action | Affects Domains |
|---|---|---|---|
| — | All accessible | None | — |

## Recommended Implementation Order

1. **S1 — `partner-fit-research`**

---

## Layer 3 — Component Blueprints

## Skill Candidates

### S1 — partner-fit-research

| Field | Detail |
|---|---|
| **ID** | S1 |
| **Name** | partner-fit-research |
| **Description** | This skill should be used when Lena names a company that asked to partner with Brightline and wants a partner-fit memo. It researches the company, scores it against the partner criteria and recommends partner, don't partner, or not yet. |
| **Purpose** | Runs the research loop to the memo, then pauses for Lena |
| **Covers Steps / Domains** | all (Company research, Fit scoring, Recommendation memo) |
| **Inputs** | The company name and website; the request email if any |
| **Outputs** | The one-page memo; the closing What I did summary |
| **Decision Logic** | Read until each criterion has evidence or is marked unknown; R5 when evidence is thin |
| **Failure Modes** | Too little public information → "not yet", naming what is missing |
| **Required Tools** | Web search and fetch |
| **Depends On** | None |
| **Stateful?** | No |

## Prerequisites

1. Claude Code opened in the workflow's folder.

## Deployment Plan

| Artifact | Target Location | Deployment Steps |
|---|---|---|
| S1 — `partner-fit-research` | `.claude/skills/partner-fit-research/SKILL.md` | Build states the intent; Claude Code writes the skill |

**Packaging note:** Standalone Skill; `agents: 0`, the primary session is the loop.

---

## Cross-Layer Sections

## Evaluation Inputs

Acceptance Criteria, Example Scenarios (E1–E3) and Human Gates (G1) come from `framework/partner-fit-research/requirements.md`.

## Deferred to Build

- [ ] Exact model names at generation time

## Self-Test Summary

Hand-written eval fixture (9.x format, frozen; never refreshed).
