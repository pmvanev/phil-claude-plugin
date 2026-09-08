"""Structural tests for the board-snapshot self-test fixtures.

The fixtures are **model-driven by design** — judging whether a run rendered the right snapshot is not
automatable here, and this file does not pretend otherwise. What it checks is that a fixture is still
well-formed and still names outcomes the skill actually defines.

**This driver ships with the suite rather than after it.** Issue #42 records eight suites in this repo
whose READMEs call themselves gates while nothing runs them — 131 fixtures behind no gate, with a green
run reading as though they had been checked. Adding an undriven ninth would be committing that defect
inside the feature that cites it.

The pattern, including the honest statement of what a structural driver cannot judge, is
`tests/test_board_setup_fixtures.py`.

Note on fixture 01, which asserts a word count: `CLAUDE.md` records that the issue-board prose fixtures
may not assert one. That rule protects the *prose standard*, where a count turns composition into
brevity. The 200-word ceiling here is a specified feature of the command, demanded by issue #34 together
with a fixture on a board large enough to breach it. Different subject, opposite conclusion, stated so
nobody reconciles them by deleting the wrong one.
"""

import json
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "board-snapshot"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

# Per SKILL.md's `## Decision outcomes`.
TERMINAL = {"SNAPSHOT-RENDERED", "SNAPSHOT-CLIPPED", "SNAPSHOT-PARTIAL"}
REPORT_LINES = {"DRIFT", "UNCOLUMNED", "INFLATION", "READ-ONLY"}

CEILING = 200


def test_fixtures_exist():
    assert len(FIXTURES) >= 7, f"expected the seven slice-01 fixtures, found {len(FIXTURES)}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_a_companion_expected(manifest):
    d = json.loads(manifest.read_text())
    assert d.get("fixture_id"), "every fixture names itself"
    assert d.get("situation"), "every fixture states the board it describes"
    assert d.get("why_this_fixture_exists"), "a fixture that cannot say why it exists is not a gate"
    assert (manifest.parent / "expected.md").exists()


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_decision_is_exactly_one_live_terminal_outcome(manifest):
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
def test_read_only_is_claimed_on_every_run(manifest):
    """`READ-ONLY` is a claim about the calls a run made, not about the tool list. The grant accepts a
    mutation document, so a fixture that omits the claim is describing a run nobody vouched for."""
    d = json.loads(manifest.read_text())
    assert "READ-ONLY" in d.get("expected_report_lines", []), \
        f"{d['fixture_id']} must claim READ-ONLY"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_fixture_forbids_something(manifest):
    """A fixture with no `must_not` cannot fail a run that did the right thing for the wrong reason."""
    d = json.loads(manifest.read_text())
    assert d.get("must_not"), f"{d['fixture_id']} forbids nothing"


def test_every_live_outcome_has_a_fixture():
    """No disclosed gaps at slice 01. Any uncovered outcome here is an oversight, not a known limit."""
    covered = {json.loads(m.read_text())["expected_decision"][0] for m in FIXTURES}
    assert TERMINAL - covered == set(), f"uncovered terminal outcomes: {TERMINAL - covered}"


def test_every_report_line_has_a_fixture():
    covered = set()
    for m in FIXTURES:
        covered |= set(json.loads(m.read_text()).get("expected_report_lines", []))
    assert REPORT_LINES - covered == set(), f"uncovered report lines: {REPORT_LINES - covered}"


def test_the_ceiling_fixture_actually_breaches_the_ceiling():
    """The card demands a fixture on a board large enough to breach 200 words. A 'breaching' board that
    would in fact fit tests nothing, and its green run is the false negative issue #42 is about."""
    m = SKILL_DIR / "self-test" / "01-ceiling-breached" / "manifest.json"
    b = json.loads(m.read_text())["board"]
    rendered_cards = b["blocked"] + b["in_flight"] + b["n_requested"]
    assert rendered_cards * 12 > CEILING, (
        f"{rendered_cards} cards at a conservative 12 words each is {rendered_cards * 12} words, "
        f"which does not exceed the {CEILING}-word ceiling — this fixture cannot force a clip"
    )


def test_the_clipping_fixture_is_the_only_one_expecting_a_clip():
    """Clipping is the ceiling firing. A second fixture expecting it would mean the ceiling is being
    hit by boards that were never built to breach it, which is a sizing bug in the fixtures."""
    clipping = [json.loads(m.read_text())["fixture_id"] for m in FIXTURES
                if json.loads(m.read_text())["expected_decision"] == ["SNAPSHOT-CLIPPED"]]
    assert clipping == ["BSNAP-SELFTEST-01"], f"unexpected clipping fixtures: {clipping}"
