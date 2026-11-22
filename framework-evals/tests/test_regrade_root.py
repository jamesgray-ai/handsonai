"""final-build fix (2026-11-22): a fixture that writes its own temporary folder into a file is compared
with the round's after the rebuilt folder is put back to the round's."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import regrade as R  # noqa: E402


class RoundRoot(unittest.TestCase):

    def test_the_rounds_folder_is_read_from_the_events(self):
        d = Path(tempfile.mkdtemp())
        (d / "events.jsonl").write_text('{"input": {"command": "cd /private/var/folders/ab/T/handsonai-evals/'
                                        'tmpx9_4z18_/workspace; ls"}}\n')
        self.assertEqual(R.round_root(d / "events.jsonl"), "/private/var/folders/ab/T/handsonai-evals/tmpx9_4z18_")
        self.assertIsNone(R.round_root(d / "missing.jsonl"))

    def test_the_rebuilt_folder_is_put_back(self):
        files = {".claude/settings.local.json": '"Write(//tmp/new12345/workspace/framework/.bin/**)"'}
        out = R.put_back_root(files, "/tmp/new12345", "/var/T/tmpold_1234")
        self.assertEqual(out[".claude/settings.local.json"], '"Write(//var/T/tmpold_1234/workspace/framework/.bin/**)"')
        self.assertIs(R.put_back_root(files, "/tmp/new12345", None), files)


if __name__ == "__main__":
    unittest.main()
