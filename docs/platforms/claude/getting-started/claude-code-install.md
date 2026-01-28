# Claude Code Setup Guide

Quick reference for setting up Claude Code in your editor and terminal.

**Official docs:** [claude.ai/code/docs/quickstart](https://code.claude.com/docs/en/quickstart)

## Prerequisites

- Code editor installed (Cursor or VS Code)
- Git installed (see Git Installation Guide)
- Claude Pro, Max, or Team subscription

## Part 1: Install the Claude Code Extension

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

After installation, you may need to configure your PATH so the `claude` command works from any directory.

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

1. Close and reopen PowerShell or CMD
2. If still not working, you may need to log out and log back in

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

Then start an interactive session:

```bash
cd /path/to/your/project
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

- Review the course slide deck for detailed walkthrough
- Try the common workflows in the official docs
- Post in Slack if you encounter issues

## Resources

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart)
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
