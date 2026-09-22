---
title: "Step 7: Improve"
description: "Step 7: Improve — evaluate a running AI workflow for quality, relevance, and evolution with periodic review, regression checks, and a graduation decision."
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

The skill runs six phases. The sections that follow expand on each:

1. **Load history** — Read the Workflow node, Design Spec, previous test results (the baseline report card lives in the file's frontmatter), and the run log if you've been keeping one.
2. **Quality signal review** — Start from the run log's evidence (run frequency, recurring edits, failures), then discuss what prompted this improvement cycle. Which signals are you seeing?
3. **Regression evaluation** — Re-run the same inputs the same way; compare line by line and show every criterion that flipped between met and not met.
4. **Graduation assessment** — Should the orchestration mechanism evolve (Skill → Agent, single agent → multi-agent)?
5. **Decision** — Three outcomes: no changes needed, tune (fix specific building blocks), or go back to Design (the architecture no longer fits, including a workflow that has outgrown its mechanism).
6. **Generate Improvement Plan** — Current report card, comparison to baseline, findings, decision, and specific actions.

## Regression Evaluation

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

Over time, some workflows outgrow their orchestration mechanism. A prompt that started simple may have accumulated so many instructions that it is unwieldy. A skill-powered workflow may need to make decisions you cannot predict in advance. The right response is not to keep patching — it is to graduate the workflow to a more capable mechanism.

### The Orchestration Ladder

| Current mechanism | Graduate to | When to graduate |
|---|---|---|
| **Skill** | **Agent** | The workflow needs to make sequencing decisions, use tools, or adapt its approach based on intermediate results — things a fixed skill sequence cannot efficiently orchestrate. |
| **Agent** (single) | **Agent** (multi-agent) | The agent is handling too many distinct responsibilities. Splitting into specialized agents (researcher, writer, editor) with clear handoffs improves quality and makes each agent easier to maintain. |

Graduation is not always the right answer. If the workflow works well at its current level, leave it. The goal is to match the mechanism to the workflow's actual needs — not to over-engineer.

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
- Findings from the regression evaluation
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

The skill reads your Design Spec and previous test results, guides you through the regression evaluation and graduation assessment, and produces the Improvement Plan.

### Example prompts

```
"Evaluate my running workflow and help me decide what to improve"
→ Full improvement cycle with regression eval and decision

"My content workflow output quality has been dropping — help me figure out why"
→ Targeted regression evaluation focused on the quality dimensions
  that are degrading
```

## Related

- [Run](../run/) — the step before Improve
- [Test](../test/) — where the report card and baseline were established
- [Design](../design/) — where to go for a Redesign outcome
- [Build](../build/) — where to go for Tune outcomes
