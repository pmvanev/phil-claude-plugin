"""Structural tests for the board-setup self-test fixtures.

The fixtures are **model-driven by design** — judging whether a run reached the right decision is
not automatable here, and this file does not pretend otherwise. What it does check is that a
fixture is still well-formed and still refers to outcomes the skill actually defines.

That gap was real: nothing detected a fixture whose JSON broke, whose `expected.md` went missing, or
whose `expected_decision` named a retired outcome. `SECTION-EXISTS` was retired in slice 02 and
three fixtures referenced it; only one of them was meant to.
"""

import json
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "board-setup"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

# The terminal outcomes and the two report lines, per SKILL.md's `## Decision outcomes`.
TERMINAL = {"WROTE", "WROTE-BESIDE-PROSE", "REFRESHED", "UNCHANGED", "DECLARED",
            "AMBIGUOUS-TARGET", "REFUSED", "MALFORMED-MARKERS"}
REPORT_LINES = {"DRIFT", "REPORTED-NOT-WRITTEN", "UNEVALUATED"}

# Two outcomes have been retired by later slices, each by the slice that shipped the thing it was
# deferring to. They may appear in a `must_not` or a `supersedes` — never as an expectation. This test
# file caught the drift when slices 03-06 landed, which is the only reason it exists.
RETIRED = {"SECTION-EXISTS", "REGION-PRESENT"}


def test_fixtures_exist():
    assert len(FIXTURES) >= 7, f"expected the seven slice-01/02 fixtures, found {len(FIXTURES)}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_a_companion_expected(manifest):
    d = json.loads(manifest.read_text())
    assert d.get("fixture_id"), "every fixture names itself"
    assert (manifest.parent / "expected.md").exists()


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_decision_is_exactly_one_live_terminal_outcome(manifest):
    """The rule SKILL.md states. A fixture carrying two is how the one-outcome contradiction hid."""
    d = json.loads(manifest.read_text())
    dec = d["expected_decision"]
    assert len(dec) == 1, f"{d['fixture_id']} expects {dec} — exactly one terminal outcome"
    assert dec[0] in TERMINAL, f"{dec[0]} is not a defined outcome"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_report_lines_are_report_lines_and_never_outcomes(manifest):
    d = json.loads(manifest.read_text())
    for line in d.get("expected_report_lines", []):
        assert line in REPORT_LINES, f"{line} is not a report line"
    assert not (set(d["expected_decision"]) & REPORT_LINES), \
        "a report line cannot be the terminal outcome"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_retired_outcome_is_only_ever_referenced_as_retired(manifest):
    """`SECTION-EXISTS` may appear in a `must_not` or a `supersedes` — never as an expectation."""
    d = json.loads(manifest.read_text())
    assert not (set(d["expected_decision"]) & RETIRED)
    assert not (set(d.get("expected_report_lines", [])) & RETIRED)


def test_every_live_outcome_has_a_fixture_or_a_recorded_reason():
    """One gap is known and disclosed: AMBIGUOUS-TARGET needs a session rooted in a two-remote
    checkout, so it cannot be reached from a fixture. Any *other* uncovered outcome is an
    oversight, and this test is what tells the two apart."""
    covered = {json.loads(m.read_text())["expected_decision"][0] for m in FIXTURES}
    uncovered = TERMINAL - covered
    assert uncovered <= {"AMBIGUOUS-TARGET"}, f"undisclosed uncovered outcomes: {uncovered}"
