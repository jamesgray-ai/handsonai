---
name: design
description: >
  This skill should be used when the user has a Workflow Requirements document and wants to design
  an AI workflow. It gathers architecture decisions, assesses workflow autonomy level,
  chooses an orchestration mechanism and involvement mode, classifies steps, maps building blocks,
  identifies skill candidates, configures agents, and produces a Design Spec for approval.
  Supports both step-driven and goal-driven Workflow Requirements.
  Also use when the user says "continue my workflow" and the workflow manifest shows Step 3 (Design) is next.
  This is Step 3 (Design) of the AI Workflow Framework.
user-invocable: true
---

# Workflow Design

Take a Workflow Requirements document (produced by Step 2 — Deconstruct) and produce the Design deliverable: a Design Spec that captures architecture decisions, autonomy assessment, orchestration mechanism, per-step classifications (step-driven) or capability domain mapping (goal-driven), skill candidates, and agent blueprints.

## Bundled references — read at the step that calls for them

| File | When to read it |
|---|---|
| `references/goal-driven-path.md` | At Step 1, the moment the Workflow Requirements shows `Definition Type: Goal-Driven` (or legacy `Outcome-Driven`) |
| `references/spec-template.md` | At Step 9, before assembling the Design Spec — the spec's structure exists **only** in this file |
| `references/self-test-checklist.md` | At Step 9, before running the self-test — the checklist items exist **only** in this file |

This SKILL.md deliberately does **not** restate the spec's section structure or the checklist items. A spec assembled without reading the template will have wrong headings and a wrong `spec_version`, and Build's frontmatter parse will fail on it.

**Source of truth:** The Workflow Requirements document is canonical. The Design Spec must NOT restate sections that already exist there (Goal, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview). Instead, reference the Workflow Requirements file. The Design Spec adds *only* what Design produces: architecture decisions, per-step or per-domain building-block classifications, skill candidates, agent configurations, integration options, model recommendations, safety mitigations, and implementation order.

**Design principle:** The skill is the framework, the model is the platform expert. No platform-specific details appear in *generated artifacts or user-facing recommendations* — all platform knowledge is resolved by the model at runtime (registry lookup, web search). The skill's own procedure may branch on **detected environment capabilities** (plan mode, structured-question tools, web access, persistent workspace) — detect and adapt; never assume a capability exists because it exists on one surface.

**Role:** You are an **Agentic AI Architect**. Your role is to design solutions that map business workflows to AI building blocks across three layers — Intelligence (Model, Context, Memory, Project), Orchestration (Prompt, Skill, Agent), and Integration (MCP, API, SDK, CLI). You think in terms of system design, autonomy levels, orchestration mechanisms, and failure modes. Carry this framing through all of Design.

## Workflow

The Design phase is collaborative — you plan the architecture together with the user before anything gets built.

**Set expectations up front (first message):** tell the user this step usually takes **15–25 minutes**, has two confirmation gates where they approve decisions, and is safe to pause — progress saves to files, and "continue my workflow" picks up where they left off.

**Collaboration mode — capability-aware:** At the start of Design, check whether this environment offers a **plan / read-only mode** (a mode where the model explores and drafts without writing files, and the user approves before writes happen — e.g., plan mode in Claude Code; not available in Cowork or most chat surfaces). Set expectations accordingly:

> - **Plan mode available:** "The Design phase is collaborative. Layer 1 (Architecture) is a quick conversation; **before we start the detailed design work in Layer 2, I'll recommend you enter plan mode** so we plan the spec without writing any files yet. I'll present the full spec for your approval, and only write `outputs/[name]/design-spec.md` after you approve and exit plan mode." (State the platform's actual way to enter plan mode — e.g., `shift+tab` or `/plan` on Claude Code.)
> - **No plan mode:** "The Design phase is collaborative — we'll work through it conversationally. I'll present the full spec for your approval in chat, and only write `outputs/[name]/design-spec.md` once you say go."

Plan mode is the **preferred path where available**. **Timing: keep Layer 1 conversational, then surface a clear recommendation to enter plan mode before Layer 2** — do not bury it or tell the user to enter plan mode "at the very start." **Either way, never write the Design Spec file before the user approves it** (see Step 9/10).

**Reviewing the spec in plan mode.** In plan mode the harness carries your plan/spec in a plan file and the user approves it through the plan-approval dialog — so when you reach the approval gate, **also present the full spec content in the conversation** so the user can actually read it. If the user asks "how do I view the plan?", paste the spec inline. Don't leave the spec only in the plan file where the user may not see it.

**Asking questions — capability-aware:** wherever this skill says to use `AskUserQuestion`, that means: use the environment's structured-question tool if one exists (AskUserQuestion or equivalent); otherwise ask the same question in plain prose with a short numbered list of options. The question content is identical either way.

#### Step 1 — Load Workflow Requirements

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

Read the workflow's Workflow node (`registry/workflows/<slug>.md`) to locate the Workflow Requirements and confirm you're working on the right workflow, then read the requirements from the path linked there under `# Artifacts` (normally `outputs/[workflow-name]/requirements.md`). **Resume orientation:** if the user arrived via "continue my workflow" or with no stated workflow, check `registry/workflows/` for existing Workflow nodes (if several, list them) and infer progress from which artifacts each node's `# Artifacts` section already links — "You've completed through Step [N] ([name]) — next is Step [N+1]" — and if Design isn't the next step, say so and route to the right skill instead of re-running finished work. If the user specifies a file path, use that. If no Workflow node exists yet, scan for a requirements file before giving up: legacy flat files (`outputs/[name]-requirements.md`), the most recent Workflow Requirements anywhere under `outputs/`, and requirements-like `*.md` files at the workspace root. When you find one, offer to link it from the Workflow node's `# Artifacts` — moving the file into `outputs/[workflow-name]/` is optional tidiness, not something the framework requires.

**Verify the requirements file exists and is parseable before relying on it.** If the file is missing, stop and tell the user — don't proceed against a path that doesn't resolve. Confirm the required headings exist (Goal — accept the legacy heading `Outcome` in older files — Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, and either Steps Overview/Step Details or the goal-driven Inputs/Rules & Constraints). If any are missing or mis-named, **say exactly which are missing** and ask the user to re-run `/deconstruct` or fix the file — don't guess at the contents.

Read the `Definition Type` field from the Metadata table. If `Goal-Driven` (or the legacy value `Outcome-Driven` — treat it as `Goal-Driven`): **STOP — read `references/goal-driven-path.md` now, in full, before proceeding.** It modifies Steps 3–9 and the spec template; do not run the goal-driven path from memory. If `Step-Driven` (or no Definition Type field is present), use the standard step-driven path below.

#### Step 2 — Confirm Understanding

For step-driven requirements: Summarize the workflow name, step count, and goal (from the Goal section of the Workflow Requirements — legacy files title it Outcome). Ask the user to confirm before proceeding.

For goal-driven requirements: Summarize the workflow name, goal, and the headline rules and constraints (from the Goal and Rules & Constraints sections). Ask the user to confirm before proceeding.

#### Step 3 — Architecture Decisions

Before assessing autonomy and orchestration, gather the information needed to make platform-aware recommendations. The approach: **one question, then extract everything else from the Workflow Requirements.**

**a. One question: Where will you use this?**

Platform is the only thing not already in the Workflow Requirements. This question is **always asked or confirmed explicitly in plain language** — never skipped, even when the platform seems obvious from earlier conversation. Most users are non-technical; do not assume they remember saying which tool they use.

**Detect before asking.** First identify the environment this session is running in (Claude Code, Cowork, Claude.ai, ChatGPT, …) from the session context. Most people run a workflow in the same tool they design it in, so when the current platform is identifiable, present it as the recommended default instead of asking cold — use `AskUserQuestion` with the current platform first, marked "(Recommended)":

> "You're designing this in **[current platform]** — most workflows run where they're designed. Run it there too, or somewhere else?"
>
> *(Options: [current platform] (Recommended) · 2–3 other common options from the platform registry · the built-in "Other" escape hatch.)*

Designing in one tool and deploying to another is a legitimate pattern (e.g., building in Cowork a workflow a teammate will run in ChatGPT) — that's what the other options are for; don't silently assume the current platform.

Only when the current environment can't be determined, fall back to the open question — a short list of the most common options pulled from the platform registry (do not list every offering — keep it to 3–4 choices plus "Other"). Example phrasing:

> "Where do you want to use this workflow? Tell me the AI tool you use day-to-day — for example, ChatGPT in your browser, Claude in your browser, Claude Code in your terminal, or something else."
>
> *This decides where the final workflow lives and what format I'll build it in.*

**Mapping the answer to a specific offering — done internally, not asked of the user.** When the user names an ecosystem that maps to multiple offerings (e.g., "Claude" → Claude.ai, Claude Code, Claude Agent SDK, Cowork), pick the **single best default for a non-technical user** (the browser/no-code option in almost all cases — e.g., "Claude" → Claude.ai; "Google" → Gemini web; "OpenAI" → ChatGPT) and confirm back in plain language with an easy correction path:

> "Got it — I'll design this for **Claude.ai** (the browser app you sign into at claude.ai). If you actually meant Claude Code in your terminal, or something else, say so and I'll switch."

Only default to a code-mode offering (Claude Code, Codex, Gemini CLI, an SDK) when there's strong signal in the conversation that the user is writing code. Never ask a non-technical user to disambiguate between technical artifact forms — that's the model's job.

**What this resolves for downstream steps:**
- **For Design:** The specific offering (e.g., Claude.ai vs. Claude Code) drives the mechanism options and the artifact form the model resolves internally.
- **For Build:** Generation maps directly from the platform + mechanism the model recorded — no re-asking the user about artifact form.

**b. Extract everything else from the Workflow Requirements**

After confirming the platform, read the Workflow Requirements and extract:

- **Tool integrations** — from per-step Inputs, Context Needed, and the Context Inventory. Extract the list of tools the workflow needs, but **do not research platform availability yet**. That happens in Build. Simply list the tools identified.

- **Trigger/schedule** — from the Metadata table. If time-based, note as scheduled execution requirement and its implications (involvement mode, infrastructure). If manual, no action needed.

- **Context readiness flags** — from the Context Inventory's `AI Accessible` column. Summarize items flagged as `Partial` or `No` — these may be structured data, but also documents, transcripts, or reference materials that aren't AI-accessible. These inform step classification — a step that depends on inaccessible context may need:
  - A prerequisite human step prepended (e.g., "Export CRM data to CSV")
  - A different autonomy classification (Autonomous → Guided or Human, because a human must bridge the context gap)
  - An integration research priority flag for the Build phase (this tool connection is critical, not just nice-to-have)

- **Browser access** — deferred to Build. If any step's Data In references a web portal, CRM login, or authenticated website, flag it during step classification (Step 6) as a "requires browser access" note on that step. Do not ask about it here.

- **Shareability** — deferred to Build. The model asks about team sharing when generating artifacts in the Build phase, not during Design.

**c. Present architecture analysis for confirmation**

Present a single confirmation block:

> "Here's what I found in your Workflow Requirements:
> - **Platform:** [confirmed platform]
> - **Tools needed:** [extracted list]
> - **Trigger:** [extracted trigger] → [implications for involvement mode]
> - [Any flags: e.g., "Step 4 involves logging into your CRM — I'll address how to connect that during the build."]
> - **Context readiness:** [count] of [total] context items are not directly AI-accessible. [Brief summary of gaps — may include structured data, documents, transcripts, or reference materials]. These gaps may affect step autonomy and will need resolution before or during Build.
> - [Organizational lens: stakeholder implications — different platform access levels, notification needs for handoffs, shareability defaults to "yes"]
>
> Integration availability on [platform] will be researched during the Build phase.
>
> Anything I missed or got wrong?"

**d. Downstream propagation — architecture decisions gate subsequent steps:**
- No-code platform + no built-in connectors → cap at Skill-Powered Workflow
- Scheduled trigger + platform doesn't support unattended runs → flag infrastructure needed
- State which extracted facts influenced the autonomy assessment and orchestration mechanism recommendation
- **Capability check:** when a design decision depends on a platform capability (agent files, skills, memory, scheduled/unattended runs), check the platform's entry in the cached registry — the presence or absence of capability keys (`agent`, `skill`, `memory`, `project`) signals support, and the entry's `notes` field carries platform quirks (e.g., install paths). If a needed key is absent or you're uncertain, do a single targeted web check **now** rather than shipping a spec Build can't honor; record it in Deferred to Build only if genuinely deferrable. **If the platform has no registry entry at all**, don't run a separate web check per decision — do **one consolidated** capability check (a single web lookup covering agents, skills, scheduling, and file access), record the findings in the spec so Build can reuse them, and leave all further platform doc-reading to Build (Step 3.6).

**Packaging is determined later, in Step 5.** Once the mechanism is selected, Step 5 proposes a Packaging value based on platform and mechanism (e.g., single skill → Standalone Skill; agent + skills on ChatGPT → Workspace Agent). Do not ask about Packaging during Step 3 — it depends on Step 5's mechanism decision.

#### Step 4 — Autonomy Assessment

Before choosing an orchestration mechanism, assess where the *whole workflow* sits on the autonomy spectrum. This is the same spectrum used for per-step classification (Step 6), applied at the workflow level.

**The autonomy spectrum:**

```
Human ———— Deterministic ———————— Guided ———————— Autonomous
(human-performed)  (fixed path)       (bounded decisions)     (context-driven path)
```

| Level | Signals | Orchestration implications |
|-------|---------|--------------------------|
| **Human** | Step requires human judgment, creativity, or physical action; AI cannot perform | No AI artifact — captured as Human step in the Decomposition table |
| **Deterministic** | Steps always execute in the same order, no branching on output quality, failure = stop or retry same step | Prompt or skill-powered workflow likely sufficient |
| **Guided** | Some steps involve bounded AI judgment, human steers at checkpoints, sequence is mostly fixed but with bounded flexibility | Skill-powered workflow or agent |
| **Autonomous** | Executor backtracks, re-invokes based on feedback, adjusts approach on failure, human checkpoints can redirect flow | Agent required |

**Present as a confident assessment with a teaching frame.** For most users this is the first time they're hearing the word "autonomy" in this context — introduce the concept briefly before applying it, so the playback educates rather than labels. Example phrasing:

> "Now I want to assess how much **autonomy** this workflow needs. Autonomy is just *how much room the AI has to decide what to do next* — it runs on a scale from Human (you do all the work) → Deterministic (AI follows a fixed script) → Guided (AI works, you steer at checkpoints) → Autonomous (AI figures out its own path).
>
> Your workflow looks **[level]** because [1-2 sentence reasoning tied to specific traits of their workflow — e.g., 'each step always runs in the same order and there's no branching based on the AI's output' for Deterministic, or 'the AI generates a draft and you decide if it's good enough to send' for Guided].
>
> *Why this matters:* the autonomy level shapes what kind of AI building block fits best — a fixed script needs less machinery than something that has to make its own decisions.
>
> Does that match how you want it to work? If you'd rather it be more or less autonomous, say so and I'll adjust."

If the user disagrees, discuss and adjust. The autonomy level chosen here drives the mechanism recommendation in Step 5.

#### Step 5 — How should this run? (Mechanism)

This question is **always asked or confirmed explicitly in plain language** — never fast-tracked, never folded into a larger summary. Most users are non-technical; do not assume they understand the difference between a "prompt", a "skill", and an "agent" without plain-language framing.

**Internal mapping (model-only — do not show this table to the user):**

| User-facing label | Internal mechanism | When it fits |
|---|---|---|
| Step-by-step prompt | `Prompt` | One-off workflow, user copy-pastes instructions and runs them manually |
| Reusable skill | `Skill-Powered Workflow` | Repeated workflow with similar inputs, user triggers by name when needed |
| Agent | `Agent` | Tool use, autonomous decisions, multi-step reasoning, or scheduled/unattended runs |

**How to present this to the user — recommendation first, then alternatives.** Pick the best fit based on the autonomy assessment and how often the workflow will run, then use `AskUserQuestion` with three plain-language options (recommended option first, marked "(Recommended)"). Example phrasing for the question text:

> "Now the big choice: **how do you want to run this workflow day-to-day?** There are three common shapes — I'll explain each, then recommend the one that fits you best.
>
> - **Step-by-step prompt** — A set of instructions you copy and paste into your AI tool each time. Lowest setup, no install. Best for one-off workflows you won't repeat often.
> - **Reusable skill** — A saved set of instructions you trigger by name (e.g., 'run the weekly review skill'). The AI loads them automatically when the situation matches. Best for workflows you'll run repeatedly with similar inputs.
> - **Agent** — A system that drives the whole workflow end-to-end on its own, calling tools and making decisions as it goes. Best when you want it to run on a schedule, handle decisions autonomously, or coordinate multiple steps without you in the loop.
>
> Based on your [autonomy level] workflow and the fact that [1-sentence signal from the workflow — e.g., 'you'll run this every Friday'], I recommend **a reusable skill**.
>
> *Why this matters:* this choice shapes the file the next step actually builds — a prompt is just instructions you keep handy, a skill is a saved capability the AI can invoke by name, and an agent is a system with its own decision-making. Each fits a different way of working.
>
> Which shape works for you?"

Use `AskUserQuestion` with three options whose labels mirror the three shapes above (one-line versions of the same descriptions), recommended option first and marked "(Recommended)".

If the user pushes back, discuss in plain language — never drop into the internal jargon (`Prompt` / `Skill-Powered Workflow` / `Agent`) when talking to them.

**Artifact form is resolved internally, not asked.** Once platform + mechanism are confirmed, the model picks the specific artifact form (e.g., a SKILL.md file, a Claude Code subagent markdown, an Agent SDK Python script, a ChatGPT Workspace Agent) using the platform's `mode` field in the registry (`code` vs `guided`) and the user's apparent technical level. Default to the simplest no-code option for that platform. **Never ask a non-technical user to pick between technical artifact forms.** Build generates the right artifact from the platform + mechanism the model recorded.

**Human Involvement — derive internally, mention only as plain language.** Determine the involvement mode (`Augmented` vs `Automated`) from the trigger (manual = Augmented; scheduled/unattended = Automated). Mention it to the user in plain language as part of the Layer 1 confirmation ("Who's in the loop") — do not ask a separate question.

Single-agent vs. multi-agent is an architecture detail decided during Agent Configuration (Step 8) if Agent is selected — not a top-level choice here.

**Who is the orchestrator? (read before designing any Agent workflow.)** On **Claude Code or Cowork — any platform with a primary agentic loop — the primary session IS the orchestrator.** Do **not** design a separate "orchestrator agent" file. What you build are:
- **Orchestration logic** — captured as an **orchestrator skill** (`disable-model-invocation: true` for a user-triggered workflow; **no `context: fork`** — it must run in the primary loop so it can dispatch sub-agents) and/or a `CLAUDE.md` run section the primary loop follows (scan/classify/dispatch/label/summarize, etc.). This is not an "agent" artifact. **Prefer a skill over a legacy slash command:** custom commands are merged into skills, so a skill still invokes as `/name` but adds portability (agentskills.io), distribution via skill tooling, and a supporting-files directory. **Naming convention:** the orchestrator skill takes the **workflow name**; component/worker artifacts (synthesizers, researchers, etc.) take **capability-specific names** — so the one user-facing entry point never collides with a sub-skill (a same-named skill silently shadows everything else, including any command).
- **Sub-agent(s)** — the workers the primary loop dispatches, one per unit of work (e.g., per item in a batch). Sometimes **zero** sub-agents are needed — the orchestration logic + skills are enough. **Scope note:** this command→skill change applies to the *orchestrator* only; fan-out workers stay as sub-agents (`.claude/agents/*.md`).

The agent artifacts you generate are always the **workers the orchestrator delegates to**, never the orchestrator itself. Reserve a standalone, self-running "agent" artifact for **SDK platforms** where you deploy the agent process yourself. (This is the single most common design mistake on Claude Code: inventing an orchestrator agent when the primary loop already is one.)

**Fast-track for complete Workflow Requirements:** If the Workflow Requirements + conversation context provide enough information to resolve the autonomy level, tool extraction, and step classifications, you may present those internal/technical dimensions as a single summary block instead of stepping through questions one at a time.

**Platform (Step 3a) and Mechanism (Step 5) are never fast-tracked.** They are always asked or confirmed explicitly in plain language, in their own discrete confirmations, even when the answer seems obvious from earlier conversation. Non-technical users must see and approve these two choices on their own — they should not be embedded inside a larger summary block.

**Packaging decision:** Pick the Packaging value from platform + mechanism (single skill → Standalone Skill; multiple related artifacts → Plugin; ChatGPT with agent + skills → Workspace Agent; ad-hoc files → Loose Files). **Cowork rule:** if the platform is Cowork and the design includes any worker sub-agents, Packaging is **Plugin** — Cowork runs custom agents only from installed plugins, so a Standalone Skill can't carry them; Standalone Skill applies to skill-only designs. Include the decision in the playback below — but always pair the technical label with a plain-language explanation so the user learns what it means.

#### Step 5b — Safety & Permissions pass

Before confirming Layer 1, walk four safety questions. This matters most when the workflow writes to live systems, runs unattended, or consumes content the user didn't author — exactly the workflows non-technical users are most likely to deploy and forget. Keep it plain-language and proportionate; for a read-only, human-triggered workflow this is one sentence, not an interrogation.

1. **Write access** — Which connected tools can this workflow *create, modify, or send* through? Apply least privilege: the workflow should request only the scopes it needs, and prefer draft-don't-send (create the draft, let the human send) until trust is established.
2. **Untrusted input** — Does any step process content the user didn't author (inbound email, web pages, form submissions, shared docs)? If yes, that content must be treated as *data, never as instructions* — the workflow must not follow directives that arrive inside the content it processes, and should flag suspicious embedded instructions to the user.
3. **Unattended runs** — Will this run on a schedule or without a human watching? If yes: human gates on outward-facing actions, a cap on actions per run, and a log of every write.
4. **Blast radius** — What's the worst realistic outcome of a bad run? Place a human gate in front of the highest-consequence action, or constrain it to drafts/test targets.

**Write-action feasibility check (required when the workflow writes to an external system).** The four questions above scope *how much* write access to request; this one asks whether the required action is **possible at all** on the chosen platform. For each write/action the workflow needs — read them from the Workflow Requirements (the `External Action` fields in Step Details for step-driven; the goal, rules, and acceptance for goal-driven) — verify the chosen integration can actually perform it. Use the capability-check mechanism from Step 5 (registry lookup + a single targeted web check) — this is exactly the "check now rather than ship a spec Build can't honor" case. Distinguish two gap types:

- **Scope gap** — the connector *supports* the action but may not be authorized yet (fixable by reconnecting/authorizing at Build). Note it and move on.
- **Capability gap** — the connector has **no such capability at all** (e.g., a read-only CRM connector with no create-deal tool). This is *not* fixable by reauthorizing, and it can invalidate the design. Flag it plainly and present **platform-aware options**, in this order:
  1. **Human-in-the-loop gate (recommended default)** — the AI prepares the change (drafts the record/message) and a human commits it in the target system. This works on *every* platform and is the safe default; recommend it first, especially on platforms without shell/code access.
  2. **A different connector/integration** that has the capability.
  3. **CLI or API fallback** — *only* where the platform has shell or code access. Say explicitly that this is **unavailable on Cowork and most chat surfaces**, so don't offer it there.
  4. **Descope the action** — drop or defer it from the workflow.

Never **hard-block** the spec on a capability gap: surface it loudly, let the user pick a path, and record the decision in the spec's **Safety & Permissions** section so Build honors it. A gap the user knowingly accepts (e.g., "I'll commit deals by hand for now") is a valid, recorded choice — not a blocker.

**Then reconcile against the constraints the business already stated.** The Workflow Requirements' `Security, Privacy & Safety` section carries constraints in the words the business used, each with a source. Build the spec's **Constraint Conformance** table: for every constraint, name the design decision that meets it and mark it `Satisfied`, `Accepted` (not met, deliberately — record a named owner and the reason), or `Open` (surfaced, not yet decided).

**Nothing here blocks the spec.** Never hard-block on a constraint: surface it, let the user pick a path, and record the decision. What is enforced is that no constraint stays silent — Layer 1's confirmation names each `Open` one in plain language and asks the user to resolve it to `Satisfied` or `Accepted` before Layer 2.

**If the Workflow Requirements has no `Security, Privacy & Safety` or `Value & Measurement` section**, it predates this format. That is not the same as having no constraints, and must never be read that way. Such a document also lacks the Context Inventory's `Sensitivity` and `Provenance` columns, so you cannot derive anything from it — ask the user directly:

- Does this workflow write to anything live — send, post, create, or change something in a real system?
- Does it use content nobody on their team wrote — inbound mail, web pages, form submissions, shared documents?
- Does it handle data they'd be uncomfortable seeing outside the company?

If any is yes, capture the constraints as you would from the section. Record each one's source as `captured at Design — requirements predate this section`, so a reader can tell a constraint the business stated during Deconstruct from one reconstructed later.

Do the same for `Value & Measurement`: ask for the objective, the desired outcome, what gets counted, today's number, and the target. A baseline reconstructed here is far more likely `Estimated` or `Unknown` than one captured while the as-is was fresh — record it honestly rather than rounding up.

Present findings in plain language as part of the Layer 1 confirmation below ("Safety: this workflow can create drafts in your email — it will never send without you"). Record them in the spec's **Safety & Permissions** section (see the template). If untrusted input meets write access with no human gate between them, say so plainly and recommend one — that combination is how prompt-injection incidents happen.

**Layer 1 confirmation — hard gate, rich playback in plain English** (after Step 5b, before moving to Step 6):

This is a **hard gate**. Do not proceed to Step 6 without explicit user approval here. This is also a **teaching moment** — play back the full design analysis so the user can see and learn the building blocks involved, not just rubber-stamp a stripped-down summary.

By this point the user has already confirmed *where* (Step 3a) and *how it runs* (Step 5) in their own discrete confirmations. This gate plays the full architecture analysis back so they can verify, learn the vocabulary, and redirect anything that's wrong before any detailed decomposition work begins.

**How to write the playback:** Use the technical term, then immediately explain it in plain language in the same line. Never drop a bare technical label on its own. Every row teaches as it confirms.

For step-driven workflows:

> "Here's the design analysis based on your workflow definition. I'll explain each piece as I go — push back on anything that's off:
>
> - **Platform:** [Claude.ai] — the [browser app you sign into at claude.ai]. This is where your workflow will live.
> - **Packaging:** [Standalone Skill] — a [single self-contained set of instructions you upload once and reuse]. (Other options: Plugin, Workspace Agent, Loose Files — yours is Standalone Skill because [reason].)
> - **Autonomy level:** [Guided] — meaning [AI handles most of the work, you steer at key checkpoints]. (The scale runs Human → Deterministic → Guided → Autonomous.)
> - **Mechanism:** [Skill-Powered Workflow] — the [reusable skill you confirmed in the last step]. Runs in [Augmented] mode, which means [you're in the loop reviewing at checkpoints, not running on a schedule].
> - **Safety:** [one-line summary of the Step 5b findings — e.g., 'this workflow can create drafts in your email; it never sends without your review']
> - **Tools needed:** [list] — these are the external services your workflow will touch. I'll figure out exact integration options (MCP server, API, CLI, SDK) during Build.
> - **Steps classified:** [N steps — brief summary, e.g., '6 steps: 2 use AI directly, 3 are reusable skills, 1 is a human review']
> - **Skill candidates:** [list of skill names you'll be building, with one-line purpose each]
> - **Agent blueprints:** [summary if any agents are involved, or 'None — this workflow doesn't need an agent']
>
> Is this right? If yes, I'll work out the step-by-step details next. If anything's off — even small wording — tell me what to change."

For goal-driven workflows, use the playback substitutions in `references/goal-driven-path.md`.

**Wait for explicit approval** ("yes", "looks good", "go ahead", etc.) before moving to Step 6. If the user pushes back, revise the relevant decision (which may mean reopening Step 3a or Step 5) and re-present this gate.

**Why every row pairs jargon + plain English:** The Design skill is also an *education* tool. Users who run it repeatedly should start recognizing terms like "Standalone Skill", "Augmented", "Guided" — but only because they've seen them explained in context, not because they were dumped on them as labels. This playback is where that learning happens.

#### Step 6 — Classify Each Step

For every refined step, classify across all three building-block layers plus autonomy and role.

**Per-step classification dimensions:**
- **Autonomy level**: Human / Deterministic / Guided / Autonomous — use only these four canonical terms. Previous terms like "Semi-Autonomous", "AI-Assist", "AI-Deterministic", or compound forms are retired per the Workflow Design Matrix.
- **Orchestration layer**: Prompt / Skill / Agent
- **Integration layer**: Which integration block(s) apply, with use/build tags
- **Intelligence layer**: Model capability, context sources, memory needs, project scope
- **Human-in-the-loop gates**: Where human review is recommended
- **Role** (organizational lens): Who performs this step — which role owns it

**Integration layer blocks:**

| Block | Description | Tag |
|-------|-------------|-----|
| **MCP** | Model Context Protocol server | Use existing / Build new |
| **API** | REST, GraphQL, or other web API | Use existing |
| **SDK** | Client library / framework | Use existing / Build new (rare) |
| **CLI** | Command-line tool | Use existing |

Most integration blocks are "use existing." "Build new" applies primarily to MCP (custom data sources) and rarely to SDKs.

**Plain-language gloss (for non-technical users — explain these the first time they come up):**
- **MCP** = a plug-and-play connection to a service, no coding needed.
- **API** = a way to talk to a service that needs a little code/setup.
- **SDK** = a coding toolkit (most technical option).
- **CLI** = a command you run in a terminal.

**Intelligence layer blocks:**

| Block | Description | Per-step classification |
|-------|-------------|----------------------|
| **Model** | Which model capability | Reasoning-heavy / Fast / Vision |
| **Context** | Files, docs, libraries needed | List specific sources |
| **Memory** | Persistent state across runs | Yes / No + what's stored |
| **Project** | Workspace or project scope | Yes / No |

**Per-step classification table format:**

| Step | Orchestration | Integration (use/build) | Intelligence | Human Gate |
|------|--------------|------------------------|--------------|------------|
| Pull calendar events | Skill | MCP: Google Calendar (use) | Model: fast | No |
| Generate coaching questions | Agent | — | Model: reasoning; Context: powerful-questions.md | Yes |
| Save prep notes | Skill | CLI: git (use) | Model: fast | No |

Each row captures one step. The Orchestration column shows the block from that layer. The Integration column lists block(s) with use/build tags, or "—" if the step needs no external tool access. The Intelligence column lists applicable blocks with their per-step classification values.

Additionally, for each step record the **autonomy level** and **role** (these appear in the full spec output but are omitted from the compact table above for readability).

If a step's inputs include items flagged as "No" or "Partial" in the Context Inventory, note this in the classification. A step classified as Autonomous but dependent on inaccessible data should be flagged: "Autonomy contingent on resolving data access for [item]."

Present the mapping as a clear table. Walk through reasoning for non-obvious classifications. Ask if the user wants to adjust anything.

**Integration Discovery**

After classifying every step, recommend available integration options for each tool need identified in the Integration layer. This helps students who don't know what CLIs, APIs, MCP servers, or SDKs exist for a given tool.

**Discovery process (4-part chain):**

1. **Curated tool catalog** — Resolve the platform registry **local-first**: if this skill is installed as part of the handsonai plugin, read the local copy at `${CLAUDE_PLUGIN_ROOT}/registries/platform-registry.json`; otherwise (standalone install) fetch the remote copy from `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`. Cache whichever copy you load for the rest of the session. Match workflow tool needs against each `curated-tools` entry's `integrations` field. Curated tools are instructor-vetted recommendations — present them first, marked as recommended.

2. **Model knowledge** — Supplement with additional integration options the model knows about. For well-known integrations (Google Calendar, Gmail, Slack, GitHub, etc.), skip web search — model knowledge is sufficient.

3. **Integration registries** — Read the `integration-registries` list from the same cached registry JSON. For each cataloged source, search for integrations matching the tool need:

   ```json
   {
     "integration-registries": [
       {
         "name": "Context7",
         "type": "mcp",
         "tool": "query-docs",
         "notes": "Library docs, API references, SDK docs via MCP"
       },
       {
         "name": "context-hub",
         "type": "local",
         "check": "context-hub --version",
         "notes": "Community-maintained integration registry (CLI)"
       },
       {
         "name": "MCP Registry",
         "type": "web-search",
         "url": "https://mcpregistry.dev",
         "notes": "MCP server directory"
       }
     ]
   }
   ```

   **MCP tool availability:** Before querying an MCP-type registry source (e.g., Context7), check the user's configured MCP servers. If the required MCP server is not configured, skip it and proceed to the next source in the chain.

4. **Web search (validation + fallback)** — For less common tools, when uncertain, or when no match is found in prior steps, search the web to verify existence and find current docs. Catches new releases and uncataloged tools. Batch searches when multiple tool needs are identified to avoid latency.

   **Latency management:** Use judgment about when web search adds value. Well-known integrations (Google Calendar, Gmail, Slack, GitHub) don't need validation searches. Reserve web search for new or niche tools.

   **Precedence rule:** When web search results contradict model knowledge (e.g., model proposes an MCP server that web search reveals was deprecated), web search takes precedence. Flag the discrepancy and present only verified options.

**Fallback ladder (never hard-fail).** Any of the lookups above can fail — the local registry may be absent (standalone install), the remote JSON may be unreachable, or web search may be unavailable on the platform. Degrade gracefully in this order, and tell the user what was degraded: **local plugin copy** → **session cache** → **remote fetch** → **model knowledge** → **web search** → **best-effort note**. If you end on model-knowledge-only or best-effort, add a one-line flag like "Integration options below are unverified (registry/web unavailable) — confirm before relying on them." Never block Design because a fetch failed.

**Matching semantics:** Matching is model-driven, not exact string matching. The model reads the workflow's tool needs (e.g., "Google Calendar access" from the step classification) and matches them against the `integrations` array values (e.g., `"google-calendar"`) using semantic understanding. This allows natural language tool needs to match standardized integration tags without requiring exact normalization.

**Presentation format:**

For step-driven: `**[Tool] access needed (Steps N, M):**`
For goal-driven: `**[Tool] access needed (Domains: X, Y):**`

> **[Tool] access needed ([Steps N, M / Domains: X, Y]):**
>
> **Curated (recommended):**
> | Block | Option | Source URL | Trade-off |
> |-------|--------|-----------|-----------|
> | MCP | [Name] MCP | [URL] | Easiest — plug-and-play |
> | CLI | [Name] CLI | [URL] | Good for automation/scripting |
>
> **Also available:**
> | Block | Option | Source URL | Trade-off |
> |-------|--------|-----------|-----------|
> | API | [Name] REST API | [URL] | Most flexible, more code |
> | SDK | [Name] Client Library | [URL] | Best DX for code-heavy builds |
>
> (Capture the Source URL during discovery — the spec's Integration Options section requires at least one per tool; never backfill or fabricate URLs at assembly time.)
>
> *Recommendation: [block] for [rationale]*

**Layer 2 confirmation moment** (after Step 6, before Skill Discovery and Component Blueprints):

The decomposition is complete. Before generating detailed component blueprints (the most expensive work to redo), confirm the L2 decisions are right:

> "Decomposition confirmed:
> - **Steps requiring new skills:** [count] — [list step IDs and proposed skill names]
> - **Steps using existing skills:** [count] — [list step IDs and existing skill names]
> - **Steps as inline prompts:** [count] — [list step IDs]
> - **Steps requiring agents:** [count] — [list]
> - **Human-performed steps:** [count] — [list]
>
> Moving to Layer 3 — Component Blueprints. I'll write the field-level spec for each new skill and agent. Confirm to proceed, or push back on the decomposition."

If the user pushes back, revise the L2 decomposition (and possibly L1 if the disagreement is architectural). Re-confirm before proceeding. Like the L1 confirmation, this is lightweight — not a hard gate — but it's the last cheap moment to catch decomposition mistakes before the detailed spec work.

#### Step 6b — Skill Discovery

For every step classified as needing a **Skill** in Step 6, search for existing skills before assuming one needs to be built.

**Search order:**

1. **Local skills and prior workflows** — Search the user's own `.claude/skills/`, plugin skills directories, and any project-level skill directories. Also read the workspace `REGISTRY.md` (if present) and the Skill Candidates sections of prior workflows' `outputs/*/design-spec.md` — skills the user built for earlier workflows are prime reuse candidates. All of these are pre-vetted and can be recommended directly.

2. **External registries** — Read the `skill-registries` list from the platform registry (same local-first resolution and session cache as Integration Discovery above: plugin-local copy at `${CLAUDE_PLUGIN_ROOT}/registries/platform-registry.json` first, remote fetch for standalone installs).

   This provides a curated, always-current list of sites to search. For each registry, search for skills matching the step's requirements.

   ```json
   {
     "skill-registries": [
       {
         "name": "skills.sh",
         "type": "web-search",
         "url": "https://skills.sh",
         "notes": "Community skill marketplace"
       },
       {
         "name": "Context7",
         "type": "mcp",
         "tool": "query-docs",
         "notes": "Library docs and skills via MCP"
       }
     ]
   }
   ```

   New registries are added by pushing to the JSON file — all users get them on their next plugin update (or immediately on standalone installs that fetch the remote copy).

3. **Web search fallback** — If no match found in cataloged registries, or if the registry fetch fails, search the web for community skills that could fulfill the step. This also catches new skill registries not yet in the catalog.

4. **User approval gate** — Present all discovered skills as **candidates**, clearly separated into:
   - **Local (pre-vetted):** Skills the user already has installed. Can be included in the spec with a confirmation.
   - **External (requires vetting):** Community skills from registries or web search. Flag security implications — these run with the model's permissions and should be reviewed before adoption. User must explicitly approve each external skill candidate before it's included.

**Presentation format:**

For each step (or capability domain, for goal-driven workflows) that needs a skill, present candidates in a table:

> **[Step 3 / Domain: Research] needs a skill: "Format coaching prep notes"**
> | Source | Skill | Status |
> |--------|-------|--------|
> | Local | `coaching-prep-notes-assembly` (your plugin) | Pre-vetted — include? |
> | Registry | `summarizing-transcripts` (from your `weekly-review` workflow) | Pre-vetted — include? |
> | skills.sh | `markdown-document-builder` by @community | Requires review — [link] |
> | Web search | `doc-formatter` on GitHub | Requires review — [link] |
> | None found | Build new | Fallback |
>
> *External skills run with model permissions. Review source code before approving.*

If no suitable existing skill is found for a step, tag that step as **"build new"** — it flows into Step 7 (Identify Skill Candidates).

#### Step 7 — Identify Skill Candidates

For steps where Skill Discovery (Step 6b) found an existing skill, skip to the next step.

This step only applies to steps tagged **"build new"** in Step 6b. Tag those steps that should become skills.

**Draft, then confirm — do not interview field-by-field.** You have already read the Workflow Requirements and run the whole design conversation; that contains almost everything these fields need. For each skill candidate, **draft all 12 fields yourself**, present the completed blueprint for correction ("Here's my draft of the [name] skill — what's wrong or missing?"), and ask direct questions only for fields you genuinely cannot infer (typically Decision Logic details, Failure Mode preferences, or constraints the user hasn't voiced). Never walk a user through 12 questions per skill.

**Scope each skill as a reusable capability, not a workflow fragment.** Name it for the capability in gerund or verb-object form (`summarizing-transcripts`, `formatting-prep-notes` — never `step-3-helper` or `[workflow-name]-part-2`); avoid vague names (`helper`, `utils`, `documents`) and the reserved words `anthropic`/`claude`. Write Inputs as parameters, not hardcoded references to this workflow's files, so the skill still works when invoked outside this workflow. Check that no name collides with a skill found in Step 6b — a duplicate name silently shadows the existing one. Only the orchestrator skill carries the workflow's name; every component skill is capability-named.

The 12 fields (field-by-field format in `references/spec-template.md`):

- **ID** — stable skill ID (S1, S2, …)
- **Name** — lowercase-hyphenated, ≤64 chars, no consecutive hyphens; matches the skill directory name; capability-named per the scoping rule above
- **Description** — ≤1024 chars, MUST start with "This skill should be used when..." — verbatim text for the SKILL.md frontmatter; drives auto-activation. Write in **third person** (never "I" or "you" as the actor), and name the **concrete trigger contexts and keywords** a user would actually say (tool names, file types, task verbs) plus what the skill does — a vague description kills auto-activation. Where confusion with a sibling skill is likely, add a "Do not use for…" clause
- **Purpose** — one-sentence internal summary for the spec reader
- **Covers Steps / Domains** — which step IDs (or capability domains) this skill spans
- **Inputs** — what the skill receives
- **Outputs** — what the skill produces
- **Decision Logic** — key rules, criteria, evaluation frameworks
- **Failure Modes** — condition → action, one per line
- **Required Tools** — integration blocks the skill needs at runtime (e.g., MCP: HubSpot)
- **Depends On** — other skill IDs (S2, S3) or artifacts that must exist first, or "None"
- **Stateful?** — Yes / No, does the skill maintain state across invocations? Drives Memory building-block decisions.

**Consolidation sweep (before presenting blueprints — no user question):** sweep the candidate list once. **Merge** candidates that are the same capability applied at different steps into one skill with multiple Covers Steps entries (the step-driven mirror of the goal-driven altitude rule). **Split** any candidate whose Decision Logic spans two unrelated capabilities — each skill should excel at one thing. Note each merge/split in one line when presenting the blueprints.

#### Step 8 — Agent Configuration

(When orchestration mechanism is Agent.) **Same draft-then-confirm approach as Step 7:** draft all 14 fields for each agent from the requirements and conversation, present the completed configuration for correction, and interview only for what you cannot infer (typically Tone & Style and Constraints). The 14 fields (field-by-field format in `references/spec-template.md`):

| Field | What to specify |
|-----------|----------------|
| **ID** | Stable agent ID (A1, A2, …) |
| **Name** | Unique agent name (lowercase-hyphenated, matches the agent filename without extension) |
| **Description** | ≤1024 chars, MUST start with "Use this agent when..." — verbatim text for the agent file frontmatter; drives invocation. Third person; name the concrete trigger contexts and keywords that should route work to this agent |
| **Mission** | One-sentence primary purpose |
| **Responsibilities** | Bulleted list of what the agent does once invoked |
| **Output Format** | Structured description of what the agent's output should look like. For workers dispatched by an orchestrator, this is the **handoff contract** — prefer a structured summary over free prose |
| **Tone & Style** | Voice and register (e.g., "concise, technical, no hedging") |
| **Constraints** | Must-not-dos, scope boundaries, source restrictions. For Autonomous agents, include a bound on iterations/actions per run (Build maps it to `maxTurns` or the platform equivalent) |
| **Failure Modes** | Condition → action, one per line — including what the agent returns to its orchestrator when it cannot complete (mirrors the skill blueprint field) |
| **Model** | Capability tier: reasoning-heavy / fast / vision |
| **Memory Scope** | user / project / local / none — cross-session learning scope. **Heuristic:** default `none`; choose memory only when the workflow genuinely benefits from cross-run state (tracking an entity over time, learned user preferences). **Avoid memory for research/freshness workflows** — stale recall becomes a liability when each run should re-gather current data. When the "learning" should be human-visible/editable, prefer a curated **context file** over opaque agent memory. If the platform's registry entry has no `memory` capability key, choose `none` or a context file. |
| **Tools** | External tools the agent needs (reference Integration Options entries by tool name). **Least privilege:** list only tools the Responsibilities require — a read/analyze agent gets no write tools — and stay consistent with the Step 5b write-access findings |
| **Skills** | Skill IDs the agent has access to (S1, S2, …) |
| **Trigger Examples** | 2-3 structured examples (context → user message → expected behavior → invocation) — Build uses these verbatim as `<example>` blocks in the description |

The build skill maps these to platform-specific fields at runtime (e.g., "reasoning-heavy" → the platform's current top reasoning model, which Build resolves via web search at generation time; trigger examples → `<example>` blocks).

For multi-agent: orchestration pattern, agent handoffs, human review gates — see the Multi-Agent Configuration section in `references/spec-template.md`.

#### Step 8b — Verify Evaluation Inputs

The Workflow Requirements already includes **Acceptance Criteria** (what good looks like, dimensions that matter, minimum bar) and **Example Scenarios** (3-5 representative inputs with what to look for, plus Golden Examples where the user supplied them) from the Deconstruct step. Do **not** ask the user to re-state these.

Confirm them briefly:

> "Your Workflow Requirements includes Acceptance Criteria and [N] Example Scenarios ([M] with golden examples). These feed directly into Step 5 (Test). Anything to add or adjust before I generate the Design Spec?"

If the user adds or adjusts anything, update the Workflow Requirements file (not the Design Spec) — that file remains the canonical source of acceptance criteria and test scenarios. The Design Spec references them by file path; it does not duplicate them.

If the Workflow Requirements is missing Acceptance Criteria or Example Scenarios entirely (which shouldn't happen if Deconstruct was run), pause and ask the user to run `/deconstruct` again or fill them in manually before continuing.

#### Step 9 — Assemble Design Spec (do not write the file yet)

**STOP — do not assemble the spec from memory. Read `references/spec-template.md` now.** The spec's exact section order, heading names, frontmatter schema, and `spec_version` literal exist only in that file. A from-memory spec will have drifted headings that break Build's parse. For goal-driven workflows, also apply the template substitutions from `references/goal-driven-path.md` (which you read at Step 1).

Assemble the full Design Spec **content** following the template — but **do not write it to disk yet**. The file is written only after the user approves it in Step 10. Target path (written in Step 10): `outputs/[workflow-name]/design-spec.md`.

**Why not write yet:** If the session is in a plan/read-only mode, writing files is blocked until the user approves and exits it; on surfaces without plan mode the same rule applies — never persist a deliverable before approval. So assemble + self-test in memory, present for approval (Step 10), then write.

**Assembly order:**

1. Assemble all spec sections following `references/spec-template.md` — in memory. Honor the template's conditional-section rules (Orchestrator Prompt Outline, Agent Configuration, Multi-Agent Configuration, Stakeholders).
2. **STOP — read `references/self-test-checklist.md` now**, then run every item against the assembled content. Do not run the checklist from memory — a recalled checklist silently shrinks.
3. **Assemble the Self-Test Summary section** as the final section of the spec, enumerating **every checklist item verbatim**, each marked ✓ (passed) or ⚠️ (issue — described inline). A summary with fewer items than the checklist file means the checklist wasn't fully run — go back. This makes the verification visible to the user and to downstream skills.
4. If any checklist item failed (⚠️), fix the underlying section **before presenting for approval**. The Self-Test Summary should ideally show all ✓ — but if a ⚠️ remains (e.g., a deliberate gap the user accepted), surface it honestly.
5. Carry the assembled content into Step 10 for approval. **Do not write the file in this step.**

#### Step 10 — Spec Approval Gate, then write the file

**This is a hard gate. Do not write the spec file or proceed without explicit approval.**

Present a summary of the assembled (not-yet-written) Design Spec. When the spec defines more than 3 component blueprints (skills + agents), open the summary with a one-line-per-blueprint recap (ID, name, purpose) so the user sees the full component inventory before approving:

> "Here's the Design Spec summary:
>
> - **Autonomy:** [level] (for goal-driven: Autonomous)
> - **Mechanism:** [orchestration mechanism] ([involvement mode])
> - **Structure:** [count] steps, [count] skill candidates, [count] agents (for goal-driven: [count] capability domains, [count] skill candidates, [count] agents)
> - **Integration options:** [count] tools with recommended integration approaches
> - **Safety:** [one-line summary — write surfaces, untrusted input handling, gates]
> - **Implementation order:** [brief summary]
>
> The full spec is **ready for approval** — I'll save it to `outputs/[workflow-name]/design-spec.md` once you approve.
>
> **Do you approve this spec?** I won't write the file or generate any artifacts until you confirm. If you want changes, tell me what to adjust and I'll revise."

If the user requests changes, **revise the assembled content in memory**, re-run the self-test, and re-present — still without writing the file.

**Only after explicit approval:**
1. **Write the spec** to `outputs/[workflow-name]/design-spec.md`. If a spec already exists from a previous run, rename the old one with a date suffix (e.g., `design-spec-2026-06-10.md`) before writing. (If the session is in plan mode, this is the point where the user exits it so the write can happen; otherwise write directly. If this environment has **no persistent workspace** — files don't survive between conversations — tell the user the spec will download as a file they should keep and re-supply at the next step, or continue the next step in this same conversation.)
2. **Update the Workflow node** (`registry/workflows/<slug>.md`): set `execution_mode` (`manual` | `augmented` | `automated`) and `autonomy` (`deterministic` | `guided` | `autonomous`), and link the Design spec in `# Artifacts`. See `indexing-registry/references/registry-bundle.md` for write rules and the full field-ownership table. Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step).
3. Then tell the user:

> - **If plan mode was used:** "Spec approved and saved to `outputs/[workflow-name]/design-spec.md`. If you're still in plan mode, **exit now** so the Build phase can generate artifacts." (Name the platform's actual exit action.)
> - **Otherwise:** "Spec approved and saved to `outputs/[workflow-name]/design-spec.md`."
>
> "To build the workflow, run the `build` skill (Step 4) (or say *'Build the workflow from my Design Spec'*)."

## Outputs

### `outputs/[workflow-name]/design-spec.md` — Design Spec

Uses the mandatory template defined in `references/spec-template.md`. The Design Spec **references** the Workflow Requirements as canonical source — it does not restate Goal, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview, or per-step requirements.

The spec opens with YAML frontmatter (workflow, requirements_file, spec_version, definition_type, mechanism, involvement, platform, platform_mode, packaging, counts) so Build and downstream skills can summarize the spec without parsing prose. It is organized into three layered groups — Architecture (L1, including Safety & Permissions), Decomposition (L2), Component Blueprints (L3) — plus cross-layer sections (Evaluation Inputs, Deferred to Build, Stakeholders, Self-Test Summary). The exact structure lives in the template file, not here.

For goal-driven workflows, the template substitutions in `references/goal-driven-path.md` apply.

## Guidelines

- **Exercise judgment within the guardrails.** This workflow is a scaffold: you may deviate from the encoded sequence when the situation clearly calls for it — state the deviation and the reason in one line. What is never negotiable: the two hard gates (Layer 1 confirmation, Spec Approval), the mandatory reference-file reads, the Safety & Permissions pass, and the spec template's structure and canonical vocabulary (Build parses them).
- Use plain language; avoid jargon unless the user introduced it
- After writing the spec, tell the user: "Design Spec saved to `outputs/[name]/design-spec.md`. Read it alongside the Workflow Requirements at `outputs/[name]/requirements.md`."
- Do not proceed past the Spec Approval Gate (Step 10) without explicit user approval
- Do not research integration availability — that happens in the Build phase
- Do not generate platform artifacts — that happens in the Build phase
- Do not restate Workflow Requirements content in the Design Spec — reference the file
- Never assemble the spec or run the self-test from memory — read the bundled reference files at the steps that call for them
