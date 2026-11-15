---
revision: 1
track: full
revisions: []
---

# Client Follow-Up — Workflow Requirements

## Goal
For each week's client calls, a plain-text follow-up email draft per call, ready for you to review and send.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep client commitments on track after every call |
| Desired Outcome | Every client call gets a follow-up the same week |
| Measure | Minutes spent writing each follow-up |
| Baseline | 20 minutes per call · Estimated |
| Target | 5 minutes per call, including review |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Client Follow-Up |
| Description | Drafts a follow-up email for each of the week's client calls from the call notes, for you to review and send. |
| Trigger | The week's client calls are done |
| Starts | schedule: every Friday afternoon |
| Per run | a batch of the week's client calls |
| Owner | Account lead |
| Lens | Individual |
| Runs today | By hand, from a notes template |
| Remembers | which calls it has already followed up |

## Path

Method preference: same way every time

- Step 1 — Remove client figures · produces call notes with the figures taken out · fixed (policy) · (you)
- Step 2 — Read the call notes · produces a list of decisions and next steps · fixed (your judgment)
- Step 3 — Draft the email · produces a plain-text email draft · uses C1, C2 · flexible · writes W1
- Step 4 — Review and send · produces the sent email · fixed (your judgment) · (you)

### Decisions

- D1 (Step 3): When the notes name no next step, it asks you for one before drafting · settled by: your criteria · criteria: no line in the notes says who does what next · value read by AI
- D2 (Step 3): When a call has already been followed up, it skips that call · settled by: a rule on a value · criteria: the call's date is on the list of calls already handled
- D3 (Step 3): When the client sounded unhappy, it keeps the draft short · settled by: open judgment · criteria: complaints, or a cancelled renewal

### Step 3 — Draft the email
**Rule:** Follow C1's tone, length and sign-off.

## Inputs

- I1 · the week's call notes · from C2 · Status: available

## Context Inventory
*The sources it uses, what we call its context.*

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Follow-up style guide | Step 3 | Exists | Internal | Authored | Yes | `context/C1-follow-up-style.md` | Tone, length and sign-off for client emails |
| C2 | Call notes | Step 1, Step 2 | Exists | Confidential | Authored | Yes | The team's shared notes folder | Client names, decisions and figures |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The draft lists every next step named in the notes, each with its owner.
2. **AC2 (must)** — The draft states no figure, date or commitment that isn't in the notes.

Reference example: —

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Renewal call (real) | `inputs/E1-renewal-call.md` — notes from a renewal call with three next steps | All three next steps, each with its owner; nothing sent | — |
| E2 | No next step (proposed, hard) | `inputs/E2-no-next-step.md` — notes from a call with no agreed next step | It asks you for a next step; no draft | — |
| E3 | A call already handled (proposed) | `inputs/E3-already-handled.md` — a call an earlier run already followed up | It skips the call an earlier run already handled | — |

## Rules & Constraints
*Its rules: what it always does, never does, and does when something happens.*

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never invents a figure, date or commitment. |
| R2 | When | When the notes hold client figures, you remove them before the AI sees the notes. · (you) |
| R3 | Fallback | When the notes are missing or garbled, it does its best and flags it in an email to you. |

## Human Gates
*The checkpoints: where a person checks or approves the work.*

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 4 | When the draft is ready, it stops until you approve it. · (you) |

## Security, Privacy & Safety

*Scope: writes to a live system; handles data you'd be uncomfortable seeing outside the company*

### Boundaries
| ID | Constraint | Source |
|---|---|---|
| P1 | The call notes reach the AI only after Step 1. | Self |

### Access
| ID | Constraint | Source |
|---|---|---|
| P2 | Only you see the drafts. | Self |

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P3 | Each run's closing summary names the drafts it created. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P4 | It never sends an email to a client, whoever asks. | Self |

Governing regime: None
Policy check: No — details removed first (Step 1)

### Writes
- W1 · Gmail (Drafts folder) · create a draft · Step 3
- W2 · email to you · send a flag · after each run
