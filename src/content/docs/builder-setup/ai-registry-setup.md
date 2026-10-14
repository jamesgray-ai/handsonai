---
title: AI Registry Setup
description: Set up your AI Registry — a Markdown knowledge bundle that tracks your workflows, skills, agents, and business context — no external tools required
schema_type: HowTo
howto_steps:
  - name: Pick a folder for your registry
    text: Any folder works — on your computer, in a cloud drive, or in a GitHub repository. Ask your AI tool whether it can create files inside that folder for you, or whether it will print each file for you to save.
  - name: Run the interview
    text: Answer the interview (about 25 minutes). Bring a services page, an org chart, or a strategy document if you have one and most of it becomes confirmation — your AI assistant drafts your Business, Line of Business, Function, and Process nodes for you to confirm.
  - name: Check your dashboard
    text: Open REGISTRY.md and confirm your processes are listed. Workflows arrive when you run Analyze — the registry starts with none.
  - name: Keep it fresh
    text: Ask your AI assistant to "update my registry" any time it looks stale, or let the framework refresh it automatically after each step.
---

Your **AI Registry** is your inventory of everything you build and run with AI: your business, its lines of business, the processes and workflows inside them, and the skills, agents, and apps those workflows use. It lives entirely in your workspace as Markdown files — no database, no external account, nothing extra to maintain.

New to Markdown? It's plain text with a few formatting marks — see [Markdown Basics](../markdown-basics/) for a ten-minute primer.

## What Your AI Registry Is

Your registry is a **knowledge bundle**: a folder of small Markdown files, each describing one real thing about your business — your company, a line of business, a function like Sales or Operations, a process, or a workflow. Every file is called a **node**. It works the same whether the "business" is a company you own, a unit you lead, the team you work in, or your personal life. Your AI assistant writes and maintains these files. If your AI tool can create files, you never touch them; if it can't, it prints each file and you save it — but you never have to *compose* one yourself.

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
├── framework/<workflow>/    ← each workflow's record: requirements, design spec, test results, run log
└── sops/ process-guides/    ← unchanged homes; Workflow nodes link to them
```

The registry lists your workflows; the files the framework writes for each one are in `framework/<workflow-name>/`. Whatever a workflow produces when it runs (a report, an email) goes wherever the workflow runs, not into either folder.

Your registry follows an open, public specification called the **Open Knowledge Format (OKF)** — this isn't a format James invented for this playbook. You can read the live spec any time: [OKF on GitHub](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). You never need to read it to use your registry — your assistant already knows it — but it's there if you're curious how the pieces fit together.

**The one thing to remember:** your AI assistant maintains your registry. You describe your business and your work in plain language; your assistant writes the nodes and regenerates the dashboards. You never edit a dashboard by hand, and you rarely need to hand-edit a node either.

## Before You Start

Two things, in this order:

1. **The Hands-on AI skills are in your AI tool.** Your registry is set up by a skill called `scaffolding-registry` and kept tidy by one called `indexing-registry`. If you installed the Hands-on AI **plugin** (Claude or ChatGPT), you already have both. If you added skills one at a time by uploading ZIP files (Gemini, Microsoft 365 Copilot, or a plan that blocks plugins), upload these two the same way you uploaded the others:
   - [scaffolding-registry.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/scaffolding-registry.zip) — sets up your registry
   - [indexing-registry.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/indexing-registry.zip) — keeps it tidy

   Haven't set up the skills yet? Follow [Install the Hands-on AI Plugin](../../ai-workflow-framework/skills/) for your tool — it has click-by-click steps for every platform — then come back here.
2. **A folder for your registry.** Any folder: on your computer, in a cloud drive such as Google Drive or OneDrive, or in a GitHub repository. You do not need GitHub — see [Where Your Registry Lives](#where-your-registry-lives).

## Where Your Registry Lives

Your registry is a folder of Markdown files, and it lives in your **working folder** — anywhere your AI can create and update files for you. That can be a folder on your computer, a folder in a cloud drive such as Google Drive or OneDrive, or a GitHub repository. GitHub is optional — it adds a few conveniences, listed at the end of this section, but nothing about your registry needs it.

The interview your assistant runs, the files it writes, and the dashboards it generates are identical everywhere. The **only** thing that differs is who saves the files. Ask your AI tool this exact question:

> "Can you create and edit files inside a folder I choose — on my computer or in my cloud drive — without me downloading anything?"

| Your AI tool says… | Typical tools | Follow |
|---|---|---|
| **Yes** | The Claude desktop app, Claude Code, ChatGPT for desktop (ChatGPT Work or Codex), Claude Code on the web or Codex with a GitHub repository, Cursor, Codex CLI, Gemini CLI | [Your assistant saves the files](#your-assistant-saves-the-files) |
| **No** | Claude on the web, ChatGPT on the web, Google Gemini, Microsoft 365 Copilot | [You save the files](#you-save-the-files) |

A downloadable file counts as "no" — if your tool offers you a file to download, it can't put it in your folder for you.

### Your Assistant Saves the Files

About 25 minutes, all of it the interview.

1. Pick the folder. **Not sure? Create a new empty folder called `ai-registry` inside your Documents folder** — that's the default. Two other options work just as well:
   - The folder on your computer you made in [Create & Clone Your First Repository](../repo-creation-and-cloning/), if you followed that guide.
   - A folder in your cloud drive, **as long as it also appears on your computer** — that means the Google Drive or OneDrive desktop app is installed and syncing. Your AI tool works on the copy on your computer; the app keeps the cloud copy current.
2. Open that folder in your AI tool:
   - **Claude Code:** open Terminal, type `cd ` (with a space after it), drag the folder from Finder or File Explorer into the Terminal window, press Enter, then type `claude` and press Enter. New to Terminal? See [Terminal Basics](../terminal-basics/).
   - **The Claude desktop app:** choose the folder as your working folder — a project or any folder on your computer. (Still see a Cowork tab? Cowork is merging into Claude; it's the same thing.)
   - **ChatGPT for desktop:** open the folder in **ChatGPT Work** or **Codex**. ChatGPT Work opens local folders only where your plan and workspace admin allow it; if yours doesn't, use Codex.
   - **Claude Code on the web or Codex in a browser:** work in a GitHub repository — the route when you can't save files on your computer.
   - **Cursor / Codex CLI / Gemini CLI:** open the folder as your project.
3. Say: *"Set up my AI registry."* This starts [The Interview](#the-interview) below.

**You should now see**, once the interview begins, a new `registry/` folder inside the folder you picked — look in Finder or File Explorer — containing `SCHEMA.md`, `index.md`, and empty typed folders (`businesses/`, `workflows/`, and so on). If the folder already had files in it — skills, agents, workflow outputs — nothing is moved or deleted. If your assistant finds files from an older version of this framework, it offers to migrate them first (see [Migrating From the Old Workflow Manifest File](#migrating-from-the-old-workflow-manifest-file)).

### You Save the Files

Your assistant runs the same interview, but instead of saving each file it prints the file's complete contents and tells you exactly where it goes — for example, *"save this as `registry/businesses/your-business.md`."* You save it. Nothing to install.

**Plan for about 50 minutes:** the 25-minute interview plus 20–30 minutes of saving. The interview produces roughly 14–17 files — your Business, Line of Business, Function, and Process nodes; the index.md for each of those directories plus the (empty) `workflows/` index; a `log.md`; and your `REGISTRY.md` dashboard — including updates to a few files it already gave you.

1. Decide where the files will go. **Easiest: a GitHub repository.** Typing a file's location creates its folders for you, and there's no way to save the wrong file type. Set one up in about three minutes, all in your browser (you need a [GitHub account](../github-setup/)):
   1. Open [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template) — a ready-made repository containing the empty registry skeleton.
   2. Click the green **Use this template** button, then **Create a new repository**. Give it a name — for example, `my-ai-registry` — choose **Private**, and click **Create repository**. Private means only you can see it.

   From now on, your repository checks your registry against its rules whenever you save a registry file. The **Actions** tab (across the top of your repository) shows a green ✓ when every file follows the rules, or a red ✗ — click it to see which file to fix. Nothing is published anywhere. While you're still saving your first set of files, a red ✗ is normal: a file can point to one you haven't saved yet, and GitHub may email you about it. Only the check after your last file counts.

   Two other options if you'd rather not use GitHub:
   - **A folder on your computer.** Create an empty folder called `ai-registry` inside your Documents folder.
   - **A folder in your cloud drive.** Only if the Google Drive or OneDrive desktop app is installed and syncing — then create the `ai-registry` folder inside your synced drive folder and treat it exactly like a folder on your computer. (The Drive and OneDrive *websites* can't create Markdown files, and re-uploading a changed file creates a duplicate.)
2. **If you chose your computer or cloud drive,** get the empty registry skeleton first, so you don't have to paste the long rules file by hand: open [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template), click the green **Code** button, then **Download ZIP**. No account needed. Unzip it and move the `registry` folder it contains into your `ai-registry` folder. (You can ignore the other folders in the download.) If you chose GitHub, your repository already has this skeleton.
3. Say: *"Set up my AI registry. You can't save files for me, so print the full contents of each file and tell me exactly where it goes. I already have the empty registry skeleton."*
4. Save each file where your assistant says — see [Saving a File by Hand](#saving-a-file-by-hand) just below for the click-by-click.
5. Repeat for every file — your assistant tells you when the set is complete, and finishes by printing your `REGISTRY.md` dashboard for you to save in your registry's folder (your repository, or the `ai-registry` folder you made), next to `registry/`.

#### Saving a File by Hand

Your assistant gives each file a **location** like `registry/businesses/your-business.md`. Read it left to right: inside your registry's folder (your repository, or the `ai-registry` folder you made), a folder called `registry`; inside that, a folder called `businesses`; inside that, a file named `your-business.md`.

**On GitHub:** open your repository, click **Add file → Create new file**, type the location exactly as given into the filename box (the slashes create the folders), paste the contents into the big box below, and click **Commit changes** — once to open the box, once to confirm. "Commit" just means save. When your assistant updates a file that already exists — it will, for the `index.md` inside `businesses/`, `workflows/`, and the other typed folders — click that file, click the pencil icon (**Edit this file**), select everything, paste the new contents, and commit the same way.

**On your computer or synced drive:** use the code editor from [AI Code Editor Setup](../editor-setup/) if you installed it — it saves plain text and shows file extensions, so the two traps below don't apply. Open your `ai-registry` folder in it, create the folders and the file at the location given, paste, save. Without a code editor, use TextEdit (Mac) or Notepad (Windows) and watch for two traps:

- **The file must be plain text.** In TextEdit choose **Format → Make Plain Text** before pasting, every time. Never paste a file into a Google Doc, Word, or Pages document — that turns a registry node into something your assistant can't read.
- **The name must end in `.md`, and your computer hides that.** When you save, type the full name including `.md`. On Windows, set **Save as type** to **All files** so Notepad doesn't add `.txt`. On Mac, if TextEdit asks whether to use `.txt` or `.md`, choose `.md`. To see extensions afterward: Finder → **Settings → Advanced → Show all filename extensions**; File Explorer → **View → Show → File name extensions**.

**You should now see** every file your assistant listed, at the location it gave. Once you save the last file, `REGISTRY.md` sits next to `registry/`. On GitHub, within a couple of minutes of your last save the **Actions** tab shows a green ✓. A red ✗ means a file broke a rule, usually a typo in a location: click the run, and the box under **Annotations** names the file and the rule. Fix that file and commit again.

:::tip[Your assistant can't see what you saved]
Because your assistant didn't save the files itself, it can't check them. Compare each location against what it told you before you save. Later, when you ask for a refresh, your assistant can read your registry back only if you've connected GitHub, Google Drive, or OneDrive to your AI tool; otherwise, paste in the file it asks about. And every framework step you run later — Analyze, Deconstruct, and so on — ends the same way: with a file or two printed for you to save.
:::

### What GitHub Adds (Optional)

You never need GitHub for your registry. If you already use it, or want one of these, it's a good home:

- **Your assistant can read your registry back** through a GitHub connector instead of you pasting files in.
- **A built-in editor in your browser**, so you can save files without installing anything or worrying about file types.
- **Version history** of every change.
- **An automatic check**, if you create your repository from the template, that tells you when a file breaks one of your registry's rules.

## What to Bring

The interview works from memory alone, but it is shorter and more accurate if you bring something that already describes your business. Any of these, pasted or attached when your assistant asks:

- **Something that lists what you offer** — a services page, a product list, a capabilities deck.
- **Something that shows who does the work** — an org chart, a team list, job descriptions. Role titles are enough; your assistant uses roles, not names, unless you ask.
- **Something that says what matters this year** — a strategy page, OKRs, an annual plan.
- **Optional:** a process inventory, an SOP folder, or process guides.

Bring one and the interview is shorter. Bring three and it is mostly confirmation. If you lead a company, the org chart and the annual plan do most of the work; if you work inside one, bring your team's charter and your job description; if this registry is for your personal life, a two-minute list of the areas you want to run better is all you need.

## The Interview

Whichever flow you're in, your assistant now runs the same **interview** — about 25 minutes: a short setup, **four parts**, and a close — working through your real business one piece at a time. It never invents details: if you don't know an answer yet, say so, and your assistant leaves that node partial rather than guessing.

| Part | What it asks | Time |
|---|---|---|
| Setup | Tells you where it will save your registry and whether your assistant saves files or prints them (decided above), asks who the registry is for — a business you own, a company you lead, your role, or your personal life — and asks for anything you brought (see What to Bring) | 4 min |
| Part 1 — Your business | Your business's name, a one-sentence identity, and the two or three outcomes that matter most this year. For a professional the "business" is your team; for personal life it is you or your household | 3 min |
| Part 2 — How it's organized | The one or more lines of business inside it (solo founders usually get just one, named after the business itself) | 4 min |
| Part 3 — Who does the work | Which functions run your business — for a company, your assistant offers a starter list (Marketing, Sales, Service Delivery, Operations, Product, Customer Success, IT/Engineering) or drafts from your org chart, and you trim or rename it (any function left owning no process is added to one or dropped before you finish); for a team, the groups you hand work to; for personal life, the roles that own each routine | 3 min |
| Part 4 — The processes that deliver it | The three to five processes that deliver each line of business — where the time, money, and customer outcomes flow. Your assistant drafts and orders them; you add, remove, rename, or move. Not where AI helps: Analyze decides that, and asks which processes matter most before it looks at them | 8 min |
| Close | A wrap-up summary, your visual dashboard (always generated, with how to open it — if your assistant is printing files, it's created once your files are in a folder it can save to), and the offer to run Analyze right away | 3 min |

While it interviews you, your assistant may show you a worked example from a fictional small consultancy to illustrate the shape of a good answer. That example is there to show you the *pattern* — it is never copied into your registry. Everything your assistant writes describes your real business.

**You should now see**, at the end of the interview, at least one Business node, one Line of Business node, one Function node, and one Process node — and an empty Workflows table. [Analyze](../../ai-workflow-framework/analyze/) fills that table, and a fresh `REGISTRY.md` summarizes all of it (in the folder you picked, next to `registry/`).

## A Workflow Node

Every workflow the framework finds or builds gets one Workflow node — Analyze writes the first ones into your backlog. This is the one node shape you'll see everywhere in this playbook; the framework's worked examples and course materials all use this exact same shape. Here's a complete example, from a small design studio:

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

- [Requirements](framework/client-onboarding-kickoff/requirements.md)
- [Design spec](framework/client-onboarding-kickoff/design-spec.md)
- [SOP](sops/client-onboarding-kickoff.md)
- [Run guide](framework/client-onboarding-kickoff/run-guide.md)

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

Your assistant re-reads every node in `registry/`, checks it against `registry/SCHEMA.md`, offers to fix what it can (and fixes it once you say yes), tells you plainly about anything it can't (for example, a broken link to a file that no longer exists), and regenerates your dashboards from scratch. Because dashboards are always regenerated rather than edited, it's completely safe to ask for a refresh at any time — you never lose anything by doing it.

**If you save the files yourself,** every refresh and every framework step ends with a file or two printed for you to save — the same routine as setup. Your assistant can re-read your nodes only if you've connected GitHub, Google Drive, or OneDrive to your AI tool; otherwise, paste in the file it asks about.

## Your Dashboard

"Dashboard" always means a **generated view** — never a place you type into directly. Your assistant produces two files from your nodes, and both live in the folder you picked, next to `registry/`:

**`registry-dashboard.html` — your visual dashboard.** This is the one you'll open most. It's a single self-contained web page — no server, no external requests, double-click it and it opens in your browser — showing your business's full value chain (business → line of business → process → workflow) laid out visually, with a click-through to any node's detail. Ask your assistant: *"Generate my visual dashboard."* On Claude, registry setup also offers it as a **Claude Artifact**: a private page you can open from Claude any time, without finding the file. Each later step updates it at the same link. To show it to someone else, see [Sharing Your Dashboard](#sharing-your-dashboard).

**`REGISTRY.md` — the plain-text index.** Regenerated automatically on every maintenance pass. Opening it, you'll see your business name and identity at the top, then a section per line of business, each with a table of its processes and the workflows inside them — status, execution mode, autonomy, and review date at a glance. Below that, a "Review dates" section lists every workflow with a `stale_after` date, soonest first, and "Skills" and "Agents" sections list everything you've built, each with a note on which workflow uses it (or a flag if nothing does — a good sign something got built but never wired in). It's the version your assistant reads back and the one that works anywhere Markdown does.

### Sharing Your Dashboard

Your dashboard is for you; you never need to publish it. If someone else should see it:

- **On Claude** (the web, the desktop app, or Claude Code), ask your assistant to *"save my dashboard as an Artifact"*. Then use the Artifact's share option to get a link, and send that link. Each later framework step updates it at the same link, so the link you sent stays current.
- **Anywhere else**, send them `registry-dashboard.html`. It's a single file that opens in any web browser.

## Platform Notes

The interview, the node shapes, and the dashboards are the same on every AI tool. What differs is only where the skill comes from and how files get written — the table is a summary; the paths above are the instructions.

| Platform | Skills come from | Where your registry lives | How files get written |
|---|---|---|---|
| Claude Code | Hands-on AI plugin | any folder on your computer | directly — if it's a Git repository, ask your assistant to commit and push when you want it backed up to GitHub |
| Claude desktop app | Hands-on AI plugin | any folder on your computer, chosen as your working folder | directly |
| ChatGPT for desktop (ChatGPT Work or Codex) | Hands-on AI plugin, or skill folders in `~/.agents/skills/` | any folder on your computer | directly — if it's a Git repository, ask your assistant to commit and push when you want it backed up to GitHub |
| Cursor, Codex CLI, Gemini CLI | skill folders in `.agents/skills/` | any folder on your computer | directly — if it's a Git repository, ask your assistant to commit and push when you want it backed up to GitHub |
| Claude on the web · ChatGPT web · Google Gemini · M365 Copilot | Hands-on AI plugin (Claude, ChatGPT) or uploaded skill ZIPs | a folder on your computer, a synced cloud-drive folder, or a GitHub repository | you save each file — [You save the files](#you-save-the-files) |

A few tool-specific details:

- **Claude Code:** `/plugin list` shows `handsonai` once the plugin is installed, and `/handsonai:scaffolding-registry` starts the interview directly if you'd rather use the slash command.
- **The Claude desktop app:** choose your registry's folder as your working folder — a project or any local folder — *before* saying "set up my AI registry"; the skill can only write inside the folder you're working in.
- **ChatGPT for desktop:** the plugin's skills work in ChatGPT Work and Codex. If you installed skill folders by hand instead, `~/.agents/skills/` makes them available in every repository; see [Install the Hands-on AI Plugin — Codex](../../ai-workflow-framework/skills/#openai-codex).
- **Browser tools (Claude on the web, ChatGPT web, Gemini, Copilot):** your assistant should print each file's complete contents and exact path. If it says "I've created your registry" without showing you any files, reply: *"Nothing was saved — print each file in full with its path."*

If a button or label on your screen doesn't match these steps, paste the step you're on into your AI assistant and ask it to walk you through it on your version. Still stuck? Bring it to a session.

## Migrating From the Old Workflow Manifest File

Earlier versions of this playbook tracked each workflow with one small file per workflow (a "workflow manifest file") instead of today's registry bundle. If your assistant finds one of these old-style files in your workspace, it offers to migrate it as part of setup (see [Your Assistant Saves the Files](#your-assistant-saves-the-files)) — you don't need to do anything by hand. If you save files yourself, tell your assistant what's in your `outputs/` folder when it asks: the old manifest files lived there, in the layout from before 9.0. It can't look for itself.

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

- If your assistant saves files: make sure the folder you opened in your AI tool is the one that holds `registry/`. If you save files yourself: your assistant can't see your folder — paste in `registry/index.md` when it asks, or tell it which files you've saved.
- Ask directly: *"Set up my AI registry"* — this is safe to run even if a partial registry already exists; it fills in only what's missing.

**My assistant reported lint errors:**

- Lint errors mean something in a node breaks a rule in `registry/SCHEMA.md` — for example, a link pointing to a file that doesn't exist, or a status value that isn't one of the four allowed ones. Your assistant explains each error in plain language and the exact file it's in; ask it to fix what it can, and address anything it can't (usually because it needs a decision only you can make, like which function owns a new process).
- Dashboards won't regenerate while lint errors exist — this is deliberate, so you're never looking at a dashboard summarizing broken data. Fix the errors first, then ask for a refresh.

**My dashboard looks stale or wrong:**

- Dashboards are always regenerated, never hand-edited — ask *"update my AI registry"* and your assistant rebuilds every dashboard from your current nodes. If the dashboard is still wrong afterward, the problem is in a node, not the dashboard; ask your assistant which node the stale information is coming from.

**GitHub shows a red ✗ on my repository:**

- This only applies if your registry lives in a GitHub repository created from the template. Each time you save a registry file, GitHub checks your registry against its rules.
- While you're still saving your first set of files, a red ✗ is normal — a file can point to one you haven't saved yet. Only the check after your last file counts.
- Click the **Actions** tab (across the top of your repository), then the run with the red ✗. The box under **Annotations** names the file and the rule it broke. (No **Annotations** box? Your copy of the template's tools is older: click the job in the left sidebar, then the step with the red ✗, and look for lines that start with `ERROR`.)
- Copy that error into your AI assistant and say *"Update my AI registry."* It offers fixes for what it can and tells you about anything it can't; if it asks, paste in the file the error names.

## Next Steps

- **Find your first workflows** — the interview ends by offering to run [Analyze](../../ai-workflow-framework/analyze/) right away; it walks the processes you just captured asking where the friction is, and adds your candidates to the registry
- **Document workflows** — Ask your assistant to write SOPs (`writing-workflow-sops`) and process guides (`writing-process-guides`)
- **Explore the plugin** — See the [Hands-on AI plugin page](../../use-the-playbook/build/) for all registry-related skills
