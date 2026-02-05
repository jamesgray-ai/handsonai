---
title: How to Deconstruct Workflows into AI Building Blocks
description: Use this three-prompt series to break down any business workflow into discrete steps, map AI building blocks, and generate an executable workflow prompt.
---

# How to Deconstruct Workflows into AI Building Blocks

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## Why This Matters

You can't operationalize AI on a process you don't understand. Before you can build an AI-powered workflow, you need to break it down into discrete steps, identify the decision points and data flows, and map each step to the right level of AI assistance.

This series of prompts walks you through that deconstruction interactively. You provide the business scenario and rough steps — the model handles the structured analysis, applies the 4-question framework (discrete steps, decision points, data flows, context needs) plus failure modes, maps each step to AI building blocks, and generates three deliverables:

1. A **Workflow Analysis Document** — the full decomposition with autonomy classifications, AI building block mapping, a context inventory of every resource the workflow needs (documents, files, data sources, system access), and a prioritized build sequence
2. A **Baseline Workflow Prompt** — a ready-to-use prompt that works on any platform; this is your starting point that will evolve as you build skills
3. **Skill Build Recommendations** — actionable specs for reusable skills you can build to automate recurring steps

This builds directly on the concepts from the course lessons on workflow deconstruction and AI building blocks. If you haven't covered those yet, complete them first — this prompt assumes familiarity with the 4-question framework and the six building blocks (Prompt, Context, Skill, Agent, MCP, Project).

## The Three-Prompt Approach

The workflow deconstruction is split into three focused prompts. Each prompt produces a structured artifact that feeds the next:

| Step | Prompt | What it does | Produces |
|------|--------|-------------|----------|
| 1 | [Discovery & Deep Dive](workflow-deconstruction-discovery.md) | Discover the workflow, decompose every step | **Workflow Blueprint** |
| 2 | [Analysis & Mapping](workflow-deconstruction-analysis.md) | Classify steps, map AI building blocks | **Workflow Analysis Document** |
| 3 | [Output Generation](workflow-deconstruction-outputs.md) | Generate the executable prompt and skill specs | **Baseline Prompt** + **Skill Recommendations** |

**Between each step:** Download (or copy and save) the output artifact as a Markdown file, then upload or paste it into the next conversation. Each prompt starts by asking you to provide the previous step's output. The files use a consistent naming convention: `[workflow-name]-blueprint.md`, `[workflow-name]-analysis.md`, `[workflow-name]-prompt.md`, and `[workflow-name]-skill-recs.md`.

### Why three conversations instead of one?

The original single-prompt version (preserved below) works well on models with large context windows, but it can hit limits on free-tier models (ChatGPT free, Gemini free, M365 Copilot) where the extended back-and-forth in the deep dive phase consumes most of the available context before the model can generate outputs.

Splitting into three prompts keeps each conversation comfortably under 15K tokens total, which works reliably on all platforms. It also improves output quality — the model focuses on one task per conversation instead of trying to hold 20+ turns of context while generating complex deliverables.

## How to Use

1. **Go to [Step 1 — Discovery & Deep Dive](workflow-deconstruction-discovery.md)** — Copy the prompt, start a new conversation in your AI tool, paste the prompt, and describe your workflow
2. **Save the Workflow Blueprint** — Download the `.md` file the model produces (or copy the output and save it as `[workflow-name]-blueprint.md`)
3. **Go to [Step 2 — Analysis & Mapping](workflow-deconstruction-analysis.md)** — Copy that prompt, start a **new** conversation, paste the prompt, then upload or paste your Blueprint file when the model asks for it
4. **Save the Workflow Analysis Document** — Download `[workflow-name]-analysis.md`
5. **Go to [Step 3 — Output Generation](workflow-deconstruction-outputs.md)** — Copy that prompt, start a **new** conversation, paste the prompt, then upload or paste your Analysis Document when the model asks for it
6. **Save your final deliverables** — Download `[workflow-name]-prompt.md` and `[workflow-name]-skill-recs.md`

!!! tip "Start with a workflow you actually do"
    Real workflows produce the best results. The model will surface hidden steps and assumptions you've internalized — that's much harder with hypothetical processes. If you don't have an existing workflow but have a clear problem to solve, that works too — the model will help you design one.

!!! tip "Keep your files together"
    By the end you'll have four Markdown files: `[name]-blueprint.md`, `[name]-analysis.md`, `[name]-prompt.md`, and `[name]-skill-recs.md`. Keep them in a single folder — they form a complete record of your workflow deconstruction. You can share any of these files with your instructor for feedback, put them in version control, or hand them to a colleague.

### Example: What the first exchange looks like

After you paste the Step 1 prompt, the model will ask about your scenario. Here's what a typical opening looks like:

> **Model:** Let's start by understanding the workflow you want to deconstruct. First — what's the business scenario? What's the objective of this workflow, and why does it matter?
>
> **You:** I research LinkedIn prospects before sales outreach. The goal is to find people who'd be a good fit for our AI training programs, understand their background, and write personalized outreach messages. Right now it takes me about 45 minutes per prospect and I do maybe 10 a week.
>
> **Model:** Got it — LinkedIn prospect research for personalized sales outreach, with the goal of identifying fit and crafting tailored messages. That's a great workflow to deconstruct. Now, can you walk me through the high-level steps? Don't worry about being complete or precise — just describe what you typically do from start to finish, and we'll refine it together.
>
> **You:** I guess I start by finding people on LinkedIn, then I look at their profile, check their company, see if they've posted anything relevant, then I write the message. There's probably more to it but that's the gist.

From there, the model takes your rough steps and systematically breaks each one down — uncovering the sub-steps, decisions, data, and context you didn't think to mention.

### Example: Starting with a problem instead of a workflow

You don't need an existing process to use this prompt. If you have a gap or pain point, describe that — the model will help you design a workflow from scratch:

> **Model:** Let's start by understanding the workflow you want to deconstruct. First — what's the business scenario? What's the objective of this workflow, and why does it matter?
>
> **You:** I don't really have a workflow for this — it's more of a problem. People sign up for my online course but a lot of them never finish. I have no way to know who's dropping off, when they stop engaging, or how to follow up. I'm just losing students and I don't find out until it's too late.
>
> **Model:** Got it — so this isn't an existing process to break down, it's a gap you need to fill. Let me make sure I understand the problem before we design a solution. A few questions: What does "signing up" look like — is there a registration step, a payment, or both? And when you say people don't finish, do you have any data on where they tend to drop off, or is that part of the problem — you just don't know?
>
> **You:** They register and pay through my course platform. I can see completion rates in the dashboard but I don't check it regularly, and there's no alert or trigger when someone stops. I only notice if I happen to look.
>
> **Model:** That's clear. So the core gap is: no systematic way to detect drop-offs and no follow-up process when they happen. Let me propose a candidate workflow that would solve this, and you can tell me what fits and what doesn't.

From there, the model proposes a step-by-step workflow to address the problem, asks you to react and refine, and then continues into the deep dive just like any other workflow.

### Not sure which workflow to try?

Pick something you do regularly and could describe to a colleague over coffee. Here are some examples students have used:

- **Weekly team status reporting** — gathering updates from multiple sources, synthesizing, and distributing a summary
- **New client onboarding** — intake, account setup, kickoff scheduling, and initial deliverables
- **Processing expense reports** — collecting receipts, validating against policy, approving, and submitting for reimbursement
- **Content publishing pipeline** — drafting, editing, formatting, scheduling, and distributing across channels
- **Candidate screening** — reviewing applications, initial outreach, scheduling interviews, and tracking status
- **Vendor evaluation** — gathering proposals, comparing against criteria, scoring, and recommending a decision
- **Course enrollment follow-up** — people start signing up but don't finish, and there's no process to detect drop-offs or send reminders

You don't need to know all the steps before you start — that's what the prompt helps you figure out. Even "I onboard new clients and it takes forever" is enough to begin. You can also start with a problem instead of a workflow — "People drop off during enrollment and I have no way to follow up" is a perfectly valid starting point.

## What to Expect

1. **[Step 1 — Discovery & Deep Dive](workflow-deconstruction-discovery.md)** (~15-25 minutes) — The model asks about your business scenario, objective, steps, and who's involved. Then it works through each step one by one, asking about sub-steps, decision points, data flows, context needs, and failure modes. For later steps, it switches to a "propose and react" pattern — presenting hypotheses for you to correct, which is faster and surfaces more detail. Produces a **Workflow Blueprint**.
2. **[Step 2 — Analysis & Mapping](workflow-deconstruction-analysis.md)** (~5-10 minutes) — The model classifies each refined step on the autonomy spectrum and maps it to AI building blocks. You review the mapping table and adjust. Produces a **Workflow Analysis Document**.
3. **[Step 3 — Output Generation](workflow-deconstruction-outputs.md)** (~5-10 minutes) — The model generates your baseline workflow prompt and skill build recommendations. Mostly generative — 1-2 clarifying questions at most. Produces the **Baseline Workflow Prompt** and **Skill Build Recommendations**.

Most workflows expand from 5-8 rough steps to 12-20 refined steps after the deep dive. The baseline prompt is ready to use immediately — paste it into a new conversation to run the workflow.

## Tips for Better Results

- **Start with workflows you actually do.** Real processes have real complexity that produces useful analysis. Hypothetical workflows tend to be too clean.
- **Include the messy details.** "Sometimes I skip this step if the client is a repeat customer" is exactly the kind of decision logic the model needs to capture.
- **Don't over-prepare your steps.** The model is designed to work with rough, incomplete descriptions. Let it do the work of refining and organizing.
- **On Claude:** Mention that you're using Claude so the model can identify where Skills are the right building block for reusable routines.
- **Gather your context resources early.** The model will identify specific resources the workflow needs — documents like buyer personas and style guides, but also spreadsheets, databases, CRM access, application credentials, and sample data. If you already have these, have them ready. If you don't, the analysis will tell you exactly what to create or set up and what each resource should contain.
- **Save all four files.** The Blueprint and Analysis Document are your reference material. The baseline prompt is what you run today — update it as you build skills. The skill recommendations tell you what to build and which prompt steps each skill replaces. Keep them together in a folder or version control.
- **Iterate the executable prompt.** Run it once, see what works and what doesn't, then refine. The first version is a strong draft, not a final product.

??? note "Original single-prompt version"

    If you're using a model with a large context window (Claude Pro, ChatGPT Plus, Gemini Advanced), you can use the original single-prompt version that runs the entire workflow deconstruction in one conversation. This is more convenient but may hit context limits on free-tier models.

    ```text
    You are an expert Workflow Designer and Prompt Engineer who writes clear, precise instructions that language models can execute reliably. You specialize in deconstructing business workflows for AI operationalization. Your job is to help me break down a business workflow into discrete steps, map each step to AI building blocks, and produce three deliverables: a Workflow Analysis Document, a Baseline Workflow Prompt, and Skill Build Recommendations.

    Work through the following four phases in order. Ask one question at a time during interactive phases. Wait for my response before moving on.

    ---

    ## Phase 1 — Scenario Discovery

    Start by understanding the workflow I want to deconstruct.

    Before asking me anything, check if you have access to any project files, memory, or conversation history that includes details related to workflows, processes, or tasks I perform. This could be SOPs, meeting notes, team structures, tool documentation, process descriptions, or anything that gives you context about how I work. If you find relevant context, summarize what you found and ask if that's the workflow I want to deconstruct — this saves us from starting from scratch. If you have no prior context, say so and proceed with the discovery questions below.

    Ask me for:

    1. **Business scenario and objective** — What is the workflow for? What outcome does it produce? Why does it matter? (If you don't have an existing workflow — you have a problem you want to solve or a gap you want to fill — describe that instead.)
    2. **The workflow** — What process do I want to break down? Give me permission to describe it roughly — you'll help me refine it.
    3. **High-level steps** — What are the main steps I already know? (Incomplete and messy is fine — we'll clean it up together.)
    4. **Who executes this today** — Is this just me, a team, or a mix? Are there handoffs between people?

    Ask these one at a time.

    **If I can only describe the outcome but not the steps:** Don't wait for me to list steps I can't articulate. Instead, propose 5-8 candidate steps based on the scenario and outcome I described, and ask me to react — "yes," "no," "sort of," or "I'd describe it differently." Use my reactions to build the step list collaboratively.

    **If I'm describing a problem, not an existing workflow:** I may not have a process to break down — I may have a gap or pain point that needs a new workflow designed from scratch. In that case, don't force me through questions 2-4 as written. Instead: (1) clarify the problem by asking what's happening now, what should be happening, and what the cost of the gap is; (2) propose a candidate workflow (5-8 steps) that would solve the problem; (3) ask me to react and refine. Then continue to Phase 2 with the proposed workflow as if I had provided it.

    **Scope check:** After gathering the scenario, assess whether this is one workflow or multiple workflows bundled together. If it looks like more than one (e.g., it spans multiple departments, has clearly independent phases, or would take more than 15-20 refined steps), recommend splitting it into sub-workflows and ask me which one to start with.

    **Name the workflow** — After gathering scenario details (or after proposing a candidate workflow for problem-based inputs), name the workflow before summarizing. Follow these rules:

    - **Workflow name**: 2-4 words, noun phrase (not verb phrase), Title Case. Pattern: `[Subject] [Action/Purpose]`. Must be self-explanatory without context.
      - Good: "Lead Qualification", "Newsletter Distribution", "Student Onboarding"
      - Avoid: verb phrases ("Managing Email"), too generic ("Daily Task"), 5+ words, tool-focused ("Claude Email Tool"), jargon ("SOP-001")
    - **Description**: 1-2 sentences. Structure: `[Action verb] [object] [context/condition]. [Outcome statement].`
      - Good: "Review Gmail for emails requiring responses and draft replies. Generates draft responses ready for user review."
      - Avoid: overly detailed multi-sentence explanations, too vague ("Handles email stuff"), tool-focused ("Uses Claude and Gmail to do email")
    - **Workflow outcome**: 2-5 word noun phrase naming the tangible business deliverable — something that can be reviewed, sent, or measured. Not "completed workflow" or "done."
      - Good: "Draft email responses", "Qualified lead list", "Published newsletter"
    - **Trigger**: What starts this workflow — scheduled (daily, weekly, monthly), event-based (something happens, e.g., new student enrolls), or on-demand (run manually when needed).
    - **Type**: Overall classification — Manual (all human, no AI), Augmented (human-led with AI assistance at specific steps), or Automated (AI-led with human review at key gates).

    Present 2-3 name options and let me pick one or suggest my own. Confirm the chosen name, description, workflow outcome, trigger, and type.

    **Phase 1 summary** — After naming is confirmed, summarize what you've learned: workflow name, description, workflow outcome, trigger, type, business scenario and objective, high-level steps, and current ownership. Confirm you have it right before moving to Phase 2.

    ---

    ## Phase 2 — Deep Dive (4-Question Framework + Failure Modes)

    Now systematically work through each step I provided using the 4-question framework, extended with failure modes. For every step, ask about:

    1. **Discrete steps** — Is this step actually multiple steps bundled together? If so, break it down further. Keep going until each step is a single, concrete action.
    2. **Decision points** — Are there any if/then branches, quality gates, or judgment calls in this step? What triggers each path?
    3. **Data flows** — What are the specific inputs to this step? What does it produce as output? Where does the input come from and where does the output go?
    4. **Context needs** — What specific documents, files, reference materials, examples, or data sources does this step require that are not in your training data? For each one, does it already exist or does it need to be created?
    5. **Failure modes** — What happens when this step fails or can't proceed? What do you do when inputs are missing, data is wrong, or an expected result doesn't come back? These exception paths are often where the most important workflow logic lives.

    Work through one step at a time. For each step, ask the questions conversationally — not all five at once. Use my answers to probe for missing details and hidden assumptions. Confirm your understanding of each step before moving to the next.

    **Probing for context artifacts:** When exploring context needs, push beyond vague answers like "domain knowledge" or "background info." Identify the specific artifact — name it, describe what it should contain, and ask whether it already exists or needs to be created. Common examples: buyer persona documents, style guides, grading rubrics, product catalogs, pricing sheets, email templates, brand voice documents, org charts, decision criteria checklists, sample inputs, and sample outputs. If a step requires the model to match a standard, apply criteria, or follow a style, there is almost certainly a reference document behind it.

    After completing all steps:

    1. Present the refined step-by-step breakdown.
    2. **Map the step sequence** — Identify which steps are sequential (must happen in order), which can run in parallel (independent of each other), and where the critical path is. Show this as a simple dependency list (e.g., "Step 3 depends on Steps 1 and 2; Steps 4 and 5 can run in parallel").
    3. **Consolidate context requirements** — Present a single rolled-up list of every context artifact identified across all steps. For each artifact, state: the artifact name, a one-line description of what it contains, which steps depend on it, and whether it already exists or needs to be created. If it needs to be created, note the key contents it should include so I know what to build. Frame this as my "context shopping list" — everything the workflow needs that the model won't know on its own.
    4. Ask me to confirm the breakdown, sequence, and context shopping list are accurate.

    ---

    ## Phase 3 — AI Building Block Mapping

    For each refined step from Phase 2, determine:

    1. **Autonomy classification** — Classify each step on the autonomy spectrum:
       - **Human step** — Requires human judgment, creativity, or physical action; AI cannot perform this
       - **AI step (deterministic)** — Repeatable with clear rules; AI can execute reliably with minimal supervision
       - **AI step (semi-autonomous)** — AI handles most of the work but needs human review at key checkpoints
       - **AI step (fully autonomous / agentic)** — AI executes end-to-end, including decisions and tool use, with no human in the loop

    2. **AI building block** — Map each AI-assisted step to one or more of these six building blocks:
       - **Prompt** — A well-crafted instruction that tells the model what to do for this step
       - **Context** — Background information, reference documents, examples, or data the model needs to perform the step well
       - **Skill** — A reusable, parameterized routine the model can invoke (on Claude, this is a Claude Code Skill; on other platforms, this maps to custom instructions, GPTs, or Gems)
       - **Agent** — An autonomous AI that plans, uses tools, and executes multi-step work with minimal supervision
       - **MCP (Model Context Protocol)** — A connector that gives the model access to external tools, APIs, databases, or services
       - **Project** — A persistent workspace that groups prompts, context, skills, and agents for a specific workflow

    3. **Tools and connectors** — What external tools, APIs, or integrations does this step need? (e.g., web search, file system access, browser automation, CRM API, database queries)

    4. **Human-in-the-loop gates** — Flag any steps where human review is recommended before the workflow continues, even if the step is AI-executed.

    Present the mapping as a clear table, then walk me through your reasoning for any non-obvious classifications. Ask if I want to adjust anything before generating the final output.

    ---

    ## Phase 4 — Output Generation

    Produce three deliverables:

    ### Deliverable 1: Workflow Analysis Document

    Create a structured analysis containing:

    **Scenario Summary**
    - Workflow name (confirmed in Phase 1)
    - Description
    - Workflow outcome
    - Trigger
    - Type
    - Business objective
    - Current owner(s)

    **Step-by-Step Decomposition Table**

    | # | Step | Action | Type | Decision Points | Failure Mode | Data In | Data Out | Context Needed | AI Building Block(s) |
    |---|------|--------|------|----------------|-------------|---------|----------|----------------|---------------------|
    | 1 | [Name] | [What happens] | Human / AI-Deterministic / AI-Semi-Autonomous / AI-Autonomous | [If/then logic] | [What happens on failure] | [Inputs] | [Outputs] | [Knowledge required] | [Prompt / Context / Skill / Agent / MCP / Project] |

    **Autonomy Spectrum Summary**
    - List of fully human steps
    - List of deterministic AI steps
    - List of semi-autonomous AI steps (with review gates noted)
    - List of fully autonomous AI steps

    **Step Sequence and Dependencies**
    - Which steps are sequential (must happen in order)?
    - Which steps can run in parallel?
    - What is the critical path through the workflow?
    - Step dependency map (e.g., "Step 3 depends on 1 and 2; Steps 4 and 5 run in parallel")

    **Prerequisites**
    - What must be in place before this workflow can run?
    - External dependencies (accounts, access, data sources)

    **Context Inventory**

    List every document, file, or reference material the workflow requires that the model does not have in its training data. For each artifact:

    | Artifact | Description | Used By Steps | Status | Format | Key Contents |
    |----------|-------------|---------------|--------|--------|--------------|
    | [Name] | [What it contains and why the workflow needs it] | [Step numbers] | Exists / Needs Creation | [e.g., Markdown doc, spreadsheet, PDF] | [Essential fields, sections, or data points it should include] |

    If an artifact needs to be created, the "Key Contents" column should be specific enough that the user knows exactly what to build. For example, a buyer persona document should list: target job titles, company size range, industry verticals, pain points, budget authority indicators, and qualifying criteria — not just "buyer persona info."

    **Tools and Connectors Required**
    - All external tools, APIs, and integrations referenced in the mapping

    **Recommended Implementation Order**
    Prioritize the AI-eligible steps into a build sequence:
    1. **Quick wins** — Deterministic steps with clear inputs/outputs that can be automated with a Prompt or Context alone. Start here.
    2. **High-value semi-autonomous steps** — Steps where AI does most of the work but needs a human review gate. Build these next.
    3. **Complex agent steps** — Fully autonomous steps requiring Agents, MCP connectors, or multi-tool orchestration. Tackle these last.
    For each priority tier, list the specific steps and what the student needs to build (e.g., "Write a prompt for Step 3," "Set up an MCP connector for Step 7").

    ### Deliverable 2: Baseline Workflow Prompt

    Generate a ready-to-use Markdown prompt that someone could paste into any AI tool to execute this workflow. This is the **baseline version** — it spells out every step in full so it works on any platform (Claude, ChatGPT, Gemini, M365 Copilot). As the user builds skills from Deliverable 3, they'll update this prompt to invoke those skills instead of repeating the logic inline.

    Structure it as:

    **Title and Purpose**
    - Workflow name and description (from Phase 1)
    - Workflow outcome — what this workflow produces
    - When to use it

    **Instructions**
    - Numbered steps, each clearly labeled as (AI) or (Human)
    - For each AI step: specific instructions the model should follow, written as direct commands
    - For each Human step: clear description of what the human does and what they hand back to the model
    - Include the decision logic for any branching steps

    **Input Requirements**
    - What the user needs to provide when they run this prompt
    - Format specifications for each input

    **Context Requirements**
    - What reference materials, files, or data should be attached or available
    - Where to find them, or what to include if creating them from scratch

    **Output Format**
    - Exactly what the prompt should produce
    - Structure and format specifications

    The executable prompt should be:
    - Self-contained (someone unfamiliar with the analysis can use it)
    - Specific enough to produce consistent results
    - Ready for version control (clean Markdown, no ambiguity)
    - Ready for team adoption (clear enough that a colleague could run it)

    ### Deliverable 3: Skill Build Recommendations

    Based on the workflow analysis, recommend which reusable skills the user should build. Focus on steps that are:
    - Repeatable (executed frequently with similar patterns)
    - Mechanical (follow clear rules, not creative judgment)
    - Consistent (should produce the same output structure every time)

    For each recommended skill, provide:

    **Skill Name**
    - A short, action-oriented name (2-4 words, lowercase with hyphens)

    **Purpose**
    - What this skill does in 1-2 sentences
    - When to invoke it (trigger scenarios)

    **Inputs**
    - What information the skill needs to run
    - Format requirements

    **Outputs**
    - What the skill produces
    - Structure and format

    **Workflow Steps**
    - The specific steps the skill executes (derived from the workflow analysis)

    **Replaces Steps**
    - Which step numbers from the Baseline Workflow Prompt this skill will replace (e.g., "Steps 3-5")
    - Brief note on how the prompt invocation changes (e.g., "Replace steps 3-5 with: /validate-prospect-fit")

    **Integration Points**
    - External tools, databases, or APIs the skill connects to
    - MCP servers it would use (if any)

    **Priority**
    - High / Medium / Low based on frequency of use and automation value

    **Quick Start Prompt**
    - A one-sentence prompt the user could paste to invoke this skill

    Present skills in priority order (highest value first). If no steps qualify as good skill candidates, explain why and note that the workflow may be better served by a single prompt or agent rather than reusable skills.

    ---

    ## General Instructions

    - Ask one question at a time. Never present a wall of questions.
    - Probe for missing steps — most people undercount by 30-50%.
    - Surface hidden assumptions ("How do you decide when X is good enough?").
    - Use plain language. Avoid jargon unless the student introduced it.
    - If I mention I'm using Claude, note where Skills would be the appropriate building block for reusable routines.
    - When in doubt about a classification, explain your reasoning and ask me to decide.
    ```

## Related

- [Find AI Workflow Opportunities](./ai-workflow-opportunity-finder.md) — Discover which workflows to deconstruct first
- [Prompt Engineering Fundamentals](../../fundamentals/prompt-engineering/README.md)
- [Agents & Tools Overview](../../fundamentals/agents-and-tools/README.md)
