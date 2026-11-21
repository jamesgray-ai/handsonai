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
import check_scripted as CS
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


HISTORY_LABEL = ("## Requests the leader typed into Claude Code before this session (its HOME history, "
                 "which the evidence pass may read; context, not graded)")


def typed_history(run):
    """The typed-request history in each Claude Code session's temp HOME: the harness's own line
    (harness.reset_home) and any the fixture planted (leader.take_planted), one request a line."""
    out = []
    many = len(run["sessions"]) > 1
    for k, s in enumerate(run["sessions"], 1):
        if s.get("platform") != "claude-code":
            continue
        shown = [f"{H.HISTORY_MARKER} draft the weekly status report"]
        for ln in (s.get("typed_history") or "").splitlines():
            try:
                shown.append(json.loads(ln).get("display", ""))
            except ValueError:
                continue
        out += [f"- {x}" + (f" (session {k})" if many else "") for x in shown if x]
    return "\n".join(out)


GROUNDING_LABEL = ("## Content the platform added to the chat on its own, without the leader or the skill "
                   "asking (Cowork's mail and Teams grounding, a connector's results; the AI saw it, so a line "
                   "saying it was set aside is true; context, not graded)")


def platform_supplied(run):
    """The content a fixture planted for the platform to supply unasked (leader.take_planted), per session."""
    out = []
    many = len(run["sessions"]) > 1
    for k, s in enumerate(run["sessions"], 1):
        g = (s.get("grounding") or "").strip()
        if g:
            out.append((f"### Session {k}\n\n" if many else "") + g)
    return "\n\n".join(out)


def build_prompt(ev, run, items, script):
    parts = [f"# Eval {ev['id']} — {ev.get('name', '')}", "", f"Expected: {ev.get('expected_output', '')}", ""]
    if script:
        parts += ["## The leader's script (for the fidelity item only)", "", script, ""]
    parts += ["## Items to grade", ""]
    parts += [f"{i}. {x['text']}" for i, x in enumerate(items, 1)]
    hist = typed_history(run)
    if hist:
        parts += ["", HISTORY_LABEL, "", hist]
    supplied = platform_supplied(run)
    if supplied:
        parts += ["", GROUNDING_LABEL, "", supplied]
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
        gone = written_then_gone(s)
        if gone:
            parts += ["## Files the session wrote that were gone by its end (moved or cleared)", ""]
            parts += [f"- {rel}" for rel in gone] + [""]
    return "\n".join(parts)


def written_then_gone(s):
    """Files a session wrote with its Write or Edit tool that weren't there at its end: a part staged in
    `package/` and then installed and cleared. The end state alone hid the staging, so a judged
    "staged in package/" failed on three runs that staged it (P2-shared-skill, trial 4, 2026-11-20)."""
    if not s.get("root"):
        return []
    ws = str(Path(s["root"]).resolve())
    out = []
    for e in _load_events(Path(s["root"]).parent / "events.jsonl"):
        if e.get("type") != "assistant":
            continue
        for c in (e.get("message") or {}).get("content") or []:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            inp = c.get("input") or {}
            if c.get("name") in ("Write", "Edit"):
                paths = [str(inp.get("file_path") or "")]
            elif c.get("name") == "Bash":
                paths = _bash_targets(str(inp.get("command") or ""))
            else:
                continue
            for fp in paths:
                i = fp.find("/workspace/")
                rel = fp[i + len("/workspace/"):] if i >= 0 else (fp[len(ws) + 1:] if fp.startswith(ws) else "")
                if rel and rel not in (s.get("files_end") or {}) and rel not in out:
                    out.append(rel)
    return out


_CD = re.compile(r"^\s*cd\s+(['\"]?)([^'\";&|]+)\1\s*(?:;|&&)")
_REDIRECT = re.compile(r"(?<![0-9&>])>>?\s*(['\"]?)([^\s;&|<>'\"]+)\1")


def _bash_targets(cmd):
    """Files a Bash command wrote by redirection (`cat > path <<'EOF'`, `> path`, `>> path`), made absolute
    from a leading `cd`. Trial 6 (2026-11-20): P2-shared-skill run 1 staged the shared skill in package/
    with a heredoc, then installed and cleared it, and the judge, shown only Write and Edit paths, said
    it was never staged."""
    m = _CD.match(cmd)
    base = m.group(2).strip() if m else ""
    out = []
    for q, p in _REDIRECT.findall(cmd):
        if p.startswith("/dev/") or p.startswith("&"):
            continue
        out.append(p if p.startswith("/") or not base else base.rstrip("/") + "/" + p)
    return out


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
    # core batch 2 (2026-11-14): the script as the leader got it, with each include-facts line expanded;
    # the raw file left the judge unable to trace shared facts, so valid runs were marked invalid
    import run_eval as RE
    script = "\n\n---\n\n".join(RE.load_script(base, p) for p in dict.fromkeys(paths) if (base / p).exists()) or None
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


# Design baseline fix (2026-11-14): 7000 left no room for the requirements once a plan was shown
READ_CAP = 10000  # characters of the leader's files shown to the rubric judge, in all
# a step line the leader fixed ("· fixed (your judgment)"): what N-10's "keeping the steps you fixed" rests on
FIXED_STEP = re.compile(r"· fixed \((?:regulation|policy|your judgment)\)")
READ_FILE_CAP = 2500
READ_CHANGED_CAP = 800  # of a cut file's share: the lines the session later changed or removed


SKILL_TEXT = "Base directory for this skill"


PLUGIN_DOC = re.compile(r"/plugin/[^\s'\"]*")
DOC_READER = re.compile(r"\b(?:cat|head|tail|sed|grep|rg|awk|less|more|nl)\b")


def _plugin_path(p):
    """A path in the plugin under test (not in the leader's workspace): its skills and references."""
    p = str(p or "")
    return "/plugin/" in p and "/workspace/" not in p.split("/plugin/", 1)[0] + "/"


def _instruction_call(b):
    """Whether a tool call reads the plugin's own text (a SKILL.md or a reference file): Read or Grep
    on a plugin path, or a Bash command that reads one with cat, head, sed, grep and the like. Its
    output is the step's instructions, never a fact the AI looked up about the leader's work. A plugin
    script a command runs (the routing script) prints tool output, unless the command reads a plugin
    file too (then all of it counts as instructions: fail closed)."""
    name, inp = b.get("name"), b.get("input") or {}
    if name == "Read":
        return _plugin_path(inp.get("file_path"))
    if name == "Grep":
        return _plugin_path(inp.get("path"))
    if name == "Bash":
        cmd = str(inp.get("command") or "")
        for part in re.split(r"&&|\|\||;|\|", cmd):
            if DOC_READER.search(part) and any(_plugin_path(m.group(0)) and not m.group(0).endswith((".py", ".sh"))
                                               for m in PLUGIN_DOC.finditer(part)):
                return True
    return False


def _events_user_blocks(events_path, instructions=None):
    """Each user-side block in a session's events.jsonl; with a set, the ids of the tool calls that
    read the plugin's own text are added to it as they're met."""
    try:
        lines = Path(events_path).read_text(errors="replace").splitlines()
    except OSError:
        return
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
            if e.get("type") == "assistant":
                if instructions is not None and b.get("type") == "tool_use" and _instruction_call(b):
                    instructions.add(b.get("id"))
            elif e.get("type") == "user":
                yield b


def _result_text(b):
    c = b.get("content")
    text = c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c or [] if isinstance(x, dict))
    return re.sub(r"(?m)^\s*\d+\t", "", text)


def _tool_results(events_path):
    """The text of every tool result in a session's events.jsonl, Read's line-number prefixes removed.
    The step's own text is never among them (see _skill_texts): the skill text the Skill tool loaded,
    and a plugin reference file the AI read. Their example figures ("(2 min)", "within 48 hours")
    aren't facts the AI looked up about the leader's work."""
    out, ins = [], set()
    for b in _events_user_blocks(events_path, ins):
        if b.get("type") != "tool_result" or b.get("tool_use_id") in ins:
            continue
        text = _result_text(b)
        if text.startswith(SKILL_TEXT):
            continue
        out.append(text)
    return out


def _skill_texts(events_path):
    """The step's own text in a session's events.jsonl: its SKILL.md as the Skill tool loaded it, and
    each plugin file (a reference, another skill's SKILL.md) a tool call read."""
    out, ins = [], set()
    for b in _events_user_blocks(events_path, ins):
        if b.get("type") == "text" and str(b.get("text", "")).startswith(SKILL_TEXT):
            out.append(b["text"])
        elif b.get("type") == "tool_result" and (b.get("tool_use_id") in ins or _result_text(b).startswith(SKILL_TEXT)):
            out.append(_result_text(b))
    return out


def _read_rank(rel):
    if "/workflows/" in f"/{rel}" and not rel.endswith("index.md"):
        return 0
    if rel.endswith(("requirements.md", "design-plan.md")):  # the plan's changes: back what Build says
        return 1
    # Analyze's evidence: the knowledge graph, SOPs, process guides, a folder the leader named, and the
    # project instructions file (core round-1 fixes, E11), so a detail the AI took from them is shown
    core = rel.split("/")
    core = core[1:] if core[0] in ("drive", "onedrive") and len(core) > 1 else core
    core = core[1:] if core[0] == "ai-workspace" and len(core) > 1 else core
    if any(p in ("knowledge", "sops", "process-guides") for p in core[:-1]) or core[-1] in ("CLAUDE.md", "AGENTS.md"):
        return 1
    if len(core) > 1 and core[0] not in ("registry", "framework", "history") and not core[0].startswith("."):
        return 1  # a folder the leader named (a Playbooks folder, say)
    if "opportunity-report" in rel or "backlog" in rel:
        return 2
    return 3 if "registry/" in rel and not rel.endswith(("index.md", "log.md")) else 4


AI_WROTE = (" [WRITTEN BY THE AI in an earlier session of this run, not the leader's: a detail found only "
            "here, and nowhere in what the leader said or brought, is invented]")


def ai_written(run):
    """(session, path) for each file in a session's start tree that the AI wrote or changed in an
    earlier session of the run: a session carried over from the one before (not begun from its own
    fixture, CS.leader_files) whose file isn't, word for word, the one the leader brought."""
    sess = run["sessions"]
    marked = any("fixture" in s for s in sess)
    out, brought = set(), {}
    for k, s in enumerate(sess, 1):
        start = s.get("files_start") or {}
        if (s.get("fixture") if marked else k == 1):
            brought = dict(start)
            continue
        out |= {(k, rel) for rel, text in start.items() if brought.get(rel) != text}
    return out


READ_PICKED_CAP = 1500  # of a cut file's share: the picked workflow's own card and summary row


def _slug(text):
    return "-" + re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") + "-"


def picked_slugs(run):
    """The workflows the run worked on: a framework/<slug>/ folder or a registry/workflows/<slug>.md node a
    session created or changed."""
    out = set()
    for s in run["sessions"]:
        start, end = s.get("files_start") or {}, s.get("files_end") or {}
        for rel in end:
            if start.get(rel) == end[rel]:
                continue
            p = rel.split("/")
            if len(p) >= 3 and p[0] == "framework":
                out.add(p[1])
            elif len(p) == 3 and p[:2] == ["registry", "workflows"] and p[2].endswith(".md"):
                out.add(p[2][:-3])
    return out


def picked_blocks(text, slugs, shown):
    """The blocks of a cut file that name a picked workflow and aren't already shown: each table (a run of
    `|` lines) and each stretch between `---` rules and headings (an Analyze card). smoke-1 fix (2026-11-14):
    N-D23's rows (How often from the card's Frequency) were judged invented when the row sat past the cut."""
    if not slugs:
        return ""
    blocks, cur, kind = [], [], None
    for ln in text.splitlines() + ["---"]:
        s = ln.strip()
        k = "rule" if re.match(r"^(?:---+|#{1,6} .*)$", s) else "table" if s.startswith("|") else "text" if s else None
        if k == "rule" or (k and kind and k != kind) or (k is None and kind == "table"):
            if "".join(cur).strip():
                blocks.append("\n".join(cur).strip())
            cur, kind = [], None
        if k in ("table", "text") or (k is None and kind):
            cur.append(ln)
            kind = k or kind
    out, size = [], 0
    # smoke-2 fix (2026-11-14): tables first, since the Candidate Summary row holds what N-D23 plays back
    # (Trigger, Deliverable, Frequency); the card's prose came first and filled the cap ("one-page" judged invented)
    for b in sorted(blocks, key=lambda b: not b.lstrip().startswith("|")):
        if b and b not in shown and any(sl in _slug(b) for sl in {f"-{x}-" for x in slugs}) \
                and size + len(b) + 1 <= READ_PICKED_CAP:
            out.append(b)
            size += len(b) + 1
    return "\n\n".join(out)


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
    ai_wrote = ai_written(run)
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
    picked = picked_slugs(run)
    # Design baseline fix (2026-11-14): the requirements before the plan (same rank), so the plan can't use
    # the budget and leave the requirements out
    for rel in sorted(found, key=lambda r: (_read_rank(r), not r.endswith("requirements.md"), r)):
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
            if "fixed" in said:  # the messages speak of fixed steps: the step lines marked fixed come first
                ranked = ([ln for ln in past if FIXED_STEP.search(ln)]
                          + [ln for ln in ranked if not FIXED_STEP.search(ln)])
            for ln in ranked:
                if overlap(ln) and sum(len(x) + 1 for x in gone) + len(ln) <= READ_CHANGED_CAP:
                    gone.append(ln)
            body = (body[:head] + "\n[…cut; lines past the cut the session later changed, or that its messages speak of:]\n"
                    + "\n".join(gone) if gone else body[:READ_FILE_CAP] + "\n[…cut]")
            extra = picked_blocks(found[rel][1], picked, body)
            if extra:
                body += "\n[the picked workflow's own card and Candidate Summary row, past the cut:]\n" + extra
        if now.get(rel):
            new = now[rel]
            keep, size = set(), 0
            # a line shown above that the session replaced comes first: its replacement (same opening
            # words, such as a field's label), so the judge sees what the line became
            lead = lambda ln: tuple(WORD.findall(ln.lower())[:2])
            shown_gone = {lead(ln) for ln in changed.get(rel, []) if ln in body and lead(ln)}
            # the replacements of lines listed past a cut (picked as the ones the messages speak of) first,
            # shortest first (a field's value), then the other replacements the messages speak of most
            # smoke-2 fix (2026-11-14): its own name, so the picked workflows (picked_slugs, above) aren't
            # overwritten for the files after it (a changed node ranks before the report, so the report's card
            # past the cut was never shown)
            gone_leads = {lead(ln) for ln in gone if lead(ln)}
            first_new = sorted((ln for ln in new if lead(ln) in shown_gone),
                               key=lambda ln: (lead(ln) not in gone_leads, -len(said & set(WORD.findall(ln.lower())))
                                               if lead(ln) not in gone_leads else len(ln)))
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
        if (k, rel) in ai_wrote:
            label += AI_WROTE
        parts.append(f"### {label}\n\n````\n{body}\n````")
        total += len(body)
    for rel, k, text in later:
        first = set(found[rel][1].splitlines())
        diff = "\n".join(ln for ln in text.splitlines() if ln.strip() and ln not in first)[:READ_CHANGED_CAP]
        if not diff or total + len(diff) > READ_CAP + READ_CAP // 2:
            continue
        mark = AI_WROTE if (k, rel) in ai_wrote else ""
        parts.append(f"### {rel} (session {k}: its lines that differ from session {found[rel][0]}'s){mark}\n\n````\n{diff}\n````")
        total += len(diff)
    return "\n\n".join(parts)


MONTH_DAY = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}\b"
FACT = re.compile(MONTH_DAY + r"|[\w.+-]*\d[\w.+-]*|[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MON = r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)"
DATE_SAID = re.compile(r"\b(?:(\d{1,2}) " + _MON + r"|" + _MON + r"\.? (\d{1,2}))\b")
# Build rounds 2026-11-18: about 11 of 59 rubric-6 flags were facts in tool output cut off here
TOOL_LINES_CAP = 3000
SHORT_NUM = re.compile(r"(?<![\w.])(\d{1,2})(?![\w.]) ([A-Za-z]{3,})")
TOOL_LINE_LEN = 300


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
    # a short number ("71 words", "12 members") is too common to match alone: match it with the
    # stem of the word after it, both on the same tool line ("word count: 71"). Trial 2026-11-19:
    # about half the rubric-6 number flags were counts a check agent's result printed.
    pairs = {(n, w[:4].lower()) for m in msgs for n, w in SHORT_NUM.findall(m)}
    if not facts and not pairs:
        return ""
    words = {w for m in msgs for w in re.findall(r"[A-Za-z][\w.-]{3,}", m)} - facts
    cands = []
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for res in _tool_results(Path(s["root"]).parent / "events.jsonl"):
            for ln in res.splitlines():
                ln = re.sub(r"\s+", " ", ln.strip())[:TOOL_LINE_LEN]
                if ln and ln not in cands and (any(f in ln for f in facts) or any(
                        re.search(rf"(?<![\w.]){n}(?![\w.])", ln) and w in ln.lower() for n, w in pairs)):
                    cands.append(ln)
    out, total = [], 0
    for ln in sorted(cands, key=lambda ln: not any(w in ln.split() for w in words)):
        if total + len(ln) <= TOOL_LINES_CAP:
            out.append(ln)
            total += len(ln)
    return "\n".join(out)


NAME_LINES_CAP = 600


def name_lines(run, msgs):
    """For each proper name a message uses mid-sentence ("the Northwind notes") that the step's own
    skill text doesn't hold, the first line of the files the leader brought (CS.leader_files: never
    a file the AI wrote in an earlier session) that names it, with its path, so a client or person from a practice input the file context had
    no room for isn't taken for an invented one. Capped at NAME_LINES_CAP characters."""
    names = set()
    for m in msgs:
        toks = re.findall(r"[A-Za-z][\w'-]*|[.!?:\n]", m)
        for prev, tok in zip(["."] + toks, toks):
            if re.fullmatch(r"[A-Z][a-z]{3,}", tok) and prev not in (".", "!", "?", ":", "\n"):
                names.add(tok)
    if not names:
        return ""
    skill = "\n".join(t for s in run["sessions"] if s.get("root")
                      for t in _skill_texts(Path(s["root"]).parent / "events.jsonl"))
    # the files the leader brought only: a later session's start tree holds what the AI wrote earlier
    files = [(rel, t) for rel, t in CS.leader_files(run) if not (rel.startswith(".") or "/." in rel)]
    out, total = [], 0
    for n in sorted(x for x in names if not re.search(rf"\b{x}\b", skill)):
        for rel, text in files:
            hit = next((ln for ln in text.splitlines() if re.search(rf"\b{n}\b", ln)), None)
            if hit:
                ln = f"{rel}: " + re.sub(r"\s+", " ", hit.strip())[:200]
                if ln not in out and total + len(ln) <= NAME_LINES_CAP:
                    out.append(ln)
                    total += len(ln)
                break
    return "\n".join(out)


STATE_LINE = re.compile(r"(?m)^\S+: state \d+ \(.*$")


def state_lines(run):
    """The routing script's own verdicts (framework-state's summary line, and which workflow files it
    found), whenever the session ran it: a not-owner or resume line describes that state ("built and
    passed its practice runs" in state 10; "started in Deconstruct" with a deconstruct-in-progress.md),
    and it shares no run of words with the message for shared_lines to find."""
    out = []
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for res in _tool_results(Path(s["root"]).parent / "events.jsonl"):
            for ln in STATE_LINE.findall(res):
                if ln not in out:
                    out.append(ln[:300])
            m = re.search(r"\{.*\}", res, re.S)
            if not (m and '"facts"' in res):
                continue
            try:
                facts = json.loads(m.group(0)).get("facts") or {}
            except ValueError:
                continue
            found = [f for f, there in (facts.get("files") or {}).items() if there is True]
            if found:
                ln = f"{facts.get('workflow', 'the workflow')}: files found: {', '.join(found)}"
                if ln not in out:
                    out.append(ln)
    return "\n".join(out[:12])


WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
SHARED_RUN = 4  # consecutive words a tool-output passage must share with a message
SHARED_LINES_CAP = 3000
SHARED_LINE_LEN = 300
SHARED_NOUN_CAP = 600  # characters of passages sharing only a three-word noun run
NOUN_WORD = 5  # letters in a "long" word of a three-word run (_noun_grams)


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


def _noun_grams(text):
    """Runs of three words with at least two long ones ("the expense inbox"): a named thing from the
    leader's files said in other surrounding words, which shares no SHARED_RUN-word run with its source."""
    w = WORD.findall(text.lower().replace("’", "'"))
    return {g for g in (tuple(w[i:i + 3]) for i in range(len(w) - 2))
            if sum(len(x) >= NOUN_WORD for x in g) >= 2}


def shared_lines(run, msgs, skip=""):
    """Passages of the AI's own tool output (a file it read, a plugin reference file, a fetched
    page, a command's output) that share a run of SHARED_RUN or more consecutive words with the
    unscripted part of its messages, so item 6 doesn't take a fact the AI read for an invented one.
    Long lines (a JSON registry's notes) are cut into sentences first. A passage whose path pattern
    (`Documents/Cowork/[workflow-slug]/`) a path in a message fills in counts too, first, cut around
    the pattern. Most shared runs first; capped at SHARED_LINES_CAP characters. Then, up to
    SHARED_NOUN_CAP, passages sharing only a three-word run with two long words ("the expense inbox")
    that nothing already shown carries; passages already in
    `skip` aren't repeated."""
    grams, nouns, paths = set(), set(), set()
    for m in msgs:
        own = re.sub(r"⟦[^⟧]*⟧", " ", m)
        grams |= _grams(own)
        nouns |= _noun_grams(own)
        paths |= set(PATH.findall(own))
    if not grams and not nouns and not paths:
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
                # a shared SHARED_RUN-word run outranks any number of shared three-word noun runs
                n = 100 * len(_grams(seg) & grams) + len(_noun_grams(seg) & nouns)
                for t in TEMPLATE_PATH.finditer(seg):
                    pat = _template_regex(t.group(0))
                    if pat and any(pat.match(p) for p in paths):
                        n, at[seg] = n + 100000, t.start()
                        break
                if n:
                    found[seg] = n
    out, total = [], 0
    for seg in sorted((x for x in found if found[x] >= 100), key=lambda x: -found[x]):
        start = max(0, at.get(seg, 0) - SHARED_LINE_LEN // 3)
        ln = seg[start:start + SHARED_LINE_LEN]
        if ln in skip or ln in out or total + len(ln) > SHARED_LINES_CAP:
            continue
        out.append(ln)
        total += len(ln)
    # then, with their own room, passages that share only a three-word noun run that nothing shown
    # above already carries, so a named thing from the leader's files isn't crowded out
    shown, noun_total = _noun_grams(skip + "\n" + "\n".join(out)), 0
    for seg in sorted((x for x in found if found[x] < 100), key=lambda x: -found[x]):
        ln = seg[:SHARED_LINE_LEN]
        new = (_noun_grams(ln) & nouns) - shown
        if not new or ln in skip or ln in out or noun_total + len(ln) > SHARED_NOUN_CAP:
            continue
        out.append(ln)
        noun_total += len(ln)
        shown |= _noun_grams(ln)
    return "\n".join(out)


SKILL_PASSAGES_CAP = 1500


def skill_passages(run, msgs):
    """Passages of the step's own instructions (the SKILL.md the Skill tool loaded, and the plugin
    files the AI read: _skill_texts) that share a run
    of SHARED_RUN or more words with the unscripted part of the messages, most shared first, capped
    at SKILL_PASSAGES_CAP characters. They're shown to the judge under their own label, apart from
    the tool lines, so a framework rule the step states ("you run it once by hand before its schedule
    goes on") isn't taken for an invented fact, while an example figure the skill gives ("within 48
    hours") never backs a detail about the leader's work."""
    grams = set()
    for m in msgs:
        grams |= _grams(re.sub(r"⟦[^⟧]*⟧", " ", m))
    if not grams:
        return ""
    found = {}
    for s in run["sessions"]:
        if not s.get("root"):
            continue
        for text in _skill_texts(Path(s["root"]).parent / "events.jsonl"):
            for seg in re.split(r"(?<=[.;!?])\s+|\n", text):
                seg = seg.strip()
                if seg and seg not in found:
                    n = len(_grams(seg) & grams)
                    if n:
                        found[seg] = n
    out, total = [], 0
    for seg in sorted(found, key=lambda x: -found[x]):
        ln = seg[:SHARED_LINE_LEN]
        if ln in out or total + len(ln) > SKILL_PASSAGES_CAP:
            continue
        out.append(ln)
        total += len(ln)
    return "\n".join(out)


SKILL_LABEL = ("## The step's own instructions, passages the messages echo (context, not graded)\n\n"
               "These are from the framework step's instructions (its skill text and the plugin's reference "
               "files), not from the leader, "
               "the leader's files or any tool. They back only a rule of how the step works that a message "
               "states. They are never a source for a fact about the leader's work: a figure, time, name, "
               "date or other detail of the leader's work found only here (an example the instructions "
               "give) is invented (item 6).\n\n")


def _events(run):
    """(session number, events path) for each session of the run that has its events."""
    for k, s in enumerate(run["sessions"], 1):
        if s.get("root"):
            yield k, Path(s["root"]).parent / "events.jsonl"


def _load_events(path):
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if isinstance(e, dict):
            out.append(e)
    return out


SETTINGS_LABEL = "## The project's Claude Code settings as each session left them (context, not graded)\n\n"
SETTINGS_CAP = 1500


def settings_files(run):
    """`.claude/settings.local.json` as each session left it, where the session changed it: the block's
    deny rules and the test helper's allow rules Build wrote there. The file context leaves out dot
    folders, so "the four `test-run.sh` lines under allow" (true: the wrapper adds four) was flagged
    as invented in four trial-3 runs (2026-11-20). Capped at SETTINGS_CAP characters."""
    out = []
    for k, s in enumerate(run["sessions"], 1):
        end = (s.get("files_end") or {}).get(".claude/settings.local.json")
        if not end or end == (s.get("files_start") or {}).get(".claude/settings.local.json"):
            continue
        label = f"Session {k}: " if len(run["sessions"]) > 1 else ""
        out.append(f"{label}.claude/settings.local.json\n{end.strip()}")
    return H.scrub("\n\n".join(out))[:SETTINGS_CAP]


def session_tools(run):
    """The tools each session had, from its first init message: the connection tools (mcp__…) by full
    name, so "this Gmail connection also offers a send action" or "it can't delete drafts" is checked
    against what the session was offered (Build rounds 2026-11-18: 8 runs flagged on rubric 6 for
    exactly that), and the others in one line."""
    out, many = [], len(run["sessions"]) > 1
    for k, path in _events(run):
        # Every init, not the first: a connection the leader adds partway through (Build's "Connect a tool")
        # shows only in the inits after it, and the first one alone listed no connection tools at all
        # (re-grade 2026-11-19: 20 runs still flagged "the tool list shows no connection tools").
        inits = [e for e in _load_events(path) if e.get("type") == "system" and e.get("subtype") == "init"]
        if not inits:
            continue
        tools = list(dict.fromkeys(str(t) for e in inits for t in e.get("tools") or []))
        mcp = [t for t in tools if t.startswith("mcp__")]
        own = [t for t in tools if not t.startswith("mcp__")]
        head = f"Session {k}: " if many else ""
        out.append(f"{head}connection tools: {', '.join(mcp) if mcp else 'none'}")
        out.append(f"{head}other tools: {', '.join(own) if own else 'none'}")
    return "\n".join(out)


TOOLS_LABEL = ("## The tools the session was offered (context, not graded)\n\n"
               "From the session's own start-up message. A connection's tools (`mcp__[connection]__[action]`) "
               "are the actions it offers: a message saying the connection offers, or lacks, an action is backed "
               "or contradicted by this list. A later session's list can lack a tool an earlier session listed "
               "because that session's settings deny it (a deny rule hides the tool from the session): the "
               "connection still offers it, so \"your connection can also send\" is backed by the earlier list.\n\n")

INPUTS_CAP = 6000
INPUT_FILE_CAP = 2000


def practice_inputs(run):
    """The workflow's practice inputs the leader brought (`inputs/` in a framework folder: the call notes
    and examples checks run on), each whole up to INPUT_FILE_CAP, in all up to INPUTS_CAP. A check
    agent reads them, so the main thread's tool results may never hold them, and a name or detail the
    AI quotes from one ("Dana Ortiz") was judged invented (Build rounds 2026-11-18, 4 runs)."""
    out, total, seen = [], 0, set()
    for rel, text in CS.leader_files(run):
        if "/inputs/" not in f"/{rel}" or rel in seen or not text.strip():
            continue
        seen.add(rel)
        body = text.strip()
        body = body if len(body) <= INPUT_FILE_CAP else body[:INPUT_FILE_CAP] + "\n[…cut]"
        if total + len(body) > INPUTS_CAP:
            continue
        out.append(f"### {rel}\n\n````\n{body}\n````")
        total += len(body)
    return "\n\n".join(out)


INPUTS_LABEL = ("## The workflow's practice inputs the leader brought (context, not graded)\n\n"
                "The leader's own files: a detail found in them is backed.\n\n")

DOCS_KEYS = {"claude-code": "claude-code", "claude-web": "claude", "claude-desktop": "claude", "chatgpt": "chatgpt",
             "codex": "openai-codex", "microsoft-365": "microsoft-365-copilot"}
DOCS_FILE = HERE.parent / "plugins" / "handsonai" / "registries" / "platform-docs.json"


def platform_docs(run, msgs=()):
    """The entries of the plugin's platform-docs.json (the official pages the step points the leader
    to) for each session's platform, and any other platform's entry whose page a message names, one
    line per topic: from the plugin copy the session ran with (its run root's plugin/), else this
    repo's. A help page a message links ("help.openai.com/…/skills-in-chatgpt") then reads as one the
    step was given, not an invented one (Build rounds 2026-11-18, 2 runs)."""
    data = None
    for s in run["sessions"]:
        if s.get("root"):
            f = Path(s["root"]).parents[1] / "plugin" / "registries" / "platform-docs.json"
            if f.exists():
                data = f
                break
    try:
        docs = json.loads((data or DOCS_FILE).read_text()).get("platforms") or {}
    except (OSError, ValueError):
        return ""
    keys = [DOCS_KEYS[s["platform"]] for s in run["sessions"] if DOCS_KEYS.get(s.get("platform"))]
    said = " ".join(msgs)
    for key, p in docs.items():
        urls = [u for v in (p.get("docs") or {}).values() for u in v]
        if any(re.sub(r"^https?://", "", u).rstrip("/") in said for u in urls):
            keys.append(key)
    out = []
    for key in dict.fromkeys(keys):
        p = docs.get(key)
        if not p:
            continue
        out.append(f"{p.get('name', key)}:")
        out += [f"- {topic}: {', '.join(urls)}" for topic, urls in (p.get("docs") or {}).items() if urls]
    return "\n".join(out)


DOCS_LABEL = ("## The platform's official pages the step was given (its platform-docs.json; context, not graded)\n\n"
              "The step is told to point the leader to these pages: a link to one is backed. They hold no fact "
              "about the leader's work.\n\n")

COMMANDS_CAP = 6000
COMMAND_LEN = 240
RESULT_LEN = 500


def tool_calls(run):
    """The AI's own tool calls and what each returned, cut short: every connection call (mcp__…, its
    input up to COMMAND_LEN), every Bash command that isn't a read of the step's own text, every Skill
    call that isn't a handsonai skill (with the synthetic message that follows it), and every Edit or
    Write on a file outside the plugin (its path and the start of what it wrote), each with the start
    of its result. Calls with short results first (a `crontab -l`, a `git log`, a `diff`, a
    draft's address), then in order, up to COMMANDS_CAP. A claim backed only by a check the AI ran
    ("nothing is scheduled on this computer", "`# edited` was added at the end") was judged invented
    when no word run of it matched the output (Build rounds 2026-11-18, about 11 runs)."""
    rows = []
    for _, path in _events(run):
        calls, skill_row = {}, None
        for e in _load_events(path):
            msg = e.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            if e.get("type") == "user" and e.get("isSynthetic") and skill_row is not None:
                # build-full-1 fix (2026-11-21): what a platform skill printed back to the session
                # ("We're having trouble connecting with your remote claude.ai account…") follows its
                # "Launching skill" result as a synthetic user message: show it with the call
                text = content if isinstance(content, str) else "\n".join(
                    b.get("text", "") for b in content or [] if isinstance(b, dict) and b.get("type") == "text")
                text = text.strip()
                if text:
                    short = text if len(text) <= RESULT_LEN else text[:RESULT_LEN] + " […cut]"
                    row = rows[skill_row]
                    rows[skill_row] = (row[0], row[1], f"{row[2]}\n{short}")
                skill_row = None
                continue
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if e.get("type") == "assistant" and b.get("type") == "tool_use":
                    name, inp = str(b.get("name") or ""), b.get("input") or {}
                    skill_row = None
                    if name == "Bash" and not _instruction_call(b):
                        calls[b.get("id")] = "$ " + re.sub(r"\s+", " ", str(inp.get("command") or ""))[:COMMAND_LEN]
                    elif name.startswith("mcp__"):
                        calls[b.get("id")] = f"{name} " + json.dumps(inp, ensure_ascii=False)[:COMMAND_LEN]
                    elif name == "Skill" and not str(inp.get("skill") or "").startswith("handsonai:"):
                        # a skill that isn't the framework's (Claude Code's own /schedule): what it did is a fact
                        calls[b.get("id")] = (f"Skill {inp.get('skill') or ''} "
                                              + json.dumps(inp.get("args") or "", ensure_ascii=False)[:COMMAND_LEN])
                    elif name in ("Edit", "Write", "MultiEdit") and not _plugin_path(inp.get("file_path")):
                        # a change the AI made itself to the leader's files (a settings rule, a skill paused)
                        body = inp.get("new_string") if name == "Edit" else inp.get("content")
                        if name == "MultiEdit":
                            body = " | ".join(str(x.get("new_string") or "") for x in inp.get("edits") or []
                                              if isinstance(x, dict))
                        calls[b.get("id")] = (f"{name} {inp.get('file_path') or ''}: "
                                              + re.sub(r"\s+", " ", str(body or ""))[:COMMAND_LEN])
                elif e.get("type") == "user" and b.get("type") == "tool_result" and b.get("tool_use_id") in calls:
                    res = _result_text(b).strip()
                    call = calls.pop(b.get("tool_use_id"))
                    short = res if len(res) <= RESULT_LEN else res[:RESULT_LEN] + " […cut]"
                    if call.startswith("Skill "):
                        skill_row = len(rows)
                    rows.append((len(res) > RESULT_LEN, len(rows), f"{call}\n{short or '(no output)'}"))
    out, total = [], 0
    for _, _, row in sorted(rows):
        if total + len(row) > COMMANDS_CAP:
            continue
        out.append(row)
        total += len(row) + 2
    return "\n\n".join(out)


COMMANDS_LABEL = ("## The AI's own commands and connection calls, with what each returned (context, not graded)\n\n"
                  "Each result is cut short. A fact a result shows (nothing scheduled, a commit's message, a "
                  "draft's address, a line a diff shows) is backed.\n\n")

# Review finding 21 (2026-11-21): rubric items 2, 5 and 6 let text quoted as the practice run showed it pass
# only when it matches what the run returned, so the run's own output has to be in front of the judge: the
# commands list above cuts each result at RESULT_LEN and leaves out check agents (the Agent tool) entirely
CHECK_RUN_LEN = 3000
CHECK_RUNS_CAP = 9000
CHECK_RUN = re.compile(r"test-run\.sh\b")


def check_runs(run):
    """What each practice or check run returned, longer than the commands list keeps it: every Bash command
    that starts the wrapper (`framework/.bin/test-run.sh check|bare|test …`) and every check agent the
    session started (the Agent or Task tool), each result up to CHECK_RUN_LEN, in order, up to CHECK_RUNS_CAP."""
    rows = []
    many = len(run["sessions"]) > 1
    for k, path in _events(run):
        calls = {}
        for e in _load_events(path):
            msg = e.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if e.get("type") == "assistant" and b.get("type") == "tool_use":
                    name, inp = str(b.get("name") or ""), b.get("input") or {}
                    if name == "Bash" and CHECK_RUN.search(str(inp.get("command") or "")):
                        calls[b.get("id")] = "$ " + re.sub(r"\s+", " ", str(inp.get("command")))[:COMMAND_LEN]
                    elif name in ("Agent", "Task"):
                        what = inp.get("subagent_type") or inp.get("description") or ""
                        calls[b.get("id")] = f"{name} {what}: " + re.sub(r"\s+", " ", str(inp.get("prompt") or ""))[:COMMAND_LEN]
                elif e.get("type") == "user" and b.get("type") == "tool_result" and b.get("tool_use_id") in calls:
                    res = _result_text(b).strip()
                    short = res if len(res) <= CHECK_RUN_LEN else res[:CHECK_RUN_LEN] + " […cut]"
                    label = f"Session {k}: " if many else ""
                    rows.append(f"{label}{calls.pop(b.get('tool_use_id'))}\n{short or '(no output)'}")
    out, total = [], 0
    for row in rows:
        if total + len(row) > CHECK_RUNS_CAP:
            out.append("[…later runs cut]")
            break
        out.append(row)
        total += len(row) + 2
    return H.scrub("\n\n".join(out))


CHECK_RUNS_LABEL = ("## What each practice or check run returned (context, not graded)\n\n"
                    "The workflow's own output and checkpoints, as the run printed them. Text a message quotes as "
                    "the run's output is backed only where it matches what is shown here, in the commands list "
                    "or in the next section.\n\n")
QUOTE_WINDOW = 300


def quoted_sources(run):
    """Each block quote (>) in the AI's messages, set against what the session's tool calls returned and
    what the leader pasted (check_scripted.quote_backed, the same comparison as the quoted_output_seen
    check): where it's found, the passage that holds it (whitespace and Markdown marks set aside, in lower
    case); where it isn't, that it's found nowhere."""
    rows, n_msg = [], 0
    many = len(run["sessions"]) > 1
    for k, s in enumerate(run["sessions"], 1):
        ai = [t["text"] for t in s["turns"] if t["role"] == "ai" and t["text"].strip()]
        quotes = []
        for m in ai:
            n_msg += 1
            quotes += [(n_msg, b) for b in CS.block_quotes(m)]
        if not quotes:
            continue
        sources = CS.session_sources(s)
        normed = [CS.quote_norm(x) for x in sources or []]
        whole = "\n".join(normed)
        for i, b in quotes:
            text = " / ".join(x.strip() for x in b if x.strip())
            head = f"Message {i}{f' (session {k})' if many else ''} quotes: {text[:200]}{' […]' if len(text) > 200 else ''}"
            ok = CS.quote_backed(b, whole) if sources is not None else False
            if ok is None:
                continue  # too short to tell apart
            if not ok:
                rows.append(f"{head}\nFOUND IN NO TOOL RESULT and nothing the leader pasted.")
                continue
            part = max(CS._quote_parts("\n".join(b)), key=len, default="")
            src = next((x for x in normed if part and part in x), "")
            at = src.find(part) if src else -1
            window = (src[max(0, at - QUOTE_WINDOW):at + len(part) + QUOTE_WINDOW] if at >= 0
                      else "(matched line by line across the session's results)")
            rows.append(f"{head}\nFound in: …{window}…")
    return H.scrub("\n\n".join(rows))


QUOTES_LABEL = ("## Block quotes in the messages, set against the session's tool results (context, not graded)\n\n"
                "Each block quote (>) a message shows, and the passage of a tool result or of what the leader "
                "pasted that holds it. A quote marked FOUND IN NO TOOL RESULT that a message presents as what a "
                "run, a file or a connection showed is invented (item 6).\n\n")


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
    hist = typed_history(run)
    read += f"{HISTORY_LABEL}\n\n{hist}\n\n" if hist else ""
    supplied = platform_supplied(run)
    read += f"{GROUNDING_LABEL}\n\n{supplied}\n\n" if supplied else ""
    tools = tool_lines(run, msgs)
    shared = shared_lines(run, msgs, tools)
    tools = "\n".join(x for x in (state_lines(run), tools, shared, name_lines(run, msgs)) if x)
    read +=(f"## Lines the AI's own tool calls printed (context, not graded)\n\n````\n{tools}\n````\n\n"
             if tools else "")
    offered = session_tools(run)
    read += f"{TOOLS_LABEL}````\n{offered}\n````\n\n" if offered else ""
    inputs = practice_inputs(run)
    read += f"{INPUTS_LABEL}{inputs}\n\n" if inputs else ""
    docs = platform_docs(run, msgs)
    read += f"{DOCS_LABEL}````\n{docs}\n````\n\n" if docs else ""
    settings = settings_files(run)
    read += f"{SETTINGS_LABEL}````\n{settings}\n````\n\n" if settings else ""
    calls = tool_calls(run)
    read += f"{COMMANDS_LABEL}````\n{calls}\n````\n\n" if calls else ""
    runs = check_runs(run)
    read += f"{CHECK_RUNS_LABEL}````\n{runs}\n````\n\n" if runs else ""
    quotes = quoted_sources(run)
    read += f"{QUOTES_LABEL}````\n{quotes}\n````\n\n" if quotes else ""
    skill = skill_passages(run, msgs)
    read += f"{SKILL_LABEL}````\n{skill}\n````\n\n" if skill else ""
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
