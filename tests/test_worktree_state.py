"""Tests for `scripts/worktree-state.py`, the read `/phil:done` makes before its plan.

`git worktree remove` refuses a worktree with modified or untracked files, but CLEAR retires the
snapshot inside a worktree before removing it, so a refusal at run time arrives after the handoff is
gone. The plan must hold a dirty worktree up front (skill-reviewer, 2026-11-02), and the command grants
no `git -C`, so this script makes the one read it needs.
"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "worktree-state.py"


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.email=t@example.com", "-c", "user.name=t",
                    "-c", "commit.gpgsign=false", *args], cwd=cwd, check=True, capture_output=True)


def repo_with_worktree(tmp_path):
    main = tmp_path / "main"
    main.mkdir()
    git(main, "init", "-q", "-b", "main")
    (main / ".gitignore").write_text(".env\n.session-handoff.md\n")
    (main / "a.txt").write_text("a\n")
    git(main, "add", "-A")
    git(main, "commit", "-qm", "base")
    wt = tmp_path / "wt"
    git(main, "worktree", "add", "-q", "-b", "feature", str(wt))
    return wt


def state(*paths):
    r = subprocess.run([sys.executable, str(SCRIPT), *map(str, paths)], capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines()


def test_a_clean_worktree_reads_clean(tmp_path):
    wt = repo_with_worktree(tmp_path)
    assert state(wt) == (0, [f"CLEAN {wt}"])


def test_a_modified_file_reads_dirty(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / "a.txt").write_text("changed\n")
    assert state(wt) == (0, [f"DIRTY {wt}"])


def test_an_untracked_file_reads_dirty(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / "notes.md").write_text("x\n")
    assert state(wt) == (0, [f"DIRTY {wt}"])


def test_ignored_files_alone_read_clean(tmp_path):
    """Git removes ignored files with the worktree and never refuses for them; the plan warns instead."""
    wt = repo_with_worktree(tmp_path)
    (wt / ".env").write_text("SECRET=1\n")
    (wt / ".session-handoff.md").write_text("snapshot\n")
    assert state(wt) == (0, [f"CLEAN {wt}"])


def test_a_path_that_is_no_worktree_reads_unreadable(tmp_path):
    missing = tmp_path / "gone"
    assert state(missing) == (0, [f"UNREADABLE {missing}"])


def test_it_writes_nothing(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / "notes.md").write_text("x\n")
    before = sorted(p.name for p in wt.iterdir())
    state(wt)
    assert sorted(p.name for p in wt.iterdir()) == before
