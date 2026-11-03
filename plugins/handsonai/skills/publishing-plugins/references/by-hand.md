# Publishing by Hand

Use these steps when the script can't run. They do exactly what `scripts/publish-plugin.sh` does.
Use your own file tools for copying, and Git for the history. Git is required: without it, nothing
can be sent to GitHub, so stop and help the user install it.

## First time

1. Write `.publish-plugin` in the plugin repository with three lines: `source=<path>`,
   `skills_dir=.claude/skills`, `agents_dir=.claude/agents` (or `skills` and `agents` if the source
   repository keeps them at the top level). Add `.publish-plugin` and `.DS_Store` to `.gitignore`.
2. Create `.claude-plugin/marketplace.json`:

   ```json
   {
     "name": "<marketplace-name>",
     "description": "<one sentence>",
     "owner": { "name": "<their name>" },
     "plugins": []
   }
   ```

3. Create `release-plan.txt` with a comment header. Each line is `<plugin|none> <skill|agent> <name>`
   (agent names without `.md`).
4. For each plugin, create `plugins/<plugin>/.claude-plugin/plugin.json`:

   ```json
   {
     "name": "<plugin>",
     "description": "<one sentence>",
     "version": "0.0.0",
     "author": { "name": "<their name>" }
   }
   ```

5. Write a README saying what the repository is and how to install it (see
   `installing-and-updating.md`).

## Every release

1. **Check.** Every skill (a folder under the skills folder holding `SKILL.md`) and every agent (a
   `.md` file at the top of the agents folder) has a line in `release-plan.txt`; ask about any that
   don't. In the plugin repository, `git status --porcelain` must show nothing except `release-plan.txt`, `.gitignore`, `.gitattributes`, and files under `.claude-plugin/` or `plugins/`; in the source repository,
   no unsaved changes under the skills or agents folders. Look for files named `.env`, `credentials.json`, `token.json`, `*.pem`,
   `*.key`, `id_rsa*`, or with "secret" or "credentials" in the name, in anything a plugin would
   release: if any exist, stop.
2. **Copy.** For each plugin, delete its `skills/` and `agents/`, then copy in exactly the skills and
   agents its lines in the release plan name. Remove any `.DS_Store`, `Thumbs.db`, `desktop.ini`,
   `node_modules` or `__pycache__` that came along inside a skill. Never remove a skill's own files.
3. **See what changed.** `git status --porcelain --untracked-files=all` in the plugin repository,
   grouped by plugin, then by skill folder or agent file. A skill or agent is *added* if it isn't in
   the last release (`git ls-tree HEAD <path>` prints nothing), *removed* if it's in the last release
   but not on disk now, and *updated* otherwise.
4. **Version each changed plugin.** Version 0.x: 1.0.0. Any removal: next major. Any addition: next
   minor. Otherwise: next patch. Set it in that plugin's `plugin.json`, then rewrite the `plugins`
   list in `marketplace.json` with one entry per plugin (`name`, `source: ./plugins/<name>`,
   `description`, `version`), copying each from its `plugin.json`.
5. **Save and send.** One commit, then push, exactly as in Phase 5 of the skill.
