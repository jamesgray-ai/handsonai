---
title: Voice-to-Text Setup Guide
description: Set up Wispr Flow or Claude Desktop Quick Entry for hands-free AI voice input
schema_type: HowTo
howto_steps:
  - name: Choose your voice input tool
    text: Pick Wispr Flow (Mac/Windows, dictates anywhere) or Claude Desktop Quick Entry (Mac only, speaks directly to Claude).
  - name: Install the app
    text: Download Wispr Flow from wisprflow.ai or install Claude Desktop from claude.ai/download.
  - name: Grant permissions
    text: Allow microphone access and configure your preferred activation method (keyboard shortcut or push-to-talk).
  - name: Test dictation
    text: Activate voice input and speak naturally. Verify transcription accuracy in a text field or Claude chat.
---

## Why Voice Input?

Writing good AI prompts often means describing complex ideas, explaining context, or thinking through a problem out loud. Voice input lets you speak those thoughts naturally — it's faster than typing and often more detailed, because talking feels more like having a conversation than writing a document.

This is especially useful when giving an AI assistant rich context: *"I'm working on a marketing email for next week's product launch, and I need three subject line options that emphasize urgency..."* — prompts like that flow naturally from speech but take effort to type.

This guide covers two options: **Wispr Flow** (dictates anywhere on your computer) and **Claude Desktop Quick Entry** (speaks directly to Claude on macOS).

## Option 1: Wispr Flow

Wispr Flow lets you dictate text anywhere on your computer using your voice.

### Install Wispr Flow

1. Go to [Wispr Flow](https://ref.wisprflow.ai/james-gray)
2. Download the app for your operating system
3. Run the installer
4. Launch Wispr Flow

### Configure Wispr Flow

1. Grant microphone permissions when prompted
2. Set your preferred activation method (keyboard shortcut or push-to-talk)
3. Open any text field (an email, a browser search bar, a note), activate voice input, and say a short test sentence

**You're done when:** your spoken words appear as typed text in whatever field you picked.

### Tips for Wispr Flow

- Speak naturally—Wispr Flow handles punctuation and formatting
- Use the keyboard shortcut to start and stop dictation
- Works in any application (editors, browsers, chat apps)

## Option 2: Claude Desktop Quick Entry (macOS Only)

Claude Desktop has a Quick Entry feature that lets you access Claude from anywhere on your Mac, including voice dictation.

**Requirements:**
- macOS 12 or later (macOS 14+ required for voice dictation)
- Claude Desktop installed and running

**Note:** Quick Entry is currently only available for macOS. Windows users can use Claude Desktop but without quick entry features.

### Enable Quick Entry

1. Open Claude Desktop
2. You'll be prompted to turn on the shortcut—click **Continue**
3. Grant permissions when prompted (accessibility, screen recording, speech recognition)
4. Manage settings in **Settings → General**

### Configure Voice Shortcut

1. Go to **Settings → General**
2. Find **Voice shortcut** (disabled by default since it overrides Caps Lock)
3. Enable and set your preferred key (default is Caps Lock)

### Using Voice Input

1. Press your voice shortcut key (e.g., Caps Lock) to start dictation
2. Speak your prompt
3. Press the shortcut key again to stop
4. Review and adjust the transcription if needed
5. Press Enter or click the send button to run

Claude Desktop launches with your transcribed prompt and responds.

**You're done when:** Claude Desktop opens with your spoken words transcribed as a prompt, and Claude responds to it.

### Tips for Claude Desktop Voice

- Use voice for longer prompts or when you want to think out loud
- The shortcut works from anywhere on your Mac—Claude opens automatically
- Review the transcription before sending
- You can also use **Quick access shortcut** (double-tap Option) to open Claude without voice

**Learn more:** [Use Quick Entry with Claude Desktop on Mac](https://support.claude.com/en/articles/12626668-use-quick-entry-with-claude-desktop-on-mac)

## When to Use Each

| Tool | Platform | Best For |
|------|----------|----------|
| **Wispr Flow** | Mac, Windows | Dictating anywhere—code editors, documents, emails, terminal |
| **Claude Desktop Quick Entry** | Mac only | Speaking directly to Claude from anywhere on your desktop |

## Troubleshooting

**Microphone not detected**
- Check system privacy settings for microphone access
- Grant permissions to the specific app

**Poor transcription accuracy**
- Speak clearly and at a steady pace
- Reduce background noise
- Check microphone input levels in system settings

**Voice input not activating**
- Verify the keyboard shortcut isn't conflicting with another app
- Restart the application

<details>
<summary>Ask AI for help</summary>

If you're stuck, paste this into ChatGPT, Claude, or Gemini:

> I'm setting up [Wispr Flow / Claude Desktop Quick Entry] on [Mac / Windows] for voice-to-text and running into this issue: [describe what's happening]. I granted microphone permissions. What should I check?

</details>
## Next Steps

- Practice dictating a few prompts to get comfortable
- Explore the official documentation for your chosen tool

## Resources

- [Wispr Flow](https://ref.wisprflow.ai/james-gray)
- [Claude Desktop](https://claude.ai/download)
