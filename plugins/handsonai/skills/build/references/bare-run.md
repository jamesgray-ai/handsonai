# Try it bare first

Read before each main skill's task: once per main skill (the part, a skill or an agent, that produces the workflow's output); helper skills skip it. It shows what the plain model already does, so the skill's instructions cover only what it missed, plus the rules that must always hold. It is never run inside your own chat, which holds the requirements.

## 1. The input

One practice input from `inputs/` whose `tests:` lines the main skill's task meets, never the flag input. Before anything sees it:

- **Strip the header.** The header lines are one explicit list, `source:`, `tests:` and `expect:`: remove them only while they lead the file, then one blank line, then stop. A line further down that reads like one (`expect: …` in the input's own text) stays.
- **A carry-over input's `Earlier run:` paragraph** (the paragraph that then opens the body, and the blank line after it) is set-up, never input, and a practice run never touches the workflow's real store. Remove it from the input, and put its state in a copy of the store the plan's `Stateful?` row names, handed to the run as one of the context files the main skill reads. On Claude Code, write the copy's text in the bare run's prompt file yourself, beside the input, named as the store's content. On Claude desktop the block carries it with the context; on Claude on the web, ChatGPT and Codex, one sentence in model wording before the block asks the leader to point the run at a test copy of [the store, in plain words] holding [that state, in plain words], never the real one. The block holds neither the header nor the paragraph.
- **A known edge:** a real input whose own text opens with a paragraph starting "Earlier run:" loses it, since the strip can't tell it from a carry-over input's set-up.

## 2. The run

The plain model, with only the context the main skill will read and no skill instructions. The prompt holds the practice-run cue ("practice run"), the never-made rule (`carried-lines.md`), the workflow's goal in one plain line, and the input. **It saves nothing,** on every platform: a file the main skill would produce comes back as its content in the answer; the practice folder isn't used.

- **Claude Code:** a headless session through the wrapper's `bare` profile, in a fresh folder recorded in `run_folders`, with no connections or only read-only ones (`setup.md` section 2 item 7). Check the wrapper's fingerprint first (`claude-code-block.md` section 5); the wrapper runs its start-up check before the prompt. A settings file that would allow a write is ignored: the `bare` profile builds its own settings from the record.
- **Claude and ChatGPT:** the leader runs it. Say the hand-over for this platform exactly, then the block to paste, in one fenced block. No N-F4 follows: the bare run's connections are all off.
  - Claude on the web and ChatGPT: "To see what the AI does with no instructions, open a new chat in your workflow's Project, so it has nothing it could send or change with. Paste this, and copy back what it says. Then delete that chat." with, after "Project", on Claude ", and before typing, switch off connectors and memory under +", and on ChatGPT ", and don't add any apps".
  - Claude desktop, a chat with no folder selected, the context the main skill reads pasted into the block: "To see what the AI does with no instructions, open a new chat with no folder selected, and before typing, switch off connectors and memory under +, so it has nothing it could send or change with. Paste this, and copy back what it says. Then delete that chat."
  - The leader copies the answer back; if they say "skip", record it and write instructions for every line.
- **Codex: no bare run in this release.** It's skipped (section 3) while release check 36 is open. No command is confirmed that starts Codex with nothing it could send or change with and no instructions: a `-c 'mcp_servers={}'` override leaves every configured connection (MCP server) on, so the plain model could still use one that sends, and Codex's global `AGENTS.md` and the leader's own skills still load. So never give the leader a Codex command for a bare run, and never tell them a Codex session has no connections or no instructions. There is no Codex hand-over to say in this release.
- **No older skill on:** an older skill the leader named at N-B51 is already switched off (Part 2 waits for its "done"), so it can't load in place of no instructions.

## 3. When it's skipped

Record it under `bare_run:` in block form, one line per main skill, the reason in double quotes (`[skill]: "skipped: [why]"`, as the record template shows; never a `{ … }` map, which a comma in the reason would break), and write instructions for every line (for an agent on Microsoft 365 you write none: Agent Builder writes them from the plan). Say a skip to the leader as one sentence, with its reason, in a paragraph of its own (never inside another line, such as the real-change list, and never left to the record alone), before that task's first check, and never what the instructions will hold in its place (no promise that they cover your rules instead): nothing is known of them until they're checked.
- on a rebuild or in fix mode, where the workflow's own installed skill would load;
- where the platform's bare-run release check hasn't passed: Microsoft 365 (release check 25), ChatGPT (16), Codex (36: a Codex command that starts with no connections, no global `AGENTS.md` and no user skills), Claude's own (13);
- on Codex when the leader works only in the Codex app or the IDE extension (`skipped: no terminal`);
- on Claude Code when the leader didn't OK the wrapper, the headless release check (6) hasn't passed, `python3` is missing, or the wrapper's fingerprint doesn't match.

## 4. Graded and shown

Grade the answer against the lines the task meets that an output can show (the bare run takes no actions). Show it in one message: each line in plain words, met or missed, ending with the promise clause, said exactly, then the next action:

"Here's what the AI did with no instructions: [result, met / missed]. I'll write instructions only for what it missed, plus your rules."

The rest of the message is model wording.

## 5. What gets written, and recorded

Write instructions for each line the bare run missed; and, whatever it did, every must-have, every rule, every checkpoint and every safety line, plus everything in `carried-lines.md`. Record `[skill]: done` under `bare_run:`, in block form, and in the record's *Also* section what the plain model handled.
