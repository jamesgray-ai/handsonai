---
title: Repository Creation and Cloning Guide
description: Create your first GitHub repository and clone it to your computer using your editor or Claude Desktop
schema_type: HowTo
howto_steps:
  - name: Create a repository
    text: Click the + menu, select New repository, name it, add a README, and click Create repository.
  - name: Clone the repository
    text: Open the Command Palette (Cmd/Ctrl + Shift + P), type Git Clone, paste the repository address, and choose a folder on your computer.
  - name: Verify the clone worked
    text: Open the terminal inside your editor and run 'git status' — it should show 'On branch main'.
---

**The end-to-end proof.** You've finished the three prerequisites — a [GitHub account](../github-setup/), [Git](../git-install/), and the [GitHub CLI](../github-cli-setup/). This guide uses all three together: you create a repository on GitHub and make a copy of it on your computer. If it works, everything is set up correctly — and you have the folder you'll build in.

## What This Guide Covers

A *repository* is a project folder that Git tracks. You create it on GitHub (in your browser), then *clone* it — make a linked copy on your own machine — so you can work on the files locally and Git keeps the two in sync.

## Prerequisites

**To create a repository (Step 1):**

1. A GitHub account

That's all — creating a repository happens entirely in your browser. (If you only need this repository for an AI agent to use through a [personal access token](../github-setup/#later-give-an-agent-or-tool-access-optional), Step 1 is all you need.)

**To clone it to your computer (Steps 2 and 3):**

1. Git installed (see [Git Installation Guide](../git-install/))
2. GitHub CLI installed and logged in (see [GitHub CLI Setup Guide](../github-cli-setup/))
3. Cursor or VS Code (see [Editor Setup Guide](../editor-setup/)) — or the Claude Desktop app

## Step 1: Create a Repository

1. From GitHub, click the **+** button (top-right corner) → **New repository**
2. Enter a repository name (e.g., `my-ai-projects`)
3. Add an optional description
4. Select **Private** (recommended for personal work)
5. Check **Add a README file**
6. Click **Create repository**

You'll land on your new repository's page with a README file. Copy the address from your browser's address bar (e.g., `https://github.com/your-username/my-ai-projects`) — you'll paste it in the next step.

## Step 2: Clone the Repository

Cloning downloads a copy of the repository to your computer and links it to GitHub. Use whichever tool you're working in.

### In Cursor or VS Code

1. Open the Command Palette: press `Cmd + Shift + P` (Mac) or `Ctrl + Shift + P` (Windows)
2. Type **Git: Clone** and press Enter
3. Paste the repository address you copied in Step 1 (e.g., `https://github.com/your-username/my-ai-projects`) and press Enter
4. Choose a folder on your computer to put it in — Documents is fine
5. When the editor asks whether to open the cloned repository, click **Open**

### In Claude Desktop (Code tab)

If you're working in the Claude Desktop app without a separate code editor, you can clone the repository by asking Claude to do it for you. Because you installed and logged in to the GitHub CLI in the [GitHub CLI Setup Guide](../github-cli-setup/), Claude can use `gh` on your behalf.

1. Open **Claude Desktop** and click the **Code** tab
2. Start a new session and pick (or create) a folder on your computer you want the repository cloned into
3. In the chat box, paste a prompt like:

   > Clone `https://github.com/your-username/my-ai-projects` into this folder.

4. Approve the command when Claude asks for permission to run `gh repo clone` (or `git clone`)
5. When it finishes, open Finder (macOS) or File Explorer (Windows) and navigate to the folder you chose — you should see the cloned repository there

## Step 3: Verify the Clone Worked

After cloning, confirm the repository is on your computer:

1. Check the **sidebar** in your editor — you should see the repository's files (at least `README.md`)
2. Open the terminal inside your editor (**View → Terminal**, or press **Ctrl + `**) and run:

```bash
git status
```

You should see a message starting `On branch main` — this confirms the repository was cloned correctly and Git is tracking it.

## Done When

- You can see the cloned repository's files in your editor (or in the Claude Desktop Code tab)
- In your terminal, you can navigate to the cloned folder (`cd my-repo-name`) and run `git status` — it shows `On branch main`

If both are true, your GitHub account, Git, and the GitHub CLI are all working together. **Next:** set up your [AI Registry](../ai-registry-setup/) in this repository.

---

## Troubleshooting

**Can't create the repository?**
- Make sure you're signed in to GitHub
- Repository names must be unique within your account — try a different name if you get a conflict

**Can't clone the repository?**
- Verify you have access to the repository
- Check that the URL is correct
- Make sure you're signed into GitHub in your editor

**Asked to sign in?**
- Your editor may ask you to sign in to GitHub the first time — follow the prompts in your browser
- Still stuck? Run `gh auth status` in a terminal. If it doesn't say you're logged in, redo [Step 3 of the GitHub CLI guide](../github-cli-setup/#step-3-log-in)
- If an AI agent or automation (not you) is doing the cloning, it needs a [personal access token](../github-setup/#later-give-an-agent-or-tool-access-optional) instead

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm trying to create/clone a GitHub repository in [Cursor / VS Code] on [Mac / Windows] and getting this error: [paste the error message]. I have Git installed, a GitHub account, and the GitHub CLI logged in. What should I try?

</details>

## Next Steps

- Set up your [AI Registry](../ai-registry-setup/) in the repository you just cloned
- Read [Git Concepts](../git-concepts/) for the vocabulary — commit, push, pull, branch — you'll meet as you work

## Resources

- [GitHub Docs](https://docs.github.com)
- [GitHub CLI manual](https://cli.github.com/manual/)
