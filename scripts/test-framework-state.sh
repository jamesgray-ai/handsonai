#!/usr/bin/env bash
#
# test-framework-state.sh — runs registry-template/tools/framework-state.js over every
# fixture in framework-fixtures/expected.json (both variants, and the one-workspace
# fixtures marked `self`) and asserts the routing state, its owner, N-B44 for state 1,
# and the "continue my workflow" result. Also asserts the failure paths (non-zero exit
# on an unreadable folder), that the script writes nothing, and that the plugin copy
# is byte-identical to the canonical one.
#
# Usage: ./scripts/test-framework-state.sh

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SCRIPT=registry-template/tools/framework-state.js
COPY=plugins/handsonai/tools/framework-state.js
FIXTURES=framework-fixtures

PASS=0
FAIL=0
ok()  { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }

echo "framework-state"
echo

TMP="$(mktemp -d)"
trap 'chmod -R u+rwx "$TMP" 2>/dev/null; rm -rf "$TMP"' EXIT
touch "$TMP/marker"
sleep 1

echo "-- every fixture in expected.json --"
OUT="$(node - "$SCRIPT" "$FIXTURES" <<'NODE'
const path = require('path');
const fs = require('fs');
const [script, fixtures] = process.argv.slice(2);
const { workflowState, continueState } = require(path.resolve(script));
const expected = JSON.parse(fs.readFileSync(path.join(fixtures, 'expected.json'), 'utf8'));

const lines = [];
const say = (ok, msg) => lines.push(`${ok ? 'PASS' : 'FAIL'}\t${msg}`);

function workflowFolders(ws) {
  const fw = path.join(ws, 'framework');
  if (!fs.existsSync(fw)) return [];
  return fs.readdirSync(fw, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !['history', 'registry'].includes(d.name) && !d.name.startsWith('.'))
    .map((d) => d.name);
}

function run(fn) {
  try { return { r: fn() }; } catch (e) { return { err: e.message }; }
}

function checkOne(label, ws, slug, exp) {
  const { r, err } = run(() => workflowState(path.join(ws, 'framework', slug)));
  if (err) return say(false, `${label}: threw: ${err}`);
  const probs = [];
  if (r.state !== exp.state) probs.push(`state ${r.state}, expected ${exp.state}`);
  if ((r.owner || null) !== (exp.owner || null)) probs.push(`owner ${r.owner}, expected ${exp.owner}`);
  if ('n_b44' in exp && !!r.n_b44 !== exp.n_b44) probs.push(`n_b44 ${!!r.n_b44}, expected ${exp.n_b44}`);
  say(!probs.length, `${label}: ${probs.length ? probs.join('; ') + ` (because ${r.reason})` : `state ${r.state} · ${r.owner || 'no owner'}${'n_b44' in exp ? ` · n_b44 ${r.n_b44}` : ''}`}`);
}

function checkContinue(label, ws, exp) {
  const { r, err } = run(() => continueState(ws));
  if (err) return say(false, `${label}: threw: ${err}`);
  const probs = [];
  if (r.continue !== exp.continue) probs.push(`continue ${r.continue}, expected ${exp.continue}`);
  if ('owner' in exp && (r.owner || null) !== (exp.owner || null)) probs.push(`owner ${r.owner}, expected ${exp.owner}`);
  if ('workflow' in exp && r.workflow !== exp.workflow) probs.push(`workflow ${r.workflow}, expected ${exp.workflow}`);
  if ('state' in exp && r.state !== exp.state) probs.push(`state ${r.state}, expected ${exp.state}`);
  if ('line' in exp && r.line !== exp.line) probs.push(`line ${r.line}, expected ${exp.line}`);
  if ('options' in exp) {
    const got = (r.options || []).map((o) => o.workflow).sort().join(',');
    const want = exp.options.slice().sort().join(',');
    if (got !== want) probs.push(`options [${got}], expected [${want}]`);
  }
  const desc = r.continue === 'ask' ? `ask [${r.options.map((o) => o.workflow).join(', ')}]`
    : r.continue === 'pick' ? `pick ${r.workflow} (state ${r.state}, ${r.owner})` : `${r.continue} (${r.owner})`;
  say(!probs.length, `${label}: ${probs.length ? probs.join('; ') : desc}`);
}

for (const [key, variants] of Object.entries(expected)) {
  for (const [variant, exp] of Object.entries(variants)) {
    const ws = variant === 'self' ? path.join(fixtures, key) : path.join(fixtures, key, variant);
    const label = variant === 'self' ? key : `${key} [${variant}]`;
    if (!fs.existsSync(ws)) { say(false, `${label}: fixture folder missing`); continue; }
    if ('continue' in exp) { checkContinue(label, ws, exp); continue; }
    if (exp.workflows) {
      for (const [slug, e] of Object.entries(exp.workflows)) checkOne(`${label} ${slug}`, ws, slug, e);
      continue;
    }
    const folders = workflowFolders(ws);
    const slug = folders.length === 1 ? folders[0] : 'client-follow-up';
    checkOne(label, ws, slug, exp);
  }
}
process.stdout.write(lines.join('\n') + '\n');
NODE
)"
while IFS=$'\t' read -r verdict msg; do
  [ -z "$verdict" ] && continue
  if [ "$verdict" = PASS ]; then ok "$msg"; else bad "$msg"; fi
done <<< "$OUT"

echo
echo "-- the command line --"
# A state, as JSON, with exit 0.
J="$(node "$SCRIPT" --json "$FIXTURES/states/s11-live/with-registry/framework/client-follow-up")"
[ $? -eq 0 ] && echo "$J" | node -e 'const r=JSON.parse(require("fs").readFileSync(0,"utf8")); process.exit(r.state===11&&r.facts&&r.facts.live===true?0:1)' \
  && ok "--json prints the state with its facts (s11-live: 11, live)" || bad "--json on s11-live"
L="$(node "$SCRIPT" --line "$FIXTURES/earlier-version/v1-results-no-round/with-registry/framework/client-follow-up")"
case "$L" in *"state 1 (Earlier version), Test"*"N-B44"*) ok "--line names state 1, its owner and N-B44" ;; *) bad "--line on v1-results-no-round: $L" ;; esac
C="$(node "$SCRIPT" --line --continue "$FIXTURES/continue/c-several-in-progress/with-registry")"
case "$C" in *"N-F9"*client-follow-up*weekly-pipeline-summary*) ok "--continue over two workflows in progress gives the N-F9 list" ;; *) bad "--continue on c-several-in-progress: $C" ;; esac

echo
echo "-- an unreadable folder exits non-zero --"
node "$SCRIPT" --json "$TMP/no-such-framework/client-follow-up" >/dev/null 2>&1
[ $? -eq 2 ] && ok "a workflow folder whose framework folder doesn't exist: exit 2" || bad "missing framework folder did not exit 2"
mkdir -p "$TMP/fw/framework"
echo "not a folder" > "$TMP/fw/framework/client-follow-up"
node "$SCRIPT" --json "$TMP/fw/framework/client-follow-up" >/dev/null 2>&1
[ $? -eq 2 ] && ok "a workflow path that is a file: exit 2" || bad "a file in place of the folder did not exit 2"
mkdir -p "$TMP/locked/framework/client-follow-up"
cp "$FIXTURES/states/s04-plan-needed/no-registry/framework/client-follow-up/requirements.md" "$TMP/locked/framework/client-follow-up/"
chmod 000 "$TMP/locked/framework/client-follow-up"
if [ -r "$TMP/locked/framework/client-follow-up" ]; then
  ok "a folder that can't be read: skipped (running as a user who can read it anyway)"
else
  node "$SCRIPT" --json "$TMP/locked/framework/client-follow-up" >/dev/null 2>&1
  [ $? -eq 2 ] && ok "a folder that can't be read: exit 2" || bad "an unreadable folder did not exit 2"
fi
chmod 755 "$TMP/locked/framework/client-follow-up"
mkdir -p "$TMP/bad/framework/client-follow-up"
printf -- '---\nrevision: 1\ntrack: light\nrevisions:\n  - { revision: 2, by: test\n---\n\n# x\n' > "$TMP/bad/framework/client-follow-up/requirements.md"
node "$SCRIPT" --json "$TMP/bad/framework/client-follow-up" >/dev/null 2>&1
[ $? -eq 2 ] && ok "frontmatter it can't parse: exit 2 (never routes on a misread fact)" || bad "malformed frontmatter did not exit 2"
node "$SCRIPT" --continue "$TMP/no-such-workspace" >/dev/null 2>&1
[ $? -eq 2 ] && ok "--continue on a folder that doesn't exist: exit 2" || bad "--continue on a missing folder did not exit 2"
node "$SCRIPT" >/dev/null 2>&1
[ $? -eq 1 ] && ok "no folder given: usage, exit 1" || bad "no arguments did not exit 1"

echo
echo "-- it never writes --"
WRITTEN="$(find "$FIXTURES" -newer "$TMP/marker" -print 2>/dev/null | head -5)"
[ -z "$WRITTEN" ] && ok "no fixture file or folder changed during the run" || bad "files changed during the run: $WRITTEN"
grep -nE 'fs\.(write|append|mkdir|rm|rename|unlink|copy|chmod|truncate|symlink|cp)' "$SCRIPT" >/dev/null \
  && bad "framework-state.js calls a file-writing fs function" || ok "framework-state.js calls no file-writing fs function"

echo
echo "-- the plugin copy --"
if [ -f "$COPY" ] && cmp -s "$SCRIPT" "$COPY"; then ok "$COPY is byte-identical to $SCRIPT"; else bad "$COPY is missing or differs from $SCRIPT"; fi

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
