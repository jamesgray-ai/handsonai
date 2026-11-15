# The opportunity report

Read after the list is confirmed, before writing the report; on print-to-save, also before giving the report so far; and when merging a later run into an existing report.

The report is written once the list is confirmed, in one batch with the nodes (`registering-candidates.md`; SKILL.md's *After the list is confirmed*). On print-to-save, a report so far is also given at the points in `resuming-and-picking-up.md`, with its **Report status** block at the top.

## Contents
- Report status (print-to-save only, while unfinished)
- Report Header
- Summary Table
- Detailed Opportunity Cards
- Workflow Candidate Summary
- Appendix: Value Lever Definitions

The report, in order:

## Report status (print-to-save only)

On print-to-save, while the report is a report so far (the list not yet confirmed), it starts with this block, which is the progress file there. Remove it at the final write. Locally and on drives, the report is written only after the list is confirmed, so it never has this block.

> **Report status:** unfinished — list not confirmed
> **Stage:** [the last step whose answer is saved, in plain words, as `resuming-and-picking-up.md` lists them]
> **Run:** [new / later / other lens] · **Lens:** [Individual / Organizational / Organizational, team]
> **Working folder:** [dedicated / general] (the web, Claude desktop and Cowork only)
> **This run's cards:** [the card numbers]
> **Already runs:** [the already-runs answers: name, home, regular use, works well or the improvement]
> **Relationship and role:** [the answers, when asked]
> **Flags:** do-more-of asked: [yes / no]; follow-ups used: [0–2]; offers made: [0–2]
> **Walking:** [every process walked in this run, in order, or "none"]

## Report Header

| | |
|---|---|
| **Name** | [User's name if known, otherwise omit row] |
| **Role** | [Role and domain] |
| **Date** | [YYYY-MM-DD] |
| **Lens** | Individual / Organizational / Individual + Organizational |
| **Opportunities identified** | [count] |
| **Goals and processes** | The goal map (`part-1-reading-and-the-lens.md`): "[goal]: [process], [process]", one entry per goal; omit the row with no goals |
| **Sources** | Working folder: [dedicated / general] (the web, Claude desktop and Cowork only; omitted elsewhere). Then one entry per source name (`evidence-pass.md`): "[source]: read [date]", "[source]: declined [date]" or "[source]: not offered". Then, when shortlist items were never shown, "Not shown: [short name] ([process]), [short name] ([process])" ("(not in a process yet)" for work not in a process yet). |

The fast path has no **Sources** row. Never a file or folder title in **Sources**: kinds only.

**The other-lens note**, under the header table, unless both lenses are done or the registry is personal-life, exactly: "This report covers the [lens just run] lens only. [The close's lens sentence.]" [lens just run] is "organizational" or "individual"; [The close's lens sentence.] is the close's lens sentence for this run, word for word in its platform's form (SKILL.md, *The close*: on Claude Code and Codex, and on print-to-save, its start phrases carry no location), for example: "This report covers the organizational lens only. The **individual lens** looks at the work you personally do each day, such as your inbox, prep and admin, and can find different workflows. Say 'run the analyze skill with the individual lens.'" Once both lenses are done, remove it.

## Summary Table

| # | Opportunity | Process | Value lever |
|---|------------|---------|-------------|
| 1 | [Name][ (already runs)] | [Process] | Streamline / Automate / Accelerate / Create value |

Never rank: no top recommendation, priority order, impact rating or size.

## Detailed Opportunity Cards

Group cards under a `#### [Process]` heading per Process, in registry order (others last), numbered straight through as in the Summary Table.

For each opportunity:

---

**[#] [Opportunity Name]**

**Status:** [Work that already runs only: "Already runs with [skill or agent], [home]", then what could be better, if anything. Omit the line otherwise.]

**Goal:** [The registry goal it serves, from the Business node's `## Objectives` (the first in order when it serves several), or "None named". Every lens.]

**Found in:** [The evidence clause, naming the source by kind ("your SOPs show a seven-step checklist for each new client"; "from what you told me"). Omit on the fast path.]

**Why it's a good candidate:**
[What characteristics make this well-suited for AI — repetitive, pattern-based, language-heavy, clear inputs/outputs, etc.]

**Current pain point:**
[What's slow, error-prone, inconsistent, or draining about how this is done today, in the student's words. A problem the AI drafted and the student didn't correct keeps its tag: "(my guess, from your [source])", or "(from your [source])" when the source states it. A size the student volunteered goes here, in their words, and a time or frequency they wrote about their own work, tagged "(from your [source])".]

**How AI helps:**
[What AI takes as input and what it produces — the work, never the mechanism]

**Value lever:** Streamline | Automate | Accelerate | Create value — [one sentence on why this lever]

**What changes for the business:**
[The outcome in plain language — who gets what, sooner, cheaper, or for the first time, and the do-more-of payoff the time freed goes to, when the student named one (only on the cards of the friction pieces known when the do-more-of question was asked, never on pieces found later). No tool, connector, or product name.]

**Systems involved today:** [Only if the user named one — the systems the work touches now. Omit the row otherwise.]

**Business Objective:** [Organizational lens only — which strategic objective this workflow supports; "None of the stated objectives — protects [what it protects]" when none fits, or "No stated objectives — protects [what it protects]" with no `## Objectives` block]
**Stakeholders:** [Organizational lens only — roles/teams involved (process owner + participants)]
**Success Metrics:** [Organizational lens only — KPIs this workflow itself moves; a broader business effect (more proposals won) is the reason, not a metric]

---

**Work that already runs:** *Current pain point* reads "None stated — runs well", or the improvement the student named ("could be better: not clear yet" when they gave no detail), and *How AI helps* describes what the skill or agent does today. Never invent either. **A registry workflow the evidence pass moved to running** gets an unnumbered card under its process, headed "[Workflow] (already in your registry, now recorded as running)", with no Summary Table or Candidate Summary row, not counted in **Opportunities identified**.

Confidential material follows `evidence-pass.md` in every field: the kind of work only, never a client, person, deal or project name, and no confidential figure (prices, rates, revenue, salaries, client figures) copied from a source; the student's own times and frequencies may be, tagged.

## Workflow Candidate Summary

Under `## Workflow Candidate Summary`, in the report's order and numbering, per candidate kept:

| Field | Content |
|-------|---------|
| **Workflow** | 2-4 word noun phrase, Title Case (each part of a hyphenated word capitalised: "Follow-Up") |
| **Process** | The Process it is filed under |
| **Goal** | The registry goal it serves (the first in order when it serves several), or "None named" |
| **Status** | Work that already runs only: "already runs with [skill or agent]"; omit the row otherwise |
| **Description** | One sentence in the naming-workflows shape: when it starts, what it produces, who receives or acts on it |
| **Trigger** | What kicks off this workflow — an event, schedule, or request; "Not clear yet — Deconstruct settles it" when it isn't known |
| **Deliverable** | The tangible output — what gets produced, sent, or decided; "Not clear yet — Deconstruct settles it" whenever the student didn't name one (never inferred), with the Description then reading naturally without it |
| **Value lever** | Streamline / Automate / Accelerate / Create value |
| **Pain point** | What's slow, error-prone, or manual today, with its tag when drafted |
| **AI opportunity** | Specific description of what AI would do |
| **Frequency** | Daily / Weekly / Monthly / Ad-hoc, only from what the student said or the evidence showed; otherwise "Not clear yet" |
| **Lens** | Individual / Organizational |
| **Business Objective** | (Organizational only) Which strategic objective this workflow supports |
| **Stakeholders** | (Organizational only) Roles/teams involved |
| **Success Metrics** | (Organizational only) KPIs this workflow itself moves, not broader business effects |

## Appendix: Value Lever Definitions

**Value lever — what kind of value does AI create here?** One per opportunity, the dominant one.

- **Streamline** — the work still happens the same way, with fewer steps, handoffs, or reformatting. Test: would the person still do it, just faster and cleaner?
- **Automate** — work a person does today runs without them. Test: does a person stop doing something they do now?
- **Accelerate** — the outcome arrives sooner, or more of it arrives in the same time. Test: is the gain measured in cycle time or throughput rather than effort?
- **Create value** — something becomes possible that was not done at all before. Test: is there no "today" version of this work to compare against?

When two levers apply, pick the one the user would use to justify the work to their manager or to themselves.
