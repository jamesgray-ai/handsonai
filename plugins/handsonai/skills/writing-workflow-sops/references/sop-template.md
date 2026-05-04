# SOP Template Reference

## Choosing a Template

The workflow's position on the autonomy spectrum determines which template to use:

```
Deterministic ———————— Guided ———————— Autonomous
(fixed path)       (bounded decisions)     (context-driven path)
```

| Autonomy Level | Template | When to use |
|---|---|---|
| **Deterministic** | Full SOP | Fixed sequence — same inputs always produce the same path |
| **Guided or Autonomous** | Lightweight SOP | Context-driven — executor adjusts path based on feedback, errors, or intermediate results |

**Key test:** Can the executor change its path at runtime based on what it encounters? If yes (guided or autonomous) → lightweight. If no (deterministic) → full.

---

## Full SOP Template (Deterministic)

Used for workflows with a fixed sequence. The SOP *is* the process definition.

```markdown
## Overview
[1-2 sentences: What this workflow accomplishes and why it matters]

## Prerequisites
- [ ] [Access/permissions required]
- [ ] [Data or inputs that must exist]
- [ ] [Tools/apps that must be connected]

## Trigger
**When:** [Schedule, event, or manual request]
**Frequency:** [Daily / Weekly / On-demand / Event-driven]

---

## Procedure

### Step 1: [Action verb + what]
[Specific instructions with exact locations, button names, or commands]

> Tip: [Optional efficiency hack or gotcha]

### Step 2: [Action verb + what]
[Continue with specific instructions]

**Decision Point:** [If X, do Y. If Z, do W.]

### Step 3: [Action verb + what]
[Continue...]

---

## Outputs
| Output | Destination | Format |
|--------|-------------|--------|
| [What gets produced] | [Where it goes] | [Type] |

## Quality Checks
- [ ] [How to verify success]
- [ ] [What good output looks like]

## When Things Go Wrong
| Problem | Solution |
|---------|----------|
| [Common failure] | [Resolution] |

---

## Automation Notes
**Execution Model:** Augmented + Deterministic

**Skill/Agent:** [Link to Claude Skill if applicable]
**Human Checkpoints:** [Where human review required]
**Logs/Monitoring:** [Where to check execution]
```

### Type Adaptations (for full SOPs)

Apply these on top of the full template based on workflow type:

#### Manual Workflows
- Emphasize detailed step-by-step instructions
- Include time estimates per step
- Add screenshots or exact UI paths when helpful
- Focus on "what you do"

#### Augmented Workflows
Mark human vs AI steps clearly:
```markdown
### Step 2: Generate draft (AI)
Claude analyzes [input] and produces [output].

### Step 3: Review and refine (Human)
Review the draft for [criteria]. Edit as needed before [next action].
```

#### Automated Workflows
- Focus on monitoring and intervention points
- Procedure describes "what the system does" not "what you do"
- Emphasize error handling and recovery
- Include log locations and success indicators

---

## Lightweight SOP Template (Guided / Autonomous)

Used for workflows where the executor adapts its path at runtime. The agent's system prompt *is* the process definition — the SOP documents the human interface to the agent.

```markdown
# Standard Operating Procedure
[1-2 sentences: What this workflow accomplishes]

---

## Execution Pattern
**Augmented + Guided** — The `<agent-name>` agent [brief description of what it does]. You [what the human does]; the agent handles [what the agent handles].

---

## How to Start

Invoke the agent:

\```
Use the <agent-name> agent to [action] [inputs]
\```

Have these ready before starting:

- [ ] [Input 1]
- [ ] [Input 2]

---

## Your Role at Each Checkpoint

The agent manages the overall flow. You make decisions at [N] checkpoints:

| Checkpoint | What you do |
|------------|-------------|
| **[Checkpoint name]** (Step N) | [What the human decides] |

---

## Outputs

| Output | Destination | Format |
|--------|-------------|--------|
| [What gets produced] | [Where it goes] | [Type] |

---

## When to Skip the Agent

Run individual skills directly when you only need one piece:

| Need | Skill |
|------|-------|
| [Specific need] | `skill-name` |

---

## Related

- **Agent**: [`.claude/agents/<agent-name>.md`](relative-path)
- **Upstream**: [Workflow name](relative-path) — [what it does]
- **Downstream**: [Workflow name](relative-path) — [what it does]
```

### Differences from full SOPs

| Full SOP (Deterministic) | Lightweight SOP (Guided / Autonomous) |
|---|---|
| Full procedure with numbered steps | No procedure section — agent owns the steps |
| Prerequisites section | "Have these ready" under How to Start |
| Trigger section | Entry point detection in How to Start |
| Quality Checks section | Omitted — agent runs its own quality checks |
| Troubleshooting section | Omitted — agent handles retry/backtracking |
| Automation Notes section | Replaced by Execution Pattern |

---

## Section Guidelines

These apply to **full SOP** sections. Lightweight SOPs follow their own template structure above.

### Overview
- 1-2 sentences maximum
- Answer: What does this do? Why does it matter?
- Avoid technical implementation details

### Prerequisites
- List only items that MUST exist before starting
- Include access, data inputs, and tool connections
- Keep to 3-5 items max

### Procedure Steps
- Start each step with action verb
- One action per step (avoid compound steps with "and then")
- Include decision points as explicit branches
- Add tips only for non-obvious gotchas

### Outputs Table
- List every tangible deliverable
- Specific destination (database name, folder path, inbox)
- Include format (PDF, Notion page, email draft)

### Quality Checks
- Measurable verification criteria
- "What good looks like" examples
- 2-4 checks maximum

### Troubleshooting
- Only COMMON failures (80/20 rule)
- Actionable solutions, not vague guidance
- 2-4 problems maximum
