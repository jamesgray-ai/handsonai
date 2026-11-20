#!/usr/bin/env python3
"""Build's scripted checks against real snippets from rounds build-single-interview-1 and -2
(2026-11-18), where the checker, not the skill, failed the run.

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import approved_lines as AL  # noqa: E402

EVALS = HERE.parents[1] / "build-workspace" / "evals" / "evals.json"


def pattern(text):
    """The file_regex pattern of the Build expectation with this text."""
    for ev in json.loads(EVALS.read_text())["evals"]:
        for x in ev["expectations"]:
            if isinstance(x, dict) and x.get("text") == text:
                return x["check"]["pattern"]
    raise KeyError(text)


class LiveChecksKeys(unittest.TestCase):
    """live_checks keys are the record template's "[kind of change]": several words, never one."""

    JR_WEB = ('live_checks:\n  create a Gmail draft: "done: Gmail Drafts of alex@brightline.example (empty draft, '
              'subject Build check, delete me)"\nskills_on: yes\n')  # JR-claude-web run 1
    DECLINED = 'live_checks:\n  gmail create a draft: "declined"\nskills_on: yes\n'  # P1-qrc-declined run 1
    SKIPPED = 'live_checks:\n  create a Gmail draft: "skipped: the leader has no test inbox"\n'

    def test_multi_word_keys_match(self):
        self.assertRegex(self.JR_WEB, pattern("[P1-qrc-self] live_checks done with its place"))
        self.assertRegex(self.DECLINED, pattern("live_checks declined"))
        self.assertRegex(self.SKIPPED, pattern("live_checks skipped"))

    def test_one_word_keys_and_other_values_still_hold(self):
        self.assertRegex('live_checks:\n  gmail-draft: "done: a draft addressed to you"\n',
                         pattern("[P1-qrc-self] live_checks done with its place"))
        self.assertNotRegex(self.JR_WEB, pattern("live_checks declined"))
        self.assertNotRegex('live_checks:\n  create a Gmail draft: "not yet"\n', pattern("live_checks declined"))
        # a deeper-indented line (a nested list item) is never a live_checks key
        self.assertNotRegex('write_block:\n  on:\n    - x: declined\n', pattern("live_checks declined"))


class NB8BlockQuotedDraft(unittest.TestCase):
    """N-B8 with the draft block-quoted as [the content]: it ends on the sign-off, with no full stop
    (EN-orientation run 3's message, with the line's own "save … to" wording)."""

    # ("today" left out: a literal " to " also matches inside "today", an older looseness of the matcher)
    MSG = ("Here's exactly what it would save to your Gmail Drafts:\n\n> **Subject:** Follow-up from this morning's call\n>\n"
           "> Hi Dana,\n>\n> Thanks for the time this morning on the renewal of the analytics contract.\n>\n"
           "> - Renewal quote, by Friday. Owner: Alex (me).\n>\n> Best,\n> Alex\n\n"
           "I haven't saved it. Is that the right place and the right kind of draft?")

    def test_the_stop_after_the_content_is_optional(self):
        forms = [f for f in AL.load().get("N-B8") if f.text]
        self.assertTrue(any(f.matches(self.MSG) for f in forms))
        main = AL.load().get("N-B8", "main")[0]
        self.assertFalse(main.matches(self.MSG))  # the approved text alone wanted the stop
        self.assertTrue(main.matches(self.MSG.replace("> Alex\n", "> Alex.\n")))
        self.assertEqual(AL.load().near_misses(self.MSG, "build"), [])

    def test_the_lines_own_words_still_count(self):
        # the round's real wording, "create in", is still not the line ("[post] to [place]")
        wrong = self.MSG.replace("save to your", "create in your").replace("haven't saved", "haven't created")
        self.assertFalse(any(f.matches(wrong) for f in AL.load().get("N-B8") if f.text))


class NF2InsideNF10(unittest.TestCase):
    """N-F10's platform forms hold the words N-F2's are fuzzy-matched against: those are N-F10's own."""

    CC = ("I saved your progress, including the Gmail check, in `framework/client-follow-up/build-record.md`. "
          "When you want to carry on, you'll first need to find your older client-follow-up skill and switch it "
          "off. Then start a new session in this project and say 'run the build skill.'")  # P1-older-stop run 2
    DESKTOP = ("If it's already on and I still can't see it, it may only appear in a new chat. Your progress is "
               "saved. Open a new chat with your working folder selected and say 'run the build skill. My files "
               "are in ai-workspace/framework/client-follow-up.' I'll pick up at this step.")  # OP-desktop-no-folder run 3

    def ids(self, msg):
        return [(ln.id, got) for ln, _, got in AL.load().near_misses(msg, "build")]

    def test_claude_code_form(self):
        self.assertNotIn(("N-F2", "start a new session in this project and say"), self.ids(self.CC))

    def test_desktop_form(self):
        self.assertNotIn(("N-F2", "open a new chat with your working folder selected"), self.ids(self.DESKTOP))

    def test_a_real_n_f2_rewording_is_still_caught(self):
        # N-F2's Claude Code form with "in" said as "open": no N-F10 form holds those words
        msg = "Then open a new session in this project and say 'run the build skill.'"
        self.assertIn("N-F2", [i for i, _ in self.ids(msg)])

if __name__ == "__main__":
    unittest.main()
