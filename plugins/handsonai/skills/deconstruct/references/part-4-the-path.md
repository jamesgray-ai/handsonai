# Part 4: The path

Read when Part 4 starts, right after its signpost. Purpose: what only the student knows about how the work should go. Design uses it to decide how much the AI works out on its own; Deconstruct never decides that. Every quoted line is said exactly; each question is its own message.

## Contents

- 1. Method
- 2. The headline path
- No method yet (replaces question 3)
- 3. Fixed or flexible, and gates
- 4. Decisions
- Regulated work
- 5. The range
- 6. Expertise
- Detail only where it matters

## 1. Method

On cold entry, play the describe-first answer back as the method, one line per step, ending "What's wrong?", in place of this question. In a personal-life registry, the personal-life wording replaces it.

**Ask:** "If you handed this to a skilled colleague, how would you want them to go about it?"
- *Why:* Design uses your method to decide which steps the AI follows exactly and which it works out itself.

**The answer stops early unless the student has said that's the end.** A method that ends where the deliverable is produced ("then write it up") has still stopped early: people leave out what happens after, such as their own review. So after the method answer, in its own message, **Ask:** "What comes after that?", repeated until the student says that's all or says they don't know. If they don't know, **Ask:** "Want me to propose the rest, and you correct it?"
- *Not sure?* Say yes, and correct what I propose.

Only the steps you add carry `· proposed by AI`; the student's own steps stay theirs. There is no step-count threshold.

**When the work is done today**, in its own message, **Ask:** "Is that how you do it today, or is it different?"

**If that answer (or any answer here) runs past a short paragraph**, your next message plays it back in plain words, one line per step, ending "What's wrong?": no prose summary, and no other question in that message. Only after the student confirms the playback, ask about the differences. When the two differ, the Path records how the student wants it done; for each step or workaround from today's way, one difference per message, **Ask:** "Today you also [step or workaround]. Should that stay?" A step or workaround they drop is not a step.

## 2. The headline path

Play the steps back in plain words, one line per step, and let the student correct it, ending "What's wrong?". As you play back, tag each step's `uses` and `writes` from the method answers (C# and W# are numbered only when written to the file).

Then, in its own message, **Ask:** "Which of these does a person do?" For each step named without who does it, **Ask:** "Who does [step]?"

A person's step carries the role tag: `(you)`, or the role in parentheses, such as `(finance team)`, meaning a person still performs this step in the new workflow. Untagged steps are AI steps.

## No method yet

Only when the student says at question 1 that they have no method at all: propose the whole path (recorded with the line `Path: proposed by AI`) and play it back as in question 2. Each proposed step carries `· proposed by AI` and stays flexible. In place of question 3:

**Ask:** "Which of these would you insist on?"
- *Why:* Steps you insist on are followed exactly; the rest the AI may change.
- *Not sure?* Insist on none for now. Test will show which steps matter.

"Insist on none" is a complete answer: every step stays flexible and keeps its tag. A step the student insists on becomes `fixed (your judgment)` and loses the tag; so does an AI-added step the student marks fixed, or one the regulation question marks `fixed (regulation)`. If the student insists on any step, the `Path: proposed by AI` line stays. The person-and-role question, the per-step gate question and questions 4 to 6 still run.

## 3. Fixed or flexible, and gates

After the path is corrected:

**Ask:** "Which of those must happen exactly that way, every time?"

On first use, say: "**Fixed** means it must happen this way, in this order. **Flexible** means the AI may adapt it. Fixed describes the method, not who does it."
- *Not sure?* Leave it flexible. You can fix a step later.

For each step marked fixed, **Ask:** "Why must [step] happen that way: a regulation, a company policy, a check, or your judgment?"
- *Why:* Design keeps a regulation or policy step exactly as it is, even when the AI could do it another way.
- *Not sure?* Say your judgment.

The reason goes on the step line: `fixed (regulation)`, `fixed (policy)`, `fixed (check)` or `fixed (your judgment)`.

For each step a person does, **Ask:** "Is [step] a point where you review or approve the work before the next step?"
- *Why:* Review and approval points become human gates, and Test checks each one.
- *Not sure?* Say no; you can add a gate later.

A yes adds a Human Gates row at that step. This is where gates are asked about; Part 5 asks no new gate questions and adds a gate only from the taking-part and when-unsure answers.

## 4. Decisions

**Ask:** "Where does the work go a different way depending on what it finds?"
- *Why:* This tells Design whether the work follows your rules or needs judgment along the way.

For each one, **Ask:** "What decides which way it goes?"

Each Decision line records who settles it: `a rule on a value`, `your criteria`, or `open judgment`. When unclear, one follow-up:

**Ask:** "Could a fixed rule settle this, does it follow criteria you could write down, or does it take judgment each time?"
- *Why:* Design uses this to decide how much of the choice the AI makes.
- *Not sure?* Say judgment. You can tighten it later.

A threshold ("over $50k → controller") is a rule on a value, whoever supplies the value. When the AI reads the value (an amount from a scanned receipt), the Decision line adds `· value read by AI`; Test checks that reading separately.

## Regulated work

When the Part 2 answer was yes, right after the decisions question (and its follow-ups), each in its own message:

**Ask:** "Which steps does the regulation require?" Ask only about steps not already marked `fixed (regulation)`; with an AI-proposed path, about the proposed steps.
- *Not sure?* Name the ones you're sure of; the rest stay flexible.

Mark those steps `fixed (regulation)`.

**Ask:** "Which decisions must a person make or approve?" (Skip decisions already gated; never say so.)
- *Why:* Those become human gates, so the AI never makes them alone.

Each becomes a Human Gates row.

## 5. The range

**Ask:** "What will come in? Give me a typical case."
- *Why:* The typical and awkward cases become the scenarios Test runs; you paste them near the end.

Then, in its own message, **Ask:** "And an awkward one?"

When nothing comes in yet, **Ask:** "Where will the information come from?" Then, separately, **Ask:** "Does it exist yet?"

Draft the Inputs lines (`I1`…) from the Part 2 trigger and these answers, tagged *(my suggestion)*, for Part 5's second draft message. A source that doesn't exist yet is recorded in Inputs with `Status: not available yet`.

## 6. Expertise

**Ask:** "What would a capable beginner get wrong here that you wouldn't?"
- *Example:* a sommelier might say: "Pairing by grape instead of by the dish's sauce."

Answers about steps go on the step. Answers that are quality standards ("lead with a hypothesis") are held and offered as checks in Part 5's third draft message, tagged *(you said)*, skipping any standard a check already covers.

## Detail only where it matters

A step gets detail (the rule, the check or handoff, the expertise) only when it carries order that matters, a rule or standard, a check or handoff, an outside action, or the student's expertise. Everything else stays one line.

**Detail table.** When the regulation answer is yes, or four or more steps need detail (never say this threshold), show the detail in one table (step, rule, check or handoff) and ask "What's wrong or missing?", never one question per step. Each rule in it is tagged *(you said)* or *(my suggestion)* and needs a keep or drop; never state a rule or threshold as fact.

Otherwise, for each step that needs detail, in its own message, **Ask:** "Does [step] have a rule it must follow, or something that must be checked before the next step?"
- *Why:* Rules and checks are what the AI must get right every time, so they're written down for that step.
- *Not sure?* Say no. Test will show if it needs one.

## End of Part 4

Say: "Design uses this to decide how much the AI works out on its own."
