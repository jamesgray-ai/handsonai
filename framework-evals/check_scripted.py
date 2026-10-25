#!/usr/bin/env python3
"""Scripted checks: the expectations a program can decide, so no model judges them.

Each `scripted` expectation in an evals.json carries a `check` object. Check types:

  ai_contains      {text, session?, turn?: first|any|all|last, line?}  an AI message contains the text
                                                                  (`line`: the approved line it quotes)
  ai_not_contains  {text, session?}                               no AI message contains it
  ai_regex         {pattern, session?, turn?}                     an AI message matches
  ai_not_regex     {pattern, session?}                            no AI message matches
  quote            {id, form?, session?, turn?, ending?}          an AI message says that approved line
                                                                  (approved-lines.json), placeholders filled;
                                                                  `ending`: a fragment form of the same line
                                                                  ("…, keeping…"): the line said with it in
                                                                  place of its closing mark
  quote_absent     {id, form?, session?}                          no AI message says it
  scripted_lines   {session?}                                     every scripted line said is word for word
                                                                  (the quote check; built in)
  vocabulary       {session?}                                     no word from rules 2.2's Never column in
                                                                  what the leader reads (built in)
  no_time_or_step_numbers {session?}                              no time estimate and no framework step
                                                                  number (rules 2.1 items 4-5; built in); a size
                                                                  the leader gave for their own work ("about
                                                                  20 minutes per follow-up") may be played back
  signposts        {skill?, of?, session?}                        the skill's "Part k of N" signposts, in
                                                                  order: deconstruct 5 (default), design 4,
                                                                  test 4, build 3; `of` for a later entry
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
  file_unchanged   {path, session?}                               every matching file is byte-identical
                                                                  at session start and end
  file_line        {path, line: n, pattern, session?}             line n (1-based) matches the pattern
  section_regex    {path, section, pattern, must?: bool}          inside one section, the pattern matches
                                                                  (must=true, default) or doesn't
  no_added_files   {except?: [globs], session?}                   no file was added during the session: the
                                                                  end tree against the session's start tree
                                                                  (the fixture's own files)
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
"""
import fnmatch
import hashlib
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
                  r"\s+minutes?\b|\bhalf an hour\b|\b(?:an|one) hour\b|\btakes? (?:about|around|roughly|under|less than)\b")
STEP_NAMES = r"(?:Analyze|Deconstruct|Design|Build|Test)"
STEP_NUMBER = re.compile(
    rf"\b[Ss]tep\s+[1-5]\b\s*(?:\(\s*{STEP_NAMES}|of\s+(?:the\s+)?(?:AI\s+Workflow\s+)?[Ff]ramework|of\s+5\b|[-:]\s*{STEP_NAMES}\b)"
    rf"|\b{STEP_NAMES}\s*\(\s*[Ss]tep\s*[1-5]\s*\)"
    rf"|\b[Ss]tep\s+[1-5]\s+(?:is|was|will be)\s+{STEP_NAMES}\b"
    rf"|\b{STEP_NAMES}\s+is\s+(?:[Ss]tep\s+[1-5]|the\s+(?:first|second|third|fourth|fifth)\s+step)\b"
    rf"|\b(?:first|second|third|fourth|fifth)\s+step\s+of\s+the\s+(?:AI\s+Workflow\s+)?[Ff]ramework\b")

SIGNPOST_IDS = {"deconstruct": (5, ["deconstruct:signpost-part-1", "deconstruct:signpost-part-2",
                                    "deconstruct:signpost-part-3", "deconstruct:signpost-part-4", "N-D9"]),
                "design": (4, ["N-0"]), "test": (4, ["N-T1"]), "build": (3, ["N-B1"])}
BUILTIN = ("scripted_lines", "vocabulary", "no_time_or_step_numbers")
BUILTIN_TEXT = {"scripted_lines": "Every scripted line the AI says is the approved line, word for word (the quote check)",
                "vocabulary": "No word from the vocabulary's Never column in anything the leader reads",
                "no_time_or_step_numbers": "No time estimate and no framework step number in anything the leader reads"}


def norm(s):
    return (s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
             .replace("—", "-").replace("–", "-").replace(" ", " "))


def qnorm(s):
    """norm, plus single and double quote marks treated alike, for word-for-word text checks."""
    return norm(s).replace('"', "'")


def corpus():
    return AL.load()


def _sessions(run, n):
    return [run["sessions"][n - 1]] if n else run["sessions"]


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
    return run["sessions"][(n or len(run["sessions"])) - 1]


def leader_text(message):
    """What the leader reads, for the wording checks: code blocks and inline code left out
    (file names, prompts to paste), since those are technical text, not wording; block-quoted
    lines too, since those show the leader's work back (an input drafted or pasted), not the AI's wording."""
    m = re.sub(r"```.*?```", " ", message, flags=re.S)
    m = re.sub(r"(?m)^[ \t]*>.*$", " ", m)
    return re.sub(r"`[^`\n]*`", " ", m)


# ---------------------------------------------------------------- wording checks

def vocabulary_hits(message):
    text = corpus().strip_approved(leader_text(message))
    hits = []
    for name, rx in NEVER:
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
                  r"(?:\s*(?:-|to)\s*(\d+(?:\.\d+)?))?\s*-?\s*(minute|min|hour|hr|second|sec)s?\b")


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
    """What the leader said about their own work's size, in any session, or wrote in a requirements
    file's Value & Measurement (the Baseline and Target): playing it back is allowed (the framework
    never estimates time, but those are the leader's numbers)."""
    said = [sizes(t["text"]) for s in run["sessions"] for t in s["turns"] if t["role"] != "ai"]
    written = [sizes(ST.section(body, "Value & Measurement")) for s in run["sessions"]
               for snap in (s.get("files_start") or {}, s.get("files_end") or {})
               for p, body in snap.items() if p.endswith("requirements.md") and isinstance(body, str)]
    return set().union(*said, *written)


def time_or_step_hits(message, allowed=frozenset()):
    # what fills an approved line's placeholder ("about [hours] saved") is part of that line here;
    # a size the leader gave for their own work ("about 20 minutes per follow-up") is theirs, not an estimate
    text = corpus().strip_approved(leader_text(message), keep_fills=False)
    hits = [("time", text[max(0, m.start() - 40):m.end() + 40].strip()) for m in TIME.finditer(text)
            if not (sizes(text[m.start():m.end() + 25]) and sizes(text[m.start():m.end() + 25]) <= allowed)]
    hits += [("step number", text[max(0, m.start() - 40):m.end() + 40].strip()) for m in STEP_NUMBER.finditer(text)]
    return hits


def quote_hits(message, skill=None):
    """Near misses of approved lines; with `skill`, only that skill's lines (and the built
    workflow's) count, so a common phrase another step's line happens to share isn't flagged."""
    return [(ln.label(), exp, got) for ln, exp, got in corpus().near_misses(message, skill=skill)]


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
            probs.append(f"folder Framework/{g['folder']} != Framework/{expect['folder']}")
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
        task = re.search(r"matches task (\S+) of design-plan\.md in my OneDrive, in Framework/([^\s.]+)", nm)
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
        # the default finds the plan wherever the platform keeps the framework folder
        # (framework/, Framework/, drive/Framework/, onedrive/Framework/), never a set-aside copy
        plans = {p: v for p, v in _files(sess, c.get("plan", "*ramework/*/design-plan.md")).items()
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


# ---------------------------------------------------------------- dispatch

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
        for s in _sessions(run, n):
            for i, m in enumerate(_ai_turns(s)):
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
            for i, m in enumerate(_ai_turns(s, which), 1):
                hit = next((f for f in forms if f.matches(m)), None)
                if hit:
                    if t == "quote":
                        return True, f"{hit.label()} in session {s['n']} AI message {i}"
                    return False, f"{hit.label()} said in session {s['n']} AI message {i}"
        return (False, f"{c['id']} not said word for word") if t == "quote" else (True, f"{c['id']} not said")
    if t == "scripted_lines":
        skill = c.get("skill") or run.get("skill")
        return _scan(run, n, lambda m: quote_hits(m, skill), "scripted line said with words changed")
    if t == "vocabulary":
        return _scan(run, n, vocabulary_hits, "Never-column word")
    if t == "no_time_or_step_numbers":
        allowed = leader_sizes(run)
        return _scan(run, n, lambda m: time_or_step_hits(m, allowed), "time estimate or step number")
    if t == "signposts":
        skill = c.get("skill", "deconstruct")
        total, ids = SIGNPOST_IDS[skill]
        total = c.get("of", total)
        want = []
        for lid in ids:
            want += [f.text for f in corpus().get(lid) if f.text and re.match(r"Part \d of \d", f.text)]
        want = [w for w in want if re.match(rf"Part \d of {total}\b", w)] or [f"Part {k} of {total}" for k in range(1, total + 1)]
        missing = want[0]
        for s in _sessions(run, n):
            text = AL.norm("\n".join(_ai_turns(s)))
            pos, ok = 0, True
            for w in want:
                j = text.find(AL.norm(w).rstrip("."), pos)
                if j < 0:
                    ok, missing = False, w
                    break
                pos = j
            if ok:
                return True, f"{skill}'s {len(want)} signposts in order (session {s['n']})"
        return False, f"{missing!r} missing or out of order"
    if t == "fill_check":
        return _fill_check(c, run)
    if t == "file_existed_during":
        for s in _sessions(run, n):
            for i, turn_files in enumerate(s["files_by_turn"]):
                if any(fnmatch.fnmatch(p, c["path"]) for p in turn_files):
                    return True, f"present after AI turn {i + 1} of session {s['n']}"
        return False, f"{c['path']} never present after any turn"
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


def fidelity(run):
    """No framework term in a leader turn before an AI turn used it (word-boundary, case as listed
    for 'AC', case-insensitive otherwise)."""
    for s in run["sessions"]:
        seen_ai = ""
        for t in s["turns"]:
            if t["role"] == "ai":
                seen_ai += "\n" + norm(t["text"])
                continue
            if t.get("scripted_reply") or t.get("prompt"):
                continue
            for term in FIDELITY_TERMS:
                flags = 0 if term == "AC" else re.I
                pat = re.compile(rf"\b{re.escape(term)}\b", flags)
                if pat.search(norm(t["text"])) and not pat.search(seen_ai):
                    return False, f"session {s['n']}: leader used {term!r} first: {t['text'][:160]!r}"
    return True, "no framework term used before the AI used it"


def builtins_for(ev, evals_data=None):
    on = list((evals_data or {}).get("builtin_checks", BUILTIN))
    return [b for b in on if b not in ev.get("skip_builtin", [])]


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
