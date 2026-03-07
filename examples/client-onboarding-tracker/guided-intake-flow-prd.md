# PRD: Guided Intake Flow

**Date:** 2026-03-07
**Author:** James Gray
**Status:** Draft
**Vision Brief:** [Client Onboarding Tracker](./vision-brief.md)
**Epic:** [Client Onboarding](https://github.com/jamesgray-ai/handsonai/issues/132)

---

## Problem Statement

New clients sign up but have no clear path through onboarding. They don't know what information to provide, in what order, or why it matters. Account managers can't tell where a client is in the process — or whether they've started at all. The result: 30% of clients go quiet in the first week, and the team wastes hours chasing them with manual follow-up emails.

The guided intake flow solves this by giving clients a structured, step-by-step experience that collects everything the team needs to begin serving them — while giving account managers visibility into exactly where each client stands.

## Target Users

**New clients** — Non-technical professionals who just signed a contract. They're motivated but don't know what to do next. They need clarity, not complexity. They want to feel like they're making progress, not filling out a bureaucratic form.

**Account managers** — Internal team members responsible for client success. They need to know which clients have completed intake, which are in progress, and which have stalled — without checking a spreadsheet or sending a "just checking in" email.

## Core Requirements

### User Story 1: Step-by-step information collection

**As a** new client, **I want to** provide my information through a guided, multi-step flow **so that** I know exactly what's needed and can complete it without confusion.

**Acceptance Criteria:**
- Intake is divided into logical steps: company info, primary contact details, project goals, timeline and constraints, and billing setup
- Each step shows only the fields relevant to that step — no overwhelming single-page form
- Required fields are clearly marked; optional fields explain why providing them is helpful
- Client can see which step they're on and how many remain (e.g., "Step 3 of 5")

### User Story 2: Progress persistence

**As a** new client, **I want to** save my progress and come back later **so that** I don't have to complete everything in one sitting.

**Acceptance Criteria:**
- Progress is automatically saved after each step is completed
- When a client returns, they resume from where they left off — not from the beginning
- A confirmation message shows when progress is saved (e.g., "Your progress has been saved. You can close this tab and come back anytime.")
- Incomplete intake flows are retained for at least 30 days before being archived

### User Story 3: Intake status visibility for account managers

**As an** account manager, **I want to** see which step each client is on in the intake flow **so that** I can proactively reach out to clients who are stuck.

**Acceptance Criteria:**
- Account manager view shows a list of all assigned clients with their current intake step
- Clients are sortable by status: not started, in progress, completed, stalled
- "Stalled" is defined as no activity for 48+ hours while intake is incomplete
- Clicking a client shows their completed steps and the specific step where they stopped

### User Story 4: Intake completion and handoff

**As a** new client, **I want to** receive a clear confirmation when I've completed intake **so that** I know what happens next and who to expect to hear from.

**Acceptance Criteria:**
- Completion screen shows a summary of all submitted information
- Client can review and edit any section before final submission
- After submission, client sees a "What happens next" message explaining the next steps in onboarding
- Account manager is notified immediately when a client completes intake

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Intake completion rate | ~70% (estimated) | 90% within 48 hours of starting |
| Average time to complete intake | Unknown (days) | Under 30 minutes of active time |
| Account manager time spent on intake follow-up | ~5 hours/week per AM | Under 1 hour/week per AM |
| Client-reported clarity on next steps | Not measured | 4.5+ out of 5 post-intake survey |

## Out of Scope

The following are explicitly **not** part of this feature — they will be addressed in separate PRDs:

- **Task assignment engine** — Automatically assigning onboarding tasks to team members after intake is complete (Feature 2)
- **Progress dashboard** — The aggregate dashboard showing all clients' onboarding status across all features (Feature 3). The account manager view described in User Story 3 is a lightweight, intake-specific status view — not the full dashboard.
- **Automated reminders** — Sending nudge emails or notifications to clients who stall (Feature 4). For the MVP, account managers will manually follow up based on the status view.
- **Completion report** — The formal summary report generated at the end of the full onboarding process (Feature 5)
- **Client-type customization** — Different intake flows for enterprise vs. SMB clients. The MVP uses a single flow for all client types. Customization will be evaluated after we have data on where different client types diverge.
- **Integrations** — Pushing intake data to CRM, billing, or project management tools. Data stays in the onboarding system for now.

## Technical Notes

- Intake flow should be mobile-responsive — clients may complete it on their phone
- Each step should be a discrete API call so progress saves are atomic (no partial-step data loss)
- Intake data schema should be extensible — we expect to add fields as we learn what's needed
- Analytics events should fire at each step transition to track drop-off rates per step

## Open Questions

- Should we allow clients to skip optional steps entirely, or require them to at least view each step?
- Do we need a "delegate to someone else" feature (e.g., client forwards intake to their office manager)?
- What's the right tone for the intake flow — professional and efficient, or warm and conversational?
- Should the account manager be able to complete intake on behalf of a client (e.g., over the phone)?

## Dependencies

- Design: Intake flow wireframes and step sequence need design review before development
- Content: Step descriptions, help text, and the "What happens next" copy need to be written
- Data: Agreement on the minimum required fields per client type
