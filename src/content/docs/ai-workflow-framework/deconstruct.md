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
| **What you'll do** | Describe your workflow; the skill proposes a path (step-driven or goal-driven) with its reason, you confirm, then work through a guided conversation that captures the requirements |
| **What you'll get** | A **Workflow Requirements** document — `outputs/[name]/requirements.md` |
| **Time** | ~45–60 minutes on your own (30–40 with an instructor guiding you) |

## Why This Matters

You can't operationalize AI on a process you don't understand. Before you can design how AI building blocks will deliver the work, you need to capture the work itself: what triggers it, what good output looks like, the decision rules, the edge cases, the context it needs.

Step 2 separates *what* from *how*. The Workflow Requirements stays in "what" territory — goal, rules, acceptance criteria. Step 3 (Design) handles the "how" — orchestration mechanism, agents, models, integrations. Keeping the two artifacts distinct means:

- The Workflow Requirements is the canonical source of truth for *what the workflow does*
- The Design Spec doesn't restate requirements; it references them
- Step 5 (Test) reads acceptance criteria and example scenarios straight from the Workflow Requirements
- Step 7 (Improve) compares the deployed workflow against the requirements baseline

This builds directly on the concept of workflow deconstruction. If terms like the "6-question framework" or "AI building blocks" are new to you, review the [Key Concepts section of the AI Workflow Framework](../#key-concepts) for quick definitions before starting.

## The Two Paths

Step 2 opens by asking you to describe the workflow, then proposes one of two paths and asks you to confirm:

| Path | When to use | Mental model |
|---|---|---|
| **Step-driven** | You can describe how the work gets done | "I know the steps" |
| **Goal-driven** | You know what "done" looks like, but the work takes different steps depending on what comes in — you give an agent system a goal and let it figure out the steps at runtime | "I know the goal" |

**Not sure which?** Ask one question: *could you write down every path the work can take?* If yes — even with branches, like a three-way triage — it's step-driven; the branches become decision points. If the path depends on what the agent finds along the way, it's goal-driven.

:::note[What "goal" means here]
An agent goal is a **deliverable with a completion state** — something you can look at after a single run and verify is done. It is *not* a business objective or an impact metric: "higher revenue" is a business objective (it's recorded under `Value & Measurement`, alongside what you'd count and where that number stands today); "a ranked list of 20 qualified prospects matching our ICP, with contact info" is an agent goal. This matches how the major agent frameworks specify work — a goal bounded by an expected output and success criteria. (If you know the product-management "outcomes over outputs" framing: the agent's goal is closer to an *output* — the business outcome belongs in Business Objective.) What makes a workflow goal-driven is that **the agent decides the path** to the goal at runtime — not simply that agents are involved. A step-driven workflow can still use an agent for an individual step; it's goal-driven only when the agent owns the overall sequence.
:::

On the goal-driven path you're still deconstructing — not the process into steps, but the goal into its parts: the deliverable, the range of situations it must handle, the rules, and what "done" looks like.

Both paths produce a Workflow Requirements document with the same shared structure — only the middle "what does the workflow do" block differs.

**Don't have either yet?** If you only have a problem ("People drop off during enrollment and I have no way to follow up"), describe it. The model proposes a candidate workflow, then routes you into one of the two paths above. No separate "problem-first" path to learn.

## How the Skill Works

Phases 1–3 establish *what* you're deconstructing and are the same for both paths. From phase 4 on, the skill follows the path you picked, and the two rejoin at phase 11.

**Step-driven (all 13 phases):**

1. **Scenario discovery** — If you reference an opportunity report from Analyze, the skill reads the workflow candidates and pre-populates metadata. Otherwise it asks about the business scenario, objective, high-level steps, and ownership. If you describe a problem instead of a workflow, the skill proposes a candidate workflow for you to react to.
2. **Scope check** — Is this one workflow or multiple bundled together? If multiple, the skill recommends splitting and asks which to start with.
3. **Name the workflow** — The skill proposes 2–3 name options (2–4 word noun phrases, Title Case) and confirms name, description, goal, trigger, and type.
4. **Deep dive** — For each step, the skill probes six dimensions: discrete steps, decision points, data flows, context needs, failure modes, data readiness.
5. **Propose and react** — From the second step of your workflow onward, the skill proposes a hypothesis across all six dimensions and asks "What's right, what's wrong, what am I missing?"
6. **Map sequence** — Identify sequential vs. parallel steps and the critical path.
7. **Human gates** — Where must a person review or approve before the workflow continues?
8. **Workflow-level rules** — Must always / must never / out of scope / tone and format / what to do when stuck.
9. **Optimize for AI** — Once the full process is mapped, the skill challenges it: steps to eliminate, collapse, parallelize, or simplify for an AI-powered version.
10. **Validate the workflow** — Walk the refined workflow end-to-end to catch gaps before Design.
11. **Consolidate context** — A rolled-up "context shopping list" of every artifact the workflow needs, classified for sensitivity.
12. **Define how you will judge the output** — a real good example first, then numbered yes/no criteria derived from it, 3–5 realistic inputs, and golden examples where they exist.
13. **Generate Workflow Requirements** — Write the structured Workflow Requirements to the output file.

**Goal-driven:** phases 1–3 are identical. Instead of decomposing steps, phase 4 runs a short interview that stays in "what" territory, then skips straight to the goal-driven validation gate (numbered 10 to mirror the step-driven one):

4. **Goal interview** *(goal-driven)* — The situation, the goal reflected back as a concrete deliverable and pressure-tested, then the variation range, inputs, rules, fallback behavior, context sources, and human gates.

Then the goal-driven gate, and both paths rejoin at phase 11:

10. **Validate** *(goal-driven)* — A quality gate checks the goal is bounded and testable, the variation range and fallback behavior are defined, the rules are sufficient, and the context is reachable.
11. **Consolidate context** — A rolled-up "context shopping list" of every artifact the workflow needs, classified for sensitivity.
12. **Define how you will judge the output** — a real good example first, then numbered yes/no criteria derived from it, 3–5 realistic inputs, and golden examples where they exist.
13. **Generate Workflow Requirements** — Write the structured Workflow Requirements to the output file.

## How to Use This

This step is facilitated by the **`deconstruct`** AI Workflow Framework skill. How you get it depends on your platform — see [Set Up the Skills](../skills/) for installation instructions.

**How to start:** Say *"run the deconstruct skill"* (or *"deconstruct my workflow"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:deconstruct`, and Cowork lists it when you type `/`.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
I need to deconstruct my [workflow name] workflow.
```

The skill proposes a path from your description, runs an interactive interview to capture the requirements, validates the workflow end-to-end, and writes the Workflow Requirements file.

### Example prompts

```
"Use deconstruct to break down my expense reporting process"
→ Interactive discovery session producing
  outputs/expense-reporting/requirements.md

"I need to document how our team handles customer escalations"
→ Walks through the discovery process, probing for hidden steps
  and decision points
```

:::tip[Don't have the skill installed yet?]
Every platform in the course can load it — [Set Up the Skills](../skills/) has the steps, and [deconstruct.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/deconstruct.zip) is the direct download.
:::

### Example: Step-driven path

After you start the conversation, the model proposes a path from what you describe. If it proposes step-driven, here's what the opening looks like:

> **Model:** Tell me about the workflow — what kicks it off, what you do, and what comes out the other end. Rough is fine.
>
> **You:** I research LinkedIn prospects before sales outreach. The goal is to find people who'd be a good fit for our AI training programs, understand their background, and write personalized outreach messages.
>
> **Model:** From what you've described this sounds **step-driven** — the same steps run each time, with a couple of decision points we'll capture. (The other path, goal-driven, is for work where the steps depend on what the agent finds along the way.) Shall we go step-driven?
>
> **You:** Yes.
>
> **Model:** Can you walk me through the high-level steps? Don't worry about being complete — we'll refine them together.
>
> **You:** I guess I start by finding people on LinkedIn, then I look at their profile, check their company, see if they've posted anything relevant, then I write the message. There's probably more to it but that's the gist.

From there, the model takes your rough steps and systematically breaks each one down — uncovering the sub-steps, decision rules, edge cases, and context you didn't think to mention. Each step in the final Workflow Requirements is captured as **Goal / Inputs / Outputs / Rules & Edge Cases / Context Needed**.

### Example: Goal-driven path

If you pick goal-driven, you don't need to map anything out. The model grounds itself in your situation first, then helps you sharpen the goal — including pushing back when the goal is a business metric instead of a deliverable:

> **Model:** This path is for when you know what you want but not the exact steps. You'll give the agent system a goal — a concrete deliverable it produces each run — plus the rules it has to follow. Let's start with the situation: what's going on, what kicks this off, and what are you trying to get done?
>
> **You:** We sell AI training programs and I spend hours every week hunting for prospects. Honestly the goal is more revenue.
>
> **Model:** More revenue is the business objective — I'll record that. The agent's goal needs to be the *thing it hands you* that contributes to it. When a run works well, what do you walk away with?
>
> **You:** A list of prospects worth reaching out to.
>
> **Model:** So the goal is roughly: a ranked list of about 20 qualified prospects matching your ideal customer profile — with name, role, company, contact info, and a one-line reason they fit — delivered as a spreadsheet every Monday. A run is done when the list is ranked and every row has those fields. Did I get that right, or what's off?
>
> **You:** Yes — and they should be people we haven't contacted before.
>
> **Model:** Good constraint, noted. One more test: describe a list that *looks* fine but you'd send back. What's wrong with it?
>
> **You:** Probably one full of big-company executives we'd never close — right titles, wrong company size.
>
> **Model:** That's an acceptance criterion — company size fits your ICP. This works as goal-driven because finding prospects takes different steps depending on the week. What's the range it needs to handle — a typical week, and the harder ones?

From there, the model continues through inputs, rules, fallback behavior (what to do when a source is unreachable), context sources, and human gates — building a goal-driven Workflow Requirements without decomposing into fixed steps.

### Example: Starting with a problem

You don't need an existing process. If you have a gap or pain point, describe that — the model proposes a candidate workflow, then asks which of the two paths fits:

> **Model:** Tell me about the situation — what's going on, and what are you trying to get done?
>
> **You:** Neither, really. People sign up for my online course but a lot of them never finish. I have no way to know who's dropping off or how to follow up.
>
> **Model:** That's a gap, not a process. Let me propose a candidate workflow: (1) detect drop-offs by polling course completion data, (2) classify the drop-off reason, (3) draft a personalized follow-up message, (4) send it. Sound roughly right?
>
> **You:** Yes, that's the shape of it.
>
> **Model:** Good. Two paths from here: do you want to refine these steps with me (step-driven), or describe the goal and let an agent figure out the steps (goal-driven)?

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
- **Competitive analysis pipeline** (goal-driven) — you know what the deliverable looks like but want an agent system to determine the research approach

You don't need to know all the steps before you start — that's what the skill helps you figure out. Even "I onboard new clients and it takes forever" is enough to begin.

## What the Skill Produces

The **Workflow Requirements** document uses a shared structure for both paths — only the middle "what does the workflow do" block differs. Every section is structured so Design (or any agent model) can parse it without re-asking questions.

**Shared sections (both paths):**

- **Goal** — what a successful run produces, when it runs, who consumes it
- **Value & Measurement** — why the workflow is worth building and how you would know it worked: the business objective it supports, the outcome that changes and for whom, what gets counted, today's number, and the target the revised workflow should hit
- **Metadata** — workflow name, trigger, owner, lens (Individual / Organizational), Definition Type (Step-Driven / Goal-Driven)
- **Context Inventory** — every artifact the workflow needs, with stable IDs (C1, C2, …), status (Exists / Needs Creation), how sensitive it is (**Public** — a published price list; **Internal** — a project tracker; **Confidential** — an unannounced roadmap; **Regulated** — anything covered by a rule such as patient records or EU customer data), where it came from (**Authored** by someone on your team, or **External** — it arrived from outside), AI accessibility (Yes / Partial / No), and location
- **Acceptance Criteria** — numbered yes/no statements (`AC1…`), the one or two marked **(must)**, and the real example they were derived from
- **Example Scenarios** — 3-5 representative inputs with what to look for in the output, plus optional **Golden Examples** — real past outputs you'd consider "exactly right." These feed Step 5 (Test), where checking against a known-good reference beats gut feel
- **Rules & Constraints** — how the work should be done: must-do, must-never-do, scope boundaries, tone, format, length, and fallback behavior when a case can't be confidently completed, each with an ID (`R1…`)
- **Human Gates** — where human review or input is required, each with an ID (`G1…`)
- **Security, Privacy & Safety** — what the workflow must protect: where data may and may not travel, who may see the outputs, what has to be recorded, what it must never do, and which regulation applies. Every constraint names its source
- **Optimization Notes** (optional, step-driven only) — what changed from the original process and why

**Step-driven middle block:**

- **Steps Overview** — a scannable numbered list, one line per step
- **Step Details** — each step captured as **Goal / Inputs / Outputs / Rules & Edge Cases / Context Needed**, plus a **Role** field when the workflow uses the Organizational lens (to capture which role owns each step)
- **Sequence** — sequential vs. parallel steps, critical path, role swimlane

Most step-driven workflows expand from 5-8 rough steps to 12-20 refined steps after the deep dive.

**Goal-driven middle block:**

- **Inputs** — what the agent system receives to start (data, materials, references, access)

Goal-driven workflows **don't** capture capability domains, agent count, or orchestration approach — those are Design decisions. Step 2 stays in "what" territory.

### Three things the skill asks about that are easy to skip

**What the workflow is worth.** Before mapping anything, the skill asks four questions: which business objective this supports, what actually changes and for whom, what you would count, and what that number is today. That last one matters more than it looks. Without today's number you can claim an improvement but never show one — and the honest answer is often "I don't know," which the skill records as `Unknown — must measure before go-live` rather than pressing you for a guess. An invented starting number is worse than none, because it makes a false improvement look provable. After the workflow has been redesigned, the skill comes back for the target: what the new number should be.

**What the workflow must protect.** Most workflows need nothing here, and the skill is built so those finish in one line. It works out whether the question applies rather than asking you a form: as it rolls up the Context Inventory, it already knows how sensitive each artifact is and whether your team wrote it. So it asks you only one thing — *does this write to anything live?* If nothing is flagged, the section reads "No sensitivity constraints" and you move on.

When something is flagged, it captures five kinds of constraint: where data may and may not travel, who may see the results, what has to be logged, what the workflow must never do, and which regulation applies. Each one records who said it — a person, a policy, a control number — because a constraint nobody can trace is one the first objection wins.

Two distinctions worth knowing, because they decide where a fact belongs:

- **Where something came from is not the same as how secret it is.** A public web page is not sensitive, but nobody on your team wrote it — and content from outside can contain instructions. A model that treats them as instructions does what a stranger told it to. A draft pricing memo is the opposite: highly sensitive, but you wrote it.
- **A prohibition is absolute; a gate is conditional.** "Never email a customer without approval" is a gate — it happens once someone approves. "Never email a customer" is a prohibition — it never happens, whoever asks. If an approval can satisfy it, it is a Human Gate.

**How you'll judge the output.** The last chapter asks for a recent output you were happy with, then turns it into numbered yes/no statements — "every row has contact info", "I could send this without editing the wording" — plus 3–5 realistic inputs to try. These are not paperwork: in [Test (Step 5)](../test/) every statement becomes a row on a report card, checked against every input, met or not met with evidence. Writing them here, while the work is fresh, is what makes Test a checklist instead of a gut feel.

### Why this format

The Workflow Requirements reads like a PRD, not an interview transcript:

- **Requirements voice** — each line states what must be true, not what the user said in conversation
- **Fixed structure** — same section headings every time, so downstream skills (Design, Test, Improve) can locate any requirement by path
- **Stable IDs** — steps are numbered, context items are `C1, C2, C3, …`, scenarios are `E1, E2, E3, …`, acceptance criteria `AC1…`, rules `R1…`, human gates `G1…`
- **Tables for lists of items with shared fields** — easier to parse than prose
- **No interview residue** — no "the user mentioned", "usually", or other narrative

### Process optimization (step-driven only)

For step-driven workflows, the skill includes an **Optimize for AI** pass after the deep dive. Once the full process is mapped, the model steps back and challenges it — looking for steps that exist only because a human was doing the work (an integration eliminates the manual transfer), steps that can be collapsed (AI drafts and formats in one pass), steps that can be parallelized (no data dependency), handoffs that can be simplified, and new steps needed for the AI version. These are presented as recommendations for you to accept or reject — you may have good reasons to keep steps as-is (compliance, audit trail, stakeholder expectations). The Workflow Requirements records what changed and why.

### Workflow validation (step-driven only)

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
Once the name is confirmed, the skill creates a folder for the workflow — `outputs/[name]/` — and a Workflow node for it in your `registry/` bundle. The node tracks which framework step you're on and where every artifact lives, so any later session (or any framework skill) can pick up exactly where you left off. `outputs/` stays the home for the artifacts themselves; your registry becomes your workflow inventory — no separate tracking system required.
:::

## Related

- **Previous step:** Not sure which workflow to deconstruct? Start with [Analyze Workflows](../analyze/) (Step 1) to identify your best candidates.
- **Next step:** Ready to design? Go to [Design Your AI Workflow](../design/) (Step 3) — assess autonomy, choose an orchestration mechanism, and map building blocks.
- [AI Workflow Framework](../) — the full seven-step methodology
- [Prompts](../../agentic-building-blocks/prompts/)
- [Agents](../../agentic-building-blocks/agents/)
