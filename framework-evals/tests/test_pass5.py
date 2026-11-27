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


if __name__ == "__main__":
    unittest.main()
