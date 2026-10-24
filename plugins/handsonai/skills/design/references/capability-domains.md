# Capability domains (`decomposition: domains`)

Read when the requirements say `AI works it out each time` (`Path: none`) and your own breakdown makes every part Autonomous with nothing fixed. Otherwise plan your own steps (`Step Pa`, `Step Pb`…) and say B54 in the review: a workflow with one input and rules that settle each decision is more reliable as a fixed set of steps.

**What a capability domain is.** A durable ability the AI draws on at runtime ("researching each section", "synthesis"), not a pipeline stage or a fixed sequence. Domains come from the requirements' Goal, Inputs, Rules & Constraints and Acceptance Criteria; the requirements never list them.
- **Altitude:** one domain per competency. Researching four report sections is one "section research" domain run as a fan-out, not four domains.
- **Cardinality:** several domains may map to one skill or agent, and one domain may fan out to parallel runs of one worker; record the fan-out in Multi-Agent Configuration (Parallelization), never as duplicate rows.
- **Premise:** domains are what the orchestrator can call on, not a path it must follow.

**The level and the mechanism** still come from the evidence (SKILL.md, Part 2; `plan-template.md` section 2), never assumed: `domains` applies only when that evidence makes every part Autonomous. Nothing about it is asked.

**In the plan:**
- **Autonomy Summary:** D10's line, word for word, then the pattern with both citations:

  > Every AI step is Autonomous and no step is fixed, so this plan maps capability domains (`decomposition: domains`). Autonomy is Autonomous — the agent system determines its own execution path based on the Goal, Path, Inputs, Rules & Constraints, and Acceptance Criteria defined in the Workflow Requirements.

- **Decomposition:** the Capability Domain Mapping replaces the step table, with the same columns and a domain name in the first:

  ```markdown
  | Domain | Autonomy | Orchestration | Integration | Intelligence | Build Output | Checkpoint | Role |
  |---|---|---|---|---|---|---|---|
  | Section research | Autonomous | A1 | Web search (use) | reasoning-heavy; C1 | New agent: A1 | — | AI |
  ```

  Build Output takes the same canonical values; expect `New skill: S[n]`, `New agent: A[n]` or `Handled by orchestrator`. On a primary-loop platform there is no Orchestrator Prompt Outline: the orchestrator is the primary loop, captured as the orchestrator skill (`orchestrator-on-primary-loop.md`); document its logic in the Deployment Plan.
- **Blueprints:** skills list `Covers Steps` as domain names. Agents are the workers the orchestrator dispatches, never the orchestrator itself; a primary-loop design may have no agent at all (orchestration logic plus skills), and then has no agent blueprint and no Multi-Agent Configuration.
- **Safety & Permissions and Constraint Conformance** apply unchanged, and weigh more: with no fixed path to inspect, the Prohibited actions and checkpoints are the boundary the AI works inside. The checkpoint question is D5 for any change in a live system.
- **Tasks:** one per distinct artifact, as for steps; *Meets* lists the AC, R, G, D and W IDs (there are no Step IDs).

**In the review,** say D8′ (SKILL.md, Part 4). The self-check reads "Step ID" as "domain" throughout.
