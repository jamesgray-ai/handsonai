#!/usr/bin/env python3
"""Deconstruct's word counter (T1 and T2). Analyze's own is wc_v31.py, beside this one, unchanged.

  python3 framework-evals/tools/wc_deconstruct.py estimate
      Builds Deconstruct's scripted messages from approved-lines.json, with illustrative fills, and counts
      them on every platform:
        T1 (at most 200 words), the first message: the opening (N-D2, the location line, N-D3 in the
            platform's form; print-to-save: N-F6 and no N-D3) and the backlog choice, a first and a later
            workflow, with 5 candidates under 4 process labels (each at most 3 words) and 3 goals (each at
            most 8 words); cold entry; running work Analyze recorded (N-D22's Status form).
        T2, the message that says how the interview will go (one interview for every workflow, 2026-11-15):
            the line itself (deconstruct:light-line) and N-D23 with a 25-word description; at most 170.
      The location line is model wording around N-F3's promise clause, filled as the skill fills it;
      every other line comes from the corpus, so a reworded line changes the count here too.

  python3 framework-evals/tools/wc_deconstruct.py transcript <turns.json | run folder>...
      Measures real runs: each session's first AI message against T1, and each AI message that says
      how the interview will go against T2 (170).

Words are counted by check_scripted.word_count, the count the `max_words` eval check uses. Exit 1 when a
message is over its limit. Never calls a model.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import approved_lines as AL  # noqa: E402
import check_scripted as CS  # noqa: E402

T1, T2 = 200, 170

# Illustrative fills only (a made-up business), at T1's limits: labels at most 3 words, goals at most 8
LABELS = ["Client delivery", "Sales pipeline", "Finance and billing", "Team operations"]
CANDIDATES = [  # (label index, name, goal or None)
    (0, "Weekly Client Status Report", "Keep every client renewal on track this year"),
    (0, "Project Kickoff Brief", None),
    (1, "Inbound Lead Summary", "Grow new consulting revenue by a fifth"),
    (2, "Monthly Invoice Check", "Cut late payments to under ten days"),
    (3, "Team Meeting Notes", None),
]
LOCATION = {  # where the files are, as N-F3's promise clause names it, and the platform clause
    "claude-code": ("this folder", ("N-F3", "On Claude Code")),
    "codex": ("this folder", ("N-F3", "On Codex")),
    "web": ("Google Drive, in ai-workspace", ("N-F3", "On the web and in Microsoft 365 Cowork")),
    "cowork": ("OneDrive, in ai-workspace", ("N-F3", "On the web and in Microsoft 365 Cowork")),
    "desktop": ("ai-workspace", None),
    "print-to-save": (None, None),
}
N_D3_FORM = {"claude-code": "Claude Code and Codex", "codex": "Claude Code and Codex", "web": "main",
             "cowork": "Microsoft 365", "desktop": "Claude desktop, files in a local folder", "print-to-save": None}
PLATFORM_NAME = {"web": "Claude", "cowork": "Cowork"}


def line(lid, form="main", **fills):
    forms = [f for f in AL.load().get(lid, form) if f.text]
    if not forms:
        raise SystemExit(f"no approved line {lid} ({form}) in approved-lines.json")
    text = forms[0].text
    for k, v in fills.items():
        text = text.replace(f"[{k}]", v)
    return text


def opening(platform):
    loc, clause = LOCATION[platform]
    parts = [line("N-D2")]
    if platform == "print-to-save":
        parts.append(line("N-F6"))
    else:
        where = line("N-F3", "promise clause", location=loc)
        if clause:
            where += " " + line(*clause, platform=PLATFORM_NAME.get(platform, ""))
        parts.append(where)
        parts.append(line("N-D3", N_D3_FORM[platform], location=loc))
    return "\n\n".join(parts)


def backlog(later=False):
    out = []
    n = 0
    for k, label in enumerate(LABELS):
        out.append(f"**Process:** {label}")
        for li, name, goal in CANDIDATES:
            if li == k:
                n += 1
                out.append(f"{n}. {name}" + (f" (goal: {goal})" if goal else ""))
    why = line("deconstruct:map-backlog-question", "why, later workflows" if later else "why")
    out.append(line("deconstruct:map-backlog-question", "Recommended"))
    out.append(f"- *Why:* {why}")
    out.append(f"- *Not sure?* {line('deconstruct:map-backlog-question', 'not-sure')}")
    return "\n".join(out)


def first_messages(platform):
    return {
        "backlog, first workflow": opening(platform) + "\n\n" + backlog(),
        "backlog, later workflow": opening(platform) + "\n\n" + backlog(later=True),
        "cold entry": opening(platform) + "\n\n" + line("deconstruct:5.1:q2"),
        "running work Analyze recorded": opening(platform) + "\n\n"
        + line("N-D22", "Status form").replace("[skill or agent][, in [where]]", "a skill, in Claude Code"),
    }


def how_it_goes_messages():
    """The interview's first message for a backlog pick: the line that says how it will go, then N-D23."""
    description = ("Drafts the weekly client status report from the project tracker and last week's notes, "
                   "ready for me to check and send each Friday")  # 25 words, illustrative
    msg = "\n\n".join([
        line("deconstruct:light-line", M="30"),
        "\n".join([line("N-D23"), line("N-D23", "Starts when", trigger="every Friday morning"),
                   line("N-D23", "Ends with", deliverable="a status report for each client"),
                   line("N-D23", "Name", name="Weekly Client Status Report"),
                   line("N-D23", "Description", description=description),
                   line("N-D23", "How often", **{"frequency, in plain words": "about once a week"}),
                   line("N-D23", "ending")])])
    return {"backlog pick": (msg, T2)}


def estimate():
    over = []
    print(f"T1: the first message (at most {T1} words)")
    rows = {p: first_messages(p) for p in LOCATION}
    kinds = list(next(iter(rows.values())))
    print(f"{'':32}" + "".join(f"{p:>15}" for p in LOCATION))
    for k in kinds:
        counts = [CS.word_count(rows[p][k]) for p in LOCATION]
        over += [(k, p, c) for p, c in zip(LOCATION, counts) if c > T1]
        print(f"{k:32}" + "".join(f"{c:>15}" for c in counts))
    print()
    print("T2: the message that says how the interview will go")
    for kind, (msg, cap) in how_it_goes_messages().items():
        c = CS.word_count(msg)
        if c > cap:
            over.append((f"how-it-will-go message, {kind}", "any", c))
        print(f"  {kind:12} {c:4} words (at most {cap})")
    return over


def ai_turns(path):
    p = Path(path)
    if p.is_dir():
        out = []
        for f in sorted(p.rglob("turns.json")):
            out.append((str(f), [t["text"] for t in json.loads(f.read_text()) if t.get("role") == "ai"]))
        return out
    return [(str(p), [t["text"] for t in json.loads(p.read_text()) if t.get("role") == "ai"])]


def transcript(paths):
    over = []
    how = [f for f in AL.load().get("deconstruct:light-line") if f.text]
    for path in paths:
        for where, msgs in ai_turns(path):
            if not msgs:
                continue
            c = CS.word_count(msgs[0])
            print(f"{where}: first message {c} words (at most {T1})")
            if c > T1:
                over.append((where, "first message", c))
            for i, m in enumerate(msgs, 1):
                if any(f.matches(m) for f in how):
                    c = CS.word_count(m)
                    print(f"{where}: AI message {i} says how the interview will go: {c} words (at most {T2})")
                    if c > T2:
                        over.append((where, f"how-it-will-go message {i}", c))
    return over


def main(argv):
    if not argv or argv[0] not in ("estimate", "transcript") or (argv[0] == "transcript" and len(argv) < 2):
        print(__doc__)
        return 2
    over = estimate() if argv[0] == "estimate" else transcript(argv[1:])
    for what, where, c in over:
        print(f"OVER: {what} ({where}): {c} words")
    print("OK" if not over else f"{len(over)} over the limit")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
