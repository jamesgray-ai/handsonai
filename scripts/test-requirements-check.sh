#!/usr/bin/env bash
# Tests for registry-template/tools/requirements-check.js (T14): the
# requirements validator Deconstruct runs before it saves requirements.md and
# Design runs on entry. Its specification is deconstruct.md 12.6.
#
# 1. Every requirements.md in framework-fixtures/ that is in this release's
#    format passes; every earlier-version one (no `revision:`) fails.
# 2. Hand-written valid variants (Path: none, "some of each", revisions log,
#    the one-line Security forms) pass.
# 3. One planted miss of each kind fails, with a message naming the section
#    and the line. Planted variants are made in a mktemp dir from
#    framework-fixtures/states/s08-test-needed/ and removed on exit; nothing
#    planted is committed.
# 4. The plugin copy is byte-for-byte the canonical one.
#
# Follows the ok/bad + summary house style of scripts/test-compose-registry.sh.
# Run: bash scripts/test-requirements-check.sh

set -uo pipefail

PASS=0
FAIL=0
ok()  { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad() { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHECK="$REPO_ROOT/registry-template/tools/requirements-check.js"
PLUGIN_COPY="$REPO_ROOT/plugins/handsonai/tools/requirements-check.js"
FIXTURES="$REPO_ROOT/framework-fixtures"
BASE="$FIXTURES/states/s08-test-needed"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

run_check() {  # <workflow dir> [options...]: runs from the folder, so messages read requirements.md:<line>
  local wf="$1"; shift
  (cd "$wf" && node "$CHECK" requirements.md "$@" 2>&1)
}

# ---------------------------------------------------------------- 1. fixtures
echo "Fixtures in framework-fixtures/"
current=0; earlier=0
while IFS= read -r f; do
  rel="${f#"$FIXTURES"/}"
  if head -5 "$f" | grep -q '^revision:'; then
    current=$((current + 1))
    out=$(node "$CHECK" "$f" 2>&1) && ok "valid: $rel" || { bad "should pass: $rel"; echo "$out" | sed 's/^/        /'; }
  else
    earlier=$((earlier + 1))
    out=$(node "$CHECK" "$f" 2>&1)
    if [ $? -eq 1 ] && grep -q 'earlier version' <<<"$out"; then ok "earlier version fails: $rel"
    else bad "earlier version should fail naming it: $rel"; fi
  fi
done < <(find "$FIXTURES" -name requirements.md | sort)
echo "  ($current in this release's format, $earlier earlier-version)"

# ---------------------------------------------------------------- helpers
plant() {  # <case name> [no-registry|with-registry]: copies the base workspace; echoes the workflow folder
  local d="$TMP/$1"
  mkdir -p "$d"
  cp -R "$BASE/${2:-no-registry}/." "$d/"
  echo "$d/framework/client-follow-up"
}
edit() {  # <file> <perl -0 program>: the edit must change the file, so no planted case is vacuous
  local before; before=$(cat "$1")
  perl -0pi -e "$2" "$1"
  [ "$before" != "$(cat "$1")" ] || { echo "  (edit made no change to $1: $2)" >&2; return 1; }
}
expect() {  # <description> <workflow dir> <regex the output must match> [options...]
  local desc="$1" wf="$2" want="$3"; shift 3
  local out rc
  out=$(run_check "$wf" "$@"); rc=$?
  if [ $rc -ne 1 ]; then bad "$desc (exit $rc, wanted 1)"; echo "$out" | sed 's/^/        /'; return; fi
  if grep -Eq "$want" <<<"$out"; then ok "$desc"
  else bad "$desc (no line matching: $want)"; echo "$out" | sed 's/^/        /'; fi
}
expect_ok() {  # <description> <workflow dir> [options...]
  local desc="$1" wf="$2"; shift 2
  local out
  out=$(run_check "$wf" "$@") && ok "$desc" || { bad "$desc"; echo "$out" | sed 's/^/        /'; }
}

# ---------------------------------------------------------------- 2. valid variants
echo "Valid variants"
wf=$(plant base); expect_ok "base fixture (no registry)" "$wf"
wf=$(plant base-reg with-registry); expect_ok "base fixture (with registry)" "$wf"
wf=$(plant base-save); expect_ok "base fixture, --before-save" "$wf" --before-save

# A: goal-driven, Path: none, no gates, nothing tripped, revisions log with plan_unaffected
mkdir -p "$TMP/goal/framework/market-scan/inputs" "$TMP/goal/framework/market-scan/context"
GOAL="$TMP/goal/framework/market-scan"
cat > "$GOAL/requirements.md" <<'EOF'
---
revision: 3
track: full
revisions:
  - revision: 2
    by: deconstruct
    lines: [AC3, R2]
  - revision: 3
    by: test
    lines: [AC2]
    plan_unaffected: true
---

# Market Scan — Workflow Requirements

## Goal
For each Monday, a one-page Markdown market scan to you, ready for you to read before the team meeting.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Faster product decisions |
| Desired Outcome | The team starts each week knowing what competitors shipped |
| Measure | Minutes spent on the scan each week |
| Baseline | 90 minutes a week · Measured |
| Target | — |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Market Scan |
| Description | Summarises what each competitor shipped last week, from the team's own notes. |
| Trigger | Monday morning |
| Owner | Head of Product |
| Lens | Organizational |
| Stakeholders | Product team |

## Path

Method preference: AI works it out each time

Path: none — the AI plans each run from the goal

### Decisions

- D1: When a competitor has no notes this week, it says so in one line · settled by: a rule on a value · value read by AI

## Inputs

- I1 · last week's competitor notes · from C1 · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Competitor notes | All | Exists | Internal | Authored | Yes | `context/C1-competitor-notes.md` | One section per competitor |
| C2 | Scan template | — | Needs Creation | Internal | Authored | Yes | Create as `context/C2-scan-template.md` | The scan's headings |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every competitor in C1 has its own line.
2. **AC2** — The scan fits on one page.
3. **AC3** — Each item names the note it came from.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Quiet week (proposed) | `inputs/E1-quiet-week.md` — notes from a week with one release | One line per competitor, most saying nothing shipped | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Always | It always names the note each item came from. |
| R2 | Never | It never guesses at a release date. |

## Human Gates

Runs: with you

No human gates — the workflow runs end-to-end with final review only.

## Security, Privacy & Safety

No sensitivity constraints — personal data only, read-only, human-triggered.

Governing regime: None

### Writes
None
EOF
printf 'source: deconstruct\ntests: AC1, AC2, R1\n\nAcme: shipped a pricing page.\nBeta Corp: nothing this week.\n' > "$GOAL/inputs/E1-quiet-week.md"
expect_ok "Path: none, no gates, nothing tripped, revisions with plan_unaffected" "$GOAL"

# C: the prohibition-only one-line form
cp -R "$TMP/goal" "$TMP/prohibit"
PRO="$TMP/prohibit/framework/market-scan"
edit "$PRO/requirements.md" 's/No sensitivity constraints — personal data only, read-only, human-triggered\.\n/No sensitivity constraints beyond the prohibition below — personal data only, read-only, human-triggered.\n\n### Prohibited actions\n| ID | Constraint | Source |\n|---|---|---|\n| P1 | It never shares the scan outside the product team, whoever asks. | Head of Product |\n/'
expect_ok "one-line Security form with a stated prohibition" "$PRO"

# B: "some of each", tags in full, External and Confidential rows, the AI's part
cp -R "$BASE/no-registry/." "$TMP/mixed/"
MIX="$TMP/mixed/framework/client-follow-up"
edit "$MIX/requirements.md" 's/Method preference: same way every time/Method preference: some of each/;
  s/- Step 1 — Read the call notes · produces a list of decisions and next steps · fixed \(your judgment\)/- Step 1 — Read the call notes · produces a list of decisions and next steps · uses C1, C2 · fixed (policy) · (account team) · proposed by AI\n- The AI plans this part/;
  s/(- Step 3 — Review and send · produces the sent email · fixed \(your judgment\) · \(you\))/$1 · parallel with Step 2/;
  s/\| C1 \| Follow-up style guide \| Step 2 \|/| C1 | Follow-up style guide | Step 2, the AI\x27s part after Step 1 |/;
  s/(\| C1 \| Follow-up style guide .*\n)/$1| C2 | Client account record | Step 1 | Exists | Confidential | External | Partial | HubSpot, through the HubSpot connection | Contacts and past calls |\n/;
  s/\*Scope: writes to a live system\*\n/*Scope: writes to a live system; reads content nobody on the team wrote; handles data you\x27d be uncomfortable seeing outside the company*\n\n### Boundaries\n| ID | Constraint | Source |\n|---|---|---|\n| P3 | Client records stay in HubSpot and the draft. | Self |\n\n### Access\n| ID | Constraint | Source |\n|---|---|---|\n| P4 | Only the account team sees the draft. | Self |\n/;
  s/\| G1 \| Step 3 \|/| G1 | the AI\x27s part after Step 1 |/'
expect_ok "\"some of each\", every step tag, External and Confidential rows" "$MIX"

# ---------------------------------------------------------------- 3. planted misses
echo "Planted misses (one of each kind)"
R=requirements.md

wf=$(plant fm-no-revision); edit "$wf/$R" 's/^revision: 1\n//m'
expect "frontmatter: no revision (earlier version)" "$wf" "^$R:2 · frontmatter · no \`revision:\`.*earlier version"

wf=$(plant fm-no-frontmatter); edit "$wf/$R" 's/\A---\n.*?\n---\n//s'
expect "frontmatter: missing altogether" "$wf" "^$R:1 · frontmatter · no frontmatter"

wf=$(plant fm-track); edit "$wf/$R" 's/^track: light$/track: medium/m'
expect "frontmatter: track not light or full" "$wf" "^$R:3 · frontmatter · \`track: medium\` must be light or full"

wf=$(plant fm-revision-log); edit "$wf/$R" 's/^revision: 1$/revision: 2/m'
expect "frontmatter: revision 2 with no revisions entry" "$wf" "^$R:4 · frontmatter · no revisions entry for revision 2"

wf=$(plant fm-revisions-by); edit "$wf/$R" 's/^revision: 1\ntrack: light\nrevisions: \[\]$/revision: 2\ntrack: light\nrevisions:\n  - revision: 2\n    by: build\n    lines: [AC3]/m'
expect "frontmatter: revisions entry by a step that can't change requirements" "$wf" "^$R:5 · frontmatter · revisions entry 2: \`by\` must be deconstruct, design or test"

wf=$(plant fm-unknown-key); edit "$wf/$R" 's/^track: light$/track: light\nstatus: draft/m'
expect "frontmatter: unexpected key" "$wf" "^$R:4 · frontmatter · unexpected key \`status\`"

wf=$(plant fm-big-change-registry with-registry); edit "$wf/$R" 's/^track: light$/track: light\nbig_change: "Now logs to HubSpot, 2026-10-20"/m'
expect "frontmatter: big_change with a registry" "$wf" "^$R:4 · frontmatter · \`big_change\` appears only with no registry"

wf=$(plant fm-big-change-saved); edit "$wf/$R" 's/^track: light$/track: light\nbig_change: "Now logs to HubSpot, 2026-10-20"/m'
expect "frontmatter: big_change in a file Deconstruct is saving" "$wf" "^$R:4 · frontmatter · \`big_change\` is removed when the redo is saved" --before-save
expect_ok "frontmatter: big_change pending with no registry (not saving)" "$wf"

wf=$(plant title); edit "$wf/$R" 's/^# Client Follow-Up — Workflow Requirements$/# Client Follow-Up Requirements/m'
expect "title: wrong form" "$wf" "^$R:7 · title · the title must read"

wf=$(plant section-renamed); edit "$wf/$R" 's/^## Human Gates$/## Checkpoints/m'
expect "sections: one renamed (unexpected)" "$wf" "^$R:83 · ## Checkpoints · unexpected section"
expect "sections: one renamed (missing)" "$wf" "· ## Human Gates · section \"## Human Gates\" is missing"

wf=$(plant section-order); edit "$wf/$R" 's/(## Inputs\n\n- I1 [^\n]*\n\n)(## Context Inventory\n\n(?:\|[^\n]*\n)+)/$2\n$1/'
expect "sections: out of order" "$wf" "^$R:[0-9]+ · ## Inputs · \"## Inputs\" is out of order"

wf=$(plant section-extra); edit "$wf/$R" 's/^## Inputs$/## Notes\n\nSome notes.\n\n## Inputs/m'
expect "sections: an extra section" "$wf" "^$R:48 · ## Notes · unexpected section"

wf=$(plant baseline); edit "$wf/$R" 's/20 minutes per call · Estimated/20 minutes per call/'
expect "Value & Measurement: Baseline without Measured/Estimated/Unknown" "$wf" "^$R:19 · ## Value & Measurement · Baseline must end"

wf=$(plant lens); edit "$wf/$R" 's/\| Lens \| Individual \|/| Lens | Personal |/'
expect "Metadata: Lens value" "$wf" "^$R:30 · ## Metadata · Lens \"Personal\" must be Individual or Organizational"

wf=$(plant method-first); edit "$wf/$R" 's/Method preference: same way every time\n\n//'
expect "Path: Method preference not first" "$wf" "^$R:34 · ## Path · \`## Path\` must open with the \`Method preference:\` line"

wf=$(plant method-moved); edit "$wf/$R" 's/Method preference: same way every time\n\n(- Step 1[^\n]*\n)/$1Method preference: same way every time\n/'
expect "Path: Method preference after a step line" "$wf" "^$R:34 · ## Path · \`## Path\` must open with the \`Method preference:\` line"

wf=$(plant method-value); edit "$wf/$R" 's/Method preference: same way every time/Method preference: mostly fixed/'
expect "Path: Method preference value" "$wf" "^$R:34 · ## Path · \`Method preference: mostly fixed\` must be one of"

wf=$(plant path-none-steps); edit "$wf/$R" 's/Method preference: same way every time\n/Method preference: AI works it out each time\n\nPath: none — the AI plans each run from the goal\n/'
expect "Path: step lines under Path: none" "$wf" "^$R:38 · ## Path · \`Path: none\` has no step lines"

wf=$(plant some-of-each); edit "$wf/$R" 's/Method preference: same way every time/Method preference: some of each/'
expect "Path: \"some of each\" with no AI-plans line" "$wf" "^$R:34 · ## Path · \"some of each\" needs at least one fixed step and at least one"

wf=$(plant step-mark); edit "$wf/$R" 's/ · uses C1 · flexible · writes W1/ · uses C1 · writes W1/'
expect "step line: no fixed-or-flexible mark" "$wf" "^$R:37 · ## Path · Step 2 has no fixed-or-flexible mark"

wf=$(plant step-person-mark); edit "$wf/$R" 's/ · produces the sent email · fixed \(your judgment\) · \(you\)/ · produces the sent email · (you)/'
expect "step line: a person's step without its mark" "$wf" "^$R:38 · ## Path · Step 3 has no fixed-or-flexible mark"

wf=$(plant step-produces); edit "$wf/$R" 's/Read the call notes · produces a list of decisions and next steps · /Read the call notes · /'
expect "step line: no produces" "$wf" "^$R:36 · ## Path · Step 1 has no \`produces\`"

wf=$(plant step-order); edit "$wf/$R" 's/ · uses C1 · flexible · writes W1/ · flexible · uses C1 · writes W1/'
expect "step line: tags out of order" "$wf" "^$R:37 · ## Path · Step 2: tags out of order"

wf=$(plant step-fixed-reason); edit "$wf/$R" 's/produces a list of decisions and next steps · fixed \(your judgment\)/produces a list of decisions and next steps · fixed/'
expect "step line: fixed without its reason" "$wf" "^$R:36 · ## Path · Step 1: \"fixed\" — fixed carries its reason"

wf=$(plant step-unknown); edit "$wf/$R" 's/ · writes W1$/ · writes W1 · urgent/m'
expect "step line: unknown tag" "$wf" "^$R:37 · ## Path · Step 2: unknown tag \"urgent\""

wf=$(plant decision-shape); edit "$wf/$R" 's/- D1 \(Step 2\): When the notes name no next step, it asks you for one before drafting · settled by: your criteria/- D1 (Step 2): if no next step → ask · settled by: your criteria/'
expect "decision: not in the When…, it… shape" "$wf" "^$R:42 · ## Path · D1 isn't in the \"When…, it…\" shape"

wf=$(plant decision-settled); edit "$wf/$R" 's/settled by: your criteria/settled by: gut feel/'
expect "decision: settled-by value" "$wf" "^$R:42 · ## Path · D1: \`settled by:\` must be"

wf=$(plant detail-block); edit "$wf/$R" 's/^### Step 2 — Draft the email$/### Step 5 — Draft the email/m'
expect "detail block: no matching step" "$wf" "^$R:44 · ## Path · detail block \"Step 5\" has no matching step line"

wf=$(plant path-heading); edit "$wf/$R" 's/^### Decisions$/### Branches/m'
expect "Path: unexpected sub-heading" "$wf" "^$R:40 · ## Path · unexpected heading \"### Branches\""

wf=$(plant input-line); edit "$wf/$R" 's/- I1 · your call notes · from you, pasted into the chat · Status: available/- I1: your call notes, pasted into the chat/'
expect "Inputs: line format" "$wf" "^$R:50 · ## Inputs · input lines read"

wf=$(plant input-status); edit "$wf/$R" 's/Status: available$/Status: yes/m'
expect "Inputs: Status value" "$wf" "^$R:50 · ## Inputs · I1: Status must be"

wf=$(plant ctx-enum); edit "$wf/$R" 's/\| Exists \| Internal \| Authored \|/| Exists | Secret | Authored |/'
expect "Context Inventory: Sensitivity value" "$wf" "^$R:56 · ## Context Inventory · C1: Sensitivity must be"

wf=$(plant ctx-ref); edit "$wf/$R" 's/ · uses C1 · flexible/ · uses C5 · flexible/'
expect "cross-reference: a C# not in the Context Inventory" "$wf" "^$R:37 · ## Path · C5 isn't in the Context Inventory"

wf=$(plant ac-format); edit "$wf/$R" 's/^3\. \*\*AC3\*\* — /3. AC3 — /m'
expect "Acceptance Criteria: line format" "$wf" "^$R:64 · ## Acceptance Criteria · acceptance criteria read"

wf=$(plant ac-dup); edit "$wf/$R" 's/^3\. \*\*AC3\*\*/3. **AC2**/m'
expect "Acceptance Criteria: duplicate ID" "$wf" "^$R:64 · ## Acceptance Criteria · AC2 is used twice"

wf=$(plant ac-none); edit "$wf/$R" 's/^\d\. \*\*AC\d[^\n]*\n//mg'
expect "Acceptance Criteria: none at all" "$wf" "^$R:58 · ## Acceptance Criteria · no acceptance criteria"

wf=$(plant rule-kind); edit "$wf/$R" 's/\| R1 \| Never \|/| R1 | Must never |/'
expect "Rules: Kind value" "$wf" "^$R:79 · ## Rules & Constraints · R1: Kind \"Must never\" must be"

wf=$(plant rule-shape); edit "$wf/$R" 's/\| R1 \| Never \| It never invents/| R1 | Never | Never invent/'
expect "Rules: a Never rule not in the \"It never…\" shape" "$wf" "^$R:79 · ## Rules & Constraints · R1: a Never rule reads \"It never…\""

wf=$(plant m-line); edit "$wf/$R" 's/(\| R3 \| Fallback[^\n]*\n)/$1| M1 | Never | It never sends anything. |\n/'
expect "no M or RF lines (an M row)" "$wf" "^$R:82 · ## Rules & Constraints · \`M1\`: there are no M or RF lines"

wf=$(plant rf-revision); edit "$wf/$R" 's/^revision: 1\ntrack: light\nrevisions: \[\]$/revision: 2\ntrack: light\nrevisions:\n  - revision: 2\n    by: deconstruct\n    lines: [RF1]/m'
expect "no M or RF lines (named in the revisions log)" "$wf" "^$R:5 · frontmatter · revisions entry 2 names \`RF1\`: there are no M or RF lines"

wf=$(plant gate-runs); edit "$wf/$R" 's/Runs: with you\n\n//'
expect "Human Gates: no Runs line" "$wf" "^$R:85 · ## Human Gates · Human Gates opens with \`Runs: with you\`"

wf=$(plant gate-role); edit "$wf/$R" 's/it stops until you approve it\. · \(you\) \|/it stops until you approve it. |/'
expect "Human Gates: checkpoint without its role tag" "$wf" "^$R:89 · ## Human Gates · G1: a checkpoint ends with the role tag"

wf=$(plant gate-step); edit "$wf/$R" 's/\| G1 \| Step 3 \|/| G1 | Step 7 |/'
expect "cross-reference: Where names a step that doesn't exist" "$wf" "^$R:89 · ## Human Gates · \"Step 7\" matches no step line"

wf=$(plant p-restart); edit "$wf/$R" 's/\| P2 \|/| P1 |/'
expect "Security: P IDs restart in the second table (one series)" "$wf" "^$R:103 · ## Security, Privacy & Safety › ### Prohibited actions · P1 is used twice"

wf=$(plant p-missing); edit "$wf/$R" 's/\| ID \| Constraint \| Source \|\n\|---\|---\|---\|\n\| P2 \| /| Constraint | Source |\n|---|---|\n| /'
expect "Security: a constraint with no P ID" "$wf" "^$R:101 · ## Security, Privacy & Safety › ### Prohibited actions · the table header must be"

wf=$(plant p-source); edit "$wf/$R" 's/whoever asks\. \| Self \|/whoever asks. | |/'
expect "Security: a constraint with no Source" "$wf" "^$R:103 · ## Security, Privacy & Safety › ### Prohibited actions · P2: no Source"

wf=$(plant sec-worked); edit "$wf/$R" 's/### Traceability\n(?:\|[^\n]*\n)+\n//'
expect "Security: a tripped category not worked (writes, no Traceability)" "$wf" "^$R:91 · ## Security, Privacy & Safety · \"### Traceability\" must be worked because it writes to a live system"

wf=$(plant sec-regime); edit "$wf/$R" 's/Governing regime: None\n\n//'
expect "Security: no Governing regime line" "$wf" "^$R:91 · ## Security, Privacy & Safety · no \`Governing regime:\` line"

wf=$(plant sec-writes); edit "$wf/$R" 's/### Writes\n- W1 · Gmail · create a draft · Step 2\n?//'
expect "Security: no ### Writes" "$wf" "^$R:91 · ## Security, Privacy & Safety · no \`### Writes\` heading"

wf=$(plant write-ref); edit "$wf/$R" 's/ · writes W1$/ · writes W2/m'
expect "cross-reference: a step writes a W# not under ### Writes" "$wf" "^$R:37 · ## Path · W2 isn't under ### Writes"

wf=$(plant input-path-abs); edit "$wf/$R" 's/`inputs\/E1-acme-renewal-call\.md`/`\/Users\/dana\/inputs\/E1-acme-renewal-call.md`/'
expect "paths: an absolute input path" "$wf" "^$R:72 · ## Example Scenarios · \`/Users/dana/inputs/E1-acme-renewal-call.md\` is an absolute path"

wf=$(plant input-path-root); edit "$wf/$R" 's/`inputs\/E1-acme-renewal-call\.md`/`framework\/client-follow-up\/inputs\/E1-acme-renewal-call.md`/'
expect "paths: an input path not relative to the workflow folder" "$wf" "^$R:72 · ## Example Scenarios · \`framework/client-follow-up/inputs/E1-acme-renewal-call.md\` isn't relative to the workflow folder"

wf=$(plant input-missing); rm "$wf/inputs/E2-no-next-step.md"
expect "practice input: the file doesn't exist" "$wf" "^$R:73 · ## Example Scenarios · E2: \`inputs/E2-no-next-step.md\` doesn't exist"

wf=$(plant input-header); edit "$wf/inputs/E1-acme-renewal-call.md" 's/\Asource: deconstruct\ntests: [^\n]*\n\n//'
expect "practice input: no header lines" "$wf" "^$R:72 · ## Example Scenarios · E1: \`inputs/E1-acme-renewal-call.md\` line 1 must be the \`source:\` header"

wf=$(plant input-tests); edit "$wf/inputs/E1-acme-renewal-call.md" 's/^tests: AC1, AC2, AC3, R1, G1$/tests: AC1, AC9/m'
expect "practice input: tests an ID the file doesn't have" "$wf" "^$R:72 · ## Example Scenarios · E1: \`inputs/E1-acme-renewal-call.md\` tests AC9, which isn't in the file"

# A line Test or Design removed (build review 1, F1): an input still naming it is a note, never a
# failure, so Design's entry check doesn't stop on it; Deconstruct's pre-save run stays strict, and
# an ID no revision names still fails (the AC9 case above).
wf=$(plant removed-line)
edit "$wf/$R" 's/^revision: 1\ntrack: light\nrevisions: \[\]$/revision: 2\ntrack: light\nrevisions:\n  - revision: 2\n    by: test\n    lines: [R1]\n    plan_unaffected: true/m'
edit "$wf/$R" 's/^\| R1 \| Never \| It never invents a figure, date or commitment\. \|\n//m'
out=$(run_check "$wf"); rc=$?
if [ $rc -eq 0 ] && grep -q "note: E1: \`inputs/E1-acme-renewal-call.md\` tests R1, a line a revision removed" <<<"$out"; then
  ok "practice input: a line a revision removed is a note, exit 0"
else bad "practice input: a removed line should be a note with exit 0 (exit $rc)"; echo "$out" | sed 's/^/        /'; fi
expect "practice input: a removed line still fails before Deconstruct saves" "$wf" "tests R1, which isn't in the file" --before-save
wf=$(plant fm-flow-revision); edit "$wf/$R" 's/^revision: 1\ntrack: light\nrevisions: \[\]$/revision: 2\ntrack: light\nrevisions:\n  - { revision: 2, by: test, lines: [R1], plan_unaffected: true }/m'
expect "frontmatter: a flow-map revisions entry names the block form" "$wf" "^$R:5 · frontmatter · write each \`revisions:\` entry in block form"

wf=$(plant secret); edit "$wf/inputs/E2-no-next-step.md" 's/\z/\nAPI key: sk-live0123456789abcdefghijklmnop\n/'
expect "no saved file holds a password or key" "$wf" "^$R:73 · ## Example Scenarios · E2: \`inputs/E2-no-next-step.md\` line [0-9]+ looks like it holds a password or key"

# ---------------------------------------------------------------- 4. usage and the plugin copy
echo "Usage and the plugin copy"
out=$(node "$CHECK" "$TMP/does-not-exist" 2>&1); [ $? -eq 2 ] && ok "unreadable file exits 2" || bad "unreadable file should exit 2"
wf=$(plant folder-arg); (node "$CHECK" "$wf" >/dev/null 2>&1) && ok "accepts the workflow folder in place of the file" || bad "should accept a workflow folder"
if [ -f "$PLUGIN_COPY" ] && cmp -s "$CHECK" "$PLUGIN_COPY"; then ok "plugin copy is byte-for-byte the canonical one"
else bad "plugins/handsonai/tools/requirements-check.js differs from registry-template/tools/requirements-check.js"; fi

echo
echo "requirements-check tests: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
