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

TERMINAL = {"PLANNED", "STOPPED", "NO-MATCH", "REFUSED-CLOSED", "CANNOT-RUN"}
OWN_LINES = {"DECLARED-PATH", "FALLBACK-PATH", "RECORDED", "ALREADY-RECORDED", "RECORD-FAILED",
             "GITHUB-ONLY", "UNDERWAY", "WROTE-NOTHING"}
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
                   "04-already-recorded", "05-gitlab", "10-nwave-no-label", "11-underway-no-worktree"):
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
def test_every_fixture_forbids_running_a_step(manifest):
    """Slice 01 stops before the first step of the path."""
    must_not = " ".join(json.loads(manifest.read_text())["must_not"]).lower()
    assert "step" in must_not, manifest.parent.name


def test_every_outcome_autopilot_adds_has_a_fixture():
    decisions, lines = set(), set()
    for m in FIXTURES:
        d = json.loads(m.read_text())
        decisions |= set(d["expected_decision"])
        lines |= set(d["expected_report_lines"])
    assert TERMINAL - decisions == set(), TERMINAL - decisions
    assert OWN_LINES - lines == set(), OWN_LINES - lines
