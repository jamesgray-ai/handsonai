#!/usr/bin/env python3
"""Build, shape release Pass 3, Tasks 3 to 6: the build record's new shapes.

Task 3 (B3): a workflow that reads no file when it runs has no place: its place row reads
`none — runs in any new chat`, Status `Not needed`.
Task 4 (B4, B5): one fresh-chat run replaces the bare run: the record's `fresh_chat_run` key (`done`,
`skipped: [why]` or `failed: [what]`) replaces `bare_run`, and the leader runs Build's hand-over on Claude
Code and Codex too, so the harness simulates that run chat for Build as it does for Test.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
sys.path.insert(0, str(EVALS))

import check_scripted as CS  # noqa: E402
import leader as L  # noqa: E402
import structure as ST  # noqa: E402
import validate_evals as V  # noqa: E402

RECORD = """---
live_checks:
  gmail-draft: "done: a draft addressed to you in Gmail Drafts"
skills_on: yes
plugins:
  - client-follow-up
write_block: "off"
schedule: none
fingerprints: {}
fresh_chat_run: done
run_folders: []
change_requests: []
---

# Client Follow-Up — Build Record

## What was built
- A skill, client-follow-up, saved inside a plugin of its own, client-follow-up.
- An older version: none that you know of.

## What it can access
**Gmail (your work account).** It creates drafts.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | none — runs in any new chat | — | Not needed | — | — | — | — | — |
| T2 | New skill: S1 | C1 | client-follow-up skill | `built/client-follow-up/SKILL.md` | Created | yes | 1 | 0 | E1: AC1 met | — |
"""


class NoPlaceWhenNothingIsRead(unittest.TestCase):
    def test_a_place_row_not_needed_passes(self):
        self.assertEqual(ST.check_build_record(RECORD), [])

    def test_not_needed_is_only_for_the_place(self):
        bad = RECORD.replace("| Created | yes | 1 | 0 | E1: AC1 met |", "| Not needed | yes | 1 | 0 | E1: AC1 met |")
        self.assertTrue(any("Not needed" in p for p in ST.check_build_record(bad)))


class OneFreshChatRun(unittest.TestCase):
    def test_the_key_sits_where_bare_run_was(self):
        self.assertIn("fresh_chat_run", ST.RECORD_KEYS)
        self.assertNotIn("bare_run", ST.RECORD_KEYS)
        self.assertEqual(ST.RECORD_KEYS[ST.RECORD_KEYS.index("fingerprints") + 1], "fresh_chat_run")

    def test_its_values(self):
        for v in ("done", '"skipped: in fix mode"', '"failed: no practice-run first line"'):
            rec = RECORD.replace("fresh_chat_run: done", f"fresh_chat_run: {v}")
            self.assertEqual(ST.check_build_record(rec), [], v)
        bad = RECORD.replace("fresh_chat_run: done", "fresh_chat_run: yes")
        self.assertTrue(any("fresh_chat_run" in p for p in ST.check_build_record(bad)))

    def test_bare_run_is_the_layout_before_11(self):
        old = RECORD.replace("fresh_chat_run: done", "bare_run:\n  client-follow-up: done")
        self.assertTrue(any("bare_run" in p for p in ST.check_build_record(old)))

    def test_builds_hand_over_is_run_on_claude_code_and_codex(self):
        for key in ("claude-code", "codex"):
            self.assertTrue(L.simulates_leader_runs("build", L.PLATFORMS[key]()), key)
        self.assertFalse(L.simulates_leader_runs("build", L.PLATFORMS["claude-code"](), ev={"leader_runs": "scripted"}))

    def test_builds_chat_hand_over_block_is_found(self):
        msg = ("Copy the grey box below with the copy icon at its top right and paste it into that chat.\n\n"
               "```\nclient-follow-up — practice run\n\nNotes from a call with Dana at Fernhill.\n```")
        self.assertTrue(L.handover_block(msg).startswith("client-follow-up — practice run"))


DENY = ("This is a practice run: if Claude itself asks you to approve sending, posting or changing something, "
        "choose Deny and tell me.")
FIRST_LINE = "If its first line isn't 'Practice run: nothing will be sent or changed.', stop the chat and tell me."
BLOCK = "Copy the grey box below and paste it into that chat.\n\n```\nclient-follow-up — practice run\n\nNotes.\n```"


def run_of(*ai):
    turns = []
    for m in ai:
        turns += [{"role": "student", "text": "go", "student": True}, {"role": "ai", "text": m}]
    return {"sessions": [{"n": 1, "turns": turns, "files_by_turn": [[]] * len(ai), "files_start": {},
                          "files_end": {}, "cap_hit": False}]}


class DenyLineInTheFreshChatHandOver(unittest.TestCase):
    """F5: Build's form of N-F4 is in the fresh-chat run's hand-over, before the block, never after the run."""
    C = {"type": "nf4_before_fresh_run"}

    def test_in_the_first_of_two_messages_passes(self):
        first = f"Open a new chat in your Project, then say 'ready' here.\n\n{DENY}\n\n{FIRST_LINE}"
        self.assertTrue(CS.check(self.C, run_of(first, BLOCK))[0])

    def test_in_the_same_message_passes(self):
        self.assertTrue(CS.check(self.C, run_of(DENY + "\n\n" + BLOCK))[0])

    def test_said_only_earlier_in_the_session_fails(self):
        self.assertFalse(CS.check(self.C, run_of(DENY, "Your skill is saved.", BLOCK))[0])

    def test_said_after_the_block_fails(self):
        self.assertFalse(CS.check(self.C, run_of("Say 'ready' here.", BLOCK, DENY))[0])

    def test_no_hand_over_passes(self):
        self.assertTrue(CS.check(self.C, run_of("Your workflow is built and checked."))[0])

    def test_the_validator_knows_it(self):
        self.assertIn("nf4_before_fresh_run", V.REQUIRED)


if __name__ == "__main__":
    unittest.main()
