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
into each plugin, or that one stays in the source repository. Nothing reaches a team until someone
decides it should, and every release of a plugin gets a new version number.

The script `scripts/publish-plugin.sh` does the copying, the release plan and the version numbers. It
needs only Bash and Git: built into macOS, and on Windows it runs in Git Bash, which comes with Git
for Windows. Where the script can't run, follow `references/by-hand.md`.

## Workflow

Run the script with `bash <this skill's folder>/scripts/publish-plugin.sh <command> --plugin-repo <plugin folder>`.
Pass paths with forward slashes, on Windows too (`C:/Users/pat/code/my-ai-work`).

**Entry.** If the plugin repository has a `.publish-plugin` settings file, this is a release. First,
if the plugin repository has a GitHub connection and GitHub already holds a release
(`git -C <plugin folder> ls-remote --heads origin` prints something), run
`git -C <plugin folder> pull --ff-only` so you start from the latest release and release plan; if
that pull fails, stop and show what Git said. Then run `list`, say in one line which source
repository and plugins it found, and go to Phase 3. If the user asked to add a plugin or move a
skill, do Phase 2 for that, then continue with Phase 3. Otherwise start at Phase 1.

#### Phase 1 — Set up the plugin repository (first time only)

Say: "First we'll set up where your plugins live. Your skills and agents stay in your source
repository; the plugin repository gets only what you release."

Ask one at a time, saying what you already know before each:

1. **The source repository.** "Which folder on your computer is your source repository, the GitHub
   repository with your skills in `.claude/skills` and your agents in `.claude/agents`?" Confirm it
   holds at least one folder with a `SKILL.md`. Setup finds `.claude/skills` and `.claude/agents`
   on its own (or `skills/` and `agents/` at the top, if that's where they are).
2. **The plugin repository.** "Do you already have an empty GitHub repository for your plugins, or
   shall I create one?" To create one, recommend private: "I recommend private: these skills are
   your company's work. Anyone you share it with needs access to the repository on GitHub." With
   their OK, run `gh repo create <name> --private --clone` (or `--public` if they choose) in the
   folder that holds the source repository, then use the new folder. Suggest a name for the
   collection, such as `acme-plugins`. If `gh` isn't installed or signed in, ask them to create the
   repository on github.com and clone it, then continue.

Run `setup --source <source>`. It records the owner from the name Git uses on this computer; add
`--owner "<name>"` if that's empty or not the user. It writes the settings file (kept out of GitHub, since it holds a
path on this computer), the `.gitignore`, a README that tells teammates how to install, the release
plan, and the marketplace file Claude reads. A plugin someone already started in `plugins/<name>/`
(with Plugin Dev or Claude's plugin creator, for example) is kept; one still at version 0.x counts
as never released. Continue to Phase 2.

#### Phase 2 — Decide what goes into each plugin

**The plugins.** If there are none yet, ask: "Who will use these? One plugin for your whole team is
the simple start; separate plugins make sense when different teams need different skills." For each
plugin, recommend a name for the team that uses it, lowercase with hyphens (`sales-team-skills`).
*Why:* "Teammates see this name when they install it." Run `add-plugin --name <name> --description
"<one sentence>"`.

**The release plan.** Run `check`. For every skill and agent it lists as `UNDECIDED`, ask which
plugin it goes into, or none. With several undecided, play them back as one list with a recommended
plugin for each and ask the user to confirm or change it. Recommend **none** for anything that's
only a tool for working in the source repository (for example a knowledge graph's `ingest` and
`lint` skills), and say why: "It helps you work in this folder; your team doesn't need it." Record
each answer with `assign <plugin|none> <skill|agent> <name>`; a skill can go into more than one
plugin.

When the user asks to move something later, use `assign` and `unassign`: "add X to the sales
plugin" is `assign sales skill X`; "stop publishing Y" is `unassign <plugin> skill Y` for each plugin
it's in, then `assign none skill Y`, without asking again. Say that taking something out of a plugin makes that plugin's next release
a major one, because anyone who used it will notice it's gone.

#### Phase 3 — Check everything is ready

Run `check`. **If it exits 3, act on that alone:** possible passwords or keys are in a skill or agent
that would be released. Show the files and stop; nothing is copied. They must come out of the skill
(and its history, if it was ever pushed) first. Never offer to save anything while they're there.
Otherwise act on what it reports, one item at a time:

- **UNDECIDED:** go back to Phase 2 for those items. Nothing undecided is released.
- **The source has changes not yet saved in its history.** Only saved work gets published, so the
  release records exactly what shipped. Show the changed files and ask: "These changes aren't saved
  in your source repository's history yet. Shall I save them now, so they're part of this release?"
  With their OK, commit them in the source repository with a message that says what changed (and
  push, if it has a GitHub connection), then run `check` again so the release names that commit.
  If they say no, stop.
- **The plugin repository has changes made by hand.** Changes to the release plan and the files the
  script writes are part of the release and aren't reported; anything listed here was changed some
  other way. Show the files and ask whether to discard them (`git -C <plugin> checkout -- <file>`,
  or delete a new file) or stop. Never release on top of them.

#### Phase 4 — Copy and show what's changing

Run `copy`. For each plugin it replaces the skills and agents with the ones the release plan lists
(skipping files that never ship, like `.DS_Store` and `evals`), then reports, plugin by plugin, what
was added, updated or removed, with a suggested version change. Plugins with no changes aren't
listed and keep their version. A `MISSING` line means the plan lists something the source no longer
has: say so, and offer to remove it from the plan.

If nothing changed, say: "Your plugins already match your source repository, so there's nothing to
release." Then stop.

Play each plugin's list back in plain words and recommend its version, with the reason:

| What changed in that plugin | Version change | Reason to give |
|---|---|---|
| First release | 1.0.0 | "Its first release." |
| A skill or agent removed | major (2.0.0) | "Anyone who used the removed one will notice it's gone." |
| A skill or agent added | minor (1.1.0) | "Something new, nothing taken away." |
| Only changes to existing ones | patch (1.0.1) | "Improvements to what's already there." |

The biggest kind of change in a plugin wins. Ask once for every changed plugin, naming each with its
version ("Release sales-team-skills as 1.0.2?" or, for two, "Release sales-team-skills as 1.0.2 and
ops-team-skills as 1.1.0?"). If they want different numbers, use them.

#### Phase 5 — Release

On their yes:

1. Run `bump <plugin> <first|major|minor|patch|X.Y.Z>` for each plugin being released. It rebuilds
   the marketplace file from the plugins, so the version numbers always agree.
2. **Validate** where the Claude Code command is installed (`claude --version` works): run
   `claude plugin validate <plugin folder>` and `claude plugin validate <plugin folder>/plugins/<name>`
   for each released plugin. Only a failed validation stops the release (the command exits non-zero,
   or doesn't end with "Validation passed"): show it, fix it in the source repository (never in the
   plugin repository), save it, and start again at Phase 3. Warnings, and the notes about what the
   public plugin directory would require (such as a LICENSE file), don't stop a release; mention
   them in one line. Where the command isn't installed, skip this: installing in
   Claude is the check.
3. Run `git -C <plugin folder> status --short` and check every file listed is under `plugins/` or
   `.claude-plugin/`, or is `.gitignore`, `README.md` or `release-plan.txt`. Ask before including
   anything else.
4. Save the release in one commit: `git -C <plugin folder> add -A`, then commit with the subject
   `Release <plugin> vX.Y.Z[, <plugin> vX.Y.Z] from <source folder name>@<source commit>` (plugins in
   alphabetical order) and a body
   with one line per released plugin: `<plugin> vX.Y.Z: added …; updated …; removed …` (leave out
   empty parts).
5. Push it: `git -C <plugin folder> push`. If the folder has no upstream yet
   (`git -C <plugin folder> rev-parse --abbrev-ref @{u}` fails), use `git -C <plugin folder> push -u origin HEAD`.
   Push last: Claude decides an update is ready from what it finds on GitHub, so it must only ever
   find a finished release. If the push fails, show what Git said and stop; never retry with force.

#### Phase 6 — Get it into Claude

Read `references/installing-and-updating.md` and give the steps for where they use Claude: on a
plugin's first release, how to add the plugin repository and install it; on later releases, how to
pick up the new version. Close with: "To release your next change, edit it in your source
repository, save it, and say 'publish my plugin'."

## Output

- In the plugin repository: `plugins/<name>/` for each plugin (its `.claude-plugin/plugin.json`,
  `skills/`, `agents/`), `.claude-plugin/marketplace.json`, `release-plan.txt`, `README.md`, and one
  commit per release, pushed to GitHub.
- A `.publish-plugin` settings file in the plugin repository, kept out of GitHub.
- The source repository is never changed, except to save (commit) the user's own changes when they
  agree.

## Guidelines

- **Nothing is released without a decision.** Every skill and agent is assigned to a plugin, or to
  none, before it can ship. The release plan is the record of who gets what.
- **Never publish what hasn't been saved in the source repository.** The release names the source
  commit, so anyone can trace a version back to exactly what shipped.
- **One release, one commit.** Each released plugin gets a new version number; the marketplace file
  is rebuilt from the plugins, never edited by hand.
- **Never force-push and never rewrite the plugin repository's history.** Teammates install from it.
- **The user approves the plugins, the release plan, the versions and the release.** Everything else
  is yours to do.
- **Skills and agents only.** A skill is a folder holding `SKILL.md`; an agent is a `.md` file at
  the top of the agents folder. Anything else in the source repository stays there.
- **Plain words.** Say "save" for commit and "send to GitHub" for push the first time you use each,
  then the plain word alone.
- `references/installing-and-updating.md`: read at Phase 6.
- `references/by-hand.md`: read when `bash` or `git` won't run, or the script reports an error you
  can't resolve.
