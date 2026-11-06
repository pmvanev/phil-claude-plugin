#!/usr/bin/env python3
"""Probe hook. SPIKE_MODE=off passes; deny refuses naming the recommended option; answer pre-fills it."""
import json
import os
import sys
from pathlib import Path

event = json.load(sys.stdin)
log = Path(os.environ.get("SPIKE_LOG", "/dev/null"))
with log.open("a") as f:
    f.write(json.dumps({"mode": os.environ.get("SPIKE_MODE"), "event": event}) + "\n")

mode = os.environ.get("SPIKE_MODE", "off")
questions = event.get("tool_input", {}).get("questions", [])
picks = {}
for q in questions:
    rec = [o["label"] for o in q.get("options", []) if "(Recommended)" in o.get("label", "")]
    if rec:
        picks[q["question"]] = rec[0]

if mode in ("deny", "deny-classify"):
    reason = "Autopilot is on and the developer is away. " + " ".join(
        f'For "{q}", take "{a}" and record it.' for q, a in picks.items())
    if mode == "deny-classify":
        reason = ("Autopilot is on and the developer is away; nobody will answer. First decide whether "
                  "this question is a BLOCKER: an outward or irreversible write nothing authorized, an "
                  "input only the developer holds (their own material, an account, a secret), or a "
                  "check that keeps failing. If it is a blocker, write nothing, print 'BLOCKED: <the "
                  "question> — <which kind>' and stop. Otherwise: " + " ".join(
                      f'take "{a}" for "{q}" and record it.' for q, a in picks.items()))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
elif mode == "answer":
    updated = dict(event.get("tool_input", {}))
    updated["answers"] = picks
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "allow",
                                             "permissionDecisionReason": "autopilot took the recommendation",
                                             "updatedInput": updated}}))
sys.exit(0)
