"""Proves scripts/check-mutates.py refuses each input its rule names: a `mutates: false` command
granting Write, Edit or bare Bash, and a command with no declaration. A limit no test here exercises
stays unproven, and its prose stays in CLAUDE.md."""
import subprocess, sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-mutates.py"


def _check(tmp_path, frontmatter):
    cmd = tmp_path / "commands" / "bad.md"
    cmd.parent.mkdir()
    cmd.write_text(f"---\n{frontmatter}\n---\n")
    return subprocess.run([sys.executable, str(SCRIPT), str(tmp_path)]).returncode


@pytest.mark.parametrize("grant", ["Write", "Edit", "Bash"])
def test_refuses_a_read_only_command_that_grants_a_writer(tmp_path, grant):
    assert _check(tmp_path, f"mutates: false\nallowed-tools: Read, {grant}") != 0


def test_refuses_a_command_with_no_declaration(tmp_path):
    assert _check(tmp_path, "allowed-tools: Read") != 0


def test_accepts_a_read_only_command_that_only_reads(tmp_path):
    assert _check(tmp_path, "mutates: false\nallowed-tools: Read, Grep") == 0
