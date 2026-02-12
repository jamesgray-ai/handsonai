---
name: building-workflows
description: >
  Design and build an AI workflow from a Workflow Definition. The Design phase chooses an execution
  pattern, classifies steps, maps building blocks, identifies skill candidates, and configures agents.
  The Construct phase generates the Baseline Workflow Prompt, skills, and agent files based on the
  chosen pattern. Use when the user has a Workflow Definition and wants to design and build the
  workflow. This is the Build step (Design + Construct).
---

# Workflow Build

Take a Workflow Definition and produce the Build deliverables: an AI Building Block Spec (Design) and a Baseline Workflow Prompt with optional skills and agent files (Construct).

## Workflow

### Design Phase

1. **Load Workflow Definition** — Read the Workflow Definition from `outputs/[workflow-name]-definition.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Workflow Definition in `outputs/`.
2. **Confirm understanding** — Summarize the workflow name, step count, and outcome. Ask the user to confirm before proceeding.
3. **Execution pattern assessment** — Walk the user through the execution pattern spectrum:

   | Pattern | Description | Signals |
   |---------|-------------|---------|
   | **Prompt** | Single self-contained prompt, all logic inline | Sequential steps, human drives the process and provides all inputs |
   | **Skill-Powered Prompt** | Prompt invoking reusable skills | Repeatable sub-routines, moderate complexity |
   | **Single Agent** | One autonomous agent with tool access | Tool use, autonomous decisions, multi-step reasoning |
   | **Multi-Agent** | Specialized agents in a pipeline | Multiple expertise domains, parallel execution, review gates |

   Decision questions:
   1. Does the workflow require tool use? (web, files, APIs)
   2. Does it require autonomous decision-making?
   3. Are there steps with complex, reusable logic? → skill candidates
   4. Does it span multiple expertise domains?
   5. Would it benefit from parallel execution or review gates?

   Present the recommended pattern with reasoning. Ask the user to confirm.

4. **Classify each step** — For every refined step, determine:
   - **Autonomy level**: Human / AI-Deterministic / AI-Semi-Autonomous / AI-Autonomous
   - **AI building block(s)**: Prompt, Context, Skill, Agent, MCP, Project
   - **Tools and connectors**: External tools, APIs, integrations needed
   - **Human-in-the-loop gates**: Where human review is recommended
   Present the mapping as a clear table. Walk through reasoning for non-obvious classifications. Ask if the user wants to adjust anything.

5. **Identify skill candidates** — Tag steps that should become skills. For each skill candidate, document:
   - Purpose (one sentence)
   - Inputs (what data the skill receives)
   - Outputs (what the skill produces)
   - Decision logic (key rules, criteria, frameworks)
   - Failure modes (what happens when inputs are missing or unexpected)

6. **Agent configuration** (when execution pattern is Single Agent or Multi-Agent) — For each agent the workflow needs, document:

   | Component | What to specify |
   |-----------|----------------|
   | **Name** | Unique agent name |
   | **Description** | Agent purpose and when it should be used |
   | **Instructions** | Mission, responsibilities, behavior, goals, tone & style, output format |
   | **Model** | Recommended model capability (reasoning-heavy, fast, etc.) |
   | **Tools** | Tools the agent can call (MCP servers, file access, web, APIs) |

   Plus: Context requirements and Goal (trigger/invocation pattern).
   For multi-agent: orchestration pattern, agent handoffs, human review gates.

7. **Generate AI Building Block Spec** — Write to `outputs/[workflow-name]-building-block-spec.md`. Includes:
   - Execution pattern recommendation
   - Step-by-step decomposition table with autonomy levels and building blocks
   - Autonomy spectrum summary
   - Skill candidate section with generation-ready detail
   - Agent configuration section (when agent-based)
   - Step sequence and dependencies
   - Prerequisites
   - Context inventory
   - Tools and connectors required
   - Recommended implementation order (quick wins → semi-autonomous → complex agent steps)
   - Where to Run recommendation

### Construct Phase

8. **Pattern-specific build path** — Based on the execution pattern, present ONLY the steps relevant to the user's pattern:

   **Prompt pattern:**
   1. Create context (from Context Inventory)
   2. Set up project workspace (if frequent use)
   3. Generate Baseline Workflow Prompt
   4. → Run

   **Skill-Powered Prompt pattern:**
   1. Create context (from Context Inventory)
   2. Set up project workspace (if frequent use)
   3. Build skills for tagged candidates (Claude: auto-generate SKILL.md files; other platforms: create custom instructions/GPTs/Gems using skill candidate specs)
   4. Generate Baseline Workflow Prompt (referencing skills)
   5. → Run

   **Single Agent pattern:**
   1. Create context (from Context Inventory)
   2. Build skills for tagged candidates
   3. Connect external tools with MCP (from Tools and Connectors section)
   4. Build the agent (Claude: auto-generate agent .md from agent config; other platforms: configure using the blueprint)
   5. → Run

   **Multi-Agent pattern:**
   1. Create context (from Context Inventory)
   2. Build skills for tagged candidates
   3. Connect external tools with MCP (from Tools and Connectors section)
   4. Build each specialist agent (Claude: auto-generate agent .md files)
   5. Build the orchestrator (Claude: auto-generate orchestrator agent)
   6. → Run

9. **Check for existing skills** — Ask: "Did you build any skills for this workflow? If yes, list each skill name and which steps it covers." If skills exist, note them for prompt generation.
10. **Check for existing AI instructions** — Before generating, check the Context Inventory for existing prompt instructions, project instructions, or system prompts. These must be included in the Baseline Prompt.
11. **Generate Baseline Workflow Prompt** — Produce a ready-to-use, self-contained prompt and write to `outputs/[workflow-name]-prompt.md`. For any step covered by a skill, replace inline instructions with a brief description. Keep full instructions only for steps NOT covered by a skill.
12. **Auto-generate skills** (Claude platform, Skill-Powered/Agent patterns) — For each skill candidate, generate a `SKILL.md` file in `.claude/skills/[skill-name]/SKILL.md` based on the skill candidate specs from the Design phase.
13. **Auto-generate agent files** (Claude platform, Agent patterns) — For each agent documented in the Design phase, generate an agent `.md` file in `.claude/agents/[agent-name].md` based on the agent configuration.
14. **Write SOP to Notion (if available)** — After the prompt is generated, check if the Notion MCP server is accessible AND this workflow was registered during the Deconstruct step. If so, offer to write the workflow SOP to the Notion page.

## Outputs

### `outputs/[workflow-name]-building-block-spec.md` — AI Building Block Spec (Design)

Includes:
- Execution pattern recommendation with reasoning
- Scenario summary (workflow metadata)
- Step-by-step decomposition table (autonomy level, building blocks, skill candidate flag)
- Autonomy spectrum summary
- Skill candidates (with generation-ready detail)
- Agent configuration (when applicable)
- Step sequence and dependencies
- Prerequisites
- Context inventory
- Tools and connectors required
- Recommended implementation order
- Where to Run recommendation

### `outputs/[workflow-name]-prompt.md` — Baseline Workflow Prompt (Construct)

Structure:
- **Title and Purpose** — Workflow name, description, outcome, when to use
- **Instructions** — Numbered steps, each labeled (AI) or (Human). AI steps get direct commands. Human steps describe what the human does and hands back. Include branching logic.
- **Input Requirements** — What the user provides when running the prompt, with format specs
- **Context Requirements** — Reference materials, files, or data to attach
- **Output Format** — What the prompt produces, with structure specs
- **Where to Run** — Normal chat vs. project recommendation

The prompt must be: self-contained, specific, version-control ready, team-adoption ready.

### Optional: Skills and Agent files (Claude platform)

- `.claude/skills/[skill-name]/SKILL.md` — Auto-generated from skill candidate specs
- `.claude/agents/[agent-name].md` — Auto-generated from agent configuration

## Guidelines

- If the user mentions Claude, note where Claude Code Skills and Agents are the appropriate implementation
- Use plain language; avoid jargon unless the user introduced it
- After writing the Design output, tell the user: "AI Building Block Spec saved to `outputs/[name]-building-block-spec.md`."
- After writing the Construct output, tell the user: "Baseline Workflow Prompt saved to `outputs/[name]-prompt.md`."
- Summarize all deliverables at the end so the user has a clear inventory
