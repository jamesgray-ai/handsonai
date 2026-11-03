---
name: publishing-plugins
description: >-
  This skill should be used when the user wants to publish their skills and agents to their team as
  a Claude plugin, or release a change to a plugin they already publish. It keeps two GitHub
  repositories apart: the source repository where the user builds and changes skills and agents,
  and a plugin repository that holds only what has been released and that teammates install from.
  Each run copies what changed, picks the new version number, saves the release and sends it to
  GitHub. Triggers: "publish my plugin", "publish my skills", "release my plugin", "set up my
  plugin repository", "update my plugin", "push my changes to the plugin", "sync my plugin".
---

# Publishing Plugins

Publish skills and agents from the folder where they're built (the **source repository**) to a
separate **plugin repository** that teammates install in Claude. The source is the workbench: work in
progress lives there. The plugin repository is the shelf: only what was released is on it, each
release with a version number, so a teammate never gets a half-finished change.

The script `scripts/publish-plugin.sh` does the copying and the version numbers. It needs only Bash
and Git: built into macOS, and on Windows it runs in Git Bash, which comes with Git for Windows. Where
the script can't run, follow `references/by-hand.md`, which does the same steps by hand.

## Workflow

Run the script with `bash <this skill's folder>/scripts/publish-plugin.sh <command> --plugin-repo <plugin folder>`.
Pass paths with forward slashes, on Windows too (`C:/Users/pat/code/my-skills`).

**Entry.** If the plugin folder has a `.publish-plugin` settings file, this is a release: say in one
line which source and plugin it found, and go to Phase 2. Otherwise start at Phase 1.

#### Phase 1 — Set up the two repositories (first time only)

Say: "First we'll set up where your plugin lives. Your skills stay where you build them; the plugin
gets its own GitHub repository that holds only what you release."

Ask one at a time, saying what you already know before each:

1. **The source repository.** "Which folder on your computer holds your skills and agents? It's the
   GitHub repository you build in, with a `skills` folder and usually an `agents` folder." Confirm it
   exists and holds at least one folder with a `SKILL.md`. If the folders have other names, record
   them for setup.
2. **The plugin's name.** Recommend one from their team or business, lowercase with hyphens
   (`acme-sales-skills`). *Why:* "Teammates see this name when they install it, so name it for the
   team, not for yourself."
3. **The plugin repository.** "Do you already have an empty GitHub repository for the plugin, or
   shall I create one?" To create one, recommend private: "I recommend private: these skills are
   your company's work. Anyone you share it with needs access to the repository on GitHub." With
   their OK, run `gh repo create <name> --private --clone` (or `--public` if they choose) in the
   folder that holds their source, then use the new folder. If `gh` isn't installed or signed in,
   ask them to create the repository on github.com and clone it, then continue.

Then run `setup --source <source> --name <name>`. It records the owner from the name Git already
uses on this computer; add `--owner "<name>"` only if that's empty or wrong (add `--skills-dir` or
`--agents-dir` if the folders are named differently). It writes the settings file (kept out of
GitHub, since it holds a path on this computer), the `.gitignore`, and the plugin's two descriptor
files. Continue to Phase 2: the first release is version 1.0.0.

#### Phase 2 — Check both repositories are ready

If the plugin repository has a GitHub connection and GitHub already holds a release
(`git -C <plugin folder> ls-remote --heads origin` prints something), run
`git -C <plugin folder> pull --ff-only` first so you start from the latest release. If that pull
fails, stop and show what Git said. Before the first release, GitHub holds nothing yet: skip the pull.

Run `check`. **If it exits 3, act on that alone** (the last item below): never offer to save
anything while a possible password or key is in the source. Otherwise act on what it reports, one
item at a time:

- **The source has changes not yet saved in its history.** Only saved work gets published, so the
  release records exactly what shipped. Show the changed files and ask: "These changes aren't saved
  in your source's history yet. Shall I save them now, so they're part of this release?" With their
  OK, commit them in the source with a message that says what changed (and push, if the source has
  a GitHub connection), then run `check` again, so the release names the commit you just made. If
  they say no, stop: publishing without them would ship an older version than they expect.
- **The plugin repository has unsaved changes.** Something was changed there by hand, or an earlier
  release stopped partway. Show the files and ask whether to discard them (`git -C <plugin> checkout
  -- . && git -C <plugin> clean -fd`) or stop. Never release on top of them. (A brand-new plugin
  repository whose only changes are the files setup just created is fine: carry on.)
- **The two version numbers differ.** Say which they are and recommend the higher one as the base
  for this release.
- **Exit 3: possible passwords or keys** in the source. Show the files and stop. Nothing is copied.
  These must come out of the skill (and its history, if it was ever pushed) before anything ships.

#### Phase 3 — Copy and show what's changing

Run `copy`. It replaces the plugin's skills and agents with the source's (skipping files that never
ship, like `.DS_Store`, `node_modules` and `evals`), then lists each skill and agent as added,
updated or removed, and suggests a version change.

If it reports no changes, say: "Your plugin already matches your source, so there's nothing to
release. Change a skill or agent in your source, save it, and say 'publish my plugin' again." Then
stop.

Play the list back in plain words, then recommend the version, with its reason:

| What changed | Version change | Reason to give |
|---|---|---|
| First release | 1.0.0 | "Your first release." |
| A skill or agent removed | major (2.0.0) | "Anyone who used the removed one will notice it's gone." |
| A skill or agent added | minor (1.1.0) | "Something new, nothing taken away." |
| Only changes to existing ones | patch (1.0.1) | "Improvements to what's already there." |

When a release mixes kinds, the biggest one wins. Ask: "Release this as version X?" If they want a
different number, use it.

#### Phase 4 — Release

On their yes:

1. Run `bump <first|major|minor|patch|X.Y.Z>`. It sets the number in both descriptor files and
   checks they match.
2. Run `git -C <plugin folder> status --short` and check every file listed is under `plugins/` or
   `.claude-plugin/`, or is `.gitignore`. Anything else wasn't put there by this release: ask before
   including it.
3. Save the release in one commit:
   `git -C <plugin folder> add -A`, then commit with the subject
   `Release vX.Y.Z from <source folder name>@<source commit>` and a body of up to three lines,
   `Added: …`, `Updated: …`, `Removed: …`, each listing names (leave out a line with nothing on it).
4. Push it: `git -C <plugin folder> push`. If the folder has no upstream yet
   (`git -C <plugin folder> rev-parse --abbrev-ref @{u}` fails), use `git -C <plugin folder> push -u origin HEAD`.
   Push last, after everything else: Claude decides an update is ready from what it finds on GitHub,
   so it must only ever find a finished release. If the push fails, show what Git said and stop;
   never retry with force.

#### Phase 5 — Get it into Claude

Read `references/installing-and-updating.md` and give the steps for where they use Claude: on the
first release, how to add the plugin repository and install the plugin; on later releases, how to
pick up the new version. Close with: "Version X is on GitHub. To release your next change, edit it
in your source, save it, and say 'publish my plugin'."

## Output

- In the plugin repository: `plugins/<name>/skills/`, `plugins/<name>/agents/`,
  `plugins/<name>/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and one commit per
  release, pushed to GitHub.
- A `.publish-plugin` settings file in the plugin folder, kept out of GitHub.
- The source is never changed, except to save (commit) the user's own changes when they agree.

## Guidelines

- **Never publish what hasn't been saved in the source.** The release message names the source
  commit, so anyone can trace a version back to exactly what shipped.
- **One release, one commit, one version number.** Both descriptor files always carry the same
  number.
- **Never force-push and never rewrite the plugin repository's history.** Teammates install from it.
- **The user approves the version and the release.** Everything else is yours to do.
- **Skills and agents only.** A skill is a folder holding `SKILL.md`; an agent is a `.md` file at the
  top of the agents folder. Anything else in the source stays there.
- **Plain words.** The user learned GitHub basics; say "save" for commit and "send to GitHub" for
  push the first time you use each, then the plain word alone.
- `references/installing-and-updating.md`: read at Phase 5.
- `references/by-hand.md`: read when `bash` or `git` won't run, or the script reports an error you
  can't resolve.
