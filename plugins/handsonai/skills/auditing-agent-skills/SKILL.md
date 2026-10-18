---
name: auditing-agent-skills
description: >
  Audits existing Agent Skills for things that have gone out of date or drifted: retired model
  names, references to skills that were renamed or removed, naming drift, weak descriptions,
  dated facts, overlapping skills, missing test cases, and skills the AI Registry doesn't
  record. Use when the user asks to check, audit, tidy or review all their skills, wants to
  know which skills are stale, or for a scheduled skill audit. Not for building or reviewing a
  single new skill (use applying-skill-best-practices), and never changes a skill without the
  user's approval.
---

# Auditing Agent Skills

This skill checks a set of existing skills against one shared checklist and reports what has gone out of date, with a proposed fix for each finding. **It never changes a skill on its own.** Every fix is a proposal until the user approves it; a wrong rename inside a skill that runs other skills can break a working workflow.

> **Platform registry:** platform facts (how a skill is installed, where context lives, scheduling, agents) come from the platform registry. Read it from `references/platform-registry.json` in this skill's own folder; if that file isn't there, from `registries/platform-registry.json` at the plugin root; if neither exists, fetch `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`. Read it once per session and reuse it. Find a platform by its key or by any name in its `aliases` list — a Design Spec that says `Cowork` or `Claude.ai` means the `claude` entry.

For this skill, the facts that matter are each platform's `capabilities.skill_listing` (what you can see of the user's skills) and `unattended_runs` (whether an audit can run on a schedule). Treat a missing value as unknown and say so.

## Load the checklist

The audit criteria live in one place, `hygiene-criteria.md`, owned by the `applying-skill-best-practices` skill. Never write your own list. Look for it in this order, relative to this skill's own folder, and tell the user which one you used:

1. `references/hygiene-criteria.md` in this skill's folder (included when this skill was downloaded as its own file);
2. `../applying-skill-best-practices/references/hygiene-criteria.md` (the two skills installed together, as in the Hands-on AI plugin);
3. `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/skills/applying-skill-best-practices/references/hygiene-criteria.md`.

If none of these is available, stop. Tell the user you couldn't load the checklist, list where you looked, and ask them to install `applying-skill-best-practices` (or share the checklist). Don't audit against criteria you made up.

## Find the skills

Check `skill_listing` for the user's platform before promising anything:

- **Where you can read skill folders** (Claude Code, Codex): read every skill the user points you to, or by default the skill folders the platform loads. Skills from a plugin are named `plugin:skill`; a reference in that form points to a plugin skill, not to a missing one.
- **Where you can only see skill names** (Claude, ChatGPT, Microsoft 365 Copilot, Gemini Enterprise at the time of writing): say what you can see and what you can't, and ask the user to attach the skills or their ZIP files. Never report a skill as fine when you haven't read it.

Say at the start of the report which skills you read and which you couldn't.

## Run the checks

Apply each criterion in the checklist to each skill. For every finding, record the skill, the criterion, the exact line or field, what's wrong, and a specific proposed change (before and after, or a diff). A few judgment calls:

- **Retired model names:** check against the platform's current model list (fetch the provider's models page if you can); don't rely on a list remembered or written into a skill.
- **Broken references:** a reference is broken only when no skill by that name exists where the platform would load it. When a skill with a similar name and the same job exists, name it as the likely rename.
- **Overlap:** two skills overlap when their descriptions would both fire for the same request. Name the request.
- **Registry coverage:** where the user keeps an AI Registry, run its own lint if one exists and use its warnings; otherwise compare the skills you read with the skills the registry's workflow entries list. For each unrecorded skill, propose which workflow it belongs to. A skill that lives only in a platform account, which the registry can't record yet, is "not cataloged yet", not an error.
- **The standards themselves:** flag any source in the best-practices sources list whose `last_reviewed` date is more than six months old, so the standards get re-checked.

Only report what needs attention. Don't list every check that passed.

## Report

Write the report using `references/audit-report-template.md` (read it when you write the report). Save it as `outputs/skill-audit-YYYY-MM-DD.md` in the user's working folder where there is one; otherwise show it in the conversation. Play findings back in plain words: name the skill and what's wrong, not file syntax, and offer to show the exact change.

## Applying fixes

Only after the user approves. Ask which fixes to apply (all, or which ones by number). Apply one at a time, show each change, and say when you're done. If a fix renames a skill or changes what another skill calls, list every skill that refers to it and update them together, or don't apply it.

## Running on a schedule

If the user wants a regular audit, check `unattended_runs` for their platform. Where scheduled runs exist, suggest a monthly run that writes the report and changes nothing. Where they don't, suggest a monthly reminder to run "audit my skills" by hand.
