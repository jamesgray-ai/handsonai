---
name: deconstruct
description: >
  This skill should be used when the user wants to deconstruct a workflow, break down a business
  process, capture requirements for an AI workflow, or define a goal for an agent system.
  Step 2 is the PRD for the workflow — it captures what the workflow must do, the rules it must
  follow, and the edge cases it must handle, in clear requirements language suitable for the
  Design step or any AI model to consume. Supports two paths: step-decomposed (you know how the
  work gets done) and goal-driven (you know what "done" looks like and want an agent system
  to determine the path). Produces a structured Workflow Requirements document.
  Also use when the user says "continue my workflow" and the workflow manifest shows Step 2 (Deconstruct) is next.
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
| **Step-decomposed** | The work runs the same way each run — you can describe how it gets done, even if the steps aren't mapped yet | "I know how the work gets done" |
| **Goal-driven** | You know what "done" looks like, but the work takes different steps depending on what comes in — so you give an agent system a goal and let it figure out the steps at runtime | "I know the goal" |

Both paths produce a Workflow Requirements document with the same shared shell — only the middle "what does the workflow do" block differs.

**What "goal" means here.** An agent goal is a **deliverable with a completion state** — something you can look at after a single run and verify is done. It is *not* a business objective or an impact metric: "higher revenue" is a business objective (record it in Metadata → Business Objective); "a ranked list of 20 qualified prospects matching our ICP, with contact info" is an agent goal. The goal bundles the deliverable plus the rules and acceptance criteria for it — what major agent frameworks call the expected output and success criteria. (If you know the product-management "outcomes over outputs" framing: the agent's goal is closer to an *output* — the business outcome belongs in Business Objective.) The defining trait of this path is **who owns the control flow**: the agent decides the *path* to the goal at runtime, while you own the *definition of done*. Note the inverse doesn't hold — a step-decomposed workflow can still use an agent for an individual step; what makes a workflow goal-driven is that the agent decides the overall sequence, not merely that agents are involved.

**Which path? (quick heuristic — share this with the user when they're unsure).** The test: *imagine two different inputs — would the work take noticeably different steps?* The choice depends only on the **nature of the work** — never on whether the user can currently list the steps.
- Choose **Step-decomposed** if the work runs **the same way each time** — same steps regardless of the input. The user does **not** need the steps written down or even fully clear in their head; describing how the work gets done is enough, and the interview maps and refines the steps with them.
- Choose **Goal-driven** if the work **takes different steps depending on what comes in**, and you'd rather define what "done" looks like plus the rules and let the agent figure out the steps at runtime.

Worked example: *"Generate my weekly status report from the same three sources"* → step-decomposed (same recipe every run). *"Triage whatever lands in my inbox and handle each appropriately"* → goal-driven (a refund request, a partnership pitch, and spam each take a completely different sequence of steps). Getting this right matters: the choice selects the document template the Design step parses, so a wrong pick creates rework downstream.

## Workflow

**Set expectations up front (first message):** tell the user this step is the most thorough interview in the framework — usually **20–40 minutes** of back-and-forth — because the requirements written here drive everything built later. Stopping early is safe: progress saves to files, and they can say "continue my workflow" in a later session to pick up where they left off.

1. **Scenario discovery** — Determine how the user is arriving and which path to take.

   **From Analyze output**: If the user references an opportunity report, file path (e.g., `outputs/ai-opportunity-report.md`), or a specific workflow candidate from an Analyze session, read the Workflow Candidate Summary from the file. Present the available candidates and ask which one to deconstruct. Pre-populate scenario metadata (name, description, trigger, deliverable, autonomy, involvement) from the candidate fields. If the candidate includes a `Lens` field, carry it forward along with any `Business Objective`, `Stakeholders`, and `Success Metrics` fields. Confirm the pre-populated details with the user. Then choose the path: if the candidate's autonomy = Autonomous, suggest goal-driven but still confirm. Otherwise present the choice below.

   **Cold entry (no Analyze output)**: Ask one question:

   > "Is the work the same every run, or does it vary by input? (Quick test: imagine two different inputs — would the work take the same steps, or different steps?)
   > - **Step-decomposed** — The work runs the same way each time. You don't need the steps written down — describing how the work gets done is enough, and I'll map and refine the steps with you, surfacing decision rules and edge cases along the way.
   > - **Goal-driven** — The steps vary depending on what comes in, but you can describe the deliverable — what "done" looks like — and want an agent system to figure out the steps at runtime. A goal here is a concrete deliverable, not a business result: "a ranked list of 20 qualified prospects" is a goal; "higher revenue" is why you want it. I'll capture the goal, inputs, acceptance criteria, and rules."

   When rendering this choice as a structured form (e.g., option cards), preserve the framing above: the step-decomposed card must say the work is *repeatable* and that the interview will map the steps — never "I can list the steps," which wrongly reads as an entry requirement. A "Not sure / I have a problem" option should invite the user in ("help me figure out the right workflow") rather than imply they lack a process.

   **Problem-first handling (no separate path)**: If the user says they don't have a process *or* a goal — just a problem ("People drop off during onboarding and I don't have a way to follow up") — propose a candidate workflow based on what they describe, then route into one of the two paths:
   > "Here's a candidate workflow that would solve this: [outline]. Do you want to refine these steps with me (step-decomposed), or just describe the goal and let an agent figure out the steps (goal-driven)?"

   **After the path is chosen, gather scenario details:**
   - **Step-decomposed**: Ask about the business scenario, objective, high-level steps, and ownership. One question at a time. If no lens was established, determine it: individual tasks (one person's repetitive work) = Individual lens; multi-role or business-objective processes = Organizational lens. Ask only if not obvious from context. Proceed to Step 2 (scope check) → Step 3 (naming) → Step 4 (deep dive).
   - **Goal-driven**: Proceed to Step 2 (scope check) → Step 3 (naming) → Step 4-GD (goal-driven interview). The interview opens with scenario grounding, so don't pre-interview here — but if the user has already described the situation, trigger, or consumer, carry those answers forward.

2. **Scope check — one trigger, one deliverable** — A workflow has exactly one trigger (what kicks it off) and one deliverable (the tangible output). Test for multiple workflows by checking:
   - **Triggers**: Multiple independent starting points? (e.g., "when a lead comes in" vs. "end of each week") → separate workflows
   - **Deliverables**: Distinct outputs at different points? If someone receives a deliverable midway and the process continues toward a different output → workflow boundary
   - **Timeframes**: Parts run on different schedules (daily vs. weekly), or significant waits between phases → likely separate workflows
   - **Step count**: Would this expand to 15+ refined steps? → may be multiple workflows
   - **Ownership boundary** (organizational lens): Does this process have a single accountable owner for the end-to-end outcome? If different people own different segments with no single owner, it may be multiple workflows.

   If multiple workflows are detected: map out each one (working name, trigger, deliverable), present the breakdown, confirm boundaries with the user, and ask which to deconstruct first. Proceed with only the chosen workflow.

3. **Name the workflow** — Present 2-3 name options. Naming conventions: a **2-4 word noun phrase** in **Title Case**, self-explanatory without context (e.g., "Lead Qualification", "Newsletter Distribution", "Student Onboarding"). Prefer `[Subject] [Action]` patterns — "Invoice Generation", "Inbox Triage" — over verb phrases or vague labels. Confirm name, description, goal, and trigger.

   **Derive the workflow ID.** Convert the confirmed name to kebab-case (lowercase, hyphens, no punctuation — "Lead Qualification" → `lead-qualification`) and confirm it with the user: "I'll use `lead-qualification` as the workflow ID — it names the folder and files for everything we produce." This ID is the single source of truth for all artifact paths; every downstream skill uses it verbatim.

4. **Deep dive (step-decomposed only)** — Before probing the first step, briefly frame what "context" means: "As we go through each step, I'll ask about the *context* it needs. Context is any data or information the step requires to do its job — that includes databases and spreadsheets, but also documents, transcripts, emails, style guides, SOPs, or even knowledge that currently lives in someone's head. If the step needs it, it's context."

   Work through each step using the 6-question framework. **Ask one question at a time, adapt to the user's answers, and skip dimensions already well-covered — this is a scaffold for *you*, never a checklist to read aloud at the user.** These six dimensions shape what to ask, not how the spec is structured. Your job is to gather enough signal across all six to write the per-step requirements block (Goal / Inputs / Outputs / Rules & Edge Cases / Context Needed) in Step 10.

   - Discrete steps (is this actually multiple steps?)
   - Decision points (if/then branches, quality gates)
   - Data flows (inputs, outputs, sources, destinations)
   - Context needs (specific documents, files, reference materials)
   - Failure modes (what happens when this step fails)
   - Context readiness (adopt a data strategist lens for each step's context inputs — **sample these probes, don't interrogate: ask the one or two that matter for this step rather than all four every time**):
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

   For step-decomposed workflows: assemble from per-step context needs gathered in Step 4. For goal-driven workflows: assemble from the Inputs + Context Sources gathered in Step 4-GD.

10. **Collect Acceptance Criteria and Example Scenarios (both paths)** — Before generating the Workflow Requirements, ask the user about acceptance criteria and example scenarios. These were previously collected during Design's Step 8b; capturing them here makes Step 2 a complete PRD and removes redundant questioning downstream.

    Ask, one at a time:
    1. "What does great output from this workflow look like? Describe what would make you say 'this is exactly right.' Examples or anti-examples are both useful here."
    2. "Which dimensions matter most? For example: accuracy, completeness, tone, specificity, timeliness, format consistency."
    3. "What's your minimum bar — what's acceptable vs. what needs more work?"
    4. "Give me 3-5 real or realistic scenarios you'd run this on — different enough to test the workflow's range. For each, briefly describe the input and what you'd look for in the output."
    5. "For any of those scenarios, do you have a **golden example** — a real past output (or excerpt) you'd consider 'exactly right' for that input?" Golden examples turn Test (Step 5) from gut-feel scoring into comparison against a known-good reference. Don't push if none exist — but if the user produces this output today, a recent good one usually does. If a golden example is a document, add it to the Context Inventory and reference its ID.

    For goal-driven workflows, Step 4-GD does **not** pre-collect full acceptance criteria — this step is the single place acceptance is captured, so ask the questions that remain unanswered directly. Two harvests from Step 4-GD feed this step: for question 4, **harvest the scenarios from the variation envelope** (the typical and edge cases the user already described); for questions 1–3, **seed from the rejection-test answers** (the plausible-but-wrong outputs the user said they'd send back). Confirm and fill gaps rather than re-eliciting from scratch.

11. **Generate Workflow Requirements** — Produce the structured Workflow Requirements document and write it to the output file. See the **Output** section below for the template, writing style, and machine-readability rules.

    **Self-check before finishing (so Design can parse it).** After writing, verify the file against the machine-readability rules and fix any miss before handing off:
    - File lives in the workflow folder using the kebab-case ID: `outputs/[workflow-name]/requirements.md` (e.g., "Inbound Lead Triage" → `outputs/inbound-lead-triage/requirements.md`), and `workflow.yaml` exists alongside it with `current_step: 2` and the requirements path registered.
    - All required headings are present and **exactly named** (no synonyms): Goal, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, plus the path-specific middle (Steps Overview + Step Details + Sequence for step-decomposed; Inputs + Rules & Constraints for goal-driven).
    - Canonical vocabulary used exactly (Definition Type, Lens, Context Status, AI Accessible) and stable IDs present (steps `1,2,3…`; context `C1,C2…`; scenarios `E1,E2…`).
    - If anything is off, fix it before telling the user it's ready.

### Goal-Driven Path (Step 4-GD)

When the user selects goal-driven, run this interview instead of the step-decomposed deep dive (Steps 4–8). The goal-driven path handles context discovery internally (question 8, Context & Data Sources), so it skips straight to Step 9 (Consolidate Context) → Step 10 (Acceptance Criteria) → Step 11 (Generate) after the interview. Same interview principles apply: one question at a time, propose-and-react after the first few answers, push beyond vague answers. If scenario discovery (Step 1) already captured the situation, trigger, or consumer, build on those answers — confirm and deepen rather than re-asking from scratch.

**Open with a frame** so the user knows what this path asks of them (parallel to the context frame the step-decomposed path opens with):

> "This path is for when you know what you want but not the exact steps — you don't need to map anything out. You'll give the agent system a goal — a concrete deliverable it produces each run — plus the rules it has to follow, and I'll handle the structure. Let's start with the situation."

1. **Scenario (ground before sharpening)**: "Tell me about the situation — what's going on, what kicks this off, and what are you trying to get done?" Plain language; no precision demanded yet. This grounds the trigger, the consumer, and the business context before the goal is sharpened. Note any business objective the user states ("we need more pipeline") — it goes in Metadata → Business Objective, not in the goal.
2. **Goal (natural, then reflect back)**: "Now the result: when a run works well, what do you walk away with? Talk like you're describing it to a colleague — don't worry about being precise." Then **reflect back a structured restatement** that covers all three of **format, structure, and scope** — plus who consumes it — and names the completion state: "So the goal is roughly [restatement], and a run is done when [completion state]. Did I get that right, or what's off?" The reflect-back is where the rigor lives; don't drop any of format/structure/scope. If the user struggles, offer a vague-vs-sharp calibration example (e.g., "'Help me with prospecting' is a start — what I'm after is more like 'a ranked list of 20 qualified prospects matching our ICP, with contact info and a one-line fit rationale, every Monday'").
3. **Goal pressure-test (challenge before accepting)**: After the reflect-back, test the goal — don't just record it. Apply whichever of these three tests the answer hasn't already passed, state which test failed and why when pushing back, and cap the challenge at 2–3 probes (interview, not interrogation):
   - **Done/not-done test (completion state)**: "If the agent handed you one run's output, could you say 'done' or 'not done' just by looking at it?" — "Improve our pipeline" fails; "a ranked list of 20 prospects with contact info" passes. If it fails, push for the concrete deliverable.
   - **Level test (business objective vs. agent goal)**: If the stated goal is metric-shaped with no deliverable ("higher revenue", "more engagement"), ladder *down*: "That's the business objective — I'll record it in Metadata. What's the *thing* the agent hands you that contributes to it?" If it's hopelessly vague ("help with email"), sharpen via format, structure, and scope.
   - **Rejection test (testability)**: "Describe an output that *looks* plausible but you'd send back. What's wrong with it?" The answers surface implicit acceptance criteria — carry them forward to seed Step 10; don't re-elicit there.

   If the user's first answer in question 2 is purely metric-shaped (no deliverable at all), skip the reflect-back and go straight to the level test. If the probe cap is reached and the goal is still untestable, switch from asking to proposing: draft a sharp candidate goal yourself from everything heard so far and ask the user to confirm or correct it — never proceed to question 4 with a goal that fails the done/not-done test.
4. **Variation envelope**: "This works as goal-driven because the work takes different steps depending on what comes in. What's the range it needs to handle? Give me the typical case, and a couple of the awkward or harder ones." These answers become the Example Scenarios in Step 10 — capture them now and harvest them there; don't re-elicit scenarios later. **Misroute check:** if the answer reveals the work actually takes the same steps every time (no meaningful variation), say so and offer to switch: "This sounds like it runs the same way each run — the step-decomposed path would capture it better. Want to switch?" Carry everything gathered so far into the step-decomposed deep dive rather than restarting.
5. **Inputs**: "What kicks it off, and what does the agent system get to work with — data, documents, access?" (Confirm against what the scenario already established rather than re-asking.)
6. **Rules & Constraints**: "What boundaries or guardrails apply? Things the agent must always do, must never do, or limits on scope, sources, tone, length."
7. **Fallback behavior**: "When it hits a case it can't confidently handle — missing info, something ambiguous — what should it do? Stop and ask you, make its best attempt and flag it, or skip that item?" This is the agent's behavior on *unplanned* exceptions — distinct from the *planned* pauses captured under Human gates. Record it under Rules & Constraints in the output. If the answer is "stop and ask," also capture it as a Human Gate (question 9) so the pause appears where Design looks for review points.
8. **Context & Data Sources**: "What external systems, data sources, documents, or reference materials should the agent system have access to?" Apply the same context readiness probing as the step-decomposed path (sample — ask the one or two probes that matter, don't run all three mechanically):
   - Access: Where does this context live today? Is it in a system with programmatic access (database, cloud app, shared drive), or does it require manual steps (logging in, copy-pasting, reading from a screen)?
   - Interpretability: Is the context in a format AI can process?
   - Persistence: Does this context need to exist as a durable artifact that AI can access across workflow runs?
9. **Human gates**: "Where should the agent system pause for human review? Or run end-to-end with final review only?"
10. **Scope check**: Same one-trigger-one-deliverable test as Step 2 — confirm the goal hasn't expanded into multiple workflows.

**Do NOT ask about capability domains, agent count, model class, tools, or orchestration approach.** Those are Design decisions. Goal-driven Deconstruct stays in "what" territory: goal, inputs, acceptance criteria, rules, context, human gates.

**Step 8-GD — Validate before consolidating (goal-driven quality gate).** Step-decomposed has a Step 8 validation gate; goal-driven needs the equivalent so a vague goal or missing guardrails doesn't sail through to Design. Walk the definition end-to-end and present a short validation summary covering:
   - **Goal is bounded, singular, and testable** — one clear deliverable that passes the done/not-done test ("help with email" is too vague; "a drafted reply per inbound inquiry" is bounded). If you can't tell from one run's output whether the goal is met, tighten it before Design.
   - **Variation range is captured** — the typical case and the awkward/edge cases are identified (these become the test scenarios in Step 10).
   - **Rules are sufficient** — must-do and must-never both covered; scope boundaries explicit enough to keep the agent in bounds.
   - **Fallback behavior is defined** — it's clear what the agent does when it can't confidently complete a case.
   - **Context is reachable** — every context/data source named has a known location and an access path (not "it's in my head" or a login-only portal with no plan to bridge it).
   - **Human gates are defined** — it's clear where (if anywhere) a human reviews, and that final-review-only is a deliberate choice.

   Present as: "Before I finalize, here's a quick check of your goal-driven definition: [findings]. Which of these should we tighten?" Update based on the user's answers. If all clear, say so and proceed.

After completing the interview and Step 8-GD, proceed directly to Step 9 (Consolidate Context) → Step 10 (Acceptance Criteria) → Step 11 (Generate Workflow Requirements) using the goal-driven output format.

## Output

Write the Workflow Requirements to `outputs/[workflow-name]/requirements.md` where `[workflow-name]` is the kebab-case workflow ID confirmed in Step 3 (e.g., `outputs/lead-qualification/requirements.md`). Create the folder if it doesn't exist.

### Workflow manifest

Deconstruct **creates the workflow's manifest** — a small `workflow.yaml` in the workflow folder that tracks state and artifact paths so any framework skill (or a fresh session) can pick up where things left off:

The manifest is also the workflow's **AI Registry entry** — the single source of truth for the metadata that appears in the generated `REGISTRY.md` (see the `indexing-registry` skill). All registry fields are optional; leave out what isn't known yet rather than inventing values.

```yaml
workflow: lead-qualification      # kebab-case ID — names the folder and all artifacts
display_name: Lead Qualification
description: >-                   # 1-2 sentence outcome-focused description
  Qualifies inbound leads against the ICP and produces a ranked list.
process_outcome: Ranked qualified-lead list   # the tangible deliverable
business_process: Sales Pipeline  # which business process this workflow belongs to
sequence: 10                      # order within the process (multiples of 10) — optional
status: under-development         # backlog | under-development | in-production
type: augmented                   # augmented | automated | manual
autonomy: guided                  # deterministic | guided | autonomous (set by design)
trigger: "New lead in CRM"        # what kicks the workflow off
owner: "[person or role]"         # copy from Metadata → Owner
platform: claude-code             # claude-code | cowork | claude-ai | scheduled-agent (set by build/run)
health: ""                        # working | needs-attention | broken (set by test/run/improve)
last_run: ""                      # YYYY-MM-DD of most recent run (set by run)
apps: []                          # integrations used, e.g., [Gmail, Notion] (set by design/build)
assets_used: []                   # skills/agents this workflow uses, by name (set by build)
definition_type: Step-Decomposed  # or Goal-Driven (legacy files may say Outcome-Driven — treat as Goal-Driven)
current_step: 2                   # last completed framework step (1-7); 0 = named only
last_updated: YYYY-MM-DD
artifacts:
  requirements: outputs/lead-qualification/requirements.md
  # downstream skills append:
  #   sop, design_spec, platform_artifacts (list), test_results,
  #   run_guide, run_log, improvement_plan
notion_url: ""                    # optional back-pointer if the user mirrors to Notion
# run also sets a top-level key: next_review: YYYY-MM-DD
```

Deconstruct populates `display_name`, `description`, `trigger`, and `owner` (from the Metadata answers it already collects), sets `status: under-development`, and leaves the rest for downstream skills. **If a stub manifest already exists** (created by `naming-workflows` with `current_step: 0`), merge into it — preserve every field already set — never overwrite it with a fresh template.

Conventions every framework skill follows (stated here once; downstream skills apply them):

- **Read the manifest on load** to locate artifacts and confirm you're working on the right workflow.
- **Resume orientation ("continue my workflow").** Any framework skill can be the re-entry point. When the user says "continue my workflow" (or invokes a skill without context), scan `outputs/` for workflow folders: if several exist, list them with their `current_step` and ask which to continue. Then orient before doing anything: "You finished Step [N] ([name]) on [last_updated] — next is Step [N+1] ([name])." If the invoked skill doesn't match the next step, say so and route to the right one instead of re-running finished work.
- **Update it after writing your output**: set `current_step`, `last_updated`, and add your artifact path under `artifacts`.
- **Refresh the AI Registry index.** After updating the manifest, refresh `REGISTRY.md` at the workspace root using the regeneration procedure in the `indexing-registry` skill (create the file if it doesn't exist yet). This is best-effort — if the environment can't write to the workspace root, note it and continue; a failed refresh never fails a framework step.
- **Never silently overwrite.** If your output file already exists from a previous run, rename the old one with a date suffix (e.g., `requirements-2026-06-10.md`) before writing.
- **Legacy layout:** if no workflow folder exists but flat files like `outputs/[name]-requirements.md` (or a requirements-like file at the workspace root) do, use those paths and offer to create the folder + manifest. **Migrating the files themselves is optional** — the manifest's artifact paths are authoritative and may point anywhere, so a user who wants their files where they are keeps them there; record that choice in the manifest's `notes` and don't re-raise migration on later runs. The manifest is the one piece the framework does require.
- **No persistent workspace:** if this environment can't keep files between conversations (no project workspace — files are produced as downloads), tell the user after each write: "Save this file — you'll re-supply it (plus `workflow.yaml`) when you run the next step, or continue the next step in this conversation." On load, if the expected files aren't present, ask the user to re-upload them instead of failing.

### Writing-style rules (MUST follow)

The output reads like a PRD, not an interview transcript. Enforce:

- **Requirements voice.** Every bullet is a statement of what must be true, not a description of what the user said. Prefer "The step accepts a list of prospect URLs" or "Output is a Markdown table with one row per prospect" over "The user mentioned they usually have a list of URLs."
- **Active voice. Present tense.** "Validate the input against the rubric" — not "The input will then be validated."
- **One requirement per line.** Use bulleted lists, not paragraphs, anywhere multiple discrete requirements appear.
- **Concrete over abstract.** Name the artifact, the field, the threshold. "Reject submissions over 500 words" — not "Filter out long submissions."
- **No interview residue.** Drop hedges ("I think", "sometimes", "usually"), narrative connectors ("then the user", "after that"), and meta-commentary about the conversation ("we discussed", "you mentioned").
- **Self-contained.** A reader who never saw the deconstruct conversation can implement against the document.
- **Markdown hygiene.** Don't use a bare `~` for "approximately" — two tildes in one paragraph render as `~~strikethrough~~`. Write "approximately"/"about" (e.g., "about 1–2 pages", "150–250 words"), or keep `~` only inside code spans/backticks.

### Machine-readability rules (MUST follow)

So Design (and any agent model) can parse the document without re-asking:

- **Fixed section headings**, in fixed order — use the exact headings in the template; no synonyms, no reordering.
- **Tables for any list of items with shared fields** (steps, context artifacts, example scenarios) — not prose.
- **Canonical vocabulary** for enumerated values:
  - Definition Type: `Step-Decomposed` or `Goal-Driven`
  - Lens: `Individual` or `Organizational`
  - Context Status: `Exists` or `Needs Creation`
  - AI Accessible: `Yes`, `Partial`, or `No`
- **Stable IDs** — number steps `1, 2, 3, …`; ID context items `C1, C2, C3, …`; ID example scenarios `E1, E2, E3, …`. Downstream artifacts reference these IDs.
- **Explicit Inputs and Outputs per step** — even when "obvious." Design uses these to build the data-flow without guessing.

### Template — shared shell

```markdown
# [Workflow Name] — Workflow Requirements

## Goal
[One paragraph: what a successful run produces, when it runs, who consumes the output.]

## Metadata

| Field | Value |
|---|---|
| Workflow Name | [name] |
| Description | [short description] |
| Trigger | [what kicks the workflow off] |
| Owner | [person or role] |
| Lens | Individual / Organizational |
| Definition Type | Step-Decomposed / Goal-Driven |
| Business Objective | [why this workflow matters — optional but recommended] |

For organizational lens, also include:
| Stakeholders | [roles/teams involved] |
| Success Metrics | [KPIs for measuring improvement] |

---

[INSERT THE STEP-DECOMPOSED BLOCK OR THE GOAL-DRIVEN BLOCK HERE — see below]

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

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | [short name] | [description] | [what makes this output "good"] | [Context Inventory ID, short inline excerpt, or "—"] |
| E2 | … | … | … | … |

Golden Examples are optional but high-value — Test (Step 5) compares actual output against them instead of relying on gut-feel scoring alone. Use "—" when none exists.

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

### Goal-Driven middle block

Insert between the Metadata table and the Context Inventory (omit Steps Overview, Step Details, and Sequence — there is no fixed step sequence for goal-driven workflows):

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
- **Fallback behavior:** [what the agent does when it can't confidently complete a case — stop and ask, best-effort and flag, or skip]
```

The Goal, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, and Human Gates sections from the shared shell still apply — goal-driven uses the same shell, just a different middle. The **Example Scenarios should reflect the variation envelope** captured in Step 4-GD: the typical case plus the awkward/edge cases the agent must handle.

## Guidelines

- Ask one question at a time — never present a wall of questions.
- Probe for missing steps — most people undercount by 30-50%.
- Surface hidden assumptions ("How do you decide when X is good enough?").
- Use plain language; avoid jargon unless the user introduced it.
- Push beyond vague context answers like "domain knowledge" — identify the specific artifact.
- Surface the assumption that existing context — data, documents, transcripts, reference materials — will "just work" for AI. Most people underestimate the work required to make context AI-accessible, especially unstructured content like SOPs, style guides, meeting transcripts, and knowledge that lives in people's heads. Adopt a data strategist lens — help the user see where context reorganization, reformatting, or externalization is needed before they commit to a workflow design that depends on inaccessible context. Push beyond "it's in the CRM" or "I just know it" — ask what system it's in, what format it's in, and whether there's programmatic access or it requires manual steps. Leave specific integration mechanisms (MCP, API, SDK) to the Design step.
- **Stay in the "what" lane.** Deconstruct defines the workflow, its context needs, its rules, and its acceptance criteria. It does not prescribe how AI will access data, which tools to use, what integrations to build, how many agents are needed, or which models to use — those are Design decisions (Step 3). Do not ask the user about capability domains, agent architecture, model class, or orchestration mechanism. If a technology concern surfaces, note it as a consideration for Design rather than resolving it here.
- After writing the Workflow Requirements file, tell the user: "Workflow Requirements saved to `outputs/[name]/requirements.md`. Ready for the `design` skill (Step 3)."
- If entering deconstruction without a prior analysis (direct workflow description), determine the lens by asking if not obvious from context.
- For goal-driven workflows, do not force step decomposition — the whole point is to capture what the agent system needs to know without prescribing execution steps.
