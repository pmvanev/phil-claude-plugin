#!/usr/bin/env python3
"""Guard G2 - test-file write-block (PreToolUse on Edit/Write).

Blocks any Edit/Write whose target path matches a test-file glob, but only while a
refactor-loop run is active (the .refactor-loop-ledger.md sentinel with `active-run: true`
exists in the project root). Outside an active run it is a no-op, so it never traps
unrelated editing.

Protocol: reads the hook payload as JSON on stdin; to block, prints a JSON decision and
exits 0. Test-path globs match architecture.md s3.4.

Substrate note (ADR-008): under the Workflow substrate the cage ALSO scans the proposed
diff in JS before `git apply` (a Bash apply bypasses the Edit/Write matcher). This hook is
the primary guard for the interactive skill substrate and defense-in-depth against any
stray Edit/Write under either substrate.
"""
import json
import os
import re
import sys

TEST_PATTERNS = [
    r"/tests?/", r"/spec/", r"/__tests__/",
    r"_test\.", r"\.test\.", r"\.spec\.",
    r"^test_.*\.py$", r"conftest\.py$",
]


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"refactor-loop guard G2: {reason}",
        }
    }))


def main():
    # Fails open only where no run can exist. Once the ledger exists, anything unreadable is a run
    # this hook cannot rule out, so it denies (CWE-636).
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = None
    if not isinstance(payload, dict):
        payload = None

    cwd = payload.get("cwd") if payload else None
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()
    ledger = os.path.join(cwd, ".refactor-loop-ledger.md")

    # Sentinel gate: only enforce during an active refactor-loop run.
    if not os.path.lexists(ledger):
        return
    try:
        with open(ledger, encoding="utf-8") as f:
            ledger_text = f.read()
    except Exception:
        deny("the run ledger exists but cannot be read, so an active run cannot be ruled out.")
        return
    if not re.search(r"active-run:\s*true", ledger_text):
        return

    if payload is None:
        deny("the hook payload is not a JSON object, so the target cannot be checked.")
        return
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    path = tool_input.get("file_path") or tool_input.get("path")
    if not isinstance(path, str) or not path:
        deny("the write names no target path, so it cannot be checked against the test globs.")
        return

    norm = path.replace("\\", "/")
    leaf = norm.rsplit("/", 1)[-1]

    if any(re.search(p, norm) or re.search(p, leaf) for p in TEST_PATTERNS):
        deny(f"writes to test files are blocked during an active run ({leaf}). "
             f"The proposer never edits the oracle.")


if __name__ == "__main__":
    main()
