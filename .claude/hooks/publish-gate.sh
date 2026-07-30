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

# Only subagent-dispatch tools are relevant. The tool has been named both Task and Agent
# across Claude Code versions, so accept either.
TOOL="$(jqr .tool_name)"
case "$TOOL" in
  Task | Agent | task | agent) ;;
  '') ;;  # unknown shape — fall through to the field probe, then fail open
  *) exit 0 ;;
esac

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
  printf -- '- %s tool=%s target=%s\n' \
    "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "${TOOL:-unknown}" "${TARGET:-unknown}"
} >> "$RUN/.dispatch-log" 2>/dev/null || true

if [ -z "$TARGET" ]; then
  # Could not determine the target agent. Fail open, but leave the full payload behind so
  # the field name can be added above.
  printf '%s\n' "$INPUT" > "$RUN/.last-unrecognised-dispatch.json" 2>/dev/null || true
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
