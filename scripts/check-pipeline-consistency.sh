#!/usr/bin/env bash
#
# check-pipeline-consistency.sh — the multi-agent pipeline is held together by string
# agreement across files that never import each other: an agent writes "02-draft.md",
# the gate checks "02-draft.md", the command promises "02-draft.md". One typo and a
# stage silently produces a file nobody reads.
#
# This asserts that agreement. Run it before demonstrating the pipeline.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

A=".claude/agents"
C=".claude/commands"
H=".claude/hooks"
PASS=0
FAIL=0

ok()  { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }

# $1 = description, $2 = file, $3 = literal string that must appear
must_contain() {
  if grep -qF -- "$3" "$2" 2>/dev/null; then ok "$1"; else bad "$1 — '$3' not found in $2"; fi
}

# $1 = description, $2 = file, $3 = literal string that must NOT appear
must_not_contain() {
  if grep -qF -- "$3" "$2" 2>/dev/null; then bad "$1 — '$3' should not be in $2"; else ok "$1"; fi
}

echo "pipeline consistency"
echo
echo "-- artifact names agree across agent, command, and gate --"

# Each stage's output filename must appear in: the agent that writes it, the gate that
# validates it, and both commands.
declare -a STAGES=(
  "01-research.md:ai-productivity-researcher"
  "02-draft.md:tech-executive-writer"
  "03-edited.md:hbr-editor"
  "03-editorial-memo.md:hbr-editor"
  "04-article.md:hbr-publisher"
  "04-article.docx:hbr-publisher"
)

for entry in "${STAGES[@]}"; do
  file="${entry%%:*}"
  agent="${entry##*:}"
  must_contain "$file written by $agent"      "$A/$agent.md"        "$file"
  must_contain "$file validated by the gate"  "$H/subagent-gate.sh" "$file"
  must_contain "$file named in /hbr-article"  "$C/hbr-article.md"   "$file"
done

echo
echo "-- the reader of each stage matches the writer of the previous one --"
must_contain "writer reads the researcher's dossier" "$A/tech-executive-writer.md" "01-research.md"
must_contain "editor reads the writer's draft"       "$A/hbr-editor.md"            "02-draft.md"
must_contain "publisher reads the editor's revision" "$A/hbr-publisher.md"         "03-edited.md"

echo
echo "-- activation flag and approval marker agree everywhere --"
for f in "$H/subagent-gate.sh" "$H/publish-gate.sh" "$C/hbr-article.md" "$C/hbr-article-strict.md"; do
  must_contain "activation flag in $(basename "$f")" "$f" "outputs/articles/.active-run"
done
must_contain "approval marker checked by publish-gate" "$H/publish-gate.sh" "APPROVED"
must_contain "approval marker written by /hbr-article" "$C/hbr-article.md"  "APPROVED"
must_contain "publish-gate guards the right agent"     "$H/publish-gate.sh" "hbr-publisher"

echo
echo "-- automatic delegation is genuinely automatic --"
# The auto command must NOT hand Claude a fixed sequence; the strict one must.
must_not_contain "/hbr-article does not prescribe stages" "$C/hbr-article.md" "Stage 1"
must_contain     "/hbr-article-strict does prescribe stages" "$C/hbr-article-strict.md" "Stage 1"
must_contain     "/hbr-article tells Claude it chooses"    "$C/hbr-article.md" "you decide which to use and when"
must_contain     "/hbr-article forbids self-serving work"  "$C/hbr-article.md" "Do not do a specialist's work yourself"

# Descriptions must carry the chain, since that is all Claude reads when delegating.
for a in ai-productivity-researcher tech-executive-writer hbr-editor hbr-publisher; do
  desc="$(awk '/^description:/{print}' "$A/$a.md")"
  if printf '%s' "$desc" | grep -qE 'FIRST step|DRAFTING step|EDITING step|FINAL step'; then
    ok "$a description states its chain position"
  else
    bad "$a description does not state its chain position"
  fi
done

echo
echo "-- least privilege --"
grep -q '^tools:.*WebSearch' "$A/ai-productivity-researcher.md" \
  && ok "researcher has web access" || bad "researcher is missing web access"
grep -q '^tools:.*WebSearch' "$A/tech-executive-writer.md" \
  && bad "writer has web access (it must write only from the dossier)" \
  || ok "writer has no web access"
grep -q '^tools:.*Bash' "$A/hbr-publisher.md" \
  && ok "publisher can run the renderer" || bad "publisher cannot run Bash"

echo
echo "-- hooks are wired and executable --"
for hook in subagent-gate.sh publish-gate.sh; do
  [ -x "$H/$hook" ] && ok "$hook is executable" || bad "$hook is not executable"
  grep -q "$hook" .claude/settings.json \
    && ok "$hook wired in settings.json" || bad "$hook not wired in settings.json"
done
jq -e '.hooks.SubagentStop and .hooks.PreToolUse' .claude/settings.json > /dev/null 2>&1 \
  && ok "settings.json declares both hook events" || bad "settings.json is missing a hook event"
jq -e '.hooks.PreToolUse[0].matcher' .claude/settings.json > /dev/null 2>&1 \
  && ok "PreToolUse has a matcher" || bad "PreToolUse has no matcher"

echo
echo "-- quality bars agree between the command and the gate --"
# The gate's floors must be reachable by what the command asks for.
must_contain "command asks for 5+ companies"    "$C/hbr-article.md" "at least 5 named companies"
must_contain "command sets the word target"     "$C/hbr-article.md" "2,000–2,500 words"
grep -q 'MIN_SOURCES=3' "$H/subagent-gate.sh" \
  && ok "gate requires 3 sources" || bad "gate source floor changed — re-check the command"
grep -q 'CHAR_FLOOR_ARTICLE=6000' "$H/subagent-gate.sh" \
  && ok "gate article floor is 6000 chars (~1,000 words, under the 2,000 target)" \
  || bad "gate article floor changed — confirm it is still below the word target"
grep -q 'WORD_CEILING_ARTICLE=2750' "$H/subagent-gate.sh" \
  && ok "gate enforces a ceiling as well as a floor" \
  || bad "gate word ceiling changed — the first live run overran with no ceiling in place"
# The agents must know the ceiling, so they self-correct rather than relying on a block.
must_contain "writer knows the ceiling" "$A/tech-executive-writer.md" "2,750 words"
must_contain "editor knows the ceiling" "$A/hbr-editor.md"            "2,750 words"

echo
echo "-- durable standards live in the agents, not only in the prompt --"
# These were once stated in the goal statement on every run. They belong in the agents,
# so a short prompt gets the same result.
must_contain "researcher carries the evidence floor" "$A/ai-productivity-researcher.md" "at least 5 named companies"
must_contain "researcher carries the recency bar"    "$A/ai-productivity-researcher.md" "last 24 months"
must_contain "writer carries the length target"      "$A/tech-executive-writer.md"      "2,000–2,500 words"
must_contain "writer overrides its own wider range"  "$A/tech-executive-writer.md"      "overrides the 2,000–4,000"

echo
echo "-- CLAUDE.md carries the conventions, so a bare prompt works in this repo --"
# The slash command stays self-contained for plugin users in other repos; CLAUDE.md is
# what lets a plain typed prompt work here without restating any of it.
must_contain "default workspace convention" CLAUDE.md "outputs/articles/<kebab-slug-of-topic>/"
must_contain "gate arming instruction"      CLAUDE.md "outputs/articles/.active-run"
must_contain "approval marker convention"   CLAUDE.md "APPROVED"
must_contain "no-self-serving rule"         CLAUDE.md "Never do a specialist's work yourself"
must_contain "both deliverables named"      CLAUDE.md "04-article.docx"

echo
echo "-- renderer is reachable --"
[ -f scripts/article-to-docx.js ] && ok "renderer present" || bad "renderer missing"
[ -x scripts/render-docx.sh ] && ok "render wrapper is executable" || bad "render wrapper not executable"
must_contain "publisher calls the render wrapper" "$A/hbr-publisher.md" "render-docx.sh"

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
