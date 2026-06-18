# Feature PRD Workflow Checklist

Quick reference for the feature PRD workflow.

## Phase 1: Define

- [ ] Ask: What feature? What problem? Who are users? What should happen? What's NOT in scope?
- [ ] Ask: NFRs? Error states? Migration needs? Dependencies? Success metrics?
- [ ] Create PRD at `specs/[feature-name]-prd.md` (or repo-conventional location)
- [ ] Write user stories (`US-n`) with acceptance criteria paired directly beneath each story
- [ ] Assign stable IDs: `US-n`, `AC-n.m`, `AC-G.n`, `NFR-n`, `ERR-n` (append, never renumber)
- [ ] Tag each criterion as `[MUST]` / `[SHOULD]` / `[COULD]`
- [ ] Add Scope section (In Scope / Out of Scope)
- [ ] Add Approach (high-level technical strategy)
- [ ] Add Data & Validation (fields, types, required, rules) if the feature stores/validates data
- [ ] Add Non-Functional Requirements as testable statements with concrete thresholds (if applicable)
- [ ] Add Error States table with ID + Priority columns (if applicable)
- [ ] Add Success Metrics & Instrumentation
- [ ] Add Dependencies & Prerequisites (if applicable)
- [ ] Add Migration & Rollback (if changing existing behavior)
- [ ] Add UI/UX Requirements (if user-facing)
- [ ] Add Design Constraints
- [ ] Add Verification section, annotating each step with the criteria IDs it covers (happy path + at least one error case)
- [ ] Add Definition of Done (completion gate covering MUST criteria, build, NFR thresholds, instrumentation)
- [ ] Add Future Considerations (if ideas surfaced during discovery)

## Phase 2: Stress-Test

- [ ] Story-criteria alignment: every story has AC, no orphaned criteria
- [ ] Testability: each criterion maps to a specific command, URL, or output
- [ ] Testable NFRs: each NFR has a concrete threshold + priority (no vague prose)
- [ ] Verification coverage: every `[MUST]` (AC, Global, NFR, Error) covered by ≥1 verification step
- [ ] ID integrity: every `US-n`/criterion ID is unique and unchanged from prior drafts
- [ ] Scope boundaries: "Out of Scope" items are specific enough to reject requests
- [ ] Edge cases: empty inputs, unauthorized users, failures — each captured as a testable `ERR-n`
- [ ] Verification completeness: happy path + error case covered
- [ ] Data & validation: fields, types, required status, and rules specified (if data-bearing)
- [ ] Definition of Done: gate filled in and consistent with MUST criteria + NFR thresholds
- [ ] Open questions: resolve any that can be decided now
- [ ] Dependencies: all prerequisites listed
- [ ] Instrumentation: success metrics defined with events to track
- [ ] Migration: rollback plan exists if changing existing behavior

## Phase 3: Create Issue

- [ ] Run: `gh issue create --title "[Feature] Name" --label "type:feature" --body-file issue-body.md`
- [ ] Link to PRD file in issue body
- [ ] Include a checklist of every `[MUST]` criterion (with IDs) for build/test tracking
- [ ] Note the issue number

## Phase 4: Handoff

- [ ] Tell user to enter plan mode
- [ ] Reference: `Plan the implementation for specs/[feature-name]-prd.md (issue #XX)`

---

## Acceptance Criteria Rules

- Numbered list (not checkboxes)
- Lead with a stable ID (`AC-n.m`), then the priority tag
- Yes/no verifiable statements
- Tagged with `[MUST]` / `[SHOULD]` / `[COULD]` priority
- Focus on *what*, not *how*
- Active voice
- Concrete expected values
- Each criterion testable by a specific command, URL, or observable output
