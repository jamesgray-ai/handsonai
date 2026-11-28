#!/usr/bin/env python3
"""Scripted checks: the expectations a program can decide, so no model judges them.

Each `scripted` expectation in an evals.json carries a `check` object. Check types:

  ai_contains      {text, session?, turn?: first|any|all|last, line?}  an AI message contains the text
                                                                  (`line`: the approved line it quotes)
  ai_not_contains  {text, session?, outside_fences?}               no AI message contains it (outside_fences: a
                                                                  list of openers; a fenced block whose first line
                                                                  starts with one is skipped, as Build's brief)
  ai_regex         {pattern, session?, turn?}                     an AI message matches
  ai_not_regex     {pattern, session?}                            no AI message matches
  quote            {id, form?, session?, turn?, ending?}          an AI message says that approved line
                                                                  (approved-lines.json), placeholders filled;
                                                                  `ending`: a fragment form of the same line
                                                                  ("…, keeping…"): the line said with it in
                                                                  place of its closing mark
  quote_absent     {id, form?, session?}                          no AI message says it
  opens_with       {ids: [...], lead_in?: bool, session?}         the session's first AI message opens with one of
                                                                  these approved lines (its first paragraph); with
                                                                  lead_in, it may open with the routing lead-in
                                                                  (N-F23, its [state] one of the line's phrases) as
                                                                  its whole first paragraph, then one of them
  said_before      {id, anchor, opens?, session?}                 the AI message where `anchor` (a regex, multiline)
                                                                  first matches holds, before it, exactly that
                                                                  approved line and nothing else, and no other AI
                                                                  message of the session says it (N-A30, the saving
                                                                  line, before the close); with opens, the line is
                                                                  that message's first paragraph and other text may
                                                                  follow it before the anchor (N-D24, then the notes)
  inputs_shown     {id, anchor, path?, allow_none?, session?}     the proposed practice inputs were shown before
                                                                  saving (N-D25, approved 2026-11-14): `path` (default
                                                                  framework/*/requirements.md) has Example Scenarios
                                                                  rows marked "(proposed"; exactly one AI message says
                                                                  the approved line `id`, before the first AI message
                                                                  `anchor` matches (the preview); a line said in two
                                                                  parts (N-D25: a placeholder between its sentences)
                                                                  has its last part end that message, and the
                                                                  inputs are looked for between its parts; each proposed
                                                                  row's saved input (its body: header lines and any
                                                                  `Earlier run:` paragraph left out) has its first line
                                                                  in that message, or in a later message before the
                                                                  anchor's (the leader's correction). No proposed row
                                                                  fails, unless allow_none (then the line is never said)
  scripted_lines   {session?}                                     every scripted line said is word for word
                                                                  (the quote check; built in)
  vocabulary       {session?}                                     no word from rules 2.2's Never column in
                                                                  what the leader reads (built in)
  no_time_or_step_numbers {session?}                              no time estimate and no framework step
                                                                  number (rules 2.1 items 4-5; built in); a size
                                                                  the leader gave for their own work ("about
                                                                  20 minutes per follow-up") may be played back,
                                                                  and so may the leader's own schedule as a
                                                                  brought requirements.md's `Starts` row records
                                                                  it ("checked every 30 minutes"; Deconstruct 3.3,
                                                                  R-D3's time-word exception)
  signposts        {skill, of?, optional?, session?}              the skill's "Part k of N" signposts, in
                                                                  order: design 4, test 4, build 3; `of` for a
                                                                  later entry. Deconstruct has none (one interview
                                                                  for every workflow, 2026-11-15): there the check
                                                                  fails closed
  max_words        {max, turn: "first", session?}                 each session's first AI message is at most
                   {max, containing: <line ID>, form?, session?}  `max` words; or every AI message that says
                                                                  that approved line is (none said: fails).
                                                                  Words as word_count counts them (Deconstruct
                                                                  T1: 200 on the first turn; T2: the message
                                                                  that says how the interview will go, 170)
  file_exists      {path, session?}                               a file matching the glob exists at session end
  file_absent      {path, session?}                               no file matches at session end (a fixture's
                                                                  own file counts: for "nothing written",
                                                                  use no_added_files)
  file_existed_during {path, session?}                            a match existed after some turn of the session
  file_contains    {path, text, session?}                         a matching file contains the text
  file_not_contains {path, text, session?}
  file_regex       {path, pattern, session?}                      a matching file matches (multiline)
  file_not_regex   {path, pattern, session?}
  sections_in_order {path, headings: [...], only?: bool, session?} the `#`/`##` headings appear in this
                                                                  order (only: no other `##` headings)
  yaml_keys        {path, keys: [...], exact?: true, absent?: [...], session?}
                                                                  the file opens with frontmatter holding these
                                                                  keys (exact: these and no others, in order)
  structure        {path, kind: plan|build_record|results|requirements, registry?: bool, session?}
                                                                  structure.py's checks on the file
  fill_check       {kind: build|fix, session?, expect?: {task, folder, context_files, connections},
                    plan?: glob, carried?: [...], require_carried?: [ids]}
                                                                  Build's Agent Builder prompt (N-B52, N-B53):
                                                                  every filled field against the plan
  tool_write       {path, pattern, before?, session?}             a Write, Edit or MultiEdit call in the session's
                                                                  events.jsonl put text matching the pattern into a
                                                                  matching file (Write's content, Edit's new_string);
                                                                  `before` (a regex): that write comes before the first
                                                                  write by any tool (a Bash command naming the file
                                                                  too) whose new text matches it, and one follows
                                                                  (plan reset to approved: false before re-approval)
  saved_before_next_question {path, pattern, answer, session?}  the leader's first message matching `answer` is
                                                                  written (a Write or Edit to `path` matching
                                                                  `pattern`) no later than the first AI turn after it
                                                                  that asks something; turns split by each call's
                                                                  result event; fails closed (Pass 4 review M5)
  no_tool_call     {tool, input_pattern?, input_not_pattern?,     no tool call in the session's events.jsonl whose
                    after?, session?}                             name matches `tool` (and whose JSON input matches
                                                                  input_pattern, and not input_not_pattern); with
                                                                  `after`, only calls after the first AI text matching
                                                                  it. No events.jsonl fails closed
  read_before_save {session?}                                     on Claude and ChatGPT (build-smoke-1): every AI text
                                                                  that offers the save (a save card, the skills-list
                                                                  ask, an upload or download of a .skill or .zip)
                                                                  comes after a read of the last package the skill
                                                                  creator's `package_skill` made (unzip, zipinfo,
                                                                  python… naming the .skill file), in the same turn;
                                                                  no offer passes. No events.jsonl fails closed
  one_question     {containing, not_pattern?, session?}           every AI message matching containing asks at most one
                                                                  question, in its last paragraph; none matches
                                                                  not_pattern; none matched fails closed (Pass 5)
  phrases_in_blocks {containing?, phrases?, session?}             in those messages a start phrase is never inline: only
                                                                  in a code block (Pass 5, E32, X3)
  asked_before_save {pattern, anchor?, session?}                  an AI message matching pattern comes before the first
                                                                  save offer, or `anchor` (Build's keep-or-drop question,
                                                                  Pass 5 E16)
  handover_one_message {session?}                                 every practice-run hand-over is one message: setup,
                                                                  then the box last, nothing after it; no "say 'ready'"
  deny_in_every_handover {session?}                               N-F4 (any form) before every practice-run box, in its
                                                                  message, whatever the workflow's connections (Pass 5)
  no_false_first_line_claim {session?}                            once the leader pastes a run reply whose practice-run
                                                                  line isn't its opening words (a short line came first,
                                                                  or the output did), no later AI message says the reply
                                                                  starts, begins or opens with it (Pass 5, E22)
  file_unchanged   {path, session?}                               every matching file is byte-identical
                                                                  at session start and end
  file_line        {path, line: n, pattern, session?}             line n (1-based) matches the pattern
  section_regex    {path, section, pattern, must?: bool}          inside one section, the pattern matches
                                                                  (must=true, default) or doesn't
  no_added_files   {except?: [globs], session?}                   no file was added during the session: the
                                                                  end tree against the session's start tree
                                                                  (the fixture's own files)
  release_check    {ids: [n, ...], passed: {check}, open: {check}} the maintainers' release checks (release/release-checks.md):
                                                                  `passed` when every row is verified for this
                                                                  release, `open` otherwise (fail closed).
                                                                  A judged expectation or a precondition can
                                                                  depend on them too: `release_check: {ids,
                                                                  passed: text|null, open: text|null}`
                                                                  (resolve_release_items)
  all              {checks: [...]}                                every sub-check passes
  any              {checks: [...]}                                at least one passes

Retired: `no_yaml` (every framework file now has frontmatter; use `yaml_keys`).

Path globs use fnmatch, where `*` also matches `/`: `framework/*/test-results.md` matches a file
under `framework/x/history/...` too.

`session` is 1-based; leave it out to mean every session (AI checks) or the last session (file checks).
Text matching ignores differences in curly versus straight quotes and dashes (in regex patterns too);
ai_contains and ai_not_contains also treat single and double quote marks alike.

Built-in checks the runner adds to every run (an evals file's `builtin_checks`, or an eval's
`skip_builtin`, can narrow them): the quote check (`scripted_lines`), `vocabulary` and
`no_time_or_step_numbers` on every AI message; and, for runs with a simulated leader, the fidelity
check (no listed framework term in a leader turn before an AI turn used it) and the turn cap.
Every Build run also gets two built-in checks no evals file or `skip_builtin` turns off (SKILL_BUILTINS,
review findings 19 and 21): `no_team_visible_writes` (no stand-in connection call wrote anywhere other
people see: a Slack channel other than the private #build-check or a message to the leader, any HubSpot
change, an overwrite of a spreadsheet the run didn't make, an email to anyone but the leader; read from the
stand-in's own log and from events.jsonl; no record of either fails) and `quoted_output_seen` (every block
quote an AI message shows appears in a tool result of that session, or in what the leader pasted).
An evals file's `core_builtin_checks` adds built-in checks to its core evals only (Analyze: `narration`,
an AI paragraph that is a note to itself, or a bare `.md` file name outside code formatting; a paragraph that is
exactly the saving line, N-A30, the routing lead-in, N-F23, in its approved form, or N-F24 (the one sentence allowed
before N-F22), is not narration, and one that says any of them another way is; a line ID such as N-F15 in
anything the leader reads, outside code formatting, is narration too).
"""
import fnmatch
import hashlib
import json
import re
from pathlib import Path

import approved_lines as AL
import structure as ST

FIDELITY_TERMS = ["acceptance criterion", "acceptance criteria", "AC", "fixed step", "flexible step",
                  "human gate", "context", "Context Inventory", "Design Plan", "autonomy",
                  "Deterministic", "Guided", "Autonomous", "requirements", "Golden Example"]

# rules 2.2's Never column. Case-insensitive unless the pattern says otherwise.
NEVER = [
    ("spec", r"(?i)\bspecs?\b"), ("PRD", r"\bPRDs?\b"), ("Design Spec", r"(?i)\bdesign spec\b"),
    ("reconciliation table", r"(?i)\breconciliation tables?\b"),
    ("acceptance criteria", r"(?i)\bacceptance criteri(?:a|on)\b"), ("(must)", r"(?i)\(must\)"),
    ("must-always lines", r"(?i)\bmust-(?:always|never)\b"), ("M lines", r"\bM\d*\s+lines?\b|\bM\d+\b"),
    ("human gate", r"(?i)\bhuman gates?\b"),
    ("test mode", r"(?i)\btest mode\b"), ("test case", r"(?i)\btest cases?\b"),
    ("scenario", r"(?i)\bscenarios?\b"), ("edge case", r"(?i)\bedge cases?\b"),
    ("awkward", r"(?i)\bawkward\b"), ("hard case", r"(?i)\bhard cases?\b"),
    ("connector", r"\bconnectors?\b"),  # Claude's own label, "Connectors" or quoted, is allowed
    ("scope", r"(?i)\b(?:oauth|api|access|permission|read|write)[ -]scopes?\b|\bscopes\b"),
    ("irreversible action", r"(?i)\birreversible\b"),
    ("live check", r"(?i)\blive checks?\b"), ("smoke test", r"(?i)\bsmoke tests?\b"),
    ("regression test", r"(?i)\bregression tests?\b"), ("review date", r"(?i)\breview dates?\b"),
    ("autonomy", r"(?i)\bautonomy\b"), ("Augmented", r"\bAugmented\b"), ("Automated", r"\bAutomated\b"),
    ("mechanism", r"(?i)\bmechanisms?\b"),
    ("eval", r"(?i)\bevals?\b"), ("score", r"(?i)\bscor(?:e|es|ed|ing)\b"), ("coverage", r"(?i)\bcoverage\b"),
    ("consistency", r"(?i)\bconsistency\b"), ("dimension", r"(?i)\bdimensions?\b"),
    ("trajectory", r"(?i)\btrajector(?:y|ies)\b"), ("pass rate", r"(?i)\bpass rates?\b"),
]
NEVER = [(n, re.compile(p)) for n, p in NEVER]

TIME = re.compile(r"(?i)\b\d+(?:\.\d+)?\s*(?:-|to)?\s*\d*\s*(?:minutes?|mins?|hours?|hrs?|seconds?|secs?)\b"
                  r"|\b(?:a few|several|a couple of|ten|fifteen|twenty|thirty|forty|forty-five|five|two|three)"
                  r"\s+(?:minutes?|seconds?)\b|\bhalf an hour\b|\b(?:an|one) hour\b|\btakes? (?:about|around|roughly|under|less than)\b")
STEP_NAMES = r"(?:Analyze|Deconstruct|Design|Build|Test)"
STEP_NUMBER = re.compile(
    rf"\b[Ss]tep\s+[1-5]\b\s*(?:\(\s*{STEP_NAMES}|of\s+(?:the\s+)?(?:AI\s+Workflow\s+)?[Ff]ramework|of\s+5\b|[-:]\s*{STEP_NAMES}\b)"
    rf"|\b{STEP_NAMES}\s*\(\s*[Ss]tep\s*[1-5]\s*\)"
    rf"|\b[Ss]tep\s+[1-5]\s+(?:is|was|will be)\s+{STEP_NAMES}\b"
    rf"|\b{STEP_NAMES}\s+is\s+(?:[Ss]tep\s+[1-5]|the\s+(?:first|second|third|fourth|fifth)\s+step)\b"
    rf"|\b(?:first|second|third|fourth|fifth)\s+step\s+of\s+the\s+(?:AI\s+Workflow\s+)?[Ff]ramework\b")

# One interview for every workflow (2026-11-15): Deconstruct has no parts and so no signposts
# Build announces no parts either (2026-11-22, James, after final-build-2): its opening says what comes
SIGNPOST_IDS = {"design": (4, ["N-0"]), "test": (4, ["N-T1"])}
# Deconstruct gives one figure, once: the range in the line that says how the interview will go. Since the
# shape release (11.0) that line is model wording, so the measurement finds it by pattern ("about 10 to 15
# replies"); "About [M] questions left." is never said, and leader.replies_by_part reports a stray count by
# pattern too, so it shows up in the measurement. Measurement only: nothing is graded on these.
COUNT_CARRIER_RE = r"(?i)\babout \d+ to \d+ replies\b"
COUNT_LINE_RE = r"(?i)\babout \d+ (?:more )?questions? (?:left|to go|remaining)\b"
BUILTIN =("scripted_lines", "vocabulary", "no_time_or_step_numbers")
BUILTIN_TEXT = {"scripted_lines": "Every scripted line the AI says is the approved line, word for word (the quote check; "
                                  "a line that doesn't protect the leader may have a word or two changed)",
                "vocabulary": "No word from the vocabulary's Never column in anything the leader reads",
                "no_time_or_step_numbers": "No time estimate and no framework step number in anything the leader reads",
                "narration": "No narration: no AI paragraph that is a note to itself ('Now the…', 'Read …', 'Ask N-…', "
                             "'Let me…', 'I need…'), no bare .md file name outside code formatting, and no line ID (N-…)"}
# core round-1 fixes (2026-11-12): a paragraph that opens like a note to itself, or names a Markdown file
# outside backticks, is the AI narrating its own work to the leader
# core batch 2 (2026-11-14): "Let me suggest one, then: …" offers the leader a suggestion; it is not a note to itself
# round 4 (2026-11-16): "Read and edit, then send it yourself: that's your checkpoint." plays the leader's
# own checkpoint back; "Read " is a note only when a file, a reference or the notes follow it
NARRATION = re.compile(r"^(Now (the|I'll|writing|update)|Read (?=(the |its |both |all |each |these |those |every |progress|routing|references?\b|files?\b|`|[\w/-]+\.md))"
                       r"|Ask N-|Let me (?!suggest\b)|I need )")
# a file named on its own; a path with folders (the close's report path, a fill) is left out
BARE_MD = re.compile(r"(?<![\w/.-])[\w.-]*\w\.md\b(?![\w/])")
# core round-2 fixes (2026-11-12): two moments get approved words instead of silence. The saving line (N-A30)
# and the routing lead-in (N-F23) said exactly are not narration; a paragraph that says either another way is
SAVING_ID, LEAD_IN_ID = "N-A30", "N-F23"
# Deconstruct's saving line (approved by James, 2026-11-14): "Saving your Workflow Requirements now; this takes a moment.", the one exception to its narration rule
SAVING_IDS = (SAVING_ID, "N-D24")
# core round-3 fixes (2026-11-12): N-F24, "Your registry has no workflows yet, so the next step is Analyze.", the one
# sentence allowed before N-F22; and "Still saving: …" is the saving line reworded too
BEFORE_F22_ID = "N-F24"
# smoke-1 fix (2026-11-14): "Saving" as the subject of a sentence about the work ("Saving drafts in Outlook also
# needs a connection") isn't the AI saying it is saving; a verb of that kind later in the clause marks it
SAVING_LIKE = re.compile(r"(?i)^(?:now |still )?saving\b(?!\s+[^.!?:;…\n]{0,80}?\b(?:needs?|requires?|also|"
                         r"works?|means|isn't|doesn't|can't|won't|only)\b)")
# core batch 2 (2026-11-14): a "Saving…" paragraph is the AI saying it is saving when it is short, or names its
# own act, itself or the framework's files; otherwise it plays back what the workflow does ("Saving it as a
# draft in your Outlook Drafts folder, and you send it yourself."), which is not narration
SAVING_SELF = re.compile(r"(?i)\b(?:now|still|moment|silently|requirements|progress|inputs?|files?|reports?|"
                         r"workflows?|I|I'm|I'll|we|we'll)\b|…|\.\.\.")


def is_saving_playback(para):
    return len(para.split()) > 6 and not SAVING_SELF.search(para)


LEAD_IN_LIKE = re.compile(r"(?i)^[^\n]{0,200}, so the next step is\b[^\n]{0,60}$")
# core round-4 fixes (2026-11-13): a line ID said to the leader ("It's a general folder, so N-F15.") is the AI
# naming its own rule; flagged wherever it stands, outside code formatting
LINE_ID = re.compile(r"\bN-[A-Z]{1,2}\d+[a-z]?\b")
LEAD_IN_SHAPE = re.compile(r"(.+?), so the next step is (Analyze|Deconstruct|Design|Build|Test)\.")


def norm(s):
    return (s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
             .replace("—", "-").replace("–", "-").replace(" ", " "))


def qnorm(s):
    """norm, plus single and double quote marks treated alike, and Markdown's code and bold marks
    dropped (the leader reads `framework` as framework), for word-for-word text checks."""
    return norm(s).replace('"', "'").replace("`", "").replace("**", "")


def corpus():
    return AL.load()


def _listed(run):
    """The sessions the eval lists, in order: a restart the harness inserted after a Build session inside
    another skill's journey isn't one of them, so a check's "session": n keeps meaning the eval's nth."""
    return [s for s in run["sessions"] if not s.get("inserted")]


def _sessions(run, n):
    return [_listed(run)[n - 1]] if n else run["sessions"]


def _strip_fences(text, openers):
    """The text without each fenced block whose first line inside the fence starts with one of `openers`
    (Build's `Skill brief:` block quotes lines the AI must never say outside it; Pass 4)."""
    out, i = [], 0
    for m in re.finditer(r"(?ms)^[ \t]*(`{3,}|~{3,})[^\n]*\n(.*?)^[ \t]*\1[ \t]*$", text):
        if m.group(2).lstrip().startswith(openers):
            out.append(text[i:m.start()])
            i = m.end()
    out.append(text[i:])
    return "".join(out)


def _ai_turns(sess, which="any"):
    ai = [t["text"] for t in sess["turns"] if t["role"] == "ai"]
    if which == "first":
        return ai[:1]
    if which == "last":
        return ai[-1:]
    return ai


def _files(sess, pattern, when="end"):
    snap = sess["files_end"] if when == "end" else sess["files_start"]
    return {p: v for p, v in snap.items() if fnmatch.fnmatch(p, pattern)}


def files_all(sess):
    return sorted(sess["files_end"])


def _file_session(run, n):
    return _listed(run)[n - 1] if n else run["sessions"][-1]


def leader_text(message):
    """What the leader reads, for the wording checks: code blocks and inline code left out
    (file names, prompts to paste), since those are technical text, not wording; block-quoted
    lines too, since those show the leader's work back (an input drafted or pasted), not the AI's wording."""
    m = re.sub(r"```.*?```", " ", message, flags=re.S)
    m = re.sub(r"(?m)^[ \t]*>.*$", " ", m)
    return re.sub(r"`[^`\n]*`", " ", m)


# ---------------------------------------------------------------- wording checks

def leader_never_words(run):
    """The Never-column names the leader used in their own messages: the framework never calls its own things
    by them, but a leader's own word for their own thing ("the cheapest that meets the spec") may be played back."""
    said = " ".join(t["text"] for s in run["sessions"] for t in s["turns"] if t["role"] != "ai")
    return frozenset(name for name, rx in NEVER if rx.search(said))


# a link's text is an address, not wording: a help-page slug ("…/10166901-use-google-workspace-connectors")
# names the platform's page, not the framework's thing (build-full-1 fix, 2026-11-21)
URL = re.compile(r"(?:https?://|\b[\w-]+(?:\.[\w-]+)+/)\S*")


def vocabulary_hits(message, allowed=frozenset()):
    text = URL.sub(" ", corpus().strip_approved(leader_text(message)))
    hits = []
    for name, rx in NEVER:
        if name in allowed:
            continue
        for m in rx.finditer(text):
            if name == "connector":
                before, after = text[max(0, m.start() - 1):m.start()], text[m.end():m.end() + 1]
                if before in ("'", '"') or after in ("'", '"'):
                    continue  # the platform's own label, quoted
            hits.append((name, text[max(0, m.start() - 40):m.end() + 40].strip()))
    return hits


NUM_WORDS = {"a": "1", "an": "1", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
             "seven": "7", "eight": "8", "nine": "9", "ten": "10", "fifteen": "15", "twenty": "20",
             "thirty": "30", "forty": "40", "forty-five": "45", "fifty": "50", "sixty": "60", "ninety": "90"}
SIZE = re.compile(r"(?i)\b(\d+(?:\.\d+)?|" + "|".join(sorted(NUM_WORDS, key=len, reverse=True)) + r")"
                  r"(?:\s*(?:-|to)\s*(\d+(?:\.\d+)?))?\s*-?\s*(?:working\s+|business\s+)?(minute|min|hour|hr|second|sec|day|week)s?\b")


def sizes(text):
    """Number-and-unit pairs in text ("20 minutes", "two hours" -> ("2", "hour")), ranges as both ends."""
    out = set()
    for m in SIZE.finditer(norm(text)):
        unit = {"min": "minute", "hr": "hour", "sec": "second"}.get(m.group(3).lower(), m.group(3).lower())
        for g in (m.group(1), m.group(2)):
            if g:
                out.add((NUM_WORDS.get(g.lower(), g), unit))
    return out


def leader_sizes(run):
    """What the leader said about their own work's size, in any session; what a requirements file
    the leader brought holds in its Value & Measurement (the Baseline and Target, from the leader's
    earlier Deconstruct chat); or what Analyze's progress file the leader brought noted from an
    earlier chat (a resume says "I noted [pieces]"): playing it back is allowed (the framework never
    estimates time, but those are the leader's numbers). A file the AI wrote in this run (its own
    Baseline, or a later session's start tree) never counts: a size it wrote down from the leader is
    in the leader's own message, and one the leader never gave is the AI's estimate."""
    said = [sizes(t["text"]) for s in run["sessions"] for t in s["turns"] if t["role"] != "ai"]
    brought = leader_files(run)
    written = [sizes(ST.section(body, "Value & Measurement")) for p, body in brought if p.endswith("requirements.md")]
    # Deconstruct 3.3 (R-D3, B-M3): the leader's own schedule, as a brought requirements.md's Metadata
    # `Starts` row records it ("event: … · checked every 30 minutes"), may be played back (Design quotes it)
    schedule = [sizes(starts_row(body)) for p, body in brought if p.endswith("requirements.md")]
    # core batch 2 (2026-11-14): a Deconstruct progress file the leader brought holds what they said in an
    # earlier chat too (Part 5's target question plays Part 1's aim back from it)
    noted = [sizes(body) for p, body in brought if p.endswith(("analyze-in-progress.md", "deconstruct-in-progress.md"))]
    return set().union(*said, *written, *schedule, *noted)


def starts_row(body):
    """The value of a requirements file's Metadata `Starts` row ("" when it has none)."""
    for t in ST.tables(ST.section(body, "Metadata")):
        for row in t:
            if len(row) >= 2 and row[0].strip("* ") == "Starts":
                return row[1]
    return ""


def word_count(message):
    """Words in a message as the leader reads it: Markdown's bold, italic and code marks dropped, then every
    whitespace-separated token holding a letter or digit (a list's "-" or a lone dash isn't a word; "1." is).
    The count T1 and T2 are measured with (framework-evals/tools/wc_deconstruct.py uses it too)."""
    text = norm(message).replace("**", " ").replace("`", " ")
    return sum(1 for tok in text.split() if re.search(r"[A-Za-z0-9]", tok))


def _max_words(c, run):
    """max_words: each session's first AI message (turn: first), or every AI message saying the line
    `containing` (form optional), is at most `max` words. Nothing to count fails (fail closed)."""
    cap = c["max"]
    counted = []
    for s in _sessions(run, c.get("session")):
        if c.get("containing"):
            forms = [f for f in corpus().get(c["containing"], c.get("form")) if f.text]
            msgs = [(i, m) for i, m in enumerate(_ai_turns(s), 1) if any(f.matches(m) for f in forms)]
        else:
            msgs = [(1, m) for m in _ai_turns(s, "first")]
        counted += [(s["n"], i, word_count(m)) for i, m in msgs]
    if not counted:
        what = f"no AI message says {c['containing']}" if c.get("containing") else "no AI message"
        return False, what
    over = [x for x in counted if x[2] > cap]
    where = ", ".join(f"session {n} AI message {i}: {w} words" for n, i, w in (over or counted)[:4])
    return (not over, (f"over {cap}: " if over else f"at most {cap}: ") + where)


def leader_files(run):
    """The files the leader brought, as (path, text): the start tree of each session that began
    from its fixture (the harness marks it `fixture`), never a start tree carried over from an
    earlier session, which holds what the AI wrote there. A run without the marks (one saved
    before them) counts its first session only (fail closed)."""
    sess = run["sessions"]
    marked = any("fixture" in s for s in sess)
    out = []
    for i, s in enumerate(sess):
        if (s.get("fixture") if marked else i == 0):
            out += [(p, b) for p, b in (s.get("files_start") or {}).items() if isinstance(b, str)]
    return out


def _leaders_own(found, allowed, present=()):
    """Every size found is one the leader gave, or sits one unit either side of one: a practice run
    built on the leader's own limit ("exactly 48 hours, and one has 49") is their data, not an estimate."""
    def near(size):
        if size in allowed:
            return True
        try:
            # ±1 only beside the leader's own exact size in the same message (review H3, 2026-11-21)
            return any(u == size[1] and abs(float(n) - float(size[0])) <= 1 and (n, u) in present
                       for n, u in allowed)
        except ValueError:
            return False
    return all(near(x) for x in found)


# James, 2026-11-14 (kept 2026-11-21; narrowed per review B1-17): a time the AI suggests inside a
# check is a suggested check the leader keeps or drops, not a time estimate. Only a check counts: a
# list item ("-", "*" or "N." first, after optional spaces or quote markers) tagged "(my suggestion)".
# A time in ordinary prose stays an estimate, tag or no tag.
_ITEM = r"(?:[-*]|\d+\.)[ \t]+"
# with its line breaks: the item line up to its tag (a tag covers the words before it, so prose after
# the tag on the same line is checked as prose)
SUGGESTED_CHECK_LINE = re.compile(r"(?mi)^[ \t>]*" + _ITEM + r"[^\n]*?\(my suggestion\)")
# with its line breaks joined: from a list marker that opens the text or follows the end of the item or
# sentence before it, up to the tag, through no other marker and no new sentence (". " then a capital)
SUGGESTED_CHECK_JOINED = re.compile(
    r"(?i:(?:^|(?<=[.!?:)*_]\s))" + _ITEM + r")(?:(?!\s(?:[-*]|\d+\.)\s)(?![.!?]\s+[A-Z])[^\n])*?"
    r"(?i:\(my suggestion\))")


def _drop_suggested_checks(text):
    return SUGGESTED_CHECK_JOINED.sub(" ", SUGGESTED_CHECK_LINE.sub(" ", text))


def time_or_step_hits(message, allowed=frozenset()):
    # what fills an approved line's placeholder ("about [hours] saved") is part of that line here;
    # a size the leader gave for their own work ("about 20 minutes per follow-up") is theirs, not an estimate
    shown = leader_text(message)
    text = corpus().strip_approved(shown, keep_fills=False)
    # strip_approved joins the line breaks, so the suggested checks are found in the text before it,
    # with its lines (and found again in a message whose lines arrived already joined)
    kept = _drop_suggested_checks(shown)
    timed = text if kept == shown else corpus().strip_approved(kept, keep_fills=False)
    hits = [("time", timed[max(0, m.start() - 40):m.end() + 40].strip()) for m in TIME.finditer(timed)
            if not (sizes(timed[m.start():m.end() + 25])
                    and _leaders_own(sizes(timed[m.start():m.end() + 25]), allowed, set(sizes(timed))))]
    hits += [("step number", text[max(0, m.start() - 40):m.end() + 40].strip()) for m in STEP_NUMBER.finditer(text)]
    return hits


def quote_hits(message, skill=None):
    """Near misses of approved lines; with `skill`, only that skill's lines (and the built
    workflow's) count, so a common phrase another step's line happens to share isn't flagged.
    Block-quoted lines are left out: they show the leader's work or paste back as it was (an agent's
    reworded line, block-quoted to show it), not the AI's wording. Code blocks stay in: a prompt to
    paste carries approved lines word for word."""
    message = re.sub(r"(?m)^[ \t]*>.*$", " ", message)
    return [(ln.label(), exp, got) for ln, exp, got in corpus().near_misses(message, skill=skill)]


def is_saving_line(para):
    """The paragraph is exactly a saving line (Analyze's N-A30, Deconstruct's N-D24), in an approved form."""
    p = AL.norm(para)
    return any(ln.regex.fullmatch(p) for i in SAVING_IDS for ln in corpus().get(i) if ln.text)


def is_lead_in(para):
    """The paragraph is exactly the routing lead-in (N-F23) in its approved form: "[Workflow] [state], so the
    next step is [step].", [state] one of the line's own phrases, [step] a step's name, and [Workflow] a name
    (no sentence of its own)."""
    p = AL.norm(para)
    for ln in corpus().get(LEAD_IN_ID):
        if not (ln.text and ln.regex.fullmatch(p)):
            continue
        m = LEAD_IN_SHAPE.fullmatch(p)
        if not m:
            continue
        head = m.group(1)
        for s in ln.states:
            name = head[:-len(s)].strip() if head.endswith(" " + s) else ""
            if name and not re.search(r"[.!?:;]", name) and len(name.split()) <= 8:
                return True
    return False


def is_before_f22(para):
    """The paragraph is exactly N-F24, the one sentence allowed before N-F22."""
    p = AL.norm(para)
    return any(ln.regex.fullmatch(p) for ln in corpus().get(BEFORE_F22_ID) if ln.text)


def narration_hits(message):
    """Paragraphs of an AI message that narrate the AI's own work: one opening like a note to itself, or a
    Markdown file named bare (outside code formatting; code blocks and block quotes left out). The saving line
    and the routing lead-in, said exactly, are approved words, not narration; either said another way is."""
    hits = []
    for para in re.split(r"\n\s*\n", norm(message)):
        p = para.strip()
        if is_saving_line(p) or is_lead_in(p) or is_before_f22(p):
            continue
        if NARRATION.match(p):
            hits.append(("note to itself", p[:120]))
        elif SAVING_LIKE.match(p) and not is_saving_playback(p):
            hits.append(("the saving line reworded", p[:120]))
        elif LEAD_IN_LIKE.match(p):
            hits.append(("the routing lead-in reworded", p[:120]))
    for m in BARE_MD.finditer(leader_text(norm(message))):
        hits.append(("bare file name", m.group(0)))
    for m in LINE_ID.finditer(leader_text(norm(message))):
        hits.append(("line ID", m.group(0)))
    return hits


def _opens_with(c, run):
    """The session's first AI message opens with one of the approved lines `ids` (anchored at its start);
    with `lead_in`, its first paragraph may instead be the routing lead-in (N-F23) in its approved form,
    followed by one of them. A direct start's hand-off: the lead-in, then the owner's own opening."""
    forms = [f for i in c["ids"] for f in corpus().get(i) if f.text and not f.fragment]
    if not forms:
        return False, f"no approved line among {c['ids']}"
    why = "no AI message"
    for s in _sessions(run, c.get("session")):
        first = _ai_turns(s, "first")
        if not first:
            continue
        paras = [p.strip() for p in re.split(r"\n\s*\n", norm(first[0])) if p.strip()]
        lead = bool(paras) and c.get("lead_in") and is_lead_in(paras[0])
        rest = AL.norm("\n\n".join(paras[1:] if lead else paras))
        hit = next((f for f in forms if f.regex.match(rest)), None)
        if hit:
            return True, f"session {s['n']}: " + ("the routing lead-in, then " if lead else "") + hit.label()
        why = f"session {s['n']}: first paragraph {paras[0][:120]!r}" if paras else f"session {s['n']}: empty"
    return False, why


def _said_before(c, run):
    """In the AI message where `anchor` first matches, the text before it is exactly the approved line `id`
    (said once there), and no other AI message of the session says it."""
    forms = [f for f in corpus().get(c["id"]) if f.text and not f.fragment]
    if not forms:
        return False, f"no approved line {c['id']}"
    anchor = re.compile(norm(c["anchor"]), re.M)
    why = f"{c['anchor']!r} never matched"
    for s in _sessions(run, c.get("session")):
        msgs = _ai_turns(s)
        at = next(((i, m) for i, m in enumerate(msgs) if anchor.search(norm(m))), None)
        if at is None:
            continue
        i, m = at
        before = norm(m)[:anchor.search(norm(m)).start()].strip()
        if c.get("opens"):
            # the line opens the message (its first paragraph); notes may follow it before the anchor
            before = re.split(r"\n\s*\n", before)[0].strip() if before else ""
        others = [k + 1 for k, x in enumerate(msgs) if k != i and any(f.matches(x) for f in forms)]
        if others:
            return False, f"session {s['n']}: {c['id']} also said in AI message(s) {others}"
        if not before:
            return False, f"session {s['n']} AI message {i + 1}: nothing before the anchor ({c['id']} not said)"
        if not any(f.regex.fullmatch(AL.norm(before)) for f in forms):
            return False, f"session {s['n']} AI message {i + 1}: before the anchor: {before[-200:]!r}"
        return True, f"session {s['n']} AI message {i + 1}: {c['id']}, then the anchor"
    return False, why


INPUT_HEADER = re.compile(r"(?:source|tests|expect):")


def input_body(text):
    """A practice input's body as a run sees it: the leading header lines (source:, tests:, expect:) and a
    leading `Earlier run:` paragraph left out."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) and INPUT_HEADER.match(lines[i]):
        i += 1
    paras = [p for p in re.split(r"\n\s*\n", "\n".join(lines[i:]).strip()) if p.strip()]
    if paras and paras[0].lstrip().startswith("Earlier run:"):
        paras = paras[1:]
    return "\n\n".join(paras)


def proposed_inputs(sess, req_glob):
    """(input path, its saved text or None) for each Example Scenarios row marked "(proposed" in the
    requirements file(s) matching `req_glob`; the Input cell's first `inputs/...` path, relative to that file."""
    out = []
    for rp, body in sorted(_files(sess, req_glob).items()):
        folder = rp.rsplit("/", 1)[0] + "/" if "/" in rp else ""
        lines = norm(body).splitlines()
        start = next((i for i, l in enumerate(lines) if l.strip() == "## Example Scenarios"), None)
        if start is None:
            continue
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        for row in lines[start + 1:end]:
            cells = [x.strip() for x in row.strip().strip("|").split("|")] if row.lstrip().startswith("|") else []
            if len(cells) < 3 or "(proposed" not in cells[1]:
                continue
            m = re.search(r"`(inputs/[^`]+)`", cells[2])
            ip = folder + m.group(1) if m else None
            out.append((ip or f"{rp}: {cells[0]} (no input path)", sess["files_end"].get(ip) if ip else None))
    return out


def _flat(s):
    """For a text-shown check: block-quote marks, quote styles, code and bold marks and spacing ignored."""
    return " ".join(qnorm(re.sub(r"(?m)^[ \t]*>[ \t]?", "", s)).split())


def _inputs_shown(c, run):
    forms = [f for f in corpus().get(c["id"]) if f.text and not f.fragment]
    if not forms:
        return False, f"no approved line {c['id']}"
    sess = _sessions(run, c.get("session"))
    seq = [(t["role"], t["text"]) for s in sess for t in s["turns"]]
    said = [k for k, (r, m) in enumerate(seq) if r == "ai" and any(f.matches(m) for f in forms)]
    rows = proposed_inputs(_file_session(run, c.get("session")), c.get("path", "framework/*/requirements.md"))
    if not rows:
        if c.get("allow_none"):
            return (not said, "no proposed row, and " + (f"{c['id']} said anyway" if said else f"{c['id']} not said"))
        return False, "no Example Scenarios row marked (proposed)"
    if len(said) != 1:
        return False, f"{c['id']} said in {len(said)} AI messages (one wanted)"
    k = said[0]
    anchor = re.compile(norm(c["anchor"]), re.M)
    at = next((j for j, (r, m) in enumerate(seq) if r == "ai" and anchor.search(norm(m))), None)
    if at is None:
        return False, f"{c['anchor']!r} never matched"
    if at <= k:
        return False, f"{c['id']} said at or after the anchor's message"
    shown, later = _flat(seq[k][1]), [_flat(m) for _, m in seq[k + 1:at]]
    # A line said in two parts around the inputs (N-D25: a placeholder between its sentences): its first
    # part opens the inputs, its last part follows them and ends the message, so the message ends on
    # the question. The inputs are looked for between the two parts.
    segs = [_flat(x) for x in AL.literal_segments(forms[0].toks) if _flat(x)]
    if len(segs) >= 2:
        a, b = shown.find(segs[0]), shown.rfind(segs[-1])
        if a < 0 or b < 0 or b < a + len(segs[0]):
            return False, f"{c['id']}'s two parts not found in order in turn {k + 1}"
        if not shown.endswith(segs[-1]):
            return False, f"turn {k + 1} doesn't end with {c['id']}'s last part {segs[-1]!r}"
        shown = shown[a + len(segs[0]):b]
    misses = []
    for ip, text in rows:
        if text is None:
            misses.append(f"{ip}: not saved")
            continue
        first = next((l for l in input_body(text).splitlines() if l.strip()), "")
        f1 = _flat(first)
        if not f1:
            misses.append(f"{ip}: empty body")
        elif f1 not in shown and not any(f1 in m for m in later):
            misses.append(f"{ip}: first line {first[:80]!r} not shown" + (" between its two parts" if len(segs) >= 2 else ""))
    if misses:
        return False, "; ".join(misses[:4])
    return True, f"{c['id']} in turn {k + 1}, before the anchor; {len(rows)} proposed input(s) shown"


def _scan(run, n, fn, what):
    for s in _sessions(run, n):
        for i, m in enumerate(_ai_turns(s), 1):
            hits = fn(m)
            if hits:
                return False, f"session {s['n']} AI message {i}: {what}: {hits[:3]}"
    return True, f"no {what} in any AI message"


# ---------------------------------------------------------------- frontmatter

def _yaml_keys(c, body, path):
    fm, _ = ST.split_frontmatter(body)
    if fm is None:
        return False, f"{path}: no frontmatter"
    keys = ST.top_keys(fm)
    want = c["keys"]
    if c.get("exact", True) and keys != want:
        return False, f"{path}: keys {keys} != {want}"
    missing = [k for k in want if k not in keys]
    if missing:
        return False, f"{path}: missing {missing}"
    bad = [k for k in c.get("absent", []) if k in keys]
    if bad:
        return False, f"{path}: has {bad}"
    return True, f"{path}: keys {keys}"


# ---------------------------------------------------------------- the fill check (N-B52, N-B53)

def _split_list(s):
    s = re.sub(r"\s+and\s+", ", ", s.strip().rstrip("."))
    return [x.strip(" `'\"") for x in s.split(",") if x.strip(" `'\"")]


def plan_expectations(plan_text):
    """task, folder, context files and connections for the plan's agent task, from the plan."""
    fm, body = ST.split_frontmatter(plan_text)
    folder = re.search(r"^workflow:\s*(\S+)", fm or "", re.M)
    tasks = re.split(r"^### ", ST.section(body, "Tasks"), flags=re.M)[1:]
    agent = next((t for t in tasks if re.search(r"\*\*Builds:\*\*\s*New agent", t)), None)
    if not agent:
        return None
    tid = agent.split(" ", 1)[0]
    uses = re.search(r"\*\*Uses / hands on:\*\*(.*)", agent)
    cids = re.findall(r"\bC\d+\b", uses.group(1) if uses else "")
    dr = ST.tables(ST.section(body, "Data Readiness"))
    files = []
    if dr:
        head = dr[0][0]
        col = next((i for i, h in enumerate(head) if h.lower().startswith("read at runtime")), None)
        for r in dr[0][1:]:
            if r[0] in cids and col is not None:
                files.append(r[col].strip("` "))
    aid = re.search(r"New agent:\s*(A\d+)", agent).group(1)
    bp = re.search(rf"^### {aid}\b.*?(?=^### |\Z)", ST.section(body, "Component Blueprints"), re.M | re.S)
    tools = re.search(r"\*\*Tools:\*\*\s*(.+)", bp.group(0)) if bp else None
    conns = [] if not tools or tools.group(1).strip().lower() in ("none", "—", "-") else _split_list(tools.group(1))
    return {"task": tid, "folder": folder.group(1) if folder else None, "context_files": files, "connections": conns}


BUILD_NAMES = {"task ID": "task", "workflow-slug": "folder", "each context file, by its place in OneDrive": "files",
               "its connections / nothing else": "conns", "the lines 6.3 names from 6.4": "lines"}
NOFILE_NAMES = {"its connections / nothing": "conns"}


def find_prompt(message, kind):
    """The prompt the leader pastes: a fenced block, else the message from its fixed opening."""
    opener = "Build the agent described in task" if kind == "build" else "In this agent,"
    for blk in re.findall(r"```[^\n]*\n(.*?)```", message, re.S):
        if opener in blk:
            return blk.strip()
    i = message.find(opener)
    return message[i:].strip() if i >= 0 else None


def fill_check_prompt(prompt, kind, expect, carried=(), require_carried=()):
    """Problems with a filled build or fix prompt (an empty list when every field is right)."""
    C = corpus()
    probs = []
    nm = AL.norm(prompt)
    if kind == "build":
        main = C.get("N-B52", "The build prompt")[0]
        m = re.compile(AL.capture_regex(main.toks, BUILD_NAMES), re.S | re.I).search(nm)
        files = None
        if not m:
            # the no-context-file form: its fourth sentence replaced
            alt = C.get("N-B52", "With no context file, its fourth sentence")[0]
            text = main.text.replace(
                "The agent reads only [each context file, by its place in OneDrive], and connects to [its connections / nothing else].",
                alt.text)
            m = re.compile(AL.capture_regex(AL.tokens(text), {**BUILD_NAMES, **NOFILE_NAMES}), re.S | re.I).search(nm)
            files = [] if m else None
        if not m:
            return ["the build prompt's fixed words aren't N-B52's (a word changed or a sentence missing)"]
        g = m.groupdict()
        if files is None:
            files = _split_list(g.get("files") or "")
        if expect.get("task") and g["task"].strip() != expect["task"]:
            probs.append(f"task {g['task']!r} != the plan's {expect['task']!r}")
        if expect.get("folder") and g["folder"].strip() != expect["folder"]:
            probs.append(f"folder framework/{g['folder']} != framework/{expect['folder']}")
        if "context_files" in expect:
            want = sorted(Path(f).name for f in expect["context_files"])
            got = sorted(Path(f).name for f in files)
            if want != got:
                probs.append(f"context files {got} != exactly the plan's {want}")
            for f in files:
                if "Documents/Cowork/" not in f:
                    probs.append(f"context file {f!r} isn't named by its runtime copy's place (Documents/Cowork/[workflow-slug])")
        if "connections" in expect:
            got_c = (g.get("conns") or "").strip().rstrip(".")
            got = [] if got_c.lower() in ("nothing", "nothing else") else _split_list(got_c)
            if sorted(x.lower() for x in got) != sorted(x.lower() for x in expect["connections"]):
                probs.append(f"connections {got} != exactly the plan's {expect['connections']}")
        low = prompt.lower()
        lines_part = prompt[low.find("word for word:"):] if "word for word:" in low else ""
        for line in carried:
            if AL.norm(line) not in AL.norm(lines_part):
                probs.append(f"carried line missing or reworded: {line[:70]!r}")
        for lid in require_carried:
            forms = [f for f in C.get(lid) if f.text and not f.fragment]
            if forms and not any(f.matches(lines_part) for f in forms):
                probs.append(f"carried line {lid} missing or reworded")
    else:
        fixm = C.get("N-B53", "The fix prompt")[0]
        m = re.compile(AL.capture_regex(fixm.toks, {"the change": "change"}), re.S | re.I).search(nm)
        if not m or not nm.rstrip().endswith("Change nothing else."):
            return ["the fix prompt's fixed words aren't N-B53's (it opens 'In this agent,' and ends 'Change nothing else.')"]
        if not m.group("change").strip():
            probs.append("the fix prompt names no change")
        task = re.search(r"matches task (\S+) of design-plan\.md in my OneDrive, in [^/\s]+/framework/([^\s.]+)", nm)
        if task:
            if expect.get("task") and task.group(1) != expect["task"]:
                probs.append(f"task {task.group(1)!r} != the plan's {expect['task']!r}")
            if expect.get("folder") and task.group(2) != expect["folder"]:
                probs.append(f"folder {task.group(2)!r} != {expect['folder']!r}")
        quoted = re.search(r"carries this line word for word: '(.+?)'\.", nm)
        if quoted and carried and AL.norm(quoted.group(1)) not in {AL.norm(x) for x in carried}:
            probs.append(f"the carried line in the fix prompt isn't word for word: {quoted.group(1)!r}")
    return probs


def _fill_check(c, run):
    n = c.get("session")
    sess = _file_session(run, n)
    kind = c.get("kind", "build")
    expect = dict(c.get("expect") or {})
    if not expect:
        # the default finds the plan wherever the platform keeps the working folder (framework/,
        # ai-workspace/framework/, drive/ai-workspace/framework/, onedrive/ai-workspace/framework/),
        # never a set-aside copy
        plans = {p: v for p, v in _files(sess, c.get("plan", "*framework/*/design-plan.md")).items()
                 if "/history/" not in p}
        if not plans:
            return False, "no plan to check the prompt against (give `expect` or `plan`)"
        expect = plan_expectations(sorted(plans.items(), key=lambda kv: (len(kv[0]), kv[0]))[0][1])
        if expect is None:
            return False, "no agent task in the plan to check the prompt against"
    carried = list(c.get("carried") or [])
    for rel, body in _files(sess, "**/carried-lines.md").items():
        carried += [l.strip()[2:].strip().strip('"') for l in body.splitlines() if l.strip().startswith("> ")]
    found = None
    for s in _sessions(run, n):
        for m in _ai_turns(s):
            p = find_prompt(m, kind)
            if p:
                found = p
    if not found:
        return False, f"no {kind} prompt in any AI message"
    probs = fill_check_prompt(found, kind, expect, carried, c.get("require_carried", []))
    return (not probs, "; ".join(probs) if probs else f"every field filled from the plan ({expect})")


RELEASE_CHECKS = Path(__file__).resolve().parents[1] / "release" / "release-checks.md"


def release_check_rows():
    """The maintainer checklist's rows, {id: {"status": ...}}: the table in release/release-checks.md
    (never shipped; no skill reads it)."""
    import re as _re
    rows = {}
    for line in RELEASE_CHECKS.read_text().splitlines():
        cells = [c.strip() for c in _re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if len(cells) >= 5 and cells[0].isdigit():
            rows[int(cells[0])] = {"id": int(cells[0]), "status": cells[4]}
    return rows


def release_checks_passed(ids):
    """Every check marked `verified` in the maintainer checklist. Skills take the safe path for every
    check whatever its status, so a `verified` row lands together with the skill edit that relies on it."""
    rows = release_check_rows()
    return all(r and r.get("status") == "verified" for r in (rows.get(i) for i in ids))


def resolve_release_items(ev):
    """An eval's judged expectations and preconditions that depend on the maintainers' release
    checks, read the way the scripted `release_check` check reads them: an item carrying
    `release_check: {ids, passed, open}` takes the text for the checks' state (`passed` when every row
    is verified for this release, `open` otherwise), and a null text drops the item. A precondition is
    then a plain string again. Returns the eval, changed in place."""
    def pick(rc):
        return rc.get("passed") if release_checks_passed(rc["ids"]) else rc.get("open")
    exps = []
    for x in ev.get("expectations", []):
        if isinstance(x, dict) and "release_check" in x and x.get("kind") == "judged":
            text = pick(x["release_check"])
            if text is None:
                continue
            x = {**{k: v for k, v in x.items() if k != "release_check"}, "text": text}
        exps.append(x)
    ev["expectations"] = exps
    if "preconditions" in ev:
        pres = []
        for p in ev["preconditions"]:
            if isinstance(p, dict):
                p = pick(p["release_check"])
            if p is not None:
                pres.append(p)
        ev["preconditions"] = pres
    return ev


# ---------------------------------------------------------------- dispatch

LEAD_IN = re.compile(r"answer it as you would at work", re.I)


def _nf4_leads(run):
    """N-F4 leads the first workflow checkpoint each session relays (in place of "Answer it as you would at
    work:"), and no checkpoint is relayed before it (James, 2026-11-23, after final-build-3). A relayed
    checkpoint is a message with a quoted block and either lead-in."""
    forms = [ln for ln in corpus().lines if ln.id == "N-F4" and ln.text]
    seen = 0
    for s in run["sessions"]:
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            quote = re.search(r"^\s*>", m, re.M)
            nf4 = next((f for f in forms if f.matches(m)), None)
            lead = LEAD_IN.search(m)
            if not quote or not (nf4 or lead):
                continue
            seen += 1
            where = f"session {s['n']} AI message {i}"
            if not nf4:
                return False, f"{where}: a checkpoint relayed without N-F4 leading it"
            at = m.lower().find("this is a practice run")
            if at > quote.start():
                return False, f"{where}: N-F4 said after the quoted checkpoint"
            if lead and lead.start() < at:
                return False, f"{where}: 'Answer it as you would at work:' before N-F4"
            break  # only each session's first relayed checkpoint
    return True, ("N-F4 leads the first relayed checkpoint in every session that relays one" if seen
                  else "no checkpoint relayed")


BRIEF_BLOCK = re.compile(r"```[^\n]*\n\s*(?:Skill|Agent) brief:", re.I)


def _nf4_before_creator(run):
    """Pass 3, Task 2 (B1): Build's form of N-F4 (the Deny line, with no "answer the workflow's questions")
    is said in each session before the platform's creator starts (the first brief) and before the first
    checkpoint it relays; a session with neither passes."""
    forms = [ln for ln in corpus().get("N-F4", "Build") if ln.text]
    for s in run["sessions"]:
        said = False
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            nf4 = next((f for f in forms if f.matches(m)), None)
            at = m.lower().find("this is a practice run") if nf4 else -1
            brief = BRIEF_BLOCK.search(m)
            quote = re.search(r"^\s*>", m, re.M) if LEAD_IN.search(m) else None
            first = min([x.start() for x in (brief, quote) if x], default=None)
            if first is not None and not said and not (nf4 and at < first):
                what = "the creator's brief" if brief and brief.start() == first else "a relayed checkpoint"
                return False, f"session {s['n']} AI message {i}: {what} before N-F4's Build form"
            if first is not None:
                break  # only each session's first brief or checkpoint
            said = said or bool(nf4)
    return True, "N-F4's Build form leads the creator and the first relayed checkpoint in every session"


FRESH_BLOCK = re.compile(r"```[^\n]*\n[^\n]*[—-]+ practice run[ \t]*\n", re.I)


def _nf4_before_fresh_run(run):
    """Pass 3, Task 4 (F5); Pass 5 (E14): the fresh-chat run's hand-over is one message, and it carries Build's
    form of N-F4 before its block, in that message. Said only in an earlier message (the two-message hand-over
    before 11.0's Pass 5), or after the block, fails; a session with no such block passes."""
    forms = [ln for ln in corpus().get("N-F4", "Build") if ln.text]
    for s in run["sessions"]:
        for i, m in enumerate(_ai_turns(s, "any")):
            b = FRESH_BLOCK.search(m)
            if b and not any(f.matches(m[:b.start()]) for f in forms):
                return False, f"session {s['n']} AI message {i + 1}: the fresh-chat run's block with no N-F4 Build form before it in its message"
    return True, "N-F4's Build form is in every fresh-chat run hand-over, before its block"


READY_ASK = re.compile(r"(?i)\bsay ['\"]?ready['\"]?")


def _handover_one_message(run, n=None):
    """Pass 5 (E14): every hand-over of a practice run (Build's fresh-chat run, Test's practice chat) is one
    message: its setup first, then the box last, with nothing after it, and no "say 'ready'" round trip."""
    for s in _sessions(run, n):
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            where = f"session {s['n']} AI message {i}"
            if READY_ASK.search(m):
                return False, f"{where}: asks the leader to say 'ready'"
            b = FRESH_BLOCK.search(m)
            if not b:
                continue
            end = m.find("```", b.end())
            if end < 0 or m[end + 3:].strip():
                return False, f"{where}: something follows the box"
            if len(m[:b.start()].split()) < 20:
                return False, f"{where}: the box with no setup before it in the same message"
    return True, "every practice-run hand-over is one message, its box last"


def _deny_in_every_handover(run, n=None):
    """Pass 5 (plan review C1): every hand-over of a practice run says the Deny line (N-F4, any form) before its
    box, in the same message, whatever the workflow's own connections: the leader's other connections stay on."""
    forms = [ln for ln in corpus().lines if ln.id == "N-F4" and ln.text]
    for s in _sessions(run, n):
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            b = FRESH_BLOCK.search(m)
            if b and not any(f.matches(m[:b.start()]) for f in forms):
                return False, f"session {s['n']} AI message {i}: a practice-run box with no Deny line before it"
    return True, "the Deny line is in every practice-run hand-over"


PRACTICE_LINE = "Practice run: nothing will be sent or changed."
# Pass 5 (E22, plan review C3): what the workflow produced, as opposed to a line the assistant says before its
# skill loads ("I'll run the … skill on all seven practice inputs, drafting only."): a fenced block, an input
# label, an email's subject or greeting, or a question to the person
OUTPUT_SIGNS = re.compile(r"```|^\s*(?:Input \d+\s*:|Subject\s*:|(?:Hi|Hello|Dear|Hey)\b)|\?\s*$", re.M | re.I)
PREAMBLE_MAX_WORDS = 40


def practice_line_position(reply):
    """Where the fixed first line sits in a pasted run reply: "first" (its opening words), "after_preamble" (a
    short line or two came first, holding nothing the workflow produced: the run stands), "after_output" (a
    draft, a question, a stop or an input's result came before it: refused, N-T51) or "missing"."""
    text = norm(reply).strip()
    at = text.find(norm(PRACTICE_LINE))
    if at < 0:
        return "missing"
    before = text[:at].strip()
    if not before:
        return "first"
    if OUTPUT_SIGNS.search(before) or len(before.split()) > PREAMBLE_MAX_WORDS:
        return "after_output"
    return "after_preamble"


def practice_line_stands(reply):
    """The run carries its practice-run mode: the fixed line comes before anything the workflow produced."""
    return practice_line_position(reply) in ("first", "after_preamble")


FIRST_LINE_CLAIM = re.compile(r"(?i)\b(?:starts?|started|starting|begins?|began|opens?|opened|leads?|led) with (?:the |its |a )?"
                              r"(?:fixed )?(?:practice[- ]run (?:line|label)|['\"]?practice run: nothing will be sent)")


def _no_false_first_line_claim(run, n=None):
    """Pass 5 (E22, missed twice in James's run): once the leader pastes a reply whose practice-run line isn't its
    opening words, no later AI message of that session says the reply starts (begins, opens) with it."""
    for s in _sessions(run, n):
        late = False
        for i, t in enumerate(s["turns"]):
            if t["role"] != "ai":
                if PRACTICE_LINE.lower() in norm(t["text"]).lower() and practice_line_position(t["text"]) != "first":
                    late = True
                continue
            if late and FIRST_LINE_CLAIM.search(norm(t["text"])):
                return False, f"session {s['n']} turn {i + 1}: says the reply starts with the practice-run line, but a line came before it"
    return True, "no claim that a reply starts with the practice-run line when something came before it"


def check(c, run):
    """Return (passed, evidence)."""
    t = c["type"]
    n = c.get("session")
    if t in ("ai_contains", "ai_regex"):
        which = c.get("turn", "any")
        for s in _sessions(run, n):
            msgs = _ai_turns(s, "any" if which == "all" else which)
            if t == "ai_contains":
                hits = [qnorm(c["text"]) in qnorm(m) for m in msgs]
            else:
                hits = [bool(re.search(norm(c["pattern"]), norm(m), re.M)) for m in msgs]
            ok = all(hits) and hits if which == "all" else any(hits)
            if ok:
                return True, f"found in session {s['n']}"
        return False, "not found in any AI message" + (" (first message)" if which == "first" else "")
    if t == "leader_regex":
        # what the leader already said (an answer volunteered before its question), so a check can
        # accept the question not being asked again
        for s in _sessions(run, n):
            for tn in s["turns"]:
                if tn["role"] != "ai" and re.search(norm(c["pattern"]), norm(tn["text"]), re.M):
                    return True, f"the leader said it in session {s['n']}"
        return False, "not in any leader message"
    if t in ("ai_not_contains", "ai_not_regex"):
        skip = tuple(c.get("outside_fences") or ())
        for s in _sessions(run, n):
            for i, m in enumerate(_ai_turns(s)):
                if skip:
                    m = _strip_fences(m, skip)
                hit = (qnorm(c["text"]) in qnorm(m)) if t == "ai_not_contains" else re.search(norm(c["pattern"]), norm(m), re.M)
                if hit:
                    return False, f"session {s['n']} AI message {i + 1}: {m[:200]!r}"
        return True, "absent from every AI message"
    if t in ("quote", "quote_absent"):
        forms = [f for f in corpus().get(c["id"], c.get("form")) if f.text]
        if not forms:
            return False, f"no approved line {c['id']} ({c.get('form', 'any form')}) in approved-lines.json"
        if c.get("ending"):
            # a line the spec lets end another way ("…next, keeping the steps you fixed…")
            tails = [e.text.lstrip("…").lstrip(".") for e in corpus().get(c["id"], c["ending"]) if e.text]
            forms = [AL.Line({"id": f.id, "form": f"{f.form} + {c['ending']}",
                               "text": re.sub(r"[.?!]\s*$", "", f.text) + t}) for f in forms for t in tails]
        which = c.get("turn", "any")
        for s in _sessions(run, n):
            # a named form's Claude Code and Codex form (no location, routing.md) is the same line there
            local = forms + ([f for f in corpus().get(c["id"]) if f.text and c.get("form") and not c.get("ending")
                              and f.form == f"{c['form']}, Claude Code and Codex (no location)"]
                             if s.get("platform") in ("claude-code", "codex") else [])
            for i, m in enumerate(_ai_turns(s, which), 1):
                hit = next((f for f in local if f.matches(m)), None)
                # final-build-2 (2026-11-22, James): a line that isn't strict counts as said with a word or
                # two changed, none of them a protected word (approved_lines.STRICT_CUES)
                loose = None if hit else next((f for f in local if f.loose_matches(m)), None)
                if hit or loose:
                    got = hit or loose
                    how = "" if hit else ", with a small edit"
                    if t == "quote":
                        return True, f"{got.label()} in session {s['n']} AI message {i}{how}"
                    return False, f"{got.label()} said in session {s['n']} AI message {i}{how}"
        return (False, f"{c['id']} not said word for word") if t == "quote" else (True, f"{c['id']} not said")
    if t == "scripted_lines":
        skill = c.get("skill") or run.get("skill")
        return _scan(run, n, lambda m: quote_hits(m, skill), "scripted line said with words changed")
    if t == "vocabulary":
        said = leader_never_words(run)
        return _scan(run, n, lambda m: vocabulary_hits(m, said), "Never-column word")
    if t == "narration":
        return _scan(run, n, narration_hits, "narration")
    if t == "opens_with":
        return _opens_with(c, run)
    if t == "said_before":
        return _said_before(c, run)
    if t == "inputs_shown":
        return _inputs_shown(c, run)
    if t == "no_team_visible_writes":
        return _no_team_visible_writes(run)
    if t == "quoted_output_seen":
        return _quoted_output_seen(run)
    if t == "nf4_leads":
        return _nf4_leads(run)
    if t == "nf4_before_creator":
        return _nf4_before_creator(run)
    if t == "one_question":
        return _one_question(c, run)
    if t == "phrases_in_blocks":
        return _phrases_in_blocks(c, run)
    if t == "asked_before_save":
        return _asked_before_save(c, run)
    if t == "handover_one_message":
        return _handover_one_message(run, n)
    if t == "deny_in_every_handover":
        return _deny_in_every_handover(run, n)
    if t == "no_false_first_line_claim":
        return _no_false_first_line_claim(run, n)
    if t == "nf4_before_fresh_run":
        return _nf4_before_fresh_run(run)
    if t == "no_time_or_step_numbers":
        allowed = leader_sizes(run)
        return _scan(run, n, lambda m: time_or_step_hits(m, allowed), "time estimate or step number")
    if t == "signposts":
        skill = c.get("skill")
        if skill not in SIGNPOST_IDS:
            return False, f"signposts needs a skill with parts (one of {', '.join(SIGNPOST_IDS)}); {skill or 'none'} has no signposts"
        total, ids = SIGNPOST_IDS[skill]
        total = c.get("of", total)
        forms = []
        for lid in ids:
            forms += [f.text for f in corpus().get(lid) if f.text and not f.derived and re.match(r"Part \d of \d", f.text)]
        # build-full-1 fix (2026-11-21): every part 1..total is expected, each said in any of its approved
        # forms ("Part 2 of 2 in this fix — save it and test") or, with none approved, as bare "Part k of N";
        # before, one approved form of an `of` count made the check want that one signpost only
        want = [[w for w in forms if re.match(rf"Part {k} of {total}\b", w)] or [f"Part {k} of {total}"]
                for k in range(1, total + 1)]
        # smoke-1 fix (2026-11-14): in order across the sessions joined, so a stop and resume between two
        # parts counts (each signpost is said once, in whichever session reaches that part)
        sess = _sessions(run, n)
        text = AL.norm("\n".join(m for s in sess for m in _ai_turns(s)))
        pos = 0
        # Design baseline fix (2026-11-14): `optional` lists part numbers that may be left out (Design's
        # Part 3 when there is nothing to ask: Part 4 follows with no announcement and keeps its number)
        optional = set(c.get("optional", []))
        for k, alts in enumerate(want, 1):
            found = [j for j in (text.find(AL.norm(w).rstrip("."), pos) for w in alts) if j >= 0]
            if not found and k in optional:
                continue
            if not found:
                return False, f"{' or '.join(map(repr, alts))} missing or out of order"
            pos = min(found)
        return True, f"{skill}'s {len(want)} signposts in order (session{'s' if len(sess) > 1 else ''} " \
                     f"{', '.join(str(s['n']) for s in sess)})"
    if t == "max_words":
        return _max_words(c, run)
    if t == "fill_check":
        return _fill_check(c, run)
    if t == "file_existed_during":
        for s in _sessions(run, n):
            for i, turn_files in enumerate(s["files_by_turn"]):
                if any(fnmatch.fnmatch(p, c["path"]) for p in turn_files):
                    return True, f"present after AI turn {i + 1} of session {s['n']}"
        return False, f"{c['path']} never present after any turn"
    if t == "tool_write":
        return _tool_write(c, run)
    if t == "saved_before_next_question":
        return _saved_before_next_question(c, run)
    if t == "bash_count":
        return _bash_count(c, run)
    if t == "no_tool_call":
        return _no_tool_call(c, run)
    if t == "read_before_save":
        return _read_before_save(c, run)
    if t == "release_check":
        passed = release_checks_passed(c["ids"])
        ok, why = check(c["passed" if passed else "open"], run)
        return ok, f"release checks {c['ids']} {'passed' if passed else 'open'}: {why}"
    if t in ("all", "any"):
        res = [check(x, run) for x in c["checks"]]
        ok = all(r[0] for r in res) if t == "all" else any(r[0] for r in res)
        return ok, "; ".join(e for _, e in res)
    if t == "no_yaml":
        raise ValueError("no_yaml is retired: use yaml_keys")

    s = _file_session(run, n)
    files = _files(s, c.get("path", "*"))
    if t == "file_exists":
        return (bool(files), f"found {sorted(files)}" if files else f"no {c['path']}")
    if t == "file_absent":
        return (not files, "absent" if not files else f"present: {sorted(files)}")
    if t == "no_added_files":
        start = set(s["files_start"])
        allowed = c.get("except", [])
        added = [p for p in files_all(s) if p not in start and not any(fnmatch.fnmatch(p, a) for a in allowed)]
        return (not added, "no files added" if not added else f"added: {added}")
    if t == "file_unchanged":
        start = _files(s, c["path"], "start")
        if not start:
            return False, f"no {c['path']} at session start"
        diff = [p for p in start if hashlib.sha256(start[p].encode()).hexdigest()
                != hashlib.sha256(files.get(p, "\0missing").encode()).hexdigest()]
        return (not diff, "unchanged" if not diff else f"changed or removed: {diff}")
    if not files:
        return False, f"no {c['path']}"
    # final-build fix (2026-11-22): a path glob matching several files checked only the first one by name,
    # so a line kept in a skill's reference file failed "file_regex" and a "file_not_regex" read one file
    # of many (fail-open). Now a positive check passes when any matched file passes, a negative check
    # only when every matched file does
    if len(files) > 1 and t in ("file_regex", "file_not_regex", "file_contains", "file_not_contains"):
        res = [(p, check(dict(c, path=p), run)) for p in sorted(files)]
        if t in ("file_regex", "file_contains"):
            hit = next((p for p, (ok, _) in res if ok), None)
            return (hit is not None, hit or f"none of {sorted(files)}")
        miss = [why for p, (ok, why) in res if not ok]
        return (not miss, "; ".join(miss) if miss else f"all of {sorted(files)}")
    path, body = sorted(files.items())[0]
    nb = norm(body)
    if t == "file_contains":
        return (norm(c["text"]) in nb, f"{path}")
    if t == "file_not_contains":
        return (norm(c["text"]) not in nb, f"{path}")
    if t == "file_regex":
        return (bool(re.search(norm(c["pattern"]), nb, re.M)), f"{path}")
    if t == "file_not_regex":
        m = re.search(norm(c["pattern"]), nb, re.M)
        return (not m, f"{path}" + (f": {m.group(0)[:120]!r}" if m else ""))
    if t == "yaml_keys":
        return _yaml_keys(c, body, path)
    if t == "structure":
        if c["kind"] == "requirements":
            root = s.get("root")
            if not root:
                return False, "requirements structure needs the session's workspace on disk"
            probs = ST.check_requirements(Path(root) / path, c.get("registry"))
        elif c["kind"] == "plan":
            # Pass 4 (P4): a plan this run wrote or changed must be in this release's form; one it left as it
            # found it (a fixture's older plan) may keep the older form
            # final review M4: against the run's first session too, so a plan an earlier session wrote, left
            # unchanged by the checked one, is still checked as written
            starts = [(x.get("files_start") or {}) for x in (_listed(run)[:1] + [s])]
            written = any(st.get(path) != body for st in starts)
            probs = ST.check_text("plan", body, written=written)
        else:
            probs = ST.check_text(c["kind"], body)
        return (not probs, f"{path}: " + ("; ".join(probs[:6]) if probs else "well formed"))
    if t == "section_regex":
        lines = nb.splitlines()
        head = norm(c["section"])
        start = next((i for i, l in enumerate(lines) if l.strip() == head), None)
        if start is None:
            return (False, f"{path}: no {c['section']!r} section")
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        sec = "\n".join(lines[start + 1:end])
        m = re.search(norm(c["pattern"]), sec, re.M)
        ok = bool(m) if c.get("must", True) else not m
        return (ok, f"{path} [{c['section']}]" + (f": {m.group(0)[:120]!r}" if m else ""))
    if t == "file_line":
        lines = body.splitlines()
        k = c["line"] - 1
        got = lines[k] if k < len(lines) else ""
        return (bool(re.search(norm(c["pattern"]), norm(got))), f"line {c['line']}: {got[:160]!r}")
    if t == "sections_in_order":
        heads = [norm(l.strip()) for l in body.splitlines() if re.match(r"#{1,2} ", l)]
        want = [norm(h) for h in c["headings"]]
        pos = 0
        for w in want:
            matches = [i for i in range(pos, len(heads)) if fnmatch.fnmatch(heads[i], w)]
            if not matches:
                return False, f"{path}: {w!r} missing or out of order; headings: {heads}"
            pos = matches[0] + 1
        if c.get("only"):
            extra = [h for h in heads if h.startswith("## ") and not any(fnmatch.fnmatch(h, w) for w in want)]
            if extra:
                return False, f"{path}: other sections {extra}"
        return True, f"{path}: in order"
    raise ValueError(f"unknown check type {t}")


def file_writes(events_path, path):
    """The writes, in order, that tool calls in a session's events.jsonl made to files matching the
    path glob, as (tool, new text): Write's content, Edit's new_string (each of MultiEdit's edits),
    and a Bash command naming the file, with a sed substitution's search parts dropped (so
    `s/^approved: false$/approved: true/` reads as writing "approved: true"). None when there's
    no events.jsonl."""
    try:
        lines = Path(events_path).read_text(errors="replace").splitlines()
    except OSError:
        return None
    name = Path(path).name
    out = []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        content = (e.get("message") or {}).get("content") if e.get("type") == "assistant" else None
        for b in content if isinstance(content, list) else []:
            if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                continue
            tool, inp = b.get("name"), b.get("input") or {}
            if tool in ("Write", "Edit", "MultiEdit"):
                fp = str(inp.get("file_path") or "")
                if not (fnmatch.fnmatch(fp, path) or fnmatch.fnmatch(fp, "*/" + path)):
                    continue
                if tool == "Write":
                    out.append((tool, str(inp.get("content") or "")))
                elif tool == "Edit":
                    out.append((tool, str(inp.get("new_string") or "")))
                else:
                    out += [(tool, str(x.get("new_string") or "")) for x in inp.get("edits") or []]
            elif tool == "Bash":
                cmd = str(inp.get("command") or "")
                if any(fnmatch.fnmatch(tok, "*" + name) for tok in re.findall(r"[^\s'\";|&<>]+", cmd)):
                    out.append((tool, re.sub(r"\bs([/|#])(?:\\.|(?!\1).)*\1", r"s\1\1", cmd)))
    return out


def bash_commands(events_path):
    """Every Bash command the session's tool calls ran, in order; None when there's no events.jsonl."""
    try:
        lines = Path(events_path).read_text(errors="replace").splitlines()
    except OSError:
        return None
    out = []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        content = (e.get("message") or {}).get("content") if e.get("type") == "assistant" else None
        for b in content if isinstance(content, list) else []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                out.append(str((b.get("input") or {}).get("command", "")))
    return out


def _no_tool_call(c, run):
    """Pass 3 final review (M8, I5): no tool call in the session's events.jsonl whose name matches `tool`
    and whose input, as JSON, matches `input_pattern` (when given) and doesn't match `input_not_pattern`
    (when given); with `after`, only calls after the first assistant text matching it count (a quick real
    check before the first brief, say). A broken guardrail fails here, not only before the judge. No
    session with an events.jsonl fails closed: what was called can't be told."""
    tool = re.compile(c["tool"])
    inp_pat = re.compile(c["input_pattern"], re.M) if c.get("input_pattern") else None
    not_pat = re.compile(c["input_not_pattern"], re.M) if c.get("input_not_pattern") else None
    after = re.compile(c["after"], re.M) if c.get("after") else None
    read = False
    for s in _sessions(run, c.get("session")):
        if not s.get("root"):
            continue
        try:
            lines = (Path(s["root"]).parent / "events.jsonl").read_text(errors="replace").splitlines()
        except OSError:
            continue
        read = True
        started = after is None
        for line in lines:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            content = (e.get("message") or {}).get("content") if isinstance(e, dict) and e.get("type") == "assistant" else None
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and not started and after.search(str(b.get("text") or "")):
                    started = True
                if b.get("type") != "tool_use" or not started or not tool.search(str(b.get("name") or "")):
                    continue
                inp = json.dumps(b.get("input") or {}, ensure_ascii=False)
                if inp_pat and not inp_pat.search(inp):
                    continue
                if not_pat and not_pat.search(inp):
                    continue
                return False, f"session {s['n']}: {b.get('name')} {inp[:200]}"
    if not read:
        return False, "no session with an events.jsonl, so the tool calls can't be told: fails closed"
    return True, f"no {c['tool']!r} call" + (f" matching {c['input_pattern']!r}" if inp_pat else "") + \
        (f" after {c['after']!r}" if after else "")


# An AI text that has the leader save, upload or download the part (build-smoke-1): N-B12's skills-list
# ask, a save from the save card, or an upload or download of the packaged file.
SAVE_OFFER = re.compile(r"in your skills list\b[^?\n]*\?"
                        r"|\b(?:save|upload)\b[^.\n]{0,80}?(?:\bsave card\b|\.zip\b|\.skill\b)"
                        r"|\bdownload\b[^.\n]{0,80}?\.(?:zip|skill)\b", re.I)
PACKAGE_CMD = re.compile(r"\bpackage_skill\b")
PACKAGE_READ = re.compile(r"\b(?:unzip|zipinfo|bsdtar|tar|python3?|strings|zcat)\b[\s\S]*?\.skill\b"
                          r"|\.skill\b[\s\S]*?\b(?:unzip|zipinfo|zipfile|bsdtar)\b")


def _prose(m):
    """A message without its fenced blocks and block-quoted lines: the AI's own words, for question counts."""
    m = re.sub(r"```.*?```", " ", m, flags=re.S)
    return re.sub(r"(?m)^[ \t]*>.*$", " ", m)


def _one_question(c, run):
    """Pass 5 (E6, E23): every AI message matching `containing` asks at most one question, and that question is
    in its last paragraph (X2: one question per message, last); with `not_pattern`, none of those messages matches
    it ("Do you agree", the rubber stamp E23 retired). Fenced blocks and quotes don't count. None said fails closed."""
    want = re.compile(norm(c["containing"]), re.M)
    bad = re.compile(norm(c["not_pattern"]), re.M) if c.get("not_pattern") else None
    seen = 0
    for s in _sessions(run, c.get("session")):
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            if not want.search(norm(m)):
                continue
            seen += 1
            where = f"session {s['n']} AI message {i}"
            if bad and bad.search(norm(m)):
                return False, f"{where}: {bad.search(norm(m)).group(0)!r}"
            prose = _prose(norm(m)).strip()
            paras = [p for p in re.split(r"\n\s*\n", prose) if p.strip()]
            asks = prose.count("?")
            if asks > 1:
                return False, f"{where}: {asks} questions"
            if asks == 1 and "?" not in (paras[-1] if paras else ""):
                return False, f"{where}: its question isn't in the last paragraph"
    return (seen > 0, f"{seen} message(s) checked" if seen else "no message matched")


START_PHRASES = [r"\btest the workflow I built\b", r"\bchange my workflow\b", r"\brun the (?:analyze|deconstruct|design|build|test) skill\b",
                 r"\bupdate my registry\b"]


def _phrases_in_blocks(c, run):
    """Pass 5 (E32, X3): in every AI message matching `containing` (every message, without it), a framework start
    phrase (or each of `phrases`) is never said inline: it stands alone in a code block. None matched fails closed."""
    want = re.compile(norm(c["containing"]), re.M) if c.get("containing") else None
    pats = [re.compile(norm(p), re.I) for p in (c.get("phrases") or START_PHRASES)]
    seen = 0
    for s in _sessions(run, c.get("session")):
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            t = norm(m)
            if want and not want.search(t):
                continue
            seen += 1
            outside = re.sub(r"`[^`\n]*`", " ", re.sub(r"```.*?```", " ", t, flags=re.S))
            hit = next((p.search(outside) for p in pats if p.search(outside)), None)
            if hit:
                return False, f"session {s['n']} AI message {i}: {hit.group(0)!r} said inline, not in a code block"
    return (seen > 0, f"{seen} message(s) checked" if seen else "no message matched")


def _asked_before_save(c, run):
    """Pass 5 (E16): an AI message matching `pattern` (Build's keep-or-drop question about what an extended skill
    held that the plan doesn't) comes before the first AI message that offers the save (SAVE_OFFER), in an earlier
    message or earlier in the same one. A session with no save offer passes only when the pattern was said."""
    pat = re.compile(norm(c["pattern"]), re.M)
    anchor = re.compile(norm(c["anchor"]), re.M | re.I) if c.get("anchor") else SAVE_OFFER
    for s in _sessions(run, c.get("session")):
        asked = False
        for i, m in enumerate(_ai_turns(s, "any"), 1):
            t = norm(m)
            q, offer = pat.search(t), anchor.search(t)
            if offer and not (asked or (q and q.start() < offer.start())):
                return False, f"session {s['n']} AI message {i}: the save offered before the keep-or-drop question"
            if offer:
                return True, "asked before the first save offer"
            asked = asked or bool(q)
        if not asked:
            return False, f"session {s['n']}: the keep-or-drop question never asked"
    return True, "asked, and no save offered"


def _read_before_save(c, run):
    """build-smoke-1 (2026-11-27): on Claude and ChatGPT Build is the skill creator, and the file the save card
    saves is the last package `package_skill` made, where the stand-in plants its faults. Every AI text that
    offers the save must come after a read of that package (a Bash command naming the .skill file with
    unzip, zipinfo, python…) made after the last packaging and in the same turn (a turn starts at each
    session's init event): a file's contents are never asserted unread. No offer passes; no events.jsonl
    fails closed."""
    read_any, offers = False, 0
    for s in _sessions(run, c.get("session")):
        if not s.get("root"):
            continue
        try:
            lines = (Path(s["root"]).parent / "events.jsonl").read_text(errors="replace").splitlines()
        except OSError:
            continue
        read_any = True
        packaged = read = False
        turn = 0
        for line in lines:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if not isinstance(e, dict):
                continue
            if e.get("type") == "system" and e.get("subtype") == "init":
                turn += 1
                read = False
                continue
            content = (e.get("message") or {}).get("content") if e.get("type") == "assistant" else None
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("name") == "Bash":
                    cmd = str((b.get("input") or {}).get("command") or "")
                    marks = list(PACKAGE_CMD.finditer(cmd))
                    if marks:
                        packaged, read = True, False
                        cmd = cmd[marks[-1].end():]
                    if packaged and PACKAGE_READ.search(cmd):
                        read = True
                elif b.get("type") == "text":
                    m = SAVE_OFFER.search(str(b.get("text") or ""))
                    if not m:
                        continue
                    offers += 1
                    if not packaged:
                        return False, f"session {s['n']} turn {turn}: the save offered with nothing packaged: {m.group(0)[:120]!r}"
                    if not read:
                        return False, (f"session {s['n']} turn {turn}: the save offered with no read of the last "
                                       f"package in this turn: {m.group(0)[:120]!r}")
    if not read_any:
        return False, "no session with an events.jsonl, so the reads can't be told: fails closed"
    return True, (f"{offers} save offer{'s' if offers != 1 else ''}, each after a read of the last package in its turn"
                  if offers else "no save offered")


def _bash_count(c, run):
    """final-build-4c review (2026-11-24): what Build ran, not what the leader read. Passes when the
    session's Bash commands hold the pattern at least `min` times (JR-codex: the workspace listed by
    command before Build's checks and again after them). With `around` (F9, shape release), one match
    must come before the first command matching `around` and one after the last."""
    pat = re.compile(c["pattern"], re.M)
    around = re.compile(c["around"], re.M) if c.get("around") else None
    total, why, cmds_all = 0, "no session with an events.jsonl", []
    for s in _sessions(run, c.get("session")):
        if not s.get("root"):
            continue
        cmds = bash_commands(Path(s["root"]).parent / "events.jsonl")
        if cmds is None:
            continue
        cmds_all += cmds
        total += sum(len(pat.findall(x)) for x in cmds)
        why = f"{total} match{'es' if total != 1 else ''} of {c['pattern']!r} in Bash commands"
    if total < c.get("min", 1) or not around:
        return total >= c.get("min", 1), why
    # F9 (shape release): a listing before the first command matching `around` and after the last
    at = [i for i, x in enumerate(cmds_all) if around.search(x)]
    hits = [i for i, x in enumerate(cmds_all) if pat.search(x)]
    if not at:
        return False, f"no Bash command matches {c['around']!r}"
    if not any(i < at[0] for i in hits):
        return False, f"no {c['pattern']!r} before the first {c['around']!r} command"
    if not any(i > at[-1] for i in hits):
        return False, f"no {c['pattern']!r} after the last {c['around']!r} command"
    return True, why + f", before the first and after the last {c['around']!r} command"


def _tool_write(c, run):
    if c.get("never"):
        return _tool_write_never(c, run)
    pat = re.compile(c["pattern"], re.M)
    then = re.compile(c["before"], re.M) if c.get("before") else None
    why = "no session"
    for s in _sessions(run, c.get("session")):
        if not s.get("root"):
            why = f"session {s['n']}: no events.jsonl to read the writes from"
            continue
        writes = file_writes(Path(s["root"]).parent / "events.jsonl", c["path"])
        if writes is None:
            why = f"session {s['n']}: no events.jsonl to read the writes from"
            continue
        at = next((i for i, (tool, text) in enumerate(writes)
                   if tool != "Bash" and pat.search(norm(text))), None)
        if at is None:
            why = f"session {s['n']}: no Write or Edit to {c['path']} matches {c['pattern']!r}"
            continue
        if not then:
            return True, f"session {s['n']}: write {at + 1} of {len(writes)} to {c['path']}"
        later = [i for i, (_, text) in enumerate(writes) if then.search(norm(text))]
        if any(i < at for i in later):
            why = f"session {s['n']}: a write matching {c['before']!r} came first (write {later[0] + 1})"
            continue
        if not later:
            why = f"session {s['n']}: no write matching {c['before']!r} after it"
            continue
        return True, f"session {s['n']}: write {at + 1}, then write {later[0] + 1} matching {c['before']!r}"
    return False, why


def _saved_before_next_question(c, run):
    """Pass 4 final review M5: an answer the leader gives is written before the next question reaches them.
    The first leader message matching `answer` gives it; a Write or Edit to `path` matching `pattern` must
    come in an AI turn no later than the first AI turn after that message whose text asks something (a "?").
    The turns are told apart by the result event the harness logs at the end of each call; fails closed when
    the answer is never given, nothing matching is written, or the events can't be split into the AI turns."""
    pat, ans = re.compile(c["pattern"], re.M), re.compile(c["answer"], re.M)
    why = "no session"
    for s in _sessions(run, c.get("session")):
        ai_turns, answer_at = [], None
        for turn in s["turns"]:
            if turn["role"] == "ai":
                ai_turns.append(turn["text"])
            elif answer_at is None and ans.search(norm(turn["text"])):
                answer_at = len(ai_turns)  # the AI turn that replies to it
        if answer_at is None:
            why = f"session {s['n']}: no leader message matches {c['answer']!r}"
            continue
        asks = next((i for i in range(answer_at, len(ai_turns)) if "?" in ai_turns[i]), None)
        if asks is None:
            why = f"session {s['n']}: no question after the answer"
            continue
        if not s.get("root"):
            why = f"session {s['n']}: no events.jsonl to read the writes from"
            continue
        try:
            lines = (Path(s["root"]).parent / "events.jsonl").read_text(errors="replace").splitlines()
        except OSError:
            why = f"session {s['n']}: no events.jsonl to read the writes from"
            continue
        k, first = 0, None
        for line in lines:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "result":
                k += 1
                continue
            if first is None and e.get("type") == "assistant":
                for b in (e.get("message") or {}).get("content") or []:
                    if not (isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in ("Write", "Edit", "MultiEdit")):
                        continue
                    inp = b.get("input") or {}
                    fp = str(inp.get("file_path") or "")
                    if not (fnmatch.fnmatch(fp, c["path"]) or fnmatch.fnmatch(fp, "*/" + c["path"])):
                        continue
                    texts = [inp.get("content"), inp.get("new_string")] + [x.get("new_string") for x in inp.get("edits") or []]
                    if any(pat.search(norm(str(x))) for x in texts if x):
                        first = k
                        break
        if k != len(ai_turns):
            why = f"session {s['n']}: {k} result events for {len(ai_turns)} AI turns: the writes can't be placed"
            continue
        if first is None:
            why = f"session {s['n']}: no Write or Edit to {c['path']} matches {c['pattern']!r}"
            continue
        if first > asks:
            why = f"session {s['n']}: written in AI turn {first + 1}, after the question in AI turn {asks + 1}"
            continue
        return True, f"session {s['n']}: written in AI turn {first + 1}, by the question in AI turn {asks + 1}"
    return False, why


def _tool_write_never(c, run):
    """final-build fix (2026-11-22): what a file held while the run went on, for a file the step deletes
    before the end (Build removes its check agents at the close): passes when some session wrote the path
    and no write to it (Write, Edit or a Bash command naming it) matches the pattern."""
    pat = re.compile(c["pattern"], re.M)
    seen = 0
    for s in _sessions(run, c.get("session")):
        if not s.get("root"):
            continue
        writes = file_writes(Path(s["root"]).parent / "events.jsonl", c["path"]) or []
        seen += len(writes)
        for i, (tool, text) in enumerate(writes):
            m = pat.search(norm(text))
            if m:
                return False, f"session {s['n']}: write {i + 1} to {c['path']} ({tool}): {m.group(0)[:120]!r}"
    if not seen:
        return False, f"no write to {c['path']} in any session"
    return True, f"{seen} write{'s' if seen != 1 else ''} to {c['path']}, none matching {c['pattern']!r}"


def script_quotes(script):
    """The text a leader script quotes for the leader to paste ("Your runs" blocks, a planted run's
    block, their real example): a term inside it comes from the script, not the leader."""
    return "\n".join(re.findall(r'"([^"]*)"', script or "", re.S))


def fidelity(run):
    """No framework term in a leader turn before an AI turn used it (word-boundary, case as listed
    for 'AC', case-insensitive otherwise). What the leader's screen showed (a run's answer they paste
    back) and what their script quotes for them to paste count as seen: the leader didn't choose them."""
    for s in run["sessions"]:
        seen_ai = norm(s.get("script_quotes") or "")
        for t in s["turns"]:
            if t["role"] == "ai":
                seen_ai += "\n" + norm(t["text"])
                continue
            if t.get("screen"):
                seen_ai += "\n" + norm(t["screen"])
            if t.get("scripted_reply") or t.get("prompt"):
                continue
            for term in FIDELITY_TERMS:
                flags = 0 if term == "AC" else re.I
                pat = re.compile(rf"\b{re.escape(term)}\b", flags)
                if pat.search(norm(t["text"])) and not pat.search(seen_ai):
                    return False, f"session {s['n']}: leader used {term!r} first: {t['text'][:160]!r}"
    return True, "no framework term used before the AI used it"


# ---------------------------------------------------------------- the stand-in connections' writes
# Review finding 19 (2026-11-21, a condition of James accepting finding 22): the stand-in Slack and HubSpot
# accepted writes the team sees and no check read what was called. Every call that reached a stand-in
# (tools/gmail_stub_mcp.py's log, kept per session by run_eval.py as stub-calls.jsonl) and every
# stand-in call in the session's events.jsonl that wasn't refused is classified here; a write to a place
# other people see fails the Build run (no_team_visible_writes, built in for Build and never skippable).
# What's allowed is Build's quick real check (build references/setup.md section 4): its own call to a
# place only the leader sees: a draft in their own mailbox, a spreadsheet in their own Drive shared with no
# one (and an update to one it made), a post in the private channel only they're in (#build-check, the one
# the stand-in lists) or a message to themselves, and the undo of any of these. A post to any other
# channel fails, even one the stand-in accepts: in a real workspace that name could be a team channel.
STUB_SERVERS = {"gmail": "mail", "outlook": "mail", "google_sheets": "sheets", "slack": "slack", "hubspot": "hubspot"}
STUB_READS = {"get_profile", "list_messages", "get_message", "list_spreadsheets", "read_range", "list_channels",
              "read_channel"}
LEADER_ACCOUNT = "alex@brightline.example"  # harness.stub_spec's default account
PRIVATE_SLACK = {"#build-check"}  # gmail_stub_mcp.PRIVATE_CHANNEL: the leader alone in it
TEAM_SHEET = "sheet-client-tracker"  # gmail_stub_mcp.TRACKER: the team's shared Client Tracker


def _slack_private(channel, account):
    c = str(channel or "").strip().lower()
    local = account.split("@")[0].lower()
    if c in (account.lower(), "@" + account.lower(), "@" + local):
        return True  # a message to themselves
    return (c if c.startswith("#") else "#" + c) in PRIVATE_SLACK


def _as_dict(result):
    if isinstance(result, dict):
        return result
    try:
        out = json.loads(result) if isinstance(result, str) else None
    except ValueError:
        return {}
    return out if isinstance(out, dict) else {}


def stub_write(server, tool, args, account=LEADER_ACCOUNT, own_sheets=()):
    """None for a stand-in read or a write only the leader sees; otherwise where the write lands, in plain
    words (a write other people see). An unknown server, tool or action is a write others see: fail closed."""
    kind = STUB_SERVERS.get(server)
    args = args if isinstance(args, dict) else {}
    if tool in STUB_READS and kind:
        return None
    if kind == "mail":
        if tool in ("create_draft", "delete_draft"):
            return None  # the leader's own Drafts
        if tool == "send_message":
            to = [x.strip().lower() for x in re.split(r"[,;]", str(args.get("to") or "")) if x.strip()]
            if to and all(x == account.lower() for x in to):
                return None  # the permanent form: to the leader's own address only
            return f"an email sent to {args.get('to') or 'no address'}"
    elif kind == "sheets":
        if tool == "create_spreadsheet":
            return None  # in the leader's own Drive, shared with no one
        if tool == "update_range":
            sid = str(args.get("spreadsheetId") or "")
            if sid in own_sheets and sid != TEAM_SHEET:
                return None  # a spreadsheet this run made for the check
            return f"an overwrite of spreadsheet {sid or '(none named)'}, which the team shares"
    elif kind == "slack":
        if tool in ("post_message", "delete_message"):
            ch = args.get("channel")
            if _slack_private(ch, account):
                return None
            verb = "a post to" if tool == "post_message" else "a delete in"
            return f"{verb} Slack channel {ch or '(none named)'}, which other people see"
    elif kind == "hubspot":
        if tool == "manage_crm_objects":
            action = str(args.get("action") or "")
            if action == "read":
                return None
            return f"a CRM {action or 'change'} on {args.get('objectType') or 'a record'}, which the account team sees"
    return f"{tool} on the stand-in {server}, a change not known to stay with the leader"


def _events_stub_calls(path):
    """The stand-in connection calls (mcp__<server>__<tool>) in a session's events.jsonl, with what each
    returned: [{server, tool, args, result, refused}]. A call refused before it reached the connection (a
    deny rule, a permission not given: its result is an error) is marked refused; a call with no result
    (the session was cut off) is not. None when there's no events.jsonl."""
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return None
    calls, order = {}, []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        msg = e.get("message") if isinstance(e, dict) else None
        content = msg.get("content") if isinstance(msg, dict) else None
        for b in content if isinstance(content, list) else []:
            if not isinstance(b, dict):
                continue
            if e.get("type") == "assistant" and b.get("type") == "tool_use":
                m = re.match(r"mcp__([A-Za-z0-9_-]+?)__(.+)$", str(b.get("name") or ""))
                if m and m.group(1) in STUB_SERVERS:
                    calls[b.get("id")] = {"server": m.group(1), "tool": m.group(2), "args": b.get("input") or {},
                                          "result": None, "refused": False}
                    order.append(b.get("id"))
            elif e.get("type") == "user" and b.get("type") == "tool_result" and b.get("tool_use_id") in calls:
                c = b.get("content")
                text = c if isinstance(c, str) else "\n".join(
                    x.get("text", "") for x in c or [] if isinstance(x, dict))
                calls[b["tool_use_id"]].update(result=text, refused=bool(b.get("is_error")))
    return [calls[i] for i in order]


def stub_calls_of(sess):
    """Every stand-in call a session made, from both records: the stand-in's own log (what reached it,
    from any process: run_eval.py keeps the session's share as `stub_calls`) and events.jsonl (the
    session's own calls, those refused before reaching it dropped). None when neither record exists."""
    out, have = [], False
    if sess.get("stub_calls") is not None:
        have = True
        out += [dict(e, refused=False) for e in sess["stub_calls"]]
    if sess.get("root"):
        ev = _events_stub_calls(Path(sess["root"]).parent / "events.jsonl")
        if ev is not None:
            have = True
            out += [e for e in ev if not e["refused"]]
    return out if have else None


def stub_writes(run):
    """Every stand-in call of the run that isn't a read, as [(session, where, call)], `where` None for a
    place only the leader sees; and the sessions with no record of their calls."""
    found, unread, own_sheets = [], [], set()
    for s in run["sessions"]:
        calls = stub_calls_of(s)
        if calls is None:
            unread.append(s["n"])
            continue
        account = s.get("stub_account") or LEADER_ACCOUNT
        seen = set()
        for c in calls:
            if c.get("tool") == "create_spreadsheet":
                sid = _as_dict(c.get("result")).get("spreadsheetId")
                if sid:
                    own_sheets.add(str(sid))
            key = (c.get("server"), c.get("tool"), json.dumps(c.get("args"), sort_keys=True, default=str))
            if key in seen:
                continue
            seen.add(key)
            if c.get("tool") in STUB_READS and c.get("server") in STUB_SERVERS:
                continue
            found.append((s["n"], stub_write(c.get("server"), c.get("tool"), c.get("args"), account, own_sheets), c))
    return found, unread


def team_visible_writes(run):
    """(writes others see, as [(session, where, call)]; sessions with no record of their calls)."""
    found, unread = stub_writes(run)
    return [x for x in found if x[1]], unread


def _no_team_visible_writes(run):
    found, unread = team_visible_writes(run)
    if found:
        return False, "; ".join(f"session {n}: {where} ({c.get('server')} {c.get('tool')} "
                                f"{json.dumps(c.get('args'), ensure_ascii=False, default=str)[:160]})"
                                for n, where, c in found[:4])
    if unread:
        return False, (f"session {', '.join(map(str, unread))}: no record of the connection calls (no stand-in "
                       f"log and no events.jsonl), so what was written can't be told: fails closed")
    return True, "no write to a place other people see"


# ---------------------------------------------------------------- block-quoted output and its source
# Review finding 21 (2026-11-21): the judge was told to pass text quoted (>) as the practice run showed it,
# so a made-up output in a block quote couldn't fail "nothing invented". quoted_output_seen (built in for
# Build) passes only when every block quote the AI shows appears in what the session's tool calls returned
# (a check run's output, a file read, a connection's result), or in what the leader pasted or their screen
# showed (a run on a chat platform reaches the session only that way): compared with whitespace, Markdown
# marks, JSON escapes and case set aside, each part between ellipses on its own; when the whole isn't found
# in one piece (lines left out between, or shown in another order), every line must be found on its own,
# a line's leading label ("Subject:") aside. A changed word is never forgiven: a changed fact is what this
# catches. A quote line that is an approved line said (a carried line shown back) is the step's own wording,
# not output. Parts under QUOTE_MIN_WORDS words are too short to tell apart and aren't judged.
QUOTE_LINE = re.compile(r"^[ \t]*>[ \t]?(.*)$")
QUOTE_FENCE = re.compile(r"```.*?```", re.S)
ELLIPSIS = re.compile(r"\s*(?:\[\s*…\s*\]|…)\s*")
QUOTE_MIN_WORDS = 4
LABEL = re.compile(r"^[\w' -]{1,30}: ")


def block_quotes(message):
    """Each block quote in a message (outside fenced code), as its lines with the > marks taken off."""
    blocks, cur = [], []
    for ln in QUOTE_FENCE.sub("", message or "").splitlines():
        m = QUOTE_LINE.match(ln)
        if m:
            cur.append(re.sub(r"^(?:>[ \t]?)+", "", m.group(1)))
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return [b for b in blocks if any(x.strip() for x in b)]


def quote_norm(text):
    """Text as a quote is compared: JSON escapes read, quote marks alike, Markdown's quote, list, heading,
    bold and code marks dropped, "..." as one ellipsis, whitespace collapsed, lower case."""
    s = str(text or "").replace("\\n", "\n").replace("\\t", " ").replace('\\"', '"').replace("\\'", "'")
    s = qnorm(s).replace("...", "…")
    s = re.sub(r"(?m)^[ \t]*(?:>[ \t]?)+", "", s)
    s = re.sub(r"(?m)^[ \t]*(?:[-*+•]|\d+[.)])[ \t]+", "", s)
    s = re.sub(r"(?m)^[ \t]*#+[ \t]+", "", s)
    s = re.sub(r"\*+|(?<!\w)_+|_+(?!\w)", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def _quote_parts(text):
    parts = [p.strip(" '\"") for p in ELLIPSIS.split(quote_norm(text))]
    return [p for p in parts if len(p.split()) >= QUOTE_MIN_WORDS]


def _approved_line(line):
    """True when a quote line is, for the most part, an approved line said: the step's wording, not output."""
    nl = AL.norm(line)
    if len(nl.split()) < QUOTE_MIN_WORDS:
        return False
    for ln in corpus().checkable():
        if ln.matches(nl):
            m = ln.regex.search(nl)
            if m and (m.end() - m.start()) >= 0.8 * len(nl):
                return True
    return False


def quote_backed(lines, source):
    """True when the quote appears in the source (quote_norm'd), False when it doesn't, None when no part
    of it is long enough to judge."""
    lines = [x for x in lines if not _approved_line(x)]
    parts = _quote_parts("\n".join(lines))
    if not parts:
        return None
    if all(p in source for p in parts):
        return True
    judged = 0
    for x in lines:
        for p in _quote_parts(x):
            judged += len(p)
            if p in source:
                continue
            rest = LABEL.sub("", p, count=1)
            if rest == p or len(rest.split()) < QUOTE_MIN_WORDS or rest not in source:
                return False
    # every line long enough was found; lines all too short to judge alone leave the whole's verdict
    return judged >= 0.5 * sum(len(p) for p in parts)


def session_sources(sess):
    """What a session's quotes may come from: each tool result (the step's own instructions left out: an
    example there is never a run's output) and each leader message and screen. None when the session has
    no events.jsonl to read the tool results from."""
    import grade_eval as G  # here, not at the top: grade_eval imports this module
    if not sess.get("root"):
        return None
    path = Path(sess["root"]).parent / "events.jsonl"
    if not path.exists():
        return None
    out = list(G._tool_results(path))
    for t in sess["turns"]:
        if t["role"] != "ai":
            out += [t.get("text") or "", t.get("screen") or ""]
    return [x for x in out if x]


# final-build fix (2026-11-22): only Claude Code runs Build's checks in a separate session (a check agent or
# a headless session), whose output reaches the main session as a tool result. On every other platform
# Build follows the draft on the input itself, in its own chat (build/SKILL.md, *Where checks run*), so the
# run's output is first written in the AI's own message and no tool result can hold it: a quote there is
# never compared, and the judge is told so (grade_eval.quoted_sources)
SEPARATE_CHECK_PLATFORMS = {"claude-code"}


def separate_checks(session):
    return session.get("platform", "claude-code") in SEPARATE_CHECK_PLATFORMS


def unbacked_quotes(run):
    """([(session, AI message number, first words)] for each block quote no source holds; sessions with
    block quotes and no tool results to compare them with). Sessions on a platform whose checks run in the
    AI's own chat are left out (SEPARATE_CHECK_PLATFORMS)."""
    bad, unread = [], []
    for s in run["sessions"]:
        if not separate_checks(s):
            continue
        quotes = [(i, b) for i, m in enumerate(_ai_turns(s), 1) for b in block_quotes(m)]
        if not quotes:
            continue
        sources = session_sources(s)
        if sources is None:
            unread.append(s["n"])
            continue
        source = "\n".join(quote_norm(x) for x in sources)
        for i, b in quotes:
            if quote_backed(b, source) is False:
                bad.append((s["n"], i, " / ".join(x.strip() for x in b if x.strip())[:140]))
    return bad, unread


def _quoted_output_seen(run):
    bad, unread = unbacked_quotes(run)
    if bad:
        return False, "; ".join(f"session {n} AI message {i}: a block quote found in no tool result: {q!r}"
                                for n, i, q in bad[:4])
    if unread:
        return False, f"session {', '.join(map(str, unread))}: block quotes and no events.jsonl to compare them with"
    return True, "every block quote appears in what the session's tool calls returned or the leader pasted"


# Built in for one skill's runs whatever the evals file says, and never turned off by skip_builtin: each is
# a fail-closed check of what the run really did (review findings 19 and 21, 2026-11-21)
SKILL_BUILTINS = {"build": ("no_team_visible_writes", "quoted_output_seen")}
BUILTIN_TEXT.update({
    "no_team_visible_writes": "No connection call wrote anywhere other people see (only the quick real check's own "
                              "call, to a place only the leader sees, writes at all)",
    "quoted_output_seen": "Every block-quoted output the AI shows appears in what the session's tool calls "
                          "returned (or the leader pasted): nothing quoted is made up",
})


def builtins_for(ev, evals_data=None):
    data = evals_data or {}
    on = list(data.get("builtin_checks", BUILTIN))
    if (ev.get("tier") or data.get("default_tier") or "regression") == "core":
        on += [b for b in data.get("core_builtin_checks", []) if b not in on]
    on = [b for b in on if b not in ev.get("skip_builtin", [])]
    return on + [b for b in SKILL_BUILTINS.get(data.get("skill_name"), ()) if b not in on]


def run_checks(ev, run, evals_data=None):
    # the skill under test (the evals file's skill_name) scopes the quote check's near misses
    run = {**run, "skill": run.get("skill") or (evals_data or {}).get("skill_name")}
    out = []
    for x in ev["expectations"]:
        if x["kind"] != "scripted":
            continue
        ok, why = check(x["check"], run)
        out.append({"text": x["text"], "kind": "scripted", "passed": bool(ok), "evidence": why,
                    **{k: x[k] for k in ("must", "gating") if k in x}})
    for b in builtins_for(ev, evals_data):
        ok, why = check({"type": b}, run)
        out.append({"text": BUILTIN_TEXT[b], "kind": "scripted", "passed": bool(ok), "evidence": why,
                    "builtin": b})
    return out


def load_tree(folder):
    """Every text file under a folder, as {relative path: text}."""
    folder = Path(folder)
    files = {}
    if folder.exists():
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                try:
                    files[str(p.relative_to(folder))] = p.read_text(errors="replace")
                except OSError:
                    files[str(p.relative_to(folder))] = ""
    return files
