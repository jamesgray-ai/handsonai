#!/usr/bin/env python3
"""Scripted checks: the expectations a program can decide, so no LLM judges them.

Each `scripted` expectation in an evals.json carries a `check` object. Check types:

  ai_contains      {text, session?, turn?: first|any|all|last}   an AI message contains the text
  ai_not_contains  {text, session?}                               no AI message contains it
  ai_regex         {pattern, session?, turn?}                     an AI message matches
  ai_not_regex     {pattern, session?}                            no AI message matches
  signposts        {session?}                                     "Part 1 of 5" … "Part 5 of 5", in order
  file_exists      {path, session?}                               a file matching the glob exists at session end
  file_absent      {path, session?}                               no file matches at session end
  file_existed_during {path, session?}                            a match existed after some turn of the session
  file_contains    {path, text, session?}                         a matching file contains the text
  file_not_contains {path, text, session?}
  file_regex       {path, pattern, session?}                      a matching file matches (multiline)
  file_not_regex   {path, pattern, session?}
  sections_in_order {path, headings: [...], only?: bool, session?} the `#`/`##` headings appear in this
                                                                  order (only: no other `##` headings)
  no_yaml          {path, session?}                               the file does not open with `---`
  file_unchanged   {path, session?}                               every matching file is byte-identical
                                                                  at session start and end
  file_line        {path, line: n, pattern, session?}             line n (1-based) matches the pattern
  no_added_files   {except?: [globs], session?}                   no file was added during the session,
                                                                  except paths matching the globs
  all              {checks: [...]}                                every sub-check passes
  any              {checks: [...]}                                at least one passes

`session` is 1-based; leave it out to mean every session (AI checks) or the last session (file checks).
Text matching ignores differences in curly versus straight quotes and dashes.

Built-in checks the runner adds to every interview run: the fidelity check (no listed framework
term in a student turn before an AI turn used it) and the turn cap.
"""
import fnmatch
import hashlib
import re
from pathlib import Path

FIDELITY_TERMS = ["acceptance criterion", "acceptance criteria", "AC", "fixed step", "flexible step",
                  "human gate", "context", "Context Inventory", "Design Plan", "autonomy",
                  "Deterministic", "Guided", "Autonomous", "requirements", "Golden Example"]


def norm(s):
    return (s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
             .replace("—", "-").replace("–", "-").replace(" ", " "))


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


def check(c, run):
    """Return (passed, evidence)."""
    t = c["type"]
    n = c.get("session")
    if t in ("ai_contains", "ai_regex"):
        which = c.get("turn", "any")
        for s in _sessions(run, n):
            msgs = _ai_turns(s, "any" if which == "all" else which)
            if t == "ai_contains":
                hits = [norm(c["text"]) in norm(m) for m in msgs]
            else:
                hits = [bool(re.search(c["pattern"], norm(m), re.M)) for m in msgs]
            ok = all(hits) and hits if which == "all" else any(hits)
            if ok:
                return True, f"found in session {s['n']}"
        return False, "not found in any AI message" + (" (first message)" if which == "first" else "")
    if t in ("ai_not_contains", "ai_not_regex"):
        for s in _sessions(run, n):
            for i, m in enumerate(_ai_turns(s)):
                hit = (norm(c["text"]) in norm(m)) if t == "ai_not_contains" else re.search(c["pattern"], norm(m), re.M)
                if hit:
                    return False, f"session {s['n']} AI message {i + 1}: {m[:200]!r}"
        return True, "absent from every AI message"
    if t == "signposts":
        for s in _sessions(run, n):
            text = norm("\n".join(_ai_turns(s)))
            pos, ok = 0, True
            for k in range(1, 6):
                j = text.find(f"Part {k} of 5", pos)
                if j < 0:
                    ok = False
                    missing = k
                    break
                pos = j
            if ok:
                return True, f"Parts 1-5 signposted in order (session {s['n']})"
        return False, f"'Part {missing} of 5' missing or out of order"
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
        return (bool(re.search(c["pattern"], nb, re.M)), f"{path}")
    if t == "file_not_regex":
        m = re.search(c["pattern"], nb, re.M)
        return (not m, f"{path}" + (f": {m.group(0)[:120]!r}" if m else ""))
    if t == "no_yaml":
        return (not body.lstrip("﻿").startswith("---"), f"{path}")
    if t == "file_line":
        lines = body.splitlines()
        k = c["line"] - 1
        got = lines[k] if k < len(lines) else ""
        return (bool(re.search(c["pattern"], norm(got))), f"line {c['line']}: {got[:160]!r}")
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
    """No framework term in a student turn before an AI turn used it (word-boundary, case as listed
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
                    return False, f"session {s['n']}: student used {term!r} first: {t['text'][:160]!r}"
    return True, "no framework term used before the AI used it"


def run_checks(ev, run):
    out = []
    for x in ev["expectations"]:
        if x["kind"] != "scripted":
            continue
        ok, why = check(x["check"], run)
        out.append({"text": x["text"], "kind": "scripted", "passed": bool(ok), "evidence": why,
                    **{k: x[k] for k in ("must", "gating") if k in x}})
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
