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
    assert "- **Andon**:" in policy and "- **Notify**:" in policy


def test_the_workflow_pulls_the_cord_on_a_red_main():
    jobs = _jobs()
    jobs.pop("tell-author", None)
    andon = jobs.pop("andon")
    needs = re.search(r"^    needs: \[(.+)\]$", andon, re.M)
    assert needs and set(n.strip() for n in needs.group(1).split(",")) == set(jobs), "needs every other job"
    assert "if: failure() && github.ref == 'refs/heads/main'" in andon
    assert re.search(r"^    permissions:\n      contents: read\n      issues: write\n", andon, re.M)
    assert "./scripts/ci/run.sh andon" in andon and "GH_TOKEN: ${{ github.token }}" in andon


def test_the_workflow_names_whoever_started_a_failed_run():
    jobs = _jobs()
    tell = jobs.pop("tell-author")
    jobs.pop("andon")
    needs = re.search(r"^    needs: \[(.+)\]$", tell, re.M)
    assert needs and set(n.strip() for n in needs.group(1).split(",")) == set(jobs), "needs every gating job"
    assert "if: failure()" in tell
    assert re.search(r"^    permissions:\n      contents: read\n      pull-requests: write\n", tell, re.M)
    assert "PR_NUMBER: ${{ github.event.pull_request.number }}" in tell and "./scripts/ci/run.sh tell-author" in tell


def test_the_andon_and_author_tasks_are_the_reference_scripts():
    for name in ("andon", "tell-author", "inform"):
        assert _task(SCRIPT, name) == _task(EXAMPLE, name), name
    fn = re.compile(r"^tell_author\(\) \{\n.*?^\}\n", re.M | re.S)
    assert fn.search(SCRIPT.read_text()).group(0) == fn.search(EXAMPLE.read_text()).group(0)
