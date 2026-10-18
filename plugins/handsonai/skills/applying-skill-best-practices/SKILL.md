---
name: applying-skill-best-practices
description: >
  Best-practice standards for building Agent Skills on any platform: checking for an existing
  skill first, scoping it to one job, writing a description that triggers, keeping instructions
  lean, choosing model and effort settings, and preparing test cases from real examples. Use
  whenever a skill is being created, changed, reviewed or tested, alongside the platform's own
  skill creator: building one from scratch, turning a conversation or a repeated task into
  something reusable, updating or fixing an existing skill, or checking a SKILL.md before it's
  shared. Applies even if the user doesn't say "skill" or "best practices". Not for building
  agents, plugins, prompts or workflows that aren't skills, for running a skill that already
  works, or for auditing a set of existing skills (use auditing-agent-skills).
---

# Applying Skill Best Practices

These are the standards a good Agent Skill meets, consolidated from Anthropic, OpenAI, AgentSkills.io and Google and checked against each other. Read `references/sources.md` when the user asks where a rule comes from, or when auditing the standards themselves. The same standards, with a worked example, are written up for people at https://handsonai.info/agentic-building-blocks/skills/skill-best-practices/. Apply them whenever a skill is created, edited, reviewed or tested.

This skill does not build skills. The platform's own skill creator (Anthropic's skill-creator, the ChatGPT or Codex skill creator, Copilot Cowork's guided flow, Gemini Enterprise's "Create skill with Gemini") owns that process. These standards tell it what "good" means at each point. Where the creator already covers something, agree with it: your job is to make sure the user's own material (real examples, what a good result looks like, the cases they worry about) goes in, not to add a competing rule.

> **Platform registry:** platform facts (how a skill is installed, where context lives, scheduling, agents) come from the platform registry. Read it from `references/platform-registry.json` in this skill's own folder; if that file isn't there, from `registries/platform-registry.json` at the plugin root; if neither exists, fetch `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`. Read it once per session and reuse it. Find a platform by its key or by any name in its `aliases` list — a Design Spec that says `Cowork` or `Claude.ai` means the `claude` entry.

For this skill, the facts that matter are each platform's `capabilities.skill_install`, `skill_settings` (whether a skill can choose its own model and effort), `skill_invocation` (how a skill is set to run only when named) and `skill_evaluation` (whether the platform's skill creator runs tests). Never state those facts from memory.

## The six decisions

Every skill rests on six decisions, grouped by when they come up. Hold each one to its standard.

### Before you build

**1. Reuse first.** Before drafting anything, find out whether a skill for this job already exists, in every place a skill can live: the skills available in this session (including skills saved to the user's platform account), local skill folders on code platforms, GitHub repos the user names, and the user's AI Registry (`registry/`) if there is one. Match on what a skill does, not only its name. Then tell the user plainly which applies:

- **Use it as is:** an existing skill already does the job. Point to it and stop.
- **Extend it:** an existing skill covers most of it. Propose the change to that skill.
- **Build new:** nothing covers it. Say what you checked.

**2. Scope.** One skill does one coherent job. Too narrow, and several skills must load for one task; too broad, and it won't trigger at the right moment. Build it from the user's real expertise, not general knowledge: their own task, the corrections they make, their documents. Gather two or three **real examples** of the task, each a starting input and a good result. If the user has none, draft realistic examples, mark them clearly as drafts, and ask the user to correct them before anything is built on them. The corrections are the user's knowledge going in.

### While you build

**3. Trigger.** The description decides when the skill runs, so it carries the most weight. The standard pattern:

> [What it does, in the third person]. Use when [the situations and words that should trigger it]. Not for [the near-misses that shouldn't].

Put the key use case first. Use the words people actually type, including cases where they don't name the domain. Stay within the platform's length limit (1,024 characters in the open standard). Names are lowercase with hyphens, match the folder name, and prefer the verb-ing form (`drafting-proposals`). Read `references/descriptions.md` when writing or revising a description.

**4. Content.** Include only what the AI wouldn't know without the skill. Test each line: *would the AI get this wrong without it?* If not, cut it. What earns its place:

- a **gotchas** section: the specific mistakes the AI makes without being told (add one every time the user corrects it);
- templates and worked examples for the output, not descriptions of it;
- a checklist and a check-your-work loop where quality matters;
- one clear default rather than a menu of options;
- a method that works for any case, not the answer to one case.

Keep `SKILL.md` under 500 lines. Move detail into reference files one level deep, and for each one say *when* to read it ("Read `references/x.md` when …"), never just "see references/". Use one term per idea throughout. Keep dated facts out of instructions. Name tools exactly, including MCP tools with their server name.

**5. Settings.** Decide how the skill may run:

- **Automatically or by name only.** A skill that sends, publishes, deploys or creates records in another system runs only when the user names it. The platform's `skill_invocation` entry says which setting does this.
- **Tool access:** list the tools the skill may use, narrowed to what the job needs (`allowed-tools` in the open standard, where the platform supports it). For a skill that acts in another system, set this list in the draft; don't leave it as an option for later.
- **Model and effort:** check the platform's `skill_settings`. Where a skill can choose its own (at the time of writing, Claude Code), recommend a model and effort level with a reason. Read `references/model-and-effort.md` when the platform allows per-skill settings or the user asks about model or effort. Where it can't, don't add those fields; say the model chosen for the conversation applies.

### Before you trust it

**6. Tests.** No skill is finished without test cases, prepared while it's being built:

- two or three **test prompts** written from the real examples;
- **what good looks like** for each, in plain words (these become checks graded Met or Not met);
- **the one case most likely to go wrong**;
- about ten **trigger prompts**, half of which should fire the skill and half near-misses that shouldn't.

Save them in the skill folder: `evals/evals.json` on Claude Code (the format Anthropic's skill-creator uses), or a plain `evals/test-cases.md` elsewhere. Then run them with and without the skill, and fix what fails. Read `references/evaluations.md` when preparing or running tests, and `references/report-template.md` when producing the test report.

## Record where it lives

Every skill has one home: the place you edit it (a folder, a GitHub repo, or a platform account). Finishing a skill includes recording it in the user's AI Registry, with where that home is, and the workflow it serves. If the registry can't yet record a skill that lives outside the workspace (an account-only skill, say), note it as not yet cataloged rather than skipping it.

## Working with the platform's skill creator

The usual request names both skills, so both load:

> Use the skill creator and follow applying-skill-best-practices to build a skill for [task]. Here are two real examples of the task: …

When this skill loads, say so once ("I'm following applying-skill-best-practices"), so the user knows the standards are in play. On a platform where the skill creator can't load a second skill alongside it, the user can attach this `SKILL.md` to the conversation instead.

## When reviewing or auditing

Hold an existing skill to the same six decisions. Report what falls short, with the line or field it concerns, and propose the change; don't rewrite a skill the user didn't ask you to change. For what counts as outdated (retired model names, broken references to other skills, naming that no longer fits), read `references/hygiene-criteria.md`. To audit a whole set of skills at once, use the `auditing-agent-skills` skill.
