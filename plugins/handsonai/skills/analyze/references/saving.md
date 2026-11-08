# Saving through a connection: which way to save

This applies wherever the working folder is reached through a connection (a storage service such as Google Drive, OneDrive, SharePoint, Dropbox or Box, or a GitHub connector) and not through files the AI writes directly (Claude Code, Codex, a folder selected on Claude desktop). It decides one thing: whether this chat saves by updating files in place, by the create-only path, or by print-to-save. The steps' own saving text says how each of those works.

1. **Any connection that can create files can be the home.** There is no list of allowed services. A connection that is on in this chat and has a tool that creates files may hold the working folder; one that can only read never does. Name the service by its own name in every location ("Dropbox, in ai-workspace").
2. **Known exceptions first.** Where you can read the platform registry, look up this platform's `capabilities.storage_quirks`; where you can't, go straight to the check (3). Where an entry for this service says files can't be updated in place, use the create-only path from the first save (or print-to-save, where it also says files can't be moved), with no check. An entry that says a service isn't available is never offered.
3. **Otherwise, check the first real saves, once per chat.** Never create a file only to test, and never delete one. After the first file this chat creates, read it back. After the first file this chat updates, read it back and confirm the new content is there. Say nothing while the checks pass.
4. **What follows from the check:**
   - The created file reads back, and the update took: update in place for the rest of the chat.
   - The update didn't take (the tool reported success, or failed, but the old content is still there), and the connection can move and rename files: the create-only path from now on. Redo that save the create-only way.
   - The update didn't take, and files can't be moved either; or the created file doesn't read back: print-to-save from now on, with that file given complete.
5. **Said only on a failure.** One line in your own words, that the last save didn't take and how this chat will save from now on; for print-to-save, N-F6 too, once. A later save that fails takes the same path down, never back up, for the rest of the chat.
6. **Never claim a save you didn't confirm.**
