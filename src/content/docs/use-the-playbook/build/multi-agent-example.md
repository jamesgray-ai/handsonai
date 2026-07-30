---
title: The Multi-Agent Example Plugin
description: A runnable worked example of multi-agent orchestration — four specialist agents, two enforcement hooks, and a human approval gate, packaged so you can install it, run it, and adapt it.
---

A **worked example, not a toolkit.** This plugin contains one complete multi-agent pipeline: four specialist agents that research, write, edit, and publish a business article, coordinated by Claude Code. The article is the excuse; the architecture is the point.

For the full teaching walkthrough — why multi-agent design works, the two ways to orchestrate, and the failures that shaped each design decision — read the [Autonomous Agent worked example](../../../ai-workflow-framework/examples/autonomous-agent/). This page is the component reference.

## Install

```
/plugin marketplace add jamesgray-ai/handsonai-plugins
/plugin install multi-agent-example@handsonai
```

**Restart Claude Code after installing.** Hooks load only when a session starts, so the gates will not exist until you do. Confirm with `/hooks`.

### Prerequisites

| Environment | What you need |
|---|---|
| **Cowork** | Nothing — the document skill is already included |
| **Claude Code** | Node.js, plus Anthropic's document skills: `/plugin install document-skills@anthropic-agent-skills` |

The `docx` npm package the renderer uses installs itself the first time you produce a document — into the plugin's own directory, never into your project. That needs network access once.

### What installing it does to your setup

This plugin ships two hooks, which merge into your Claude Code configuration and run automatically on matching events. That is a genuine change to your environment, so the scope matters: **both hooks exit immediately unless `outputs/articles/.active-run` exists in your current project.** That flag is created only when you start a pipeline run and removed when it ends. With no run in progress they do nothing, in any project.

This is also why it is a separate plugin from [Hands-on AI](../handsonai/) — installing a methodology toolkit should never silently add hooks to your environment.

## Run it

```
/hbr-article
```

Or with your own topic:

```
/hbr-article how mid-market manufacturers are using AI agents in procurement
```

Deliverables land in `outputs/articles/<slug>/` as `04-article.md` and `04-article.docx`.

For a live demonstration, paste [the goal statement](../../../ai-workflow-framework/examples/autonomous-agent/#the-goal-statement) instead of the slash command — the command is that same prompt saved, and an audience learns more from watching plain English produce four delegated agents.

Then run `/hbr-article-strict` on the same topic and compare the transcripts. Same agents, same hooks, same deliverables — but you chose the sequence instead of Claude. That contrast is the most instructive thing in the plugin.

## Agents

### ai-productivity-researcher

Finds documented case studies of organizations using AI, with quantified outcomes. Works from a tiered source hierarchy (HBR, MIT SMR, McKinsey, and analyst reports at the top), refuses unsourced claims, and flags single-source findings. In the pipeline it writes the research dossier that every later stage depends on.

Its tool list is deliberately broad — it is the only agent with web access.

### tech-executive-writer

Writes the article for a senior business audience: technical depth translated into business consequence, one clear big idea, concrete named examples. In the pipeline it drafts from the dossier and nothing else.

**It has no web access.** That is a design choice, not an oversight — it cannot invent a source that the researcher did not find. Restricting tools is a way to shape behavior, not just a safety measure.

### hbr-editor

Applies Harvard Business Review editorial standards, loading the [`editing-hbr-articles`](#editing-hbr-articles) skill for the detailed criteria. In the pipeline it produces two files: the publication-ready revision with edits already applied, and a separate memo explaining what changed and why.

The split matters. An earlier version returned only critique — excellent feedback that nothing downstream could publish. An agent whose output is *advice* cannot sit in the middle of a pipeline unless something acts on it.

### hbr-publisher

Produces both deliverables and then **inspects its own output** — converting the Word file and reading the rendered pages to confirm the title page and heading hierarchy came out right. It uses the plugin's pinned renderer rather than writing layout code per run, so every document comes out identical.

It is the one agent the approval hook guards: it cannot be dispatched until a human has approved.

## Skills

### editing-hbr-articles

The editorial criteria the editor loads before working: opening hooks and thesis clarity, evidence quality and source hierarchy, voice and language patterns to cut, and length guidelines by content type. Useful on its own for reviewing any business writing.

## Hooks

### subagent-gate.sh

A `SubagentStop` hook that validates each stage's artifacts before that agent is allowed to finish. It blocks a thin or uncited dossier, an under-length draft, a revision missing its memo, a critique masquerading as a finished article, and — most importantly — a markdown deliverable with no valid Word file beside it.

It validates **workspace state rather than agent identity**, because the hook payload does not reliably name the agent that just stopped. Checking which files exist and whether they are sound is more robust than trusting metadata.

### publish-gate.sh

A `PreToolUse` hook that inspects every subagent dispatch. If the target is `hbr-publisher` and no approval marker exists in the workspace, the harness refuses to launch it and tells Claude to ask the human first.

It is deliberately **fail-open**: an unrecognised payload, a missing field, malformed input, or no active run all allow the dispatch. A gate that wedges a live session would be worse than one that occasionally misses.

Be clear about what it is: a **guardrail against drift, not a security boundary.** The orchestrator could write the approval marker itself. What the hook guarantees is that skipping the human is a deliberate act rather than an accident, and that every dispatch attempt is logged.

## Commands

### /hbr-article

**Automatic delegation.** States the topic and the delegation constraint, and deliberately does not name a sequence. Claude decides which specialists to use and when. This is the [goal statement](../../../ai-workflow-framework/examples/autonomous-agent/#the-goal-statement) plus the workspace setup, so it works in any project.

### /hbr-article-strict

**Deterministic orchestration.** The same pipeline with the four stages spelled out in order, each with its input and output file. Use it when you need the same path every run, and as the contrast that makes the automatic version legible.

## Verify it before you trust it

Every enforcement mechanism ships with tests:

```bash
bash hooks/test-subagent-gate.sh      # 24 assertions on the quality gate
bash hooks/test-publish-gate.sh       # 17 assertions on the approval gate
bash scripts/test-article-to-docx.sh  # 16 assertions on the renderer
```

## Adapting it

1. **Replace the agents** with your own specialists, keeping each one's Workspace Mode section: read this file, write that file, return a summary not the work, never ask clarifying questions, and here is what the gate will check.
2. **Rewrite the descriptions.** Under automatic delegation, the agent `description` fields *are* the workflow — name each agent's place in the chain and the agents either side of it.
3. **Edit the gate rules** so they check what "good" means for your artifacts. Keep them to things that are objectively true or false.
4. **Point the approval gate** at whatever your irreversible step is.
5. **Write the goal statement last** — an outcome if you want delegation, a sequence if you want repeatability.

## Related

- [Autonomous Agent worked example](../../../ai-workflow-framework/examples/autonomous-agent/) — the full walkthrough
- [The Hands-on AI Plugin](../handsonai/) — the framework toolkit, separate on purpose
- [Using Plugins](../using-plugins/) — installing and managing plugins
- [Multi-Agent Collaboration](../../../agentic-building-blocks/agents/capability-patterns/multi-agent-collaboration/) — the capability pattern
- [Human-in-the-Loop](../../../agentic-building-blocks/agents/capability-patterns/human-in-the-loop/) — designing review gates
