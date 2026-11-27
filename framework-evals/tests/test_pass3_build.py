#!/usr/bin/env python3
"""Build, shape release Pass 3, Tasks 3 to 6: the build record's new shapes.

Task 3 (B3): a workflow that reads no file when it runs has no place: its place row reads
`none — runs in any new chat`, Status `Not needed`.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
sys.path.insert(0, str(EVALS))

import structure as ST  # noqa: E402

RECORD = """---
live_checks:
  gmail-draft: "done: a draft addressed to you in Gmail Drafts"
skills_on: yes
plugins:
  - client-follow-up
write_block: "off"
schedule: none
fingerprints: {}
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


if __name__ == "__main__":
    unittest.main()
