---
name: scaffolding-registry
description: >
  This skill should be used when the user wants to set up their AI Registry as a
  knowledge bundle — a registry/ folder with SCHEMA.md and concept nodes for the
  workflows, processes, and functions of their business. Triggers: "set up my
  registry", "set up my AI registry", "create my registry", "scaffold my
  registry", starting the registry lab, or when any framework skill finds no
  registry/SCHEMA.md where the leader keeps their framework files. NOT the
  business knowledge graph: for "build my knowledge graph" or a knowledge/
  folder about the work itself (clients, offerings, processes as knowledge),
  use building-knowledge-graph. Re-running on an existing bundle fills gaps; it
  never re-scaffolds.
---

# Scaffolding Registry

Stand up a leader's AI Registry as an [OKF v0.3](https://github.com/open-knowledge-format/open-knowledge-format) knowledge bundle: a `registry/` folder with a `SCHEMA.md` producer profile and concept nodes for their real business. This is the on-ramp: a short guided interview that captures the leader's real business, its lines of business, and the processes that deliver them, each with its owner. It names no workflows: the `analyze` skill does that next, writing them into the backlog.

**Your first message settles where the files go.** Unless the leader named their folder, or this chat is already working in a folder on their computer (Claude desktop's selected folder, Claude Code, Codex; a sandbox or workspace the AI runs in online is not their computer, and a zip handed back from it is not saving; a folder the app made for this chat alone, named by date or after the chat, is never the working folder), the first message is N-F16 (no drive in this chat can save) or the storage question, N-F1, exactly as *Where the files live* gives them. That holds on Claude or ChatGPT on the web in any tab or mode, ChatGPT's Work tab included. Nothing comes before it: not the opening, not the first question. **Every scripted line is said in full:** every sentence, in its order, with only its [brackets] filled; never dropped, merged, shortened or paraphrased.

## What this builds

The registry lives in the **working folder**, the one folder that holds the leader's AI Registry (`registry/`), their workflows (`framework/`, the framework folder) and their knowledge graph (`knowledge/`). Where that folder is depends on where the leader works (see *Where the files live* below): on Claude Code and Codex it is the workspace; on the web (Claude, ChatGPT), a folder in a storage service the leader connects (Google Drive, OneDrive, Dropbox and others), `ai-workspace/` unless they keep another; in Microsoft 365 Copilot (Cowork), that folder in OneDrive; on Claude desktop, the folder the leader selects in the prompt window. The layout inside it is the same everywhere:

```
<working folder>/            ← the workspace on Claude Code and Codex; ai-workspace/ (or the leader's own folder) elsewhere
├── REGISTRY.md              ← Tier 1 dashboard (derived, never hand-edited)
├── registry-dashboard.html  ← Tier 2 visual dashboard (derived; always generated at setup)
├── registry/                ← the OKF v0.3 bundle
│   ├── SCHEMA.md            ← producer profile (written by scaffolding-registry)
│   ├── index.md             ← bundle root; frontmatter okf_version: "0.3"
│   ├── log.md               ← setup decisions, schema changes, workflow events (newest date first)
│   ├── businesses/  lines-of-business/  functions/
│   ├── processes/   workflows/          notes/
│   │       (each typed directory has its own index.md)
├── framework/               ← the framework folder (made by the first step that saves a workflow, never by this skill)
│   └── <workflow>/          ← the workflow's record: requirements.md, design-plan.md,
│                              build-record.md, test-results.md, with inputs/, context/
│                              and history/
├── knowledge/               ← the knowledge graph, when the leader builds one (building-knowledge-graph)
├── sops/  process-guides/   ← unchanged homes; nodes link to them
```

A workflow's **run log** is never in the working folder: it lives where the workflow runs. Event facts stay in the workflow's record, never in registry nodes.

The registry is the structured record every framework skill reads and writes: `analyze` writes backlog Workflow nodes into it, `deconstruct` starts a workflow (`under-development`) and links its requirements, `design` records how the workflow decides and runs and links its plan, `build` links the skills and agents it built, and `test` links the test results and takes the workflow live (`in-production`). `registry/SCHEMA.md` is the contract that makes that possible: it defines the six concept types (Business, LineOfBusiness, Process, Workflow, Note, Function), their required frontmatter, and the rules (enum values, link discipline, banned fields) that every skill's writes and every maintenance pass's lint checks agree on. Write it once per registry, using `references/schema-template.md` verbatim; after that, the leader's own copy is authoritative and every skill re-reads it before writing.

## Platform & Workspace

The procedure below is identical everywhere: the same four phases (0–3), the same node shapes, the same SCHEMA.md. Platforms differ only in how the skill instructions arrive and how files get saved.

| Platform | Skill delivery | Where the registry lives | How files are saved |
|---|---|---|---|
| Claude Code | handsonai plugin | `registry/` in the workspace | directly |
| ChatGPT desktop (Codex) | same SKILL.md dirs at `~/.agents/skills/` (user-level default) or repo `.agents/skills/` (optional pin) | `registry/` in the workspace | directly |
| Claude desktop app | handsonai plugin (installed once, shared with Claude on the web) or skill ZIP | `registry/` inside the working folder the leader selects in the chat | directly |
| Claude on the web | handsonai plugin (paid plans; same install as the Claude desktop app) or skill ZIP (Releases channel) | `ai-workspace/registry/` (or the leader's own working folder) in a connected storage service that can create files (Google Drive, OneDrive on a work or school account, Dropbox, …) | through the connection |
| ChatGPT web (paid plans) | handsonai plugin via Plugins > Add marketplace, or Personal Skill upload (same ZIP) | `ai-workspace/registry/` (or the leader's own working folder) in a connected storage service that can create files (Google Drive, OneDrive on a work or school account, Dropbox, …) | through the connection |
| Microsoft 365 Copilot (Cowork) | Cowork skills (the plugin archive or a skill ZIP) | `ai-workspace/registry/` (or the leader's own working folder) in OneDrive, separate from Cowork's own folder | Cowork's own OneDrive edits |
| Gemini Spark / Gemini Enterprise | skill ZIP via Skills > Upload | none until a place that can save is added | nothing can save: N-F16, and wait (`references/saving.md`, rule 5) |

A few rules follow from that table:

- **(a) Assistant-agnostic procedures.** Everything in this file (the phases, the write rules, the interview questions) is written for "your AI assistant" in general. Platforms differ only in delivery and saving, never in what gets written or asked.
- **(b) Save through the drive.** On the web and in Cowork, write every file through the drive connection into `registry/` in the working folder. How to save comes from the tools the connection gives you (`references/saving.md`). Where a connection can only create files but can move and rename them, follow the drive-saving rule in the `indexing-registry` skill's `references/registry-bundle.md` (§2, rule 8). Where there are no files and no connection that can save, nothing is written: N-F16, and wait (`references/saving.md`, rule 5). Never leave the leader assuming a file landed somewhere it didn't. A file the leader would have to download doesn't count as saved.
- **(c) Home: any folder; GitHub is optional.** A local folder, a drive folder, or a GitHub repository all work: the bundle is plain Markdown with relative links and never depends on Git. Never require GitHub, and never mention it, the template repository or its scripts unless the leader asks (*Talking about the check*, in the `indexing-registry` skill, gives the one short answer).
- **(d) One skill artifact, three channels.** The same agentskills.io-standard SKILL.md, packaged by `build-skill-zips.sh` in the handsonai-plugins repository, is what Codex desktop scans locally, what ChatGPT web's Personal Skills accepts as an upload, and what Claude and Cowork accept as an uploaded skill. There is no separate packaging for each.
- **(e) Repo-checked-in skills are optional, not the default.** Codex desktop can read `.agents/skills/` inside the leader's repo, but the default is a user-level install (`~/.agents/skills/`): checking a skill into every repo it's used in invites version drift between repos. Only pin a repo-local copy when the leader has a specific reason to.

**Platform note (Claude):** the closing step always generates the visual dashboard as a file that opens in any browser. On Claude, also offer it as a Claude Artifact — a private page the leader can open from Claude any time and share with a link — using the interview guide's wording: on Claude on the web, Claude desktop and in a cloud session as the close's one question; on Claude Code, only where the session can publish a Claude Artifact, as a choice inside N-SR8 rather than a question. The Artifact is in addition to the file, never instead of generating it.

## Where the files live

Settle this before anything else, because every later step reads and saves in the same place. **Nothing comes before it:** no greeting, no opening, no first question (3c-EL).

- **On Claude or ChatGPT on the web, in any tab or mode, ChatGPT's Work tab included (never Claude desktop, Microsoft 365 Cowork, Claude Code or Codex: any chat not working in a folder on the leader's computer counts as the web, and a sandbox or workspace the AI runs in online is not the leader's computer, and a folder the app made for this chat alone, named by date or after the chat, is never the working folder), first a drive this chat can save to.** When no connection in this chat can create files, or you can't tell, the first message is N-F16, said exactly: "I can't see a drive I can save to in this chat. Add your cloud drive to this chat from the prompt box (or connect it first, if you haven't), with saving allowed, then say 'done'. Your work is saved as you go, so it needs a place: a drive such as Google Drive or OneDrive, a folder on your computer, or GitHub." No menu path beyond "from the prompt box". On "done", look again (N-F16 again if there's still none); until then, wait (`references/saving.md`, rule 5).

- **Claude Code and Codex:** the registry is `registry/` in the workspace. Nothing is asked. **A cloud session** (the session says it runs in the cloud, or the workspace is a fresh clone of a GitHub repository with nothing of the leader's own computer in reach): name the repository, never a path on the machine. N-F3's [location] is "your [repository] repository on GitHub", and the opening adds once: "Changes are saved to GitHub, on a branch." After the close's check, commit `registry/`, `REGISTRY.md` and `registry-dashboard.html` and push them to the session's branch yourself, and again after the Artifact's log line, asking nothing (it is how the work is kept there; never rely on the platform to prompt it), and, whenever that branch isn't the repository's default, say N-F18: "Your work is saved on GitHub, on the branch [branch]. Before your next step, merge it into main, or choose this branch when you start the next session." There, the Git save-point offer isn't made. If you can't tell whether this is a cloud session, say N-F18 whenever the work was pushed to a branch other than the default. A website or link the session can't reach: say so in one line, ask the leader to paste the key text or answer from memory; never propose changing the environment, network, permissions or credentials.
- **Claude desktop:** the registry goes inside the working folder selected in this chat. When this is the leader's first framework skill and the chat has no folder selected, the first message is N-F12, said exactly, with its *Why* when the leader asks why:

  > "Your AI work lives in one working folder on your computer: your AI Registry, your workflows and your knowledge graph. Select your working folder in the prompt window. If you don't have one, make a folder called ai-workspace, for example in Documents, and select that. Open each step of the framework in a new chat with that folder selected. Say 'done' when it's selected[, or 'use my drive' to keep it in [storage service] instead]."
  >
  > *Why:* "Every step reads and saves these files, so a new chat needs to find them."

  If the leader can't find where to select a folder, say you can't confirm the exact steps, that they can select it their own way, and which page to check (`references/platform-facts.md`, rule 2); never make up a menu path, and never a guessed name for an item, even with 'something like': say what to look for in plain words only, as N-F12 does. Offer "use my drive" only when a connection that can create files is on, with [storage service] filled as on the web; on that answer, continue as on the web. When the selected folder is a general folder (below), the big-folder follow-up comes first; on "go ahead", make `ai-workspace` inside it as the working folder and say in one line, in your own words, to select that folder in each later framework chat.
- **On the web and in Microsoft 365 Copilot (Cowork):** take the location from the start phrase ("set up my registry. My files are in Google Drive, in ai-workspace."), or find the working folder: a folder named ai-workspace in the drive; else a folder holding `registry/SCHEMA.md` or `framework/`, taken as the working folder once the leader confirms it in one line. When there's no working folder yet (this is the leader's first framework skill), ask the storage question as the first message, before the opening and before anything is read or written. Files uploaded to the chat are never the working folder. Never pick the AI's own file library (such as ChatGPT's Library) yourself, or search it in place of asking; but where this chat's tools can create and change files in it, name it in the storage question's [storage service] beside any drive ("Google Drive or your ChatGPT Library"), and a folder there that the leader names or chooses is a working folder like any other, saved by the same rule as a drive. Where [storage service] names more than one place and the leader says "go ahead", ask which one in one line. Say N-F1 exactly and in full (every sentence, in order; none dropped, merged or shortened), filling [storage service] with the storage services connected in this chat whose connection can create files, by their own names ("Google Drive", or "Google Drive or Dropbox"); where you can't tell which is connected, "connected storage"; in Cowork, its Microsoft 365 form:

  > "Where should your working folder go? It holds your AI Registry, your workflows and your knowledge graph. Say 'go ahead' and I'll make a private folder called ai-workspace in your [storage service], or tell me the name of one you already have. To keep it somewhere else, such as Google Drive, OneDrive or Box, add it to this chat from the prompt box first. The connection reaches your whole drive, but I'll only read and save inside that folder, and never share or delete anything. Run each step of the framework in a new chat that isn't inside one of your [Claude / ChatGPT] Projects." Where [storage service] is only the AI's own library (no drive in this chat), its fourth sentence is "I'll only read and save inside that folder, and never share or delete anything."

  Microsoft 365:

  > "Where's your working folder? It's the one folder that holds your AI Registry, your workflows and your knowledge graph. If you already have one in your OneDrive, tell me its name. If not, I'll make a folder called ai-workspace there, separate from Cowork's own folder. Cowork can see your whole OneDrive, but I'll only read and save inside your working folder, and never share or delete anything. Please run each step of the framework in a new Cowork chat. Say 'go ahead', or tell me your folder's name."
  >
  > *Why:* "Every step reads and saves these files, so a new chat needs to find them."

  Never assume the leader has a working folder, or that they don't. On "go ahead", make `ai-workspace/` with `registry/` inside it. When they name a folder, use it: first look for it: where it isn't in the [storage service] (or the folder), ask N-F17, "I can't find [folder] in your [storage service]. Shall I create it there? Say 'go ahead', or tell me another folder's name.", and on "go ahead" make it there; ask for a link only when the folder clearly exists but can't be reached by name, then make `registry/` inside it. Never make `framework/`: the first step that saves a workflow makes it. Analyze and every later step take the location from the start phrase, so the storage question is never asked twice.
- **A general folder** (a drive's top level, or a folder named Documents, Desktop or Downloads, or the home folder): before saving anything, the big-folder follow-up (N-F15), said exactly:

  > "That folder holds a lot besides your AI work. I'd suggest a new, clean folder called ai-workspace instead, so the framework only ever touches your AI work. Say 'go ahead', or 'use it anyway'."

  On "go ahead", make `ai-workspace` (on the web, in the drive; on Claude desktop, inside the selected folder) and use it as the working folder; on "use it anyway", use the folder they named or selected. When you're unsure whether any other folder is one (its file names show a lot besides AI work), ask N-F15b instead, said exactly: "Is this a folder you set up for your AI work?" On yes, use the folder; on no, the big-folder follow-up. A folder that holds only `registry/`, `framework/` and `knowledge/` is never asked about. Both are asked only on the web, Claude desktop and Cowork; never on Claude Code, Codex, the Work tab in a local folder or in a cloud session. Analyze uses an N-F15b answer given here when it runs in this chat, so it isn't asked twice.
- **No files and no connection that can save** (Gemini, or on the web with no drive that can save): N-F16, and wait (`references/saving.md`, rule 5).

Never ask the leader to approve a path; say where the registry is saved in the opening (see the interview guide).

## Before scaffolding

Before running the interview, check what's already in the working folder (locally, the workspace):

0. **A `knowledge/` folder exists** → leave it alone — never write to it or lint it; Phase 0 may read it as an intake source. It is the business knowledge graph, a different OKF bundle with its own `SCHEMA.md` and its own lint (built by `building-knowledge-graph`). Say so in one sentence and continue with the registry checks below.
1. **`registry/SCHEMA.md` exists** → this is **gap-filling mode**, not a fresh scaffold. Look for it as soon as the location is known, before the opening and before the first question. Then these steps, in this order, every one of them, with nothing said before the first:
   1. **Confirm a folder you found.** Where you found the registry by looking (the leader didn't name the folder), confirm it in one line, naming the folder and where it is, and wait for the answer. Where the leader named it, go on.
   2. **Say N-SR2 exactly:** "You already have a registry here, so I'll check it for gaps instead of starting over." No preamble before it. If you already asked a question it makes unnecessary, say so in one line rather than dropping it silently.
   3. **The gap pass.** List which concept types have zero nodes and which typed directories are missing their `index.md`, tell the leader what's missing, and offer to fill only those gaps. With no gaps, say so in one line, then the close's check, the dashboard and N-A7.
   4. **The close's check, every time, gaps or not** (*Close*). It fills or fixes each Function's `# Owns` block, including the earlier form with the heading inside the markers. Finding the pages present is not the check: a registry that looks complete still gets it.
   5. **The dashboard and `REGISTRY.md`, rebuilt**, as at any close.
   6. **The close as the interview guide gives it**, ending with N-A7: Analyze's start phrase and the location, as text the leader can copy.

   To the leader the files are "pages": never "schema", "structure" or "nodes". Never overwrite an existing node, and never rewrite `SCHEMA.md` once the leader has one — their copy is authoritative from here on.
2. **No `registry/SCHEMA.md`** → run the interview below from Phase 0. Files left by an earlier version of the framework are never read, moved or converted: the registry is set up fresh beside them.

## The interview

Four phases (0–3), run in order. Follow `references/interview-guide.md` for the exact opening, questions, card, process messages and close — this section is the map; that file is the script.

**How the leader experiences it.** No parts or phase numbers: an opening with one open question, a card to confirm, one message per line of business for its processes, then the close. A business with three lines of business answers about five questions; with one line, about three.

| What the leader sees | Phase | What gets saved |
|---|---|---|
| The opening and the first question (N-SR4, N-SR1, the save line, N-SR5), then a follow-up only for what the answer left out | 0 | The empty skeleton, after the answer |
| The card: who it's for, name, what it does, goals, lines of business (N-SR6) | 1 | Business and Lines of Business, on yes |
| Processes and their owners, one line of business per message (two per message with four or more lines; N-SR7) | 2 | Processes, and each Function the first time it owns one, on each yes |
| The close | 3 | The founding log entry, then the check and the views |

Rules for every message in this interview:

- **One question per message.** Never number two or three questions in one message.
- **Ask only for what's missing.** The first question is open; ask a follow-up only for something the answer and the sources left out (what it offers, then goals), and never ask the same thing twice. When the card or a line's draft came only from the leader's last answer, ask "Shall I save this?", not whether it matches.
- **Never name a skill, or a hand-off between skills.** Say what happens in plain words ("Now I'll check your registry and build your dashboard.").
- **Play back in plain words, never as a file.** Show drafts as labeled plain text (the card; Process · Owner), never as raw frontmatter, Markdown headings, or file names. A Note is never its own question: a volunteered insight is saved with the next confirmation (the interview guide's *Phase 3*). Offer "Want to see the file itself?" once, only if the leader asks how it's stored.
- **Confirm before writing.** Write each card or line only after the leader confirms it. After an edit, play back only what changed and save on yes. If you interpret an answer (two goals or three?), ask; don't write your reading and offer to fix it.
- **Never mention a check that found nothing**, a lint rule, or the maintenance pass as the reason for a question. Give the leader's reason instead.
- **A one-line *Why* with each question,** except save confirmations (N-SR6, "Shall I save this?", "Shall I save these?"), where the draft above is the reason. *Example* and *Not sure?* lines, and the Brightwork example (`references/example-registry.md`), only when the leader says "not sure" or asks. If the leader says "skip the explanations", drop the *Why* too.
- **No time and no step numbers.** Never say how long the interview takes, and never number the framework's steps: name the step ("Analyze").

**Phase 0 — Opening and the first question.** The storage question, when it's needed, comes first (*Where the files live*). Detect, don't ask, how files are saved (with no files and no connection that can save, N-F16 and wait). Scan the working folder silently for a source to draft from (`references/intake-sources.md`); mention it only when you found one. Then the opening, N-SR4 with N-SR1, the save line (N-F3's promise clause, and the platform's save-permission line), and the first question, N-SR5, all in one message. Work out who the registry is for from the answer (`references/personas.md`, *Working out who it's for*); ask one follow-up only when it's unclear. Follow up only on gaps (what it offers, then goals). Goals only as the leader gives them: never invented or drafted; with none, record none and say N-SR3, "Your goals for this year aren't recorded yet; tell me them any time." Then write the skeleton (it holds nothing about the business, so it needs no confirmation). The template repo (`https://github.com/jamesgray-ai/ai-registry-template`) is only the answer to "where's the template repo?" — never a prerequisite.

**Phase 1 — The card.** One message: who it's for, the business's name, a one-sentence identity, website (when given), goals, and the lines of business in a curated order (ordered yourself by the goals, each with a one-line description; lines of business defined in one clause on the card). Set `state` yourself — `active` unless the leader described something not yet launched, paused or winding down. The number of lines follows how many distinct things the business offers, never how many people do the work: a solo consultant with three offerings gets three lines, and a single-offering business gets one line named after the business — no artificial splitting. On yes, write the Business page (goals as a bulleted list under a `## Objectives` heading in the body, below the identity sentence and above `# Lines of Business`; prose only, no frontmatter field; `analyze` reads it so the leader is never asked for goals twice; omitted when there are none) and one LineOfBusiness page per line. Almost always exactly one business per registry; for a professional it is their team, for the personal persona it is the person or household.

**Phase 2 — Processes and their owners.** Per line of business, three to five processes that deliver it (fewer when one person does all of a line's work as one piece of work; never split one to reach three) — where the time, money and customer outcomes actually flow — ordered yourself by value-chain order and the leader's goals; **never ask the leader to rank them** (Analyze asks which matter most before it walks them). Each process has a required `owner:`, drafted from what the leader said about who does the work (`references/personas.md`, *Owners*): for a founder working alone, three or four hats named for the area of work. Don't ask for SOPs or guides: fill `guide:` only when a source turned one up. Map how the business delivers, never where AI might help. Not exhaustive: Analyze grows this later. **The functions are the owners:** write a Function page the first time a process the leader confirms uses it, with its empty GENERATED `# Owns` block, so no Function ever owns nothing — there is no starter set and no question about unused functions. The owning Functions' `# Owns` blocks are stale until the close's check regenerates them — that's expected, not an error.

**Phase 3 — Close.** The founding `log.md` entry (who the registry is for, in exactly one of the fixed forms in `references/personas.md`, *The founding log line*: `analyze` and `deconstruct` read it), the empty `registry/workflows/index.md` (Analyze fills the workflows in — this scaffold never names one), a Note only if the leader volunteered an insight (never prompt for one), then the check, the views and the close — see Close below.

When a source covers part of the interview, the first question opens with what it covers ("From your [source], I can see …") and asks only for what it lacks; the card and the process drafts use it. Write only what the leader confirms. Sources shorten the interview.

If the leader can't finish, write what they have confirmed, note the gap for the close-out summary, and move on — missing pages are homework for later; fictional ones are never an acceptable substitute.

## Write rules

- **The leader's `registry/SCHEMA.md` is authoritative once it exists.** Re-read it immediately before every write in this skill, including during gap-filling — never write from memory of what the schema template said.
- **Stamp `generated: { by: process:scaffolding-registry, at: <YYYY-MM-DDTHH:MM:SSZ> }`** (single-line flow map; `at` is the moment of the write as a UTC instant, such as `2026-10-24T15:04:05Z`) on every node this skill creates or whose content it changes (a page whose curated list gains a line included); a formatting or link repair leaves `generated` as it is. `SCHEMA.md` isn't a node: it is copied exactly as the template ships it, its own `generated` line included. Never write a bare date, and never write `verified`: only the leader's own check is recorded there (`registry-bundle.md`, rule 11).
- **Business and line-of-business state goes in `state`** (`state: active`), never `status`, which the schema keeps for the lifecycle (`draft`, `stable`, `deprecated`). A link to a file outside `registry/` (a `guide:`) is file-relative from the page: `guide: ../../process-guides/<file>.md`.
- **Function nodes are always written with their empty GENERATED `# Owns` block** (the `# Owns` heading above and outside the markers, nothing between them yet; `indexing-registry`'s *Regenerate GENERATED blocks* shows the filled form) at creation time — never deferred to a later maintenance pass. A Function missing that block is a lint error, because the maintenance pass has nothing to fill.
- **Slugs are plain ASCII kebab-case** — fold accents (`Café Orders` → `cafe-orders`), `&` → `and`, strip other punctuation — so filenames and links agree on every platform.
- **Every new node gets added to its typed directory's `index.md`.** A concept file with no entry in its directory index is a lint error; write or update the index in the same pass as the node. An index with no nodes yet has exactly this body — the heading, a blank line, and `_No entries yet — your AI assistant fills this index as nodes are added._` — which is the text compose writes, so a fresh scaffold composes with no file rewritten. Index entries use bundle-root-relative leading-slash links — `[Client Onboarding](/processes/client-onboarding.md)`, never a bare same-directory link like `[Client Onboarding](client-onboarding.md)`, which reads from the index's own folder and which the schema forbids for a link to another page.
- **On a drive,** every file is saved through the connection, the way `references/saving.md` decides from the connection's tools, by the drive-saving rule in the `indexing-registry` skill's `references/registry-bundle.md` (§2, rule 8). Nothing on a drive is ever shared, trashed or deleted.

## Close

End Phase 3 by writing a founding `registry/log.md` entry describing the scaffolding run (what was created), under today's `## YYYY-MM-DD` heading as a `- **Registry scaffolded** — …` bullet (`registry-bundle.md` §7), and making sure every typed directory has an `index.md`, even a stub one — including `registry/workflows/index.md`, which starts empty because this skill writes no Workflow node; the `analyze` skill adds the first ones.

Then invoke the `indexing-registry` skill for the first maintenance pass: it lints the new bundle, generates the Tier 1 `REGISTRY.md` — which is written in the registry's parent folder, next to `registry/` and not inside it — and **always** generates the Tier 2 visual dashboard, `registry-dashboard.html`. The dashboard is not an option at setup: it is the leader's window into the registry, and a leader offered it as one of "two options" skips it. On the web the pass saves through the drive connection, like every other save. This is a best-effort hand-off — if the maintenance pass can't run for some reason, say so plainly rather than leaving the leader assuming it happened. The lab should end with something visual on screen, not a blank terminal.

Then deliver the close exactly as the interview guide gives it: what was made (counts), where it's saved, the dashboard and how to open it on this platform (the close names the dashboard only, never `REGISTRY.md`; on Claude Code and Codex, N-SR8: the leader says "open my dashboard" and you open it), that the leader can reshape the registry any time by asking, and Analyze's paragraph (N-A7) with Analyze's start phrase and the location. The pass checks the pages this skill wrote plus the cross-page essentials (`indexing-registry`, *Check the registry*), claims no more, and says nothing when they pass. If you say anything before it, say only: "Now I'll check your registry and build your dashboard." Never name a skill or a hand-off between skills ("the scaffolding skill hands the pages to…"), and never claim more than this check covers ("I'll check every page against every rule" is wrong here). To the leader it is "checking your registry", the files are "pages", never nodes, and no "maintenance pass", lint, compose, script, `tools/`, GitHub Action or template repository is named unless they ask; never ask them to choose between those. Say nothing about lint results or GENERATED blocks; the close asks at most one question, as the guide gives it: on Claude on the web, Claude desktop and in a cloud session, the Claude Artifact offer (on Claude Code it is a choice inside N-SR8, made only where the session can publish a Claude Artifact, not a question); elsewhere, only where the folder is a git repository (detected with `git rev-parse --show-toplevel`), the save-point offer (commit locally; don't push as part of it). Analyze's start phrase is given as the next step, never as a question. If the leader then says it, or asks to run Analyze in this chat, invoke the `analyze` skill; it knows the registry was built in this conversation, so it says its opening with its same-chat registry clause, and asks no second storage question.
