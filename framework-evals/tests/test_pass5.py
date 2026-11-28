#!/usr/bin/env python3
"""Shape release Pass 5: the end-to-end fixes (E1–E32, James's Claude desktop run, 2026-11-27).

Task 1: the build record's new keys (uses_skills, kept_from_existing, shared_with) and the practice-run
line's two cases (E22, plan review C3): a short preamble before the line, ahead of anything the workflow
produced, stands; a draft, question or stop before the line is refused. Test never says a reply with a
preamble "starts with" the line.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
sys.path.insert(0, str(EVALS))

import check_scripted as CS  # noqa: E402
import structure as ST  # noqa: E402

RECORD = """---
skills_on: yes
plugins:
  - case-study-information-request
write_block: "off"
schedule: none
fingerprints: {}
fresh_chat_run: done
run_folders: []
change_requests: []
---

# Case Study Information Request — Build Record

## What was built
- A skill, case-study-information-request.
- An older version: none that you know of.

## What it can access
No connections.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | none — runs in any new chat | — | Not needed | — | — | — | — | — |
| T1 | Extended skill: S1 | — | case-study-information-request | `built/case-study-information-request/SKILL.md` | Extended | yes | 1 | 0 | E1: AC1–AC8 met | — |
"""

NEW_KEYS = """uses_skills:
  - plugin: jamesgray-os
    skill: applying-brand-guidelines
kept_from_existing:
  - part: case-study-information-request
    item: "the line offering a call at the booking link"
    kept: "no"
shared_with:
  - workflow: framework-v-next
    schedule: none
    until: "go-live of B1"
"""


def with_keys(text=NEW_KEYS):
    return RECORD.replace("change_requests: []\n", "change_requests: []\n" + text)


class RecordNewKeys(unittest.TestCase):
    def test_record_new_keys(self):
        self.assertEqual(ST.check_build_record(with_keys()), [])
        for k in ("uses_skills", "kept_from_existing", "shared_with"):
            self.assertIn(k, ST.RECORD_KEYS)

    def test_an_unknown_key_still_fails(self):
        self.assertTrue(any("not in rules" in p for p in ST.check_build_record(with_keys("depends_on: []\n"))))

    def test_shapes(self):
        bad = with_keys("uses_skills:\n  - applying-brand-guidelines\n")
        self.assertTrue(any("uses_skills" in p for p in ST.check_build_record(bad)))
        bad = with_keys("kept_from_existing:\n  - part: x\n    item: y\n")
        self.assertTrue(any("kept_from_existing" in p for p in ST.check_build_record(bad)))
        bad = with_keys("shared_with:\n  - workflow: x\n    schedule: sometimes\n    until: z\n")
        self.assertTrue(any("shared_with" in p for p in ST.check_build_record(bad)))


LINE = "Practice run: nothing will be sent or changed."
PREAMBLE = "I'll run the case study request skill on all seven practice inputs, drafting only."
DRAFT = "Subject: A case study about our work together\n\nHi Dana,\n\nThank you for working with us."


class PracticeLineBeforeOutput(unittest.TestCase):
    def test_practice_line_before_output(self):
        self.assertEqual(CS.practice_line_position(f"{LINE}\n\n{DRAFT}"), "first")
        self.assertEqual(CS.practice_line_position(f"{PREAMBLE}\n\n{LINE}\n\n{DRAFT}"), "after_preamble")
        self.assertEqual(CS.practice_line_position(f"{DRAFT}\n\n{LINE}"), "after_output")
        self.assertEqual(CS.practice_line_position(DRAFT), "missing")

    def test_a_question_or_a_stop_before_the_line_is_output(self):
        self.assertEqual(CS.practice_line_position(f"Which client is this for?\n\n{LINE}"), "after_output")
        self.assertEqual(CS.practice_line_position(f"```\nInput 1:\nDraft\n```\n\n{LINE}"), "after_output")

    def test_stands(self):
        self.assertTrue(CS.practice_line_stands(f"{PREAMBLE}\n\n{LINE}\n\n{DRAFT}"))
        self.assertFalse(CS.practice_line_stands(f"{DRAFT}\n\n{LINE}"))


def run_of(*turns):
    out = []
    for who, text in turns:
        out.append({"role": "student" if who == "leader" else "ai", "text": text})
    return {"sessions": [{"n": 1, "turns": out, "files_by_turn": [[]] * len(out), "files_start": {},
                          "files_end": {}, "cap_hit": False}]}


class NoFalseFirstLineClaim(unittest.TestCase):
    C = {"type": "no_false_first_line_claim"}

    def test_no_false_first_line_claim(self):
        pasted = f"{PREAMBLE}\n\n{LINE}\n\n{DRAFT}"
        bad = run_of(("leader", pasted), ("ai", "Your block starts with the practice-run line, and nothing was sent."))
        self.assertFalse(CS.check(self.C, bad)[0])
        good = run_of(("leader", pasted), ("ai", "A short line came before the practice-run line, before the workflow "
                                                 "started, so the run stands."))
        self.assertTrue(CS.check(self.C, good)[0])

    def test_a_reply_that_does_start_with_it_may_say_so(self):
        run = run_of(("leader", f"{LINE}\n\n{DRAFT}"), ("ai", "Your block starts with the practice-run line."))
        self.assertTrue(CS.check(self.C, run)[0])

    def test_known_to_validate(self):
        import validate_evals as V
        self.assertIn("no_false_first_line_claim", V.REQUIRED)


# ---------------------------------------------------------------- Task 2: the practice-chat hand-over

DENY_BUILD = ("This is a practice run: if Claude itself asks you to approve sending, posting or changing something, "
              "choose Deny and tell me.")
DENY_TEST = DENY_BUILD + " Answer the workflow's own questions as you would at work."
BOX = "```\nclient-follow-up — practice run\nRound 1\n\nInput 1:\nNotes.\n```"
SETUP = ("1. Open an incognito chat in Claude, outside any Project.\n"
         "2. If 'Practice run: nothing will be sent or changed.' doesn't come before its first draft or question, "
         "stop the chat and tell me.")
AFTER = ("When it finishes, click the Copy icon under its last reply. That copies the whole reply. Paste all of it here.\n\n"
         "Copy the box below with the copy icon at its top right, and paste it into that chat.")


def ai_run(*ai):
    return run_of(*[x for m in ai for x in (("leader", "go"), ("ai", m))])


class HandoverOneMessage(unittest.TestCase):
    C = {"type": "handover_one_message"}

    def test_handover_one_message(self):
        one = f"{SETUP}\n\n{DENY_TEST}\n\n{AFTER}\n\n{BOX}"
        self.assertTrue(CS.check(self.C, ai_run(one))[0])

    def test_two_messages_with_ready_fails(self):
        first = f"{SETUP} Then say 'ready' here."
        self.assertFalse(CS.check(self.C, ai_run(first, f"{AFTER}\n\n{BOX}"))[0])

    def test_text_after_the_box_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(f"{SETUP}\n\n{DENY_TEST}\n\n{AFTER}\n\n{BOX}\n\nSay 'done' when it's open."))[0])

    def test_a_box_with_no_setup_before_it_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(f"Copy the box below and paste it into that chat.\n\n{BOX}"))[0])

    def test_no_hand_over_passes(self):
        self.assertTrue(CS.check(self.C, ai_run("Your workflow is built."))[0])


class DenyLineUnconditional(unittest.TestCase):
    C = {"type": "deny_in_every_handover"}

    def test_deny_line_unconditional(self):
        # a workflow with no sending connection: the leader's other connections stay on, so the Deny line is said anyway
        without = f"{SETUP}\n\n{AFTER}\n\n{BOX}"
        self.assertFalse(CS.check(self.C, ai_run(without))[0])
        for deny in (DENY_TEST, DENY_BUILD):
            self.assertTrue(CS.check(self.C, ai_run(f"{SETUP}\n\n{deny}\n\n{AFTER}\n\n{BOX}"))[0], deny)

    def test_said_only_in_an_earlier_message_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(DENY_TEST, f"{SETUP}\n\n{AFTER}\n\n{BOX}"))[0])

    def test_builds_fresh_run_check_drops_the_earlier_message(self):
        first = f"Open a new chat in your Project.\n\n{DENY_BUILD}"
        box = "Copy the box below and paste it into that chat.\n\n```\nclient-follow-up — practice run\n\nNotes.\n```"
        self.assertFalse(CS.check({"type": "nf4_before_fresh_run"}, ai_run(first, box))[0])

    def test_known_to_validate(self):
        import validate_evals as V
        for t in ("handover_one_message", "deny_in_every_handover"):
            self.assertIn(t, V.REQUIRED)


# ---------------------------------------------------------------- Task 3: what a built part carries

KEEP_Q = ("Your drafting-client-emails skill also offers a call at calendly.com/alex-brennan/intro, which your plan "
          "doesn't ask for. Keep it or drop it?")
CARD = "Click Save skill on the save card under this message to save drafting-client-emails.skill."


class KeptItemsListed(unittest.TestCase):
    C = {"type": "asked_before_save", "pattern": "(?i)(?:calendly|booking link)[^?\\n]*\\b(?:keep|drop)\\b"}

    def test_kept_items_listed(self):
        self.assertTrue(CS.check(self.C, ai_run(KEEP_Q, CARD))[0])

    def test_save_card_with_no_keep_or_drop_question_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(CARD))[0])

    def test_question_only_after_the_card_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(CARD, KEEP_Q))[0])

    def test_an_anchor_in_place_of_the_save_offer(self):
        c = dict(self.C, anchor="```[^\\n]*\\n\\s*Skill brief:")
        brief = "```\nSkill brief: drafting-client-emails\nWhat it does: drafts.\n```"
        self.assertTrue(CS.check(c, ai_run(KEEP_Q, brief))[0])
        self.assertFalse(CS.check(c, ai_run(brief, KEEP_Q))[0])

    def test_known_to_validate(self):
        import validate_evals as V
        self.assertEqual(V.REQUIRED.get("asked_before_save"), ["pattern"])


if __name__ == "__main__":
    unittest.main()
