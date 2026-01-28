# Claude Projects Setup Guide

Quick reference for creating and configuring Claude Projects for persistent context.

## What Are Projects?

Projects let you organize conversations around a specific topic or task. You can add:

- **Project Knowledge** — Documents, files, and code that Claude references in all chats
- **Project Instructions** — Custom guidelines that shape Claude's behavior

Projects are available on all plans. Free users can create up to 5 projects.

## Create a Project

1. Go to [claude.ai/projects](https://claude.ai/projects) or click **Projects** in the sidebar
2. Click **+ New Project** in the upper right
3. Enter a project name and description
4. For Team/Enterprise: choose visibility (private or shared)

## Add Project Knowledge

Project knowledge provides context for all conversations within the project.

1. Open your project
2. Click the **+** button in the project knowledge section (right side)
3. Upload documents, text files, or code
4. Files are now available to Claude in all project chats

**Tips:**
- Add all relevant documents upfront—more context helps Claude assist you better
- Use clear, descriptive file names so Claude can find the right information
- Paid plans automatically enable RAG mode when content approaches context limits

## Set Project Instructions

Project instructions guide Claude's behavior across all chats in the project.

1. Open your project
2. Click **Set project instructions**
3. Write your guidelines (tone, role, format preferences, etc.)
4. Save

**Example instructions:**
```
You are helping me with [specific task].

When responding:
- Use a professional tone
- Format code examples in Python
- Ask clarifying questions before making assumptions
```

**Note:** Context is not shared across individual chats within a project—only content in the project knowledge base is available to all chats.

## Organize Your Projects

**Star projects** — Click the ⋮ menu or star icon to mark frequently-used projects for quick access

**Move chats to projects** — Use the dropdown arrow next to a chat name to add standalone conversations to a project

**Archive projects** — Click ⋮ menu → Archive (archived projects appear at the bottom of your list)

**Delete projects** — Unarchive first, then use ⋮ menu to delete permanently

## Share Projects (Team/Enterprise)

1. Click **Share project** next to the project name
2. Add members by name or email
3. Choose permission level:
   - **Can use** — View contents and chat, but cannot edit
   - **Can edit** — Modify instructions, knowledge, and member settings
4. Shared projects appear in recipients' "Shared with me" tab

## Troubleshooting

**Claude isn't using my uploaded files?**
- Verify files uploaded successfully (check project knowledge section)
- Try asking Claude directly about the content: "What files do you have access to?"
- For large knowledge bases, Claude uses RAG—be specific in your questions

**Project instructions not being followed?**
- Check instructions are saved (re-open the project to verify)
- Be explicit and specific in your instructions
- Start a new chat within the project after updating instructions

**Can't share a project?**
- Sharing requires Team or Enterprise plan
- Verify you have edit permissions on the project

## Next Steps

- Review the course slide deck for detailed walkthrough
- Post in Slack if you encounter issues

## Resources

- [What Are Projects?](https://support.claude.com/en/articles/9517075-what-are-projects)
- [How to Create and Manage Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)
- [Project Visibility and Sharing](https://support.claude.com/en/articles/9519189-project-visibility-and-sharing)
- [Examples of Projects You Can Create](https://support.claude.com/en/articles/9529781-examples-of-projects-you-can-create)
