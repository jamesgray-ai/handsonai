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

    def test_named_reason_names_no_release(self):
        # PR #318 review: a reason tied to one release's notes goes stale after it ships
        why = self.rows([ev("TE-z")], named=["TE-z"])["TE-z"]["why"]
        self.assertEqual(why, "named in the release notes")


class GateBanner(unittest.TestCase):
    def test_named_safety_run_says_partial(self):
        # PR #318 review: `--tier safety <ids>` must never read as the whole gate
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        import run_eval as R
        self.assertIn("partial gate run", R.safety_banner(3, named=True))
        self.assertNotIn("partial", R.safety_banner(9, named=False))


if __name__ == "__main__":
    unittest.main()
