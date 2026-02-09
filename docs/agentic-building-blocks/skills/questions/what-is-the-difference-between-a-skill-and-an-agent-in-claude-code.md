---
question: "What is the difference between a skill and an agent in Claude Code?"
short_answer: "A skill is a reusable routine that does one thing when invoked, while an agent is an autonomous system that plans, uses tools, and orchestrates multi-step workflows."
platforms: [claude]
topic: skills
date: 2026-02-08
author: James Gray
---

# What is the difference between a skill and an agent in Claude Code?

**Short answer:** A skill is a reusable routine that does one thing when invoked, while an agent is an autonomous system that plans, uses tools, and orchestrates multi-step workflows.

## The Full Answer

The core difference comes down to **autonomy and scope**. A skill is a packaged set of instructions — think of it as a specialized recipe or playbook that Claude follows when you invoke it. Skills are deterministic and focused: they do one thing well, consistently, every time. When you run a skill, you're giving Claude the knowledge of *how* to do something specific, like drafting a meeting recap or formatting a status report.

An agent, by contrast, is autonomous. It doesn't just follow a recipe — it decides what to do, breaks complex goals into steps, chooses which tools and skills to use, and iterates based on results (*as explained in the [official Claude documentation on agents](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)*). Agents maintain their own context windows, have access to tools (file operations, web search, code execution), and can invoke skills as part of larger workflows. If skills are tools in a toolbox, agents are the skilled worker using the toolbox to complete a project.

Consider a weekly client report workflow. A **skill** would package the instructions for formatting the report: "Take these inputs (updates, metrics, blockers) and produce a report in our standard template with these sections." You invoke it with this week's data, and it generates the report. An **agent**, on the other hand, could autonomously gather this week's completed tasks from your project management tool via MCP, pull time entries from your time tracker, generate the report using the skill, draft an email, and flag anything that needs your review — all without step-by-step prompting.

The distinction also affects **when you use each**. Use skills when you have a well-defined, repeatable task that you run manually but want to package for consistency and reuse across sessions. Use agents when the workflow requires planning, tool use, or multiple steps that would be tedious to coordinate through individual prompts (*as outlined in [Daniel Miessler's guide on when to use skills vs agents](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents)*). Skills and agents aren't mutually exclusive — in fact, they're complementary. A well-designed agentic workflow often involves agents that invoke skills at the right moments, combining the agent's autonomy with the skill's expertise (*as described in [The New Stack's analysis of skills and agents working together](https://thenewstack.io/ai-agents-or-skills-why-the-answer-is-both/)*).

## Example: Client Onboarding Workflow

Here's how the same workflow looks with a skill vs. an agent:

**Using a Skill:**
```markdown
You invoke: /skill client-onboarding-checklist

Input you provide:
- Client name: Acme Corp
- Project start date: 2026-02-15
- Primary contact: Jane Smith

The skill produces:
- A formatted onboarding checklist in your standard template
- Pre-filled sections with the client details
- Standard next steps and milestones
```

**Using an Agent:**
```markdown
You invoke: /agent onboard-new-client

Input you provide:
- Client name: Acme Corp

The agent autonomously:
1. Searches your CRM for the client record (via MCP)
2. Pulls the signed contract and extracts key dates
3. Creates a project workspace in your PM tool
4. Generates the onboarding checklist using the client-onboarding-checklist skill
5. Drafts a welcome email to the primary contact
6. Schedules a kickoff meeting based on team availability
7. Returns a summary of all actions taken
```

The skill does one focused task when you call it. The agent orchestrates an entire workflow, deciding what tools and skills to use along the way.

## Key Takeaways

- **Skills are routines** — they package reusable expertise and do one thing consistently when invoked
- **Agents are autonomous** — they plan, use tools, invoke skills, and execute multi-step workflows
- **Skills persist across sessions** — they're like permanent training that lives in Claude's knowledge base
- **Agents orchestrate workflows** — they decide *when* to use skills and *how* to sequence actions
- **They work together** — agents often invoke skills as part of larger workflows, combining autonomy with specialized expertise

## Related Questions

- [How do I create a skill in Claude Code?](../../platforms/claude/skills/index.md)
- [When should I use a skill vs. a project?](../skills/index.md)
- [What can agents do with MCP?](../mcp/index.md)

---

**Sources:**
- [Skills explained: How Skills compares to prompts, Projects, MCP, and subagents | Claude](https://claude.com/blog/skills-explained)
- [Agent Skills - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [When to Use Claude Code Skills vs Workflows vs Agents | Daniel Miessler](https://danielmiessler.com/blog/when-to-use-skills-vs-commands-vs-agents)
- [AI Agents or Skills? Why the Answer Is 'Both' - The New Stack](https://thenewstack.io/ai-agents-or-skills-why-the-answer-is-both/)
- [Claude Skills vs Sub-agents: Architecture, Use Cases, and Effective Patterns | Medium](https://medium.com/@SandeepTnvs/claude-skills-vs-sub-agents-architecture-use-cases-and-effective-patterns-3e535c9e0122)
