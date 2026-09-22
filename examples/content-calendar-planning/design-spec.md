---
workflow: content-calendar-planning
requirements_file: outputs/content-calendar-planning/requirements.md
spec_version: 3.0
approved: true
definition_type: Step-Driven
mechanism: Skill
involvement: Augmented
platform: Claude Code
platform_mode: code
packaging: Standalone Skill
counts:
  steps: 10
  skills: 5
  agents: 0
  integrations: 1
---

> `approved: true` because this is a finished, approved example — a spec Design has just written carries `approved: false` until the user approves it in the session.

# Content Calendar Planning — Design Spec

## Source

**Workflow Requirements:** `outputs/content-calendar-planning/requirements.md` (published in this example folder as `workflow-requirements.md`)

This Design Spec consumes the Workflow Requirements as canonical input. Goal, Value & Measurement, Metadata, Context Inventory, Security, Privacy & Safety, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview, and per-step requirements are defined there — not restated here. Read the Workflow Requirements alongside this spec when building. Context IDs used below (C1–C9) are the numbered items in that file's Context Shopping List.

## Value & Measurement

Restated from the Workflow Requirements so this document says what the workflow is *for*. A reviewer should not have to open a second file to learn why it exists. Design does not re-derive these.

| Field | Value |
|---|---|
| Business Objective | Maintain a consistent, balanced content presence across LinkedIn, Substack Newsletter, X, and YouTube that builds audience trust, reinforces the Graymatter brand, and supports upcoming course launches. |
| Desired Outcome | James Gray — the single owner of the content operation — ends each Sunday session with an approved 2-week content plan already committed to Notion, instead of deciding what to publish day by day. |
| Measure | Minutes spent in the Sunday planning session, and the number of weeks in which every channel hits its cadence target. |
| Baseline | Not recorded · Unknown |
| Target | One session of about 30 minutes producing a plan that meets cadence targets on all four channels, with no mid-week re-planning. |

A `Baseline` of `Unknown` carries through as a visible flag, not a blank: it tells Build and Run that instrumentation is part of the job. This example's Workflow Requirements predates the `Value & Measurement` format — the objective above is sourced from its Scenario Metadata, and the measure, baseline, and target were captured at Design rather than stated by the business.

---

The spec is organized into three layers that build on each other:

1. **Architecture (L1)** — strategic decisions: platform, mechanism, autonomy, packaging
2. **Decomposition (L2)** — for each step, what AI building block delivers it
3. **Component Blueprints (L3)** — field-level specs for each new skill and agent

---

## Layer 1 — Architecture

*Strategic decisions that shape everything downstream.*

## Execution Pattern

**Skill** — One skill the user invokes by name ("plan my content") that drives the whole collaborative planning session: it carries Steps 5–9 as its own instruction blocks and calls component skills for the repeatable Notion operations at the bookends (Steps 1–4 and 10). Not an Agent, because the decisions that matter here — which themes to run, which ideas make the cut, how heavy the week can be — are creative judgments that benefit from James sitting at the decision points rather than an executor choosing its own path.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lens | Individual | Single-person content operation — one owner, one calendar, no approval chain beyond James. |
| Platform | Claude Code | James's primary AI development environment, and where the Notion MCP server already runs. |
| Platform Mode | code | Claude Code is a code-mode platform — skills are files on disk and artifacts are markdown. |
| Orchestration | Skill | James starts the session on Sunday and it follows the mapped ten steps, pausing where he said a person should look. Nothing branches on the AI's own findings, so nothing needs an agent's runtime path-finding. |
| Involvement | Augmented | Weekly collaborative session — James reviews and approves at the decision points, and no writes happen without him. |
| Packaging | Standalone Skill | A single workflow's skills, installed into James's own `.claude/skills/` directory and invoked by name. There is no second consumer, so there is nothing to distribute through a plugin or marketplace. |
| Trigger | Weekly (Sunday), manual | Manual trigger means no scheduling infrastructure and no unattended-run risk — the involvement mode stays Augmented. |

**Packaging values:**
- **Plugin** — Multiple related artifacts shipped together (e.g., handsonai-plugins marketplace plugin, set of `.claude/` files distributed via marketplace).
- **Standalone Skill** — A single skill, uploaded directly (e.g., zip uploaded to Claude.ai, single SKILL.md in `.claude/skills/`, Codex skill in `.agents/skills/`, ChatGPT skill).
- **Workspace Agent** — A ChatGPT Workspace Agent that bundles orchestration + skills + tools as a unit.
- **Loose Files** — Individual files in a project directory, no distribution layer.

## Autonomy Spectrum Summary

**Workflow-level autonomy: Guided.** James starts the session and steers it at checkpoints; the sequence of the ten steps is fixed, but four of them involve bounded creative judgment by the AI that a human reacts to. Nothing backtracks or re-plans its own route, which is what would push this to Autonomous.

Per-step classifications (from the Decomposition table below):

- **Deterministic** (Steps 1, 2, 4, 10): Mechanical data operations — query or write Notion databases, no judgment needed. Fully automated via component skills.
- **Guided** (Steps 5, 6, 7, 8): AI proposes, human reacts and approves. Driven by the orchestrator's inline instruction blocks, with bounded creative judgment inside rules the Workflow Requirements sets (pillar balance, cadence targets, channel-format fit).
- **Human** (Steps 3, 9): Human drives, AI supports. Step 3 is James's own recall of the week, captured through an existing skill. Step 9 is the approval gate the whole workflow turns on.

## Safety & Permissions

| Question | Finding | Mitigation |
|---|---|---|
| **Write access** — which integrations can this workflow create, modify, or send through? | Notion (update Content Calendar entries: Status, Content Pillar, Effort, Priority, Planned Date; create Post entries in the Posts database). No other write surface — nothing is published, emailed, or sent. | Least privilege: share only the Content Calendar, Posts, and Cohorts databases with the Notion integration. All writes are confined to Step 10, which runs only after the Step 9 approval gate. |
| **Untrusted input** — does any step consume content the user didn't author? | None. Every input is James's own Notion workspace, his own engagement metrics, and his own recall of the week. | No mitigation needed today. If the future Content Performance Collection workflow ever imports third-party comment text into the Posts database, that text must be treated as data, never as instructions, and suspicious embedded directives flagged to James. |
| **Unattended runs** — does this run on a schedule or without a human watching? | No. Manual weekly trigger, James present throughout. | Keep it that way: the Step 9 gate is what makes the trigger safe to leave manual. |
| **Blast radius** — worst realistic outcome if a run goes wrong? | A batch of draft Post entries lands with wrong dates, or a Post row is created without its Source Content relation. Nothing is published to any channel; every entry is `Draft` or `Planned`. | Human gate at Step 9 before any write. `committing-content-plan` validates the Source Content relation before creating a Post and refuses rather than writing an orphan, checks for an existing Draft with the same title and channel, and reports which entries failed on partial failure. |

Build enforces these mitigations during connector setup (write-scope pre-flight, least-privilege authorization). Run re-verifies the unattended-run items in its fresh/scheduled-session section.

### Constraint Conformance

This example's Workflow Requirements predates the `Security, Privacy & Safety` section. That is not the same as "no constraints" — the constraints below were captured at Design from the rules and failure modes the business already stated in the step details, and are sourced as such.

| Constraint | From | Met by | State |
|---|---|---|---|
| Promotional content stays at no more than 30–40% of the calendar unless a launch is imminent | Editorial · Workflow Requirements Step 4 (Decision Points) | Step 4 surfaces promotional obligations as explicit constraints on Step 5; the ratio is one of the things James checks at the Step 9 gate | Satisfied |
| Nothing is written to Notion until James approves the plan | Operational · Workflow Requirements Steps 9–10 | Human gate at Step 9; S5 runs only after approval, and the orchestrator holds the plan in the session until then | Satisfied |
| A Post entry must never exist without a Source Content relation to a Content Calendar entry | Data integrity · Workflow Requirements Step 10 (Failure Modes) | S5 validates the relation before every create and errors rather than writing an orphan | Satisfied |
| Refinement at Step 9 is capped at three rounds, then commit what is agreed and flag the rest | Operational · Workflow Requirements Step 9 (Failure Modes) | The orchestrator's Step 9 block carries the three-round cap and the fallback | Satisfied |
| Notion credentials and content stay on James's machine | Privacy · Captured at Design | The Notion MCP server runs locally under Claude Code against James's own integration token; no third-party service sits in the path | Satisfied |

- **Satisfied** — the design decision that meets it is named.
- **Accepted** — not met, deliberately. Record a named owner and the reason.
- **Open** — surfaced, not yet decided.

**Nothing here blocks the spec.** What is enforced is that no constraint stays silent — completeness of *decision*, not of satisfaction.

## Integration Options

### Notion (Steps 1, 2, 3, 4, 10)

Claude Code has no platform-native Notion connector, so Notion reaches the workflow through an integration you add. Options, closest-to-native first:

| Block | Option | Source URL | Trade-off |
|-------|--------|-----------|-----------|
| MCP | Notion MCP server | https://github.com/makenotion/notion-mcp-server | Closest thing to a native connector here — plug-and-play, full database CRUD, no code to maintain |
| API | Notion REST API | https://developers.notion.com | Most flexible, more code required |
| SDK | `@notionhq/client` | https://github.com/makenotion/notion-sdk-js | Best developer experience for code-heavy builds |

*Recommendation: MCP for this workflow — all five steps are standard database CRUD, and MCP is the least-code path on Claude Code. Share only the Content Calendar, Posts, and Cohorts databases with the integration, per the Safety & Permissions write-access finding.*

## Model Recommendation

**Default capability:** fast — Six of the ten steps are database queries and writes that need no deep reasoning.

*(Plain-language gloss for non-technical users: **reasoning-heavy** = slower but handles complex judgment/nuance; **fast** = quicker, best for simple/high-volume steps; **vision** = can read images/screenshots.)*

**Per-step overrides:**
- Steps 5–9: reasoning-heavy — theme selection, channel mapping, titling, sequencing, and the refinement dialogue all involve bounded creative judgment about content strategy and audience fit. Steps 5 and 6 lean on it hardest.

**Per-platform mapping:** resolved by Build at generation time — Build verifies the current model names for the chosen platform via web search. Only capability tiers are recorded here; specific model IDs go stale.

---

## Layer 2 — Decomposition

*For each step, what AI building block delivers it.*

## Step-by-Step Decomposition

Steps are defined in the Workflow Requirements. This table adds the building-block classification and the concrete Build output for each:

| Step | Name (from Requirements) | Autonomy | Orchestration | Integration (use/build) | Intelligence | Build Output | Human Gate? |
|------|------|----------|---------------|------------------------|--------------|--------------|-------------|
| Step 1 | Review Recent Content Performance | Deterministic | Skill | MCP: Notion (use) | Model: fast; Context: C2, C9 | New skill: S2 | No |
| Step 2 | Review Content Idea Backlog | Deterministic | Skill | MCP: Notion (use) | Model: fast; Context: C1 | New skill: S3 | No |
| Step 3 | Capture Fresh Ideas | Human | Skill | MCP: Notion (use) | Model: fast; Context: C4 | Use existing: registering-content-ideas | Yes |
| Step 4 | Check Upcoming Business Priorities | Deterministic | Skill | MCP: Notion (use) | Model: fast; Context: C3, C8 | New skill: S4 | No |
| Step 5 | Select Ideas and Set Weekly Themes | Guided | Prompt | — | Model: reasoning-heavy; Context: C4, C7 | Inline prompt → Workflow Requirements Step 5 | Yes |
| Step 6 | Map Ideas to Channels | Guided | Prompt | — | Model: reasoning-heavy; Context: C5, C6 | Inline prompt → Workflow Requirements Step 6 | Yes |
| Step 7 | Create Post Plan | Guided | Prompt | — | Model: reasoning-heavy; Context: C5, C7 | Inline prompt → Workflow Requirements Step 7 | No |
| Step 8 | Sequence and Balance | Guided | Prompt | — | Model: reasoning-heavy; Context: C5 | Inline prompt → Workflow Requirements Step 8 | No |
| Step 9 | Refine and Approve the Plan | Human | Prompt | — | Model: reasoning-heavy | Inline prompt → Workflow Requirements Step 9 | Yes |
| Step 10 | Commit Content Plan | Deterministic | Skill | MCP: Notion (use) | Model: fast; Context: C1, C2 | New skill: S5 | No |

Column definitions:
- **Step**: Step ID from Workflow Requirements
- **Autonomy**: Human / Deterministic / Guided / Autonomous
- **Orchestration**: Prompt / Skill / Agent
- **Integration**: Block + tool + action tag, or "—" if none
- **Intelligence**: Model class + context sources (C-IDs from the Workflow Requirements' Context Shopping List)
- **Build Output**: the concrete artifact Build produces for the step
- **Human Gate?**: Yes / No (sourced from the Workflow Requirements)

## Orchestrator Prompt Outline

The high-level shape of the orchestrator James runs to execute the workflow. This is not the full text — it's the structural skeleton Build expands. Build derives full step content from the Workflow Requirements' step details. **The orchestrator ships as a skill** — James runs the whole sequence by name — and is blueprinted as `S1` below so the spec's inventory matches what Build produces.

```
[Intro: this skill runs the weekly content calendar planning session. Run it on Sunday.
 It reviews what shipped, what's in the backlog, and what's coming up, then plans and
 commits the next two weeks across LinkedIn, Substack Newsletter, X, and YouTube.]

[Steps 1, 2, 4 — run in parallel, independent data pulls]
  - Source: Workflow Requirements Steps 1, 2, 4
  - Build Output: New skill: S2 / New skill: S3 / New skill: S4
  - User provides: lookback window (default 14 days), lookahead window (default 6 weeks)
  - Produces: performance signals, prioritized backlog with pillar balance, promotional obligations

[Step 3 invocation]
  - Source: Workflow Requirements Step 3
  - Build Output: Use existing: registering-content-ideas
  - User provides: ideas from the past week that were never captured
  - Produces: new Content Calendar entries with Status = "Idea"

[PAUSE for user review — Human Gate, Workflow Requirements Step 3]
  - What user is reviewing: whether the backlog is now complete enough to plan from
  - User decides: proceed, or add more ideas first

[Step 5 invocation]
  - Source: Workflow Requirements Step 5
  - Build Output: Inline prompt → Workflow Requirements Step 5
  - User provides: theme selection from the 2-3 options proposed per week
  - Produces: selected ideas with pillar, effort, priority, target date (not yet written)

[PAUSE for user review — Human Gate, Workflow Requirements Step 5]
  - What user is reviewing: weekly themes and the pillar balance across the 2-week window
  - User decides: which themes run, which ideas make the cut

[Step 6 invocation]
  - Source: Workflow Requirements Step 6
  - Build Output: Inline prompt → Workflow Requirements Step 6
  - User provides: corrections to the channel mapping
  - Produces: idea-to-channel mapping, capped at 2-3 channels per idea

[PAUSE for user review — Human Gate, Workflow Requirements Step 6]
  - What user is reviewing: anchor channel and derivatives per idea, against cadence targets
  - User decides: accept the mapping or redirect it

[Steps 7 and 8 invocation — run without pausing]
  - Source: Workflow Requirements Steps 7, 8
  - Build Output: Inline prompt → Workflow Requirements Step 7 / Step 8
  - Produces: post plan with titles, angles, Source Content links, and balanced planned dates

[Step 9 invocation]
  - Source: Workflow Requirements Step 9
  - Build Output: Inline prompt → Workflow Requirements Step 9
  - User provides: reactions — swap, move, scale back, add
  - Cap: three rounds of refinement, then commit what is agreed and flag the rest

[PAUSE for approval — Human Gate, Workflow Requirements Step 9]
  - What user is reviewing: the complete 2-week plan, cadence counts, pillar balance
  - User decides: approve. Nothing is written to Notion before this point.

[Step 10 invocation — only after approval]
  - Source: Workflow Requirements Step 10
  - Build Output: New skill: S5
  - Produces: Content Calendar entries set to "Planned", Post entries created as "Draft"
    with Source Content relations set

[Final output: an approved 2-week content plan committed to Notion, plus a confirmation
 listing the entries updated and created with links. One row appended to
 outputs/content-calendar-planning/runs.md.]
```

## Data Readiness Summary

Items in the Workflow Requirements' Context Shopping List that are not yet AI-accessible.

| Context ID | Current State | Required Action | Affects Steps |
|---|---|---|---|
| C5 — Channel cadence targets | No | Write the targets into the orchestrator skill as an inline reference table (LinkedIn 3/wk, Substack Newsletter 3-5/wk, X long-form 1/wk, YouTube 1/wk) | 6, 8, 9 |
| C6 — Channel-format fit rules | No | Write the fit rules into the orchestrator skill as an inline reference table (Substack 800-2000 words, LinkedIn 200-500, X 500-1500, YouTube 5-15 min) | 6 |
| C8 — Business calendar | Partial | Google Calendar is not connected to Claude Code in this setup; James checks it manually during Step 4 and relays the priorities | 4 |
| C9 — Performance benchmarks per channel | No | Built over time by the separate Content Performance Collection workflow (Backlog). Until then, S2 uses its "no metrics available" fallback path | 1 |

C1–C4 and C7 are accessible: the three Notion databases through the MCP server, and the pillar definitions and brand voice as inline context in the orchestrator skill.

## Recommended Implementation Order

Build artifacts in this order. Dependencies within each tier follow the `Depends On` field of each skill.

### Quick Wins (implement first)
1. **S1 — `content-calendar-planning`** — Get the conversational flow working end-to-end first. Steps 5–9 are inline prompt logic and need no infrastructure, so the workflow delivers value before a single component skill exists.
2. **S3 — `reviewing-content-backlog`** — Simple query, high value. This is the most-used input step and the critical path starts here.
3. **S4 — `checking-business-priorities`** — Simple query, prevents missed promotional opportunities.

### Core (implement second)
1. **S2 — `reviewing-content-performance`** — Depends on the Posts database carrying metrics. Start with the "no metrics" fallback path and enhance it when the Content Performance Collection workflow exists.
2. **S5 — `committing-content-plan`** — The execution step, and the only one that writes. More complex (two databases and a relation), so build it after the planning flow is validated.

### Future Enhancement (optional)
1. **`registering-content-ideas`** — Already exists and is deployed. No work needed.
2. **Content Performance Collection workflow** — A separate workflow (Backlog). Unlocks the full value of Step 1 by populating C9.

---

## Layer 3 — Component Blueprints

*Field-level specs for each new skill. Build uses these to generate artifacts.*

## Skill Candidates

S1 is the orchestrator skill — it takes the workflow name and covers all ten steps. S2–S5 are the capability-named component skills it calls.

### S1 — content-calendar-planning

| Field | Detail |
|---|---|
| **ID** | S1 |
| **Name** | content-calendar-planning |
| **Description** | This skill should be used when the user wants to plan or refresh their content calendar for the next two weeks — typically the weekly Sunday planning session — or says "plan my content", "run content calendar planning", or "what am I posting over the next two weeks". It runs the full ten-step session: reviews recent post performance and the idea backlog in Notion, captures stragglers, checks upcoming cohort launches, proposes weekly themes balanced across the three content pillars, maps ideas to LinkedIn, Substack Newsletter, X, and YouTube, sequences the plan, and — only after the user approves it — commits Content Calendar and Posts entries to Notion. |
| **Purpose** | The orchestrator: runs the collaborative planning session, carries Steps 5–9 as inline instruction blocks, and calls the component skills at the bookends. Workflow-specific by design — not reusable beyond this workflow. |
| **Covers Steps / Domains** | Steps 1–10 (all) |
| **Inputs** | Lookback window — how far back to review performance (default: 14 days)<br>Lookahead window — how far ahead to check cohorts (default: 6 weeks)<br>Planning window — how many weeks to plan (default: 2)<br>Fresh ideas — James's recall of the week, provided at Step 3<br>Availability — how heavy the coming weeks are, provided at Step 9 |
| **Outputs** | An approved 2-week content plan, committed to Notion as "Planned" Content Calendar entries and "Draft" Post entries with Source Content relations set; a confirmation listing what was updated and created; one row appended to `outputs/content-calendar-planning/runs.md`. |
| **Decision Logic** | Follows the Orchestrator Prompt Outline above. Steps 1, 2, and 4 run in parallel. Nothing is written to Notion before the Step 9 approval. Refinement at Step 9 is capped at three rounds, then commit what is agreed and flag the rest for mid-week adjustment. Cadence targets (C5) and channel-format fit rules (C6) are carried inline and are the guardrail for Steps 6 and 8. |
| **Failure Modes** | Backlog empty after Step 2 → tell the user Step 3 is critical this week and spend the time there.<br>User does not approve at Step 9 → stop before Step 10, save the draft plan in the session, write nothing.<br>Notion unreachable → stop and report which step failed; never partially commit.<br>Refinement passes three rounds → commit what is agreed, list the unresolved items. |
| **Required Tools** | MCP: Notion (use) |
| **Depends On** | S2, S3, S4, S5, and the installed `registering-content-ideas` skill |
| **Stateful?** | No — each Sunday session is self-contained. The state that matters lives in Notion; `runs.md` is a log, not state the skill reads back. |

### S2 — reviewing-content-performance

| Field | Detail |
|---|---|
| **ID** | S2 |
| **Name** | reviewing-content-performance |
| **Description** | This skill should be used when the user wants to know how recently published content performed — for example "how did last week's posts do", "review my content performance", or as the opening step of a content planning session. It queries the Notion Posts database for posts published in a lookback window, ranks them by impressions and engagement rate, and returns top performers, underperformers, and "do more of / stop doing" signals. When no metrics are populated it says so rather than guessing. |
| **Purpose** | Turn the Posts database into the performance signals that inform idea selection. Reusable by any workflow that needs a read on recent content performance. |
| **Covers Steps / Domains** | Step 1 |
| **Inputs** | Lookback window — how many days back to review (default: 14) |
| **Outputs** | Performance summary: top 3 performers (topic, channel, metrics), underperformers, "do more of / stop doing" signals. If no metrics data, returns qualitative guidance. |
| **Decision Logic** | Sort by Impressions descending, then Engagement Rate. Flag any post with 2x average impressions as a top performer. Flag any with less than 50% of average as an underperformer. If no metrics data, return "No metrics available — qualitative review needed." |
| **Failure Modes** | No published posts in the window → return an empty summary with a note.<br>No metrics populated → flag the dependency on the Content Performance Collection workflow (C9) and return the qualitative path. |
| **Required Tools** | MCP: Notion (use) |
| **Depends On** | None |
| **Stateful?** | No — each call is a fresh query over the window it is given. |

### S3 — reviewing-content-backlog

| Field | Detail |
|---|---|
| **ID** | S3 |
| **Name** | reviewing-content-backlog |
| **Description** | This skill should be used when the user wants to see what content ideas are waiting to be planned — for example "what's in my content backlog", "review my idea pipeline", or as an input step in a content planning session. It queries the Notion Content Calendar for entries with Status = "Idea" and returns a prioritized summary with a breakdown across the three content pillars, staleness flags, and warnings when one pillar is under-represented. |
| **Purpose** | Turn the idea backlog into a prioritized, pillar-aware shortlist to plan from. Reusable by any workflow that needs the current state of the idea pipeline. |
| **Covers Steps / Domains** | Step 2 |
| **Inputs** | None — always queries Status = "Idea" |
| **Outputs** | Backlog summary: total count, breakdown by Content Pillar (Master AI / Master Yourself / Build What Matters), list sorted by Priority then Date Added, timeliness flags, pillar imbalance warnings. |
| **Decision Logic** | Count ideas per pillar to surface imbalances. Flag any idea older than 30 days as potentially stale. Flag any with Priority = "Critical" or "High" as must-consider. Identify the pillar with the fewest ideas. |
| **Failure Modes** | Empty backlog → return "Backlog empty — Step 3 (Capture Fresh Ideas) is critical this week." |
| **Required Tools** | MCP: Notion (use) |
| **Depends On** | None |
| **Stateful?** | No — reads the current state of the database each time. |

### S4 — checking-business-priorities

| Field | Detail |
|---|---|
| **ID** | S4 |
| **Name** | checking-business-priorities |
| **Description** | This skill should be used when the user needs to know which business commitments upcoming content has to support — for example "what launches are coming up", "what do I need to promote", or as an input step in a content planning session. It queries the Notion Cohorts database for cohorts with Status = "Upcoming" inside a lookahead window and returns each one with weeks-until-start and a recommended promotional intensity. |
| **Purpose** | Convert upcoming launches into concrete promotional obligations that constrain the plan. Reusable by any workflow that needs the launch calendar. |
| **Covers Steps / Domains** | Step 4 |
| **Inputs** | Lookahead window — how many weeks ahead to check (default: 6) |
| **Outputs** | List of upcoming cohorts with Name, Course, Start Date, weeks until start, and recommended promotional intensity (light / medium / heavy). Summary of promotional content needs. |
| **Decision Logic** | 6+ weeks out = light (awareness content, 1 post/week). 3-5 weeks = medium (value-driven content, 2 posts/week). 1-2 weeks = heavy (urgency and enrollment-focused, 3+ posts/week). Active cohort = no promo needed. No upcoming cohorts = plan 100% organic. |
| **Failure Modes** | No upcoming cohorts → return "No upcoming launches — plan 100% organic content."<br>Business calendar items (C8) are not AI-accessible → prompt James to relay anything the Cohorts database does not cover. |
| **Required Tools** | MCP: Notion (use) |
| **Depends On** | None |
| **Stateful?** | No. |

### S5 — committing-content-plan

| Field | Detail |
|---|---|
| **ID** | S5 |
| **Name** | committing-content-plan |
| **Description** | This skill should be used when an approved content plan needs to be written to Notion — for example "commit the plan", "save this to Notion", or as the final step of a content planning session. It updates Content Calendar entries to Status = "Planned" with pillar, effort, priority, and planned date, and creates Post entries in the Posts database with title, channel, planned date, angle notes, and a Source Content relation back to the originating idea. It refuses to create a Post without that relation. |
| **Purpose** | The one write step: commit an approved plan to both Notion databases without creating orphans or duplicates. Reusable by any workflow that commits a content plan. |
| **Covers Steps / Domains** | Step 10 |
| **Inputs** | Approved plan containing: (1) content ideas with pillar, effort, priority, planned date, and Content Calendar entry URL; (2) posts with title, channel, source content link, planned date, and angle/hook notes |
| **Outputs** | Confirmation with the count of Content Calendar entries updated, the count of Post entries created, and links to the entries. |
| **Decision Logic** | For each content idea: update Status to "Planned", set Content Pillar, Effort, Priority, Planned Date. For each post: create an entry in the Posts database with Post Title, Channel, Source Content relation (linked to the Content Calendar entry), Planned Date, Status = "Draft", and the angle/hook in Notes. Always validate the Source Content relation before creating a Post entry. |
| **Failure Modes** | API failure → retry once, then report which entries failed; never leave a half-written plan unreported.<br>Missing Source Content link → error, do not create an orphan post.<br>Duplicate detection → check for an existing Draft post with the same title and channel before creating. |
| **Required Tools** | MCP: Notion (use) |
| **Depends On** | S3 — `reviewing-content-backlog` (Content Calendar entries must exist for Posts to link to) |
| **Stateful?** | No — idempotent per run, with duplicate detection standing in for memory. |

## Prerequisites

1. Claude Code installed, with the Notion MCP server configured and the Content Calendar, Posts, and Cohorts databases shared with the integration.
2. Content Calendar database exists with Status options: Idea, Planned, In Progress, In Review, Published.
3. Posts database exists with Channel options and a Source Content relation to Content Calendar.
4. Cohorts database exists with Status options: Upcoming, Active, Completed.
5. Content Pillar options set to: Master AI, Master Yourself, Build What Matters.
6. The `registering-content-ideas` skill is installed and working.

## Deployment Plan

| Artifact | Target Location | Deployment Steps |
|---|---|---|
| S1 — `content-calendar-planning` | `.claude/skills/content-calendar-planning/SKILL.md` | Generate the orchestrator with Steps 5–9 as inline instruction blocks, cadence targets and fit rules as inline reference tables, and calls out to S2–S5. Set `disable-model-invocation: true` so it is only ever started by name. |
| S2 — `reviewing-content-performance` | `.claude/skills/reviewing-content-performance/SKILL.md` | Generate from the blueprint; verify against the Posts database, including the no-metrics path. |
| S3 — `reviewing-content-backlog` | `.claude/skills/reviewing-content-backlog/SKILL.md` | Generate from the blueprint; verify pillar counts against the Content Calendar. |
| S4 — `checking-business-priorities` | `.claude/skills/checking-business-priorities/SKILL.md` | Generate from the blueprint; verify the intensity bands against the Cohorts database. |
| S5 — `committing-content-plan` | `.claude/skills/committing-content-plan/SKILL.md` | Generate from the blueprint; test the relation validation and duplicate check against a throwaway entry before running it on a real plan. |
| MCP: Notion | `.mcp.json` in the project (or user-level MCP config) | Install the Notion MCP server, authorize it with a Notion integration token, and share only the three databases with that integration. |

**Packaging note:** Standalone Skill — S1 through S5 install as five skill directories under `.claude/skills/` in James's content project. There is no second consumer, so there is no plugin or marketplace layer; the skills travel with the project directory.

**Orchestrator artifact (primary-loop platforms):** the user-triggered entry point is the orchestrator **skill** `content-calendar-planning` (`disable-model-invocation: true`, no `context: fork`), not a slash command. It takes the workflow name; S2–S5 take capability-specific names so the entry point never shadows a component skill. There are no sub-agents — `agents: 0` — and the orchestration logic lives in S1 and in this Deployment Plan.

**Run Logging:** S1 appends one row to `outputs/content-calendar-planning/runs.md` at the end of every run — date, trigger, result (posts planned, cadence met yes/no), edits needed — creating the file with its header if absent. Build bakes this into the orchestrator artifact.

**Recommended for frequent use:** keep the content project open as a Claude Code project with the five skills pre-loaded, so the Sunday session starts by name with nothing to set up.

---

## Cross-Layer Sections

*These sections apply across all three layers — handoff and metadata that doesn't belong to a single layer.*

## Evaluation Inputs

**Acceptance Criteria, Example Scenarios (including Golden Examples), and Human Gates are sourced from the Workflow Requirements file** (`outputs/content-calendar-planning/requirements.md`). They are not duplicated here — Step 5 (Test) reads them from that file directly. Listed by ID so a reader knows what Test will check:

- **AC1** — The plan covers a 2-week rolling window, and every planned post carries a Post Title, Channel, Source Content link, and Planned Date. (Yes / No)
- **AC2** — Each planned week meets the channel cadence targets: LinkedIn 3, Substack Newsletter 3–5, X long-form 1, YouTube 1. (Yes / No)
- **AC3** — All three content pillars appear across the 2-week window; no pillar is absent. (Yes / No)
- **AC4** — Every promotional obligation surfaced at Step 4 has at least one planned post. (Yes / No)
- **AC5** — Nothing was written to Notion before James approved the plan at Step 9. (Yes / No)
- **AC6** — Every Post entry created has its Source Content relation set to an existing Content Calendar entry; no orphan posts, no duplicate Draft with the same title and channel. (Yes / No)

**Golden Example** — one completed Sunday session, kept in the Workflow Requirements' Example Scenarios: a healthy backlog, one cohort five weeks out, and the approved plan it produced (weekly themes, idea-to-channel mapping, post titles and dates, and the Notion entries committed). Test compares a new run against it criterion by criterion; every criterion is a yes or no, never a score.

## Deferred to Build

Decisions intentionally left for Build to resolve. Build should not need to re-ask the user about anything else in the spec.

- [ ] Exact model version per capability tier on Claude Code (the tiers above are guidance; Build verifies current names)
- [ ] Notion MCP server setup specifics — integration token creation, which databases to share, transport
- [ ] Whether cadence targets and fit rules (C5, C6) live inline in S1 or in a separate reference file it reads
- [ ] The exact column set of `runs.md`

## Self-Test Summary

*Populated by the Design skill after running the Build Skill Needs Checklist (`references/self-test-checklist.md`).*

**Structure**
- ✓ Frontmatter present with workflow, requirements_file, spec_version `3.0`, approved, definition_type, mechanism, involvement, platform, platform_mode, packaging, counts
- ✓ Counts match the body — 10 steps, 5 Skill Candidates, 0 Agent Configuration entries, 1 Integration Options tool
- ✓ Source section names the Workflow Requirements file path
- ✓ All mandatory template sections present in template order; conditional sections handled per their rules
- ✓ Architecture Decisions table has Lens, Platform, Platform Mode, Orchestration, Involvement, Packaging, and Trigger rows
- ✓ Every step has separate Orchestration, Integration, Intelligence, and Build Output columns
- ✓ Step IDs match the Workflow Requirements (Step 1 … Step 10)
- ✓ Every step uses canonical autonomy terms (Human / Deterministic / Guided)
- ✓ Every Integration entry carries block type, tool name, and use/build tag
- ✓ Every Build Output is a canonical form (`New skill: SN`, `Use existing: …`, `Inline prompt → Workflow Requirements Step N`)
- ✓ Packaging is a canonical value (`Standalone Skill`); mechanism is `Skill`, not a legacy label

**Skill Candidates**
- ✓ Every `New skill: SN` reference has a matching entry (S2, S3, S4, S5), plus S1 the orchestrator
- ✓ All five entries carry all 12 fields
- ✓ Names are lowercase-hyphenated, under 64 characters, no consecutive hyphens; S2–S5 are capability-named, S1 takes the workflow name
- ✓ Every Description starts with "This skill should be used when…", is third-person, under 1024 characters, and names at least two concrete trigger contexts
- ✓ No two candidates describe the same capability at different steps
- ✓ S1 is the orchestrator skill, named with the workflow slug, Covers Steps: all
- ✓ No `Extend existing:` cells in this spec — Step 3 uses `Use existing: registering-content-ideas` unchanged

**Agent Configuration**
- ✓ No `New agent: AN` references — zero sub-agents, so the section is omitted and `agents: 0` is set
- ✓ Not applicable — no agent entries to carry the 14 fields
- ✓ Not applicable — no agent descriptions
- ✓ Not applicable — no agent tool lists; the only write surface (Notion via S5) is scoped in Safety & Permissions
- ✓ Not applicable — fewer than two agents, so no Multi-Agent Configuration section

**Cross-references**
- ✓ Notion is the only tool in the Integration column and has an Integration Options entry with three Source URLs
- ✓ Every `Depends On` reference points to a defined skill ID (S1 → S2–S5; S5 → S3) or to the named installed skill

**Mechanism-specific**
- ✓ Orchestrator Prompt Outline present — mechanism is `Skill`
- ✓ Agent Configuration omitted with `agents: 0`, and the orchestration logic is documented in the Deployment Plan

**Safety**
- ✓ Safety & Permissions present in Layer 1 with all four questions answered and mitigations named
- ✓ Constraint Conformance table present; five constraints, all Satisfied; none left silent
- ✓ Value & Measurement restates objective, outcome, measure, baseline, and target; `Baseline: Not recorded · Unknown` carried through as a visible flag
- ✓ The Workflow Requirements predates these sections — constraints and value fields are sourced as captured at Design, not presented as business statements
- ✓ No untrusted input, so the combined untrusted-input-plus-write rule does not apply; the write step is still behind the Step 9 human gate

**Completeness**
- ✓ Model Recommendation present with a default capability, per-step overrides, and the per-platform mapping note
- ✓ Data Readiness Summary present, referencing Context IDs C5, C6, C8, C9
- ✓ Deployment Plan present with target location and steps for all five skills and the MCP server, plus a packaging note
- ✓ Evaluation Inputs present, pointing to the Workflow Requirements; criteria listed by ID, not duplicated
- ✓ Deferred to Build lists what Build resolves at generation time
- ✓ Self-Test Summary present at the end, enumerating every checklist item
