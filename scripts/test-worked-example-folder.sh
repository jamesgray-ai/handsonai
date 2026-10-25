#!/usr/bin/env bash
# Checks the worked-example folder, examples/weekly-status-report: an internal test fixture (not published
# on the site) holding one workflow taken through the five steps to live on Claude desktop, in this
# release's file formats. Documents/Framework/ is the framework folder; Documents/status-reports/ is the
# workflow's own working folder. scripts/test-compose-registry.sh checks its registry; this checks the
# workflow's record and the built skill.
#   Run: bash scripts/test-worked-example-folder.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EX="$ROOT/examples/weekly-status-report"
FW="$EX/Documents/Framework"
W="$FW/weekly-status-report"
RUN="$EX/Documents/status-reports"
TOOLS="$ROOT/registry-template/tools"
STRUCT="$ROOT/framework-evals/structure.py"
CARRIED="$ROOT/plugins/handsonai/skills/build/references/carried-lines.md"
SKILL="$W/package/skills/weekly-status-report/SKILL.md"

PASS=0; FAIL=0
ok()  { echo "  ok    $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }

# -- the flat folder: the four record files, inputs/, context/, package/, history/; nothing earlier
for f in requirements.md design-plan.md build-record.md test-results.md inputs context package history/test-results-round-1.md; do
  [ -e "$W/$f" ] && ok "workflow folder has $f" || bad "workflow folder is missing $f"
done
left=$(cd "$EX" && find . \( -name run-guide.md -o -name improvement-plan.md -o -name design-spec.md -o -name 'runs*.md' -o -name test-runs -o -name outputs \) -print)
[ -z "$left" ] && ok "no run guide, improvement plan, design spec, run log, test-runs/ or outputs/" || bad "earlier-version files left: $left"

# -- each file in its template's format (the checks later steps and scripts rely on)
out=$(python3 "$STRUCT" plan "$W/design-plan.md" 2>&1) && ok "design-plan.md: plan structure" || bad "design-plan.md: $out"
out=$(python3 "$STRUCT" build_record "$W/build-record.md" 2>&1) && ok "build-record.md: record structure" || bad "build-record.md: $out"
for r in "$W/test-results.md" "$W"/history/test-results-round-*.md; do
  out=$(python3 "$STRUCT" results "$r" 2>&1) && ok "${r#$W/}: results structure" || bad "${r#$W/}: $out"
done
out=$(node "$TOOLS/requirements-check.js" "$W" 2>&1) && ok "requirements.md passes the requirements check" || bad "requirements check: $out"

# -- routing reads it as live, with and without the registry
st() { node "$TOOLS/framework-state.js" "$W" "$@" --json 2>/dev/null | node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{try{const j=JSON.parse(s);console.log(j.state+' '+j.name)}catch{console.log('unreadable')}})"; }
[ "$(st)" = "11 Live" ] && ok "routing: state 11 (Live) with the registry" || bad "routing with the registry: $(st)"
[ "$(st --no-registry)" = "11 Live" ] && ok "routing: Live from the build record's Live since line" || bad "routing with no registry: $(st --no-registry)"

# -- practice inputs: the two header lines, a known source, line IDs that exist
for f in "$W"/inputs/E*.md; do
  n=$(basename "$f")
  if head -1 "$f" | grep -qE '^source: (deconstruct|design|test|flag)$' && sed -n 2p "$f" | grep -qE '^tests: ' && [ -z "$(sed -n 3p "$f")" ]; then
    missing=""; for id in $(sed -n 2p "$f" | sed 's/^tests: //; s/,//g'); do
      [ "$id" = "KW" ] && continue
      grep -qE "\*\*$id( \(must\))?\*\*|^\| $id \|" "$W/requirements.md" || missing="$missing $id"
    done
    [ -z "$missing" ] && ok "inputs/$n: header and line IDs" || bad "inputs/$n names lines the requirements don't have:$missing"
  else bad "inputs/$n doesn't open with source:, tests: and a blank line"; fi
done
grep -q '^source: flag$' "$W"/inputs/E*.md && ok "a flag input exists" || bad "no flag input (source: flag)"

# -- the two places: no framework file where the workflow runs; runtime copies match the steps' copies
stray=""; for f in requirements.md design-plan.md build-record.md test-results.md; do [ -e "$RUN/$f" ] && stray="$stray $f"; done
[ -z "$stray" ] && ok "the workflow's folder holds no framework file" || bad "framework files in the workflow's folder:$stray"
cmp -s "$RUN/status-report-2026-05-22.md" "$W/context/C2-report-2026-05-22.md" && ok "C2's runtime copy matches context/" || bad "C2's runtime copy differs from context/"
cmp -s "$RUN/tone-guide.md" "$W/context/C3-tone-guide.md" && ok "C3's runtime copy matches context/" || bad "C3's runtime copy differs from context/"

# -- the built skill carries the lines every built workflow carries, word for word, and no IDs
for line in "Practice run: nothing will be sent or changed." \
  "Under the practice-run cue, never send, post or change anything: go up to each change, show exactly what you would send or change and where, and don't make it. A change that can't be undone is always shown, even when it's the last action in a batch." \
  "When a practice run is given its input, work from that input; don't fetch it from its usual source, and make any lookup you still need read-only." \
  "All results"; do
  grep -qF "$line" "$CARRIED" || { bad "carried-lines.md no longer has: $line"; continue; }
  grep -qF "$line" "$SKILL" && ok "skill carries: ${line:0:50}…" || bad "skill is missing: $line"
done
grep -qF "This had [X], which I wasn't designed for. If I should handle it, in a new chat with your framework folder added, say 'change my workflow: [X, in a few words]. My files are in Framework/weekly-status-report.', and paste this run's input too." "$SKILL" \
  && ok "skill carries the flag line in its Claude desktop form, with the location" || bad "skill is missing the Claude desktop flag line"
grep -qE '\b(AC|R|G|P|T)[0-9]+\b|\bKW\b' "$SKILL" && bad "skill text carries requirement or task IDs: $(grep -noE '\b(AC|R|G|P|T)[0-9]+\b|\bKW\b' "$SKILL" | head -3 | tr '\n' ' ')" || ok "skill text carries no requirement or task IDs"
[ "$(find "$W/package" -type f | grep -vc '/SKILL.md$')" -eq 0 ] && ok "package/ holds only the skill" || bad "package/ holds more than the skill"

# -- the record's fingerprint is the skill's text
want=$(shasum -a 256 "$SKILL" | cut -d' ' -f1)
grep -q "sha256:$want" "$W/build-record.md" && ok "build record's fingerprint matches the kept skill" || bad "build record's fingerprint isn't sha256:$want"

# -- internal fixture: marked as one, and nothing on the site links it
head -5 "$EX/README.md" | grep -q "Internal test fixture, not published" && ok "README says it's an internal test fixture" || bad "README lacks the internal-fixture note"
hits=$(grep -rlE "examples/weekly-status-report|weekly-status-report\.zip|examples/worked-example" "$ROOT/src/content/docs" "$ROOT/src/integrations" 2>/dev/null | grep -v '/blog/' || true)
[ -z "$hits" ] && ok "no site page or integration links or ships the fixture" || bad "the site still links or ships it: $hits"

echo; echo "$PASS ok, $FAIL bad"; [ "$FAIL" -eq 0 ]
