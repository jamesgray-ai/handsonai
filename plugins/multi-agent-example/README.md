# Multi-Agent Example

**A worked example, not a toolkit.** This plugin contains one complete multi-agent
pipeline — four specialist agents that research, write, edit, and publish a business
article — built to be read, run once, and then adapted to your own work. The article is
the excuse; the architecture is the point.

Full walkthrough: **https://handsonai.info/ai-workflow-framework/examples/autonomous-agent/**

## What you get

| Component | What it is |
|---|---|
| `ai-productivity-researcher` | Agent — finds case studies with quantified, sourced outcomes |
| `tech-executive-writer` | Agent — drafts the article from the research dossier |
| `hbr-editor` | Agent — produces the publication-ready revision plus an editorial memo |
| `hbr-publisher` | Agent — produces both deliverables and inspects its own output |
| `editing-hbr-articles` | Skill — the editorial standards the editor loads |
| `subagent-gate.sh` | Hook (`SubagentStop`) — validates each stage's artifacts before the agent may finish |
| `publish-gate.sh` | Hook (`PreToolUse`) — blocks publishing until a human approves |
| `/multi-agent-example:hbr-article` | Command — automatic delegation: states the outcome, lets Claude pick the specialists |
| `/multi-agent-example:hbr-article-strict` | Command — deterministic: the same pipeline driven by an explicit sequence |
| `article-to-docx.js` | Script — pinned Word layout, so every run produces an identical document |

## Prerequisites

**Claude:** nothing. The document skill is already included.

**Claude Code:** you need Anthropic's document skills plugin, and Node.js. Node.js runs
the Word renderer and both gates, which use it to read what Claude Code sends them —
there is no other developer tool to install. Check with `node --version`; if it is
missing, install it from https://nodejs.org.

```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

The `docx` npm package the renderer uses is installed automatically the first time you
produce a document — into this plugin's own directory, never into your project. That step
needs network access once.

## Install

```
/plugin marketplace add jamesgray-ai/handsonai-plugins
/plugin install multi-agent-example@handsonai
```

Then:

1. Run `/reload-plugins` (or restart Claude Code) so the plugin's agents, commands, and
   hooks load into the session you are in.
2. Type `/hooks` and confirm both gates are listed as coming from this plugin: a
   `SubagentStop` hook running `subagent-gate.sh` and a `PreToolUse` hook running
   `publish-gate.sh`. A gate you believe is protecting you but that never loaded is worse
   than no gate.

## Installing hooks changes your environment — here is exactly how

This plugin ships two hooks, which merge into your Claude Code configuration and run
automatically. That is a real change, so it is worth being precise about the scope:

**Both hooks exit immediately unless `outputs/articles/.active-run` exists in your current
project.** That flag is created only when you start a pipeline run and deleted when it
ends. With no run in progress, the hooks do nothing to any other subagent or tool call in
any project.

The hooks join your session when the plugin loads — that is the `/reload-plugins` (or
restart) step above, and `/hooks` is how you confirm it happened.

## Running it

Plugin commands are named after the plugin, so the full command is
`/multi-agent-example:hbr-article`. You can also type `/hbr-article` and pick it from
the menu.

```
/multi-agent-example:hbr-article
```

Or with your own topic:

```
/multi-agent-example:hbr-article how mid-market manufacturers are using AI agents in procurement
```

### Or type the prompt

The slash command is a saved prompt. For a demonstration, pasting the prompt itself is more
convincing — an audience sees plain English produce four delegated agents and two documents:

```text
Write an HBR-style article for senior business leaders on companies that have
successfully deployed AI agents, and what separated them from the ones still
running pilots.

Use outputs/articles/ai-agents-in-production/ as the workspace and arm the gates first:
  echo "outputs/articles/ai-agents-in-production" > outputs/articles/.active-run

Delegate every stage to the specialist subagents, passing each one the absolute
workspace path. Do not research, write, edit, or publish any of it yourself.
Stop and ask me to approve before anything is published.
```

It is this short because the standards live in the system rather than the message. The
filenames are in each agent's Workspace Mode, the evidence floor (5+ named companies,
sources within 24 months) is in `ai-productivity-researcher`, and the length target
(2,000–2,500 words) is in `tech-executive-writer`. They hold on every run, including the
ones where you forget to ask.

Add the workspace convention to your own project's `CLAUDE.md` and the middle paragraph
goes away too, leaving a three-line prompt.

Then watch: Claude decides which specialist to dispatch and when, each agent writes a file
rather than pasting its work back, a gate blocks anything that falls short, and you are
asked to approve before anything is published. Deliverables land in
`outputs/articles/<slug>/` as `04-article.md` and `04-article.docx`.

To see the contrast that makes the example worth studying, run
`/multi-agent-example:hbr-article-strict` on the same topic and compare the two
transcripts. Same agents, same hooks, same deliverables — but you chose the sequence
instead of Claude.

## Verifying it before you trust it

```bash
bash hooks/test-subagent-gate.sh     # the quality gate, including its retry limit
bash hooks/test-publish-gate.sh      # the approval gate
bash scripts/test-article-to-docx.sh # the renderer
```

Each suite prints how many checks passed and failed.

## Adapting it

The five things to change, in order:

1. **The agents** — replace the four specialists with your own. Keep the "Workspace Mode"
   section in each: read this file, write that file, return a summary not the work, never
   ask clarifying questions, and here is what the gate will check.
2. **The descriptions** — under automatic delegation, the agent `description` fields *are*
   the workflow. Name each agent's place in the chain and the agents either side of it, or
   Claude has nothing to chain on.
3. **The durable standards** — put evidence bars, length targets, and format rules in the
   agents, not in the prompt. Anything you state per run is a standard you can forget.
4. **The gate rules** — edit `subagent-gate.sh` so it checks what "good" means for your
   artifacts. Keep it to things that are objectively true or false.
5. **The approval point** — `publish-gate.sh` blocks one named agent. Point it at whatever
   your irreversible step is.

## Known constraints

- The approval gate is a **guardrail against drift, not a security boundary**. The
  orchestrator could write the approval marker itself. What the hook guarantees is that
  skipping the human is a deliberate act rather than an accident, and that every dispatch
  attempt is logged.
- The quality gate sends a stage's work back **at most twice**. If it still falls short,
  the agent is allowed to finish — an endless loop would be worse — but the gate writes
  `QUALITY GATE FAILED after 2 retries: <reason>` to `run-log.md` and shows it to you on
  screen, and both commands tell the orchestrator to stop and report it. Failing work is
  never passed silently.
- Automatic delegation is not deterministic. It can skip a stage or reorder one. The gates
  are what make that acceptable — they enforce the outcome whatever path was taken. Use
  `/multi-agent-example:hbr-article-strict` when you need the same path every time.
- Visual verification of the Word file needs LibreOffice and Poppler. Without them the
  publisher skips that check and says so.

## License

MIT. Adapt it freely — that is what it is for.
