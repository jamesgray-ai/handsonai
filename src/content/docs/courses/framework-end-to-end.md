---
title: Run the Framework End-to-End
description: Run the AI Workflow Framework end-to-end on a Competitive Intelligence workflow, from your requirements to a tested, live skill and agent in your workspace.
---

In this exercise you run the AI Workflow Framework end-to-end yourself, live in class. Starting from the Workflow Requirements you write with Deconstruct, you take a **Competitive Intelligence** workflow through Design, Build and Test, then take it live and run it on a real competitor. You finish with a `competitor-research` skill and a `competitor-brief` agent that produce a structured brief.

## Lesson: Ship a Workflow Using the AI Workflow Framework

Run the framework yourself with the Hands-on AI plugin installed, in Claude Code or Claude. Each step runs in a new chat (a new session on Claude Code). You don't need to remember which step comes next: say **"continue my workflow"**, with where your files are, and the framework picks up where your workflow is. Every step ends by giving you the phrase that starts the next one. In Claude Code you can also use the slash commands (`/handsonai:design`, `/handsonai:build`, `/handsonai:test`).

### Hands-on assignment

**Starting point:** your Workflow Requirements, written with Deconstruct (below).
**Ending point:** a tested, live skill and agent producing a brief on a real competitor.

1. **Design** — Turn your requirements into an approved Design Plan. Design drafts the whole plan, asks you only what it couldn't settle, and ends in a task list. See [Design](../../ai-workflow-framework/design/).
2. **Build** — Build the `competitor-research` skill and `competitor-brief` agent task by task from your plan, with each task checked. Build writes a build record of what was built and what it can access. See [Build](../../ai-workflow-framework/build/).
3. **Test** — Run practice runs on realistic inputs, including one real example the workflow hasn't seen. Practice runs never send or change anything. Test grades what the workflow produced against your requirements and gives its verdict. See [Test](../../ai-workflow-framework/test/).
4. **Take it live** — When Test says it's ready and asks "Take it live?", say yes. Then do the first real run yourself, on a real competitor, and watch `knowledge/competitors/{name}.md` emerge.

### Write the Workflow Requirements first

Run [Deconstruct](../../ai-workflow-framework/deconstruct/) on the Competitive Intelligence workflow before class. It writes `requirements.md` in the workflow's folder, which is where the rest of the framework starts.

### Set up your workspace before class

Do these steps in the folder you have open in the Claude desktop app or Claude Code.

**Step 1 — get a `registry/` folder.** Open the folder you'll work in (any folder — it doesn't need to be a GitHub repository) in your AI assistant and say *"Set up my AI registry."* It creates the `registry/` folder for you. If you'd like GitHub to check your registry automatically, start from the [AI Registry template repository](https://github.com/jamesgray-ai/ai-registry-template) instead — the [AI Registry setup guide](/builder-setup/ai-registry-setup/) walks through both.

**Step 2 — write the requirements.** In a new chat, say *"run the deconstruct skill on the Competitive Intelligence workflow."* It creates `framework/competitive-intelligence-brief/` in your workspace, saves `requirements.md` there, and adds the workflow to your registry as a Workflow node (`registry/workflows/competitive-intelligence-brief.md`, with `status: under-development`).

**Step 3 — check the node.** Open `registry/workflows/competitive-intelligence-brief.md` and confirm its `# Artifacts` list links your requirements. That node is the small file every framework step reads first. When class starts, say *"continue my workflow"* in a new chat and Design picks up right where your requirements leave off.

### What you'll walk away with

- A `competitor-research` skill and a `competitor-brief` agent installed in your workspace, tested and live
- A populated `knowledge/competitors/{name}.md` file on a real competitor
- First-hand reps on Deconstruct, Design, Build and Test, moved along with "continue my workflow"

## Keeping It Working

Once it's live, the workflow carries its own upkeep. Each run flags anything it wasn't designed for, with the phrase to fix it: "change my workflow". To re-check it later, say "test the workflow I built". See [Test](../../ai-workflow-framework/test/).
