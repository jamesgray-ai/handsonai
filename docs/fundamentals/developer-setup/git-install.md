# Git Installation Guide

Quick reference for installing Git on your local machine.

## Check If Git Is Already Installed

Open your terminal and run:

```bash
git --version
```

If you see a version number (e.g., `git version 2.39.0`), Git is already installed. You can skip to verification.

## macOS

### Option 1: Xcode Command Line Tools (Recommended)

1. Open Terminal
2. Run: `xcode-select --install`
3. Click **Install** in the popup dialog
4. Wait for installation to complete

This installs Git along with other developer tools.

### Option 2: Homebrew

If you have Homebrew installed:

```bash
brew install git
```

## Windows

### Download and Install

1. Go to [git-scm.com](https://git-scm.com)
2. Click **Download for Windows**
3. Run the installer
4. Use the default settings (click Next through the prompts)
5. Complete the installation

### Important Settings During Install

- **Default editor**: Choose your preferred editor or keep the default
- **PATH environment**: Select "Git from the command line and also from 3rd-party software" (recommended)
- **Line endings**: Select "Checkout Windows-style, commit Unix-style line endings" (recommended)

## Verify Installation

After installing, open a new terminal window and run:

```bash
git --version
```

You should see a version number confirming Git is installed.

## Configure Your Identity

Set your name and email for Git commits:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the same email address associated with your GitHub account.

## Troubleshooting

**Command not found (Mac)?**
- Close and reopen Terminal after installation
- Try running `xcode-select --install` again

**Command not found (Windows)?**
- Close and reopen your terminal
- Make sure you selected the PATH option during installation
- Reinstall and select "Git from the command line and also from 3rd-party software"

**Permission errors?**
- On Mac, you may need to enter your password during Xcode tools installation
- On Windows, run the installer as Administrator

## Next Steps

- Set up your GitHub account (see GitHub Setup Guide)
- Install your code editor (see Editor Setup Guide)
- Post in Slack if you encounter issues

## Resources

- [Git Downloads](https://git-scm.com/downloads)
- [Git Documentation](https://git-scm.com/doc)
