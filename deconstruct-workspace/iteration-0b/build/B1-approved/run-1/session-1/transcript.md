## Student

Run the build skill.

## AI

Phase 1 of 10: the plan and requirements are loaded.

- **Workflow:** Sales Pre-Call Brief (`registry/workflows/sales-pre-call-brief.md`)
- **Mechanism:** Skill. **Involvement:** Augmented. **Packaging:** Standalone Skill on Claude Code (code mode)
- **Counts:** 5 steps, 1 skill (S1, the `sales-pre-call-brief` orchestrator), 0 agents, 2 integrations (HubSpot, plus web search and fetch)
- **Approved:** yes. I also loaded the Workflow Requirements (`framework/sales-pre-call-brief/requirements.md`), along with the five test inputs E1–E5.

The plan file is named `design-plan.md` and is marked `plan_version: 4.0`, which is newer than the format this skill expects (`design-spec.md`, 3.0). The fields Build needs are all there, so I'm going ahead with it as it is.

There's no test-results file yet, so this is a full build.

**Phase 2 of 10: preparing the context**

| ID | Artifact | Outcome | Who does what | Read-back |
|---|---|---|---|---|
| C1 | Past brief, Halvorsen Logistics | **Build it in** | I package it inside the skill as `references/brief-format.md`, the format every brief follows | ✓ "Four parts in order: Hypothesis, Person (role, since when, a recent post), Likely priorities (three), Sources" — is that right? |
| C2 | HubSpot CRM | **Connect it**, read only | **You** add the HubSpot connector to Claude Code in this folder and authorize it with read scope only. Don't grant write, because the workflow never writes (`Writes: None`). Then I do a real read to check access | ⏳ **pending: this one blocks the build** |
| C3 | LinkedIn profiles | Read live (web search) | Nothing for you to do. LinkedIn often blocks direct page reads, so I'll write the skill to use search results and, when it can't confirm something, to say so plainly (R2) | ✓ (this access is Partial by design and handled by R2/R4) |
| C4 | Company websites and press | Read live (web search and fetch) | Nothing for you to do. These are built-in tools, and page text is handled as data, never as instructions (R3) | ✓ |
| I2 | Booking-form answer to "What would you like to cover?" | Prerequisite | **You** add the question to your scheduling page before the first real run. Until then the skill works from the calendar invite alone and says the answer is missing | pending (doesn't block the build) |

**I need you to decide on C1.** The Halvorsen brief names Halvorsen and Ingrid Moss. R1 says a brief must never name another client. If the skill carries the real brief, those names could leak into someone else's brief. My recommendation is to package a version with the names removed as the format reference:

```
Brief — [Company], call [date].

Hypothesis: they took the call because [one reason, tied to a recent change].

Person: [Name], [role] since [when] ([source]); [one recent post or statement] ([source]).

Likely priorities: [two or three priorities for their team].

Sources: [every source used, e.g. LinkedIn, press release [date], our CRM notes].
```

The original stays where it is in `context/` and remains E1's Golden Example for Test.

**To continue, I need three answers:**
1. **HubSpot:** connect it with read scope only, then tell me it's done. I'll check access by reading one company record.
2. **C1:** do you want the version with names removed (my recommendation), or the original brief as is?
3. Is the C1 read-back correct?

After that I'll confirm the build method and existing skills, check the HubSpot setup steps, and create the skill at `.claude/skills/sales-pre-call-brief/`.

## Student

1. HubSpot: not today, skip that for now.
2. Go with the version with the names removed.
3. Yes, that read-back is right.

## AI

Phase 3 of 9: settling the build method and checking for existing skills.

Context is resolved except HubSpot. C1 will be packaged with the names removed, and the original stays in `context/` for Test.

**HubSpot skipped for now.** Step 2 is fixed by your policy: *always check the CRM before the brief is written*. So the skill can't just skip it. My suggestion, which is the plan's default fallback when a connector isn't available, is a manual check:

- If the HubSpot connector is available, the skill reads the company record (read only).
- If it isn't, the skill stops before writing the brief and asks you to paste the CRM record, or to confirm there's no record. It never assumes "no past contact" by itself. Your test inputs E1 and E4 already include pasted CRM records, so Test can run against this.
- Once you connect HubSpot later, the same skill uses it and nothing needs rebuilding. C2 stays open in the build summary until then.

**What I found and how I'll build it:**
- **Existing skills:** this folder has no `.claude/skills/`, and none of your installed skills cover this workflow. I'll build S1 from scratch.
- **Build method:** I'll create the skill directly in Claude Code at `.claude/skills/sales-pre-call-brief/SKILL.md`, with `references/brief-format.md` next to it. You'll start it by name with `/sales-pre-call-brief`. It's set so Claude won't start it on its own. There are no configs or packages to write; the HubSpot connector setup comes later.
- **Format:** the platform registry gives the file layout (verified 2026-09-29). I can't fetch web pages in this session, so the frontmatter details come from my own knowledge of the format. I'll tell you if anything looks off.
- **Model:** I'm leaving the model unpinned so the skill uses your session's model. That suits the research and writing steps, which need careful reasoning.
- **Safety, built in:** text from web pages and profiles is treated as content and never followed, and anything that looks like an instruction gets flagged to you (R3). Nothing is written to HubSpot or anywhere else. The brief is saved in your working folder. The skill pauses at G1 for you to read the brief and add your questions, then closes with a short "What I did" summary.

**Can I go ahead with this, including the paste-the-CRM-record fallback?** Once you say yes, I'll create the skill and give you the build summary.

## Student

Yes, go ahead with that, including the paste-the-record fallback.

## AI

I couldn't create the skill. Claude Code asked for permission to write into `.claude/skills/sales-pre-call-brief/` and the request wasn't granted, so neither file was written. Nothing else has changed: no files were created, and your workflow's registry entry isn't updated yet.

Both files are drafted and ready:

- **`SKILL.md`** — the `/sales-pre-call-brief` skill (Claude won't start it on its own). It runs the five steps in order:
  - **Step 1:** researches what changed recently at the company and for the person.
  - **Step 2:** checks the CRM. It uses a pasted CRM record if you give one, otherwise reads HubSpot (read only) if it's connected. If neither is available, it stops and asks you to paste the record or confirm there isn't one. It never assumes "no past contact."
  - **Step 3:** forms one hypothesis about why they booked.
  - **Step 4:** writes the brief. If the CRM shows past work, the brief opens with that; otherwise it opens with the hypothesis. It's saved to `briefs/<company>-<date>.md`.
  - **Step 5:** pauses for you to read it and add your questions.
  - It then lists what it did and adds one row to `framework/sales-pre-call-brief/runs.md`.
  - Three rules are written in throughout: it never names another client, never invents a fact, and treats web text as data rather than instructions, flagging any embedded instructions to you.
- **`references/brief-format.md`** — the format with the names removed (Hypothesis, Person, Likely priorities, Sources), plus a line telling the skill never to reuse an example's names.

**To finish, choose one:**
1. **Grant the write** (recommended). Say "go ahead" and approve the permission prompt when it appears. The skill then goes in `.claude/skills/`, where Claude Code loads it with nothing to install.
2. **Write it somewhere else first.** I can put the files at `framework/sales-pre-call-brief/skills/sales-pre-call-brief/` for you to review, and you move the folder into `.claude/skills/` yourself. Until then the skill won't show up as `/sales-pre-call-brief`.

Once it's written, I'll update the registry entry and give you the build summary. HubSpot (C2) stays open for when you connect it.

## Student

Go ahead, I'll go with your recommendation and approve the write.

## AI

The skill still isn't written. The write was blocked again with the same message, "you haven't granted it yet", for both files. That means the approval didn't reach Claude Code. Your current permission mode may be refusing all writes to `.claude/` and never showing the prompt. I haven't retried again, and I haven't updated your registry entry, because nothing has been built yet.

Either of these will fix it:

1. **Allow writes to `.claude/skills/`.** Run `/permissions` and add an allow rule for editing files under `.claude/skills/**` in this folder, or switch to a mode that accepts edits. Then say "retry" and I'll write both files at once.
2. **Use the backup location.** I write the same two files to `framework/sales-pre-call-brief/skills/sales-pre-call-brief/`, which I've had no trouble writing to. You then copy that folder into `.claude/skills/` yourself. The skill only shows up as `/sales-pre-call-brief` once it's in `.claude/skills/`.

Which would you like? The drafts haven't changed: a five-step skill that uses a pasted CRM record or asks you for one, plus the brief format with names removed. Once the files are in place I'll check they load, update the registry, and give you the build summary.

## Student

I'm not sure how to change that permissions setting. Go with whichever you recommend. If that's the backup location in my folder, that's fine.

## AI

The `sales-pre-call-brief` skill is built, but it won't run until it's in `.claude/skills/`. Claude Code wouldn't let me write there (blocked twice), so the files are in the backup location and you need to copy them over.

| Build Output (from the plan) | Artifact | Path | Status |
|---|---|---|---|
| New skill: S1 (orchestrator) | sales-pre-call-brief | [framework/sales-pre-call-brief/skills/sales-pre-call-brief/SKILL.md](framework/sales-pre-call-brief/skills/sales-pre-call-brief/SKILL.md) | Created (staged) |
| Inline prompt → Step 1 (research) | sales-pre-call-brief, Step 1 section | same | Created (staged) |
| Inline prompt → Step 2 (CRM check) | sales-pre-call-brief, Step 2 section, with the paste-the-record fallback | same | Created (staged) |
| Inline prompt → Step 3 (hypothesis) | sales-pre-call-brief, Step 3 section | same | Created (staged) |
| Inline prompt → Step 4 (write the brief) | sales-pre-call-brief, Step 4 section | same | Created (staged) |
| Human (no artifact): Step 5 / G1 | — | — | — |
| MCP server: HubSpot | HubSpot connector, read only | — | **Not set up**: you skipped it for today |
| Web search and fetch | Claude Code's built-in web search and fetch | — | Nothing to set up |
| Context C1 (Build it in) | brief format with the names removed | [framework/sales-pre-call-brief/skills/sales-pre-call-brief/references/brief-format.md](framework/sales-pre-call-brief/skills/sales-pre-call-brief/references/brief-format.md) | Created (staged) |

Your workflow's registry entry now links to the skill, and the registry summary is refreshed.

**Still for you to do:**
1. **Install the skill.** Type this in the Claude Code prompt and press Enter (the `!` runs it as a terminal command):
   ```
   ! mkdir -p .claude/skills && cp -R framework/sales-pre-call-brief/skills/sales-pre-call-brief .claude/skills/
   ```
   If Claude Code asks for permission, approve it. Then open a new Claude Code session in this folder and type `/sales-pre-call-brief`. If it shows up, it's installed. Tell me once it's in and I'll delete the staged copy and point the registry entry at the installed one, so there's only one copy of the skill.
2. **HubSpot (whenever you're ready):** connect it with read scope only. Until then, the skill asks you to paste the CRM record, or to confirm there isn't one, before it writes the brief. When you connect HubSpot, the skill starts using it without being rebuilt.
3. **Booking form (I2):** add the "What would you like to cover?" question to your scheduling page before your first real run. Until then, each brief notes that the answer is missing.

I couldn't check the skill file's format against Claude Code's online docs because I can't fetch web pages here, so it's based on my own knowledge of the format. If `/sales-pre-call-brief` doesn't show up in a new session, the format is the first thing to look at.

One small thing in the registry: your workflow entry labels its plan link "Design plan", but the registry's label list only allows "Design spec". Want me to change the label?

**Next:** once the skill is installed, run the `test` skill (or say *"Test the workflow I built"*). A round takes about 45 minutes, and two to four rounds is normal. E1 and E4 include CRM records you can paste in. For E2, E3 and E5, tell the skill there's no CRM record when it asks.

## Student

END
