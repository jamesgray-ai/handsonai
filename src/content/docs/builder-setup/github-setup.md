---
title: GitHub Setup Guide
description: Create a GitHub account with 2FA, install the GitHub CLI, and choose between a CLI login and a personal access token
schema_type: HowTo
howto_steps:
  - name: Create a GitHub account
    text: Go to github.com, click Sign up, follow the prompts, verify your email address, and enable two-factor authentication.
  - name: Install GitHub CLI
    text: Install gh via Homebrew (macOS), winget (Windows), or apt (Linux), then run gh auth login to connect your GitHub account.
  - name: Choose your authentication method
    text: Use gh auth login when you're running commands yourself. Generate a fine-grained personal access token when a hosted agent or automation needs to authenticate without you present.
---## What Is GitHub?

GitHub is a website where people store and share code projects. If Git tracks your changes locally (like a save history on your computer), GitHub is where that history lives in the cloud — backed up, shareable, and accessible from anywhere.

As you build with AI, you'll create prompts, skills, agents, and project files that become the foundation of your workflows. GitHub is where those files live in the cloud — backed up, versioned, and accessible from any machine. Think of it as your portfolio and safety net in one place. Your files are stored in *repositories* (project folders that Git tracks), and you work with them by *cloning* — making a local copy on your computer.

This guide walks you through creating a GitHub account, securing it, and setting up the two ways you'll authenticate with GitHub. Once you're set up, head to the [Repository Creation and Cloning Guide](../repo-creation-and-cloning/) to create your first repository.

## Prerequisites

**For everyone (section 1 — creating your account):**

- An email address for your GitHub account
- Your phone with an authenticator app, for two-factor authentication

Section 1 and the token steps in section 3 happen entirely in your browser — nothing to install. If a hosted AI agent or automation is the only thing that needs GitHub access, those are all you need.

**Additionally, if you'll run Git commands yourself (section 2):**

- Git installed (see [Git Installation Guide](../git-install/))
- An editor such as Cursor or VS Code — useful, but not required for anything in this guide (see [Editor Setup Guide](../editor-setup/))

## 1. Create a GitHub Account

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

**Already have an account with 2FA enabled?** Skip to step 2.

## 2. Install GitHub CLI

The GitHub CLI (`gh`) is required for cloning repos from Claude Desktop's Code tab and for letting Cursor or Claude Code authenticate with GitHub programmatically. Install it before creating or cloning a repository.

### macOS

With [Homebrew](https://brew.sh):

```bash
brew install gh
```

**No Homebrew?** If you installed Git via Xcode Command Line Tools (the recommended path above), you probably don't have Homebrew. Download the macOS `.pkg` installer from [cli.github.com](https://cli.github.com) and run it — no terminal needed.

### Windows

```powershell
winget install --id GitHub.cli
```

### Linux (Debian/Ubuntu)

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

## 3. Choose How You'll Authenticate: Token vs. CLI Login

**A token is a stored secret. A CLI login is a session.**

`gh auth login` opens your browser, you approve, and the credential is stored locally on your machine (in `gh`'s configuration or your system credential helper). That works when **you** are the one running commands. It cannot work when something else needs to reach GitHub without you present — an AI agent, an automation, a hosted tool — because that thing can't access your machine's credential storage. For those, you generate a token and give it to them.

| | Fine-grained personal access token | `gh auth login` |
|---|---|---|
| What it is | A credential you generate and store | An interactive browser flow; the token is stored locally in `gh`'s config or your system credential helper |
| Use when | Something *other than you* must authenticate — a hosted agent, CI, an automation | *You* are working on your own machine |
| Scope | Per-repository, per-permission, with an expiry date | A broad set of account scopes (repo, read:org, gist, workflow) |
| Main risk | It's a secret: if it leaks it works until revoked or expired | Broad scope, and anyone with access to your machine can read it with `gh auth token` |

Prefer **fine-grained** personal access tokens over classic tokens throughout. Even at their widest setting, fine-grained tokens still expire and still grant only the specific permissions you tick. Classic tokens do neither — they carry coarse scopes across every repository you can reach, and can be created with no expiry at all.

### Creating a Fine-Grained Personal Access Token

1. Go to **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Give it a descriptive name (e.g., `claude-code-my-repo`)
4. Choose the **Resource owner** — your personal account, or an organisation if the repository belongs to one. Organisation-owned tokens usually need an admin to approve them before they work, which can take days; start early if that applies to you.
5. Set an **expiration** that outlasts whatever you're building with it — if you're on a course, set it past the last session; otherwise 30 or 90 days is a good default. GitHub caps custom expiry at 366 days. Avoid "No expiration" where offered. A token that expires mid-project silently breaks every integration using it.
6. Set **Repository access**. Which option is right depends on what the resource owner already owns:
   - **A personal account with little or nothing in it:** **All repositories** is fine, and is the simpler choice — it covers current *and future* repositories, so you can generate the token before you've created a repo and it will still work afterwards. The blast radius is whatever that account owns, which is close to nothing.
   - **An account or organisation holding work you care about:** **Only select repositories**, and choose just the repo(s) needed. This requires the repository to exist first. Never point a token at an organisation's full repository list to save a step.
7. Under **Permissions**, grant only what's needed (e.g., **Contents: Read and write** for an agent that commits and pushes — GitHub adds **Metadata: Read** automatically)
8. Click **Generate token**
9. **Copy the token now** — GitHub shows it exactly once and cannot show it to you again

### Storing Your Token Safely

Save the token in a password manager (1Password, Bitwarden, etc.), not in a plain text file, a `.env` you might commit, or a note. If a hosted agent or tool needs the token, paste it directly into that tool's credential/secret field rather than writing it to disk in your repository.

## Git Concepts

Understanding these terms helps when working with Claude Code.

### Commit

A **commit** saves a snapshot of your changes with a message describing what you did. Think of it as a save point you can return to.

### Push

**Push** uploads your local commits to GitHub. Until you push, your changes only exist on your computer.

### Pull

**Pull** downloads the latest changes from GitHub to your local copy. Do this before starting work to stay in sync.

### Staging

Before committing, you **stage** files to indicate which changes to include. You can commit some changes while leaving others for later.

## Using Claude Code for Git Operations

Once you have Claude Code installed, you can perform Git operations by asking Claude in natural language:

- "Commit my changes with a descriptive message"
- "Push my commits to GitHub"
- "Pull the latest changes"
- "Show me what files have changed"

Claude Code handles the Git commands for you.

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
