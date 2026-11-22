#!/usr/bin/env python3
"""The approved-lines corpus (approved-lines.json) and the matching every scripted check uses.

Never reads the skills: scripted lines are checked against the corpus only (rules 2.3).

- `[...]` in a line's text is a placeholder, filled when the line is said: it matches anything.
- `[Label: '…']` is a clause said only in that case: it matches its own text or nothing.
- `…` (and `...`) is an elision: it matches anything.
- An entry with `"retired"` (when and why) is no longer approved: the corpus leaves it out.
- A list of options where some are marked "only where…" (N-14) is said with only the options that
  apply, so the whole list is one placeholder.
- Text is compared after `norm`: curly and straight quotes alike, single and double quotes alike,
  dashes alike, `**`/backticks dropped, whitespace collapsed.
- Between clauses, a semicolon and a full stop match each other ("how it should go; until" and
  "how it should go. Until"): a `;` ending a word, or a `.` ending a word with another word after
  it, matches either mark. Every other mark is exact; a colon above all, since a line like N-T25's
  ": say" is how a slot stuffed with whole sentences is caught.

`Corpus.near_misses(message)` is the quote check's core: every run of six or more fixed words from a
line that appears in a message with one or two words changed, where no approved form appears exactly
there. That is a scripted line said wrong. Given the skill under test, it looks only at that skill's
lines (and the built workflow's), and it skips a run under SHORT_RUN_WORDS words whose only change
is its first or last word: what's left is a common phrase, not a scripted line.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CORPUS = HERE / "approved-lines.json"
MIN_SEGMENT_WORDS = 6
SHORT_RUN_WORDS = 8

# final-build-2 (2026-11-22, James): word for word is kept only for the lines that protect the leader. A line is
# strict when it carries a safety cue below (a button to choose, an approval, what can't be undone, a pause, a
# kept copy, a delete or overwrite, regulated or confidential content, a password or key) or is a line every
# built part carries. Any other line may be said with a word or two changed (cap as near_misses), unless the
# change touches a protected word: a negation, "only", a button name, a number, a sentence mark or a start
# phrase's words.
STRICT_CUES = re.compile(r"\b(?:Deny|Allow once|Always allow|allow|approv\w*|undone|undo|hard block|practice run|"
                         r"pause\w*|a copy|delet\w*|overwrit\w*|regulat\w*|confidential|sensitive|password)\b", re.I)
PUNCT_WORD = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?|[.:;?!]")
PROTECTED = {".", ":", ";", "?", "!", "not", "no", "never", "don't", "won't", "can't", "isn't", "aren't", "nothing", "only", "deny",
             "allow", "always", "once", "stop",
             # a start phrase stays exact: its step, "skill", "run" and the routing words
             "analyze", "deconstruct", "design", "build", "test", "skill", "run", "change", "continue", "workflow", "my"}


def _pwords(s):
    """Words and sentence marks (. : ; ? !), lower-cased: a loose match keeps a line's sentences as they are."""
    return [w.lower() for w in PUNCT_WORD.findall(norm(s))]


def _protected_change(seg, win):
    """True when the edit from seg to win adds, drops or swaps a protected word or a number."""
    key = lambda ws: sorted(w for w in ws if w in PROTECTED or any(ch.isdigit() for ch in w))
    return key(seg) != key(win)


def norm(s):
    s = (s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
         .replace("—", "-").replace("–", "-").replace(" ", " ").replace("…", "…"))
    s = s.replace("**", "").replace("`", "").replace('"', "'")
    return re.sub(r"\s+", " ", s).strip()


WORD = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")


def words(s):
    return [w.lower() for w in WORD.findall(norm(s))]


# ---------------------------------------------------------------- parsing a line's text

def _match_bracket(s, i):
    """Index of the ']' closing the '[' at s[i], counting nested brackets."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "[":
            depth += 1
        elif s[j] == "]":
            depth -= 1
            if depth == 0:
                return j
    return -1


LABEL_CLAUSE = re.compile(r"^\s*([A-Z][^:\[\]']{0,60}):\s*'(.*)'\s*$", re.S)
LABEL_ALTS = re.compile(r"\s*[A-Z][^:\[\]']{0,60}:\s*'(.*?)'(?=\s+[A-Z][^:\[\]']{0,60}:\s*'|\s*$)", re.S)


def tokens(text):
    """[('lit', str) | ('hole',) | ('opt', tokens)] for a line's text."""
    out, buf, i = [], [], 0
    s = text
    while i < len(s):
        c = s[i]
        if c == "[":
            j = _match_bracket(s, i)
            if j < 0:
                buf.append(c)
                i += 1
                continue
            if buf:
                out.append(("lit", "".join(buf)))
                buf = []
            inner = s[i + 1:j]
            m = LABEL_CLAUSE.match(inner)
            alts = LABEL_ALTS.findall(inner) if m else []
            if len(alts) > 1 and LABEL_ALTS.sub("", inner).strip() == "":
                # "[Can be undone: 'A' Permanent: 'B']": one labelled clause or the other, each optional
                out += [("opt", tokens(a)) for a in alts]
            elif m and "' / " not in m.group(2) and "'; " not in m.group(2):
                out.append(("opt", tokens(m.group(2))))
            else:
                out.append(("hole", inner))
            i = j + 1
            continue
        if c == "…" or s.startswith("...", i):
            if buf:
                out.append(("lit", "".join(buf)))
                buf = []
            out.append(("hole", "…"))
            i += 1 if c == "…" else 3
            continue
        buf.append(c)
        i += 1
    if buf:
        out.append(("lit", "".join(buf)))
    return _collapse_option_lists(out)


LIST_SEP = re.compile(r"^\s*,?\s*(?:or\s+)?$")
CONDITIONAL = re.compile(r"\bonly (?:where|when|if)\b")


def _collapse_option_lists(toks):
    """A list of options some of which are said only where they apply ("You can [A], [B — only where
    one exists], or [C — only where allowed]") is said with just the options that apply, so its
    commas and "or" can't be fixed words: the run of holes is one hole."""
    out, i = [], 0
    while i < len(toks):
        if toks[i][0] != "hole":
            out.append(toks[i])
            i += 1
            continue
        j = i
        while (j + 2 < len(toks) and toks[j + 1][0] == "lit" and LIST_SEP.match(toks[j + 1][1])
               and toks[j + 2][0] == "hole"):
            j += 2
        run = [t for t in toks[i:j + 1] if t[0] == "hole"]
        if len(run) > 1 and any(CONDITIONAL.search(t[1]) for t in run):
            out.append(("hole", " | ".join(t[1] for t in run)))
        else:
            out += toks[i:j + 1]
        i = j + 1
    return out


# After a hole, a literal "." also matches a fill that ends in a quote with its own mark inside it
# ("…say 'is it ready?'" for "…say [question]."): the full stop is then said inside the quote.
AFTER_HOLE_STOP = r"(?:\.|[.?!]['\"’”])"


def _lit_regex(lit, after_hole=False):
    n = norm(lit)
    if not n:
        return r"\s*" if lit.strip() == "" and lit else ""
    raw = n.split(" ")
    parts = []
    for i, p in enumerate(raw):
        # a semicolon and a full stop between clauses match each other (never a colon or comma)
        if p.endswith(";") and len(p) > 1:
            parts.append(re.escape(p[:-1]) + "[;.]")
        elif p.endswith(".") and len(p) > 1 and i < len(raw) - 1 and WORD.match(raw[i + 1]):
            parts.append(re.escape(p[:-1]) + "[.;]")
        else:
            parts.append(re.escape(p))
    if after_hole and not lit[:1].isspace() and parts and parts[0].startswith(r"\."):
        parts[0] = AFTER_HOLE_STOP + parts[0][2:]
    lead = r"\s*" if lit[:1].isspace() else ""
    trail = r"\s*" if lit[-1:].isspace() else ""
    return lead + r"\s+".join(parts) + trail


def to_regex(toks):
    out = []
    for k, t in enumerate(toks):
        if t[0] == "lit":
            out.append(_lit_regex(t[1], after_hole=k > 0 and toks[k - 1][0] == "hole"))
        elif t[0] == "hole":
            out.append(r".*?")
        else:
            out.append("(?:" + to_regex(t[1]) + ")?")
    return "".join(out)


def capture_regex(toks, names):
    """A regex for a line whose holes named in `names` ({bracket text: group name}) capture what
    filled them; other holes and optional clauses match as usual."""
    out = []
    for k, t in enumerate(toks):
        if t[0] == "lit":
            out.append(_lit_regex(t[1], after_hole=k > 0 and toks[k - 1][0] == "hole"))
        elif t[0] == "hole":
            g = names.get(t[1])
            out.append(f"(?P<{g}>.+?)" if g else r".*?")
        else:
            out.append("(?:" + to_regex(t[1]) + ")?")
    return "".join(out)


def literal_segments(toks):
    """The fixed runs of a line: the literal pieces between holes (optional clauses split runs too)."""
    segs, cur = [], []
    for t in toks:
        if t[0] == "lit":
            cur.append(t[1])
        else:
            if cur:
                segs.append("".join(cur))
                cur = []
            if t[0] == "opt":
                segs += literal_segments(t[1])
    if cur:
        segs.append("".join(cur))
    return segs


# ---------------------------------------------------------------- the corpus

class Line:
    def __init__(self, e):
        self.id, self.form, self.text = e["id"], e["form"], e.get("text")
        self.kind, self.skills, self.files = e.get("kind"), e.get("skills", []), e.get("files", {})
        self.fragment = bool(e.get("fragment"))
        self.derived = bool(e.get("derived"))  # built here from another form, never placed in a skill file
        # a line whose [state] takes only listed phrases (N-F23, the routing lead-in, core round-2 fixes)
        self.states = list(e.get("states", []))
        self.toks = tokens(self.text) if self.text else []
        self._rx = None
        self.segments = [s for s in (words(x) for x in literal_segments(self.toks)) if s]
        # the prefilter's needle: the longest fixed run that must be said (never an optional clause's)
        req = [norm(x) for x in literal_segments([t if t[0] != "opt" else ("hole", "") for t in self.toks])]
        self.longest = max(req, key=len, default="") or max(
            (norm(x) for x in literal_segments(self.toks)), key=len, default="")
        self.strict = self.kind == "carried" or bool(self.text and STRICT_CUES.search(self.text))
        # the fixed runs a loose match needs, with sentence marks kept and optional clauses left out
        self.loose_segments = [s for s in (_pwords(x) for x in literal_segments(
            [t if t[0] != "opt" else ("hole", "") for t in self.toks])) if s]

    @property
    def regex(self):
        if self._rx is None:
            self._rx = re.compile(to_regex(self.toks), re.S | re.I) if self.text else None
        return self._rx

    def matches(self, message):
        """True when this form, its placeholders filled any way, appears in the message."""
        if not self.text:
            return False
        nm = norm(message)
        longest = self.longest
        # the literal's leading stop can sit inside a closing quote in the message ("…owns it.' It
        # changes"), which the regex allows: leave it out of the prefilter (P2-shared-skill, trial 3)
        if longest and _pre(longest).lstrip(".;:, ") not in _pre(nm):
            return False
        return bool(self.regex.search(nm))

    def loose_matches(self, message):
        """A line that isn't strict, said with a word or two changed in its fixed runs (never a protected
        word or a sentence mark, and only in a run of three or more), each run in order: it counts as said.
        Strict lines never match loosely."""
        if self.strict or not self.text or not self.loose_segments:
            return False
        ws, pos = _pwords(message), 0
        for seg in self.loose_segments:
            cap = 1 if len(seg) < 12 else 2
            hit = None
            for a in range(pos, len(ws)):
                for d in sorted(range(-cap, cap + 1), key=abs):
                    L = len(seg) + d
                    if L < 1 or a + L > len(ws):
                        continue
                    win = ws[a:a + L]
                    if win == seg or (len(seg) >= 3 and _edit_distance(seg, win, cap) <= cap
                                      and not _protected_change(seg, win)):
                        hit = a + L
                        break
                if hit is not None:
                    break
            if hit is None:
                return False
            pos = hit
        return True

    def label(self):
        return f"{self.id} ({self.form})"


def _edit_distance(a, b, cap):
    """Word-level Levenshtein distance, stopping early above cap."""
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        best = cur[0]
        for j, y in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y))
            best = min(best, cur[j])
        if best > cap:
            return cap + 1
        prev = cur
    return prev[-1]


PLATFORM_REFUSE_LABELS = [("Cancel", "Copilot Cowork")]
OPTIONAL_STOP_AFTER = {"N-B8": "[the content]"}  # a fill that can be a block-quoted draft (see Corpus)
# A near miss of one line whose words are, exactly, part of another line's fixed run is that other line
# said, not the first one reworded: N-F10's platform forms ("To pick up, start a new session in this
# project and say…", "…open a new chat with your working folder selected and say…") hold the words N-F2's
# forms are fuzzy-matched against ("in a new session in this project and say"). Build rounds 2026-11-18.
SAID_AS = {"N-F2": ("N-F10",)}


def _contains(seq, sub):
    n = len(sub)
    return n > 0 and any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))


class Corpus:
    def __init__(self, path=DEFAULT_CORPUS):
        data = json.loads(Path(path).read_text())
        self.meta = data.get("meta", {})
        # a "retired" entry (its value says when and why) stays in the file as a record only: it is no
        # longer approved, so it is never matched, placed or quoted, and an eval that still names it fails
        self.retired = [e for e in data["lines"] if e.get("retired")]
        data["lines"] = [e for e in data["lines"] if not e.get("retired")]
        # a "clause" entry is part of another line (N-B4's count-one OK clause): only the whole lines
        # built from it below are matched, so it never passes or fails a quote check on its own
        self.lines = [Line(e) for e in data["lines"] if not e.get("clause")]
        # a platform's own refuse label fills a line's "choose Deny" (3c-DW: "Cancel" in Copilot Cowork);
        # derived forms name no file, so the placement check has nothing to place for them
        for e in data["lines"]:
            for label, platform in PLATFORM_REFUSE_LABELS:
                if e.get("text") and "choose Deny" in e["text"]:
                    self.lines.append(Line(dict(e, form=f"{e['form']}, {platform}",
                                                text=e["text"].replace("choose Deny", f"choose {label}"), files={}, derived=True)))
        # N-B8's [the content] is often the draft itself, block-quoted, which ends on its sign-off ("> Alex")
        # with no full stop before "I haven't…": the stop after the content is then optional (Build rounds
        # 2026-11-18, JR-claude-web and JR-chatgpt). Every word stays the approved line's own.
        for e in data["lines"]:
            if e["id"] in OPTIONAL_STOP_AFTER and e.get("text") and not e.get("clause"):
                hole = OPTIONAL_STOP_AFTER[e["id"]]
                if f"{hole}. " in e["text"]:
                    self.lines.append(Line(dict(e, form=f"{e['form']}, content with no full stop",
                                                text=e["text"].replace(f"{hole}. ", f"{hole} ", 1), files={}, derived=True)))
        # a line said "in N-F2's new-chat form" (the bring-in line) has its platform forms approved as
        # fragments of that form ("in a new session", "in a new chat with your working folder selected",
        # "in a new Cowork chat with:…"); the whole line each makes is the same approved line on that platform
        for e in data["lines"]:
            main = next((m for m in data["lines"] if m["id"] == e["id"] and m.get("form") == "main"), None)
            frag = (e.get("text") or "").strip("…").strip()
            if not (e.get("fragment") and main and frag.startswith("in a new ")
                    and "in a new chat with:" in (main.get("text") or "")):
                continue
            text = (main["text"].replace("in a new chat with:", frag.rstrip(":") + ":") if " with" in frag
                    else main["text"].replace("in a new chat with:", frag + " with:"))
            if frag == "in a new session":
                # Claude Code and Codex: N-F2's form there ("in a new session in this project", no location),
                # as the no-location forms below make it; never "in a new session" with the location kept
                text = _no_location(text)
            if any(m["id"] == e["id"] and m.get("text") == text for m in data["lines"]):
                continue  # already approved as a whole line (N-F2's Claude Code and Codex form)
            label = re.sub(r"^In N-F2's platform forms \(", "", e["form"])
            self.lines.append(Line(dict(main, form=f"{label}, whole line", text=text, files={}, derived=True)))
        # On Claude Code and Codex a start phrase carries no location, and "in a new session" reads "in a new
        # session in this project" (rules 4.2): every line that gives '[start phrase]. My files are in
        # [location].' has that form, derived here, unless it is already approved as it is
        for e in data["lines"]:
            src = e.get("text") or ""
            if e.get("fragment") or e.get("clause") or LOCATION_TAIL not in src:
                continue
            # only the platform-neutral forms: a web, desktop or Microsoft 365 form keeps its location
            if re.search(r"(?i)desktop|microsoft 365|cowork|on the web|chatgpt|gemini|cloud", e.get("form") or ""):
                continue
            text = _no_location(src)
            if any(m["id"] == e["id"] and m.get("text") == text for m in data["lines"]):
                continue
            self.lines.append(Line(dict(e, form=f"{e['form']}, Claude Code and Codex (no location)", text=text,
                                        files={}, derived=True)))
        # N-B4's "First I'll need you to … connect [tools], check [a draft] and OK [L] quick real checks
        # and setup changes": "A clause with nothing in it is left out" (build SKILL.md, *The opening*,
        # "Its clauses"). With no draft to check, no tool to connect or nothing to OK, the clause goes and
        # the list closes up; every word that stays is the approved line's own.
        # With [L] at 1 the OK clause takes a count-one form (3c-EC: "OK 1 quick real check", "OK 1 setup
        # change"), approved as fragments; each whole form of N-B4 is approved with it in the clause's place.
        c = "OK [L] quick real checks and setup changes"
        ones = [f for f in data["lines"] if f["id"] == "N-B4" and f.get("clause") and f.get("text")]
        for e in data["lines"]:
            if e["id"] != "N-B4" or not e.get("text") or e.get("clause") or c not in e["text"]:
                continue
            for f in ones:
                self.lines.append(Line(dict(e, form=f"{e['form']}, {f['form']}", text=e["text"].replace(c, f["text"]),
                                            files={}, derived=True)))
        for e in [ln for ln in data["lines"] if not ln.get("clause")] + [dict(id=ln.id, form=ln.form, text=ln.text, kind=ln.kind, skills=ln.skills) for ln in self.lines
                                                if ln.id == "N-B4" and ln.derived]:
            if e["id"] != "N-B4" or not e.get("text"):
                continue
            t = e["text"]
            a, b = "connect [tools]", "check [a draft]"
            ok = next((o for o in [c] + [f["text"] for f in ones] if f"{a}, {b} and {o}" in t), None)
            if ok is None:
                continue
            # Only forms that end on the fixed OK clause: one whose list ended on a hole
            # ("connect [tools]; then…") would let that hole swallow a reworded OK clause.
            for name, repl in (("no draft", f"{a} and {ok}"), ("nothing to connect", f"{b} and {ok}"),
                               ("only OKs", ok)):
                self.lines.append(Line(dict(e, form=f"{e['form']}, {name}", text=t.replace(f"{a}, {b} and {ok}", repl),
                                            files={}, derived=True)))
        self.by_id = {}
        for ln in self.lines:
            self.by_id.setdefault(ln.id, []).append(ln)
        self._index = None

    def get(self, line_id, form=None):
        # a named form includes the variants derived from it ("after an orientation line, no draft":
        # a clause with nothing in it is left out); EN-orientation failed 3/3 on a correct opening
        # with no draft to check (trial 2, 2026-11-20)
        forms = self.by_id.get(line_id, [])
        return [f for f in forms if form is None or f.form == form
                or (getattr(f, "derived", False) and f.form.startswith(form + ", "))]

    def checkable(self):
        return [ln for ln in self.lines if ln.text and not ln.fragment]

    def spannable(self):
        """Every form whose exact saying marks a span as approved: the whole lines, and the fragment forms
        (a fragment said word for word is approved there, so near-miss detection must not flag it)."""
        return [ln for ln in self.lines if ln.text]

    # -- the index of fixed runs, for near misses
    def index(self):
        if self._index is None:
            idx = {}
            for ln in self.checkable():
                for k, seg in enumerate(ln.segments):
                    if len(seg) < MIN_SEGMENT_WORDS:
                        continue
                    idx.setdefault(("head", tuple(seg[:3])), []).append((ln, k))
                    idx.setdefault(("tail", tuple(seg[-3:])), []).append((ln, k))
            self._index = idx
        return self._index

    def exact_spans(self, ws):
        """Word spans in ws where some fixed run of some line (or of a fragment form) appears exactly."""
        spans = []
        idx = self.index()
        for i in range(len(ws) - 2):
            for ln, k in idx.get(("head", tuple(ws[i:i + 3])), []):
                seg = ln.segments[k]
                if ws[i:i + len(seg)] == seg:
                    spans.append((i, i + len(seg)))
        for ln in self.lines:
            if not (ln.fragment and ln.text):
                continue
            for seg in ln.segments:
                if len(seg) < 3:
                    continue
                for i in range(len(ws) - len(seg) + 1):
                    if ws[i:i + len(seg)] == seg:
                        spans.append((i, i + len(seg)))
        return spans

    def said_spans(self, message):
        """Word spans of the message where some approved form is said in full (placeholders filled)."""
        nm = norm(message)
        low = nm.lower()
        starts = [m.start() for m in WORD.finditer(nm)]
        spans = []
        for ln in self.spannable():
            longest = ln.longest
            if not longest or _pre(longest) not in _pre(low):
                continue
            for m in ln.regex.finditer(nm):
                a = sum(1 for p in starts if p < m.start())
                b = sum(1 for p in starts if p < m.end())
                if b > a:
                    spans.append((a, b))
        return spans

    def near_misses(self, message, skill=None):
        """[(line, expected run, found words)] for each fixed run said with a word or two changed,
        where no approved form is said in full there. With `skill`, only lines that skill says
        (or the built workflow says) count."""
        ws = words(message)
        exact = self.exact_spans(ws) + self.said_spans(message)
        found, seen = [], set()
        idx = self.index()
        for i in range(len(ws) - 2):
            for key, anchor in ((("head", tuple(ws[i:i + 3])), "head"), (("tail", tuple(ws[i:i + 3])), "tail")):
                for ln, k in idx.get(key, []):
                    if not _owned(ln, skill):
                        continue
                    seg = ln.segments[k]
                    cap = 1 if len(seg) < 12 else 2
                    best = None
                    for d in sorted(range(-cap, cap + 1), key=abs):
                        L = len(seg) + d
                        if L < 3:
                            continue
                        a = i if anchor == "head" else i + 3 - L
                        if a < 0 or a + L > len(ws):
                            continue
                        win = ws[a:a + L]
                        if win == seg:
                            best = None
                            break
                        dist = _edit_distance(seg, win, cap)
                        if 0 < dist <= cap and (best is None or dist < best[0]):
                            best = (dist, a, L, win)
                    if best is None:
                        continue
                    _, a, L, win = best
                    if not ln.strict and not _protected_change(seg, win):
                        continue
                    if _edge_word_only(seg, win) or _start_phrase_only(seg, win):
                        continue
                    if len(seg) < SHORT_RUN_WORDS and best[0] == 1 and not _rest_said(ln, k, ws):
                        continue
                    # only when that other line is actually said here (review H4, 2026-11-21)
                    if any(_contains(s2, win) and _contains(ws, s2) for other in SAID_AS.get(ln.id, ())
                           for o in self.by_id.get(other, []) for s2 in o.segments):
                        continue
                    if any(min(a + L, e) - max(a, s) >= min(L, e - s) * 0.5 for s, e in exact):
                        continue
                    sig = (ln.id, k, a)
                    if sig in seen:
                        continue
                    seen.add(sig)
                    found.append((ln, " ".join(seg), " ".join(win)))
        # one report per place: keep the closest line for each start position
        best = {}
        for ln, exp, got in found:
            key = got
            if key not in best or len(exp) > len(best[key][1]):
                best[key] = (ln, exp, got)
        return list(best.values())

    def strip_approved(self, message, keep_fills=True):
        """The message with every approved line's text removed, so the vocabulary and time checks
        see only model wording (and, with keep_fills, what filled the placeholders)."""
        nm = norm(message)
        low = nm.lower()
        for ln in self.checkable():
            longest = ln.longest
            if not longest or _pre(longest) not in _pre(low):
                continue
            nm = ln.regex.sub(lambda m: _holes_only(ln, m.group(0)) if keep_fills else " ", nm)
            low = nm.lower()
        return nm


LOCATION_TAIL = ". My files are in [location].'"


def _no_location(text):
    """A line's Claude Code and Codex form: its start phrases end at the phrase, and a new session is in this project."""
    text = text.replace(LOCATION_TAIL, ".'")
    return re.sub(r" in a new session(?! in this project)", " in a new session in this project", text)


def _pre(s):
    """The cheap substring prefilter's form: lower case, with `;` read as `.` (they match each other
    between clauses; see _lit_regex)."""
    return s.lower().replace(";", ".")


def _owned(ln, skill):
    """A line counts for the skill under test when that skill (or the built workflow) says it.
    No skill given, or a line naming no skill: it counts."""
    return not skill or not ln.skills or skill in ln.skills or "built-workflow" in ln.skills


def _edge_word_only(seg, win):
    """A short run whose only change is its first or last word: the rest is a common phrase."""
    if len(seg) >= SHORT_RUN_WORDS or len(win) != len(seg):
        return False
    return win[1:] == seg[1:] or win[:-1] == seg[:-1]


# fixed runs every routing line shares ("…. My files are in [location].'"): saying them is no sign that
# a particular line was said
COMMON_RUNS = {("my", "files", "are", "in")}


def _run_said(seg, ws):
    """The run is in ws word for word or, when it is six words or more, with a word or two changed."""
    if _contains(ws, seg):
        return True
    if len(seg) < MIN_SEGMENT_WORDS:
        return False
    cap = 1 if len(seg) < 12 else 2
    for L in range(max(1, len(seg) - cap), len(seg) + cap + 1):
        for a in range(0, len(ws) - L + 1):
            if ws[a] not in seg and ws[a + L - 1] not in seg:
                continue
            if _edit_distance(seg, ws[a:a + L], cap) <= cap:
                return True
    return False


def _rest_said(ln, k, ws):
    """build-full-1 fix (2026-11-21): a short run (under SHORT_RUN_WORDS words) said with one word changed
    is that line reworded only when something else of the line was said too: another of its fixed runs of
    three words or more (not a run every routing line shares) appears in the message. "and leave everything
    as it is" alone is not N-B14 ("…I'll redo just that…, and leave everything else as it is"), nor "I'll pick
    up here next time" N-B9, nor "In the new chat, add your Google Drive" N-F2. A line with no other such
    run (the short run is the line) is still flagged."""
    others = [seg for j, seg in enumerate(ln.segments) if j != k and len(seg) >= 3 and tuple(seg) not in COMMON_RUNS]
    if not others:
        return True
    return any(_run_said(seg, ws) for seg in others)


START_PHRASE = re.compile(r"\bsay (?:run the \w+ skill(?: on \w+)?|test the workflow i built|change my workflow)"
                          r"(?: my files are in)?\b")


def _start_phrase_only(seg, win):
    """A run that shares only a start phrase ("say 'run the design skill. My files are in'") with
    what was said, its other words mostly different: model wording that ends on a start phrase,
    not a scripted line said wrong ("To review it, say…" against "To answer it, say…")."""
    s, w = " ".join(seg), " ".join(win)
    m = START_PHRASE.search(s)
    if not m or m.group(0) not in w:
        return False
    rest_s = (s[:m.start()] + " " + s[m.end():]).split()
    k = w.index(m.group(0))
    rest_w = (w[:k] + " " + w[k + len(m.group(0)):]).split()
    if not rest_s:
        return True
    return _edit_distance(rest_s, rest_w, len(rest_s)) >= max(1, len(rest_s) - 1)


def _holes_only(ln, said):
    """Keep only what filled the placeholders: the fixed words are approved, the fill isn't."""
    out = said
    for seg in sorted((norm(x) for x in literal_segments(ln.toks)), key=len, reverse=True):
        if len(seg) > 2:
            out = re.sub(re.escape(seg), " ", out, flags=re.I)
    return " " + out + " "


@lru_cache(maxsize=4)
def load(path=str(DEFAULT_CORPUS)):
    return Corpus(path)
