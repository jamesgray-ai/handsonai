---
name: writing-vision-briefs
description: Use when a user has a fuzzy idea they want to explore before writing a formal PRD. Captures the essence of an idea as a Vision Brief — a structured, business-focused artifact that feeds directly into the feature-prd workflow.
user-invocable: true
---

# Vision Brief Workflow

Guide the user through capturing a fuzzy idea as a structured Vision Brief — a business-focused artifact that clarifies what they want to build and why, before diving into technical specs.

## When to Use This Skill

- User has an early-stage idea that isn't ready for a PRD yet
- User says things like "I have an idea," "I'm thinking about," "what if we," or "I want to explore"
- User needs help articulating what they want to build in plain language
- User wants to validate an idea before committing to a full spec

## Workflow Overview

| Phase | Goal |
|-------|------|
| 1. Discover | Ask questions one at a time to understand the idea |
| 2. Refine | Present the draft Vision Brief, iterate until solid |
| 2.5 Evaluate | Go/no-go decision gate — assess and recommend next action |
| 3. Scope | Assess the size — is this one feature or multiple? Break it down |
| 4. Handoff | Save everything and guide the user to their first feature PRD |

---

## Phase 1: Discover

Ask the user questions **one at a time**. Use multiple-choice options when possible to reduce cognitive load. Wait for each answer before asking the next question.

### Question sequence

**Question 1 — The Problem:**
> "What's the pain point or missed opportunity you're trying to address? In a sentence or two, what frustrates you (or your users) today?"

**Follow-up probe — Quantify the problem:**
> "Can you put rough numbers on it? How often does this happen, how many people are affected, what does it cost in time or money?"

If they can't quantify, that's fine — note it in the brief as a validation signal (e.g., "Impact not yet quantified — consider validating before building"). Don't push hard, but do flag it.

**Question 2 — Who Feels It:**
> "Who specifically experiences this problem? What's their role or situation?"

Offer multiple-choice options based on common user types if the context suggests them. For example:
- (a) End users / customers
- (b) Internal team members
- (c) Administrators / managers
- (d) Someone else — describe them

**Question 3 — Stakeholders & Decision-Makers:**
> "Who else cares about this? Who needs to approve it, who's affected by the change, and who should review the solution before it ships?"

Help the user think broadly:
- Decision maker (who says yes/no to building this?)
- Reviewers (who should weigh in on the approach?)
- Affected parties (who's impacted even if they're not the primary user?)

If the user says "just me," that's a valid answer — note it and move on.

**Question 4 — Current State:**
> "How are you handling this today? Any workarounds, tools, or manual processes — even ugly ones?"

This reveals the severity of the pain (hacking together workarounds = high urgency), what "good enough" looks like (the bar to clear), and implicit requirements (what they like or hate about current approaches).

**Follow-up — Alternatives considered:**
> "Have you looked at existing solutions — tools, services, or approaches that already exist? What's missing from them, or why won't they work?"

If they haven't explored alternatives, note that as a signal. If they have, capture what they tried and why it fell short.

**Question 5 — Strategic Context:**
> "Why is now the right time to solve this? What's changed — or what will happen if you don't act?"

This separates "nice to have" ideas from urgent, high-value ones. If the user says "nothing specific," that's a useful signal too — note it and move on.

**Question 6 — The Vision:**
> "Imagine this problem is solved. What does the ideal outcome look like? Don't describe a solution — describe the result."

**Question 7 — Key Capabilities:**
> "What 3-5 things must the solution be able to do? Write them from the user's perspective — 'I can...' or 'Users can...'"

If the user gives a vague answer, help them break it down:
> "Let me help break that down. It sounds like you need: [a], [b], and [c]. What am I missing?"

**After capabilities are listed, ask the user to prioritize:**
> "If you could only ship ONE of these capabilities, which one? That's your must-have. Which ones could wait for a later version?"

Categorize each capability as **Must have** or **Nice to have** based on their answer.

**Question 8 — Inspiration (optional):**
> "Is there a product, feature, or experience — even in a different domain — that does something close to what you're imagining? This helps me understand the vibe you're going for."
>
> "And on the flip side — is there a product that does this badly? What specifically would you want to avoid?"

If the user says "nothing comes to mind" for either direction, skip those parts in the brief. Don't push — this is a bonus question.

**Question 9 — Success Criteria:**
> "Let's define success in two timeframes:
> - **Early signal** (first 1-2 weeks): What's the first sign this is working?
> - **Real outcome** (1-3 months): What measurable result tells you this was worth building?"

If the user struggles, offer concrete examples:
> "For instance, an early signal might be 'setup completion goes from 60% to 85%' and a real outcome might be 'support tickets drop by half.' What would yours be?"

**Question 10 — Risks & Assumptions:**
> "What's the biggest risk or assumption here? What would need to be true for this to work — and what could derail it?"

If the user says "I'm not sure," help them surface it:
> "Every idea has a hidden bet. Yours might be something like 'users will actually use this if we build it' or 'the data we need already exists.' What's the bet you're making?"

**Question 11 — Dependencies:**
> "What needs to exist before you can build this? Any tools, data, infrastructure, decisions, or other features that must be in place first?"

If the user says "nothing" or "not sure," probe gently:
> "Think about it from two angles: technical prerequisites (data sources, APIs, platforms) and organizational ones (approvals, budget, team availability)."

**Question 12 — Constraints:**
> "What's already in place? Any boundaries I should know about — budget, timeline, existing tools, audience size?"

If the user says "none" or "not sure," that's fine — note it in the brief and move on.

### Tone guidelines

- Use plain language. No technical jargon (no "architecture," "components," "data flow," "API").
- Be encouraging and conversational. This is ideation, not interrogation.
- If the user gives a long, rambling answer, reflect it back concisely: "So the core problem is [X] — does that capture it?"
- If the user is struggling, offer examples to prime their thinking.
- Coach toward specificity. If an answer is vague ("make things better"), gently push: "What does 'better' look like? Can you describe a moment where someone says 'this is working'?"

---

## Phase 2: Refine

After gathering all answers, draft a Vision Brief using the template in [vision-brief-template.md](references/vision-brief-template.md).

**Important:** The template includes inline examples that set the bar for world-class product thinking. Replace each example with the user's actual content — but use the examples as your target for specificity and strategic reasoning. If the user's answers are vague, coach them toward the level of detail shown in the examples during refinement.

Present the draft to the user:

> "Here's your Vision Brief. Read through it and tell me what needs adjusting — I'll refine until it feels right."

Iterate until the user is satisfied. Common refinements:
- Tightening the problem statement
- Adding or removing capabilities
- Clarifying who the users really are
- Sharpening the success criteria
- Surfacing risks the user hadn't considered

### Stakeholder review prompt

Before moving to the next phase, ask:

> "Should anyone else review this brief before we proceed? Sometimes a quick sanity check from a stakeholder or subject-matter expert saves rework later."

If they want a review, pause here and let them share the brief. If not, proceed.

---

## Phase 2.5: Evaluate

Before investing time in scoping and breaking down features, present a quick assessment to help the user decide whether to proceed.

### Present the assessment

> "Before we dive into scoping, let me give you a quick read on this idea:"
>
> | Dimension | Assessment |
> |-----------|------------|
> | **Problem severity** | [Low / Medium / High — based on frequency, people affected, cost] |
> | **Strategic alignment** | [Low / Medium / High — based on urgency, competitive pressure, growth impact] |
> | **Confidence level** | [Low / Medium / High — based on whether the problem is quantified, assumptions are validated, alternatives are explored] |
> | **Rough effort** | [Small / Medium / Large — based on capabilities count, dependencies, constraints] |
>
> **Recommendation:** [One of the three options below]

### Decision gate

Ask the user explicitly:

> "Based on this assessment, I'd recommend: **[recommendation]**. What do you want to do?
>
> 1. **Proceed** — The idea is clear and worth building. Let's scope it out.
> 2. **Validate first** — There are open questions or unvalidated assumptions. Let's identify what to test before committing to build.
> 3. **Park it** — This isn't the right time. I'll save what we have so you can revisit later."

**Guidelines for recommendations:**
- Recommend **Proceed** when problem severity is medium-high, confidence is medium-high, and the idea aligns strategically
- Recommend **Validate first** when confidence is low (unquantified problem, untested assumptions, no alternatives explored) or when the biggest risk hasn't been addressed
- Recommend **Park it** when strategic alignment is low, the problem is mild, or the user themselves seem lukewarm

**If the user chooses "Validate first":**
> "Let's identify the top 1-3 things you'd want to validate. For each one, what's the cheapest way to test it?"

Help them define lightweight validation steps (e.g., "interview 3 users," "run a time study for one week," "prototype just the core interaction"). Add these to the Open Questions section of the brief with a "Validation needed" tag.

**If the user chooses "Park it":**
Save the Vision Brief as-is with `**Status:** Parked` and move to Phase 4 (Handoff) — skip Phase 3 (Scope).

---

## Phase 3: Scope

After the Vision Brief is solid, assess the size of the work. A vision often contains multiple features — building everything at once would be too much. This phase breaks the vision into pieces the user can build one at a time.

### Assess the scope

Review the Vision Brief's **Key Capabilities** section and ask:

> "Let's figure out the scope. Looking at your vision, I see [N] capabilities. Some visions are small enough to build as a single feature. Bigger visions need to be broken into smaller pieces so you can build and ship them one at a time.
>
> Let me break this down for you."

### How to break it down

Use this hierarchy:

| Level | What it means | Example |
|-------|--------------|---------|
| **Vision** | The big-picture outcome you described | "Modernize customer onboarding" |
| **Epic** | A major chunk of work within the vision — too big to build at once, but a clear theme | "Self-service signup flow" or "Admin dashboard" |
| **Feature** | One specific, buildable piece — small enough to plan and implement in a focused sprint | "Email verification step" or "Progress indicator" |

**Rules for good features:**
- Each feature is independently useful — it delivers value on its own, even if other features aren't built yet
- Each feature can be described in one sentence
- Each feature could be built and shipped without waiting for the others
- A feature is NOT a single button or field — it's a complete, working behavior from the user's perspective

### Present the breakdown

Present the breakdown as a simple outline:

> "Here's how I'd break your vision into buildable pieces:
>
> **Epic 1: [Epic Name]**
>
> - Feature 1a: [one-sentence description]
> - Feature 1b: [one-sentence description]
>
> **Epic 2: [Epic Name]**
>
> - Feature 2a: [one-sentence description]
> - Feature 2b: [one-sentence description]
>
> Each feature becomes its own spec that we'll plan and build separately. Does this breakdown feel right? Want to add, combine, or split anything?"

**If the vision is small** (1-3 capabilities that naturally form a single feature):

> "This vision is focused enough to build as a single feature — no need to break it into smaller pieces. Let's move straight to writing the spec."

In this case, there are no epics. Skip the epic issue creation and go directly to Phase 4 handoff with one feature.

### Iterate the breakdown

Work with the user until they're happy with the breakdown. Common adjustments:
- Splitting a feature that's still too big ("That's really two things — X and Y")
- Combining features that don't make sense alone ("These only work together, let's merge them")
- Reordering to identify what to build first
- Moving a feature between epics

### Recommend a starting point

Once the breakdown is approved, present three sequencing strategies and let the user choose:

> "Here are three ways to think about what to build first:
>
> 1. **Riskiest first** — **[Feature X]** tests your biggest assumption: [assumption]. If it doesn't work, you'll know before investing in the rest.
> 2. **Quickest win** — **[Feature Y]** is the simplest to build and proves the approach works. Good for building momentum.
> 3. **Highest value** — **[Feature Z]** delivers the most impact immediately. Best if you're confident in the approach.
>
> Which strategy fits your situation?"

Fill in the specific feature names and reasoning based on the user's capabilities and risks. If the same feature fits multiple strategies, say so.

### Create epic issues

Before creating any issues, present the proposed issues for approval:

> "I'm ready to create these GitHub issues to track your epics:
>
> 1. **[Epic] Epic Name 1** — [one-line summary of what this epic covers]
> 2. **[Epic] Epic Name 2** — [one-line summary of what this epic covers]
>
> Each issue will link to the Vision Brief and list the features as a checklist. Want me to go ahead, or adjust any names first?"

Wait for the user to approve before creating. Then, for each epic:

```bash
gh issue create --title "[Epic] Epic Name" --label "type:epic" --body "..."
```

The epic issue body should include:
- Link to the Vision Brief file
- The full feature breakdown for that epic (as a checklist)
- Note that individual feature issues will reference this epic

---

## Phase 4: Handoff

### Save the Vision Brief

Choose the output location based on what exists in the repo:
1. If a `specs/` directory exists, use `specs/[name]-vision.md`
2. If a `docs/specs/` directory exists, use `docs/specs/[name]-vision.md`
3. If the repo's CLAUDE.md specifies a spec output location, use that (with `-vision` suffix)
4. Otherwise, create `specs/[name]-vision.md`

**Include the feature breakdown in the Vision Brief.** After the Future Considerations section, add:

```markdown
## Feature Breakdown

### Epic 1: [Epic Name] (issue #XX)
- [ ] Feature 1a: [one-sentence description]
- [ ] Feature 1b: [one-sentence description]

### Epic 2: [Epic Name] (issue #XX)
- [ ] Feature 2a: [one-sentence description]
- [ ] Feature 2b: [one-sentence description]

**Recommended starting feature:** [Feature Name] — [reason and sequencing strategy]
```

If the vision is a single feature (no epics), omit this section.

### Guide the user to the next step

**If the vision was broken into features:**

> "Your Vision Brief and feature breakdown are saved at `specs/[name]-vision.md`. I've created epic issues to track the big picture.
>
> The next step is writing a detailed spec for your first feature: **[Feature Name]**. Run:
> ```
> /agentic-coding:writing-feature-prds
> ```
> Then tell Claude: *'Write a PRD for [Feature Name] from the Vision Brief at specs/[name]-vision.md (epic issue #XX)'*
>
> You'll repeat this for each feature in the breakdown — one PRD at a time, one feature at a time."

**If the vision is a single feature:**

> "Your Vision Brief is saved at `specs/[name]-vision.md`. This is focused enough to build as a single feature. Run:
> ```
> /agentic-coding:writing-feature-prds
> ```
> Then tell Claude: *'Use the Vision Brief at specs/[name]-vision.md as the starting point.'*"

---

## Quick Reference

See [vision-brief-template.md](references/vision-brief-template.md) for the template structure.

### How visions become features

```
Vision Brief
  → Evaluate (go/no-go decision gate)
    → Scope assessment
      → Epic(s) — tracked as GitHub issues with type:epic
        → Feature(s) — each one gets its own PRD in Step 1
          → PRD → Plan → Implement → Ship
```

### Vision Brief → PRD mapping

When writing a PRD for a single feature from a Vision Brief, these sections map directly:

| Vision Brief Section | Maps to PRD Input |
|---------------------|-------------------|
| The Problem | Motivation + problem quantification |
| Who Feels It | User type for user stories |
| Stakeholders | PRD stakeholder context + review assignments |
| Current State | Context for problem severity and implicit requirements |
| Alternatives Considered | Approach context — what was ruled out and why |
| Strategic Context | Urgency and prioritization signal |
| The Vision | Summary — scoped to this feature |
| Key Capabilities | User stories and acceptance criteria (scoped to this feature) |
| Inspiration | Reference points for design and UX decisions |
| What Success Looks Like | Success Metrics & Instrumentation |
| Risks & Assumptions | Open questions and validation needs |
| Dependencies | Dependencies & Prerequisites section |
| Constraints & Context | Scope boundaries, non-functional requirements, and design constraints |
| Future Considerations | PRD's Future Considerations section |
