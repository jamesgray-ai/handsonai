#!/usr/bin/env python3
"""list_safety_candidates.py proposes safety tests for James to approve (shape release G1).

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import list_safety_candidates as LSC  # noqa: E402


def ev(eid, **kw):
    return {"id": eid, "name": eid.lower(), "tier": "core", "expectations": ["says hello"], **kw}


class Candidates(unittest.TestCase):
    def rows(self, evals, named=()):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "evals.json"
            p.write_text(json.dumps({"skill_name": "test", "evals": evals}))
            return {r["id"]: r for r in LSC.candidates(p, named=set(named))}

    def test_prefix_covers_and_plain(self):
        rows = self.rows([ev("TS-x"), ev("TE-y", covers=["never sends without approval"]), ev("TE-z"),
                          ev("TE-r", tier="regression", safety=True), ev("TE-q", retired=True)])
        self.assertTrue(rows["TS-x"]["proposed"])
        self.assertTrue(rows["TE-y"]["proposed"])
        self.assertFalse(rows["TE-z"]["proposed"])
        self.assertNotIn("TE-r", rows)  # regression evals aren't candidates
        self.assertNotIn("TE-q", rows)  # retired evals aren't either

    def test_named_by_release_notes_always_proposed(self):
        self.assertTrue(self.rows([ev("TE-z")], named=["TE-z"])["TE-z"]["proposed"])


if __name__ == "__main__":
    unittest.main()
