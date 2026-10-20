"""Tests for `hooks/refactor-loop/block-test-file-write.py` — guard G2.

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
