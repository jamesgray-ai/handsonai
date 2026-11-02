---
revision: 1
track: full
revisions: []
---

# Launch Announcer — Workflow Requirements

## Goal
For each product release marked ready, the release announced everywhere it should be, within an hour of the release.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Every customer hears about new features the day they ship |
| Desired Outcome | No release goes unannounced in any channel |
| Measure | Hours from release to the last announcement |
| Baseline | 2 days · Estimated |
| Target | 1 hour |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Launch Announcer |
| Description | Announces each release in every channel it belongs in, from the release notes, as soon as the release is marked ready. |
| Trigger | A release is marked ready in the release tracker |
| Owner | Product marketing manager |
| Lens | Organizational |
| Stakeholders | Product; support; sales |

## Path

Method preference: same way every time

- Step 1 — Read the release notes · produces the headline and three highlights · uses C1 · flexible
- Step 2 — Write each announcement · produces one announcement per channel · uses C2 · flexible
- Step 3 — Publish the changelog entry · produces an entry on the changelog page · flexible · writes W1
- Step 4 — Update the in-app banner · produces a new banner · flexible · writes W2
- Step 5 — Post on the partner portal · produces a partner portal post · flexible · writes W3
- Step 6 — Update the sales battlecard · produces an updated battlecard · flexible · writes W4
- Step 7 — Post in the support wiki · produces a support wiki entry · flexible · writes W5
- Step 8 — Post in #announcements · produces a Slack post · flexible · writes W6

## Inputs

- I1 · the release notes · from the release tracker · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Release notes format | Step 1 | Exists | Internal | Authored | Yes | `context/C1-release-notes-format.md` | Where the headline and highlights sit |
| C2 | Channel style guide | Step 2 | Exists | Internal | Authored | Yes | `context/C2-channel-style.md` | Length and tone for each channel |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every channel gets its announcement.
2. **AC2 (must)** — Every announcement states only features in the release notes.
3. **AC3** — Each announcement fits its channel's length limit.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Exports release (real) | `inputs/E1-exports-release.md` — release 4.2 with spreadsheet exports | Six announcements, one per channel | — |
| E2 | Bug-fix release (proposed) | `inputs/E2-bug-fix-release.md` — a release with fixes only | Only the changelog entry and the support wiki entry | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never announces a feature that isn't in the release notes. |
| R2 | When | When a release holds fixes only, it announces it in the changelog and the support wiki only. |
| R3 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates

Runs: without you

No human gates — the workflow runs end-to-end with final review only.

## Security, Privacy & Safety

*Scope: writes to a live system*

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P1 | Each run's summary links every announcement it published. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P2 | It never announces a release that isn't marked ready, whoever asks. | Self |

Governing regime: None

### Writes
- W1 · the changelog page (our own website's CMS; it has no connection) · publish the entry · Step 3
- W2 · the in-app banner (set in our admin console; it has no connection) · replace the banner · Step 4
- W3 · the partner portal (it has no connection) · post the announcement · Step 5
- W4 · the sales battlecard (a page in our in-house wiki; it has no connection) · overwrite the "What's new" section · Step 6
- W5 · the support wiki (it has no connection) · post the entry · Step 7
- W6 · Slack · post in #announcements · Step 8
