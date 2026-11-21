"""Client Follow-Up in the shape today's Deconstruct writes (`Path: none`), laid over a routing-state workspace.

The routing-state library (`framework-fixtures/states/`, `edge/`, `continue/`) holds Client Follow-Up in the
older, step-shaped form (three steps, a `### Decisions` line, a measured Baseline). Every file the redesigned
Deconstruct saves has `Path: none — the AI plans each run from the goal`, no steps and no decisions, the four
glosses, `Used By: All`, a moment for a checkpoint's Where and a write's `after [moment]`, Baseline `— · Unknown`,
and an `expect:` line on each practice input. `client-follow-up/` beside this file is that file and its inputs;
`apply(t)` lays it over a workspace copied from the library, so Design's, Build's and Test's fixture builders
start from what Deconstruct writes now. An eval about an older file keeps the library's step-shaped copy and
says so.

What changes, and only where the workspace holds the library's own copy, so a file a fixture already changed
is never overwritten (for `requirements.md` the body is compared, and a raised `revision` or a `big_change`
in the frontmatter is kept):
- `requirements.md` and `inputs/E1-…`, `inputs/E2-…`: replaced by this folder's. D1 ("asks you for a next
  step before drafting") is the When rule R4; G1's Where is "After the draft is ready"; W1 ends
  `· after the email is drafted`.
- `design-plan.md`: the plan Design writes for a `Path: none` file with planned steps (`Step Pa`, `Step Pb`,
  `Step Pc`, design `drafting.md`); T2 meets R4 and no Step or D line of the requirements; KW builds the flag
  and re-check lines only (no time-saved line: the Baseline is unknown, plan-template.md section 7).
- `build-record.md`: KW's row names the flag and re-check lines.

`add_law(t)` then gives that file a rule and a checkpoint that name a law (R5 and G2, FINRA Rule 2210), as
Deconstruct writes them after a yes to the law question, with the plan, built skill and record to match: the
base of the law evals in Design, Build and Test.

Usage from a builder: `sys.path.insert(0, str(FF / "path-none")); import path_none as PN; PN.apply(t)`.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
FF = HERE.parent
NEW = HERE / "client-follow-up"
OLD = FF / "states" / "s06-build-needed" / "with-registry" / "framework" / "client-follow-up"
CFU = "client-follow-up"

PLAN_SUBS = [
    ("Guided: Step 2 decides how to word the deliverable", "Guided: Step Pb decides how to word the deliverable"),
    ("| Step 1 | Deterministic | ", "| Step Pa — Read the call notes | Deterministic | "),
    ("| Step 2 | Guided | ", "| Step Pb — Draft the email | Guided | "),
    ("| Step 3 | — | — | — | — | Human (no artifact) | G1 | You |",
     "| Step Pc — Review and send | — | — | — | — | Human (no artifact) | G1 | You |"),
    ("1. Read what comes in (Step 1).", "1. Read what comes in (Step Pa)."),
    ("2. Write the deliverable with C1 (Step 2).", "2. Write the deliverable with C1 (Step Pb)."),
    ("- **Covers Steps:** Step 1, Step 2, Step 3", "- **Covers Steps:** Step Pa, Step Pb, Step Pc"),
    ("- **Meets:** Step 1, Step 2, Step 3, D1, AC1, AC2, AC3, R1, R2, R3, G1, W1",
     "- **Meets:** Step Pa, Step Pb, Step Pc, AC1, AC2, AC3, R1, R2, R3, R4, G1, W1"),
    ("- **Builds:** the flag line, the re-check line and the time-saved line in S1",
     "- **Builds:** the flag line and the re-check line in S1"),
]
# the subs every plan built from the library's plan must take (the rest may already be changed by a fixture)
PLAN_REQUIRED = ("| Step 1 | Deterministic | ", "- **Covers Steps:** Step 1, Step 2, Step 3")
RECORD_SUBS = [("flag, re-check and time-saved lines", "flag and re-check lines")]


def body(text):
    """The text after a requirements file's frontmatter (a fixture may have raised the revision)."""
    return text.split("\n---\n", 1)[1] if text.startswith("---\n") else text


def is_library_copy(path, name, ignore_frontmatter=False):
    p = Path(path)
    if not p.exists():
        return False
    mine, lib = p.read_text(), (OLD / name).read_text()
    return body(mine) == body(lib) if ignore_frontmatter else mine == lib


def apply(t, slug=CFU):
    """Lay the `Path: none` Client Follow-Up over workspace `t`. Returns True when the requirements were
    replaced (the workspace held the library's own copy), False when they were left as they are."""
    wf = Path(t) / "framework" / slug
    req = wf / "requirements.md"
    if not is_library_copy(req, "requirements.md", ignore_frontmatter=True):
        return False
    # the workspace's own frontmatter (a raised revision, a big_change) stays; the body is today's shape
    front = req.read_text().split("\n---\n", 1)[0]
    req.write_text(front + "\n---\n" + body((NEW / "requirements.md").read_text()))
    for src in sorted((NEW / "inputs").iterdir()):
        dst = wf / "inputs" / src.name
        if not dst.exists() or is_library_copy(dst, f"inputs/{src.name}"):
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(src.read_text())
    plan = wf / "design-plan.md"
    if plan.exists():
        text = plan.read_text()
        missing = [old for old in PLAN_REQUIRED if old not in text]
        if missing:
            raise SystemExit(f"{plan}: not the library's plan, can't lay Path: none over it (missing {missing})")
        for old, new in PLAN_SUBS:
            text = text.replace(old, new)
        plan.write_text(text)
    rec = wf / "build-record.md"
    if rec.exists():
        text = rec.read_text()
        for old, new in RECORD_SUBS:
            text = text.replace(old, new)
        rec.write_text(text)
    return True


# ---------- a law-named rule and checkpoint ----------
# What Deconstruct writes when the law question's answer is yes (interview.md, *A law or regulation*): a rule
# "It always [does that], as [the law] requires." and a checkpoint "[The checkpoint], as [the law] requires.",
# never offered for dropping, the regime on the `Governing regime:` line, and the full track. Design, Build and
# Test may never drop or loosen either line (design updating-the-plan.md; test requirement-lines.md).
LAW = "FINRA Rule 2210"
LAW_REGIME = "Governing regime: FINRA Rule 2210 (communications with the public)"
LAW_RULE = "| R5 | Always | It always ends each draft with the disclosure line in C2, as FINRA Rule 2210 requires. |"
LAW_GATE = ("| G2 | After you approve the draft | When you approve the draft, it waits for a registered principal to "
            "approve it before it goes to the client, as FINRA Rule 2210 requires. · (registered principal) |")
DISCLOSURE = ("Brightline Advisory LLC is a member of FINRA and SIPC. This email is not an offer or a recommendation "
              "to buy or sell any security.")
LAW_SKILL_LINES = (
    "\nEnd every draft with the disclosure line in `references/disclosure-line.md`, word for word, as FINRA Rule 2210 requires.\n"
    "After the person approves the draft, it waits for a registered principal to approve it before it goes to the client, "
    "as FINRA Rule 2210 requires.\n")
E1_EXPECT = "A draft listing all three next steps, each with its owner; no figure, date or commitment the notes don't give"


def _sub(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"{p}: {old!r} not found")
    p.write_text(text.replace(old, new, 1))


def add_law(t, slug=CFU):
    """Give the `Path: none` Client Follow-Up (after `apply`) a law-named rule (R5: every draft ends with the
    firm's disclosure line, C2) and a law-named checkpoint (G2: a registered principal approves each draft before
    it goes out), both naming FINRA Rule 2210, on the full track. Where the workspace has them, the plan (T2
    meets R5 and G2; Step Pd, the principal's review; the Organizational lens), the built skill (both lines, and C2's runtime copy) and
    the build record (C2's row) follow. The caller recomputes fingerprints."""
    wf = Path(t) / "framework" / slug
    req = wf / "requirements.md"
    if "track: light\n" in req.read_text():  # the law answer was yes: the full track (interview.md)
        _sub(req, "track: light\n", "track: full\n")
    _sub(req, "| Tone, length and sign-off for client emails |\n",
         "| Tone, length and sign-off for client emails |\n"
         "| C2 | Firm disclosure line | All | Exists | Internal | Authored | Yes | `context/C2-disclosure-line.md` | "
         "The sentence every client email ends with |\n")
    _sub(req, "it asks you for one before it drafts anything. |\n", "it asks you for one before it drafts anything. |\n" + LAW_RULE + "\n")
    _sub(req, "it stops until you approve it. · (you) |\n", "it stops until you approve it. · (you) |\n" + LAW_GATE + "\n")
    _sub(req, "Governing regime: None", LAW_REGIME)
    _sub(req, "| Lens | Individual |", "| Lens | Organizational |\n| Stakeholders | Registered principal (compliance) |")
    _sub(req, f"| {E1_EXPECT} |", f"| {E1_EXPECT}; it ends with the disclosure line |")
    e1 = wf / "inputs" / "E1-acme-renewal-call.md"
    _sub(e1, "tests: AC1, AC2, AC3, R1, G1\n", "tests: AC1, AC2, AC3, R1, R5, G1, G2\n")
    _sub(e1, f"expect: {E1_EXPECT}\n", f"expect: {E1_EXPECT}; it ends with the disclosure line\n")
    ctx = wf / "context" / "C2-disclosure-line.md"
    ctx.parent.mkdir(parents=True, exist_ok=True)
    ctx.write_text(f"# Disclosure line\n\nEvery client email ends with this sentence, word for word:\n\n{DISCLOSURE}\n")
    plan = wf / "design-plan.md"
    if plan.exists():
        text = plan.read_text()
        for old, new in (
                ("R1, R2, R3, R4, G1, W1", "R1, R2, R3, R4, R5, G1, G2, W1"),
                ("- **Uses / hands on:** I1; C1\n", "- **Uses / hands on:** I1; C1, C2\n"),
                ("practice runs E1 and E2 meet AC1, AC2, AC3, R1, R3", "practice runs E1 and E2 meet AC1, AC2, AC3, R1, R3, R5"),
                ("| Lens | Individual | One person runs it for their own work |",
                 "| Lens | Organizational | A registered principal approves each draft |"),
                ("## Stakeholders\nNone: Individual lens.",
                 "## Stakeholders\n- Registered principal (compliance): approves each draft before it goes to the client (G2)."),
                ("| Step Pc — Review and send | — | — | — | — | Human (no artifact) | G1 | You |",
                 "| Step Pc — Review and send | — | — | — | — | Human (no artifact) | G1 | You |\n"
                 "| Step Pd — Principal review | — | — | — | — | Human (no artifact) | G2 | Registered principal |"),
                ("- **Covers Steps:** Step Pa, Step Pb, Step Pc", "- **Covers Steps:** Step Pa, Step Pb, Step Pc, Step Pd"),
                ("- **Meets:** Step Pa, Step Pb, Step Pc,", "- **Meets:** Step Pa, Step Pb, Step Pc, Step Pd,"),
                ("3. Stop for your review (G1); an unattended run stops here and leaves a draft.",
                 "3. Stop for your review (G1); an unattended run stops here and leaves a draft. Then wait for a registered "
                 "principal's approval (G2); every draft ends with C2's disclosure line (R5).")):
            if old not in text:
                raise SystemExit(f"{plan}: {old!r} not found")
            text = text.replace(old, new, 1)
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("| C1 | Exists |"):
                lines.insert(i + 1, line.replace("| C1 |", "| C2 |", 1))
                break
        plan.write_text("\n".join(lines))
    skill = Path(t) / ".claude" / "skills" / slug / "SKILL.md"
    if skill.exists():
        skill.write_text(skill.read_text().rstrip("\n") + "\n" + LAW_SKILL_LINES)
        ref = skill.parent / "references" / "disclosure-line.md"
        ref.parent.mkdir(parents=True, exist_ok=True)
        ref.write_text(ctx.read_text())
    rec = wf / "build-record.md"
    if rec.exists():
        lines = rec.read_text().split("\n")
        for i, line in enumerate(lines):
            if line.startswith("| T2 | — | C1 | Follow-up style guide (runtime copy) |"):
                lines.insert(i + 1, line.replace("| C1 | Follow-up style guide (runtime copy) |", "| C2 | Disclosure line (runtime copy) |")
                             .replace("follow-up-style.md", "disclosure-line.md"))
                break
        rec.write_text("\n".join(lines))
