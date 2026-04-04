---
title: "Step 5: Test"
description: Run structured tests on your AI workflow artifacts — smoke test, eval suite, building block evals — and establish a quality baseline before deployment.
---> **Part of:** [Business-First AI Framework](index.md)

## Where You Are

You've just finished [Build (Step 4)](build/index.mdx). You should have:

- **Platform artifacts** — prompts, skills, agents, and configs generated for your platform
- **Context artifacts** — style guides, reference materials, and examples
- **AI Building Block Spec** (`[name]-building-block-spec.md`) — which includes the evaluation criteria and test scenarios defined during [Design](design.md)

Your first run is a test, not a deployment. The goal is to verify that the workflow produces good output before you share it with your team or use it on real work.

## Your First Run

Start with a single test — pick one realistic scenario and run the workflow end to end. This is your smoke test. You are checking the basics:

- **Does it run at all?** — Can you execute every step without errors?
- **Does it produce output?** — Is there a result, or does it stall?
- **Is the output in the right format?** — Does it look like what you expected?

If any of these fail, go back to [Build](build/index.mdx) and fix the obvious issue before continuing. Common first-run problems:

- Missing context files the model references but cannot find
- MCP connections that are not configured or are not responding
- Skills that are installed but not correctly linked to the workflow

:::tip[Don't optimize yet]
The first run is about confirming the workflow functions. Resist the urge to fine-tune output quality — that comes next. Get it running, then evaluate.
:::
## Structured Evaluation

Once the smoke test passes, move to a full evaluation using the criteria defined during Design. Your AI Building Block Spec includes **evaluation dimensions** (the qualities you care about — accuracy, tone, completeness, specificity) and **test scenarios** (realistic inputs that exercise different parts of the workflow).

### Run the Eval Suite

For each test scenario:

1. **Run the workflow** with the test input
2. **Score the output** on each evaluation dimension using a 1-5 scale:

    | Score | Meaning |
    |-------|---------|
    | **5** | Excellent — ready to use as-is |
    | **4** | Good — minor edits only |
    | **3** | Acceptable — needs some rework but the structure is right |
    | **2** | Weak — significant gaps, wrong direction on one or more dimensions |
    | **1** | Failure — output is unusable or fundamentally off-target |

3. **Note specific issues** — What exactly was wrong? Which dimension scored low and why?

Record your scores. These become your baseline for measuring improvement (during this test cycle) and regression (during [Improve](improve.md)).

### Evaluate Building Blocks in Isolation

If the overall workflow scores poorly, test individual building blocks separately to isolate the problem:

- **Test a skill** by running it with sample inputs outside the full workflow. Does it produce the expected output on its own?
- **Test context** by asking the model a question that should be answerable from your reference materials. Does it find and use the right information?
- **Test an agent** by giving it a single task from the workflow. Does it use its tools correctly? Does it make reasonable decisions?

Isolating building blocks helps you find the weak link without guessing.

## Establish Your Baseline

After running the full eval suite, calculate an average score across all scenarios and dimensions. This is your **baseline** — the starting quality level of your workflow.

Record the baseline alongside your individual scores. You will use this number in two ways:

1. **During this test cycle** — to measure whether your fixes are improving things
2. **During [Improve (Step 7)](improve.md)** — to detect quality regression over time

:::note[What's a passing score?]
There is no universal threshold. A workflow that drafts internal meeting notes might be fine at 3.5 average. A workflow that generates client-facing proposals might need 4.5. You decide what "ready" means based on how much manual editing you are willing to accept.
:::
## Diagnose and Fix

When something is off, the fix depends on *what* went wrong. Use this table to map problems to building blocks:

| Problem | What to fix |
|---|---|
| Output is generic or off-brand | Add more **context** — examples, style guides, reference materials |
| Steps are skipped or misunderstood | Refine the **prompt** — make the instructions more explicit |
| A step needs domain expertise the AI does not have | Build a **skill** for that step — codify the expertise into a reusable routine |
| The AI needs to make unpredictable decisions | Convert from prompt to **agent** — let the AI plan its approach |
| Output format is wrong | Check the prompt's output format instructions — add explicit formatting examples |
| The model ignores your reference materials | Check that context files are correctly linked and formatted — the model may not be finding them |
| Tool connections fail during execution | Verify MCP connections — test each tool integration independently |

After each fix, re-run the affected test scenarios and compare scores to your previous run. You are looking for improvement on the dimensions that scored low.

## Code-First Troubleshooting

If you chose the code-first architecture approach during Design, you may encounter additional issues:

| Problem | What to check |
|---|---|
| API calls return errors | Verify API keys, rate limits, and request format match the provider's current spec |
| Agent does not use tools | Check that tools are correctly registered in the agent configuration and that permissions are granted |
| Multi-agent handoffs fail | Verify the output format of each agent matches the expected input format of the next agent in the pipeline |
| Scheduled runs produce different results | Check for time-dependent context (dates, market data) that may have changed between runs |
| SDK version mismatch | Ensure your SDK version matches the documentation the model used during Build — update if needed |

## Readiness Decision

After testing and iterating, you reach one of two outcomes:

**Ready to deploy.** You can run the workflow on a new scenario and trust the output without heavy editing. Your eval scores are at or above the threshold you set. Move to **[Step 6: Run](run.md)**.

**Not ready.** One or more dimensions consistently score below your threshold. Go back to **[Step 4: Build](build/index.mdx)**, fix the identified building blocks, and return to Test. Re-run the full eval suite — do not skip scenarios that passed previously, because a fix in one area can affect others.

:::note[2-4 iterations is normal]
Most workflows need multiple rounds of Build-then-Test before they are ready for deployment. Each iteration should be targeted — fix a specific issue, re-test, and measure improvement. If you have been through four iterations and scores are not improving, consider going back to [Design (Step 3)](design.md) to re-examine your architecture decisions.
:::
## How to Use This

This step is facilitated by the **`test`** Business-First AI Framework skill. See [Get the Skills](skills.mdx) for installation instructions across all supported platforms.

**Start with this prompt:**

```
Test my workflow against the evaluation criteria in the Building Block Spec.
```

The skill guides you through the smoke test, eval suite, building block evals, baseline establishment, and diagnosis process.

## Related

- [Design Your AI Workflow](design.md) — where evaluation criteria and test scenarios are defined
- [Build](build/index.mdx) — where you fix issues identified during testing
- [Run](run.md) — the next step once your workflow passes testing
- [Improve](improve.md) — where you re-run evals to detect regression on deployed workflows
