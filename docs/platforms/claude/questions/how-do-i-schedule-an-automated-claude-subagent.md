---
question: "How do I schedule an automated Claude subagent?"
short_answer: "Add scheduling instructions to your project's CLAUDE.md file, then ask Claude Code to schedule your subagent — it creates the wrapper scripts, logging, and OS-level scheduled task (launchd on macOS, Task Scheduler on Windows) automatically."
platforms: [claude]
topic: agents
date: 2026-02-02
author: James Gray
---

# How do I schedule an automated Claude subagent?

**Short answer:** Add scheduling instructions to your project's CLAUDE.md file, then ask Claude Code to schedule your subagent — it creates the wrapper scripts, logging, and OS-level scheduled task (launchd on macOS, Task Scheduler on Windows) automatically.

## The Full Answer

Claude Code subagents can run on a schedule without any human interaction — like a research assistant that gathers information while you sleep, or a competitor monitor that runs every Monday morning. The key is that Claude Code handles all the platform-specific scheduling configuration for you. You don't need to write cron jobs, plist files, or PowerShell scripts yourself.

The process has two prerequisites: Claude Code installed and authenticated, and a subagent already defined as a markdown file (e.g., `.claude/agents/my-agent.md`). Once those are in place, you add a scheduling section to your project's CLAUDE.md that tells Claude Code how to set up headless operation — using `--dangerously-skip-permissions` for unattended tool use, full paths to the Claude binary, and proper logging. Without these instructions, Claude Code won't know the special flags needed for scheduled operation and your subagent will fail silently.

With the CLAUDE.md updated, scheduling is as simple as asking Claude Code: "Schedule my research-daily subagent to run every weekday at 7:30 AM." Claude Code creates the wrapper script, configures the OS scheduler (launchd on macOS, Task Scheduler on Windows), sets up logging, and activates it. On macOS, if your machine is asleep at the scheduled time, the subagent runs when it wakes up.

You manage scheduled subagents entirely through Claude Code — pausing, resuming, changing schedules, viewing logs, and removing tasks are all conversational commands.

## How to Get Started

Follow the step-by-step guide: **[Scheduling Claude Code Subagents](../subagents/scheduling-subagents.md)**

The guide covers:

1. Adding the required scheduling instructions to your CLAUDE.md
2. Asking Claude Code to create the schedule
3. Testing the subagent manually
4. Managing and troubleshooting scheduled tasks

### Common Scheduling Patterns

| Subagent Type | Suggested Schedule | Example Prompt |
|---------------|-------------------|----------------|
| Daily news/research | Weekdays at 7–8 AM | "Run every weekday at 7:30 AM" |
| Competitor monitoring | Weekly on Monday | "Run every Monday at 8:00 AM" |
| Weekly summaries | Friday afternoon | "Run every Friday at 4:00 PM" |
| Frequent updates | Every few hours | "Run every 4 hours during business hours" |

## Key Takeaways

- Claude Code handles all the OS-level scheduling configuration — you just ask it in natural language
- You must add scheduling instructions to your project's CLAUDE.md first, or headless operation will fail silently
- Subagents use `--dangerously-skip-permissions` to run unattended — review what your subagent does before enabling this
- On macOS, launchd catches up on missed runs when your machine wakes — your morning digest still gets created
- Manage everything through Claude Code: pause, resume, reschedule, view logs, and remove tasks conversationally

## Related Questions

- [What is the best way to name Claude agent skills?](./what-is-the-best-way-to-name-claude-agent-skills.md)
- [Scheduled Subagent Troubleshooting](../subagents/scheduling-subagent-issues.md)
