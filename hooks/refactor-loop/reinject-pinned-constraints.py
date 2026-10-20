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
import subprocess
import sys


# The grammar of each header line G7 re-injects. A line outside its grammar is dropped, so no free text
# reaches the prompt whoever wrote the ledger: a tarball of a working copy carries its own `.git`, and
# git then answers "untracked" for a ledger the packer wrote (CWE-1427, issue 48). `runner:` is a
# free-text command and is never re-injected; the loop re-reads the ledger at every boundary anyway.
HEADER = re.compile(
    r"pinned: \[(?:[a-z0-9-]+(?:, [a-z0-9-]+)*)?\]"
    r"|iter: \d+ / max \d+"
    r"|baseline: (?:green|red) @ [0-9a-f]{7,40}"
    r"|theta: \d+(?:\.\d+)?"
    r"|status: [A-Za-z]+(?:-[A-Za-z]+)*"
)


def tracked(cwd):
    """True unless git answers that the ledger is untracked.

    The loop writes the ledger and never commits it, so a tracked ledger came from whoever can commit
    to the repo, and re-injecting it would let a cloned repo author every prompt's context (CWE-1427,
    issue 48). Only exit 1 is that answer. Exit 128 covers a directory unpacked from an archive, with
    no `.git`, and a repository git refuses as dubiously owned; either ledger may be anyone's.
    """
    try:
        proc = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", ".refactor-loop-ledger.md"],
            cwd=cwd, capture_output=True, timeout=5)
    except Exception:
        return True
    return proc.returncode != 1


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    cwd = payload.get("cwd") or os.getcwd()
    ledger = os.path.join(cwd, ".refactor-loop-ledger.md")

    if not os.path.isfile(ledger) or tracked(cwd):
        return
    try:
        ledger_text = open(ledger, encoding="utf-8").read()
    except Exception:
        return
    if not re.search(r"active-run:\s*true", ledger_text):
        return

    header = "; ".join(
        line.rstrip() for line in ledger_text.splitlines() if HEADER.fullmatch(line.rstrip())
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
