---
title: Terminal Basics
description: Learn essential command-line skills for macOS and Windows — navigation, commands, and paths
schema_type: HowTo
howto_steps:
  - name: Open your terminal
    text: "macOS: Press Cmd+Space, type Terminal, press Enter. Windows: Click Start, type PowerShell, click Windows PowerShell."
  - name: Open the terminal in your editor
    text: In Cursor or VS Code, press Ctrl+` (backtick) to open the integrated terminal panel.
  - name: Learn essential commands
    text: Practice pwd (print directory), ls (list files), cd (change directory), mkdir (create folder), and clear (clear screen).
  - name: Try the practice exercise
    text: Follow the guided exercise to navigate directories, create folders, and confirm your commands work.
---

# Terminal Basics

Get comfortable with the command line before diving into developer tools.

## What Is the Terminal?

The terminal is a text-based way to talk to your computer. Instead of clicking through menus and windows, you type commands and press Enter.

Why does this matter? Most developer tools — Git, Claude Code, and other builder tools — are designed to run from the terminal. Every setup guide that follows assumes you can open a terminal and type a command.

The good news: you only need a handful of commands to get started.

## Open Your Terminal

=== "macOS"

    You have two quick ways to open Terminal:

    1. **Spotlight Search**: Press ++cmd+space++, type `Terminal`, press Enter
    2. **Finder**: Open Applications > Utilities > Terminal

    You'll see a window with a short line of text ending in `$` or `%` and a blinking cursor. That's your **prompt** — it means the terminal is ready for a command.

=== "Windows"

    1. **Start Menu**: Click Start, type `PowerShell`, click **Windows PowerShell**
    2. **Windows Terminal** (if installed): Click Start, type `Terminal`, click **Terminal**

    You'll see a window with a line ending in `>` and a blinking cursor. That's your **prompt** — it means the terminal is ready for a command.

## Open the Terminal in Your Editor

!!! note "Come back after Step 2"
    This section requires a code editor. If you're following the [Builder Stack Setup Guide](index.md) in order, complete Step 2 (Editor Setup) first, then return here.

Once you have Cursor or VS Code installed, you can use the terminal directly inside your editor. This is where you'll spend most of your time — running commands without switching windows.

The steps are the same for both Cursor and VS Code:

1. Open Cursor or VS Code
2. Press ++ctrl+grave++ (the backtick key, to the left of 1 on most keyboards)
3. A terminal panel opens at the bottom of the editor

You can also open it from the menu: **Terminal > New Terminal**.

!!! tip "Keep it visible"
    Drag the top edge of the terminal panel to resize it. Many developers keep the terminal open at all times while they work.

## Essential Commands

These are the commands you'll use most often. macOS/Linux and Windows PowerShell use slightly different names for some of them.

=== "macOS / Linux"

    | Command | What It Does |
    |---------|-------------|
    | `pwd` | Print your current directory (where am I?) |
    | `ls` | List files and folders in the current directory |
    | `cd foldername` | Move into a folder |
    | `cd ..` | Go back up one level |
    | `cd ~` | Go to your home directory |
    | `mkdir foldername` | Create a new folder |
    | `clear` | Clear the screen |

=== "Windows PowerShell"

    | Command | What It Does |
    |---------|-------------|
    | `Get-Location` | Print your current directory (where am I?) |
    | `dir` | List files and folders in the current directory |
    | `cd foldername` | Move into a folder |
    | `cd ..` | Go back up one level |
    | `cd ~` | Go to your home directory |
    | `mkdir foldername` | Create a new folder |
    | `cls` | Clear the screen |

!!! tip "PowerShell aliases"
    PowerShell also accepts `pwd`, `ls`, and `clear` as shortcuts. If you see those commands in a guide, they'll work on Windows too.

## Try It Yourself

Open your terminal and follow along. This short exercise builds muscle memory with commands you'll use throughout these guides.

=== "macOS / Linux"

    ```bash
    # 1. Check where you are
    pwd

    # 2. List what's in this folder
    ls

    # 3. Move to your Desktop
    cd ~/Desktop

    # 4. Create a test folder
    mkdir terminal-test

    # 5. List again — you should see your new folder
    ls

    # 6. Move into it
    cd terminal-test

    # 7. Confirm you're inside
    pwd

    # 8. Go back up one level
    cd ..

    # 9. Clean up — remove the test folder
    rmdir terminal-test
    ```

=== "Windows PowerShell"

    ```powershell
    # 1. Check where you are
    Get-Location

    # 2. List what's in this folder
    dir

    # 3. Move to your Desktop
    cd ~\Desktop

    # 4. Create a test folder
    mkdir terminal-test

    # 5. List again — you should see your new folder
    dir

    # 6. Move into it
    cd terminal-test

    # 7. Confirm you're inside
    Get-Location

    # 8. Go back up one level
    cd ..

    # 9. Clean up — remove the test folder
    rmdir terminal-test
    ```

If every step worked, you're ready for the rest of the setup guides.

## Key Concepts

### Paths

A **path** describes the location of a file or folder on your computer.

- **Absolute path** — the full address from the root of your drive:
    - macOS: `/Users/yourname/Documents/project`
    - Windows: `C:\Users\yourname\Documents\project`
- **Relative path** — the address from wherever you are right now:
    - `cd Documents` (move into a Documents folder inside your current location)
    - `cd ../other-folder` (go up one level, then into a different folder)

Notice that macOS/Linux uses forward slashes (`/`) and Windows uses backslashes (`\`).

### The Prompt

The `$`, `%`, or `>` at the start of each line is the **prompt**. It means the terminal is waiting for your input. You don't type the prompt character — just the command after it.

### Case Sensitivity

- **macOS/Linux**: File and folder names are case-sensitive. `Documents` and `documents` are different folders.
- **Windows**: File and folder names are **not** case-sensitive. `Documents` and `documents` refer to the same folder.

### Tab Completion

Start typing a file or folder name and press ++tab++. The terminal will auto-complete the name if there's a match, or show you options if there are multiple matches. This saves typing and helps avoid typos.

## Troubleshooting

**"I typed a command and nothing happened"**

- Make sure you pressed Enter after the command
- Check for typos — commands must be spelled exactly right

**"command not found" or "not recognized"**

- The tool you're trying to use isn't installed, or your system doesn't know where to find it
- Follow the relevant installation guide, then try again

**"Permission denied"**

- You may need administrator rights
- On macOS, prefix the command with `sudo` (you'll be asked for your password)
- On Windows, right-click PowerShell and choose **Run as Administrator**

**"I'm lost and don't know where I am"**

- Run `pwd` (macOS/Linux) or `Get-Location` (Windows) to see your current directory
- Run `cd ~` to go back to your home directory
