---
title: Repository Creation and Cloning Guide
description: Create your first GitHub repository and clone it to your computer using your editor or Claude Desktop
schema_type: HowTo
howto_steps:
  - name: Create a repository
    text: Click the + menu, select New repository, name it, add a README, and click Create repository.
  - name: Clone a repository
    text: Open the Command Palette (Cmd/Ctrl + Shift + P), type Git Clone, paste the repository URL, and choose a local folder.
  - name: Verify the clone
    text: Open the integrated terminal and run 'git status' to confirm the repository was cloned correctly.
---## What This Guide Covers

Once you have a GitHub account (see the [GitHub Setup Guide](../github-setup/)), the next step is creating a repository — a project folder that Git tracks. If you'll also work with the files on your own machine, you then clone it, so you have a local copy to work in.

## Prerequisites

**To create a repository (section 1):**

- A GitHub account

That's all. Creating a repository happens entirely in your browser — nothing to install. If a hosted agent or automation is the only thing that will touch this repository, you can stop after section 1.

**Additionally, to clone it to your machine (sections 2 and 3):**

- Git installed (see [Git Installation Guide](../git-install/))
- GitHub CLI authenticated (see [GitHub Setup Guide](../github-setup/))
- Cursor or VS Code installed (see [Editor Setup Guide](../editor-setup/))

## 1. Create a Repository

1. From GitHub, click the **+** button (top-right corner) → **New repository**
2. Enter a repository name (e.g., `my-ai-projects`)
3. Add an optional description
4. Select **Private** (recommended for personal work)
5. Check **Add a README file**
6. Click **Create repository**

You'll land on your new repository's page with a README file. The URL in your browser (e.g., `https://github.com/your-username/my-ai-projects`) is what you'll use to clone it in the next step.

## 2. Clone a Repository

Download (clone) a repository from GitHub using whichever tool you're working in.

### In Cursor or VS Code

1. Open the Command Palette (Cmd/Ctrl + Shift + P)
2. Type **Git: Clone**
3. Paste the repository URL (e.g., `https://github.com/username/project-name.git`)
4. Choose a local folder location
5. Open the cloned repository when prompted

### In Claude Desktop (Code tab)

If you're working in the Claude Desktop app without a separate code editor, you can clone a repo by asking Claude to do it for you. Because you installed and authenticated the GitHub CLI in the [GitHub Setup Guide](../github-setup/), Claude can use `gh` on your behalf.

1. Open **Claude Desktop** and click the **Code** tab
2. Start a new session and pick (or create) a local folder you want the repo cloned into
3. In the chat box, paste a prompt like:

   > Clone `https://github.com/username/project-name.git` into this folder.

4. Approve the command when Claude asks for permission to run `gh repo clone` (or `git clone`)
5. When it finishes, open Finder (macOS) or File Explorer (Windows) and navigate to the folder you chose — you should see the cloned repo there

## 3. Verify the Clone Worked

After cloning, confirm the repository is on your machine:

1. Check the **sidebar** in your editor — you should see the project's files and folders
2. Open the integrated terminal (**Ctrl + `**) and run:

```bash
git status
```

You should see a message like `On branch main` — this confirms the repository was cloned correctly and Git is tracking it.

## Troubleshooting

**Can't create the repository?**
- Make sure you're signed in to GitHub
- Repository names must be unique within your account — try a different name if you get a conflict

**Can't clone the repository?**
- Verify you have access to the repository
- Check that the URL is correct
- Make sure you're signed into GitHub in your editor

**Authentication issues?**
- Your editor may prompt you to sign into GitHub
- Follow the browser authentication flow when prompted
- If you're cloning as an automation or hosted agent rather than yourself, it needs a [fine-grained personal access token](../github-setup/#give-an-agent-or-tool-access), not `gh auth login`

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm trying to create/clone a GitHub repository in [Cursor / VS Code] on [Mac / Windows] and getting this error: [paste the error message]. I have Git installed, a GitHub account, and the GitHub CLI authenticated. What should I try?

</details>
## Next Steps

- Try cloning a public repository to practice the workflow
- Set up your AI platform (see [Platforms](../../platforms/))

## Resources

- [GitHub Docs](https://docs.github.com)
- [GitHub CLI manual](https://cli.github.com/manual/)
