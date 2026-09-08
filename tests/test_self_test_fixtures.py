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
import json
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


def test_rl03_fixture_still_poses_the_question_the_anti_flattery_clause_must_answer():
    """`03-no-span-praise` is judged by the refactor-loop verdict router, not by pytest — the router
    must coerce it to `CANNOT_ASSESS` and never `accept`.

    **This replaced an empty function carrying an unconditional skip.** That stub had no body, so no
    change to anything could ever have made it fail; it reported a permanently-disabled test where
    there was no test. What is checkable here is not the coercion but the *input*: that the fixture
    still presents flattery with no span, so it is still the thing the clause has to reject.

    A fixture can rot into passing its own question — someone adds a span while tidying, and the
    router then coerces nothing, correctly, on an input that no longer poses the problem. The same
    shape as `test_the_ceiling_fixture_actually_breaches_the_ceiling` in the board suite."""
    v = json.loads((RL / "03-no-span-praise" / "verdict.json").read_text())
    assert v["verdict"] == "accept", "the fixture must ARRIVE as an accept for coercion to be tested"
    criteria = v["per_criterion"]
    assert criteria, "a verdict with no criteria tests nothing"
    assert all(c.get("span") is None for c in criteria), \
        "every criterion must lack a span; a span makes this an assessable verdict and not flattery"
    assert (RL / "03-no-span-praise" / "expected.md").exists()
