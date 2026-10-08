---
title: "Step 6: Run"
description: "Step 6: Run — do the first real run on real work in a new chat, then leave a one-page Run Card, a run log, and a review date behind for whoever runs it next."
---

> **Part of:** [AI Workflow Framework](../)

## Where You Are

You've just finished [Test (Step 5)](../test/). Your last test round ended with the verdict **Ready**: every line of the report card met on every input, or a miss you looked at and accepted. That round's report card is now your **baseline**, the one [Improve (Step 7)](../improve/) compares against later. Your workflow's skill is installed in the account that will run it, and your Workflow node says `under-development`.

Every run so far used test inputs, usually in a test-run mode that wrote nothing real. Run is where the workflow does this week's actual work, for the first time, with you watching.

| | |
|---|---|
| **What you'll do** | Run the workflow on real work in a new chat, started the way you'll start it every time; then confirm the run and agree a review date |
| **What you'll get** | A one-page **Run Card**, a run log with its first row, and a review date on your Workflow node |
| **Time** | 15–20 minutes of framework work, plus one real run of your workflow (however long that normally takes), plus about 15 minutes if it will run on a schedule |

## The Words You'll Hear

| Word | What it means |
|---|---|
| **Opening chat** | The chat where you start the `run` skill. It reads your test results and Design Spec, hands you the start instruction, and writes the Run Card, the run log, and your Workflow node. |
| **Run chat** | A brand-new chat where you run the workflow on real work, exactly as you will every time from now on. |
| **"Log this run"** | What you say once the real run has finished. The skill checks the run against your criteria, writes the Run Card, logs the run, and marks the workflow live. From then on, saying it after any run adds a row to the log. |
| **Run Card** | The one page the skill writes after the first real run: how to start the workflow, what to have ready, what to check before you act on its output, how to log a run, and when your first review is. Saved as `run-guide.md`. |
| **Run log** | A table with one row per run (`runs.md`): date, input, result, edits needed, notes. Improve reads it as evidence instead of asking you to remember. |
| **Human gate** | A place where the workflow pauses and waits for your decision. Deconstruct numbered them G1, G2… |
| **(must) line** | An acceptance criterion marked *must* in Deconstruct. A miss on one is never acceptable. |
| **Connector** | A tool the workflow reaches into: HubSpot, Gmail, a spreadsheet. Each one is authorized per account, so a connector that worked in one chat can be missing in another person's. |
| **Review date** | The date your first Improve review is due, recorded on your Workflow node as `stale_after`. One month out for a workflow you run weekly or more, three months for one you run less often, moved back to the nearest day the workflow runs. |
| **Augmented / Automated** | How your workflow was designed to run, from the Design Spec. Augmented: you start it and take part at its gates. Automated: it runs without you, on a schedule or a trigger. Only an Automated workflow gets a schedule in this step. |

## Before You Start

Confirm these four things. Each takes a minute.

1. **The verdict was Ready.** Open `outputs/[workflow-name]/test-results.md`. The lines at the top should say `round_status: complete` and `readiness: ready`. If they say anything else, the skill will send you back: an unfinished round goes to Test, a not-ready verdict to Build's fix mode, and a waiting-on-access verdict to Build to authorize the connector it names.
2. **The skill is installed where the workflow will run.** Open a new chat in the account that will run it and ask for your workflow's skill by name. If it responds as your workflow, you're set. If it doesn't, go back to [Build](../build/) and finish the install step. If you changed any of its files after installing, reinstall first; the installed copy doesn't update itself. The skill asks you one question about this, naming the skills and the connectors together.
3. **You have this week's real input, or the workflow pulls it.** Your Requirements' Step 1 says which. If it pulls from a connector, that connector must be authorized in the account that will run it. If you've moved the workflow to a different platform since Design, say so when asked: it has to have been tested on the platform it runs on, or the skill sends you to Build to regenerate it there.
4. **You know what this run does for real.** This is not a test run. Once you approve at a gate, the email sends, the row is added, the file is saved and shared. The skill lists every write before you start, with the gate that stands in front of it. Read that list, and point the workflow at the real thing only if you're ready for the result.

## Where You Run From

Two chats are involved, and each one needs different things in reach. If you went through [Test](../test/#where-you-run-from), this is the same arrangement.

**The opening chat needs your workspace.** That's the folder holding everything the framework has produced so far: `registry/` (your Workflow node), `outputs/[workflow-name]/` (requirements, design spec, test results), and the built skill. The `run` skill reads those and writes the Run Card and run log next to them.

- **Claude Code, Codex, Gemini CLI:** open the session *in that folder*. Every chat opened there shares the same files.
- **Cowork:** connect that folder as the working folder (a Project is not required), then start the chat.
- **Claude (Chat), ChatGPT:** there is no folder on your computer the chat can reach. Give the opening chat your workspace the way you did in earlier steps — connect your registry repo through the GitHub connector, or upload the bundle folder — and when the step ends, **save `run-guide.md`, `runs.md`, and your updated Workflow node back into your workspace yourself**. The skill prints each one under the path to save it at, and lists all three at the end.

**The run chat needs the installed skill and the workflow's context files, and nothing else.** It is an ordinary working chat: the one you'll open every week from now on.

- **Shared-folder platforms:** open the new chat in the same workspace folder. The built skill is installed there, and the workflow can write its output and its log row there.
- **Claude (Chat), ChatGPT:** open the new chat inside the Project that holds the workflow's context files. The workflow can't write files from there, so it ends by printing its output and its log row for you to save.

**Then find your path.** The one thing that changes how you hand the run back is whether a new chat on your platform can see the files your opening chat wrote.

| Your path | Platforms | What you do when the real run finishes |
|---|---|---|
| **Shared folder** | Claude Code, Cowork, Codex, Gemini CLI | Say *log this run* in the run chat. The skill checks the run and finishes the step right there. |
| **Separate chats** | Claude (Chat), ChatGPT, Gemini Spark, Gemini Enterprise, M365 Copilot | Copy one message from the run chat into the opening chat, then say *log this run* there. Step 9 shows exactly how. |

Both paths produce the same Run Card and the same log. The skill works out which path applies by itself; you never have to tell it.

## Do This

### Part 1 — Get ready (in your opening chat)

1. Open a chat that can reach your workspace — the folder holding `registry/` and `outputs/` (see [Where You Run From](#where-you-run-from) for your platform).
2. Say **"run the run skill"** (Claude Code also accepts `/handsonai:run`).
3. The skill reads your test results and confirms the verdict was **Ready**. If it wasn't, it tells you which step to go back to and stops.
4. The skill lists **everything this run will do for real** — each file it saves, draft it creates, row it adds, message it sends — and the gate in front of each. Read the list. This is the moment to decide whether to point it at the real record or wait.
5. The skill hands you three things: **where to open the new chat**, the **exact phrase** that starts the workflow (not as a test run), and **what to give it** — this week's real input, or nothing if the workflow pulls its own. On the separate-chats path it also tells you how to carry the run back (step 9).

### Part 2 — The first real run (in a new run chat)

6. Open a **brand-new chat** where the skill said: the same workspace folder, or inside the Project that holds the workflow's context files.
7. Start the workflow with the phrase from step 5 and give it the real input. Work through the run as you will every time: when it pauses at a gate, decide. Approve only what you'd send. Let it finish; it should end with its "What I did" summary.
8. Use the output. It's real work: send the report, file the draft, share the document, as the workflow was designed to.

### Part 3 — Log this run

9. **Shared folder path** (Claude Code, Cowork, Codex, Gemini CLI): in the run chat, say **"log this run"**. Skip to step 10.

    **Separate chats path** (Claude Chat, ChatGPT, Gemini, Copilot): the opening chat can't see the run chat, so you carry one message across. Do this:

    1. In the run chat, say: **"Put your final output and your What I did summary together in one message."**
    2. Click the **copy** icon on that message. (The "What I did" summary records every place the workflow paused and what you decided, so this one message is all the skill needs.)
    3. Go back to the **opening chat**, paste the message, and on the next line type **"log this run"**. Send it.

10. The skill checks the run against your check list and shows you a short table with evidence: every gate paused and what you decided, every **(must)** line met, the output where the Design Spec said it would land, each connector reached in this account, and (on shared-folder platforms) today's row already in the run log. You confirm or override each line.
11. Answer one question: *how much did you edit the output before using it — nothing, a little, or a lot?* That answer becomes the "Edits needed" cell of today's log row. If your Requirements named a Measure one run can read (minutes start to finish, items processed), the skill asks for this run's number in the same breath; it goes in the "Notes" cell.
12. If anything failed, the skill says which of two things it was. **The environment** (a connector not authorized in this account, a context file in the wrong place): fix that, run the same input again in a new chat, say *log this run* again. **The workflow itself** (a gate that didn't pause, a must line missed): the workflow doesn't go live today. The skill sends you to Test to open a round on this input, so Build can fix what it finds.

### Part 4 — Go live

13. The skill writes your **Run Card** and shows it to you. Read the "How to start it" section once as if you were a teammate; if it wouldn't get you to a running workflow, say so now.
14. The skill writes the run log with today's row (or checks the row the workflow wrote itself), proposes your **review date** as a date, and marks your Workflow node in production. Put the date in your calendar now, with the event title *"Run the improve skill on [workflow name]"*.
15. On the separate-chats path, save the three files the skill prints — `run-guide.md`, `runs.md`, and the Workflow node — into your workspace.

### Part 5 — Put it on a schedule (Automated workflows only)

16. If your Design Spec said **Automated**, the skill now sets up the schedule on your platform, checks that the context files the schedule needs are reachable from it, and takes you through a five-question safety checklist, each answered from the installed workflow. Five yeses and it enables the schedule. The first scheduled run is the first run nobody watches: open the run log after it fires and check that row two is there.

    If your workflow is **Augmented**, there is no step 16. The Run Card says "This runs when you start it"; if you later want a schedule, that's a design change, and the route is [Design](../design/), not this step.

:::tip[Pacing]
If your workflow takes a while to run (a long report, a batch of records), do Part 1 now and Parts 2 to 4 when the real work comes round — Friday morning for a Friday report. The skill remembers where you are: say *"continue my workflow"* in your workspace and it will tell you what's next.
:::

## Your Run Card

The Run Card is one page with six fixed sections, in this order. It is written after the first real run, not before, so it describes what actually happened rather than what should:

1. **Your first real run** — what happened today, in two sentences, and what to expect next time. If you accepted a miss on a non-must line, the reason is recorded here.
2. **How to start it** — the exact phrase or click that starts the workflow, and the input to give it. If teammates will run it too: how they install the same package in their account, which connectors they need authorized, and the same phrase.
3. **What to have ready** — the inputs in hand; the skills and agents installed in the account that runs it; every connector that must be authorized **in that same account**; every context file, with its location. A fresh chat inherits nothing from the session that built the workflow, and a scheduled run inherits less; this list is what a clean chat needs to succeed.
4. **What to check before you act on the output** — the human gates in plain words (what the workflow pauses for and what you're deciding), your **(must)** lines, and at most two other lines worth a glance. It's meant to be read in the minute before you act, not studied.
5. **Log the run** — one line in `outputs/[name]/runs.md`: date, input, result, edits needed, notes, and whether the workflow writes that row itself or prints it for you.
6. **Your first review** — the date, why it's that date ("monthly, for a weekly workflow"), and the exact sentence that re-enters the framework: *"Run the improve skill on [workflow name]."*

The Run Card is shown in the conversation and saved to `outputs/[name]/run-guide.md`, so you can reopen it weeks later or hand it to someone else.

### Keep a run log

`outputs/[name]/runs.md` is a table with one row per run: date, input or trigger, result, edits needed, notes. It takes ten seconds, and when you review the workflow in [Improve (Step 7)](../improve/) it's the difference between "I think it's been fine?" and evidence of drift, recurring edits, or failures.

On shared-folder platforms, Build wrote the logging step into your workflow's skill, so it adds its own row at the end of every real run; the first real run is where the `run` skill checks that it did. On Claude Chat and ChatGPT, where a chat can't write to your workspace, the workflow prints its row and you add it to the file.

If your Requirements named a Measure that one run can read (minutes door to door, items processed), the notes cell is where it goes, and that's how an `Unknown` baseline becomes a number.

## If Your Team Will Run It

For a workflow only you run, the Run Card is the whole hand-over. For one that serves a team or a department, a few more things keep it running after the first week.

- **Share the Run Card**, and record a five-minute screen capture of one full run. People copy what they see more readily than what they read.
- **Name a workflow owner** — someone who can troubleshoot a failed run, show a new person how to start it, and decide when it needs the Improve step.
- **Decide who can change it.** The skill, its context files, and its connectors. Well-meaning edits by whoever ran it last are the fastest way to quietly degrade quality.
- **Decide where outputs live** and who can see them. Compliance, audit trails, and teammates looking for last week's report all depend on this.
- **Check adoption in the first few weeks.** If people aren't running it, find out why: usually it's hard to start, the output needs too much editing, or they don't know it exists. If they're working around it, something in the design is off.

When the step ends, the skill offers to write the workflow up as a standard operating procedure for the team. Take it up for anything more than one person will run.

## If It Runs on a Schedule

Only for workflows designed as Automated in [Design](../design/). An Augmented workflow has a person at its gates by design, and a schedule removes that person; the skill won't set one up, and will point you back to Design if you ask.

For an Automated workflow, the skill reads how your platform runs things unattended and tells you plainly if it doesn't: some platforms have no scheduler, and some can run a schedule only when the workflow's context files are in a place the schedule can reach. It then takes you through the **safety checklist** from your Design Spec, each question answered from the installed workflow, not the plan:

1. The account that owns the schedule has only the access the workflow actually uses.
2. The human gates and draft-don't-send rules are built into the installed skill, so the workflow stops or drafts where the design says, with nobody there to stop it.
3. Anything the workflow reads that you didn't write (inbound email, web pages, form submissions) is treated as data, never as instructions.
4. There's a cap on how many actions one run can take.
5. Every write shows up in the run log.

A "no" on any line means the schedule waits until Build has made the change. An unattended run does exactly what its permissions allow, with nobody watching; the checklist is the difference between a scheduled workflow and an unsupervised one.

## What This Produces

- `outputs/[name]/run-guide.md` — the Run Card, six sections.
- `outputs/[name]/runs.md` — the run log, with today's run as row one.
- Your Workflow node updated: status `in-production`, the review date as `stale_after`, and links to both files under its artifacts.

## How the Skill Works

This is what the `run` skill is doing under the hood, phase by phase. You don't need to drive these; the walkthrough above is the student's view of the same sequence.

1. **Load context** — the Workflow node, the Design Spec, the installed artifacts, and the test results. The verdict has to be Ready: an unfinished round routes to Test, not-ready to Build's fix mode, waiting-on-access to Build to authorize the connector. Then it lists every real write the run will make and hands you the start instruction.
2. **The first real run** — your real input, in a new chat, started the way an operator would start it. The skill checks the run against your check list with evidence: gates paused, must lines met, output where it belongs, connectors reached, log row present. A failure is sorted into environment (fix and re-run) or workflow (back to Test, no go-live today).
3. **Write the Run Card** — the one page you'll actually use, each section from a named source, saved to `outputs/[name]/run-guide.md`.
4. **Run log, registry, review date** — today's run as row one, the review date by rule (one month for weekly or more often, three months otherwise, one month for anything automated, moved back to the nearest run day), the node marked in production in the same session.
5. **Put it on a schedule** — Automated workflows only, after the Run Card exists: the platform's mechanism, where the context must live for it, the five-line safety checklist, and the schedule enabled only on five yeses. Skipped silently for an Augmented workflow.

## How to Use This

This step is facilitated by the **`run`** AI Workflow Framework skill. See [Install the Hands-on AI Plugin](../skills/) for installation instructions across all supported platforms.

**How to start:** Say *"run the run skill"* (or *"put my workflow into production"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:run`, and Cowork lists it when you type `/`. Then, once the real run has finished, say *log this run* in the chat that holds the run — the run chat, or the opening chat once you've pasted the run into it. After the workflow is live, saying *log this run* after any run adds a row to the log.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
Put my workflow into production — let's do the first real run.
```

### Example prompts

```
"Run the run skill on my weekly status report"
→ Confirms the Ready verdict, hands you the start instruction,
  and after you say "log this run" writes the Run Card and log

"This one needs to run every Monday without me"
→ Checks it was designed as Automated, then walks the
  scheduling setup and the safety checklist after the first run
```

## Next Step

Once your workflow is live, its Workflow node carries a review date. When that date arrives — or sooner, if the output starts needing more edits — start a new conversation and say: **"Run the `improve` skill on [workflow name]."** The node, the baseline test results, and the run log carry everything **[Step 7: Improve](../improve/)** needs; you don't have to re-explain the workflow.

## Related

- [Test](../test/) — the step before Run
- [Improve](../improve/) — the step after Run
- [Build](../build/) — where to go if the first real run reveals an environment or install problem
- [AI Workflow Design Matrix](../workflow-design-matrix/) — how autonomy and involvement combine into workflow archetypes
