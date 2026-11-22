# Part 3: package, install, keep a copy

Read at Part 3, and whenever a fix or a live change installs. Nothing is packaged or installed while a task waits or has `Failed check`; a task `Built, misses [line]` is packaged with the rest (N-B57 then takes its with-a-miss form, section 2), and a schedule-only request holds nothing up.

**Contents:** 1. Package · 2. Install · 3. Fingerprints · 4. Keep a copy · 5. What's still waiting · 6. Finish the record and the registry

## 1. Package

By the plan's `packaging`:
- **Standalone Skill:** each skill saved on its own, in the form the platform takes.
- **Plugin:** one plugin, with nothing from the record in it. On Claude it's uploaded as a .zip (Customize, then Plugins, then Add, then Upload plugin); no marketplace. Plugins need a paid Claude plan (Pro, Max, Ultra, Team or Enterprise), said for those plans by name, never as the leader's. Its skills work in a Claude chat, but its agents run only in Cowork (and Claude Code), never in a chat on the web or desktop: the install line may count the agents, and nothing you say implies they run in a chat. A plan that puts worker agents in a workflow run in a Claude chat can't run as planned: a change request (N-B9). On Microsoft 365 a Claude plugin .zip is converted on upload. Use the platform's own plugin builder where one exists; never hand-zip a plugin there.
- **Workspace Agent** (ChatGPT, guided): an instruction document for what the leader creates in the platform's interface, from your skills and the plan's configuration. It carries everything in `carried-lines.md` and sets every write action to "Always ask". Until release check 18 passes, its protection is the instruction only, said in N-B21 (`SKILL.md`).
- **Loose Files:** written to their places.
- **Codex, until release check 8 passes** (skill loading across the CLI, the desktop app and the IDE extension): whatever the plan's `packaging`, install standalone skills in `.agents/skills/`, never a plugin, and name in the close the surfaces where they load. Record the change from the plan's packaging as a ruling ("what, why, cost if wrong").

**Who makes it, and where the kept copy goes.** `package/` is always in the workflow's framework folder (`framework/[workflow-slug]/package/` in the working folder). The leader's steps here count in N-B4's [K].

| Platform | Who makes it | How it reaches the platform | The kept copy | The leader's steps |
|---|---|---|---|---|
| Claude (web, desktop) | You stage each part's text in `package/` as it's checked; for a plugin, you make the .zip with the platform's plugin builder | Skills: Claude's creator saves the staged text into the account. A plugin: the leader uploads the .zip | `package/`, written through the drive connection (web) or locally (desktop); where the connection can't write a binary .zip, the leader downloads it from the chat and saves it there | Confirm the skills appear; for a plugin, download (where needed), upload and confirm |
| ChatGPT | You make each skill's .zip in the chat; for a Workspace Agent, the instruction document | The leader uploads each skill (Plugins, then the Skills tab, then Create, then Upload from your computer), or creates the agent from the document. Skills are on the Business, Enterprise, Healthcare and Edu plans only (not Free, Plus or Pro), and an admin can withhold skill uploading; Workspace Agents on Business and Enterprise only, off on Enterprise until an admin turns them on. A leader on another plan, or without the option, is told so plainly in one line, never sent to a menu they don't have; nothing is installed, the parts stay staged, and it's a change request (N-B9) | `package/`, through the drive connection; a binary .zip the connection can't write, the leader downloads and saves there | Download, upload (or create the agent) and confirm |
| Claude Code, Codex | You write the skill folders, or the plugin | You install at the workspace's own location for the plan's packaging | `history/built-YYYY-MM-DD-HHMM/`, a copy you write of each staged part from `package/` at Part 3, before the first part is installed (a Git commit, when the leader takes the Git offer, is extra) | None beyond the read-back |
| Microsoft 365 | You stage each skill's text, and each agent's build prompt, in `package/` as it's checked | Skills: Copilot's creator saves the staged text into Cowork's skills folder; a Claude plugin .zip is converted on upload. An agent: Agent Builder's own chat makes it from the build prompt the leader pastes (`microsoft-365-agent.md`) | `package/` in `ai-workspace/framework/[workflow-slug]/` in OneDrive (for an agent, its build and fix prompts) | Confirm the skills appear; for each agent, the Agent Builder steps |
| Print-to-save | You give the text of each part | The leader saves each part, with your steps | The leader keeps the files with the build record (N-F6) | Save and confirm |

Then:
- **A first build** is packaged without asking. On a rebuild with an Organizational lens, ask first: **Ask:** "If teammates already have this workflow, they'll need the new version. Ready to share it?"
- **One loadable copy of each skill:** staged or installed, never both. The built copy in `history/` (Claude Code, Codex) sits where no platform loads skills, so it never counts as a second copy.
- **The archive check:** list the package (`unzip -l`); confirm it isn't empty, holds each skill's `SKILL.md` and each agent's file, and holds no record file (`requirements.md`, `design-plan.md`, `build-record.md`, `test-results.md`, `inputs/`, `context/`, `history/`). Delete a bad archive and its temporary files before trying again.
- **A plugin's version** rises on each rebuild.

## 2. Install

Every part in `package/` is saved together, already checked, one part after another in one pass with nothing else between them (on Microsoft 365 the skills first, then each agent). The creator (on Claude Code and Codex, you) saves the staged text as it is; it never makes the part again from the blueprint. Then re-run the built-text check (`carried-lines.md` section 7) on what was saved, and fix any gap before going on.

**The leader's install line** (N-B12), said exactly, then "Do you see…?":
- One skill: **Ask:** "[Exact steps.] Do you see [skill] in your skills list?" (N-B12)
- Several: **Ask:** "Save each of these [N] skills: [names]. [Steps.] Do you see all [N] in your skills list?"
- Plugin: **Ask:** "[Steps to upload the zip.] Do you see [plugin] under Plugins, with its [N] skills and [M] agents?"
- Guided: **Ask:** "[Steps from the instruction document.] Open your Workspace Agent: does it list [skills]?" Your checks covered the skills you made; the part the leader creates in the interface is first run whole in Test, said in one line.

**The already-there clause** (N-B12). Where you can't see the target (Claude, ChatGPT, print-to-save), for every part the record doesn't show you made (a first build, or a part new in a rebuild), open the install line with it, before the steps, whether or not the platform would show a replace prompt. It's said before anything is saved, so an "already there" holds the whole save:
- One part: "Before you save: if your skills list already has one called [skill], don't replace it; say 'already there' instead."
- Several, after the names: "Before you save: if your skills list already has one with any of these names, don't replace it; say 'already there' and its name instead."

An "already there", or a skill of the same name the creator finds, stops that part's install and counts as a yes to the older-version question: take its yes path first (`setup.md` section 6: the skill form, then a copy, since the new part would be saved over it, or a different name; `live-change.md`), then give the install line again, with the replace steps for that part or its different name. The staged parts still go in together in one pass.

**The replace steps** only for a part the record says you made (a rebuild), or one the older-version yes path cleared to go in over an older skill of the same name, with a copy kept; where the leader switched that skill off at N-B51's skill form, the steps end by switching it on again once it's replaced. When a part goes in over the older version, rewrite the older-version line in its replaced form (`build-record-template.md`).

**Claude Code and Codex:** before anything is saved, **Ask:** "Everything is built and checked. I'll now save [N] parts where [platform] starts them: [names]. OK to go ahead?" (N-B57; [N] and [names] count every part in `package/`). That form is for a package whose every row passed its check. When a row is `Built, misses [line]`, "Everything is built and checked" alone isn't true, so its with-a-miss form is said instead, exactly: "Everything is built and checked, apart from [the miss, in plain words]. I'll now save [N] parts where [platform] starts them: [names]. OK to go ahead?" ([the miss] names each line a part misses, as its progress line said it; N-B57's with-a-miss form). A no: nothing is saved; the parts stay staged and the record shows them so, and you stop with N-F10. On a yes, before the first part is installed, copy each staged part's files from `package/` into `history/built-YYYY-MM-DD-HHMM/` with your Write tool, so the version you built can always be put back, with or without Git, even when the install stops partway. Then save each staged file into the installed folder with your Write tool, one file at a time, over the old file where there is one (never `rm`, `mv` or a script, and never by asking the leader to run a command). Claude Code may also ask the leader to allow each write under `.claude/` (not in bypass mode, and Codex never does): that prompt is expected after N-B57's yes; don't ask again in chat. If the leader declines that prompt, that part and every part after it stay staged in `package/`: stop, with the record showing them staged, so the next entry finishes the install (`SKILL.md`, *Resume*). The parts saved before it are installed, so the stop's message says, in one line (model wording) before N-F10, that the workflow is only partly installed and isn't to be run until the install is finished; then N-F10, last. Otherwise confirm each file is where the platform reads it and that the skill appears in the skill list. A part changed after the install (a gap the built-text check found) is copied into `history/built-…/` again, so the built copy always matches what was installed. On Codex, a plugin's skills don't load in the IDE extension; say so when the leader works there. Until release check 8 passes, Codex gets standalone skills in `.agents/skills/` (section 1).

**Microsoft 365:** Copilot's creator saves the staged skills into Cowork's skills folder, and the install line confirms they show. Then each agent: `microsoft-365-agent.md`.

**A session that ends partway through the install** leaves the record showing which parts are still staged (`package/…` in the Path or location column); the next entry finishes the install before anything else, saying not to run the workflow until then.

## 3. Fingerprints

In one Edit of the record after the last install, mark each row `Saved: yes` with its installed place, and record a fingerprint of each installed skill and agent (none for an agent on Microsoft 365, whose instructions you can't read back) and of each runtime context copy you can read back: `sha256:` and the hex digest of its text, or, where no code can run, its size and date.

## 4. Keep a copy

Inside the close, before its Test sentence, say where the copy is (N-B37), exactly, in the form that fits:
- Where the leader downloads and saves it: "Keep a copy of what I built: [download steps for the package]. Save it with your build record, outside [platform]. You'll need it to share with teammates, to go back to this version, or when you change it later."
- Where you kept it yourself: "A copy of what I built is in [folder], with your build record."
- An agent on Microsoft 365, whose kept copy is its build and fix prompts in `package/`: "The prompts that made [Agent] are in [folder], with your build record. Pasting them into Agent Builder again makes it again, close to how it is now but not word for word." Say the same in the record's "Put back the kept copy".

## 5. What's still waiting

Inputs marked `not available yet` (the D12 line in `SKILL.md`), and in the record's remaining manual steps and the close: any kind of change whose quick real check was declined or skipped (the first real run proves it); real targets not reached yet; a requirement line a task misses (`Built, misses [line]`), which Test settles; a schedule whose safety record is incomplete; any open item.

## 6. Finish the record and the registry

Steps 1 to 4 make no text between their tool calls: no line on what you're writing, saving, lifting or recording. Your only text is step 1's own (N-B21a and the settings message), then the Git offer and the close.

1. **Settings and folders** (Claude Code): lift the block with N-B21a and clear the run folders (`claude-code-block.md` section 8). Then say, in one short message of your own words, what's left in the leader's settings and how to remove each if they drop the workflow: the wrapper's allow and the rules protecting its folder, which stay for Test and are removed at go-live, and any allow rule the leader added during Build.
2. **"What was built" and "What it can access"** at the top of the record, written with step 3's values and the lift's `write_block: off` in one Write of the whole record, keeping Test's "Live since" and "How to switch it off" lines and the older-version line (`build-record-template.md`).
3. **Set `plan_revision` and `last_close_after_round`** (the last round's number, 0 before any round). Only at a close.
4. **The registry** (`SKILL.md`, *Output*).
5. **The Git offer, then the close** (`SKILL.md`, Part 3): the close is the last message.

## The Git offer

**The Git offer,** only when the workflow folder is in a Git repository (with a shell, `git rev-parse --show-toplevel` returns the workspace; never on the web or in a drive), once, while finishing the record, just before the close. In a cloud session: no offer; commit, push and N-F18, as `references/routing-rare.md` says. Elsewhere: **Ask:** "Your folder keeps a history of its changes (it's a Git repository). Want me to save this point in that history, so you can come back to it later? It stays on your computer — nothing is shared." On a yes, commit locally and never push (for a cloud routine, pushing is the leader's own step in the switch-on steps). Stage exactly the framework's own paths and the built workflow, by name: `framework/[slug]/` (its `history/` and `package/` included), `framework/.bin/` where you wrote the wrapper, `registry/` where it's in the repository, and each installed part and runtime context copy the record lists; never `git add -A`, `-a` or `.`, never a `practice*/` folder, `.claude/settings.local.json`, an `.env` or key file, or anything else, and leave the leader's other changes as they were. Never at a stop.

## The close

**The close** (N-B13), your last message, said exactly: "Your workflow is built and checked. Here's what you have: [What was built, in plain words: each part and what it does, where it lives, how to start it, what's still waiting]. What it can access is written up in your build record, if anyone asks. [Rulings that matter.] [N-B37.] [Print-to-save: 'Save the files below.'][ First build, full track: 'Two or three test rounds is normal.'] [The Test sentence.]" (N-B13) A part the leader made in the platform's interface, which you couldn't run (a Workspace Agent, an agent on Microsoft 365), is named as first run in Test. The rounds bracket is never filled now: Test's opening says it to every leader (James, 2026-11-21), so the close leaves it out on every build. On a live workflow, N-B38 (`references/live-change.md`) takes the place of the Test sentence and the rounds sentence. The Test sentence, by platform:
- Claude on the web and ChatGPT: "Start Test in a new chat outside your workflow's Project. Add your [storage service] to it, then say 'test the workflow I built. My files are in [location].'"
- Claude desktop with the files in a local folder: "Start Test in a new chat with your working folder selected: 'test the workflow I built. My files are in [location].'" With the files in a drive, the web form above (N-F2).
- Microsoft 365: "Start Test in a new Cowork chat with: 'test the workflow I built. My files are in OneDrive, in ai-workspace/framework/[workflow-slug].'"
- Claude Code and Codex: "Start Test in a new session in this project and say 'test the workflow I built.'" (on Claude Code you may add that typing `/test` and picking it from the list works too)

Every start phrase Build gives outside a scripted line gives it with the location, for a new chat, in N-F2's form for the platform ("Start [step] in a new chat. Add your [storage service] to it, then say '[start phrase]. My files are in [location].'"; Claude Code and Codex, "Start [step] in a new session in this project and say '[start phrase].'"; Claude desktop with the files in a local folder, "Start [step] in a new chat with your working folder selected: '[start phrase]. My files are in [location].'"; Microsoft 365, "Start [step] in a new Cowork chat with: '[start phrase]. My files are in OneDrive, in ai-workspace/framework/[workflow-slug].'"), and none offers to start another step in this chat. A scripted line that gives a start phrase (N-B9, the open-item stop) is said as written.

