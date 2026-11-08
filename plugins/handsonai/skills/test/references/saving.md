# Saving through a connection

This applies wherever the working folder is reached through a connection (whatever storage service is connected in this chat) and not through files you write directly (Claude Code, Codex, a folder selected on Claude desktop). Name the service by its own name in every location ("Dropbox, in ai-workspace"). Rule 5 applies where nothing can be saved at all.

1. **Decide how to save from the tools this connection gives you; never test-write.** A tool that changes a file's contents: update in place. Only tools to create files and to move or rename them: the create-only path (move the current file into `history/` as `[file]-YYYY-MM-DD-HHMM.md`, then create the new one). No tool that creates files: print-to-save (N-F6, once).
2. **When you read a file you will save again, read its exact contents** (the tool that returns the file as stored, not a summary or a reformatted view). If you can only get a reformatted view, say so once and don't rewrite that file from it; give the change for the leader to apply.
3. **If a save returns an error, say so in one line and take the next path down** (in place, then create-only, then print-to-save). Never claim a save that returned an error.
4. **Never create a file only to test saving, and never delete one.**
5. **With nothing that can save (print-to-save),** where you can create a file the leader can download, give one zip of the working folder, its folders intact, at each save point (the end of a part, a pause, the close), each replacing the last, with N-F6 once; otherwise give each changed file complete, with N-F6. When the next step is given a zip, unpack it if you can; otherwise ask for the files.
6. **An HTML page in a drive shows as code when it's opened there.** Wherever you point the leader to `registry-dashboard.html` (or any HTML page) in a drive, say to download it and open it in their browser, or to open it from the drive's synced folder on their computer.
