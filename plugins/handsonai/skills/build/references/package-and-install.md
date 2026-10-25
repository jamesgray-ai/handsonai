# Part 3: package, install, keep a copy

Read at Part 3, and whenever a fix or a live change installs. Nothing is packaged or installed while a task waits or has `Failed check`; a task `Built, misses [line]` is packaged with the rest, and a schedule-only request holds nothing up.

**Contents:** 1. Package · 2. Install · 3. Fingerprints · 4. Keep a copy · 5. What's still waiting · 6. Finish the record and the registry

## 1. Package

By the plan's `packaging`:
- **Standalone Skill:** each skill saved on its own, in the form the platform takes.
- **Plugin:** one plugin, with nothing from the record in it. On Claude it's uploaded as a .zip (Customize, then Plugins, then Upload plugin); no marketplace. On Microsoft 365 a Claude plugin .zip is converted on upload. Use the platform's own plugin builder where one exists; never hand-zip a plugin there.
- **Workspace Agent** (ChatGPT, guided): an instruction document for what the leader creates in the platform's interface, from your skills and the plan's configuration. It carries everything in `carried-lines.md` and sets every write action to "Always ask". Until release check 18 passes, its protection is the instruction only, said in N-B21.
- **Loose Files:** written to their places.
- **Codex, until release check 8 passes** (skill loading across the CLI, the desktop app and the IDE extension): whatever the plan's `packaging`, install standalone skills in `.agents/skills/`, never a plugin, and name in the close the surfaces where they load. Record the change from the plan's packaging as a ruling ("what, why, cost if wrong").

**Who makes it, and where the kept copy goes.** `package/` is always in the workflow's framework folder (`Framework/[workflow-slug]/package/` in a drive). The leader's steps here count in N-B4's [K].

| Platform | Who makes it | How it reaches the platform | The kept copy | The leader's steps |
|---|---|---|---|---|
| Claude (web, desktop) | You stage each part's text in `package/` as it's checked; for a plugin, you make the .zip with the platform's plugin builder | Skills: Claude's creator saves the staged text into the account. A plugin: the leader uploads the .zip | `package/`, written through the drive connection (web) or locally (desktop); where the connection can't write a binary .zip, the leader downloads it from the chat and saves it there | Confirm the skills appear; for a plugin, download (where needed), upload and confirm |
| ChatGPT | You make each skill's .zip in the chat; for a Workspace Agent, the instruction document | The leader uploads each .zip under Skills, or creates the agent from the document | `package/`, through the drive connection; a binary .zip the connection can't write, the leader downloads and saves there | Download, upload (or create the agent) and confirm |
| Claude Code, Codex | You write the skill folders, or the plugin | You install at the workspace's own location for the plan's packaging | The installed folder, under Git where the workspace is a repository | None beyond the read-back |
| Microsoft 365 | You stage each skill's text, and each agent's build prompt, in `package/` as it's checked | Skills: Copilot's creator saves the staged text into Cowork's skills folder; a Claude plugin .zip is converted on upload. An agent: Agent Builder's own chat makes it from the build prompt the leader pastes (`microsoft-365-agent.md`) | `package/` in `Framework/[workflow-slug]/` in OneDrive (for an agent, its build and fix prompts) | Confirm the skills appear; for each agent, the Agent Builder steps |
| Print-to-save | You give the text of each part | The leader saves each part, with your steps | The leader keeps the files with the build record (N-F6) | Save and confirm |

Then:
- **A first build** is packaged without asking. On a rebuild with an Organizational lens, ask first: **Ask:** "If teammates already have this workflow, they'll need the new version. Ready to share it?"
- **One copy of each skill** is kept: staged or installed, never both.
- **The archive check:** list the package (`unzip -l`); confirm it isn't empty, holds each skill's `SKILL.md` and each agent's file, and holds no record file (`requirements.md`, `design-plan.md`, `build-record.md`, `test-results.md`, `inputs/`, `context/`, `history/`). Delete a bad archive and its temporary files before trying again.
- **A plugin's version** rises on each rebuild.

## 2. Install

Every part still in `package/` (on Claude and Microsoft 365 always; on every platform when the workflow is live, and for a shared skill; on a Claude Code or Codex first build, any part still there, such as one finished `Built, misses [line]`) is saved together, already checked, one part after another in one pass with nothing else between them (on Microsoft 365 the skills first, then each agent). The creator (on Claude Code and Codex, you) saves the staged text as it is; it never makes the part again from the blueprint. Then re-run the built-text check (`carried-lines.md` section 7) on what was saved, and fix any gap before going on.

**The leader's install line,** said exactly, then "Do you see…?":
- One skill: **Ask:** "[Exact steps.] Do you see [skill] in your skills list?"
- Several: **Ask:** "Save each of these [N] skills: [names]. [Steps.] Do you see all [N] in your skills list?"
- Plugin: **Ask:** "[Steps to upload the zip.] Do you see [plugin] under Plugins, with its [N] skills and [M] agents?"
- Guided: **Ask:** "[Steps from the instruction document.] Open your Workspace Agent: does it list [skills]?" Your checks covered the skills you made; the part the leader creates in the interface is first run whole in Test, said in one line.

**The already-there clause.** Where you can't see the target (Claude, ChatGPT, print-to-save), for every part the record doesn't show you made (a first build, or a part new in a rebuild), open the install line with it, before the steps, whether or not the platform would show a replace prompt. It's said before anything is saved, so an "already there" holds the whole save:
- One part: "Before you save: if your skills list already has one called [skill], don't replace it; say 'already there' instead."
- Several, after the names: "Before you save: if your skills list already has one with any of these names, don't replace it; say 'already there' and its name instead."

An "already there", or a skill of the same name the creator finds, stops that part's install and counts as a yes to the older-version question: take its yes path first (`setup.md` section 6: the skill form, then a copy, since the new part would be saved over it, or a different name; `live-change.md`), then give the install line again, with the replace steps for that part or its different name. The staged parts still go in together in one pass.

**The replace steps** only for a part the record says you made (a rebuild), or one the older-version yes path cleared to go in over an older skill of the same name, with a copy kept; where the leader switched that skill off at N-B51's skill form, the steps end by switching it on again once it's replaced. When a part goes in over the older version, rewrite the older-version line in its replaced form (`build-record-template.md`).

**Claude Code and Codex:** save each staged file into the installed folder with your Write tool, one file at a time, over the old file where there is one (never `rm`, `mv` or a script, and never by asking the leader to run a command: Claude Code asks the leader to allow each write under `.claude/`, which is their save; don't ask again in chat). If the leader declines that prompt, that part stays staged in `package/`: stop, with the record showing it staged, so the next entry finishes the install (`SKILL.md`, *Resume*). Then confirm each file is where the platform reads it and that the skill appears in the skill list. On Codex, a plugin's skills don't load in the IDE extension; say so when the leader works there. Until release check 8 passes, Codex gets standalone skills in `.agents/skills/` (section 1).

**Microsoft 365:** Copilot's creator saves the staged skills into Cowork's skills folder, and the install line confirms they show. Then each agent: `microsoft-365-agent.md`.

**A session that ends partway through the install** leaves the record showing which parts are still staged (`package/…` in the Path or location column); the next entry finishes the install before anything else, saying not to run the workflow until then.

## 3. Fingerprints

Mark each row `Saved: yes` with its installed place, and record a fingerprint of each installed skill and agent (none for an agent on Microsoft 365, whose instructions you can't read back) and of each runtime context copy you can read back: `sha256:` and the hex digest of its text, or, where no code can run, its size and date.

## 4. Keep a copy

Inside the close, before its Test sentence, say where the copy is, exactly, in the form that fits:
- Where the leader downloads and saves it: "Keep a copy of what I built: [download steps for the package]. Save it with your build record, outside [platform]. You'll need it to share with teammates, to go back to this version, or when you change it later."
- Where you kept it yourself: "A copy of what I built is in [folder], with your build record."
- An agent on Microsoft 365, whose kept copy is its build and fix prompts in `package/`: "The prompts that made [Agent] are in [folder], with your build record. Pasting them into Agent Builder again makes it again, close to how it is now but not word for word." Say the same in the record's "Put back the kept copy".

## 5. What's still waiting

Inputs marked `not available yet` (the D12 line in `SKILL.md`), and in the record's remaining manual steps and the close: any kind of change whose quick real check was declined or skipped (the first real run proves it); real targets not reached yet; a requirement line a task misses (`Built, misses [line]`), which Test settles; a schedule whose safety record is incomplete; any open item.

## 6. Finish the record and the registry

1. **Settings and folders** (Claude Code): lift the block with N-B21a and clear the run folders (`claude-code-block.md` section 8). Then say, in one short message of your own words, what's left in the leader's settings and how to remove each if they drop the workflow: the wrapper's allow, which stays for Test and is removed at go-live, and any allow rule the leader added during Build.
2. **"What was built" and "What it can access"** at the top of the record, keeping Test's "Live since" and "How to switch it off" lines and the older-version line (`build-record-template.md`).
3. **Set `plan_revision` and `last_close_after_round`** (the last round's number, 0 before any round). Only at a close.
4. **The registry** (`SKILL.md`, *Output*).
5. **The Git offer, then the close** (`SKILL.md`, Part 3): the close is the last message.
