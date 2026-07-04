---
title: Product Requirements Documents
description: What a PRD is, how to write one, and why clear requirements are the most powerful prompt you can give an AI coding agent
date: 2026-02-16
author: James Gray
---A Product Requirements Document (PRD) is the document that aligns a team on **what they're building** before they start building it. It captures the problem, the proposed solution, what success looks like, and what's explicitly out of scope. A good PRD prevents the most expensive kind of waste — building the wrong thing.

## Why PRDs Exist

Without a PRD, teams operate on assumptions. The designer imagines one solution, the engineer builds another, and the stakeholder expected something different. A PRD makes everyone's assumptions explicit and gets alignment before work begins — when changing direction is cheap.

## Anatomy of a PRD

A PRD doesn't need to be long, but it needs to answer a few core questions clearly:

### Problem Statement

What problem are you solving, and for whom? This isn't a feature description — it's a description of the pain. A good problem statement makes the reader feel the frustration.

> **Weak:** "We need a notification system."
>
> **Strong:** "Customers miss time-sensitive updates because they only see them when they happen to open the app. Support tickets about missed updates have increased 40% this quarter."

### Goals and Non-Goals

**Goals** define what success looks like. Be specific enough that you could measure it.

**Non-goals** are just as important — they define what you're explicitly *not* trying to solve. This prevents scope creep and keeps the team focused.

> **Goal:** Customers receive time-sensitive updates within 5 minutes, even when the app is closed.
>
> **Non-goal:** We are not building a general-purpose messaging system. Marketing notifications are out of scope.

### Proposed Solution

Describe the approach at a level that communicates the intent without dictating every implementation detail. Include enough specifics that the team can estimate effort and identify risks.

### Success Metrics

How will you know this worked? Define measurable outcomes before building, not after.

> - Support tickets about missed updates decrease by 50% within 30 days of launch
> - 80% of time-sensitive notifications are opened within 15 minutes

### Open Questions

What don't you know yet? Listing open questions signals intellectual honesty and focuses early conversations on resolving unknowns rather than debating known decisions.

### Preconditions and Assumptions

Every behavior has an entry state — things that must already be true before it applies. A **precondition** is what has to hold for a step to run: the user is signed in, a record already exists, an earlier step finished. An **assumption** is something you're relying on being true but won't build or check yourself, like "the email provider is already set up." Writing these down matters most when an AI agent builds the work — preconditions become the guard checks and permission rules it needs to write, and unstated assumptions are a common source of bugs.

> **Precondition:** The user has a verified account before they can send a notification.
>
> **Assumption:** The existing notification service is already configured to deliver to external addresses.

## Good PRD vs. Bad PRD

| Aspect | Bad PRD | Good PRD |
|--------|---------|----------|
| Problem | "Users want notifications" | "Users miss time-sensitive updates, causing 40% more support tickets" |
| Scope | Lists features without boundaries | States explicit goals AND non-goals |
| Success | "Users should be happier" | "Support tickets decrease 50% within 30 days" |
| Detail level | Either too vague or too detailed | Enough to estimate and identify risks |
| Open questions | None listed (implies false certainty) | Lists 3-5 unresolved questions |

## When You Need a PRD

**Write a PRD when:**

- Multiple people need to understand and agree on what's being built
- The change is large enough that building the wrong thing would be expensive
- Stakeholders need to approve the direction before work starts
- The work will take more than a few days

**Skip the PRD when:**

- The change is small and obvious (fixing a typo, updating a configuration)
- You're the only person affected and can course-correct instantly
- It's a quick experiment you're prepared to throw away

## Specs vs. PRDs

These terms are sometimes used interchangeably, but they serve different purposes:

- **PRD** — Focuses on the **what and why**. Written primarily for alignment across the team. Answers: what problem are we solving, what does success look like, what's in scope?
- **Spec (Technical Specification)** — Focuses on the **how**. Written primarily for engineers. Answers: what's the architecture, what APIs change, what are the data models?

A PRD comes first. Once the team agrees on what to build, engineers may write a spec for how to build it. For smaller projects, a single document can serve both roles.

## The AI Connection

A well-written PRD is the most powerful prompt you can give an AI coding agent.

When you hand an AI agent a clear PRD with a defined problem, specific goals, non-goals, and measurable success criteria, the agent has everything it needs to plan an approach, make implementation decisions, and evaluate its own output. The PRD's structure maps directly to how AI agents work:

- **Problem statement** → The agent understands the purpose behind its task
- **Goals and non-goals** → The agent knows what's in scope and what to avoid
- **Preconditions and assumptions** → The agent knows the entry state to guard for and what it can safely take for granted
- **Success metrics** → The agent can verify whether its solution meets the bar
- **Open questions** → The agent knows where to ask for clarification rather than guessing

The quality gap between "build me a notification system" and a well-structured PRD isn't just about better communication — it's about giving the AI the context it needs to make good decisions independently.

## Related

- [User Stories & Acceptance Criteria](../user-stories/) — breaking PRD requirements into buildable pieces
- [Software Development Lifecycle](../sdlc/) — where PRDs fit in the plan-build-test-ship cycle
- [Roadmaps & Prioritization](../roadmapping/) — deciding which PRDs to write first
- [Context](../../agentic-building-blocks/context/) — how AI tools use documents like PRDs as context
