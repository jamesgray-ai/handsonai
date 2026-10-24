# Evaluating a skill

## Contents
- What to prepare (every platform)
- Running the tests: Claude Code
- Running the tests: Claude
- Running the tests: other platforms
- The grading prompt
- What to do with the results

Testing is part of building a skill, not a later step. The point is simple: does the skill do the job better than no skill, and does it run when it should?

## What to prepare (every platform)

Prepare these while the skill is being built, from the user's real examples:

1. **Two or three test prompts**, written the way the user would really ask, with real detail (file names, names of reports, the situation).
2. **What good looks like** for each prompt, in plain words: "uses our three brand colors", "flags any deal with no next step". Each becomes a check graded **Met** or **Not met**.
3. **The one case most likely to go wrong**, as an extra test prompt.
4. **About ten trigger prompts:** five that should fire the skill and five near-misses that shouldn't (see `descriptions.md`).

Start small. Two or three test prompts are enough for a first round; add more once you've seen results. Write checks that can be verified from the output ("the report lists every open deal"), not judgments ("the report is good"). Leave qualities that need a person's eye, such as tone, to the user's review.

Save the tests inside the skill folder so they can be run again after every change: `evals/evals.json` on Claude Code, `evals/test-cases.md` elsewhere.

## Running the tests: Claude Code

Give Anthropic's skill-creator the user's real examples in the conversation, ideally before it proposes test prompts, so it builds the tests from them rather than inventing its own. It then:

- runs each test prompt with and without the skill, in separate agents, so the comparison is fair;
- grades the checks, with evidence;
- opens a review page where the user reads each result side by side and writes feedback;
- can tune the description against the trigger prompts.

## Running the tests: Claude

The same handoff works: give skill-creator the examples first. In a Claude task (the desktop app), it can run the tests with and without the skill and grade them, as on Claude Code. In an ordinary Claude chat, it runs the test prompts itself in the conversation with no with-and-without comparison and no description tuning, so treat that as a sanity check and use the by-hand steps below for the comparison.

## Running the tests: other platforms

Check the platform's `skill_evaluation` entry in the platform registry. Where the platform's skill creator can run tests, hand it the same examples first. Where it can't, run the same tests by hand:

1. **Without the skill:** run each test prompt in a fresh chat with the skill turned off, and save the result.
2. **With the skill:** run it in a fresh chat with the skill on, and save the result.
3. **Grade:** paste the checks and both results into a fresh chat with the grading prompt below.
4. **Trigger check:** type each trigger prompt into a fresh chat and note whether the skill activated.
5. **Fix and rerun:** take what failed back to the skill creator, fix the skill, and run everything again as the next round.

A fresh chat each time matters: a conversation that already discussed the skill isn't a fair test.

## The grading prompt

```
You are grading one test of an AI skill. Be strict: a check is Met only if the
result shows concrete evidence for it. A heading with nothing under it is Not met.

Checks:
[paste the checks for this test prompt, one per line]

Result WITHOUT the skill:
[paste]

Result WITH the skill:
[paste]

For each check, give Met or Not met for each result, with a short quote or
specific reference as evidence. Then write a test report with:
- a header: skill name, round, platform, how it ran (by hand), and model;
- the number of checks met with the skill and without it;
- a table with one row per check: test prompt, check, without the skill,
  with the skill, evidence;
- if you ran trigger prompts, a table: prompt, should fire?, fired?, result;
- a "Fix next" list with one line for every check not met with the skill
  and every trigger that misbehaved, ending "Then rerun everything."
```

## What to do with the results

- **A check met with the skill but not without it** is where the skill earns its place. Keep what produced it.
- **A check met either way** tests nothing. Replace it with one that matters.
- **A check not met either way** is either too hard or wrongly written. Fix the check or the test prompt.
- **Results that vary between runs** usually mean an ambiguous instruction. Add an example or tighten the wording.
- **Fix the underlying cause, not the one example.** The skill will meet many prompts the tests never saw.
- Every correction the user makes is a candidate for the skill's gotchas section.

Stop when the checks pass, the user's review finds nothing to change, and a fresh round shows no further gain.

For deeper methods (blind comparison of two versions, benchmarking across many runs, tuning a description with held-out prompts), see the "Going deeper" section of https://handsonai.info/agentic-building-blocks/skills/skill-best-practices/; Anthropic's skill-creator documentation and the AgentSkills.io evaluation guide in `sources.md` go further.
