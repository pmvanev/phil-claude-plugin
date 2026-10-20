"""Tests for the refactor-loop guards that read the run ledger: G2 and G7.

G2 — `hooks/refactor-loop/block-test-file-write.py`.

G2 keeps the proposer off the oracle: while a refactor-loop run is active, no Edit or Write may touch a
test file. Outside a run it must stay silent, so it never traps unrelated editing.

The two halves fail in opposite directions. With no ledger there is no run, and the hook allows. Once
the ledger exists, every input the hook cannot read is a run it cannot rule out, and the hook denies.
Wound: an undecodable ledger, or a `tool_input` that was not an object, let a test-file write through
(CWE-636, issue 48).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
HOOK = REPO / "hooks" / "refactor-loop" / "block-test-file-write.py"
LEDGER = ".refactor-loop-ledger.md"


def run(stdin, cwd):
    """Returns the permission decision, or None when the hook allows by staying silent."""
    proc = subprocess.run([sys.executable, str(HOOK)], input=stdin, cwd=cwd,
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"]


def write(tmp, tool_input):
    return run(json.dumps({"tool_name": "Write", "tool_input": tool_input, "cwd": str(tmp)}), tmp)


@pytest.fixture
def active(tmp_path):
    (tmp_path / LEDGER).write_text("active-run: true\n")
    return tmp_path


# --------------------------------------------------------------------------- the guard's job


def test_no_ledger_allows_a_test_file_write(tmp_path):
    assert write(tmp_path, {"file_path": "tests/test_x.py"}) is None


def test_an_inactive_ledger_allows_a_test_file_write(tmp_path):
    (tmp_path / LEDGER).write_text("active-run: false\n")
    assert write(tmp_path, {"file_path": "tests/test_x.py"}) is None


def test_an_active_run_denies_a_test_file_write(active):
    assert write(active, {"file_path": "tests/test_x.py"}) == "deny"


def test_an_active_run_allows_a_production_file_write(active):
    assert write(active, {"file_path": "src/app.py"}) is None


# --------------------------------------------------------------------------- fails closed once the ledger exists


def test_an_undecodable_ledger_denies(tmp_path):
    (tmp_path / LEDGER).write_bytes(b"active-run: true\n\xff\xfe")
    assert write(tmp_path, {"file_path": "tests/test_x.py"}) == "deny"


def test_a_ledger_that_is_not_a_file_denies(tmp_path):
    (tmp_path / LEDGER).mkdir()
    assert write(tmp_path, {"file_path": "tests/test_x.py"}) == "deny"


@pytest.mark.parametrize("tool_input", [["tests/test_x.py"], "tests/test_x.py", 7])
def test_a_tool_input_that_is_not_an_object_denies(active, tool_input):
    assert write(active, tool_input) == "deny"


@pytest.mark.parametrize("tool_input", [{}, {"file_path": 42}, {"file_path": ["tests/test_x.py"]}])
def test_a_target_path_that_is_not_a_string_denies(active, tool_input):
    assert write(active, tool_input) == "deny"


@pytest.mark.parametrize("stdin", ["not json", "[]", "null"])
def test_a_payload_that_is_not_an_object_denies(active, stdin):
    assert run(stdin, active) == "deny"


# --------------------------------------------------------------------------- G7: tracked ledgers
#
# `hooks/refactor-loop/reinject-pinned-constraints.py` re-states the ledger's pinned lines as context on
# every prompt. The loop writes that ledger and never commits it, so a ledger version control tracks
# came from whoever can commit to the repo, and a cloned repo could author every prompt's context
# (CWE-1427, issue 48). G7 speaks only on git's definite "not tracked" answer. Wound: the first fix
# read every git failure as untracked, so a ledger unpacked from an archive, with no `.git`, or in a
# repository git refused as dubiously owned, still reached every prompt.

G7 = REPO / "hooks" / "refactor-loop" / "reinject-pinned-constraints.py"
PINNED = "active-run: true\npinned: never edit a test\n"


def reinject(cwd, env=None):
    proc = subprocess.run([sys.executable, str(G7)], cwd=cwd, capture_output=True, text=True,
                          input=json.dumps({"prompt": "go", "cwd": str(cwd)}), timeout=30, env=env)
    assert proc.returncode == 0, proc.stderr
    if not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def test_g7_restates_the_pinned_lines_of_an_untracked_ledger(tmp_path):
    git(tmp_path, "init", "-q")
    (tmp_path / LEDGER).write_text(PINNED)
    assert "pinned: never edit a test" in reinject(tmp_path)


def test_g7_is_silent_outside_a_repository(tmp_path):
    """An archive unpacks with no `.git`, so a ledger here may be anyone's."""
    (tmp_path / LEDGER).write_text(PINNED)
    assert reinject(tmp_path) is None


def test_g7_is_silent_when_git_refuses_the_repository(tmp_path):
    import os
    git(tmp_path, "init", "-q")
    (tmp_path / LEDGER).write_text(PINNED)
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_TEST_ASSUME_DIFFERENT_OWNER": "1"}
    assert reinject(tmp_path, env) is None


def test_g7_is_silent_without_git(tmp_path):
    (tmp_path / LEDGER).write_text(PINNED)
    assert reinject(tmp_path, {"PATH": str(tmp_path)}) is None


def test_g7_is_silent_on_a_ledger_version_control_tracks(tmp_path):
    git(tmp_path, "init", "-q")
    (tmp_path / LEDGER).write_text(PINNED)
    git(tmp_path, "add", LEDGER)
    assert reinject(tmp_path) is None
