---
revision: 1
track: light
revisions: []
---

# Client Follow-Up — Workflow Requirements

## Goal
For each client call, a plain-text follow-up email draft to the client, ready for you to review and send the same day.

## Output

What: a follow-up email draft
For: the client on the call
Form: plain text, under 150 words, with a subject line
Voice: yours, as in your follow-up style guide
Structure:
    Subject: [the call's topic]
    Thanks for the call
    Next steps, each with its owner
    Sign-off
Delivered as: set in Design

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | — |
| Desired Outcome | — |
| Measure | — |
| Baseline | — · Unknown |
| Target | — |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Client Follow-Up |
| Description | Drafts a follow-up email after each client call from your call notes, for you to review and send. |
| Trigger | You finish a client call and paste in your notes |
| Starts | you |
| Per run | one client call |
| Owner | Account lead |
| Lens | Individual |

## Path

Method preference: AI works it out each time
Path: none — the AI plans each run from the goal

## Inputs

- I1 · your call notes · from you, pasted into the chat · Status: available

## Context Inventory
*The sources it uses, what we call its context.*

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Follow-up style guide | All | Exists | Internal | Authored | Yes | `context/C1-follow-up-style.md` | Tone, length and sign-off for client emails |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line.

1. **AC1** — The draft lists every next step named in the notes, each with its owner. · from: I1
2. **AC2** — The draft states no figure, date or commitment that isn't in the notes. · from: I1, R1
3. **AC3** — The draft follows the tone and sign-off of your style guide. · from: C1
4. **AC4** — The draft has a subject line. · from: the output alone

Reference example: —

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Renewal call (real) | `inputs/E1-acme-renewal-call.md` — notes from a renewal call with three next steps | A draft listing all three next steps, each with its owner; no figure, date or commitment the notes don't give | — |
| E2 | No next step (made up) | Test writes it — notes from a call that ended with no agreed next step | It asks you for a next step before it drafts anything; no draft until you answer | — |

## Rules & Constraints
*Its rules: what it always does, never does, and does when something happens.*

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never invents a figure, date or commitment. |
| R2 | When | When the draft is ready, you send it yourself. · (you) |
| R3 | Fallback | When it can't confidently handle a case, it does its best and flags it. |
| R4 | When | When the notes name no next step, it asks you for one before it drafts anything. |

## Human Gates
*The checkpoints: where a person checks or approves the work.*

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | After the draft is ready | When the draft is ready, it stops until you approve it. · (you) |

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
- W1 · Gmail · create a draft · after the email is drafted
