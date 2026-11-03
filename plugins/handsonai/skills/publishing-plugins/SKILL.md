---
name: publishing-plugins
description: >-
  This skill should be used when the user wants to publish their skills and agents to their team as
  Claude plugins, or release a change to plugins they already publish. It keeps two GitHub
  repositories apart: the source repository where the user builds and changes skills and agents, and
  a plugin repository that holds only released work and that teammates install from. One plugin
  repository can hold several plugins; the user decides which skills and agents go into each, and
  that decision is recorded. Each run copies what changed, recommends the new version number for
  each plugin, saves the release and sends it to GitHub. Triggers: "publish my plugin", "publish my
  skills", "release my plugin", "set up my plugin repository", "update my plugin", "add a plugin",
  "add this skill to my plugin", "stop publishing this skill".
---

# Publishing Plugins

Publish skills and agents from the **source repository**, where they're built and changed, to a
separate **plugin repository** that teammates install in Claude. Skills and agents live once, in the
source repository's `.claude/skills/` and `.claude/agents/`. The plugin repository can hold several
plugins (one per team, for example), and a **release plan** in it records which skills and agents go
into each plugin, or which are kept just for the user. Nothing reaches a team until someone decides
it should, and every release of a plugin gets a new version number.

The script `scripts/publish-plugin.sh` does the copying, the release plan and the version numbers. It
needs Bash and Git on the user's own computer: built into macOS; on Windows, Git for Windows (which
brings Git Bash). It runs where Claude works on the user's computer: Claude Code, including the Code
tab in the Claude desktop app. If you can't run commands on the user's computer, or `git` isn't
installed, say so plainly and stop: "Publishing needs to run on your own computer. Open the Code tab
in the Claude desktop app, choose this folder, and say 'publish my plugin' there." Where `bash` is
missing but `git` works, follow `references/by-hand.md`.

The leader never types a path, a Git command or a file name. You find folders, run commands, and
play back what you found in plain words for them to confirm.

## Workflow

Run the script with `bash <this skill's folder>/scripts/publish-plugin.sh <command> --plugin-repo <plugin folder>`.
Pass paths with forward slashes, on Windows too.

**Entry.** Find the plugin repository: look in the current folder, then in its parent folder's other
folders, for a `.publish-plugin` file. If one names the current folder (or the folder the user
mentioned) as its `source=`, this is a release:

1. If the plugin repository has a GitHub connection and GitHub already holds a release
   (`git -C <plugin folder> ls-remote --heads origin` prints something), run
   `git -C <plugin folder> pull --ff-only` so you start from the latest release. If that fails,
   show what Git said and stop.
2. Run `list` and say in one line what you found: "Your source repository is my-ai-work; your plugin
   repository acme-plugins holds sales-team-skills (version 1.0.2)."
3. If the user asked to add a plugin or move a skill, do Phase 2 for that. Then go to Phase 3.

Otherwise this is the first time: start at Phase 1.

#### Phase 1 — Set up the plugin repository (first time only)

Say: "Two places are involved. Your **source repository** is where you build and change your skills;
it stays as it is. Your **plugin repository** is a second GitHub repository that holds only what you
choose to share. Teammates add it to Claude once, and every update you release reaches them. Claude
calls a repository like this a marketplace."

1. **Find the source repository yourself.** Start from the folder you're working in. It's the source
   repository if it has skills in `.claude/skills` (folders, each holding a `SKILL.md`) or agents in
   `.claude/agents`. If not, look one level down in its folders. Play back what you found: "Your
   source repository is **my-ai-work**. It has 6 skills (meeting-recap, proposal-writer, …) and 1
   agent (research-helper). Is that the right one?" Treat a vague yes ("it's my AI folder") as yes
   once you've named its skills back to them. If you can't find it, ask: "What's the name of
   the folder where you keep your skills? You can also drag it into this chat." Never ask for a path.
2. **Create the plugin repository, next to the source repository, never inside it.** Recommend: "I
   recommend I create it for you on GitHub as **private**: these skills are your company's work, and
   private means only people you add can install them." Ask what their company or team is called if
   you don't know, and suggest that name with `-plugins` on the end (`acme-plugins`). Keep it clearly
   different from the plugin names to come (`acme-plugins` holds `sales-team-skills`). Teammates see
   it when they add it, so it's lowercase with hyphens; convert whatever they say into that form. With their OK, run
   `gh repo create <name> --private --clone` **in the source repository's parent folder**. If `gh`
   isn't installed or signed in, ask them to create an empty private repository on github.com (no
   README, no license) and paste its web address here; then run `git clone <address>` in the source
   repository's parent folder yourself.

Run `setup --plugin-repo <plugin folder> --source <source folder>`. It refuses two folders that are
the same or one inside the other, and a source with no skills or agents; if it does, say what's
wrong in one line and fix it with the user. It records the owner from the name Git uses on this
computer; add `--owner "<their name>"` if that's empty or not them. Continue to Phase 2.

#### Phase 2 — Decide what goes into each plugin

**The plugins.** Say: "A plugin is a bundle of your skills and agents that a teammate installs in one
step." If there are none yet, ask: "Who should get these? One plugin for your whole team is the
simple start; separate plugins make sense when different teams need different skills." Name each
plugin for the team that uses it, lowercase with hyphens (`sales-team-skills`), converting what they
say; teammates see the name when they install it. Run
`add-plugin --plugin-repo <plugin folder> --name <name> --description "<one sentence>"`.

**The release plan.** Run `check`. Before asking anything, fix what it reports that isn't a choice:

- `RENAME`: a skill or agent folder whose name has spaces or capitals can't be released. Offer to
  rename it in the source repository ("Call Notes" → `call-notes`); with their OK, rename the folder
  and the `name:` in its `SKILL.md`, then record the rename as a version in the source repository
  and send it to GitHub (their OK to rename covers this; don't ask again in Phase 3).
- `EMPTY`: a skill whose `SKILL.md` has no name isn't finished. Say so and leave it out until it is.

Then for the `UNDECIDED` skills and agents, play them back as one list with your recommendation for
each, and ask the user to confirm or change it:

"Here's who I suggest gets what:
- **sales-team-skills:** meeting-recap, proposal-writer, research-helper
- **Kept just for you (not shared):** ingest, lint — they help you work in this folder; your team
  doesn't need them.
Does that look right?"

"Kept just for you" never deletes anything: it stays in the source repository and simply isn't
released. Record each answer with `assign <plugin|none> <skill|agent> <name>` (`none` means kept
just for you); a skill can go into more than one plugin.

Later changes: "add X to the sales plugin" is `assign sales-team-skills skill X`; "stop sharing Y"
is `unassign <plugin> skill Y` for each plugin it's in, then `assign none skill Y`, without asking
again. Say that taking something out of a plugin makes that plugin's next release a major one,
because anyone who used it will notice it's gone.

#### Phase 3 — Check everything is ready

Run `check`. **If it exits 3, act on that alone.** A file that looks like a password or key is in
something that would be shared. Say: "[file] in [skill] looks like a password or key. I won't share
it. I'll move it out of the skill folder to [skill]-private-files next to your source repository. If
it was ever sent to GitHub, change that password or key." With their OK, move it, then run `check`
again. Never offer to record anything while it's there.

Otherwise act on what it reports, one item at a time:

- **RENAME, EMPTY, UNDECIDED:** back to Phase 2 for those items. Nothing undecided is shared.
- **MISSING:** the release plan lists something that's no longer in the source repository. Say so,
  and remove it from the plan with `unassign`. If it was in a plugin, that plugin's next release is a
  major one.
- **The source has changes not yet saved in its history.** Leaders often answer "I did save" here;
  they mean the file. Say: "Your changes to [skill] are on your computer but not yet recorded as a
  version in your source repository. Only recorded versions are shared, so your team gets exactly
  what you recorded. Shall I record them and send them to GitHub?" With their OK, commit them in the
  source repository with a message that says what changed, push if it has a GitHub connection, and
  run `check` again so the release names that version. If they say no, stop.
- **The plugin repository has changes made by hand.** Name each file and say what you recommend:
  "Someone changed README.md in your plugin repository directly. Your plugin repository should only
  change through publishing. I recommend I undo that change; if it's something you want to keep,
  tell me and we'll make it part of this release." To undo, run
  `git -C <plugin> checkout -- <file>`. Never release on top of an unexplained change.
- **The source repository isn't a Git repository.** Say: "Your source repository needs to be on
  GitHub so every release can say exactly what it came from." Stop, and help them set it up first.

#### Phase 4 — Copy and show what's changing

Run `copy`. It copies each plugin's skills and agents from the source repository (leaving out files
that never ship, like `.DS_Store` and `evals`) and reports, plugin by plugin, what was added,
updated or removed, with a suggested version. Plugins with no changes aren't listed and keep their
version.

If nothing changed, say: "Your plugins already match your source repository, so there's nothing to
release." If only `release-plan.txt` changed (for example, a new skill kept just for them), record
and send it with the message "Update release plan" so the record on GitHub stays current. Then stop.

Play each plugin's changes back in plain words and recommend its version, with the reason:

| What changed in that plugin | Version | Reason to give |
|---|---|---|
| First release | 1.0.0 | "Its first release." |
| A skill or agent removed | major (2.0.0) | "Anyone who used the removed one will notice it's gone." |
| A skill or agent added | minor (1.1.0) | "Something new, nothing taken away." |
| Only changes to existing ones | patch (1.0.1) | "Improvements to what's already there." |

The biggest kind of change in a plugin wins. Ask once, naming each changed plugin with its version:
"Release sales-team-skills as version 1.0.2?" If they want a different number, it must be higher
than the last release; the script refuses anything else.

#### Phase 5 — Release

On their yes:

1. Run `bump <plugin> <first|major|minor|patch|X.Y.Z>` for each plugin being released. It counts up
   from the last release, so running it twice never skips a number, and it rebuilds the marketplace
   file so the version numbers always agree.
2. **Validate** where the `claude` command is installed (`claude --version` works): run
   `claude plugin validate <plugin folder>` and `claude plugin validate <plugin folder>/plugins/<name>`
   for each released plugin. Only a failed validation stops the release (the command exits
   non-zero, or doesn't end with "Validation passed"): say what failed in plain words, fix it in the
   source repository (never in the plugin repository), record it, and start again at Phase 3. Say
   nothing about warnings or about what the public plugin directory would require (such as a
   LICENSE file).
3. Run `git -C <plugin folder> status --short` and check every file is under `plugins/` or
   `.claude-plugin/`, or is `.gitignore`, `README.md` or `release-plan.txt`. Ask before including
   anything else.
4. Record the release in one commit: `git -C <plugin folder> add -A`, then commit with the subject
   `Release <plugin> vX.Y.Z[, <plugin> vX.Y.Z] from <source folder name>@<source commit>` (plugins in
   alphabetical order) and a body with one line per released plugin:
   `<plugin> vX.Y.Z: added …; updated …; removed …` (leave out empty parts).
5. Send it to GitHub: `git -C <plugin folder> push`. If the folder has no upstream yet
   (`git -C <plugin folder> rev-parse --abbrev-ref @{u}` fails), use
   `git -C <plugin folder> push -u origin HEAD`. Push last: Claude decides an update is ready from
   what it finds on GitHub, so it must only ever find a finished release. If the push fails, say what
   went wrong in plain words and stop; never retry with force.

#### Phase 6 — Get it into Claude

Read `references/installing-and-updating.md` and give the steps for where they use Claude: on a
plugin's first release, how to add the plugin repository and install the plugin, and how to give a
teammate access; on later releases, how to get the new version. Close with: "Version [X] of
[plugin] is on GitHub. Next time you change a skill, open Claude in **[source folder]** and say
'publish my plugin'. Your plugin repository is **[plugin folder]**, next to it."

## Output

- In the plugin repository: `plugins/<name>/` for each plugin (its `.claude-plugin/plugin.json`,
  `skills/`, `agents/`), `.claude-plugin/marketplace.json`, `release-plan.txt`, `README.md`, and one
  commit per release, pushed to GitHub.
- A `.publish-plugin` settings file in the plugin repository, kept out of GitHub.
- The source repository changes only when the user agrees: recording their own edits, or renaming a
  folder that can't be released.

## Guidelines

- **Nothing is shared without a decision.** Every skill and agent is assigned to a plugin, or kept
  just for the user, before it can ship. The release plan is the record of who gets what.
- **Only recorded versions are shared.** The release names the source version it came from, so
  anyone can trace a plugin version back to exactly what was shared.
- **One release, one commit.** Each released plugin gets a higher version number; the marketplace
  file is rebuilt from the plugins, never edited by hand.
- **Never force-push and never rewrite the plugin repository's history.** Teammates install from it.
- **The user approves the plugins, the release plan, the versions and the release.** Everything else
  is yours to do, including finding folders and running every command.
- **Plain words.** Say "record a version" for commit and "send to GitHub" for push; never "commit",
  "push", "clone" or a path in a question. Name the real skill, plugin and folder, never "it".
- **Skills and agents only.** A skill is a folder holding `SKILL.md`; an agent is a `.md` file at
  the top of the agents folder. Nothing else in the source repository is ever copied.
- `references/installing-and-updating.md`: read at Phase 6.
- `references/by-hand.md`: read when `bash` won't run but `git` does, or the script reports an error
  you can't resolve.
