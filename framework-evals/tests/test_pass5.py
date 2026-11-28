#!/usr/bin/env python3
"""Shape release Pass 5: the end-to-end fixes (E1–E32, James's Claude desktop run, 2026-11-27).

Task 1: the build record's new keys (uses_skills, kept_from_existing, shared_with) and the practice-run
line's two cases (E22, plan review C3): a short preamble before the line, ahead of anything the workflow
produced, stands; a draft, question or stop before the line is refused. Test never says a reply with a
preamble "starts with" the line.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
sys.path.insert(0, str(EVALS))

import check_scripted as CS  # noqa: E402
import structure as ST  # noqa: E402

RECORD = """---
skills_on: yes
plugins:
  - case-study-information-request
write_block: "off"
schedule: none
fingerprints: {}
fresh_chat_run: done
run_folders: []
change_requests: []
---

# Case Study Information Request — Build Record

## What was built
- A skill, case-study-information-request.
- An older version: none that you know of.

## What it can access
No connections.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | none — runs in any new chat | — | Not needed | — | — | — | — | — |
| T1 | Extended skill: S1 | — | case-study-information-request | `built/case-study-information-request/SKILL.md` | Extended | yes | 1 | 0 | E1: AC1–AC8 met | — |
"""

NEW_KEYS = """uses_skills:
  - plugin: jamesgray-os
    skill: applying-brand-guidelines
kept_from_existing:
  - part: case-study-information-request
    item: "the line offering a call at the booking link"
    kept: "no"
shared_with:
  - workflow: framework-v-next
    schedule: none
    until: "go-live of B1"
"""


def with_keys(text=NEW_KEYS):
    return RECORD.replace("change_requests: []\n", "change_requests: []\n" + text)


class RecordNewKeys(unittest.TestCase):
    def test_record_new_keys(self):
        self.assertEqual(ST.check_build_record(with_keys()), [])
        for k in ("uses_skills", "kept_from_existing", "shared_with"):
            self.assertIn(k, ST.RECORD_KEYS)

    def test_an_unknown_key_still_fails(self):
        self.assertTrue(any("not in rules" in p for p in ST.check_build_record(with_keys("depends_on: []\n"))))

    def test_shapes(self):
        bad = with_keys("uses_skills:\n  - applying-brand-guidelines\n")
        self.assertTrue(any("uses_skills" in p for p in ST.check_build_record(bad)))
        bad = with_keys("kept_from_existing:\n  - part: x\n    item: y\n")
        self.assertTrue(any("kept_from_existing" in p for p in ST.check_build_record(bad)))
        bad = with_keys("shared_with:\n  - workflow: x\n    schedule: sometimes\n    until: z\n")
        self.assertTrue(any("shared_with" in p for p in ST.check_build_record(bad)))


LINE = "Practice run: nothing will be sent or changed."
PREAMBLE = "I'll run the case study request skill on all seven practice inputs, drafting only."
DRAFT = "Subject: A case study about our work together\n\nHi Dana,\n\nThank you for working with us."


class PracticeLineBeforeOutput(unittest.TestCase):
    def test_practice_line_before_output(self):
        self.assertEqual(CS.practice_line_position(f"{LINE}\n\n{DRAFT}"), "first")
        self.assertEqual(CS.practice_line_position(f"{PREAMBLE}\n\n{LINE}\n\n{DRAFT}"), "after_preamble")
        self.assertEqual(CS.practice_line_position(f"{DRAFT}\n\n{LINE}"), "after_output")
        self.assertEqual(CS.practice_line_position(DRAFT), "missing")

    def test_a_question_or_a_stop_before_the_line_is_output(self):
        self.assertEqual(CS.practice_line_position(f"Which client is this for?\n\n{LINE}"), "after_output")
        self.assertEqual(CS.practice_line_position(f"```\nInput 1:\nDraft\n```\n\n{LINE}"), "after_output")

    def test_stands(self):
        self.assertTrue(CS.practice_line_stands(f"{PREAMBLE}\n\n{LINE}\n\n{DRAFT}"))
        self.assertFalse(CS.practice_line_stands(f"{DRAFT}\n\n{LINE}"))


def run_of(*turns):
    out = []
    for who, text in turns:
        out.append({"role": "student" if who == "leader" else "ai", "text": text})
    return {"sessions": [{"n": 1, "turns": out, "files_by_turn": [[]] * len(out), "files_start": {},
                          "files_end": {}, "cap_hit": False}]}


class NoFalseFirstLineClaim(unittest.TestCase):
    C = {"type": "no_false_first_line_claim"}

    def test_no_false_first_line_claim(self):
        pasted = f"{PREAMBLE}\n\n{LINE}\n\n{DRAFT}"
        bad = run_of(("leader", pasted), ("ai", "Your block starts with the practice-run line, and nothing was sent."))
        self.assertFalse(CS.check(self.C, bad)[0])
        good = run_of(("leader", pasted), ("ai", "A short line came before the practice-run line, before the workflow "
                                                 "started, so the run stands."))
        self.assertTrue(CS.check(self.C, good)[0])

    def test_a_reply_that_does_start_with_it_may_say_so(self):
        run = run_of(("leader", f"{LINE}\n\n{DRAFT}"), ("ai", "Your block starts with the practice-run line."))
        self.assertTrue(CS.check(self.C, run)[0])

    def test_known_to_validate(self):
        import validate_evals as V
        self.assertIn("no_false_first_line_claim", V.REQUIRED)


# ---------------------------------------------------------------- Task 2: the practice-chat hand-over

DENY_BUILD = ("This is a practice run: if Claude itself asks you to approve sending, posting or changing something, "
              "choose Deny and tell me.")
DENY_TEST = DENY_BUILD + " Answer the workflow's own questions as you would at work."
BOX = "```\nclient-follow-up — practice run\nRound 1\n\nInput 1:\nNotes.\n```"
SETUP = ("1. Open an incognito chat in Claude, outside any Project.\n"
         "2. If 'Practice run: nothing will be sent or changed.' doesn't come before its first draft or question, "
         "stop the chat and tell me.")
AFTER = ("When it finishes, click the Copy icon under its last reply. That copies the whole reply. Paste all of it here.\n\n"
         "Copy the box below with the copy icon at its top right, and paste it into that chat.")


def ai_run(*ai):
    return run_of(*[x for m in ai for x in (("leader", "go"), ("ai", m))])


class HandoverOneMessage(unittest.TestCase):
    C = {"type": "handover_one_message"}

    def test_handover_one_message(self):
        one = f"{SETUP}\n\n{DENY_TEST}\n\n{AFTER}\n\n{BOX}"
        self.assertTrue(CS.check(self.C, ai_run(one))[0])

    def test_two_messages_with_ready_fails(self):
        first = f"{SETUP} Then say 'ready' here."
        self.assertFalse(CS.check(self.C, ai_run(first, f"{AFTER}\n\n{BOX}"))[0])

    def test_text_after_the_box_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(f"{SETUP}\n\n{DENY_TEST}\n\n{AFTER}\n\n{BOX}\n\nSay 'done' when it's open."))[0])

    def test_a_box_with_no_setup_before_it_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(f"Copy the box below and paste it into that chat.\n\n{BOX}"))[0])

    def test_no_hand_over_passes(self):
        self.assertTrue(CS.check(self.C, ai_run("Your workflow is built."))[0])


class DenyLineUnconditional(unittest.TestCase):
    C = {"type": "deny_in_every_handover"}

    def test_deny_line_unconditional(self):
        # a workflow with no sending connection: the leader's other connections stay on, so the Deny line is said anyway
        without = f"{SETUP}\n\n{AFTER}\n\n{BOX}"
        self.assertFalse(CS.check(self.C, ai_run(without))[0])
        for deny in (DENY_TEST, DENY_BUILD):
            self.assertTrue(CS.check(self.C, ai_run(f"{SETUP}\n\n{deny}\n\n{AFTER}\n\n{BOX}"))[0], deny)

    def test_said_only_in_an_earlier_message_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(DENY_TEST, f"{SETUP}\n\n{AFTER}\n\n{BOX}"))[0])

    def test_builds_fresh_run_check_drops_the_earlier_message(self):
        first = f"Open a new chat in your Project.\n\n{DENY_BUILD}"
        box = "Copy the box below and paste it into that chat.\n\n```\nclient-follow-up — practice run\n\nNotes.\n```"
        self.assertFalse(CS.check({"type": "nf4_before_fresh_run"}, ai_run(first, box))[0])

    def test_known_to_validate(self):
        import validate_evals as V
        for t in ("handover_one_message", "deny_in_every_handover"):
            self.assertIn(t, V.REQUIRED)


# ---------------------------------------------------------------- Task 3: what a built part carries

KEEP_Q = ("Your drafting-client-emails skill also offers a call at calendly.com/alex-brennan/intro, which your plan "
          "doesn't ask for. Keep it or drop it?")
CARD = "Click Save skill on the save card under this message to save drafting-client-emails.skill."


class KeptItemsListed(unittest.TestCase):
    C = {"type": "asked_before_save", "pattern": "(?i)(?:calendly|booking link)[^?\\n]*\\b(?:keep|drop)\\b"}

    def test_kept_items_listed(self):
        self.assertTrue(CS.check(self.C, ai_run(KEEP_Q, CARD))[0])

    def test_save_card_with_no_keep_or_drop_question_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(CARD))[0])

    def test_question_only_after_the_card_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(CARD, KEEP_Q))[0])

    def test_an_anchor_in_place_of_the_save_offer(self):
        c = dict(self.C, anchor="```[^\\n]*\\n\\s*Skill brief:")
        brief = "```\nSkill brief: drafting-client-emails\nWhat it does: drafts.\n```"
        self.assertTrue(CS.check(c, ai_run(KEEP_Q, brief))[0])
        self.assertFalse(CS.check(c, ai_run(brief, KEEP_Q))[0])

    def test_known_to_validate(self):
        import validate_evals as V
        self.assertEqual(V.REQUIRED.get("asked_before_save"), ["pattern"])


# ---------------------------------------------------------------- Task 4: grading, verdict and go-live

GRADING_OLD = ("Input 1 met all 12 lines it was tested on. Input 2 met 14.\n\nDo you agree with these? And for each draft, "
               "would you edit it not at all, a little or a lot?")
GRADING_NEW = ("All 7 inputs behaved: every check met, nothing sent.\n\n| Input | What it had to do | | Anything to look at |\n"
               "|---|---|---|---|\n| Input 1 | Ask for results, invent none | ✅ | — |\n\nTell me if any of these looks wrong.\n\n"
               "The checks show it does what you wrote down; this shows whether it's good enough to use. The drafts are "
               "Input 1, 2, 5 and 6 in your practice chat: would you edit each not at all, a little or a lot?")


class GradingOneQuestion(unittest.TestCase):
    C = {"type": "one_question", "containing": "(?i)not at all, a little or a lot", "not_pattern": "(?i)\\bdo you agree\\b"}

    def test_grading_one_question(self):
        self.assertTrue(CS.check(self.C, ai_run(GRADING_NEW))[0])
        self.assertFalse(CS.check(self.C, ai_run(GRADING_OLD))[0])

    def test_a_question_before_the_last_paragraph_fails(self):
        two = GRADING_NEW.replace("Tell me if any of these looks wrong.", "Does any of these look wrong?")
        self.assertFalse(CS.check(self.C, ai_run(two))[0])

    def test_none_said_fails_closed(self):
        self.assertFalse(CS.check(self.C, ai_run("Your workflow is built."))[0])


GOLIVE_INLINE = ("It's live.\n\nRe-check it any time with 'test the workflow I built', especially if you find yourself "
                 "editing more than you used to. To change it, say 'change my workflow. My files are in ai-workspace/framework/x.'")
GOLIVE_BLOCKS = ("It's live.\n\nRe-check it any time, especially if you find yourself editing more than you used to. "
                 "To re-check it, say:\n\n```\ntest the workflow I built. My files are in ai-workspace/framework/x.\n```\n\n"
                 "To change it, say:\n\n```\nchange my workflow. My files are in ai-workspace/framework/x.\n```")


class GoLivePhrasesInBlocks(unittest.TestCase):
    C = {"type": "phrases_in_blocks", "containing": "(?i)\\bIt's live\\b"}

    def test_golive_phrases_in_blocks(self):
        self.assertTrue(CS.check(self.C, ai_run(GOLIVE_BLOCKS))[0])
        self.assertFalse(CS.check(self.C, ai_run(GOLIVE_INLINE))[0])

    def test_known_to_validate(self):
        import validate_evals as V
        self.assertEqual(V.REQUIRED.get("one_question"), ["containing"])
        self.assertIn("phrases_in_blocks", V.REQUIRED)


# ---------------------------------------------------------------- Task 5: Build's wording

import json as _json
import tempfile as _tempfile

BRIEF = "```\nSkill brief: case-study-information-request\nWhat it does: drafts the request email.\n```"


def events_run(events):
    root = Path(_tempfile.mkdtemp()) / "workspace"
    root.mkdir()
    lines = [{"type": "system", "subtype": "init"}]
    for kind, val in events:
        if kind == "text":
            lines.append({"type": "assistant", "message": {"content": [{"type": "text", "text": val}]}})
        else:
            lines.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": kind, "input": val}]}})
    (root.parent / "events.jsonl").write_text("\n".join(_json.dumps(x) for x in lines))
    run = run_of(*[("ai", v) for k, v in events if k == "text"])
    run["sessions"][0]["root"] = str(root)
    return run


class BriefShownInText(unittest.TestCase):
    C = {"type": "brief_in_text"}
    WRITE = ("Write", {"file_path": "./sandbox/case-study-information-request/SKILL.md", "content": "x"})

    def test_brief_shown_in_text(self):
        ok = events_run([("text", "Here's what I'm asking the skill creator to make:\n\n" + BRIEF), self.WRITE])
        self.assertTrue(CS.check(self.C, ok)[0])

    def test_brief_only_in_a_tool_call_fails(self):
        only_tool = events_run([("Write", {"file_path": "./sandbox/brief.md", "content": BRIEF}), self.WRITE,
                                ("text", "1 of 2: Update the case study request skill — drafted and checked")])
        self.assertFalse(CS.check(self.C, only_tool)[0])

    def test_brief_after_the_creator_started_fails(self):
        late = events_run([self.WRITE, ("text", "Here's what I'm asking the skill creator to make:\n\n" + BRIEF)])
        self.assertFalse(CS.check(self.C, late)[0])

    def test_no_events_fails_closed(self):
        self.assertFalse(CS.check(self.C, run_of(("ai", BRIEF)))[0])


# ---------------------------------------------------------------- Task 6: Design

def _plan():
    """A Design Plan as Build's fixtures write it (approved), built fresh by the build workspace's fixture builder."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("bfx", EVALS.parent / "build-workspace" / "evals" / "fixtures" / "make_fixture.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    t = str(Path(_tempfile.mkdtemp()) / "w")
    B.FIXTURES["cc-first"](t)
    return (Path(t) / "framework" / "client-follow-up" / "design-plan.md").read_text()


class ApprovalRefusedWithQuestionToAsk(unittest.TestCase):
    TO_ASK = ("## Open items\n1. **Reuse the existing case study request skill (to ask).** Why it matters: it decides "
              "whether T1 extends it. Blocks: T1. Who answers: you. Safe default: none (not a safety item).")
    WAITING = ("## Open items\n1. **Access to the shared Call notes folder.** Why it matters: T1 reads it. Blocks: T1. "
               "Who answers: IT. Safe default: none (not a safety item).")

    def test_approval_refused_with_question_to_ask(self):
        plan = _plan()
        self.assertIn("approved: true", plan)
        bad = plan.replace("## Open items\nNone.", self.TO_ASK)
        self.assertTrue(any("to ask" in p for p in ST.check_plan(bad, written=False)))

    def test_an_item_waiting_on_access_is_allowed(self):
        ok = _plan().replace("## Open items\nNone.", self.WAITING)
        self.assertFalse(any("to ask" in p for p in ST.check_plan(ok, written=False)))

    def test_a_draft_may_hold_a_question_to_ask(self):
        draft = _plan().replace("approved: true", "approved: false").replace("## Open items\nNone.", self.TO_ASK)
        self.assertFalse(any("to ask" in p for p in ST.check_plan(draft, written=False)))


def choice_events(*steps):
    """An events.jsonl: ("ask", question) is an AskUserQuestion call, ("pick", answer) its result, ("write", text) a
    Write to the plan, ("say", text) the AI's text; one result event closes the turn."""
    lines = [{"type": "system", "subtype": "init"}]
    for kind, val in steps:
        if kind == "ask":
            lines.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "AskUserQuestion", "input": {"questions": [{"question": val}]}}]}})
        elif kind == "pick":
            lines.append({"type": "user", "message": {"content": [{"type": "tool_result", "content": val}]}})
        elif kind == "write":
            lines.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "input": {"file_path": "/w/framework/x/design-plan.md", "content": val}}]}})
        else:
            lines.append({"type": "assistant", "message": {"content": [{"type": "text", "text": val}]}})
    lines.append({"type": "result"})
    root = Path(_tempfile.mkdtemp()) / "workspace"
    root.mkdir()
    (root.parent / "events.jsonl").write_text("\n".join(_json.dumps(x) for x in lines))
    run = run_of(("leader", "run the design skill"), ("ai", "\n".join(v for k, v in steps if k == "say") or "ok"))
    run["sessions"][0]["root"] = str(root)
    return run


class WidgetAnswerSaved(unittest.TestCase):
    C = {"type": "saved_before_next_question", "path": "*design-plan.md", "pattern": "Add to it", "answer": "(?i)add to it"}
    Q1 = "Use your existing skill as it is, add to it, or build a new one?"
    Q2 = "Where should the draft be saved?"

    def test_widget_answer_saved(self):
        run = choice_events(("ask", self.Q1), ("pick", "Add to it"), ("write", "Open item 1 Answered: Add to it"), ("ask", self.Q2))
        self.assertTrue(CS.check(self.C, run)[0])

    def test_next_choice_before_the_save_fails(self):
        run = choice_events(("ask", self.Q1), ("pick", "Add to it"), ("ask", self.Q2), ("write", "Answered: Add to it"))
        self.assertFalse(CS.check(self.C, run)[0])

    def test_never_saved_fails(self):
        run = choice_events(("ask", self.Q1), ("pick", "Add to it"), ("say", "Part 4 of 4 — review and approve. Do you approve the plan?"))
        self.assertFalse(CS.check(self.C, run)[0])


# ---------------------------------------------------------------- Task 7: every close

CLOSE_OLD = ("Your workflow is built and checked. Here's what you have: a skill that drafts the request email, saved in your "
             "account. What it can access is written up in your build record, if anyone asks. A copy is in built/. "
             "Nothing is still waiting. Start Test in a new chat and say: test the workflow I built.")
CLOSE_NEW = ("**The booking link is out of the email.**\n\n**What you have:** the case study request skill, updated in "
             "your account. It's yours to read or edit any time.\n\n**Kept for you:** the earlier version, in "
             "`history/kept-copy-2026-11-27-1651/`.\n\n**Next:** start Test in a new chat with your working folder "
             "selected, then say:\n\n```\ntest the workflow I built. My files are in ai-workspace/framework/x.\n```")


class CloseShape(unittest.TestCase):
    C = {"type": "close_shape", "containing": "(?i)test the workflow I built"}

    def test_close_shape(self):
        self.assertTrue(CS.check(self.C, ai_run(CLOSE_NEW))[0])

    def test_one_paragraph_close_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(CLOSE_OLD))[0])

    def test_lines_with_no_news_fail(self):
        noisy = CLOSE_NEW.replace("It's yours to read", "Nothing is still waiting. It's yours to read")
        self.assertFalse(CS.check(self.C, ai_run(noisy))[0])

    def test_phrase_not_last_in_a_code_block_fails(self):
        self.assertFalse(CS.check(self.C, ai_run(CLOSE_NEW + "\n\nGood luck!"))[0])

    def test_claude_codes_slash_note_may_follow_the_block(self):
        self.assertTrue(CS.check(self.C, ai_run(CLOSE_NEW + "\n\n(In Claude Code, you can also type `/test` and pick it from the list.)"))[0])

    def test_headline_optional(self):
        plain = CLOSE_NEW.replace("**The booking link is out of the email.**\n\n", "Workflow Requirements saved to x.\n\n")
        self.assertFalse(CS.check(self.C, ai_run(plain))[0])
        self.assertTrue(CS.check(dict(self.C, headline=False), ai_run(plain))[0])


if __name__ == "__main__":
    unittest.main()
