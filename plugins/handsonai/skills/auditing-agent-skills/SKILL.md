---
name: auditing-agent-skills
description: >
  Audits existing Agent Skills for things that have gone out of date or drifted: retired model
  names, references to skills that were renamed or removed, naming drift, weak descriptions,
  dated facts, overlapping skills, missing test cases, and skills the AI Registry doesn't
  record. Use when the user asks to check, audit, tidy or review their skills as a set, asks
  any question about one kind of drift across them (which skills are out of date, use old
  models, still point at renamed skills, overlap, or are missing from the registry), or for a
  scheduled skill audit. Not for building or reviewing a
  single skill (use applying-skill-best-practices), and never changes a skill without the
  user's approval.
---

# Auditing Agent Skills

This skill checks a set of existing skills against one shared checklist and reports what has gone out of date, with a proposed fix for each finding. **It never changes a skill on its own.** Every fix is a proposal until the user approves it; a wrong rename inside a skill that runs other skills can break a working workflow.

> **Platform registry:** platform facts (how a skill is installed, where context lives, scheduling, agents) come from the platform registry. Read it from `references/platform-registry.json` in this skill's own folder; if that file isn't there, from `registries/platform-registry.json` at the plugin root; if neither exists, fetch `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`. Read it once per session and reuse it. Find a platform by its key or by any name in its `aliases` list.

For this skill, the facts that matter are each platform's `capabilities.skill_listing` (what you can see of the user's skills) and `unattended_runs` (whether an audit can run on a schedule). Treat a missing value as unknown and say so.

## Load the checklist

The audit criteria live in one place, `hygiene-criteria.md`, owned by the `applying-skill-best-practices` skill. Never write your own list. Look for it in this order, relative to this skill's own folder, and tell the user which one you used:

1. `references/hygiene-criteria.md` in this skill's folder (included when this skill was downloaded as its own file);
2. `../applying-skill-best-practices/references/hygiene-criteria.md` (the two skills installed together, as in the Hands-on AI plugin);
3. `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/skills/applying-skill-best-practices/references/hygiene-criteria.md`.

If none of these is available, stop. Tell the user you couldn't load the checklist, list where you looked, and ask them to install `applying-skill-best-practices` (or share the checklist). Don't audit against criteria you made up.

## Find the skills

Check `skill_listing` for the user's platform before promising anything:

- **Where `skill_listing` says the AI can read skill folders:** read every skill the user points you to, or by default the skill folders the platform loads. Skills from a plugin are named `plugin:skill`; a reference in that form points to a plugin skill, not to a missing one.
- **Where it says the AI sees only skill names, or nothing:** say what you can see and what you can't, and ask the user to attach the skills or their ZIP files. Never report a skill as fine when you haven't read it.

Say at the start of the report which skills you read and which you couldn't.

**More than about 20 skills:** audit in batches of about 20. First list every skill's name and description: check overlap and broken references against that full list, and run registry coverage and the standards check once, in batch 1's report. Then split the skills into batches (alphabetical unless the user picks an order). Read each batch's skills yourself; don't hand skills to helper agents, which is where findings get lost and the report drifts from the template. In a conversation, give batch 1's full report and stop: ask before starting the next. On a scheduled run, where no one can answer, audit every batch in turn and write one report per batch.

## Run the checks

When the user asks about one kind of drift (which skills use old models, say), run that check first and report it in the template's format, with "Checks run" naming only that check; then offer the full audit. Otherwise apply each criterion in the checklist to each skill. For every finding, record the skill, the criterion, the exact line or field, what's wrong, and a specific proposed change: a before and after for anything that edits a file; for a fix that is work rather than an edit (writing test cases, re-reading a source), the exact action and the file it creates or updates. Check the proposed changes against each other before reporting: two findings must never propose conflicting fixes. A few judgment calls:

- **Retired model names:** check against the platform's current model list (fetch the provider's models page if you can); don't rely on a list remembered or written into a skill.
- **Broken references:** a reference is broken only when no skill by that name exists where the platform would load it. When a skill with a similar name and the same job exists, name it as the likely rename.
- **Naming:** flag a name only when it breaks the convention the user's other skills follow, and say which convention. Judge the form by the name's first word (`closing-the-month-checklist` starts with a verb-ing word, so it fits a verb-ing convention).
- **Test cases:** look in the skill's own folder (for example `evals/evals.json`) and open what the skill points to before flagging test cases as missing.
- **Overlap:** two skills overlap when their descriptions would both fire for the same request. Name the request.
- **Registry coverage:** where the user keeps an AI Registry, run its own lint if one exists and use its warnings; otherwise compare the skills you read with the skills the registry's workflow entries list. For each unrecorded skill, propose which workflow it belongs to as an exact change: the workflow entry's file and the line to add to its skills list, or, when no workflow fits, a new entry with its name and file. A skill that lives only in a platform account, which the registry can't record yet, is "not cataloged yet", not an error.
- **The standards themselves:** apply checklist criterion 7 to the best-practices sources list, so the standards get re-checked. Find it at `../applying-skill-best-practices/references/sources.md`, or else `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/skills/applying-skill-best-practices/references/sources.md`; if neither is available, say this check couldn't run.

Only report what needs attention. Don't list every check that passed, and don't list something that isn't wrong (a reference that resolves, a plugin skill named `plugin:skill`) as a finding, even with a note that it's fine. Report each problem once: when two skills overlap, that's one finding naming both.

## Report

Write the report using `references/audit-report-template.md` (read it when you write the report). Save it as `outputs/skill-audit-YYYY-MM-DD.md` (with `-batch-k` added when batching) in the user's working folder where there is one; otherwise show it in the conversation. Play findings back in plain words: name the skill and what's wrong, not file syntax, and offer to show the exact change.

Each batch gets its own report in the template's format; never replace it with a summary of your own design. With many findings, open with a short summary by severity, but still number every finding and give each its proposed change (in an appendix if the list is long), and on a full audit still run every check in the checklist, including registry coverage, test cases and source dates. Count the skills from the actual list you read: skills with findings plus skills without must equal skills read, and every skill named under no findings must be in that count.

## Applying fixes

Only after the user approves. Ask which fixes to apply (all, or which ones by number). Apply one at a time, show each change, and say when you're done. If a fix renames a skill or changes what another skill calls, list every skill that refers to it and update them together, or don't apply it.

## Running on a schedule

If the user wants a regular audit, check `unattended_runs` for their platform. Where scheduled runs exist, suggest a monthly run that writes the report and changes nothing. Where they don't, suggest a monthly reminder to run "audit my skills" by hand.
