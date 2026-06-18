#!/usr/bin/env python3
"""Guard G7 - pinned-constraint re-inject (UserPromptSubmit hook).

INTERACTIVE SKILL SUBSTRATE ONLY. Obviated under the Workflow substrate (ADR-008): the
Workflow holds loop state in JS variables, not a compacting context, so there is nothing to
re-assert. Wire this only when running the prose `skills/refactor-loop/SKILL.md` fallback.

Re-asserts the durable, compaction-immune pinned constraints from the ledger header at every
prompt boundary, so context compaction can never silently evict a safety rule. Decay belongs
on world state, never on rules. Gated on the refactor-loop sentinel.

Protocol: reads the hook payload as JSON on stdin; to inject context, prints a JSON object
with hookSpecificOutput.additionalContext (UserPromptSubmit).
"""
import json
import os
import re
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
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

    header = "; ".join(
        line for line in ledger_text.splitlines()
        if re.match(r"^(pinned|iter|baseline|runner|theta|status):", line)
    )
    if not header:
        return

    context = (
        "refactor-loop pinned constraints (re-asserted from .refactor-loop-ledger.md, the "
        f"durable source): {header}. These hold for every iteration regardless of context "
        "compaction."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
