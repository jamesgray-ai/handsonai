---
revision: 1
track: full
revisions: []
---

# Invoice Coding — Workflow Requirements

## Goal
For each supplier invoice, a coded invoice line for the bookkeeper, ready to enter the same day.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep the books current without month-end catch-up |
| Desired Outcome | Every invoice carries the right account and cost centre before it's entered |
| Measure | Minutes per invoice |
| Baseline | 6 minutes per invoice · Estimated |
| Target | 1 minute per invoice |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Invoice Coding |
| Description | Codes each supplier invoice to the right account and cost centre, for the bookkeeper to check and enter. |
| Trigger | A supplier invoice arrives in the accounts inbox |
| Owner | Bookkeeper |
| Lens | Individual |

## Path

Method preference: AI works it out each time

Path: none — the AI plans each run from the goal

### Decisions

- D1: When the supplier is on the coding table, it uses that supplier's account and cost centre · settled by: a rule on a value · value read by AI
- D2: When the supplier isn't on the table, it marks the invoice for you to code · settled by: a rule on a value

## Inputs

- I1 · one supplier invoice (PDF text) · from the accounts inbox, pasted into the chat · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Supplier coding table | All | Exists | Internal | Authored | Yes | `context/C1-coding-table.md` | Each supplier's account and cost centre |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The coded line uses the account and cost centre the table gives the supplier.
2. **AC2 (must)** — An invoice from a supplier not on the table is marked for you, with no account guessed.
3. **AC3** — The coded line carries the invoice number, date and total.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Office supplies (real) | `inputs/E1-office-supplies.md` — an invoice from a supplier on the table | The table's account and cost centre | — |
| E2 | New supplier (proposed, hard) | `inputs/E2-new-supplier.md` — an invoice from a supplier not on the table | Marked for you, no account guessed | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never guesses an account. |
| R2 | Fallback | When it can't confidently handle a case, it skips that item and flags it. |

## Human Gates

Runs: with you

No human gates — the workflow runs end-to-end with final review only.

## Security, Privacy & Safety

No sensitivity constraints — personal data only, read-only, human-triggered.

Governing regime: None

### Writes
None
