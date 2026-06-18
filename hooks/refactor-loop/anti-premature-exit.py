#!/usr/bin/env python3
"""Guard G10 - anti-premature-exit (Stop hook).

INTERACTIVE SKILL SUBSTRATE ONLY. Obviated under the Workflow substrate (ADR-008): the
Workflow's JS owns the loop condition, so the model cannot end the turn mid-loop and there
is nothing to guard. Wire this only when running the prose `skills/refactor-loop/SKILL.md`
fallback.

Forces the loop to keep going until its DONE predicate is satisfied. Gated on the
refactor-loop sentinel so it never traps unrelated sessions: it fires only when
.refactor-loop-ledger.md exists with `active-run: true`. When the loop reaches DONE/HALT it
clears active-run and this hook goes silent.

Protocol: reads the hook payload as JSON on stdin; to force continuation, prints a JSON
decision with "decision": "block" and a reason fed back to the model.
"""
import json
import os
import re
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return  # malformed payload: allow the stop

    # Avoid an infinite loop: if this Stop was itself triggered by a prior block, allow it.
    if payload.get("stop_hook_active") is True:
        return

    cwd = payload.get("cwd") or os.getcwd()
    ledger = os.path.join(cwd, ".refactor-loop-ledger.md")

    if not os.path.isfile(ledger):
        return
    try:
        ledger_text = open(ledger, encoding="utf-8").read()
    except Exception:
        return
    if not re.search(r"active-run:\s*true", ledger_text):
        return

    print(json.dumps({
        "decision": "block",
        "reason": (
            "refactor-loop guard G10: the run is still active (.refactor-loop-ledger.md has "
            "active-run: true). Continue the state machine until the DONE predicate (green AND "
            "no unresolved >=major above threshold AND iter < max) or HALT (iter >= max) is "
            "reached, then clear active-run. Do not end the turn before the guard is satisfied."
        ),
    }))


if __name__ == "__main__":
    main()
