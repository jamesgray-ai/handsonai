---
title: AI Registry Setup
description: Set up your AI Registry — a Markdown knowledge bundle that tracks your workflows, skills, agents, and business context — no external tools required
schema_type: HowTo
howto_steps:
  - name: Choose your registry's home
    text: Pick a template repo, an existing workspace, or a no-repo cloud path as the home for your AI Registry bundle.
  - name: Run the interview
    text: Answer the interview (about 30 minutes) — your AI assistant writes your Business, Line of Business, Function, Process, and first Workflow nodes as you go.
  - name: Review your first Workflow node
    text: Open the Workflow node your assistant wrote in registry/workflows/ and confirm it matches your real work.
  - name: Keep it fresh
    text: Ask your AI assistant to "update my registry" any time it looks stale, or let the framework refresh it automatically after each step.
---Your **AI Registry** is your inventory of everything you build and run with AI: your business, its lines of business, the processes and workflows inside them, and the skills, agents, and apps those workflows use. It lives entirely in your workspace as Markdown files — no database, no external account, nothing extra to maintain.

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

## Prerequisites

- A folder for your AI work — ideally a GitHub repository (see [Git](../git-install/) and [GitHub](../github-setup/) setup), but any folder works
- Claude with the [Hands-on AI plugin](../../use-the-playbook/build/) installed (Claude Code or Cowork), or the individual framework skills added to your AI assistant another way — see [Platform Guide](#platform-guide) below

## Choose Your Home

Pick **one** of these three paths. Each is complete on its own — follow the one that matches your situation and skip the other two.

### Path A: Start From the Template Repo

Use this if you're starting fresh and don't have a workspace yet. This is the easiest path — it arrives with your registry's structure already in place.

1. Open the AI Registry template repository: [github.com/jamesgray-ai/ai-registry-template](https://github.com/jamesgray-ai/ai-registry-template) (or ask your AI assistant: *"Where's the AI Registry template repo?"* — it knows this URL too).
2. Click the green **Use this template** button near the top of the page, then **Create a new repository**.
3. Give the new repository a name — for example, `my-ai-registry` — and click **Create repository**.
4. Clone your new repository to your computer (see the [GitHub setup guide](../github-setup/) if you haven't cloned a repo before), or open it directly in Cowork.
5. Open the cloned folder in your AI assistant (Claude Code: `cd` into the folder and run `claude`; Cowork: open the folder as a project).
6. Tell your assistant: *"Set up my AI registry."* This starts the interview in [The Interview](#the-interview) below.

**You should now see** a `registry/` folder already containing `SCHEMA.md`, `index.md`, and empty typed folders (`businesses/`, `workflows/`, and so on) — ready for the interview to fill in.

### Path B: Add a Registry to an Existing Workspace

Use this if you already have a workspace or repository with skills, agents, or workflow outputs in it, and want to add a registry on top.

1. Open your existing workspace folder in your AI assistant (Claude Code or Cowork).
2. Tell your assistant: *"Set up my AI registry."*
3. Your assistant checks your workspace for anything to migrate — an older workflow manifest file or workflow folders without one. If it finds something, it offers to migrate it as part of the interview (see [Migrating from the Old Workflow Manifest File](#migrating-from-the-old-workflow-manifest-file) below). If it finds nothing to migrate, it starts the interview directly.
4. Work through the interview in [The Interview](#the-interview) below.

**You should now see** a new `registry/` folder appear at the root of your existing workspace, alongside your current `outputs/`, `sops/`, and `.claude/` folders — nothing already there is moved or deleted.

### Path C: No Repository — Generate and Commit From the Cloud

Use this if you're working in claude.ai, ChatGPT web, or M365 Copilot without a local clone of your workspace — these tools can't write directly to your files, so your assistant generates the registry content in the conversation and you save it yourself.

1. Start a conversation with your AI assistant and say: *"Set up my AI registry — I don't have a local workspace, generate the files for me."*
2. Your assistant runs the same interview as the other two paths (see [The Interview](#the-interview)), but instead of writing files directly, it prints each file's full contents in the chat and tells you exactly where it belongs — for example, "save this as `registry/businesses/your-business.md`."
3. For each file your assistant gives you, create it in your GitHub repository: open the repository on github.com, click **Add file → Create new file**, paste in the exact path your assistant gave you (e.g. `registry/businesses/your-business.md`) as the filename, paste the content, and commit.
4. Repeat for every file your assistant generated — it will tell you when the set is complete.
5. Once every file is committed, tell your assistant: *"I've committed all the files — regenerate my dashboard."* It reads what you just committed (via your GitHub connector, if one is set up) and produces the index.

**You should now see** every file your assistant listed present in your GitHub repository at the paths it specified, and a confirmation from your assistant that your dashboard reflects them. Because your assistant cannot verify a commit it didn't make itself, always double check that the file paths match exactly what it told you.

## The Interview

However you got here, your assistant now runs the same **interview — seven phases (0–6)** — about 30 minutes, working through your real business one piece at a time. It never invents details: if you don't know an answer yet, say so, and your assistant leaves that node partial rather than guessing.

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

**You should now see**, at the end of the interview, at least one Business node, one Line of Business node, one Function node, one Process node, and one Workflow node — plus a fresh `REGISTRY.md` at your workspace root summarizing all of it.

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

## Your Dashboard

"Dashboard" always means a **generated view** — never a place you type into directly. Your registry produces up to three, in increasing order of setup:

**Tier 1 — `REGISTRY.md`.** Plain Markdown, and the one every workspace gets automatically. Opening it, you'll see your business name and identity at the top, then a section per line of business, each with a table of its processes and the workflows inside them — status, execution mode, autonomy, and review date at a glance. Below that, a "Review dates" section lists every workflow with a `stale_after` date, soonest first, so you can see what needs a look. A "Skills" and "Agents" section lists everything you've built, each with a note on which workflow uses it (or a flag if nothing does — a good sign something got built but never wired in). This file lives at your workspace root and updates every time your assistant runs a maintenance pass.

**Tier 2 — `registry-dashboard.html`.** An optional, richer visual view of the same data — clickable, with your business's full value chain (business → line of business → process → workflow) laid out visually, and a click-through to any node's detail. It's a single self-contained file: no server, no external requests, opens straight in a browser from your own computer. Ask your assistant: *"Generate my visual dashboard"* to produce it. On Claude Code or Cowork, your assistant can also publish it as a shareable Artifact.

**Tier 3 — Published to GitHub Pages.** If you started from the template repo (Path A above), it ships with an automated check-and-publish step that runs every time you push a change to your `registry/` folder — it regenerates both Tier 1 and Tier 2 and publishes the Tier 2 view to a public URL, with no need to run anything yourself. It's dormant until you turn on GitHub Pages for your repository (your template repo's README covers the one-time toggle). This tier only exists for the template-repo path — registries added to an existing workspace (Path B) stay at Tier 1 and 2 unless you set this up separately.

## Platform Guide

*Platform instructions are re-verified at every release — see the project's platform verification checklist.*

The interview, the node shapes, and the dashboards are identical everywhere — what differs by platform is how the skill that runs your interview gets installed, and how it writes bytes to your files.

| Platform | Skill delivery | Where your registry lives | How writes happen |
|---|---|---|---|
| Claude Code | Hands-on AI plugin | local clone on your computer | direct edits; you commit and push |
| Cowork | Hands-on AI plugin via the marketplace | your repo folder opened as a project | direct edits |
| ChatGPT desktop (Codex) | same skill files, installed once for your user account | local clone on your computer | direct edits; you commit and push |
| claude.ai | uploaded skill file | your GitHub repo, connected or generate-and-commit | generate-and-commit — see below |
| ChatGPT web (Business/Enterprise) | uploaded Personal Skill | your GitHub repo via connector | generate-and-commit — see below |
| M365 Copilot | packaged agent instructions | SharePoint or your GitHub repo | generate-and-commit — see below |

Each platform section below is complete on its own — you only need to read the one for the platform you're using.

### Claude Code

1. Install the Hands-on AI plugin: `/plugin marketplace add jamesgray-ai/handsonai-plugins`, then `/plugin install handsonai@handsonai`. See the [plugin marketplace page](../../use-the-playbook/build/) if you haven't installed a plugin before.
2. Open a terminal, `cd` into your workspace folder, and run `claude` to start a session.
3. Follow [Choose Your Home](#choose-your-home) above — Path A or Path B both work directly from Claude Code.

**You should now see** the `handsonai` plugin listed when you run `/plugin`, and your assistant able to run `/handsonai:scaffolding-registry` or respond to "set up my AI registry."

### Cowork

:::note[Not yet verified — ask your instructor]
The registry setup flow hasn't been verified end-to-end on Cowork for this playbook yet. Ask your instructor before relying on this path for a live session. If you're working through this self-paced, the [Claude Code](#claude-code) path is the verified one.
:::

1. Install the Hands-on AI plugin from the marketplace inside Cowork's plugin manager. See the [plugin marketplace page](../../use-the-playbook/build/) for the exact steps.
2. Open your workspace folder as a Cowork project.
3. Follow [Choose Your Home](#choose-your-home) above — Path A or Path B both work directly from Cowork.

**You should now see** the Hands-on AI plugin's skills available in your Cowork project, and your assistant able to respond to "set up my AI registry" inside that project.

### ChatGPT Desktop (Codex)

:::note[Not yet verified — ask your instructor]
The registry setup flow hasn't been verified end-to-end in ChatGPT desktop's Codex mode for this playbook yet. Ask your instructor before relying on this path for a live session. If you're working through this self-paced, the [Claude Code](#claude-code) path is the verified one.
:::

1. Download the Hands-on AI skill files your instructor provides (the same package used everywhere else in this playbook).
2. Install them at the user level so they're available across every repo you work in: place the skill folders in `~/.agents/skills/` on your computer. (You can instead check a copy into a single repo's `.agents/skills/` folder if you have a specific reason to pin that repo to its own copy — most students don't need this.)
3. Open your workspace folder in ChatGPT desktop's Codex mode.
4. Follow [Choose Your Home](#choose-your-home) above — Path A or Path B both work, since Codex edits your local files directly.

**You should now see** Codex able to read the skill instructions and respond to "set up my AI registry" by writing files into your local workspace folder.

### claude.ai

:::note[Not yet verified — ask your instructor]
The exact steps for connecting claude.ai to your GitHub repository (via its GitHub connector) haven't been verified against the current claude.ai interface for this playbook. Ask your instructor for the current click-by-click steps before relying on this path for a live session. If you're working through this self-paced and don't need to stay in claude.ai specifically, consider the Claude Code path instead — see [Claude Code](#claude-code) above.
:::

1. Upload the Hands-on AI skill file your instructor provides to your claude.ai account (Settings → Capabilities → Skills, or wherever claude.ai currently places skill uploads).
2. If you have a GitHub repository connector configured, connect it to the repository you want as your registry's home; if not, plan to use Path C ([No Repository](#path-c-no-repository--generate-and-commit-from-the-cloud)) instead.
3. Start a conversation and say: *"Set up my AI registry."*
4. Follow [Path C](#path-c-no-repository--generate-and-commit-from-the-cloud) above if claude.ai cannot write to your repository directly — it will generate each file for you to commit by hand.

**You should now see** either files committed directly to your connected repository, or a complete set of file contents in the conversation with the exact path for each — never a vague "I've created your registry" without specifics.

### ChatGPT Web (Business/Enterprise)

:::note[Not yet verified — ask your instructor]
The exact steps for uploading a Personal Skill and connecting a GitHub repository in ChatGPT web haven't been verified against the current interface for this playbook. Ask your instructor for the current click-by-click steps before relying on this path for a live session.
:::

1. Upload the Hands-on AI skill file your instructor provides as a Personal Skill in your ChatGPT workspace settings.
2. If your workspace has a GitHub connector configured, connect it to the repository you want as your registry's home; if not, plan to use Path C ([No Repository](#path-c-no-repository--generate-and-commit-from-the-cloud)) instead.
3. Start a conversation and say: *"Set up my AI registry."*
4. Follow [Path C](#path-c-no-repository--generate-and-commit-from-the-cloud) above if ChatGPT cannot write to your repository directly.

**You should now see** either files committed directly to your connected repository, or a complete set of file contents in the conversation with the exact path for each.

### M365 Copilot

:::note[Not yet verified — ask your instructor]
The exact steps for packaging the Hands-on AI skill as Copilot agent instructions, and connecting SharePoint or GitHub, haven't been verified against the current Copilot interface for this playbook. Ask your instructor for the current click-by-click steps before relying on this path for a live session.
:::

1. Ask your instructor for the packaged Copilot agent instructions covering the Hands-on AI registry skills.
2. Configure Copilot's SharePoint or GitHub connector to point at wherever your registry will live.
3. Start a conversation and say: *"Set up my AI registry."*
4. Follow [Path C](#path-c-no-repository--generate-and-commit-from-the-cloud) above if Copilot cannot write to your files directly — save each generated file at the path it specifies.

**You should now see** either files saved directly at the connected location, or a complete set of file contents in the conversation with the exact path for each.

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

- This tier only applies if you started from the template repo (Path A) — registries added to an existing workspace don't have it unless you set it up separately.
- Confirm GitHub Pages is turned on for your repository (Settings → Pages in your repo on github.com) — it's off by default until you enable it.
- Check the **Actions** tab in your repository for a failed run — Actions is the tab on your repository's GitHub page that lists every automated run; a red ✗ next to a run means it failed. Click that run and read the first red line for the reason. A broken node (one with a lint error) blocks publishing on purpose, the same way it blocks a local dashboard refresh. The failure message names the file and the rule it broke.

## Next Steps

- **Find AI opportunities** — Use the [Analyze](../../ai-workflow-framework/analyze/) guide to identify where AI can add value
- **Deconstruct your first workflow** — Follow the [Deconstruct](../../ai-workflow-framework/deconstruct/) guide; your registry updates itself as you go
- **Document workflows** — Ask your assistant to write SOPs (`writing-workflow-sops`) and process guides (`writing-process-guides`)
- **Explore the plugin** — See the [Hands-on AI plugin page](../../use-the-playbook/build/) for all registry-related skills
