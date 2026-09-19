---
title: GitHub Account Setup Guide
description: Create a GitHub account and turn on two-factor authentication — the first of three prerequisites, done entirely in your browser
schema_type: HowTo
howto_steps:
  - name: Create your GitHub account
    text: Go to github.com, click Sign up, use a personal email address, follow the prompts, and verify your email.
  - name: Turn on two-factor authentication
    text: In Settings → Password and authentication, enable two-factor authentication with an authenticator app, the GitHub mobile app, or a passkey, and save your recovery codes.
  - name: Confirm you're done
    text: You can sign in, there is no verify-your-email banner, and Settings → Password and authentication shows two-factor authentication Enabled.
---

**Prerequisite 1 of 3.** This guide creates your GitHub account. There is nothing to install — it all happens in your browser. [Git](../git-install/) and the [GitHub CLI](../github-cli-setup/) come next.

:::note[Looking for the GitHub CLI?]
Installing and logging in to the GitHub CLI (the `gh` program) now has its own guide: [GitHub CLI Setup](../github-cli-setup/).
:::

## What Is GitHub?

GitHub is a website where people store, version, and share files — application code, but equally the prompts, skills, agents, and markdown you build with AI. If Git tracks your changes locally (like a save history on your computer), GitHub is where that history lives in the cloud — backed up, shareable, and accessible from anywhere.

As you build with AI, you'll create prompts, skills, agents, and project files that become the foundation of your workflows. GitHub is where those files live in the cloud — backed up, versioned, and accessible from any machine. Think of it as your portfolio and safety net in one place. Your files are stored in *repositories* (project folders that Git tracks), and you work with them by *cloning* — making a local copy on your computer.

## Prerequisites

1. An email address — ideally a personal one (Step 1 explains why)
2. Your phone, for two-factor authentication

## Step 1: Create Your GitHub Account

1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Enter your email. **Use a personal email address** — this account belongs to you, not your employer, and you keep it when you change jobs. You can add a work email later under **Settings → Emails**.
4. Follow the prompts to choose a username and password
5. Verify your email — GitHub sends a code or a link. Until you do, the site shows a yellow "Please verify your email address" banner.
6. **Write down the email address you used.** The Git guide asks for it in its identity step.

**Already have an account?** Make sure 2FA is on (Step 2), then jump to [Done When](#done-when).

## Step 2: Turn On Two-Factor Authentication (2FA)

1. Click your profile picture (top right) → **Settings** → **Password and authentication**
2. Under **Two-factor authentication**, click **Enable two-factor authentication**
3. Choose a method — any of these works:
   1. **Authenticator app** (recommended): Microsoft Authenticator, Google Authenticator, Authy, or 1Password. If your company uses Microsoft 365, you probably already have Microsoft Authenticator on your phone.
   2. **GitHub Mobile** app
   3. **Passkey** (Face ID, Touch ID, or Windows Hello)
4. Follow the prompts — for an authenticator app, scan the QR code and enter the six-digit code it shows
5. Save the recovery codes GitHub shows you somewhere safe (a password manager, not a text file) — you'll need one if you lose your phone
6. Tip: once 2FA is set up, you can also install the **GitHub mobile app**, sign in, and add it as a second method under **Settings → Password and authentication** — future sign-ins become a single tap on your phone instead of typing a code

<details>
<summary>Want to keep your email address private on GitHub? (optional)</summary>

GitHub's **Keep my email addresses private** setting (under **Settings → Emails**) gives you a substitute address ending in `@users.noreply.github.com`. If you turn it on, use that substitute address when the Git guide asks for your email:

```bash
git config --global user.email "12345678+yourusername@users.noreply.github.com"
```

Otherwise, if the companion setting **Block command line pushes that expose my email** is on, GitHub rejects pushes made with your real email (`error: GH007`).

</details>

## Done When

| Prerequisite | Done when |
|---|---|
| **1. GitHub account** | You can sign in at github.com, there is no "verify your email" banner, and **Settings → Password and authentication** shows two-factor authentication **Enabled** |

**Next:** [Install Git](../git-install/) — prerequisite 2 of 3.

---

## Troubleshooting

**Didn't get the verification email?**
- Check your spam folder, then click **Resend** in the yellow banner at the top of github.com

**Lost access to your authenticator?**
- Sign in with one of the recovery codes you saved, then set up 2FA again under **Settings → Password and authentication**

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm creating a GitHub account and turning on two-factor authentication, and I'm getting this error: [paste the error message]. What should I try?

</details>

## Later: Give an Agent or Tool Access (Optional)

**You do not need this to finish setup.** Come back here only when something *other than you* — an AI agent, an automation, or a hosted tool — needs to reach GitHub on your behalf. Nothing here requires installing anything.

### Why an agent needs its own credential

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

**If you generate a token, make it a fine-grained one.** GitHub offers two kinds. The older "classic" tokens reach every repository you can reach and grant broad permission scopes. Fine-grained tokens only ever grant the specific repositories and permissions you tick — even at their widest setting.

### Creating a Fine-Grained Personal Access Token

1. Go to **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Give it a descriptive name (e.g., `claude-code-my-repo`)
4. Choose the **Resource owner** — your personal account, or an organisation if the repository belongs to one. If your own username is the only option, choose it — that's the normal case on a personal account. Organisation-owned tokens usually need an admin to approve them before they work, which can take days; start early if that applies to you.
5. Set an **expiration** that outlasts whatever you're building with it — if you're on a course, set it past the last session; otherwise 30 or 90 days is a good default. On a personal account GitHub also offers **No expiration** — skip it; an expiry date is your safety net if the token ever leaks. Pick deliberately either way: a token that lapses mid-project silently breaks every integration using it. (Tokens for organisation-owned repositories are usually capped at 366 days by the organisation's policy.)
6. Set **Repository access** — **Only select repositories**, and choose just the repo(s) needed. Create the repository first if it doesn't exist yet (see the [Repository Creation and Cloning Guide](../repo-creation-and-cloning/)); you can't select one that isn't there.

   **All repositories** also exists, and covers current *and future* repositories — occasionally useful on a personal account holding nothing you care about, when you want a token that keeps working as you add repos. Two reasons to prefer selecting: many tools that consume a token require a specific repository anyway (Notion's Claude agent connector, for one, states this on its connect screen), and on any account holding real work the wider scope is a genuine risk. Never point a token at an organisation's full repository list to save a step.
7. Under **Permissions**, grant only what's needed. The tool you're connecting will list the permissions it requires — treat that list as authoritative. Two you'll meet often: **Contents** (read and write files) and **Pull requests** (open a pull request instead of writing straight to the main branch), each set to **Read and write**. GitHub adds **Metadata: Read** automatically.
8. Click **Generate token**
9. **Copy the token now** — GitHub shows it exactly once and cannot show it to you again

### Storing Your Token Safely

Save the token in a password manager (1Password, Bitwarden, etc.) — not in a plain text file, a document, or a note on your computer. If a hosted agent or tool needs the token, paste it directly into that tool's credential/secret field rather than writing it to disk in your repository.

### Troubleshooting Tokens

**Token doesn't work?**
- Confirm the token hasn't expired
- Confirm the repository you're targeting is one of the repositories the token was scoped to
- Confirm the token has the permission the operation needs (e.g., **Contents: Read and write** to push commits)

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I created a fine-grained personal access token on GitHub for [name of the tool or agent], and it's getting this error: [paste the error message]. What should I check?

</details>

## Resources

- [GitHub Docs](https://docs.github.com)
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
