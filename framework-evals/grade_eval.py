#!/usr/bin/env python3
"""The graders, each one blind `claude -p` call per run, called by run_eval.py.

- `grade`: the eval's own `judged` expectations, its preconditions and (for runs with a simulated
  leader) the judged fidelity check, from each session's transcript and every file the session
  added, changed or removed, in full (no truncation). `scripted` expectations are check_scripted.py's.
- `grade_rubric`: the judge rubric (rules 2.4; prompts/judge-rubric.md) on every unscripted AI
  message. Approved lines are marked ⟦…⟧ so only model wording is judged on its words. Each of the
  nine items becomes one expectation that passes when every message passes it.

Graders run from the run root's empty grader/ folder with no plugin and no tools, so each sees only
what its prompt gives it, and must return exactly one result per item, in order.
"""
import json
import re
from pathlib import Path

import approved_lines as AL
import harness as H

HERE = Path(__file__).resolve().parent
RUBRIC_PROMPT = HERE / "prompts" / "judge-rubric.md"
RUBRIC_ITEMS = ["Plain words: nothing from the Never column", "At most one question (or a listed exception)",
                "Ends with a question or a clear next action", "No framework step number and no time estimate",
                "Names the real thing; says what's known before asking", "Nothing invented",
                "No requirement or task ID outside an approved line", "Any start phrase exact, with the location",
                "Short: acknowledgements a few words, playbacks in plain words"]

GRADER = """You grade a test run of an AI skill against a checklist. Be strict and literal:
an item that quotes wording passes only if that wording appears (small punctuation
differences aside). An item about a file passes only if the file shows it. If the run
stopped before the point an item is about, mark it failed with evidence "not reached".
A precondition item reads "when the AI gave the cue, the student did X": if the AI never
gave the cue, it passes with evidence "cue not given".
Return only JSON: {"results": [{"n": 1, "passed": true|false, "evidence": "..."}]},
one entry per numbered item, in the order given, quoting evidence briefly."""

FIDELITY_ITEM = ("Fidelity (precondition): every fact the leader gave appears in or follows from the "
                 "leader's script; the leader invented nothing outside it")


def items_for(ev):
    items = [{"text": x["text"], "kind": "judged", **{k: x[k] for k in ("must", "gating") if k in x}}
             for x in ev["expectations"] if x["kind"] == "judged"]
    items += [{"text": p, "kind": "judged", "precondition": True} for p in ev.get("preconditions", [])]
    if ev.get("student") or any(isinstance(s.get("student"), str) for s in ev.get("sessions", [])):
        items.append({"text": FIDELITY_ITEM, "kind": "judged", "precondition": True})
    return items


def build_prompt(ev, run, items, script):
    parts = [f"# Eval {ev['id']} — {ev.get('name', '')}", "", f"Expected: {ev.get('expected_output', '')}", ""]
    if script:
        parts += ["## The leader's script (for the fidelity item only)", "", script, ""]
    parts += ["## Items to grade", ""]
    parts += [f"{i}. {x['text']}" for i, x in enumerate(items, 1)]
    for s in run["sessions"]:
        parts += ["", f"# Session {s['n']}", "", "## Transcript", ""]
        for t in s["turns"]:
            parts += [f"### {'AI' if t['role'] == 'ai' else 'Leader'}", "", t["text"], ""]
        if s["cap_hit"]:
            parts += ["(The run stopped at the turn cap.)", ""]
        parts += ["## Files the session touched", ""]
        for rel in sorted(set(s["files_start"]) | set(s["files_end"])):
            a, b = s["files_start"].get(rel), s["files_end"].get(rel)
            if a == b:
                continue
            kind = "added" if a is None else "removed" if b is None else "changed"
            parts += [f"### {kind}: {rel}", "", "````", b or "", "````", ""]
    return "\n".join(parts)


def _call_json(rnd, root, prompt, system, key, n_expected):
    res = None
    for _ in range(2):
        text, rec = H.call(rnd, "grader", root, prompt, cwd=root / "grader", tools=[], system_prompt=system)
        m = re.search(r"\{.*\}", text, re.S)
        try:
            res = json.loads(m.group(0))[key] if m else None
        except (ValueError, KeyError):
            res = None
        if res is not None and len(res) == n_expected and [r.get("n") for r in res] == list(range(1, n_expected + 1)):
            rec["role"] = "grader"
            return res, rec
    raise H.HarnessFailure(f"grader returned {len(res) if res else 'no'} results for {n_expected} items")


def grade(rnd, root, ev, run, evals_dir=None):
    """Returns (judged results, call record or None)."""
    items = items_for(ev)
    if not items:
        return [], None
    base = Path(evals_dir) if evals_dir else HERE
    paths = [ev["student"]] if ev.get("student") else []
    paths += [s["student"] for s in ev.get("sessions", []) if isinstance(s.get("student"), str)]
    script = "\n\n---\n\n".join((base / p).read_text() for p in dict.fromkeys(paths) if (base / p).exists()) or None
    res, rec = _call_json(rnd, root, build_prompt(ev, run, items, script), GRADER, "results", len(items))
    return [{**x, "passed": bool(r.get("passed")), "evidence": r.get("evidence", "")} for x, r in zip(items, res)], rec


def mark_scripted(message, corpus=None):
    """The message with each approved line it says wrapped in ⟦…⟧."""
    corpus = corpus or AL.load()
    out = AL.norm(message)
    low = out.lower()
    for ln in corpus.checkable():
        segs = [AL.norm(x) for x in AL.literal_segments(ln.toks)]
        longest = max(segs, key=len, default="")
        if len(longest.split()) < 4 or longest.lower() not in low:
            continue
        out = ln.regex.sub(lambda m: "⟦" + m.group(0) + "⟧", out)
        low = out.lower()
    # norm drops backticks; put back the message's code-formatted names (`context/C1-call-notes.md`)
    # so the judge can apply item 7's file-name exemption
    for span in dict.fromkeys(re.findall(r"`([^`\n]+)`", message)):
        n = AL.norm(span)
        if n and f"`{n}`" not in out:
            out = re.sub(r"(?<![\w/.-])" + re.escape(n) + r"(?![\w/-])", lambda m: f"`{m.group(0)}`", out)
    return out


READ_CAP = 7000  # characters of the leader's files shown to the rubric judge, in all
READ_FILE_CAP = 2500


def _tool_results(events_path):
    """The text of every tool result in a session's events.jsonl, Read's line-number prefixes removed."""
    out = []
    try:
        lines = Path(events_path).read_text(errors="replace").splitlines()
    except OSError:
        return out
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        content = (e.get("message") or {}).get("content") if e.get("type") == "user" else None
        for b in content if isinstance(content, list) else []:
            if not isinstance(b, dict) or b.get("type") != "tool_result":
                continue
            c = b.get("content")
            text = c if isinstance(c, str) else "\n".join(
                x.get("text", "") for x in c or [] if isinstance(x, dict))
            out.append(re.sub(r"(?m)^\s*\d+\t", "", text))
    return out


def _read_rank(rel):
    if "/workflows/" in f"/{rel}" and not rel.endswith("index.md"):
        return 0
    if rel.endswith(("requirements.md", "design-plan.md")):  # the plan's changes: back what Build says
        return 1
    if "opportunity-report" in rel or "backlog" in rel:
        return 2
    return 3 if "registry/" in rel and not rel.endswith(("index.md", "log.md")) else 4


def files_read(run):
    """The leader's files the AI read during the run, as they were before the session (so nothing
    the AI wrote itself), most relevant first: workflow nodes, requirements and plan, the backlog, the rest.
    A file counts as read when its longer lines appear in a tool result (a Read, or a cat in Bash,
    on any folder: drive/, onedrive/ or the workspace itself). Capped at READ_CAP characters."""
    found = {}
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        results = "\n".join(_tool_results(Path(s["root"]).parent / "events.jsonl"))
        if not results:
            continue
        for rel, text in s["files_start"].items():
            if rel in found or rel.startswith(".") or "/." in rel or not text.strip():
                continue
            long_lines = [ln.strip() for ln in text.splitlines() if len(ln.strip()) >= 30]
            if long_lines and sum(ln in results for ln in long_lines) >= min(2, len(long_lines)):
                found[rel] = text
    parts, total = [], 0
    for rel in sorted(found, key=lambda r: (_read_rank(r), r)):
        body = found[rel].strip()
        body = body if len(body) <= READ_FILE_CAP else body[:READ_FILE_CAP] + "\n[…cut]"
        if total + len(body) > READ_CAP:
            continue
        parts.append(f"### {rel}\n\n````\n{body}\n````")
        total += len(body)
    return "\n\n".join(parts)


FACT = re.compile(r"[\w.+-]*\d[\w.+-]*|[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
TOOL_LINES_CAP = 1500


def tool_lines(run, msgs):
    """Lines of the AI's own tool output (a version a command printed, an address a connection
    returned) that hold a figure or address its messages give, so item 6 doesn't take a fact the AI
    looked up for an invented one. Only lines with such a token; capped at TOOL_LINES_CAP characters."""
    facts = {f.strip(".,") for m in msgs for f in FACT.findall(m) if len(f.strip(".,")) >= 3}
    if not facts:
        return ""
    out, total = [], 0
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for res in _tool_results(Path(s["root"]).parent / "events.jsonl"):
            for ln in res.splitlines():
                ln = ln.strip()[:200]
                if ln and ln not in out and any(f in ln for f in facts) and total + len(ln) <= TOOL_LINES_CAP:
                    out.append(ln)
                    total += len(ln)
    return "\n".join(out)


WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
SHARED_RUN = 4  # consecutive words a tool-output passage must share with a message
SHARED_LINES_CAP = 1500
SHARED_LINE_LEN = 300


def _grams(text):
    w = WORD.findall(text.lower().replace("’", "'"))
    return {tuple(w[i:i + SHARED_RUN]) for i in range(len(w) - SHARED_RUN + 1)}


def shared_lines(run, msgs, skip=""):
    """Passages of the AI's own tool output (a file it read, a plugin reference file, a fetched
    page, a command's output) that share a run of SHARED_RUN or more consecutive words with the
    unscripted part of its messages, so item 6 doesn't take a fact the AI read for an invented one.
    Long lines (a JSON registry's notes) are cut into sentences first. Most shared runs first;
    capped at SHARED_LINES_CAP characters; passages already in `skip` aren't repeated."""
    grams = set()
    for m in msgs:
        grams |= _grams(re.sub(r"⟦[^⟧]*⟧", " ", m))
    if not grams:
        return ""
    found = {}
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for res in _tool_results(Path(s["root"]).parent / "events.jsonl"):
            for seg in re.split(r"(?<=[.;!?])\s+|\n|\\n", res):
                seg = seg.strip()
                if not seg or seg in found:
                    continue
                n = len(_grams(seg) & grams)
                if n:
                    found[seg] = n
    out, total = [], 0
    for seg in sorted(found, key=lambda x: -found[x]):
        ln = seg[:SHARED_LINE_LEN]
        if ln in skip or ln in out or total + len(ln) > SHARED_LINES_CAP:
            continue
        out.append(ln)
        total += len(ln)
    return "\n".join(out)


def rubric_prompt(run):
    """Each AI message, with what the leader said just before it as context (not graded), so
    item 6 can tell a fact the leader gave from an invented one; and, once at the top, what the AI
    read from the leader's files (context, not graded), so a detail taken from them isn't invented."""
    msgs, said = [], []
    for s in run["sessions"]:
        before = []
        for t in s["turns"]:
            if t["role"] == "ai" and t["text"].strip():
                msgs.append(mark_scripted(t["text"]))
                said.append("\n\n".join(before))
                before = []
            elif t["role"] != "ai" and t["text"].strip() and not t.get("end"):
                before.append(t["text"].strip())
    def block(i, m, ctx):
        quoted = "\n".join("> " + ln for ln in ctx.splitlines()) if ctx else "> (nothing)"
        return f"## Message {i}\n\nThe leader said just before (context, not graded):\n\n{quoted}\n\nThe message:\n\n{m}"
    body = "\n\n".join(block(i, m, c) for i, (m, c) in enumerate(zip(msgs, said), 1))
    read = files_read(run)
    read = (f"## What the AI read from the leader's files (context, not graded)\n\n{read}\n\n"
            if read else "")
    tools = tool_lines(run, msgs)
    shared = shared_lines(run, msgs, tools)
    tools = "\n".join(x for x in (tools, shared) if x)
    read +=(f"## Lines the AI's own tool calls printed (context, not graded)\n\n````\n{tools}\n````\n\n"
             if tools else "")
    return msgs, f"Grade each of these {len(msgs)} messages on the rubric.\n\n{read}{body}"


def grade_rubric(rnd, root, ev, run):
    """Returns (nine expectations, call record or None)."""
    msgs, prompt = rubric_prompt(run)
    if not msgs:
        return [], None
    res, rec = _call_json(rnd, root, prompt, RUBRIC_PROMPT.read_text(), "messages", len(msgs))
    out = []
    for k, name in enumerate(RUBRIC_ITEMS, 1):
        fails = [r for r in res if k in (r.get("fail") or [])]
        out.append({"text": f"Judge rubric {k}: {name} (every unscripted message)", "kind": "judged", "rubric": k,
                    "passed": not fails,
                    "evidence": "; ".join(f"message {r['n']}: {r.get('evidence', '')}" for r in fails)[:600]
                    or f"all {len(msgs)} messages pass"})
    return out, rec
