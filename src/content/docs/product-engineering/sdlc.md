---
title: Software Development Lifecycle
description: "How software gets built — the plan-build-test-ship cycle, Agile and Waterfall methodologies, sprints, and key team roles, explained for non-technical readers."
date: 2026-02-16
author: James Gray
---The Software Development Lifecycle (SDLC) is the process a team follows to turn an idea into working software. Every team does it slightly differently, but the core pattern is the same: figure out what to build, build it, make sure it works, ship it, and learn from the results.

## The Core Cycle

Software development follows a repeating loop:

**Plan → Build → Test → Ship → Learn → (repeat)**

- **Plan** — Decide what to build and why. Write requirements, break work into pieces, estimate effort.
- **Build** — Write the code, create the designs, set up the infrastructure.
- **Test** — Verify that what you built works correctly, handles edge cases, and doesn't break existing functionality.
- **Ship** — Release the software to users. This might mean deploying a website, publishing an app update, or handing off a script.
- **Learn** — Observe how users interact with it. Collect feedback. Identify what to improve or build next.

Then the cycle starts again. The difference between methodologies is mostly about how fast this cycle spins and how much you plan upfront.

## Waterfall

Waterfall is the sequential approach: complete each phase fully before moving to the next. Requirements are locked early, and the team works through design, development, testing, and deployment in order.

**When it works well:**

- The requirements are well-understood and unlikely to change (regulatory systems, hardware interfaces, compliance projects)
- The cost of changing direction mid-project is very high
- Multiple teams need to coordinate on a fixed timeline

**The trade-off:** You don't see working software until late in the process. If the requirements were wrong — or the market shifted — you've invested heavily before discovering the problem.

## Agile and Iterative Development

Agile flips the model: instead of planning everything upfront, work in short cycles and ship incrementally. Each cycle produces working software that you can show to stakeholders, test with users, and learn from.

The core idea is simple — **reduce the time between having an idea and getting feedback on it**. If something isn't working, you find out in weeks, not months.

### Sprints

A sprint is a fixed time period (typically one or two weeks) during which the team commits to completing a defined set of work. At the end of the sprint, something shippable exists.

**How a sprint typically works:**

1. **Sprint Planning** — The team reviews the prioritized backlog (the list of everything that could be built) and commits to a set of items they can complete in the sprint.
2. **Daily Standup** — A brief daily check-in (15 minutes or less) where each person shares what they did, what they're doing next, and whether anything is blocking them.
3. **Work** — The team builds, tests, and completes the committed items.
4. **Sprint Review** — The team demonstrates what they built to stakeholders and collects feedback.
5. **Retrospective** — The team reflects on how the sprint went and identifies one or two improvements for next time.

### The Backlog

The backlog is the prioritized list of everything the team could build. Items at the top are the most important and best-defined. Items lower down may be rough ideas. The product manager owns the backlog and continuously refines it based on stakeholder input, user feedback, and business priorities.

## Key Roles

| Role | What They Do | When They're Most Active |
|------|-------------|------------------------|
| **Product Manager** | Decides what to build and why. Owns the requirements and priorities. Represents the customer's needs. | Planning, throughout the cycle |
| **Designer** | Creates the user experience — how the product looks, feels, and flows. | Planning and early build |
| **Engineer** | Writes the code. Implements the designs and requirements. Makes technical decisions about how to build it. | Build and test |
| **QA / Tester** | Verifies that what was built meets the requirements and doesn't break anything. | Test (and increasingly throughout) |

In smaller teams, one person may wear multiple hats. In AI-driven development, a single person often fills the PM and QA roles while an AI agent handles engineering.

## Estimation

Teams estimate work to plan sprints and set expectations. Two common approaches:

**Story Points** — Relative sizing. A task rated "3 points" is about three times the effort of a "1 point" task. Points measure complexity, not hours. Teams calibrate over time — they learn that their team completes about 20 points per sprint, which helps predict capacity.

**T-Shirt Sizing** — Even simpler. Label tasks as S, M, L, or XL. Useful for rough roadmap planning when precision isn't needed. Small = a day or less. Medium = a few days. Large = a week or more. XL = needs to be broken into smaller pieces.

**Why estimation is hard:** Humans consistently underestimate effort for creative and technical work. Unknown unknowns — things you discover only while doing the work — are the biggest source of surprises. Good teams account for this by building in buffer and tracking their historical accuracy.

## AI Changes the Cycle

AI compresses the build-test phase dramatically. Tasks that took a sprint can happen in hours when an AI coding agent handles the implementation. This changes team dynamics in practical ways:

- **Planning matters more.** When building is fast, the bottleneck shifts to knowing what to build. Clear requirements and well-defined acceptance criteria become the constraint — not engineering time.
- **Iteration gets cheaper.** If building the wrong thing costs a sprint, teams are cautious. If building the wrong thing costs an hour, teams can experiment more freely.
- **Roles shift.** The person directing the AI agent acts as both product manager and engineering lead. They need to define what to build (PM skill) and evaluate whether the output is correct (engineering judgment).
- **Testing becomes critical.** AI can produce working code quickly, but "works" and "works correctly for all cases" are different things. The verify step becomes the quality gate.

## Related

- [Product Requirements](../requirements/) — the document that kicks off the Plan phase
- [User Stories & Acceptance Criteria](../user-stories/) — how work gets broken into buildable pieces
- [Project Tracking with GitHub](../tracking/) — the tools teams use to manage the Build phase
- [Agents](../../agentic-building-blocks/agents/) — AI agents that handle the Build and Test phases autonomously
