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


FENCE = re.compile(r"```[^\n`]*\n?(.*?)```", re.S)
EDGE_HOLE = r"[^.!?]*?"  # a fill at a line's start or end: within its own sentence


def _mark_regex(ln):
    """The line's regex for marking: a fill at its very start or end is matched within its sentence,
    so the marker holds the fill without running back to the message's start."""
    rx = getattr(ln, "_mark_rx", None)
    if rx is None:
        toks = ln.toks
        head = EDGE_HOLE if toks and toks[0][0] == "hole" else ""
        tail = r"[^.!?]*[.!?]?" if len(toks) > 1 and toks[-1][0] == "hole" else ""
        core = toks[1 if head else 0:len(toks) - (1 if tail else 0)]
        rx = ln._mark_rx = re.compile(head + AL.to_regex(core) + tail, re.S | re.I)
    return rx


def _mark_text(text, corpus):
    """Normalised text with every approved line said in it wrapped once in ⟦…⟧. Spans are found on
    the unmarked text and merged, so a shorter line said inside a longer one ("Build the agent
    described in task" in the build prompt) never splits the longer line's marker and leaves its
    fills ("T2 of design-plan.md") outside it."""
    out = AL.norm(text)
    low = out.lower()
    spans = []
    for ln in corpus.checkable():
        segs = [AL.norm(x) for x in AL.literal_segments(ln.toks)]
        longest = max(segs, key=len, default="")
        if len(longest.split()) < 4 or longest.lower() not in low:
            continue
        for m in _mark_regex(ln).finditer(out):
            s, e = m.start(), m.end()
            while s < e and out[s] == " ":
                s += 1
            if e > s:
                spans.append([s, e])
    merged = []
    for s, e in sorted(spans):
        if merged and s < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    for s, e in reversed(merged):
        out = out[:s] + "⟦" + out[s:e] + "⟧" + out[e:]
    return out


def mark_scripted(message, corpus=None):
    """The message with each approved line it says wrapped in ⟦…⟧. A fenced code block (a prompt the
    leader pastes into a platform) stays fenced, so the judge can tell it from the message's wording."""
    corpus = corpus or AL.load()
    parts, at = [], 0
    for m in FENCE.finditer(message):
        parts.append(_mark_text(message[at:m.start()], corpus))
        parts.append("\n```\n" + _mark_text(m.group(1), corpus) + "\n```\n")
        at = m.end()
    parts.append(_mark_text(message[at:], corpus))
    out = " ".join(p for p in parts if p.strip()).strip()
    # norm drops backticks; put back the message's code-formatted names (`context/C1-call-notes.md`)
    # so the judge can apply item 7's file-name exemption
    for span in dict.fromkeys(re.findall(r"`([^`\n]+)`", message)):
        n = AL.norm(span)
        if n and f"`{n}`" not in out:
            out = re.sub(r"(?<![\w/.-])" + re.escape(n) + r"(?![\w/-])", lambda m: f"`{m.group(0)}`", out)
    return out


READ_CAP = 7000  # characters of the leader's files shown to the rubric judge, in all
READ_FILE_CAP = 2500
READ_CHANGED_CAP = 800  # of a cut file's share: the lines the session later changed or removed


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


def files_read(run, msgs=()):
    """The leader's files the AI read during the run, as they were before the session (so nothing
    the AI wrote itself), most relevant first: workflow nodes, requirements and plan, the backlog, the rest.
    A file counts as read when its longer lines appear in a tool result (a Read, or a cat in Bash,
    on any folder: drive/, onedrive/ or the workspace itself). A file cut at READ_FILE_CAP keeps, after
    its head, the lines the session went on to change or remove that share the most words with the
    AI's messages, then the other lines past the cut that share two or more (up to READ_CHANGED_CAP),
    so what the AI says it fixed in a saved draft, or read in a profile at the end of a record, is shown.
    A file the session changed is followed, under a label saying so, by its changed lines as the session
    left them (up to READ_CHANGED_CAP, those sharing most words with the messages first), so a fix the AI
    reports is judged against the after-state, not only the line it replaced.
    Where sessions started from different fixtures, a file read again with other contents is shown
    once more for that session, as the lines that differ from the first version shown, so a message
    is judged against its own session's files. Capped at READ_CAP characters."""
    said = {w for m in msgs for w in WORD.findall(m.lower()) if len(w) >= 4}
    many = len(run["sessions"]) > 1
    found, changed, now, later = {}, {}, {}, []
    for k, s in enumerate(run["sessions"], 1):
        if not s.get("root"):
            continue
        results = "\n".join(_tool_results(Path(s["root"]).parent / "events.jsonl"))
        if not results:
            continue
        for rel, text in s["files_start"].items():
            if rel.startswith(".") or "/." in rel or not text.strip():
                continue
            if rel in found and (found[rel][1] == text or any(r == rel and t == text for r, _, t in later)):
                continue
            long_lines = [ln.strip() for ln in text.splitlines() if len(ln.strip()) >= 30]
            if not (long_lines and sum(ln in results for ln in long_lines) >= min(2, len(long_lines))):
                continue
            if rel in found:
                later.append((rel, k, text))
                continue
            found[rel] = (k, text)
            end_text = (s.get("files_end") or {}).get(rel)
            end = set((end_text or "").splitlines())
            changed[rel] = [ln for ln in text.splitlines() if ln.strip() and ln not in end]
            first = set(text.splitlines())
            now[rel] = [ln for ln in (end_text or "").splitlines() if ln.strip() and ln not in first]
    parts, total = [], 0
    for rel in sorted(found, key=lambda r: (_read_rank(r), r)):
        k, body = found[rel][0], found[rel][1].strip()
        gone = []
        if len(body) > READ_FILE_CAP:
            head = READ_FILE_CAP - READ_CHANGED_CAP
            def overlap(ln):
                return len(said & set(WORD.findall(ln.lower())))
            past = body[head:].splitlines()
            ranked = sorted((ln for ln in changed.get(rel, []) if body.find(ln) >= head), key=lambda ln: -overlap(ln))
            ranked += sorted((ln for ln in past if ln.strip() and ln not in ranked and overlap(ln) >= 2),
                             key=lambda ln: -overlap(ln))
            for ln in ranked:
                if overlap(ln) and sum(len(x) + 1 for x in gone) + len(ln) <= READ_CHANGED_CAP:
                    gone.append(ln)
            body = (body[:head] + "\n[…cut; lines past the cut the session later changed, or that its messages speak of:]\n"
                    + "\n".join(gone) if gone else body[:READ_FILE_CAP] + "\n[…cut]")
        if now.get(rel):
            new = now[rel]
            keep, size = set(), 0
            # a line shown above that the session replaced comes first: its replacement (same opening
            # words, such as a field's label), so the judge sees what the line became
            lead = lambda ln: tuple(WORD.findall(ln.lower())[:2])
            shown_gone = {lead(ln) for ln in changed.get(rel, []) if ln in body and lead(ln)}
            # the replacements of lines listed past a cut (picked as the ones the messages speak of) first,
            # shortest first (a field's value), then the other replacements the messages speak of most
            picked = {lead(ln) for ln in gone if lead(ln)}
            first_new = sorted((ln for ln in new if lead(ln) in shown_gone),
                               key=lambda ln: (lead(ln) not in picked, -len(said & set(WORD.findall(ln.lower())))
                                               if lead(ln) not in picked else len(ln)))
            for ln in first_new + sorted((ln for ln in new if ln not in first_new),
                                         key=lambda ln: -len(said & set(WORD.findall(ln.lower())))):
                if size + len(ln) + 1 <= READ_CHANGED_CAP:
                    keep.add(ln)
                    size += len(ln) + 1
            body += ("\n[the session changed this file; its changed lines as the session left them:]\n"
                     + "\n".join(ln for ln in new if ln in keep))
        if total + len(body) > READ_CAP:
            continue
        label = f"{rel} (session {k})" if many else rel
        parts.append(f"### {label}\n\n````\n{body}\n````")
        total += len(body)
    for rel, k, text in later:
        first = set(found[rel][1].splitlines())
        diff = "\n".join(ln for ln in text.splitlines() if ln.strip() and ln not in first)[:READ_CHANGED_CAP]
        if not diff or total + len(diff) > READ_CAP + READ_CAP // 2:
            continue
        parts.append(f"### {rel} (session {k}: its lines that differ from session {found[rel][0]}'s)\n\n````\n{diff}\n````")
        total += len(diff)
    return "\n\n".join(parts)


MONTH_DAY = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}\b"
FACT = re.compile(MONTH_DAY + r"|[\w.+-]*\d[\w.+-]*|[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MON = r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)"
DATE_SAID = re.compile(r"\b(?:(\d{1,2}) " + _MON + r"|" + _MON + r"\.? (\d{1,2}))\b")
TOOL_LINES_CAP = 1500


def tool_lines(run, msgs):
    """Lines of the AI's own tool output (a version a command printed, an address a connection
    returned, a file date `ls -l` showed) that hold a figure, address or month-and-day date its
    messages give, so item 6 doesn't take a fact the AI looked up for an invented one. Only lines with
    such a token, spaces collapsed; lines that also hold a word of the messages (a file name beside
    the date) come first; capped at TOOL_LINES_CAP characters."""
    facts = {f.strip(".,") for m in msgs for f in FACT.findall(m) if len(f.strip(".,")) >= 3}
    # a date said as "20 October" or "October 20" also matches the ISO form a file holds ("-10-20")
    for m in msgs:
        for d, mon, mon2, d2 in DATE_SAID.findall(m):
            facts.add(f"-{MONTHS.index((mon or mon2)[:3].title()) + 1:02d}-{int(d or d2):02d}")
    if not facts:
        return ""
    words = {w for m in msgs for w in re.findall(r"[A-Za-z][\w.-]{3,}", m)} - facts
    cands = []
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for res in _tool_results(Path(s["root"]).parent / "events.jsonl"):
            for ln in res.splitlines():
                ln = re.sub(r"\s+", " ", ln.strip())[:200]
                if ln and ln not in cands and any(f in ln for f in facts):
                    cands.append(ln)
    out, total = [], 0
    for ln in sorted(cands, key=lambda ln: not any(w in ln.split() for w in words)):
        if total + len(ln) <= TOOL_LINES_CAP:
            out.append(ln)
            total += len(ln)
    return "\n".join(out)


WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
SHARED_RUN = 4  # consecutive words a tool-output passage must share with a message
SHARED_LINES_CAP = 1500
SHARED_LINE_LEN = 300


PATH = re.compile(r"[\w.~-]+(?:/[\w.~-]+)+/?")
TEMPLATE_PATH = re.compile(r"[\w.~-]+(?:/(?:[\w.~-]+|\[[^\]\s/]+\]|<[^>\s/]+>))+/?")


def _template_regex(token):
    """A path pattern with a [placeholder] or <placeholder> segment as a regex any filled-in path
    matches from its start; None for a path with no placeholder."""
    bits = re.split(r"(\[[^\]\s/]+\]|<[^>\s/]+>)", token)
    if len(bits) == 1:
        return None
    return re.compile("".join(r"[^/\s`]+" if i % 2 else re.escape(b) for i, b in enumerate(bits)))


def _grams(text):
    w = WORD.findall(text.lower().replace("’", "'"))
    return {tuple(w[i:i + SHARED_RUN]) for i in range(len(w) - SHARED_RUN + 1)}


def shared_lines(run, msgs, skip=""):
    """Passages of the AI's own tool output (a file it read, a plugin reference file, a fetched
    page, a command's output) that share a run of SHARED_RUN or more consecutive words with the
    unscripted part of its messages, so item 6 doesn't take a fact the AI read for an invented one.
    Long lines (a JSON registry's notes) are cut into sentences first. A passage whose path pattern
    (`Documents/Cowork/[workflow-slug]/`) a path in a message fills in counts too, first, cut around
    the pattern. Most shared runs first; capped at SHARED_LINES_CAP characters; passages already in
    `skip` aren't repeated."""
    grams, paths = set(), set()
    for m in msgs:
        own = re.sub(r"⟦[^⟧]*⟧", " ", m)
        grams |= _grams(own)
        paths |= set(PATH.findall(own))
    if not grams and not paths:
        return ""
    found, at = {}, {}
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for res in _tool_results(Path(s["root"]).parent / "events.jsonl"):
            for seg in re.split(r"(?<=[.;!?])\s+|\n|\\n", res):
                seg = seg.strip()
                if not seg or seg in found:
                    continue
                n = len(_grams(seg) & grams)
                for t in TEMPLATE_PATH.finditer(seg):
                    pat = _template_regex(t.group(0))
                    if pat and any(pat.match(p) for p in paths):
                        n, at[seg] = n + 1000, t.start()
                        break
                if n:
                    found[seg] = n
    out, total = [], 0
    for seg in sorted(found, key=lambda x: -found[x]):
        start = max(0, at.get(seg, 0) - SHARED_LINE_LEN // 3)
        ln = seg[start:start + SHARED_LINE_LEN]
        if ln in skip or ln in out or total + len(ln) > SHARED_LINES_CAP:
            continue
        out.append(ln)
        total += len(ln)
    return "\n".join(out)


def rubric_prompt(run):
    """Each AI message, with what the leader said just before it as context (not graded), so
    item 6 can tell a fact the leader gave from an invented one; and, once at the top, what the AI
    read from the leader's files (context, not graded), so a detail taken from them isn't invented."""
    msgs, said, where = [], [], []
    many = len(run["sessions"]) > 1
    for k, s in enumerate(run["sessions"], 1):
        before = []
        for t in s["turns"]:
            if t["role"] == "ai" and t["text"].strip():
                msgs.append(mark_scripted(t["text"]))
                said.append("\n\n".join(before))
                where.append(f" (session {k})" if many else "")
                before = []
            elif t["role"] != "ai" and t["text"].strip() and not t.get("end"):
                before.append(t["text"].strip())
    def block(i, m, ctx, w):
        quoted = "\n".join("> " + ln for ln in ctx.splitlines()) if ctx else "> (nothing)"
        return f"## Message {i}{w}\n\nThe leader said just before (context, not graded):\n\n{quoted}\n\nThe message:\n\n{m}"
    body = "\n\n".join(block(i, m, c, w) for i, (m, c, w) in enumerate(zip(msgs, said, where), 1))
    read = files_read(run, msgs)
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
