#!/usr/bin/env bash
#
# PreToolUse human-approval gate for the multi-agent article pipeline.
#
# Wired in .claude/settings.json against subagent-dispatch tools. It blocks the
# publishing agent from being launched until a human has approved the article, so the
# human-in-the-loop step is enforced by the harness rather than merely requested in a
# prompt. Under automatic delegation, "the orchestrator was told to ask first" is exactly
# the instruction most likely to be skipped.
#
# Deliberately FAIL-OPEN. Every uncertainty — no activation flag, an unrecognised payload
# shape, a missing field — exits 0 and allows the dispatch. A gate that wedges a live
# demonstration is worse than one that occasionally misses. The only case it blocks is the
# one it is certain about: this is a pipeline run, this is the publishing agent, and no
# approval marker exists.
#
# NOTE: this is a guardrail against drift, not a security boundary. The orchestrator could
# write the approval marker itself. What the hook guarantees is that skipping the human is
# a deliberate act rather than an accident, and that it leaves an audit trail.
#
# Exit 0 = allow the dispatch.
# Exit 2 = block; stderr is fed back to the orchestrator.

set -uo pipefail

INPUT="$(cat)"

jqr() {
  printf '%s' "$INPUT" | jq -r "try ($1 // empty) catch empty" 2>/dev/null || true
}

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(jqr .cwd)}"
[ -n "$PROJECT_DIR" ] || PROJECT_DIR="$PWD"

# Only a pipeline run arms this gate.
FLAG="$PROJECT_DIR/outputs/articles/.active-run"
[ -f "$FLAG" ] || exit 0

RUN_REL="$(tr -d '[:space:]' < "$FLAG")"
case "$RUN_REL" in
  outputs/articles/*) ;;
  *) exit 0 ;;
esac
case "$RUN_REL" in *..*) exit 0 ;; esac

RUN="$PROJECT_DIR/$RUN_REL"
[ -d "$RUN" ] || exit 0

# From here on this is definitely a pipeline run, so the gate is meant to be enforcing.
#
# jq is how this gate reads the dispatch payload. Without it every field probe below
# returns empty, the target agent is never identified, and the script falls through to
# its fail-open exit — silently allowing the publisher to run with no human approval, for
# every dispatch, for the whole session. That is the one failure this gate exists to
# prevent, so it is the one case where it fails CLOSED: jq's absence is a condition we
# can establish with certainty, and a loud stop with a fix is strictly better than a
# guarantee that has quietly stopped being true.
#
# (The SubagentStop gate makes the opposite call for the same missing tool — see the
# comment there. The asymmetry is deliberate: this gate blocking is recoverable, that
# one blocking risks an infinite loop.)
if ! command -v jq > /dev/null 2>&1; then
  cat >&2 <<'EOF'
BLOCKED — the human-approval gate cannot run.

jq is not installed, so this hook cannot read the dispatch payload and cannot tell
whether a human has approved this article. Rather than let the publishing step through
unchecked, it is stopping here.

Fix it with one of:
  macOS         brew install jq
  Debian/Ubuntu sudo apt-get install jq

Then dispatch the publisher again. If you would rather proceed without the automated
gate, confirm approval with the human yourself and remove the hook from settings.
EOF
  exit 2
fi

# Only subagent-dispatch tools are relevant. The tool has been named both Task and Agent
# across Claude Code versions, so accept either.
TOOL="$(jqr .tool_name)"

# Record the dispatch BEFORE deciding whether the tool name is one we know.
#
# This used to sit below the target probe, so an unrecognised tool name exited here and
# left no trace at all — failing open silently, which is exactly what the file promises
# never to do. The audit trail is the fallback for every uncertainty in this gate, so it
# has to be written before any of them can exit.
{
  printf -- '- %s tool=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "${TOOL:-unknown}"
} >> "$RUN/.dispatch-log" 2>/dev/null || true

KNOWN_DISPATCH_TOOL=0
case "$TOOL" in
  Task | Agent | task | agent) KNOWN_DISPATCH_TOOL=1 ;;
esac

# Note there is no early exit on an unrecognised tool name. The tool has been called both
# Task and Agent across Claude Code versions, and renaming it again is precisely the
# drift this gate probes six field spellings to survive — exiting on the name would skip
# that probe and miss a `subagent_type: hbr-publisher` sitting in plain sight. Whether
# the name was recognised only changes how loudly an empty probe is reported below.

# The field naming for the target agent has also varied. Probe the known spellings and
# fall back to scanning the raw payload.
TARGET=""
for candidate in \
  '.tool_input.subagent_type' \
  '.tool_input.subagentType' \
  '.tool_input.agent_type' \
  '.tool_input.agentType' \
  '.tool_input.subagent' \
  '.subagent_type'
do
  TARGET="$(jqr "$candidate")"
  [ -n "$TARGET" ] && break
done

# Record what the payload actually looked like, so the shape can be confirmed on the
# first real run rather than assumed. Kept in the workspace, which is gitignored.
{
  printf -- '  target=%s\n' "${TARGET:-unknown}"
} >> "$RUN/.dispatch-log" 2>/dev/null || true

if [ -z "$TARGET" ]; then
  # No target agent found. Fail open either way, but only keep the payload when the tool
  # WAS a recognised dispatch tool — that is the genuinely surprising case, and the file
  # is there to be read when adding a field spelling. Keeping it for every other tool
  # would overwrite that evidence with noise on the very next call.
  if [ "$KNOWN_DISPATCH_TOOL" = "1" ]; then
    printf '%s\n' "$INPUT" > "$RUN/.last-unrecognised-dispatch.json" 2>/dev/null || true
  fi
  exit 0
fi

# Not the publishing agent? Not our business.
case "$TARGET" in
  *hbr-publisher*) ;;
  *) exit 0 ;;
esac

if [ -s "$RUN/APPROVED" ]; then
  exit 0
fi

cat >&2 <<EOF
BLOCKED: publishing requires human approval first.

You tried to dispatch hbr-publisher, but no approval marker exists at:
  $RUN_REL/APPROVED

Publishing is the irreversible step in this pipeline, so a human decides it — not you.

Do this instead:
  1. Use AskUserQuestion to ask the human whether to publish. Show them the significant
     editorial changes from 03-editorial-memo.md, the article's title and opening
     paragraph, and the paths to both files so they can read them.
  2. Only if they approve, record it:
       echo "approved by human at \$(date -u '+%Y-%m-%dT%H:%M:%SZ')" > $RUN_REL/APPROVED
  3. Then dispatch hbr-publisher again.

If they decline, send their notes back to hbr-editor for revision and ask again.
Do not create the approval marker on the human's behalf.
EOF
exit 2
