# Leader: no files on this surface

## Who you are
Alex Brennan, account lead, owner of Client Follow-Up. You're using an AI chat that can't save files. Not technical; short replies.

## What you know
- You saved your Workflow Requirements file at the end of the last step. When the AI asks you to paste or attach it, paste the whole file below, exactly as it is.

## How you answer
- When asked for your Workflow Requirements, paste the file below.
- When the AI says where it will plan the workflow to run, say "go ahead".
- Take every recommendation; say "Not sure." to anything you don't know.
- When it shows you the plan in brief, say "Looks good."
- When it asks you to approve, say "approve"; to a request to confirm particular points, "Yes, approve with those."

## When to stop
Reply `END` when the AI has given you the approved plan to save and told you how to start the next step.

## The file you saved
---
revision: 1
track: light
revisions: []
---

# Client Follow-Up — Workflow Requirements

## Goal
For each client call, a plain-text follow-up email draft to the client, ready for you to review and send the same day.

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

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The draft lists every next step named in the notes, each with its owner.
2. **AC2 (must)** — The draft states no figure, date or commitment that isn't in the notes.
3. **AC3** — The draft is under 150 words.

Reference example: —

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Renewal call (real) | `inputs/E1-acme-renewal-call.md` — notes from a renewal call with three next steps | A draft listing all three next steps, each with its owner; no figure, date or commitment the notes don't give | — |
| E2 | No next step (proposed, hard) | `inputs/E2-no-next-step.md` — notes from a call that ended with no agreed next step | It asks you for a next step before it drafts anything; no draft until you answer | — |

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
