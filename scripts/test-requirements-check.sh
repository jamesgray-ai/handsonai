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
#    3b and 3c add the fields Deconstruct 3.3 brought and the shape the single
#    interview writes now (framework-fixtures/path-none/: Path: none, moments,
#    `· after [moment]`, an emptied category, law-named lines), each with its
#    valid forms and the step references such a file can't hold.
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
# An earlier file's inputs carry no expect: line. They pass Design's entry check (T13); Deconstruct's
# own pre-save run requires the line on its inputs, so a re-run fills it first (R-D9, B-M4).
wf=$(plant base-save)
expect "base fixture, --before-save: Deconstruct's inputs need their expect: line (R-D9)" "$wf" "^requirements\.md:72 · ## Example Scenarios · E1: \`inputs/E1-acme-renewal-call\.md\` has no \`expect:\` line" --before-save

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

# ---------------------------------------------------------------- 3b. the fields Deconstruct 3.3 adds
# Deconstruct requirements v3.3, section 6 (Validator and tools), items 1-7. One committed
# fixture (framework-fixtures/edge/e-new-fields) carries every new field; each item then gets its valid forms and its planted misses.
# Every field is optional, so the earlier fixtures above keep passing (T13).
echo "New fields (Deconstruct v3.3: Starts, Per run, Remembers, criteria, D lines in tests, expect, after each run, Policy check, glosses)"
NEWF_ROOT="$TMP/newf"
NEWF="$NEWF_ROOT/framework/client-follow-up"
# the shared committed fixture (stage 10), also read by the Design and Test evals: revision 1, as Deconstruct
# writes it. Section 3b's revision cases need Test's policy confirmation on top (revision 2, `by: test`,
# `lines: [Policy check]`), so the copy gets that entry here, as the inline fixture of stage 3 had it.
mkdir -p "$NEWF_ROOT"
cp -R "$FIXTURES/edge/e-new-fields/no-registry/." "$NEWF_ROOT/"
edit "$NEWF/requirements.md" 's/\A---\nrevision: 1\ntrack: full\nrevisions: \[\]\n---\n/---\nrevision: 2\ntrack: full\nrevisions:\n  - revision: 2\n    by: test\n    lines: [Policy check]\n    plan_unaffected: true\n---\n/'
newf() {  # <case name>: a fresh copy of the new-fields workspace; echoes the workflow folder
  local d="$TMP/nf-$1"
  rm -rf "$d"; cp -R "$NEWF_ROOT" "$d"
  echo "$d/framework/client-follow-up"
}
R=requirements.md
wf=$(newf ok); expect_ok "a file with every new field passes" "$wf"
expect_ok "...and passes Deconstruct's pre-save run (every Deconstruct input has expect:)" "$wf"

# 1. Metadata: Starts, Per run, Remembers (optional, in the explicit order)
for v in 'you' 'you, when a client asks for a summary' 'schedule: on the 1st of each month' \
         'event: a new form reply arrives · checked every 30 minutes' 'event: a new form reply arrives · checked as often as it can'; do
  wf=$(newf starts-ok); edit "$wf/$R" "s/\\| Starts \\| schedule: every Friday afternoon \\|/| Starts | $v |/"
  expect_ok "Starts: \"$v\" passes" "$wf"
done
wf=$(newf perrun-one); edit "$wf/$R" 's/\| Per run \| a batch of the week.s client calls \|/| Per run | one client call |/'
expect_ok "Per run: \"one …\" passes" "$wf"
wf=$(newf starts-bad); edit "$wf/$R" 's/\| Starts \| schedule: every Friday afternoon \|/| Starts | sometimes |/'
expect "Metadata: a Starts value outside its four forms" "$wf" "^$R:[0-9]+ · ## Metadata · \"Starts\" must read"
wf=$(newf starts-event-no-check); edit "$wf/$R" 's/\| Starts \| schedule: every Friday afternoon \|/| Starts | event: a new form reply arrives |/'
expect "Metadata: an event Starts with no checking interval" "$wf" "^$R:[0-9]+ · ## Metadata · \"Starts\" must read"
wf=$(newf perrun-bad); edit "$wf/$R" 's/\| Per run \| a batch of the week.s client calls \|/| Per run | 40 a week |/'
expect "Metadata: a Per run value outside its two forms" "$wf" "^$R:[0-9]+ · ## Metadata · \"Per run\" must read"
wf=$(newf remembers-empty); edit "$wf/$R" 's/\| Remembers \| which calls it has already followed up \|/| Remembers |  |/'
expect "Metadata: an empty Remembers row" "$wf" "^$R:[0-9]+ · ## Metadata · \"Remembers\" has no value"
wf=$(newf starts-order); edit "$wf/$R" 's/(\| Trigger \| [^\n]*\n)(\| Starts \| [^\n]*\n)/$2$1/'
expect "Metadata: Starts before Trigger is out of order" "$wf" "^$R:[0-9]+ · ## Metadata · row \"Trigger\" is out of order"
wf=$(newf remembers-order); edit "$wf/$R" 's/(\| Owner \| [^\n]*\n)/| Remembers | which calls it has already followed up |\n$1/; s/(\| Runs today \| [^\n]*\n)\| Remembers \| [^\n]*\n/$1/'
expect "Metadata: Remembers before Owner is out of order" "$wf" "^$R:[0-9]+ · ## Metadata · row \"Owner\" is out of order"

# 2. Decision lines: criteria after any settled-by value, never with " · " inside
wf=$(newf crit-sep); edit "$wf/$R" 's/criteria: no line in the notes says who does what next/criteria: no owner · no date/'
expect "decision: criteria text holding \" · \"" "$wf" "^$R:[0-9]+ · ## Path · D1: the criteria text can't contain \" · \""
wf=$(newf crit-order); edit "$wf/$R" 's/ · criteria: no line in the notes says who does what next · value read by AI/ · value read by AI · criteria: no line in the notes says who does what next/'
expect "decision: criteria after value read by AI" "$wf" "^$R:[0-9]+ · ## Path · D1: after \`settled by:\`, only"
wf=$(newf crit-empty); edit "$wf/$R" 's/ · criteria: no line in the notes says who does what next/ · criteria:/'
expect "decision: an empty criteria tag" "$wf" "^$R:[0-9]+ · ## Path · D1: \`· criteria:\` has no text"
wf=$(newf crit-unknown); edit "$wf/$R" 's/ · criteria: no line in the notes says who does what next · value read by AI/ · urgent · value read by AI/'
expect "decision: an unknown tag after settled by" "$wf" "^$R:[0-9]+ · ## Path · D1: after \`settled by:\`, only"
wf=$(newf crit-settled); edit "$wf/$R" 's/settled by: open judgment · criteria/settled by: gut feel · criteria/'
expect "decision: a settled-by value outside the three, with criteria after it" "$wf" "^$R:[0-9]+ · ## Path · D3: \`settled by:\` must be"

# 3. tests: may name D lines, which must exist in ### Decisions
wf=$(newf tests-d9); edit "$wf/inputs/E3-already-handled.md" 's/^tests: D2$/tests: D9/m'
expect "practice input: tests a D line ### Decisions doesn't have" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E3: \`inputs/E3-already-handled.md\` tests D9, which isn't in the file"
wf=$(newf tests-p); edit "$wf/inputs/E1-renewal-call.md" 's/^tests: AC1, AC2, R1, G1$/tests: AC1, P4/m'
expect "practice input: a listed input names a P line" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E1: \`inputs/E1-renewal-call.md\` tests \"P4\"; \`tests:\` names AC, R, G and D lines only"
wf=$(newf d-removed)
edit "$wf/$R" 's/^revision: 2$/revision: 3/m; s/(    plan_unaffected: true\n)---/$1  - revision: 3\n    by: test\n    lines: [D2]\n    plan_unaffected: true\n---/'
edit "$wf/$R" 's/^- D2 \(Step 3\)[^\n]*\n//m'
out=$(run_check "$wf"); rc=$?
if [ $rc -eq 0 ] && grep -q "note: E3: \`inputs/E3-already-handled.md\` tests D2, a line a revision removed" <<<"$out"; then
  ok "practice input: a D line a revision removed is a note, exit 0"
else bad "practice input: a removed D line should be a note with exit 0 (exit $rc)"; echo "$out" | sed 's/^/        /'; fi
expect "practice input: a removed D line still fails before Deconstruct saves" "$wf" "tests D2, which isn't in the file" --before-save

# 4. Input headers: an optional expect: line 3, the blank line 4, content from line 5
wf=$(newf expect-empty); edit "$wf/inputs/E1-renewal-call.md" 's/^expect: [^\n]*$/expect:/m'
expect "practice input: an empty expect: line" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E1: \`inputs/E1-renewal-call.md\` line 3, \`expect:\`, is empty"
wf=$(newf expect-no-blank); edit "$wf/inputs/E1-renewal-call.md" 's/(^expect: [^\n]*\n)\n/$1/m'
expect "practice input: no blank line after expect:" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E1: \`inputs/E1-renewal-call.md\` line 4 must be blank, after the three header lines"
wf=$(newf expect-no-content); printf 'source: deconstruct\ntests: AC1\nexpect: a draft\n\n' > "$wf/inputs/E1-renewal-call.md"
expect "practice input: expect: but no input under the headers" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E1: \`inputs/E1-renewal-call.md\` holds no input under its headers"
wf=$(newf expect-line3); edit "$wf/inputs/E1-renewal-call.md" 's/^expect: [^\n]*\n\n/Notes:\n/m'
expect "practice input: line 3 neither expect: nor blank" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E1: \`inputs/E1-renewal-call.md\` line 3 must be blank, or the \`expect:\` header"
wf=$(newf expect-missing-save); edit "$wf/inputs/E2-no-next-step.md" 's/^expect: [^\n]*\n//m'
expect_ok "practice input: expect: is optional outside Deconstruct's pre-save run" "$wf"
expect "practice input: --before-save requires expect: on a Deconstruct input" "$wf" "^$R:[0-9]+ · ## Example Scenarios · E2: \`inputs/E2-no-next-step.md\` has no \`expect:\` line" --before-save
wf=$(newf expect-test-source); edit "$wf/inputs/E2-no-next-step.md" 's/^expect: [^\n]*\n//m; s/^source: deconstruct$/source: test/m'
expect_ok "practice input: --before-save leaves expect: optional on an input Test wrote" "$wf"

# 5. Writes: after each run with steps (the flag W line); nothing else after a moment
wf=$(newf write-after-other); edit "$wf/$R" 's/send a flag · after each run/send a flag · after the run/'
expect "Writes: after [moment] other than after each run, with steps" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety › ### Writes · W2: name the step that writes"
wf=$(newf write-after-case); edit "$wf/$R" 's/send a flag · after each run/send a flag · After each run/'
expect "Writes: after each run is that exact phrase" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety › ### Writes · W2 ends with"

# 6. Policy check: once, after Governing regime, before ### Writes, five values, its reference cross-checked
for v in 'Allowed' 'No — C2 left out' 'No — not live until approved' 'Not sure — to check' 'No — details removed first (R2)'; do
  wf=$(newf policy-ok); edit "$wf/$R" "s/^Policy check: No — details removed first \\(Step 1\\)\$/Policy check: $v/m"
  expect_ok "Policy check: \"$v\" passes" "$wf"
done
wf=$(newf policy-none); edit "$wf/$R" 's/^Policy check: [^\n]*\n//m'
expect_ok "Policy check: no line (the question wasn't asked)" "$wf"
wf=$(newf policy-value); edit "$wf/$R" 's/^Policy check: No — details removed first \(Step 1\)$/Policy check: Fine/m'
expect "Policy check: a value outside the five" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety · \`Policy check:\` reads"
wf=$(newf policy-form); edit "$wf/$R" 's/^Policy check: No — details removed first \(Step 1\)$/Policy check: No — details removed first (step 1)/m'
expect "Policy check: the step reference in another form" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety · \`Policy check:\` reads"
wf=$(newf policy-step); edit "$wf/$R" 's/\(Step 1\)$/(Step 9)/m'
expect "Policy check: names a step the path doesn't have" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety · \"Step 9\" matches no step line"
wf=$(newf policy-rule); edit "$wf/$R" 's/\(Step 1\)$/(R9)/m'
expect "Policy check: names a rule the file doesn't have" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety · \`Policy check:\` names R9, which isn't in Rules & Constraints"
wf=$(newf policy-before); edit "$wf/$R" 's/Governing regime: None\nPolicy check: ([^\n]*)\n/Policy check: $1\nGoverning regime: None\n/'
expect "Policy check: before Governing regime" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety · the \`Policy check:\` line comes after the \`Governing regime:\` line"
wf=$(newf policy-twice); edit "$wf/$R" 's/(Policy check: [^\n]*\n)/$1$1/'
expect "Policy check: twice" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety · a second \`Policy check:\` line"
wf=$(newf policy-after); edit "$wf/$R" 's/(Policy check: [^\n]*\n)\n### Writes\n/\n### Writes\n$1/'
expect "Policy check: after ### Writes" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety › ### Writes · the \`Policy check:\` line comes before \`### Writes\`"
wf=$(newf policy-token-ids); edit "$wf/$R" 's/lines: \[Policy check\]/lines: [Policy check, R2]/'
expect_ok "revisions: lines may hold the Policy check token alongside IDs" "$wf"
wf=$(newf policy-token-case); edit "$wf/$R" 's/lines: \[Policy check\]/lines: [policy check]/'
expect "revisions: the token is exactly \"Policy check\"" "$wf" "^$R:[0-9]+ · frontmatter · revisions entry 2 names \`policy check\`, which isn't a label"

# 7. Glosses: optional, fixed text, right under their four headings
wf=$(newf gloss-none); edit "$wf/$R" 's/^\*(The sources it uses|The practice runs|Its rules|The checkpoints)[^\n]*\*\n//mg'
expect_ok "glosses: optional (a file without them passes)" "$wf"
wf=$(newf gloss-reworded); edit "$wf/$R" 's/^\*The sources it uses, what we call its context\.\*$/*The sources it uses.*/m'
expect "glosses: reworded" "$wf" "^$R:[0-9]+ · ## Context Inventory · the line under \`## Context Inventory\` is its fixed gloss"
wf=$(newf gloss-moved); edit "$wf/$R" 's/^\*Its rules: what it always does, never does, and does when something happens\.\*\n//m; s/^(## Human Gates\n)\*The checkpoints[^\n]*\*\n/$1*Its rules: what it always does, never does, and does when something happens.*\n/m'
expect "glosses: one under the wrong heading" "$wf" "^$R:[0-9]+ · ## Human Gates · the line under \`## Human Gates\` is its fixed gloss"

# ---------------------------------------------------------------- 3c. the shape today's Deconstruct writes
# Every file the single interview saves has `Path: none` (no steps, no decisions): a checkpoint's Where is a
# moment, a write ends `· after [moment]`, a category whose every line the leader dropped stays as its heading and
# an empty table, and a law answer gives a rule and a checkpoint that name the law ("…, as [the law] requires.").
# Base: the committed fixture framework-fixtures/path-none/client-follow-up (also the Design, Build and Test
# evals' base). Its planted misses are the step references a `Path: none` file can't hold.
echo "Today's Deconstruct shape (Path: none: moments, after [moment], an emptied category, law-named lines)"
PN_SRC="$FIXTURES/path-none/client-follow-up"
pnf() {  # <case name>: a fresh copy of the Path: none workflow folder; echoes it
  local d="$TMP/pn-$1"
  rm -rf "$d"; mkdir -p "$d"; cp -R "$PN_SRC/." "$d/"
  echo "$d"
}
R=requirements.md
wf=$(pnf ok); expect_ok "the Path: none base passes" "$wf"
expect_ok "...and passes Deconstruct's pre-save run" "$wf"

wf=$(pnf gate-moment); edit "$wf/$R" 's/(\| G1 \| After the draft is ready \| [^\n]*\n)/$1| G2 | Before the email goes to the client | When you have edited the draft, it waits for you to confirm the recipient before it goes to the client. · (you) |\n/'
expect_ok "Human Gates: a G line whose Where is a moment, under Path: none" "$wf"

wf=$(pnf write-moment); edit "$wf/$R" 's/(- W1 · Gmail · create a draft · after the email is drafted\n)/$1- W2 · Slack #client-updates · post a one-line note · after you approve the draft\n/'
expect_ok "Writes: a W line ending \`· after [moment]\`, under Path: none" "$wf"

wf=$(pnf emptied-category); edit "$wf/$R" 's/(### Traceability\n\| ID \| Constraint \| Source \|\n\|---\|---\|---\|\n)\| P1 [^\n]*\n/$1/'
expect_ok "Security: a worked category whose every line was dropped is its heading and an empty table" "$wf"

wf=$(pnf law-lines)
edit "$wf/$R" 's/^track: light$/track: full/m;
  s/(\| R4 \| When \| [^\n]*\n)/$1| R5 | Always | It always ends each draft with the firm\x27s disclosure line, as FINRA Rule 2210 requires. |\n/;
  s/(\| G1 \| After the draft is ready \| [^\n]*\n)/$1| G2 | After you approve the draft | When you approve the draft, it waits for a registered principal to approve it before it goes to the client, as FINRA Rule 2210 requires. · (registered principal) |\n/;
  s/^Governing regime: None$/Governing regime: FINRA Rule 2210 (communications with the public)/m'
expect_ok "a law-named rule and a law-named checkpoint (\`…, as [the law] requires.\`), with the regime named" "$wf"

wf=$(pnf gate-step); edit "$wf/$R" 's/\| G1 \| After the draft is ready \|/| G1 | Step 3 |/'
expect "Human Gates: \`Where: Step 3\` under Path: none" "$wf" "^$R:[0-9]+ · ## Human Gates · \"Step 3\" matches no step line in ## Path"

wf=$(pnf write-step); edit "$wf/$R" 's/ · after the email is drafted$/ · Step 2/m'
expect "Writes: a W line naming \`Step 2\` under Path: none" "$wf" "^$R:[0-9]+ · ## Security, Privacy & Safety › ### Writes · \"Step 2\" matches no step line in ## Path"

wf=$(pnf usedby-step); edit "$wf/$R" 's/\| C1 \| Follow-up style guide \| All \|/| C1 | Follow-up style guide | Step 2 |/'
expect "Context Inventory: \`Used By: Step 2\` under Path: none" "$wf" "^$R:[0-9]+ · ## Context Inventory · \"Step 2\" matches no step line in ## Path"

# ---------------------------------------------------------------- 3d. the 11.0 format (shape release)
echo "The 11.0 format: an Output section and traced checks"
p11() {  # <case>: a copy of the 11.0 fixture; echoes the workflow folder
  local d="$TMP/f11-$1"; mkdir -p "$d"; cp -R "$FIXTURES/format-11/client-follow-up" "$d/"; echo "$d/client-follow-up"
}
wf=$(p11 ok)
expect_ok "11.0: twelve sections, six Output lines, traced checks, a scenario Test writes" "$wf"
expect_ok "11.0: the same file before saving" "$wf" --before-save
wf=$(p11 test-input); cp "$wf/inputs/E1-acme-renewal-call.md" "$wf/inputs/E3-test.md"
edit "$wf/inputs/E3-test.md" 's/^expect: [^\n]*\n//m; s/^source: [^\n]*$/source: test/m'
edit "$wf/$R" 's/(\| E2 \| [^\n]*\n)/$1| E3 | Test-written (made up) | `inputs\/E3-test.md` — notes Test wrote | It drafts the email | — |\n/'
expect_ok "11.0: --before-save leaves expect: optional on an input Test wrote" "$wf" --before-save
wf=$(p11 no-output); edit "$wf/$R" 's/## Output\n.*?Delivered as: set in Design\n\n//s'
expect "11.0: no Output section before saving" "$wf" "section \"## Output\" is missing" --before-save
wf=$(p11 no-from); edit "$wf/$R" 's/ · from: I1, R1$//m'
expect "11.0: a check with no source" "$wf" 'AC2: add "· from:"'
wf=$(p11 unknown-id); edit "$wf/$R" 's/ · from: C1$/ · from: I7/m'
expect "11.0: a check naming a source that doesn't exist" "$wf" "AC3: from names I7, which isn't in Inputs"
wf=$(p11 no-voice); edit "$wf/$R" 's/^Voice: [^\n]*\n//m'
expect "11.0: an Output line missing" "$wf" "Output: Voice: is missing"
wf=$(p11 must); edit "$wf/$R" 's/\*\*AC1\*\*/**AC1 (must)**/'
expect "11.0: no (must) in an 11.0 file" "$wf" "AC1: no \(must\) in this format"
wf=$(p11 regulated-none); edit "$wf/$R" 's/\| Internal \| Authored \|/| Regulated | Authored |/'
expect "11.0: a Regulated source with Governing regime None" "$wf" "Regulated"

# ---------------------------------------------------------------- 4. usage and the plugin copy
echo "Usage and the plugin copy"
out=$(node "$CHECK" "$TMP/does-not-exist" 2>&1); [ $? -eq 2 ] && ok "unreadable file exits 2" || bad "unreadable file should exit 2"
wf=$(plant folder-arg); (node "$CHECK" "$wf" >/dev/null 2>&1) && ok "accepts the workflow folder in place of the file" || bad "should accept a workflow folder"
if [ -f "$PLUGIN_COPY" ] && cmp -s "$CHECK" "$PLUGIN_COPY"; then ok "plugin copy is byte-for-byte the canonical one"
else bad "plugins/handsonai/tools/requirements-check.js differs from registry-template/tools/requirements-check.js"; fi

echo
echo "requirements-check tests: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
