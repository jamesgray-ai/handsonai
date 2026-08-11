---
name: naming-workflows
description: >
  This skill should be used when the user wants to name a workflow, write workflow descriptions,
  standardize workflow documentation, add a workflow to the AI Registry, or structure workflow
  entries. Generates consistent, outcome-focused names and descriptions for business workflows
  and records them in the workflow's Workflow node.
user-invocable: true
---

# Naming Workflows

Generate consistent, professional names and descriptions for business workflows, then record them in the workflow's Workflow node — the workflow's AI Registry entry.

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

## Workflow Naming Rules

### Format Requirements
- **Length**: 2-4 words maximum
- **Structure**: Noun phrases (not verb phrases)
- **Style**: Title case
- **Clarity**: Self-explanatory without context

### Naming Patterns by Domain

**Sales workflows:**
- Pattern: `[Prospect Type] [Action]`
- Examples: Student Enrollment, Lead Qualification, Proposal Generation

**Marketing workflows:**
- Pattern: `[Content Type] [Action/Purpose]`
- Examples: Newsletter Distribution, Social Media Scheduling, Content Repurposing

**Product workflows:**
- Pattern: `[Deliverable] [Action]`
- Examples: Lesson Content Creation, Curriculum Design, Exercise Development

**Education workflows:**
- Pattern: `[Student/Cohort] [Activity]`
- Examples: Student Onboarding, Course Access Setup, Live Session Delivery

**Consulting workflows:**
- Pattern: `[Deliverable/Phase] [Action]`
- Examples: Engagement Planning, Strategic Assessment, Implementation Support

**Operations workflows:**
- Pattern: `[Function] [Process]`
- Examples: Email Response Drafting, Calendar Management, System Maintenance

**Finance workflows:**
- Pattern: `[Transaction Type] [Action]`
- Examples: Invoice Generation, Payment Processing, Revenue Tracking

### Common Patterns

| If workflow monitors/checks | Use "[Subject] Monitoring" or "[Subject] Review" |
| If workflow creates output | Use "[Output] Creation" or "[Output] Generation" |
| If workflow sends/distributes | Use "[Item] Distribution" or "[Item] Delivery" |
| If workflow onboards/sets up | Use "[Subject] Onboarding" or "[Subject] Setup" |
| If workflow recovers/follows up | Use "[Subject] Recovery" or "[Subject] Follow-up" |

### Anti-Patterns (Avoid)

❌ Verb phrases: "Managing Email", "Creating Content"
❌ Too generic: "Daily Task", "Process 1"
❌ Too long: "Student Enrollment Payment Processing and Confirmation"
❌ Tool-focused: "Claude Email Tool", "Using Zapier for X"
❌ Jargon without context: "SOP-001", "Flow Alpha"

## Description Writing

### Format
Write 1-2 concise sentences that answer:
1. **What** does this workflow do?
2. **What** is the outcome/output?

### Structure
`[Action verb] [object] [context/condition]. [Outcome statement].`

### Examples

**Good descriptions:**
- "Review Gmail for emails requiring responses and draft replies. Generates draft responses ready for user review."
- "Convert course waitlist prospects into enrolled students through targeted email campaigns. Results in payment confirmations and enrollment completions."
- "Extract key insights from lesson recordings and repurpose into LinkedIn posts and Substack content. Produces 5+ social assets per lesson."

**Avoid:**
- Overly detailed: "This workflow checks the Gmail inbox every morning at 7:30 AM using Claude's email skill to scan for messages that..."
- Too vague: "Handles email stuff"
- Tool-focused: "Uses Claude and Gmail to do email"

## Process Outcome Writing

### Format
Write a short phrase (2-5 words) naming the concrete business deliverable.

### Requirements
- **Tangible**: Something that can be reviewed, sent, or measured
- **Specific**: Not "completed workflow" or "done"
- **Noun phrase**: The thing produced, not the action

### Examples

| Workflow | Process Outcome |
|----------|-----------------|
| Email Response Drafting | Draft email responses |
| Lead Qualification | Qualified lead list |
| Content Repurposing | 5+ social assets |
| Student Onboarding | Onboarded students |
| Newsletter Distribution | Published newsletter |
| Invoice Generation | Sent invoices |

### Anti-Patterns (Avoid)
- ❌ "Workflow completed" (not tangible)
- ❌ "Emails processed" (too vague)
- ❌ "Done" (not descriptive)
- ❌ "Successfully ran the email workflow" (action, not deliverable)

## Workflow Context Properties

When naming/describing workflows, consider these registry fields:

**Domain** (inherited from Business Process):
- Sales, Marketing, Product, Education, Consulting, Operations, Finance

**Trigger**:
- Daily/Weekly/Monthly schedule
- Event-based (payment received, email arrives)
- Manual/Ad-hoc

**Sequence** (within Business Process):
- Use multiples of 10 (10, 20, 30...) to allow insertions without renumbering
- Parallel workflows can share the same sequence number
- Only required when workflow is part of a multi-step process
- Leave blank for standalone workflows

## Examples by Domain

### Sales Domain
| Workflow Name | Description | Process Outcome |
|---------------|-------------|-----------------|
| Lead Qualification | Identify and score prospects using research tools and qualification criteria. Produces ranked lead list with contact details. | Qualified lead list |
| Student Enrollment | Process active student applications through payment and confirmation. Results in enrolled students ready for onboarding. | Enrolled students |
| Enrollment Recovery | Re-engage prospects who abandoned the enrollment process. Generates personalized follow-up sequences. | Re-engagement emails |

### Marketing Domain
| Workflow Name | Description | Process Outcome |
|---------------|-------------|-----------------|
| Content Repurposing | Transform lesson recordings into multi-platform social content. Creates LinkedIn posts, X threads, and Substack excerpts. | 5+ social assets |
| Newsletter Distribution | Publish newsletter content and distribute across platforms. Delivers newsletter to subscribers and social channels. | Published newsletter |
| Social Media Scheduling | Plan and schedule weekly LinkedIn and X content. Produces content calendar with scheduled posts. | Weekly content calendar |

### Product Domain
| Workflow Name | Description | Process Outcome |
|---------------|-------------|-----------------|
| Lesson Content Creation | Design and write online course lesson materials. Produces slide decks, exercises, and student resources. | Complete lesson package |
| Curriculum Design | Structure course outline aligned with learning objectives. Creates module sequence with Bloom's taxonomy alignment. | Course curriculum |
| Exercise Development | Create hands-on activities for course participants. Generates practical exercises with solutions and rubrics. | Student exercises |

### Education Domain
| Workflow Name | Description | Process Outcome |
|---------------|-------------|-----------------|
| Student Onboarding | Grant course access and prepare students for Day 1. Delivers welcome materials, Slack access, and technical setup. | Onboarded students |
| Live Session Delivery | Teach scheduled scheduled cohort sessions. Facilitates learning, Q&A, and student engagement. | Completed session |
| Assessment & Feedback | Review student work and provide constructive feedback. Generates graded assignments with improvement guidance. | Graded assignments |

### Operations Domain
| Workflow Name | Description | Process Outcome |
|---------------|-------------|-----------------|
| Email Response Drafting | Review inbox for urgent messages and create draft replies. Produces professionally written responses ready for review. | Draft email responses |
| Calendar Management | Coordinate scheduling across meetings and cohort sessions. Maintains organized calendar with buffer time. | Updated calendar |
| Slack Response Drafting | Monitor Slack channels and create appropriate replies. Generates context-aware draft responses. | Draft Slack messages |

## Usage Workflow

When user provides a workflow description:

1. **Identify domain** (based on business function)
2. **Determine pattern** (creation, monitoring, distribution, etc.)
3. **Generate 2-3 name options** using relevant pattern
4. **Write description** (action + outcome)
5. **Suggest Process Outcome** (concrete deliverable)
6. **Present options** for user selection
7. **Identify the Process** — scan `registry/processes/*.md` curated `# Workflows` lists (each list's parent Process node is a candidate); present matches and let the user confirm or name a new process
8. **Determine Sequence** if part of a multi-step process:
   - Check the chosen Process node's `# Workflows` list for the sibling workflows' order
   - Assign next available multiple of 10 (or ask user for placement)
   - Use same sequence number for parallel workflows
9. **Record in the registry** after user confirms selections (see below)

## Recording the Workflow (AI Registry entry)

The workflow's registry entry is its Workflow concept node: `registry/workflows/<workflow-id>.md`, where the ID is the kebab-case form of the confirmed name ("Lead Qualification" → `lead-qualification`). See `indexing-registry/references/registry-bundle.md` for resolution, write rules, and the full field-ownership table.

After the user confirms name, description, and process outcome:

1. **If a Workflow node already exists** for this workflow (the user is renaming or enriching), update only the fields below — preserve everything else, and never write inside a GENERATED block.
2. **If none exists** (naming before running deconstruct), create a **stub node** with `status: backlog` (meaning "named only" — deconstruct will merge into it later, never overwrite fields you set):

```yaml
---
type: Workflow
title: "Lead Qualification"
description: "Identify and score prospects using research tools and qualification criteria. Produces ranked lead list with contact details."
generated: { by: process:naming-workflows, at: YYYY-MM-DD }
status: backlog
trigger: "Weekly (Sunday)"
execution_mode: augmented   # manual | augmented | automated
---
# Lead Qualification

Identify and score prospects using research tools and qualification criteria. Produces ranked lead list with contact details.

# Artifacts

# Skills

# Agents

# Insights

<!-- GENERATED:insights -->
<!-- /GENERATED -->
```

Then add its line to the chosen Process's `# Workflows` list (`registry/processes/<process-slug>.md`) — never write `process:`, `owner:`, or `sequence:` on the Workflow node itself; process membership and sequence live only in the parent list.

**Default values:**
- Status: `backlog` (use this whenever the user is only cataloging ideas or naming ahead of deconstruct)
- Execution mode: `augmented` (human-in-the-loop) unless fully automated

**New Process rule:** if the chosen process doesn't exist yet as a Process node, ask **"Which function owns this process?"** — offer the registry's `functions/` list — and write a complete minimal Process node (`title`, `description`, `owner: <function-slug>`, an empty `# Workflows` list to append into) before adding the workflow's line. Never create an ownerless Process stub; the schema requires `owner:` on every Process node.

3. **Create or update `REGISTRY.md` at the workspace root** — this is part of the step, not optional. Follow the procedure in the `indexing-registry` skill if available; otherwise write the file directly from the registry data you have (Workflows / Skills / Agents tables, `—` for unknowns). Skip only if the environment can't write to the workspace root — and tell the user you skipped it, never silently.

Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step).

## Quick Reference

**Name formula:** `[Subject] [Action/Purpose]` (2-4 words, noun phrase)
**Description formula:** `[Action verb] [object] [condition]. [Outcome].` (1-2 sentences)
**Process Outcome:** Concrete deliverable (not "completed workflow")
**Sequence:** Multiples of 10 within Business Process (10, 20, 30...)

## Sequence Example

**Business Process:** ⚡ Lightning Lesson Launch

| Sequence | Workflow | Trigger |
|:--------:|----------|---------|
| 10 | Lightning Lesson Design | Ad-hoc (new lesson idea) |
| 20 | Lightning Lesson Content Creation | 2-3 weeks before event |
| 30 | Lightning Lesson Promotion | 2-3 weeks before event |
| 40 | Lightning Lesson Conversion | Post-event (within 48 hours) |

**Note:** Content Creation (20) and Promotion (30) could share sequence "20" if they run in parallel.
