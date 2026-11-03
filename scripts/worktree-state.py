#!/usr/bin/env python3
"""Say whether removing each worktree would lose work.

`/phil:done` reads this before composing its plan, and removes a worktree only where it reads `CLEAN`.
CLEAR retires a worktree's handoff snapshot before removing the worktree, so a refusal that arrives only
at removal comes after the snapshot is gone; the plan must hold such a worktree, with its snapshot, up
front. The command grants no `git -C`, so this script makes that one read.

For each path, prints one line:

- `CLEAN <path>` — removing it loses nothing git or this script can see but its ignored files, which
  `git worktree remove` deletes with the worktree. One indented `ignored: <entry>` line follows for each
  top-level ignored file or folder, so the plan can name what goes.
- `DIRTY <path>` — a modified, staged or untracked file, followed by one indented line per change, as
  `git status --porcelain` prints it, so the plan can show what would be lost.
- `HIDDEN <path>` — work `git worktree remove` deletes without objecting, or a submodule it refuses,
  followed by one indented line per finding. An adversarial run on 2026-11-02 removed each of these
  with exit 0: a repository nested in an ignored folder, an edit hidden by `--assume-unchanged` or
  `--skip-worktree`, and a commit only the worktree's own history held.
- `MOVED <path>` — with `--expect-head <sha>`, a `HEAD` other than that commit, followed by both. A
  commit made after the plan is reachable from the worktree's branch, so nothing else here flags it, and
  removing the worktree with its branch would delete it (plugin-validator, 2026-11-03). A sha shorter
  than 7 characters never matches.
- `UNREADABLE <path>` — not a worktree, or git could not read it.

`DIRTY` outranks `MOVED`, which outranks `HIDDEN`. Reads only; writes nothing. Exits 0 whenever it could
judge its arguments.
"""
import os
import subprocess
import sys


def git(path: str, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", path, *args], capture_output=True, text=True, input=stdin)


def ignored(path: str) -> list[str]:
    """Each top-level ignored entry, NUL-separated: without `-z` git quotes a non-ASCII name, and the
    quoted string names no directory (skill-reviewer, 2026-11-03)."""
    listed = git(path, "ls-files", "-z", "--others", "--ignored", "--exclude-standard", "--directory")
    return sorted(e.rstrip("/") for e in listed.stdout.split("\0") if e)


def ignored_repositories(path: str) -> list[str]:
    found = []
    for entry in ignored(path):
        top = os.path.join(path, entry)
        if not os.path.isdir(top):
            continue
        for root, dirs, files in os.walk(top):
            if ".git" in dirs or ".git" in files:
                found.append(os.path.relpath(root, path))
                dirs[:] = []
    return sorted(found)


def hidden_edits(path: str) -> list[str]:
    lines = []
    for row in git(path, "ls-files", "-v").stdout.splitlines():
        tag, name = row[:1], row[2:]
        if tag in ("S", "s"):
            lines.append(f"hidden edit (skip-worktree): {name}")
        elif tag.islower():
            lines.append(f"hidden edit (assume-unchanged): {name}")
    return lines


def submodules(path: str) -> list[str]:
    rows = git(path, "ls-files", "--stage").stdout.splitlines()
    return [f"submodule: {row.split(chr(9), 1)[1]}" for row in rows if row.startswith("160000 ")]


def unreachable_history(path: str) -> list[str]:
    reflog = git(path, "log", "-g", "--format=%H", "HEAD").stdout
    if not reflog.strip():
        return []
    # Not `--all`: it counts this worktree's own refs/worktree/* and refs/bisect/*, which the removal
    # deletes (skill-reviewer, 2026-11-03). Stash entries are shared, and survive.
    lost = git(path, "rev-list", "--stdin", "--not", "--branches", "--tags", "--remotes",
               stdin=reflog).stdout.split()
    if not lost:
        return []
    noun = "commit" if len(lost) == 1 else "commits"
    return [f"{len(lost)} {noun} only this worktree's history holds"]


def judge(path: str, expect_head: str | None = None) -> str:
    result = git(path, "status", "--porcelain", "--untracked-files=normal")
    if result.returncode != 0:
        return f"UNREADABLE {path}"
    changes = [line for line in result.stdout.splitlines() if line.strip()]
    if changes:
        return "\n".join([f"DIRTY {path}", *(f"  {line}" for line in changes)])
    if expect_head:
        actual = git(path, "rev-parse", "HEAD").stdout.strip()
        if len(expect_head) < 7 or not actual.startswith(expect_head.lower()):
            return f"MOVED {path}\n  HEAD {actual}, expected {expect_head}"
    findings = [*(f"ignored repository: {r}" for r in ignored_repositories(path)),
                *hidden_edits(path), *submodules(path), *unreachable_history(path)]
    if findings:
        return "\n".join([f"HIDDEN {path}", *(f"  {line}" for line in findings)])
    return "\n".join([f"CLEAN {path}", *(f"  ignored: {entry}" for entry in ignored(path))])


def main(argv: list[str]) -> int:
    expect_head = None
    if argv[:1] == ["--expect-head"]:
        expect_head, argv = (argv[1], argv[2:]) if len(argv) > 1 and argv[1] else (None, [])
    if not argv:
        print("usage: worktree-state.py [--expect-head <sha>] <worktree-path>...", file=sys.stderr)
        return 2
    for path in argv:
        print(judge(path, expect_head))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
