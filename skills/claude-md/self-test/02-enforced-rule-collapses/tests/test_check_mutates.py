"""Proves scripts/check-mutates.py refuses the input that motivated it: a command declaring
`mutates: false` while granting Write."""
import subprocess, sys
from pathlib import Path


def test_refuses_a_read_only_command_that_grants_write(tmp_path):
    cmd = tmp_path / "commands" / "bad.md"
    cmd.parent.mkdir()
    cmd.write_text("---\nmutates: false\nallowed-tools: Read, Write\n---\n")
    script = Path(__file__).resolve().parent.parent / "scripts" / "check-mutates.py"
    result = subprocess.run([sys.executable, str(script), str(tmp_path)])
    assert result.returncode != 0
