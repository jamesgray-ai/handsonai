#!/usr/bin/env python3
"""Deconstruct's eval tooling: the word count and `max_words` (T1, T2), the time check's exemption for the
leader's own schedule (a brought `Starts` row, R-D3), reply counts (leader.replies_by_part: Deconstruct's
single interview has no parts, and one count, in the line that says how it will go), validate_evals' shape
check for `max_words`, and the Deconstruct word counter (tools/wc_deconstruct.py). No model is called.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
sys.path.insert(0, str(EVALS))
sys.path.insert(0, str(EVALS / "tools"))

import approved_lines as AL  # noqa: E402
import check_scripted as CS  # noqa: E402
import leader as L  # noqa: E402
import validate_evals as V  # noqa: E402
import wc_deconstruct as WC  # noqa: E402


def session(n, *pairs, files_start=None, fixture=True):
    """A session from (leader text, AI text) pairs."""
    turns = []
    for lead, ai in pairs:
        if lead is not None:
            turns.append({"role": "student", "text": lead})
        if ai is not None:
            turns.append({"role": "ai", "text": ai})
    return {"n": n, "turns": turns, "files_by_turn": [], "files_start": files_start or {}, "files_end": {},
            "cap_hit": False, "root": None, "fixture": fixture}


def ok(c, *sessions):
    return CS.check(c, {"sessions": list(sessions)})


def line(lid, form="main"):
    return next(f.text for f in AL.load().get(lid, form) if f.text)


# the line that says how the interview will go: the one count the single interview says (2026-11-15)
HOW_LINE = line("deconstruct:light-line").replace("[M]", "24")
# "About [M] questions left." is never said by the single interview; it stays in the corpus so a run that says it is seen
COUNT = line("deconstruct:questions-left").replace("[M]", "12")


class WordCount(unittest.TestCase):
    def test_counts_words_as_the_leader_reads_them(self):
        self.assertEqual(CS.word_count("Three plain words"), 3)
        # Markdown's marks and a list's bullets aren't words; a list number is one
        self.assertEqual(CS.word_count("**Process:** Sales\n- *Why:* Start small.\n1. Lead Summary"), 8)
        self.assertEqual(CS.word_count("A dash — between `code` words"), 5)
        self.assertEqual(CS.word_count(""), 0)


class MaxWords(unittest.TestCase):
    def test_first_turn(self):
        short, long_ = "word " * 200, "word " * 201
        self.assertTrue(ok({"type": "max_words", "max": 200, "turn": "first"}, session(1, ("go", short), ("ok", long_)))[0])
        passed, why = ok({"type": "max_words", "max": 200, "turn": "first"}, session(1, ("go", long_)))
        self.assertFalse(passed)
        self.assertIn("201 words", why)
        # every session's first message counts (a resume is in T1), unless `session` narrows it
        two = [session(1, ("go", short)), session(2, ("resume", long_))]
        self.assertFalse(ok({"type": "max_words", "max": 200, "turn": "first"}, *two)[0])
        self.assertTrue(ok({"type": "max_words", "max": 200, "turn": "first", "session": 1}, *two)[0])
        # nothing to count fails closed
        self.assertFalse(ok({"type": "max_words", "max": 200, "turn": "first"}, session(1, ("go", None)))[0])

    def test_containing_a_line(self):
        n_d23 = "\n".join([line("N-D23"), "Starts when: every Friday", "Ends with: a report",
                           "Name: Weekly Report (rename it here if you like)", "Description: Drafts it.",
                           line("N-D23", "ending")])
        how_msg = "\n\n".join([HOW_LINE, n_d23])
        c = {"type": "max_words", "max": 170, "containing": "deconstruct:light-line"}
        self.assertTrue(ok(c, session(1, ("go", "Hello."), ("1", how_msg)))[0])
        padded = how_msg + " extra" * (171 - CS.word_count(how_msg))
        self.assertFalse(ok(c, session(1, ("go", "Hello."), ("1", padded)))[0])
        # a line never said fails closed, and the check never counts other messages
        self.assertFalse(ok(c, session(1, ("go", "word " * 500)))[0])
        # the retired track line names no approved line any more: nothing to count, so it fails closed
        self.assertFalse(ok({"type": "max_words", "max": 170, "containing": "N-L1"}, session(1, ("go", how_msg)))[0])

    def test_validator_shapes(self):
        corpus = AL.load()
        good = [{"type": "max_words", "max": 200, "turn": "first"},
                {"type": "max_words", "max": 170, "containing": "deconstruct:light-line"},
                {"type": "max_words", "max": 170, "containing": "deconstruct:light-line", "form": "main"}]
        bad = [{"type": "max_words", "turn": "first"},
               {"type": "max_words", "max": "200", "turn": "first"},
               {"type": "max_words", "max": 0, "turn": "first"},
               {"type": "max_words", "max": 200},
               {"type": "max_words", "max": 200, "turn": "first", "containing": "deconstruct:light-line"},
               {"type": "max_words", "max": 200, "turn": "last"},
               {"type": "max_words", "max": 200, "containing": "N-NOPE"},
               # retired with the two-track interview (2026-11-15): no longer approved lines
               {"type": "max_words", "max": 150, "containing": "N-L1"},
               {"type": "max_words", "max": 150, "containing": "N-D17"}]
        for c in good:
            errs = []
            V.check_check(c, "x", errs, 1, corpus)
            self.assertEqual(errs, [], c)
        for c in bad:
            errs = []
            V.check_check(c, "x", errs, 1, corpus)
            self.assertTrue(errs, c)


class StartsExemption(unittest.TestCase):
    REQ = ("## Metadata\n\n| Field | Value |\n|---|---|\n| Workflow Name | Lead Follow-Up |\n"
           "| Trigger | A new lead arrives in the CRM |\n"
           "| Starts | event: a new lead arrives in the CRM · checked every 30 minutes |\n")

    def test_the_leaders_schedule_may_be_played_back(self):
        said = "It checks for new leads every 30 minutes, the schedule you set."
        brought = {"framework/lead-follow-up/requirements.md": self.REQ}
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, session(1, ("go", said), files_start=brought))[0])
        # without the row, the same words are a time the AI gave
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, session(1, ("go", said)))[0])
        # the row exempts only its own figure, never one Design chose itself
        other = "It checks every 5 minutes, the shortest the platform allows."
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, session(1, ("go", other), files_start=brought))[0])

    def test_only_what_the_leader_brought_counts(self):
        # a requirements file written in an earlier session of this run is the AI's, not the leader's
        said = "It checks every 30 minutes."
        brought = {"framework/lead-follow-up/requirements.md": self.REQ}
        first = session(1, ("go", "Hello."), fixture=True)
        second = session(2, ("resume", said), files_start=brought, fixture=False)
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, first, second)[0])

    def test_starts_row(self):
        self.assertEqual(CS.starts_row(self.REQ), "event: a new lead arrives in the CRM · checked every 30 minutes")
        self.assertEqual(CS.starts_row("## Metadata\n\n| Trigger | x |\n"), "")


class RepliesByPart(unittest.TestCase):
    def test_single_interview_has_one_count_and_no_parts(self):
        s = session(1,
                    ("run the deconstruct skill", "Which workflow?"),
                    ("1", "Do you have anything written down?"),
                    ("no", HOW_LINE + "\n\nHere's what your Analyze report has for this workflow:"),
                    ("looks right", "Everything for this workflow goes in its own folder.\n\nWill it send or change anything itself?"),
                    ("no", "Is there a law or regulation that governs this work?"),
                    ("no", "Thanks."),
                    ("END", None))
        r = L.replies_by_part([s])
        # no signposts: every reply is "entry", whatever the AI says
        self.assertEqual(r["by_part"], {"entry": 6})
        self.assertEqual(r["replies"], 6)
        # the one count point: the line that says how the interview will go, with the replies still to come
        self.assertEqual([(p["at"], p["message"], p["still_to_come"]) for p in r["count_points"]],
                         [("deconstruct:light-line", 3, 3)])

    def test_a_part_signpost_no_longer_splits_deconstruct(self):
        # the retired five-part interview's signposts and N-D17 mean nothing now: no part, no count point
        s = session(1, ("go", "It runs in five parts, about 45 questions.\n\nReady to start Part 1?"),
                    ("yes", "Part 1 of 5 — what this is worth."), ("fine", "Part 2 of 5 — where it starts and ends, and a name."),
                    ("ok", None))
        r = L.replies_by_part([s])
        self.assertEqual(r["by_part"], {"entry": 4})
        self.assertEqual(r["count_points"], [])
        self.assertNotIn("deconstruct", CS.SIGNPOST_IDS)
        self.assertEqual(CS.COUNT_CARRIERS, [("deconstruct:light-line", "main")])

    def test_a_stray_count_line_shows_across_sessions(self):
        # "About [M] questions left." is never said now; a run that says it gets a count point, so it shows
        s1 = session(1, ("run it", "Which workflow?"), ("1", "Anything written down?"),
                     ("no", "\n\n".join([HOW_LINE, "Here's what your Analyze report has for this workflow:"])),
                     ("looks right", None))
        s2 = session(2, ("run it on Weekly Report", COUNT + "\n\nWhat is it for?"), ("a summary", "Thanks."))
        r = L.replies_by_part([s1, s2])
        self.assertEqual(r["by_part"], {"entry": 6})
        self.assertEqual([(p["at"], p["session"], p["still_to_come"]) for p in r["count_points"]],
                         [("deconstruct:light-line", 1, 3), ("the count line", 2, 1)])

    def test_another_skill(self):
        s = session(1, ("go", "Part 1 of 4 — the plan."), ("ok", "Part 2 of 4 — safety."), ("fine", None))
        self.assertEqual(L.replies_by_part([s], "design")["by_part"], {"entry": 1, "Part 1": 1, "Part 2": 1})


class DeconstructWordCounter(unittest.TestCase):
    def test_estimate_builds_every_platform_from_the_corpus(self):
        rows = {p: WC.first_messages(p) for p in WC.LOCATION}
        for p, msgs in rows.items():
            for kind, msg in msgs.items():
                self.assertIn(line("N-D2"), msg, (p, kind))
                self.assertNotIn("[location]", msg, (p, kind))
        self.assertIn("I can't save files here", rows["print-to-save"]["backlog, first workflow"])
        self.assertNotIn("Stopping early is safe", rows["print-to-save"]["backlog, first workflow"])
        self.assertIn(line("N-D3", "Microsoft 365").replace("[location]", "OneDrive, in ai-workspace"),
                      rows["cowork"]["backlog, first workflow"])
        msg = rows["web"]["backlog, first workflow"]
        self.assertIn(line("deconstruct:map-backlog-question", "why"), msg)
        self.assertNotIn(line("deconstruct:map-backlog-question", "why"), rows["web"]["backlog, later workflow"])
        # the fills keep T1's limits: labels at most 3 words, goals at most 8
        self.assertTrue(all(len(x.split()) <= 3 for x in WC.LABELS))
        self.assertTrue(all(len(g.split()) <= 8 for _, _, g in WC.CANDIDATES if g))
        # T2: one message, for every workflow: the line that says how the interview will go, then N-D23
        msgs = WC.how_it_goes_messages()
        self.assertEqual(list(msgs), ["backlog pick"])
        how, cap = msgs["backlog pick"]
        self.assertEqual(cap, 170)
        self.assertTrue(how.startswith("After this, I'll ask a few safety questions"))
        self.assertIn("about 24 questions from here", how)
        self.assertLessEqual(CS.word_count(how), cap)
        self.assertNotIn("Part 1", how)
        self.assertNotIn("workflow because", how)

    def test_transcript_mode(self):
        how_msg = "\n\n".join([HOW_LINE, "Here's what your Analyze report has for this workflow:"])
        turns = [{"role": "student", "text": "go"}, {"role": "ai", "text": "word " * 150},
                 {"role": "student", "text": "1"}, {"role": "ai", "text": how_msg}]
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "turns.json"
            p.write_text(json.dumps(turns))
            with redirect_stdout(io.StringIO()):
                self.assertEqual(WC.main(["transcript", str(p)]), 0)
            turns[1]["text"] = "word " * 201
            p.write_text(json.dumps(turns))
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(WC.main(["transcript", str(p)]), 1)
            self.assertIn("OVER", out.getvalue())
            # T2: the message that says how the interview will go, over 170 words
            turns[1]["text"] = "word " * 150
            turns[3]["text"] = how_msg + " extra" * 171
            p.write_text(json.dumps(turns))
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(WC.main(["transcript", str(p)]), 1)
            self.assertIn("how-it-will-go message 2", out.getvalue())


if __name__ == "__main__":
    unittest.main()
