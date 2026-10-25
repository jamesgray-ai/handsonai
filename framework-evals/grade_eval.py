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
    return out


def rubric_prompt(run):
    """Each AI message, with what the leader said just before it as context (not graded), so
    item 6 can tell a fact the leader gave from an invented one."""
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
    return msgs, f"Grade each of these {len(msgs)} messages on the rubric.\n\n{body}"


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
