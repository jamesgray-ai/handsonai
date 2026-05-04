# Process Guide Template Reference

## Full Template Structure

```markdown
## Purpose

[2-3 sentences: Why this process exists, what business outcome it drives, and the impact of doing it well vs poorly]

## When to Execute

**Trigger:** [What initiates this process]
**Frequency:** [How often - daily/weekly/event-driven]
**Timing:** [Best day/time, duration estimate]
**Owner:** [Who is responsible]

---

## Process Overview

```
[Workflow 1] → [Workflow 2] → [Workflow 3]
     ↓              ↓              ↓
  [Output]      [Output]       [Output]
```

**Total Duration:** [X] minutes/hours
**Workflows:** [X] workflows in sequence

---

## Workflow Sequence

### 1. [Workflow Name]
**Trigger:** [What kicks off this workflow]
**Duration:** [Time estimate]
**Output:** [What gets produced]
**Next:** [What happens after / triggers next workflow]

> 📋 **SOP:** [<Workflow Name> SOP](../sops/<workflow-name>-sop.md)

### 2. [Workflow Name]
**Trigger:** [What kicks off this workflow]
**Duration:** [Time estimate]
**Output:** [What gets produced]
**Next:** [What happens after / triggers next workflow]

> 📋 **SOP:** [<Workflow Name> SOP](../sops/<workflow-name>-sop.md)

### 3. [Workflow Name]
[Continue pattern...]

---

## Decision Points

### [Decision Point Name]
**When:** [At what stage this decision occurs]
**Options:**
- **If [condition A]:** [Action/path A]
- **If [condition B]:** [Action/path B]

**Default:** [What to do if unsure]

---

## Success Criteria

After completing this process, you should have:
- [ ] [Tangible output 1]
- [ ] [Tangible output 2]
- [ ] [Measurable outcome]

**Leading Indicator:** [Early sign it's working]
**Lagging Indicator:** [Longer-term proof of success]

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| [What typically goes wrong] | [How to avoid it] |
| [Another common mistake] | [How to prevent] |

---

## Orchestrator Agent (Optional)

**Agent:** [`<agent-name>`](path/to/agent.md)
**Invocation:** `Use the <agent-name> agent to [action]`

This agent handles sequencing, progress tracking, and skill invocation for the end-to-end process. See the agent file for configuration and capabilities.

---

## Related Processes

- **Upstream:** [Process that feeds into this one]
- **Downstream:** [Process that follows this one]
- **Parallel:** [Process that may run alongside]
```

## Section Guidelines

### Purpose
- 2-3 sentences maximum
- Connect to business outcomes (revenue, efficiency, risk)
- Answer: "What happens if we don't do this?"

### When to Execute
- Be specific about timing (not "regularly" but "Every Sunday at 10am")
- Include duration estimate for planning
- Note any dependencies or prerequisites

### Process Overview
- Visual representation of workflow flow
- Show outputs at each stage
- Keep it simple - details are in the SOPs

### Workflow Sequence
- One entry per workflow in execution order
- Include trigger (what starts it), duration, and output
- Link to the SOP markdown file using relative paths
- Note handoffs between workflows

### Decision Points
- Only include meaningful branch points
- Provide clear criteria for each option
- Always include a default/fallback

### Success Criteria
- Tangible, verifiable outputs
- Include both leading and lagging indicators
- Should be checkable within 24-48 hours

### Common Pitfalls
- Focus on mistakes that actually happen (not theoretical)
- Provide actionable prevention, not just warnings
- 2-4 pitfalls maximum

## Domain-Specific Adaptations

### Operations Processes (e.g., Weekly Review)
- Emphasize rhythm and consistency
- Include time-blocking recommendations
- Focus on habit formation

### Marketing Processes (e.g., Cohort Launch)
- Include timeline with milestones
- Connect to conversion metrics
- Note content dependencies

### Sales Processes (e.g., Graduate Upsell)
- Emphasize timing relative to customer journey
- Include personalization points
- Connect to revenue targets

## Writing Tips

1. **Start with the end**: What does success look like?
2. **Time-box everything**: People need to plan their calendar
3. **Link, don't repeat**: Reference SOPs for details
4. **Make it scannable**: Someone should understand in 2 minutes
5. **Include the "why"**: Context motivates execution
