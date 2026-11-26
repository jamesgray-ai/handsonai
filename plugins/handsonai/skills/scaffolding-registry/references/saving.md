# Saving through a connection

This applies wherever the working folder is reached through a connection (whatever storage service is connected in this chat) and not through files you write directly (Claude Code, Codex, a folder selected on Claude desktop). Name the service by its own name in every location ("Dropbox, in ai-workspace"). Rule 5 applies where nothing can be saved at all.

1. **Decide how to save from the tools this connection gives you; never test-write.** A tool that changes a file's contents: update in place. Only tools to create files and to move or rename them: the create-only path (move the current file into `history/` as `[file]-YYYY-MM-DD-HHMM.md`, then create the new one). No tool that creates files: nothing can be saved here (rule 5).
2. **When you read a file you will save again, read its exact contents** (the tool that returns the file as stored, not a summary or a reformatted view). If you can only get a reformatted view, say so once and don't rewrite that file from it; give the change for the leader to apply.
3. **If a save returns an error, say so in one line and take the next path down** (in place, then create-only). When neither saves, say so plainly, keep what was captured in this chat, and follow rule 5. Never claim a save that returned an error.
4. **Never create a file only to test saving, and never delete one.**
5. **With nothing that can save,** say N-F16 and wait: the framework always saves to the leader's own storage (a drive such as Google Drive or OneDrive, a folder on their computer, or GitHub), and never hands files over for the leader to save by hand. Nothing is written until a place that can save is added.
6. **An HTML page in a drive shows as code when it's opened there.** Wherever you point the leader to `registry-dashboard.html` (or any HTML page) in a drive, say to download it and open it in their browser, or to open it from the drive's synced folder on their computer.
