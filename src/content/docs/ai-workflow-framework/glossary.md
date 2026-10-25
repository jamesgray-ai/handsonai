---
title: Framework Glossary
description: "Every term you meet in the five-step AI Workflow Framework, in plain language: practice runs, checkpoints, tracks, the Design Plan, re-checks and more."
---

Every term you'll meet across the five steps, in plain language, each linked to the page that introduces it.

**Agent (how it runs)** — A workflow that decides its own path while it runs, uses tools on its own judgment, and can run without you. [Design](../design/) chooses an agent when the steps depend on what the workflow finds along the way. On Microsoft 365 Copilot, agents are made in Agent Builder.

**Agent (building block)** — A configured worker with a job, tools and limits, which a person or another part of the workflow hands work to. See [Agentic Building Blocks](../../agentic-building-blocks/).

**Augmented / Automated** — Who takes part while a workflow runs. **Augmented**: a person is in the workflow along the way, guiding or working with the AI. **Automated**: no one takes part until it's done; starting a run by hand doesn't make it Augmented. Set in [Design](../design/); see the [AI Workflow Design Matrix](../workflow-design-matrix/).

**Autonomy** — How much the AI decides on its own, judged by what decides the next step. **Deterministic**: you give instructions and the AI carries out every step you set. **Guided**: you give bounded decisions with your method (a rubric, criteria, a process), and the AI decides by it. **Autonomous**: you give a goal, and the AI plans its own steps until the goal is met. [Design](../design/) names the level once, in its plan review. See the [AI Workflow Design Matrix](../workflow-design-matrix/).

**Backlog** — The list of candidate workflows [Analyze](../analyze/) saves, each with the work, the pain and the value: cards in your registry, or `backlog.md` in your Framework folder without one.

**Build record** — The file [Build](../build/) writes (`build-record.md`): what was built, where it's installed, and what it can access. Once the workflow is live, it also says how to switch it off.

**Building blocks** — The pieces a workflow is built from, in four layers: Intelligence (Model, Context, Memory, Project), Orchestration (Prompt, Skill, Agent, Harness), Integration (MCP, API, SDK, CLI) and Governance (Registry, Observability, Evaluation). See [Agentic Building Blocks](../../agentic-building-blocks/).

**"Change my workflow"** — The phrase that starts any change to a workflow that's planned, built or live. [Design](../design/) picks it up and judges whether the change is small or big; every change starts at the requirements. See [Keeping It Working](../#keeping-it-working).

**Change that can't be undone** — Anything a workflow does that can't simply be taken back: sending an email, posting a message, deleting or overwriting a record. Design puts a checkpoint before it, and a practice run never makes one.

**Checkpoint** — A point where the workflow stops and asks a person first, such as before it sends anything. One of the [three kinds of line](../#how-it-fits-together) in your requirements, captured in [Deconstruct](../deconstruct/).

**Connection** — How a workflow reaches a system such as a CRM, a calendar or a drive. Your platform may call it a connector or an app. [Build](../build/) has you connect each one in your own account and proves it works.

**Context** — The documents, examples and reference material a workflow reads while it runs, such as a style guide or a template. Captured in [Deconstruct](../deconstruct/), kept in the workflow's `context/` folder, and placed where the workflow runs by [Build](../build/).

**"Continue my workflow"** — The phrase that moves a workflow on from wherever it is. Say it in a new chat; any of the five skills reads your files, works out which step is next, and picks up there. See [Moving From Step to Step](../#moving-from-step-to-step).

**Design Plan** — The plan [Design](../design/) writes (`design-plan.md`) for how AI will do the work: where it runs, how much it decides on its own, which parts are skills or agents, what it connects to, and the task list Build follows. You approve it before anything is built.

**Flag line** — The line at the end of every run that flags anything the workflow wasn't designed for, such as a new kind of input or a checkpoint it had to guess at, with the phrase to fix it: "change my workflow". Part of [keeping it working](../#keeping-it-working).

**Framework folder** — The folder that holds your workflow files, called Framework: in Google Drive, in OneDrive or on your computer, or `framework/` in your workspace on Claude Code and Codex. Each workflow gets its own folder inside it. It's kept apart from the workflow's place.

**Keeping it working** — What every workflow carries so it stays useful once it's live: the flag line, a re-check date, and "change my workflow". It's part of every workflow, not a step. See [Keeping It Working](../#keeping-it-working).

**Lens** — What an [Analyze](../analyze/) session looks at: **Individual** (your own work) or **Organizational** (your business's processes, across several roles).

**Live** — A workflow you've taken live at the end of [Test](../test/) and now use for real work. Live is a fact about the workflow, not a step: a live workflow keeps running while it's changed or re-checked.

**Must-have** — A check the output can't pass without. Marked among what every output must get right in [Deconstruct](../deconstruct/); a miss on a must-have is never accepted.

**Practice inputs** — Realistic examples, taken from your real work, that [Test](../test/) runs the workflow on. Captured in [Deconstruct](../deconstruct/) and saved in the workflow's `inputs/` folder. Each round also includes one real example the workflow hasn't seen.

**Practice run** — A run of the workflow that sends and changes nothing. It goes up to each change, shows exactly what it would send or change and where, and stops there. Every workflow [Build](../build/) makes has one, and every run in [Test](../test/) is one.

**Quick real check** — One small real change, made during [Build](../build/)'s setup somewhere only you can see, with your OK first, that proves a kind of change works.

**Re-check** — Running [Test](../test/) again on a live workflow with "test the workflow I built", to see whether it still does what it must. Test sets a date for it when the workflow goes live, three months out.

**Registry** — Your AI Registry: a folder of Markdown cards describing your business, its processes and its workflows, which every framework step reads and updates so you never describe your work twice. See the [AI Registry Setup guide](../../builder-setup/ai-registry-setup/).

**Round** — One pass of [Test](../test/): every practice input and your real example run once, each requirement checked with proof, then a verdict of Ready, Not ready, or waiting on a connection's access. On the full track, two or three rounds is normal.

**Rules it follows** — Sentences in your requirements that say how the workflow must behave: "It always…", "It never…", "When…, it…". One of the [three kinds of line](../#how-it-fits-together), captured in [Deconstruct](../deconstruct/).

**Run log** — A one-line-per-run record the workflow keeps in its own place, where the platform lets it write one. Re-check reminders and time saved come from it. Not every workflow keeps one; those that don't still end each run with the flag line.

**Skill (how it runs)** — A workflow you start by name that follows the same steps each time, pausing where you said. [Design](../design/) chooses a skill when you trigger the work yourself and the steps repeat.

**Skill (building block)** — Any reusable set of instructions the AI follows, including smaller skills a workflow uses for one part of the job. See [Agentic Building Blocks](../../agentic-building-blocks/).

**`stale_after`** — The re-check date on a workflow's registry card. [Test](../test/) sets it when the workflow goes live, three months out, and resets it after each Ready re-check.

**Track (light, full)** — How thorough the five steps are for a workflow. **Light** is for small, low-risk workflows; **full** is for the rest. Same steps and files; each step is shorter on the light track. Any sign of risk keeps a workflow on the full track. Proposed in [Deconstruct](../deconstruct/).

**Tricky case** — An input that's harder than usual: missing information, an unusual request, something that tests a rule. Your practice inputs should include at least one.

**What it must get right** — Yes-or-no checks in your requirements that every output must pass. One of the [three kinds of line](../#how-it-fits-together), captured in [Deconstruct](../deconstruct/) and checked in every [Test](../test/) round.

**"What I did" summary** — The short summary a workflow ends each run with: the steps it took, where it paused for you, and what it did with your tools. [Test](../test/) uses it to check the path, but always grades the output itself, never the summary's claims about it.

**Workflow's place** — Where the workflow runs: its own Project or folder; on Microsoft 365 Copilot, Copilot Cowork's own folder or the agent itself. It holds only what the workflow reads while it runs, never your requirements or plan, so Test's runs stay cold.

**Workflow node** — A workflow's card in your registry (`registry/workflows/<slug>.md`), tracking its status and files across every step. First written by [Analyze](../analyze/).

**Workflow Requirements** — The clear, testable description of what a workflow must do (`requirements.md`): its goal, what every output must get right, the rules it follows, where a person checks, and its practice inputs. Written in [Deconstruct](../deconstruct/) and read by every later step.
