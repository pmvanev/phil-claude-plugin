"""Structural tests for the done self-test fixtures.

The fixtures are **model-driven by design** — judging whether a run rendered the right report is not
automatable here, and this file does not pretend otherwise. It checks that each fixture is well-formed,
names outcomes `skills/done/SKILL.md` defines, and that together they cover every outcome. The pattern is
`tests/test_board_snapshot_fixtures.py`.

This driver ships with the suite: issue 42 records suites in this repo whose READMEs call themselves
gates while nothing runs them.
"""
import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "done"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

TERMINAL = {"READY", "NOT-READY"}
REPORT_LINES = {"OPEN-ASKS", "NOT-LANDED", "NO-PIPELINE", "WROTE-NOTHING"}


def test_the_skill_defines_exactly_these_outcomes():
    """The sets above are the skill's own. If the skill renames one, this fails before the fixtures
    quietly name an outcome nothing defines."""
    text = (SKILL_DIR / "SKILL.md").read_text()
    section = text.split("## Decision outcomes", 1)[1].split("\n## ", 1)[0]
    named = set(re.findall(r"`([A-Z][A-Z-]+)`", section))
    assert named == TERMINAL | REPORT_LINES, named


def test_slice_01_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("01-open-checklist-item", "02-narrated-only", "03-open-pull-request",
                   "04-red-main", "05-no-pipeline", "06-session-ask-beside-the-card"):
        assert wanted in names, f"slice 01 brief names fixture {wanted}"


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
    assert set(d.get("expected_report_lines", [])) <= REPORT_LINES


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_run_claims_it_wrote_nothing(manifest):
    """Slice 01 writes nothing. The grant accepts a mutation document, so the run vouches for itself."""
    assert "WROTE-NOTHING" in json.loads(manifest.read_text())["expected_report_lines"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_an_open_ask_or_an_unlanded_merge_never_reads_ready(manifest):
    d = json.loads(manifest.read_text())
    lines = set(d["expected_report_lines"])
    if lines & {"OPEN-ASKS", "NOT-LANDED"}:
        assert d["expected_decision"] == ["NOT-READY"], d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_fixture_forbids_merging(manifest):
    """D2, AC2.4: the command never merges, whatever it finds."""
    must_not = " ".join(json.loads(manifest.read_text())["must_not"]).lower()
    assert "merge" in must_not


def test_every_outcome_has_a_fixture():
    decisions, lines = set(), set()
    for m in FIXTURES:
        d = json.loads(m.read_text())
        decisions |= set(d["expected_decision"])
        lines |= set(d["expected_report_lines"])
    assert TERMINAL - decisions == set(), TERMINAL - decisions
    assert REPORT_LINES - lines == set(), REPORT_LINES - lines
