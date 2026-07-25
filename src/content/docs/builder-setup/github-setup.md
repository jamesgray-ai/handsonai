---
title: GitHub Setup Guide
description: Create a GitHub account with 2FA, install the GitHub CLI, and choose between a CLI login and a personal access token
schema_type: HowTo
howto_steps:
  - name: Create a GitHub account
    text: Go to github.com, click Sign up, follow the prompts, verify your email address, and enable two-factor authentication.
  - name: Choose how you'll authenticate
    text: Use gh auth login when you're running commands yourself. Generate a fine-grained personal access token when a hosted agent or automation needs to authenticate without you present.
  - name: Give an agent or tool access
    text: Generate a fine-grained personal access token scoped to a specific repository, grant only the permissions the tool asks for, and store it in a password manager.
  - name: Work with files on your own machine
    text: Install gh via Homebrew or the macOS installer, winget (Windows), or apt (Linux), then run gh auth login to connect your GitHub account.
---## What Is GitHub?

GitHub is a website where people store, version, and share files — application code, but equally the prompts, skills, agents, and markdown you build with AI. If Git tracks your changes locally (like a save history on your computer), GitHub is where that history lives in the cloud — backed up, shareable, and accessible from anywhere.

As you build with AI, you'll create prompts, skills, agents, and project files that become the foundation of your workflows. GitHub is where those files live in the cloud — backed up, versioned, and accessible from any machine. Think of it as your portfolio and safety net in one place. Your files are stored in *repositories* (project folders that Git tracks), and you work with them by *cloning* — making a local copy on your computer.

## How to Use This Guide

**Everyone creates an account.** After that the guide forks, and you follow only the path that matches how you'll work:

| You need | Read |
|---|---|
| An AI agent, automation, or hosted tool to reach GitHub for you | [Give an agent or tool access](#give-an-agent-or-tool-access) |
| To work with the files yourself, on your own machine | [Work with files on your own machine](#work-with-files-on-your-own-machine) |

Plenty of people need both. Nobody needs to read the whole page top to bottom — [Choose how you'll authenticate](#choose-how-youll-authenticate) explains the difference if you're not sure which is you.

**Create your repository before you generate a token** — a token has to be scoped to a repository that already exists. The [Repository Creation and Cloning Guide](../repo-creation-and-cloning/) covers that, and its first section needs nothing installed.

New to the vocabulary — repository, commit, push, branch, merge? The [Git Concepts Reference](../git-concepts/) explains all of it without asking you to install anything.

## Prerequisites

**For everyone:**

- An email address for your GitHub account
- Your phone with an authenticator app, for two-factor authentication

Creating an account and generating a token happen entirely in your browser — nothing to install.

**Additionally, if you'll run Git commands yourself:**

- Git installed (see [Git Installation Guide](../git-install/))
- An editor such as Cursor or VS Code — useful, but not required for anything in this guide (see [Editor Setup Guide](../editor-setup/))

## Create Your GitHub Account

1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Follow the prompts to create your account
4. Verify your email address
5. Enable two-factor authentication (2FA):
   - Go to **Settings → Password and authentication**
   - Under **Two-factor authentication**, click **Enable two-factor authentication**
   - Choose an authenticator app (recommended — e.g., 1Password, Authy, Google Authenticator) or a security key
   - Scan the QR code with your authenticator app and enter the generated code to confirm
   - Save the recovery codes GitHub shows you somewhere safe (a password manager, not a text file) — you'll need one if you lose access to your authenticator

**Already have an account with 2FA enabled?** Skip ahead to whichever path you need.

## Choose How You'll Authenticate

Your GitHub password gets *you* into the website. It does not get anything else in — not the tools on your computer, and not an AI agent working on your behalf. Those need their own way to prove they're allowed.

There are two, and **which one you need depends on who is doing the asking**:

- **You, at your own computer.** You sign in once, and the tools on that machine remember you. This is a **CLI login** — CLI means "command line interface", the text-based way of working with a tool instead of clicking around a website. GitHub's is called the **GitHub CLI**.
- **Something acting on your behalf.** An AI agent, an automation, or a hosted tool needs a **personal access token** — a long string of characters you generate once and paste into that tool. It's a credential you hand over, like giving someone a key.

The difference that matters: a **CLI login is tied to your machine**, so anything that isn't on your machine can't use it. A **token travels** — which is what makes it work for a hosted agent, and also what makes it worth protecting.

| | Personal access token | GitHub CLI login |
|---|---|---|
| What it is | A credential you generate and paste into a tool | You sign in through your browser once; your computer remembers |
| Use it when | Something *other than you* needs access — an AI agent, an automation, a scheduled job | *You* are working on your own machine |
| How much access | Only the repositories and permissions you tick, and it expires on a date you choose | Broad access to your account, and it doesn't expire on its own |
| What to watch | It's a secret. If it leaks, it works until you revoke it or it expires | Anyone who can use your computer can use your GitHub access |

**If you generate a token, make it a fine-grained one.** GitHub offers two kinds, and the older "classic" tokens reach every repository you can reach and can be created with no expiry at all. Fine-grained tokens always expire and only ever grant the specific permissions you tick — even at their widest setting.

## Give an Agent or Tool Access

Complete this path when something *other than you* needs to reach GitHub — an AI agent, an automation, or a hosted tool. Nothing here requires installing anything.

### Creating a Fine-Grained Personal Access Token

1. Go to **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Give it a descriptive name (e.g., `claude-code-my-repo`)
4. Choose the **Resource owner** — your personal account, or an organisation if the repository belongs to one. Organisation-owned tokens usually need an admin to approve them before they work, which can take days; start early if that applies to you.
5. Set an **expiration** that outlasts whatever you're building with it — if you're on a course, set it past the last session; otherwise 30 or 90 days is a good default. Fine-grained tokens always expire, and GitHub caps a custom expiry at 366 days, so pick deliberately: one that lapses mid-project silently breaks every integration using it.
6. Set **Repository access** — **Only select repositories**, and choose just the repo(s) needed. Create the repository first if it doesn't exist yet (see the [Repository Creation and Cloning Guide](../repo-creation-and-cloning/)); you can't select one that isn't there.

   **All repositories** also exists, and covers current *and future* repositories — occasionally useful on a personal account holding nothing you care about, when you want a token that keeps working as you add repos. Two reasons to prefer selecting: many tools that consume a token require a specific repository anyway (Notion's Claude agent connector, for one, states this on its connect screen), and on any account holding real work the wider scope is a genuine risk. Never point a token at an organisation's full repository list to save a step.
7. Under **Permissions**, grant only what's needed. The tool you're connecting will list the permissions it requires — treat that list as authoritative. Two you'll meet often: **Contents** (read and write files) and **Pull requests** (open a pull request instead of writing straight to the main branch), each set to **Read and write**. GitHub adds **Metadata: Read** automatically.
8. Click **Generate token**
9. **Copy the token now** — GitHub shows it exactly once and cannot show it to you again

### Storing Your Token Safely

Save the token in a password manager (1Password, Bitwarden, etc.), not in a plain text file, a `.env` you might commit, or a note. If a hosted agent or tool needs the token, paste it directly into that tool's credential/secret field rather than writing it to disk in your repository.

## Work With Files on Your Own Machine

Complete this path when *you* will be running Git commands locally — in a terminal, an AI code editor, or a coding agent on your machine.

### Install GitHub CLI

The GitHub CLI (`gh`) is the simplest way to authenticate Git on your own machine, and it is what AI code editors and coding agents use to reach GitHub on your behalf. Install it before cloning a repository. Skip this section entirely if you won't be working with files locally.

#### macOS

With [Homebrew](https://brew.sh):

```bash
brew install gh
```

**No Homebrew?** If you installed Git via [Xcode Command Line Tools](../git-install/#option-1-xcode-command-line-tools-recommended) — the path the Git guide recommends — you probably don't have Homebrew. Download the macOS `.pkg` installer from [cli.github.com](https://cli.github.com) and run it — no terminal needed.

#### Windows

```powershell
winget install --id GitHub.cli
```

#### Linux (Debian/Ubuntu)

```bash
sudo apt install gh
```

For other Linux distributions, see the [official install instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md).

### Authenticate

```bash
gh auth login
```

Before it opens your browser, `gh` asks four questions in the terminal. Use the arrow keys to choose and press Enter:

| Question | Choose |
|---|---|
| What account do you want to log into? | **GitHub.com** |
| What is your preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate? | **Login with a web browser** |

It then shows a one-time code and opens your browser. Paste the code, approve the access, and return to the terminal — it confirms when it's done.

### Verify

```bash
gh --version
gh auth status
```

`gh auth status` should show you are logged in to `github.com` as your username.

**Official docs:** [GitHub CLI manual](https://cli.github.com/manual/)

## Troubleshooting

**`gh auth login` fails or hangs?**
- Make sure you have a browser available to complete the flow
- Try `gh auth login --web` to force the browser-based flow
- Check `gh auth status` afterward to confirm

**Token doesn't work?**
- Confirm the token hasn't expired
- Confirm the repository you're targeting is one of the repositories the token was scoped to
- Confirm the token has the permission the operation needs (e.g., **Contents: Read and write** to push commits)

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm setting up GitHub authentication (2FA / gh auth login / a fine-grained personal access token) and getting this error: [paste the error message]. What should I try?

</details>
## Next Steps

- [Create a repository and clone it](../repo-creation-and-cloning/) — the next step now that your account and authentication are set up

## Resources

- [GitHub Docs](https://docs.github.com)
- [GitHub CLI manual](https://cli.github.com/manual/)
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
