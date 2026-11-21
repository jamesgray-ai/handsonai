#!/usr/bin/env bash
# Tests for subagent-gate.sh — the SubagentStop quality gate.
#
# Run: bash .claude/hooks/test-subagent-gate.sh
#
# Each case builds a synthetic workspace, pipes SubagentStop JSON into the gate,
# and asserts the exit code (0 = allow, 2 = block) and the blocking reason.

set -uo pipefail

GATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/subagent-gate.sh"
PASS=0
FAIL=0

# A minimal but rule-satisfying dossier / draft. The gate enforces length and
# citation floors, so fixtures must clear them.
make_sources() {
  printf 'Source: https://hbr.org/example-%s\n' 1 2 3
}
make_body() {
  # $1 = target character count
  local target="$1" out=""
  while [ "${#out}" -lt "$target" ]; do
    out+="Enterprise AI agents changed how this company handles its highest-volume "
    out+="workflows, and the measured result was reported publicly. "
  done
  printf '%s\n' "$out"
}

run_gate() {
  # $1 = project dir (becomes cwd in the payload)
  printf '{"session_id":"test","cwd":"%s","hook_event_name":"SubagentStop","stop_hook_active":false}' "$1" \
    | bash "$GATE" 2>"$TMP/stderr"
  echo $?
}

assert() {
  # $1 = case name, $2 = expected exit, $3 = actual exit, $4 = expected substring in stderr ("" to skip)
  local name="$1" want="$2" got="$3" needle="${4:-}"
  if [ "$want" != "$got" ]; then
    echo "  FAIL  $name — expected exit $want, got $got"
    [ -s "$TMP/stderr" ] && echo "        stderr: $(head -c 300 "$TMP/stderr")"
    FAIL=$((FAIL + 1))
    return
  fi
  if [ -n "$needle" ] && ! grep -qi -- "$needle" "$TMP/stderr"; then
    echo "  FAIL  $name — stderr did not mention '$needle'"
    echo "        stderr: $(head -c 300 "$TMP/stderr")"
    FAIL=$((FAIL + 1))
    return
  fi
  echo "  ok    $name"
  PASS=$((PASS + 1))
}

# Builds a fresh project dir with an activated run workspace.
# Sets $TMP (project root) and $RUN (run directory).
new_workspace() {
  TMP="$(mktemp -d)"
  RUN="$TMP/outputs/articles/demo"
  mkdir -p "$RUN"
  echo "outputs/articles/demo" > "$TMP/outputs/articles/.active-run"
}

echo "subagent-gate.sh"

# --- Inertness ------------------------------------------------------------

TMP="$(mktemp -d)"
assert "no activation flag → inert" 0 "$(run_gate "$TMP")"
rm -rf "$TMP"

new_workspace
rm "$TMP/outputs/articles/.active-run"
mkdir -p "$TMP/outputs/articles/demo"
assert "flag deleted mid-repo → inert" 0 "$(run_gate "$TMP")"
rm -rf "$TMP"

# stop_hook_active used to make the gate exit 0 unchecked, so an agent's second attempt
# after being sent back was never looked at. A retry must be checked like any other stop.
new_workspace
printf '{"session_id":"t","cwd":"%s","hook_event_name":"SubagentStop","stop_hook_active":true}' "$TMP" \
  | bash "$GATE" 2>"$TMP/stderr"
assert "stop_hook_active no longer skips the checks" 2 "$?" "without writing any file"
rm -rf "$TMP"

new_workspace
echo "outputs/articles/does-not-exist" > "$TMP/outputs/articles/.active-run"
assert "flag names missing dir → inert" 0 "$(run_gate "$TMP")"
rm -rf "$TMP"

# --- Empty workspace ------------------------------------------------------

new_workspace
assert "no artifacts → block" 2 "$(run_gate "$TMP")" "without writing any file"
rm -rf "$TMP"

# --- Research stage -------------------------------------------------------

new_workspace
echo "too short" > "$RUN/01-research.md"
assert "thin dossier → block" 2 "$(run_gate "$TMP")" "01-research.md"
rm -rf "$TMP"

new_workspace
make_body 1500 > "$RUN/01-research.md"
assert "dossier without citations → block" 2 "$(run_gate "$TMP")" "source"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
assert "valid dossier → allow" 0 "$(run_gate "$TMP")"
rm -rf "$TMP"

# --- Draft stage ----------------------------------------------------------

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 2000; make_sources; } > "$RUN/02-draft.md"
assert "short draft → block" 2 "$(run_gate "$TMP")" "02-draft.md"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
assert "valid draft → allow" 0 "$(run_gate "$TMP")"
rm -rf "$TMP"

# --- Length ceiling -------------------------------------------------------
# The first live run produced a 3,030-word article against a 2,000-2,500 target. The
# gate had a floor but no ceiling, so nothing caught it.

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 40000; make_sources; } > "$RUN/02-draft.md"   # ~5,700 words
assert "over-length draft → block" 2 "$(run_gate "$TMP")" "over length"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 40000; make_sources; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
assert "over-length revision → block" 2 "$(run_gate "$TMP")" "over length"
rm -rf "$TMP"

# --- Stray markup ---------------------------------------------------------
# The first live run left a literal </content> tag at the end of 03-edited.md.

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; printf '\n</content>\n'; } > "$RUN/02-draft.md"
assert "stray tag in draft → block" 2 "$(run_gate "$TMP")" "stray markup"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; printf '\n</content>\n'; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
assert "stray tag in revision → block" 2 "$(run_gate "$TMP")" "stray markup"
rm -rf "$TMP"

# The deliverable itself, which the publishing stage rewrites after every upstream check
# has already passed.
new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
{ make_body 6500; make_sources; printf '\n</content>\n'; } > "$RUN/04-article.md"
# A placeholder is enough: the stray-markup check runs before the .docx validity check,
# so this must block on the tag, not on the file being a fake Word document. The message
# assertion is what proves which rule actually fired.
printf 'placeholder' > "$RUN/04-article.docx"
assert "stray tag in the deliverable → block" 2 "$(run_gate "$TMP")" "stray markup"
rm -rf "$TMP"

# --- Editor stage ---------------------------------------------------------

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; } > "$RUN/03-edited.md"
assert "edited draft without memo → block" 2 "$(run_gate "$TMP")" "03-editorial-memo.md"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; printf '\n- **Original**: the old line\n'; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
assert "critique masquerading as revision → block" 2 "$(run_gate "$TMP")" "critique"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
assert "valid revision → allow" 0 "$(run_gate "$TMP")"
rm -rf "$TMP"

# --- Publisher stage ------------------------------------------------------

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
{ make_body 6500; make_sources; } > "$RUN/04-article.md"
assert "markdown without Word file → block" 2 "$(run_gate "$TMP")" "04-article.docx"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
{ make_body 6500; make_sources; } > "$RUN/04-article.md"
echo "not a real docx" > "$RUN/04-article.docx"
assert "corrupt Word file → block" 2 "$(run_gate "$TMP")" "not a valid"
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
{ make_body 6500; make_sources; } > "$RUN/02-draft.md"
{ make_body 6500; make_sources; } > "$RUN/03-edited.md"
echo "memo" > "$RUN/03-editorial-memo.md"
{ make_body 6500; make_sources; } > "$RUN/04-article.md"
# Build a structurally valid .docx: a ZIP containing word/document.xml
BUILD="$(mktemp -d)"
mkdir -p "$BUILD/word"
echo '<?xml version="1.0"?><w:document/>' > "$BUILD/word/document.xml"
(cd "$BUILD" && zip -qr "$RUN/04-article.docx" .)
rm -rf "$BUILD"
assert "complete run → allow" 0 "$(run_gate "$TMP")"

# --- Regression: a REAL Word file, not a hand-built fixture ---------------
# A small synthetic ZIP hides a SIGPIPE/pipefail bug in the validity check, because
# `unzip` finishes writing its short listing before `grep` can exit early. Only a
# genuine document's longer listing exposes it. Render one and run the gate for real.

# The renderer sits at scripts/ relative to the plugin root when this ships as a plugin,
# and relative to the repo root when run from a checkout. Try both. Use the render-docx.sh
# wrapper rather than the raw .js: on a fresh plugin install the `docx` package is absent,
# and only the wrapper installs it.
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RENDERER=""
for candidate in \
  "$HOOK_DIR/../scripts/render-docx.sh" \
  "$HOOK_DIR/../../scripts/render-docx.sh"
do
  [ -f "$candidate" ] && { RENDERER="$candidate"; break; }
done

if [ -n "$RENDERER" ] && command -v node > /dev/null; then
  new_workspace
  { make_body 1500; make_sources; } > "$RUN/01-research.md"
  { make_body 6500; make_sources; } > "$RUN/02-draft.md"
  { make_body 6500; make_sources; } > "$RUN/03-edited.md"
  echo "memo" > "$RUN/03-editorial-memo.md"
  {
    echo '---'
    echo 'title: Regression Fixture'
    echo 'author: James Gray'
    echo '---'
    echo
    echo '## Body'
    echo
    make_body 6500
    make_sources
  } > "$RUN/04-article.md"
  bash "$RENDERER" "$RUN/04-article.md" "$RUN/04-article.docx" > /dev/null 2>&1
  assert "real rendered .docx → allow" 0 "$(run_gate "$TMP")"
  # $TMP is left in place so the audit-trail check below inspects this run's log.
else
  echo "  skip  real .docx regression (node or renderer unavailable)"
fi

# --- Audit trail ----------------------------------------------------------

if [ -s "$RUN/run-log.md" ]; then
  echo "  ok    run-log.md written"
  PASS=$((PASS + 1))
else
  echo "  FAIL  run-log.md was not written"
  FAIL=$((FAIL + 1))
fi

# SubagentStop fires several times per agent. The first live run logged 10 lines for
# 4 stages, which buried the shape of the run. Repeated passes with an unchanged
# artifact set must not add lines.
BEFORE=$(grep -c 'gate passed' "$RUN/run-log.md")
run_gate "$TMP" > /dev/null
run_gate "$TMP" > /dev/null
AFTER=$(grep -c 'gate passed' "$RUN/run-log.md")
if [ "$BEFORE" = "$AFTER" ]; then
  echo "  ok    repeated passes do not duplicate log lines ($AFTER entries)"
  PASS=$((PASS + 1))
else
  echo "  FAIL  log grew from $BEFORE to $AFTER on unchanged artifacts"
  FAIL=$((FAIL + 1))
fi

# Hooks run in parallel. A real run produced two identical log lines because two events
# in the same second both read the old last line before either appended. Fire several
# concurrently and assert the log does not grow.
CONCURRENT_BEFORE=$(grep -c 'gate passed' "$RUN/run-log.md")
for _ in 1 2 3 4 5 6; do
  printf '{"cwd":"%s","hook_event_name":"SubagentStop","stop_hook_active":false}' "$TMP" \
    | bash "$GATE" 2>/dev/null &
done
wait
CONCURRENT_AFTER=$(grep -c 'gate passed' "$RUN/run-log.md")
if [ "$CONCURRENT_BEFORE" = "$CONCURRENT_AFTER" ]; then
  echo "  ok    concurrent hook invocations do not duplicate log lines"
  PASS=$((PASS + 1))
else
  echo "  FAIL  concurrent invocations grew the log $CONCURRENT_BEFORE → $CONCURRENT_AFTER"
  FAIL=$((FAIL + 1))
fi

# The lock must never be left behind — a stale lock would silence the log for the rest
# of the run.
if [ ! -d "$RUN/.log.lock" ]; then
  echo "  ok    no stale lock left behind"
  PASS=$((PASS + 1))
else
  echo "  FAIL  .log.lock was not released"
  FAIL=$((FAIL + 1))
fi

# The concurrency test above is timing-dependent and will not reliably reproduce the
# race, so assert the mechanism directly: while the lock is held, no other invocation
# may write. Combined with mkdir being atomic, that is what makes the fix correct.
mkdir -p "$RUN/.log.lock"
HELD_BEFORE=$(grep -c 'gate passed' "$RUN/run-log.md")
# The state change must be one that PASSES every rule, or the gate blocks before it ever
# reaches the logging code and the test proves nothing. Removing both deliverables leaves
# a valid mid-pipeline state with a different artifact set.
mv "$RUN/04-article.md" "$TMP/held-article.md"
mv "$RUN/04-article.docx" "$TMP/held-article.docx"
run_gate "$TMP" > /dev/null
HELD_AFTER=$(grep -c 'gate passed' "$RUN/run-log.md")
rmdir "$RUN/.log.lock"
mv "$TMP/held-article.md" "$RUN/04-article.md"
mv "$TMP/held-article.docx" "$RUN/04-article.docx"
if [ "$HELD_BEFORE" = "$HELD_AFTER" ]; then
  echo "  ok    a held lock prevents a concurrent write (critical section respected)"
  PASS=$((PASS + 1))
else
  echo "  FAIL  wrote to the log while the lock was held — the critical section is not enforced"
  FAIL=$((FAIL + 1))
fi

# But a genuine new stage must still be recorded.
#
# "A new stage" means the ARTIFACT SET changes — that is what the log dedups on. Writing
# a new file outside the six tracked artifacts, or rewriting one already logged, is
# correctly suppressed, so neither proves anything here. Removing both deliverables
# leaves the same valid mid-pipeline state the held-lock test used, and that set differs
# from the last line written.
GENUINE_BEFORE=$(grep -c 'gate passed' "$RUN/run-log.md")
mv "$RUN/04-article.md" "$TMP/final-article.md"
mv "$RUN/04-article.docx" "$TMP/final-article.docx"
run_gate "$TMP" > /dev/null
FINAL=$(grep -c 'gate passed' "$RUN/run-log.md")
mv "$TMP/final-article.md" "$RUN/04-article.md"
mv "$TMP/final-article.docx" "$RUN/04-article.docx"
# -gt, not -ge. The claim is that a genuine new stage is still recorded, so the log must
# GROW. `-ge` is also satisfied when it does not grow at all, which is exactly the
# regression this assertion exists to catch — it would pass even if logging broke
# completely.
if [ "$FINAL" -gt "$GENUINE_BEFORE" ]; then
  echo "  ok    log still records real stage changes"
  PASS=$((PASS + 1))
else
  echo "  FAIL  log stopped recording changes"
  FAIL=$((FAIL + 1))
fi
rm -rf "$TMP"

# --- Bounded retries --------------------------------------------------------
# A failing agent is sent back at most twice. Its next failing stop is let through, but
# recorded as QUALITY GATE FAILED in run-log.md and shown to the person via the
# documented systemMessage JSON — never passed silently, and never looped.

# $1 = agent_id ("" to omit), $2 = stop_hook_active. Stdout lands in $TMP/stdout.
stop_as() {
  local id_field=""
  [ -n "$1" ] && id_field="\"agent_id\":\"$1\","
  printf '{"session_id":"t","cwd":"%s","hook_event_name":"SubagentStop",%s"stop_hook_active":%s}' \
    "$TMP" "$id_field" "$2" | bash "$GATE" >"$TMP/stdout" 2>"$TMP/stderr"
  echo $?
}

check() {
  # $1 = name, $2 = condition result (0 = true)
  if [ "$2" -eq 0 ]; then echo "  ok    $1"; PASS=$((PASS + 1)); else echo "  FAIL  $1"; FAIL=$((FAIL + 1)); fi
}

new_workspace
echo "too short" > "$RUN/01-research.md"
assert "first failing stop → send-back 1 of 2" 2 "$(stop_as agent-a false)" "send-back 1 of 2"
assert "retry 1 still failing → send-back 2 of 2" 2 "$(stop_as agent-a true)" "send-back 2 of 2"
grep -q "last attempt" "$TMP/stderr"; check "the final send-back warns it is the last attempt" $?
assert "retry 2 still failing → limit reached, agent may finish" 0 "$(stop_as agent-a true)"
grep -q '"systemMessage"' "$TMP/stdout" && grep -q 'QUALITY GATE FAILED after 2 retries' "$TMP/stdout"
check "limit reached → systemMessage shown to the person" $?
node -e 'JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"))' "$TMP/stdout" 2>/dev/null
check "limit-reached output is valid JSON" $?
grep -q 'QUALITY GATE FAILED after 2 retries: 01-research.md is too thin' "$RUN/run-log.md"
check "limit reached → failure and reason recorded in run-log.md" $?
# No infinite loop: however many more times the agent stops, it is never blocked again,
# and the failure is logged once, not once per stop.
LOOPED=0
for _ in 1 2 3 4 5 6 7 8 9 10; do
  [ "$(stop_as agent-a true)" = "0" ] || LOOPED=1
done
check "ten further stops are never blocked (no loop)" "$LOOPED"
[ "$(grep -c 'QUALITY GATE FAILED' "$RUN/run-log.md")" = "1" ]
check "the failure is logged once, not once per stop" $?
# Budgets are per agent: a different agent in the same run is still checked in full.
assert "another agent in the same run still gets its own send-backs" 2 "$(stop_as agent-b false)" "send-back 1 of 2"
rm -rf "$TMP"

# Fixing the work after a send-back passes, and clears that agent's counter.
new_workspace
echo "too short" > "$RUN/01-research.md"
stop_as agent-c false > /dev/null
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
assert "fixed after one send-back → allow" 0 "$(stop_as agent-c true)"
[ ! -f "$RUN/.gate-send-backs-agent-c" ]; check "a pass clears the agent's send-back counter" $?
! grep -q 'QUALITY GATE FAILED' "$RUN/run-log.md"; check "a fixed stage records no failure" $?
rm -rf "$TMP"

# No agent_id in the payload: one counter for the run, reset by any stop that is not a
# hook-driven continuation — still bounded.
new_workspace
echo "too short" > "$RUN/01-research.md"
assert "no agent_id: first stop → send-back 1" 2 "$(stop_as "" false)" "send-back 1 of 2"
assert "no agent_id: retry 1 → send-back 2" 2 "$(stop_as "" true)" "send-back 2 of 2"
assert "no agent_id: retry 2 → limit reached" 0 "$(stop_as "" true)"
assert "no agent_id: a fresh stop starts a new budget" 2 "$(stop_as "" false)" "send-back 1 of 2"
rm -rf "$TMP"

# A workspace the gate cannot write to must not become a loop: if the counter cannot be
# saved, it gives up (visibly) instead of blocking with a count that never advances.
# Skipped when running as root, where permissions do not bite.
if [ "$(id -u)" != "0" ]; then
  new_workspace
  chmod 555 "$RUN"
  assert "unwritable workspace → no block loop" 0 "$(stop_as agent-d false)"
  grep -q 'QUALITY GATE FAILED' "$TMP/stdout"; check "unwritable workspace → failure still shown" $?
  chmod 755 "$RUN"
  rm -rf "$TMP"
fi

# --- Node.js missing ------------------------------------------------------
# The gate reads the payload with Node.js, its only parser. Without Node it
# must still run every check — no silent pass — keep the retry budget bounded, and tell
# the person once per run. Run it on a PATH holding only the tools the gate uses.
NO_NODE_BIN="$(mktemp -d)"
for tool in bash cat tr cut rm date wc grep sed tail mkdir rmdir sleep unzip; do
  src="$(command -v "$tool" 2>/dev/null)" && [ -x "$src" ] && ln -s "$src" "$NO_NODE_BIN/$tool"
done

stop_no_node() {
  printf '{"session_id":"t","cwd":"%s","hook_event_name":"SubagentStop","agent_id":"x","stop_hook_active":%s}' "$TMP" "$1" \
    | CLAUDE_PROJECT_DIR="$TMP" PATH="$NO_NODE_BIN" "$NO_NODE_BIN/bash" "$GATE" >"$TMP/stdout" 2>"$TMP/stderr"
  echo $?
}

new_workspace
echo "too short" > "$RUN/01-research.md"
assert "no Node: checks still run → send-back 1" 2 "$(stop_no_node false)" "01-research.md"
grep -q "Node.js" "$TMP/stderr"; check "no Node: the send-back mentions Node.js" $?
grep -q 'NOTE: Node.js not found' "$RUN/run-log.md"; check "no Node: recorded in run-log.md" $?
assert "no Node: retry 1 → send-back 2" 2 "$(stop_no_node true)" "send-back 2 of 2"
assert "no Node: retry 2 → limit reached, no loop" 0 "$(stop_no_node true)"
grep -q 'QUALITY GATE FAILED' "$TMP/stdout"; check "no Node: limit-reached systemMessage shown" $?
[ "$(stop_no_node true)" = "0" ]; check "no Node: further stops are not blocked" $?
[ "$(grep -c 'NOTE: Node.js not found' "$RUN/run-log.md")" = "1" ]
check "no Node: the notice is logged once per run" $?
rm -rf "$TMP"

new_workspace
{ make_body 1500; make_sources; } > "$RUN/01-research.md"
assert "no Node: valid work → allow" 0 "$(stop_no_node false)"
grep -q '"systemMessage".*Node.js is not installed' "$TMP/stdout"
check "no Node: a passing stop still tells the person Node.js is missing" $?
stop_no_node false > /dev/null
[ ! -s "$TMP/stdout" ]; check "no Node: the on-screen notice is shown once per run" $?
rm -rf "$TMP" "$NO_NODE_BIN"

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
