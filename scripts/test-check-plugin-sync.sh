#!/usr/bin/env bash
# Tests for the distributed-repo mode of scripts/check-plugin-sync.sh and the drift
# gate in scripts/sync-plugins.sh (issue #225).
#
# Every assertion here was watched fail against a deliberately drifted tree before the
# implementation made it pass. The check this suite guards was rewritten twice in one
# week because it passed while proving nothing — a test that cannot go red is the exact
# failure mode this file exists to prevent, so keep that discipline when extending it.
#
# The distributed repo is faked in a temp dir via HANDSONAI_PLUGINS_DIR; the canonical
# side is the real plugins/handsonai in this repo, copied fresh before each case and
# mutated only on the fake distributed side. HOME is also pointed at the temp dir for
# every sync-plugins.sh invocation as a belt-and-braces guard: even a regression that
# ignores HANDSONAI_PLUGINS_DIR cannot reach the real ~/Code/jamesgray/handsonai-plugins.
#
# Run: bash scripts/test-check-plugin-sync.sh

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECK="$ROOT/scripts/check-plugin-sync.sh"
SYNC="$ROOT/scripts/sync-plugins.sh"
CANON="$ROOT/plugins/handsonai"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
FAKE="$TMP/handsonai-plugins"
FAKE_HOME="$TMP/home"
mkdir -p "$FAKE_HOME"
PASS=0
FAIL=0

ok()   { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }
skip() { echo "  skip  $1"; }

command -v jq > /dev/null || { echo "jq is required to run these tests (brew install jq)"; exit 1; }

# A fresh, perfectly synced fake distributed repo, including the marketplace.json that
# sync-plugins.sh needs to get past its preflight.
reset_fake() {
  rm -rf "$FAKE"
  mkdir -p "$FAKE/plugins" "$FAKE/.claude-plugin"
  cp -R "$CANON" "$FAKE/plugins/handsonai"
  local v
  v="$(jq -r '.version' "$CANON/.claude-plugin/plugin.json")"
  jq -n --arg v "$v" '{name: "handsonai", version: "9.0.0",
    plugins: [{name: "handsonai", source: "./plugins/handsonai",
               description: "fixture", version: $v}]}' \
    > "$FAKE/.claude-plugin/marketplace.json"
}

run_check() {  # $1 = plugin arg; output lands in $TMP/out, exit code in $RC
  HANDSONAI_PLUGINS_DIR="$FAKE" bash "$CHECK" "$1" > "$TMP/out" 2>&1
  RC=$?
}

echo "check-plugin-sync.sh — distributed mode"

# --- In sync --------------------------------------------------------------

reset_fake
run_check handsonai
if [ "$RC" -eq 0 ] && grep -qi 'in sync' "$TMP/out"; then
  ok "freshly synced trees pass"
else
  bad "freshly synced trees should pass (exit $RC): $(tail -1 "$TMP/out")"
fi

# --- Content drift ---------------------------------------------------------

reset_fake
DRIFT_FILE="$(cd "$FAKE/plugins/handsonai" && find skills -name 'SKILL.md' | sort | head -1)"
echo "drifted line for test" >> "$FAKE/plugins/handsonai/$DRIFT_FILE"
run_check handsonai
if [ "$RC" -eq 1 ] && grep -q "DRIFTED" "$TMP/out" && grep -qF "$DRIFT_FILE" "$TMP/out"; then
  ok "a modified distributed file is reported as DRIFTED"
else
  bad "content drift in $DRIFT_FILE not reported (exit $RC)"
fi

# --- File missing from the distributed copy (the #225 incident) -------------

reset_fake
rm "$FAKE/plugins/handsonai/$DRIFT_FILE"
run_check handsonai
if [ "$RC" -eq 1 ] && grep -q "MISSING in distributed" "$TMP/out" && grep -qF "$DRIFT_FILE" "$TMP/out"; then
  ok "a file absent from the distributed copy is reported"
else
  bad "missing distributed file not reported (exit $RC)"
fi

# --- File only in the distributed copy (rsync --delete would destroy it) ----

reset_fake
echo "orphan" > "$FAKE/plugins/handsonai/skills/orphan-note.md"
run_check handsonai
if [ "$RC" -eq 1 ] && grep -q "MISSING in canonical" "$TMP/out" && grep -qi "delete" "$TMP/out"; then
  ok "a distributed-only file is reported, with a deletion warning"
else
  bad "distributed-only file not reported with deletion warning (exit $RC)"
fi

# --- plugin.json version special case ---------------------------------------

reset_fake
jq '.version = "0.0.1"' "$FAKE/plugins/handsonai/.claude-plugin/plugin.json" > "$TMP/pj" \
  && mv "$TMP/pj" "$FAKE/plugins/handsonai/.claude-plugin/plugin.json"
run_check handsonai
if [ "$RC" -eq 0 ] && grep -qi "version" "$TMP/out" && grep -qF "0.0.1" "$TMP/out"; then
  ok "a version-only plugin.json difference is a note, not drift"
else
  bad "version-only plugin.json difference mishandled (exit $RC)"
fi

# A LOWER distributed version is the benign mid-release shape. A HIGHER one means the
# distributed copy is ahead of canonical (a reverted bump, or a direct edit), and letting
# it through as a note would let sync-plugins silently DOWNGRADE the published version.
reset_fake
jq '.version = "99.0.0"' "$FAKE/plugins/handsonai/.claude-plugin/plugin.json" > "$TMP/pj" \
  && mv "$TMP/pj" "$FAKE/plugins/handsonai/.claude-plugin/plugin.json"
run_check handsonai
if [ "$RC" -eq 1 ] && grep -qi "newer\|ahead\|downgrade" "$TMP/out"; then
  ok "a distributed version AHEAD of canonical is drift, not a note"
else
  bad "distributed-ahead version should be drift — syncing would downgrade the published plugin (exit $RC)"
fi

reset_fake
jq '.description = "tampered"' "$FAKE/plugins/handsonai/.claude-plugin/plugin.json" > "$TMP/pj" \
  && mv "$TMP/pj" "$FAKE/plugins/handsonai/.claude-plugin/plugin.json"
run_check handsonai
if [ "$RC" -eq 1 ] && grep -q "DRIFTED" "$TMP/out" && grep -q "plugin.json" "$TMP/out"; then
  ok "a non-version plugin.json difference is still drift"
else
  bad "non-version plugin.json drift not reported (exit $RC)"
fi

# --- Skips ------------------------------------------------------------------

HANDSONAI_PLUGINS_DIR="$TMP/nowhere" bash "$CHECK" handsonai > "$TMP/out" 2>&1
RC=$?
if [ "$RC" -eq 0 ] && grep -qi "skip" "$TMP/out"; then
  ok "missing distributed clone skips with a message instead of failing"
else
  bad "missing distributed clone should skip (exit $RC): $(tail -1 "$TMP/out")"
fi

reset_fake
rm -rf "$FAKE/plugins/handsonai"
run_check handsonai
if [ "$RC" -eq 0 ] && grep -qi "never .*synced\|not .*synced\|skip" "$TMP/out"; then
  ok "a plugin never synced to the distributed repo skips with a message"
else
  bad "never-synced plugin should skip (exit $RC): $(tail -1 "$TMP/out")"
fi

# --- Usage errors and back-compat -------------------------------------------

reset_fake
run_check no-such-plugin
if [ "$RC" -eq 2 ]; then
  ok "an unknown plugin name is a usage error (exit 2), not a pass or drift"
else
  bad "unknown plugin should exit 2, got $RC"
fi

# Assert the mirror mode's exclusive header, not just the plugin name — distributed-mode
# output also contains "multi-agent-example", so the loose grep passed even if a
# mode-routing regression sent the no-arg case down the distributed path. Pinning
# HANDSONAI_PLUGINS_DIR to nowhere makes that regression produce a SKIPPED message
# (exit 0) instead of a plausible distributed run, so the header assertion must miss.
HANDSONAI_PLUGINS_DIR="$TMP/nowhere" bash "$CHECK" > "$TMP/out" 2>&1
RC=$?
if [ "$RC" -le 1 ] && grep -q "multi-agent-example: repo vs plugin" "$TMP/out"; then
  ok "no-argument invocation still runs the multi-agent-example mirror check"
else
  bad "no-argument invocation no longer runs the mirror check (exit $RC): $(head -1 "$TMP/out")"
fi

# --- sync-plugins.sh drift gate ---------------------------------------------

echo
echo "sync-plugins.sh — drift gate"

CANON_PJ="$CANON/.claude-plugin/plugin.json"
CANON_VERSION="$(jq -r '.version' "$CANON_PJ")"

run_sync() {  # env overrides come via leading VAR=... args to env
  env HOME="$FAKE_HOME" HANDSONAI_PLUGINS_DIR="$FAKE" "$@" \
    bash "$SYNC" handsonai patch < /dev/null > "$TMP/out" 2>&1
  RC=$?
}

# Every gate test can touch the real, tracked canonical plugin.json — the acknowledge
# and clean-state paths bump it by design, and even the refusal path's failure recovery
# must be able to restore it. So the whole section is gated on that file being clean in
# git (a restore must never discard a developer's uncommitted edits), and the restore
# lives in the EXIT trap, not in sequential statements a Ctrl-C could land between.
if [ -n "$(git -C "$ROOT" status --porcelain -- plugins/handsonai/.claude-plugin/plugin.json)" ]; then
  skip "all gate tests (canonical plugin.json has uncommitted changes — commit or revert first)"
else
  trap 'git -C "$ROOT" checkout -- plugins/handsonai/.claude-plugin/plugin.json; rm -rf "$TMP"' EXIT

  reset_fake
  echo "drifted line for test" >> "$FAKE/plugins/handsonai/$DRIFT_FILE"
  run_sync
  if [ "$RC" -ne 0 ] && grep -qi "drift" "$TMP/out"; then
    ok "unacknowledged drift refuses to sync"
  else
    bad "sync should refuse on unacknowledged drift (exit $RC)"
  fi
  if [ "$(jq -r '.version' "$CANON_PJ")" = "$CANON_VERSION" ] \
     && grep -q "drifted line for test" "$FAKE/plugins/handsonai/$DRIFT_FILE"; then
    ok "refusal leaves both trees untouched"
  else
    bad "refusal mutated the canonical plugin.json or the distributed tree"
  fi

  reset_fake
  echo "drifted line for test" >> "$FAKE/plugins/handsonai/$DRIFT_FILE"
  run_sync SYNC_ACK_DRIFT=1
  if [ "$RC" -eq 0 ] && ! grep -q "drifted line for test" "$FAKE/plugins/handsonai/$DRIFT_FILE"; then
    ok "SYNC_ACK_DRIFT=1 acknowledges the drift and the sync proceeds"
  else
    bad "acknowledged sync should proceed and overwrite the drift (exit $RC)"
  fi
  # Restore between tests so the next case computes against the committed version;
  # safe because the section only runs when the file started clean.
  git -C "$ROOT" checkout -- "plugins/handsonai/.claude-plugin/plugin.json"

  reset_fake
  run_sync
  if [ "$RC" -eq 0 ]; then
    ok "an in-sync state syncs without needing acknowledgment"
  else
    bad "in-sync state should not be gated (exit $RC): $(grep -i error "$TMP/out" | head -1)"
  fi
fi

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
