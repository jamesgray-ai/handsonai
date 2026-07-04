# Feature: Task Assignment Engine

**Date:** 2026-03-07
**Author:** James Gray
**Status:** Draft
**Vision Brief:** [Client Onboarding Tracker](./vision-brief.md)
**Epic:** [Client Onboarding](https://github.com/jamesgray-ai/handsonai/issues/132)

## Summary

Automatically assign onboarding tasks to the right team members when a client completes intake, with clear ownership and deadlines based on role and availability.

## Motivation

When a new client completes the guided intake flow, someone has to figure out what happens next — and right now, that someone is an account manager working from memory and a spreadsheet. They manually create tasks, guess who's available, and hope nothing slips through the cracks. At 80 new clients per month, that's 80 rounds of "who should handle the welcome call?" and "is the implementation specialist free this week?"

The result: tasks get assigned unevenly (one person drowns while another has capacity), deadlines are inconsistent or missing entirely, and when someone is out sick, their tasks just... don't happen until someone notices. New account managers are especially vulnerable — they don't yet know who does what or what the standard task list even looks like.

This feature eliminates the guesswork. When a client completes intake, the system automatically creates all onboarding tasks, assigns each to the right person based on their role and current workload, and sets deadlines based on configurable SLAs. Every task has a clear owner and a deadline from the moment it's created.

## User Stories & Acceptance Criteria

### US-1 — Automatic task creation on intake completion

**As an** account manager, **I want** onboarding tasks to be automatically created when a client completes intake **so that** I don't have to manually set up a task list for every new client.

**Preconditions:**
1. `PRE-1.1` An intake completion event has fired for the client (emitted by Feature 1 — see Dependencies)
2. `PRE-1.2` An active task template exists defining the onboarding tasks to create

**Acceptance Criteria:**
1. `AC-1.1` `[MUST]` When a client submits the final step of the intake flow, the system creates all onboarding tasks defined in the active task template
2. `AC-1.2` `[MUST]` Each created task has a title, description, assigned team member, and deadline
3. `AC-1.3` `[MUST]` Tasks are created within 30 seconds of intake completion
4. `AC-1.4` `[MUST]` The account manager who owns the client relationship is notified that tasks have been created
5. `AC-1.5` `[SHOULD]` Task creation is idempotent — if the intake completion event fires twice, duplicate tasks are not created

**Postconditions:**
1. `POST-1.1` All template tasks for the client are persisted in a single transaction (all-or-none — see `NFR-2`)
2. `POST-1.2` A `tasks.created` event is emitted and the owning account manager has a notification

### US-2 — Role-based task routing

**As a** team member, **I want** tasks to be assigned to me based on my role **so that** I only receive tasks I'm qualified to handle.

**Preconditions:**
1. `PRE-2.1` Each task type in the template has a role mapping configured _(else `ERR-3` — task created unassigned, admin alerted)_

**Acceptance Criteria:**
1. `AC-2.1` `[MUST]` Each task type is mapped to a specific role (e.g., "welcome call" routes to account manager, "technical setup" routes to implementation specialist)
2. `AC-2.2` `[MUST]` Tasks are only assigned to team members with the matching role
3. `AC-2.3` `[SHOULD]` The role-to-task mapping is configurable by an admin without code changes
4. `AC-2.4` `[COULD]` A task type can be mapped to multiple roles (e.g., either an account manager or a senior CSM can handle a welcome call)

### US-3 — Availability-based assignment

**As a** team lead, **I want** tasks to be distributed based on team members' current workload **so that** no one person is overwhelmed while others sit idle.

**Preconditions:**
1. `PRE-3.1` At least one team member holding the required role is marked `available` _(else the fallback path applies — `AC-G.2`, `ERR-1`)_

**Acceptance Criteria:**
1. `AC-3.1` `[MUST]` When multiple team members share the same role, the system assigns the task to the team member with the fewest open onboarding tasks
2. `AC-3.2` `[MUST]` A team member can be marked as "unavailable" (e.g., out of office), and the system skips them during assignment
3. `AC-3.3` `[SHOULD]` If two team members have equal workload, either may be assigned (no specific tiebreaker required for MVP)
4. `AC-3.4` `[COULD]` Team members can set a maximum concurrent task limit

**Postconditions:**
1. `POST-3.1` Each created task is assigned to exactly one member (or the fallback), and the assignment audit log records the assignee and workload reason (see `AC-G.1`)

### US-4 — Deadline assignment

**As an** account manager, **I want** each task to have an automatic deadline **so that** the team knows when each step needs to be completed and clients aren't left waiting.

**Preconditions:**
1. `PRE-4.1` Each task type has an SLA duration configured on its template

**Acceptance Criteria:**
1. `AC-4.1` `[MUST]` Each task type has a configurable SLA (e.g., "welcome call" = 24 hours, "account configuration" = 48 hours)
2. `AC-4.2` `[MUST]` Deadlines are calculated from the time of intake completion
3. `AC-4.3` `[MUST]` Deadlines are visible on each task to the assigned team member
4. `AC-4.4` `[SHOULD]` SLA durations are configurable per task template by an admin

### Global Acceptance Criteria
1. `AC-G.1` `[MUST]` All task assignments are logged with timestamp, assigned team member, and reason for assignment (role match + workload)
2. `AC-G.2` `[MUST]` If no team member is available for a given role, the task is assigned to the team lead for that role and flagged for attention
3. `AC-G.3` `[SHOULD]` Assignment logic is deterministic — same inputs produce the same assignment (for debugging and audit)

## Scope

### In Scope
- Automatic task creation triggered by intake completion event from Feature 1
- Task template system (define which tasks are created, their role mapping, and SLA)
- Role-based routing of tasks to qualified team members
- Workload-based distribution within a role (least-loaded assignment)
- Configurable SLA deadlines per task type
- Unavailability marking for team members
- Fallback assignment to team lead when no one is available
- Assignment audit log

### Out of Scope
- Manual task reassignment UI (future feature — for now, reassignment is a database update)
- Escalation workflows for overdue tasks (covered by Feature 4: Automated Reminders)
- Client-facing task visibility (clients see their intake flow, not internal tasks)
- Calendar or schedule integration for availability (using open task count instead)
- Reporting or analytics on task assignment patterns
- Notification delivery mechanism (uses existing notification infrastructure)

## Approach

The task assignment engine has three components:

1. **Task templates** — A database table defining task types, their required role, SLA duration, and description. Seeded with default onboarding tasks, configurable via an admin interface.

2. **Assignment logic** — A service that listens for the intake completion event (emitted by Feature 1), generates tasks from templates, and assigns each to the least-loaded team member with the correct role. Runs server-side in the Node.js backend.

3. **Team member registry** — Extends the existing user model with role and availability status fields. Used by the assignment logic to determine eligible assignees.

The engine is event-driven: Feature 1's intake completion triggers task creation. Tasks are stored in a `tasks` table with foreign keys to the client and assigned team member.

## Data & Validation

**Fields:**

| Field | Type | Required | Rules / limits |
|-------|------|----------|----------------|
| Task title | text | yes | From the task template; 1–120 chars |
| Task description | text | yes | From the task template |
| Assigned team member | reference (user) | yes (or fallback) | Must hold the task's required role; unassigned only on invalid mapping (ERR-3) |
| Required role | enum | yes | From the team's defined role list |
| Deadline | datetime | yes | Computed as intake completion time + task SLA |
| SLA duration | duration | yes (on template) | Positive; configured per task type |
| Team member availability | enum | yes (on user) | `available` / `unavailable` |
| Assignment reason | text | yes (on log) | Role match + workload at assignment time |

**State transitions** (task lifecycle relevant to this feature):
- (none) → `assigned` on creation when an eligible team member exists
- (none) → `fallback_assigned` (flagged "needs attention") when no eligible member is available
- (none) → `unassigned` when the role mapping references a role with no members (ERR-3)

**Cross-field & business rules:**
- A task is assigned to the least-loaded available member holding the required role
- Deadlines are always derived from SLA + intake completion time, never set manually at creation
- All tasks for one intake are created in a single transaction — all or none (NFR-2)

## Roles & Permissions

| Role | Action | Allowed? | Condition |
|------|--------|----------|-----------|
| Admin | Create/edit task templates, role mappings, SLA durations | yes | — |
| Team member | View own assigned tasks | yes | Only tasks assigned to them |
| Team member | Toggle own availability | yes | Only their own status |
| Team lead | Receive fallback assignments | yes | For roles they lead (`ERR-1`) |
| Account manager | Be notified when tasks are created | yes | For clients they own |
| Team member | Reassign a task to someone else | no | Out of scope for MVP — reassignment is a DB update |

## Non-Functional Requirements

- **Performance:** `NFR-1` `[MUST]` All tasks for a single intake completion are created and assigned within 30 seconds; the assignment logic itself completes in under 2 seconds (remainder is event propagation and DB writes).
- **Reliability:** `NFR-2` `[MUST]` Task creation is transactional — either all tasks for an intake are created, or none are. Partial task creation never occurs.
- **Scalability:** `NFR-3` `[MUST]` Concurrent intake completions produce no race conditions in workload-based assignment (row-level locking or optimistic concurrency on the task-count query); verify with a concurrent-completion load test.

## Error States

| ID | Scenario | Expected Behavior | Priority |
|----|----------|-------------------|----------|
| `ERR-1` | No available team member for a role | Task is assigned to the team lead for that role. Task is flagged with a "needs attention" indicator. | `[MUST]` |
| `ERR-2` | Intake completion event fires twice (duplicate) | Second event is ignored — task creation is idempotent based on client ID + intake submission timestamp. | `[MUST]` |
| `ERR-3` | Invalid role mapping (task template references a role with no team members) | Task is created but left unassigned. Admin is notified via system alert. Assignment retries when a team member with that role is added. | `[SHOULD]` |
| `ERR-4` | Database transaction fails during task creation | All tasks for that intake are rolled back. Event is re-queued for retry (max 3 attempts). Account manager is notified if all retries fail. | `[MUST]` |

## Success Metrics & Instrumentation

- **Primary metric:** Percentage of onboarding tasks with a clear owner within 1 minute of intake completion — target 100% (current: 0%, all manual)
- **Secondary metrics:**
  - Average time from intake completion to all tasks assigned — target under 30 seconds
  - Task workload variance across team members with the same role — target <20% deviation from mean
  - Percentage of tasks requiring manual reassignment within 24 hours — target under 5%
- **Events to track:**
  - `tasks.created` — batch of tasks created for a client (includes count, client ID)
  - `task.assigned` — individual task assigned (includes role, assignee, workload at time of assignment)
  - `task.fallback_assigned` — task assigned to team lead due to no availability
  - `task.assignment_failed` — task could not be assigned (includes reason)
- **Evaluation timeline:** 2 weeks post-launch for assignment accuracy and speed; 4 weeks for workload distribution and reassignment rates

## Assumptions

- `ASM-1` The existing notification infrastructure is available and delivers to team members and account managers. This feature triggers notifications but does not build the delivery mechanism (see Out of Scope).
- `ASM-2` Each defined role normally has at least one team member; the fallback (`ERR-1`) and unassigned (`ERR-3`) paths handle the exceptions, but steady-state role coverage is assumed.
- `ASM-3` A team member's open-task count in the database accurately reflects real workload — assignment relies on it, since there is no calendar/schedule integration in the MVP.

## Dependencies & Prerequisites

- **Feature 1 (Guided Intake Flow):** Must be complete and emitting the intake completion event that triggers task creation
- **User model updates:** The existing user model needs role and availability fields — coordinate with the team to avoid migration conflicts
- **Task template seed data:** The initial set of onboarding tasks, their role mappings, and SLA durations must be defined with the CS team before development

## UI/UX Requirements

- **Admin template UI:** Simple CRUD interface for managing task templates — add/edit/remove task types, set role mappings, configure SLA durations. Table layout with inline editing.
- **Availability toggle:** Team members can toggle their availability status from their profile or a team settings page. Clear visual indicator (green/gray dot) of current status.
- **Task list view:** Assigned team members see their tasks with client name, task description, deadline, and status. Sortable by deadline. (Minimal for MVP — the full task management UI comes later.)

## Design Constraints

- Must use the existing user model — extend with new fields rather than creating a separate team member table
- Must be event-driven — triggered by Feature 1's completion event, not by polling or a cron job
- Must use the existing Node.js backend and PostgreSQL database — no new infrastructure
- Admin UI must use the existing React component library and design system
- Assignment logic must be stateless and deterministic — all state comes from the database at query time

## Verification

### Happy path
1. Configure task templates: "Welcome call" (account manager role, 24h SLA), "Technical setup" (implementation specialist, 48h SLA). _(AC-2.1, AC-4.1)_
2. Mark at least two account managers as available, with different open task counts
3. Complete a client intake flow (Feature 1) — all template tasks are created within 30 seconds, each with title, description, assignee, and deadline; the owning account manager is notified. _(AC-1.1, AC-1.2, AC-1.3, AC-1.4, NFR-1)_
4. Verify "Welcome call" is assigned to the account manager with fewer open tasks. _(AC-3.1)_
5. Verify "Technical setup" is assigned to an available implementation specialist (unavailable members are skipped). _(AC-2.2, AC-3.2)_
6. Verify deadlines are visible on each task and match the configured SLAs calculated from intake completion time. _(AC-4.2, AC-4.3)_
7. Verify the assignment audit log contains an entry for each task with role, assignee, and workload reason. _(AC-G.1)_

### Edge case: No available team member
1. Mark all implementation specialists as unavailable
2. Complete a client intake flow
3. Verify "Technical setup" is assigned to the team lead and flagged for attention. _(AC-G.2, ERR-1)_
4. Verify a `task.fallback_assigned` event is logged

### Edge case: Duplicate intake completion event
1. Complete a client intake flow
2. Manually re-fire the intake completion event for the same client
3. Verify no duplicate tasks are created. _(AC-1.5, ERR-2)_

### Edge case: Transaction failure
1. Inject a database failure mid-creation for one intake
2. Verify all tasks for that intake are rolled back (no partial set) and the event is re-queued for retry. _(NFR-2, ERR-4)_

### Edge case: Concurrent intake completions
1. Fire intake completion for several clients simultaneously (load test) while multiple team members share the same role
2. Verify assignment is race-free — each task counts toward workload exactly once, no member is assigned past the least-loaded rule, and creation+assignment stays within the 30s threshold. _(NFR-3)_

## Examples (Golden Path)

- `EX-1` **Input:** a client completes intake; templates are "Welcome call" (account-manager role, 24h SLA) and "Technical setup" (implementation-specialist role, 48h SLA); two account managers are available with 3 and 5 open tasks respectively → **Expected:** both tasks are created within 30s in one transaction; "Welcome call" is assigned to the AM with 3 open tasks; deadlines are set to completion + 24h and + 48h; `tasks.created` and per-task `task.assigned` events are logged. _(exercises AC-1.1, AC-3.1, AC-4.2, POST-1.1, POST-3.1)_
- `EX-2` **Input:** all implementation specialists are marked `unavailable` when a client completes intake → **Expected:** "Technical setup" is assigned to the team lead, flagged "needs attention", and a `task.fallback_assigned` event is logged. _(exercises AC-G.2, ERR-1 — violated `PRE-3.1`)_

## Definition of Done

- [ ] All `[MUST]` criteria pass: AC-1.1–1.4, AC-2.1–2.2, AC-3.1–3.2, AC-4.1–4.3, AC-G.1–G.2, NFR-1–3, ERR-1, ERR-2, ERR-4
- [ ] Every `[MUST]` criterion is covered by a verification step that has been run
- [ ] Every precondition (`PRE-1.1`–`PRE-4.1`) is enforced, or its violation is handled per the linked `ERR` row
- [ ] Build / CI passes
- [ ] NFR thresholds measured and met: tasks created+assigned <30s, assignment logic <2s, concurrent completions race-free under load test, creation is transactional
- [ ] All four `task*` analytics events fire and are visible where consumed
- [ ] Task template seed data defined with the CS team and loaded
- [ ] User model role + availability fields migrated without conflict

## Open Questions

- Should task templates vary by client type (e.g., enterprise vs. SMB), or is one template set sufficient for MVP?
- What roles exist on the team today, and what tasks map to each role?
- Should the admin UI for task templates be part of this feature, or can templates be seeded via database migration for MVP?
- How should the system handle intake re-submission (e.g., client completes intake twice) — create duplicate tasks or skip?

## Future Considerations

- Calendar integration — using Google Calendar or Outlook availability instead of manual toggle for smarter assignment
- Reassignment UI — allowing team leads to drag-and-drop reassign tasks when workload shifts
- Workload analytics — dashboard showing assignment patterns, SLA adherence rates, and team capacity utilization
- Client-type templates — different task sets for enterprise vs. SMB onboarding once we have data on divergent needs
- Task dependencies — sequential task ordering (e.g., "technical setup" can't start until "welcome call" is complete)

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-03-07 | Initial draft | James Gray |
| 2026-07-03 | Added per-story preconditions/postconditions, Assumptions, Roles & Permissions, and Golden Path examples | James Gray |
