"""Gate probe: one interactive session, two prompts. The first, /spikeap:auto, should be answered by the
hook; the second, a plain ask in the same session after the turn ends, should reach a human."""
import json
import subprocess
import time
from pathlib import Path

here = Path(__file__).resolve().parent
work = here / "runs" / "g1-gate"
work.mkdir(parents=True, exist_ok=True)
marks = work / "marks"
session = "spike-gate"


def tmux(*a):
    return subprocess.run(["tmux", *a], capture_output=True, text=True).stdout


def screen():
    return tmux("capture-pane", "-p", "-t", session, "-S", "-120")


def send(text):
    tmux("send-keys", "-t", session, "-l", text)
    time.sleep(1)
    tmux("send-keys", "-t", session, "Enter")


tmux("kill-session", "-t", session)
tmux("new-session", "-d", "-s", session, "-x", "220", "-y", "60", "-c", str(work),
     f"SPIKE_MODE=gate SPIKE_MARKS={marks} claude --plugin-dir {here}/plugin --model sonnet "
     f"--permission-mode bypassPermissions")
time.sleep(10)
for _ in range(3):
    s = screen()
    if "❯ No" in s or "Yes, I accept" in s:
        tmux("send-keys", "-t", session, "Down")
        time.sleep(1)
        tmux("send-keys", "-t", session, "Enter")
        time.sleep(4)

send("/spikeap:auto")
first = "timeout"
for _ in range(30):
    time.sleep(5)
    if (work / "answer.txt").exists():
        time.sleep(10)
        first = "answered without a human"
        break
    if "Enter to select" in screen():
        first = "question shown to a human"
        break
marked_after_first = sorted(p.name for p in marks.iterdir() if p.name != "events.log") if marks.exists() else []

send("Use the AskUserQuestion tool to ask me one question: 'Tea or coffee?', options "
     "'Tea (Recommended)' and 'Coffee'. Then tell me what I picked.")
second = "timeout"
for _ in range(30):
    time.sleep(5)
    s = screen()
    if "Tea or coffee" in s and "Enter to select" in s:
        second = "question shown to a human"
        break
    if "Autopilot is on" in s:
        second = "denied by the hook"
        break
final = screen()
tmux("send-keys", "-t", session, "Escape")
time.sleep(1)
tmux("kill-session", "-t", session)
events = (marks / "events.log").read_text().splitlines() if (marks / "events.log").exists() else []
print(json.dumps({"first_prompt": first, "marks_left_after_first_turn": marked_after_first,
                  "second_prompt": second, "events": [json.loads(e) for e in events]}, indent=1))
print(final[-1500:])
