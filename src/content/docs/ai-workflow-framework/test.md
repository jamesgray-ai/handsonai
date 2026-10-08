---
title: "Step 5: Test"
description: Test your AI workflow with a report card — each Deconstruct criterion is met or not met, with evidence, graded in the new chat where the run happened.
---

> **Part of:** [AI Workflow Framework](../)

## Where You Are

You've just finished [Build (Step 4)](../build/). You have an installed skill (or agent), a Design Spec, and a Workflow Requirements document. The Requirements holds the yes/no acceptance criteria, the rules, the human gates, and the 3–5 realistic inputs you wrote in [Deconstruct](../deconstruct/) — each input saved as its own file under `outputs/[workflow-name]/inputs/`.

Your first run is a test, not a deployment. This step takes about 45 minutes per round, and most workflows need two to four rounds before they're ready. That's normal, not failure.

## The Words You'll Hear

| Word | What it means |
|---|---|
| **Round** | One full pass of testing: every input run once, then a verdict. A fix in Build starts a new round. |
| **Input** | One realistic thing to run the workflow on — a real tracker export, a real email, a real brief. Deconstruct saved 3–5 of these as files and numbered them E1, E2, E3… The skill also calls them *scenarios*. |
| **Opening chat** | The chat where you start the `test` skill. It reads your Requirements and Design, writes the check list, and keeps the results file. On the separate-chats path, you come back to it after every run. |
| **Run chat** | A brand-new chat where you run the workflow on one input, exactly as an operator would. One run chat per input. |
| **Check list** | Every behaviour your workflow must show, pulled from your Requirements: acceptance criteria (AC1, AC2…), rules (R1, R2…), human gates (G1, G2…), and each step's stated output. |
| **Report card** | The table the skill produces after each run: one row per check-list line, Met or Not met, with evidence. |
| **"What I did"** | The short summary every workflow you built prints at the end of a run — the steps it took, where it paused for you, what it did with your tools, and where the result is. The skill uses it as evidence. |

## Before You Start

Confirm these three things. Each one takes a minute and saves you a wasted run.

1. **The skill is installed.** Open a new chat and ask for your workflow's skill by name (for example, *"run the weekly-status-report skill"*). If it responds as your workflow, you're set. If it doesn't know what you mean, go back to [Build](../build/) and finish the install step.
2. **Your inputs exist.** Open `outputs/[workflow-name]/inputs/`. There should be one file per input (E1, E2…). If any file holds only a placeholder line telling you what to paste in, get that real input ready now.
3. **You know what your workflow touches.** If it sends email, writes to a CRM, or creates calendar events, a test run does that for real. Decide now whether to point it at a test record (a test contact, a draft folder, a copy of the sheet). The skill will list everything the round created and offer to remove it at the end — but it can't unsend an email.

## Where You Run From

Two chats are involved in every round, and each one needs different things in reach.

**The opening chat needs your workspace.** That's the folder holding everything the framework has produced so far: `registry/` (your Workflow node), `outputs/[workflow-name]/` (requirements, design spec, the inputs), and the built skill. The `test` skill reads all of those and writes the results file next to them.

- **Claude Code, Codex, Gemini CLI:** open the session *in that folder*. Every chat opened there shares the same files.
- **Cowork:** connect that folder as the working folder (a Project is not required), then start the chat.
- **Claude (Chat), ChatGPT:** there is no folder on your computer the chat can reach. Give the opening chat your workspace the way you did in earlier steps — connect your registry repo through the GitHub connector, or upload the bundle folder — and when the round ends, **save `test-results.md` back into your workspace yourself**. The skill will remind you.

**The run chat needs the installed skill and the workflow's context files, and nothing else.** It must *not* have seen your Requirements, Design Spec, or results before the run starts; that's what keeps the test honest.

- **Shared-folder platforms:** open the new chat in the same workspace folder. The built skill is installed there, and that's how the run chat can also reach the results file to grade into. Just don't open or discuss the requirements or design in that chat before you run.
- **Claude (Chat), ChatGPT:** open the new chat inside the Project that holds the workflow's context files (see the caution below about what that Project may contain).

**Then find your path.** The one thing that changes how you grade is whether a new chat on your platform can see the files your opening chat wrote. The walkthrough below uses these two labels:

| Your path | Platforms | How you grade each run |
|---|---|---|
| **Shared folder** | Claude Code, Cowork, Codex, Gemini CLI | Say *test this* in the run chat. The skill grades right there. |
| **Separate chats** | Claude (Chat), ChatGPT, Gemini Spark, Gemini Enterprise, M365 Copilot | Copy one message from the run chat into the opening chat, then say *test this* there. Step 10 shows exactly how. |

Both paths produce the same report card in the same results file. The skill works out which path applies by itself; you never have to tell it.

:::caution[If your workflow lives in a Project]
On Claude (Chat) and ChatGPT, your workflow's context files live in a Project, and you open each run chat inside that Project. Keep your **Requirements, Design Spec, and test results out of that Project's knowledge**. If they're in there, every new chat has already seen your design, and the skill will refuse to grade the run as a fair test.
:::

## Do This

### Part 1 — Open the round (in your opening chat)

1. Open a chat that can reach your workspace — the folder holding `registry/` and `outputs/` (see [Where You Run From](#where-you-run-from) for your platform).
2. Say **"run the test skill"** (Claude Code also accepts `/handsonai:test`).
3. The skill reads your Requirements and Design, then shows you the **check list** and the **passing rule**: every line Met on every input; a miss on a **(must)** line always fails; any other miss is either fixed or explicitly accepted. It asks whether to add or drop any line. Answer, and it writes the round's results file.
4. The skill reads your built skill against the Requirements to catch obvious gaps (a missing gate, a reference file it never mentions), confirms it ends each run with a "What I did" summary, and notes whether it has a test-run mode. If something's missing, it tells you now, before you spend a run.
5. If your workflow uses connectors (HubSpot, Gmail, a spreadsheet), the skill confirms each one has the access it needs. If one is blocked, the round still runs — that step is marked "not run", never faked.
6. The skill hands you **the first input, pasted in full**, plus a one-line instruction for starting the workflow in a new chat on your platform. Copy the input.

### Part 2 — Run one input (in a new run chat)

7. Open a **brand-new chat**. If your workflow lives in a Project or folder with context files, open the new chat inside it. Do not reuse the opening chat, and do not bring your Requirements or Design in with you.
8. Start the workflow the way an operator would — ask for the skill by name, using the instruction the skill gave you in step 6. If your workflow has a test-run mode (the skill will have told you in step 4), start it that way so the run doesn't write to your real run log.
9. Paste the input. Work through the run exactly as you would in real use: when the workflow pauses at a gate, decide. Let it finish. It should end with its "What I did" summary.

### Part 3 — Grade that run

10. **Shared folder path** (Claude Code, Cowork, Codex, Gemini CLI): in the run chat, say **"test this"**. Skip to step 11.

    **Separate chats path** (Claude Chat, ChatGPT, Gemini, Copilot): the opening chat can't see the run chat, so you carry one message across. Do this:

    1. In the run chat, say: **"Put your final output and your What I did summary together in one message."**
    2. Click the **copy** icon on that message. (The "What I did" summary already records every place the workflow paused and what you decided, so this one message is all the grader needs.)
    3. Go back to the **opening chat**, paste the message, and on the next line type **"test this"**. Send it.
    4. The skill asks one question first: *did that chat see your Requirements, Design Spec, or the skill's source files before the run started?* The installed skill itself doesn't count; it has to be there. Answer honestly. If it did, you'll be handed the same input to run again in a clean chat.

11. The skill tells you which input it thinks this was (E1, E2…), then presents the **report card**: one row per check-list line, Met or Not met, with evidence — a count, a quoted phrase, a missing element. Never "looks fine".
12. **You confirm or override each row.** The skill grades first; you are the judge. If you disagree with a row, say so and why.
13. Answer one closing question: *how much would you have to edit this before using it — nothing, a little, or a lot?* This is separate from the report card. A line is Met or Not met on evidence; this answer records your overall effort, and the two can disagree.
14. The skill saves the confirmed card and tells you what's left: *"1 of 3 graded — run E2 in a new chat next."* It hands you the next input, pasted in full.

### Part 4 — Repeat, then get the verdict

15. Go back to **step 7** for each remaining input. One input per run chat, every time. Don't fix anything between inputs — note it and keep going.
16. After the last input is graded, in whichever chat graded it, the skill diagnoses every miss (which building block caused it), gives the **verdict**, and lists any test records to clean up:
    - **Ready** — every line met on every input, or a miss you looked at and accepted for a recorded reason. Move to [Run (Step 6)](../run/).
    - **Not ready** — at least one miss you haven't accepted. Go back to [Build](../build/), which regenerates only the building blocks the results name, then come back here and open a new round. Re-run the inputs that failed, then the full set.
    - **Waiting on access** — the logic passed but a connector's write access isn't authorized yet. Fix the access. No rebuild needed.

:::tip[Pacing a first round]
A first round with three inputs is realistically 45–60 minutes. If you're short on time, open the round and run E1 end to end, then do the remaining inputs later. The skill remembers where you are: say *"continue my workflow"* in your workspace and it will tell you which input is next.
:::

## Six Rules for Judging Your Workflow

1. **Judge it against what you wrote in Deconstruct**, not against how the output feels.
2. **Use real inputs**, including one hard case.
3. **Run each input in a new chat that has never seen your requirements or design.** A run inside the conversation that built it sees everything you said while building and looks better than it will in real use.
4. **Every criterion is met or it isn't.** One miss is a miss.
5. **The AI grades first, with evidence. You make the call.**
6. **Test, fix, test again.** Two to four rounds is normal. Don't fix mid-test.

## The Report Card

For each input you run, the skill produces one table. Every row is something you said the workflow must do, tagged with where it came from. The rows that judge the **output** come first, then the rows that judge the **path the run took**:

| Expected | From | Result | Evidence |
|---|---|---|---|
| Every prospect row has contact info | AC1 (must) | Met | 20 of 20 rows |
| Never includes previously contacted people | R3 | Not met | 2 rows already in the CRM export |
| Pauses before sending | G1 | Met | What I did: "paused for your approval before sending — you approved 18 of 20" |
| Step 2 output: ranked list | Step 2 output | Met | 20 rows, ranked best-fit first |

`AC` rows are your acceptance criteria, `R` rows your rules, `G` rows your human gates, and each step's stated output gets a row too. The **Evidence** column is what makes the grade trustworthy.

Rows about what the output contains are proved from the output itself. Rows about what the workflow did along the way are proved from the **"What I did"** summary at the end of the run. A line that neither that summary nor the conversation shows is marked "not run", with the reason, instead of being guessed at.

Three cases are graded the same way every time, so you know what to expect:

- **A gate that never had a reason to fire** on this input (an "ambiguous status" gate on a week with no ambiguous statuses) is Met when the summary says it didn't fire and why. If no input in the whole round triggers it, the verdict says that line is untested and suggests an input for next round.
- **A behaviour your test-run mode deliberately swaps** (no run-log row, output printed for you to save instead of written to a file) is graded on the swap. It is not a miss.
- **Two or more lines that say the same thing** (a rule that restates a criterion) all go Not met when one defect breaks them, and the fix is listed once.

**Golden examples.** Where you supplied a real past output that was exactly right, the skill compares the new output against it — output only, never the path: what's missing, what's extra, what's different in substance. A golden example is one good answer, not the only one; the question is "would you send this instead?" Keep at least one input without a golden example, so you learn whether the workflow generalizes.

**The edits question.** Your answer to "nothing, a little, or a lot" is recorded with each input. Its trend over time is the earliest sign of drift when you come back in [Improve](../improve/).

## Diagnose and Fix

| What went wrong | What to change |
|---|---|
| Output is generic or off-brand | Add **context** — examples, style guide, reference material |
| A step was skipped or misunderstood | The **orchestrator skill** — make that step's instruction explicit |
| A step needs expertise the AI doesn't have | A **component skill** — build or extend one for that step |
| Output format is wrong | The **orchestrator skill** — add an explicit format example |
| The AI ignored a reference file | **Context** — check the file is where the skill expects it and is readable |
| A tool call failed | The **connector** — verify it independently, then re-run |
| The output looks right but the path was wrong (a gate skipped, a rule broken on the way) | The **orchestrator skill** — make the gate or rule explicit; **Design** if no rule covers it |
| The AI had to make decisions your rules didn't cover | **Design** — the workflow may need an agent, or clearer rules |

Every miss names its building block, so Build knows exactly what to regenerate. After a fix, re-run the failed inputs, then the full set — a fix in one place can affect another.

:::note[Two to four rounds is normal]
If you've been through four rounds and the same lines keep failing, the problem is usually the design, not the build. Go back to [Design (Step 3)](../design/).
:::

## What This Produces

`outputs/[workflow-name]/test-results.md` — the check list, the report card per input, the diagnosis table, accepted misses, the verdict as a count ("11 of 12 lines met across 2 inputs"), and machine-readable frontmatter so [Improve](../improve/) can later show you exactly which lines changed. Earlier rounds are kept alongside it with a date suffix.

## How the Skill Works

This is what the `test` skill is doing under the hood, phase by phase. You don't need to drive these; the walkthrough above is the student's view of the same sequence.

1. **Load context** — the requirements (criteria, rules, gates, inputs), the design spec, and where the built skill lives.
2. **Confirm the passing rule** — every line of the report card Met on every input; a miss on a **(must)** line always fails; any other miss is fixed or explicitly accepted. The results file is written at the end of this step, so a line you add or drop here is in it from the start.
3. **Smoke run** — the skill reads the built workflow against the requirements to catch obvious gaps before you spend a run.
4. **Integration pre-flight** — confirms each connector has the access it needs in the account that will run the workflow; a blocked write path is marked "not run", never faked. If your workflow connects to nothing, the skill says so in one line and moves on.
5. **Run and grade each scenario** — you run each input in a new chat; the skill grades that whole run (in the run chat, or from the run pasted back into the opening chat), fills in the report card with evidence, and you confirm or override each line. Every line is graded on every input.
6. **Diagnose every miss** — each Not met line is mapped to the building block that caused it, including a right-looking output that took a wrong path.
7. **Verdict** — Ready, Not ready (back to Build, which regenerates only what's named), or Waiting on access.
8. **Clean up test records** — anything the test created in a live system is listed and offered for removal.

## How to Use This

This step is facilitated by the **`test`** AI Workflow Framework skill. See [Install the Hands-on AI Plugin](../skills/) for installation instructions across all supported platforms.

**How to start:** Say *"run the test skill"* — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:test`, and Cowork lists it when you type `/`. Then, after each run, say *test this* in the chat that holds the run — the run chat, or the opening chat once you've pasted the run into it.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
Run the test skill on my workflow.
```

## Related

- [Deconstruct Workflows](../deconstruct/) — where the criteria, rules, gates, and inputs are captured
- [Build](../build/) — where misses get fixed
- [Run](../run/) — the next step once every line is met
- [Improve](../improve/) — where the same report card is re-run to catch drift
