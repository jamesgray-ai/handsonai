# Knowledge Graph Interview Guide

Phases 0–5 plus the Close, about 30 minutes. Timeboxes are budgets, not targets. If a phase overruns, write what you have, say what is missing, and move on. Missing pages are homework; invented ones are never a fallback.

Two words you will use constantly, and how to explain them if asked: a **type** is a kind of thing (Client, Playbook); a **concept** is one real one (Acme, the kickoff checklist). Say "kind of thing" and "the real ones" until the user starts using the words themselves.

---

## Phase 0 — Home and boundaries (2 min)

**Say first:** "I'm working in `<full path>`. Is this the project folder for your knowledge graph? It's the folder that will hold your rules file, your skills, a `raw/` folder for documents, and the `knowledge/` folder where the graph itself goes."

**Then state the platform:** "You're on <Claude Code | Cowork | the ChatGPT app's Codex view | Cursor | Gemini CLI | …>, so your rules file will be `<CLAUDE.md | AGENTS.md>` and your skills will live in `<.claude/skills/ | .agents/skills/>`." On Cursor or Gemini CLI, the rules file is `AGENTS.md` (both tools read it; Gemini CLI also reads `GEMINI.md`, but `AGENTS.md` is the portable choice) and the skills folder is `.agents/skills/`.

**Mode check (do not ask, detect):** can you create a file in this folder? If not: "This build needs a tool that can write files on your computer: Claude Code, Cowork, or the ChatGPT desktop app's Codex view. A browser chat window can't do it. Open your folder in one of those and say *build my knowledge graph* again." Then stop.

**Report what is already here**, one line each, only for things that exist:
- `registry/`: "You have an AI registry here. It stays untouched; it records what you build with AI. This build models the work itself and goes in `knowledge/` beside it."
- `knowledge/SCHEMA.md`: "You already have a knowledge graph. I'll read its rulebook and fill gaps rather than rebuild." → gap-filling mode.
- `types.md` without `knowledge/`: "You have an approved type list from an earlier session but no graph yet. Want to revise the list first, or go straight to the build step? (When you're ready to build, send the single word **build**.)" → resume mode.

**Actor id:** "One housekeeping question: when you confirm a page is right, I'll record that as verified by you. What name should I record? Your first name is fine." Form the id yourself as `human:<lowercase-slug>` (Pat → `human:pat`); never ask the user to type that form.

**Example to show:** none; this phase is about the user's environment.

**What to write:** nothing.

---

## Phase 1 — Look around first (3 min)

**Say first (the roadmap):** "Here is how the next half hour goes. I need to learn what your work runs on: the clients, offerings, processes, tools, and policies you make decisions about every week. There are two ways I can learn that: I can read what you already have, and I can ask you. Reading first is worth it: a proposal or a process doc names the real things in your business better than anyone can from memory, and it gives every page I write a source to point back to. So I look around first, then ask about what I could not find, then propose the kinds of things your work runs on and how they connect. The only thing I create before you approve anything is a `raw/` folder for your documents; I build nothing else until you send the word **build**."

**Then the sixty-second explainer, about their business:** "Here's the whole idea in a minute. Your business runs on a few kinds of things, and real ones of each. Clients is a kind; Acme is a real one. Offerings is a kind; the AI roadmap you sell is a real one. Processes is a kind; your onboarding checklist is a real one. You already name the real ones every week. We'll list those first, because they're easy to name, then work out which kinds they belong to. Then we'll connect the kinds using sentences you already say, like 'Acme is on the pilot' or 'the onboarding checklist runs at every kickoff.' That's the graph: your business written down as the things it runs on and how they connect, so I can answer questions about it from your own pages. You describe your work; I'll do the sorting." (Swap the examples for the user's own words as soon as you have them.)

**Then the privacy line:** "One rule before I read anything: nothing with personal data about identifiable people goes into the graph. No payroll, no health records, no individual HR files, whichever way it would arrive."

**Then create `raw/`** at the project root and say: "I've made a `raw/` folder at the top of your project. That's where your source documents go. I'll read them; I'll never change them."

**Then scan** the project folder: README files, SOPs, process guides, proposals, requirements files from earlier framework steps, transcripts, the names of spreadsheets. Skip `registry/`; it is about AI builds, not the work.

**Opening question:** "Do you have two or three documents that describe your work — a proposal, a client summary, a process doc, a team charter? Tell me where they are, drop them into the `raw/` folder I just made, or say skip and I'll learn it all from the interview."

**Follow-ups:**
- If your platform has connectors, saved memory, or another folder in the session: "I can also look at <your Drive | your email | what I remember from earlier conversations | the other folder open in this session> for the names of clients, projects, offerings, and processes. Want me to?" Describe what you would look for, not which files; never look without a yes.
- If the user drops files in `raw/`: read them now.

**Report, in plain words**, in this shape:
> "Here's what I can see so far. The work looks like <one sentence>. Named things I found: <list, each with where it came from: 'Acme (proposal-2026.pdf)'>. I didn't find anything about <gaps>. Correct me on any of it."

If nothing was found: "I couldn't find anything about your work in this folder yet, so I'll ask." Never present a guess as something you read.

**Example to show:** none.

**What to write:** the `raw/` folder only.

---

## Phase 2 — Interview, concrete first (7 min)

One question at a time. Before each, check whether Phase 1 already answered it; if so, say "I think I already know this one from <source>: <answer>. Right?" and move on when confirmed. If Phase 1 answered only part of a question, say what you already know and ask only for what is missing, then confirm the combined answer.

**0. The explainer was already given in Phase 1.** Do not repeat it. If the user seems lost, restate it in one sentence: "kinds of things, and real ones of each; we find the real ones first."

**1. Scope.** "Are we mapping the work *you* do, your *team's* work, or the *whole company's*? Pick the one you actually make decisions about day to day." Record the answer; Phase 5 writes it on `overview.md`.

**2. Named things.** "What are the five to ten most important named things in that work? Clients, products, projects, tools, policies, teams, whatever they are. Real names, not categories." If they jotted a list before the lesson, take it.

**3. Who and what.** "Who do you do this work for, and what do you deliver to them?" Accept any answer: customers, patients, members, students, internal stakeholders, the board. Use the user's word for them from now on.

**4. What repeats.** "Walk me through a typical week or month. What work comes back around?"

**5. What you look up.** "When you're making a decision, what do you wish you could look up instead of asking someone or digging through files?"

**Probe list** (use it to check for gaps after the five questions; never propose types from it): the people or organizations you serve · the things you deliver · the work that repeats · the tools and systems you rely on · the rules and policies you work under · the assets or places you manage · the projects, cases, or engagements you run. If a family clearly matters to this user and nothing was said about it, ask one question about it. If it does not apply, leave it alone.

**Example type lists, shown as illustrations only.** Show at most one, the closest to the user's role, and only if they ask what a finished list looks like. Never copy one into `types.md`.

| Role | Types that came out of the interview |
|---|---|
| Fractional CFO | Client, Engagement, Deliverable, Playbook, Tool |
| HR lead inside a company | Policy, Role, Team, Process, System |
| Product manager | Product, Feature, Customer Segment, Release, Decision |
| Clinic operations lead | Service, Provider, Protocol, Supplier, Location |
| Nonprofit director | Program, Funder, Partner, Campaign, Policy |
| E-commerce operator | Product, Supplier, Channel, Campaign, Standard Operating Procedure |

**Stalled-interview fallback** (only if the user cannot get started after five minutes): "Let's start from four kinds that fit almost any work and correct them: **Offerings** (what you deliver), **People you serve** (use your own word: clients, patients, members), **Processes** (the work that repeats), and **Notes** (what you've learned that doesn't belong anywhere else yet). Which of these are wrong for you, and what's missing?"

**What to write:** nothing.

---

## Phase 3 — Propose and iterate (8 min)

### Types round (5 min)

**Propose** 4–7 types in this shape, one block per type, with three real named examples (two if that is genuinely all there are — see the pushback line below):
> **Client** — an organization you do paid work for. Real ones you mentioned: Acme Manufacturing, Bowman Foods, Reston Health.

Always include:
> **Note** — anything you learn that doesn't belong to one of the others yet, and answers worth keeping. Starts empty; that's expected.

**Then say:** "This is a draft to argue with. Rename anything that isn't a word you actually use. Tell me which to merge, drop, or add."

**Pushback lines** (use them; the user needs to be challenged):
- Over-modeling: "You named one Vendor. Until there are three, Vendor is a line on the pages that use it, not a kind of its own. Fold it in?"
- Homeless item: "You mentioned the quarterly board deck twice and it has no home on this list. Is it a Deliverable, or a Note?"
- Consultant word: "Would you say 'Engagement' to a colleague, or 'project'? Let's use your word."
- Same-shape pages: "Client and Partner look identical on the page. Same kind with a label, or genuinely different?"

**Iterate** until the user says the types are right. Ask explicitly: "Are the types right?"

### Relationships round (3 min)

**Say first:** "Now the sentences that connect them. I'll say what I think is true using your real examples; you correct me."

**Propose** connections as sentences, one per line, using named examples:
> "Acme has two Engagements: the AI Roadmap and the Pilot."
> "The Kickoff Checklist was used in the Acme Pilot."
> "Priya is your contact at Acme."

**For each sentence the user keeps, ask the earn-its-place question:** "What would you look up by following that link?" If they cannot answer, drop it: "Then we won't record it; it's not a connection you use."

**Then agree the heading on each side, in their words:** "On a Client page that's a section called *Engagements*. On an Engagement page, a section called *Client*. Good names, or would you call them something else?"

**Ask about order once per relationship where it could matter:** "Does the order of those matter, like steps or a timeline? If so I'll keep the list in order and say so in the rulebook." If order matters but you didn't collect the ordering facts (dates, sequence), seed the list in the order the user named the items and note in `SCHEMA.md` "order by <key>; confirm on first ingest".

If the user keeps a relationship in general ("clients have projects") but does not confirm a specific pairing, record the relationship in `types.md` and `SCHEMA.md` and leave the link sections `_None yet._` on the pages; never guess a pairing.

**Cap:** one to three relationships per type. If the user wants more, use the earn-its-place question again.

**Example to show:** the `# How they connect` section inside the `types.md` block in `references/example-knowledge-graph.md` (§ "types.md"), only if asked.

**What to write:** nothing yet.

---

## Phase 4 — Approve (1 min)

**Trigger:** the user says the list is right, explicitly. This comes after the relationships round; the approval covers types and connections together.

**What to write:** exactly one file, `types.md`, at the project root, in this shape:

```markdown
# The types

## Client
An organization we do paid work for.
Examples: Acme Manufacturing, Bowman Foods, Reston Health

## Engagement
One piece of contracted work, for one client.
Examples: Acme AI Roadmap, Acme Pilot, Bowman Data Review

## Playbook
A repeatable way we do something.
Examples: Kickoff Checklist, Discovery Interview, Handover Pack

## Note
Anything learned that has no other home yet, and answers worth keeping.
Examples: none yet

# How they connect

- A Client has Engagements. Heading: `# Engagements` on the Client page, `# Client` on the Engagement page. Order: by start date, oldest first.
- An Engagement uses Playbooks. Heading: `# Playbooks used` on the Engagement page, `# Used in` on the Playbook page. Order: no.
```

**Then say:** "That's your blueprint. Read it once, top to bottom. When you're ready for me to build the graph from it, send the single word **build** on its own."

---

## Phase 5 — Build (4 min)

**Trigger:** the word `build` as its own message. A go-word buried in a sentence does not count; if you get one, say "Send **build** on its own and I'll go."

Follow `references/build-spec.md` exactly. Fetch the latest OKF spec first. Report at the end, grouped as graph, rules, skills, with paths.

---

## Close — the loop, once (5 min)

Follow SKILL.md § Close. Lines to use:

- Cowork check: "Type `/ingest` and tell me whether it offers to run. If nothing happens, we'll add the two skills to your Claude account so they load."
- Ingest: "Pick one document in `raw/`, or paste one, and say *ingest it*."
- Query: "Ask me something that crosses a connection, like *which playbooks have we used with Acme?* I'll answer only from your pages and tell you which ones I read."
- File the answer: "Want me to keep that answer as a Note so it's there next time?"
- Lint: "Say *lint* and I'll sweep every page against your rulebook and report."
- Verify: "Open <one seeded page> and tell me if it's right. If it is, I'll mark it verified by you."
- Dictate: "What do you know that is in nobody's document? Tell me the way you'd tell a colleague, and I'll put it on the pages it belongs to."
- Obsidian: "If you want to see it drawn: install Obsidian, choose *Open folder as vault*, pick `knowledge/`, and click the graph icon."
- Hand-off: "You have a working graph with a handful of pages. It becomes useful at ten or more concepts across three types. Seed it on your real material this week and run the loop again."
