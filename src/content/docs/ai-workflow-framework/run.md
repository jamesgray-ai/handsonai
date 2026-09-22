---
title: "Step 6: Run"
description: "Step 6: Run — do the first real run on real work, then leave a one-page Run Card, a run log, and a review date behind for whoever runs it next."
---

> **Part of:** [AI Workflow Framework](../)

## Where You Are

You've just finished [Test (Step 5)](../test/). Your workflow:

- Passes its report card — every criterion met, or a miss you've explicitly accepted
- Has a recorded baseline for future comparison
- Has its skills, agents, and connectors installed on the platform that will run it

Every run so far used test inputs. Run is where the workflow does this week's real work.

| | |
|---|---|
| **What you'll do** | Do the first real run on real work with the model watching, then agree a review date |
| **What you'll get** | A one-page **Run Card**, a run log, and a `stale_after` review date on your Workflow node |
| **Time** | ~15–20 minutes |

## How the Skill Works

The skill runs four steps:

1. **Load context** — the Workflow node, the Design Spec, the installed artifacts, and the test results (if the verdict isn't Ready, it sends you back to Test).
2. **The first real run** — your real input, in a fresh session, started the way an operator would start it.
3. **Write the Run Card** — the one page you'll actually use, saved to `outputs/[name]/run-guide.md`.
4. **Run log, registry, review date** — today's run logged, the node marked in production, and the next review scheduled.

## Your Run Card

The Run Card is one page with six fixed sections, in this order. It is written after the first real run, not before — so it describes what actually happened rather than what should:

1. **Your first real run** — what happened today, in two sentences, and what to expect next time.
2. **How to start it** — the exact phrase or click that starts the workflow, and the input to give it. If teammates will run it too, how they install it and the same phrase.
3. **What to have ready** — the inputs in hand; the skills and agents installed in the account that runs it; every connector that must be authorized **in that same account**; every context file, with its location — and, for an unattended run, the permissions granted in advance. A fresh conversation inherits nothing from the session that built the workflow, and an unattended run inherits less — this list is what a clean session needs to succeed.
4. **What to check before you act on the output** — the human gates in plain words (what the workflow pauses for and what you're deciding), plus your **(must)** criteria as a two-line reminder.
5. **Log the run** — one line in `outputs/[name]/runs.md`: date, input, result, edits needed, notes.
6. **Your first review** — the date, and the exact sentence that re-enters the framework: *"Run the improve skill on [workflow name]."*

The Run Card is shown to you in the conversation and saved to `outputs/[name]/run-guide.md`, so you can reopen it weeks later or hand it to someone else.

### Keep a run log

The run skill also creates `outputs/[name]/runs.md` — a one-line-per-run log (date, input, result, edits needed). It takes ten seconds per run, and when you review the workflow later in [Improve (Step 7)](../improve/), it's the difference between "I think it's been fine?" and actual evidence of drift, recurring edits, or failures. If the workflow runs on the platform itself, Build wires self-logging into the orchestrator artifact so it appends its own log line each run (Run verifies it did on today's run) — logging costs you nothing.

## How It Gets Started

"How to start it" on your Run Card is one of these. Most workflows are the first two:

| Pattern | What it means | Best for |
|---------|--------------|----------|
| **Run the skill** | Open a fresh conversation and invoke the workflow by name | The default: any workflow you start yourself, wherever you already work |
| **Run in a project** | Invoke it inside a persistent workspace that already holds the context files | Workflows you repeat against the same reference materials |
| **Let the agent run** | Describe what you need and let the agent orchestrate the steps and tools | Multi-step workflows with tool use and decisions between steps |
| **On a schedule** | A trigger runs it without you — **Automated workflows only** | Recurring work with no human input during the run (daily digests, weekly reports, monitoring) |

Start with the simplest pattern that fits. You can always move to a more involved one later.

### Run in a Project

Set up a persistent workspace where your prompt, context files, and settings are pre-loaded. That way you do not re-attach the same files every run.

**When to use it:**

- You run the workflow regularly (weekly or more)
- The workflow uses the same reference materials each time
- You want consistent settings (model, instructions) across runs

**How to do it:** Create a project on your platform (Claude Project, ChatGPT Project or Workspace Agent, Gemini Gem, M365 Copilot notebook). Upload your context files, add the orchestrator skill (or, on platforms without skills, its instructions) as project instructions, and configure any settings. Future runs start with everything in place — you just provide the new input.

### Let the Agent Run

For agent-based workflows, you describe what you need in natural language and let the agent orchestrate the process — invoking skills, using tools, and making sequencing decisions.

**When to use it:**

- The workflow involves multiple steps with tool use
- The agent needs to make decisions based on intermediate results
- You want hands-off execution with review at defined checkpoints

**How to do it:** Make sure your agent is installed and configured (Build did this, and the Run Card's "What to have ready" lists what it needs). Then describe your task — the agent picks the right tools and follows its instructions. Review output at any human-in-the-loop gates before the agent continues.

### Automate on a Schedule

**Only for workflows designed as Automated.** If your Workflow node's execution mode is `augmented`, the workflow runs when you start it, and that's the whole answer — come back to this step later if that changes. Scheduling an augmented workflow removes the person the design assumed would be there.

For an automated workflow, the skill states your platform's scheduling mechanism, the pre-granted permissions and non-interactive credentials it needs, and then the **safety checklist** from your Design Spec's Safety & Permissions section, in plain words:

- Least-privilege scopes — only what the workflow actually does, nothing broader
- Human gates and draft-don't-send actually enforced in the deployed artifacts, not just described in the spec
- Content you didn't author (inbound email, web pages, form submissions) treated as data, never as instructions
- A cap on actions per run
- Every write visible in the run log

An unattended run can do exactly what its pre-granted permissions allow, with nobody watching — that checklist is the difference between a scheduled workflow and an unsupervised one. If your platform doesn't support unattended runs, the skill says so and names the platforms that do rather than improvising a workaround.

## Operationalize for Your Team

For individual workflows, deployment may be as simple as running the workflow yourself and using the output. For organizational workflows — ones that serve a team, department, or company — additional steps help ensure adoption and sustainability.

### Share and Train

- **Document the workflow** — Your Run Card is the primary reference. Share it with anyone who will run the workflow.
- **Create a short walkthrough** — A 5-minute screen recording showing someone running the workflow from start to finish is more effective than written instructions for visual learners.
- **Identify a workflow owner** — Someone who understands the workflow well enough to troubleshoot, train new users, and make the call on when it needs updating.

### Set Governance Expectations

- **Who can modify the workflow?** — Define who has permission to edit the prompt, update context files, or change agent configurations. Unrestricted edits by well-meaning teammates can degrade quality quickly.
- **When should the workflow be reviewed?** — Set a cadence (monthly or quarterly) or trigger conditions (business process changes, quality complaints) for revisiting the workflow in [Improve (Step 7)](../improve/).
- **Where do outputs go?** — Define where the workflow's outputs are stored and who has access. This matters for compliance, audit trails, and team coordination.

### Monitor Adoption

In the first few weeks after deployment, check:

- **Is the workflow being used?** — If adoption is low, find out why. Common reasons: the workflow is hard to run, the output needs too much editing, or people do not know it exists.
- **Is the output quality holding up?** — Early feedback from actual users often surfaces issues that testing missed.
- **Are people working around the workflow?** — If users skip the workflow and do the work manually, that is a signal that something is not working.

## How to Use This

This step is facilitated by the **`run`** AI Workflow Framework skill. See [Set Up the Skills](../skills/) for installation instructions across all supported platforms.

**How to start:** Say *"run the run skill"* (or *"put my workflow into production"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:run`, and Cowork lists it when you type `/`.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
Put my workflow into production — let's do the first real run.
```

The skill reads your Design Spec, your installed artifacts, and your test results, runs the workflow on real work with you, then writes the Run Card, starts the run log, and sets the review date.

### Example prompts

```
"Run the run skill on my weekly status report"
→ Does the first real run, then writes the Run Card and run log

"This one needs to run every Monday without me"
→ Checks it was designed as Automated, then walks the
  scheduling setup and the safety checklist
```

## Next Step

Once your workflow is running in production, the run skill records a `stale_after` review date on the Workflow node (monthly for high-frequency workflows, quarterly for occasional ones). When that date arrives — or sooner, if quality signals suggest it — start a new conversation and say: **"Run the `improve` skill on [workflow name]."** The node, baseline test scores, and run log carry everything **[Step 7: Improve](../improve/)** needs; you don't have to re-explain the workflow.

## Related

- [Test](../test/) — the step before Run
- [Improve](../improve/) — the step after Run
- [Build](../build/) — where to go if deployment reveals issues that need fixes
- [AI Workflow Design Matrix](../workflow-design-matrix/) — how autonomy and involvement combine into workflow archetypes
