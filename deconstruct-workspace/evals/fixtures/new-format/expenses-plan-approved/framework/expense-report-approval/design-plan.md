---
workflow: expense-report-approval
requirements_file: framework/expense-report-approval/requirements.md
plan_version: 4.0
approved: true
autonomy: deterministic
decomposition: steps
mechanism: Skill
involvement: Augmented
platform: Claude Code
platform_mode: code
packaging: Standalone Skill
counts:
  steps: 7
  skills: 1
  agents: 0
  integrations: 1
---

# Expense Report Approval — Design Plan

## Source

**Workflow Requirements:** `framework/expense-report-approval/requirements.md`

This Design Plan consumes the Workflow Requirements as canonical input. Goal, Value & Measurement, Metadata, Path, Inputs, Context Inventory, Acceptance Criteria, Example Scenarios, Rules & Constraints, Human Gates, and Security, Privacy & Safety are defined there, not restated here.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Fewer audit findings on expense reimbursements |
| Desired Outcome | Employees get a clear decision with the reason, and reimbursements go out faster |
| Measure | Analyst hours a week spent checking expense reports |
| Baseline | About 12 hours a week · Estimated |
| Target | 4 analyst hours a week |

---

## Layer 1 — Architecture

## Execution Pattern

**Skill** — the same seven steps run for every report, with two people's approvals on the path.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lens | Organizational | Analysts, the controller and payroll take part |
| Platform | Claude Code | Where the Finance Operations team works |
| Platform Mode | code | Claude Code runs skills as files in the project folder |
| Orchestration | Skill | Fixed order; started for each submitted report |
| Involvement | Augmented | `Runs: with you`; the analyst reviews every decision (G1) |
| Packaging | Standalone Skill | One skill, installed in `.claude/skills/` |
| Trigger | An employee submits an expense report | The analyst starts a run per report |

## Autonomy Spectrum Summary

Workflow-level: **Deterministic.** Steps 1 and 4 are `fixed (regulation)` and are kept exactly as the requirements state them. D1 is a rule on a value; the AI reads the total from the receipts, so the decision stays Deterministic and Test checks the reading separately (`D1 reading`). Steps 2, 3, 5 and 7 follow set rules. Steps 4 and 6 are Human.

**Role swimlane:** Steps 1–3, 5 and 7 — AI; Step 4 — controller; Step 6 — finance analyst.

## Safety & Permissions

1. **Write access:** W1, posting the decision to Concur (Step 7), only after the analyst approves at G1.
2. **Untrusted input:** scanned receipts are read as data.
3. **Unattended runs:** none; every run pauses at G1.
4. **Blast radius:** a wrong decision on one report, caught at G1.

### Constraint Conformance

| Constraint | State | Notes |
|---|---|---|
| Staff expense data stays in Concur and approved tools | Satisfied | Concur connector only |
| Decision notes visible only to the employee, payroll and Finance Operations | Satisfied | Posted on the report in Concur |
| Every decision records who approved it and which limit applied | Satisfied | The note and the What I did summary carry both |
| Never send emails | Satisfied | No email tool |

## Integration Options

### Concur (Steps 1 and 7)

*Recommendation: a Concur connector with read access to reports and receipts and write access to approvals only.*

## Model Recommendation

**Default capability:** vision for Step 1 (receipt reading); reasoning-heavy for Step 5. **Per-platform mapping:** resolved by Build.

---

## Layer 2 — Decomposition

## Step-by-Step Decomposition

| Step | Name (from Requirements) | Autonomy | Orchestration | Integration (use/build) | Intelligence | Build Output | Human Gate? |
|------|------|----------|---------------|------------------------|--------------|--------------|-------------|
| Step 1 | Match each receipt to its line item | Deterministic | Prompt | MCP: Concur (use) | Model: vision; Context: C2 | Inline prompt → Workflow Requirements Step 1 | No |
| Step 2 | Check amounts against the policy limits | Deterministic | Prompt | — | Model: fast; Context: C1 | Inline prompt → Workflow Requirements Step 2 | No |
| Step 3 | Route by report total | Deterministic | Prompt | — | Model: fast | Inline prompt → Workflow Requirements Step 3 | No |
| Step 4 | Controller approval over $5,000 | Human | — | — | — | Human (no artifact) | Yes — G2 |
| Step 5 | Write the decision note | Deterministic | Prompt | — | Model: reasoning | Inline prompt → Workflow Requirements Step 5 | No |
| Step 6 | Analyst review | Human | — | — | — | Human (no artifact) | Yes — G1 |
| Step 7 | Post the decision to Concur | Deterministic | Prompt | MCP: Concur (use) | Model: fast | Inline prompt → Workflow Requirements Step 7 | No |

All seven steps are wired together by **S1 — `expense-report-approval`**, the orchestrator skill.

## Coverage

| Building block | Labels it delivers |
|---|---|
| S1 — `expense-report-approval` (orchestrator) | Step 1, Step 2, Step 3, Step 5, Step 7, D1, I1, I2, W1, R1, R2, R3, R4, G3 |
| Human — controller | Step 4, G2 |
| Human — finance analyst | Step 6, G1 |

## Orchestrator Prompt Outline

```
[Intro: checks a submitted expense report and routes it for approval.]
[Step 1] Match each receipt to its line item (fixed: regulation — follow exactly)
[Step 2] Check amounts against the policy limits
[Step 3] Route by report total (D1)
[PAUSE — G2 when the total is over $5,000: the controller approves or returns]
[Step 5] Write the decision note
[PAUSE — G1: the analyst reviews the decision]
[Step 7] Post the decision to Concur (W1)
[Closing run summary: What I did]
```

## Data Readiness Summary

| Context ID | Current State | Required Action | Affects Steps |
|---|---|---|---|
| C2 | Concur not connected yet | Authorize the Concur connector: read reports and receipts, write approvals | Steps 1, 7 |

## Recommended Implementation Order

1. **S1 — `expense-report-approval`**, the orchestrator skill.
2. The Concur connector.

---

## Layer 3 — Component Blueprints

## Skill Candidates

### S1 — expense-report-approval

| Field | Detail |
|---|---|
| **ID** | S1 |
| **Name** | expense-report-approval |
| **Description** | This skill should be used when Northbank's Finance Operations team wants a submitted expense report checked against the expense policy and routed for approval. It matches every receipt to its line, checks policy limits, routes by the report total, writes the decision note, pauses for the analyst's review and posts the decision to Concur. |
| **Purpose** | Runs Steps 1–7 in order, pausing at G2 and G1 |
| **Covers Steps / Domains** | all (Steps 1–7) |
| **Inputs** | I1 (the report), I2 (the receipts); pasted in a test run |
| **Outputs** | The decision note; the decision posted to Concur; the closing What I did summary |
| **Decision Logic** | Steps 1 and 4 exactly as required by regulation; D1 routes by total |
| **Failure Modes** | Unsure → stop and ask the analyst (G3). Unreadable receipt → mismatch, named |
| **Required Tools** | MCP: Concur (read reports and receipts; write approvals) |
| **Depends On** | None |
| **Stateful?** | No |

## Prerequisites

1. Claude Code opened in the working folder.
2. The Concur connector, authorized as above.

## Deployment Plan

| Artifact | Target Location | Deployment Steps |
|---|---|---|
| S1 — `expense-report-approval` | `.claude/skills/expense-report-approval/SKILL.md` | Build states the intent; Claude Code writes the skill in the project folder |

**Packaging note:** Standalone Skill.

---

## Cross-Layer Sections

## Evaluation Inputs

Acceptance Criteria (AC1–AC4), Example Scenarios (E1–E4; E2 is the hard case) and Human Gates (G1–G3) come from `framework/expense-report-approval/requirements.md`.

## Deferred to Build

- [ ] Exact model names at generation time
- [ ] Concur connector scopes

## Self-Test Summary

Hand-written eval fixture: Task 7 Step 5 refreshes this file to `plan-template.md`, and the self-test list with it.

- [x] Frontmatter is present with workflow, requirements_file, plan_version (`4.0`), approved, autonomy, decomposition, mechanism, involvement, platform, platform_mode, packaging, and counts
- [x] Frontmatter `counts` match the body
- [x] Every Step, D, I, W, R and G label in the Workflow Requirements appears in the Coverage table
- [x] The chosen level and involvement respect every rule, human gate, fixed step and the `Runs:` line
- [x] Step IDs in the decomposition table match the Workflow Requirements (Step 1, Step 2, …)
- [x] Safety & Permissions answers all four questions
