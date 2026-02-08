---
title: AI Coding CLI Installation Guide
description: Install Claude Code and other AI coding CLIs (OpenAI Codex, Gemini CLI) on macOS, Linux, or Windows
schema_type: HowTo
howto_steps:
  - name: Install the Claude Code extension
    text: Open the Extensions panel (Cmd/Ctrl + Shift + X), search for Claude Code, and click Install.
  - name: Install the CLI
    text: Run the install command for your OS — curl on macOS/Linux or irm on Windows PowerShell.
  - name: Set up your PATH
    text: Ensure the claude command is available from any directory by configuring your shell profile or system PATH.
  - name: Log in
    text: Run 'claude' in your terminal and authenticate through the browser with your Claude subscription.
  - name: Verify installation
    text: Run 'claude --version' to confirm the CLI is working, then start an interactive session.
---

# AI Coding CLI Setup Guide

Quick reference for setting up Claude Code in your editor and terminal.

**Official docs:** [code.claude.com/docs/en/quickstart](https://code.claude.com/docs/en/quickstart)

## Prerequisites

- Code editor installed (Cursor or VS Code)
- Git installed (see Git Installation Guide)
- Claude Pro, Max, or Team subscription

## Part 1: Install the Claude Code Extension

!!! tip "Already done?"
    If you installed the Claude Code extension during Step 2 (Editor Setup), skip to Part 2.

The Claude Code extension works the same in both Cursor and VS Code.

1. Open the Extensions panel (Cmd/Ctrl + Shift + X)
2. Search for **Claude Code**
3. Click **Install**
4. Follow any sign-in prompts

Once installed, you'll use Claude Code through the integrated terminal in your editor.

## Part 2: CLI Installation

The Claude Code CLI lets you use Claude directly in your terminal.

### macOS / Linux

Open Terminal and run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Windows PowerShell

Open PowerShell and run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

### Windows CMD

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

## Set Up Your PATH

Your PATH is a list of folders your computer checks when you type a command. If Claude Code's folder isn't in that list, your terminal won't recognize the `claude` command.

After installation, you may need to configure your PATH so `claude` works from any directory.

### macOS / Linux

The installer usually updates your shell profile automatically. If `claude` isn't recognized:

1. Close and reopen your terminal, or
2. Run one of these commands depending on your shell:

```bash
# For zsh (default on modern Macs)
source ~/.zshrc

# For bash
source ~/.bashrc
```

If the command still isn't found, add Claude Code to your PATH manually:

```bash
# For zsh
echo 'export PATH="$HOME/.claude/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export PATH="$HOME/.claude/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Windows

The installer should add Claude Code to your PATH automatically. If `claude` isn't recognized:

To add it manually:
1. Press Win + R, type sysdm.cpl, press Enter
2. Go to Advanced > Environment Variables
3. Under "User variables", select Path > Edit
4. Click New and add %USERPROFILE%\.local\bin
5. Restart your terminal

!!! note "Windows users"
    You need [Git for Windows](https://git-scm.com/downloads/win) installed — it provides Git Bash, which Claude Code requires. If Git Bash isn't detected, open PowerShell and run:

    ```powershell
    $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
    ```

## Log In

Start Claude Code and log in with your Claude account:

```bash
claude
```

You'll be prompted to authenticate in your browser. Follow the prompts to connect your Claude subscription.

Once logged in, your credentials are stored and you won't need to log in again.

## Verify Installation

Test that everything is working:

```bash
claude --version
```

Then start a conversation with Claude:

```bash
cd ~/Desktop/my-project  # replace with your actual project folder
claude
```

Ask Claude a question to confirm it's working:

```
> what does this project do?
```

## Troubleshooting

**"command not found: claude"**
- Close and reopen your terminal
- On Mac, run `source ~/.zshrc` or `source ~/.bashrc`
- Check the PATH setup section above

**Authentication fails**
- Make sure you have an active Claude Pro, Max, or Team subscription
- Try running `/login` inside Claude Code to re-authenticate
- Check your browser completed the authentication flow

**Permission denied during install (Mac/Linux)**
- The install script may need sudo access
- Try: `curl -fsSL https://claude.ai/install.sh | sudo bash`

**Slow or hanging responses**
- Check your internet connection
- Try exiting (`Ctrl+C`) and starting a new session

**Installation succeeded but claude command hangs**
- Ensure you're in a directory with a project (not an empty folder)
- Try `claude --help` to verify the CLI responds

## Essential Commands

| Command | What it does |
|---------|--------------|
| `claude` | Start interactive mode |
| `claude "task"` | Run a one-time task |
| `claude -c` | Continue most recent conversation |
| `claude commit` | Create a Git commit |
| `/help` | Show available commands (inside Claude Code) |
| `/login` | Re-authenticate (inside Claude Code) |
| `exit` or Ctrl+C | Exit Claude Code |

## Next Steps

- Explore the [Claude Code documentation](https://code.claude.com/docs/en/quickstart) for more workflows
- Try asking Claude to explain a project, commit changes, or write tests

## Resources

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)

---

## Other AI Coding CLIs

Claude Code is the primary CLI covered in this cookbook, but you may also want to install these alternatives.

### OpenAI Codex CLI

OpenAI's command-line coding agent.

**Prerequisites:** Requires [Node.js](https://nodejs.org/) 22+ (which includes npm, the package manager used to install it) and an OpenAI API key.

**Install (macOS / Linux):**

```bash
npm install -g @openai/codex
```

**Verify:**

```bash
codex --version
```

**Authenticate:**

```bash
export OPENAI_API_KEY="your-api-key"
```

See the [Codex CLI documentation](https://github.com/openai/codex) for full setup.

### Gemini CLI

Google's command-line AI coding assistant.

**Prerequisites:** Requires [Node.js](https://nodejs.org/) 18+ (which includes npm) and a Google account.

**Install (macOS / Linux):**

```bash
npm install -g @google/gemini-cli
```

**Verify:**

```bash
gemini --version
```

See the [Gemini CLI documentation](https://github.com/google-gemini/gemini-cli) for full setup.
