---
name: build
description: >
  This skill should be used when the user has an approved AI Building Block Spec and wants to
  build platform artifacts for their AI workflow. It offers a build path choice, researches
  integration availability, generates platform-appropriate artifacts (prompts, skills, agents, configs),
  This is Step 4 (Build) of the Business-First AI Framework.
user-invocable: true
---

# Workflow Build

Take an approved AI Building Block Spec and generate platform-appropriate artifacts: prompts, skills, agents, configs, and connectors.

**Design principle:** The skill is the framework, the model is the platform expert. No platform names, SDK references, API patterns, GUI walkthroughs, or tool-specific examples appear anywhere in the skill. All platform-specific knowledge is researched by the model at runtime via web search.

**Role:** You are an **Agentic AI Architect**. Your role is to build solutions that map business workflows to AI building blocks across all three layers — Intelligence (Model, Context, Memory, Project), Orchestration (Prompt, Skill, Agent), and Integration (MCP, API, SDK, CLI). You think in terms of system design, artifact generation, and platform-specific implementation.

## Workflow

Artifact generation begins only after the AI Building Block Spec has been approved in the Design phase.

#### Step 1 — Load Building Block Spec

Read the AI Building Block Spec from `outputs/[workflow-name]-building-block-spec.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Building Block Spec in `outputs/`.

Confirm you've loaded the spec by summarizing: workflow name, orchestration mechanism, involvement mode, number of steps, number of skill candidates, and number of agents.

Verify the spec contains an Architecture Decisions section and Integration Options section. If either is missing, inform the user: "This spec appears to predate the current format. Some sections are missing. I can either (a) proceed with what's available and ask questions as needed, or (b) you can regenerate the spec by running the Design skill again."

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
3. After presenting the Construction Guide, tell the user: "To generate the Run Guide, run `/business-first-ai:run`."

#### Step 3 — Mechanism-Specific Build Path

Based on the orchestration mechanism, present ONLY the steps relevant to the user's mechanism:

**Before starting any mechanism path:** Check the Data Readiness Summary. For items with state "Partial" or "No", resolve required actions first — these gate dependent steps. If resolution requires user action (e.g., exporting data, granting access), present the action list and wait for confirmation before proceeding.

**Prompt mechanism:**
1. Create context (from Context Inventory)
2. Set up project workspace (if frequent use)
3. Generate platform artifacts
4. → Run Guide

**Skill-Powered Prompt mechanism:**
1. Create context (from Context Inventory)
2. Set up project workspace (if frequent use)
3. Build skills for tagged candidates
4. Generate platform artifacts
5. → Run Guide

**Agent mechanism:**
1. Create context (from Context Inventory)
2. Build skills for tagged candidates
3. Connect external tools (from Integration Options section)
4. Generate platform artifacts (agent config, skills, connectors)
5. → Run Guide

After presenting the mechanism-specific build path, proceed to Step 3.5 to discover available creation tools before generating any artifacts.

#### Step 3.5 — Discover Available Creation Tools

Before generating artifacts, discover what creation tools are available in this session. Skills are an open standard — they live in platform-specific directories but follow the same SKILL.md format everywhere.

1. **Extract building block types** from the loaded Building Block Spec — list each type and count (e.g., "3 skills, 1 agent, 1 MCP server config").

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
   `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/business-first-ai/registries/platform-registry.json`

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

For each integration listed in the Building Block Spec's "Integration Options" section, resolve platform-specific integration documentation:

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

Read the "Integration Options" section from the loaded Building Block Spec. This section already identifies each integration, its category (built-in, available with setup, possible with code, manual), and source URLs discovered during the Design phase.

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

Based on the platform from Architecture Decisions. Resolve any deferred decisions now: ask about **shareability** (will team members run this?) to determine artifact format (file-based vs. code-based), and resolve the **specific platform offering** if not yet determined (e.g., Claude Code vs. Claude.ai, ADK vs. Gemini web). Infer **code comfort** from the specific offering (Claude Code = code-comfortable, ChatGPT = no-code).

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

  1. Invoke it via the Skill tool, passing:
     - The building block's full spec from the Building Block Spec (name, purpose, inputs, outputs, decision logic, failure modes, which workflow steps it covers)
     - The artifact format requirements resolved in Step 3.6 (or the fallback reference if Step 3.6 did not resolve a format)
     - Whether platform-specific extensions should be applied (based on Architecture Decisions)
     - This context: "This building block spec comes from an approved AI Building Block Spec (Business-First AI Framework, Step 3 Design). The intent, inputs, outputs, decision logic, and failure modes are already defined. Use this as your starting context."
  2. Let the creation skill run its full workflow. Do not skip or abbreviate any stage.
  3. After completion, move to the next building block. Later blocks may reference earlier ones.

  **If no creation skill was matched (inline generation):**

  1. **For skills:** Use the artifact format from Step 3.6. If unavailable, fetch the agentskills.io specification (live from `https://agentskills.io/specification`, fallback to `references/skill-spec.md`). Generate the skill following that spec. Apply platform-specific extensions as documented for the target platform.
  2. **For agents:** Use the artifact format from Step 3.6. If unavailable and on Claude Code, fall back to `references/agent-spec.md`. For other platforms, fall back to web search. Generate the agent following the resolved spec.
  3. **For other block types (MCP servers, hooks, commands, prompts):** Use the artifact format from Step 3.6. If unavailable, research the platform's current format via web search and generate accordingly.

**f. Generate artifacts.** The skill provides the *specs* (what each building block should do, its inputs/outputs/instructions from the Design phase). The model provides the *implementation* (how to build it on the user's platform, using the verified specification and platform documentation as authoritative sources).

After completing Build, tell the user: "To generate the Run Guide, run `/business-first-ai:run` (or say *'Generate the Run Guide for my workflow'*)."

## Outputs

### Platform Artifacts

Prompts, skills, agents, orchestration configs, and connector setups in whatever format is appropriate to the user's chosen platform. Generated by the model based on the Building Block Spec and Architecture Decisions. For code-mode platforms, these are source files; for guided-mode platforms, these are step-by-step GUI instruction documents. For building blocks with a matched creation skill (discovered at runtime in Step 3.5), artifacts are built by delegating to that skill's full workflow. For building blocks without a matched creation skill, artifacts are generated inline using the format resolved from the platform registry in Step 3.6 (falling back to `references/skill-spec.md` for skills, `references/agent-spec.md` for Claude Code agents, or web search for other platforms).

## Guidelines

- Use plain language; avoid jargon unless the user introduced it
- After generating platform artifacts, summarize what was produced and where each artifact was saved
- Do not start Build without a loaded and approved Building Block Spec
- Web search is required for integration research and platform documentation verification
