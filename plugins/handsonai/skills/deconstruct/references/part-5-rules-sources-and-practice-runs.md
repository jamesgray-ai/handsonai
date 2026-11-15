# Part 5: Rules, sources and practice runs

Read when Part 5 starts, before its first message (SKILL.md also has you read the requirements template now, for what goes in each draft). On the light track, read it only for what that track borrows: live writes, taking part, the paste request, and *The inputs you wrote, shown before saving*. The light track keeps its own count of practice runs (two or three, the typical case required), so *A tricky one stays* and the order of proposed inputs don't apply there. Every quoted line is said exactly; each question is its own message. In a personal-life registry, the personal-life wording replaces the live-writes question when no step carries a `writes` tag.

Say first, after the signpost and the count line, in the same message: "Last part: I'll draft the rules it follows, where you check its work, the sources it uses and the cases we'll test it on. You correct each one."

**Saving within this part:** on a connection that updates files in place, save the progress file silently after each confirmed draft or playback, with `Next: Part 5 — Rules, sources and practice runs · after: [last confirmed question, in plain words]` (SKILL.md, *Pause and resume*).

**The policy question** (full track only), for a source first shown in this part: in the next message, right after the reply that showed it, before this part's next question; a source first shown in a draft's reply (the second draft) is asked about in the next message, before the privacy questions, never inside a draft. When a paste triggers both, the confidential check first. Its wording, its "no" question and what each answer records are in `part-2-scope-and-a-name.md`, *The policy question*, word for word. A removal step chosen here is a `When` rule in the first draft, never a new step.
- **When draft 1 is already confirmed** (a source first shown in the second draft's reply, or when a real input is pasted): when the next bullet applies, it comes first, and this line only once the removal stands. Play the `When` rule back in its own one-line message (model wording) with a keep or drop. Its Boundaries line joins the security limits; if those were already played back, or there's no security-limits message, it goes in that same one-line message.
- **If `Runs: without you` and the leader does the removal** (`· (you)`), the two answers conflict (`part-2-scope-and-a-name.md`, *On a `Runs: without you` workflow*): ask rule 10's line, word for word, in the order the leader gave the answers: "Earlier you said [first answer]. Now you've said [second answer]. Which one holds?" The removal kept: `Runs: with you`. `Runs: without you` kept: ask the "no" question again, word for word, so the leader picks another option.

## Contents

- Always asked, never drafted: live writes (with each write's place), taking part, when it's unsure
- The drafts, and the questions between them
- The practice runs: which inputs, in which order, and each one's expected result; the inputs you wrote, shown before saving
- The target, then the preview

## Always asked, never drafted

Each in its own message, before the drafts.

**1. Live writes.** When steps carry `writes` tags, a confirmation listing them in plain words:

**Ask:** "It writes to: [list]. Anything else?"

With no tags, say what's known and ask only the open part. When the leader sends it themselves (a step or rule they perform): **Ask:** "You send it yourself. Will the AI save the draft anywhere, such as in your email?" Otherwise: **Ask:** "Will it send or change anything itself, or only prepare drafts for you? Saving a draft in your email counts — tell me where."
- *Why:* Anything it changes outside this conversation is checked before it's built, and gets a limit that fits the risk.

The *Why* goes with whichever form is asked first. A saved draft is a write, recorded with its action (`save as a draft`). When the leader says it never sends, acknowledge that in one line and offer it as a prohibited action in the first draft. For a write named here for the first time, propose where it happens: "That's after step [N], once [x], right?", or with no steps, "That's after [moment], right?"; the Writes line names that step or moment.

**Each write's place** (no new question). In the confirmation's [list], name each write with its place, or say its place isn't known yet, in this form: "[action] in [system], in [place]; [action] to [system], [place] not known yet". Only the bracket is filled; the question's words stay as written. With no `writes` tags (the other forms), there's no list: a place the reply didn't give is shown as "[place] not known yet" in the next draft that names the write (the first draft, or the security limits). Never ask a separate question about a place. Recorded inside W's `[system]` field: `[system] [place, as the leader named it]`, or `[system] ([place] to confirm)` when it stays unknown.

**2. Taking part while it runs.** When a checkpoint, step or rule the leader performs already settles it, state it: "You review every [deliverable] before it's sent, so this runs with you." (naming what they do). Only [deliverable] is filled: "review" and "sent" stay as written, even when the leader posts or approves it. Only when nothing settles it:

**Ask:** "While it runs, do you want to take part, like reviewing a draft, answering its questions or approving something, or should it run from start to finish without you?"
- *Why:* If it runs without you, it can't stop to ask, so it needs clear rules for when it's unsure.

Record it at the top of Human Gates: `Runs: with you` or `Runs: without you`.
- "Without you" when the leader has named a review or approval point: **Ask:** "You said it should run without you, but you also want to approve [point]. Which one holds?" A checkpoint the leader performs that's still kept in the drafts after "without you" is asked about again; if they keep it, the line becomes `Runs: with you`.
- A checkpoint someone else performs (a controller) leaves `Runs:` as answered.
- A policy removal the leader does (`· (you)`), on `Runs: without you`: rule 10's line, as *The policy question* above says.
- An approval point in the answer that matches no checkpoint is added, *(you said)*; when its step is unclear, in its own message, **Ask:** "Which step does that come after?"

The send-back reason isn't asked again: the third draft plays the must-haves back, each marked "(must-have)", never Part 3's must-have line reworded.

**3. When it's unsure,** asked once, even when the leader said something like it earlier (an answer about one case isn't the rule for every case):

**Ask:** "When it hits a case it can't confidently handle — for example, [the leader's tricky case] — should it stop and ask you, or do its best and flag it?"
- *Why:* This becomes a rule the workflow follows every time a case doesn't fit.
- *Not sure?* Do its best and flag it. You can change it after testing.

Add "or skip that item" only when one run handles several items (`Per run: a batch of [cases]`, Part 2): **Ask:** "When it hits a case it can't confidently handle — for example, [the leader's tricky case] — should it stop and ask you, do its best and flag it, or skip that item?" When it runs without the leader, leave "stop and ask you" out of the choices (with a batch: **Ask:** "When it hits a case it can't confidently handle — for example, [the leader's tricky case] — should it do its best and flag it, or skip that item?"); when that leaves one choice, say instead: "Since it runs without you, when it isn't sure it'll do its best and flag it for you." Recorded as the Fallback rule. "Stop and ask you" also adds a checkpoint. Where a flag goes is part of the rule: never inside the deliverable unless it's unmistakable and removed before sending; when only the leader reads the deliverable, stating plainly what wasn't found ("No recent news found") is content. What it can't confidently handle, and where an unattended run's flags go, are drafted in the first draft, never asked (*The drafts*).

## The drafts, and the questions between them

Four short messages, and a fifth, the security limits, when a sensitivity test trips; what goes in each is in the requirements template. Never say how many drafts are coming. A draft holds no question of its own besides its ending; a gap stays in the draft as a suggestion or an unknown for the leader to correct. Every line is tagged, and each suggestion needs an explicit keep or drop (the rubber-stamp guard). Each requirement lives in one place: behaviours in the first draft, qualities of the output in the third.

1. **The rules**, ending "What would you change or add?" Besides the rules already given, it drafts, each tagged *(my suggestion)* for a keep or drop (details in the requirements template, draft 1):
   - **the conditions it can't confidently handle,** taken from the tricky case and the out-of-bounds rule, in the Fallback;
   - **where flags go, when `Runs: without you`:** "…it does its best and flags it in [an email / a chat message] to you", an email by default, a chat message only when the leader has named the chat tool they use (named as they named it). Dropped, the flag stays in the end-of-run message;
   - **an alternative output** for an out-of-bounds case, as a `When` rule;
   - **a policy removal chosen after Part 4's playback** (or with no steps), as a `When` rule with its role tag;
   - **a write's place not known yet,** shown as "[place] not known yet" where no list named it.
2. **Checkpoints, sources and inputs**, ending "What would you change or add?" The sources are introduced the first time in these words, word for word: "These are the sources it uses, what we call its **context**: any information a step needs to do its job, such as documents, spreadsheets, emails, style guides, or knowledge that lives in someone's head."

   **The privacy questions** follow straight after: one per source the AI can't reach that trips a test (any `Confidential` or `Regulated` row, any `External` source), each in its own message:

   **Ask:** "When this runs, can the workflow reach [source] itself, for example through a connection to [tool], or will you paste it in each time?"
   - *Why:* If it can't reach it, it has to ask you for it on every run.
   - *Not sure?* Say you'll paste it. You can connect it later.

   With a plural [source]: **Ask:** "When this runs, can the workflow reach [source] itself, for example through a connection to [tool], or will you paste them in each time?"
   - *Not sure?* Say you'll paste them. You can connect them later.

   The answer sets the source's `AI Accessible`, and its Inputs line follows it ("from C1, through the [storage service] connection"). When a write's system needs a connection, say once, after the access questions: "Saving drafts in [system] also needs a connection; we'll set that up when it's built." (naming what it writes). A write trips only the Prohibited actions and Traceability categories, never this question, which is about sources.

   A row saved as `Regulated` when the law answer was no or not sure: say you marked [source] as regulated, then **Ask:** "Which one? A name or a description is fine." once; if it stays unknown, `Governing regime: Not sure — to check`. This doesn't switch on the detail table.

   **The security limits,** only when a sensitivity test trips: their own short message after the privacy questions, unnumbered, so the third and fourth drafts keep their numbers. Ends "What would you change or add?"

   **Then the standing-rules question,** when it applies, and on both tracks only from the leader's second workflow (the requirements template, *Standing rules*).
3. **What every [deliverable] must get right**, ending "What would you change or add?"
4. **The practice runs** (below).

## The practice runs

Three to five in total. **Which inputs, in this order, stopping at five in all:**
- **Real inputs first,** ahead of any proposed one: the input behind the Golden Example is E1; the typical case from Part 4 is `(real)`; the tricky case is `(real, hard)`; and any other real input the leader named.
- **Then proposed inputs,** marked `(proposed)` (or `(proposed, hard)` for the hard case), each aimed at one risk, skipping any a real input already covers, in this order:
  1. the typical case, when the leader gave no real one;
  2. the tricky case, when the leader gave none;
  3. one input aimed at an "It never…" rule or a checkpoint (one such input, not one per rule);
  4. out of bounds, when an "out" rule exists;
  5. carry-over, when Part 4 recorded `Remembers: [what]`: [a case] an earlier run already handled;
  6. a decision branch, when a decision exists.
- **Never proposed here:** an empty or malformed input, or an input carrying an instruction aimed at the AI. Test writes those. Propose only inputs the leader could actually get hold of.

Open with "Here are the practice runs we'll test it on.", word for word on both tracks ("we'll", never "I'd" or "I'll": the leader confirms these runs too), play each back in plain words (never the `(real)` or `hard` tags, never a line's label), and end with N-D11's full form, word for word: "Change, replace or drop any; keep three to five, including your typical and tricky [cases]. When we test it, each of these is run and checked against your requirements." Each playback says what the input is and **what should happen with it, in plain words**: the leader is confirming the result it will be checked against. For illustration only (use the leader's own case and rule): "this one checks it never contacts someone it has already contacted" for a rule; "this one checks that [the case, in the leader's words] [the branch's path, in the leader's words]" for a decision branch.

**Each input's expected result** (no new question): every input saved here gets an `expect:` line from the playback the leader confirmed, in the form "[what it produces or does]; [what it doesn't do]".
- **For an input aimed at a decision, an out-of-bounds rule or carry-over,** the expected result is taken from that line's own wording (the decision's path; the `When` rule's "does what instead"; the `Remembers` row), and the playback says that same thing in plain words, so the leader confirms what will be checked. Never a different expectation for these.
- "What to look for in the output" in Example Scenarios is the `expect:` line, word for word.
- **A carry-over input** opens its body with one paragraph, `Earlier run: [what an earlier run left behind, in plain words: the cases it handled, the last deliverable]`, then a blank line, then the input itself (the requirements template, *inputs/*). Playback says it in plain words ("as if an earlier run already handled [case]").

Then:
- **A tricky one stays.** If fewer than three remain after their changes, or no hard case, propose replacements and have each one kept before going on. The input aimed at a rule or checkpoint doesn't count as the hard case.
- **No reference question per row.** The Golden Example, when there is one, is the only reference.
- **The real inputs, pasted now.** For a real input named but not pasted ("last Friday's tracker export"): **Ask:** "Paste a set of [inputs], or say 'draft one' and I'll write a made-up example from your description for you to check." On print-to-save, say instead: "paste it in and I'll include it in the files you save, so testing is copy-and-paste rather than a hunt". A made-up example is shown in full and checked: **Ask:** "Does this look like your real [inputs]?" It never states what the workflow must work out (no "Buying for:" line, no flag it should raise), and a made-up example of the leader's own typical or tricky case stays `(real)`. A password or key inside a pasted input is replaced with a placeholder before saving, and N-F14 is said (SKILL.md). The confidential check runs before saving. Only when they genuinely can't get hold of it today, the file holds one placeholder line naming exactly what to paste in before testing, and say so.
- **The inputs you wrote, shown before saving** (both tracks). When any kept run is a proposed one (`(proposed)` or `(proposed, hard)`, a carry-over input and a kept replacement included), then once the leader has confirmed the practice runs (the reply to N-D11's message, and any re-ask) and the real inputs above are in, show every input you wrote, in full, in one message of its own, with N-D25 said word for word in two parts around them, so the message ends on its question:

  > Here are the practice inputs I wrote. [Every input I wrote, in full, each under a plain label naming its run.] Does each look like what you'd really get?

  That is: its first sentence opens the message; then each input under a short label in plain words naming its run (never `(proposed)`, `hard`, an E number or a line's label), the input itself as a block quote: exactly the text you'll save; then its second sentence, alone, as the message's last line. Nothing follows it.
  - A carry-over input's set-up is shown too, in plain words, in its label ("as if an earlier run already handled [case]"), never as its `Earlier run:` line. The header lines (`source:`, `tests:`, `expect:`) are never shown.
  - Not shown again: real inputs, and a made-up example from "draft one", already shown and checked with "Does this look like your real [inputs]?". Inputs the leader pasted are saved as given, as above.
  - The leader's corrections are taken as given, and the corrected text is what's saved; a yes keeps them as shown. Nothing you wrote reaches `inputs/` unseen. Then the confidential check, where it applies.
- **Numbered and saved** as the requirements template says (*inputs/ and context/*).

## The target, then the preview

Each in its own message. When the leader stated an aim in Part 1, in their own words (never one only the Analyze report or the card stated: `part-1-what-this-is-worth.md`, *An aim*): **Ask:** "In Part 1 you said [aim]. Is that the target, and what about [the other kept measure]?" (with one kept measure, without ", and what about [the other kept measure]"). With no aim, one per kept measure:

**Ask:** "What should [measure] be once this is running?"
- *Why:* It's what you'll judge the workflow against when you re-check it.
- *Example:* a bookkeeper might say: "Month-end close in two days instead of five."

The *Why* and *Example* go with whichever form is asked first.

**Then the preview,** always, in its own message, right after the target and before anything is written; never skipped, even when the interview ran long. Its words are in the requirements template's *The preview*, already read.
