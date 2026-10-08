#!/usr/bin/env bash
# Asserts the worked-example page's fenced file blocks match the committed example folder.
#   check (default):   every `<!-- file: P -->` block == examples/weekly-status-report/P (byte for byte),
#                      except the allowed paths; every `<!-- excerpt: P -->` block appears verbatim inside P.
#   --extract DIR:     write every `file:` block to DIR/P (bootstrap; never run against the real folder
#                      after it exists unless you mean to overwrite).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAGE="$ROOT/src/content/docs/ai-workflow-framework/examples/worked-example.md"
FOLDER="$ROOT/examples/weekly-status-report"
MODE="${1:-check}"; OUT="${2:-}"

# Allowed differences (path → reason). Keep in step with the spec's Fidelity rules.
# (A case statement, not an associative array: macOS ships bash 3.2.)
allowed_reason() {
  case "$1" in
    outputs/ai-opportunity-report.md) echo "page trims to two of four opportunities" ;;
    outputs/weekly-status-report/test-results-2026-06-05.md|outputs/weekly-status-report/test-results-2026-06-08.md) echo "page trims check lists and cards to six lines per scenario" ;;
    outputs/weekly-status-report/design-spec.md) echo "page compacts the Self-Test Summary" ;;
    outputs/weekly-status-report/skill/weekly-status-report/SKILL.md) echo "page shows the skill as Build created it; folder holds the post-fix version" ;;
    *) echo "" ;;
  esac
}

PASS=0; FAIL=0
ok()  { echo "  ok    $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL+1)); }

# Walk the page: a marker line, then a fence line, then content until the matching closing fence.
# Blocks are emitted to a temp dir as NNN.<kind>.<path-with-slashes-as-__>.
TMP=$(mktemp -d)
awk -v out="$TMP" '
  function flush() { if (f) { close(f); f="" } }
  /^<!-- (file|excerpt|none)(: [^ ]+)? -->$/ {
    kind=$2; sub(/:$/,"",kind); p=($3=="-->")?"":$3; pending=1; next
  }
  pending && /^(````|```)/ {
    match($0,/^`+/); fence=substr($0,1,RLENGTH); n++; pp=p; gsub("/","__",pp)
    f=sprintf("%s/%03d.%s.%s", out, n, kind, (pp==""?"-":pp)); pending=0; inblock=1; next
  }
  inblock && $0==fence { inblock=0; flush(); next }
  inblock { print > f; next }
  /^(````|```)/ && !inblock && !pending { unmarked++; print "UNMARKED fence at line " NR > "/dev/stderr" }
  END { if (unmarked) exit 3 }
' "$PAGE" || { echo "  FAIL  fenced block(s) without a marker (see above)"; exit 1; }

shopt -s nullglob
for blk in "$TMP"/*; do
  name=$(basename "$blk"); kind=${name#*.}; kind=${kind%%.*}; p=${name#*.*.}; p=${p//__//}
  case "$kind" in
    none) ok "unverified block (${p:-no file}) skipped by marker" ;;
    file)
      target="$FOLDER/$p"
      if [ "$MODE" = "--extract" ]; then mkdir -p "$(dirname "$OUT/$p")"; cp "$blk" "$OUT/$p"; ok "extracted $p"; continue; fi
      [ -f "$target" ] || { bad "$p: folder file missing"; continue; }
      if cmp -s "$blk" "$target"; then ok "$p matches the page"
      elif [ -n "$(allowed_reason "$p")" ]; then ok "$p differs as allowed: $(allowed_reason "$p")"
      else bad "$p differs from the page and is not an allowed difference"; diff -u "$blk" "$target" | head -20 | sed 's/^/        /'; fi ;;
    excerpt)
      target="$FOLDER/$p"
      [ "$MODE" = "--extract" ] && { ok "excerpt $p (not extracted)"; continue; }
      [ -f "$target" ] || { bad "$p: folder file missing (excerpt)"; continue; }
      if python3 - "$blk" "$target" <<'PY'
import sys; blk=open(sys.argv[1]).read().strip(); tgt=open(sys.argv[2]).read()
sys.exit(0 if blk in tgt else 1)
PY
      then ok "excerpt of $p appears verbatim"; else bad "excerpt of $p not found verbatim in the folder file"; fi ;;
  esac
done
rm -rf "$TMP"
echo; echo "$PASS ok, $FAIL bad"; [ "$FAIL" -eq 0 ]
