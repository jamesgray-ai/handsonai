# Content Calendar Planning — Workflow Requirements

> **Note:** This example was produced under the older Workflow Definition format. The body below uses Scenario Metadata, Refined Steps (sub-steps / decision points / data in / data out / failure modes per step), and a Context Shopping List. The current PRD-style Workflow Requirements format uses Outcome, Metadata, Steps Overview, per-step Goal·Inputs·Outputs·Rules & Edge Cases·Context, Context Inventory, Acceptance Criteria, Example Scenarios, and Human Gates. This example will be regenerated to match the current format in a follow-up.

## Scenario Metadata

| Field | Value |
|---|---|
| **Workflow Name** | Content Calendar Planning |
| **Description** | Plan and sequence content across LinkedIn, Substack Newsletter, X, and YouTube for a 2-week rolling window. Reviews performance, checks business priorities, proposes AI-generated weekly themes balanced across three content pillars, maps ideas to channels, and commits titled Post entries with planned dates to the Content Calendar and Posts databases. |
| **Workflow Outcome** | Approved 2-week content plan with Post entries committed to Notion |
| **Trigger** | Weekly (Sunday) |
| **Type** | Augmented |
| **Business Process** | Content Distribution (Marketing) |
| **Business Objective** | Maintain a consistent, balanced content presence across four channels that builds audience trust, reinforces the Graymatter brand, and supports upcoming course launches. |
| **Current Owner** | James Gray |

### Channel Cadence Targets (per week)

| Channel | Target |
|---|---|
| LinkedIn Post | 3 |
| Substack Newsletter | 3-5 |
| X (long-form article) | 1 |
| YouTube | 1 (repurposed from Substack how-to content) |

> **Note:** Daily Substack Notes and shorter X posts are handled by the separate **Daily Content Distribution** workflow.

### Content Pillars

| Pillar | Description |
|---|---|
| **Master AI** | Step-by-step guidance to learn, use, and build with AI tools — from daily productivity to agentic workflows |
| **Master Yourself** | Mindset shifts, habits, and self-leadership practices to unlock potential and lead through rapid change |
| **Build What Matters** | Strategic frameworks, case studies, and tactics to create measurable value in career and business |

---

## Refined Steps

### Phase 1: Input Gathering

#### Step 1: Review Recent Content Performance

| Dimension | Detail |
|---|---|
| **Action** | Review published content from the last 2 weeks to identify what resonated and what didn't. |
| **Sub-steps** | (a) Query Posts database for posts with Published Date in the last 2 weeks. (b) Note top 3 performers by impressions/engagement — what topic, channel, and format worked. (c) Note underperformers — anything to drop or rethink. (d) If no metrics data available, do a qualitative scan of LinkedIn notifications and Substack stats for 2 minutes. |
| **Decision Points** | Are there clear "do more of this" or "stop doing this" signals? |
| **Data In** | Posts database: Published Date, Channel, Impressions, Engagements, Engagement Rate, Source Content |
| **Data Out** | Short list of performance signals that inform idea selection in Step 5 |
| **Context Needed** | Performance benchmarks per channel (to be built over time as data accumulates) |
| **Failure Modes** | No published posts or no metrics data in the Posts database. **Mitigation:** Skip to qualitative review; note the gap. Dependency on future Content Performance Collection workflow (currently in Backlog). |

#### Step 2: Review Content Idea Backlog

| Dimension | Detail |
|---|---|
| **Action** | Query the Content Calendar database for all entries with Status = "Idea" and review the pipeline. |
| **Sub-steps** | (a) Pull all "Idea" entries from Content Calendar. (b) Scan for anything that's become timely or urgent (news cycle, upcoming launch, trending topic). (c) Mentally flag 5-8 candidate ideas worth planning. |
| **Decision Points** | Is the backlog healthy (10+ ideas) or thin? If thin, Step 3 becomes more important. |
| **Data In** | Content Calendar database: Status = "Idea", Name, Description, Content Pillar, Priority |
| **Data Out** | Shortlist of candidate ideas to consider in Step 5 |
| **Context Needed** | Your sense of what's timely right now — domain knowledge you bring |
| **Failure Modes** | Empty backlog. **Mitigation:** Step 3 fills the gap. Commit to using `registering-content-ideas` skill during the week to capture ideas as they come. |

#### Step 3: Capture Fresh Ideas

| Dimension | Detail |
|---|---|
| **Action** | Quick sweep for any content ideas from the past week that haven't been captured yet. Not a full brainstorm — a "stragglers" check. |
| **Sub-steps** | (a) Review the week — what did you teach, discuss in coaching, or learn? (b) Scan AI news and trends — anything your audience needs to know? (c) Add each new idea to Content Calendar as Status = "Idea" with Name and short Description. |
| **Decision Points** | Is this idea worth capturing? Quick gut check: "Would my audience care about this in 2 weeks?" |
| **Data In** | Your memory of the week, bookmarks, notes, saved articles |
| **Data Out** | New entries in Content Calendar (Status = "Idea") |
| **Context Needed** | Content pillars (Master AI, Master Yourself, Build What Matters) for tagging |
| **Failure Modes** | You blank on the week. **Mitigation:** Keep a running note during the week (phone, Notion, voice memo) so Sunday isn't a cold start. |

#### Step 4: Check Upcoming Business Priorities

| Dimension | Detail |
|---|---|
| **Action** | Check for upcoming cohort launches, events, or promotions that content should support in the next 2-4 weeks. |
| **Sub-steps** | (a) Query Cohorts database for Status = "Upcoming" with Start Date within 6 weeks — flag promotional content needs. (b) Check calendar for Lightning Lessons, speaking events, partnerships, or deadlines. (c) List "must-promote" items with target channels and rough timing. |
| **Decision Points** | How much of the calendar should be promotional vs. organic? Guideline: no more than 30-40% promotional unless a launch is imminent. |
| **Data In** | Cohorts database (Status, Start Date, Course name), business calendar |
| **Data Out** | List of promotional obligations that constrain Step 5 (e.g., "Need 2 LinkedIn posts and 1 Substack newsletter about the March cohort") |
| **Context Needed** | Course launch timeline — how many weeks before a cohort start do you begin promoting? Your launch marketing playbook. |
| **Failure Modes** | No upcoming cohorts or events. **Mitigation:** This step completes quickly and you plan 100% organic content. |

---

### Phase 2: Planning

#### Step 5: Select Ideas and Set Weekly Themes

| Dimension | Detail |
|---|---|
| **Action** | AI analyzes the backlog and proposes weekly themes balanced across pillars. You select themes, then choose ideas that fit. |
| **Sub-steps** | (a) AI reviews backlog by Content Pillar — checks which pillar has been underrepresented recently. (b) AI proposes 2-3 theme options per week (e.g., "Master AI: Automate your weekly reporting" or "Build What Matters: Turning course knowledge into career leverage"). (c) You select themes for Week 1 and Week 2. (d) Select 4-6 content ideas per week that align with the chosen themes. (e) Reserve slots for promotional content from Step 4. (f) For each selected idea, note: Content Pillar, Effort, Priority, target Planned Date. |
| **Decision Points** | Is the pillar balance healthy across the 2-week window? Is there room for promotional content alongside organic? Does this idea fit the weekly theme? |
| **Data In** | Content Calendar (Status = "Idea"), recent published content pillar distribution, promotional obligations from Step 4, performance signals from Step 1 |
| **Data Out** | Selected ideas with assigned pillars, priorities, effort estimates, and rough dates (not yet written to Notion) |
| **Context Needed** | Content pillar definitions, Graymatter brand voice ("curated intelligence, filtering noise, hands-on practical"), recent pillar distribution |
| **Failure Modes** | All ideas cluster under one pillar. **Mitigation:** AI flags the imbalance and suggests ideas from underrepresented pillars. Planning too much — 12+ ideas/week beyond capacity. **Mitigation:** Cadence targets are the guardrail (8-10 pieces/week). |

#### Step 6: Map Ideas to Channels

| Dimension | Detail |
|---|---|
| **Action** | For each planned idea, decide which channels it will appear on. One content idea maps to 1-3 posts. |
| **Sub-steps** | (a) For each idea, determine the "anchor" channel — where the deepest version lives (usually Substack Newsletter). (b) Map derivative posts — a Substack newsletter might also become a LinkedIn post (key insight extracted), an X article (provocative take), and a YouTube video (how-to tutorial). (c) Identify the YouTube video candidate for each week — which idea has the best visual/tutorial potential? |
| **Decision Points** | Does every idea need to be on every channel? No. Match format to channel strength. Cap at 2-3 channels per idea to avoid over-mapping. |
| **Data In** | Selected ideas from Step 5, channel cadence targets |
| **Data Out** | Mapping of idea to channels (e.g., "Idea A -> Substack Newsletter + LinkedIn Post + X Article") |
| **Context Needed** | Channel-format fit rules (see below) |
| **Failure Modes** | Over-mapping — trying to put every idea on every channel creates too much work. **Mitigation:** Cap at 2-3 channels per idea. Under-mapping — not hitting cadence targets. **Mitigation:** Check totals against targets before proceeding. |

**Channel-Format Fit Rules:**

| Channel | Best For | Typical Length |
|---|---|---|
| Substack Newsletter | Deep dives, tutorials, frameworks, case studies | 800-2000 words |
| LinkedIn Post | Actionable insights, personal stories, provocative takes | 200-500 words |
| X (long-form article) | Opinionated long-form, contrarian takes, trend analysis | 500-1500 words |
| YouTube | How-to tutorials, walkthroughs, visual demonstrations | 5-15 minutes |

#### Step 7: Create Post Plan

| Dimension | Detail |
|---|---|
| **Action** | For each idea-channel combination, draft the Post entry details. |
| **Sub-steps** | (a) Write a Post Title tailored to the channel format (a LinkedIn title is different from a Substack title). (b) Write a brief angle/hook — what makes this post different from the source idea on this specific channel? (c) Assign Planned Date. (d) Note the Source Content link (which Content Calendar entry this derives from). |
| **Decision Points** | Does the Post Title reflect the channel format? Is the angle distinct enough from the anchor version? |
| **Data In** | Idea-to-channel mapping from Step 6, planned dates |
| **Data Out** | Draft post plan (not yet in Notion) — list of posts with Title, Channel, Source Content, Planned Date, angle/hook notes |
| **Context Needed** | Graymatter brand voice, channel-specific writing conventions |
| **Failure Modes** | Generic titles that don't work for the channel. **Mitigation:** AI proposes channel-appropriate titles. |

#### Step 8: Sequence and Balance

| Dimension | Detail |
|---|---|
| **Action** | Review the full 2-week post plan for distribution and balance. Adjust dates to avoid clusters and gaps. |
| **Sub-steps** | (a) Visual scan of the 2-week calendar — check for gaps and clusters. (b) Verify: no more than 2 posts on the same day, no channel going 3+ days without a post. (c) Place YouTube video mid-week (best engagement). Spread Substack newsletters across the week. (d) Adjust Planned Dates as needed. |
| **Decision Points** | If two big pieces land on the same day, which moves? Priority order: promotional > timely > evergreen. |
| **Data In** | Draft post plan from Step 7 |
| **Data Out** | Sequenced and balanced post plan with final dates |
| **Context Needed** | Channel cadence targets, day-of-week best practices |
| **Failure Modes** | Everything bunched on Monday/Tuesday with empty Thurs/Friday. **Mitigation:** Calendar visualization catches this. |

---

### Phase 3: Approval

#### Step 9: Refine and Approve the Plan

| Dimension | Detail |
|---|---|
| **Action** | AI presents the complete 2-week plan for collaborative review. Iterate together until the plan is approved. |
| **Sub-steps** | (a) AI presents a structured summary: weekly themes, content ideas with pillars, channel mapping, post titles, planned dates, cadence counts, pillar balance. (b) You review and react — "swap this idea," "move this to Week 2," "I need more Master Yourself content," "this week is heavy for me, scale back." (c) AI adjusts the plan based on feedback. (d) Repeat until you approve. |
| **Decision Points** | Is the plan realistic given your week? If heavy teaching week, scale back. If light week, add one more piece. Are cadence targets met? Is pillar balance healthy? |
| **Data In** | Complete post plan from Steps 5-8 |
| **Data Out** | Approved 2-week content plan |
| **Context Needed** | Your weekly schedule/availability, any known constraints |
| **Failure Modes** | Endless iteration without converging. **Mitigation:** Limit to 3 rounds of refinement. If still not right, commit what's agreed and flag remaining items for mid-week adjustment. |

---

### Phase 4: Execution

#### Step 10: Commit Content Plan

| Dimension | Detail |
|---|---|
| **Action** | Write the approved plan to both Notion databases. |
| **Sub-steps** | (a) Update Content Calendar entries: Status -> "Planned", assign Content Pillar, Effort, Priority, Planned Date. (b) Create Post entries in Posts database: Post Title, Channel, Source Content (linked to Content Calendar entry), Planned Date, Status = "Draft", angle/hook in Notes field. (c) Present confirmation with links to the updated entries. |
| **Decision Points** | None — this is mechanical execution of the approved plan. |
| **Data In** | Approved plan from Step 9 |
| **Data Out** | Content Calendar entries updated to "Planned". Post entries created as "Draft" in Posts database with Source Content linked. |
| **Context Needed** | Content Calendar and Posts database connections configured in your AI tool. |
| **Failure Modes** | Forgetting to link Source Content (breaks parent-child relationship). **Mitigation:** Always set the Source Content relation when creating Post entries. API failure. **Mitigation:** Retry; entries are idempotent. |

---

## Step Sequence and Dependencies

### Dependency Map

```
Step 1 (Performance) ──┐
Step 2 (Backlog) ──────┤──> Step 5 (Select & Theme) ──> Step 6 (Map Channels)
Step 3 (Fresh Ideas) ──┤        ↑                            │
Step 4 (Priorities) ───┘    promotional                      ▼
                           constraints                  Step 7 (Post Plan)
                                                             │
                                                             ▼
                                                        Step 8 (Sequence)
                                                             │
                                                             ▼
                                                        Step 9 (Refine & Approve)
                                                             │
                                                             ▼
                                                        Step 10 (Commit)
```

### Parallel Steps

- **Steps 1, 2, 4** can run in parallel — they are independent data pulls from different sources (Posts DB, Content Calendar DB, Cohorts DB + calendar).
- **Step 3** benefits from Step 2 completing first (to avoid adding duplicate ideas), but is not strictly blocked.

### Sequential Steps

- Steps 5 → 6 → 7 → 8 → 9 → 10 must run in sequence. Each builds on the output of the previous step.

### Critical Path

Steps 2 → 5 → 6 → 7 → 8 → 9 → 10 is the critical path. Step 2 (backlog review) is the primary input that everything else depends on.

---

## Context Shopping List

| # | Artifact | Description | Used By Steps | Status | Key Contents |
|---|---|---|---|---|---|
| 1 | **Content Calendar database** | Backlog of content ideas with Status, Pillar, Priority, Planned Date | 2, 3, 5, 10 | Exists | Status options: Idea, Planned, In Progress, In Review, Published. Content Pillars: Master AI, Master Yourself, Build What Matters. |
| 2 | **Posts database** | Individual channel-specific posts linked to content ideas | 1, 7, 8, 10 | Exists | Channels: LinkedIn Post, LinkedIn Newsletter, Substack Newsletter, Substack Note, X, YouTube, + others. Status: Draft, Scheduled, Published, Archived. |
| 3 | **Cohorts database** | Upcoming course cohorts with Start Date and Status | 4 | Exists | Status: Upcoming, Active, Completed. Key fields: Start Date, Course, Name. |
| 4 | **Content pillar definitions** | Descriptions of the three Graymatter content pillars | 5, 6, 9 | Exists | Master AI: "Step-by-step guidance to learn, use, and build with AI tools." Master Yourself: "Mindset shifts, habits, and self-leadership practices." Build What Matters: "Strategic frameworks, case studies, and tactics to create measurable value." |
| 5 | **Channel cadence targets** | Target number of posts per channel per week | 6, 8, 9 | Needs Creation | LinkedIn Post: 3/week. Substack Newsletter: 3-5/week. X (long-form article): 1/week. YouTube: 1/week. |
| 6 | **Channel-format fit rules** | What content type works best on each channel | 6 | Needs Creation | Substack: deep dives, tutorials (800-2000 words). LinkedIn: actionable insights, stories (200-500 words). X: opinionated long-form (500-1500 words). YouTube: how-to tutorials (5-15 min). |
| 7 | **Graymatter brand voice** | Brand positioning and voice guidelines | 5, 6, 7 | Exists | "Curated intelligence for professionals overwhelmed by AI noise. Filtering noise, translating complexity. Hands-on, practical application." |
| 8 | **Business calendar** | Upcoming events, deadlines, speaking engagements | 4 | Exists | Google Calendar or equivalent. Checked manually during Step 4. |
| 9 | **Performance benchmarks per channel** | What "good" looks like for impressions/engagement per channel | 1 | Needs Creation | To be built over time as data accumulates via the Content Performance Collection workflow (Backlog). |

---

## Related Workflows

| Workflow | Relationship | Status |
|---|---|---|
| **Daily Content Distribution** | Handles daily Substack Notes and shorter X posts — separated from this weekly planning workflow | Under Development |
| **Content Performance Collection** | Feeds Step 1 by automatically populating Posts database with engagement metrics | Backlog |
| **Content Publishing** | Downstream — executes the actual writing and publishing of planned content | Exists |

---

## Database Changes Made During Deconstruction

1. **Content Calendar — Status field**: Added "Planned" option between "Idea" and "In Progress"
2. **Content Calendar — Content Pillar field**: Updated options from (AI, Career Strategy, Self-Leadership) to (Master AI, Master Yourself, Build What Matters)
3. **Workflows database**: Registered "Daily Content Distribution" (Under Development) and "Content Performance Collection" (Backlog)
4. **Content Calendar Planning workflow**: Updated description and outcome to reflect refined scope
