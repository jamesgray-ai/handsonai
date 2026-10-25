#!/usr/bin/env python3
"""Extract framework-evals/approved-lines.json from the private framework spec (one-off; never in CI).

Usage:
  python3 extract_approved_lines.py <spec-dir> [--out FILE]      extract, write, then run the count check
  python3 extract_approved_lines.py <spec-dir> --check [FILE]    count check only, against an existing file

<spec-dir> is the business repo's learning/framework-walkthrough/final/. The spec is private, so
this script runs only on a machine that has it; its output is committed in handsonai and frozen.
Change the corpus only through T03's route (a line approval), then re-run this script.

What it reads (build-task-list T18; rules 2.3):
  - framework-rules.md 12 (shared lines) and 4.2 (the lines routing.md gives);
  - each step's line table: analyze.md 9, deconstruct.md 19, design.md 12, build.md 12 (and its
    "Kept word for word" lines, D12 and the Git save-point offer), test.md 12;
  - lines-to-approve.md (the record of 3c-DJ): the text of every row whose table cell points
    elsewhere ("In 4.2", "Section 3"), and a cross-check of every other row;
  - Deconstruct's approved questions and teaching lines (**Ask:**, *Why*, *Example*, *Not sure?*)
    and its signposts, which live in the body of deconstruct.md, not in a table;
  - the carried lines with fixed wording (rules 8.1's practice-run line, the "All results" label).
  - the "skill's files" sections (analyze 3 and 6, deconstruct 17, design 13, build 15, test 15)
    for `files`: build and test list each line's file; for the others the file follows from
    the section the line is said in (PLACEMENT below records each inference).

One entry per line and form: id, form, text (exact, with [placeholders] and [Label: '…'] clauses
as the spec writes them), kind, skills, files ({skill: file}), source. The count check fails when
any row of any line table, or any row of lines-to-approve.md, has no entry.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

FIVE = ["analyze", "deconstruct", "design", "build", "test"]
SKILL_NAMES = FIVE + ["scaffolding-registry", "indexing-registry"]

# ---------------------------------------------------------------- markdown helpers


def read(spec, name):
    return (spec / name).read_text()


def section_lines(text, head_re, stop_re=r"^## "):
    """The lines after the first heading matching head_re, up to the next heading matching stop_re."""
    lines = text.split("\n")
    for i, l in enumerate(lines):
        if re.match(head_re, l):
            out = []
            for m in lines[i + 1:]:
                if re.match(stop_re, m):
                    break
                out.append(m)
            return out
    raise SystemExit(f"heading not found: {head_re}")


def tables_in(lines):
    """Each markdown table in the lines, as a list of rows (lists of cells), header first."""
    tables, cur = [], None
    for l in lines:
        if l.startswith("|"):
            if cur is None:
                cur = []
                tables.append(cur)
            if re.match(r"^\|[\s\-|:]+\|\s*$", l):
                continue
            cells = re.split(r"(?<!\\)\|", l.strip())[1:-1]
            cur.append([c.strip().replace("\\|", "|") for c in cells])
        else:
            cur = None
    return tables


# ---------------------------------------------------------------- quotes and forms

def scan_quotes(s):
    """Top-level double-quoted strings in a cell, with the text before each (its label).
    Nested quotes ("…mark it "not sized yet", and…") are kept inside: an opening quote follows a
    space or bracket and precedes a non-space; a closing quote follows a non-space."""
    out, depth, start, last_end = [], 0, None, 0
    n = len(s)
    for i, c in enumerate(s):
        if c != '"':
            continue
        prev = s[i - 1] if i > 0 else " "
        nxt = s[i + 1] if i + 1 < n else " "
        if depth == 0:
            if (prev in " ([:\t—" or i == 0) and nxt != " ":
                depth, start = 1, i + 1
                label = s[last_end:i]
        else:
            if prev not in " ([\t":
                depth -= 1
                if depth == 0:
                    out.append((label, s[start:i]))
                    last_end = i + 1
            elif nxt != " ":
                depth += 1
    return out, s[last_end:]


TEACH = {"why": "why", "example": "example", "not sure?": "not-sure", "not sure": "not-sure"}


def strip_parens(s):
    while True:
        t = re.sub(r"\([^()]*\)", "", s)
        if t == s:
            return s
        s = t


def form_name(label, k, used):
    """A short form name from the text before a quote: the clause just before its colon."""
    lab = re.sub(r"\*\*?", "", label)
    m = re.search(r"(Why|Example|Not sure\??)\s*(?:\([^)]*\))?\s*:?\s*$", lab)
    if m:
        name = TEACH[m.group(1).lower().rstrip(":")]
    elif re.fullmatch(r"\s*In 4\.2[.:]?\s*", lab) or (k == 1 and not lab.strip()):
        name = "main"
    elif re.match(r"\s*Model wording, except the promise clause", lab):
        name = "promise clause"
    else:
        flat = strip_parens(lab)
        if ":" in flat:
            before = flat[:flat.rfind(":")]
            clause = re.split(r"(?<=[.;\]])\s+|\[", before)[-1].split(":")[-1]
            clause = re.sub(r",?\s+(?:it\s+)?adds$", "", clause.strip(" ,;[]()"))
            name = clause if len(clause) <= 50 else clause.split(",")[0]
            name = name or f"main-{k}"
        elif re.search(r"\bthen\b", flat, re.I):
            name = "then"
        else:
            name = "main" if k == 1 else f"main-{k}"
    name = re.sub(r"\s+", " ", name).strip() or f"main-{k}"
    base, j = name, 2
    while name in used:
        name = f"{base}-{j}"
        j += 1
    used.add(name)
    return name


def is_fragment(text):
    """A piece of a line (a clause substituted into another form), never checked on its own."""
    t = text.strip()
    return bool(re.match(r"^(…|\.\.\.|,|[a-z])", t)) or t.endswith("…")


def forms_of(cell):
    """(form name, text) for each quoted form in a cell. A short quote with no label of its own after
    the first ("choose Deny", "the path is "done"") is a word the author's note quotes, not a form."""
    quotes, _ = scan_quotes(cell)
    used, out = set(), []
    for k, (label, text) in enumerate(quotes, 1):
        text = text.strip()
        if not text:
            continue
        if k > 1 and not strip_parens(label).rstrip().endswith(":") and len(text.split()) <= 3:
            continue
        out.append((form_name(label, k, used), text))
    return out


# ---------------------------------------------------------------- ids, status, skills

ALIASES = {
    "running work": "running-work", "the running-work message": "running-work",
    "bring-in line": "bring-in-line", "the bring-in line": "bring-in-line",
    "retired line": "retired-line", "the retired line": "retired-line",
    "open-item line": "open-item-line", "the open-item line": "open-item-line",
    "go-live re-check line": "go-live-recheck-line",
    "time-saved line": "time-saved-line", "the time-saved line": "time-saved-line",
    "git save point": "git-save-point", "save point": "git-save-point",
    "the description": "analyze:description",
    "platform fallback": "design:platform-fallback", "confirm-back": "design:confirm-back",
    "n-t6 + n-t7": "N-T6+N-T7",
    '"map" in the backlog question': "deconstruct:map-backlog-question",
    "\"map\" in part 1's after-signpost line": "deconstruct:map-part-1-after-signpost",
}


def norm_id(cell):
    s = re.sub(r"\*\*", "", cell).strip()
    s = re.sub(r"\s*\((?:promise|change form|Claude Code|fallback|no-undo|second-run|golden|bracketed|open point)[^)]*\)\s*$", "", s)
    return ALIASES.get(s.lower(), s)


def approval(status):
    s = status.strip()
    if "3c-DI" in s:
        return "3c-DI (2026-10-24), the wording the decision records"
    if "2026-10-24" in s:
        return "3c-DJ (2026-10-24)" + (", with the line review's change" if "line review" in s else "")
    return "approved before 3c-DJ" + (f" ({s[len('Approved'):].strip(' ,')})" if s.startswith("Approved") and len(s) > 8 else "")


def skills_from(used_by):
    u = used_by.lower()
    out = []
    if "every step" in u or "any step" in u:
        out += FIVE
    for name in SKILL_NAMES:
        if re.search(rf"\b{re.escape(name)}\b", u) and name not in out:
            out.append(name)
    if "built workflow" in u:
        out.append("built-workflow")
    return out


# ---------------------------------------------------------------- placement (files)

ROUTING_LINES = {"N-F3a", "N-F7", "N-F9", "N-F13", "N-B44", "N-T19", "N-T22", "running-work",
                 "bring-in-line", "retired-line", "open-item-line"}
CARRIED = {"N-T20", "N-T21", "time-saved-line", "practice-run-line", "all-results-label"}
BUILD_CARRIED_FILE = "references/carried-lines.md"

# Deconstruct (17) and Design (13) list files by section, not by line: the line's file is the one
# that holds the section it's said in. A line said in more than one part lives in SKILL.md (build
# 15 and test 15's "one home per line"). These are inferences, recorded in each entry's note.
DECONSTRUCT_SECTION_FILES = [
    (r"^5\.1", "references/choosing-a-workflow.md"),
    (r"^5\.3", "references/from-a-document.md"),
    (r"^8\.part-1", "references/part-1-what-this-is-worth.md"),
    (r"^8\.part-2", "references/part-2-scope-and-a-name.md"),
    (r"^8\.part-3", "references/part-3-the-outcome.md"),
    (r"^8\.part-4", "references/part-4-the-path.md"),
    (r"^8\.part-5", "references/part-5-rules-sources-and-practice-runs.md"),
    (r"^9", "references/requirements-template.md"),
    (r"^10", "references/light-track.md"),
    (r"^11", "references/re-runs.md"),
    (r"^12", "references/requirements-template.md"),
    (r"^15", "references/personal-life.md"),
]
DECONSTRUCT_TABLE_FILES = {
    "N-D2": "SKILL.md", "N-D17": "SKILL.md", "N-D3": "SKILL.md", "N-D4": "SKILL.md", "N-D5": "SKILL.md",
    "N-D6": "references/part-2-scope-and-a-name.md", "N-D7": "SKILL.md",
    "N-D8": "references/part-4-the-path.md", "N-D9": "SKILL.md",
    "N-D10": "references/requirements-template.md",
    "N-D11": "SKILL.md",  # said in Part 5 (full) and 10.1 (light): one home, SKILL.md
    "N-D12": "references/part-5-rules-sources-and-practice-runs.md",
    "N-D13": "references/requirements-template.md",  # 17: requirements-template holds "the preview"
    "N-D14": "SKILL.md", "N-D15": "references/re-runs.md", "N-D16": "references/re-runs.md",
    "N-D18": "references/part-1-what-this-is-worth.md", "N-D19": "references/part-1-what-this-is-worth.md",
    "N-D20": "references/part-3-the-outcome.md", "N-D21": "SKILL.md", "N-D22": "SKILL.md",
    "deconstruct:map-backlog-question": "references/choosing-a-workflow.md",
    "deconstruct:map-part-1-after-signpost": "references/part-1-what-this-is-worth.md",
}
DESIGN_FILES = {  # design 13: SKILL.md holds the entry, opening, four parts, questions, approval and close
    "N-21": "references/updating-the-plan.md", "N-23": "references/updating-the-plan.md",
    "N-25": "references/updating-the-plan.md", "N-28": "references/updating-the-plan.md",
    "N-29": "references/updating-the-plan.md",
    "D10": "references/capability-domains.md",  # the Autonomy Summary for decomposition: domains
}
ANALYZE_REFERENCE_FILES = {
    "N-A4": "references/the-walk.md",
    "N-A5": "references/the-walk.md",
    "N-A8": "references/report-format.md",
}
ANALYZE_FILES = {"N-A7": ("scaffolding-registry", "references/interview-guide.md")}


def parse_file_table(spec, name, skill):
    """build 15 / test 15: {line id: file} from the 'Approved lines it holds' column."""
    lines = section_lines(read(spec, name), r"^## 15\. The skill's files")
    t = tables_in(lines)[0]
    out = {}
    for row in t[1:]:
        f = row[0].strip("` ").split("`, `")[0]
        held = row[3]
        if f == "references/routing.md":
            continue  # the 4.2 lines: routing.md, set for every skill below
        held = held.replace("N-T6 + N-T7", "N-T6+N-T7")
        for i in re.findall(r"N-[A-Z]+\d+[a-z]?(?:\+N-T7)?", held):
            out.setdefault(i, f)
        low = held.lower()
        for phrase, i in (("git save-point", "git-save-point"), ("git save point", "git-save-point"),
                          ("go-live re-check line", "go-live-recheck-line"),
                          ("time-saved line", "time-saved-line"), ("practice run: nothing", "practice-run-line")):
            if phrase in low:
                out.setdefault(i, f)
    return out


def files_for(entry_id, skills, form, spec_ctx, section=None):
    """{skill: file} and a note when the placement is inferred."""
    files, notes = {}, []
    for sk in skills:
        if sk == "built-workflow":
            files["build"] = BUILD_CARRIED_FILE
            continue
        if entry_id in ROUTING_LINES and not (entry_id == "N-T19" and form.startswith("inside")):
            files[sk] = "references/routing.md"
            continue
        if sk == "build":
            f = spec_ctx["build_files"].get(entry_id)
            files[sk] = f or "SKILL.md"
            if not f:
                notes.append("build: not in build 15's table; SKILL.md (said throughout)")
        elif sk == "test":
            f = spec_ctx["test_files"].get(entry_id)
            files[sk] = f or "SKILL.md"
            if not f:
                notes.append("test: not in test 15's table; SKILL.md (said throughout)")
        elif sk == "deconstruct":
            f = DECONSTRUCT_TABLE_FILES.get(entry_id)
            if not f and section:
                f = next((ff for pat, ff in DECONSTRUCT_SECTION_FILES if re.match(pat, section)), "SKILL.md")
            files[sk] = f or "SKILL.md"
            notes.append(f"deconstruct: inferred from deconstruct 17 by section {section or '(table row)'}")
        elif sk == "design":
            files[sk] = DESIGN_FILES.get(entry_id, "SKILL.md")
            notes.append("design: inferred from design 13 by section")
        elif sk == "analyze":
            # analyze 4, "The skill's own files" (3c-DQ): the walk and the report format moved
            # into references; every other Analyze line stays in SKILL.md.
            files[sk] = ANALYZE_REFERENCE_FILES.get(entry_id, "SKILL.md")
        elif sk == "indexing-registry":
            files[sk] = "SKILL.md"
        elif sk == "scaffolding-registry":
            files[sk] = "SKILL.md"
            notes.append("scaffolding-registry: asked before it writes anything (analyze 6 item 3); SKILL.md inferred")
    if entry_id in ANALYZE_FILES:
        sk, f = ANALYZE_FILES[entry_id]
        files = {sk: f}
    return files, "; ".join(notes)


# ---------------------------------------------------------------- kinds

TEACHING_IDS = {"N-0", "N-B1", "N-T1", "N-D9", "N-D2", "N-D17", "N-1", "N-3", "N-8", "N-10", "N-15", "N-19",
                "D3′", "D8′", "B54", "N-A1", "N-A3", "N-A6", "N-A7", "D12", "design:confirm-back",
                "analyze:description", "deconstruct:description", "build:description", "test:description",
                "deconstruct:map-part-1-after-signpost", "N-D20", "N-D13"}
STRUCTURE_IDS = {"D10", "analyze:description", "deconstruct:description", "build:description", "test:description"}


def kind_of(entry_id, form, text, skills):
    if "built-workflow" in skills or entry_id in CARRIED:
        return "carried"
    if entry_id in STRUCTURE_IDS:
        return "structure"
    if form in ("why", "example", "not-sure"):
        return "teaching"
    if entry_id.startswith("deconstruct:signpost") or entry_id in TEACHING_IDS:
        return "teaching"
    if "?" in re.sub(r"\[[^\]]*\]", "", text):
        return "question"
    return "safety or promise"


# ---------------------------------------------------------------- extraction

TABLES = [  # (file, heading regex, table index, columns: id, used-by or None, text, status, label)
    ("framework-rules.md", r"^## 12\. Shared scripted lines", 0, (0, 1, 3, 4), "framework-rules.md 12"),
    ("analyze.md", r"^## 9\. Lines the leader sees", 0, (0, None, 2, 3), "analyze.md 9"),
    ("deconstruct.md", r"^## 19\. Lines the leader sees", 0, (0, None, 2, 3), "deconstruct.md 19"),
    ("design.md", r"^## 12\. Design's lines", 0, (0, None, 2, 3), "design.md 12"),
    ("build.md", r"^## 12\. Lines the leader sees", 0, (0, None, 2, 3), "build.md 12"),
    ("test.md", r"^## 12\. Lines the leader sees", 0, (0, None, 2, 3), "test.md 12"),
]
STEP_OF = {"analyze.md": "analyze", "deconstruct.md": "deconstruct", "design.md": "design",
           "build.md": "build", "test.md": "test"}
LTA_SECTIONS = [r"^## Shared lines", r"^## Analyze", r"^## Deconstruct", r"^## Design", r"^## Build", r"^## Test",
                r"^## Registry skills"]


def table_rows(spec):
    """Every row of every line table: (table label, id, used-by, cell text, status, step)."""
    rows = []
    for fname, head, idx, (ci, cu, ct, cs), label in TABLES:
        t = tables_in(section_lines(read(spec, fname), head))[idx]
        for r in t[1:]:
            rows.append({"table": label, "id": norm_id(r[ci]), "used_by": r[cu] if cu is not None else None,
                         "cell": r[ct], "status": r[cs], "step": STEP_OF.get(fname)})
    return rows


def lta_rows(spec):
    text = read(spec, "lines-to-approve.md")
    rows = []
    for h in LTA_SECTIONS:
        t = tables_in(section_lines(text, h))[0]
        for r in t[1:]:
            rows.append({"table": "lines-to-approve.md " + h.strip("^# "), "id": norm_id(r[0]), "cell": r[2]})
    return rows


def qn(s):
    s = (s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
         .replace("–", "-").replace("—", "-").replace(" ", " ").replace("**", "").replace('"', "'"))
    return re.sub(r"\s+", " ", s).strip()


def deconstruct_body(spec):
    """Approved questions, teaching lines and signposts in deconstruct.md's body (sections 3-15)."""
    lines = read(spec, "deconstruct.md").split("\n")
    sec, out, last_ask = "", [], None
    counters = {}
    for ln, l in enumerate(lines, 1):
        m = re.match(r"^## (\d+)\.", l)
        if m:
            sec = m.group(1)
            if int(sec) >= 16:
                break
            continue
        m = re.match(r"^### (\d+\.\d+)", l)
        if m:
            sec = m.group(1)
            continue
        m = re.match(r"^### Part (\d): ", l)
        if m:
            sec = f"8.part-{m.group(1)}"
            continue
        if not sec or sec in ("1", "2"):
            continue
        sm = re.match(r'^Signpost: (.*)$', l)
        if sm:
            qs, _ = scan_quotes(sm.group(1))
            part = re.search(r"Part (\d) of 5", qs[0][1]).group(1)
            out.append({"id": f"deconstruct:signpost-part-{part}", "form": "main", "text": qs[0][1],
                        "section": "8", "line": ln})
            if len(qs) > 1:
                out.append({"id": f"deconstruct:signpost-part-{part}", "form": "after-signpost", "text": qs[1][1],
                            "section": sec, "line": ln})
            continue
        for am in re.finditer(r"\*\*Ask:\*\* (?=\")", l):
            qs, _ = scan_quotes(l[am.end():])
            if not qs:
                continue
            counters[sec] = counters.get(sec, 0) + 1
            last_ask = {"id": f"deconstruct:{sec}:q{counters[sec]}", "form": "main", "text": qs[0][1].strip(),
                        "section": sec, "line": ln}
            out.append(last_ask)
        tm = re.match(r"^\s*- \*(Why|Example|Not sure\?):?\*(?: \(\*\*([^*]+)\*\*\))?:?\s+(.*)$", l)
        if tm and last_ask is not None:
            out.append({"id": last_ask["id"], "form": TEACH[tm.group(1).lower()], "text": tm.group(3).strip(),
                        "section": last_ask["section"], "line": ln, "via": tm.group(2)})
    return out


def descriptions(spec):
    """The approved skill descriptions (structure: they show in skill lists)."""
    out = []
    for fname, sid, head in (("analyze.md", "analyze:description", r"^## 3\. The flow"),
                             ("deconstruct.md", "deconstruct:description", r"^## 17\. The skill's files"),
                             ("build.md", "build:description", r"^## 15\. The skill's files"),
                             ("test.md", "test:description", r"^## 15\. The skill's files")):
        body = section_lines(read(spec, fname), head)
        for i, l in enumerate(body):
            if re.match(r"^\*\*The description\*\*", l):
                q = next(x for x in body[i + 1:] if x.startswith("> "))
                out.append({"id": sid, "text": q[2:].strip(), "step": STEP_OF[fname],
                            "source": f"{fname} {head.split()[1]} (the description)"})
                break
    return out


def build_kept(spec):
    """build.md 12's "Kept word for word" bullets: D12 and the Git save-point offer."""
    body = section_lines(read(spec, "build.md"), r"^## 12\. Lines the leader sees")
    out = []
    for l in body:
        if l.startswith("- D12:"):
            qs, _ = scan_quotes(l)
            out.append(("D12", "main", qs[0][1]))
            out.append(("D12", "each line", qs[1][1]))
        if l.startswith("- The Git save-point offer:"):
            qs, _ = scan_quotes(l)
            out.append(("git-save-point", "main", qs[0][1]))
    return out


def routing_text(spec):
    lines = read(spec, "framework-rules.md").split("\n")
    a = next(i for i, l in enumerate(lines) if "<!-- routing.md: begin -->" in l)
    b = next(i for i, l in enumerate(lines) if "<!-- routing.md: end -->" in l)
    return "\n".join(lines[a + 1:b])


def extract(spec):
    spec_ctx = {"build_files": parse_file_table(spec, "build.md", "build"),
                "test_files": parse_file_table(spec, "test.md", "test")}
    rows = table_rows(spec)
    lta = lta_rows(spec)
    lta_by_id = {}
    for r in lta:
        lta_by_id.setdefault(r["id"], []).append(r)
    entries, warnings = [], []
    shared_skills = {}

    def add(eid, form, text, skills, source, section=None, note=""):
        files, fnote = files_for(eid, skills, form, spec_ctx, section)
        e = {"id": eid, "form": form, "text": text, "kind": kind_of(eid, form, text or "", skills),
             "skills": skills, "files": files, "source": source}
        if text and is_fragment(text):
            e["fragment"] = True
        n = "; ".join(x for x in (note, fnote) if x)
        if n:
            e["note"] = n
        entries.append(e)

    # 1. every row of every line table
    for r in rows:
        eid = r["id"]
        skills = skills_from(r["used_by"]) if r["used_by"] is not None else [r["step"]]
        if eid == "N-A7":
            skills = ["scaffolding-registry"]
        if eid == "git-save-point":
            skills = ["design", "test"]
        shared_skills[eid] = skills
        forms = forms_of(r["cell"])
        src = f"{r['table']}; {approval(r['status'])}"
        if eid == "N-T19":  # the table gives only the built workflow's inside openers
            forms = [("inside" if f == "main" else "inside: " + f, t) for f, t in forms]
        pointer = re.match(r"^\s*(In 4\.2|Section \d+|The approved lines)", r["cell"])
        lt = lta_by_id.get(eid)
        if lt:
            # lines-to-approve.md is the approval's record: a row that points elsewhere takes its text
            # from there, and a form the line table only sketches ("…in a new session…") is added whole
            lforms = forms_of(lt[0]["cell"])
            if pointer and not pointer.group(1).startswith("In 4.2"):
                forms = lforms
                src += "; text from lines-to-approve.md"
            else:
                have = {qn(t) for _, t in forms}
                names = {x for x, _ in forms}
                extra = [(f if f not in names else f + " (lines-to-approve)", t)
                         for f, t in lforms if qn(t) not in have and not any(qn(t) in h for h in have)]
                if extra:
                    forms += extra
                    src += "; forms added from lines-to-approve.md: " + ", ".join(f for f, _ in extra)
        if not forms:
            warnings.append(f"{eid}: no wording in {r['table']} (the row is a rule, not a line): {r['cell'][:80]!r}")
            add(eid, "none", None, skills, src, note="No line to say: " + r["cell"])
            continue
        for form, text in forms:
            sk = skills
            if eid == "N-T19" and form.startswith("inside"):
                sk = ["built-workflow"]
            add(eid, form, text, sk, src)

    # 2. lines-to-approve rows with no line-table row (Deconstruct's two "map" rewordings)
    table_ids = {r["id"] for r in rows}
    for r in lta:
        if r["id"] not in table_ids:
            if "Registry skills" in r["table"]:
                sk, src = ["indexing-registry"], "3c-DP (2026-10-24), build T31 from eval IR1"
            else:
                sk, src = ["deconstruct"], "3c-DJ (2026-10-24), open point 20"
            for form, text in forms_of(r["cell"]):
                add(r["id"], form, text, sk, f"{r['table']}; {src}")

    # 3. cross-check: every lines-to-approve form is in the corpus under its id
    have = {}
    for e in entries:
        if e["text"]:
            have.setdefault(e["id"], set()).add(qn(e["text"]))
    for r in lta:
        for form, text in forms_of(r["cell"]):
            if qn(text) not in have.get(r["id"], set()):
                warnings.append(f"lines-to-approve {r['id']} form {form!r} differs from the line table: {text[:90]!r}")

    # 4. build's kept-word-for-word lines (D12; the Git offer already has a row via design/test)
    for eid, form, text in build_kept(spec):
        if eid == "git-save-point":
            continue
        add(eid, form, text, ["build"], "build.md 12, Kept word for word; approved before 3c-DJ")

    # 5. Deconstruct's approved questions, teaching lines and signposts (its body)
    known = {}
    for e in entries:
        if "deconstruct" in e["skills"] and e["text"]:
            known[qn(e["text"])] = e["id"]
    seen_alias = {}
    for b in deconstruct_body(spec):
        q = qn(b["text"])
        bid = b["id"]
        if bid in seen_alias:
            bid = seen_alias[bid]
        if b["form"] == "main" and q in known:
            seen_alias[b["id"]] = known[q]
            continue
        if b["form"] != "main" and qn(b["text"]) in known and known[qn(b["text"])] == bid:
            continue
        if b["form"] != "main" and any(e["id"] == bid and e["form"] == b["form"] for e in entries):
            continue
        add(bid, b["form"], b["text"], ["deconstruct"],
            f"deconstruct.md {b['section']} (line {b['line']}); approved: 'every other quoted line in this document is approved' (19)",
            section=b["section"])

    # 6. the descriptions, the carried practice-run line and the "All results" label
    for d in descriptions(spec):
        if any(e["id"] == d["id"] for e in entries):
            continue
        add(d["id"], "main", d["text"], [d["step"]], d["source"] + "; approved (James, 2026-10-24)")
    add("practice-run-line", "main", "Practice run: nothing will be sent or changed.", ["built-workflow"],
        "framework-rules.md 8.1; build.md 6.4 item 1 (the fixed first line)")
    add("all-results-label", "main", "All results", ["built-workflow"],
        "framework-rules.md 8.1; build.md 6.4 item 1 (the combined block's heading)")

    # 7. routing.md cross-check: each 4.2 line's text is in 4.2
    rt = qn(routing_text(spec))
    for e in entries:
        if e["text"] and not e.get("fragment") and e["id"] in ROUTING_LINES and "references/routing.md" in e["files"].values():
            core = re.split(r"\[[^\]]*\]", e["text"])
            longest = max(core, key=len).strip()
            if len(longest) > 20 and qn(longest) not in rt:
                warnings.append(f"{e['id']} form {e['form']!r}: not found in rules 4.2: {longest[:80]!r}")
    return entries, rows, lta, warnings


# ---------------------------------------------------------------- count check

def count_check(spec, corpus):
    rows = table_rows(spec)
    lta = lta_rows(spec)
    ids = {e["id"] for e in corpus["lines"]}
    missing = [f"{r['table']}: {r['id']}" for r in rows if r["id"] not in ids]
    missing += [f"{r['table']}: {r['id']}" for r in lta if r["id"] not in ids]
    by_table = {}
    for r in rows:
        by_table.setdefault(r["table"], [0, 0])
        by_table[r["table"]][0] += 1
        by_table[r["table"]][1] += r["id"] in ids
    by_step = {}
    for e in corpus["lines"]:
        for s in e["skills"]:
            by_step.setdefault(s, [set(), 0])
            by_step[s][0].add(e["id"])
            by_step[s][1] += 1
    print("Count check against the spec's line tables:")
    for t, (n, ok) in by_table.items():
        print(f"  {t}: {ok} of {n} rows have an entry")
    print(f"  lines-to-approve.md: {sum(r['id'] in ids for r in lta)} of {len(lta)} rows have an entry")
    print("Entries per skill (lines / line-and-form entries):")
    for s in FIVE + ["scaffolding-registry", "indexing-registry", "built-workflow"]:
        if s in by_step:
            print(f"  {s}: {len(by_step[s][0])} lines, {by_step[s][1]} entries")
    kinds = {}
    for e in corpus["lines"]:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print(f"Total: {len({e['id'] for e in corpus['lines']})} lines, {len(corpus['lines'])} entries; kinds {kinds}")
    if missing:
        print(f"COUNT CHECK FAILED: {len(missing)} row(s) with no entry:")
        for m in missing:
            print("  ", m)
        return 1
    print("COUNT CHECK PASSED")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec_dir")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "approved-lines.json"))
    ap.add_argument("--check", nargs="?", const="", default=None,
                    help="count check only, against FILE (default: --out)")
    a = ap.parse_args()
    spec = Path(a.spec_dir).expanduser().resolve()
    if not (spec / "framework-rules.md").exists():
        sys.exit(f"{spec} is not the framework spec folder (no framework-rules.md)")
    if a.check is not None:
        corpus = json.loads(Path(a.check or a.out).read_text())
        sys.exit(count_check(spec, corpus))
    entries, rows, lta, warnings = extract(spec)
    digests = {n: hashlib.sha256((spec / n).read_bytes()).hexdigest()[:16]
               for n in ("framework-rules.md", "analyze.md", "deconstruct.md", "design.md", "build.md",
                         "test.md", "lines-to-approve.md")}
    corpus = {
        "meta": {
            "what": "Every approved scripted line and form of the AI Workflow Framework 10.0.0 (rules 2.3), "
                    "the corpus the quote check reads. Dev-only: never shipped in the plugin.",
            "generated_by": "framework-evals/tools/extract_approved_lines.py <spec-dir>",
            "spec": "business repo, learning/framework-walkthrough/final/ (private)",
            "spec_digests": digests,
            "frozen": "2026-10-24, after the line approval (3c-DJ); change only through T03's route",
            "placeholders": "[...] is filled when the line is said and matches anything; [Label: '...'] is "
                            "a clause said only in that case (optional); ... and … are elisions",
            "kinds": ["question", "safety or promise", "teaching", "carried", "structure"],
            "files": "per skill, the one file that holds the line (analyze 3 and 6, deconstruct 17, design 13, "
                     "build 15, test 15); references/routing.md for the lines rules 4.2 gives; "
                     "build's references/carried-lines.md for the carried lines",
            "extraction_warnings": warnings,
        },
        "lines": entries,
    }
    Path(a.out).write_text(json.dumps(corpus, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {a.out}: {len(entries)} entries")
    if warnings:
        print(f"{len(warnings)} extraction warning(s):")
        for w in warnings:
            print("  ", w)
    sys.exit(count_check(spec, corpus))


if __name__ == "__main__":
    main()
