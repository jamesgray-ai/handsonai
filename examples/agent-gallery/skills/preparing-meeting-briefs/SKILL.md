---
name: preparing-meeting-briefs
description: >
  This skill should be used when the user wants to prepare for a meeting, research attendees
  or companies before a call, or needs talking points for an upcoming conversation. Produces
  a structured meeting prep brief with attendee profiles, company snapshots, talking points,
  and suggested questions.
user-invocable: true
---

# Preparing Meeting Briefs

Research meeting attendees and their companies to produce a concise, actionable prep brief.

## Workflow

1. **Gather meeting details** — Ask for: attendee name(s), company, meeting type, and the user's goal
2. **Research attendees** — Search for LinkedIn profiles, recent posts, and public activity
3. **Research company** — Search for recent news, strategic direction, and relevant context
4. **Synthesize brief** — Produce a formatted Meeting Prep Brief (see format below) and write it to `outputs/meeting-prep-[company-name].md`. Create the `outputs/` directory if it doesn't exist.
5. **Refine with user** — Ask if any section needs more depth or adjustment

## Output Format

```markdown
**Meeting Prep Brief**

**Meeting:** [Purpose]
**With:** [Names and roles]

### Attendee Profiles
[Name — Title at Company]
- Background: [2-3 sentences]
- Recent activity: [Notable posts or statements]
- Conversation starters: [1-2 specific topics]

### Company Snapshot
- What they do: [One sentence]
- Recent news: [2-3 bullets, last 90 days]
- Strategic priorities: [Current focus areas]

### Suggested Talking Points
1. [Point with rationale]
2. [Point with rationale]
3. [Point with rationale]

### Questions to Ask
1. [Preparation-demonstrating question]
2. [Priority-surfacing question]
3. [Goal-advancing question]

### Watch Out For
- [Sensitive topics or potential objections]
```

## Research Guidelines

- **Prioritize recency** — information from the last 90 days is most valuable
- **Be specific** — "They launched X product in January" beats "They're focused on innovation"
- **Flag uncertainty** — distinguish verified facts from reasonable inferences
- **Keep it scannable** — the brief should take under 5 minutes to read
- After writing the brief, tell the user: "Meeting prep brief saved to `outputs/meeting-prep-[company-name].md`. Review it before your meeting and let me know if any section needs more depth."
