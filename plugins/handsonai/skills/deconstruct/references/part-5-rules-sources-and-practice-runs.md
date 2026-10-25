# Part 5: Rules, sources and practice runs

Read when Part 5 starts, right after its signpost (SKILL.md also has you read the requirements template now, for what goes in each draft). On the light track, read it only for what that track borrows: live writes, taking part, and the paste request. The light track keeps its own count of practice runs (two or three, the typical case required), so *A tricky one stays* and the reference question don't apply there. Every quoted line is said exactly; each question is its own message. In a personal-life registry, the personal-life wording replaces the live-writes question when no step carries a `writes` tag.

Say first: "Last part: I'll draft the rules it follows, where you check its work, the sources it uses and the cases we'll test it on. You correct each one."

## Contents

- Always asked, never drafted: live writes, taking part, when it's unsure
- The drafts, and the questions between them
- The practice runs
- The target, then the preview

## Always asked, never drafted

Each in its own message, before the drafts.

**1. Live writes.** When steps carry `writes` tags, a confirmation listing them in plain words:

**Ask:** "It writes to: [list]. Anything else?"

With no tags, say what's known and ask only the open part. When the leader sends it themselves (a step or rule they perform): **Ask:** "You send it yourself. Will the AI save the draft anywhere, such as in your email?" Otherwise: **Ask:** "Will it send or change anything itself, or only prepare drafts for you? Saving a draft in your email counts — tell me where."
- *Why:* Anything it changes outside this conversation is checked before it's built, and gets a limit that fits the risk.

The *Why* goes with whichever form is asked first. A saved draft is a write, recorded with its action (`save as a draft`). When the leader says it never sends, acknowledge that in one line and offer it as a prohibited action in the first draft. For a write named here for the first time, propose where it happens: "That's after step [N], once [x], right?", or with no steps, "That's after [moment], right?"; the Writes line names that step or moment.

**2. Taking part while it runs.** When a checkpoint, step or rule the leader performs already settles it, state it: "You review every [deliverable] before it's sent, so this runs with you." (naming what they do). Only when nothing settles it:

**Ask:** "While it runs, do you want to take part, like reviewing a draft, answering its questions or approving something, or should it run from start to finish without you?"
- *Why:* If it runs without you, it can't stop to ask, so it needs clear rules for when it's unsure.

Record it at the top of Human Gates: `Runs: with you` or `Runs: without you`.
- "Without you" when the leader has named a review or approval point: **Ask:** "You said it should run without you, but you also want to approve [point]. Which one holds?" A checkpoint the leader performs that's still kept in the drafts after "without you" is asked about again; if they keep it, the line becomes `Runs: with you`.
- A checkpoint someone else performs (a controller) leaves `Runs:` as answered.
- An approval point in the answer that matches no checkpoint is added, *(you said)*; when its step is unclear, in its own message, **Ask:** "Which step does that come after?"

The send-back reason isn't asked again: the third draft plays the must-haves back.

**3. When it's unsure,** asked once, even when the leader said something like it earlier (an answer about one case isn't the rule for every case):

**Ask:** "When it hits a case it can't confidently handle — for example, [the leader's tricky case] — should it stop and ask you, or do its best and flag it?"
- *Why:* This becomes a rule the workflow follows every time a case doesn't fit.
- *Not sure?* Do its best and flag it. You can change it after testing.

Add "or skip that item" only when one run handles several items (a batch of emails, a list of leads). When it runs without the leader, leave "stop and ask you" out of the choices; when that leaves one choice, say instead: "Since it runs without you, when it isn't sure it'll do its best and flag it for you." Recorded as the Fallback rule. "Stop and ask you" also adds a checkpoint. Where a flag goes is part of the rule: never inside the deliverable unless it's unmistakable and removed before sending; when only the leader reads the deliverable, stating plainly what wasn't found ("No recent news found") is content.

## The drafts, and the questions between them

Four short messages, and a fifth, the security limits, when a sensitivity test trips; what goes in each is in the requirements template. Never say how many drafts are coming. A draft holds no question of its own besides its ending; a gap stays in the draft as a suggestion or an unknown for the leader to correct. Every line is tagged, and each suggestion needs an explicit keep or drop (the rubber-stamp guard). Each requirement lives in one place: behaviours in the first draft, qualities of the output in the third.

1. **The rules**, ending "What would you change or add?"
2. **Checkpoints, sources and inputs**, ending "What would you change or add?"

   **The privacy questions** follow straight after: one per source the AI can't reach that trips a test (any `Confidential` or `Regulated` row, any `External` source), each in its own message:

   **Ask:** "When this runs, can the workflow reach [source] itself, for example through a connection to [tool], or will you paste it in each time?"
   - *Why:* If it can't reach it, it has to ask you for it on every run.
   - *Not sure?* Say you'll paste it. You can connect it later.

   The answer sets the source's `AI Accessible`, and its Inputs line follows it ("from C1, through the Google Drive connection"). When a write's system needs a connection, say once, after the access questions: "Saving drafts in [system] also needs a connection; we'll set that up when it's built." (naming what it writes). A write trips only the Prohibited actions and Traceability categories, never this question, which is about sources.

   A row saved as `Regulated` when the law answer was no or not sure: say you marked [source] as regulated, then **Ask:** "Which one? A name or a description is fine." once; if it stays unknown, `Governing regime: Not sure — to check`. This doesn't switch on the detail table.

   **The security limits,** only when a sensitivity test trips: their own short message after the privacy questions, unnumbered, so the third and fourth drafts keep their numbers. Ends "What would you change or add?"

   **Then the standing-rules question,** when it applies (the requirements template, *Standing rules*).
3. **What every [deliverable] must get right**, ending "What would you change or add?"
4. **The practice runs** (below).

## The practice runs

Three to five in total, built as the requirements template says. Open with "Here are the practice runs we'll test it on.", play each back in plain words (never the `(real)` or `hard` tags, never a line's label: "this one checks it never contacts someone we've already emailed"), and end with N-D11's full form (SKILL.md), word for word.

Then:
- **A tricky one stays.** If fewer than three remain after their changes, or no hard case, propose replacements and have each one kept before going on. The input aimed at a rule or checkpoint doesn't count as the hard case.
- **A reference for each real row,** skipped when Part 3 recorded no reference example. Otherwise, for each `(real)` row without one, in its own message, **Ask:** "Have you sent a [deliverable] after a [case] like this that you'd want every one to match?", with [case] naming that row's case in the leader's words ("the Heron program"), so no two asks read the same; only [deliverable] and [case] change, and every other word, "like this that you'd want" included, is said as written. Record its Context Inventory ID, a short excerpt, or "—". A `(proposed)` row has "—"; a reference you wrote is never recorded.
- **The real inputs, pasted now.** For a real input named but not pasted ("last Friday's tracker export"): **Ask:** "Paste a set of [inputs], or say 'draft one' and I'll write a made-up example from your description for you to check." On print-to-save, say instead: "paste it in and I'll include it in the files you save, so testing is copy-and-paste rather than a hunt". A made-up example is shown in full and checked: **Ask:** "Does this look like your real [inputs]?" It never states what the workflow must work out (no "Buying for:" line, no flag it should raise), and a made-up example of the leader's own typical or tricky case stays `(real)`. A password or key inside a pasted input is replaced with a placeholder before saving, and N-F14 is said (SKILL.md). The confidential check runs before saving. Only when they genuinely can't get hold of it today, the file holds one placeholder line naming exactly what to paste in before testing, and say so.
- **Numbered and saved** as the requirements template says (*inputs/ and context/*).

## The target, then the preview

Each in its own message. When the leader stated an aim in Part 1: **Ask:** "In Part 1 you said [aim]. Is that the target, and what about [the other kept measure]?" (with one kept measure, without ", and what about [the other kept measure]"). With no aim, one per kept measure:

**Ask:** "What should [measure] be once this is running?"
- *Why:* It's what you'll judge the workflow against when you re-check it.
- *Example:* a bookkeeper might say: "Month-end close in two days instead of five."

The *Why* and *Example* go with whichever form is asked first.

**Then the preview,** always, in its own message, right after the target and before anything is written; never skipped, even when the interview ran long. Its words are in the requirements template's *The preview*, already read.
