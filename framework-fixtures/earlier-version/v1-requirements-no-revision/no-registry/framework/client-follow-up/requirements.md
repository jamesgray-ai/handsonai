# Client Follow-Up — Workflow Requirements

## Goal
For each client call, a plain-text follow-up email draft to the client, ready for you to review and send the same day.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep client commitments on track after every call |
| Desired Outcome | Every client call gets a follow-up the same day, listing the agreed next steps and who owns each |
| Measure | Minutes spent writing each follow-up |
| Baseline | 20 minutes per call · Estimated |
| Target | 5 minutes per call, including review |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Client Follow-Up |
| Description | Drafts a follow-up email after each client call from your call notes, for you to review and send. |
| Trigger | You finish a client call and paste in your notes |
| Owner | Account lead |
| Lens | Individual |

## Path

Method preference: same way every time

- Step 1 — Read the call notes · produces a list of decisions and next steps · fixed (your judgment)
- Step 2 — Draft the email · produces a plain-text email draft in Gmail Drafts · uses C1 · flexible · writes W1
- Step 3 — Review and send · produces the sent email · fixed (your judgment) · (you)

### Decisions

- D1 (Step 2): When the notes name no next step, it asks you for one before drafting · settled by: your criteria

### Step 2 — Draft the email
**Rule:** Follow C1's tone, length and sign-off.
**Check or handoff:** The draft waits in Gmail Drafts for your review.

## Inputs

- I1 · your call notes · from you, pasted into the chat · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Follow-up style guide | Step 2 | Exists | Internal | Authored | Yes | `context/C1-follow-up-style.md` | Tone, length and sign-off for client emails |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The draft lists every next step named in the notes, each with its owner.
2. **AC2 (must)** — The draft states no figure, date or commitment that isn't in the notes.
3. **AC3** — The draft is under 150 words.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Renewal call (real) | `inputs/E1-acme-renewal-call.md` — notes from a renewal call with three next steps | All three next steps, each with its owner | — |
| E2 | No next step (proposed, hard) | `inputs/E2-no-next-step.md` — notes from a call that ended with no agreed next step | It asks you for a next step before it drafts anything | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never invents a figure, date or commitment. |
| R2 | When | When the draft is ready, you send it yourself. · (you) |
| R3 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 3 | When the draft is ready, it stops until you approve it. · (you) |

## Security, Privacy & Safety

*Scope: writes to a live system*

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P1 | Each run's closing summary names the draft it created in Gmail Drafts. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P2 | It never sends an email, whoever asks. | Self |

Governing regime: None

### Writes
- W1 · Gmail · create a draft · Step 2
