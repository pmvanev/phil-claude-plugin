#!/usr/bin/env python3
"""Run the repo's test suite as a `SessionStart` invariant, reporting only failures.

**Why this exists.** 400+ tests, a dozen hand-written check functions, and nothing ran any of them
unless a human typed `pytest`. There is no CI in this repository — no `.github/`, no pipeline config —
and `.claude/settings.json` wires only the invariant runner and the skew detector. So every check
added by every slice, including the twelve this file was added alongside, reported compliance by
staying quiet: exactly the failure `check-invariants.py`'s own docstring names.

`CLAUDE.md`'s threshold for adding a check here is a defect found twice. The written-but-never-called
defect is now on its fourth recorded appearance in this repo, and the shared-fragment registry drifted
twice with its remedy also sitting in an unrun pytest.

Exit 0 when the suite passes, 1 when it does not. Silence on success is the contract for everything
`check-invariants.py` runs — a runner that announces success every session trains people to stop
reading it.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TAIL_LINES = 25


def main() -> int:
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
            cwd=REPO, capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        print("FAIL  pytest is not installed — the suite did not run, which is not the same as passing")
        return 1
    except subprocess.TimeoutExpired:
        print("FAIL  the test suite did not finish within 120s")
        return 1

    if proc.returncode == 0:
        return 0

    lines = (proc.stdout or proc.stderr).strip().splitlines()
    # Only the verdict and the named failures. Dumping pytest's progress dots into a SessionStart
    # report is how a runner teaches people to stop reading it — the same failure as staying silent.
    named = [ln for ln in lines if ln.startswith("FAILED") or ln.startswith("ERROR")]
    summary = [ln for ln in lines if " passed" in ln or " failed" in ln or " error" in ln]
    print("FAIL  repo test suite")
    for line in (summary[-1:] + named)[:TAIL_LINES]:
        print(f"      {line.strip()}")
    if not named:
        print("      (no named failures — run `python3 -m pytest -q` for the full output)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
