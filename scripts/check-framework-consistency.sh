#!/usr/bin/env bash
#
# check-framework-consistency.sh — the seven framework skills and their docs pages describe the
# same sequence of phases, and four files spell the mechanism enum the same way. Nothing
# imports anything, so drift is silent. This asserts the agreement.
#
# Run: bash scripts/check-framework-consistency.sh

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

for entry in analyze:analyze.md deconstruct:deconstruct.md design:design.md build:build.mdx test:test.md run:run.md improve:improve.md; do
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
echo "-- mechanism enum spelled identically --"
ENUM='Skill | Agent'
for f in "$SK/design/references/spec-template.md" "$SK/design/references/self-test-checklist.md" "$SK/build/SKILL.md" "$DOCS/index.md"; do
  if grep -qF -- "$ENUM" "$f"; then ok "'$ENUM' in $f"; else bad "'$ENUM' missing from $f"; fi
done
for f in "$SK"/*/SKILL.md "$SK"/design/references/*.md; do
  if grep -qE 'Skill-Powered (Workflow|Prompt)' "$f" && ! grep -qiE 'legacy' "$f"; then
    bad "$f mentions a legacy mechanism name without calling it legacy"
  fi
done

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
