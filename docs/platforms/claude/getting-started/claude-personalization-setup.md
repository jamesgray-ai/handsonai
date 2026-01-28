# Claude Personalization and Memory Setup Guide

Quick reference for configuring Claude's personalization features and memory.

## Overview

Claude offers three personalization features:

| Feature | Scope | Availability |
|---------|-------|--------------|
| **Profile Preferences** | All conversations | All plans |
| **Memory** | Standalone chats + per-project | Pro, Max, Team, Enterprise |
| **Styles** | Response format/tone | All plans |

## Part 1: Profile Preferences

Profile preferences are account-wide settings that apply to all your conversations.

### Set Up Profile Preferences

1. Click your initials (lower left corner)
2. Go to **Settings**
3. Find **"What preferences should Claude consider in responses?"**
4. Enter your preferences and save

### What to Include

- Your role and professional context
- Preferred communication style (concise, detailed, formal, casual)
- Common terms or concepts you use
- Typical scenarios you encounter
- Technical preferences (languages, frameworks, tools)

**Example:**
```
I'm a product manager at a SaaS company. I prefer concise responses
with bullet points. When discussing technical topics, explain concepts
simply—I'm not a developer. Default to Slack-friendly formatting.
```

## Part 2: Memory

Memory lets Claude remember context across conversations, building on what you've discussed before.

**Available on:** Pro, Max, Team, Enterprise (web, desktop, mobile)

### Enable Memory

1. Go to **Settings → Capabilities**
2. Toggle **Memory** on
3. Grant any permissions if prompted

**Note:** Enterprise members can only enable memory when their organization Owner has activated it.

### How Memory Works

- Claude automatically summarizes your conversations
- Creates a synthesis of key insights across your chat history
- Updates every 24 hours
- Provides context for new standalone conversations
- Each project has its own separate memory space

### What Claude Remembers

Claude focuses on work-related context:
- Your role, projects, and professional context
- Communication and working style preferences
- Technical and coding preferences
- Project details and ongoing work

### View and Edit Memory

1. Go to **Settings → Capabilities**
2. Click **"View and edit memory"**
3. Review what Claude remembers
4. Edit summaries directly or add specific information

**Tip:** You can also tell Claude to remember something mid-conversation: "Remember that I prefer Python over JavaScript."

### Manage Memory

**Pause memory** — Claude keeps existing memories but won't use them or create new ones

**Reset memory** — Permanently deletes all memories (cannot be undone)

To access these options, toggle memory off in Settings → Capabilities.

## Part 3: Styles

Styles customize how Claude formats and delivers responses.

### Create a Custom Style

1. Go to **Settings → Styles**
2. Click **Create style**
3. Define your preferred format and tone
4. Save and apply to conversations

### Use Cases

- Switch between concise and detailed responses
- Match your writing style for drafts
- Adjust tone for different contexts (professional, casual)

## Chat Search (Paid Plans)

Memory includes the ability to search past conversations.

1. Go to **Settings → Capabilities**
2. Ensure **"Search and reference chats"** is enabled
3. Ask Claude naturally: "What did we discuss about the Q3 roadmap?"

Claude uses RAG to find relevant past conversations.

## Troubleshooting

**Memory not available?**
- Requires Pro, Max, Team, or Enterprise plan
- Check Settings → Capabilities to enable
- Enterprise users: verify your admin has enabled the feature

**Claude not remembering things?**
- Memory updates within 24 hours of conversations
- Project chats have separate memory from standalone chats
- Check "View and edit memory" to see what's stored

**Want to exclude a conversation from memory?**
- Use incognito mode for chats you don't want saved
- Deleted conversations are removed from memory synthesis

## Next Steps

- Review the course slide deck for detailed walkthrough
- Post in Slack if you encounter issues

## Resources

- [Understanding Claude's Personalization Features](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features)
- [Using Claude's Chat Search and Memory](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context)
- [Importing and Exporting Your Memory](https://support.claude.com/en/articles/12123587-importing-and-exporting-your-memory-from-claude)
