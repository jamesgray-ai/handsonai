---
name: writing-feature-prds
description: Use when starting a new feature, defining requirements before implementation, or when the user says "new feature", "create a spec", "create a PRD", or "feature PRD".
user-invocable: true
---

# Feature PRD Workflow

Guide the user through creating a well-defined feature PRD (Product Requirements Document) before implementation.

**Important:** A PRD describes **one feature** — a single, buildable piece of work. If the user's idea is bigger than one feature (multiple epics, many capabilities), they should run `/agentic-coding:writing-vision-briefs` first to break it down. This skill takes one feature as input, not an entire vision.

## When to Use This Skill

- User wants to build a new feature
- User mentions "create a spec", "create a PRD", "new feature", or "feature PRD"
- User wants to define requirements before coding
- User has completed a Vision Brief and is ready to spec out one of the features from the breakdown

## Workflow Overview

| Phase | Goal |
|-------|------|
| 1. Define | Create PRD in a `specs/` directory |
| 2. Stress-test | Review for gaps and ambiguities |
| 3. Track | GitHub issue with `type:feature` label |
| 4. Handoff | Move to plan mode for implementation planning |

---

## Phase 1: Define the Feature

**First, figure out where the user is coming from:**

**Path A — Coming from a Vision Brief (recommended flow):**
If the user references a Vision Brief or a specific feature from a breakdown (e.g., "Write a PRD for email verification from specs/onboarding-vision.md"):

1. Read the Vision Brief
2. Find the specific feature in the Feature Breakdown section
3. Systematically translate each Vision Brief section into PRD content using this mapping:

| Vision Brief Section | PRD Section | How to Translate |
|---------------------|-------------|-----------------|
| The Problem | Motivation | Scope the problem to this specific feature. Keep quantification from the brief. |
| Who Feels It | User Stories | Use as the user type(s) in story format. |
| Stakeholders | (note in issue) | Carry over to the GitHub issue body for review assignments. |
| Current State | Motivation | Add as context for why the current state is insufficient. |
| Alternatives Considered | Design Constraints | Note what was ruled out and why — these become constraints. |
| Strategic Context | Motivation | Include urgency signals that apply to this feature. |
| The Vision | Summary | Scope the vision statement down to this one feature. |
| Key Capabilities | User Stories + AC | Map relevant capabilities to stories with `[MUST]`/`[SHOULD]`/`[COULD]` criteria. |
| Inspiration | UI/UX Requirements | Pull in relevant design references for user-facing features. |
| What Success Looks Like | Success Metrics | Translate early signals and real outcomes into measurable metrics for this feature. |
| Risks & Assumptions | Open Questions + Assumptions | Risks you're unsure about → Open Questions. Things you're relying on being true but won't build/verify → the Assumptions section. |
| Dependencies | Dependencies & Prerequisites | Carry over dependencies relevant to this feature. |
| Constraints & Context | Design Constraints + NFRs | Split into design constraints and non-functional requirements. |
| Future Considerations | Future Considerations | Carry over items relevant to this feature's domain. |

4. Confirm with the user: "I'm writing the PRD for **[Feature Name]** from your Vision Brief. I've pulled in the problem, users, and relevant capabilities. Anything you'd change before I draft the full PRD?"

**Path B — Starting fresh (no Vision Brief):**
If the user doesn't mention a Vision Brief:

1. Ask: "Do you have a Vision Brief for this idea? If so, point me to it and I'll use it as a head start. If not, no worries — I'll walk you through the questions."
2. If they provide one, follow Path A above
3. If they don't have one, check the scope: does their idea sound like one feature, or something bigger?
    - If it sounds like one feature, proceed with the questions below
    - If it sounds bigger (multiple capabilities, multiple user types, multiple workflows), suggest they start with a Vision Brief first: "This sounds like it might be bigger than one feature. Want to run `/agentic-coding:writing-vision-briefs` first to break it into pieces? That way we can spec each piece clearly."

Ask the user these questions to understand the feature:

1. **What feature are you building?** (one sentence)
2. **What problem does it solve?** (why does this need to exist?)
3. **Who are the users?** (user type for user stories — and are there distinct roles with different permissions?)
4. **What should happen?** (key behaviors/requirements — and if the feature collects or stores data, what are the fields and their validation rules? What state should the system be in *afterward*? If you can, give one concrete example: input → expected result.)
5. **What must already be true before each behavior applies?** (preconditions — user state, data that must already exist, permissions already held, a prior step already completed). Don't expect a full list here — you'll propose likely preconditions per story during drafting (see "Deriving Preconditions" below); this question just surfaces the obvious ones.
6. **What is explicitly NOT part of this feature?** (scope boundaries — prevents scope creep)
7. **Are there performance, security, or accessibility requirements?** Push for *concrete, measurable* targets — "response under 1s at p95," "WCAG 2.1 AA," "auth required on every write" — because these become testable NFRs. If the user says "nothing special," record an explicit baseline (e.g., "page loads under 3s") rather than leaving it silent — an untestable NFR is no NFR.
8. **What should happen when things go wrong?** (error states — invalid input, network failure, missing data, permission denied). If this is a simple feature, a brief answer is fine.
9. **What are you assuming is already true** about the environment, users, or data that this feature won't build or verify? (assumptions — e.g., "the email provider is already configured," "users are on modern browsers"). These are different from dependencies: an assumption is believed-but-unverified; a dependency must exist first.
10. **Does this change existing behavior, data, or URLs?** (migration needs — if yes, we'll need a migration and rollback plan). If no, skip the Migration section in the PRD.
11. **What does this depend on?** (other features, data sources, APIs, tools that must exist first). If nothing, skip the Dependencies section.
12. **How will you measure success after launch?** (primary metric, what to track, when to evaluate). If the user isn't sure, help them define at least one leading indicator.

Then create a PRD file. Use this structure for the PRD:

### PRD Template

```markdown
# Feature: [Feature Name]

**Epic:** [Epic Name] (issue #XX) — omit if standalone feature
**Vision Brief:** specs/[name]-vision.md — omit if no Vision Brief exists

## Summary
One-sentence description of the feature.

> *Example: "Add email verification to the signup flow so new accounts are confirmed before accessing the workspace."*

## Motivation
Why this feature needs to exist. What problem it solves. Include quantification where available.

> *Example: "12% of new accounts are created with invalid or disposable email addresses, generating ~40 bounced welcome emails per week and inflating our active user count. This wastes marketing spend on unreachable users and skews our activation metrics."*

## User Stories & Acceptance Criteria

### US-1 — [Short title]
**As a** [user type], **I want** [goal] **so that** [benefit].

**Preconditions:** _(state that must hold before this story's behavior applies — omit if none)_
1. `PRE-1.1` [Entry-state that must be true — e.g., "User is authenticated"]
2. `PRE-1.2` [e.g., "A syntactically valid email was submitted"]

**Acceptance Criteria:**
1. `AC-1.1` `[MUST]` [Yes/no verifiable statement]
2. `AC-1.2` `[MUST]` [Another verifiable statement]
3. `AC-1.3` `[SHOULD]` [A desirable but non-blocking criterion]

**Postconditions:** _(the end-state this story guarantees on success — omit for trivial/read-only stories, or when the ACs already fully capture the end-state)_
1. `POST-1.1` [Resulting state — e.g., "Account is marked verified and persisted"]

> *Example:*
> ### US-1 — Email verification on signup
> **As a** new user, **I want** to verify my email during signup **so that** my account is secured and I receive important notifications.
>
> **Preconditions:**
> 1. `PRE-1.1` The signup form was submitted with a syntactically valid email _(else `ERR-1`)_
> 2. `PRE-1.2` No verified account already exists for that email _(else `ERR-4`)_
>
> **Acceptance Criteria:**
> 1. `AC-1.1` `[MUST]` Verification email is sent within 30 seconds of form submission
> 2. `AC-1.2` `[MUST]` Clicking the verification link activates the account and redirects to the dashboard
> 3. `AC-1.3` `[MUST]` Unverified accounts cannot access workspace features
> 4. `AC-1.4` `[SHOULD]` "Resend verification" button is available on the pending screen
> 5. `AC-1.5` `[COULD]` Verification link includes the user's name in the email greeting
>
> **Postconditions:**
> 1. `POST-1.1` The account is persisted with `verified = true` and a verified-at timestamp
> 2. `POST-1.2` A `welcome_email_sent` event is emitted for the activated account

### US-2 — [Short title]
**As a** [user type], **I want** [goal] **so that** [benefit].

**Preconditions:** _(omit if none)_
1. `PRE-2.1` [Entry-state that must be true]

**Acceptance Criteria:**
1. `AC-2.1` `[MUST]` [Yes/no verifiable statement]

### Global Acceptance Criteria
_Criteria that apply across all stories (e.g., performance, accessibility). Omit if none._
1. `AC-G.1` `[MUST]` [Yes/no verifiable statement]

## Scope

### In Scope
- [What this feature includes]

### Out of Scope
- [What this feature explicitly does NOT include]

## Approach
High-level technical approach and key design decisions. Keep this brief — detailed implementation planning happens in plan mode.

## Data & Validation
_Omit for features with no meaningful data model (static pages, copy-only changes). For anything that collects, stores, or validates data, specify the shape and rules so the build matches intent. This is still **what**, not **how** — describe fields and rules, not table schemas or column types in SQL._

**Fields:**

| Field | Type | Required | Rules / limits |
|-------|------|----------|----------------|
| [field name] | [text / number / email / date / enum / …] | [yes / no] | [format, min/max, allowed values, uniqueness] |

**State transitions** _(only if the feature moves through states):_
- [State A] → [State B] when [condition]

**Cross-field & business rules:** [Rules not captured per-field — e.g., "end date must be after start date"; "at least one contact method required"]

## Roles & Permissions
_Who can do what. Omit for single-role features. This feeds story preconditions (authorization) and error states (permission denied), so keep it consistent with both._

| Role | Action | Allowed? | Condition |
|------|--------|----------|-----------|
| [role] | [action] | [yes / no] | [when / scoping constraint — e.g., "only records they own"] |

> *Example:*
> | Role | Action | Allowed? | Condition |
> |------|--------|----------|-----------|
> | Member | Verify own email | yes | — |
> | Member | Resend verification | yes | Only for their own pending account |
> | Admin | Manually mark an account verified | yes | Any account in their workspace |

## Non-Functional Requirements
_Each NFR is a testable statement, just like an acceptance criterion: an ID, a priority tag, and a **concrete, measurable threshold** — plus how to verify it where the method isn't obvious. Include only relevant categories. If the feature truly has no special requirement in a category, record an explicit baseline (e.g., "page loads under 3s") rather than vague prose or silence. "Fast" and "secure" are not testable; "under 1s at p95" and "all inputs server-side validated" are._

- **Performance:** `NFR-1` `[MUST]` [Concrete threshold — e.g., "Each request completes in under 500ms at p95 under normal load"]
- **Security:** `NFR-2` `[MUST]` [e.g., "All user input is validated server-side; auth required on every write endpoint"]
- **Accessibility:** `NFR-3` `[SHOULD]` [e.g., "Meets WCAG 2.1 AA — verify with axe DevTools, zero critical violations"]
- **Scalability:** [e.g., "Handles 1,000 concurrent users with no degradation below the performance threshold"]
- **Reliability:** [e.g., "Failed writes retry once after 5s; surface an error to the user if still failing"]
- **Compatibility:** [e.g., "Works on the latest two versions of Chrome, Safari, Firefox, and Edge"]

## Error States
_What should happen when things go wrong? Cover the most likely failure scenarios. Each row is a testable expectation — give it an ID and a priority. Every `[MUST]` error behavior must be covered by a step in the Verification section. A violated precondition (`PRE-n.m`) that isn't silently enforced belongs here as an `ERR` row._

| ID | Scenario | Expected Behavior | Priority |
|----|----------|-------------------|----------|
| `ERR-1` | [Error scenario 1] | [What the user sees/what happens] | `[MUST]` |
| `ERR-2` | [Error scenario 2] | [What the user sees/what happens] | `[MUST]` |

> *Example:*
> | ID | Scenario | Expected Behavior | Priority |
> |----|----------|-------------------|----------|
> | `ERR-1` | Invalid email format entered (violates `PRE-1.1`) | Inline validation message: "Please enter a valid email address." Form does not submit. | `[MUST]` |
> | `ERR-2` | Verification link expired (>24h) | Landing page shows "Link expired" with a "Resend verification" button. | `[MUST]` |
> | `ERR-3` | Email delivery fails | System retries once after 5 minutes. If still failed, logs error and shows "Didn't receive it?" prompt. | `[SHOULD]` |
> | `ERR-4` | Email already has a verified account (violates `PRE-1.2`) | Message: "That email is already registered. Try signing in." Form does not create a duplicate. | `[MUST]` |

## Success Metrics & Instrumentation
_How will you know this feature is working? Define what to measure and when to evaluate._

- **Primary metric:** [The one number that tells you this worked]
- **Secondary metrics:** [Supporting indicators]
- **Events to track:** [Specific user actions or system events to instrument]
- **Evaluation timeline:** [When to check — e.g., "2 weeks post-launch for early signal, 6 weeks for full assessment"]

## Assumptions
_Things believed true but NOT verified or built by this feature. If an assumption turns out wrong, the design may need to change. Omit if none._

- `ASM-1` [e.g., "The transactional email provider is already configured and can deliver to external domains"]
- `ASM-2` [e.g., "Users access the app on modern evergreen browsers"]

_How this differs from neighbours: an assumption you're **sure must** be true → promote it to a **Dependency** (something to verify/build first); one you're **unsure** about → move it to **Open Questions** (something to resolve)._

## Dependencies & Prerequisites
_Omit this section if there are no dependencies._

- [Feature, data source, API, or tool that must exist first]
- [Decision that must be made before implementation]

## Migration & Rollback
_Omit this section if the feature doesn't change existing behavior, data, or URLs._

- **Migration plan:** [How existing users/data transition to the new behavior]
- **Rollback plan:** [How to revert if something goes wrong]
- **Backwards compatibility:** [What stays the same for existing users during transition]

## UI/UX Requirements
_Omit this section for non-user-facing features (APIs, background jobs, infrastructure)._

- **Key interactions:** [Primary user flows and interaction patterns]
- **Copy & messaging:** [Key labels, error messages, confirmation text]
- **Responsive behavior:** [How it adapts across screen sizes, if applicable]
- **Design references:** [Links to wireframes, mockups, or inspiration screenshots]

## Design Constraints
Constraints the implementation must respect — technical boundaries, conventions, and decisions that limit how the feature can be built. This is NOT an implementation plan.

- [Constraint 1 — e.g., "Must use the existing auth middleware, not a custom solution"]
- [Constraint 2 — e.g., "Must work without JavaScript for core functionality"]
- [Constraint 3 — e.g., "Must not introduce new runtime dependencies"]

## Verification
Step-by-step instructions to verify the feature works end-to-end after implementation. Cover the happy path and at least one error/edge case. Annotate each step with the criteria IDs it verifies, in parentheses — e.g. `_(AC-1.2, NFR-1)_`.

**Coverage rule:** Every `[MUST]` criterion — story AC, Global AC, NFR, and Error State — must be covered by at least one verification step. This is what lets an agent (and you) confirm nothing required ships untested.

**Precondition setup:** where a step depends on a precondition, **arrange that `PRE` state as setup** before the action — e.g., "Given `PRE-1.1` holds (a valid email was submitted), click the link → …". A step whose preconditions aren't arranged will fail for the wrong reason.

> *Example:*
> ### Happy path
> 1. **Setup:** submit the signup form with a valid, unregistered email _(establishes `PRE-1.1`, `PRE-1.2`)_ → verification email arrives within 30s. _(AC-1.1)_
> 2. Click the verification link → account activates and redirects to the dashboard. _(AC-1.2, POST-1.1)_
> 3. Before verifying, attempt to open a workspace page → access is blocked. _(AC-1.3)_
>
> ### Edge case: invalid input
> 1. Enter a malformed email → inline error appears, form does not submit. _(ERR-1, violates PRE-1.1)_

## Examples (Golden Path)
_One or more concrete worked examples: input → expected output. An agentic coding model builds more accurately from a worked example than from prose rules. Reference the story/AC each example exercises. Omit only if the ACs and Data & Validation rules already leave nothing to a concrete example._

- `EX-1` **Input:** [concrete input] → **Expected:** [concrete output] _(exercises AC-1.1, AC-1.2)_

> *Example:*
> - `EX-1` **Input:** signup submitted with `ada@example.com` (no existing account) → **Expected:** verification email sent within 30s; on link click, account row shows `verified = true` and the user lands on `/dashboard`. _(exercises AC-1.1, AC-1.2, POST-1.1)_

## Definition of Done
_The gate for calling this feature complete — every box checked before it ships. This is the feature-specific complement to the verification steps above._

- [ ] All `[MUST]` acceptance criteria pass (story, Global, NFR, Error State)
- [ ] Every `[MUST]` criterion is covered by a verification step that has actually been run
- [ ] Every precondition (`PRE-n.m`) is enforced, or its violation is handled per the linked `ERR` row
- [ ] Build / CI passes
- [ ] NFR thresholds are measured and met (not assumed)
- [ ] Instrumentation events fire and are visible where they're consumed
- [ ] Migration and rollback executed and tested (if the Migration section applies)
- [ ] Docs / changelog updated (if applicable)

## Open Questions
- [Any unresolved decisions or questions]

## Future Considerations
_Ideas that came up during requirements gathering but are out of scope for this feature. A parking lot for good ideas worth remembering._

- [Future idea 1]
- [Future idea 2]

## Revision History
_Track significant changes to this PRD after initial draft._

| Date | Change | Author |
|------|--------|--------|
| [date] | Initial draft | [name] |
```

### Output Location

Choose the PRD location based on what exists in the repo:
1. If a `specs/` directory exists, use `specs/[feature-name]-prd.md`
2. If a `docs/specs/` directory exists, use `docs/specs/[feature-name]-prd.md`
3. If the repo's CLAUDE.md specifies a spec output location, use that
4. Otherwise, create `specs/[feature-name]-prd.md`

### Writing User Stories & Acceptance Criteria

Each user story gets its own acceptance criteria directly beneath it. This keeps requirements traceable — you can verify which criteria map to which user goal without jumping between sections.

**Story guidelines:**
- Write one story per distinct user goal (not one per persona doing the same thing)
- Different personas with different goals get separate stories
- A story without acceptance criteria is incomplete
- If a single requirement covers all stories (e.g., "Page loads in under 2 seconds"), place it in the **Global Acceptance Criteria** subsection after the last story

**Stable IDs (you assign these as you draft — the author never hand-maintains them):**
- **User stories:** `US-1`, `US-2`, … — give each story its own ID on the heading, not just a title.
- **Story preconditions:** `PRE-<story#>.<n>` — e.g. `PRE-1.1` is the first precondition of `US-1`. The story is this skill's "use case"; its preconditions and postconditions bracket the entry and exit state around the acceptance criteria.
- **Story acceptance criteria:** `AC-<story#>.<n>` — e.g. `AC-1.1` is the first criterion of `US-1`. The story number is baked into the ID so every criterion visibly traces to its story.
- **Story postconditions:** `POST-<story#>.<n>` — e.g. `POST-1.1` is the first postcondition of `US-1`.
- **Global acceptance criteria:** `AC-G.1`, `AC-G.2`, …
- **Non-functional requirements:** `NFR-1`, `NFR-2`, …
- **Error states:** `ERR-1`, `ERR-2`, …
- **Assumptions:** `ASM-1`, `ASM-2`, …
- **Golden examples:** `EX-1`, `EX-2`, …

**ID stability rule:** IDs are permanent. When adding stories or criteria later, append new numbers — **never renumber existing ones**, because plans, tests, and the GitHub issue reference them. If a story or criterion is dropped, retire its number rather than reusing it.

**Acceptance criteria rules:**
- Use numbered list (not checkboxes)
- Lead each criterion with its ID, then its priority tag (e.g. `AC-1.1` `[MUST]` …)
- Write yes/no verifiable statements
- Tag each criterion with priority: `[MUST]` (required for launch), `[SHOULD]` (important but not blocking), or `[COULD]` (nice to have, build if time permits)
- Focus on *what*, not *how*
- Use active voice ("Error message is displayed" not "User sees error")
- Include concrete expected values when possible
- Each criterion must be testable by running a specific command, visiting a URL, or checking a specific output

### Deriving Preconditions

A user story is this skill's "use case." Its **Preconditions** describe the entry state, and its **Postconditions** describe the exit state, that bracket the acceptance criteria. Don't wait for the user to volunteer preconditions — most people can't enumerate their own entry-state. **Propose them yourself.**

For each story, walk this checklist and list every category that applies as a `PRE` item, then confirm or prune with the user:

- **Authentication** — must the user be signed in?
- **Authorization / role** — does the action require a specific role, or ownership of the target record?
- **Data existence** — must a record, parent, or resource already exist for this to operate on?
- **Prior-step completion** — must an earlier workflow step already have finished (e.g., "intake is complete")?
- **Resource / quota availability** — seats, credits, rate limits, an available assignee?
- **Feature flag / configuration** — must something be enabled or configured first?
- **Input-validity state** — must the input already be in a valid/normalized state before this behavior runs?

**Then close the loop:** each `PRE` should either be *enforced* by the feature or *paired with an `ERR` row* describing what happens when it's violated (e.g., `PRE-2.1` "an eligible assignee exists" → `ERR-3` "no eligible assignee → task flagged for manual assignment"). A precondition with neither an enforcement nor an error path is an untested assumption.

Do the same lightweight pass for **Postconditions** — the resulting state each story guarantees (data persisted, event emitted, navigation landed). Keep them distinct from acceptance criteria so you don't restate the same thing twice: an **AC is an externally observable, testable behavior** ("clicking the link activates the account"); a **Postcondition is the resulting system/persisted state** that remains true afterward, some of it not user-visible ("the account row has `verified = true`," "a `welcome_email_sent` event was emitted"). If a tester *observes it happening*, it's an AC; if it's the *state left behind*, it's a Postcondition. Omit Postconditions entirely when the ACs already fully capture the end-state.

---

## Phase 2: Stress-Test the PRD

After drafting the PRD, review it critically:

> "Let me review this PRD critically. What edge cases are missing? Which acceptance criteria are ambiguous?"

Check for:

1. **Story-criteria alignment** — Is every user story covered by at least one acceptance criterion? Is there an acceptance criterion that doesn't map to any story? (Orphaned criteria signal possible scope creep.)
2. **Testability** — Can each acceptance criterion be verified with a specific command, URL visit, or observable output? If not, make it more concrete.
3. **Testable NFRs** — Does each non-functional requirement have a concrete, measurable threshold and a priority tag? Reject vague prose ("fast," "secure") — replace with numbers and conditions.
4. **Verification coverage** — Is every `[MUST]` criterion (story AC, Global AC, NFR, Error State) covered by at least one verification step? List any `[MUST]` with no covering step — those are untested-by-design.
5. **ID integrity** — Does every story (`US-n`) and criterion have a unique ID? Are IDs unchanged from any prior draft of this PRD? (Renumbering breaks downstream references.)
6. **Scope boundaries** — Are the "Out of Scope" items specific enough to reject future feature requests? Would a new team member know where this feature stops?
7. **Edge cases** — What happens with empty inputs, unauthorized users, network failures, or concurrent actions? Is each likely failure captured as an `ERR-n` row with a testable expected behavior?
8. **Verification completeness** — Does the Verification section cover the happy path AND at least one error case?
9. **Open questions** — Are all open questions truly unresolved, or can any be decided now?
10. **Dependencies** — Are all prerequisites listed? Would someone picking this up cold know what needs to exist first?
11. **Instrumentation** — Are success metrics defined with specific events to track? Can you actually measure whether this feature worked?
12. **Migration needs** — If existing behavior changes, is there a migration plan and rollback strategy? Are URL redirects needed?
13. **Data & validation** — If the feature stores or validates data, are the fields, types, required/optional status, and validation rules specified? (Omit only if there's no real data model.)
14. **Definition of Done** — Is the completion gate filled in and consistent with the `[MUST]` criteria and NFR thresholds?
15. **Preconditions present & guarded** — Does each non-trivial story list its entry preconditions (`PRE-n.m`)? Is each one either enforced by the feature or paired with an `ERR` row for its violation? A `PRE` with neither is an untested assumption.
16. **Postconditions established** — Where a story guarantees an end-state (`POST-n.m`), do its acceptance criteria actually establish that state? Are postconditions kept distinct from ACs rather than restating them?
17. **Assumptions are truly assumptions** — Is each `ASM-n` believed-but-unverified? Should any be promoted to a Dependency (you're sure it must be true) or demoted to an Open Question (you're unsure)?
18. **Roles/permissions complete** — If multiple roles exist, is the Roles & Permissions matrix complete and consistent with the story preconditions (authorization) and the permission-denied error states?
19. **Golden example present** — Is there at least one concrete worked example (`EX-n`) that traces to a story/AC? (Omit only if the ACs and data rules leave nothing to a concrete example.)

Iterate with the user until the PRD is solid.

---

## Phase 3: Create GitHub Issue

Once the PRD is finalized, create a GitHub issue to track the feature. A GitHub issue is a to-do item in your project that links back to the PRD so you can track progress, leave comments, and close it when the feature ships.

Write the issue body to a temporary file and create the issue with `--body-file` (the body now contains a multi-line checklist, which inline `--body` mangles):

```bash
gh issue create --title "[Feature] Feature Name" --label "type:feature" --body-file issue-body.md
```

The issue body should include:
- Link to the PRD file
- Summary of the feature
- **A checklist of every `[MUST]` criterion** (story AC, Global AC, NFR, Error State), each with its ID, so build and test progress is trackable as checkboxes that tie back to the PRD. `[SHOULD]`/`[COULD]` criteria stay in the PRD; the issue tracks what's required to ship.
- **If this feature belongs to an epic:** Reference the epic issue (e.g., "Part of #XX") so the feature is linked to the bigger picture

Use this shape for the checklist:

```markdown
## Acceptance Criteria — MUST (build/test tracking)
- [ ] AC-1.1 Verification email is sent within 30 seconds of form submission
- [ ] AC-1.2 Clicking the verification link activates the account and redirects to the dashboard
- [ ] NFR-1 Each request completes in under 500ms at p95 under normal load
- [ ] ERR-1 Invalid email shows an inline error; the form does not submit
```

---

## Phase 4: Handoff to Planning

The PRD defines *what* to build. The next step is planning *how* to build it — Claude will enter **plan mode** to explore the codebase, design the approach, and break the work into implementation tasks before writing any code.

Tell the user:

> "Your PRD and issue are ready. The next step is planning the implementation. Tell Claude:
>
> *'Plan the implementation for specs/[feature-name]-prd.md (tracked in issue #XX)'*
>
> Claude will enter plan mode — it'll explore your codebase, design the approach, and present an implementation plan for your approval before writing any code."

---

## Quick Reference

See [workflow-checklist.md](references/workflow-checklist.md) for a condensed checklist.
