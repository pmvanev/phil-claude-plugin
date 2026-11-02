#!/usr/bin/env python3
"""Say whether each worktree holds work that `git worktree remove` would refuse to discard.

`/phil:done` reads this before composing its plan. CLEAR retires a worktree's handoff snapshot before
removing the worktree, so a refusal that arrives only at removal comes after the snapshot is gone; the
plan must hold a dirty worktree, with its snapshot, up front. The command grants no `git -C`, so this
script makes that one read.

For each path, prints one line:

- `CLEAN <path>` — no modified, staged or untracked file. Ignored files may remain, and
  `git worktree remove` deletes them with the worktree; the plan says so.
- `DIRTY <path>` — something git would refuse to discard, followed by one indented line per change, as
  `git status --porcelain` prints it, so the plan can show what would be lost.
- `UNREADABLE <path>` — not a worktree, or git could not read it.

Reads only; writes nothing. Exits 0 whenever it could judge its arguments.
"""
import subprocess
import sys


def judge(path: str) -> str:
    result = subprocess.run(["git", "-C", path, "status", "--porcelain", "--untracked-files=normal"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return f"UNREADABLE {path}"
    changes = [line for line in result.stdout.splitlines() if line.strip()]
    if not changes:
        return f"CLEAN {path}"
    return "\n".join([f"DIRTY {path}", *(f"  {line}" for line in changes)])


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: worktree-state.py <worktree-path>...", file=sys.stderr)
        return 2
    for path in argv:
        print(judge(path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
