---
name: deconstruct
description: >
  This skill should be used when the user wants to deconstruct a workflow, break down a business
  process, capture requirements for an AI workflow, or define an outcome for an agent system.
  Step 2 is the PRD for the workflow — it captures what the workflow must do, the rules it must
  follow, and the edge cases it must handle, in clear requirements language suitable for the
  Design step or any AI model to consume. Supports two paths: step-decomposed (you know how the
  work gets done) and outcome-driven (you know what "done" looks like and want an agent system
  to determine the path). Produces a structured Workflow Requirements document.
  This is Step 2 of the AI Workflow Framework.
user-invocable: true
---

# Workflow Deconstruction

Step 2 is the **PRD for the workflow**. It captures *what* the workflow must do and the rules it must follow — not *how* AI building blocks will deliver it (that's Step 3, Design).

The output is a **Workflow Requirements** document written in clear, concise requirements language. It must be self-contained enough that a reader who never saw this conversation — including the Design skill or any agent model — can act on it without re-interviewing the user.

## The Two Paths

Step 2 has **two paths**, mapped directly to the two ways students think about a workflow:

| Path | When to use | Mental model |
|------|-------------|--------------|
| **Step-decomposed** | You can describe how the work gets done | "I know the steps" |
| **Outcome-driven** | You know what "done" looks like but the path varies; you want an agent system to figure it out at runtime | "I know the outcome" |

Both paths produce a Workflow Requirements document with the same shared shell — only the middle "what does the workflow do" block differs.

## Workflow

1. **Scenario discovery** — Determine how the user is arriving and which path to take.

   **From Analyze output**: If the user references an opportunity report, file path (e.g., `outputs/ai-opportunity-report.md`), or a specific workflow candidate from an Analyze session, read the Workflow Candidate Summary from the file. Present the available candidates and ask which one to deconstruct. Pre-populate scenario metadata (name, description, trigger, deliverable, autonomy, involvement) from the candidate fields. If the candidate includes a `Lens` field, carry it forward along with any `Business Objective`, `Stakeholders`, and `Success Metrics` fields. Confirm the pre-populated details with the user. Then choose the path: if the candidate's autonomy = Autonomous, suggest outcome-driven but still confirm. Otherwise present the choice below.

   **Cold entry (no Analyze output)**: Ask one question:

   > "Do you know the steps, or just the outcome?
   > - **Step-decomposed** — You can describe how the work gets done. I'll interview you to refine the steps and surface decision rules and edge cases.
   > - **Outcome-driven** — You know what "done" looks like but want an agent system to figure out the steps. I'll capture the outcome, inputs, acceptance criteria, and rules."

   **Problem-first handling (no separate path)**: If the user says they don't have a process *or* an outcome — just a problem ("People drop off during onboarding and I don't have a way to follow up") — propose a candidate workflow based on what they describe, then route into one of the two paths:
   > "Here's a candidate workflow that would solve this: [outline]. Do you want to refine these steps with me (step-decomposed), or just describe the outcome and let an agent figure out the steps (outcome-driven)?"

   **After the path is chosen, gather scenario details:**
   - **Step-decomposed**: Ask about the business scenario, objective, high-level steps, and ownership. One question at a time. If no lens was established, determine it: individual tasks (one person's repetitive work) = Individual lens; multi-role or business-objective processes = Organizational lens. Ask only if not obvious from context. Proceed to Step 2 (scope check) → Step 4 (deep dive).
   - **Outcome-driven**: Ask the user to describe the outcome — what should the agent system produce, what triggers the need, and who consumes the output. One question at a time. Proceed to Step 2 (scope check) → Step 4-OD (outcome-driven interview).

2. **Scope check — one trigger, one deliverable** — A workflow has exactly one trigger (what kicks it off) and one deliverable (the tangible output). Test for multiple workflows by checking:
   - **Triggers**: Multiple independent starting points? (e.g., "when a lead comes in" vs. "end of each week") → separate workflows
   - **Deliverables**: Distinct outputs at different points? If someone receives a deliverable midway and the process continues toward a different output → workflow boundary
   - **Timeframes**: Parts run on different schedules (daily vs. weekly), or significant waits between phases → likely separate workflows
   - **Step count**: Would this expand to 15+ refined steps? → may be multiple workflows
   - **Ownership boundary** (organizational lens): Does this process have a single accountable owner for the end-to-end outcome? If different people own different segments with no single owner, it may be multiple workflows.

   If multiple workflows are detected: map out each one (working name, trigger, deliverable), present the breakdown, confirm boundaries with the user, and ask which to deconstruct first. Proceed with only the chosen workflow.

3. **Name the workflow** — Present 2-3 name options following naming conventions (2-4 word noun phrase, Title Case). Confirm name, description, outcome, and trigger.

4. **Deep dive (step-decomposed only)** — Before probing the first step, briefly frame what "context" means: "As we go through each step, I'll ask about the *context* it needs. Context is any data or information the step requires to do its job — that includes databases and spreadsheets, but also documents, transcripts, emails, style guides, SOPs, or even knowledge that currently lives in someone's head. If the step needs it, it's context."

   Work through each step using the 6-question framework. These six dimensions are the **interview scaffold** — they shape what to ask, not how the spec is structured. Your job is to gather enough signal across all six to write the per-step requirements block (Goal / Inputs / Outputs / Rules & Edge Cases / Context Needed) in Step 10.

   - Discrete steps (is this actually multiple steps?)
   - Decision points (if/then branches, quality gates)
   - Data flows (inputs, outputs, sources, destinations)
   - Context needs (specific documents, files, reference materials)
   - Failure modes (what happens when this step fails)
   - Context readiness (adopt a data strategist lens for each step's context inputs):
     - Access: Where does this context live today? How do you access it — is it in a system with programmatic access (database, cloud app, shared drive), or does it require manual steps (logging in, copy-pasting, reading from a screen)?
     - Interpretability: Is the context in a format AI can process? (Structured: database tables, spreadsheets, JSON. Semi-structured: emails, documents with consistent formatting. Unstructured: handwritten notes, images, proprietary formats.)
     - Persistence: Does this context need to exist as a durable artifact that AI can access across workflow runs? If it's currently "in someone's head" or communicated verbally, flag that it needs to be externalized and stored somewhere AI-accessible.
     - Reorganization signal: If access, interpretability, or persistence is limited, flag that the context may need to be made more accessible or better organized — note this as a consideration for the Design step.
   - Role transitions (organizational lens with multiple stakeholders only) — Who performs this step? Does ownership change between steps? Are there handoff points?

   When probing context needs, push beyond vague answers — identify the specific artifact. For any step where AI is already being used, ask specifically for existing prompt instructions, project instructions, or system prompts — these contain workflow logic that must be included in the Baseline Prompt.

5. **Propose and react (step-decomposed only)** — After the first step of the deep dive, switch to propose-and-react: propose a hypothesis across all dimensions (including context readiness and role transitions for organizational workflows) and ask "What's right, what's wrong, what am I missing?" instead of asking each question individually. Include a context readiness hypothesis: "I think this context lives in [location] and is in [format] which AI can interpret. Is that right?"

6. **Map sequence (step-decomposed only)** — After all steps, identify sequential vs. parallel steps and the critical path.

7. **Optimize for AI (step-decomposed only)** — Now that the full process is mapped, step back and challenge it. The user described their *current* process — but an AI-powered version may not need every step. Present optimization recommendations for the user to react to. Look for:
   - **Eliminable steps** — Steps that exist only because a human was doing the work. Examples: manual data transfer between systems (an integration eliminates this), reformatting output from one step to match the input of the next (AI handles format natively), or "wait for X to be available" steps that become instant with API access.
   - **Collapsible steps** — Adjacent steps that AI can do in a single pass. Examples: separate "draft" and "format" steps, or "research" followed immediately by "summarize findings" — these are distinct for humans but one operation for AI.
   - **Parallelizable steps** — Steps that were sequential only because a human can do one thing at a time. If two steps have no data dependency, flag that AI can run them concurrently.
   - **Simplifiable handoffs** — Handoffs or review gates that exist because of human error rates, not genuine decision points. An AI quality check might replace a human review loop, or a multi-step approval chain might collapse to a single human gate on the final output.
   - **New steps needed** — Occasionally the AI version needs a step the human version didn't: a validation check, a data enrichment pass, or an explicit context-loading step that was implicit when a human just "knew" the background.

   **Present as a propose-and-react summary:**

   > "Now that we've mapped the full process, here's how I'd optimize it for AI:
   > - **Eliminate**: [step(s)] — [reason, e.g., 'direct access to your CRM data replaces the manual export']
   > - **Collapse**: [step(s)] into one — [reason, e.g., 'AI drafts and formats in a single pass']
   > - **Parallelize**: [step(s)] — [reason, e.g., 'no data dependency between these']
   > - **Simplify**: [handoff/gate] — [reason, e.g., 'AI evaluation replaces manual QA, human reviews final output only']
   > - **Add**: [new step] — [reason, e.g., 'need an explicit context-loading step for data the human carried in their head']
   >
   > These are recommendations — you may have reasons to keep steps as-is (compliance, audit trail, stakeholder expectations). What looks right, and what should stay?"

   Update the refined steps based on the user's confirmed optimizations. Renumber if steps were added, removed, or merged. If the user rejects all optimizations, that's fine — proceed with the original steps.

8. **Validate the workflow (step-decomposed only)** — Before consolidating context, walk through the refined workflow end-to-end and present a validation summary. This is the quality gate that catches gaps before the workflow moves to Design. Check for:
   - **Completeness** — Are there gaps in the end-to-end flow? Steps where an output doesn't connect to the next step's input?
   - **Logic gaps** — Decision points without clear criteria? Steps that assume information not produced by a prior step?
   - **Edge cases** — Scenarios the user hasn't mentioned (empty inputs, unexpected formats, partial data, exception paths)?
   - **Redundancy** — Steps that duplicate work or produce outputs no downstream step consumes?
   - **Handoff clarity** — For each step transition: is it clear what passes from one step to the next, and in what form?

   Present as a validation summary:

   > "Let me validate the workflow before we finalize it. Walking through the end-to-end flow, here's what I found:
   > - **[Finding type]**: [specific gap, e.g., 'Step 3 produces a draft but Step 4 expects a formatted document — is there an implicit formatting step?']
   > - **[Finding type]**: [specific gap]
   > - **No issues found in**: [dimensions that checked out]
   >
   > Which of these need to be addressed?"

   Update refined steps based on the user's responses. If no issues are found, say so and proceed.

9. **Consolidate context** — Present a rolled-up "context inventory" of every piece of context the workflow needs — documents, data, rules, examples, and any other knowledge from the user's domain that the model doesn't have.

   For step-decomposed workflows: assemble from per-step context needs gathered in Step 4. For outcome-driven workflows: assemble from the Inputs + Context Sources gathered in Step 4-OD.

10. **Collect Acceptance Criteria and Example Scenarios (both paths)** — Before generating the Workflow Requirements, ask the user about acceptance criteria and example scenarios. These were previously collected during Design's Step 8b; capturing them here makes Step 2 a complete PRD and removes redundant questioning downstream.

    Ask, one at a time:
    1. "What does great output from this workflow look like? Describe what would make you say 'this is exactly right.'"
    2. "Which dimensions matter most? For example: accuracy, completeness, tone, specificity, timeliness, format consistency."
    3. "What's your minimum bar — what's acceptable vs. what needs more work?"
    4. "Give me 3-5 real or realistic scenarios you'd run this on — different enough to test the workflow's range. For each, briefly describe the input and what you'd look for in the output."

    For outcome-driven workflows, these answers also inform the Acceptance Criteria built up in Step 4-OD — fold them together rather than asking twice.

11. **Generate Workflow Requirements** — Produce the structured Workflow Requirements document and write it to the output file. See the **Output** section below for the template, writing style, and machine-readability rules.

### Outcome-Driven Path (Step 4-OD)

When the user selects outcome-driven, run this interview instead of the step-decomposed deep dive (Steps 4–8). The outcome-driven path handles context discovery internally (question 7), so it skips straight to Step 9 (Consolidate Context) → Step 10 (Acceptance Criteria) → Step 11 (Generate) after the interview. Same interview principles apply: one question at a time, propose-and-react after the first few answers, push beyond vague answers.

1. **Outcome**: "What does a successful run produce? Describe the deliverable — format, structure, scope."
2. **Inputs**: "What does the agent system receive to start? What triggers the work, and what materials does it have access to?"
3. **Acceptance signals**: "What does the deliverable need to demonstrate to be considered 'good'? Examples or anti-examples are great here." (This feeds the Acceptance Criteria; Step 10 will sharpen it further.)
4. **Rules & Constraints**: "What boundaries or guardrails apply? Things the agent must always do, must never do, or limits on scope, sources, tone, length."
5. **Context & Data Sources**: "What external systems, data sources, documents, or reference materials should the agent system have access to?" Apply the same context readiness probing as the step-decomposed path:
   - Access: Where does this context live today? Is it in a system with programmatic access (database, cloud app, shared drive), or does it require manual steps (logging in, copy-pasting, reading from a screen)?
   - Interpretability: Is the context in a format AI can process?
   - Persistence: Does this context need to exist as a durable artifact that AI can access across workflow runs?
6. **Human gates**: "Where should the agent system pause for human review? Or run end-to-end with final review only?"
7. **Scope check**: Same one-trigger-one-deliverable test as Step 2 — confirm the outcome hasn't expanded into multiple workflows.

**Do NOT ask about capability domains, agent count, model class, tools, or orchestration approach.** Those are Design decisions. Outcome-driven Deconstruct stays in "what" territory: outcome, inputs, acceptance criteria, rules, context, human gates.

After completing the interview, proceed directly to Step 9 (Consolidate Context) → Step 10 (Acceptance Criteria) → Step 11 (Generate Workflow Requirements) using the outcome-driven output format.

## Output

Write the Workflow Requirements to `outputs/[workflow-name]-requirements.md` where `[workflow-name]` is the kebab-case workflow name (e.g., `lead-qualification` → `outputs/lead-qualification-requirements.md`).

### Writing-style rules (MUST follow)

The output reads like a PRD, not an interview transcript. Enforce:

- **Requirements voice.** Every bullet is a statement of what must be true, not a description of what the user said. Prefer "The step accepts a list of prospect URLs" or "Output is a Markdown table with one row per prospect" over "The user mentioned they usually have a list of URLs."
- **Active voice. Present tense.** "Validate the input against the rubric" — not "The input will then be validated."
- **One requirement per line.** Use bulleted lists, not paragraphs, anywhere multiple discrete requirements appear.
- **Concrete over abstract.** Name the artifact, the field, the threshold. "Reject submissions over 500 words" — not "Filter out long submissions."
- **No interview residue.** Drop hedges ("I think", "sometimes", "usually"), narrative connectors ("then the user", "after that"), and meta-commentary about the conversation ("we discussed", "you mentioned").
- **Self-contained.** A reader who never saw the deconstruct conversation can implement against the document.

### Machine-readability rules (MUST follow)

So Design (and any agent model) can parse the document without re-asking:

- **Fixed section headings**, in fixed order — use the exact headings in the template; no synonyms, no reordering.
- **Tables for any list of items with shared fields** (steps, context artifacts, example scenarios) — not prose.
- **Canonical vocabulary** for enumerated values:
  - Definition Type: `Step-Decomposed` or `Outcome-Driven`
  - Lens: `Individual` or `Organizational`
  - Context Status: `Exists` or `Needs Creation`
  - AI Accessible: `Yes`, `Partial`, or `No`
- **Stable IDs** — number steps `1, 2, 3, …`; ID context items `C1, C2, C3, …`; ID example scenarios `E1, E2, E3, …`. Downstream artifacts reference these IDs.
- **Explicit Inputs and Outputs per step** — even when "obvious." Design uses these to build the data-flow without guessing.

### Template — shared shell

```markdown
# [Workflow Name] — Workflow Requirements

## Outcome
[One paragraph: what a successful run produces, when it runs, who consumes the output.]

## Metadata

| Field | Value |
|---|---|
| Workflow Name | [name] |
| Description | [short description] |
| Trigger | [what kicks the workflow off] |
| Owner | [person or role] |
| Lens | Individual / Organizational |
| Definition Type | Step-Decomposed / Outcome-Driven |
| Business Objective | [why this workflow matters — optional but recommended] |

For organizational lens, also include:
| Stakeholders | [roles/teams involved] |
| Success Metrics | [KPIs for measuring improvement] |

---

[INSERT THE STEP-DECOMPOSED BLOCK OR THE OUTCOME-DRIVEN BLOCK HERE — see below]

---

## Context Inventory

| ID | Artifact | Used By | Status | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|
| C1 | [name] | [Step IDs or "All"] | Exists / Needs Creation | Yes / Partial / No | [path, URL, system name, or "Create as [path]"] | [what's in it] |

Notes:
- For items with `Status: Needs Creation`, the Location column captures where the artifact should be persisted — AI must be able to reach it.
- For organizational workflows, include existing process documentation here: SOPs, training guides, compliance requirements, SLAs.

## Acceptance Criteria

### What good output looks like
[Concrete description in plain language — what would make the user say "this is exactly right"?]

### Dimensions that matter
- [Dimension] — [what to evaluate]
- [Dimension] — [what to evaluate]

### Minimum bar
[What's acceptable vs. what needs more work — in plain terms, not a numeric threshold.]

## Example Scenarios

| ID | Scenario | Input | What to look for in the output |
|---|---|---|---|
| E1 | [short name] | [description] | [what makes this output "good"] |
| E2 | … | … | … |

## Human Gates

| Where | What requires human input |
|---|---|
| [step ID or phase] | [decision, approval, review] |

If no human gates are required, write: "No human gates — the workflow runs end-to-end with final review only."

## Optimization Notes (optional, step-decomposed only)
[Brief record of what changed from the original process and why — only if optimizations were applied in Step 7. Include declined optimizations and the reasoning, since this preserves context for Design.]
```

### Step-Decomposed middle block

Insert between the Metadata table and the Context Inventory:

```markdown
## Steps Overview

1. [Step name] — [one-line summary]
2. [Step name] — [one-line summary]
3. …

## Step Details

### Step 1 — [Step Name]
- **Goal:** [what this step achieves, one sentence]
- **Inputs:** [data/context coming in — name the artifact or reference a Context Inventory ID]
- **Outputs:** [what passes to the next step]
- **Rules & Edge Cases:**
  - [decision criterion or branch]
  - [what to do when an input is missing, malformed, or empty]
  - [quality threshold or exception path]
- **Context Needed:** [list of Context Inventory IDs the step depends on, e.g., C1, C3]
- **Role:** [who performs this step — organizational lens only]

### Step 2 — [Step Name]
… (same fields)

## Sequence

- **Sequential steps:** [list]
- **Parallel steps:** [list with grouping, e.g., "Steps 2 and 3 run in parallel"]
- **Critical path:** [longest dependency chain]
- **Role swimlane** (organizational lens only): [brief view of which role owns each step]
```

### Outcome-Driven middle block

Insert between the Metadata table and the Context Inventory (omit Steps Overview, Step Details, and Sequence — there is no fixed step sequence for outcome-driven workflows):

```markdown
## Inputs

- [What the agent system receives to start — data, materials, references, access]
- [One bullet per discrete input]

## Rules & Constraints

- **Must do:** [list]
- **Must never do:** [list]
- **Scope boundaries:** [what's in scope, what's out]
- **Tone / format / length:** [if applicable]
- **Source restrictions:** [if applicable]
```

The Outcome, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, and Human Gates sections from the shared shell still apply — outcome-driven uses the same shell, just a different middle.

## Guidelines

- Ask one question at a time — never present a wall of questions.
- Probe for missing steps — most people undercount by 30-50%.
- Surface hidden assumptions ("How do you decide when X is good enough?").
- Use plain language; avoid jargon unless the user introduced it.
- Push beyond vague context answers like "domain knowledge" — identify the specific artifact.
- Surface the assumption that existing context — data, documents, transcripts, reference materials — will "just work" for AI. Most people underestimate the work required to make context AI-accessible, especially unstructured content like SOPs, style guides, meeting transcripts, and knowledge that lives in people's heads. Adopt a data strategist lens — help the user see where context reorganization, reformatting, or externalization is needed before they commit to a workflow design that depends on inaccessible context. Push beyond "it's in the CRM" or "I just know it" — ask what system it's in, what format it's in, and whether there's programmatic access or it requires manual steps. Leave specific integration mechanisms (MCP, API, SDK) to the Design step.
- **Stay in the "what" lane.** Deconstruct defines the workflow, its context needs, its rules, and its acceptance criteria. It does not prescribe how AI will access data, which tools to use, what integrations to build, how many agents are needed, or which models to use — those are Design decisions (Step 3). Do not ask the user about capability domains, agent architecture, model class, or orchestration mechanism. If a technology concern surfaces, note it as a consideration for Design rather than resolving it here.
- After writing the Workflow Requirements file, tell the user: "Workflow Requirements saved to `outputs/[name]-requirements.md`. Ready for the `design` skill (Step 3)."
- If entering deconstruction without a prior analysis (direct workflow description), determine the lens by asking if not obvious from context.
- For outcome-driven workflows, do not force step decomposition — the whole point is to capture what the agent system needs to know without prescribing execution steps.
