---
date: 2026-09-19
authors:
  - jamesgray
tags:
  - Builder Setup
  - Courses
description: "Git and GitHub setup is now three numbered prerequisites — GitHub account, Git, GitHub CLI — each with a 'Done when' test; the checklist grows to ten steps."
title: "Git & GitHub setup, rebuilt as three prerequisites you can check off"
---

Setting up Git and GitHub used to be two pages that hid three separate jobs. It's now three guides, in the order you do them, each ending with a **Done when** block you can verify in under a minute:

1. [GitHub Account](/builder-setup/github-setup/) — browser only; sign up with a personal email and turn on 2FA
2. [Git](/builder-setup/git-install/) — install it and tell it who you are
3. [GitHub CLI](/builder-setup/github-cli-setup/) — install `gh` and log in once, with the exact prompts and expected output shown

What changed and why:

- **Success is defined.** The same three "Done when" tests appear on each guide, the [Builder Tools Setup](/builder-setup/) index, and the [Tools Setup Checklist](/courses/tools-setup-checklist/), which grows from 8 to 10 steps.
- **Mac users get the installer, not the binary.** cli.github.com's Mac download is a bare program file; the guide sends you to the signed `.pkg` on the releases page and says why. Windows users get the MSI from cli.github.com.
- **Beginner stalls removed.** The macOS "install developer tools?" popup is explained, the Windows installer no longer asks you to pick an editor that isn't offered, and both install pages tell you what a company laptop may need from IT.
- **Personal access tokens are optional.** They're only for when an AI agent or automation — not you — needs GitHub access, so they've moved to the end of the account guide.

If you set these up under the old guides, nothing changes on your machine — run the three Done-when tests and you're current.
