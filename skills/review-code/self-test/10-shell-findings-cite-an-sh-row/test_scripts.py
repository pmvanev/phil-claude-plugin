"""Every script in the fixture parses under the shell its shebang names, so a review judges real code."""
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).parent
SCRIPTS = [
    ("bash", "deploy.sh"),
    ("bash", "rotate-logs.sh"),
    ("bash", "check-services.sh"),
    ("bash", "lib/log.sh"),
    ("bash", "lib/paths.sh"),
    ("sh", "ci-entry.sh"),
    ("sh", "bin/healthcheck"),
]


@pytest.mark.parametrize("shell, script", SCRIPTS)
def test_the_script_parses_under_its_shell(shell, script):
    assert subprocess.run([shell, "-n", str(HERE / script)], capture_output=True).returncode == 0
