import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import structure

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "framework-fixtures/edge/e-retired-brought-back/no-registry/framework/client-follow-up/test-results.md"


class VerdictPhrase(unittest.TestCase):
    def setUp(self):
        self.text = FIXTURE.read_text()

    def test_the_10x_lines_phrase_still_passes(self):
        self.assertEqual([p for p in structure.check_results(self.text) if "Verdict" in p], [])

    def test_the_11_0_checks_phrase_passes(self):
        t = self.text.replace("13 of 13 lines met across 4 inputs", "13 of 13 checks met across 4 inputs")
        self.assertEqual([p for p in structure.check_results(t) if "Verdict" in p], [])

    def test_a_verdict_with_no_count_still_fails(self):
        t = self.text.replace("13 of 13 lines met across 4 inputs.", "")
        self.assertTrue([p for p in structure.check_results(t) if "Verdict" in p])


if __name__ == "__main__":
    unittest.main()
