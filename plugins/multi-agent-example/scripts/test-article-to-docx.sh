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
skip() { echo "  skip  $1"; }
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
  # A SECOND ordered list, separated from the first by prose. Without it the numbering
  # assertion below cannot fail: one bullet list plus one numbered list already yields
  # two distinct numIds whether or not each list gets its own counter.
  echo 'Then measure whether any of it worked.'
  echo
  echo '### What To Track'
  echo
  echo '1. Cycle time end to end'
  echo '2. Escalation rate'
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
# Every unzip-based assertion is guarded on unzip existing. Redirecting a missing
# command's output leaves an empty file, which is indistinguishable from a broken
# document — and would report three confident, specific, wrong failures against a
# renderer that worked perfectly.
if command -v unzip > /dev/null; then
  unzip -l "$OUT" > "$TMP/listing.txt" 2>/dev/null
  if grep -q 'word/document.xml' "$TMP/listing.txt"; then
    ok "valid .docx (ZIP containing word/document.xml)"
  else
    bad "not a valid .docx"
  fi
else
  skip "structure checks (unzip unavailable)"
fi

# --- Content --------------------------------------------------------------

# Guarded on pandoc, and the whole section skipped without it. The "no raw markdown
# leaked" assertion below is a NEGATIVE grep, so an empty extraction makes it pass: it
# would report the document clean precisely when the extraction that proves it never
# ran. That is the one assertion standing between a mangled document and the deliverable,
# so it must never be able to go green by accident.
if ! command -v pandoc > /dev/null; then
  skip "content checks (pandoc unavailable — cannot read text back out of the .docx)"
else

# Normalised to one line: pandoc hard-wraps its plain output, so a multi-word
# needle would otherwise straddle a line break and never match.
TEXT="$TMP/plain.txt"
pandoc -f docx -t plain "$OUT" 2>/dev/null | tr '\n' ' ' | tr -s ' ' > "$TEXT"

if [ ! -s "$TEXT" ]; then
  bad "pandoc produced no text from the .docx"
fi

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

fi  # end pandoc guard

if command -v unzip > /dev/null; then
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

  # Two separate ordered lists must not share one counter, or the second renders as
  # 4, 5, 6 instead of restarting at 1. The fixture has one bullet list and two ordered
  # lists, so a correct render produces three distinct w:numId values. Sharing one
  # counter produces two — which is why the fixture needs the second ordered list.
  NUM_IDS="$(grep -o '<w:numId w:val="[0-9]*"' "$TMP/document.xml" | sort -u | wc -l | tr -d ' ')"
  if [ "${NUM_IDS:-0}" -ge 3 ]; then
    ok "each ordered list gets its own numbering instance ($NUM_IDS distinct)"
  else
    bad "ordered lists share one numbering instance ($NUM_IDS distinct, expected 3) — the second list will not restart at 1"
  fi
else
  skip "hyperlink, heading-style and list-numbering checks (unzip unavailable)"
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
