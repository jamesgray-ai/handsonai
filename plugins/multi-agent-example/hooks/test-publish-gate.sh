#!/usr/bin/env bash
# Tests for publish-gate.sh — the PreToolUse human-approval gate.
#
# Run: bash .claude/hooks/test-publish-gate.sh

set -uo pipefail

GATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/publish-gate.sh"
PASS=0
FAIL=0

new_workspace() {
  TMP="$(mktemp -d)"
  RUN="$TMP/outputs/articles/demo"
  mkdir -p "$RUN"
  echo "outputs/articles/demo" > "$TMP/outputs/articles/.active-run"
}

# $1 = tool name, $2 = subagent field name, $3 = target agent
dispatch() {
  local tool="$1" field="$2" target="$3"
  printf '{"session_id":"t","cwd":"%s","hook_event_name":"PreToolUse","tool_name":"%s","tool_input":{"%s":"%s","prompt":"go"}}' \
    "$TMP" "$tool" "$field" "$target" | bash "$GATE" 2>"$TMP/stderr"
  echo $?
}

assert() {
  local name="$1" want="$2" got="$3" needle="${4:-}"
  if [ "$want" != "$got" ]; then
    echo "  FAIL  $name — expected exit $want, got $got"
    FAIL=$((FAIL + 1)); return
  fi
  if [ -n "$needle" ] && ! grep -qi -- "$needle" "$TMP/stderr"; then
    echo "  FAIL  $name — stderr missing '$needle'"
    echo "        $(head -c 200 "$TMP/stderr")"
    FAIL=$((FAIL + 1)); return
  fi
  echo "  ok    $name"
  PASS=$((PASS + 1))
}

echo "publish-gate.sh"

# --- Blocks the publisher without approval --------------------------------

new_workspace
assert "publisher without approval → block" 2 "$(dispatch Agent subagent_type hbr-publisher)" "requires human approval"
rm -rf "$TMP"

new_workspace
assert "publisher, legacy Task tool → block" 2 "$(dispatch Task subagent_type hbr-publisher)" "requires human approval"
rm -rf "$TMP"

# Field-name variants across Claude Code versions must all be recognised.
for field in subagent_type subagentType agent_type agentType subagent; do
  new_workspace
  assert "recognises field '$field' → block" 2 "$(dispatch Agent "$field" hbr-publisher)"
  rm -rf "$TMP"
done

# --- Allows the publisher once approved -----------------------------------

new_workspace
echo "approved by human at 2026-07-30T12:00:00Z" > "$RUN/APPROVED"
assert "publisher with approval → allow" 0 "$(dispatch Agent subagent_type hbr-publisher)"
rm -rf "$TMP"

new_workspace
: > "$RUN/APPROVED"   # empty marker does not count
assert "empty approval marker → block" 2 "$(dispatch Agent subagent_type hbr-publisher)" "requires human approval"
rm -rf "$TMP"

# --- Leaves everything else alone -----------------------------------------

new_workspace
assert "other agent (writer) → allow" 0 "$(dispatch Agent subagent_type tech-executive-writer)"
rm -rf "$TMP"

new_workspace
assert "other agent (editor) → allow" 0 "$(dispatch Agent subagent_type hbr-editor)"
rm -rf "$TMP"

new_workspace
printf '{"cwd":"%s","tool_name":"Bash","tool_input":{"command":"ls"}}' "$TMP" | bash "$GATE" 2>"$TMP/stderr"
assert "unrelated tool (Bash) → allow" 0 "$?"
rm -rf "$TMP"

# --- Inert outside a pipeline run -----------------------------------------

TMP="$(mktemp -d)"
printf '{"cwd":"%s","tool_name":"Agent","tool_input":{"subagent_type":"hbr-publisher"}}' "$TMP" \
  | bash "$GATE" 2>"$TMP/stderr"
assert "no activation flag → allow (inert)" 0 "$?"
rm -rf "$TMP"

# --- Fails open on an unrecognised payload --------------------------------

new_workspace
printf '{"cwd":"%s","tool_name":"Agent","tool_input":{"mystery_field":"hbr-publisher"}}' "$TMP" \
  | bash "$GATE" 2>"$TMP/stderr"
assert "unknown field name → allow (fail open)" 0 "$?"
if [ -s "$RUN/.last-unrecognised-dispatch.json" ]; then
  echo "  ok    unrecognised payload captured for inspection"
  PASS=$((PASS + 1))
else
  echo "  FAIL  unrecognised payload was not captured"
  FAIL=$((FAIL + 1))
fi
rm -rf "$TMP"

new_workspace
# CLAUDE_PROJECT_DIR must be passed explicitly here. Every other case reaches the gate
# through dispatch(), which supplies `cwd` in the payload — but this payload has no cwd
# by design, so without the env var the gate resolves the project directory to whatever
# repo the test happens to run from, finds no activation flag there, and exits inert at
# the very first check. The assertion then passed while exercising nothing at all about
# malformed JSON.
printf 'not json at all' | CLAUDE_PROJECT_DIR="$TMP" bash "$GATE" 2>"$TMP/stderr"
assert "malformed payload → allow (fail open)" 0 "$?"
rm -rf "$TMP"

# --- Audit trail ----------------------------------------------------------

new_workspace
dispatch Agent subagent_type hbr-editor > /dev/null
if grep -q 'target=hbr-editor' "$RUN/.dispatch-log" 2>/dev/null; then
  echo "  ok    dispatch log records the target agent"
  PASS=$((PASS + 1))
else
  echo "  FAIL  dispatch log missing"
  FAIL=$((FAIL + 1))
fi
rm -rf "$TMP"

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
