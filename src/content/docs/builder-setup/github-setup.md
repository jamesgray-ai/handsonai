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

- Email address for GitHub account
- Cursor or VS Code installed (see [Editor Setup Guide](../editor-setup/))
- Git installed (see [Git Installation Guide](../git-install/))

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

```bash
brew install gh
```

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

Follow the browser prompts to connect your GitHub account.

### Verify

```bash
gh --version
gh auth status
```

`gh auth status` should show you are logged in to `github.com` as your username.

**Official docs:** [GitHub CLI manual](https://cli.github.com/manual/)

## 3. Choose How You'll Authenticate: Token vs. CLI Login

**A token is a stored secret. A CLI login is a session.**

`gh auth login` opens your browser, you approve, and the token lands in *your machine's* keychain. That works when **you** are the one running commands. It cannot work when something else needs to reach GitHub without you present — an AI agent, an automation, a hosted tool — because that thing can't read your keychain. For those, you generate a token and give it to them.

| | Fine-grained personal access token | `gh auth login` |
|---|---|---|
| What it is | A credential you generate and store | An interactive browser flow; token stored in your local keychain |
| Use when | Something *other than you* must authenticate — a hosted agent, CI, an automation | *You* are working on your own machine |
| Scope | Per-repository, per-permission, with an expiry date | Your full account access |
| Main risk | It's a secret: if it leaks it works until revoked or expired | Bound to the machine you logged in on |

Prefer **fine-grained** personal access tokens over classic tokens throughout — classic tokens grant broad, all-repository access with no expiry, which is far more than most integrations need.

### Creating a Fine-Grained Personal Access Token

1. Go to **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Give it a descriptive name (e.g., `claude-code-my-repo`)
4. Set an **expiration** — 30 or 90 days is a good default; avoid "No expiration"
5. Under **Repository access**, select **Only select repositories** and choose the specific repo(s) it needs — avoid "All repositories"
6. Under **Permissions**, grant only what's needed (e.g., **Contents: Read and write** for an agent that commits and pushes)
7. Click **Generate token**
8. **Copy the token now** — GitHub shows it exactly once and cannot show it to you again

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
