#!/usr/bin/env python3
"""The safety flag and `--tier safety`: the shape release's paid gate is the tagged safety tests
only, 3 runs each (1 on Microsoft 365 and Codex).

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
import run_eval as RE  # noqa: E402
import validate_evals as VE  # noqa: E402


def ev(eid, **kw):
    base = {"id": eid, "name": eid, "expected_output": "x", "expectations": ["x"], "files": [],
            "prompt": "hi", "tier": "core"}
    base.update(kw)
    return base


def write_evals(tmp, evals):
    p = Path(tmp) / "evals.json"
    p.write_text(json.dumps({"skill_name": "test", "how_to_run": "x", "evals": evals}))
    return p


def errors(evals):
    with tempfile.TemporaryDirectory() as tmp:
        return VE.validate_file(write_evals(tmp, evals))


class SafetyValidation(unittest.TestCase):
    def test_safety_on_regression_is_an_error(self):
        errs = errors([ev("A", tier="regression", safety=True)])
        self.assertTrue(any("safety is set only on a core eval" in e for e in errs), errs)

    def test_safety_must_be_true_boolean(self):
        errs = errors([ev("A", safety="true")])
        self.assertTrue(any("safety must be true" in e for e in errs), errs)

    def test_safety_core_runs_one_on_main_platform(self):
        errs = errors([ev("A", safety=True, core_runs=1, platform="claude-code")])
        self.assertTrue(any("a safety eval runs 3 times" in e for e in errs), errs)
        for plat in ("microsoft-365", "codex"):
            errs = errors([ev("A", safety=True, core_runs=1, platform=plat)])
            self.assertFalse(any("a safety eval runs 3 times" in e for e in errs), (plat, errs))


class SafetySelection(unittest.TestCase):
    def test_is_safety(self):
        data = {"evals": []}
        self.assertTrue(RE.is_safety(ev("A", safety=True), data))
        self.assertFalse(RE.is_safety(ev("B"), data))
        self.assertFalse(RE.is_safety(ev("C", safety=True, retired=True), data))
        self.assertFalse(RE.is_safety(ev("D", safety="true"), data))

    def test_tier_safety_selects_only_safety(self):
        evals = [ev("S1", safety=True), ev("S2", safety=True), ev("C1"), ev("C2"), ev("C3")]
        got = RE.select_tier(evals, {"evals": evals}, "safety")
        self.assertEqual([e["id"] for e in got], ["S1", "S2"])

    def test_tier_safety_none_exits(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write_evals(tmp, [ev("C1"), ev("C2")])
            r = subprocess.run([sys.executable, str(HERE / "run_eval.py"), str(Path(tmp) / "out"),
                                "--evals", str(p), "--tier", "safety", "--dry-run"],
                               capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("no safety evals selected", r.stderr + r.stdout)


if __name__ == "__main__":
    unittest.main()
