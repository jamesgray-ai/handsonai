#!/usr/bin/env bash
#
# SubagentStop quality gate for the multi-agent article pipeline.
#
# Wired in .claude/settings.json. Fires whenever ANY subagent in this repo finishes,
# so the first thing it does is check an activation flag and exit inert if this is not
# a pipeline run.
#
# The SubagentStop payload does not reliably identify which agent just stopped, so this
# gate validates WORKSPACE STATE rather than agent identity: it checks every artifact
# that exists against its rule and blocks on the first violation. That makes it
# stage-agnostic, idempotent, and impossible to fool by renaming an agent.
#
# Exit 0 = allow the subagent to stop (with a JSON systemMessage when the gate gave up).
# Exit 2 = block; stderr is fed back to the subagent as instructions to fix its work.
#
# Retries are bounded. A failing subagent is sent back at most MAX_SEND_BACKS times; if
# its work still fails after that, the gate lets it finish but records
# "QUALITY GATE FAILED after N retries: <reason>" in run-log.md and shows the same line
# to the person. It never passes failing work silently, and it can never loop forever.
#
# The payload is parsed with Node.js, which the plugin already needs for its Word
# renderer. Node is only used to read `agent_id` and `stop_hook_active` (which key the
# retry counter) and `cwd`; every quality rule below is plain shell, so a machine without
# Node still gets every check — see the "Node.js missing" section.

set -uo pipefail

INPUT="$(cat)"

HAVE_NODE=0
command -v node > /dev/null 2>&1 && HAVE_NODE=1

json_field() {
  # Prints a top-level field of the hook payload, or nothing. Falls back to empty on any
  # error so a payload change can never crash the gate and wedge the session.
  [ "$HAVE_NODE" = "1" ] || return 0
  printf '%s' "$INPUT" | node -e '
    let d = "";
    process.stdin.on("data", c => d += c).on("end", () => {
      try {
        const v = JSON.parse(d)[process.argv[1]];
        if (v !== undefined && v !== null) process.stdout.write(String(v));
      } catch (e) {}
    });' "$1" 2>/dev/null || true
}

json_string() {
  # Encodes $1 as a JSON string without needing Node, so the gate can always emit its
  # documented JSON output — including on a machine where Node is missing.
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\t'/\\t}"
  s="${s//$'\r'/}"
  printf '"%s"' "$s"
}

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(json_field cwd)}"
[ -n "$PROJECT_DIR" ] || PROJECT_DIR="$PWD"

FLAG="$PROJECT_DIR/outputs/articles/.active-run"
[ -f "$FLAG" ] || exit 0

RUN_REL="$(tr -d '[:space:]' < "$FLAG")"
[ -n "$RUN_REL" ] || exit 0

# Refuse to follow a flag that points outside the project's outputs directory.
case "$RUN_REL" in
  /* | *..*) exit 0 ;;
  outputs/articles/*) ;;
  *) exit 0 ;;
esac

RUN="$PROJECT_DIR/$RUN_REL"
[ -d "$RUN" ] || exit 0

LOG="$RUN/run-log.md"

log_line() {
  # Appends one line to the run's audit trail, creating it with its header if needed.
  # Never fails the gate: an unwritable log loses the line, not the decision.
  {
    [ -f "$LOG" ] || printf '# Run log\n\nOne line per completed stage, appended by the SubagentStop gate. A FAILED line records a stage that finished with work below the bar.\n\n' > "$LOG"
    printf -- '- %s — %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$1" >> "$LOG"
  } 2>/dev/null
}

# ---------------------------------------------------------------------------
# Retry budget
# ---------------------------------------------------------------------------
# This gate used to exit 0 whenever `stop_hook_active` was true. The hooks reference
# defines that field as "true when Claude Code is already continuing as a result of a
# stop hook" (https://code.claude.com/docs/en/hooks#stop-input) — so the agent's second
# attempt, the one made after being sent back, was let through without any check. A
# second weak attempt passed unseen.
#
# Instead, every stop is checked, and the number of send-backs is counted in a small
# state file in the run workspace, next to run-log.md. The counter is keyed by the
# payload's `agent_id` (one per subagent), so each agent gets its own budget and the
# key never resets mid-sequence. Without an agent_id it falls back to one key for the
# run, reset whenever a stop is NOT a hook-driven continuation.
#
# The bound is ours, and it sits well under Claude Code's own backstop: "Claude Code
# overrides a Stop hook after it blocks eight times in a row with no tool call from
# Claude in between" (https://code.claude.com/docs/en/hooks-guide, "Stop hook hits the
# block cap"). We never rely on that cap.

MAX_SEND_BACKS=2

AGENT_KEY="$(json_field agent_id | tr -cd 'A-Za-z0-9_-' | cut -c1-64)"
if [ -z "$AGENT_KEY" ]; then
  AGENT_KEY="run"
  if [ "$HAVE_NODE" = "1" ] && [ "$(json_field stop_hook_active)" != "true" ]; then
    rm -f "$RUN/.gate-send-backs-run" "$RUN/.gate-failed-run" 2>/dev/null
  fi
fi
COUNTER="$RUN/.gate-send-backs-$AGENT_KEY"
FAILED_MARK="$RUN/.gate-failed-$AGENT_KEY"

# ---------------------------------------------------------------------------
# Node.js missing
# ---------------------------------------------------------------------------
# Without Node the gate cannot read `agent_id` or `stop_hook_active`. It does NOT skip
# the checks over that (the old behaviour, when its JSON parser was missing, was to wave
# every subagent through unchecked). The rules below are plain shell and still run; the only thing lost is the
# per-agent counter, so the retry budget is shared by the whole run. That is still
# bounded, so still loop-free. The person is told once per run, in the run log and on
# screen, so the degraded mode is never silent. (The project directory still resolves:
# Claude Code exports CLAUDE_PROJECT_DIR to every hook process.)
if [ "$HAVE_NODE" = "0" ] && [ ! -f "$RUN/.gate-node-missing" ]; then
  : 2>/dev/null > "$RUN/.gate-node-missing"
  log_line "NOTE: Node.js not found — the quality gate is running every check, but its retry limit is shared by the whole run instead of counted per agent. Install Node.js (https://nodejs.org) to restore it."
  NODE_NOTICE="Article pipeline: Node.js is not installed. The quality gate is still checking every stage, but the plugin needs Node.js (https://nodejs.org) for its Word document and for per-agent retry limits. Install it before the publishing step."
else
  NODE_NOTICE=""
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CHAR_FLOOR_RESEARCH=1000
CHAR_FLOOR_ARTICLE=6000    # ~1,000 words; the target is 2,000-2,500
WORD_CEILING_ARTICLE=2750  # the 2,500 target plus 10% tolerance
MIN_SOURCES=3

chars() {
  if [ -f "$1" ]; then
    wc -c < "$1" | tr -d '[:space:]'
  else
    echo 0
  fi
}

words() {
  if [ -f "$1" ]; then
    wc -w < "$1" | tr -d '[:space:]'
  else
    echo 0
  fi
}

# Agents occasionally wrap their output in XML-ish tags borrowed from their own
# prompt scaffolding. It is invisible in a summary and lands in the published file.
stray_tags() {
  if [ -f "$1" ]; then
    grep -cE '</?(content|document|article|output|response)>' "$1" 2>/dev/null | tr -d '[:space:]'
  else
    echo 0
  fi
}

sources() {
  # grep exits 1 on no match, which under `pipefail` would poison the pipeline —
  # so count with a plain grep -c and normalise instead of chaining.
  if [ -f "$1" ]; then
    local n
    n="$(grep -o 'https\?://' "$1" 2>/dev/null | grep -c '' || true)"
    printf '%s' "${n:-0}" | tr -d '[:space:]'
  else
    echo 0
  fi
}

block() {
  # $1 = human-readable instruction fed back to the subagent.
  local reason="$1" count sent
  count="$(tr -cd '0-9' 2>/dev/null < "$COUNTER")"
  count="${count:-0}"
  sent="$count"

  if [ "$count" -lt "$MAX_SEND_BACKS" ]; then
    count=$((count + 1))
    printf '%s\n' "$count" 2>/dev/null > "$COUNTER"
    # Send the work back only if the new count was really saved. Otherwise the next stop
    # would read the old count and block again, so a read-only workspace could become a
    # loop. If it was not saved, fall through to the give-up path below instead.
    if [ "$(tr -cd '0-9' 2>/dev/null < "$COUNTER")" = "$count" ]; then
      {
        printf 'BLOCKED by the article pipeline quality gate (send-back %s of %s).\n\n%s\n\nWorkspace: %s\nFix this before finishing.\n' \
          "$count" "$MAX_SEND_BACKS" "$reason" "$RUN_REL"
        if [ "$count" -ge "$MAX_SEND_BACKS" ]; then
          printf '\nThis is your last attempt. If the work still fails this check when you stop, the gate will let you finish but record QUALITY GATE FAILED in run-log.md. If you cannot fix it, say so plainly in the first line of your summary.\n'
        fi
        if [ -n "$NODE_NOTICE" ]; then printf '\nNote: %s\n' "$NODE_NOTICE"; fi
      } >&2
      exit 2
    fi
  fi

  # Limit reached: stop sending the work back, but do not pass it silently.
  #
  # Blocking again is exactly what can loop. Exiting 0 lets the subagent stop, and the
  # documented `systemMessage` field ("Warning message shown to the user",
  # https://code.claude.com/docs/en/hooks#json-output) puts the failure in front of the
  # person. `decision: "block"` and `additionalContext` are not options here: both keep
  # the subagent running (https://code.claude.com/docs/en/hooks#stop-decision-control).
  # A SubagentStop hook cannot write into the orchestrator's context, so the orchestrator
  # learns of it from run-log.md, which both commands tell it to check after each stage.
  local summary="QUALITY GATE FAILED after $sent retries: $reason"
  summary="${summary//$'\n'/ }"
  if [ ! -f "$FAILED_MARK" ]; then
    : 2>/dev/null > "$FAILED_MARK"
    log_line "$summary"
  fi
  local msg="Article pipeline ($RUN_REL): $summary See run-log.md before continuing."
  [ -n "$NODE_NOTICE" ] && msg="$msg $NODE_NOTICE"
  printf '{"systemMessage": %s}\n' "$(json_string "$msg")"
  exit 0
}

# ---------------------------------------------------------------------------
# Rule 1 — something must have been produced
# ---------------------------------------------------------------------------
# 00-goal.md and run-log.md are written by the orchestrator and this gate, not by a
# subagent, so they do not count as work.

STAGE_FILES=0
for f in 01-research.md 02-draft.md 03-edited.md 03-editorial-memo.md 04-article.md 04-article.docx; do
  [ -s "$RUN/$f" ] && STAGE_FILES=$((STAGE_FILES + 1))
done

if [ "$STAGE_FILES" -eq 0 ]; then
  block "You finished without writing any file to the shared workspace. Every stage of this pipeline hands off through a file — write your output file, then stop."
fi

# ---------------------------------------------------------------------------
# Rule 2 — research dossier
# ---------------------------------------------------------------------------

if [ -f "$RUN/01-research.md" ]; then
  if [ "$(chars "$RUN/01-research.md")" -lt "$CHAR_FLOOR_RESEARCH" ]; then
    block "01-research.md is too thin ($(chars "$RUN/01-research.md") characters, minimum $CHAR_FLOOR_RESEARCH). Return at least 5 named companies with quantified, sourced outcomes."
  fi
  if [ "$(sources "$RUN/01-research.md")" -lt "$MIN_SOURCES" ]; then
    block "01-research.md contains $(sources "$RUN/01-research.md") source URLs, minimum $MIN_SOURCES. Every claim needs a traceable link — add full citations."
  fi
fi

# ---------------------------------------------------------------------------
# Rule 3 — draft
# ---------------------------------------------------------------------------

if [ -f "$RUN/02-draft.md" ]; then
  if [ "$(chars "$RUN/02-draft.md")" -lt "$CHAR_FLOOR_ARTICLE" ]; then
    block "02-draft.md is under length ($(chars "$RUN/02-draft.md") characters, minimum $CHAR_FLOOR_ARTICLE). The target is 2,000-2,500 words."
  fi
  if [ "$(words "$RUN/02-draft.md")" -gt "$WORD_CEILING_ARTICLE" ]; then
    block "02-draft.md is over length ($(words "$RUN/02-draft.md") words, ceiling $WORD_CEILING_ARTICLE). The target is 2,000-2,500 words. Cut the weakest material — do not simply stop mid-argument."
  fi
  if [ "$(stray_tags "$RUN/02-draft.md")" -gt 0 ]; then
    block "02-draft.md contains stray markup tags such as </content>. Write plain markdown only — that file is the article, not a wrapped response."
  fi
fi

# ---------------------------------------------------------------------------
# Rule 4 — the editor must produce a revision, not a critique
# ---------------------------------------------------------------------------

if [ -f "$RUN/03-edited.md" ]; then
  if [ ! -s "$RUN/03-editorial-memo.md" ]; then
    block "03-edited.md exists but 03-editorial-memo.md is missing or empty. Write both: the revised article and the memo explaining what changed and why."
  fi
  if grep -qE '\*\*Original\*\*:|Priority Actions|\*\*Suggested\*\*:' "$RUN/03-edited.md" 2>/dev/null; then
    block "03-edited.md contains critique markers (\"**Original**:\", \"**Suggested**:\" or \"Priority Actions\"). That file must be the finished article with your edits already applied — put the commentary in 03-editorial-memo.md instead."
  fi
  if [ "$(chars "$RUN/03-edited.md")" -lt "$CHAR_FLOOR_ARTICLE" ]; then
    block "03-edited.md is under length ($(chars "$RUN/03-edited.md") characters, minimum $CHAR_FLOOR_ARTICLE). Edit the article, do not truncate it."
  fi
  if [ "$(sources "$RUN/03-edited.md")" -lt "$MIN_SOURCES" ]; then
    block "03-edited.md contains $(sources "$RUN/03-edited.md") source URLs, minimum $MIN_SOURCES. Editing must not drop the citations."
  fi
  if [ "$(words "$RUN/03-edited.md")" -gt "$WORD_CEILING_ARTICLE" ]; then
    block "03-edited.md is over length ($(words "$RUN/03-edited.md") words, ceiling $WORD_CEILING_ARTICLE). The target is 2,000-2,500 words. Editing includes cutting — tighten it rather than passing the overrun through."
  fi
  if [ "$(stray_tags "$RUN/03-edited.md")" -gt 0 ]; then
    block "03-edited.md contains stray markup tags such as </content>. That file must be the finished article in plain markdown, nothing else."
  fi
fi

# ---------------------------------------------------------------------------
# Rule 5 — both deliverables, and the Word file must really be a Word file
# ---------------------------------------------------------------------------

if [ -f "$RUN/04-article.md" ]; then
  # Check the file that actually ships. Rules 3 and 4 screen 02-draft.md and 03-edited.md
  # for stray markup, but 04-article.md was left unchecked — and the publishing stage
  # rewrites it, adding frontmatter and metadata. Everything upstream could be clean and
  # a </content> introduced here would still reach the reader.
  if [ "$(stray_tags "$RUN/04-article.md")" -gt 0 ]; then
    block "04-article.md contains stray markup tags such as </content>. The deliverable must be clean markdown — remove them and regenerate the Word file so the two match."
  fi
  if [ ! -s "$RUN/04-article.docx" ]; then
    block "04-article.md exists but 04-article.docx is missing or empty. This pipeline delivers TWO files. Generate the Word document with scripts/article-to-docx.js and confirm it exists."
  fi
  # Capture the listing before matching. Piping into `grep -q` under `pipefail` reports
  # failure even on a match: grep exits at the first hit, unzip dies of SIGPIPE, and
  # that non-zero status becomes the pipeline's. It only shows up once the archive
  # listing is long enough for grep to finish first — i.e. on real documents, not on
  # small test fixtures.
  #
  # Guard on unzip's presence first. `|| true` cannot distinguish "this archive has no
  # word/document.xml" from "unzip is not installed" — both yield an empty listing. Left
  # unguarded, a machine without unzip rejects a perfectly valid document, tells the
  # publisher to regenerate it, and blocks the regenerated file too: an unbreakable loop
  # at the pipeline's terminal stage. If we cannot verify, we do not manufacture a verdict.
  if ! command -v unzip > /dev/null 2>&1; then
    printf 'NOTE: unzip is not installed, so 04-article.docx could not be verified as a real Word file. It exists and is non-empty; check it by hand.\n' >&2
  else
    DOCX_LISTING="$(unzip -l "$RUN/04-article.docx" 2>/dev/null || true)"
    if ! printf '%s' "$DOCX_LISTING" | grep -c 'word/document.xml' > /dev/null; then
      block "04-article.docx is not a valid Word document — it is not a ZIP archive containing word/document.xml. Regenerate it with scripts/article-to-docx.js."
    fi
  fi
fi

# ---------------------------------------------------------------------------
# Passed — append to the audit trail
# ---------------------------------------------------------------------------

# This agent's work now meets the bar, so its send-back budget is spent no further.
rm -f "$COUNTER" "$FAILED_MARK" 2>/dev/null

[ -f "$LOG" ] || printf '# Run log\n\nOne line per completed stage, appended by the SubagentStop gate. A FAILED line records a stage that finished with work below the bar.\n\n' > "$LOG"

PRESENT=""
for f in 01-research.md 02-draft.md 03-edited.md 03-editorial-memo.md 04-article.md 04-article.docx; do
  [ -s "$RUN/$f" ] && PRESENT="$PRESENT $f"
done

# SubagentStop fires more than once per agent, so logging every pass produces several
# identical lines per stage and buries the shape of the run. Only record a pass when the
# set of artifacts actually changed — then the log is exactly one line per stage.
#
# Hooks run in parallel, so read-compare-append is a race: two events firing in the same
# second both read the old last line and both append. That happened on a real run. mkdir
# is atomic on POSIX, so it serialises the critical section without needing flock, which
# is not available by default on macOS.
LOCK="$RUN/.log.lock"
for _ in 1 2 3 4 5 6 7 8 9 10; do
  if mkdir "$LOCK" 2>/dev/null; then
    LAST="$(grep '— gate passed — artifacts:' "$LOG" 2>/dev/null | tail -1 | sed 's/.*artifacts://')"
    if [ "$LAST" != "$PRESENT" ]; then
      printf -- '- %s — gate passed — artifacts:%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$PRESENT" >> "$LOG"
    fi
    rmdir "$LOCK" 2>/dev/null
    break
  fi
  sleep 0.1
done
# If the lock was never acquired, the log entry is skipped rather than risking a
# duplicate. The audit trail is a convenience; never block an agent over it.

[ -n "$NODE_NOTICE" ] && printf '{"systemMessage": %s}\n' "$(json_string "$NODE_NOTICE")"
exit 0
