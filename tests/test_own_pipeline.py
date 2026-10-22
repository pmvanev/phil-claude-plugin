"""This repository's own pipeline keeps the andon its policy declares.

`CLAUDE.md` declares an Andon field, so `.github/workflows/ci.yml` must pull the cord on a red main
(PIPE-25), through `scripts/ci/run.sh andon`. That task is copied from `/phil:build-ci`'s reference
script, whose behaviour `tests/test_build_ci.py` pins, so this file holds the copy to the reference.

Written 2026-10-22, when the andon landed.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POLICY = REPO / "CLAUDE.md"
WORKFLOW = REPO / ".github" / "workflows" / "ci.yml"
SCRIPT = REPO / "scripts" / "ci" / "run.sh"
EXAMPLE = REPO / "skills" / "build-ci" / "examples" / "run.sh"


def _task(script, name):
    """A `case` branch of the entry-point script, from its label to its `;;`."""
    m = re.search(rf"^  {name}\)\n.*?^    ;;\n", script.read_text(), re.M | re.S)
    assert m, f"{script.relative_to(REPO)} has no {name} task"
    return m.group(0)


def _jobs():
    """Each job's name and its block of `ci.yml`."""
    body = WORKFLOW.read_text().split("\njobs:\n", 1)[1]
    return dict(re.findall(r"^  ([\w-]+):\n((?:^(?:    .*)?\n)*)", body, re.M))


def test_the_policy_declares_an_andon():
    policy = POLICY.read_text().split("## CI policy", 1)[1].split("\n## ", 1)[0]
    assert "- **Andon**:" in policy


def test_the_workflow_pulls_the_cord_on_a_red_main():
    jobs = _jobs()
    andon = jobs.pop("andon")
    needs = re.search(r"^    needs: \[(.+)\]$", andon, re.M)
    assert needs and set(n.strip() for n in needs.group(1).split(",")) == set(jobs), "needs every other job"
    assert "if: failure() && github.ref == 'refs/heads/main'" in andon
    assert re.search(r"^    permissions:\n      contents: read\n      issues: write\n", andon, re.M)
    assert "./scripts/ci/run.sh andon" in andon and "GH_TOKEN: ${{ github.token }}" in andon


def test_the_andon_task_is_the_reference_scripts():
    assert _task(SCRIPT, "andon") == _task(EXAMPLE, "andon")
