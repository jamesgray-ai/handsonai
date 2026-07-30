#!/usr/bin/env bash
# Tests for scripts/article-to-docx.js — the pipeline's Word renderer.
#
# Run: bash scripts/test-article-to-docx.sh

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Go through the wrapper, not straight to node. On a fresh install the `docx` package is
# not present, and only the wrapper installs it — testing the raw renderer means the
# whole suite fails for anyone who just installed the plugin.
RENDER="$(dirname "${BASH_SOURCE[0]}")/render-docx.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0

ok()   { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }
check() { if [ "$1" = "0" ]; then ok "$2"; else bad "$2"; fi; }

echo "article-to-docx.js"

# --- Fixture --------------------------------------------------------------

FIXTURE="$TMP/article.md"
{
  echo '---'
  echo 'title: When Agents Earn Their Keep'
  echo 'subtitle: What separates the companies getting returns from the ones running pilots'
  echo 'author: James Gray'
  echo 'date: 2026-07-30'
  echo '---'
  echo
  echo '## The Big Idea'
  echo
  echo 'Most companies deploying AI agents are **measuring the wrong thing**. They track'
  echo 'model accuracy when they should track *cycle time*. See [the research](https://hbr.org/example).'
  echo
  echo '> The agents that paid for themselves were the ones nobody had to supervise.'
  echo
  echo '### Three Signals'
  echo
  echo '- Ownership sits with an operating leader, not a lab'
  echo '- The workflow was already measured before automation'
  echo '- Escalation paths were designed first'
  echo
  echo 'Consider the numbers. A firm that cut handling time by 40 percent did so by'
  echo 'narrowing scope, not widening it.'
  echo
  echo '## What To Do Monday'
  echo
  echo '1. Pick one measured workflow'
  echo '2. Instrument the handoffs'
  echo '3. Set an escalation rule'
  echo
  echo '## Sources'
  echo
  echo '- Harvard Business Review, "Agents at Work" (2026) — https://hbr.org/example'
} > "$FIXTURE"

OUT="$TMP/article.docx"

# --- Render ---------------------------------------------------------------

bash "$RENDER" "$FIXTURE" "$OUT" > "$TMP/render.log" 2>&1
check "$?" "renders without error"
[ -s "$OUT" ] && ok "output file is non-empty" || bad "output file is missing or empty"

# --- Structure ------------------------------------------------------------

# Note: capture command output to files before grepping. Piping straight into
# `grep -q` under `set -o pipefail` reports failure even on a match, because grep
# exits early and the upstream command dies of SIGPIPE.
unzip -l "$OUT" > "$TMP/listing.txt" 2>/dev/null
if grep -q 'word/document.xml' "$TMP/listing.txt"; then
  ok "valid .docx (ZIP containing word/document.xml)"
else
  bad "not a valid .docx"
fi

# --- Content --------------------------------------------------------------

# Normalised to one line: pandoc hard-wraps its plain output, so a multi-word
# needle would otherwise straddle a line break and never match.
TEXT="$TMP/plain.txt"
pandoc -f docx -t plain "$OUT" 2>/dev/null | tr '\n' ' ' | tr -s ' ' > "$TEXT"

for needle in \
  "When Agents Earn Their Keep" \
  "James Gray" \
  "The Big Idea" \
  "Three Signals" \
  "nobody had to supervise" \
  "Ownership sits with an operating leader" \
  "Pick one measured workflow" \
  "Sources"
do
  if grep -qF "$needle" "$TEXT"; then
    ok "contains: $needle"
  else
    bad "missing: $needle"
  fi
done

# Markdown syntax must be consumed, not passed through literally.
if grep -qE '\*\*|## |\]\(http' "$TEXT"; then
  bad "raw markdown leaked into the document"
else
  ok "no raw markdown syntax in output"
fi

# Bold/italic must survive as real formatting, not be dropped.
if grep -q 'measuring the wrong thing' "$TEXT"; then
  ok "bold text preserved as content"
else
  bad "bold text lost"
fi

# Links must survive with their target.
unzip -p "$OUT" word/_rels/document.xml.rels > "$TMP/rels.xml" 2>/dev/null
if grep -q 'hbr.org/example' "$TMP/rels.xml"; then
  ok "hyperlink target preserved"
else
  bad "hyperlink target lost"
fi

# Headings must use built-in styles so Word's navigation pane and TOC work.
unzip -p "$OUT" word/document.xml > "$TMP/document.xml" 2>/dev/null
if grep -q 'w:val="Heading1"' "$TMP/document.xml"; then
  ok "uses built-in heading styles"
else
  bad "headings are not built-in styles"
fi

# --- Pagination -----------------------------------------------------------

if command -v soffice > /dev/null && command -v pdfinfo > /dev/null; then
  (cd "$TMP" && soffice --headless --convert-to pdf "$OUT" > /dev/null 2>&1)
  PDF="$TMP/article.pdf"
  if [ -s "$PDF" ]; then
    PAGES="$(pdfinfo "$PDF" 2>/dev/null | awk '/^Pages:/ {print $2}')"
    if [ "${PAGES:-0}" -ge 2 ]; then
      ok "paginates (title page + body = $PAGES pages)"
    else
      bad "expected at least 2 pages, got ${PAGES:-unknown}"
    fi
  else
    bad "LibreOffice could not open the .docx"
  fi
else
  echo "  skip  pagination (soffice/pdfinfo unavailable)"
fi

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
