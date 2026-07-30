#!/usr/bin/env bash
#
# check-plugin-sync.sh — the multi-agent-example pipeline exists in two places:
#
#   .claude/{agents,skills,commands,hooks}/ and scripts/   → what runs in THIS repo
#   plugins/multi-agent-example/                           → what students install
#
# They must stay identical, or the demo and the distributed plugin quietly diverge.
# This fails loudly the moment they do.
#
# Run: bash scripts/check-plugin-sync.sh

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN="$ROOT/plugins/multi-agent-example"
DRIFT=0
CHECKED=0

compare() {
  # $1 = repo-relative path, $2 = plugin-relative path
  local a="$ROOT/$1" b="$PLUGIN/$2"
  CHECKED=$((CHECKED + 1))
  if [ ! -f "$a" ]; then
    echo "  MISSING in repo:   $1"; DRIFT=$((DRIFT + 1)); return
  fi
  if [ ! -f "$b" ]; then
    echo "  MISSING in plugin: $2"; DRIFT=$((DRIFT + 1)); return
  fi
  if ! diff -q "$a" "$b" > /dev/null; then
    echo "  DRIFTED:           $1  vs  plugins/multi-agent-example/$2"
    DRIFT=$((DRIFT + 1))
  fi
}

echo "multi-agent-example: repo vs plugin"

for a in ai-productivity-researcher tech-executive-writer hbr-editor hbr-publisher; do
  compare ".claude/agents/$a.md" "agents/$a.md"
done

for c in hbr-article hbr-article-strict; do
  compare ".claude/commands/$c.md" "commands/$c.md"
done

for h in subagent-gate.sh publish-gate.sh test-subagent-gate.sh test-publish-gate.sh; do
  compare ".claude/hooks/$h" "hooks/$h"
done

for s in article-to-docx.js test-article-to-docx.sh render-docx.sh; do
  compare "scripts/$s" "scripts/$s"
done

compare ".claude/skills/editing-hbr-articles/SKILL.md" "skills/editing-hbr-articles/SKILL.md"
compare ".claude/skills/editing-hbr-articles/references/editorial-criteria.md" \
        "skills/editing-hbr-articles/references/editorial-criteria.md"

echo
if [ "$DRIFT" -eq 0 ]; then
  echo "$CHECKED files checked — all in sync"
else
  echo "$CHECKED files checked — $DRIFT out of sync"
  echo
  echo "plugins/multi-agent-example/ is canonical. Copy from there to .claude/, then re-run."
fi

[ "$DRIFT" -eq 0 ]
