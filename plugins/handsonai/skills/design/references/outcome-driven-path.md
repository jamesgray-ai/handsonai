# Outcome-Driven Processing Path

When the Workflow Requirements has `Definition Type: Outcome-Driven`, the following modifications apply to the standard Design workflow. Read this file in full before proceeding past Step 1 for an outcome-driven workflow — these substitutions change Steps 3–9 and the spec template.

**Step 3 (Architecture Decisions):** Same as standard, but the source sections differ. For outcome-driven Workflow Requirements, extract tools from the **Inputs**, **Rules & Constraints**, and **Context Inventory** sections (there are no per-step data flows to read from). Capability Domains do not exist in the Workflow Requirements — they are derived in Step 6.

**Step 4 (Autonomy Assessment):** State as fact: "This is an outcome-driven workflow — autonomy is **Autonomous** by definition. The agent system determines its own execution path."

**Step 5 (Orchestration Mechanism):** State as fact: "Orchestration is **Agent**." Still determine the involvement mode (Augmented/Automated) from the definition's Human Gates section and trigger type. Still ask the platform sub-choice if the platform has multiple agent offerings.

**On Claude Code/Cowork, "Agent" mechanism does NOT mean "build an orchestrator agent file."** It means the workflow is driven by an agentic loop — and that loop is the **primary session**. The artifacts you produce are the orchestration logic (command/`CLAUDE.md` run section) plus the **sub-agent(s)** the primary loop dispatches (see "Who is the orchestrator?" in Step 5 of the skill). Carry this into Capability Domain Mapping and Agent Configuration below.

**Step 6 (Classify Each Step) → Capability Domain Mapping:** Replace per-step classification with capability domain mapping.

**Important:** Capability Domains are derived by Design — they are **not** captured in the Workflow Requirements (the Workflow Requirements stays in "what" territory; capability decomposition is "how"). Infer capability domains from the Workflow Requirements' Outcome, Inputs, Rules & Constraints, and Acceptance Criteria. Propose them to the user and confirm before mapping.

For each derived capability domain:

| Domain | Integration Needs | Intelligence Requirements | Reusable Skill? |
|--------|-------------------|--------------------------|-----------------|
| [domain] | Tools/connectors needed | Model class, context sources | Yes/No + rationale |

Same Integration Discovery and Skill Discovery processes apply, operating on capability domains instead of steps.

**Step 7 (Skill Candidates):** Same field structure — identify which capability domains should become skills. Each skill candidate uses the full 12-field Skill Candidate block (with Covers Domains in place of Covers Steps).

**Step 8 (Agent Configuration):** This is usually the primary blueprint section. Agent Configuration documents the **sub-agent(s) the orchestrator dispatches** — the workers — using all 13 standard fields, drawing Description, Mission, Responsibilities, Output Format, and Constraints from the Workflow Requirements' Outcome, Rules & Constraints, and Acceptance Criteria.

**Mandatory-but-with-an-exception:** document at least one agent **whenever the design includes a sub-agent/agent artifact** (the common case). A valid outcome-driven design on a primary-loop platform (Claude Code/Cowork) may have **zero sub-agents** — just orchestration logic (command/`CLAUDE.md` run section) + skills. In that case record `agents: 0` in the frontmatter counts and document the orchestration logic in the Deployment Plan / Orchestrator notes instead — **do not invent a sub-agent to satisfy the field.** Never document the orchestrator (the primary loop) as an agent artifact.

**Step 8b (Verify Evaluation Inputs):** Same as step-decomposed — confirm Acceptance Criteria and Example Scenarios in the Workflow Requirements are complete; do not duplicate.

**Step 9 (Generate Spec):** Use the modified template sections below. The spec uses the same filename pattern and same frontmatter shape (with `definition_type: Outcome-Driven`). The Step-by-Step Decomposition section is replaced with Capability Domain Mapping; the Autonomy Spectrum Summary becomes a brief Autonomous statement; Build Output is captured per domain rather than per step.

## Spec template modifications

Replace the `## Step-by-Step Decomposition` section of `references/spec-template.md` with:

```markdown
## Capability Domain Mapping

(Capability domains are derived by Design from the Workflow Requirements' Outcome, Inputs, Rules, and Acceptance Criteria. They are not present in the Workflow Requirements.)

| Domain | Description | Integration (use/build) | Intelligence | Build Output |
|--------|-------------|------------------------|--------------|--------------|

**Build Output values:** Same canonical forms as the step-decomposed table (`New skill: SN`, `Use existing: [name]`, `New agent: AN`, etc.). For outcome-driven workflows, expect most domains to map to either `New skill: SN` (the orchestrator/sub-agent delegates to a reusable skill) or `Handled by orchestrator` (the orchestrating primary loop — or a deployed agent on SDK platforms — handles the domain inline via its own instructions; legacy synonym: `Handled by agent`).

### Autonomy Statement

This is an outcome-driven workflow. Autonomy is Autonomous — the agent system determines its own execution path based on the Outcome, Inputs, Rules & Constraints, and Acceptance Criteria defined in the Workflow Requirements.
```

Additional substitutions:
- Replace `## Autonomy Spectrum Summary` with the Autonomy Statement above.
- Omit `## Orchestrator Prompt Outline` (on Claude Code/Cowork the **primary loop is the orchestrator** — captured as orchestration logic in the Deployment Plan, not an agent file).
- Skill Candidates use the same 12-field block (with `Covers Domains` instead of `Covers Steps`).
- Agent Configuration documents the **sub-agent(s) the orchestrator dispatches** and is included whenever the design has ≥1 sub-agent (the common case). A primary-loop design with **zero sub-agents** (orchestration logic + skills only) is valid: set `agents: 0` and document the orchestration logic in the Deployment Plan instead.
- The Safety & Permissions section applies unchanged — outcome-driven workflows are Autonomous by definition, so the unattended-runs and blast-radius rows deserve extra attention.

## Checklist modifications

Apply the "Outcome-driven modifications" listed at the end of `references/self-test-checklist.md`.

## Layer 1 playback substitutions

For the Layer 1 confirmation gate, use the standard playback structure with these substitutions:

- **Autonomy level:** Autonomous — meaning [the system figures out its own path based on the outcome and rules you defined]. (Outcome-driven workflows are always Autonomous by definition.)
- **Mechanism:** Agent — [the workflow is driven by an agentic loop that decides what to do based on context, not a fixed script]. On Claude Code/Cowork that loop is the **primary session (the orchestrator)**.
- Replace **Steps classified** with **Capability domains mapped** — explain in plain language ("the buckets of capability the workflow needs to cover").
- **Agent blueprint:** summarize the **sub-agent(s) the orchestrator will dispatch** (the workers), or "None — the primary loop orchestrates directly using skills" if no sub-agent is needed. Do **not** describe a standalone orchestrator agent on Claude Code/Cowork.

## Presentation formats

- Integration Discovery: `**[Tool] access needed (Domains: X, Y):**` instead of step numbers.
- Skill Discovery: `**[Domain: Research] needs a skill: "..."**` instead of step IDs.
