#!/usr/bin/env python3
"""Run this repo's invariant checks and report only what fails.

A check nobody runs is a check that reports compliance by staying quiet — the failure shape this
board keeps rediscovering. These are wired to SessionStart so they run without being remembered.

Silent when everything passes: a runner that announces success every session trains people to
stop reading it, and then it is silent in the way that matters. Never fails the session — a broken
check must not block work, and must not be mistaken for a clean one either.
"""

import json
import subprocess
import sys
from pathlib import Path

CHECKS = [
    ("command mutation declarations", "check-readonly-commands.py"),
    ("product SSOT traceability", "check-product-ssot.py"),
    # Added 2026-08-26. Nothing ran pytest automatically — no CI exists here — so every check written
    # as a test reported compliance by staying quiet, which is the defect this runner exists to stop.
    ("repo test suite", "check-tests.py"),
]


def main() -> int:
    here = Path(__file__).resolve().parent
    failures = []

    for label, script in CHECKS:
        path = here / script
        if not path.exists():
            failures.append(f"{label}: {script} is missing")
            continue
        try:
            r = subprocess.run(
                [sys.executable, str(path)],
                capture_output=True, text=True, timeout=30,
            )
        except Exception as e:
            failures.append(f"{label}: could not run {script} ({e})")
            continue
        if r.returncode != 0:
            detail = "\n".join(f"    {line}" for line in r.stdout.strip().splitlines() if line)
            failures.append(f"{label}:\n{detail}")

    if not failures:
        return 0

    message = "REPO INVARIANT CHECK FAILED\n" + "\n".join(f"  {f}" for f in failures)
    json.dump(
        {
            "systemMessage": message,
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": message,
            },
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
