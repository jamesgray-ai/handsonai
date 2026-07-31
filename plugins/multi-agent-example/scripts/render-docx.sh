#!/usr/bin/env bash
#
# render-docx.sh — turn a pipeline article into a Word document, in any environment.
#
#   bash render-docx.sh <input.md> <output.docx>
#
# The docx *skill* (instructions for producing Word files) and the docx *npm package*
# (the library that writes the file) are two different things, and they are available in
# different places:
#
#   Cowork / Claude.ai   skill built in, `docx` package preinstalled  → nothing to do
#   Claude Code (local)  skill via document-skills@anthropic-agent-skills,
#                        `docx` package absent                        → install it once
#
# The docx skill's own guidance says exactly this: "docx is preinstalled — do not run
# npm install first. Only if that require fails: npm install docx."  This script is that
# rule, automated, so the publishing agent never has to guess which environment it is in.
#
# It then runs the pinned renderer rather than generating layout code on the fly, so the
# document comes out identical on every run.

set -uo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: bash render-docx.sh <input.md> <output.docx>" >&2
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Input not found: $INPUT" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RENDERER="$SCRIPT_DIR/article-to-docx.js"

if [ ! -f "$RENDERER" ]; then
  echo "Renderer not found next to this script: $RENDERER" >&2
  exit 1
fi

command -v node > /dev/null || {
  echo "Node.js is required to produce the Word document, but 'node' was not found." >&2
  echo "Install Node (https://nodejs.org) and run this again." >&2
  exit 1
}

# --- Preflight: is the docx package importable from here? -------------------

have_docx() {
  (cd "$SCRIPT_DIR" && node -e "require('docx')" > /dev/null 2>&1)
}

if ! have_docx; then
  echo "docx package not available — installing it once (this is expected on Claude Code)..."
  # --prefix, because `cd` alone does not do what the old comment claimed.
  #
  # npm picks its install location by walking UP for the nearest package.json, and
  # scripts/ has none — so from this repo the install landed in the repo root's
  # node_modules, not beside the renderer, and the .gitignore entries for
  # scripts/node_modules/ were dead. It only differed when installed as a plugin, where
  # no ancestor package.json exists. --prefix pins it either way, which is what the
  # isolation claim needed all along.
  #
  # Keep npm's output. Discarding it leaves nothing to distinguish "no network" from
  # "npm is not installed", "the plugin directory is read-only", "the registry returned
  # 403", or "the disk is full" — and the message below used to assert the network cause
  # for all of them. The re-check of have_docx is what decides success; the log is only
  # there so a failure can be diagnosed instead of guessed at.
  NPM_LOG="$(mktemp)"
  (cd "$SCRIPT_DIR" && npm install --prefix "$SCRIPT_DIR" --no-save --no-audit --no-fund docx) \
    > "$NPM_LOG" 2>&1 || true

  if ! have_docx; then
    {
      echo "Could not make the docx package available."
      echo
      echo "npm said:"
      echo
      tail -20 "$NPM_LOG" | sed 's/^/  /'
      echo
      # Note the path. `npm install docx` in the current directory does NOT help: Node
      # resolves from the renderer's own directory, which when this ships as a plugin is
      # inside the read-only plugin install, not the user's project.
      echo "Two ways forward:"
      echo
      echo "  1. Install it where the renderer can find it, then run this again:"
      echo "       (cd \"$SCRIPT_DIR\" && npm install docx)"
      echo "  2. Or produce the Word file directly with the docx skill instead of this script."
      echo
      echo "The markdown deliverable is unaffected — only the .docx step needs this."
    } >&2
    rm -f "$NPM_LOG"
    exit 1
  fi
  rm -f "$NPM_LOG"
fi

# --- Render -----------------------------------------------------------------

node "$RENDERER" "$INPUT" "$OUTPUT" || exit 1

# --- Verify: it must be a real Word file, not just a file that exists --------

if [ ! -s "$OUTPUT" ]; then
  echo "Renderer reported success but produced no file: $OUTPUT" >&2
  exit 1
fi

# Only claim the file is invalid if we could actually look inside it. `|| true` renders
# "unzip is missing" and "this is not a Word file" identical, which would fail every
# render on a machine without unzip and send the caller chasing the renderer.
if ! command -v unzip > /dev/null 2>&1; then
  echo "NOTE: unzip is not installed, so $OUTPUT could not be verified as a real Word file." >&2
else
  LISTING="$(unzip -l "$OUTPUT" 2>/dev/null || true)"
  if ! printf '%s' "$LISTING" | grep -c 'word/document.xml' > /dev/null; then
    echo "Output is not a valid Word document (no word/document.xml): $OUTPUT" >&2
    exit 1
  fi
fi

echo "OK: $OUTPUT"
