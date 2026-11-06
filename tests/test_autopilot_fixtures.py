"""Structural tests for the autopilot self-test fixtures.

The fixtures are model-driven: judging whether a run printed the right path is a read by hand. This file
checks that each fixture is well-formed, names outcomes `skills/autopilot/SKILL.md` defines, and that
together they cover every outcome autopilot adds. The pattern is `tests/test_start_fixtures.py`.
"""
import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "autopilot"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

TERMINAL = {"PLANNED", "CARRIED", "BLOCKED", "STOPPED", "NO-MATCH", "REFUSED-CLOSED", "CANNOT-RUN"}
OWN_LINES = {"DECLARED-PATH", "FALLBACK-PATH", "RECORDED", "ALREADY-RECORDED", "RECORD-FAILED",
             "DONE-IS-YOURS", "UNDERWAY", "RESUMED", "LANDED", "HANDED-OFF", "WROTE-NOTHING"}
RUNS_STEPS = {"CARRIED", "BLOCKED"}
FROM_START = {"PICKED", "ANOTHERS-CARD", "OPEN-IN-DONE", "CLAIMED", "NO-BOARD-BLOCK", "NOT-ASSIGNED",
              "CLAIM-FAILED", "READ-BACK-MISMATCH", "WORKTREE-CUT", "WORKTREE-ENTERED", "WORKTREE-FAILED"}
STOPS_BEFORE_CLAIM = {"STOPPED", "NO-MATCH", "REFUSED-CLOSED", "CANNOT-RUN"}


def test_the_skill_defines_exactly_these_outcomes():
    text = (SKILL_DIR / "SKILL.md").read_text()
    section = text.split("## Decision outcomes", 1)[1].split("\n## ", 1)[0]
    named = set(re.findall(r"`([A-Z][A-Z-]+)`", section))
    assert named == TERMINAL | OWN_LINES | FROM_START, named ^ (TERMINAL | OWN_LINES | FROM_START)


def test_slice_01_fixtures_exist():
    """The slice 01 brief names AC1.1 and AC1.2; the rest cover the outcomes."""
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("01-declared-path-beside-nwave", "02-no-declared-path", "03-nwave-fallback",
                   "04-already-recorded", "05-gitlab-path-recorded", "10-nwave-no-label",
                   "11-underway-no-worktree", "12-done-step-is-yours", "14-move-to-done-is-yours",
                   "15-gitlab-already-recorded"):
        assert wanted in names, f"slice 01 names fixture {wanted}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_is_well_formed(manifest):
    d = json.loads(manifest.read_text())
    for key in ("fixture_id", "situation", "why_this_fixture_exists"):
        assert d.get(key), f"{manifest.parent.name} lacks {key}"
    assert (manifest.parent / "expected.md").exists()
    assert d.get("must_not"), "a fixture that forbids nothing cannot fail a right-for-the-wrong-reason run"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_exactly_one_terminal_outcome_and_only_known_report_lines(manifest):
    d = json.loads(manifest.read_text())
    assert len(d["expected_decision"]) == 1 and d["expected_decision"][0] in TERMINAL
    assert set(d.get("expected_report_lines", [])) <= OWN_LINES | FROM_START


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_that_stops_before_the_claim_wrote_nothing(manifest):
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] in STOPS_BEFORE_CLAIM:
        assert "WROTE-NOTHING" in d["expected_report_lines"], d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_planned_run_read_a_path(manifest):
    """Every planned run printed a path, declared or fallen back to — never both, never neither."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"] == ["PLANNED"]:
        found = {"DECLARED-PATH", "FALLBACK-PATH"} & set(d["expected_report_lines"])
        assert len(found) == 1, d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_that_runs_no_step_forbids_running_one(manifest):
    """`--plan` and every stop before the path stop before its first step."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] not in RUNS_STEPS:
        assert "step" in " ".join(d["must_not"]).lower(), d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_that_runs_steps_forbids_answering_as_the_developer(manifest):
    """Spike row 5: an answer the run took never reads as the developer's."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] in RUNS_STEPS:
        must_not = " ".join(d["must_not"]).lower()
        assert "developer answered" in must_not, d["fixture_id"]
        assert "/phil:done" in must_not, d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_that_runs_steps_is_handed_off(manifest):
    """D8, D13: every run that reaches RUN ends with /phil:handoff, unless its fixture is about the
    handoff failing."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] in RUNS_STEPS and "handoff fails" not in d["situation"]:
        assert "HANDED-OFF" in d["expected_report_lines"], d["fixture_id"]


def test_slice_02_and_03_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("16-carried-to-landing", "17-rule-answers", "18-blocker-own-material",
                   "19-check-keeps-failing", "20-resumed", "21-unnamed-write-stops",
                   "22-gitlab-carried", "23-path-end-hands-off", "24-blocker-still-stands",
                   "25-route-verdict-is-yours"):
        assert wanted in names, f"slices 02 and 03 name fixture {wanted}"


def test_slice_04_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("26-red-pipeline-fixed", "27-red-pipeline-blocks", "28-default-branch-red",
                   "29-no-pipeline", "30-wave-boundary", "31-last-wave-stays-in-progress",
                   "32-closing-reference-blocks", "33-gitlab-no-pipeline",
                   "34-default-branch-red-before-merge"):
        assert wanted in names, f"slice 04 names fixture {wanted}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_landed_run_never_closes_the_card(manifest):
    """D13: landing is not done; the card stays open and In Progress."""
    d = json.loads(manifest.read_text())
    if "LANDED" in d["expected_report_lines"]:
        must_not = " ".join(d["must_not"]).lower()
        assert "closing keyword" in must_not or "close the card" in must_not, d["fixture_id"]
        assert "HANDED-OFF" in d["expected_report_lines"], d["fixture_id"]


def test_the_register_lists_every_token_each_manifest_expects():
    """Both reviewers found the register's Outcome column dropping tokens the manifests expect."""
    register = (SKILL_DIR / "self-test" / "README.md").read_text()
    for m in FIXTURES:
        d = json.loads(m.read_text())
        row = next(line for line in register.splitlines() if f"`{m.parent.name[3:]}`" in line)
        cells = set(re.findall(r"`([A-Z][A-Z-]+)`", row))
        assert cells == set(d["expected_decision"]) | set(d["expected_report_lines"]), m.parent.name


def test_every_outcome_autopilot_adds_has_a_fixture():
    decisions, lines = set(), set()
    for m in FIXTURES:
        d = json.loads(m.read_text())
        decisions |= set(d["expected_decision"])
        lines |= set(d["expected_report_lines"])
    assert TERMINAL - decisions == set(), TERMINAL - decisions
    assert OWN_LINES - lines == set(), OWN_LINES - lines


def test_slice_05_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("35-dogfood-from-repo-guide", "36-dogfood-test-account", "37-dogfood-local-run",
                   "38-dogfood-no-way-blocks", "39-no-running-product-no-walk",
                   "40-repo-rule-binds-the-walk"):
        assert wanted in names, f"slice 05 names fixture {wanted}"
