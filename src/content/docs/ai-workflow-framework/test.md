---
title: "Step 5: Test"
description: Test your AI workflow with a report card — each Deconstruct criterion is met or not met, with evidence, graded in a fresh conversation.
---

> **Part of:** [AI Workflow Framework](../)

## Where You Are

You've just finished [Build (Step 4)](../build/). You have an installed skill (or agent), the Design Spec, and the Workflow Requirements — which holds the yes/no acceptance criteria, rules, human gates, and 3–5 realistic inputs you wrote in [Deconstruct](../deconstruct/).

Your first run is a test, not a deployment.

## Six rules for judging your workflow

1. **Judge it against what you wrote in Deconstruct**, not against how the output feels.
2. **Use real inputs**, including one hard case.
3. **Run it in a fresh conversation.** A run inside the conversation that built it sees everything you said while building and looks better than it will in real use.
4. **Every criterion is met or it isn't.** One miss is a miss.
5. **The AI grades first, with evidence. You make the call.**
6. **Test, fix, test again.** Two to four rounds is normal. Don't fix mid-test.

## How the Skill Works

1. **Load context** — the requirements (criteria, rules, gates, inputs), the design spec, and where the built skill lives.
2. **Confirm the passing rule** — every line of the report card Met on every input; a miss on a **(must)** line always fails; any other miss is fixed or explicitly accepted.
3. **Smoke run** — the skill reads the built workflow against the requirements to catch obvious gaps before you spend a run.
4. **Integration pre-flight** — confirms each connector has the access it needs in the account that will run the workflow; a blocked write path is marked "not run", never faked.
5. **Run and grade each scenario** — you run each input in a new chat and bring the output back; the skill fills in the report card with evidence; you confirm or override each line.
6. **Diagnose every miss** — each Not met line is mapped to the building block that caused it.
7. **Verdict** — Ready, Not ready (back to Build, which regenerates only what's named), or Waiting on access.
8. **Clean up test records** — anything the test created in a live system is listed and offered for removal.

## The Report Card

For each input you run, the skill produces one table. Every row is something you said the workflow must do, tagged with where it came from:

| Expected | From | Result | Evidence |
|---|---|---|---|
| Every prospect row has contact info | AC1 (must) | Met | 20 of 20 rows |
| Never includes previously contacted people | R3 | Not met | 2 rows already in the CRM export |
| Pauses before sending | G1 | Met | Draft created, not sent |

`AC` rows are your acceptance criteria, `R` rows your rules, `G` rows your human gates, and each step's stated output gets a row too. The **Evidence** column is what makes the grade trustworthy: a count, a quoted phrase, a missing element — never "looks fine".

Where you supplied a **golden example** (a real past output that was exactly right), the skill compares against it: what's missing, what's extra, what's different in substance. A golden example is one good answer, not the only one — the question is "would you send this instead?" Keep at least one input without a golden example, so you learn whether the workflow generalizes.

After each input, one more question: how much would you have to edit this before using it — nothing, a little, or a lot? That answer is recorded, and its trend over time is the earliest sign of drift when you come back in [Improve](../improve/).

## Where the Workflow Runs

Two conversations:

- **The Test conversation** runs the `test` skill. It has your requirements and design. It grades.
- **A fresh conversation** has only the installed skill and one input. It runs. In Claude, start a new chat and ask for the skill by name; in ChatGPT, a new chat with the skill invoked by name. If the workflow lives in a project with context files, the fresh chat is inside that project.

You paste or attach the output back into the Test conversation. This keeps the run honest and, because the skill must be installed for the fresh chat to work, it proves the installation at the same time.

## Diagnose and Fix

| What went wrong | What to change |
|---|---|
| Output is generic or off-brand | Add **context** — examples, style guide, reference material |
| A step was skipped or misunderstood | The **orchestrator skill** — make that step's instruction explicit |
| A step needs expertise the AI doesn't have | A **component skill** — build or extend one for that step |
| Output format is wrong | The **orchestrator skill** — add an explicit format example |
| The AI ignored a reference file | **Context** — check the file is where the skill expects it and is readable |
| A tool call failed | The **connector** — verify it independently, then re-run |
| The AI had to make decisions your rules didn't cover | **Design** — the workflow may need an agent, or clearer rules |

Every miss names its building block, so Build knows exactly what to regenerate. After a fix, re-run the failed inputs, then the full set — a fix in one place can affect another.

## Readiness

**Ready** — every line met on every input, or a miss you looked at and accepted for a recorded reason. Move to **[Run](../run/)**.

**Not ready** — at least one miss you haven't accepted. Back to **[Build](../build/)**, which regenerates only the building blocks named in your results, then return here.

**Waiting on access** — the logic passed but a connector's write access isn't authorized yet. Fix the access; no rebuild needed.

:::note[Two to four rounds is normal]
If you've been through four rounds and the same lines keep failing, the problem is usually the design, not the build. Go back to [Design (Step 3)](../design/).
:::

## What This Produces

`outputs/[name]/test-results.md` — the report card per input, the diagnosis table, accepted misses, the verdict as a count ("11 of 12 lines met across 2 inputs"), and machine-readable frontmatter so [Improve](../improve/) can later show you exactly which lines changed.

## How to Use This

This step is facilitated by the **`test`** AI Workflow Framework skill. See [Set Up the Skills](../skills/) for installation instructions across all supported platforms.

**How to start:** Say *"run the test skill"* (or *"test the workflow"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:test`, and Cowork lists it when you type `/`.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
Test my workflow against the acceptance criteria in my Workflow Requirements.
```

## Related

- [Deconstruct Workflows](../deconstruct/) — where the criteria, rules, gates, and inputs are captured
- [Build](../build/) — where misses get fixed
- [Run](../run/) — the next step once every line is met
- [Improve](../improve/) — where the same report card is re-run to catch drift
