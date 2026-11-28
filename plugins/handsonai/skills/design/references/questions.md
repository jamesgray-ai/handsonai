# Part 3's questions

Read before the first question of Part 3, whenever a change in the review or an update creates one of these questions, and before any requirement write. Section names in italics are SKILL.md's.

Each question is its own message even when several are alike: one N-14 per write the connection can't make, never one for all of them. **The cap:** at most five (three on the light track), follow-on questions included. Safety questions (D5, D5″, N-14, N-32, a missing safety answer, `SKILL.md` step 4) are never cut and fill the cap first; when they alone reach it, ask every one and nothing else. Order among them: a missing safety answer first (`SKILL.md` step 4: the security limits drafted, or the Fallback proposed, with N-L2 straight before it where `light-track.md` says), then the checkpoint question (D5, D5″), judged on the plan as drafted, before another answer changes `Runs:`; then N-14; then N-32 (a write it adds brings its own limits straight after the yes). On an update or a change in the review, which have no Part 3, the same order holds among the update's own questions, before anything else is asked. Over the cap, nothing is guessed silently: D4′ and D7 take their safe defaults; reuse takes the recommended option; a constraint the plan can't meet stays an open item blocking its tasks; a fact question takes your recommended answer, shown in the review as an assumption, or becomes an open item where no answer can responsibly be assumed (a write's target, an input that doesn't exist yet). Say each held line (D5, D5″, N-14, N-32, D4′, D7, N-16, and N-13's "Adding to it also changes [other workflows].") whole and word for word, its options inside it as written (only the brackets filled): never split one of its sentences in two or its question into separate questions, and "I recommend [option], because [reason]." stays one sentence. The fact question (N-11) and the reuse question (N-13) are models *(your words)*: say what they say, in that order, in your own plain words, its options all offered. Then its *Why* and *Not sure?* (each marked *(your words)* is a model too). Where the platform has a structured-question tool, the options go through it; otherwise the message ends with them repeated as a bare numbered list, each option copied from the line as said, nothing added, so it ends on the choice (every option the line offered, never fewer than two). After each answer, check the plan again and add any question it creates, within the cap. After the last, run the self-check and the plan check again.

**A fact only the leader knows** (something left open or "to check" that changes the design, a place recorded `([place] to confirm)` included; one that doesn't is an open item with no question; never a fact the requirements record: a write's place, how runs start, where flags go, what it remembers):

**Ask:** "Your requirements leave [what] open, and it changes how I build [part]. [Question in plain words]?" *(your words)*
- *Why:* [what it changes]. Where the leader could over-answer, say how much detail is needed.
- *Not sure?* Say not sure; I'll note it, and only [the part] waits for it. *(your words)*

**Reuse:**

**Ask:** "You already have [skill], which you use for [workflow or purpose]. It covers [part]. Use it as it is, add to it, or build a new one for this?" *(your words)* When adding to it changes other workflows, add "Adding to it also changes [other workflows]." Then "I recommend [option], because [reason]." (N-13, *your words*)
- *Why:* Reusing what you have keeps one version to look after. *(your words)*
- On the answer, the part's blueprint gets `Uses skills from: [plugin] ([skill])` when the skill lives in another plugin (`plan-template.md`, *Component Blueprints*), saved with the answer.
- *Not sure?* Say not sure; I'll [the recommended option], and you can change it later. *(your words)*

**A write the connection can't make:**

**Ask:** "Your requirements say it should [the write], but the [system] connection can't do that. You can [make that change yourself | have [the named role] make that change], [use another connection — only where one exists], [use a workaround in code — only where allowed], or [leave it out — only where no limit requires it]. I recommend [option], because [reason]." (N-14; the bracketed conditions are for you, not said.) When there's no connection to [system] at all, **Ask:** "Your requirements say it should [the write], but there's no connection to [system]. You can [make that change yourself | have [the named role] make that change], [use a workaround in code — only where allowed], or [leave it out — only where no limit requires it]. I recommend [option], because [reason]." (N-14, no connection)
- *Why:* If the plan counts on a change the connection can't make, the workflow would fail at that point. *(your words)*

A person's change becomes a Human step; when that person is the leader and the requirements say `Runs: without you`, `Runs:` becomes `with you` (N-15).

**A delivery that needs a write,** when the leader asks for the output to reach them in a way only a write makes ("save it as a Gmail draft"), or the requirements' Output names such a delivery (a draft in [system], a file in [place]) that no line in `### Writes` makes. Never added by the plan alone, and never offered when nothing asks for it: an Output that only says "email", with no write, is shown in the chat. Asked once, where it arises: in Part 3, a safety question after N-14; in the review or an update, first among its own questions:

**Ask:** "Delivering it as [the delivery, in plain words] means the workflow would also [the write, in plain words], and your requirements don't include that yet. Should I add it to your requirements, or keep it shown in the chat for you to copy?" (N-32)

On a yes, in this order: the track check (`light-track.md`; N-L2 only when the write is a sign of risk and a safety answer follows); the write as the next `W` line under `### Writes` (`requirement-lines.md`; a `None` line there goes); its security limits by `SKILL.md` step 4 (a), straight after the yes, drafted in one message, each kept or dropped, for each category it trips that has no table; then one N-15 for the whole change, `revision` raised once (*Requirement writes*, below). The plan's `Delivered as:` then names it, and the plan check runs again (N-14 if the connection can't make it). On "keep it in the chat", or without a yes: `Delivered as:` is shown in the chat, and the requirements don't change.

**The checkpoint question,** when the plan changes something with no checkpoint before it: running without the leader, as below; running with them, its own form (*With the leader*, below). Without the leader: for an Autonomous plan, any change in a live system; below Autonomous, a change that can't be undone. Drafts are exempt at every level; undoable changes below Autonomous; and so is a flag sent only to the leader (the flag `W` line, `· send a flag · after each run`, kept in the rules draft): never asked about, it's a consequential point instead. Asked once, and again only when a change in the review newly creates it. Autonomous, said as approved:

**Ask:** "This workflow works out its own path, runs without you, and changes something live: [the writes, in plain words]. No one sees a change before it's made, so a mistake goes straight into [system]. Should I add a point where someone reviews or approves [the change] first, or do you accept that risk?"

Below Autonomous:

**Ask:** "This workflow runs without you and makes a change that can't be undone: [the change, in plain words]. No one sees it before it's made, so a mistake goes straight into [system]. Should I add a point where someone reviews or approves it first, or do you accept that risk?"

With several changes that can't be undone, **Ask:** "This workflow runs without you and makes changes that can't be undone: [the changes, in plain words]. No one sees them before they're made, so a mistake goes straight into [system]. Should I add a point where someone reviews or approves them first, or do you accept that risk?"

**With the leader,** when the plan runs with them and makes a change that can't be undone (a send included) with nothing stopping for them to see it first: drafts and undoable changes stay exempt, and a checkpoint the leader already performs settles it. Asked once, like the forms above:

**Ask:** "This workflow makes a change that can't be undone while you run it: [the change, in plain words]. Nothing stops for you to see it first, so a mistake goes straight into [system]. Should I add a point where you review or approve it first, or do you accept that risk?" (D5″, with you)

**An unchecked regime** on an Autonomous plan:

**Ask:** "I've planned it to [the planned level, in plain words]. Whether a law or regulation governs this work is still marked for you to check. Should it stay that way before that's checked, or should I keep it to [the next level down, in plain words] until it is? I recommend keeping it to [that] until it's checked." (D4′)
- *Why:* Rules can require steps it mustn't skip. *(your words)*

**A choice against a limit,** when any answer breaks a rule, checkpoint, fixed step or `Runs:` that was the leader's to set:

**Ask:** "You asked for [the choice, in plain words], but your requirements say [the limit, in plain words]. Which one holds?" (D7)

D7 is always asked first, in its own message, even when the leader's request already sounds settled: a rule is loosened only on their answer to it. Any question that follows from the answer (a check whose only source was that rule: keep it or drop it) comes after, never in its place.

A `fixed (regulation)` or `fixed (policy)` step, or a rule or checkpoint that names a law as its reason ("…, as [the law] requires."), isn't the leader's to change: say in one line that the rules (or the policy) require it, so it stays, and move on.

**A constraint the plan can't meet:**

**Ask:** "Your requirements say [constraint], and this plan can't fully meet it because [reason]. Do you want to [option that meets it], or accept it as it is, with someone named who owns that risk? I recommend [option], because [reason]." (N-16)
- *Why:* Every limit you set gets a decision, so none is quietly dropped. *(your words)*

**When the leader can't answer:** a fact question becomes an open item (only the tasks it blocks wait); reuse takes the recommended option; a safety choice is never left pending and takes its safe default, recorded and shown at approval:

| Unanswered | Safe default |
|---|---|
| D5, D5″ | A checkpoint before the change, added to the requirements as the next G line (N-15), performed by the leader unless the requirements name another role. When the leader performs it, `Runs:` becomes `with you`; a checkpoint another role performs keeps `Runs: without you`. Either way involvement becomes Augmented, the new G line binds every artifact, and the mechanism is checked again |
| D4′ | The next level down, with the regime left `Open` |
| N-14 | A person makes the change |
| N-16 | None you may choose: an `Open` constraint, an open item blocking the tasks it touches |
| D7 | The limit in the requirements holds |

**Requirement writes.** Where an answer changes a requirement line (a limit the leader changed, a safe-default checkpoint, the `Runs:` line, a missing safety answer, `SKILL.md` step 4, a write added on N-32's yes), write it in the leader's words in the "When… it…" shape, in the formats in `references/requirement-lines.md` (read it before the first requirement write: the table's columns, the `Kind` values, the `Runs:` line and P rows, and that a check never takes a `(must)` marker (a 10.x file's `(must)` marks nothing); a new line takes the next number in its series, and a removed line's number is never reused); raise `revision`; log it in `revisions` (`by: design`, the line IDs), written in block form, never as `{ … }`:

```yaml
revisions:
  - revision: 3
    by: design
    lines: [G2]
```

A line removed (D7's or N-14's "leave it out", an open item's way out) also comes out of every `tests:` header in `inputs/` that names it and, on an 11.0 file, an R line out of every check's `· from:` that names it (`requirement-lines.md`); a check that named only that rule is never converted on your own: ask the leader once whether to keep it (its source then `the output alone`, said to them) or drop it *(your words)*; it is asked even over the cap, and a leader who can't say keeps it (the stricter choice), its source `the output alone`, shown in the review as an assumption; an input left testing nothing moves to `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its Example Scenarios row, if it has one, is removed in the same write, its E ID in the entry's `lines` (the table's last row stays: give its `tests:` the lines the input still exercises, by your reading). Then, where code can run, run `node [plugin root]/tools/requirements-check.js [workflow folder]` (never mentioned to the leader) and fix any problem it names before going on (exit 1); where it can't run, isn't there, or exits with anything but 0 or 1, check what you wrote by hand (`requirement-lines.md`, *Checking by hand*). Say (N-15): "I've updated your Workflow Requirements to match: [the change]." *(your words)*

**An open item** the leader says "not sure" to is noted in one line (model wording): that it's noted, which parts wait, and that the rest goes ahead.
