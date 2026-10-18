# Writing a description that triggers

The description is the only part of a skill the AI sees before deciding to load it. Everything about when the skill runs depends on it.

## The pattern

> [What it does, in the third person]. Use when [triggers]. Not for [near-misses].

- **What it does:** concrete verbs and objects ("Drafts follow-up emails from sales call notes"), not "Helps with emails".
- **Use when:** the situations and the words people actually type. Include cases where the user describes the need without naming it ("even if they don't say 'proposal'"). Lean slightly pushy: AI models tend to under-use skills.
- **Not for:** the nearest things it could be confused with. This is what stops false triggers.

Anthropic asks for the third person; AgentSkills.io suggests "Use this skill when…". The pattern above satisfies both.

## Before and after

```yaml
# Before: too vague to trigger reliably
description: Helps with sales emails.

# After
description: >
  Drafts follow-up emails from sales call notes, in our voice, with the agreed next step and
  date. Use after any sales or discovery call, or when the user pastes call notes and asks what
  to send, even if they don't say "follow-up". Not for cold outreach or marketing campaigns.
```

## Limits and naming

- The open standard caps the description at 1,024 characters; Claude Code truncates the skill listing at 1,536 characters for `description` plus `when_to_use`. Put the key use case first.
- Names: lowercase letters, numbers and hyphens; match the folder name; no leading, trailing or double hyphens; avoid the words "claude" and "anthropic". Prefer the verb-ing form (`drafting-follow-up-emails`). Avoid vague names (`helper`, `utils`).
- No XML tags in the name or description.

## Trigger prompts

Write about ten realistic prompts, saved with the skill's test cases:

- **Should fire (five):** vary the phrasing (formal, casual, with a typo), how explicit it is, and how much context it carries. The most useful are ones where the skill helps but the prompt doesn't name it.
- **Shouldn't fire (five):** near-misses that share words with the skill but need something else. "Write a fibonacci function" tests nothing for an email skill; "write a cold outreach email to a new prospect" does.

Run each prompt in a fresh conversation and note whether the skill loaded. If a should-fire prompt misses, broaden the "Use when" to the general situation it represents; if a near-miss fires, sharpen the "Not for". Don't paste the failing prompt's exact words into the description: fix the category, not the example.
