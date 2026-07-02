"""Repo test suite — drives the golden self-test fixtures and asserts each produces its
documented outcome.

The fixtures under `*/self-test/` are NOT collected as ordinary tests (see `pytest.ini`
`norecursedirs`): they are *inputs*, not a flat suite, and one of them ships an
intentionally-red baseline (the "never refactor on a red suite" precondition). This driver is
what verifies them — for each fixture it builds a throwaway git repo, runs the suite, applies
the fixture's patch, and asserts the resulting gate outcome (STOP / REVERT / COMMIT / broadened
API). It is the automated form of the DELIVER-wave dogfood.

Covers:
  - skills/refactor-tests/self-test/   (this plugin's refactor-tests safety loop, fixtures 01-05)
  - refactor/self-test/                (the pre-existing refactor-loop gate, fixtures 01-02)
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
RT = REPO / "skills" / "refactor-tests" / "self-test"
RL = REPO / "refactor" / "self-test"


# --- helpers ---------------------------------------------------------------------------------

def _git(cwd, *args, check=False):
    result = subprocess.run(
        ["git", "-c", "user.email=selftest@example.com", "-c", "user.name=selftest",
         "-c", "commit.gpgsign=false", *args],
        cwd=str(cwd), capture_output=True, text=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result


def _suite_green(cwd):
    """True iff `pytest` passes in cwd (a real subprocess, isolated from this run)."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=str(cwd), capture_output=True, text=True,
    )
    return result.returncode == 0


def _new_repo_from(fixture):
    """Copy a fixture's source files into a fresh temp git repo with a committed baseline."""
    tmp = Path(tempfile.mkdtemp(prefix="selftest-"))
    for src in fixture.glob("*.py"):
        shutil.copy(src, tmp / src.name)
    _git(tmp, "init", "-q", check=True)
    _git(tmp, "add", "-A", check=True)
    _git(tmp, "commit", "-qm", "baseline", check=True)
    return tmp


def _apply(tmp, patch):
    result = _git(tmp, "apply", "--recount", str(patch))
    assert result.returncode == 0, f"patch failed to apply: {result.stderr}"


def _tracked_clean(tmp):
    return _git(tmp, "status", "--porcelain", "--untracked-files=no").stdout.strip() == ""


def _commit_count(tmp):
    return int(_git(tmp, "rev-list", "--count", "HEAD").stdout.strip())


# --- refactor-tests safety loop (skills/refactor-tests/self-test) -----------------------------

def test_rt01_baseline_red_is_the_stop_precondition():
    # Arrange: fixture 01 ships a buggy SUT, so its suite is red at baseline.
    tmp = _new_repo_from(RT / "01-baseline-red-stop")
    try:
        # Assert: red baseline -> the loop must STOP (never refactor on red).
        assert not _suite_green(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rt02_botched_move_reds_suite_then_auto_reverts_clean():
    fixture = RT / "02-postapply-red-autorevert"
    tmp = _new_repo_from(fixture)
    try:
        assert _suite_green(tmp)                       # green baseline
        _apply(tmp, fixture / "move.patch")            # a move that silently changes the test
        assert not _suite_green(tmp)                   # suite goes red
        _git(tmp, "checkout", "--", "test_cart.py", check=True)  # auto-revert
        assert _suite_green(tmp)                        # back to green
        assert _tracked_clean(tmp)                      # working tree restored
        assert _commit_count(tmp) == 1                  # nothing committed
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rt03_correct_move_stays_green_and_commits_on_approval():
    fixture = RT / "03-approve-commit-on-green"
    tmp = _new_repo_from(fixture)
    try:
        assert _suite_green(tmp)                        # green baseline
        _apply(tmp, fixture / "move.patch")            # correct Extract Fixture
        assert _suite_green(tmp)                        # stays green -> reaches human gate
        _git(tmp, "add", "-A", check=True)             # approve -> commit
        _git(tmp, "commit", "-qm", "approved", check=True)
        assert _suite_green(tmp)
        assert _commit_count(tmp) == 2                  # exactly one new commit
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rt04_reject_reverts_clean_even_when_suite_is_green():
    fixture = RT / "04-reject-reverts-clean"
    tmp = _new_repo_from(fixture)
    try:
        assert _suite_green(tmp)
        _apply(tmp, fixture / "move.patch")            # same green move as fixture 03
        assert _suite_green(tmp)                        # green, but the human rejects
        _git(tmp, "checkout", "--", "test_cart.py", check=True)
        assert _tracked_clean(tmp)                      # human overrides green: clean revert
        assert _commit_count(tmp) == 1                  # nothing written
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rt05_review_fixture_is_wellformed():
    # The --review detector is an LLM task; here we assert the fixture is runnable and complete.
    fixture = RT / "05-review-seeds-backlog"
    tmp = _new_repo_from(fixture)
    try:
        assert _suite_green(tmp)                        # smells file runs green
        assert (fixture / "expected-backlog.md").exists()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- refactor-loop gate (refactor/self-test) --------------------------------------------------

def test_rl01_bad_diff_breaks_the_suite():
    fixture = RL / "01-breaks-test"
    tmp = _new_repo_from(fixture)
    try:
        assert _suite_green(tmp)                        # green baseline
        _apply(tmp, fixture / "bad-diff.patch")        # behavior-changing diff
        assert not _suite_green(tmp)                    # G3 hard-gate-red -> REVERT
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rl02_bad_diff_broadens_public_api_while_suite_stays_green():
    fixture = RL / "02-broadens-api"
    tmp = _new_repo_from(fixture)
    try:
        assert _suite_green(tmp)                        # green baseline
        _apply(tmp, fixture / "bad-diff.patch")        # silent public-API broadening
        assert _suite_green(tmp)                        # test gate alone cannot catch it
        assert '"line_total"' in (tmp / "before.py").read_text()  # G4 (manifest mismatch) catches it
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@pytest.mark.skip(
    reason="03-no-span-praise is a critic-verdict fixture with no runnable code path; "
           "it is driven by the refactor-loop verdict router, not by pytest."
)
def test_rl03_critic_verdict_fixture():
    ...
