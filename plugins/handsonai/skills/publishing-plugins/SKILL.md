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
2. Run `list` and say in one line what you found (if it marks a version "not yet on GitHub", say
   that too): "Your source repository is my-ai-work; your plugin
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
2. **The plugin repository.** First ask: "Do you already have a GitHub repository for your plugins?"
   If yes, find its folder on their computer the same way, run `setup` on it, and play back what it
   holds. If setup says nothing was changed because the repository lists a plugin this skill doesn't
   manage, or its marketplace file isn't one this skill wrote, say so plainly and recommend a new,
   empty plugin repository, so their existing one keeps working as it is. If no, or for a new one, **create it next
   to the source repository, never inside it.** Recommend: "I
   recommend I create it for you on GitHub as **private**: these skills are your company's work, and
   private means only people you add can install them."
3. **Name the plugin repository: its own question, never folded into another.** Ask: "What's your
   company called? Your teammates see the plugin repository's name when they add it to Claude." Never
   take a name from their GitHub account, their computer or a folder without asking. Suggest their
   answer with `-plugins` on the end and ask them to keep it or type their own: "I'll call it
   **acme-plugins**. Keep that name, or type another?" Keep it clearly different from the plugin
   names to come (`acme-plugins` holds `sales-team-skills`). It's lowercase with hyphens; convert
   whatever they say into that form. With their OK, run
   `gh repo create <name> --private --clone --description "<company>'s Claude plugins, released from <source folder name>."`
   **in the source repository's parent folder**. If `gh` isn't installed or signed in, ask them to
   create an empty private repository with that name on github.com (no README, no license) and paste
   its web address here; then run `git clone <address>` in the source repository's parent folder
   yourself.

Run `setup --plugin-repo <plugin folder> --source <source folder>`. It refuses two folders that are
the same or one inside the other, and a source with no skills or agents; if it does, say what's
wrong in one line and fix it with the user. It records the owner from the name Git uses on this
computer; add `--owner "<their name>"` if that's empty or not them. A new plugin repository starts on
a branch called `main`, like the source. Continue to Phase 2.

#### Phase 2 — Decide what goes into each plugin

**The plugins.** Say: "A plugin is a bundle of your skills and agents that a teammate installs in one
step." If there are none yet, ask three questions, one at a time, each confirmed before the next.
Never fill in an answer for them, and never offer a rename only through "Other".
1. "Who should get these? One plugin for your whole team is the simple start; separate plugins make
   sense when different teams need different skills."
2. **The plugin's name**, from their answer: "I'll call it **sales-team-skills**. Your teammates see
   this name in Claude. Keep it, or type another?" Lowercase with hyphens; convert what they say.
3. **Its description**, one sentence a teammate reads before installing: "I'll describe it as:
   'Meeting, proposal and research skills for the sales team.' Keep it, or change it?"

Then run `add-plugin --plugin-repo <plugin folder> --name <name> --description "<sentence>"`.

**The release plan.** Run `check`. Before asking anything, fix what it reports that isn't a choice:

- `RENAME`: a skill or agent folder whose name has spaces or capitals can't be released. Offer to
  rename it in the source repository ("Call Notes" → `call-notes`); with their OK, rename the folder
  and the `name:` in its `SKILL.md`, then commit and push the rename in the source repository
  (their OK to rename covers this; don't ask again in Phase 3).
- `EMPTY`: a skill whose `SKILL.md` has no name isn't finished. Say so and leave it out until it is.

Then for the `UNDECIDED` skills and agents, ask the user to choose, one plugin or "kept just for you"
for each. **Who gets what is their decision: never mark a choice as recommended and never preselect
sharing.** You may point out what each one does, in a few words, to help them choose:

"Which of these should your team get, and which are just for you?
- meeting-recap: turns meeting notes into a three-bullet recap
- proposal-writer: drafts proposals in your format
- ingest: loads files into this folder
For each: **sales-team-skills**, or **kept just for you**?"

"Kept just for you" never deletes anything: it stays in the source repository and simply isn't
released. Record each answer with `assign <plugin|none> <skill|agent> <name>` (`none` means kept
just for you); a skill can go into more than one plugin.

Later changes: "add X to the sales plugin" is `assign sales-team-skills skill X`; "stop sharing Y"
is `unassign <plugin> skill Y` for each plugin it's in, then `assign none skill Y`, without asking
again. Say it in plain words: "Taking [skill] out of [plugin]. It stays in your source repository."
Then say that taking something out of a plugin makes that plugin's next release a major one,
because anyone who used it will notice it's gone. Never narrate your own checks ("that's the removal
you asked for"): say what's happening to their skill.

#### Phase 3 — Check everything is ready

Run `check`. **If it exits 3, act on that alone.** Something that would be shared looks like a
password or key. Each finding is a file name, or a file and line number (`file:12`). Never offer to
commit anything until it's resolved, and never move a skill's `SKILL.md`.
- **A whole file** (like `.env` or `credentials.json`): say "[file] in [skill] looks like a password
  or key, so I won't share it. I'll move it out of the skill folder to a folder next to your source
  repository." With their OK, move it.
- **A line in a file:** read that line yourself, without repeating the value in full. If it's a real
  key, say "Line [n] of [file] in [skill] holds what looks like a real key. I'll take it out of the
  skill; keys belong in your connectors or settings, not in a shared skill." With their OK, remove it.
  If it's a made-up example, say "Line [n] of [file] has an example key that looks real enough to stop
  the release. I'll shorten it to [a shortened form, such as xoxb-…]." With their OK, edit it.
- Then commit and push the change in the source repository, and run `check` again. To tell whether
  a real key was ever shared, check the file's history in the source repository
  (`git -C <source> log --oneline -- <file>`): if it was committed before and the source repository
  is on GitHub, assume it was shared and add: "Change that key where you got it, because it's
  been shared."

Otherwise act on what it reports, one item at a time:

- **UNPUSHED:** a release was saved on this computer but never reached GitHub (an earlier send
  failed). Send it now with `git -C <plugin folder> push` (or `push -u origin HEAD` with no
  upstream), then run `check` again. If it fails again, say what went wrong in plain words and stop.
- **RENAME, EMPTY, UNDECIDED:** back to Phase 2 for those items. Nothing undecided is shared.
- **MISSING** and **ONLY IN PLUGIN** mean this release would remove something from a plugin.
  - **They just asked to stop sharing it** (Phase 2): that's their approval. Don't ask again.
  - **It's no longer in the source repository** (deleted or renamed): if it's there under another
    name, add that to the plan with `assign`. Otherwise ask once: "[name] is in your [plugin] plugin
    but no longer in your source repository, so this release removes it, and anyone who uses it
    will notice. Remove it?" With their OK, `unassign` any MISSING line.
  - **It's in the plugin but was never in the release plan** (the plugin was started some other
    way): if it's in the source, ask whether it should stay in the plugin and `assign` it if so;
    if not, ask as above.
  When the only things `check` still reports are removals they approved, go on to Phase 4. The
  plugin's release is a major one.
- **The source has changes not yet committed.** Leaders often answer "I did save" here; they mean
  the file. Say: "Your changes to [skill] aren't committed and pushed to [source folder] yet. Only
  committed work is released, so your team gets exactly what's on GitHub. Shall I commit and push
  them now?" With their OK, commit them in the source repository with a message that says what
  changed, push, and run `check` again so the release names that version. If they say no, stop.
- **SOURCE UNPUSHED:** the source version is committed but not on GitHub. Say: "Your latest change
  to [source folder] ([what the commit changed]) is committed but not pushed to GitHub yet. Every
  release names the source version it came from, so that version has to be on GitHub. Shall I push
  it now?" The only choices are **push it now** or **stop**: never offer to release without pushing.
  With their OK, `git -C <source> push` (or `push -u origin HEAD` with no upstream), then run
  `check` again. If the push fails, say what went wrong in plain words and stop.
- **NOTE ... no GitHub connection:** the source repository isn't on GitHub. Say: "Your source
  repository isn't on GitHub yet, so nobody else can see the version a release came from." Offer to
  put it on GitHub as a private repository (`gh repo create <name> --private --source <source> --push`)
  before releasing.
- **The plugin repository has changes made by hand.** Name each file and say what you recommend:
  "Someone changed README.md in your plugin repository directly. Your plugin repository should only
  change through publishing. I recommend I undo that change; if it's something you want to keep,
  tell me and we'll make it part of this release." To undo a changed file, run
  `git -C <plugin> checkout -- <file>`. A new file (marked `??`) can't be undone that way: with
  their OK, move it out of the plugin repository to a folder next to it. Never release on top of an
  unexplained change.
- **The source repository isn't a Git repository.** Say: "Your source repository needs to be on
  GitHub so every release can say exactly what it came from." Stop, and help them set it up first.

#### Phase 4 — Copy and show what's changing

Run `copy`. It copies each plugin's skills and agents from the source repository (leaving out system
clutter like `.DS_Store`) and reports, plugin by plugin, what was added,
updated or removed, with a suggested version. Plugins with no changes aren't listed and keep their
version.

An `EMPTY PLUGIN` line means a plugin would be released with nothing in it: ask whether that's
intended before going on (usually the answer is to add skills to it in Phase 2, or not release it).

If nothing changed, say: "Your plugins already match your source repository, so there's nothing to
release." If only `release-plan.txt` changed (for example, a new skill kept just for them), commit
and push it with the message "Update release plan" so the record on GitHub stays current. Then stop.

**The description.** When a plugin's release adds or removes a skill or agent, read its description
(`list` shows it) and check it still describes what's in the plugin. If it doesn't, propose a new
sentence: "Your plugin's description still mentions brand guidelines, which this release removes.
I'll change it to: 'Meeting and news skills for the sales team.' Keep that, or change it?" With
their OK, run `describe <plugin> --description "<sentence>"`. Teammates read it before installing.

Play each plugin's changes back in plain words and recommend its version, with the reason:

| What changed in that plugin | Version | Reason to give |
|---|---|---|
| First release | 1.0.0 | "Its first release." |
| A skill or agent removed | major (2.0.0) | "Anyone who used the removed one will notice it's gone." |
| A skill or agent added | minor (1.1.0) | "Something new, nothing taken away." |
| Only changes to existing ones | patch (1.0.1) | "Improvements to what's already there." |

The biggest kind of change in a plugin wins. Ask once, naming each changed plugin with its version
and the reason: "Release sales-team-skills as version 1.0.2? It improves meeting-recap; nothing added
or taken away." The choices are **release** or **not yet**; don't add a separate question for the
number. If they ask for a different number, it must be higher than the last release; the script
refuses anything else.

#### Phase 5 — Release

On their yes:

1. Run `bump <plugin> <first|major|minor|patch|X.Y.Z>` for each plugin being released. It counts up
   from the last release, so running it twice never skips a number, and it rebuilds the marketplace
   file so the version numbers always agree.
2. **Validate** where the `claude` command is installed (`claude --version` works): run
   `claude plugin validate <plugin folder>` and `claude plugin validate <plugin folder>/plugins/<name>`
   for each released plugin. The exit code decides: only a non-zero exit stops the release. Ignore
   warnings, "passed with warnings" and notes about what the public plugin directory would require
   (such as a LICENSE file), and say nothing about them. On a failure, say what failed in plain words.
   If it's in a skill or agent, fix it in the source repository (never in the plugin repository),
   commit and push it, and start again at Phase 3. If it's in the plugin or marketplace file, stop: say the
   release can't go out and nothing was sent. If the plugin repository already has a release, undo
   this one's changes with `git -C <plugin folder> checkout -- . && git -C <plugin folder> clean -fd`;
   on a first release there's nothing to undo.
3. Run `git -C <plugin folder> status --short` and check every file is under `plugins/` or
   `.claude-plugin/`, or is `.gitignore`, `.gitattributes`, `README.md` or `release-plan.txt`. Ask before including
   anything else.
4. Commit the release in one commit: `git -C <plugin folder> add -A`, then commit with the subject
   `Release <plugin> vX.Y.Z[, <plugin> vX.Y.Z] from <source folder name>@<source commit>` (plugins in
   alphabetical order) and a body with one line per released plugin:
   `<plugin> vX.Y.Z: added …; updated …; removed …` (leave out empty parts).
5. **Tag each released plugin's version** on that commit, so every version is listed on the
   repository's Tags page on GitHub: `git -C <plugin folder> tag -a <plugin>-vX.Y.Z -m "<plugin> vX.Y.Z: <the body line>"`.
   If Git says the tag already exists, check GitHub: `git -C <plugin folder> ls-remote --tags origin <plugin>-vX.Y.Z`.
   Prints nothing: it's left over from a release that never finished, so move it to this commit by
   adding `-f`. Prints a line: that version is already on GitHub, so stop, undo this release's
   commit (`git -C <plugin folder> reset --soft HEAD~1`) and say the version was already released.
6. Push it to GitHub with its tags: `git -C <plugin folder> push --follow-tags`. If the folder has no
   upstream yet (`git -C <plugin folder> rev-parse --abbrev-ref @{u}` fails), use
   `git -C <plugin folder> push --follow-tags -u origin HEAD`. Push last: Claude decides an update is
   ready from what it finds on GitHub, so it must only ever find a finished release. If the push
   fails, say what went wrong in plain words and stop; never retry with force.

#### Phase 6 — Get it into Claude

Read `references/installing-and-updating.md` and give the steps for where they use Claude: on a
plugin's first release, how to add the plugin repository and install the plugin, and how to give a
teammate access; on later releases, how to get the new version. Close with: "Version [X] of
[plugin] is on GitHub. Every version is listed on your plugin repository's Tags page. Next time you
change a skill, commit and push it in **[source folder]**, then say 'publish my plugin'. Your plugin
repository is **[plugin folder]**, next to it."

## Output

- In the plugin repository: `plugins/<name>/` for each plugin (its `.claude-plugin/plugin.json`,
  `skills/`, `agents/`), `.claude-plugin/marketplace.json`, `release-plan.txt`, `README.md`, and one
  commit per release, tagged `<plugin>-vX.Y.Z`, pushed to GitHub.
- A `.publish-plugin` settings file in the plugin repository, kept out of GitHub.
- The source repository changes only when the user agrees: committing and pushing their own edits,
  or renaming a folder that can't be released.

## Guidelines

- **Nothing is shared without a decision.** Every skill and agent is assigned to a plugin, or kept
  just for the user, before it can ship. The release plan is the record of who gets what.
- **Only committed and pushed versions are shared.** The release names the source version it came
  from, and that version is on GitHub, so anyone can trace a plugin version back to exactly what was
  shared.
- **One release, one commit.** Each released plugin gets a higher version number; the marketplace
  file is rebuilt from the plugins, never edited by hand.
- **Never force-push and never rewrite the plugin repository's history.** Teammates install from it.
- **The user approves the names, the description, who gets what, the versions and the release.** Ask
  each as its own question. Everything else is yours to do, including finding folders and running
  every command.
- **Plain words.** Say "commit" (save a version in the repository's history) and "push" (send it to
  GitHub); the course teaches both. Never "clone", "upstream" or a path in a question. Name the real
  skill, plugin and folder, never "it". Never narrate the script's checks; say what is happening to
  their skills.
- **Skills and agents only.** A skill is a folder holding `SKILL.md`; an agent is a `.md` file at
  the top of the agents folder. Nothing else in the source repository is ever copied.
- `references/installing-and-updating.md`: read at Phase 6.
- `references/by-hand.md`: read when `bash` won't run but `git` does, or the script reports an error
  you can't resolve.
