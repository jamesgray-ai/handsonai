A10 = "This step aims to find 3 to 5 **candidate workflows**: pieces of work worth building with AI, such as work that eats time or slips, or work you'd do more of if you could. They're saved to your **backlog** (your list of workflows to build). Then Deconstruct works out what the one you choose must do."
R2 = "I'll start from your registry: 12 processes and your 3 goals."
R2later = "I'll start from your registry: 12 processes, your 3 goals, and the 5 workflows already in your backlog."
A11 = "I'll look at this from the business's point of view: the processes that drive your goals."
F19 = "Changes are saved to GitHub, on a branch."
A2 = {
 "claude-code": "I'll read and save your files in this folder. When Claude Code asks before I save a file, you can allow edits for this session; I'll only change the files this step needs. Stopping early is safe. Progress is saved. To pick up, start a new session in this project and say 'run the analyze skill.'",
 "codex": "I'll read and save your files in this folder. When Codex asks before I save a file, you can allow it for this session; I'll only change the files this step needs. Stopping early is safe. Progress is saved. To pick up, start a new session in this project and say 'run the analyze skill.'",
 "web": "I'll read and save your files in Google Drive, in ai-workspace. When Claude asks to save to your drive here, choose Always allow for this chat; I'll only read and save inside your working folder. Stopping early is safe. Progress is saved. To pick up, say 'run the analyze skill. My files are in Google Drive, in ai-workspace.'",
 "desktop": "I'll read and save your files in ai-workspace. Stopping early is safe. Progress is saved. To pick up, open a new chat with your working folder selected and say 'run the analyze skill. My files are in ai-workspace.'",
 "cowork": "I'll read and save your files in OneDrive, in ai-workspace. When Cowork asks to save to your drive here, choose Always allow for this chat; I'll only read and save inside your working folder. Stopping early is safe. Progress is saved. To pick up, open a new Cowork chat and say 'run the analyze skill. My files are in OneDrive, in ai-workspace.'",
 "cloud": "I'll read and save your files in your harbor-ops repository on GitHub. When Claude Code asks before I save a file, you can allow edits for this session; I'll only change the files this step needs. Stopping early is safe. Progress is saved. To pick up, start a new session in this project and say 'run the analyze skill.'",
}
TAIL = "I'll keep only Harbor Advisory work, leave out names and confidential details, and save only what you keep."
A12 = {
 "claude-code": "Besides your registry, may I look through your knowledge graph, SOPs and process guides in this folder, your memory files, and the requests you've typed into Claude Code in any project? " + TAIL + " Say yes, no, or which ones, or name another folder to add.",
 "codex": "Besides your registry, may I look through your knowledge graph, SOPs and process guides in this folder, and your project instructions file? " + TAIL + " Say yes, no, or which ones, or name another folder to add.",
 "web": "Besides your registry, may I look through the 12 other documents in your working folder (SOPs and notes) and your saved memory and past chats in your Claude account (not your drive)? " + TAIL + " Say yes, no, or which ones.",
 "desktop": "Besides your registry, may I look through the 12 other documents in your working folder (SOPs and notes) and your saved memory and past chats in your Claude account? " + TAIL + " Say yes, no, or which ones.",
 "cowork": "Besides your registry, may I look through the 12 other documents in your working folder (SOPs and notes)? " + TAIL + " Say yes, no, or which ones.",
 "cloud": "Besides your registry, may I look through your knowledge graph, SOPs and process guides in this repository, and its project instructions file? " + TAIL + " Say yes, no, or which ones, or name another folder to add.",
}
A12_memory = "May I look through your saved memory and past chats in your Claude account (not your drive)? " + TAIL + " Say yes or no. You can also attach a document that shows the work."
A12_general = "Documents holds a lot besides your AI work, so I'd look only in your knowledge graph and your saved memory and past chats, plus any folder in it you name. May I? " + TAIL + " Say yes, no, or name a folder to add."
A12_later_web = "Besides your registry, may I look through the 4 documents added or changed in your working folder since October (SOPs) and your saved memory and past chats in your Claude account (not your drive)? " + TAIL + " Say yes, no, or which ones."
A14_open = "Think of the last few weeks across Consulting, Learning and Coaching, including anything that only comes around now and then, like a launch. Where did time go, or things slip, that you'd rather hadn't? Two or three is plenty; 'not sure' is fine too. You can also attach a document that shows the work."
A14_team_open = "Think of the last few weeks, including anything that only comes around now and then. Where did your team's time go, or things slip, that you'd rather hadn't? Two or three is plenty; 'not sure' is fine too. You can also attach a document that shows the work."
A11_team = "I'll look at this from your team's point of view: the processes your team runs."
def n(s): return len(s.replace("**", "").split())
print("N-A10", n(A10), "| N-A14 opening", n(A14_open), "| team", n(A14_team_open))
for k, v in A12.items(): print("N-A12", k, n(v))
print("N-A12 memory-only", n(A12_memory), "| general", n(A12_general), "| later web", n(A12_later_web))
print()
for p in A2:
    base = n(A10) + n(R2) + n(A11) + n(A2[p])
    extra = n(F19) if p == "cloud" else 0
    print(f"{p:12} scan {base + extra + n(A12[p]):3} | same chat {base - n(R2) + 6 + extra + n(A12[p]):3} | later {base - n(R2) + n(R2later) + extra + n(A12[p]):3} | nothing to scan {base + extra + n(A14_open):3} | team nothing {base - n(A11) + n(A11_team) + extra + n(A14_team_open):3}")
print("web memory-only", n(A10)+n(R2)+n(A11)+n(A2['web'])+n(A12_memory))
print("desktop general", n(A10)+n(R2)+n(A11)+n(A2['desktop'])+n(A12_general))
print("web later (N-A10 first sentence only)", n(A10.split('. They')[0])+n(R2later)+n(A11)+n(A2['web'])+n(A12_later_web))

for p in A2:
    later = n(A10.split('. They')[0]) + n(R2later) + n(A11) + n(A2[p]) + n(A12[p])
    print("later run (short N-A10)", p, later)
