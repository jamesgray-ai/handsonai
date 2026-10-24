#!/usr/bin/env bash
# Tests for scripts/framework/test-run.sh, the framework's wrapper for headless Claude
# Code sessions (build-task-list T16; rules 8.4, 8.5, 8.7, 8.11).
#
# No live model: a stub `claude` on PATH records every call (arguments, stdin, the
# environment it was given) and replays a scripted stream-json start-up message. Each
# case builds a throwaway workspace in a temp dir; nothing touches the real ~/.claude.
# Every assertion here should go red when the guard it covers is removed: keep that
# discipline when extending it.
#
# Run: bash scripts/test-test-run.sh

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANON="$ROOT/scripts/framework/test-run.sh"
KIT_DOCS=("$ROOT/plugins/handsonai/skills/build/references/claude-code-block.md"
          "$ROOT/plugins/handsonai/skills/test/references/claude-code-runs.md")
TMP="$(cd "$(mktemp -d)" && pwd -P)"
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0
ok()  { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }
expect_rc() { if [ "$RC" = "$1" ]; then ok "$2"; else bad "$2 (exit $RC, wanted $1): $(head -c 400 "$TMP/err")"; fi; }
has()   { if grep -qF -- "$1" "$2"; then ok "$3"; else bad "$3"; fi; }
hasnt() { if grep -qF -- "$1" "$2"; then bad "$3"; else ok "$3"; fi; }

WS="$TMP/ws"; PLUGIN="$TMP/plugin/skills/test/scripts"; STUB="$TMP/stub"; RUNS="$TMP/runs"
SID="0b6c3f2e-1a2b-4c3d-8e9f-0a1b2c3d4e5f"
FAKE_SECRET="fakevalue-$$-not-a-real-token"

write_stub() {
  mkdir -p "$STUB"
  cat > "$STUB/claude" <<'STUBEOF'
#!/bin/bash
D="$(cd "$(dirname "$0")" && pwd -P)"
if [ "${1:-}" = "--version" ]; then echo "2.1.309 (Claude Code)"; exit 0; fi
{ for a in "$@"; do printf '%s\n' "$a"; done; echo "----"; } >> "$D/calls.log"
{ cat; echo; echo "----"; } >> "$D/stdin.log"
env >> "$D/env.log"; echo "----" >> "$D/env.log"
sed "s#__CWD__#$(pwd -P)#g" "$D/stream.jsonl"
exit 0
STUBEOF
  chmod +x "$STUB/claude"
}

INIT_TOOLS='"Read","Glob","Grep","Skill","ToolSearch","Write","Edit","mcp__crm__list_records","mcp__crm__get_record","mcp__crm__fetch_url","mcp__crm__update_record"'
DEFAULT_SERVERS='[{"name":"crm","status":"connected"}]'
DEFAULT_EXTRA='"skills":["wf-a-skill"],"plugins":[]'
stream() {  # $1 = tools json list body, $2 = mode, $3 = servers json, $4 = extra init fields
  local tools="${1:-$INIT_TOOLS}" mode="${2:-dontAsk}"
  local servers="${3:-$DEFAULT_SERVERS}" extra="${4:-$DEFAULT_EXTRA}"
  printf '{"type":"system","subtype":"init","session_id":"%s","cwd":"__CWD__","permissionMode":"%s","tools":[%s],"mcp_servers":%s,%s}\n' \
    "$SID" "$mode" "$tools" "$servers" "$extra" > "$STUB/stream.jsonl"
  printf '{"type":"assistant","message":{"content":[{"type":"text","text":"READY"}]}}\n{"type":"result","subtype":"success","is_error":false,"result":"Practice run: nothing will be sent or changed.","session_id":"%s"}\n' "$SID" >> "$STUB/stream.jsonl"
}

PROFILE_A='version 1
workflow wf-a
connection crm stdio npx -y crm-mcp-server
connection_env crm CRM_TOKEN
tool crm read mcp__crm__list_records | Lists records in the CRM. Read-only; does not modify anything.
tool crm read mcp__crm__get_record | Gets one record by its id
tool crm read mcp__crm__fetch_url | Fetches any URL with any HTTP method
tool crm write mcp__crm__update_record | Updates a record
skill .claude/skills/wf-a-skill
context context/C1-roster.md
headless_writes practice'

record() {  # $1 slug, $2 write_block yaml, $3 fingerprint, $4 profile body
  local fp="$3"
  mkdir -p "$WS/framework/$1/inputs"
  {
    echo "---"; echo "workflow: $1"; printf '%s\n' "$2"
    if [ -n "$fp" ]; then echo "fingerprints:"; echo "  wrapper: sha256:$fp"; fi
    echo "---"; echo "# Build record"; echo; echo "## Claude Code profile"; echo
    echo '```framework-profile'; printf '%s\n' "$4"; echo '```'
  } > "$WS/framework/$1/build-record.md"
  printf -- '---\nworkflow: %s\nplatform: claude-code\n---\nUses the CRM connection (crm).\n' "$1" > "$WS/framework/$1/design-plan.md"
}

BLOCK_ON_A='write_block:
  on:
    - mcp__crm__update_record
    - mcp__crm__fetch_url
    - Bash(claude:*)
    - Bash(claude *)
  leader_rules: []
  leader_allow: []'

fresh() {  # a clean workspace with workflow wf-a, the wrapper, the plugin copy and the stub
  rm -rf "$WS" "$TMP/plugin" "$STUB" "$RUNS"
  mkdir -p "$WS/framework/.bin" "$PLUGIN" "$WS/.claude/skills/wf-a-skill" "$WS/context" "$RUNS"
  cp "$CANON" "$WS/framework/.bin/test-run.sh"; cp "$CANON" "$PLUGIN/test-run.sh"
  HASH="$(shasum -a 256 "$CANON" | cut -d' ' -f1)"
  record wf-a "$BLOCK_ON_A" "$HASH" "$PROFILE_A"
  printf -- '---\nname: wf-a-skill\ndescription: test\n---\nbody\n' > "$WS/.claude/skills/wf-a-skill/SKILL.md"
  echo "roster" > "$WS/context/C1-roster.md"
  printf 'source: deconstruct\ntests: AC1, R2\n\nThe input text for E1.\n' > "$WS/framework/wf-a/inputs/E1-sample.md"
  echo "Practice run. Run the workflow on the input in input/." > "$TMP/prompt.md"
  write_stub; stream
}

W() {  # run the workspace copy of the wrapper; stdout to $TMP/out, stderr to $TMP/err
  ( cd "$WS" && env -i HOME="$TMP/home" PATH="$STUB:/usr/bin:/bin" TMPDIR="$RUNS" \
      CRM_TOKEN="$FAKE_SECRET" LEAK_ME="should-not-pass" \
      bash framework/.bin/test-run.sh "$@" ) > "$TMP/out" 2> "$TMP/err"
  RC=$?
}
calls() { [ -f "$STUB/calls.log" ] && grep -c '^----$' "$STUB/calls.log" || echo 0; }

echo "test-run.sh: refusals (no session may start)"
fresh
for flags in "--dangerously-skip-permissions" "--allow-dangerously-skip-permissions" \
             "--permission-mode acceptEdits" "--permission-mode=bypassPermissions" \
             "--permission-prompts host"; do
  # shellcheck disable=SC2086
  W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" $flags
  expect_rc 2 "refuses $flags"
done
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "--dangerously-skip-permissions"
expect_rc 2 "refuses a bypass flag smuggled in as a value"
for flags in "--settings x.json" "--mcp-config x.json" "--tools Bash" "--allowedTools Bash" \
             "--model opus" "-p" "--add-dir /" "--plugin-dir /tmp" "--bare" "--safe-mode"; do
  # shellcheck disable=SC2086
  W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" $flags
  expect_rc 2 "refuses a Claude Code flag the profile owns: $flags"
done
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --resume not-a-uuid --run-folder /tmp
expect_rc 2 "refuses a resume that isn't a session id"
W test wf-a --prompt-file "$TMP/prompt.md"
expect_rc 2 "refuses without the plugin's copy to check the fingerprint against"
W
expect_rc 2 "refuses no arguments (bash 3.2 safe)"
W test "../etc" --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 2 "refuses a slug that isn't one"
echo "Do the thing." > "$TMP/nocue.md"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/nocue.md"
expect_rc 2 "refuses a prompt without the practice-run cue"
if [ "$(calls)" = 0 ]; then ok "claude was never started by a refused call"; else bad "claude started on a refused call"; fi

echo "test-run.sh: fingerprint (fails closed)"
fresh
record wf-a "$BLOCK_ON_A" "$(printf '0%.0s' {1..64})" "$PROFILE_A"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 4 "record's fingerprint doesn't match"
fresh
echo "# drift" >> "$PLUGIN/test-run.sh"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 4 "plugin's own copy doesn't match"
fresh
echo "# drift" >> "$PLUGIN/test-run.sh"
record wf-a "$BLOCK_ON_A" "$(printf 'a%.0s' {1..64})" "$PROFILE_A"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 4 "matches neither the record nor the plugin's copy"
fresh
record wf-a "$BLOCK_ON_A" "" "$PROFILE_A"
W block-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
expect_rc 4 "no fingerprint in the record"
fresh
echo "# edited in the workspace" >> "$WS/framework/.bin/test-run.sh"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 4 "an edited workspace copy"
fresh
cp "$CANON" "$WS/plugin-copy.sh"
W test wf-a --plugin-copy "$WS/plugin-copy.sh" --prompt-file "$TMP/prompt.md"
expect_rc 4 "a 'plugin copy' inside the workspace isn't accepted"
fresh
mkdir -p "$WS/elsewhere"; cp "$CANON" "$WS/elsewhere/test-run.sh"
( cd "$WS" && env -i HOME="$TMP/home" PATH="$STUB:/usr/bin:/bin" TMPDIR="$RUNS" bash elsewhere/test-run.sh test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" ) > "$TMP/out" 2> "$TMP/err"; RC=$?
expect_rc 4 "runs only from framework/.bin/"
if [ "$(calls)" = 0 ]; then ok "claude was never started on a fingerprint failure"; else bad "claude started despite a fingerprint failure"; fi

echo "test-run.sh: a session that passes its start-up check"
fresh
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --input framework/wf-a/inputs/E1-sample.md
expect_rc 0 "test profile runs"
has "startup_check: passed" "$TMP/out" "reports the start-up check"
RUN="$(sed -n 's/^run_folder: //p' "$TMP/out")"
[ -n "$RUN" ] && [ -d "$RUN" ] && ok "reports its run folder" || bad "no run folder reported"
CFG="$RUN.config"
[ "$(calls)" = 2 ] && ok "a probe, then the real session" || bad "expected 2 claude calls, got $(calls)"
for f in --restricted --strict-mcp-config --include-hook-events dontAsk --permission-prompts none; do
  has "$f" "$STUB/calls.log" "passes $f"
done
hasnt "dangerously" "$STUB/calls.log" "never passes a bypass flag"
has "--no-session-persistence" "$STUB/calls.log" "the probe leaves no session behind"
head -1 "$STUB/stdin.log" | grep -qF "READY" && ok "the probe's prompt goes first" || bad "the probe didn't go first"
python3 - "$CFG/settings.json" <<'EOF' && ok "settings: writes and the mixed tool denied, never allowed; reads allowed; hooks off" || bad "settings content"
import json, sys
s = json.load(open(sys.argv[1])); p = s["permissions"]
assert p["defaultMode"] == "dontAsk" and s["disableAllHooks"] is True
for w in ("mcp__crm__update_record", "mcp__crm__fetch_url"):
    assert w in p["deny"] and not any(a.startswith(w) for a in p["allow"]), w
for r in ("mcp__crm__list_records", "mcp__crm__get_record"):
    assert r in p["allow"], r
assert "Bash" in p["deny"] and "WebFetch" in p["deny"]
assert all("practice/**" in a for a in p["allow"] if a.startswith(("Write", "Edit")))
EOF
has '"CRM_TOKEN": "${CRM_TOKEN}"' "$CFG/mcp.json" "connection config names the environment variable"
if grep -rqF "$FAKE_SECRET" "$CFG" "$RUN" "$TMP/out" "$TMP/err"; then bad "the secret's value was written or printed"; else ok "the secret's value is never written or printed"; fi
grep -q "^CRM_TOKEN=" "$STUB/env.log" && ok "the named variable reaches the session" || bad "named variable missing"
grep -q "^LEAK_ME=" "$STUB/env.log" && bad "an unnamed variable leaked into the session" || ok "nothing else from the caller's environment passes"
if grep -q "^tests:" "$RUN/input/E1-sample.md" || grep -q "^source:" "$RUN/input/E1-sample.md"; then bad "the input's header reached the run"; else ok "the input's source/tests header is stripped"; fi
[ -f "$RUN/.claude/skills/wf-a-skill/SKILL.md" ] && ok "the workflow's skill is in the run folder" || bad "skill not copied"
[ -f "$RUN/context/C1-roster.md" ] && ok "its context is in the run folder" || bad "context not copied"
case "$RUN" in "$WS"*) bad "run folder inside the workspace";; *) ok "run folder outside the workspace";; esac

echo "test-run.sh: resume only through the same profile"
cp "$STUB/calls.log" "$TMP/calls.before"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --resume "$SID" --run-folder "$RUN"
expect_rc 0 "resume through the test profile"
has "$SID" "$STUB/calls.log" "passes the session id to --resume"
[ "$(calls)" = 4 ] && ok "the resume passes the start-up check again (probe + session)" || bad "resume didn't re-run the start-up check"
W check wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --resume "$SID" --run-folder "$RUN"
expect_rc 2 "a resume through another profile is refused"
mkdir -p "$RUNS/stray"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --resume "$SID" --run-folder "$RUNS/stray"
expect_rc 2 "a resume in a folder the wrapper didn't make is refused"

echo "test-run.sh: start-up check fails closed"
startup_case() {  # $1 label; stream already written
  fresh_keep_stream=1
  : > "$STUB/calls.log"; : > "$STUB/stdin.log"
  W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --input framework/wf-a/inputs/E1-sample.md
  expect_rc 3 "$1"
  if grep -qF "The input text for E1" "$STUB/stdin.log"; then bad "  ...and the real prompt was sent"; else ok "  ...and the real prompt was never sent"; fi
}
fresh; stream "$INIT_TOOLS,\"mcp__crm__delete_everything\""; startup_case "a tool neither allowed nor denied (added since the block)"
fresh; stream "$INIT_TOOLS,\"NewBuiltinTool\""; startup_case "an unknown built-in tool"
fresh; stream "" "default"; startup_case "the session isn't in the profile's permission mode"
fresh; stream "" "dontAsk" '[{"name":"crm","status":"connected"},{"name":"gmail","status":"connected"}]'; startup_case "a connection the profile doesn't hold"
fresh; stream "" "dontAsk" '[]'; startup_case "the workflow's connection didn't load"
fresh; stream "" "dontAsk" '[{"name":"crm","status":"failed"}]'; startup_case "the workflow's connection didn't connect"
fresh; stream "" "dontAsk" "" '"skills":["wf-a-skill"],"plugins":[{"name":"leader-plugin"}]'; startup_case "a plugin loaded"
fresh; stream "" "dontAsk" "" '"skills":["something-else"],"plugins":[]'; startup_case "the workflow's skill didn't load"
fresh; stream; { echo '{"type":"system","subtype":"hook_started","hook_name":"SessionStart"}'; cat "$STUB/stream.jsonl"; } > "$STUB/s2"; mv "$STUB/s2" "$STUB/stream.jsonl"; startup_case "a hook ran"
fresh; stream; { echo '{"type":"assistant","message":{}}'; cat "$STUB/stream.jsonl"; } > "$STUB/s2"; mv "$STUB/s2" "$STUB/stream.jsonl"; startup_case "the session acted before its start-up message"
fresh; echo '{"type":"result","result":"x"}' > "$STUB/stream.jsonl"; startup_case "no start-up message at all"

echo "test-run.sh: the profile is read from the record and checked against the plan"
fresh
record wf-a "write_block: off" "$HASH" "$PROFILE_A"
W check wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 5 "a check session refuses to run with the block off"
fresh
record wf-a "$BLOCK_ON_A" "$HASH" "${PROFILE_A/connection crm stdio npx -y crm-mcp-server/connection crm claude-ai}"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 7 "a claude.ai connector can't be passed headless: the leader runs those inputs"
fresh
record wf-a "$BLOCK_ON_A" "$HASH" "$PROFILE_A
connection mail stdio mail-server
tool mail read mcp__mail__list_threads | Lists threads"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 5 "a connection the plan doesn't name is refused"
fresh
record wf-a "$BLOCK_ON_A" "$HASH" "$PROFILE_A
command rm -rf"
printf 'Uses crm. Runs rm -rf.\n' >> "$WS/framework/wf-a/design-plan.md"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 5 "a command that can change things is never allowed"
fresh
record wf-a "$BLOCK_ON_A" "$HASH" "$PROFILE_A
command jq"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 5 "a command the plan doesn't name is refused"
fresh
record wf-a "$BLOCK_ON_A" "$HASH" "$PROFILE_A
context framework/wf-a/requirements.md"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 5 "context from the framework folder is refused"
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --input framework/wf-a/design-plan.md
expect_rc 5 "(record refused before the input is looked at)"
fresh
W test wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md" --input framework/wf-a/design-plan.md
expect_rc 2 "an input from outside inputs/ is refused"
leftover="$(find "$RUNS" -maxdepth 3 -name 'test-*' 2>/dev/null | wc -l | tr -d ' ')"
[ "$leftover" = 0 ] && ok "a refused session leaves no run folder behind" || bad "run folder left behind ($leftover)"

echo "test-run.sh: no secret's value is ever passed on"
secret_case() {  # $1 label, $2 profile, $3 the value that must not be echoed
  fresh; record wf-a "$BLOCK_ON_A" "$HASH" "$2"
  W block-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
  expect_rc 5 "$1"
  if grep -qF -- "$3" "$TMP/out" "$TMP/err"; then bad "  ...and the value was repeated"; else ok "  ...and the value isn't repeated"; fi
}
secret_case "a header holding a value" "$PROFILE_A
connection_header crm Authorization Bearer abcd1234efgh5678ijkl" "abcd1234efgh5678ijkl"
secret_case "an env entry holding a value" "$PROFILE_A
connection_env crm CRM_TOKEN=abcd1234efgh5678ijkl" "abcd1234efgh5678ijkl"
secret_case "a key in a command's arguments" "${PROFILE_A/crm-mcp-server/crm-mcp-server --key sk-ant-api03-abcdefghijklmnop}" "sk-ant-api03-abcdefghijklmnop"
secret_case "a long key-like literal" "${PROFILE_A/crm-mcp-server/crm-mcp-server A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8}" "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"

echo "test-run.sh: the read floor (block-rules)"
fresh
record wf-a "$BLOCK_ON_A" "$HASH" "$PROFILE_A
tool crm read mcp__crm__manage_contacts | Lists and manages contacts
tool crm read mcp__crm__search_deals
tool crm read mcp__crm__query_records | Runs a query; can also insert or update rows
tool crm read mcp__crm__get_record_history | Gets a record's history. It does not change anything."
W block-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
expect_rc 0 "block-rules runs"
python3 - "$TMP/out" <<'EOF' && ok "mixed and unproven tools are writes: denied, never on a check agent's list" || bad "read floor"
import json, sys
o = json.load(open(sys.argv[1]))
writes = {"mcp__crm__update_record", "mcp__crm__fetch_url", "mcp__crm__manage_contacts",
          "mcp__crm__search_deals", "mcp__crm__query_records"}
reads = {"mcp__crm__list_records", "mcp__crm__get_record", "mcp__crm__get_record_history"}
assert writes <= set(o["deny"]), set(o["deny"])
assert not (writes & set(o["check_agent_tools"])), o["check_agent_tools"]
assert set(o["check_agent_tools"]) == reads, o["check_agent_tools"]
assert {"Bash(claude:*)", "Bash(claude *)"} <= set(o["deny"])
assert {d["tool"] for d in o["demoted_to_write"]} == writes - {"mcp__crm__update_record"}
EOF
fresh
mkdir -p "$WS/.claude"
printf '{"permissions":{"deny":["mcp__crm__update_record","Bash(rm:*)"],"allow":["mcp__crm__list_records"]}}' > "$WS/.claude/settings.local.json"
record wf-a "write_block: off" "$HASH" "$PROFILE_A"
W block-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
python3 - "$TMP/out" <<'EOF' && ok "a rule the leader already had is recorded as theirs, never Build's" || bad "leader's rules"
import json, sys
o = json.load(open(sys.argv[1]))
assert o["leader_rules"] == ["mcp__crm__update_record"], o["leader_rules"]
assert "mcp__crm__update_record" not in o["record_write_block"]["on"]
assert "mcp__crm__update_record" not in o["add"]
assert o["leader_allow"] == ["mcp__crm__list_records"]
EOF

echo "test-run.sh: lifting the block with two workflows sharing a rule"
fresh
record wf-a 'write_block:
  on:
    - mcp__crm__update_record
    - mcp__crm__fetch_url
    - Bash(claude:*)
  leader_rules:
    - Bash(rm:*)
  leader_allow: []' "$HASH" "$PROFILE_A"
record wf-b 'write_block:
  on: [mcp__crm__update_record, "Bash(claude:*)", mcp__crm__delete_record]
  leader_rules: []
  leader_allow: []' "" "version 1
workflow wf-b"
W lift-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
expect_rc 0 "lift-rules runs"
python3 - "$TMP/out" <<'EOF' && ok "removes only wf-a's own rule; the shared ones stay for wf-b" || bad "lift with a shared rule"
import json, sys
o = json.load(open(sys.argv[1]))
assert o["remove"] == ["mcp__crm__fetch_url"], o
assert set(o["kept_shared"]) == {"mcp__crm__update_record", "Bash(claude:*)"}, o
EOF
sed -i.bak 's/^write_block:$/write_block: off/; /^  on: \[/d; /^  leader_rules: \[\]/d; /^  leader_allow: \[\]/d' "$WS/framework/wf-b/build-record.md"
W lift-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
python3 - "$TMP/out" <<'EOF' && ok "once wf-b's block is lifted, wf-a can remove the shared rules too" || bad "lift after the other block is off"
import json, sys
o = json.load(open(sys.argv[1]))
assert set(o["remove"]) == {"mcp__crm__update_record", "mcp__crm__fetch_url", "Bash(claude:*)"}, o
EOF
record wf-a 'write_block:
  on:
    - mcp__crm__delete_record
    - Bash(rm:*)
  leader_rules: []
  leader_allow: []' "$HASH" "$PROFILE_A"
record wf-b 'write_block: off' "" "version 1
workflow wf-b"
printf -- '---\nworkflow: wf-c\nwrite_block:\n  leader_rules:\n    - Bash(rm:*)\n  on: []\n---\n' > "$WS/framework/wf-c.md"
mkdir -p "$WS/framework/wf-c"; mv "$WS/framework/wf-c.md" "$WS/framework/wf-c/build-record.md"
W lift-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
python3 - "$TMP/out" <<'EOF' && ok "a rule any record lists as the leader's own is never removed" || bad "leader's rule removed"
import json, sys
o = json.load(open(sys.argv[1]))
assert o["remove"] == ["mcp__crm__delete_record"] and o["kept_leader"] == ["Bash(rm:*)"], o
EOF
printf -- '---\nworkflow: wf-c\nwrite_block: {on: [x]}\n---\n' > "$WS/framework/wf-c/build-record.md"
W lift-rules wf-a --plugin-copy "$PLUGIN/test-run.sh"
expect_rc 5 "another record's block can't be read: nothing is lifted"

echo "test-run.sh: the wrapper's allow"
fresh
record wf-b "write_block: off" "" "version 1
workflow wf-b"
W allow-rules wf-a --plugin-copy "$PLUGIN/test-run.sh" --lift
python3 - "$TMP/out" <<'EOF' && ok "kept while another workflow isn't live yet" || bad "allow kept for another workflow"
import json, sys
o = json.load(open(sys.argv[1])); assert o["remove"] == [] and o["kept_for"] == ["wf-b"], o
assert any("framework/.bin" in d and d.startswith("Write(") for d in o["deny"])
EOF
printf -- '---\ngo_live: done\nround_status: complete\n---\n' > "$WS/framework/wf-b/test-results.md"
W allow-rules wf-a --plugin-copy "$PLUGIN/test-run.sh" --lift
python3 - "$TMP/out" <<'EOF' && ok "removed once no other workflow needs it" || bad "allow removal"
import json, sys
o = json.load(open(sys.argv[1])); assert o["remove"] and o["kept_for"] == [], o
EOF

echo "test-run.sh: settings read-back"
fresh
mkdir -p "$WS/.claude"
printf '{"permissions":{"deny":["mcp__crm__update_record"],"allow":["mcp__crm__update_record","Bash(framework/.bin/test-run.sh *)"],"defaultMode":"acceptEdits"}}' > "$WS/.claude/settings.local.json"
W settings-check wf-a --plugin-copy "$PLUGIN/test-run.sh"
python3 - "$TMP/out" <<'EOF' && ok "names missing block rules, write tools on an allow list, and the modes" || bad "settings-check"
import json, sys
o = json.load(open(sys.argv[1]))
assert o["ok"] is False and "mcp__crm__fetch_url" in o["block_rules_missing"]
assert o["allow_rules_on_write_tools"] == ["mcp__crm__update_record"]
assert o["allow_rules_added_since_block"] == ["mcp__crm__update_record"]
assert o["default_modes"]["local"] == "acceptEdits" and o["wrapper_allowed"] is True
EOF

echo "test-run.sh: the practice folder and its marker"
fresh
W practice-create wf-a --plugin-copy "$PLUGIN/test-run.sh" --round 1
expect_rc 0 "creates the round's practice folder"
[ -f "$WS/practice/.framework-practice" ] && ok "with the marker file" || bad "no marker"
W practice-create wf-a --plugin-copy "$PLUGIN/test-run.sh" --round 2
expect_rc 5 "won't reuse a folder left from an earlier round"
W practice-clear wf-a --plugin-copy "$PLUGIN/test-run.sh" --path practice/
expect_rc 0 "clears its own marked folder"
[ -e "$WS/practice" ] && bad "folder still there" || ok "the marked folder is gone"
mkdir -p "$WS/practice"; echo "leader's own" > "$WS/practice/notes.md"
W practice-create wf-a --plugin-copy "$PLUGIN/test-run.sh" --round 1
has "practice-wf-a/" "$TMP/out" "an unmarked practice/ means practice-<slug>/"
W practice-clear wf-a --plugin-copy "$PLUGIN/test-run.sh" --path practice
expect_rc 5 "never clears an unmarked folder"
[ -f "$WS/practice/notes.md" ] && ok "the leader's folder is untouched" || bad "the leader's folder was cleared"
W practice-clear wf-a --plugin-copy "$PLUGIN/test-run.sh" --path context
expect_rc 5 "never clears any other folder"
rm -f "$WS/practice-wf-a/.framework-practice"
W practice-clear wf-a --plugin-copy "$PLUGIN/test-run.sh" --path practice-wf-a
expect_rc 5 "a folder whose marker is gone isn't cleared"

echo "test-run.sh: run folders"
fresh
W bare wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 3 "bare profile: the stub's connection and skill fail its start-up check (it holds none)"
stream '"Read","Glob","Grep"' "dontAsk" '[]' '"plugins":[]'
W bare wf-a --plugin-copy "$PLUGIN/test-run.sh" --prompt-file "$TMP/prompt.md"
expect_rc 0 "bare profile runs with no connections and no skills"
has "--disable-slash-commands" "$STUB/calls.log" "bare run loads no skill instructions"
RUN="$(sed -n 's/^run_folder: //p' "$TMP/out")"
[ -n "$RUN" ] && [ -d "$RUN" ] && ok "the bare run reports its run folder" || bad "no run folder reported"
[ ! -d "$RUN/.claude/skills" ] && ok "the bare run folder holds no skill" || bad "bare run holds a skill"
mkdir -p "$RUNS/handsonai-framework-runs/wf-a/unmarked"
W runs-clear wf-a --plugin-copy "$PLUGIN/test-run.sh" --path "$RUNS/handsonai-framework-runs/wf-a/unmarked"
expect_rc 5 "won't clear a folder the wrapper didn't make"
W runs-clear wf-a --plugin-copy "$PLUGIN/test-run.sh" --path "$RUN"
expect_rc 0 "clears its own run folder"
[ ! -e "$RUN" ] && [ ! -e "$RUN.config" ] && ok "run folder and its config gone" || bad "run folder left"

echo "test-run.sh: the kit names no secret's value"
for f in "$CANON" "${KIT_DOCS[@]}"; do
  if [ ! -f "$f" ]; then bad "missing kit file $f"; continue; fi
  if grep -nE 'sk-[A-Za-z0-9_-]{12,}|xox[abprs]-[A-Za-z0-9-]{8,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|[Bb]earer [A-Za-z0-9._~+/=-]{16,}' "$f" \
      | grep -vE 'SECRET_RES|re.compile|r"' > "$TMP/hits"; then
    bad "$(basename "$f") holds a secret-shaped value: $(head -1 "$TMP/hits")"
  else ok "$(basename "$f") holds no secret-shaped value"; fi
done

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" = 0 ]
