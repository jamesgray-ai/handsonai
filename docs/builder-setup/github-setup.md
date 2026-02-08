---
title: GitHub Setup Guide
description: Create a GitHub account, clone repositories, and learn core Git concepts for AI development
schema_type: HowTo
howto_steps:
  - name: Create a GitHub account
    text: Go to github.com, click Sign up, follow the prompts, and verify your email address.
  - name: Clone a repository
    text: Open the Command Palette (Cmd/Ctrl + Shift + P), type Git Clone, paste the repository URL, and choose a local folder.
---

# GitHub Setup Guide

Quick reference for setting up GitHub for your projects.

## Prerequisites

- Email address for GitHub account
- Cursor or VS Code installed (see [Editor Setup Guide](editor-setup.md))
- Git installed (see [Git Installation Guide](git-install.md))

## 1. Create a GitHub Account

1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Follow the prompts to create your account
4. Verify your email address

**Already have an account?** Skip to step 2.

## 2. Clone a Repository

Use your code editor to download (clone) repositories from GitHub.

### In Cursor or VS Code

1. Open the Command Palette (Cmd/Ctrl + Shift + P)
2. Type **Git: Clone**
3. Paste the repository URL (e.g., `https://github.com/username/project-name.git`)
4. Choose a local folder location
5. Open the cloned repository when prompted

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

**Can't clone the repository?**
- Verify you have access to the repository
- Check that the URL is correct
- Make sure you're signed into GitHub in your editor

**Authentication issues?**
- Your editor may prompt you to sign into GitHub
- Follow the browser authentication flow when prompted

## Next Steps

- Install Claude Code to manage Git operations with natural language (see [AI Coding CLIs Guide](claude-code-install.md))
- Try cloning a public repository to practice the workflow

## Resources

- [GitHub Docs](https://docs.github.com)
