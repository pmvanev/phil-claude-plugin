"""CLI-level tests: every documented invocation returns a JSON refusal, never a traceback.

**This file exists because a fix was written and never called.** `classify_file` was added at 0.57.0
specifically to stop `FileNotFoundError` escaping, its docstring explains why, and its only caller in
the entire repo was its own unit test. `main()` never invoked it, so the CLI stayed broken while the
suite went green.

That is `CLAUDE.md`'s named recurring defect — *"the function was written and never called, which is
this board's recurring defect reproduced inside the fix for it"* — and its instruction is to **test
that a new check fails on the input that motivated it**. A unit test asserting `classify_file` returns
a dict does not do that. These tests run the scripts as scripts.

Callers parse stdout as JSON. A traceback is not parseable, so an unhandled exception is not a rough
edge — it is a contract break.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
REGION_PLACE = ROOT / "scripts" / "region-place.py"
RENDER_BLOCK = ROOT / "scripts" / "render-block.py"
PROBE_BOARD = ROOT / "scripts" / "probe-board.py"


def run_cli(script, *args):
    p = subprocess.run([sys.executable, str(script), *args],
                       capture_output=True, text=True, timeout=60)
    return p


def assert_json_refusal(p):
    """stdout parses as JSON and says it refused. No traceback anywhere."""
    assert "Traceback" not in p.stderr, f"unhandled exception:\n{p.stderr[-600:]}"
    try:
        payload = json.loads(p.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"stdout is not JSON:\n{p.stdout[:400]}\nstderr:\n{p.stderr[-400:]}")
    assert payload.get("status") == "refused", payload
    assert payload["refusal"]["reason"], payload
    return payload


# --- region-place.py: the absent file, the motivating input -------------------------------

def test_classify_on_an_absent_file_refuses_in_json(tmp_path):
    p = run_cli(REGION_PLACE, "--file", str(tmp_path / "nosuch.md"), "--classify")
    payload = json.loads(p.stdout)
    # `file-absent` is a STATE, not a refusal — the skill's PLACE step promises to create the file.
    assert payload.get("state") == "file-absent", payload
    assert payload["sha256"] is None
    assert "Traceback" not in p.stderr


def test_place_into_an_absent_file_creates_it_without_a_sha(tmp_path):
    """The create path was doubly unreachable: `main()` crashed before dispatch, and it demanded
    `--expect-sha`, which an absent file can never supply."""
    target = tmp_path / "nosuch.md"
    region = tmp_path / "region.md"
    region.write_text("<!-- phil:board-setup:v1:begin -->\ngenerated x\n"
                      "- Forge: GitHub *(probed · Q1)*\n<!-- phil:board-setup:v1:end -->\n")
    p = run_cli(REGION_PLACE, "--file", str(target), "--place", str(region))
    assert "Traceback" not in p.stderr, p.stderr[-500:]
    payload = json.loads(p.stdout)
    assert payload["status"] == "ok" and payload["created"] is True, payload
    assert target.exists() and "## Issue board" in target.read_text()


def test_an_existing_file_still_demands_its_sha(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# T\n")
    region = tmp_path / "region.md"
    region.write_text("<!-- phil:board-setup:v1:begin -->\nx\n<!-- phil:board-setup:v1:end -->\n")
    assert_json_refusal(run_cli(REGION_PLACE, "--file", str(target), "--place", str(region)))


def test_a_missing_region_file_refuses_in_json(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# T\n")
    assert_json_refusal(run_cli(REGION_PLACE, "--file", str(target),
                                "--place", str(tmp_path / "gone.md"), "--expect-sha", "x"))


def test_a_missing_declaration_file_refuses_in_json(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# T\n")
    assert_json_refusal(run_cli(REGION_PLACE, "--file", str(target),
                                "--declare", str(tmp_path / "gone.md"), "--expect-sha", "x"))


def test_malformed_drift_json_refuses_in_json(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# T\n\n## Issue board\n\n- a line\n")
    bad = tmp_path / "probe.json"
    bad.write_text("{not json at all")
    assert_json_refusal(run_cli(REGION_PLACE, "--file", str(target), "--drift", str(bad)))


def test_no_mode_given_refuses_in_json(tmp_path):
    target = tmp_path / "CLAUDE.md"
    target.write_text("# T\n")
    assert_json_refusal(run_cli(REGION_PLACE, "--file", str(target)))


# --- render-block.py ----------------------------------------------------------------------

def test_render_with_a_missing_probe_refuses_in_json(tmp_path):
    assert_json_refusal(run_cli(RENDER_BLOCK, "--probe", str(tmp_path / "gone.json"),
                                "--stamp", "2026-08-17T21:00Z"))


def test_render_with_malformed_probe_json_refuses_in_json(tmp_path):
    bad = tmp_path / "probe.json"
    bad.write_text("{nope")
    assert_json_refusal(run_cli(RENDER_BLOCK, "--probe", str(bad),
                                "--stamp", "2026-08-17T21:00Z"))


def test_render_refuses_a_probe_that_did_not_succeed(tmp_path):
    """A refused probe must not render as a valid region.

    `render_region` did not read `probe["status"]`, so a refusal produced a well-formed,
    marker-carrying, `probed`-labelled region with zero facts and exit 0 — which then passed
    `region-place`'s marker checks and reached disk. Fixture 02 forbids exactly this and was enforced
    only by model discipline, in the one place the design deliberately moved off it.
    """
    refused = tmp_path / "probe.json"
    refused.write_text(json.dumps({"schema": "board-setup-probe/v1", "status": "refused",
                                   "refusal": {"reason": "missing project scope",
                                               "fix": "gh auth refresh -s project"}}))
    p = run_cli(RENDER_BLOCK, "--probe", str(refused), "--stamp", "2026-08-17T21:00Z")
    assert "phil:board-setup:v1:begin" not in p.stdout, "a refused probe rendered a region"
    assert_json_refusal(p)


# --- probe-board.py: the promised forge/host mismatch refusal ------------------------------

def test_a_forge_host_mismatch_is_refused_as_the_help_text_promises():
    """`--forge`'s help says a GitLab host with `--forge github` "is refused rather than
    half-served". No such check existed, so it probed the wrong forge and reported `status: ok`."""
    assert_json_refusal(run_cli(PROBE_BOARD, "--repo", "a/b",
                                "--host", "gitlab.com", "--forge", "github"))
    assert_json_refusal(run_cli(PROBE_BOARD, "--repo", "a/b",
                                "--host", "github.com", "--forge", "gitlab"))
