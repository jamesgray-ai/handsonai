# Running work brought in

Read when the workflow is running work Analyze recorded (state 0: an `in-production` node with no workflow folder) and the leader asked for it by name, said "change my workflow" here, or another step started Deconstruct on it. Section names in italics are SKILL.md's.

Running work Analyze recorded (an `in-production` node with no workflow folder) arrives by name ("run the deconstruct skill on [workflow]", or "change my workflow" said here, taken as the same request), or started directly by another step, whose skill call says "run the deconstruct skill on [workflow]" with the leader's own words after it. It needs a registry. However it arrived, its first question is N-D22 (step 3), even when the leader named a change (noted for the interview). Take it as a new workflow:
1. The opening, with the working folder as the location (only when it hasn't been said yet: when the leader named the work at the backlog choice or at cold entry, it has), then one line (model wording): this brings [workflow] into the framework, and the version that runs today keeps running as it is until Build installs the new one.
2. Prefill from the node, as for a backlog pick: the name, description, trigger and deliverable, and any other field it has; with its card in `framework/ai-opportunity-report.md`, the card's fields too (`references/choosing-a-workflow.md`, *Prefilled*).
3. In cold entry's place, and before N-D1, one of two forms of N-D22, word for word:
   - **Its Analyze card has a Status line** ("Already runs with [skill or agent], [home]"): **Ask:** "Your Analyze report says it runs with [skill or agent][, in [where]]. Tell me what happens in it, from what kicks it off to what comes out the other end, and whether it runs on a schedule. Rough is fine." Fill [where] only when the card names it; otherwise the bracketed clause is left out.
   - **Every other case** (a node Analyze didn't write, or a card with no Status line): **Ask:** "Tell me how it runs today: what kicks it off, what happens, what comes out the other end, and whether you do it by hand or it's set up somewhere (a skill, an agent, an automation), on a schedule or not. Rough is fine."

   Its answer is played back at Part 4's method question and becomes the Metadata's `Runs today` row, played back with Part 2.
4. The normal interview from N-D1 on, on either track. Nothing is skipped because the work already runs.
   - **When Analyze recorded it** (its card has a Status line): Part 1 takes the card form (`part-1-what-this-is-worth.md`), and Part 2 opens with N-D23 (`part-2-scope-and-a-name.md`; on the light track, item 0), so nothing Analyze recorded is asked again.
   - **Otherwise,** the N-D22 answer prefills Part 2's trigger and deliverable, confirmed with "Does that match?", and Part 2 runs as for cold entry.
5. The registry write keeps `status: in-production`.

A stop before the first progress save leaves it in state 0: the leader starts again the same way.
