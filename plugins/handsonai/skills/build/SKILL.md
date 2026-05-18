---
name: build
description: >
  This skill should be used when the user has an approved Design Spec and wants to
  build platform artifacts for their AI workflow. It offers a build path choice, researches
  integration availability, generates platform-appropriate artifacts (prompts, skills, agents, configs),
  and writes them to the right locations for the user's platform.
  This is Step 4 (Build) of the AI Workflow Framework.
user-invocable: true
---

# Workflow Build

Take an approved Design Spec and generate platform-appropriate artifacts: prompts, skills, agents, configs, and connectors.

**Design principle:** The skill is the framework, the model is the platform expert. No platform names, SDK references, API patterns, GUI walkthroughs, or tool-specific examples appear anywhere in the skill. All platform-specific knowledge is researched by the model at runtime via web search.

**Role:** You are an **Agentic AI Architect**. Your role is to build solutions that map business workflows to AI building blocks across all three layers — Intelligence (Model, Context, Memory, Project), Orchestration (Prompt, Skill, Agent), and Integration (MCP, API, SDK, CLI). You think in terms of system design, artifact generation, and platform-specific implementation.

## Workflow

Artifact generation begins only after the Design Spec has been approved in the Design phase.

#### Step 1 — Load Design Spec and Workflow Requirements

Read the Design Spec from `outputs/[workflow-name]-design-spec.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Design Spec in `outputs/`.

**Parse the frontmatter first.** The spec opens with YAML frontmatter containing: `workflow`, `requirements_file`, `spec_version`, `definition_type`, `mechanism`, `involvement`, `platform`, `platform_mode`, `packaging`, and `counts`. Use these values to summarize the spec — no need to parse the body to get the headline numbers.

**Also load the Workflow Requirements.** The Design Spec references the Workflow Requirements via its `requirements_file` frontmatter field (or the Source section if frontmatter is absent). Read that file too — it contains the per-step requirements, Context Inventory, Acceptance Criteria, Example Scenarios, and Human Gates that the Design Spec deliberately does NOT restate. Build needs both files together.

Confirm you've loaded both by summarizing: workflow name, orchestration mechanism, involvement mode, packaging, counts (steps, skills, agents, integrations), and that the Workflow Requirements was loaded.

**Spec version compatibility:**
- `spec_version: 2.1` (current) → current format with three-layer grouping, Orchestrator Prompt Outline, and Self-Test Summary; proceed.
- `spec_version: 2.0` → older format without layer grouping or Orchestrator Outline; proceed (Build's fallback derives the orchestrator from Workflow Requirements directly).
- No frontmatter or older `spec_version` → spec predates the current format. Inform the user: "This spec is in an older format. Some fields (Packaging, Build Output column, Skill/Agent IDs, Deployment Plan, Orchestrator Prompt Outline) may be missing. I can either (a) proceed with what's available and ask questions as needed, or (b) you can regenerate the spec by running the Design skill again."

#### Step 2 — Build Path Choice

Offer two paths:

> "How would you like to proceed?
>
> 1. **I'll build it** — I generate all artifacts (skills, agents, prompts, configs) based on the approved spec.
> 2. **I'll build it myself** — The spec is your deliverable. I'll provide a Construction Guide with build sequence and platform-specific format guidance instead of generating artifacts."

If the user chooses path 2:

1. Run Step 3.5 (Discover Available Creation Tools) to build the Creation Tools Map.
2. Generate a **Construction Guide** containing:
   - The build sequence from the spec (implementation order)
   - For each building block:
     - What to build (name, purpose, inputs/outputs from the spec)
     - The format specification to follow
     - **If a creation skill was matched:** "You have `[skill-name]` available. Invoke it (e.g., `/[skill-name]`) and pass the spec below as your starting context."
     - **If no creation skill matched:** The format reference and key requirements for manual creation
3. After presenting the Construction Guide, tell the user: "To test the workflow, run the `test` skill (Step 5)."

#### Step 3 — Mechanism-Specific Build Path

Based on the orchestration mechanism, present ONLY the steps relevant to the user's mechanism:

**Before starting any mechanism path:** Check the Data Readiness Summary. For items with state "Partial" or "No", resolve required actions first — these gate dependent steps. If resolution requires user action (e.g., exporting data, granting access), present the action list and wait for confirmation before proceeding.

**Prompt mechanism:**
1. Create context (from Context Inventory)
2. Set up project workspace (if frequent use)
3. Generate platform artifacts
4. → Test Plan
5. → Run Guide

**Skill-Powered Prompt mechanism:**
1. Create context (from Context Inventory)
2. Set up project workspace (if frequent use)
3. Build skills for tagged candidates
4. Generate platform artifacts
5. → Test Plan
6. → Run Guide

**Agent mechanism:**
1. Create context (from Context Inventory)
2. Build skills for tagged candidates
3. Connect external tools (from Integration Options section)
4. Generate platform artifacts (agent config, skills, connectors)
5. → Test Plan
6. → Run Guide

After presenting the mechanism-specific build path, proceed to Step 3.5 to discover available creation tools before generating any artifacts.

#### Step 3.5 — Discover Available Creation Tools

Before generating artifacts, discover what creation tools are available in this session. Skills are an open standard — they live in platform-specific directories but follow the same SKILL.md format everywhere.

1. **Extract building block types** from the loaded Design Spec — list each type and count (e.g., "3 skills, 1 agent, 1 MCP server config").

2. **Discover available creation skills** using two tiers:

   **Tier 1 — System-level discovery.** Check if the current environment provides a list of available skills (typically shown in system reminders, session context, or tool listings). If available, scan skill names and descriptions for any that indicate the ability to *create, generate, scaffold, or build* one of the needed building block types. Match semantically — look for descriptions containing phrases like "create a skill", "build an agent", "scaffold a plugin", "create hooks", "generate MCP servers", etc.

   **Tier 2 — Filesystem discovery (fallback).** If no system-level skill list is available, or if the list may be incomplete, scan the platform-appropriate skill directories for SKILL.md files. Read each file's YAML frontmatter (`name` and `description` fields) to identify creation-capable skills. Use the platform's skill directory:

   | Platform | Skill Directories |
   |----------|------------------|
   | Claude Code | `.claude/skills/` |
   | Cursor | `.cursor/skills/`, `.claude/skills/`, `.codex/skills/`, `.agents/skills/` |
   | Codex CLI | `.agents/skills/` |
   | Gemini CLI | `.gemini/skills/`, `.agents/skills/` |
   | VS Code Copilot | `.github/skills/`, `.agents/skills/` |
   | Cowork / Claude.ai | System-managed (Tier 1 only) |

   For the authoritative and up-to-date directory listing, read `docs/agentic-building-blocks/skills/index.md` (Platform Implementations table).

   If neither tier finds any skills (e.g., ChatGPT web, Gemini app), state: "No creation skills detected in this environment — all building blocks will be generated inline." Then proceed.

3. **Build a Creation Tools Map.** For each building block type needed by the spec, record the matched creation skill (if any) or "Inline generation" as the fallback:

   | Building Block Type | Count | Matched Creation Skill | Method |
   |---|---|---|---|
   | Skill | 3 | *(matched skill name or "none")* | Delegate / Inline |
   | Agent | 1 | *(matched skill name or "none")* | Delegate / Inline |

4. **Present the map for confirmation.** Show the user: "Here's how I plan to build each block type. For items with a matched creation skill, I'll delegate to that skill's full workflow. For items without, I'll generate inline using reference specifications. Does this look right?"

   Wait for user confirmation before proceeding.

#### Step 3.6 — Platform Research

Before generating artifacts, resolve platform-specific format requirements and integration documentation so that artifact generation (Step 6) produces correctly formatted output on the first pass.

> **Caching note:** The registry JSON is fetched once per session. If the Design phase already fetched it, use the cached copy.

**Tier 1 — Platform Doc Resolution**

1. **Fetch the platform registry** (or use session cache):
   `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`

2. **Look up the user's platform** in the `platforms` section of the registry JSON.

3. **Determine mode and language:**
   - Read the `mode` field (`code` or `guided`) for the matched platform.
   - For `code` mode: read the `language` field (e.g., `markdown`, `python`, `yaml`).
   - For `guided` mode: note that artifacts will be GUI workflow steps and configuration options rather than files.

4. **If platform not found:** Fall back to model knowledge combined with web search to determine the platform's artifact format. Log a warning: "Platform not found in registry — using model knowledge and web search for format requirements."

5. **For each building block needing an artifact**, fetch the corresponding doc URL from the registry:
   - Look up the building block type in the platform's `docs` section (e.g., `skills`, `agents`, `mcp`, `hooks`, `prompts`).
   - Fetch the linked documentation to extract artifact format requirements.

6. **Extract artifact format requirements:**
   - **Code mode:** frontmatter schema, file structure, naming conventions, language, and any platform-specific extensions.
   - **Guided mode:** GUI workflow steps, configuration options, and setup sequences.

7. **Pass format requirements forward.** Store the resolved format requirements so Step 6 (Generate Platform Artifacts) can use them directly instead of re-researching.

**Tier 2 — Integration Doc Resolver**

For each integration listed in the Design Spec's "Integration Options" section, resolve platform-specific integration documentation:

1. **Read `integration-registries`** from the cached registry JSON. This section catalogs known sources for integration documentation (e.g., MCP registry, platform marketplaces, connector catalogs).

2. **Search each cataloged source.** For each integration needing research:
   - Check MCP availability first — if an MCP tool for searching a cataloged source is available in the current session (e.g., `mcp-registry` search), use it.
   - If the MCP tool is available, query it for the integration name and platform.

3. **WebFetch fallback for uncataloged sources.** If the integration is not found in any cataloged source, or the cataloged source has no MCP tool available:
   - Use WebFetch to retrieve the integration's documentation directly from its known URL or official site.
   - If no URL is known, fall back to web search to locate the integration's documentation.

Present a summary of resolved platform format requirements and integration docs to the user before proceeding.

#### Step 4 — Check for Existing Skills and Instructions

This is separate from Step 3.5's creation tool discovery — here you're checking for workflow skills that have already been built and should be incorporated, not for skills that create other skills.

Before generating artifacts:
- Ask: "Did you build any skills for this workflow? If yes, list each skill name and which steps it covers."
- Check the Context Inventory for existing prompt instructions, project instructions, or system prompts. These must be incorporated into the generated artifacts.

#### Step 5 — Integration Research

Read the "Integration Options" section from the loaded Design Spec. This section already identifies each integration, its category (built-in, available with setup, possible with code, manual), and source URLs discovered during the Design phase.

**Use the carried-forward URLs as starting points.** The Design phase's Integration Discovery already answered "what's available?" — the focus here is "how do I connect it on the user's platform?"

For each integration listed in the spec:
1. Start from the source URL provided in the "Integration Options" section
2. Research platform-specific setup: installation steps, configuration, authentication, and any prerequisites for the user's platform
3. Confirm the integration category still applies on this platform. Recategorize if needed:
   - Built-in (works out of the box)
   - Available with setup (MCP server, connector, or plugin exists)
   - Possible with code (API integration required)
   - Manual (copy-paste between tools)

**Web search is used for platform availability research** — verifying setup steps, finding platform-specific guides, and confirming compatibility. Discovery of integrations themselves is already done. If the environment doesn't support web search, instruct the user to switch to a tool that does.

Present the integration mapping and ask the user to confirm before generating artifacts. If any critical integration is manual-only, discuss implications for the orchestration mechanism (may need to downgrade or add human-in-the-loop steps).

If the Integration Options section is missing from the spec (older format), inform the user and offer two paths: (a) Run Integration Discovery now — research available integration approaches for each tool identified in the spec's Integration Options or Step-by-Step Decomposition tables, or (b) proceed with web-search-only research for each integration need as it arises during artifact generation.

#### Step 6 — Generate Platform Artifacts

Based on the platform and packaging decisions from Architecture Decisions. Resolve the items in the spec's **Deferred to Build** section now:

- **Specific platform offering** if not yet determined (e.g., "Claude" → Claude Code vs. Claude.ai vs. Cowork)
- **Shareability** — file-based vs. code-based distribution; influences artifact format
- **Exact model version per platform** — verify current model names via web search for the user's platform
- **Integration setup specifics** — auth flow, region, plan tier per integration

Use the spec's **Step-by-Step Decomposition Build Output column** (or **Capability Domain Mapping Build Output column** for outcome-driven) as your generation checklist. Each row tells you exactly what to produce:
- `New skill: SN` → generate the skill defined in the matching Skill Candidates entry
- `Use existing: [name]` → no generation needed; verify the skill exists and reference it
- `New agent: AN` → generate the agent defined in the matching Agent Configuration entry
- `Inline prompt → Workflow Requirements Step N` → fold this step's Goal/Inputs/Outputs/Rules from the Workflow Requirements into the main orchestrator prompt
- `MCP server: [name]` → configure the connector using the Integration Options entry
- `Human (no artifact)` → skip; no AI artifact for this step
- `Handled by agent` (outcome-driven only) → no separate artifact; capability is covered by the agent's Instructions

Apply the spec's **Packaging** decision to group the generated artifacts:
- **Plugin** → assemble into a marketplace plugin directory structure (e.g., handsonai-plugins layout for Claude marketplace)
- **Standalone Skill** → ship as a single uploadable artifact (zip for Claude.ai, single SKILL.md for code-mode platforms, single skill for ChatGPT)
- **Workspace Agent** → bundle orchestration + skills + tools as a ChatGPT Workspace Agent (the current ChatGPT primitive; Custom GPTs are deprecated). Research current Workspace Agent creation flow via web search before generating.
- **Loose Files** → write files to platform-appropriate paths; no distribution wrapper

**When mechanism is `Prompt` or `Skill-Powered Prompt`:** read the spec's `Orchestrator Prompt Outline` section as the structural skeleton for the orchestrator prompt. The outline names which step invokes which skill, where PAUSE points sit, and what the user provides at each gate. Expand the outline into the full orchestrator prompt by pulling step content (Goal, Inputs, Outputs, Rules & Edge Cases) from the Workflow Requirements. If the section is absent (older spec or mechanism = Agent), fall back to deriving the orchestrator directly from Workflow Requirements Step Details + Human Gates.

**a. Resolve platform documentation from the registry.** Use the platform doc URLs fetched in Platform Research (Step 3.6) from the registry's `platforms` section. These provide current, authoritative documentation for each building block's artifact format.

If playbook platform guides are available locally (e.g., `docs/platforms/claude/index.md`), use them as supplementary context — not as the primary source.

**b. Verify currency (if needed).** The registry provides current doc URLs maintained by the framework author. Use web search only if the fetched docs appear outdated or if the registry was unavailable in Step 3.6.

**c. Follow the resolved artifact format specifications.** For each building block in the spec, use the artifact format extracted during Platform Research (Step 3.6). If Platform Research did not resolve a format (registry unavailable, platform not found), fall back to:
- Skills: `references/skill-spec.md`
- Agents (Claude Code): `references/agent-spec.md`
- Other platforms: web search

**d. Apply code vs guided mode branching.** Based on the platform's `mode` from the registry (determined in Step 3.6):

- **Code mode:** Generate source files in the platform's `language` (Python, TypeScript, markdown). This is the standard behavior — proceed with artifact generation as described below.
- **Guided mode:** Generate step-by-step GUI instruction documents. For each building block, produce a document that walks the user through configuring it in the platform's interface, using the GUI documentation fetched from the registry. Include: which screens to navigate to, what fields to fill in, what settings to configure, and what to verify after each step.

**e. Generate each building block.** For each building block in the spec, follow the Creation Tools Map from Step 3.5:

  **If a creation skill was matched for this block type:**

  1. Invoke it via the Skill tool, passing the building block's full spec from the Design Spec:
     - **For skills (S1, S2, …):** all 12 fields from the Skill Candidates entry — ID, Name, Description, Purpose, Covers Steps/Domains, Inputs, Outputs, Decision Logic, Failure Modes, Required Tools, Depends On, Stateful?
     - **For agents (A1, A2, …):** all 13 fields from the Agent Configuration entry — ID, Name, Description, Mission, Responsibilities, Output Format, Tone & Style, Constraints, Model, Memory Scope, Tools, Skills, Trigger Examples. If multi-agent, also pass the relevant Handoff Contracts and the Orchestration Pattern.
     - The artifact format requirements resolved in Step 3.6 (or the fallback reference if Step 3.6 did not resolve a format)
     - Whether platform-specific extensions should be applied (based on Architecture Decisions and Packaging)
     - This context: "This building block comes from an approved Design Spec (AI Workflow Framework, Step 3 Design). The intent, name, description, inputs, outputs, decision logic, and failure modes are already defined. Use this as your starting context."
  2. Let the creation skill run its full workflow. Do not skip or abbreviate any stage.
  3. After completion, move to the next building block. Later blocks may reference earlier ones via their stable IDs.

  **If no creation skill was matched (inline generation):**

  1. **For skills:** Use the artifact format from Step 3.6. If unavailable, fetch the agentskills.io specification (live from `https://agentskills.io/specification`, fallback to `references/skill-spec.md`). Generate the skill using the Skill Candidates entry — use the `Name` field as the directory name and the `Description` field verbatim in the SKILL.md frontmatter. Apply platform-specific extensions as documented for the target platform.
  2. **For agents:** Use the artifact format from Step 3.6. If unavailable and on Claude Code, fall back to `references/agent-spec.md`. For other platforms, fall back to web search. Generate the agent using the Agent Configuration entry — use the `Name` as the filename, the `Description` field verbatim in the agent file frontmatter (and include the Trigger Examples as `<example>` blocks in the description), and the Mission, Responsibilities, Output Format, Tone & Style, and Constraints fields as the agent's system prompt body.
  3. **For other block types (MCP servers, hooks, commands, prompts):** Use the artifact format from Step 3.6. If unavailable, research the platform's current format via web search and generate accordingly.

**f. Generate artifacts.** The skill provides the *specs* (what each building block should do, its inputs/outputs/instructions from the Design phase). The model provides the *implementation* (how to build it on the user's platform, using the verified specification and platform documentation as authoritative sources).

**g. Place and deploy each artifact per the Deployment Plan.** The Design Spec's Deployment Plan table specifies the target location and deployment steps for every artifact. For each generated artifact:
1. Write the artifact to its target location from the Deployment Plan.
2. Execute or document the deployment steps (e.g., "run `claude mcp add ...`", "upload zip via plugin marketplace", "create new GPT and paste instructions").
3. If the target location requires user action (e.g., a manual GPT creation flow), produce a step-by-step guide tailored to the user's platform.

After completing Build, summarize what was generated, where each artifact was placed, and any remaining manual deployment steps. Then tell the user: "To test the workflow, run the `test` skill (Step 5) (or say *'Test the workflow I built'*)."

## Outputs

### Platform Artifacts

Prompts, skills, agents, orchestration configs, and connector setups in whatever format is appropriate to the user's chosen platform. Generated by the model based on the Design Spec and Architecture Decisions. For code-mode platforms, these are source files; for guided-mode platforms, these are step-by-step GUI instruction documents. For building blocks with a matched creation skill (discovered at runtime in Step 3.5), artifacts are built by delegating to that skill's full workflow. For building blocks without a matched creation skill, artifacts are generated inline using the format resolved from the platform registry in Step 3.6 (falling back to `references/skill-spec.md` for skills, `references/agent-spec.md` for Claude Code agents, or web search for other platforms).

## Guidelines

- Use plain language; avoid jargon unless the user introduced it
- After generating platform artifacts, summarize what was produced and where each artifact was saved
- Do not start Build without a loaded and approved Design Spec
- Web search is required for integration research and platform documentation verification
