---
title: Git Concepts Reference
description: What repository, commit, push, pull, branch, pull request, and merge actually mean — the vocabulary behind every Git command you run
---

## What This Page Covers

Seven words do most of the work in Git and GitHub. Once you can narrate the path a change takes through them, the commands stop being incantations you copy and start being steps you understand.

This is a reference, not a setup guide. Nothing here asks you to install or configure anything — see the [Git Installation Guide](../git-install/) and [GitHub Setup Guide](../github-setup/) for that.

The same seven concepts hold whether a repository stores application code or the prompts, skills, agents, and markdown you build with AI.

## The Seven Concepts

### Repository

A **repository** — "repo" — is the folder Git tracks. Everything inside it is versioned: every edit, every addition, every deletion, with a record of who made it and when.

A repository exists in two places at once. There is the **remote** copy on GitHub, and there is your **local** copy on your own machine. They are the same repository, and keeping them in step is what push and pull are for.

### Commit

A **commit** saves a snapshot of your changes with a message describing what you did. Think of it as a save point you can return to.

Commits are the unit of history. A good message matters more than most people expect, because the message is what your future self reads when trying to work out why something changed.

### Push

**Push** uploads your local commits to GitHub. Until you push, your changes exist only on your computer — and a laptop is not a backup.

### Pull

**Pull** downloads the latest changes from GitHub to your local copy. Do this before you start work, so you are building on what everyone else already has rather than on a stale version.

### Branch

A **branch** is a parallel version of the repository. You make one so you can work without touching the version everyone depends on — usually called `main`.

This is the concept that makes the rest safe. Experiment on a branch and the worst case is that you throw the branch away. Experiment directly on `main` and the worst case is considerably worse.

### Pull Request

A **pull request** proposes that the work on your branch be folded into `main`. It shows the **diff** — exactly which lines were added and removed — and gives other people somewhere to review and comment before anything lands.

> **Pull and pull request are not the same thing**, and the names actively mislead. A **pull** brings other people's finished work *down* to your machine. A **pull request** proposes your unfinished work *upward* for review. They move in opposite directions.

### Merge

**Merge** completes the journey: the reviewed branch is folded into `main`, and its commits become part of the main history. After a merge, everyone who pulls gets your work.

## Staging: One More Term

Before committing, you **stage** the files you want that commit to include. It lets you commit some changes now and leave others for later, rather than being forced to save everything at once.

## The Lifecycle of a Change

The concepts are stations on one path, and it is the same path every time:

1. **Pull** the current `main`, so you start from what everyone else has.
2. **Branch**, so your work is isolated.
3. Add or edit files, **committing** at each meaningful checkpoint.
4. **Push**, so the work leaves your machine.
5. Open a **pull request**, so the change can be reviewed.
6. **Merge** it into `main`.

Each step protects against something specific: pulling protects against building on a stale version, branching against breaking `main` while you experiment, committing against losing work, pushing against losing your machine, and review against unreviewed change reaching the version everyone depends on.

## Using an AI Assistant for Git Operations

Most AI coding tools can run these operations for you in plain language, so you rarely type the commands by hand. With Claude Code, for example:

- "Commit my changes with a descriptive message"
- "Push my commits to GitHub"
- "Pull the latest changes"
- "Show me what files have changed"

The assistant runs the underlying Git commands. Understanding what it is doing is still worth your time — when something goes wrong, the vocabulary above is what lets you read the error and say what you want instead.

## Next Steps

- Install Git (see [Git Installation Guide](../git-install/))
- Set up your GitHub account and credentials (see [GitHub Setup Guide](../github-setup/))
- Create and clone a repository (see [Repository Creation and Cloning Guide](../repo-creation-and-cloning/))

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
