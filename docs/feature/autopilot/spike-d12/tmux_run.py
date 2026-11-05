"""Drive an interactive claude session in tmux: python3 tmux_run.py <name> <mode> <command>."""
import json
import subprocess
import sys
import time
from pathlib import Path

name, mode, command = sys.argv[1], sys.argv[2], sys.argv[3]
here = Path(__file__).resolve().parent
work = here / "runs" / name
work.mkdir(parents=True, exist_ok=True)
session = f"spike-{name}"


def tmux(*args):
    return subprocess.run(["tmux", *args], capture_output=True, text=True).stdout


def screen():
    return tmux("capture-pane", "-p", "-t", session, "-S", "-80")


launch = (f"SPIKE_MODE={mode} SPIKE_LOG={work}/hook.log claude --plugin-dir {here}/plugin "
          f"--model sonnet --permission-mode bypassPermissions")
tmux("kill-session", "-t", session)
tmux("new-session", "-d", "-s", session, "-x", "220", "-y", "60", "-c", str(work), launch)
log = []
time.sleep(10)
for _ in range(3):  # trust or bypass dialogs
    s = screen()
    if "trust" in s.lower() or "Yes, I accept" in s or "Do you want" in s:
        log.append(("dialog", s[-1200:]))
        if "Yes, I accept" in s or "❯ No" in s:
            tmux("send-keys", "-t", session, "Down")
            time.sleep(1)
        tmux("send-keys", "-t", session, "Enter")
        time.sleep(4)
tmux("send-keys", "-t", session, "-l", command)
time.sleep(1)
tmux("send-keys", "-t", session, "Enter")
outcome = "timeout"
for _ in range(36):
    time.sleep(5)
    s = screen()
    if (work / "answer.txt").exists():
        time.sleep(8)
        outcome = "answered"
        break
    if "Which colour" in s and ("Blue (Recommended)" in s and "Red" in s) and "❯" in s \
            and "Enter to select" in s:
        outcome = "question shown to a human"
        break
log.append(("final screen", screen()[-3500:]))
tmux("send-keys", "-t", session, "Escape")
time.sleep(1)
tmux("kill-session", "-t", session)
(work / "screens.json").write_text(json.dumps(log, indent=1))
answer = (work / "answer.txt").read_text().strip() if (work / "answer.txt").exists() else None
hook = (work / "hook.log").read_text().count("\n") if (work / "hook.log").exists() else 0
print(json.dumps({"run": name, "mode": mode, "outcome": outcome, "answer.txt": answer,
                  "hook_calls": hook}, indent=1))
print(log[-1][1][-2500:])
