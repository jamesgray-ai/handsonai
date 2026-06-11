---
title: "Step 2: Deconstruct Workflows into Requirements"
description: Capture your workflow as a Product Requirements Document (PRD) — clear requirements, decision rules, and edge cases that feed directly into the Design step.
---

> **Part of:** [AI Workflow Framework](../)

## What This Is

Step 2 is the **Product Requirements Document (PRD) for your workflow**. It captures *what* the workflow must do, *the rules it must follow*, and *the edge cases it must handle* — in clear requirements language that feeds directly into Step 3 (Design).

The output is a single Markdown file: the **Workflow Requirements** document. It's structured so the Design step — or any AI model — can read it and act on it without re-interviewing you.

| | |
|---|---|
| **What you'll do** | Choose one of two paths (you know the steps, or you know the outcome), then work through a guided conversation that captures the requirements |
| **What you'll get** | A **Workflow Requirements** document — `outputs/[name]/requirements.md` |
| **Time** | ~15-25 minutes of interactive conversation |

## Why This Matters

You can't operationalize AI on a process you don't understand. Before you can design how AI building blocks will deliver the work, you need to capture the work itself: what triggers it, what good output looks like, the decision rules, the edge cases, the context it needs.

Step 2 separates *what* from *how*. The Workflow Requirements stays in "what" territory — outcome, rules, acceptance criteria. Step 3 (Design) handles the "how" — orchestration mechanism, agents, models, integrations. Keeping the two artifacts distinct means:

- The Workflow Requirements is the canonical source of truth for *what the workflow does*
- The Design Spec doesn't restate requirements; it references them
- Step 5 (Test) reads acceptance criteria and example scenarios straight from the Workflow Requirements
- Step 7 (Improve) compares the deployed workflow against the requirements baseline

This builds directly on the concept of workflow deconstruction. If terms like the "6-question framework" or "AI building blocks" are new to you, review the [Key Concepts section of the AI Workflow Framework](../#key-concepts) for quick definitions before starting.

## The Two Paths

Step 2 presents one question upfront: **do you know the steps, or just the outcome?**

| Path | When to use | Mental model |
|---|---|---|
| **Step-decomposed** | You can describe how the work gets done | "I know the steps" |
| **Outcome-driven** | You know what "done" looks like, but the work takes different steps depending on what comes in — you want an agent system to figure out the steps at runtime | "I know the outcome" |

**Not sure which?** Imagine two different inputs and ask: *would the work take noticeably different steps?* If it runs the same way every time, it's step-decomposed. If the steps change depending on what comes in — a refund request, a partnership pitch, and a spam message each handled differently — it's outcome-driven.

:::note[What "outcome" means here]
The outcome is the **bounded result a single run produces** — the deliverable plus its rules and acceptance criteria — not a business goal or impact metric. ("Reduce churn" is a goal; "a drafted retention email per at-risk customer" is an outcome.) What makes a workflow outcome-driven is that **the agent decides the path** to that result at runtime — not simply that agents are involved. A step-decomposed workflow can still use an agent for an individual step; it's outcome-driven only when the agent owns the overall sequence.
:::

Both paths produce a Workflow Requirements document with the same shared structure — only the middle "what does the workflow do" block differs.

**Don't have either yet?** If you only have a problem ("People drop off during enrollment and I have no way to follow up"), describe it. The model proposes a candidate workflow, then routes you into one of the two paths above. No separate "problem-first" path to learn.

## How the Skill Works

Phases 1–3 establish *what* you're deconstructing and are the same for both paths. From phase 4 on, the skill follows the path you picked.

**Phases 1–3 (both paths):**

1. **Scenario analysis** — If you reference an opportunity report from Analyze, the skill reads the workflow candidates and pre-populates metadata. Otherwise it asks about the business scenario, objective, high-level steps, and ownership. If you describe a problem instead of a workflow, the skill proposes a candidate workflow for you to react to.
2. **Scope check** — Is this one workflow or multiple bundled together? If multiple, the skill recommends splitting and asks which to start with.
3. **Name the workflow** — The skill proposes 2–3 name options (2–4 word noun phrases, Title Case) and confirms name, description, outcome, trigger, and type.

**Step-decomposed (phase 4 on):**

4. **Deep dive** — For each step, the skill probes six dimensions: discrete steps, decision points, data flows, context needs, failure modes, data readiness.
5. **Propose and react** — From step 4 onward, the skill proposes a hypothesis across all six dimensions and asks "What's right, what's wrong, what am I missing?"
6. **Optimize for AI** — Once the full process is mapped, the skill challenges it: steps to eliminate, collapse, parallelize, or simplify for an AI-powered version.
7. **Map sequence** — Identify sequential vs. parallel steps and the critical path.
8. **Validate** — Walk the refined workflow end-to-end to catch gaps before Design.

**Outcome-driven (phase 4 on):** Instead of decomposing steps, the skill runs a short interview that stays in "what" territory:

4. **Outcome** — You describe what you want in plain language ("like you'd tell a colleague"); the skill reflects back a structured deliverable (format, structure, scope) and confirms.
5. **Variation, inputs, rules, fallback, context, human gates** — The skill captures the range of situations to handle, what the agent receives, the guardrails, what to do when it's stuck, the data sources, and where to pause for review.
6. **Validate** — A quality gate checks the outcome is bounded, the variation range and fallback behavior are defined, the rules are sufficient, and the context is reachable.

**Both paths converge (final phases):**

- **Consolidate context** — Present a rolled-up "context shopping list" of every artifact the workflow needs.
- **Acceptance criteria & example scenarios** — Capture what good output looks like and 3–5 representative scenarios to test against.
- **Generate Workflow Requirements** — Write the structured Workflow Requirements to the output file.

## How to Use This

This step is facilitated by the **`deconstruct`** AI Workflow Framework skill. How you get it depends on your platform — see [Set Up the Skills](../skills/) for installation instructions.

**Command:** `/handsonai:deconstruct` (Claude Code) — or invoke by name on any other platform.

**Platform compatibility:** Claude Code ✓ &nbsp;|&nbsp; Claude.ai ✓ &nbsp;|&nbsp; Claude Cowork ✓ &nbsp;|&nbsp; ChatGPT ✓ &nbsp;|&nbsp; Gemini ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Codex / Antigravity ✓

**Start with this prompt:**

```
I need to deconstruct my [workflow name] workflow.
```

The skill asks you to choose a path, runs an interactive interview to capture the requirements, validates the workflow end-to-end, and writes the Workflow Requirements file.

### Example prompts

```
"Use deconstruct to break down my expense reporting process"
→ Interactive discovery session producing
  outputs/expense-reporting/requirements.md

"I need to document how our team handles customer escalations"
→ Walks through the discovery process, probing for hidden steps
  and decision points
```

:::tip[If your AI tool doesn't support skills]
Download the skill file from [GitHub](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins/handsonai/skills/deconstruct) and paste it into your system prompt or project instructions.
:::

### Example: Step-decomposed path

After you start the conversation, the model asks you to choose a path. If you pick step-decomposed, here's what the opening looks like:

> **Model:** Do you know the steps, or just the outcome? (Quick test: imagine two different inputs — would the work take the same steps, or different steps?)
> - **Step-decomposed** — The work runs the same way each time and you can describe how it gets done.
> - **Outcome-driven** — You know what "done" looks like, but the work takes different steps depending on what comes in, so an agent figures out the steps.
>
> **You:** Step-decomposed. I research LinkedIn prospects before sales outreach. The goal is to find people who'd be a good fit for our AI training programs, understand their background, and write personalized outreach messages.
>
> **Model:** Got it — LinkedIn prospect research for personalized sales outreach. Can you walk me through the high-level steps? Don't worry about being complete or precise — we'll refine them together.
>
> **You:** I guess I start by finding people on LinkedIn, then I look at their profile, check their company, see if they've posted anything relevant, then I write the message. There's probably more to it but that's the gist.

From there, the model takes your rough steps and systematically breaks each one down — uncovering the sub-steps, decision rules, edge cases, and context you didn't think to mention. Each step in the final Workflow Requirements is captured as **Goal / Inputs / Outputs / Rules & Edge Cases / Context Needed**.

### Example: Outcome-driven path

If you pick outcome-driven, you don't need to map anything out. You describe what you want in plain language, and the model does the structuring — reflecting back a crisp deliverable for you to confirm:

> **Model:** This path is for when you know what you want but not the exact steps — you don't need to map anything out. Just tell me what "done" looks like and the rules it has to follow. Describe what you want out of this, like you're telling a colleague.
>
> **You:** I want a competitive analysis report every week so I'm not caught off guard by what our competitors are doing.
>
> **Model:** So the deliverable is roughly a weekly competitive analysis brief — a markdown doc, a couple of pages, with an executive summary up top and a section per competitor covering what they shipped, pricing, and messaging — for you to read before the week starts. Did I get that right, or what's off?
>
> **You:** Yes, top 5 competitors, and add any strategic moves like funding or leadership changes.
>
> **Model:** Got it. This works as outcome-driven because the work takes different steps depending on what's happening that week. What's the range it needs to handle — a typical week, and the harder ones?
>
> **You:** Most weeks it's incremental — a feature here, a blog post there. But sometimes a competitor raises funding or rebrands, and that should get more attention.

From there, the model continues through inputs, rules, fallback behavior (what to do when a source is unreachable), context sources, and human gates — building an outcome-driven Workflow Requirements without decomposing into fixed steps.

### Example: Starting with a problem

You don't need an existing process. If you have a gap or pain point, describe that — the model proposes a candidate workflow, then asks which of the two paths fits:

> **Model:** Do you know the steps, or just the outcome?
>
> **You:** Neither, really. People sign up for my online course but a lot of them never finish. I have no way to know who's dropping off or how to follow up.
>
> **Model:** That's a gap, not a process. Let me propose a candidate workflow: (1) detect drop-offs by polling course completion data, (2) classify the drop-off reason, (3) draft a personalized follow-up message, (4) send it. Sound roughly right?
>
> **You:** Yes, that's the shape of it.
>
> **Model:** Good. Two paths from here: do you want to refine these steps with me (step-decomposed), or describe the outcome and let an agent figure out the steps (outcome-driven)?

You pick the path, and the conversation continues into the deep dive.

### Not sure which workflow to try?

Browse the [AI Use Cases](../../use-cases/) section for inspiration — type to search or filter by primitive (content creation, research, coding, data analysis, ideation, automation).

Or pick something you do regularly and could describe to a colleague over coffee. Here are some examples students have used:

- **Weekly team status reporting** — gathering updates from multiple sources, synthesizing, and distributing a summary
- **New client onboarding** — intake, account setup, kickoff scheduling, and initial deliverables
- **Processing expense reports** — collecting receipts, validating against policy, approving, and submitting for reimbursement
- **Content publishing pipeline** — drafting, editing, formatting, scheduling, and distributing across channels
- **Candidate screening** — reviewing applications, initial outreach, scheduling interviews, and tracking status
- **Vendor evaluation** — gathering proposals, comparing against criteria, scoring, and recommending a decision
- **Course enrollment follow-up** — people start signing up but don't finish, and there's no process to detect drop-offs or send reminders
- **Competitive analysis pipeline** (outcome-driven) — you know what the deliverable looks like but want an agent system to determine the research approach

You don't need to know all the steps before you start — that's what the skill helps you figure out. Even "I onboard new clients and it takes forever" is enough to begin.

## What the Skill Produces

The **Workflow Requirements** document uses a shared structure for both paths — only the middle "what does the workflow do" block differs. Every section is structured so Design (or any agent model) can parse it without re-asking questions.

**Shared sections (both paths):**

- **Outcome** — what a successful run produces, when it runs, who consumes it
- **Metadata** — workflow name, trigger, owner, lens (Individual / Organizational), Definition Type (Step-Decomposed / Outcome-Driven)
- **Context Inventory** — every artifact the workflow needs, with stable IDs (C1, C2, …), status (Exists / Needs Creation), AI accessibility (Yes / Partial / No), and location
- **Acceptance Criteria** — what good output looks like, dimensions that matter (accuracy, completeness, tone, etc.), and the minimum bar
- **Example Scenarios** — 3-5 representative inputs with what to look for in the output, plus optional **Golden Examples** — real past outputs you'd consider "exactly right." These feed Step 5 (Test), where scoring against a known-good reference beats gut-feel ratings
- **Human Gates** — where human review or input is required
- **Optimization Notes** (optional, step-decomposed only) — what changed from the original process and why

**Step-decomposed middle block:**

- **Steps Overview** — a scannable numbered list, one line per step
- **Step Details** — each step captured as **Goal / Inputs / Outputs / Rules & Edge Cases / Context Needed**, plus a **Role** field when the workflow uses the Organizational lens (to capture which role owns each step)
- **Sequence** — sequential vs. parallel steps, critical path, role swimlane

Most step-decomposed workflows expand from 5-8 rough steps to 12-20 refined steps after the deep dive.

**Outcome-driven middle block:**

- **Inputs** — what the agent system receives to start (data, materials, references, access)
- **Rules & Constraints** — must-do / must-never-do, scope boundaries, guardrails, tone, length limits, and **fallback behavior** (what the agent does when it can't confidently complete a case — stop and ask, best-effort and flag, or skip)

Outcome-driven workflows **don't** capture capability domains, agent count, or orchestration approach — those are Design decisions. Step 2 stays in "what" territory.

### Why this format

The Workflow Requirements reads like a PRD, not an interview transcript:

- **Requirements voice** — each line states what must be true, not what the user said in conversation
- **Fixed structure** — same section headings every time, so downstream skills (Design, Test, Improve) can locate any requirement by path
- **Stable IDs** — steps are numbered, context items are `C1, C2, C3, …`, scenarios are `E1, E2, E3, …`
- **Tables for lists of items with shared fields** — easier to parse than prose
- **No interview residue** — no "the user mentioned", "usually", or other narrative

### Process optimization (step-decomposed only)

For step-decomposed workflows, the skill includes an **Optimize for AI** pass after the deep dive. Once the full process is mapped, the model steps back and challenges it — looking for steps that exist only because a human was doing the work (an integration eliminates the manual transfer), steps that can be collapsed (AI drafts and formats in one pass), steps that can be parallelized (no data dependency), handoffs that can be simplified, and new steps needed for the AI version. These are presented as recommendations for you to accept or reject — you may have good reasons to keep steps as-is (compliance, audit trail, stakeholder expectations). The Workflow Requirements records what changed and why.

### Workflow validation (step-decomposed only)

After optimization, the skill runs a **validation pass** — walking through the refined workflow end-to-end to catch gaps before it moves to Design. This is the quality gate that stress-tests the workflow for:

- **Completeness** — Are there gaps where one step's output doesn't connect to the next step's input?
- **Logic gaps** — Decision points without clear criteria, or steps that assume information not produced by a prior step?
- **Edge cases** — Scenarios you haven't mentioned (empty inputs, unexpected formats, partial data, exception paths)?
- **Redundancy** — Steps that duplicate work or produce outputs no downstream step consumes?
- **Handoff clarity** — Is it clear what passes between each step, and in what form?

The model presents its findings as a summary and asks you to confirm or address each one. Any issues get resolved before the Workflow Requirements is finalized.

## Tips for Better Results

- **Start with workflows you actually do.** Real processes have real complexity that produces useful requirements. Hypothetical workflows tend to be too clean.
- **Include the messy details.** "Sometimes I skip this step if the client is a repeat customer" is exactly the kind of decision rule that belongs in the requirements.
- **Don't over-prepare your steps.** The model works with rough, incomplete descriptions. Let it do the work of refining.
- **Gather your context resources early.** The model identifies specific resources the workflow needs — documents, spreadsheets, databases, CRM access, application credentials, sample data. If you already have these, have them ready. If you don't, the analysis tells you exactly what to create or set up.

:::tip[Your workflow gets its own folder]
Once the name is confirmed, the skill creates a folder for the workflow — `outputs/[name]/` — with a small `workflow.yaml` manifest inside. The manifest tracks which framework step you're on and where every artifact lives, so any later session (or any framework skill) can pick up exactly where you left off. Your `outputs/` directory becomes your workflow inventory — no separate tracking system required.
:::

## Related

- **Previous step:** Not sure which workflow to deconstruct? Start with [Analyze Workflows](../analyze/) (Step 1) to identify your best candidates.
- **Next step:** Ready to design? Go to [Design Your AI Workflow](../design/) (Step 3) — assess autonomy, choose an orchestration mechanism, and map building blocks.
- [AI Workflow Framework](../) — the full seven-step methodology
- [Prompts](../../agentic-building-blocks/prompts/)
- [Agents](../../agentic-building-blocks/agents/)
