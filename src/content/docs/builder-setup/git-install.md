---
title: Git Installation Guide
description: Install Git on macOS or Windows, configure your identity, and verify installation
schema_type: HowTo
howto_steps:
  - name: Check if Git is already installed
    text: Open your terminal and run 'git --version'. If you see a version number, Git is already installed.
  - name: Install Git on your operating system
    text: "macOS: Run 'xcode-select --install' or use Homebrew. Windows: Download from git-scm.com and run the installer."
  - name: Verify installation
    text: Open a new terminal window and run 'git --version' to confirm Git is installed.
  - name: Configure your identity
    text: Set your name and email for Git commits using 'git config --global user.name' and 'git config --global user.email'.
---## What Is Git?

Git is a version control tool — it tracks every change you make to your files over time. Think of it like a detailed undo history that never expires. You can save a snapshot of your work (called a *commit*), go back to any previous version, and see exactly what changed and when.

For AI development, Git is essential for two reasons. First, AI coding tools use it behind the scenes — every time an AI assistant edits a file, that change gets tracked as a commit, giving you a clear record of what the AI did and letting you undo anything you don't want. Second, the prompts, skills, and agents you create are valuable building blocks that power your AI workflows. Git ensures you never lose them — every version is saved, and you can always recover or refine what you've built.

This guide installs Git on your machine and sets up your identity so your work is properly attributed.

## Opening a Terminal

Every command in this guide is typed into a terminal — a window where you type instructions instead of clicking them.

- **macOS:** press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows:** press Start, type `PowerShell`, press Enter.

You type a command, press Enter, and read what comes back. Never used a terminal before? The [Terminal Basics primer](/courses/tools-setup-checklist/) is about 15 minutes and covers everything the guides below assume.

Every command in this guide and the [GitHub Setup Guide](../github-setup/) works in PowerShell — they all run the `git` or `gh` program, which the installer adds to your system.

**Windows: when you might want Git Bash instead.** The Git installer also adds **Git Bash**, a terminal that behaves like the macOS one. If you follow a tutorial written for Mac or Linux — anything using `ls`, `touch`, or forward-slash paths — run it in Git Bash and the commands work unchanged. For everything in these guides, PowerShell is fine.

> **PowerShell says `git` is not recognized?** Git installed without being added to your PATH. See [Troubleshooting](#troubleshooting) to fix it — or use Git Bash, which works either way.

## Check If Git Is Already Installed

Open your terminal and run:

```bash
git --version
```

If you see a version number (e.g., `git version 2.39.0`), Git is already installed. You can skip to verification.

## macOS

### Option 1: Xcode Command Line Tools (Recommended)

1. Open Terminal
2. Run: `xcode-select --install`
3. Click **Install** in the popup dialog
4. Wait for installation to complete

This installs Git along with other developer tools.

### Option 2: Homebrew

Homebrew is a popular tool for installing developer software on macOS. If you don't have it, use Option 1 above.

```bash
brew install git
```

## Windows

### Download and Install

1. Go to [git-scm.com](https://git-scm.com)
2. Click **Download for Windows**
3. Run the installer
4. Use the default settings (click Next through the prompts)
5. Complete the installation

### Important Settings During Install

- **Default editor**: Select **VS Code** or **Cursor** if listed — avoid the default (Vim) unless you're familiar with it
- **PATH environment**: Select "Git from the command line and also from 3rd-party software" (recommended)
- **Line endings**: Select "Checkout Windows-style, commit Unix-style line endings" (recommended)

## Verify Installation

After installing, open a new terminal window and run:

```bash
git --version
```

You should see a version number confirming Git is installed.

## Configure Your Identity

Set your name and email for Git commits:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the email address you plan to use for your GitHub account (set up in the next step). If these don't match, your commits still work but GitHub won't attribute them to your profile — they show up as an unlinked name, and fixing it later means rewriting history.

Confirm your identity actually saved:

```bash
git config --list
```

Look for `user.name` and `user.email` in the output, with the values you just set.

## Corporate Networks (Proxy / Firewall)

On a work machine, Git may fail to reach GitHub if traffic has to go through a corporate proxy or a restrictive firewall.

**Behind a proxy:**

```bash
git config --global http.proxy http://proxy.company.com:port
git config --global https.proxy http://proxy.company.com:port
```

Ask your IT team for the proxy address and port if you don't have it. To remove the setting later: `git config --global --unset http.proxy`.

**Behind a firewall that blocks SSH:** if `git clone git@github.com:...` hangs or times out, corporate firewalls often allow HTTPS (port 443) but block the SSH port. Use the HTTPS clone URL instead (`https://github.com/...`) — this is also what the [GitHub Setup Guide](../github-setup/) and [Repository Creation and Cloning Guide](../repo-creation-and-cloning/) use by default.

## Troubleshooting

**Command not found (Mac)?**
- Close and reopen Terminal after installation
- Try running `xcode-select --install` again

**Command not found (Windows)?**
- Close and reopen your terminal
- Make sure you selected the PATH option during installation
- Reinstall and select "Git from the command line and also from 3rd-party software"

**PATH still broken after reinstalling on Windows?**
1. Open **Start → Environment Variables** (search "edit the system environment variables")
2. Click **Environment Variables…**
3. Under **System variables**, select **Path**, click **Edit**
4. Confirm an entry exists for Git's `cmd` folder (typically `C:\Program Files\Git\cmd`) — click **New** and add it if missing
5. Click **OK** on every dialog, then close and reopen your terminal
6. Run `git --version` again to confirm

**Permission errors?**
- On Mac, you may need to enter your password during Xcode tools installation
- On Windows, run the installer as Administrator

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm trying to install Git on [Mac / Windows] and getting this error: [paste the error message]. I followed the steps from the official guide. What should I try next?

</details>
## Next Steps

- Set up your GitHub account (see [GitHub Setup Guide](../github-setup/))
- Set up your AI platform (see [Platforms](../../platforms/))

## Resources

- [Git Downloads](https://git-scm.com/downloads)
- [Git Documentation](https://git-scm.com/doc)
