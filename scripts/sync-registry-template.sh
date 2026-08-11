#!/usr/bin/env bash
#
# sync-registry-template.sh — rsync registry-template/ (canonical, in this repo) to the
# jamesgray-ai/ai-registry-template clone (default ~/Code/jamesgray/ai-registry-template,
# override with AI_REGISTRY_TEMPLATE_DIR). That clone is the starter repo students
# actually pull down — same "canonical vs what ships" shape as sync-plugins.sh, minus
# the plugin.json version bump this repo has no equivalent of.
#
# Usage: ./scripts/sync-registry-template.sh
#
# What this does:
#   1. Runs check-registry-consistency.sh (no --full — the doc-migration checks land
#      in Batch E; add --full to this call once that's done).
#   2. Runs check-plugin-sync.sh registry-template and, if it reports drift, shows the
#      report and requires acknowledgment (interactive, or SYNC_ACK_DRIFT=1) before
#      overwriting the clone — same convention as sync-plugins.sh's non-multi-agent-example
#      branch, because at sync time drift is usually the release payload, not a mistake.
#   3. Rsyncs registry-template/ -> the clone, deleting anything the clone has that
#      canonical doesn't, excluding .git.
#
# What this does NOT do:
#   - Commit or push anywhere, in this repo or the clone. You review and commit the
#     clone's changes yourself, same "you drive both pushes" doctrine as sync-plugins.sh.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$ROOT/registry-template"
DEST_DIR="${AI_REGISTRY_TEMPLATE_DIR:-$HOME/Code/jamesgray/ai-registry-template}"

# Pre-flight
[ -d "$SRC_DIR" ] || { echo "Error: $SRC_DIR not found" >&2; exit 1; }
[ -d "$DEST_DIR" ] || { echo "Error: $DEST_DIR not found — clone jamesgray-ai/ai-registry-template first (or set AI_REGISTRY_TEMPLATE_DIR)" >&2; exit 1; }
[ -f "$ROOT/scripts/check-registry-consistency.sh" ] || { echo "Error: scripts/check-registry-consistency.sh is missing — refusing to sync unverified." >&2; exit 1; }
[ -f "$ROOT/scripts/check-plugin-sync.sh" ] || { echo "Error: scripts/check-plugin-sync.sh is missing — refusing to sync unverified." >&2; exit 1; }

# Guard against a mis-set AI_REGISTRY_TEMPLATE_DIR nuking an unrelated directory.
# Unlike sync-plugins.sh's DEST_DIR — a namespaced plugins/<name>/ subpath — this
# DEST_DIR is the raw env var, so `rsync --delete` below treats it as its own root:
# a wrong-but-existing path puts everything in that directory in the blast radius.
# Refuse to proceed unless DEST_DIR actually looks like an ai-registry-template clone:
# a real .git, plus either the registry/ dir a real clone has, or nothing else at all
# (a fresh `git clone` before this script has ever populated it).
dest_looks_like_template_clone() {
  local dir="$1"
  [ -d "$dir/.git" ] || return 1
  [ -d "$dir/registry" ] && return 0
  # Empty apart from .git counts as a fresh clone.
  [ -z "$(find "$dir" -mindepth 1 -maxdepth 1 -not -name '.git')" ]
}

if ! dest_looks_like_template_clone "$DEST_DIR"; then
  echo "Error: refusing to sync: $DEST_DIR does not look like an ai-registry-template clone." >&2
  echo "Expected layout: a git clone containing .git/ and registry/ (or an empty fresh clone with just .git/)." >&2
  exit 1
fi

# Registry consistency first — no point shipping a template that already disagrees with
# itself. Not --full yet: the doc-migration checks it adds depend on Batch E, which
# hasn't landed. Add --full here once it has.
"$ROOT/scripts/check-registry-consistency.sh" || { echo "Error: registry consistency failed" >&2; exit 1; }

# Drift check against the clone. `|| CHECK_RC=$?` keeps set -e from aborting before the
# code is inspected, same as sync-plugins.sh.
CHECK_RC=0
AI_REGISTRY_TEMPLATE_DIR="$DEST_DIR" bash "$ROOT/scripts/check-plugin-sync.sh" registry-template || CHECK_RC=$?
if [ "$CHECK_RC" -ge 2 ]; then
  echo "Error: drift check could not run (exit $CHECK_RC). Fix that before syncing." >&2
  exit 1
fi
if [ "$CHECK_RC" -eq 1 ]; then
  echo
  echo "The drift above is what this sync will overwrite in the clone"
  echo "(and any 'MISSING in canonical' files will be deleted from it)."
  if [ "${SYNC_ACK_DRIFT:-}" = "1" ]; then
    echo "SYNC_ACK_DRIFT=1 — drift acknowledged, proceeding."
  elif [ -t 0 ]; then
    read -r -p "Ship these changes? [y/N] " REPLY
    case "$REPLY" in
      y|Y|yes|YES) ;;
      *) echo "Error: drift not acknowledged — sync aborted." >&2; exit 1 ;;
    esac
  else
    echo "Error: unacknowledged drift and no terminal to confirm on." >&2
    echo "Review the report above, then re-run with SYNC_ACK_DRIFT=1 to ship it." >&2
    exit 1
  fi
fi

echo "Syncing registry-template/ -> $DEST_DIR"
rsync -av --delete --exclude '.git' "$SRC_DIR/" "$DEST_DIR/"

cat <<EOF

Synced. registry-template/ -> $DEST_DIR

This script does NOT commit or push. Review the changes in the clone, then commit and
push there yourself.
EOF
