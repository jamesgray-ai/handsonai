---
name: deconstruct
description: >
  This skill should be used when the user wants to deconstruct a workflow, break down a business
  process, define an outcome for an agent system, or deeply analyze a workflow's steps, decisions,
  data flows, and failure modes. Supports four entry paths: step-decomposed (6-question framework),
  problem-first, outcome-driven (for autonomous agent systems), or Compose — a lean three-turn flow
  that outputs an orchestration prompt directly when the user already has the skills/sub-agents in
  place. The first three paths produce a structured Workflow Definition; Compose produces only an
  orchestration prompt. This is Step 2 of the AI Workflow Framework.
user-invocable: true
---

# Workflow Deconstruction

Interactively discover a business workflow via one of four paths. The step-decomposed (6-question framework), problem-first, and outcome-driven paths all produce a structured Workflow Definition. The Compose path is the lean alternative: when the user already has the skills or sub-agents their workflow needs and can describe each step, Compose skips the deep dive and outputs an orchestration prompt directly in three turns — no Workflow Definition file.

## Workflow

1. **Scenario discovery** — Determine how the user is arriving and which path to take:

   **From Analyze output**: If the user references an opportunity report, file path (e.g., `outputs/ai-opportunity-report.md`), or a specific workflow candidate from an Analyze session, read the Workflow Candidate Summary from the file. Present the available candidates and ask which one to deconstruct. Pre-populate scenario metadata (name, description, trigger, deliverable, autonomy, involvement) from the candidate fields. If the candidate includes a `Lens` field, carry it forward along with any `Business Objective`, `Stakeholders`, and `Success Metrics` fields. Confirm the pre-populated details with the user. Then choose the path: if the candidate's autonomy = Autonomous, suggest option (c) but still confirm. Otherwise present the three choices below.

   **Cold entry (no Analyze output)**: Present three choices as the **first question**:

   > "How would you like to approach this?
   > (a) **Deconstruct a known process** — You can describe the steps and I'll interview you to surface hidden details
   > (b) **Start from a problem** — You know what's broken; I'll propose a workflow and we refine it together
   > (c) **Define an outcome** — You know what you want produced but want an agent system to figure out the approach
   > (d) **Compose** — You already have skills and/or sub-agents and know the workflow; I'll write the orchestration prompt directly"

   **After the user chooses, gather scenario details based on their path:**
   - **Option (a)**: Ask about the business scenario, objective, high-level steps, and ownership. One question at a time. If no lens was established, determine it: individual tasks (one person's repetitive work) = Individual lens; multi-role or business-objective processes = Organizational lens. If not obvious from context, ask. Proceed to Step 2 (scope check) → Step 4 (deep dive with 6-question framework).
   - **Option (b)**: Ask the user to describe what's broken. Propose a candidate workflow for them to react to. Then recommend whether step-decomposed or outcome-driven fits better, with reasoning. User confirms or overrides — honor their choice either way. If step-decomposed, proceed to Step 2 → Step 4. If outcome-driven, proceed to Step 2 → Step 4-OD.
   - **Option (c)**: Ask the user to describe the outcome they want — what should the agent system produce, what triggers the need, and who consumes the output. One question at a time. Proceed to Step 2 (scope check) → Step 4-OD (outcome-driven interview).
   - **Option (d) — Compose**: Proceed to the **Compose three-turn flow** (see Step 1c below). Do NOT call Step 2 (scope check) or Step 4 (deep dive); Compose handles its own lean intake inline and writes no Workflow Definition file.

**Step 1c — Compose three-turn flow (only reached from Option d):**

The Compose path is the **lean** path. No formal pre-flight, no Workflow Definition file, no `/design` invocation. The conversation captures what's needed, confirms it back, and outputs an orchestration prompt the student can run.

**Turn 1 — Intake.** Ask the student for everything in one message:

> "Tell me four things in one message:
> 1. **Workflow name and outcome** — what does this workflow produce?
> 2. **Where your components live** — Claude account (Claude.ai + Cowork), Claude Code, ChatGPT, or a mix?
> 3. **The steps** — numbered, one line each.
> 4. **Which component runs each step** — name and type (skill or sub-agent)."

If the student answers Turn 1 incompletely, ask only for the missing pieces in Turn 2 — do not restart.

**Turn 2 — Confirm + autonomy/involvement.** Restate what you heard in 5–8 lines: workflow name, hosting, steps, component-to-step mapping. Use ✓ when a component clearly fits its step; flag concerns inline (vague step, missing component, suspected mismatch) and ask for a quick fix.

If the workflow looks more complex than the Compose path is built for — 8+ steps, no components for half the steps, "etc." in step descriptions, or 3+ decision points the student didn't surface — say so directly and offer to switch:

> "This is more involved than the Compose path is built for — [specific reason]. The Known Process path (`/deconstruct` option a) will surface the gaps before they bite. Want to switch?"

Then ask the two questions that actually shape the prompt:

- *"Deterministic (fixed sequence, no AI judgment) or guided (the AI scores, evaluates, or adapts between steps)?"*
- *"Augmented (AI pauses for your input at any point) or automated (runs straight through)?"*

**Turn 3 — Output the orchestration prompt.** Generate the prompt in the standard shape below and return it as a code block the student can copy. Map the autonomy + involvement answers to one of four patterns:

- **Deterministic, automated** — components fire in sequence, no pauses, no AI judgment.
- **Deterministic, augmented** — same fixed sequence with a PAUSE for student review between named steps.
- **Guided, augmented** — scoring/evaluation/adaptation between steps, with a PAUSE for steering.
- **Guided, automated** — same decision logic, but the AI makes the bounded calls without pausing.

**Standard output shape:**

~~~markdown
---
workflow: <Workflow Name>
outcome: <one-sentence outcome>
autonomy: deterministic | guided
involvement: augmented | automated
components:
  - name: <name>
    type: skill       # used in step 1
  - name: <name>
    type: sub-agent   # used in step 2
---

# <Workflow Name>

## Intent
<one-paragraph "what this workflow does and when to run it">

## Prompt
<the orchestration prompt body>
~~~

**Prompt-body constraints — clarity, brevity, token efficiency:**

- One instruction per line where possible. Imperative voice. No filler ("please", "kindly", "make sure to").
- No re-explanation of what the components do — components have their own descriptions.
- No preamble or commentary. Open with the first instruction, not "In this workflow, we will…".
- PAUSE points are uppercase and unambiguous on their own line: `PAUSE — wait for me to confirm which insights to feature.`
- Reuse the student's own wording for inputs, outputs, and decision criteria. Avoid synthesizing new jargon.
- Inline tone or formatting guidance only when it changes the output (e.g., "narrative tone, not bullet-heavy"). Skip aesthetics.

**Component verification, hosting-aware:**

- **Claude Code (local files):** Read each named component's frontmatter (SKILL.md or agent file) under `.claude/skills/` and `.claude/agents/` (plus installed plugin caches). Confirm it exists, fits the step, and isn't an obvious mismatch. Mention an alternative only if you spot a clearly stronger match in the student's local inventory.
- **Claude account, ChatGPT, or mix:** You cannot introspect. Trust the student's mapping. Ask for clarification only if a component name sounds wrong for the step it's assigned to. If the student doesn't remember a component's name, ask them to paste their available components from wherever they're hosted.

**Saving the artifact:**

Tell the student to save the orchestration prompt wherever they keep prompts:
- Claude Code users: a `prompts/<workflow-name>.md` file in their project.
- Everyone else: a Google Doc, Notion page, Claude account project file, ChatGPT saved prompt, or plain note.

Do **not** write any file to `outputs/`. The Compose path produces conversation output only.

**End of Compose flow.** Do not hand off to `/design`, `/build`, `/test`, or `/run`. The student tests the workflow by running the prompt.

2. **Scope check — one trigger, one deliverable** — A workflow has exactly one trigger (what kicks it off) and one deliverable (the tangible output). Test for multiple workflows by checking:
   - **Triggers**: Multiple independent starting points? (e.g., "when a lead comes in" vs. "end of each week") → separate workflows
   - **Deliverables**: Distinct outputs at different points? If someone receives a deliverable midway and the process continues toward a different output → workflow boundary
   - **Timeframes**: Parts run on different schedules (daily vs. weekly), or significant waits between phases → likely separate workflows
   - **Step count**: Would this expand to 15+ refined steps? → may be multiple workflows
   - **Ownership boundary** (organizational lens): Does this process have a single accountable owner for the end-to-end outcome? If different people own different segments with no single owner, it may be multiple workflows.
   If multiple workflows are detected: map out each one (working name, trigger, deliverable), present the breakdown, confirm boundaries with the user, and ask which to deconstruct first. Proceed with only the chosen workflow.
3. **Name the workflow** — Present 2-3 name options following naming conventions (2-4 word noun phrase, Title Case). Confirm name, description, outcome, trigger, and type.
4. **Deep dive** — Before probing the first step, briefly frame what "context" means: "As we go through each step, I'll ask about the *context* it needs. Context is any data or information the step requires to do its job — that includes databases and spreadsheets, but also documents, transcripts, emails, style guides, SOPs, or even knowledge that currently lives in someone's head. If the step needs it, it's context."

   Work through each step using the 6-question framework:
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
5. **Propose and react** — After the first step of the deep dive, switch to propose-and-react: propose a hypothesis across all dimensions (including context readiness and role transitions for organizational workflows) and ask "What's right, what's wrong, what am I missing?" instead of asking each question individually. Include a context readiness hypothesis: "I think this context lives in [location] and is in [format] which AI can interpret. Is that right?"
6. **Map sequence** — After all steps, identify sequential vs. parallel steps and the critical path.
7. **Optimize for AI** (step-decomposed path only) — Now that the full process is mapped, step back and challenge it. The user described their *current* process — but an AI-powered version may not need every step. Present optimization recommendations for the user to react to. Look for:
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

8. **Validate the workflow** (step-decomposed path only) — Before consolidating context, walk through the refined workflow end-to-end and present a validation summary. This is the quality gate that catches gaps before the workflow moves to Design. Check for:
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

9. **Consolidate context** — Present a rolled-up "context shopping list" of every piece of context the workflow needs — documents, data, rules, examples, and any other knowledge from the user's domain that the model doesn't have.
10. **Generate Workflow Definition** — Produce the structured Workflow Definition and write it to the output file.

### Outcome-Driven Path (Step 4-OD)

When the user selects option (c) or the problem-first funnel recommends outcome-driven, run this interview instead of the step-decomposed deep dive (Steps 4–9). The outcome-driven path handles context discovery internally (question 7), so it skips straight to Generate Workflow Definition (Step 10) after the interview. Same interview principles apply: one question at a time, propose-and-react after the first few answers, push beyond vague answers.

1. **Goal**: "What does a successful run produce? Describe the deliverable."
2. **Inputs**: "What does the agent system receive to start? What triggers the work, and what materials does it have access to?"
3. **Expected outputs**: "What format, structure, and detail level does the deliverable need? Describe or show what 'good' looks like."
4. **Constraints**: "What boundaries or guardrails apply? Things the agent must always do, must never do, or limits on scope, sources, tone, length."
5. **Quality criteria**: "How will you evaluate whether the output is good vs. bad? What dimensions matter — accuracy, completeness, tone, specificity, timeliness?" (These feed directly into the Test step.)
6. **Capability domains**: "What does the agent system need to be good at? Not steps, but kinds of work — research, analysis, writing, data extraction, etc." After the first few answers, propose candidate domains from the goal/constraints and ask: "What's right, what's wrong, what am I missing?"
7. **Tools and context sources**: "What external systems, data sources, documents, or reference materials should the agent system have access to?" Apply the same context readiness probing as the step-decomposed path:
   - Access: Where does this context live today? Is it in a system with programmatic access (database, cloud app, shared drive), or does it require manual steps (logging in, copy-pasting, reading from a screen)?
   - Interpretability: Is the context in a format AI can process?
   - Persistence: Does this context need to exist as a durable artifact that AI can access across workflow runs?
8. **Human gates**: "Where should the agent system pause for human review? Or run end-to-end with final review only?"
9. **Scope check**: Same one-trigger-one-deliverable test as Step 2 — confirm the outcome hasn't expanded into multiple workflows.

After completing the interview, proceed directly to **Generate Workflow Definition** (Step 10) using the outcome-driven output format.

## Output

Write the Workflow Definition to `outputs/[workflow-name]-definition.md` where `[workflow-name]` is the kebab-case workflow name (e.g., `lead-qualification`).

The Workflow Definition uses a shared header with conditional sections depending on the definition type.

### Scenario Metadata (both formats)
- Workflow name, description, outcome, trigger, type, business objective, current owner(s), lens (Individual/Organizational)
- **Definition Type**: `Step-Decomposed` or `Outcome-Driven`
- For organizational lens: stakeholders (roles/teams involved), success metrics (KPIs for measuring improvement)

### Step-Decomposed Sections (when Definition Type = Step-Decomposed)

#### Refined Steps
For each step: number, name, action, sub-steps, decision points, data in/out, context needs, failure modes

#### Optimization Summary (produced by Step 7 — Optimize for AI; included if any optimizations were applied)
Brief record of what changed from the original process and why:
- Steps eliminated, collapsed, parallelized, or added
- Rationale for each change
- Any optimizations the user declined and why (preserves the reasoning for Design)

#### Step Sequence and Dependencies
- Sequential steps, parallel steps, critical path, dependency map
- Role swimlane (organizational lens with multiple roles) — a view showing which role owns each step

#### Context Shopping List
For each artifact: name, description, used by steps, status (Exists/Needs Creation), key contents, AI Accessible? (Yes/Partial/No), readiness notes

For items with `Status: Needs Creation`, the readiness notes should also capture where the artifact should be persisted — not just that it needs to be created, but that it needs a home AI can reach.

For organizational workflows, also prompt for existing process documentation: SOPs, training guides, compliance requirements, SLAs.

### Outcome-Driven Sections (when Definition Type = Outcome-Driven)

#### Goal
What a successful run produces — the deliverable described concretely.

#### Inputs
What the agent system receives to start — trigger, data, materials.

#### Expected Outputs
Format, structure, quality expectations, and an example of what "good" looks like.

#### Constraints
Boundaries, guardrails, must-do / must-not-do rules.

#### Quality Criteria
Evaluation dimensions, what good vs. bad looks like, minimum bar. These feed directly into Step 5 (Test).

#### Capability Domains
Table with columns: Domain Name, Description, Associated Tools/Data. Each domain represents a kind of work the agent system needs to be good at (e.g., research, analysis, writing, data extraction).

#### Tools and Context Sources
External systems, reference materials, with context readiness assessment for each:
- Access (direct AI access vs. human intervention needed)
- Interpretability (structured / semi-structured / unstructured)
- Persistence (durable artifact vs. needs externalization)

#### Human Gates
Where human review is expected — checkpoints during execution, or final review only.

## Guidelines

- Ask one question at a time — never present a wall of questions
- Probe for missing steps — most people undercount by 30-50%
- Surface hidden assumptions ("How do you decide when X is good enough?")
- Use plain language; avoid jargon unless the user introduced it
- Push beyond vague context answers like "domain knowledge" — identify the specific artifact
- Surface the assumption that existing context — data, documents, transcripts, reference materials — will "just work" for AI. Most people underestimate the work required to make context AI-accessible, especially unstructured content like SOPs, style guides, meeting transcripts, and knowledge that lives in people's heads. Adopt a data strategist lens — help the user see where context reorganization, reformatting, or externalization is needed before they commit to a workflow design that depends on inaccessible context. Push beyond "it's in the CRM" or "I just know it" — ask what system it's in, what format it's in, and whether there's programmatic access or it requires manual steps. Leave specific integration mechanisms (MCP, API, SDK) to the Design step.
- Stay in the "what" lane. Deconstruct defines the workflow, its context needs, and its failure modes. It does not prescribe how AI will access data, which tools to use, or what integrations to build — those are Design decisions (Step 3). If a technology concern surfaces, note it as a consideration for Design rather than resolving it here.
- After writing the Workflow Definition file, tell the user: "Workflow Definition saved to `outputs/[name]-definition.md`. Ready for the `design` skill (Step 3)."
- If entering deconstruction without a prior analysis (direct workflow description), determine the lens by asking if not obvious from context.
- For outcome-driven definitions, do not force step decomposition — the whole point is to capture what the agent system needs to know without prescribing execution steps.
- When the problem-first funnel (option b) recommends outcome-driven, explain why: "This looks like a workflow where the agent system should determine its own approach. I'd recommend the outcome-driven path because [reasoning]."
