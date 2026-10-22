"""The SessionStart invariant runner finishes inside its hook's timeout, and so reports.

`.claude/settings.json` gives `scripts/check-invariants.py` a fixed timeout, and the runner gives each
check its own. A check that cannot finish in time reports a timeout every session, which trains a
reader to skip the report: the silence this runner exists to break, in the opposite direction. The
suite took 25-90 s against a 30 s limit, so from the day CI landed (1.5.x) every SessionStart printed
"REPO INVARIANT CHECK FAILED". CI now runs the suite on every pull request and every main commit.

Written 2026-10-22.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNNER = REPO / "scripts" / "check-invariants.py"
SETTINGS = REPO / ".claude" / "settings.json"


def _hook_timeout():
    hooks = json.loads(SETTINGS.read_text())["hooks"]["SessionStart"][0]["hooks"]
    return next(h["timeout"] for h in hooks if "check-invariants.py" in h["command"])


def test_the_runner_finishes_inside_its_hook_and_reports_nothing_on_a_passing_tree():
    start = time.monotonic()
    out = subprocess.run([sys.executable, str(RUNNER)], capture_output=True, text=True,
                         timeout=_hook_timeout())
    elapsed = time.monotonic() - start
    assert elapsed < _hook_timeout() / 2, f"{elapsed:.0f}s leaves no margin under the hook's limit"
    assert out.stdout == "", out.stdout


def test_ci_runs_the_suite_the_runner_left_out():
    """The suite left SessionStart only because CI runs it; if CI stops, the reason goes with it."""
    script = (REPO / "scripts" / "ci" / "run.sh").read_text()
    workflow = (REPO / ".github" / "workflows" / "ci.yml").read_text()
    assert "python3 -m pytest -q" in script and "./scripts/ci/run.sh test" in workflow
    assert "check-tests.py" not in RUNNER.read_text()
