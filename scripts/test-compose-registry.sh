#!/usr/bin/env bash
# Tests for registry-template/tools/lint-registry.js (Task 5) and, once it
# exists, tools/compose-registry.js (Task 6). Follows the ok/bad/skip +
# summary house style from scripts/test-check-plugin-sync.sh.
#
# Every fixture stages into an isolated mktemp git repo (see stage() below) so
# `git check-ignore` inside lint sees only the fixture's own .gitignore, never
# this repo's unanchored `outputs/` rule -- that's also why
# `registry-template/tools/fixtures/**` is un-ignored in the root .gitignore.
#
# Run: bash scripts/test-compose-registry.sh

set -uo pipefail

PASS=0
FAIL=0
ok()   { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }
skip() { echo "  skip  $1"; }

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$REPO_ROOT/registry-template/tools"
FIX="$TOOLS/fixtures"
stage() {  # copy a fixture workspace to an isolated temp git repo; echoes the path
  local ws; ws=$(mktemp -d)
  cp -R "$FIX/$1/." "$ws/"
  (cd "$ws" && git init -q . && git add -A >/dev/null 2>&1)
  echo "$ws"
}
run_lint()    { local ws; ws=$(stage "$1"); (cd "$ws" && node "$TOOLS/lint-registry.js" registry >/dev/null 2>&1); }
lint_output() { local ws; ws=$(stage "$1"); (cd "$ws" && node "$TOOLS/lint-registry.js" registry 2>&1); }
run_lint_at() { (cd "$1" && node "$TOOLS/lint-registry.js" registry); }
compose_at()  { WS=$(stage "$1"); (cd "$WS" && node "$TOOLS/compose-registry.js" registry); }  # sets $WS for assertions

# lint: valid bundle passes
run_lint valid-bundle && ok "valid bundle lints clean (exit 0)" || bad "valid bundle should lint clean"
# lint: warnings present but exit 0
# (variable-capture pattern throughout -- lint_output legitimately exits 1 on
# error fixtures, and with `pipefail` active that must never sit on the left
# of a pipeline whose only job is to grep the captured text.)
out=$(lint_output valid-bundle)
grep -q "WARN.*stale_after" <<<"$out" && ok "overdue stale_after warned" || bad "expected overdue warning"
grep -q "WARN.*orphan-skill" <<<"$out" && ok "orphan capability warned" || bad "expected orphan-capability warning"
# lint: each broken fixture fails with a message naming the file
grep -q "WARN" <<<"$out" || bad "expected warnings on valid bundle"
out=$(lint_output broken/warn-bad-actor)
grep -q "WARN.*generated.by" <<<"$out" && ok "actor-string warned" || bad "expected actor warning"
out=$(lint_output broken/warn-misfiled-note)
grep -q "WARN.*[Nn]ote" <<<"$out" && ok "misfiled note warned" || bad "expected note warning"
for case in bad-enum dir-type-mismatch missing-owner missing-frontmatter broken-link banned-field \
            unclaimed-sop double-claim sop-backpointer-mismatch runlog-status-contradiction \
            double-parent-list unassigned-inproduction missing-owns-block unterminated-generated \
            multiline-frontmatter hand-edited-generated missing-index-entry missing-dir-index \
            legacy-timestamp; do
  if run_lint "broken/$case"; then bad "$case: lint should exit 1"; else
    out=$(lint_output "broken/$case")
    grep -q "ERROR" <<<"$out" && ok "$case errors" || bad "$case: no ERROR line"
  fi
done
run_lint broken/unassigned-backlog && ok "unassigned backlog is warning-only" || bad "backlog unassigned must not error"
# lint: gitignore tolerance -- valid bundle with outputs/ deleted still lints clean
tmp=$(mktemp -d); cp -R "$FIX/valid-bundle/." "$tmp/"; rm -rf "$tmp/outputs"
printf 'outputs/\n' > "$tmp/.gitignore"; (cd "$tmp" && git init -q . && git add -A >/dev/null)
run_lint_at "$tmp" && ok "gitignored artifact links tolerated" || bad "gitignore tolerance failed"

# compose: refuses while lint errors
(cd "$FIX/broken/bad-enum" && ! node "$TOOLS/compose-registry.js" registry) && ok "compose refuses on lint errors" || bad "compose must refuse"
# compose: valid bundle → golden REGISTRY.md
compose_at valid-bundle
diff -u "$FIX/golden/REGISTRY.md" "$WS/REGISTRY.md" && ok "REGISTRY.md matches golden" || bad "REGISTRY.md drift"
# compose: fills Workflow `# Insights` GENERATED block (reverse view of the Note's link)
grep -q "/notes/first-workflow-insight.md" "$WS/registry/workflows/second-workflow.md" && ok "compose fills Workflow Insights GENERATED block" || bad "Insights block not filled"
# compose: deterministic — two runs byte-identical
cp "$WS/REGISTRY.md" /tmp/r1; (cd "$WS" && node "$TOOLS/compose-registry.js" registry)
cmp -s /tmp/r1 "$WS/REGISTRY.md" && ok "deterministic" || bad "output differs across runs"
# compose: data island valid + golden
(cd "$WS" && node "$TOOLS/compose-registry.js" --island-only registry) > /tmp/island.json
node -e "JSON.parse(require('fs').readFileSync('/tmp/island.json'))" && ok "island parses" || bad "island invalid JSON"
diff -u "$FIX/golden/data-island.json" /tmp/island.json && ok "island matches golden" || bad "island drift"
# compose: empty skeleton bundle (student's first Action run)
WS=$(mktemp -d); cp -R "$REPO_ROOT/registry-template/registry" "$WS/registry"
(cd "$WS" && git init -q . && node "$TOOLS/compose-registry.js" registry) && ok "empty bundle composes" || bad "empty bundle crashed"
grep -q "No workflows yet" "$WS/REGISTRY.md" && ok "empty dashboard has guidance line" || bad "missing empty-state line"
# compose: self-healing rename — stale GENERATED links must not deadlock
WS=$(stage valid-bundle)
mv "$WS/registry/workflows/first-workflow.md" "$WS/registry/workflows/first-workflow-weekly.md"
sed -i '' 's/^title: .*/title: "First Workflow Weekly"/' "$WS/registry/workflows/first-workflow-weekly.md"
sed -i '' 's|/workflows/first-workflow.md|/workflows/first-workflow-weekly.md|' "$WS/registry/processes/"*.md
# root index's GENERATED block deliberately still holds the stale old link
(cd "$WS" && node "$TOOLS/compose-registry.js" registry) && ok "rename does not deadlock compose" || bad "rename deadlocked"
run_lint_at "$WS" && ok "post-rename lint clean" || bad "post-rename lint dirty"

echo
echo "$PASS ok, $FAIL bad"
[ "$FAIL" -eq 0 ]
