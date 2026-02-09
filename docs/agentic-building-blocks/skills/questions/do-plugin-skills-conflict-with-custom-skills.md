---
question: "If I add skills using plugins provided by developers, will they conflict with my custom skills?"
short_answer: "No. Plugin skills and custom skills live in separate directories and use namespaced identifiers, so they never overwrite or interfere with each other — even if they cover similar topics."
platforms: [claude]
topic: skills
date: 2026-02-09
author: James Gray
---

# If I add skills using plugins provided by developers, will they conflict with my custom skills?

**Short answer:** No. Plugin skills and custom skills live in separate directories and use namespaced identifiers, so they never overwrite or interfere with each other — even if they cover similar topics.

## The Full Answer

Claude Code stores skills in four separate locations, each with a different scope. From highest to lowest priority:

| Location | Path | Applies to |
|:---------|:-----|:-----------|
| Enterprise | Managed settings (set by your organization) | All users in your organization |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

When skills at different levels share the same name, higher-priority locations win: enterprise overrides personal, personal overrides project. But plugin skills are different — they use a **namespaced identifier** in the format `plugin-name:skill-name`. This means a plugin skill like `business-first-ai:editing-hbr-articles` can never collide with a personal skill you named `editing-hbr-articles`. They are treated as entirely separate skills.

This namespacing also means you can safely install multiple plugins from different developers without worrying about name collisions between them. A skill called `writing-posts` in one plugin is `plugin-a:writing-posts`, while the same name in another plugin is `plugin-b:writing-posts` — both exist independently.

In practice, if you've built a custom skill that does something similar to a plugin skill, both remain available. Claude sees all of them and picks the most relevant one based on your request. You can also invoke either one directly using its slash command (`/my-skill` for your custom skill or `/plugin-name:skill-name` for the plugin version).

## Example

Say you have a personal skill for writing LinkedIn posts and you install a plugin that also includes a LinkedIn writing skill:

```
# Your custom skill
~/.claude/skills/write-linkedin-post/SKILL.md
→ Invoked with: /write-linkedin-post

# Plugin skill
business-first-ai plugin
→ Invoked with: /business-first-ai:writing-linkedin-posts
```

Both skills load independently. Your custom skill uses your personal voice and formatting preferences. The plugin skill follows the plugin author's framework. You can use either one — or let Claude pick the best match based on your prompt.

## Key Takeaways

- **Plugin skills are namespaced** — they use `plugin-name:skill-name`, so they cannot conflict with your personal or project skills
- **The four skill levels are isolated** — enterprise, personal, project, and plugin skills each live in separate directories
- **Same-name resolution only applies within non-plugin levels** — enterprise > personal > project, but plugin skills are always separate
- **Multiple plugins coexist safely** — each plugin's skills are namespaced to that plugin
- **Claude sees all available skills** — it picks the most relevant one, or you can invoke a specific one directly with its slash command

## Related Questions

- [What is the difference between a skill and an agent in Claude Code?](./what-is-the-difference-between-a-skill-and-an-agent-in-claude-code.md)

---

**Sources:**

- [Extend Claude with skills — Where skills live | Claude Code Docs](https://code.claude.com/docs/en/skills#where-skills-live)
