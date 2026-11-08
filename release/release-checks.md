# Release checks (maintainer checklist)

Not shipped in the plugin, and no skill reads it. These are the platform behaviours the framework's
skills don't rely on until someone has tried them by hand. Every skill takes the safe path written
in its own text (the **Skills do today** column) for every check here, whatever its status.

**To change what a skill does after a check passes:** run the check, record it below (status
`verified`, the date, the release, who ran it), then edit the skill text that describes the safe path
and its evals in the same pull request. Recording a pass here changes nothing on its own.

Run the open checks before each cohort release, and again when a platform's release notes change
something a check rests on. Where a version can be read (`claude --version` on Claude Code), record
the range you tested in **Verified on**.

The eval harness reads the **Status** column (`framework-evals/check_scripted.py`): an eval item
marked `release_check` grades the `open` text unless every check it names is `verified` here.
Keep the table's columns as they are.

| ID | Platforms | Check | Skills do today | Status | Verified on | Verified for release | Run by |
|---|---|---|---|---|---|---|---|
| 1 | claude-code | A deny rule added mid-session is applied | The leader restarts the session once, before Build's checking part | open |  |  |  |
| 2 | claude-code | A deny rule binds a check agent running a sub-agent's text; a check agent's `tools:` allow list refuses every unlisted tool | Those checks rely on the instruction, said in N-B21 | open |  |  |  |
| 3 | claude-code | Write and Edit limited to the session's own folder's `practice/` in a headless session (unlisted tools refused) | Write and Edit denied outright in headless sessions; the AI's runs and Build's headless checks show their files in their output | open |  |  |  |
| 4 | claude-code | Deny rules bind in every permission mode Build's own session can be in (default, accept-edits, auto, bypass) | The check sessions keep their allow lists; N-B21a's fallback sentence says only those were limited | open |  |  |  |
| 5 | claude-code | `/mcp` switches a connection off for that session only, without changing the leader's settings | No `/mcp` step in Test's hand-over; N-F4 in every Claude Code hand-over | open |  |  |  |
| 6 | claude-code | `claude -p` under a subscription login from a clean folder; what loads headless and whether `--setting-sources` and the plugin flags leave it out; `--strict-mcp-config` with claude.ai connections and env-var configs; allow-rule merging; unlisted tools refused; Test's deny rules bind; the workflow loads from `.claude/` or `--plugin-dir`; a checkpoint ends the turn and `--resume` through the wrapper keeps the settings; the wrapper refuses bypass flags | Test: the leader runs the practice inputs (N-T42). Build: check agents only, and no bare run | open |  |  |  |
| 7 | claude-code, claude | How a cloud routine, a desktop task and a Claude scheduled task treat a checkpoint: a gate the platform holds, or the instruction only | Treated as the instruction only: N-B49 before the switch-on steps (rules 5.3) | open |  |  |  |
| 8 | openai-codex | Skill loading across the CLI, the desktop app and the IDE extension | Build installs standalone skills in `.agents/skills/` and names the surfaces where they load | open |  |  |  |
| 9 | openai-codex | N-B45's command (`codex --sandbox read-only -c 'mcp_servers={}'` in a new empty folder) starts a session with no connections that can't write | No bare run on Codex | open |  |  |  |
| 10 | claude | Google Drive (Claude): moving and renaming through update_file, for the create-only path | The save check (saving.md): print-to-save where the connection can't move files | retired |  |  |  |
| 11 | claude | Microsoft 365 connection writes on work accounts, admin-enabled | The save check (saving.md): a first save that fails falls back to print-to-save; another connected service can be named instead | retired |  |  |  |
| 12 | claude | Scheduled tasks can read Project knowledge | The `SCH` task places the context where the task can read it, or the workflow runs by hand | open |  |  |  |
| 13 | claude | A new chat: connectors and memory switched off under + before the first message (the bare run; Test's run chats with only the workflow's connectors on) | No bare run on that surface; Test's hand-overs there say N-F4 whatever the workflow's own connections | open |  |  |  |
| 14 | claude | On desktop, a chat with a folder selected asks before it creates or changes a file there | The desktop hand-over's "told to save nothing there" is the only protection for that folder, said plainly; once confirmed, N-F4 covers it too | open |  |  |  |
| 15 | chatgpt | Project-only memory doesn't stop skills | Default memory, with the transcript check | open |  |  |  |
| 16 | chatgpt | A new chat in the workflow's Project with no apps added (or only the workflow's) can't reach the Project's or the account's other apps | No bare run on ChatGPT; Test's hand-overs say N-F4 whatever the workflow's own connections | open |  |  |  |
| 17 | chatgpt | How a scheduled task and a Workspace Agent's scheduled run treat a checkpoint (and a write action set to "Always ask") | Treated as the instruction only: N-B49 before the switch-on steps (rules 5.3) | open |  |  |  |
| 18 | chatgpt | A Workspace Agent's write actions can be set to "Always ask", and the built-text check can read its instruction document | The Workspace Agent's protection is the instruction only, said in N-B21 | open |  |  |  |
| 19 | chatgpt | Skills on Plus and Pro | The guided path, or skills not offered on those plans | open |  |  |  |
| 20 | chatgpt | Drive writes on Plus and Pro; Business and Enterprise write actions needing an admin | The save check (saving.md): a first save that fails falls back to print-to-save, or ask the admin | retired |  |  |  |
| 21 | microsoft-365-copilot | Agent creation. Skills: Cowork creates them. Agents: Agent Builder's own chat (Copilot › Chat › Agents › New agent) builds one from a build prompt naming the plan's task, `design-plan.md`, `requirements.md` and their OneDrive folder, asking nothing they answer; Copilot's ordinary Chat reads the files but can't create one | If a later run fails: N-B52's recovery form for a leader in the ordinary chat; where Agent Builder can't build from the files, a change request (N-B9), and Design re-plans the agent's work as Cowork skills | verified | 2026-10-21 (skills), 2026-10-24 (agents); James's tests | 10.0 |  |
| 22 | microsoft-365-copilot | Creating files in a separate OneDrive folder; editing Markdown in place | If a later run fails: the create-only path in that folder if Cowork can create and move files there; print-to-save otherwise | verified | 2026-10-21; James's test | 10.0 |  |
| 23 | microsoft-365-copilot | A new Cowork chat, with nothing attached, reads and updates the files in the working folder from the location alone | If a later run fails: N-F13's Microsoft 365 form, as at any chat that can't read the files | verified | 2026-10-21; James's test | 10.0 |  |
| 24 | microsoft-365-copilot | Cowork asks before each connector write in an attended chat | Build's checks rely on the instruction only, said in N-B21 | open |  |  |  |
| 25 | microsoft-365-copilot | Connections off per session | No bare run; Test's hand-overs give no switch-off step (N-F4 is said in every one there anyway) | open |  |  |  |
| 26 | microsoft-365-copilot | How unattended runs handle approvals: a gate that stops at a checkpoint, or not | Treated as the instruction only: N-B49 before the switch-on steps (rules 5.3) | open |  |  |  |
| 27 | microsoft-365-copilot | A workflow reads its own run log in Cowork's folder | No run log, no re-check line, no time saved | open |  |  |  |
| 28 | microsoft-365-copilot | A Cowork skill can be added under an agent's Skills | Design keeps everything an agent needs in its own instructions, and no skill starts an agent (design 5.4) | open |  |  |  |
| 29 | microsoft-365-copilot | Agent Builder's chat changes an existing agent from a fix prompt (the agent opened with Edit) | N-B53's rebuild form: a new agent from the build prompt with the fix in it; the leader deletes the old one once the new one shows; either way, Test's after-fix round re-runs every input that uses the agent | open |  |  |  |
| 30 | microsoft-365-copilot | An Agent Builder agent, with a Work content source on, can't send, post or change anything, or asks before it does | N-T8's protection clause in every agent hand-over, whatever the workflow's own connections; a write the plan routes through an agent counts as resting on the instruction, said in N-B21 | open |  |  |  |
| 31 | microsoft-365-copilot | Agent Builder keeps the lines a build prompt quotes word for word in the agent's instructions (the practice-run first line, the never-made rule, the closing block's label, the flag line) | The paste-back: after Create and each fix the leader pastes the agent's instructions, Build checks them, and a gap gets a fix prompt before any test run (N-B52 step 6, N-B53); a gap still there after three tries: `Failed check`, the leader asked to delete the agent (N-B54, 3c-DI), a change request (N-B9), and Design re-plans the agent's work as Cowork skills, with no Test round on the agent meanwhile | open |  |  |  |
| 32 | microsoft-365-copilot | A Cowork skill, in a new chat with nothing attached, reads a context file in OneDrive at the place written into it | Each run chat attaches the workflow's context files from the workflow's own folder in Cowork's folder (N-T8's attach clause) | open |  |  |  |
| 33 | microsoft-365-copilot, chatgpt | The button that refuses an action in Microsoft 365 Copilot Cowork and in ChatGPT is labelled "Deny", as N-F4 says (3c-DJ) | N-F4 names that platform's own label, from this registry's `approval_labels.refuse` | retired |  |  |  |
| 34 | claude | Claude desktop: desktop_add_folder ('Work in a folder' in the chat bar) still matches the app | Say the exact steps couldn't be verified; the leader selects the folder their own way | retired |  |  |  |
| 35 | microsoft-365-copilot | An Agent Builder agent can run on a schedule | Plan scheduled work as Cowork skills run by a scheduled prompt, never an Agent Builder agent | open |  |  |  |

## Retired checks

- **10:** retired 2026-11-07: skills no longer look up storage behaviour; they read every save back (the save rule in `references/saving.md`).
- **11:** retired 2026-11-07: as 10.
- **20:** retired 2026-11-07: as 10.
- **33:** retired 2026-11-07: skills no longer carry a platform's button labels; N-F4 tells the leader to refuse the action with the platform's own refuse button, by its function, not a stored label.
- **34:** retired 2026-11-07: skills no longer carry a menu path for selecting a folder on Claude desktop; the fail-safe rule (never make up a menu path; say so and let the leader find it, with the Claude docs link) is the behaviour.
