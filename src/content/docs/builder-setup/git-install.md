---
title: Git Installation Guide
description: Install Git on macOS or Windows and configure your identity — the second of three prerequisites, with a Done-when check at the end
schema_type: HowTo
howto_steps:
  - name: Open your terminal
    text: "macOS: press Cmd + Space, type Terminal, press Enter. Windows: press Start, type PowerShell, press Enter."
  - name: Check if Git is already installed
    text: Run 'git --version'. If you see a version number, skip to Step 5. On a Mac, a popup offering to install the command line developer tools may appear — click Install.
  - name: Install Git
    text: "macOS: run 'xcode-select --install' (or brew install git if you already use Homebrew). Windows: download from git-scm.com and run the installer, clicking Next on every screen except the default editor."
  - name: Verify installation
    text: Open a new terminal window and run 'git --version' to confirm Git is installed.
  - name: Configure your identity
    text: Set your name and the email address on your GitHub account with 'git config --global user.name' and 'git config --global user.email', then print both back to confirm.
---

**Prerequisite 2 of 3.** You have a [GitHub account](../github-setup/) and know which email address is on it. This guide installs Git on your computer and tells it who you are. The [GitHub CLI](../github-cli-setup/) comes next.

:::note[On a company laptop?]
You may need admin rights or IT approval to run an installer. Ask IT before you start. If commands work at home but fail at work, see [Corporate Networks](#corporate-networks-proxy--firewall) below.
:::

## What Is Git?

Git is a version control tool — it tracks every change you make to your files over time. Think of it like a detailed undo history that never expires. You can save a snapshot of your work (called a *commit*), go back to any previous version, and see exactly what changed and when.

For AI development, Git is essential for two reasons. First, AI coding tools use it behind the scenes — every time an AI assistant edits a file, that change gets tracked as a commit, giving you a clear record of what the AI did and letting you undo anything you don't want. Second, the prompts, skills, and agents you create are valuable building blocks that power your AI workflows. Git ensures you never lose them — every version is saved, and you can always recover or refine what you've built.

This guide installs Git on your machine and sets up your identity so your work is properly attributed.

## Step 1: Open Your Terminal

Every command in this guide is typed into a terminal — a window where you type instructions instead of clicking them.

1. **macOS:** press `Cmd + Space`, type `Terminal`, press Enter.
2. **Windows:** press Start, type `PowerShell`, press Enter.

You type a command, press Enter, and read what comes back. Never used a terminal before? The [Terminal Basics primer](/builder-setup/terminal-basics/) is about 15 minutes and covers everything the guides below assume.

## Step 2: Check If Git Is Already Installed

Open your terminal and run:

```bash
git --version
```

1. **You see a version number** (e.g., `git version 2.39.0`)? Git is already installed. Skip to [Step 5: Configure Your Identity](#step-5-configure-your-identity).
2. **On a Mac, a popup appears** saying *The "git" command requires the command line developer tools. Would you like to install the tools now?* That's not an error — it's the installer. Click **Install**, wait for it to finish (10–30 minutes; the time estimate is famously unreliable), then continue to [Step 4](#step-4-verify-installation). You've just done Option 1 below.
3. **Anything else** (`command not found`, `not recognized`)? Continue to Step 3.

## Step 3: Install Git

Follow the section for your computer, then continue to Step 4.

### macOS

#### Option 1: Xcode Command Line Tools (Recommended)

1. In your terminal, run: `xcode-select --install`
2. Click **Install** in the popup dialog
3. Wait for installation to complete — the download can take 10–30 minutes, and the dialog's time estimate is famously unreliable (it may claim hours). Let it run.

This installs Git along with Apple's other free developer tools. (You don't need the full Xcode app — just these command line tools.)

> **Seeing "command line tools are already installed"?** That red text isn't a problem — it means Git is already there. Skip to [Step 4: Verify Installation](#step-4-verify-installation).

#### Option 2: Homebrew

Homebrew is a popular tool for installing developer software on macOS. If you don't have it, use Option 1 above.

```bash
brew install git
```

<details>
<summary>Don't have Homebrew? (not required — Option 1 is simpler)</summary>

Homebrew is a package manager some Mac users install for developer tools. If you want it anyway, follow the one-line install command at [brew.sh](https://brew.sh). Two things catch people out:

1. It asks for your Mac password partway through and then runs for 5–10 minutes — that's normal.
2. On an Apple Silicon Mac, the last lines of output say **Next steps** and show two commands to add Homebrew to your PATH. Run them. If you skip this, `brew` says `command not found` in every new terminal.

</details>

### Windows

#### Download and Install

1. Go to [git-scm.com](https://git-scm.com)
2. Click **Download for Windows**
3. Open your **Downloads** folder and double-click the file (named like `Git-2.xx-64-bit.exe`). If Windows asks *Do you want to allow this app to make changes?*, click **Yes**
4. Click **Next** through the prompts — the installer shows about ten screens. On every screen except the three listed below, the default is right: just click **Next**
5. Click **Install**, wait for the progress bar to finish, then click **Finish**

#### Important Settings During Install

These screens appear in this order as you click through:

1. **Default editor**: Select **Visual Studio Code** if it's listed. If it isn't (you haven't installed an editor yet), choose **Notepad** — you can change this later. Avoid the default (Vim) unless you're familiar with it.
2. **PATH environment**: Select "Git from the command line and also from 3rd-party software" — this is already the default, so just confirm it's selected
3. **Line endings**: Select "Checkout Windows-style, commit Unix-style line endings" — also the default

## Step 4: Verify Installation

After installing, open a new terminal window and run:

```bash
git --version
```

You should see a version number confirming Git is installed.

## Step 5: Configure Your Identity

Set your name and email for Git commits. Replace `Your Name` and `your.email@example.com` with your own, and keep the quotation marks — without them, a name with a space in it won't save correctly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the email address on your GitHub account — the one you wrote down in the [GitHub Account guide](../github-setup/). If they don't match, your commits still work, but GitHub shows them under an unlinked name instead of your profile. That's easy to fix later — add the email address to your GitHub account (**Settings → Emails**) and GitHub links your past commits to your profile automatically.

Turned on **Keep my email addresses private** on GitHub? Use the substitute `@users.noreply.github.com` address instead — see the [GitHub Account guide](../github-setup/#step-2-turn-on-two-factor-authentication-2fa) for where to find it.

Confirm your identity actually saved:

```bash
git config --global user.name
git config --global user.email
```

Each command prints back the value you just set. If either prints nothing, re-run the matching command above.

## Done When

| Prerequisite | Done when |
|---|---|
| **2. Git installed** | `git --version` prints a version number, and `git config --global user.name` and `git config --global user.email` each print back the value you set |

**Next:** [Install the GitHub CLI](../github-cli-setup/) — prerequisite 3 of 3.

---

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

**Behind a firewall that blocks SSH:** if `git clone git@github.com:...` hangs or times out, corporate firewalls often allow HTTPS (port 443) but block the SSH port. Use the HTTPS clone URL instead (`https://github.com/...`) — this is also what the [GitHub CLI Setup Guide](../github-cli-setup/) and [Repository Creation and Cloning Guide](../repo-creation-and-cloning/) use by default.

</details>

## Troubleshooting

**Command not found (Mac)?**
- Close and reopen Terminal after installation
- Try running `xcode-select --install` again

**Command not found (Windows)?**
- Close and reopen your terminal
- Make sure you selected the PATH option during installation
- Reinstall and select "Git from the command line and also from 3rd-party software"
- Or use **Git Bash** instead of PowerShell — the Git installer adds it, and it finds `git` either way. Git Bash also behaves like the macOS terminal, so tutorials written for Mac or Linux (anything using `ls`, `touch`, or forward-slash paths) work in it unchanged. For everything in these guides, PowerShell is fine.

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

- Install the GitHub CLI (see [GitHub CLI Setup Guide](../github-cli-setup/))
- Then create and clone your first repository (see [Repository Creation and Cloning Guide](../repo-creation-and-cloning/))

## Resources

- [Git Downloads](https://git-scm.com/downloads)
- [Git Documentation](https://git-scm.com/doc)
