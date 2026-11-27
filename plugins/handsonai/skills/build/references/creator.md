# The brief, the platform's creator, and the check before saving

Read before you build any skill or agent (Part 2, step 3), in fix mode, and for a live change. The platform builds every part with its own native way of making it; you write the brief, check what it made against the plan before anything is saved or used, and record it. You write a part yourself only where the platform has no native way to make it.

**Contents:** 1. Who builds, per platform · 2. The brief · 3. Before the creator starts · 4. While the creator works · 5. The check before saving · 6. The kept copy · 7. Saving, in Part 3 · 8. Schedules and connections

## 1. Who builds, per platform

| Platform | Skills | Agents | Where you check |
|---|---|---|---|
| Claude (desktop, web) | Claude's `skill-creator`, in this chat | Claude itself, asked in this chat to help build a custom subagent: it walks through the steps and makes a plugin to save to the account, like a skill | In the chat, before anything is saved |
| Claude Code | The skill-creator plugin when it's installed; otherwise you write the files (writing them is Claude Code's own way to make a skill) | You, asked in this session to write the subagent file (`.claude/agents/`); no plugin-dev | The files in `built/`, before first use |
| Codex | `$skill-creator`, in this session | Codex custom agents: one TOML file per agent (`name`, `description`, `developer_instructions`), made by Codex in this session from the brief. Sandbox and connections can't be set in the agent's file (they come from the session): where the plan allows no changes, switch its tools off in the file (`features.shell_tool = false`, and the other `features.*` it doesn't need). Check developers.openai.com/codex/subagents at build time: the format may change | The files in `built/` |
| ChatGPT | Its skill creator, in this chat | A Workspace Agent, from your build prompt in the agent screen (the instruction document, `package-and-install.md` section 1); the leader pastes its instructions back | In the chat; for an agent, the paste-back, before first use |
| Microsoft 365 | Copilot's creator, in Cowork | Agent Builder, from your build prompt (`microsoft-365-agent.md`, N-B52 and N-B53) | In the chat; where you can't read what it made, the leader's paste-back, before first use |

Every part gets the same two guardrails, whoever builds it: any test its builder runs is a practice run, after N-F4's Build form; and its text (instructions, tools, name and description) is checked against the plan, the practice-run lines word for word, before it's saved or used.

## 2. The brief

One brief per part, written from the plan's task and its blueprint, as one fenced block in the chat, its first line `Skill brief: [part name]` (an agent's: `Agent brief: [part name]`), then these labelled parts:

- **What it does:** one or two sentences, from the blueprint.
- **Description:** the description it's saved with (what it does and when to use it), from the blueprint.
- **Steps:** the steps in order, with each checkpoint where it stops for the person.
- **Rules:** every check, rule, limit and Never line it carries, in the requirements' wording (`carried-lines.md` section 3). A rule tagged ` · (you)` or ` · ([role])` is that person's: it's never in the brief as the AI's rule.
- **Output structure:** the output's form and structure from the requirements' `## Output`. This is its one copy: it goes into the skill itself, and `context/` keeps no copy of it.
- **Tools:** for an agent, the tools it may use, reads only where the plan allows no change.
- **Keep these exactly:** the practice-run lines, word for word (`carried-lines.md` section 2: the cue, the fixed first line, the never-made rule in every part that changes something, the given-input rule, the closing block), the outside-content and never-read lines, the `KW` lines in this platform's form, then: "Keep these lines exactly as written. Test it only under the practice-run cue: start every test with 'practice run'. Never install or save it until I say it passed."
- On Claude Code, with the skill-creator plugin: add "Use only the plugin's steps for writing the skill; never its eval or description-optimising loops." (they start sessions outside the wrapper, where nothing blocks a change).
- On Claude Code and Codex: add "Write it in `framework/[workflow-slug]/built/[part name]/`, nowhere else."

No IDs (requirement, task or line) in the brief: only the wording. The brief is the creator's whole source: never hand it the plan or the requirements files.

## 3. Before the creator starts

Once in each session that builds or checks a part, before the first brief: N-F4's Build form, where it applies (`SKILL.md`, *Phase 2*). Then hand the creator the first brief.

## 4. While the creator works

- **Its questions** are answered from the plan; the leader never sees them. A question the plan can't answer is a ruling or a change request (`SKILL.md`, step 3).
- **Its tests,** its own way of checking, are welcome, under the cue only. Before a test starts, read what it will run: a test without the cue never runs. Tell the creator in the same chat to start every test with "practice run", and only then let it go on. A test that ran without the cue anyway: say so in one line *(your words)*, naming what it showed or changed; a real change it made is listed and offered for undo with the quick real checks' changes (N-B33).
- **Nothing is saved or installed** while it works: not into the account, not where the platform loads skills or agents.

## 5. The check before saving

When the creator says the part is ready, read its final text: in the chat on Claude, ChatGPT and Microsoft 365 (where you can't read it there, ask the leader to paste it back); the files in `built/[part name]/` on Claude Code and Codex. Check it against the plan with the built-text check (`carried-lines.md` section 7): every check, rule, step and checkpoint; the output's structure; its name and description; every Never line; the practice-run lines word for word; no IDs.

- **A gap:** ask the creator, in the same chat, to fix it, quoting the missing or changed line word for word, then check again. Up to three tries in all.
- **Still missing after three tries, for a practice-run line, a Never line or a line that names a law:** the part is `Failed check`. Nothing of it is saved, and the build stops there: no other task is built after it. Never `Built, misses` for these. Say in one line *(your words)* that [the part] couldn't be made to keep [the line, in plain words], so it isn't saved, then the stop as every stop ends (`SKILL.md`, *The end of the part, and every stop*), with N-F10's form for this platform and Build's phrase last.
- **Any other line still missing after three tries:** `SKILL.md`, *A check that fails*.
- **It passed:** write the final text to the kept copy (section 6) and go on to the part's other checks (`SKILL.md`, step 5).

## 6. The kept copy

One fixed place for every part, on every platform: `framework/[workflow-slug]/built/[part name]/` in the working folder. A skill's text is `built/[skill name]/SKILL.md` (with its supporting files beside it); an agent's is its file in that folder (`built/[agent name]/[agent name].md` on Claude and Claude Code, `.toml` on Codex); a Workspace Agent's instruction document is `built/[agent name]/instructions.md`; an agent on Microsoft 365 keeps its build prompt and fix prompts there (`microsoft-365-agent.md`). On Claude, ChatGPT and Microsoft 365 you write it once the check passes, from the text the creator showed; on Claude Code and Codex the creator drafts there.

It's what Part 3 saves, what fix mode and a live change start from, and what putting back the built version reinstalls (`fix-mode.md` section 4). Before a rebuild writes over it, a live change moves the current copy into `history/kept-copy-YYYY-MM-DD-HHMM/` (`live-change.md` section 2). A folder built before this release keeps its copy in `package/` or `history/built-*/`: read it there, and write the next copy in `built/`.

## 7. Saving, in Part 3

Every part is saved together in Part 3, once every task has passed its checks (`package-and-install.md` section 2):

- **Claude and ChatGPT:** the leader saves each part from the creator's save card, after N-B12's already-there clause (said before the first save card). Ask the creator for each save card with the kept copy's text, unchanged.
- **Claude, one line:** say *(your words)* that Claude saves each skill (or agent) inside a plugin of its own, naming it, and record each plugin's name in the record's `plugins:` (Test leaves them on when it switches the others off).
- **Claude Code and Codex:** after N-B57's yes, the creator (or you, with no creator) writes each part from `built/` where the platform loads it.
- **Microsoft 365:** Copilot's creator saves the skills in Cowork's skills folder; each agent by Agent Builder (`microsoft-365-agent.md`).

Then check what was saved, where you can read it (Claude Code, Codex, Cowork's skills folder): the built-text check again, since a platform can shorten a description or drop a line as it saves. Where you can't read it, N-B12's question confirms it shows.

## 8. Schedules and connections

The platform's own scheduler and connection screens make them. Your part is the brief (what to set, in one sentence and a link to the platform's page in `platform-docs.json`) and the check that each is set as the plan says (`setup.md` section 2; `standard-tasks.md` for `SCH`).
