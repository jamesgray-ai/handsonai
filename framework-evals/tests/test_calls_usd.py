#!/usr/bin/env python3
"""harness.calls_usd: a run's real cost when `claude -p --resume` reports running totals.

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import harness as H  # noqa: E402


def skill(session, turn, usd, resumed=None):
    c = {"role": "skill", "session": session, "turn": turn, "total_cost_usd": usd}
    if resumed is not None:
        c["resumed"] = resumed
    return c


class CallsUsd(unittest.TestCase):
    def test_cumulative_series_counts_the_last_value(self):
        calls = [skill(1, 1, 0.40, False), skill(1, 2, 0.45, True), skill(1, 3, 0.60, True)]
        self.assertAlmostEqual(H.calls_usd(calls), 0.60)

    def test_two_sessions_are_two_series(self):
        calls = [skill(1, 1, 0.40, False), skill(1, 2, 0.50, True),
                 skill(2, 1, 0.30, False), skill(2, 2, 0.70, True)]
        self.assertAlmostEqual(H.calls_usd(calls), 0.50 + 0.70)

    def test_a_drop_is_a_reset_counted_whole(self):
        calls = [skill(1, 1, 0.40, False), skill(1, 2, 0.90, True),
                 skill(1, 3, 0.20, True), skill(1, 4, 0.35, True)]
        self.assertAlmostEqual(H.calls_usd(calls), 0.90 + 0.35)

    def test_single_call_roles_count_whole(self):
        # student calls are fresh each turn (a growing prompt, never resumed): each is its own cost
        calls = [{"role": "student", "session": 1, "turn": t, "total_cost_usd": v, "resumed": False}
                 for t, v in enumerate([0.02, 0.01, 0.03], 1)]
        calls += [{"role": "grader", "total_cost_usd": 0.20, "resumed": False},
                  {"role": "rubric", "total_cost_usd": 0.22, "resumed": False},
                  {"role": "run_chat", "total_cost_usd": 0.10, "resumed": False}]
        self.assertAlmostEqual(H.calls_usd(calls), 0.06 + 0.20 + 0.22 + 0.10)

    def test_interleaved_student_calls_dont_break_the_skill_series(self):
        calls = [skill(1, 1, 0.40, False), {"role": "student", "session": 1, "turn": 1, "total_cost_usd": 0.02},
                 skill(1, 2, 0.50, True), {"role": "student", "session": 1, "turn": 2, "total_cost_usd": 0.03}]
        self.assertAlmostEqual(H.calls_usd(calls), 0.50 + 0.05)

    def test_legacy_records_without_resumed(self):
        # rounds before the field: skill turns after the first of their session are resumed
        calls = [skill(1, 1, 0.40), skill(1, 2, 0.45), skill(1, 3, 0.60),
                 {"role": "student", "session": 1, "turn": 1, "total_cost_usd": 0.02},
                 {"role": "student", "session": 1, "turn": 2, "total_cost_usd": 0.03},
                 {"role": "grader", "total_cost_usd": 0.2}]
        self.assertAlmostEqual(H.calls_usd(calls), 0.60 + 0.05 + 0.2)

    def test_missing_cost_counts_zero(self):
        self.assertEqual(H.calls_usd([{"role": "grader", "total_cost_usd": None}]), 0)


if __name__ == "__main__":
    unittest.main()
