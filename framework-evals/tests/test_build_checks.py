#!/usr/bin/env python3
"""Build's scripted checks against real snippets from rounds build-single-interview-1 and -2
(2026-11-18), where the checker, not the skill, failed the run.

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import approved_lines as AL  # noqa: E402
import check_scripted as CS  # noqa: E402

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

    # final-build-2 (2026-11-22, James): N-F2 and N-F10 point the way and protect nothing, so a word or two
    # changed ("start a new session" for "in a new session") is no near miss; a protected word changed still is
    def test_claude_code_form(self):
        said = "Your progress is saved. To pick up, start a new session in this project and say 'run the build skill.'"
        self.assertNotIn("N-F2", [i for i, _ in self.ids(said)])
        self.assertNotIn("N-F2", [i for i, _ in self.ids(self.CC)])

    def test_desktop_form(self):
        said = ("Your progress is saved. To pick up, open a new chat with your working folder selected and say "
                "'run the build skill. My files are in ai-workspace/framework/client-follow-up.'")
        self.assertNotIn("N-F2", [i for i, _ in self.ids(said)])
        self.assertNotIn("N-F2", [i for i, _ in self.ids(self.DESKTOP)])

    def test_a_protected_word_changed_in_n_f2_is_still_caught(self):
        msg = ("Start Design in a new chat. Never add your Google Drive to it, then say 'run the design skill. "
               "My files are in Google Drive, in ai-workspace/framework/client-follow-up.'")
        self.assertIn("N-F2", [i for i, _ in self.ids(msg)])


class NamedFormIncludesItsDerivedForms(unittest.TestCase):
    """A quote check naming a form also accepts that form with an empty clause left out (trial 2,
    2026-11-20: EN-orientation failed 3/3 on a correct opening with no draft to check)."""

    OPENING = ("Build makes your workflow for Client Follow-Up from your approved plan, task by task, checking each "
               "part as it goes. First I'll need you to set up a Project for your workflow, connect Gmail and OK 2 "
               "quick real checks and setup changes; then I build and check the rest, and I'll ask you to confirm "
               "about 5 things along the way. Stopping early is safe: progress is saved after each task. To pick up, "
               "say 'run the build skill. My files are in Google Drive, in ai-workspace/framework/client-follow-up.' "
               "Let's start with the Project for your workflow.")

    def test_no_draft_variant_counts_as_the_named_form(self):
        forms = AL.load().get("N-B4", "after an orientation line")
        self.assertTrue(any(f.matches(self.OPENING) for f in forms))

    def test_another_approved_form_is_not_pulled_in(self):
        forms = AL.load().get("N-B4", "Every task waits")
        self.assertFalse(any(f.form.startswith("Every task waits, after an orientation line") and not f.derived
                             for f in forms))



class StopInsideAClosingQuote(unittest.TestCase):
    def test_a_line_whose_hole_ends_in_a_quoted_sentence_matches(self):
        # P2-shared-skill run 3 (trial 3): N-B25 said exactly, its [before and after] ending "…owns it.'"
        f = AL.load().get("N-B25", "main")[0]
        self.assertTrue(f.matches("drafting-client-emails is also used by Client Check-In. Here's the change: "
                                  "before, it says \"Sign with your first name.\"; after, it says \"List every "
                                  "next step agreed.\" It changes those workflows too. Shall I make it?"))


def _run_of(*ai_messages):
    turns = []
    for m in ai_messages:
        turns += [{"role": "student", "text": "go", "student": True}, {"role": "ai", "text": m}]
    return {"sessions": [{"n": 1, "turns": turns, "files_by_turn": [[]] * len(ai_messages),
                          "files_start": {}, "files_end": {}, "cap_hit": False, "root": None}]}


class VocabularySkipsLinks(unittest.TestCase):
    """build-full-1 (2026-11-21): a help-page slug flagged "connector"."""

    def test_a_link_slug_is_not_wording(self):
        for m in ("See https://support.claude.com/en/articles/10166901-use-google-workspace-connectors for the steps.",
                  "See support.claude.com/en/articles/10166901-use-google-workspace-connectors for the steps."):
            self.assertEqual(CS.vocabulary_hits(m), [], m)

    def test_the_word_outside_a_link_still_counts(self):
        m = "Add the Gmail connector (support.claude.com/en/articles/10166901) first."
        self.assertEqual([n for n, _ in CS.vocabulary_hits(m)], ["connector"])


class ShortRunNeedsTheRestOfItsLine(unittest.TestCase):
    """build-full-1 (2026-11-21): a 6-7 word run with one word changed, and nothing else of its line said,
    is model wording, not the line reworded."""

    def misses(self, msg, skill="build"):
        return [(ln.id, got) for ln, _, got in AL.load().near_misses(msg, skill)]

    def test_false_hits_from_the_round(self):
        for msg, lid in [
            ("Say 'done' when it's paused, 'it only runs when I start it', or 'stop' to leave everything as it is.",
             "N-B14"),  # P1-older-yes-cc-copy run 2/3
            ("If you'd rather leave the old one alone for now, say 'stop'. Nothing is installed so far, and I'll "
             "pick up here next time.", "N-B9"),  # P1-older-yes-cc-copy run 3
            ("Your progress is saved. In the new chat, add your Google Drive and Gmail from the prompt box before "
             "you type anything.\n\nTo pick up, say 'run the build skill. My files are in Google Drive, in "
             "ai-workspace/framework/client-follow-up.'", "N-F2"),  # P2-sch-claude-web run 1
        ]:
            self.assertNotIn(lid, [i for i, _ in self.misses(msg)], msg)

    def test_a_rewording_with_the_rest_of_the_line_is_still_caught(self):
        # review of 390f375b8 (James, 2026-11-22): N-B14 is held word for word, so any word changed is a near miss
        msg = "Test found a typo in the draft step. I'll redo just that, and leave nothing else as it is."
        self.assertIn("N-B14", [i for i, _ in self.misses(msg, None)])
        msg = "Test found a typo in the draft step. I'll redo just that, and leave everything as it is."
        self.assertIn("N-B14", [i for i, _ in self.misses(msg, None)])

    def test_a_short_line_on_its_own_is_still_caught(self):
        msg = "OK, Client Follow-Up stays as it was: its plan are back in place, and something has changed."
        self.assertIn("N-D16", [i for i, _ in self.misses(msg, None)])
        # review of 390f375b8 (James, 2026-11-22): N-D16 is a safety line, so a word left out is a near miss too
        self.assertIn("N-D16", [i for i, _ in self.misses("It keeps running as is.", None)])


class BuildAnnouncesNoParts(unittest.TestCase):
    """final-build-2 (2026-11-22, James): Build says no part name or count; its tests check that none is said."""

    C = {"type": "ai_not_regex", "pattern": "\\bPart [0-9] of [0-9]\\b"}

    def test_a_part_count_fails(self):
        self.assertFalse(CS.check(self.C, _run_of("Part 2 of 3 — building and checking"))[0])
        self.assertFalse(CS.check(self.C, _run_of("**Part 1 of 2 in this fix**"))[0])
        self.assertTrue(CS.check(self.C, _run_of("1 of 3: Gmail connection — built and checked"))[0])

    def test_build_has_no_signposts_check(self):
        self.assertFalse(CS.check({"type": "signposts", "skill": "build"}, _run_of("Part 1 of 3 — your setup"))[0])


class MeaningChangingSwapsFail(unittest.TestCase):
    """Review of 3c05a9783 (business b1e38a79): a swap that changes what a protective line means is never a
    small edit. Each case: the line filled, said as approved (passes), then with the one swap (fails)."""

    CASES = [
        ("N-B8", "main", "I haven't Acme it.", "I have Acme it."),
        ("N-T9", "main", "(nothing is sent or changed)", "(nothing is kept or changed)"),
        ("N-T48", "main", "Switch it off for good", "Switch it on for good"),
        ("N-SR4", "main", "nothing is saved until you confirm it", "nothing is saved after you confirm it"),
        ("N-23", "On a live workflow", "keeps running as it is until Build", "keeps running as it is after Build"),
        ("git-save-point", "main", "nothing is shared", "nothing is kept"),
        ("N-B21a", "main", "I've lifted that now", "I've kept that now"),
        ("deconstruct:policy", "not-sure", "it won't go live until you've checked", "it won't go live unless you've checked"),
    ]

    @staticmethod
    def filled(text):
        return re.sub(r"\[[^\]]*\]", "Acme", text)

    def test_each_swap_fails(self):
        for lid, form, old, new in self.CASES:
            line = next(l for l in AL.load().get(lid, form) if l.text)
            said = self.filled(line.text)
            self.assertIn(old, said, (lid, said))
            c = {"type": "quote", "id": lid, "form": form}
            self.assertTrue(CS.check(c, _run_of(said))[0], (lid, said))
            self.assertFalse(CS.check(c, _run_of(said.replace(old, new)))[0], (lid, new))



class SafetyOrPromiseLinesAreWordForWord(MeaningChangingSwapsFail):
    """Review of 390f375b8 (business 9b286fbc): a word list can't catch every swap, so a line approved-lines.json
    labels "safety or promise" is held word for word, cues or not. A fresh set of swaps, none in the list above."""

    CASES = [
        ("N-B21", "Codex", "keeps them from changing anything", "lets them keep changing anything"),
        ("N-T58", "main", "which just passed its test", "which just failed its test"),
        ("N-B26", "No private place", "would reach your team", "would miss your team"),
        ("N-B50", "main", "is built and checked", "is built and unchecked"),
        ("N-B40", "main", "can't draw on our conversations", "can draw on our conversations"),
        ("N-B35", "main", "That didn't work", "That did work"),
        ("N-D16", "main", "are back in place", "are out of place"),
        ("N-A19", "left out", "I left out", "I added in"),
    ]


class ApprovalQuestionsAreWordForWord(MeaningChangingSwapsFail):
    """Review of 390f375b8 (James, 2026-11-22): a question is where the leader approves something, so every
    question line is held word for word too. N-F2 and N-F10, which only say how to carry on, keep a small edit."""

    CASES = [
        ("N-B42", "main", "download it now", "delete it now"),
        ("N-T18", "main", "Remove it?", "Keep it?"),
        ("N-T34", "Ready, not yet live", "everything met", "everything missed"),
        ("N-16", "main", "with someone named who owns that risk", "with nobody named who owns that risk"),
        ("N-T32", "main", "Accept it as untested for now", "Accept it as tested for now"),
        ("N-E2", "main", "put back the built version", "remove the built version"),
        ("N-B25", "main", "It changes those workflows too", "It spares those workflows too"),
    ]

    def test_only_teaching_and_structure_lines_and_the_way_on_take_a_small_edit(self):
        c = AL.load()
        for ln in c.lines:
            if ln.text and not ln.strict:
                self.assertTrue(ln.kind in ("teaching", "structure") or ln.id in ("N-F2", "N-F10"), (ln.id, ln.kind))
        line = next(l for l in c.get("N-B5", "why") if l.text)
        said = self.filled(line.text)
        q = {"type": "quote", "id": "N-B5", "form": "why"}
        self.assertTrue(CS.check(q, _run_of(said.replace("reads your real", "reads your actual")))[0])


class NF4LeadsTheFirstRelayedCheckpoint(unittest.TestCase):
    """James, 2026-11-23 (after final-build-3): N-F4 leads the first checkpoint each session relays."""

    NF4 = ("This is a practice run: if Claude itself asks you to approve sending, posting or changing something, "
           "choose Deny and tell me. Answer the workflow's own questions as you would at work.")
    Q = "> Here's the draft to Dana. Approve it, or tell me what to change?"
    C = {"type": "nf4_leads"}

    def runs(self, *msgs):
        return {"sessions": [{"n": 1, "turns": [t for m in msgs for t in (
            {"role": "student", "text": "ok", "student": True}, {"role": "ai", "text": m})]}]}

    def test_leading_the_first_checkpoint_passes(self):
        self.assertTrue(CS.check(self.C, self.runs(self.NF4 + "\n\n" + self.Q,
                                                   "Answer it as you would at work:\n\n" + self.Q))[0])

    def test_a_checkpoint_relayed_without_it_fails(self):
        self.assertFalse(CS.check(self.C, self.runs("Answer it as you would at work:\n\n" + self.Q,
                                                    self.NF4 + "\n\n" + self.Q))[0])

    def test_said_after_the_quote_or_after_the_short_lead_in_fails(self):
        self.assertFalse(CS.check(self.C, self.runs(self.Q + "\n\n" + self.NF4))[0])
        self.assertFalse(CS.check(self.C, self.runs("Answer it as you would at work: " + self.NF4 + "\n\n" + self.Q))[0])

    def test_no_checkpoint_relayed_passes(self):
        self.assertTrue(CS.check(self.C, self.runs("1 of 3: Gmail connection — built and checked"))[0])


class CodexListingReadFromTheCommands(unittest.TestCase):
    """final-build-4c review (2026-11-24): the workspace listing is read from Build's Bash commands."""

    C = {"type": "bash_count", "pattern": "\\bfind \\.[^\\n|;]*-type f", "min": 2}

    def run_with(self, *cmds):
        import tempfile
        d = Path(tempfile.mkdtemp())
        (d / "changes").mkdir()
        lines = [json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Bash", "input": {"command": c}}]}}) for c in cmds]
        (d / "events.jsonl").write_text("\n".join(lines))
        return {"sessions": [{"n": 1, "turns": [], "root": str(d / "changes")}]}

    def test_listed_before_and_after_passes(self):
        self.assertTrue(CS.check(self.C, self.run_with("find . -type f | sort > /tmp/a", "cat x",
                                                        "find . -type f | sort > /tmp/b; diff /tmp/a /tmp/b"))[0])

    def test_listed_once_or_never_fails(self):
        self.assertFalse(CS.check(self.C, self.run_with("find . -type f | sort > /tmp/a", "cat x"))[0])
        self.assertFalse(CS.check(self.C, self.run_with("ls", "cat x"))[0])


class InsertedRestartKeepsSessionNumbers(unittest.TestCase):
    """Review of 11a620994: a restart the harness inserts after a Build session in another skill's
    journey isn't one of the eval's sessions, so "session": n still names the eval's nth."""

    def test_session_numbers_skip_the_inserted_restart(self):
        mk = lambda n, text, ins=False: {"n": n, "inserted": ins, "turns": [{"role": "ai", "text": text}],
                                         "files_start": {}, "files_end": {}}
        run = {"sessions": [mk(1, "round one"), mk(2, "build asks for a restart"), mk(3, "build after it", True),
                            mk(4, "round two"), mk(5, "go live")]}
        self.assertTrue(CS.check({"type": "ai_contains", "text": "round two", "session": 3}, run)[0])
        self.assertTrue(CS.check({"type": "ai_contains", "text": "go live", "session": 4}, run)[0])
        self.assertFalse(CS.check({"type": "ai_contains", "text": "build after it", "session": 3}, run)[0])
        self.assertIs(CS._file_session(run, 4), run["sessions"][4])
        self.assertIs(CS._file_session(run, None), run["sessions"][-1])


class NT34WebFormStaysOnTheWeb(unittest.TestCase):
    """Review of b3f4b3d41: N-T34's web form is its own form. The plain Not ready check, used on Claude Code,
    Codex, Claude desktop and Microsoft 365, fails the web sentence, and no Claude Code variant is derived."""

    WEB = ("Not ready yet: 1 to fix. Start Build in a new chat. Add your Google Drive to it, then say 'run the "
           "build skill. My files are in Google Drive, in ai-workspace/framework/client-follow-up.'")

    def test_the_web_sentence_fails_the_plain_form_and_passes_its_own(self):
        self.assertFalse(CS.check({"type": "quote", "id": "N-T34", "form": "Not ready"}, _run_of(self.WEB))[0])
        self.assertTrue(CS.check({"type": "quote", "id": "N-T34", "form": "On the web, not ready"}, _run_of(self.WEB))[0])
        plain = "Not ready yet: 1 to fix. Say 'run the build skill.'"
        self.assertTrue(CS.check({"type": "quote", "id": "N-T34", "form": "Not ready"}, _run_of(plain))[0])

    def test_no_claude_code_variant_of_the_web_form(self):
        forms = [ln.form for ln in AL.load().lines if ln.id == "N-T34"]
        self.assertFalse([f for f in forms if f.startswith("On the web, not ready,")])
        self.assertFalse([f for f in AL.load().get("N-T34", "Not ready") if "Start Build in a new chat" in (f.text or "")])

if __name__ == "__main__":
    unittest.main()
