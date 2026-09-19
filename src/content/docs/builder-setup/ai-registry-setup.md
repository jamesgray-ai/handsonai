---
title: AI Registry Setup
description: Set up your AI Registry — a Markdown knowledge bundle that tracks your workflows, skills, agents, and business context — no external tools required
schema_type: HowTo
howto_steps:
  - name: Choose your registry's home
    text: Pick the path for your AI tool — the template repo or an existing workspace if your tool edits files directly, or the browser-only path if it hands you files to save on github.com.
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

Your registry is a **knowledge bundle**: a folder of small Markdown files, each describing one real thing about your business — your company, a line of business, a function like Sales or Operations, a process, or a workflow. Every file is called a **node**. Your AI assistant writes and maintains these files; you almost never open a text editor to hand-edit one.

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
2. **A place for your registry to live.** Ideally a GitHub repository (a [GitHub account](../github-setup/) is all you need for the browser-only path below), but any folder on your computer works if your AI tool can edit files there.

## Which Path Is Yours?

The interview your assistant runs, the files it produces, and the dashboards it generates are identical on every AI tool. The **only** thing that differs is whether your AI tool can save files for you, or hands you the files to save yourself:

| If you use… | Your AI tool can… | Follow |
|---|---|---|
| **Claude Code**, **Cowork** (the Cowork tab in the Claude app), **ChatGPT desktop** (the Codex tab), **Cursor**, **Codex CLI**, or **Gemini CLI** | Edit files in a folder on your computer directly | [Path A](#path-a-start-from-the-template-repo) (fresh start) or [Path B](#path-b-add-a-registry-to-an-existing-workspace) (existing workspace) |
| **claude.ai**, **ChatGPT on the web**, **Google Gemini**, or **Microsoft 365 Copilot** | Generate each file in the chat for you to save | [Path C](#path-c-browser-only--save-the-files-on-githubcom) (browser only) |

Not sure which row you're in? Ask your AI tool: *"Can you create and edit files in a folder on my computer?"* Yes → Path A or B. No → Path C.

## Choose Your Home

Pick **one** path. Each is complete on its own — follow the one that matches your situation and skip the other two.

### Path A: Start From the Template Repo

Use this if your AI tool edits files directly and you don't have a workspace yet. This is the easiest path — the repository arrives with your registry's structure already in place.

1. Open the AI Registry template repository: [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template) (or ask your AI assistant: *"Where's the AI Registry template repo?"* — it knows this URL too).
2. Click the green **Use this template** button near the top of the page, then **Create a new repository**.
3. Give the new repository a name — for example, `my-ai-registry` — and click **Create repository**.
4. Clone your new repository to your computer — see the [Repository Creation and Cloning guide](../repo-creation-and-cloning/) if you haven't cloned a repo before.
5. Open the cloned folder in your AI tool:
   - **Claude Code:** in a terminal, `cd` into the folder and run `claude`
   - **Cowork:** open the folder as a project
   - **ChatGPT desktop:** open the folder in the **Codex** tab
   - **Cursor / Codex CLI / Gemini CLI:** open the folder as your project
6. Tell your assistant: *"Set up my AI registry."* This starts the interview in [The Interview](#the-interview) below.

**You should now see** a `registry/` folder already containing `SCHEMA.md`, `index.md`, and empty typed folders (`businesses/`, `workflows/`, and so on) — ready for the interview to fill in.

### Path B: Add a Registry to an Existing Workspace

Use this if your AI tool edits files directly and you already have a workspace or repository with skills, agents, or workflow outputs in it, and want to add a registry on top.

1. Open your existing workspace folder in your AI tool (see step 5 of Path A for how, per tool).
2. Tell your assistant: *"Set up my AI registry."*
3. Your assistant checks your workspace for anything to migrate — an older workflow manifest file or workflow folders without one. If it finds something, it offers to migrate it as part of the interview (see [Migrating from the Old Workflow Manifest File](#migrating-from-the-old-workflow-manifest-file) below). If it finds nothing to migrate, it starts the interview directly.
4. Work through the interview in [The Interview](#the-interview) below.

**You should now see** a new `registry/` folder appear at the root of your existing workspace, alongside your current `outputs/`, `sops/`, and `.claude/` folders — nothing already there is moved or deleted.

### Path C: Browser Only — Save the Files on github.com

Use this if you work in claude.ai, ChatGPT on the web, Google Gemini, or Microsoft 365 Copilot. These tools can't save files to your computer, so your assistant runs the same interview and prints each file for you to save on github.com — no terminal, nothing to install, and no cloning. GitHub then builds your dashboard for you automatically.

**One-time setup (about 3 minutes, all in your browser):**

1. Open the AI Registry template repository: [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template).
2. Click the green **Use this template** button, then **Create a new repository**. Give it a name — for example, `my-ai-registry` — choose **Public**, and click **Create repository**.
3. In your new repository, click **Settings** (the tab across the top), then **Pages** in the left sidebar. Under **Build and deployment → Source**, choose **GitHub Actions**. That's it — this tells GitHub to build your dashboard every time you save a registry file.

:::note[Public repository, public dashboard]
On a free GitHub account, the automatic dashboard (GitHub Pages) only works on a **public** repository, and the dashboard address is visible to anyone who has it. Your registry describes your business in general terms — names of processes and workflows, not client data — but if you'd rather keep it private, choose **Private** in step 2 and skip step 3. You still get your registry; just ask your assistant to print `REGISTRY.md` for you to save whenever you want the dashboard refreshed.
:::

**The interview:**

4. Start a conversation with your AI assistant and say: *"Set up my AI registry. I'm working in the browser and can't save files, so print the full contents of each file and tell me exactly where it goes."*
5. Your assistant runs the interview in [The Interview](#the-interview) below. Instead of saving files, it prints each file's complete contents and its exact path — for example, *"save this as `registry/businesses/your-business.md`."*
6. For each file, save it on github.com: open your repository, click **Add file → Create new file**, type the exact path your assistant gave you as the filename (typing `registry/businesses/your-business.md` creates the folders for you), paste the contents into the editor, and click **Commit changes** (twice — once to open the dialog, once to confirm).
7. Repeat for every file your assistant generates — it tells you when the set is complete.

**You should now see** every file your assistant listed present in your repository at the path it specified. Within a couple of minutes, the **Actions** tab shows a green ✓, and your dashboards are live at `https://<your-username>.github.io/<your-repo-name>/` — the visual dashboard at that address, and `REGISTRY.md` at `.../REGISTRY.md`. A red ✗ instead means one file broke a rule (usually a path typo or a mistyped field) — click the run, read the first red line, fix that file, and commit again.

:::tip[Your assistant can't see what you saved]
Because your assistant didn't save the files itself, it can't check them. Compare each path against what it told you before you commit. If your AI tool offers a GitHub connector, connecting it to this repository lets your assistant read your registry back when you update it later.
:::

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

**Tier 1 — `REGISTRY.md`.** Plain Markdown, and the one every workspace gets automatically. Opening it, you'll see your business name and identity at the top, then a section per line of business, each with a table of its processes and the workflows inside them — status, execution mode, autonomy, and review date at a glance. Below that, a "Review dates" section lists every workflow with a `stale_after` date, soonest first, so you can see what needs a look. A "Skills" and "Agents" section lists everything you've built, each with a note on which workflow uses it (or a flag if nothing does — a good sign something got built but never wired in). This file lives at your workspace root and updates every time your assistant runs a maintenance pass. (On [Path C](#path-c-browser-only--save-the-files-on-githubcom), GitHub generates it for you and publishes it at `https://<your-username>.github.io/<your-repo-name>/REGISTRY.md`.)

**Tier 2 — `registry-dashboard.html`.** An optional, richer visual view of the same data — clickable, with your business's full value chain (business → line of business → process → workflow) laid out visually, and a click-through to any node's detail. It's a single self-contained file: no server, no external requests, opens straight in a browser from your own computer. Ask your assistant: *"Generate my visual dashboard"* to produce it. On Claude Code or Cowork, your assistant can also publish it as a shareable Artifact.

**Tier 3 — Published to GitHub Pages.** If you started from the template repo (Path A or C above), it ships with an automated check-and-publish step that runs every time you push a change to your `registry/` folder — it regenerates both Tier 1 and Tier 2 and publishes the Tier 2 view to a public URL, with no need to run anything yourself. It's dormant until you turn on GitHub Pages for your repository — one time, in your browser: **Settings → Pages → Build and deployment → Source → GitHub Actions**. This tier only exists for the template-repo paths (A and C) — registries added to an existing workspace (Path B) stay at Tier 1 and 2 unless you set this up separately.

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
