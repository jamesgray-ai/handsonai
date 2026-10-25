#!/usr/bin/env python3
"""The approved-lines corpus (approved-lines.json) and the matching every scripted check uses.

Never reads the skills: scripted lines are checked against the corpus only (rules 2.3).

- `[...]` in a line's text is a placeholder, filled when the line is said: it matches anything.
- `[Label: '…']` is a clause said only in that case: it matches its own text or nothing.
- `…` (and `...`) is an elision: it matches anything.
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
            if m and "' / " not in m.group(2) and "'; " not in m.group(2):
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


def _lit_regex(lit):
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
    lead = r"\s*" if lit[:1].isspace() else ""
    trail = r"\s*" if lit[-1:].isspace() else ""
    return lead + r"\s+".join(parts) + trail


def to_regex(toks):
    out = []
    for t in toks:
        if t[0] == "lit":
            out.append(_lit_regex(t[1]))
        elif t[0] == "hole":
            out.append(r".*?")
        else:
            out.append("(?:" + to_regex(t[1]) + ")?")
    return "".join(out)


def capture_regex(toks, names):
    """A regex for a line whose holes named in `names` ({bracket text: group name}) capture what
    filled them; other holes and optional clauses match as usual."""
    out = []
    for t in toks:
        if t[0] == "lit":
            out.append(_lit_regex(t[1]))
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
        self.toks = tokens(self.text) if self.text else []
        self._rx = None
        self.segments = [s for s in (words(x) for x in literal_segments(self.toks)) if s]

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
        longest = max((norm(x) for x in literal_segments(self.toks)), key=len, default="")
        if longest and _pre(longest) not in _pre(nm):
            return False
        return bool(self.regex.search(nm))

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


class Corpus:
    def __init__(self, path=DEFAULT_CORPUS):
        data = json.loads(Path(path).read_text())
        self.meta = data.get("meta", {})
        self.lines = [Line(e) for e in data["lines"]]
        # a platform's own refuse label fills a line's "choose Deny" (3c-DW: "Cancel" in Copilot Cowork);
        # derived forms name no file, so the placement check has nothing to place for them
        for e in data["lines"]:
            for label, platform in PLATFORM_REFUSE_LABELS:
                if e.get("text") and "choose Deny" in e["text"]:
                    self.lines.append(Line(dict(e, form=f"{e['form']}, {platform}",
                                                text=e["text"].replace("choose Deny", f"choose {label}"), files={}, derived=True)))
        self.by_id = {}
        for ln in self.lines:
            self.by_id.setdefault(ln.id, []).append(ln)
        self._index = None

    def get(self, line_id, form=None):
        forms = self.by_id.get(line_id, [])
        return [f for f in forms if form is None or f.form == form]

    def checkable(self):
        return [ln for ln in self.lines if ln.text and not ln.fragment]

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
        """Word spans in ws where some fixed run of some line appears exactly."""
        spans = []
        idx = self.index()
        for i in range(len(ws) - 2):
            for ln, k in idx.get(("head", tuple(ws[i:i + 3])), []):
                seg = ln.segments[k]
                if ws[i:i + len(seg)] == seg:
                    spans.append((i, i + len(seg)))
        return spans

    def said_spans(self, message):
        """Word spans of the message where some approved form is said in full (placeholders filled)."""
        nm = norm(message)
        low = nm.lower()
        starts = [m.start() for m in WORD.finditer(nm)]
        spans = []
        for ln in self.checkable():
            longest = max((norm(x) for x in literal_segments(ln.toks)), key=len, default="")
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
                    if _edge_word_only(seg, win) or _start_phrase_only(seg, win):
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
            segs = [norm(x) for x in literal_segments(ln.toks)]
            longest = max(segs, key=len, default="")
            if not longest or _pre(longest) not in _pre(low):
                continue
            nm = ln.regex.sub(lambda m: _holes_only(ln, m.group(0)) if keep_fills else " ", nm)
            low = nm.lower()
        return nm


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
