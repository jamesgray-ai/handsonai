---
title: Scheduled Subagent Troubleshooting
description: "Troubleshoot scheduled Claude Code subagents on macOS and Windows — launchd and Task Scheduler errors, PATH problems, permissions, and missing log output."
---Common issues and solutions when running scheduled Claude Code subagents.

## First Step: Ask Claude Code

Before diving into manual troubleshooting, ask Claude Code to diagnose the problem:

```
My claude-research-daily subagent isn't working. Can you check what's wrong?
```

Claude Code can check your subagent's status, review logs, and identify common issues automatically.

## Quick Diagnosis Checklist

If you prefer to check manually:

- [ ] Is Claude Code authenticated? (Ask: "Are you authenticated?")
- [ ] Is the script executable? (macOS only)
- [ ] Is the schedule loaded/active?
- [ ] Are logs being created?
- [ ] Does the subagent work when run manually?

## Common Issues

### Both Platforms

#### Claude Code Authentication Expired

**Symptoms:**
- Subagent runs but produces no output
- Logs show authentication error

**Solution:**

Ask Claude Code: "Check if you're authenticated and help me log in if needed."

Or run directly:
```bash
claude auth status
claude auth login
```

After re-authenticating, your scheduled subagents will work again—no need to recreate them.

#### Subagent Runs But No Output File Created

**Symptoms:**
- Logs show subagent started
- No error messages
- Expected digest/report file doesn't exist

**Possible causes:**
1. **Wrong working directory** - Subagent can't find its configuration file
2. **Output path doesn't exist** - The reports folder wasn't created
3. **Subagent configuration issue** - Something in the subagent's markdown file needs adjustment

**Solutions:**

Ask Claude Code: "My claude-research-daily ran but I don't see the digest file. What happened?"

Or check manually:
1. Verify the subagent configuration file is in the working directory
2. Verify output directory exists (`~/reports/` or `C:\Users\YourName\reports\`)
3. Review logs to see what Claude actually did

#### Subagent Works Manually But Not On Schedule

**Symptoms:**
- Running the script directly works fine
- Scheduled runs fail or produce no output

**Solution:**

Ask Claude Code: "My claude-research-daily works when I run it manually but not on schedule. What's different?"

Common causes:
- Environment variables differ in scheduled context
- Working directory is wrong
- Path to `claude` command not found

### macOS-Specific Issues

#### Subagent Not Appearing in Schedule List

**Symptoms:**
- `launchctl list | grep claude` shows nothing
- You loaded the plist but nothing happened

**Solution:**

Ask Claude Code: "I tried to set up my claude-research-daily subagent but it's not showing up in launchctl. Can you check the plist file?"

Claude Code will validate the plist syntax and check that the Label matches the filename.

#### Permission Denied

**Symptoms:**
- Error: "Permission denied" in logs
- Script won't execute

**Solution:**

Ask Claude Code: "My claude-research-daily script has a permission denied error. Can you fix it?"

Or run:
```bash
chmod +x ~/scripts/ai-news-digest.sh
```

### Windows-Specific Issues

#### Task Shows But Doesn't Run

**Symptoms:**
- Task appears in Task Scheduler
- "Last Run Result" shows error code
- Task never actually executes

**Solution:**

Ask Claude Code: "My claude-research-daily task is in Task Scheduler but shows an error. What's wrong?"

Common fixes:
- Check "Run whether user is logged on or not" in task properties
- Uncheck "Start only if on AC power" if on a laptop
- Verify the script path is correct

#### PowerShell Execution Policy Error

**Symptoms:**
- Error about scripts being disabled

**Solution:**

Ask Claude Code: "I'm getting a PowerShell execution policy error with my subagent. How do I fix it?"

The task action should use:
```
powershell.exe -ExecutionPolicy Bypass -File "C:\Scripts\your-script.ps1"
```

## How to Check Logs

**Ask Claude Code:**
```
Show me the logs from my claude-research-daily subagent's last run.
```

Or:
```
Are there any errors in my subagent logs?
```

### Manual Log Commands (Reference)

**macOS:**
```bash
cat $(ls -t ~/Library/Logs/claude-subagents/*.log | head -1)
```

**Windows PowerShell:**
```powershell
Get-Content (Get-ChildItem "C:\Users\$env:USERNAME\Logs\claude-subagents\*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1)
```

## How to Remove a Subagent

**Ask Claude Code:**
```
Remove my claude-research-daily subagent completely, including all the files.
```

Claude Code will unload the schedule and delete the associated files for you.

### Manual Removal (Reference)

**macOS:**
```bash
launchctl unload ~/Library/LaunchAgents/local.claude.ainewsdigest.plist
rm ~/Library/LaunchAgents/local.claude.ainewsdigest.plist
rm ~/scripts/ai-news-digest.sh
```

**Windows:**
- Open Task Scheduler → Find task → Right-click → Delete
- Delete the script file from `C:\Scripts\`

## Getting Help

If you've tried the above and still have issues:

1. **Ask Claude Code for a full diagnosis:**
   ```
   My claude-research-daily subagent isn't working. Run a full diagnosis and
   tell me everything that might be wrong.
   ```

2. **Test Claude Code directly:**
   ```bash
   cd ~/agents/ai-news
   claude -p "Test: what's the latest AI news today?"
   ```
   If this fails, the issue is with Claude Code itself, not the scheduling.

3. **Post in the course Slack** with:
   - Your operating system
   - The error message (exact text)
   - What you've already tried
