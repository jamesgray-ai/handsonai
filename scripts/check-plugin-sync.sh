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

# Where a plugin-relative path lives in this repo. `scripts/` maps to the repo's own
# scripts/ directory; everything else sits under .claude/.
repo_path_for() {
  case "$1" in
    scripts/*) echo "$1" ;;
    *)         echo ".claude/$1" ;;
  esac
}

echo "multi-agent-example: repo vs plugin"

# Enumerate from the plugin tree rather than a hardcoded list.
#
# A literal list only guards the files someone remembered to add to it. Adding a fifth
# agent, a second skill, or a new script to the plugin without editing this script would
# print "all in sync" while the two trees genuinely differed — and sync-plugins.sh treats
# a pass here as permission to ship.
#
# .claude-plugin/ is excluded deliberately: plugin.json exists only in the plugin, and
# node_modules/ is build output, not source.
while IFS= read -r rel; do
  # hooks/hooks.json has no repo twin ON PURPOSE. A plugin registers its hooks through
  # hooks/hooks.json; this repo registers the same two scripts through .claude/settings.json.
  # Different files, different formats, same wiring — check-pipeline-consistency.sh is what
  # verifies the two registrations agree.
  [ "$rel" = "hooks/hooks.json" ] && continue
  compare "$(repo_path_for "$rel")" "$rel"
done < <(cd "$PLUGIN" && find agents commands hooks scripts skills -type f \
           -not -path '*/node_modules/*' -not -name '.DS_Store' 2>/dev/null | sort)

# And the other direction, for the directories this pipeline owns outright. A repo-side
# file with no plugin counterpart is drift too — the demo would use something students
# never receive. Limited to exclusive paths: .claude/agents/ and scripts/ are shared with
# unrelated repo content, so they cannot be swept this way.
while IFS= read -r path; do
  rel="${path#$ROOT/.claude/}"
  [ -f "$PLUGIN/$rel" ] || { echo "  MISSING in plugin: $rel (exists in repo)"; DRIFT=$((DRIFT + 1)); }
done < <(find "$ROOT/.claude/hooks" "$ROOT/.claude/skills/editing-hbr-articles" -type f \
           -not -name '.DS_Store' 2>/dev/null | sort)

while IFS= read -r path; do
  name="$(basename "$path")"
  [ -f "$PLUGIN/commands/$name" ] || { echo "  MISSING in plugin: commands/$name (exists in repo)"; DRIFT=$((DRIFT + 1)); }
done < <(find "$ROOT/.claude/commands" -type f -name 'hbr-*' 2>/dev/null | sort)

echo
if [ "$DRIFT" -eq 0 ]; then
  echo "$CHECKED files checked — all in sync"
else
  echo "$CHECKED files checked — $DRIFT out of sync"
  echo
  echo "plugins/multi-agent-example/ is canonical. Copy from there to .claude/, then re-run."
fi

[ "$DRIFT" -eq 0 ]
