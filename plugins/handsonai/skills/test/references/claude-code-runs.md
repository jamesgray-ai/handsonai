# The AI's runs on Claude Code

Read this on Claude Code, when a round runs: the AI's own runs of the practice inputs, the round's practice folder, and the wrapper's `test` profile.

**Contents:** 1. Before the first run · 2. The practice folder · 3. Starting a run · 4. Checkpoints and resuming · 5. Two runs, compared · 6. When a run can't be kept separate · 7. The round's close · 8. Release checks this rests on

## 1. Before the first run

The AI runs each practice input twice, in headless sessions started only through `framework/.bin/test-run.sh` with the `test` profile; the leader runs the real example by hand. Never start `claude` any other way, and never pass it a flag: the wrapper builds every setting from the build record and the plan and refuses `--dangerously-skip-permissions`, any permission-mode flag, and every other Claude Code flag.

Before the first run, and again before every run and every resume:

1. **The version.** Read `claude --version`. Outside the range the platform registry records for release check 6, the AI doesn't run the inputs: N-T42 (section 6).
2. **The fingerprint.** `shasum -a 256 framework/.bin/test-run.sh <this skill's folder>/scripts/test-run.sh`. Both must equal the build record's `fingerprints.wrapper`. A mismatch fails closed: N-T42. Nothing is ever edited to make them match.
3. **The allow, on a live workflow.** Go-live removed the wrapper's allow. At the start of Part 2 of a round on a live workflow, ask N-T47:

   > "For this round I need to allow my test script again in this project's settings, so I can run your practice inputs in separate sessions. I'll remove it when the round ends. Shall I go ahead?"

   On a yes, add the `allow` and `deny` rules `framework/.bin/test-run.sh allow-rules <slug> --plugin-copy …` prints to `.claude/settings.local.json`, adding only. On a no, the leader runs the practice inputs too (N-T8, as on the other platforms).
4. **A block Build left on** (`write_block` not `off` in the record) stays on through the round, so it binds the leader's runs too, and comes off at the round's close (section 7). Test adds no block and no hook of its own: the leader's own run is protected as on every platform (3c-DD).

## 2. The practice folder

The leader's run saves its results into the round's practice folder in the workspace, by the practice-run instruction. Test makes it, with its marker, before the first hand-over:

```bash
framework/.bin/test-run.sh practice-create <slug> --plugin-copy <this skill's folder>/scripts/test-run.sh --round <n>
```

It prints the folder: `practice/`, or `practice-<slug>/` where a `practice/` without this workflow's marker is already there or several workflows share the workspace. Record that path in the round's Environment section and the results file's `environment`. The marker file is `.framework-practice`. If it refuses because a marked folder is still there from an earlier round, clear that one first (section 7) at the path that round recorded; if a folder is there without the marker, it's the leader's own and is never used or cleared.

Each of the leader's runs saves into `[practice folder]/[input]-[run]/`, named in Test's hand-over block. Nothing reads the practice folder during the round except Test, after a run comes back.

The AI's runs don't use it. Each has its own `practice/` inside its own run folder, outside the repository.

## 3. Starting a run

Write each run's prompt to a file outside `framework/` (the round's scratch file, say): the workflow's start phrase, the cue "practice run", the round's number, the input's name, the run number, that the input is in `input/[file]`, and that anything it saves goes in its own `practice/` folder. Nothing from the requirements, the plan or this round's file goes in the prompt.

```bash
framework/.bin/test-run.sh test <slug> --plugin-copy <this skill's folder>/scripts/test-run.sh \
  --prompt-file <prompt file> --input framework/<slug>/inputs/<E-file>.md
```

Start both runs of each input, and the inputs, in parallel. The wrapper:

- refuses any input outside `framework/<slug>/inputs/`, and strips its `source:` and `tests:` header, so no line ID reaches the run;
- makes a fresh run folder outside the repository holding the installed skills and agents, their context and the input, and prints `run_folder:` first: record it in the round's Environment at once;
- builds the session's settings from the record: every write action of every connection denied, the connections' reads and the context allowed, Write and Edit only inside the run folder's `practice/` (where release check 3 has passed), only the commands and domains the plan names, Bash and WebFetch denied otherwise, the permission mode fixed, and the connection config naming each variable, never a value;
- runs the start-up check for every session: the settings read back, then a probe session with the same settings, then the real one, each checked from its start-up message before anything else (the tool list, the connections, the permission mode, any plugin, any hook);
- prints `session_id:`, `startup_check: passed`, the run's result, and each file the run saved in its `practice/`.

Grade from that output. Hold a file the run saved to the same standard as its closing block. A run that shows signs of reading the framework folder or a practice folder is refused and run again (the transcript check).

**An input whose path writes through a command line** goes to the leader, never to a headless run. Say N-T43, then N-T8:

> "I can't let a practice run use the command line without risking a change, so you'll run [input] yourself:"

## 4. Checkpoints and resuming

A run ends its turn at a checkpoint. Ask the leader N-T9, one checkpoint per message:

> "[Input]: it's asking you: [the checkpoint's question] (nothing is sent or changed). What would you decide?"

Then resume that run, through the same profile, in the same run folder, with the leader's decision in a new prompt file:

```bash
framework/.bin/test-run.sh test <slug> --plugin-copy <this skill's folder>/scripts/test-run.sh \
  --prompt-file <decision file> --resume <session_id> --run-folder <run_folder>
```

The wrapper refuses a resume through another profile or in a folder it didn't make, and the resumed session passes the start-up check again, so it keeps every protection. Check the fingerprint again first (section 1).

The second run of the same input reuses the leader's decision. Show the leader its content only when it differs in what the checkpoint is about, with N-T9's second form:

> "[Input], second try, with a different draft: [the difference]. Same decision?"

## 5. Two runs, compared

Both runs must meet a line for it to count as met. When they disagree, show both and say N-T31:

> "[Input] passed once and missed once ([the line]), so it isn't reliable yet. It's on the list for Build to tighten."

Then the next input, or the verdict. The disagreement is a build miss, with Cause `two runs differ`. Before the per-input reply, show the leader what the run produced (the weaker run's, when the two differ).

Where a miss's cause isn't clear, run that one part alone on the same input, in a fresh session through the same profile.

## 6. When a run can't be kept separate

Every one of these fails closed to the leader running the practice inputs, in one batched session, as on the other platforms. Say N-T42, then N-T8:

> "I can't run these on my own here without your other settings coming along, so you'll run them:"

| What happened | The wrapper's exit |
|---|---|
| `claude --version` is outside release check 6's verified range | (checked before the call) |
| The fingerprint doesn't match the record and this skill's copy | 4, or your own check first |
| The start-up check failed: a tool neither allowed nor denied, a hook loaded, the wrong permission mode, a connection missing or extra, a plugin loaded, the workflow not loaded | 3 |
| `python3` or `claude` missing | 6 |
| The record or plan can't be used safely | 5 |
| A connection can't be passed without copying a secret (a claude.ai connector, today) | 7: only the inputs that need that connection go to the leader |

Never retry with other settings, and never start a session another way. A refusal (exit 2) means the call was wrong: fix the call, never the settings.

## 7. The round's close

Whatever the verdict, and when a round is set aside:

1. **The practice folder:** clear the one this round created, at the path recorded in its Environment:

   ```bash
   framework/.bin/test-run.sh practice-clear <slug> --plugin-copy … --path <recorded path>
   ```

   The wrapper clears only `practice/` or `practice-<slug>/` holding this workflow's marker. A folder without the marker, or one this round didn't record, is never cleared: leave it and say so.
2. **The AI's run folders:** clear each one recorded in the Environment with `runs-clear <slug> --plugin-copy … --path <run folder>`. The wrapper clears only folders it made for this workflow.
3. **A block taken over from Build:** `framework/.bin/test-run.sh lift-rules <slug> --plugin-copy …`, then remove exactly the rules in `remove` from `.claude/settings.local.json`, set `write_block: off` in the record, and read the settings back with `settings-check`. A rule another workflow's block still lists, or one the leader had, stays.
4. **The wrapper's allow, on a live workflow:** `allow-rules <slug> --plugin-copy … --lift`, then remove exactly the rules in `remove`. When `kept_for` names another workflow that still needs it, it stays. Before a first go-live, the allow stays until go-live removes it the same way.
5. **Read the settings back** with `settings-check`.

## 8. Release checks this rests on

Each is a rules 13.2 row (the platform registry's `release_checks` id). Until a row is recorded as passed on a range that includes the running `claude --version`, take its fallback.

| Row | What's assumed | Fallback |
|---|---|---|
| 3 | A headless session's Write and Edit stay inside its own `practice/` | Build records `headless_writes none`: Write and Edit denied outright, and a file-output run is graded from the files shown in its output |
| 5 | `/mcp` switches a connection off for one session only | No `/mcp` step in the hand-over; N-F4 in every Claude Code hand-over |
| 6 | Headless runs under the subscription login; the leader's settings, hooks, instructions and memory stay out; `--strict-mcp-config` with a config naming a variable; unlisted tools refused; Test's deny rules bind; the workflow loads from the run folder's `.claude/`; a checkpoint ends the turn and `--resume` keeps the settings; the wrapper refuses bypass flags | The leader runs the practice inputs (N-T42) |
