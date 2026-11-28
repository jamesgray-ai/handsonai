#!/usr/bin/env python3
"""Fixes from Pass 0's review (shape release): the safety gate never shrinks silently, and a
regrade's judge sees the skill's platform facts as the original run's did.

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import regrade as RG  # noqa: E402
import validate_evals as VE  # noqa: E402


def ev(eid, **kw):
    base = {"id": eid, "name": eid, "expected_output": "x", "expectations": ["x"], "files": [],
            "prompt": "hi", "tier": "core"}
    base.update(kw)
    return base


def write_evals(tmp, evals):
    p = Path(tmp) / "evals.json"
    p.write_text(json.dumps({"skill_name": "build", "how_to_run": "x", "evals": evals}))
    return p


def errors(evals):
    with tempfile.TemporaryDirectory() as tmp:
        return VE.validate_file(write_evals(tmp, evals))


class RegradeKeepsTheSkill(unittest.TestCase):
    def test_rebuilt_run_carries_the_skill_name(self):
        with tempfile.TemporaryDirectory() as t:
            rdir = Path(t) / "run-1"
            (rdir / "session-1").mkdir(parents=True)
            (rdir / "eval.json").write_text(json.dumps({"id": "X", "prompt": "hi", "fixture": "empty"}))
            (rdir / "session-1" / "turns.json").write_text("[]")
            work = Path(t) / "work"
            work.mkdir()
            run = RG.rebuild_run(rdir, Path(t), {"skill_name": "build"}, work)
        self.assertEqual(run.get("skill"), "build")


class BlockedSafetyEvalFailsTheGate(unittest.TestCase):
    def test_blocked_safety_eval_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write_evals(tmp, [ev("S1", safety=True), ev("S2", safety=True, blocked_on="T99")])
            r = subprocess.run([sys.executable, str(HERE / "run_eval.py"), str(Path(tmp) / "out"),
                                "--evals", str(p), "--tier", "safety", "--dry-run"],
                               capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("blocked safety evals", r.stderr + r.stdout)
        self.assertIn("S2", r.stderr + r.stdout)


class SafetyFlagIsChecked(unittest.TestCase):
    def test_mixed_platform_safety_eval_needs_three_runs(self):
        e = ev("A", safety=True, core_runs=1, sessions=[{"prompt": "a"}, {"prompt": "b", "platform": "codex"}])
        e.pop("prompt")
        errs = errors([e])
        self.assertTrue(any("a safety eval runs 3 times" in x for x in errs), errs)

    def test_misspelled_safety_key_is_an_error(self):
        for key in ("Safety", "safe", "SAFETY"):
            errs = errors([ev("A", **{key: True})])
            self.assertTrue(any("did you mean safety" in x for x in errs), (key, errs))


if __name__ == "__main__":
    unittest.main()
