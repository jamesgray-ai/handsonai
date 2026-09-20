---
title: AI Registry Setup
description: Set up your AI Registry — a Markdown knowledge bundle that tracks your workflows, skills, agents, and business context — no external tools required
schema_type: HowTo
howto_steps:
  - name: Pick a folder for your registry
    text: Any folder works — on your computer, in a cloud drive, or in a GitHub repository. Ask your AI tool whether it can create files inside that folder for you, or whether it will print each file for you to save.
  - name: Run the interview
    text: Answer the interview (about 30 minutes) — your AI assistant writes your Business, Line of Business, Function, Process, and first Workflow nodes as you go.
  - name: Review your first Workflow node
    text: Open the Workflow node your assistant wrote in registry/workflows/ and confirm it matches your real work.
  - name: Keep it fresh
    text: Ask your AI assistant to "update my registry" any time it looks stale, or let the framework refresh it automatically after each step.
---

Your **AI Registry** is your inventory of everything you build and run with AI: your business, its lines of business, the processes and workflows inside them, and the skills, agents, and apps those workflows use. It lives entirely in your workspace as Markdown files — no database, no external account, nothing extra to maintain.

New to Markdown? It's plain text with a few formatting marks — see [Markdown Basics](../markdown-basics/) for a ten-minute primer.

## What Your AI Registry Is

Your registry is a **knowledge bundle**: a folder of small Markdown files, each describing one real thing about your business — your company, a line of business, a function like Sales or Operations, a process, or a workflow. Every file is called a **node**. Your AI assistant writes and maintains these files. If your AI tool can create files, you never touch them; if it can't, it prints each file and you save it — but you never have to *compose* one yourself.

On top of those nodes sit a few **dashboards** — files your assistant generates *from* your nodes, purely for you to read. You never hand-edit a dashboard either; if one looks wrong or stale, you ask your assistant to regenerate it, and the fix sticks because the fix happens in the nodes, not the dashboard.

Here's the shape of a workspace after setup:

```
my-ai-workspace/
├── REGISTRY.md              ← dashboard: at-a-glance index (generated)
├── registry/                ← your registry bundle
│   ├── SCHEMA.md            ← the rules your assistant reads before every write
│   ├── index.md             ← bundle root (declares okf_version: "0.2")
│   └── businesses/ lines-of-business/ functions/
│       processes/ workflows/ notes/
├── outputs/<workflow>/      ← raw work: requirements, run logs, artifacts
└── sops/ process-guides/    ← unchanged homes; Workflow nodes link to them
```

Your registry follows an open, public specification called the **Open Knowledge Framework (OKF)** — this isn't a format James invented for this playbook. You can read the live spec any time: [OKF on GitHub](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf). You never need to read it to use your registry — your assistant already knows it — but it's there if you're curious how the pieces fit together.

**The one thing to remember:** your AI assistant maintains your registry. You describe your business and your work in plain language; your assistant writes the nodes and regenerates the dashboards. You never edit a dashboard by hand, and you rarely need to hand-edit a node either.

## Before You Start

Two things, in this order:

1. **The Hands-on AI skills are in your AI tool.** Your registry is set up by a skill called `scaffolding-registry` and kept tidy by one called `indexing-registry`. If you installed the Hands-on AI **plugin** (Claude or ChatGPT), you already have both. If you added skills one at a time by uploading ZIP files (Gemini, Microsoft 365 Copilot, or a plan that blocks plugins), upload these two the same way you uploaded the others:
   - [scaffolding-registry.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/scaffolding-registry.zip) — sets up your registry
   - [indexing-registry.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/indexing-registry.zip) — keeps it tidy

   Haven't set up the skills yet? Follow [Set Up the Skills](../../ai-workflow-framework/skills/) for your tool — it has click-by-click steps for every platform — then come back here.
2. **A folder for your registry.** Any folder: on your computer, in a cloud drive such as Google Drive or OneDrive, or in a GitHub repository. You do not need GitHub — see [Where Your Registry Lives](#where-your-registry-lives).

## Where Your Registry Lives

Your registry is a folder of Markdown files. It can live anywhere: a folder on your computer, a folder in a cloud drive such as Google Drive or OneDrive, or a GitHub repository. GitHub is optional — it adds a few conveniences, listed at the end of this section, but nothing about your registry needs it.

The interview your assistant runs, the files it writes, and the dashboards it generates are identical everywhere. The **only** thing that differs is who saves the files. Ask your AI tool this exact question:

> "Can you create and edit files inside a folder I choose — on my computer or in my cloud drive — without me downloading anything?"

| Your AI tool says… | Typical tools | Follow |
|---|---|---|
| **Yes** | Claude Code, Cowork (the Cowork tab in the Claude app), ChatGPT desktop (the Codex tab), Cursor, Codex CLI, Gemini CLI | [Your assistant saves the files](#your-assistant-saves-the-files) |
| **No** | claude.ai, ChatGPT on the web, Google Gemini, Microsoft 365 Copilot | [You save the files](#you-save-the-files) |

A downloadable file counts as "no" — if your tool offers you a file to download, it can't put it in your folder for you.

### Your Assistant Saves the Files

About 30 minutes, all of it the interview.

1. Pick the folder. **Not sure? Create a new empty folder called `ai-registry` inside your Documents folder** — that's the default. Two other options work just as well:
   - The folder on your computer you made in [Create & Clone Your First Repository](../repo-creation-and-cloning/), if you followed that guide.
   - A folder in your cloud drive, **as long as it also appears on your computer** — that means the Google Drive or OneDrive desktop app is installed and syncing. Your AI tool works on the copy on your computer; the app keeps the cloud copy current.
2. Open that folder in your AI tool:
   - **Claude Code:** open Terminal, type `cd ` (with a space after it), drag the folder from Finder or File Explorer into the Terminal window, press Enter, then type `claude` and press Enter. New to Terminal? See [Terminal Basics](../terminal-basics/).
   - **Cowork:** choose the folder as your working folder — it can be a Cowork project or any folder on your computer.
   - **ChatGPT desktop:** open the folder in the **Codex** tab.
   - **Cursor / Codex CLI / Gemini CLI:** open the folder as your project.
3. Say: *"Set up my AI registry."* This starts [The Interview](#the-interview) below.

**You should now see**, once the interview begins, a new `registry/` folder inside the folder you picked — look in Finder or File Explorer — containing `SCHEMA.md`, `index.md`, and empty typed folders (`businesses/`, `workflows/`, and so on). If the folder already had files in it — skills, agents, workflow outputs — nothing is moved or deleted. If your assistant finds files from an older version of this framework, it offers to migrate them first (see [Migrating From the Old Workflow Manifest File](#migrating-from-the-old-workflow-manifest-file)).

### You Save the Files

Your assistant runs the same interview, but instead of saving each file it prints the file's complete contents and tells you exactly where it goes — for example, *"save this as `registry/businesses/your-business.md`."* You save it. Nothing to install.

**Plan for about an hour:** the 30-minute interview plus 20–30 minutes of saving. The interview produces roughly 15–20 files, including updates to a few files it already gave you.

1. Decide where the files will go. **Easiest: a GitHub repository.** Typing a file's location creates its folders for you, there's no way to save the wrong file type, and GitHub builds your dashboard automatically. Set one up in three minutes in [Optional: Let GitHub Build Your Dashboard](#optional-let-github-build-your-dashboard), then come back here. Two other options if you'd rather not use GitHub:
   - **A folder on your computer.** Create an empty folder called `ai-registry` inside your Documents folder.
   - **A folder in your cloud drive.** Only if the Google Drive or OneDrive desktop app is installed and syncing — then create the `ai-registry` folder inside your synced drive folder and treat it exactly like a folder on your computer. (The Drive and OneDrive *websites* can't create Markdown files, and re-uploading a changed file creates a duplicate.)
2. **If you chose your computer or cloud drive,** get the empty registry skeleton first, so you don't have to paste the long rules file by hand: open [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template), click the green **Code** button, then **Download ZIP**. No account needed. Unzip it and move the `registry` folder it contains into your `ai-registry` folder. (You can ignore the other folders in the download.) If you chose GitHub, your repository already has this skeleton.
3. Say: *"Set up my AI registry. You can't save files for me, so print the full contents of each file and tell me exactly where it goes. I already have the empty registry skeleton."*
4. Save each file where your assistant says — see [Saving a File by Hand](#saving-a-file-by-hand) just below for the click-by-click.
5. Repeat for every file — your assistant tells you when the set is complete, and finishes by printing your `REGISTRY.md` dashboard for you to save in your `ai-registry` folder, next to `registry/`.

#### Saving a File by Hand

Your assistant gives each file a **location** like `registry/businesses/your-business.md`. Read it left to right: inside your `ai-registry` folder, a folder called `registry`; inside that, a folder called `businesses`; inside that, a file named `your-business.md`.

**On GitHub:** open your repository, click **Add file → Create new file**, type the location exactly as given into the filename box (the slashes create the folders), paste the contents into the big box below, and click **Commit changes** — once to open the box, once to confirm. "Commit" just means save. When your assistant updates a file that already exists — it will, for the `index.md` inside `businesses/`, `workflows/`, and the other typed folders — click that file, click the pencil icon (**Edit this file**), select everything, paste the new contents, and commit the same way.

**On your computer or synced drive:** use the code editor from [AI Code Editor Setup](../editor-setup/) if you installed it — it saves plain text and shows file extensions, so the two traps below don't apply. Open your `ai-registry` folder in it, create the folders and the file at the location given, paste, save. Without a code editor, use TextEdit (Mac) or Notepad (Windows) and watch for two traps:

- **The file must be plain text.** In TextEdit choose **Format → Make Plain Text** before pasting, every time. Never paste a file into a Google Doc, Word, or Pages document — that turns a registry node into something your assistant can't read.
- **The name must end in `.md`, and your computer hides that.** When you save, type the full name including `.md`. On Windows, set **Save as type** to **All files** so Notepad doesn't add `.txt`. On Mac, if TextEdit asks whether to use `.txt` or `.md`, choose `.md`. To see extensions afterward: Finder → **Settings → Advanced → Show all filename extensions**; File Explorer → **View → Show → File name extensions**.

**You should now see** every file your assistant listed, at the location it gave. On GitHub, within a couple of minutes the **Actions** tab shows a green ✓ and your dashboard is live (see [Your Dashboard](#your-dashboard)); a red ✗ means one file broke a rule, usually a typo in a location — click the run, read the first red line, fix that file, and commit again. On your computer, you'll see `REGISTRY.md` next to `registry/` once you save the last file.

:::tip[Your assistant can't see what you saved]
Because your assistant didn't save the files itself, it can't check them. Compare each location against what it told you before you save. Later, when you ask for a refresh, your assistant can read your registry back only if you've connected GitHub, Google Drive, or OneDrive to your AI tool; otherwise, paste in the file it asks about. And every framework step you run later — Analyze, Deconstruct, and so on — ends the same way: with a file or two printed for you to save.
:::

### What GitHub Adds (Optional)

You never need GitHub for your registry. If you already use it, or want one of these, it's a good home:

- **Your assistant can read your registry back** through a GitHub connector instead of you pasting files in.
- **A built-in editor in your browser**, so you can save files without installing anything or worrying about file types.
- **Version history** of every change.
- **An automatic, always-current dashboard** — see [Optional: Let GitHub Build Your Dashboard](#optional-let-github-build-your-dashboard).

## The Interview

Whichever path you took, your assistant now runs the same **interview — seven phases, numbered 0–6** — about 30 minutes, working through your real business one piece at a time. It never invents details: if you don't know an answer yet, say so, and your assistant leaves that node partial rather than guessing.

| Phase | What it asks | Time |
|---|---|---|
| 0. Home | Where your registry will live (covered above) | 2 min |
| 1. Business | Your business's name and a one-sentence identity | 3 min |
| 2. Lines of Business | The one or more lines of business inside it (solo founders usually get just one, named after the business itself) | 4 min |
| 3. Functions | Which functions run your business — your assistant offers a starter list (Marketing, Sales, Service Delivery, Operations, Product, Customer Success, IT/Engineering) and you trim or rename it | 3 min |
| 4. Processes | The two or three highest-value processes per line of business — not an exhaustive list, just where AI could help most right now | 8 min |
| 5. First Workflow | One real workflow, written out in full — the one you'll carry through the rest of the [AI Workflow Framework](../../ai-workflow-framework/) | 7 min |
| 6. Close | An optional note if something worth recording came up, plus a wrap-up summary | 3 min |

While it interviews you, your assistant may show you a worked example from a fictional small consultancy to illustrate the shape of a good answer. That example is there to show you the *pattern* — it is never copied into your registry. Everything your assistant writes describes your real business.

**You should now see**, at the end of the interview, at least one Business node, one Line of Business node, one Function node, one Process node, and one Workflow node — plus a fresh `REGISTRY.md` summarizing all of it (at your workspace root on Paths A and B; at your GitHub Pages address on Path C, a couple of minutes after your last commit).

## A Workflow Node

Every workflow you run gets one Workflow node — a single Markdown file in `registry/workflows/`. This is the one node shape you'll see everywhere in this playbook; the framework's worked examples and course materials all use this exact same shape. Here's a complete example, from a small design studio:

```markdown
---
type: Workflow
title: "Client Onboarding Kickoff"
description: "Kestrel Studio's in-production client onboarding workflow — from signed contract to kickoff call scheduled."
generated: { by: process:run, at: 2026-06-01 }
status: in-production
definition_type: step-driven
execution_mode: augmented
autonomy: guided
trigger: "manual"
stale_after: 2026-12-01
---
# Client Onboarding Kickoff

Runs every time a new client signs a contract. Confirms contract details,
provisions the client's shared folder, and schedules the kickoff call.

# Artifacts

- [Requirements](outputs/client-onboarding-kickoff/requirements.md)
- [Design spec](outputs/client-onboarding-kickoff/design-spec.md)
- [SOP](sops/client-onboarding-kickoff.md)
- [Run guide](outputs/client-onboarding-kickoff/run-guide.md)

# Skills

- [drafting-kickoff-email](.claude/skills/drafting-kickoff-email/SKILL.md)

# Agents

- [contract-details-checker](.claude/agents/contract-details-checker.md)
```

Everything above the second `---` is **frontmatter** — structured fields your assistant reads and writes. Everything below is prose and links you (and your assistant) can read normally.

The `generated: { by: ..., at: ... }` line appears on every node your assistant writes — it records which process wrote the file and when, so you always know a node's provenance without asking.

### The Four Enums

An **enum** (short for "enumeration") is just a field that only accepts one of a fixed list of values — never free text. Four frontmatter fields on a Workflow node only ever take one of a fixed set of values. Your assistant validates against this list every time it writes or checks a node — these are exactly the values you'll ever see:

| Field | Allowed values |
|---|---|
| `status` | `backlog` \| `under-development` \| `in-production` \| `retired` |
| `definition_type` | `step-driven` \| `goal-driven` |
| `execution_mode` | `manual` \| `augmented` \| `automated` |
| `autonomy` | `deterministic` \| `guided` \| `autonomous` |

:::note[Older spellings still read fine]
Earlier versions of this playbook used `step-decomposed` and `outcome-driven` instead of `step-driven` and `goal-driven`. Your assistant tolerates reading either spelling in an old node, but it only ever writes the current ones (`step-driven`, `goal-driven`) going forward.
:::

The bundle root (`registry/index.md`) also declares one frontmatter field of its own: `okf_version: "0.2"`, the version of the OKF spec your registry follows. You'll never need to change it by hand.

## Keeping It Fresh

You almost never trigger a registry refresh yourself — the [AI Workflow Framework](../../ai-workflow-framework/) does it for you automatically:

- Every framework step (Analyze through Improve) updates the Workflow node it just touched, then refreshes your dashboards as its last action.
- Running the interview again on an existing registry fills in whatever's missing — it never re-runs from scratch or overwrites a node you've already filled in.

You only need to ask for a refresh yourself when you've added a skill, agent, or workflow **outside** the framework, or a dashboard looks stale or wrong. Either way, just say:

> "Update my AI registry."

Your assistant re-reads every node in `registry/`, checks it against `registry/SCHEMA.md`, fixes what it can, tells you plainly about anything it can't (for example, a broken link to a file that no longer exists), and regenerates your dashboards from scratch. Because dashboards are always regenerated rather than edited, it's completely safe to ask for a refresh at any time — you never lose anything by doing it.

**On Path C** (browser only), GitHub does the refresh for you: every time you save a file in `registry/`, it re-checks every node and republishes your dashboards within a couple of minutes — nothing to ask for. Your assistant can only re-read your nodes if your AI tool has a GitHub connector pointed at your repository; without one, paste in the file it asks about.

## Your Dashboard

"Dashboard" always means a **generated view** — never a place you type into directly. Your registry produces up to three, in increasing order of setup:

**Tier 1 — `REGISTRY.md`.** Plain Markdown, and the one every workspace gets automatically. Opening it, you'll see your business name and identity at the top, then a section per line of business, each with a table of its processes and the workflows inside them — status, execution mode, autonomy, and review date at a glance. Below that, a "Review dates" section lists every workflow with a `stale_after` date, soonest first, so you can see what needs a look. A "Skills" and "Agents" section lists everything you've built, each with a note on which workflow uses it (or a flag if nothing does — a good sign something got built but never wired in). This file lives at your workspace root and updates every time your assistant runs a maintenance pass. (If GitHub builds your dashboard — see below — it publishes this file at `https://<your-username>.github.io/<your-repo-name>/REGISTRY.md`.)

**Tier 2 — `registry-dashboard.html`.** An optional, richer visual view of the same data — clickable, with your business's full value chain (business → line of business → process → workflow) laid out visually, and a click-through to any node's detail. It's a single self-contained file: no server, no external requests, opens straight in a browser from your own computer. Ask your assistant: *"Generate my visual dashboard"* to produce it. On Claude Code or Cowork, your assistant can also publish it as a shareable Artifact.

**Tier 3 — Published to GitHub Pages.** Only for registries that live in a GitHub repository created from the template, below. GitHub re-checks every node and republishes both the Tier 1 and Tier 2 dashboards every time you save a file — nothing to ask for.

### Optional: Let GitHub Build Your Dashboard

The **AI Registry template repository** is a ready-made GitHub repository containing the empty registry skeleton plus an automated check-and-publish step. Start from it if your registry will live on GitHub and you want the dashboard built for you. You never run anything yourself. (No GitHub account? The same page's **Code → Download ZIP** button gives you the skeleton alone — see [You Save the Files](#you-save-the-files).)

**One-time setup, about 3 minutes, all in your browser.** You need a [GitHub account](../github-setup/).

1. Open [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template).
2. Click the green **Use this template** button, then **Create a new repository**. Give it a name — for example, `my-ai-registry` — choose **Public**, and click **Create repository**.
3. In your new repository, click **Settings** (the tab across the top), then **Pages** in the left sidebar. Under **Build and deployment → Source**, choose **GitHub Actions**.

Then set up your registry in that repository, using whichever flow fits your tool in [Where Your Registry Lives](#where-your-registry-lives): if your assistant saves files, download a copy of the repository to your computer first (see [Create & Clone Your First Repository](../repo-creation-and-cloning/)) and open that folder; if it doesn't, save each file on github.com. After each save, the **Actions** tab shows a green ✓ within a couple of minutes, and your dashboards are live at `https://<your-username>.github.io/<your-repo-name>/` — the visual dashboard at that address and `REGISTRY.md` at `.../REGISTRY.md`.

:::note[Public repository, public dashboard]
On a free GitHub account, GitHub Pages only works on a **public** repository, and the dashboard address is visible to anyone who has it. Your registry describes your business in general terms — names of processes and workflows, not client data — but if you'd rather keep it private, choose **Private** in step 2 and skip step 3. You still get your registry; ask your assistant for `REGISTRY.md` whenever you want the dashboard refreshed.
:::

## Platform Notes

The interview, the node shapes, and the dashboards are the same on every AI tool. What differs is only where the skill comes from and how files get written — the table is a summary; the paths above are the instructions.

| Platform | Skills come from | Where your registry lives | How files get written |
|---|---|---|---|
| Claude Code | Hands-on AI plugin | a folder on your computer (a cloned repo) | directly — ask your assistant to commit and push when you want it backed up to GitHub |
| Cowork | Hands-on AI plugin (same install as Claude Chat) | a folder on your computer, opened as a project | directly |
| ChatGPT desktop (Codex tab) | Hands-on AI plugin, or skill folders in `~/.agents/skills/` | a folder on your computer (a cloned repo) | directly — ask your assistant to commit and push when you want it backed up to GitHub |
| Cursor, Codex CLI, Gemini CLI | skill folders in `.agents/skills/` | a folder on your computer | directly — ask your assistant to commit and push when you want it backed up to GitHub |
| claude.ai · ChatGPT web · Google Gemini · M365 Copilot | Hands-on AI plugin (Claude, ChatGPT) or uploaded skill ZIPs | your GitHub repository | you save each file on github.com — [Path C](#path-c-browser-only--save-the-files-on-githubcom) |

A few tool-specific details:

- **Claude Code:** `/plugin list` shows `handsonai` once the plugin is installed, and `/handsonai:scaffolding-registry` starts the interview directly if you'd rather use the slash command.
- **Cowork:** open your repository folder as a Cowork project *before* saying "set up my AI registry" — the skill can only write inside the project you have open. Your visual dashboard can also be published as a shareable Claude Artifact.
- **ChatGPT desktop:** the plugin's skills work in the Codex tab. If you installed skill folders by hand instead, `~/.agents/skills/` makes them available in every repository; see [Set Up the Skills — Codex](../../ai-workflow-framework/skills/#openai-codex).
- **Browser tools (claude.ai, ChatGPT web, Gemini, Copilot):** your assistant should print each file's complete contents and exact path. If it says "I've created your registry" without showing you any files, reply: *"Nothing was saved — print each file in full with its path."*

If a button or label on your screen doesn't match these steps, paste the step you're on into your AI assistant and ask it to walk you through it on your version. Still stuck? Bring it to a session.

## Migrating From the Old Workflow Manifest File

Earlier versions of this playbook tracked each workflow with one small file per workflow (a "workflow manifest file") instead of today's registry bundle. If your assistant finds one of these old-style files in your workspace, it offers to migrate it as part of [Path B](#path-b-add-a-registry-to-an-existing-workspace) or [Path A](#path-a-start-from-the-template-repo)'s setup — you don't need to do anything by hand.

**What your assistant does during migration:**

- Creates a proper Workflow node in `registry/workflows/` from the old file's contents, converting old field names to the current ones (for example, the old file's status values become the current `status` enum — `Archived` becomes `retired`).
- Carries over the old outcome description into the new node's `description` field, so nothing you wrote is lost.
- Converts the old review-date field into the current `stale_after` field.
- Drops fields that no longer belong in a node at all — things like which platform a workflow ran on, or its last-run timestamp, which now live with the workflow's actual run history instead of in the registry.
- Records the migration in `registry/log.md`, so there's a permanent note of what was converted and when.

**What to check after migration:**

- Open the new Workflow node and confirm the description still reads correctly — migration preserves the words, but it's worth a skim.
- Confirm the workflow appears correctly in your Process node's workflow list, and that its status matches what you expect.
- If you had several old-style files, ask your assistant to confirm all of them were migrated — check `registry/log.md` for the full list.

## Troubleshooting

**"My registry wasn't found" / `registry/` doesn't exist:**

- Make sure you're working inside your actual workspace folder — your assistant can only write where it has file access.
- Ask directly: *"Set up my AI registry"* — this is safe to run even if a partial registry already exists; it fills in only what's missing.

**My assistant reported lint errors:**

- Lint errors mean something in a node breaks a rule in `registry/SCHEMA.md` — for example, a link pointing to a file that doesn't exist, or a status value that isn't one of the four allowed ones. Your assistant explains each error in plain language and the exact file it's in; ask it to fix what it can, and address anything it can't (usually because it needs a decision only you can make, like which function owns a new process).
- Dashboards won't regenerate while lint errors exist — this is deliberate, so you're never looking at a dashboard summarizing broken data. Fix the errors first, then ask for a refresh.

**My dashboard looks stale or wrong:**

- Dashboards are always regenerated, never hand-edited — ask *"update my AI registry"* and your assistant rebuilds every dashboard from your current nodes. If the dashboard is still wrong afterward, the problem is in a node, not the dashboard; ask your assistant which node the stale information is coming from.

**My GitHub Pages dashboard (Tier 3) isn't publishing:**

- This tier only applies if you started from the template repo (Path A or C) — registries added to an existing workspace don't have it unless you set it up separately.
- Confirm GitHub Pages is turned on for your repository (**Settings → Pages → Source → GitHub Actions** in your repo on github.com) — it's off by default until you enable it.
- Check the **Actions** tab in your repository for a failed run — Actions is the tab on your repository's GitHub page that lists every automated run; a red ✗ next to a run means it failed. Click that run and read the first red line for the reason. A broken node (one with a lint error) blocks publishing on purpose, the same way it blocks a local dashboard refresh. The failure message names the file and the rule it broke.

## Next Steps

- **Find AI opportunities** — Use the [Analyze](../../ai-workflow-framework/analyze/) guide to identify where AI can add value
- **Deconstruct your first workflow** — Follow the [Deconstruct](../../ai-workflow-framework/deconstruct/) guide; your registry updates itself as you go
- **Document workflows** — Ask your assistant to write SOPs (`writing-workflow-sops`) and process guides (`writing-process-guides`)
- **Explore the plugin** — See the [Hands-on AI plugin page](../../use-the-playbook/build/) for all registry-related skills
