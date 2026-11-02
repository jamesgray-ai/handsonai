#!/usr/bin/env bash
#
# sync-routing.sh — the AI Workflow Framework's routing rule is written once and copied
# byte for byte into every step skill, so all five skills route a workflow the same way.
#
# Canonical files (edit these, never the copies):
#   scripts/framework/routing.md   the routing rule (the spec's `references/routing.md`
#                                  block, everything between its two markers)
#   scripts/framework/test-run.sh  the test-run wrapper (optional here: copied if present)
#
# Copies:
#   plugins/handsonai/skills/{analyze,deconstruct,design,build,test}/references/routing.md
#   plugins/handsonai/skills/{build,test}/scripts/test-run.sh
#
# Usage:
#   bash scripts/sync-routing.sh                    # copy canonical -> skills, then check
#   bash scripts/sync-routing.sh --check            # fail if any copy differs (CI)
#   bash scripts/sync-routing.sh --check SPEC       # also compare routing.md with the
#                                                   # block between the markers in SPEC
#   bash scripts/sync-routing.sh --update-from SPEC # rewrite routing.md from SPEC's block,
#                                                   # copy it to the skills, then check
#
# SPEC is the private business repo's framework-rules.md. CI can't read that repo, so the
# spec comparison only runs when the path is given.
#
# Exit codes: 0 in sync, 1 drift, 2 usage error or a file is missing.
#
# What this does NOT do: run any git command. Review and commit the copies yourself.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANON_DIR="$ROOT/scripts/framework"
CANON_ROUTING="$CANON_DIR/routing.md"
CANON_TEST_RUN="$CANON_DIR/test-run.sh"
SKILLS_DIR="$ROOT/plugins/handsonai/skills"
ROUTING_SKILLS=(analyze deconstruct design build test)
TEST_RUN_SKILLS=(build test)
BEGIN_MARKER='<!-- routing.md: begin -->'
END_MARKER='<!-- routing.md: end -->'

usage() {
  sed -n '15,24p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' >&2
  exit 2
}

# Print everything strictly between the begin and end marker lines of $1, byte for byte.
# Refuses unless each marker appears exactly once, begin before end.
extract_block() {
  local spec="$1" nb ne lb le
  [ -f "$spec" ] || { echo "Error: spec not found: $spec" >&2; return 2; }
  nb=$(grep -cxF -- "$BEGIN_MARKER" "$spec" || true)
  ne=$(grep -cxF -- "$END_MARKER" "$spec" || true)
  if [ "$nb" != 1 ] || [ "$ne" != 1 ]; then
    echo "Error: $spec must hold each marker exactly once (found begin: $nb, end: $ne)." >&2
    return 2
  fi
  lb=$(grep -nxF -- "$BEGIN_MARKER" "$spec" | cut -d: -f1)
  le=$(grep -nxF -- "$END_MARKER" "$spec" | cut -d: -f1)
  [ "$lb" -lt "$le" ] || { echo "Error: in $spec the end marker comes before the begin marker." >&2; return 2; }
  sed -n "$((lb + 1)),$((le - 1))p" "$spec"
}

sync_copies() {
  local skill dest
  [ -f "$CANON_ROUTING" ] || { echo "Error: $CANON_ROUTING not found — nothing to sync." >&2; exit 2; }
  for skill in "${ROUTING_SKILLS[@]}"; do
    [ -d "$SKILLS_DIR/$skill" ] || { echo "Error: skill folder missing: $SKILLS_DIR/$skill" >&2; exit 2; }
    dest="$SKILLS_DIR/$skill/references/routing.md"
    mkdir -p "$(dirname "$dest")"
    cp "$CANON_ROUTING" "$dest"
    echo "  copied  routing.md  -> skills/$skill/references/routing.md"
  done
  if [ -f "$CANON_TEST_RUN" ]; then
    for skill in "${TEST_RUN_SKILLS[@]}"; do
      dest="$SKILLS_DIR/$skill/scripts/test-run.sh"
      mkdir -p "$(dirname "$dest")"
      cp "$CANON_TEST_RUN" "$dest"
      chmod +x "$dest"
      echo "  copied  test-run.sh -> skills/$skill/scripts/test-run.sh"
    done
  else
    echo "  skipped test-run.sh: scripts/framework/test-run.sh is not there yet."
  fi
}

# Compare copies with the canonical files; with a spec path, the canonical routing.md
# with the spec's block too. Returns 0 in sync, 1 drift, 2 missing canonical/spec.
check_copies() {
  local spec="${1:-}" skill copy drift=0 tmp rc
  [ -f "$CANON_ROUTING" ] || { echo "Error: $CANON_ROUTING not found." >&2; return 2; }

  for skill in "${ROUTING_SKILLS[@]}"; do
    copy="$SKILLS_DIR/$skill/references/routing.md"
    if [ ! -f "$copy" ]; then
      echo "  MISSING  skills/$skill/references/routing.md"; drift=1
    elif ! cmp -s "$CANON_ROUTING" "$copy"; then
      echo "  DIFFERS  skills/$skill/references/routing.md"
      diff "$CANON_ROUTING" "$copy" | sed 's/^/           /' | head -20 || true
      drift=1
    else
      echo "  ok       skills/$skill/references/routing.md"
    fi
  done

  for skill in "${TEST_RUN_SKILLS[@]}"; do
    copy="$SKILLS_DIR/$skill/scripts/test-run.sh"
    if [ ! -f "$CANON_TEST_RUN" ]; then
      if [ -f "$copy" ]; then
        echo "  ORPHAN   skills/$skill/scripts/test-run.sh (no scripts/framework/test-run.sh to match)"; drift=1
      else
        echo "  skipped  skills/$skill/scripts/test-run.sh (scripts/framework/test-run.sh not there yet)"
      fi
    elif [ ! -f "$copy" ]; then
      echo "  MISSING  skills/$skill/scripts/test-run.sh"; drift=1
    elif ! cmp -s "$CANON_TEST_RUN" "$copy"; then
      echo "  DIFFERS  skills/$skill/scripts/test-run.sh"; drift=1
    else
      echo "  ok       skills/$skill/scripts/test-run.sh"
    fi
  done

  if [ -n "$spec" ]; then
    tmp="$(mktemp)"
    rc=0
    extract_block "$spec" > "$tmp" || rc=$?
    if [ "$rc" -ne 0 ]; then rm -f "$tmp"; return 2; fi
    if cmp -s "$tmp" "$CANON_ROUTING"; then
      echo "  ok       scripts/framework/routing.md matches the spec's routing.md block"
    else
      echo "  DIFFERS  scripts/framework/routing.md vs the spec's routing.md block ($spec)"
      diff "$tmp" "$CANON_ROUTING" | sed 's/^/           /' | head -20 || true
      echo "           To take the spec's wording: bash scripts/sync-routing.sh --update-from \"$spec\""
      drift=1
    fi
    rm -f "$tmp"
  else
    echo "  skipped  spec comparison (pass the path to framework-rules.md to run it)"
  fi

  return "$drift"
}

report() {
  local rc="$1"
  echo
  case "$rc" in
    0) echo "Routing copies in sync." ;;
    1) echo "Error: routing copies have drifted. Edit scripts/framework/ (never the copies), then run: bash scripts/sync-routing.sh" >&2 ;;
    *) echo "Error: the routing check could not run." >&2 ;;
  esac
  exit "$rc"
}

MODE="${1:-sync}"
case "$MODE" in
  sync)
    [ $# -le 1 ] || usage
    echo "Syncing scripts/framework/ -> plugins/handsonai/skills/"
    sync_copies
    echo
    echo "Checking"
    RC=0; check_copies || RC=$?
    report "$RC"
    ;;
  --check)
    [ $# -le 2 ] || usage
    echo "Checking routing copies"
    RC=0; check_copies "${2:-}" || RC=$?
    report "$RC"
    ;;
  --update-from)
    [ $# -eq 2 ] || usage
    TMP="$(mktemp)"
    RC=0; extract_block "$2" > "$TMP" || RC=$?
    if [ "$RC" -ne 0 ]; then rm -f "$TMP"; exit 2; fi
    cat "$TMP" > "$CANON_ROUTING"
    rm -f "$TMP"
    echo "Wrote scripts/framework/routing.md from $2"
    sync_copies
    echo
    echo "Checking"
    RC=0; check_copies "$2" || RC=$?
    report "$RC"
    ;;
  -h|--help) usage ;;
  *) usage ;;
esac
