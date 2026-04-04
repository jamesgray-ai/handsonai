---
title: "Step 6: Run"
description: Deploy your tested AI workflow — choose a run pattern, follow your Run Guide, share with your team, and operationalize for ongoing use.
---> **Part of:** [Business-First AI Framework](index.md)

## Where You Are

You've just finished [Test (Step 5)](test.md). Your workflow:

- Passes the eval suite at a quality level you trust
- Has a recorded baseline for future comparison
- Has platform artifacts ready for deployment

Now it is time to put the workflow into production use.

## Start with Your Run Guide

At the end of Build and Test, the model generates a **Run Guide** (`[name]-run-guide.md`) — a plain-language walkthrough tailored to your platform, architecture approach, and technical comfort level. It tells you exactly what to do with the artifacts that were built:

1. **What was built** — Every artifact listed with what it does and where it lives
2. **Setup steps** — Numbered instructions for getting each artifact into the right place on your platform (menu paths, button names, what you should see when it is working)
3. **First production run** — A guided run with real input, expected behavior, and what to check
4. **What to do next** — How to run it again, share with teammates, and when to revisit

The Run Guide is saved to `outputs/[name]-run-guide.md` so you can reference it later or share it with your team.

## Choose Your Run Pattern

Not every workflow runs the same way. The right pattern depends on how often you use the workflow, how technical you are, and whether the workflow runs attended or unattended.

| Pattern | What it means | Best for |
|---------|--------------|----------|
| **Paste and run** | Copy the prompt into any AI chat and run it | One-off tasks, sharing with non-technical teammates |
| **Run in a project** | Set up a persistent project workspace with pre-loaded context | Workflows you repeat with the same reference materials |
| **Command an agent** | Describe what you need and let the agent handle it | Multi-step workflows that benefit from tool use and autonomous decisions |
| **Code-first** | Run via API or SDK from your own application | Production integrations, high-volume processing, custom UIs |
| **Automate on schedule** | Set up a scheduled trigger so the workflow runs without you | Recurring tasks (daily reports, weekly summaries, monitoring) |

Start with the simplest pattern that fits your needs. You can always move to a more advanced pattern later.

### Paste and Run

The most portable option. Copy your prompt (and any context) into a chat with your AI tool and run it. This works with any AI platform — Claude, ChatGPT, Gemini, M365 Copilot, or any other tool that accepts text input.

**When to use it:**

- You run the workflow occasionally (not daily)
- You want to share it with someone who does not have your platform setup
- You are testing a new variation before committing to a more permanent setup

**How to do it:** Open your AI tool, paste the prompt, attach any context files referenced in the prompt, and submit. Review the output and iterate in conversation if needed.

### Run in a Project

Set up a persistent workspace where your prompt, context files, and settings are pre-loaded. This eliminates the need to paste and attach files every time.

**When to use it:**

- You run the workflow regularly (weekly or more)
- The workflow uses the same reference materials each time
- You want consistent settings (model, instructions) across runs

**How to do it:** Create a project on your platform (Claude Project, ChatGPT GPT, Gemini Gem, M365 Copilot notebook). Upload your context files, add your prompt as project instructions or a system prompt, and configure any settings. Future runs start with everything in place — you just provide the new input.

### Command an Agent

For agent-based workflows, you describe what you need in natural language and let the agent orchestrate the process — invoking skills, using tools, and making sequencing decisions.

**When to use it:**

- The workflow involves multiple steps with tool use
- The agent needs to make decisions based on intermediate results
- You want hands-off execution with review at defined checkpoints

**How to do it:** Make sure your agent is installed and configured (follow the Run Guide). Then describe your task — the agent picks the right tools and follows its instructions. Review output at any human-in-the-loop gates before the agent continues.

### Code-First

Run the workflow programmatically via API or SDK. This is for workflows that integrate into your own applications, process data at scale, or need custom logic around the AI calls.

**When to use it:**

- The workflow is part of a larger application
- You need to process many inputs in batch
- You want programmatic control over the execution flow

**How to do it:** Use the API or SDK artifacts generated during Build. Your Run Guide includes the specific endpoints, authentication setup, and code examples for your platform. Integrate the calls into your application and add error handling appropriate to your use case.

### Automate on a Schedule

Set up a trigger so the workflow runs without manual intervention — daily, weekly, or on a custom schedule.

**When to use it:**

- The workflow should run at a regular cadence (daily news digest, weekly report, monthly review)
- You want the output waiting for you rather than having to remember to run it
- The workflow does not require human input during execution

**How to do it:** The approach depends on your platform and architecture:

- **Claude Code** — Use a scheduled task (launchd on Mac, Task Scheduler on Windows) with `claude -p "your prompt" --dangerously-skip-permissions`
- **API-based** — Set up a cron job, GitHub Action, or cloud scheduler that calls your API endpoint
- **Platform-native** — Some platforms offer built-in scheduling or automation triggers

Your Run Guide includes platform-specific scheduling instructions if your workflow supports it.

## Operationalize for Your Team

For individual workflows, deployment may be as simple as running the workflow yourself and using the output. For organizational workflows — ones that serve a team, department, or company — additional steps help ensure adoption and sustainability.

### Share and Train

- **Document the workflow** — Your Run Guide serves as the primary reference. Share it with anyone who will run the workflow.
- **Create a short walkthrough** — A 5-minute screen recording showing someone running the workflow from start to finish is more effective than written instructions for visual learners.
- **Identify a workflow owner** — Someone who understands the workflow well enough to troubleshoot, train new users, and make the call on when it needs updating.

### Set Governance Expectations

- **Who can modify the workflow?** — Define who has permission to edit the prompt, update context files, or change agent configurations. Unrestricted edits by well-meaning teammates can degrade quality quickly.
- **When should the workflow be reviewed?** — Set a cadence (monthly or quarterly) or trigger conditions (business process changes, quality complaints) for revisiting the workflow in [Improve (Step 7)](improve.md).
- **Where do outputs go?** — Define where the workflow's outputs are stored and who has access. This matters for compliance, audit trails, and team coordination.

### Monitor Adoption

In the first few weeks after deployment, check:

- **Is the workflow being used?** — If adoption is low, find out why. Common reasons: the workflow is hard to run, the output needs too much editing, or people do not know it exists.
- **Is the output quality holding up?** — Early feedback from actual users often surfaces issues that testing missed.
- **Are people working around the workflow?** — If users skip the workflow and do the work manually, that is a signal that something is not working.

## How to Use This

This step is facilitated by the **`run`** Business-First AI Framework skill. See [Get the Skills](skills.mdx) for installation instructions across all supported platforms.

**Start with this prompt:**

```
Generate a Run Guide for my workflow and help me deploy it.
```

The skill reads your Building Block Spec and artifacts, generates the Run Guide, and walks you through choosing a run pattern and getting the workflow into production.

## Next Step

Once your workflow is running in production, set a reminder to revisit it. Move to **[Step 7: Improve](improve.md)** when quality signals suggest it is time — or on the review cadence you set during operationalization.

## Related

- [Test](test.md) — the step before Run
- [Improve](improve.md) — the step after Run
- [Build](build/index.mdx) — where to go if deployment reveals issues that need fixes
- [AI Workflow Design Matrix](workflow-design-matrix.md) — how autonomy and involvement combine into workflow archetypes
