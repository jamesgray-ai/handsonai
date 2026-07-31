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
# Exit 0 = allow the subagent to stop.
# Exit 2 = block; stderr is fed back to the subagent as instructions to fix its work.

set -uo pipefail

INPUT="$(cat)"

json_field() {
  # Reads a top-level field from the hook payload. Falls back to empty on any error
  # so a payload change can never crash the gate and wedge the session.
  printf '%s' "$INPUT" | jq -r "try (.$1 // empty) catch empty" 2>/dev/null || true
}

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(json_field cwd)}"
[ -n "$PROJECT_DIR" ] || PROJECT_DIR="$PWD"

# Never re-enter: if we already blocked once and the subagent is stopping again as a
# result, let it go rather than risk an infinite block loop.
[ "$(json_field stop_hook_active)" = "true" ] && exit 0

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

# jq is how this gate reads `stop_hook_active` — the guard that stops a blocked subagent
# from being blocked forever. Without jq that field always reads empty, the guard never
# fires, and any block this gate issues can turn into an infinite loop.
#
# So this gate fails OPEN on a missing jq, loudly. That is the opposite of what
# publish-gate.sh does with the same missing tool, and deliberately so: a publish gate
# that blocks is recoverable in one step, whereas this gate blocking with a dead loop
# guard can wedge the run entirely. Quality checks are worth losing; the session is not.
if ! command -v jq > /dev/null 2>&1; then
  cat >&2 <<'EOF'
WARNING: the article pipeline quality gate is not running.

jq is not installed, so this hook cannot read the payload field that prevents an
infinite block loop. It is allowing this subagent through unchecked rather than risk
wedging the run — no artifact was validated.

Install jq (macOS: brew install jq / Debian: sudo apt-get install jq) to restore the
quality checks, and review the artifacts by hand for this run.
EOF
  exit 0
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
  # $1 = human-readable instruction fed back to the subagent
  printf 'BLOCKED by the article pipeline quality gate.\n\n%s\n\nWorkspace: %s\nFix this before finishing.\n' \
    "$1" "$RUN_REL" >&2
  exit 2
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

LOG="$RUN/run-log.md"
[ -f "$LOG" ] || printf '# Run log\n\nOne line per completed stage, appended by the SubagentStop gate.\n\n' > "$LOG"

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

exit 0
