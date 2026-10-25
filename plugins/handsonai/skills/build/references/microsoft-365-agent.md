# An agent on Microsoft 365

Read when the plan has an agent on Microsoft 365. Skills are made in Cowork by Copilot's creator, like any skill. An agent is made by Agent Builder's own chat in Copilot's Chat tab (Copilot › Chat › Agents › New agent), from a build prompt you write and the leader pastes, never in Cowork and never in Copilot's ordinary chat, which can describe an agent but can't make one. Agent Builder reads the plan and the requirements itself, so you don't draft the agent's text or hand it a blueprint. The prompts are the one place a task ID reaches the leader's screen, since Agent Builder reads the plan by it; they're text the leader pastes, not lines said to them.

**Contents:** 1. The build prompt · 2. Making the agent (Part 3) · 3. The paste-back check · 4. Three tries, then delete · 5. A fix, or a task rebuilt from a changed plan · 6. Putting it back, and live changes · 7. Release checks this rests on

## 1. The build prompt

At the agent's task in Part 2, write the prompt from this template, said word for word with only the brackets filled, and stage it in `package/[agent-name]-build-prompt.md`:

"Build the agent described in task [task ID] of design-plan.md, using the requirements in requirements.md. Both files are in my OneDrive, in Framework/[workflow-slug]. Everything you need is in those files, so don't ask me anything they already answer. The agent reads only [each context file, by its place in OneDrive], and connects to [its connections / nothing else]. Its instructions must also include these lines, word for word: [the lines 6.3 names from 6.4]."

With no context file, its fourth sentence is: "The agent reads no files, and connects to [its connections / nothing]."

Fill it from the plan, exactly: the agent's task ID; the workflow's folder; exactly the context files the agent reads, each by its runtime copy's place (`Documents/Cowork/[workflow-slug]/[file]`, never the steps' copy in `Framework/[workflow-slug]/context/`), and nothing else; exactly its connections, as the blueprint's *Tools* line writes them, and nothing else. Copy each fill as it stands, adding and rewording nothing: a context file is its place alone, with no "in my OneDrive" after it (the sentence before already says where); a connection is the *Tools* entry with its brackets, never reworded into a clause ("Outlook (create drafts)", not "Outlook, to create drafts only"); and, word for word, the lines `carried-lines.md` section 6 lists. The plan's blueprint already gives the name, description, rules, checkpoints and "What I did" list. The leader never copies a name, description or instructions into the form. Until release check 28 passes, the agent's blueprint holds everything it needs, so add no skill to it. The prompt is your own text, quote-checked like any scripted line; the agent's *Done when* practice runs are Test's first run of it.

## 2. Making the agent (Part 3)

Once for each agent, after any skills are saved. Numbered steps, each said as written:

"[Agent] is made in Copilot's Agent Builder, not here in Cowork: 1. Open Copilot, choose Chat, then Agents, then New agent. 2. Paste this into the Message Agent Builder box:" ("here in Cowork", never "here in Copilot Cowork")

then the build prompt, in a block to copy, then:

"3. Under Knowledge, add [file] from your OneDrive, in Documents/Cowork/[workflow-slug], if it isn't listed yet. Add it from there, not through Agent Builder's offer to attach it, which may pick the copy in your Framework folder. If Agent Builder asks you anything[ else], paste its question here. 4. Before you choose Create, check that Knowledge lists only [the context files / nothing], and remove anything else. Then open Work content and check that only [what the workflow uses / nothing] is switched on; switch off anything else, and tell me if something won't switch off. 5. Choose Create. 6. When [Agent] shows under Agents, open it, choose Edit, copy everything under Instructions, and paste it here, so I can check it kept the lines it must carry."

- With no context file, step 3 is only "If Agent Builder asks you anything, paste its question here." ("else" only follows the Knowledge sentences).
- The Knowledge step is said for every context file, whatever Agent Builder reports: a file it finds by path isn't proved to reach the agent, and a file just saved is seldom indexed yet.
- A question Agent Builder asks comes back through the leader; answer it from the plan (a change request when the answer would change what is built).
- Something under Work content that won't switch off is recorded in "What it can access" as reachable.
- **A leader in Copilot's ordinary chat** (it only described the agent, or said it can't create one), said once, then the main form's steps 3 to 6: "That was Copilot's ordinary chat, which can describe an agent but can't make one. Go back to step 1: open Copilot, choose Chat, then Agents, then New agent, and paste the same text into the Message Agent Builder box."
- No install line for an agent: step 6 takes its place. No fingerprint is recorded for it, so N-E1's agent form is asked before any later rebuild.

## 3. The paste-back check

Run the built-text check (`carried-lines.md` section 7) on the instructions the leader pastes back, and keep the pasted text in the record ("Also": the instructions the leader last pasted back), for fix mode and a rebuild.

- **Your own prompt pasted back.** A paste holding a build or fix prompt's own fixed sentences ("Build the agent described in task", "Its instructions must also include these lines, word for word", "Change nothing else") is the prompt still on the leader's clipboard, not the agent's instructions. Never check it; say exactly, and ask for the paste again (not counted as a try): "That's the prompt I wrote, not [Agent]'s instructions. Open [Agent], choose Edit, copy everything under Instructions, and paste it here."
- **A gap** (a carried line missing or reworded; the first line and the never-made rule above all, word for word), before any test run. To show the leader a line the agent reworded, block-quote the agent's wording as they pasted it, on a line of its own (it's their paste shown back), and name the line it should be in plain words; never repeat the reworded words inside your own sentence, here or later (to tell the old agent from the new one, say "the one made first"). **While release check 29 hasn't passed** (today), the rebuild path in section 5, with the build prompt carrying the missing or reworded line: one path, one paste-back request, and the gappy agent deleted only once the new one passes. **Once check 29 passes:** N-B53's opening, its fix prompt in the carried-line fill, and its check sentence (section 5), with [the change] saying in plain words what's missing or reworded and no miss sentence; for example "put back the line every practice run must start with". After its "done", one paste-back request, said exactly: "Paste [Agent]'s instructions here again, so I can check the fix." Then the check again. N-B53's own paste-back sentence isn't said on this path.
- **When the check passes,** at the first build: "[Agent] is made, and its instructions carry every line they must, so your test runs can start." (in fix mode, N-B53's done form instead). Then the next action.
- **Once release check 31 passes** (Agent Builder keeps a build prompt's lines word for word), step 6 is "6. Say 'done' when you see [Agent] under Agents.", nothing is pasted back, the check is skipped, and the done form is: "[Agent] is made. I can't read its instructions from here, so your test runs are its first check."

## 4. Three tries, then delete

Up to three tries in all. A carried line is never finished as `Built, misses [line]`: it isn't a requirement line. After the third failed try, record `Failed check` for the agent's task; in N-B9's reason say plainly that Agent Builder keeps leaving out [the line, in plain words] that every practice run needs, so the agent can't be tested safely and isn't to be used; and ask, said exactly:

"Please delete [Agent]: in Copilot, open Agents, find [Agent], and choose Delete. Say 'done' when it's gone."

On the rebuild path (section 5), the newer copy from the third try is deleted first, as in its step 5, so this request leaves no copy of the agent made in this pass. On a live workflow it isn't asked for the agent that was running (below).

Record the task's row as `Failed check`, and in its Check column "Failed check, deleted" once the leader says "done", or "Failed check, not deleted" until then (said again at your next entry). Then stop with the change request and N-B9, so Design re-plans the agent's work as Cowork skills.

**On a live workflow** the agent that was running is never the one deleted: on the rebuild path (section 5) it stays as it is, and only the newer copies that failed are deleted. Nothing is left without its agent. Skills this pass already saved (Part 3 saves them before the agents) would run beside the old agent, a mix of versions, so before the stop give the steps to put those skills back from the kept copy (the record's "Put back the kept copy"), in N-B9's reason in plain words, and record in those skills' rows that the kept version is to be put back (the next entry's direct-edit check then sees which is installed). Fail closed: no close, so no Test round runs on the agent until a check has confirmed its lines. After Design declined that request, N-B50.

## 5. A fix, or a task rebuilt from a changed plan

**Which path.** While release check 29 hasn't passed (today), every fix, update and paste-back gap takes the rebuild path at the end of this section, and nothing else here applies; the fix goes into a copy of the build prompt, staged as `package/[agent-name]-build-prompt-[n].md`. Once check 29 passes, the edit-in-place path that follows.

Fix the agent the way it was made: write a short fix prompt for its Agent Builder chat, stage it in `package/[agent-name]-fix-prompt-[n].md` beside the build prompt, and give the line at the end of the fixes, said exactly:

"To [fix / update] [Agent], open Copilot, choose Chat, then Agents, open [Agent] and choose Edit, then paste this into the Agent Builder box:"

then the fix prompt, in a block to copy, then:

"[Context file changed: 'Under Knowledge, remove [file] and add it again from your OneDrive, in Documents/Cowork/[workflow-slug], so the agent reads the new version. ']Before you save, check that Knowledge lists only [the context files / nothing], and that under Work content only [what it uses / nothing] is still on. Say 'done' when it's saved."

**The fix prompt,** one template for a fix and a changed plan:

"In this agent, [the change], so it [the requirement it must meet, in plain words / matches task [task ID] of design-plan.md in my OneDrive, in Framework/[workflow-slug] / carries this line word for word: '[the line]'].[ In a test it [the miss, in plain words].] Change nothing else."

The miss sentence only in fix mode, for a Test miss; the plan's task for a task rebuilt from a changed plan, with no miss; the carried-line fill for a gap the paste-back found. A context file the change touches is staged in `package/` with the prompt and saved again in the workflow's own folder only in Part 3, right before this line, so a new version never reaches a live agent ahead of the rest of its fix; the Knowledge clause then has the leader replace it.

After its "done", until release check 31 passes, the paste-back, said exactly: "Now open [Agent], choose Edit, copy everything under Instructions, and paste it here, so I can check the change kept every line it must carry." Check it again (a paste of the fix prompt itself is asked for again, as in section 3; a gap gets the carried-line fill), keep the new text in the record, then the done form: "[Agent] is [fixed / updated], and Test re-runs everything that uses it." Once release check 31 passes, no paste-back, and: "[Agent] is [fixed / updated]. I can't read its instructions from here, so Test re-runs everything that uses it." Then your close.

**Where release check 29 hasn't passed** (Agent Builder changing an existing agent from a fix prompt; today, so this is the path every fix, update and paste-back gap takes), the rebuild path, in this order. A changed context file is staged and saved again in Part 3 as above, and section 2's step 3 adds it under Knowledge in the new agent.

1. The rebuild form's opening, said exactly: "Agent Builder can't change [Agent] in place, so we'll make a new one with the fix in it."
2. Section 2's steps 1 to 6 (N-B52's main form), the build prompt carrying the fix (for a gap, the missing or reworded line; for a Test miss or a changed plan, the change). Its step 6 is the one paste-back request on this path: N-B53's own paste-back sentence and N-B52's gap sentence aren't said.
3. The paste-back check (section 3) on the new agent's instructions.
4. **Only once it passes:** "Now delete the old [Agent] under Agents, so only the new one runs. Say 'done' when it's gone." Said whole, as the message's last line: when the two agents share a name, the line that tells the leader which one is the old one (the one made first) comes before it, never inside it. Never before: until the new one passes, the old one stays (on a live workflow, still running as it was). Then the done form for the moment (section 3's at a first build; N-B53's in fix mode).
5. **A new one that fails its check** counts as a try. Before the next try, the leader deletes that newer copy, in N-B54's words with [Agent] filled as "the newer [Agent]" (the name both copies share), and waits for "done"; the old one is untouched. After the third failed try, section 4.

## 6. Putting it back, and live changes

- **Kept copy:** the build prompt and every fix prompt in `package/`. Putting it back means building it again from them (section 2, then section 5 for each fix kept), which gives the same instructions in substance, not word for word; say so in one line, and in the record's "Put back the kept copy".
- **Before a live agent changes:** where the record holds the instructions the leader last pasted back and N-E1's agent form said nothing changed since, that text is the copy: save it, with the prompts from `package/`, in `history/kept-copy-YYYY-MM-DD-HHMM/`, asking nothing. Only where the record has none (release check 31 passed, so nothing was pasted) or N-E1 said it changed does N-B48 ask the leader to keep a copy, with Agent Builder's steps to copy its instructions out.

## 7. Release checks this rests on

| Row | What's assumed | Until it passes |
|---|---|---|
| 21 | Agent Builder builds an agent from a build prompt (verified) | If a later run fails: the recovery form for the ordinary chat; where Agent Builder can't build from the files, a change request (N-B9) |
| 28 | A Cowork skill can be added under an agent's Skills | No skill added to an agent |
| 29 | Agent Builder changes an existing agent from a fix prompt | The rebuild path (section 5): a new agent, one paste-back, and the old one deleted only once the new one passes |
| 30 | An agent with a Work content source on can't send, post or change anything, or asks first | Any write the plan routes through an agent rests on the instruction, said in N-B21 |
| 31 | Agent Builder keeps a build prompt's lines word for word | The paste-back and its check |
