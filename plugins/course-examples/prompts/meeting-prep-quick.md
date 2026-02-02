# Meeting Prep Quick Prompt

A portable prompt for quick meeting preparation. Works with any AI tool — Claude, ChatGPT, Gemini, or M365 Copilot. For a more thorough, automated research experience in Claude Code, use the `meeting-prep-researcher` agent instead.

## How to Use

1. Copy the prompt below into any AI conversation
2. Fill in the details about your upcoming meeting
3. Review and refine the output before your meeting

## The Prompt

```text
I have an upcoming meeting and need to prepare. Here are the details:

**Meeting with:** [Name(s) and title(s)]
**Company:** [Company name]
**Meeting type:** [Sales call / partnership discussion / interview / team sync / other]
**My goal:** [What I want to accomplish in this meeting]
**Context:** [Any additional context — how we connected, prior conversations, etc.]

Please research the attendee(s) and company, then produce a concise meeting prep brief that includes:

1. **Attendee profiles** — Background, role, recent public activity, and 1-2 specific conversation starters
2. **Company snapshot** — What they do, recent news (last 90 days), and apparent strategic priorities
3. **Suggested talking points** — 3 specific points tailored to my goal, with brief rationale for each
4. **Questions to ask** — 3 thoughtful questions that demonstrate preparation and advance my goal
5. **Watch out for** — Any sensitive topics, potential objections, or landmines to avoid

Keep the brief scannable — I should be able to read it in under 5 minutes. Prioritize recent, specific, actionable information over generic background.
```

## When to Use This vs. the Agent

| Scenario | Use this prompt | Use the agent |
|----------|----------------|---------------|
| Quick prep in any AI tool | Yes | No — agent is Claude Code only |
| Deep research with follow-up questions | No — limited to one exchange | Yes — agent can iterate |
| Need to prep for multiple meetings | Copy-paste for each | Agent handles the conversation flow |
| Team members without Claude Code | Yes | Not available to them |
