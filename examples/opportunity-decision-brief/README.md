# Opportunity Decision Brief

This folder is a Claude plugin. The download on the `example-skills` release of `handsonai-plugins` is a ZIP of this folder.

A worked example of an orchestration skill from the *Build Agentic Workflows with Skills* lesson.

Type one command with a business opportunity after it:

    /opportunity-decision-brief A 6-week cohort teaching small-firm CPAs to build AI intake agents, priced at $1,500

The skill clarifies the idea with you, sends four research sub-agents out in parallel (market, customer, competitive, risk), hands their cited reports to a fifth that writes the brief, and stops so you make the go / refine / no-go call. Briefs save to `opportunity-briefs/` in your working folder. It uses web research only.

## Install

- **Claude:** Customize → Plugins → + → Upload, and choose this ZIP.
- **Claude Code:** unzip it, then copy `skills/opportunity-decision-brief/` into your project's `.claude/skills/` and the five files in `agents/` into `.claude/agents/`.

## What's inside

- `skills/opportunity-decision-brief/SKILL.md`: the orchestration skill. It takes the opportunity as an argument (`$ARGUMENTS`).
- `agents/`: `market-researcher`, `customer-researcher`, `competitive-researcher`, `risk-researcher`, `brief-synthesizer`.
