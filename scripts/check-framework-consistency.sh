#!/usr/bin/env bash
#
# check-framework-consistency.sh — the framework skills and their docs pages describe the
# same sequence of phases, four files spell the mechanism enum the same way, and the retired
# run and improve skills and the dropped framework agent stay gone. Nothing imports
# anything, so drift is silent. This asserts the agreement. It also runs two checks
# that keep the skills' shared wording identical:
#
#   - routing copies: references/routing.md in the five step skills, and the test-run
#     wrapper in build and test, byte-identical to scripts/framework/ (sync-routing.sh --check);
#   - the placement check: every approved line in framework-evals/approved-lines.json is in
#     the file it names, word for word, placeholders as wildcards (check-line-placement.py).
#     Skills listed in scripts/line-placement-pending.txt (rewrite not landed) are report-only.
#
# Run: bash scripts/check-framework-consistency.sh
#      FRAMEWORK_SPEC=<path to the business repo's framework-rules.md> bash scripts/check-framework-consistency.sh
#        (also compares scripts/framework/routing.md with the spec's block; CI can't read the
#        private spec, so it runs only when the path is given)

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SK="plugins/handsonai/skills"
DOCS="src/content/docs/ai-workflow-framework"
PASS=0; FAIL=0
ok()  { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }

echo "framework consistency"
echo
echo "-- phase lists: skill headings vs docs 'How the Skill Works' --"

# Skill phases: "#### Phase N — Name" or "#### Phase N (goal-driven) — Name" → "N|Name"
skill_phases() {
  grep -E '^#### Phase [0-9]+( \(goal-driven\))? — ' "$1" \
    | sed -E 's/^#### Phase ([0-9]+)( \(goal-driven\))? — (.*)$/\1\2|\3/'
}
# Docs phases: numbered bold entries under "## How the Skill Works" until the next "## "
docs_phases() {
  # Docs entry: "N. **Name** — …" or, for a path-specific phase, "N. **Name** *(goal-driven)* — …"
  awk '/^## How the Skill Works/{f=1;next} /^## /{f=0} f' "$1" \
    | grep -E '^[0-9]+\. \*\*' \
    | sed -E 's/^([0-9]+)\. \*\*([^*]+)\*\*(.*)$/\1|\2|\3/' \
    | awk -F'|' '{ n=$1; if ($3 ~ /\(goal-driven\)/) n=n" (goal-driven)"; print n"|"$2 }'
}

for entry in analyze:analyze.md deconstruct:deconstruct.md design:design.md build:build.mdx test:test.md; do
  skill="${entry%%:*}"; page="${entry##*:}"
  s=$(skill_phases "$SK/$skill/SKILL.md" | sort -u)
  d=$(docs_phases "$DOCS/$page" | sort -u)
  if [ -z "$s" ]; then bad "$skill: no '#### Phase N — ' headings found"; continue; fi
  if [ "$s" == "$d" ]; then ok "$skill: $(echo "$s" | wc -l | tr -d ' ') phases agree with $page"
  else
    bad "$skill: phases differ from $page"
    diff <(echo "$s") <(echo "$d") | sed 's/^/        /'
  fi
done

echo
echo "-- run, improve and the framework agent stay retired (10.0.0) --"
back=""
for p in "$SK/run" "$SK/improve" "$DOCS/run.md" "$DOCS/improve.md" run-workspace improve-workspace \
         plugins/handsonai/agents/framework-agent.md framework-agent-workspace; do
  [ -e "$p" ] && back="$back $p"
done
if [ -z "$back" ]; then ok "no run or improve skill, eval workspace or docs page, and no framework-agent"
else bad "retired run/improve/framework-agent material is back:$back"; fi

echo
echo "-- mechanism enum spelled identically --"
ENUM='Skill | Agent'
# Design's template is plan-template.md from T23 on; spec-template.md until then.
DESIGN_TEMPLATE="$SK/design/references/plan-template.md"
[ -f "$DESIGN_TEMPLATE" ] || DESIGN_TEMPLATE="$SK/design/references/spec-template.md"
for f in "$DESIGN_TEMPLATE" "$SK/design/references/self-test-checklist.md" "$SK/build/SKILL.md" "$DOCS/index.md"; do
  if grep -qF -- "$ENUM" "$f"; then ok "'$ENUM' in $f"; else bad "'$ENUM' missing from $f"; fi
done
for f in "$SK"/*/SKILL.md "$SK"/design/references/*.md; do
  if grep -qE 'Skill-Powered (Workflow|Prompt)' "$f" && ! grep -qiE 'legacy' "$f"; then
    bad "$f mentions a legacy mechanism name without calling it legacy"
  fi
done

echo
echo "-- framework record lives in framework/, not outputs/ (9.0) --"
# Legacy-layout detection and the move routine legitimately name outputs/<slug>/: exempt the two
# migration files, and any line that says it is about the pre-9.0 layout ("9.0" on the line).
# A workflow's own output may still be shown as outputs/<file> -- the pattern only matches a
# placeholder folder (outputs/[workflow-name]/, outputs/<slug>/, ...) or the Analyze report.
EXEMPT='migrating-legacy-workspaces.md|interview-guide.md|registry-bundle.md'
hits=$(grep -rnE 'outputs/((\[workflow-name\]|\[name\]|<slug>|<workflow-slug>|<workflow>|<name>)/|ai-opportunity-report)' \
         "$SK" plugins/handsonai/README.md 2>/dev/null | grep -vE "$EXEMPT" | grep -viE '9\.0|legacy' || true)
if [ -z "$hits" ]; then ok "no framework skill or README writes the record to outputs/"
else bad "framework record path still under outputs/:"; echo "$hits" | sed 's/^/        /'; fi

echo
echo "-- routing copies: identical to scripts/framework/ --"
if [ -n "${FRAMEWORK_SPEC:-}" ]; then
  out=$(bash scripts/sync-routing.sh --check "$FRAMEWORK_SPEC" 2>&1); rc=$?
else
  out=$(bash scripts/sync-routing.sh --check 2>&1); rc=$?
fi
echo "$out" | grep -vE '^(Checking routing copies|Routing copies in sync\.)?$'
if [ "$rc" -eq 0 ]; then ok "routing.md and test-run.sh copies match scripts/framework/"
else bad "routing copies have drifted (exit $rc): edit scripts/framework/, then run bash scripts/sync-routing.sh"; fi

echo
echo "-- placement: every approved line in its named file, word for word --"
out=$(python3 scripts/check-line-placement.py --quiet 2>&1); rc=$?
echo "$out" | tail -n +2
if [ "$rc" -eq 0 ]; then ok "approved lines in place (skills on scripts/line-placement-pending.txt report only)"
else bad "approved lines missing or drifted (exit $rc): see above; python3 scripts/check-line-placement.py lists each one"; fi

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
