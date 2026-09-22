---
title: "Step 7: Improve"
description: "Step 7: Improve — re-run your report card against the baseline, see which lines flipped, and decide: no changes, tune, or go back to Design."
---

> **Part of:** [AI Workflow Framework](../)

## The Problem

Without a structured improvement process, AI workflows follow one of two failure patterns:

**Set and forget.** The workflow was useful when you built it, but business context has shifted, new tools have launched, and the output quality has drifted. Nobody notices until someone complains — or worse, until flawed output makes it to a client.

**Constant tinkering.** Someone tweaks the prompt every time the output is not perfect, introducing regressions and making it impossible to tell whether the workflow is actually getting better or just different. The team never trusts the workflow enough to rely on it.

Improve teaches you when to revisit a running workflow, how to evaluate it systematically, and what to do with the findings.

## When to Revisit

Not every workflow needs monthly check-ups. Watch for these quality signals — any one of them is reason to run an improvement cycle:

| Signal | What it means |
|--------|--------------|
| **Increasing manual edits** | Users are spending more time fixing output than they used to — quality may be drifting |
| **Changed business context** | Your products, audience, terminology, processes, or competitive landscape have shifted since the workflow was built |
| **New tools available** | Your platform has launched new features, MCP servers, or integrations that could make the workflow more capable |
| **Steps being skipped** | Users bypass certain steps because they are not adding value — the workflow may have unnecessary complexity |
| **Complaints or errors** | Someone reports that the output was wrong, off-brand, or missed something important |
| **Scheduled review cadence** | You set a review date during [Run (Step 6)](../run/) — it has arrived |

:::tip[Set a reminder during Run]
When you operationalize a workflow in Step 6, set a calendar reminder for your first review. Monthly is a good default for high-frequency workflows. Quarterly works for workflows you run less often.
:::

## How the Skill Works

The skill runs seven phases. The sections that follow expand on each:

1. **Load workflow context** — Read the Workflow node, Design Spec, Run Guide, the test results holding the baseline report card, and the run log if you've been keeping one.
2. **Current state assessment** — Start from the run log's evidence (run frequency, recurring edits, failures), then talk through what the log can't show: how much editing the output needs, and what has changed since you built it.
3. **Quality evaluation** — Read the signals: rising edits, new decision types, steps being skipped, lines flipping between rounds, or you adding steps by hand.
4. **Graduation assessment** — Has the workflow outgrown its mechanism?
5. **Regression check** — Re-run the same inputs the same way; compare line by line against the baseline and show every report-card line that flipped.
6. **Operationalization review** — For workflows a team uses: adoption, training, and governance. Skipped for personal workflows.
7. **Recommendation** — One of three outcomes: no changes needed, tune (fix specific building blocks), or go back to Design.

## Regression Check

*Plain language: a **regression check** re-runs the same inputs you tested in Step 5 and shows which report-card lines changed — the same lines, so a change means something moved.*

| Finding | What it means |
|---|---|
| **No line flipped, edits stable** | The workflow is holding up. |
| **A line flipped Met → Not met** | Something changed at that step or rule — context outdated, platform behaviour shifted, or a recent edit. The line names the cause. |
| **Several lines flipped at once** | Systemic — check for a platform update, a removed context file, or a broken connector. |
| **Edits rising with no flips** | Early drift. Look at what the edits have in common before a line fails. |
| **New inputs fail while old ones pass** | The criteria or context don't cover new situations — extend them in Requirements. |

Record the new report card alongside your baseline. This creates a quality history you can reference in future cycles.

## Graduation Assessment

Over time, some workflows outgrow their orchestration mechanism. The right response is not to keep patching — it is to graduate the workflow to a more capable mechanism.

### The Orchestration Ladder

| Current mechanism | Graduate to | When to graduate |
|---|---|---|
| **Skill** | **Agent** | The workflow needs to make sequencing decisions, use tools, or adapt its approach based on intermediate results — things a fixed skill sequence cannot efficiently orchestrate. |
| **Agent** (single) | **Agent** (multi-agent) | The agent is handling too many distinct responsibilities. Splitting into specialized agents (researcher, writer, editor) with clear handoffs improves quality and makes each agent easier to maintain. |

Graduation is not always the right answer. If the workflow works well at its current level, leave it. The goal is to match the mechanism to the workflow's actual needs — not to over-engineer.

If your Design Spec was written before v8 it may name the mechanism *Prompt* or *Skill-Powered Workflow*. Read *Skill-Powered Workflow* as *Skill*. A *Prompt* workflow's first graduation is to a Skill — the same instructions saved as a skill you invoke by name — and it is a Redesign outcome like the others.

Graduation is a Redesign outcome.

## For Organizations

If the workflow serves a team or business process, the improvement cycle includes an operationalization review:

- **Adoption** — Is the team using the workflow? If adoption has dropped, find out why and address it.
- **Training** — Are new team members being onboarded to the workflow? Update training materials if the workflow has changed.
- **Governance** — Are the right people maintaining the workflow? Have edit permissions stayed appropriate?
- **ROI** — Is the workflow still saving time or improving quality compared to the manual alternative? Quantify if possible.

## Decision Framework

Every improvement cycle ends with one of three outcomes:

| Outcome | What it means | Next step |
|---------|--------------|-----------|
| **No changes needed** | No line flipped, edits stable, no quality signals, workflow fits its purpose | Record the result and set the next review date |
| **Tune** | Specific building blocks need adjustment — context is outdated, a prompt needs refinement, a tool connection needs updating | Go to [Build (Step 4)](../build/), fix the identified issues, then [Test (Step 5)](../test/) |
| **Redesign** | Architecture assumptions have changed — different mechanism, new building blocks, or the workflow has outgrown a skill and needs an agent | Go to [Design (Step 3)](../design/) with the reason recorded |

The Improve step completes the lifecycle loop. Every outcome either confirms the workflow is healthy or sends you back to an earlier step with a specific target — never a vague "make it better."

## What This Produces

An **Improvement Plan** saved to `outputs/[workflow-name]/improvement-plan.md` that captures:

- Which report-card lines flipped since the baseline, and the edits trend
- Quality signals that triggered the review
- Findings from the regression check
- Graduation assessment (if applicable)
- Decision outcome and rationale
- Specific actions to take (which building blocks to fix, what context to update, etc.)
- Next review date

## How to Use This

This step is facilitated by the **`improve`** AI Workflow Framework skill. See [Set Up the Skills](../skills/) for installation instructions across all supported platforms.

**How to start:** Say *"run the improve skill"* (or *"review my workflow"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:improve`, and Cowork lists it when you type `/`.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
Evaluate my running workflow and help me decide what to improve.
```

The skill reads your Design Spec and previous test results, guides you through the regression check and graduation assessment, and produces the Improvement Plan.

### Example prompts

```
"Evaluate my running workflow and help me decide what to improve"
→ Full improvement cycle with regression check and decision

"My content workflow output quality has been dropping — help me figure out why"
→ Targeted regression check focused on the report-card lines
  that are degrading
```

## Related

- [Run](../run/) — the step before Improve
- [Test](../test/) — where the report card and baseline were established
- [Design](../design/) — where to go for a Redesign outcome
- [Build](../build/) — where to go for Tune outcomes
