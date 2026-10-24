# Test's simulated leaders

Scripts for `test-workspace/evals/evals.json`, in the shared format (`framework-evals/students/README.md`): who you are, what you know, how you answer, when to stop. Each is the owner of the workflow in the eval's fixture; the fixture's files hold everything about the work, so the scripts hold only the leader's choices, their real example, and what only the leader can see.

`default.md` is the usual owner of Client Follow-Up. On the platforms where the simulation opens the run chat for you (Claude on the web and desktop, ChatGPT, Microsoft 365), you paste back what your screen shows. On Claude Code and Codex your screen doesn't show the run, so the script carries the blocks your runs ended with ("Your runs"), written as a built workflow would write them. The other scripts start from `default.md`'s facts and change one behaviour each. No script uses a framework or evaluation term.
