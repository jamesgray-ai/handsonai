import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from leader import handover_block

BLOCK = "```\nclient-follow-up — practice run\nRound 1\n\nInput: E1-acme\nnotes\n```"


class HandoverBlock(unittest.TestCase):
    def test_one_message_hand_over_still_found(self):
        msg = "Open a new Codex session in `/w`, and paste the block below.\n\n" + BLOCK
        self.assertTrue(handover_block(msg).startswith("client-follow-up"))

    def test_one_message_chat_hand_over(self):
        # chat platforms (Pass 5, E14): setup steps, then the box line, then the box, last
        msg = ("1. Open an incognito chat in Claude, outside any Project.\n\n"
               "Copy the box below with the copy icon at its top right, and paste it into that chat.\n\n" + BLOCK)
        self.assertTrue(handover_block(msg).startswith("client-follow-up"))

    def test_setup_message_with_no_block_is_not_a_hand_over(self):
        msg = "Open an incognito chat in Claude, outside any Project."
        self.assertIsNone(handover_block(msg))

    def test_paste_the_box_below(self):
        msg = "Open a new Codex session in `/w`, and paste the box below.\n\n" + BLOCK
        self.assertTrue(handover_block(msg).startswith("client-follow-up"))

    def test_a_code_block_without_a_paste_ask_is_not_a_hand_over(self):
        self.assertIsNone(handover_block("Here's your requirements excerpt:\n\n" + BLOCK))


if __name__ == "__main__":
    unittest.main()
