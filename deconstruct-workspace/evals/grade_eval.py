#!/usr/bin/env python3
"""The judged grader: one blind `claude -p` call per run, called by run_eval.py.

It marks only `judged` expectations, the eval's preconditions, and (for interview evals) the
judged fidelity check, from each session's transcript and every file the session added,
changed or removed, in full (no truncation). `scripted` expectations are check_scripted.py's.
The grader runs from the run root's empty grader/ folder with no plugin and no tools, so it
sees only what this prompt gives it. It must return exactly one result per item, in order.
"""
import json
import re

import harness as H

GRADER = """You grade a test run of an AI skill against a checklist. Be strict and literal:
an item that quotes wording passes only if that wording appears (small punctuation
differences aside). An item about a file passes only if the file shows it. If the run
stopped before the point an item is about, mark it failed with evidence "not reached".
A precondition item reads "when the AI gave the cue, the student did X": if the AI never
gave the cue, it passes with evidence "cue not given".
Return only JSON: {"results": [{"n": 1, "passed": true|false, "evidence": "..."}]},
one entry per numbered item, in the order given, quoting evidence briefly."""

FIDELITY_ITEM = ("Fidelity (precondition): every fact the student gave appears in or follows from the "
                 "student's script; the student invented nothing outside it")


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
        parts += ["## The student's script (for the fidelity item only)", "", script, ""]
    parts += ["## Items to grade", ""]
    parts += [f"{i}. {x['text']}" for i, x in enumerate(items, 1)]
    for s in run["sessions"]:
        parts += ["", f"# Session {s['n']}", "", "## Transcript", ""]
        for t in s["turns"]:
            parts += [f"### {'AI' if t['role'] == 'ai' else 'Student'}", "", t["text"], ""]
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


def grade(rnd, root, ev, run, evals_dir=None):
    """Returns (judged results, call record or None)."""
    items = items_for(ev)
    if not items:
        return [], None
    from pathlib import Path
    base = Path(evals_dir) if evals_dir else Path(__file__).resolve().parent
    paths = [ev["student"]] if ev.get("student") else []
    paths += [s["student"] for s in ev.get("sessions", []) if isinstance(s.get("student"), str)]
    script = "\n\n---\n\n".join((base / p).read_text() for p in dict.fromkeys(paths) if (base / p).exists()) or None
    prompt = build_prompt(ev, run, items, script)
    for attempt in range(2):
        text, rec = H.call(rnd, "grader", root, prompt, cwd=root / "grader", tools=[], system_prompt=GRADER)
        m = re.search(r"\{.*\}", text, re.S)
        try:
            res = json.loads(m.group(0))["results"] if m else None
        except (ValueError, KeyError):
            res = None
        if res is not None and len(res) == len(items) and [r.get("n") for r in res] == list(range(1, len(items) + 1)):
            break
    else:
        raise H.HarnessFailure(f"grader returned {len(res) if res else 'no'} results for {len(items)} items")
    out = []
    for x, r in zip(items, res):
        out.append({**x, "passed": bool(r.get("passed")), "evidence": r.get("evidence", "")})
    rec["role"] = "grader"
    return out, rec
