---
title: Run Workflows
description: How to execute your AI workflow — choosing between normal chats, projects, and agent systems based on what you built.
---

# Run Workflows

You've built your building blocks — context artifacts, a prompt, maybe skills, agents, or MCP connections. Now run the workflow.

The most common question at this point is: **"Where do I run this? How do I run this?"** The answer depends on what you built.

## Choose Your Execution Pattern

| What you built | Execution pattern | Where to run it |
|---|---|---|
| Prompt + context files | **Paste and run** in a normal chat | Any AI tool (Claude, ChatGPT, Gemini, M365 Copilot) |
| Prompt + context + project | **Run in a project** — context is pre-loaded, paste the prompt each run | Claude Projects, ChatGPT Projects, Gemini Gems, M365 Copilot Notebooks |
| Agent + skills + MCP | **Command an agent** — give a goal, it plans and executes | Claude Code subagents, OpenAI Agents, Google Agents, M365 Copilot Agents |
| Any of the above + a schedule | **Automate** — recurring trigger, runs without you | Claude Code + launchd / Task Scheduler |

If you ran the [Prompt](prompt.md) step, your Build outputs include a **Where to Run** section — it recommends whether to run your workflow in a normal chat or a project, based on how many context files you have and how often you'll run it. Use that as your starting point. If you don't have that output, the guidance below will help you decide.

---

## Paste and Run

The simplest execution pattern. You have a prompt and maybe some context files. Open a chat, provide what the prompt needs, and get the output.

**How to run it:**

1. Open any AI tool — Claude, ChatGPT, Gemini, M365 Copilot, or any chat interface
2. If you have context files (reference materials, style guides, example data), attach or upload them to the conversation
3. Paste your Baseline Workflow Prompt
4. Provide the inputs the prompt asks for — the prompt's input requirements section tells you exactly what's needed
5. Review the output

This is where most workflows start, and many stay here permanently. If the workflow runs well as a paste-and-run prompt, there's no reason to add complexity.

---

## Run in a Project

When you're running the same workflow frequently and attaching the same context files every time, move it into a project. A project pre-loads your context so you just paste the prompt and go.

### Normal chat vs. project

| | Normal chat | Project |
|---|---|---|
| **Use when** | Infrequent workflow (monthly or less), few or no context files, one-off or experimental runs | Frequent workflow (weekly+), 3+ context files, team members need to run the same workflow |
| **Context** | Attached fresh each run | Pre-loaded — available in every conversation |
| **History** | Single conversation | Multiple conversations share the same context |
| **Setup effort** | None | A few minutes to create the project and upload files |

### How to run it:

1. **Create the project** — name it after your workflow
2. **Upload your context artifacts** — the documents, data, rules, and examples from the [Context](context.md) step
3. **Add custom instructions** (optional) — a brief orientation for the AI about this workflow's purpose
4. **Start a new conversation** within the project
5. **Paste the Baseline Workflow Prompt** — the prompt is always pasted fresh each run, never embedded in project instructions. The prompt IS the workflow.
6. **Provide inputs and review the output**

Each time you run the workflow, start a new conversation in the project. The context is already there — you just paste the prompt and provide the inputs.

### Where to create a project

| Platform | Feature name | How to create |
|---|---|---|
| Claude | Claude Projects | Sidebar > **Projects** > **New Project** |
| ChatGPT | ChatGPT Projects | Sidebar > **Projects** > **New Project** |
| Gemini | Gems | **Gems** tab > **Create Gem** |
| M365 Copilot | Notebooks | **Notebooks** in Copilot sidebar |

For platform-specific setup details, see [Agentic Building Blocks > Projects](../../agentic-building-blocks/projects/index.md).

---

## Command an Agent

When your workflow includes steps where the AI needs to plan its own approach, decide which tools to call, and adapt based on what it finds, you run it through an agent system. You give a goal — the agent figures out the path.

### How it's different from a prompt

With a prompt, you define every step and the AI follows your script. With an agent, you define the *outcome* and the agent decides how to get there. The agent plans, calls tools, evaluates results, adjusts its approach, and executes multi-step work autonomously. You review at human review gates, not at every step.

### How to run it:

1. **Give the agent a goal in natural language** — describe what you want done, not how to do it step by step
2. **The agent plans and executes** — it reads context, calls tools (via MCP), invokes skills, and adapts based on intermediate results
3. **Review at defined gates** — your agent definition specifies where the agent pauses for human approval
4. **Accept or redirect** — approve the output or give the agent further direction

### Where to run agents

| Platform | Agent system | How it works |
|---|---|---|
| Claude | Claude Code subagents | Define agents as `.md` files with system prompts, skills, and tool access. Run with `claude --agent` or via the `workflow-deconstructor` pattern. |
| OpenAI | OpenAI Agents | Build agents with the Agents API or in the Assistants playground. Agents have tools, instructions, and persistent threads. |
| Google | Google Agents | Build with Vertex AI Agent Builder or Gemini's agent capabilities. Agents connect to Google Workspace tools. |
| M365 Copilot | Copilot Agents | Build declarative or custom agents in Copilot Studio. Agents connect to Microsoft Graph and business data. |

For Claude-specific agent setup, see [Agentic Building Blocks > Agents](../../agentic-building-blocks/agents/index.md).

---

## Automate on a Schedule

When you want a workflow to run automatically — daily, weekly, or in response to triggers — without a human initiating each run. This is the highest level of the autonomy spectrum (the range from fully human-driven to fully AI-driven).

Scheduling requires an agent system with CLI (command-line interface) access — the ability to run commands from a terminal. Currently, Claude Code subagents (specialized AI assistants that run as part of a larger agent system) are the most straightforward option for this.

**How it works:**

1. Define the agent and its workflow (same as "Command an Agent" above)
2. Create a wrapper script that invokes the agent with a prompt
3. Register the script with a scheduler (launchd on macOS, Task Scheduler on Windows)
4. The workflow runs at the scheduled time, saves outputs, and logs results

**When to automate vs. when to keep manual:**

- **Automate** when the workflow is stable (you've run it several times and trust the output), the trigger is time-based or event-based, and the cost of a bad run is low
- **Keep manual** when you're still iterating on the prompt or agent, the workflow requires judgment calls you haven't codified, or the output goes directly to customers or stakeholders without review

For the full setup guide, see [Scheduling Subagents](../../platforms/claude/subagents/scheduling-subagents.md).

---

## Your First Run

The first run is a test, not a production run. Expect to iterate.

**What to evaluate:**

- Did the output match what you expected?
- Were any steps skipped or misunderstood?
- Did the AI ask for something it should have had (missing context)?
- Was the output quality good enough, or generic?

**Common first-run issues:**

- **Generic output** — the AI doesn't have enough context. Add reference materials, examples, or style guides.
- **Steps skipped or wrong** — the prompt instructions are too vague. Make the steps more explicit.
- **AI asks for information it should know** — a context file is missing. Check your Context Inventory from the Building Block Map.

## Iterating After the First Run

Use this table to figure out which building block to adjust based on what went wrong:

| Problem | What to fix |
|---|---|
| Output quality is generic or off-brand | Add more **context** — reference materials, examples, style guides |
| Steps are skipped or misunderstood | Refine the **prompt** — make instructions more explicit, add examples of expected output |
| A step needs domain expertise the AI doesn't have | Build a **skill** for that step — codify the expertise so the prompt can invoke it |
| The AI needs to make decisions you can't predict in advance | Convert from prompt to **agent** — let the AI plan its own approach |
| The workflow should run without you triggering it | Add **scheduling** — automate with a recurring trigger |

This maps directly back to the [Build overview](index.md#what-youll-do-next) — iterating is climbing the building block ladder based on what the workflow actually needs.

## Related

- [Build overview](index.md#what-youll-do-next) — the full seven-step build process including skills, agents, and MCP
- Worked Examples — [Deterministic Automation](deterministic-automation.md), [AI Collaborative](ai-collaborative.md), [Autonomous Agent](autonomous-agent.md)
- [Scheduling Subagents](../../platforms/claude/subagents/scheduling-subagents.md) — full automation setup guide
- [Agentic Building Blocks](../../agentic-building-blocks/index.md) — platform-specific implementation details
