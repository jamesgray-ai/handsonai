# Feature: Guided Intake Flow

**Date:** 2026-03-07
**Author:** James Gray
**Status:** Draft
**Vision Brief:** [Client Onboarding Tracker](./vision-brief.md)
**Epic:** [Client Onboarding](https://github.com/jamesgray-ai/handsonai/issues/132)

## Summary

Walk new clients through a structured, step-by-step intake flow that collects all required onboarding information with progress tracking and save-and-resume support.

## Motivation

New clients sign up but have no clear path through onboarding. They don't know what information to provide, in what order, or why it matters. Account managers can't tell where a client is in the process — or whether they've started at all. The result: 30% of clients go quiet in the first week, and the team wastes hours chasing them with manual follow-up emails.

This isn't a content problem — a self-serve knowledge base already exists and has a 23% completion rate. The gap is contextual, step-by-step guidance that collects structured data while showing clients exactly where they are and what's next.

The guided intake flow solves this by giving clients a structured, step-by-step experience that collects everything the team needs to begin serving them — while giving account managers visibility into exactly where each client stands.

**Target users:**

- **New clients** — Non-technical professionals who just signed a contract. They're motivated but don't know what to do next. They need clarity, not complexity. They want to feel like they're making progress, not filling out a bureaucratic form.
- **Account managers** — Internal team members responsible for client success. They need to know which clients have completed intake, which are in progress, and which have stalled — without checking a spreadsheet or sending a "just checking in" email.

## User Stories & Acceptance Criteria

### US-1 — Step-by-step information collection

**As a** new client, **I want to** provide my information through a guided, multi-step flow **so that** I know exactly what's needed and can complete it without confusion.

**Acceptance Criteria:**
1. `AC-1.1` `[MUST]` Intake is divided into logical steps: company info, primary contact details, project goals, timeline and constraints, and billing setup
2. `AC-1.2` `[MUST]` Each step shows only the fields relevant to that step — no overwhelming single-page form
3. `AC-1.3` `[MUST]` Required fields are clearly marked; optional fields explain why providing them is helpful
4. `AC-1.4` `[MUST]` Client can see which step they're on and how many remain (e.g., "Step 3 of 5")
5. `AC-1.5` `[SHOULD]` Each step includes a brief explanation of why the information is needed

### US-2 — Progress persistence

**As a** new client, **I want to** save my progress and come back later **so that** I don't have to complete everything in one sitting.

**Acceptance Criteria:**
1. `AC-2.1` `[MUST]` Progress is automatically saved after each step is completed
2. `AC-2.2` `[MUST]` When a client returns, they resume from where they left off — not from the beginning
3. `AC-2.3` `[MUST]` A confirmation message shows when progress is saved (e.g., "Your progress has been saved. You can close this tab and come back anytime.")
4. `AC-2.4` `[SHOULD]` Incomplete intake flows are retained for at least 30 days before being archived

### US-3 — Intake status visibility for account managers

**As an** account manager, **I want to** see which step each client is on in the intake flow **so that** I can proactively reach out to clients who are stuck.

**Acceptance Criteria:**
1. `AC-3.1` `[MUST]` Account manager view shows a list of all assigned clients with their current intake step
2. `AC-3.2` `[MUST]` Clients are sortable by status: not started, in progress, completed, stalled
3. `AC-3.3` `[MUST]` "Stalled" is defined as no activity for 48+ hours while intake is incomplete
4. `AC-3.4` `[SHOULD]` Clicking a client shows their completed steps and the specific step where they stopped

### US-4 — Intake completion and handoff

**As a** new client, **I want to** receive a clear confirmation when I've completed intake **so that** I know what happens next and who to expect to hear from.

**Acceptance Criteria:**
1. `AC-4.1` `[MUST]` Completion screen shows a summary of all submitted information
2. `AC-4.2` `[MUST]` Client can review and edit any section before final submission
3. `AC-4.3` `[MUST]` After submission, client sees a "What happens next" message explaining the next steps in onboarding
4. `AC-4.4` `[MUST]` Account manager is notified immediately when a client completes intake
5. `AC-4.5` `[COULD]` Client receives a confirmation email with a copy of their submitted information

### Global Acceptance Criteria
1. `AC-G.1` `[MUST]` Analytics events fire at each step transition to track drop-off rates per step
2. `AC-G.2` `[MUST]` All intake data is validated before advancing to the next step
3. `AC-G.3` `[SHOULD]` Intake flow loads within 2 seconds on a standard broadband connection

## Scope

### In Scope
- Multi-step intake form with progress indicator
- Per-step field validation and save
- Save-and-resume functionality with 30-day retention
- Completion summary with review-and-edit before final submission
- Account manager status view (lightweight, intake-specific — not the full dashboard)
- Step-transition analytics events for drop-off tracking
- "What happens next" messaging on completion

### Out of Scope
- **Task assignment engine** — Automatically assigning onboarding tasks to team members after intake is complete (Feature 2)
- **Progress dashboard** — The aggregate dashboard showing all clients' onboarding status across all features (Feature 3). The account manager view described in Story 3 is a lightweight, intake-specific status view — not the full dashboard.
- **Automated reminders** — Sending nudge emails or notifications to clients who stall (Feature 4). For the MVP, account managers will manually follow up based on the status view.
- **Completion report** — The formal summary report generated at the end of the full onboarding process (Feature 5)
- **Client-type customization** — Different intake flows for enterprise vs. SMB clients. The MVP uses a single flow for all client types.
- **Integrations** — Pushing intake data to CRM, billing, or project management tools. Data stays in the onboarding system for now.

## Approach

The intake flow is a multi-step React form backed by a REST API. Each step maps to a discrete API endpoint so saves are atomic — no partial-step data loss. Client progress is stored server-side and keyed to their account, enabling save-and-resume across devices.

The account manager status view is a simple list endpoint that aggregates intake progress across assigned clients, with a "stalled" flag computed from the last activity timestamp.

Step-transition events are sent to the analytics pipeline on each step completion and on final submission, giving us per-step drop-off data from day one.

## Data & Validation

**Fields:**

| Field | Type | Required | Rules / limits |
|-------|------|----------|----------------|
| Company name | text | yes | 1–120 chars |
| Industry | enum | yes | From the standard industry list |
| Primary contact name | text | yes | 1–80 chars |
| Primary contact email | email | yes | Valid email format; used for all intake notifications |
| Primary contact phone | text | no | E.164 format if provided |
| Project goals | text | yes | 1–2,000 chars |
| Target start date | date | no | Must be today or later |
| Budget range | enum | no | From the predefined budget bands |
| Billing contact email | email | yes (billing step) | Valid email format |

**State transitions** (intake status):
- `not started` → `in progress` when the client completes Step 1
- `in progress` → `stalled` when no activity for 48+ hours while incomplete
- `in progress` / `stalled` → `completed` when the client submits the final step

**Cross-field & business rules:**
- A step cannot be advanced until all required fields on it pass validation
- Billing contact email may match the primary contact email (no uniqueness requirement)

## Non-Functional Requirements

- **Performance:** `NFR-1` `[MUST]` Each step transition (save + load next) completes in under 1 second at p95; intake flow initial load completes in under 2 seconds on a standard broadband connection.
- **Accessibility:** `NFR-2` `[MUST]` All form elements meet WCAG 2.1 AA — keyboard navigable, screen-reader compatible, sufficient color contrast (verify: axe DevTools, zero critical violations).
- **Compatibility:** `NFR-3` `[MUST]` Fully usable on mobile (single-column, 44px+ touch targets) and on the latest two versions of Chrome, Safari, Firefox, and Edge.
- **Reliability:** `NFR-4` `[MUST]` Auto-save never fails silently — a failed save surfaces an error message with a retry option.

## Error States

| ID | Scenario | Expected Behavior | Priority |
|----|----------|-------------------|----------|
| `ERR-1` | Invalid input on a required field | Inline validation message appears below the field. Step does not advance until corrected. | `[MUST]` |
| `ERR-2` | Auto-save fails (network error) | Toast notification: "Unable to save. Check your connection and try again." Retry button available. | `[MUST]` |
| `ERR-3` | Session timeout (inactive 60+ minutes) | Client is prompted to re-authenticate. Progress up to the last completed step is preserved. | `[MUST]` |
| `ERR-4` | Client navigates away mid-step | Unsaved fields on the current step are lost. Completed steps are preserved. Browser shows "unsaved changes" warning. | `[SHOULD]` |
| `ERR-5` | Intake link accessed after completion | Client sees their submitted summary in read-only mode with a message: "Your intake is complete." | `[MUST]` |

## Success Metrics & Instrumentation

- **Primary metric:** Intake completion rate — target 90% within 48 hours of starting (current estimate: ~70%)
- **Secondary metrics:**
  - Average time to complete intake — target under 30 minutes of active time (current: unknown, likely days)
  - Account manager time spent on intake follow-up — target under 1 hour/week per AM (current: ~5 hours/week)
  - Client-reported clarity on next steps — target 4.5+ out of 5 on post-intake survey
- **Events to track:**
  - `intake.started` — client opens the intake flow
  - `intake.step_completed` — client completes a step (includes step number)
  - `intake.step_abandoned` — client leaves mid-step (includes step number and time spent)
  - `intake.resumed` — client returns to a previously started flow
  - `intake.completed` — client submits the final step
- **Evaluation timeline:** 2 weeks post-launch for early signal on completion rates; 6 weeks for full assessment including AM time savings and client survey data

## Dependencies & Prerequisites

- Design: Intake flow wireframes and step sequence need design review before development
- Content: Step descriptions, help text, and the "What happens next" copy need to be written
- Data: Agreement on the minimum required fields per client type
- Infrastructure: Analytics pipeline must accept custom events for step-transition tracking

## UI/UX Requirements

- **Key interactions:** Progressive disclosure — one step visible at a time with a progress bar showing overall position. Forward/back navigation between completed steps. Review-and-edit screen before final submission.
- **Copy & messaging:** Each step has a short heading (e.g., "Tell us about your company") and a one-line explanation of why the information matters. Completion screen includes a "What happens next" section with specific next steps and timeline expectations.
- **Responsive behavior:** Full-width single-column layout on mobile. Side progress indicator on desktop, top bar on mobile. Touch-friendly input targets (minimum 44px).
- **Design references:** Stripe's onboarding flow (progressive disclosure pattern), Typeform (conversational step-by-step feel)

## Design Constraints

- Must use the existing React component library and design system — no new UI framework
- Must work with the existing Node.js/PostgreSQL backend — no new infrastructure
- Intake data schema must be extensible (JSON column or normalized tables) — we expect to add fields as we learn what's needed
- Must not require JavaScript-disabled fallback for MVP, but core form elements should use semantic HTML for accessibility

## Verification

### Happy path
1. Open the intake flow as a new client; complete Step 1 (company info) — progress saves, step indicator shows "Step 1 of 5", then advances to Step 2 within 1s. _(AC-1.1, AC-1.2, AC-1.4, AC-2.1, AC-2.3, NFR-1)_
2. Confirm required fields are marked and each step explains why the info is needed. _(AC-1.3, AC-1.5)_
3. Close the browser tab and reopen the intake link — you resume at Step 2, not the beginning. _(AC-2.2)_
4. Complete all remaining steps — the completion summary shows all submitted data; data was validated before each advance. _(AC-4.1, AC-G.2)_
5. Edit one field on the summary screen and re-submit — the change is saved. _(AC-4.2)_
6. Submit the final step — a "What happens next" message appears and the account manager is notified immediately. _(AC-4.3, AC-4.4)_
7. Open the account manager view — the client shows as "completed", list is sortable by status. _(AC-3.1, AC-3.2)_
8. Verify analytics events fired for each step transition. _(AC-G.1)_
9. Re-open the completed intake link — it shows the submitted summary in read-only mode. _(ERR-5)_

### Edge case: Stalled client detection
1. Start intake as a new client — complete Step 1 only
2. Wait 48+ hours (or simulate time passage in test)
3. Check account manager view — client shows as "stalled" with last activity on Step 1; clicking shows where they stopped. _(AC-3.3, AC-3.4)_

### Edge case: Network failure and invalid input during save
1. Enter an invalid value in a required field and attempt to advance — inline validation appears and the step does not advance. _(ERR-1)_
2. Complete Step 1 with network connectivity, then disable network before completing Step 2
3. Attempt to advance — error toast appears with a retry option (no silent failure). _(ERR-2, NFR-4)_
4. Re-enable network and retry — the step saves successfully

### Edge case: Session timeout
1. Start intake, complete Step 1, then remain inactive for 60+ minutes
2. Return and attempt to continue — client is prompted to re-authenticate; progress up to the last completed step is preserved. _(ERR-3)_

### Non-functional checks
1. Run axe DevTools on each step and the summary screen — zero critical violations; tab through every field and submit using the keyboard only. _(NFR-2)_
2. Complete a full intake on a phone (single-column, 44px+ touch targets) and on the latest two versions of Chrome, Safari, Firefox, and Edge. _(NFR-3)_

## Definition of Done

- [ ] All `[MUST]` criteria pass: AC-1.1–1.4, AC-2.1–2.3, AC-3.1–3.3, AC-4.1–4.4, AC-G.1–G.2, NFR-1–4, ERR-1–3, ERR-5
- [ ] Every `[MUST]` criterion is covered by a verification step that has been run
- [ ] Build / CI passes
- [ ] NFR thresholds measured and met: step transition <1s p95, initial load <2s, WCAG 2.1 AA (axe clean), no silent auto-save failures
- [ ] All five `intake.*` analytics events fire and are visible in the analytics pipeline
- [ ] Mobile and the latest two versions of Chrome, Safari, Firefox, Edge verified
- [ ] Step copy and "What happens next" content reviewed and in place

## Open Questions

- Should we allow clients to skip optional steps entirely, or require them to at least view each step?
- What's the right tone for the intake flow — professional and efficient, or warm and conversational?
- Should the account manager be able to complete intake on behalf of a client (e.g., over the phone)?

## Future Considerations

- Client-type customization — different intake steps for enterprise vs. SMB clients, evaluated after we have data on where client types diverge
- Delegation feature — allowing a client to forward intake to their office manager to complete on their behalf
- CRM integration — pushing intake data to Salesforce or HubSpot automatically on completion
- Conditional steps — showing or hiding steps based on answers to previous steps (e.g., skip billing if client is on a custom contract)

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-03-07 | Initial draft | James Gray |
