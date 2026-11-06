#!/usr/bin/env python3
"""Probe gate: UserPromptSubmit marks a session that typed /spikeap:auto, PreToolUse(AskUserQuestion)
denies only in a marked session, Stop clears the mark. The mark lives in $SPIKE_MARKS/<session_id>."""
import json
import os
import sys
from pathlib import Path

event = json.load(sys.stdin)
marks = Path(os.environ.get("SPIKE_MARKS", "/tmp/spike-marks"))
marks.mkdir(parents=True, exist_ok=True)
sid = event.get("session_id", "none")
mark = marks / sid
name = event.get("hook_event_name")
with (marks / "events.log").open("a") as f:
    f.write(json.dumps({"event": name, "sid": sid, "marked": mark.exists(),
                        "prompt": event.get("prompt", "")[:60]}) + "\n")

if name == "UserPromptSubmit" and event.get("prompt", "").lstrip().startswith("/spikeap:auto"):
    mark.write_text("active")
elif name == "Stop" and mark.exists():
    mark.unlink()
elif name == "PreToolUse" and mark.exists():
    qs = event.get("tool_input", {}).get("questions", [])
    rec = [o["label"] for q in qs for o in q.get("options", []) if "(Recommended)" in o.get("label", "")]
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": f"Autopilot is on; take {rec} and record it."}}))
sys.exit(0)
