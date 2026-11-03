# Publishing by Hand

Use these steps when the script can't run. They do exactly what `scripts/publish-plugin.sh` does.
Use your own file tools for copying, and Git for the history. Git is required: without it, nothing
can be sent to GitHub, so stop and help the user install it.

## First time: the two descriptor files

Create `.claude-plugin/marketplace.json` at the plugin repository's root:

```json
{
  "name": "<plugin-name>",
  "owner": { "name": "<their name>" },
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./plugins/<plugin-name>",
      "description": "<one sentence>",
      "version": "0.0.0"
    }
  ]
}
```

Create `plugins/<plugin-name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<plugin-name>",
  "description": "<one sentence>",
  "version": "0.0.0",
  "author": { "name": "<their name>" }
}
```

Add `.publish-plugin` and `.DS_Store` to `.gitignore`. Write `.publish-plugin` with four lines:
`source=<path>`, `plugin=<name>`, `skills_dir=.claude/skills`, `agents_dir=.claude/agents` (or `skills` and `agents` if the source keeps them at the top level).

## Every release

1. **Check.** `git status --porcelain` in the plugin repository must be empty, and in the source it
   must show no changes under the skills or agents folders. Both version fields must match. Look for
   files named `.env`, `*.pem`, `*.key`, `id_rsa*`, or with "secret" or "credentials" in the name
   under the source's skills and agents: if any exist, stop.
2. **Copy.** Delete `plugins/<name>/skills/` and `plugins/<name>/agents/`. Copy each source skill
   folder that contains `SKILL.md` into `plugins/<name>/skills/`, and each `.md` file at the top of
   the source's agents folder into `plugins/<name>/agents/`. Remove any `.DS_Store`, `Thumbs.db`,
   `desktop.ini`, `node_modules`, `__pycache__`, `evals`, `*-workspace` or `iteration-*` that came
   along.
3. **See what changed.** `git status --porcelain --untracked-files=all` in the plugin repository.
   Group the paths by skill folder or agent file. A skill or agent is *added* if it isn't in the last
   release (`git ls-tree HEAD <path>` prints nothing), *removed* if it's in the last release but not
   on disk now, and *updated* otherwise.
4. **Version.** First release: 1.0.0. Any removal: next major. Any addition: next minor. Otherwise:
   next patch. Set the same number in both files, then re-read both to confirm they match.
5. **Save and send.** One commit, then push, exactly as in Phase 4 of the skill.
