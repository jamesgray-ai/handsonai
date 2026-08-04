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

You type a command, press Enter, and read what comes back. Never used a terminal before? The [Terminal Basics primer](/builder-setup/terminal-basics/) is about 15 minutes and covers everything the guides below assume.

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
4. Wait for installation to complete — the download can take 10–30 minutes, and the dialog's time estimate is famously unreliable (it may claim hours). Let it run.

This installs Git along with other developer tools.

> **Seeing "command line tools are already installed"?** That red text isn't a problem — it means Git is already there. Skip to [Verify Installation](#verify-installation).

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
4. Click **Next** through the prompts — the installer shows about ten screens, and the defaults are fine everywhere except the three settings below
5. Complete the installation

### Important Settings During Install

These screens appear in this order as you click through:

- **Default editor**: Select **VS Code** or **Cursor** if listed. If neither appears (you haven't installed an editor yet), choose **Notepad** — you can change this later. Avoid the default (Vim) unless you're familiar with it.
- **PATH environment**: Select "Git from the command line and also from 3rd-party software" — this is already the default, so just confirm it's selected
- **Line endings**: Select "Checkout Windows-style, commit Unix-style line endings" — also the default

## Verify Installation

After installing, open a new terminal window and run:

```bash
git --version
```

You should see a version number confirming Git is installed.

## Configure Your Identity

Set your name and email for Git commits. Keep the quotation marks — without them, a name with a space in it won't save correctly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the email address you plan to use for your GitHub account (set up in the next step). If they don't match, your commits still work, but GitHub shows them under an unlinked name instead of your profile. That's easy to fix later — add the email address to your GitHub account (**Settings → Emails**) and GitHub links your past commits to your profile automatically.

> **Planning to keep your email private on GitHub?** GitHub's **Keep my email addresses private** setting (under **Settings → Emails**) gives you a substitute address ending in `@users.noreply.github.com`. Once your account exists, come back and run the email command again with that address:
>
> ```bash
> git config --global user.email "12345678+yourusername@users.noreply.github.com"
> ```
>
> Otherwise, if the companion setting **Block command line pushes that expose my email** is on, GitHub rejects pushes made with your real email (`error: GH007`).

Confirm your identity actually saved:

```bash
git config --global user.name
git config --global user.email
```

Each command prints back the value you just set. If either prints nothing, re-run the matching command above.

## Corporate Networks (Proxy / Firewall)

If Git commands work at home but fail on your work machine, your company network is the likely cause. Don't troubleshoot this alone: ask your IT team whether your network uses a proxy, and share this section with them — the commands below are the fix, but IT has the details (like the proxy address) that make them work.

<details>
<summary>Proxy and firewall fixes (for you and your IT team)</summary>

**Behind a proxy:**

```bash
git config --global http.proxy http://proxy.company.com:port
git config --global https.proxy http://proxy.company.com:port
```

Ask your IT team for the proxy address and port if you don't have it. To remove both settings later — do unset **both**, or the leftover `https.proxy` keeps breaking HTTPS remotes once you're off the corporate network:

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

**Behind a firewall that blocks SSH:** if `git clone git@github.com:...` hangs or times out, corporate firewalls often allow HTTPS (port 443) but block the SSH port. Use the HTTPS clone URL instead (`https://github.com/...`) — this is also what the [GitHub Setup Guide](../github-setup/) and [Repository Creation and Cloning Guide](../repo-creation-and-cloning/) use by default.

</details>

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
