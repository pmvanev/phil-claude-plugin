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


def test_a_modified_file_reads_dirty_and_is_named(tmp_path):
    """The plan shows a dirty worktree's changes beside it (the developer's answer, 2026-11-02)."""
    wt = repo_with_worktree(tmp_path)
    (wt / "a.txt").write_text("changed\n")
    assert state(wt) == (0, [f"DIRTY {wt}", "   M a.txt"])


def test_an_untracked_file_reads_dirty_and_is_named(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / "notes.md").write_text("x\n")
    assert state(wt) == (0, [f"DIRTY {wt}", "  ?? notes.md"])


def test_ignored_files_alone_read_clean(tmp_path):
    """Git removes ignored files with the worktree and never refuses for them; the plan warns instead."""
    wt = repo_with_worktree(tmp_path)
    (wt / ".env").write_text("SECRET=1\n")
    (wt / ".session-handoff.md").write_text("snapshot\n")
    assert state(wt) == (0, [f"CLEAN {wt}", "  ignored: .env", "  ignored: .session-handoff.md"]), \
        "skill-reviewer, 2026-11-03: the plan said nothing of an ignored .env the removal deleted"


def test_a_path_that_is_no_worktree_reads_unreadable(tmp_path):
    missing = tmp_path / "gone"
    assert state(missing) == (0, [f"UNREADABLE {missing}"])


def test_it_writes_nothing(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / "notes.md").write_text("x\n")
    before = sorted(p.name for p in wt.iterdir())
    state(wt)
    assert sorted(p.name for p in wt.iterdir()) == before


# --- HIDDEN: work `git worktree remove` deletes without objecting ----------------------------------
#
# The adversarial run of 2026-11-02 removed, with exit 0, a repository nested in an ignored folder,
# edits hidden by --assume-unchanged or --skip-worktree, and commits only the worktree's history held;
# git refuses a worktree with a submodule. `/phil:done` removes a worktree only where this reads CLEAN
# (the developer's answer, 2026-11-03), so each of those must read HIDDEN.

def test_an_ignored_nested_repository_reads_hidden(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / ".gitignore").write_text(".env\n.session-handoff.md\nvendor/\n")
    git(wt, "commit", "-qam", "ignore vendor")
    nested = wt / "vendor" / "lib"
    nested.mkdir(parents=True)
    git(nested, "init", "-q")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  ignored repository: vendor/lib"])


def test_an_assume_unchanged_edit_reads_hidden(tmp_path):
    wt = repo_with_worktree(tmp_path)
    git(wt, "update-index", "--assume-unchanged", "a.txt")
    (wt / "a.txt").write_text("changed\n")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  hidden edit (assume-unchanged): a.txt"])


def test_a_skip_worktree_edit_reads_hidden(tmp_path):
    wt = repo_with_worktree(tmp_path)
    git(wt, "update-index", "--skip-worktree", "a.txt")
    (wt / "a.txt").write_text("changed\n")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  hidden edit (skip-worktree): a.txt"])


def test_a_submodule_reads_hidden(tmp_path):
    wt = repo_with_worktree(tmp_path)
    lib = tmp_path / "lib"
    lib.mkdir()
    git(lib, "init", "-q", "-b", "main")
    (lib / "x").write_text("x\n")
    git(lib, "add", "-A")
    git(lib, "commit", "-qm", "lib")
    git(wt, "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(lib), "sub")
    git(wt, "commit", "-qm", "add submodule")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  submodule: sub"])


def test_a_commit_only_the_worktrees_history_holds_reads_hidden(tmp_path):
    wt = repo_with_worktree(tmp_path)
    (wt / "a.txt").write_text("lost\n")
    git(wt, "commit", "-qam", "a commit then abandoned")
    git(wt, "reset", "-q", "--hard", "HEAD~1")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  1 commit only this worktree's history holds"])


def test_a_commit_another_ref_holds_is_not_hidden(tmp_path):
    """A commit pushed or merged elsewhere survives the worktree, so it holds nothing."""
    wt = repo_with_worktree(tmp_path)
    (wt / "a.txt").write_text("kept\n")
    git(wt, "commit", "-qam", "kept")
    git(wt, "branch", "keep")
    git(wt, "reset", "-q", "--hard", "HEAD~1")
    assert state(wt) == (0, [f"CLEAN {wt}"])


def test_dirty_outranks_hidden(tmp_path):
    wt = repo_with_worktree(tmp_path)
    git(wt, "update-index", "--assume-unchanged", "a.txt")
    (wt / "notes.md").write_text("x\n")
    assert state(wt) == (0, [f"DIRTY {wt}", "  ?? notes.md"])


# --- MOVED: a worktree whose HEAD left the merged tip ----------------------------------------------
#
# plugin-validator, 2026-11-03: a commit made in the worktree after the plan is reachable from its
# branch, so it reads CLEAN, and `ExitWorktree` with `discard_changes: true` would delete it with the
# branch. `--expect-head` names the merged tip the removal depends on.

def head(wt):
    return subprocess.run(["git", "-C", str(wt), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def state_expecting(sha, *paths):
    r = subprocess.run([sys.executable, str(SCRIPT), "--expect-head", sha, *map(str, paths)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines()


def test_a_worktree_at_the_expected_head_reads_clean(tmp_path):
    wt = repo_with_worktree(tmp_path)
    assert state_expecting(head(wt), wt) == (0, [f"CLEAN {wt}"])


def test_a_short_expected_head_matches(tmp_path):
    wt = repo_with_worktree(tmp_path)
    assert state_expecting(head(wt)[:7], wt) == (0, [f"CLEAN {wt}"])


def test_a_commit_after_the_merged_tip_reads_moved(tmp_path):
    wt = repo_with_worktree(tmp_path)
    merged = head(wt)
    (wt / "a.txt").write_text("after the plan\n")
    git(wt, "commit", "-qam", "after the plan")
    assert state_expecting(merged, wt) == (0, [f"MOVED {wt}", f"  HEAD {head(wt)}, expected {merged}"])


# --- skill-reviewer, 2026-11-03 ----------------------------------------------------------------------

def test_an_ignored_repository_under_a_non_ascii_name_reads_hidden(tmp_path):
    """Without -z, git quotes the name, and the quoted string names no directory."""
    wt = repo_with_worktree(tmp_path)
    (wt / ".gitignore").write_text(".env\n.session-handoff.md\nvendör/\n")
    git(wt, "commit", "-qam", "ignore vendör")
    nested = wt / "vendör" / "lib"
    nested.mkdir(parents=True)
    git(nested, "init", "-q")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  ignored repository: vendör/lib"])


def test_a_commit_only_a_worktree_ref_holds_reads_hidden(tmp_path):
    """Removing a worktree deletes its own refs/worktree/*, so they keep nothing safe."""
    wt = repo_with_worktree(tmp_path)
    (wt / "a.txt").write_text("wip\n")
    git(wt, "commit", "-qam", "wip")
    git(wt, "update-ref", "refs/worktree/wip", "HEAD")
    git(wt, "reset", "-q", "--hard", "HEAD~1")
    assert state(wt) == (0, [f"HIDDEN {wt}", "  1 commit only this worktree's history holds"])


def test_an_empty_expected_head_is_refused(tmp_path):
    wt = repo_with_worktree(tmp_path)
    code, _ = state_expecting("", wt)
    assert code == 2
