---
title: GitHub CLI Setup Guide
description: Install the GitHub CLI (gh) on macOS or Windows and log in once, so Git and the AI tools on your computer can reach GitHub as you
schema_type: HowTo
howto_steps:
  - name: Install the GitHub CLI
    text: "macOS: download the macOS_universal.pkg from the GitHub CLI releases page and run it. Windows: download the MSI from cli.github.com and run it."
  - name: Open your terminal
    text: "macOS: press Cmd + Space, type Terminal, press Enter. Windows: press Start, type PowerShell, press Enter. Open a new window so it sees the newly installed program."
  - name: Log in
    text: Run 'gh auth login', choose GitHub.com, HTTPS, Yes, and Login with a web browser, then enter the one-time code and click Authorize GitHub CLI in your browser.
  - name: Confirm you're done
    text: Run 'gh --version' and 'gh auth status'. You should see a version number and a line saying you are logged in to github.com.
---

**Prerequisite 3 of 3.** You have a [GitHub account](../github-setup/) and [Git](../git-install/) installed. This guide installs the GitHub CLI and logs it in, so your computer — and the AI tools on it — can reach GitHub as you.

## What Is the GitHub CLI?

The GitHub CLI (`gh`) is a small program that lets your computer talk to GitHub. You sign in through it once, and from then on Git and the AI code editors and coding agents on your machine can push and pull your files without asking for a password every time. CLI means "command line interface" — you use it by typing commands in a terminal rather than clicking in a browser.

The official home of the GitHub CLI is [cli.github.com](https://cli.github.com).

:::note[On a company laptop?]
You may need admin rights or IT approval to run an installer. Ask IT before you start. If commands work at home but fail at work, see [Corporate Networks](/builder-setup/git-install/#corporate-networks-proxy--firewall) in the Git guide.
:::

## Step 1: Install the GitHub CLI

Follow the section for your computer, then continue to Step 2.

### macOS

1. Open the [GitHub CLI releases page](https://github.com/cli/cli/releases/latest).
2. Scroll down to **Assets**. If you only see a few files, click **Show all assets**.
3. Press `Cmd + F`, type `universal.pkg`, and click the file it highlights — it's named like `gh_2.101.0_macOS_universal.pkg` (the number changes with each release). It downloads.
4. Open your **Downloads** folder and double-click the file. Click **Continue** → **Install**, enter your Mac password when asked, then **Close**.
5. If Terminal is already open, quit it — you'll open a fresh one in Step 2.

*Why not cli.github.com?* It's the official home of the GitHub CLI, but its Mac download is a bare program file, not an installer — it won't work with a double-click. Its Windows download is fine.

**Already have [Homebrew](https://brew.sh)?** `brew install gh` does the same thing. Don't install Homebrew just for this.

### Windows

1. Go to [cli.github.com](https://cli.github.com).
2. Click the dropdown button next to the green **Copy** button (on Windows it reads **Install with WinGet**) and choose **Windows — Download MSI**. The installer downloads.
3. Open your **Downloads** folder and double-click the file. Click **Next**, then **Install** — approve the Windows security prompt if one appears — then **Finish**.
4. If PowerShell is already open, close it — you'll open a fresh one in Step 2.

**Prefer a command?** In PowerShell, run `winget install --id GitHub.cli`. The first time you use `winget` it asks *Do you agree to all the source agreements terms?* — type `Y` and press Enter. If PowerShell says `winget` is not recognized, use the MSI above instead.

## Step 2: Open Your Terminal

Every remaining command is typed into a terminal — a window where you type instructions instead of clicking them. Open a **new** window now, even if you had one open before: a terminal only notices newly installed programs when it starts.

1. **macOS:** press `Cmd + Space`, type `Terminal`, press Enter.
2. **Windows:** press Start, type `PowerShell`, press Enter.

Never used a terminal before? The [Terminal Basics primer](../terminal-basics/) is about 15 minutes and covers everything this guide assumes.

## Step 3: Log In

Run:

```bash
gh auth login
```

Before it opens your browser, `gh` asks four questions in the terminal. Use the arrow keys to choose and press Enter:

| Question | Choose |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations on this host? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

The exact wording shifts slightly between `gh` versions, but the questions come in this order and these are the answers to give. Answering **Yes** to the third question is what lets Git push and pull without ever asking you for a password.

Then, in order:

1. The terminal says **First copy your one-time code:** followed by a code like `A1B2-C3D4`, then **Press Enter to open github.com in your browser…** — note the code, then press Enter.
2. Your browser opens a GitHub page asking for the code. Type it in and click **Continue**.
3. GitHub shows **Authorize GitHub CLI**. Click it. It may ask for your password or a two-factor code first — that's normal.
4. The browser shows **Congratulations, you're all set!** You can close that tab.
5. Back in the terminal, the last line reads `✓ Logged in as your-username`.

## Done When

| # | Prerequisite | Done when |
|---|---|---|
| 3 | **GitHub CLI installed and logged in** | `gh --version` prints a version number, and `gh auth status` prints `✓ Logged in to github.com account <your-username>` |

Run both now:

```bash
gh --version
gh auth status
```

The output looks like this (your version number and username will differ):

```
gh version 2.101.0 (2026-09-15)
github.com
  ✓ Logged in to github.com account your-username (keyring)
  - Active account: true
  - Git operations protocol: https
```

If you see both, all three prerequisites are done. **Next:** [Create and clone your first repository](../repo-creation-and-cloning/) — the end-to-end proof that your account, Git, and the CLI all work together.

---

## Troubleshooting

**`gh` is not recognized / command not found after installing?**
- Close and reopen your terminal, then run `gh --version` again — a terminal only picks up newly installed programs when it starts

**Downloaded a `.zip` from cli.github.com on a Mac?**
- Delete it. That file is a bare program, not an installer. Follow the macOS steps in [Step 1](#step-1-install-the-github-cli) to get the `.pkg` from the releases page instead

**`gh auth login` fails or hangs?**
- Make sure you have a browser available to complete the flow
- Try `gh auth login --web` to force the browser-based flow
- Check `gh auth status` afterward to confirm

**`gh auth status` says "You are not logged into any GitHub hosts"?**
- The browser step didn't finish. Run `gh auth login` again and make sure you reach the **Congratulations, you're all set!** page before returning to the terminal

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm installing the GitHub CLI (`gh`) on [Mac / Windows] and logging in with `gh auth login`, and I'm getting this error: [paste the error message]. What should I try?

</details>

## Resources

- [GitHub CLI](https://cli.github.com) — official home and downloads
- [GitHub CLI manual](https://cli.github.com/manual/)
