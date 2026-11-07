---
title: Code Editor Setup Guide
description: "Optional: install Cursor or VS Code to browse and edit your files alongside your AI platform — download, first launch, and AI extensions."
schema_type: HowTo
howto_steps:
  - name: Choose your editor
    text: Pick Cursor (AI-first editing) or VS Code (free, familiar). Both work for AI development.
  - name: Download and install
    text: Go to cursor.com or code.visualstudio.com, download for your OS, and run the installer.
  - name: Verify installation
    text: Open your editor, go to File > Open Folder, and confirm you can navigate files and folders.
  - name: Open the terminal in your editor
    text: Press Ctrl+` (backtick) to open the integrated terminal panel at the bottom of your editor.
  - name: Install AI extensions
    text: Add AI coding extensions — Claude Code, OpenAI Codex, or Gemini Code Assist.
---

:::note[Optional]
You don't need a code editor for a Hands-on AI course. The **Code** tab in the Claude desktop app and the **Codex** tab in the ChatGPT desktop app already work with the files on your computer. Install an editor when you want a second window for browsing and editing those files.
:::

## What Is a Code Editor?

A code editor is a text editor built for working with files of instructions rather than documents. It gives you a file browser, a place to read and edit files, and a built-in terminal, all in one window.

It's useful alongside your AI platform: you can see every file the AI creates or changes, organized in folders, and edit Markdown files directly. Many editors have AI built in or support AI extensions that read and edit files alongside you.

This guide covers **Cursor** and **VS Code**, and how to add AI extensions for the platforms you use.

## Choose Your Editor

Both options work well:

| Editor | Best For | Cost |
|--------|----------|------|
| **Cursor** | Built-in AI editing | Free tier available |
| **VS Code** | Familiar editor + extensions | Free |

## Option 1: Cursor

Cursor is VS Code with AI capabilities built in.

### Install Cursor

1. Go to [cursor.com](https://cursor.com)
2. Download for your operating system
3. Run the installer
4. Launch Cursor

New to Cursor? The [Cursor Documentation](https://docs.cursor.com) covers the interface layout, settings, and keyboard shortcuts.

## Option 2: VS Code

### Install VS Code

1. Go to [code.visualstudio.com](https://code.visualstudio.com)
2. Download for your operating system
3. Run the installer
4. Launch VS Code

New to VS Code? The [Getting Started guide](https://code.visualstudio.com/docs/getstarted/getting-started) covers the interface layout, settings, and keyboard shortcuts.

## Verify Installation

1. Open your editor (Cursor or VS Code)
2. Go to **File → Open Folder** and select any folder on your computer (e.g., your Desktop)
3. Confirm you see the folder's contents in the **sidebar** (left panel) — you should see files and subfolders listed
4. Try clicking a file in the sidebar to open it in the editor

If the sidebar shows your files, your editor is working correctly.

## Open the Terminal in Your Editor

Your editor has a terminal built in, so when a guide asks you to run a command, you can do it without switching windows.

The steps are the same for both Cursor and VS Code:

1. Open Cursor or VS Code
2. Press **Ctrl + `** (the backtick key, to the left of 1 on most keyboards)
3. A terminal panel opens at the bottom of the editor

You can also open it from the menu: **Terminal > New Terminal**.

Drag the top edge of the terminal panel to resize it.

## Install AI Extensions

After installing your editor, add AI coding extensions (small add-ons that give your editor new capabilities) for the platforms you have a **paid subscription** to. You don't need all of these — just install the one(s) that match your accounts.

### Claude Code

Requires a **paid Claude plan**. The Claude Code extension connects your editor to Claude's AI capabilities.

1. Open the Extensions panel (**Cmd/Ctrl + Shift + X**)
2. Search for **Claude Code**
3. Click **Install**
4. Follow any sign-in prompts

The Claude Code extension also includes an integrated terminal panel. See [Getting Started with Claude](../../platforms/claude/getting-started/#3-install-claude-code) for Claude Code CLI setup.

### OpenAI Codex

Requires a **paid ChatGPT plan**. OpenAI's coding assistant extension for VS Code and Cursor.

1. Open the Extensions panel (**Cmd/Ctrl + Shift + X**)
2. Search for **Codex** (by OpenAI)
3. Click **Install**
4. Sign in with your OpenAI account when prompted

See [OpenAI Codex documentation](https://openai.com/index/codex/) for details.

### Gemini Code Assist

Google's AI coding assistant extension. Sign in with your Google account; Google's documentation lists which plans include it.

1. Open the Extensions panel (**Cmd/Ctrl + Shift + X**)
2. Search for **Gemini Code Assist**
3. Click **Install**
4. Sign in with your Google account when prompted

See [Gemini Code Assist documentation](https://cloud.google.com/products/gemini-code-assist) for details.

## Troubleshooting

**Editor won't open after installation?**

- Restart your computer and try again
- Re-download the installer from the official site and reinstall
- On Mac, you may need to allow the app in **System Settings → Privacy & Security**

**Extension not appearing after install?**

- Make sure you clicked **Install** (not just searched for it)
- Check the **Installed** tab in the Extensions panel to confirm it's listed
- Try reloading the editor window: open the Command Palette (**Cmd/Ctrl + Shift + P**) and type **Developer: Reload Window**

**Extension installed but not working?**

- Check if the extension requires sign-in — look for a notification or status bar icon
- Some extensions need an API key or subscription (e.g., Claude Code requires a paid Claude plan)
- Disable other AI extensions temporarily to rule out conflicts

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm setting up [Cursor / VS Code] on [Mac / Windows] and running into this issue: [describe what's happening]. I followed the installation steps from the official site. What should I try next?

</details>

## Next Steps

Want to back up your files and keep their history? That's optional too, and takes three pieces, in this order:

- Create your GitHub account (see [GitHub Account Setup Guide](../github-setup/))
- Install Git (see [Git Installation Guide](../git-install/))
- Install the GitHub CLI (see [GitHub CLI Setup Guide](../github-cli-setup/))

## Resources

- [Cursor Documentation](https://cursor.com/docs)
- [VS Code Documentation](https://code.visualstudio.com/docs)
