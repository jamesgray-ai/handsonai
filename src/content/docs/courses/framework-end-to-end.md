---
title: Run the Framework End-to-End
description: Run the AI Workflow Framework end-to-end on a Competitive Intelligence workflow, from your requirements to a tested, live workflow in your workspace.
---

In this exercise you run the AI Workflow Framework end-to-end yourself, live in class. Starting from the Workflow Requirements you write with Deconstruct, you take a **Competitive Intelligence** workflow through Design, Build and Test, then take it live and run it on a real competitor. You finish with the workflow Design plans for it, built and installed in your workspace: often one skill named for the workflow, plus an agent only where the plan needs one. It produces a structured brief.

## Lesson: Ship a Workflow Using the AI Workflow Framework

Run the framework yourself with the Hands-on AI plugin installed, in Claude Code (or the Claude desktop app). Each step runs in a new chat (a new session on Claude Code). You don't need to remember which step comes next: say **"continue my workflow"**, with where your files are, and the skill works out which step is next. If it's that skill's step, it picks up there; if not, it gives you the phrase to start the right step in a new chat. Every step ends by giving you the phrase that starts the next one. In Claude Code you can also use the slash commands (`/handsonai:design`, `/handsonai:build`, `/handsonai:test`).

### Hands-on assignment

**Starting point:** your Workflow Requirements, written with Deconstruct (below).
**Ending point:** a tested, live workflow producing a brief on a real competitor.

1. **Design** — Turn your requirements into an approved Design Plan. Design drafts the whole plan, asks you only what it couldn't settle, and ends in a task list. See [Design](../../ai-workflow-framework/design/).
2. **Build** — Build the parts your plan lists, task by task, with each task checked. Build writes a build record of what was built and what it can access. See [Build](../../ai-workflow-framework/build/).
3. **Test** — Run practice runs on realistic inputs, plus one new input the workflow hasn't seen. Practice runs show each change instead of making it. Test grades what the workflow produced against your requirements and gives its verdict. See [Test](../../ai-workflow-framework/test/).
4. **Take it live** — When Test says it's ready and asks "Take it live?", say yes. Then do the first real run yourself, on a real competitor, and check the brief it produces, where your requirements say it goes (for example `knowledge/competitors/{name}.md`).

### Write the Workflow Requirements first

Run [Deconstruct](../../ai-workflow-framework/deconstruct/) on the Competitive Intelligence workflow before class. It writes `requirements.md` in the workflow's folder, which is where the rest of the framework starts.

### Set up your workspace before class

Do these steps in the folder you have open in the Claude desktop app or Claude Code.

**Step 1 — get a `registry/` folder.** Open the folder you'll work in (any folder — it doesn't need to be a GitHub repository) in your AI assistant and say *"Set up my AI registry."* It creates the `registry/` folder for you. If you'd like GitHub to check your registry automatically, start from the [AI Registry template repository](https://github.com/jamesgray-ai/ai-registry-template) instead — the [AI Registry setup guide](/builder-setup/ai-registry-setup/) walks through both.

**Step 2 — write the requirements.** In a new chat, say *"run the deconstruct skill on the Competitive Intelligence workflow."* It creates a folder for the workflow named after the name you choose (for example `framework/competitive-intelligence-brief/` on Claude Code), saves `requirements.md` there, and adds the workflow to your registry as a Workflow node (for example `registry/workflows/competitive-intelligence-brief.md`, with `status: under-development`).

**Step 3 — check the node.** Open the workflow's file in `registry/workflows/` and confirm its `# Artifacts` list links your requirements. That node is the small file every framework step reads first. When class starts, say *"run the design skill. My files are in framework/[your workflow's folder]."* (or *"continue my workflow"*) in a new session.

### What you'll walk away with

- Your Competitive Intelligence workflow installed in your workspace, tested and live
- A brief on a real competitor, saved where your requirements say it goes
- First-hand reps on Deconstruct, Design, Build and Test, moved along with "continue my workflow"

## Keeping It Working

Once it's live, the workflow carries its own upkeep. Each run flags anything it wasn't designed for, with the phrase to fix it: "change my workflow". To re-check it later, say "test the workflow I built". See [Test](../../ai-workflow-framework/test/).
