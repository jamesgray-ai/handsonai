# What counts as outdated

The criteria a skill review or audit holds existing skills to. They describe what to flag, not how to run an audit. Report each finding with the skill, the line or field, and the proposed change. Never change a skill without the user's approval: a wrong rename inside an orchestration skill breaks every workflow that runs it.

1. **Retired or outdated model names.** A `model:` setting, or a model named in the instructions, that is no longer current. Check against the platform's live model list, not a list remembered or written into a skill.
2. **Broken references to other skills.** A skill names another skill that has been renamed or removed. Check orchestration skills first: one missing step stops the whole sequence.
3. **Naming that no longer fits the convention** in use, for the skill's own name and the names it refers to.
4. **Description problems:** over the platform's length limit, missing a "Use when…" trigger, or missing a "Not for…" boundary; two skills whose descriptions overlap enough to compete.
5. **Stale content:** dated facts in instructions, broken links, and skills with no test cases.
6. **Registry coverage:** skills the user's AI Registry doesn't record, and registry entries that point at skills which no longer exist. Where the registry has its own lint, use its warnings rather than re-deriving them. A skill the registry can't yet record (one that lives only in a platform account, say) is "not cataloged yet", not an error.
7. **The standards themselves:** a source in `sources.md` whose `last_reviewed` date is more than six months old, so the guidance may have moved on. Flag it for re-reading; the fix belongs in this skill.
