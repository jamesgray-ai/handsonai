---
title: "Step 7: Improve"
description: Evaluate a running AI workflow for quality, relevance, and evolution opportunities — periodic review, regression evaluation, graduation assessment, and decision framework.
---> **Part of:** [Business-First AI Framework](index.md)

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
| **Scheduled review cadence** | You set a review date during [Run (Step 6)](run.md) — it has arrived |

:::tip[Set a reminder during Run]
When you operationalize a workflow in Step 6, set a calendar reminder for your first review. Monthly is a good default for high-frequency workflows. Quarterly works for workflows you run less often.
:::
## Regression Evaluation

Re-run the **eval suite** from [Test (Step 5)](test.md) using the same test scenarios and scoring dimensions. Then compare results to your recorded baseline.

### What to look for

| Finding | What it means |
|---------|--------------|
| **Scores are stable or improving** | The workflow is holding up. No action needed unless you identified other quality signals. |
| **Scores dropped on specific dimensions** | Something has changed — context may be outdated, platform behavior may have shifted, or recent edits to the prompt introduced a regression. |
| **Scores dropped across the board** | A systemic issue. Check whether a platform update changed default behavior, a context file was removed, or a tool connection broke. |
| **New scenarios produce poor results** | The workflow works for the original test cases but not for new situations. The prompt or context may need to be expanded to cover additional cases. |

Record the new scores alongside your baseline. This creates a quality history you can reference in future cycles.

## Graduation Assessment

Over time, some workflows outgrow their orchestration mechanism. A prompt that started simple may have accumulated so many instructions that it is unwieldy. A skill-powered prompt may need to make decisions you cannot predict in advance. The right response is not to keep patching — it is to graduate the workflow to a more capable mechanism.

### The Orchestration Ladder

| Current mechanism | Graduate to | When to graduate |
|---|---|---|
| **Prompt** | **Skill-Powered Prompt** | Steps have become complex enough that you are repeating the same multi-step instructions across runs. Extracting those into reusable skills would make the prompt cleaner and the sub-steps more reliable. |
| **Skill-Powered Prompt** | **Agent** | The workflow needs to make sequencing decisions, use tools, or adapt its approach based on intermediate results — things a human following a fixed skill sequence cannot efficiently orchestrate. |
| **Agent** (single) | **Agent** (multi-agent) | The agent is handling too many distinct responsibilities. Splitting into specialized agents (researcher, writer, editor) with clear handoffs improves quality and makes each agent easier to maintain. |

Graduation is not always the right answer. If the workflow works well at its current level, leave it. The goal is to match the mechanism to the workflow's actual needs — not to over-engineer.

:::note[Graduation means going back to Design]
When you graduate a workflow to a new mechanism, you are changing the architecture. Return to [Design (Step 3)](design.md) to reassess the orchestration mechanism, update the Building Block Spec, then proceed through Build and Test with the new architecture.
:::
## For Organizations

If the workflow serves a team or business process, the improvement cycle includes an operationalization review:

- **Adoption** — Is the team using the workflow? If adoption has dropped, find out why and address it.
- **Training** — Are new team members being onboarded to the workflow? Update training materials if the workflow has changed.
- **Governance** — Are the right people maintaining the workflow? Have edit permissions stayed appropriate?
- **ROI** — Is the workflow still saving time or improving quality compared to the manual alternative? Quantify if possible.

## Decision Framework

Every improvement cycle ends with one of four outcomes:

| Outcome | What it means | Next step |
|---------|--------------|-----------|
| **No changes needed** | Eval scores are stable, no quality signals, workflow fits its purpose | Record the result and set the next review date |
| **Tune** | Specific building blocks need adjustment — context is outdated, a prompt needs refinement, a tool connection needs updating | Go to [Build (Step 4)](build/index.mdx), fix the identified issues, then [Test (Step 5)](test.md) |
| **Redesign** | Architecture assumptions have changed — the workflow needs a different orchestration mechanism, new building blocks, or a fundamentally different approach | Go to [Design (Step 3)](design.md) and rework the Building Block Spec |
| **Evolve** | The workflow should graduate to a more capable orchestration mechanism (see [Graduation Assessment](#graduation-assessment)) | Go to [Design (Step 3)](design.md) and upgrade the mechanism |

The Improve step completes the lifecycle loop. Every outcome either confirms the workflow is healthy or sends you back to an earlier step with a specific target — never a vague "make it better."

## What This Produces

An **Improvement Plan** saved to `outputs/[workflow-name]-improvement-plan.md` that captures:

- Current eval scores compared to baseline
- Quality signals that triggered the review
- Findings from the regression evaluation
- Graduation assessment (if applicable)
- Decision outcome and rationale
- Specific actions to take (which building blocks to fix, what context to update, etc.)
- Next review date

## How to Use This

This step is facilitated by the **`improve`** Business-First AI Framework skill. See [Get the Skills](skills.mdx) for installation instructions across all supported platforms.

**Start with this prompt:**

```
Evaluate my running workflow and help me decide what to improve.
```

The skill reads your Building Block Spec and previous test results, guides you through the regression evaluation and graduation assessment, and produces the Improvement Plan.

## Related

- [Run](run.md) — the step before Improve
- [Test](test.md) — where the eval suite and baseline were established
- [Design](design.md) — where to go for Redesign or Evolve outcomes
- [Build](build/index.mdx) — where to go for Tune outcomes
