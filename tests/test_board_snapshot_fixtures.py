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

import importlib.util
import json
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "board-snapshot"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

# Per SKILL.md's `## Decision outcomes`.
TERMINAL = {"SNAPSHOT-RENDERED", "SNAPSHOT-CLIPPED", "SNAPSHOT-PARTIAL"}
REPORT_LINES = {"DRIFT", "UNCOLUMNED", "INFLATION", "READ-ONLY"}

CEILING = 200
PER_ROW_BOUND = 100
MODES = {"standing", "all"}

_pl_spec = importlib.util.spec_from_file_location(
    "plain_language", Path(__file__).resolve().parent.parent / "scripts" / "plain_language.py")
plain_language = importlib.util.module_from_spec(_pl_spec)
_pl_spec.loader.exec_module(plain_language)


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


# --- slice 02: the two modes bound themselves differently, so the fixtures are held to different rules ---

@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_fixture_declares_its_mode(manifest):
    """Without this the rules below cannot be applied, and a fixture would fall through both."""
    d = json.loads(manifest.read_text())
    assert d.get("mode") in MODES, f"{d['fixture_id']} declares mode {d.get('mode')!r}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_the_orientation_read_can_never_clip(manifest):
    """`--all` drops nothing, so SNAPSHOT-CLIPPED there is a defect wearing an outcome name."""
    d = json.loads(manifest.read_text())
    if d["mode"] != "all":
        return
    assert d["expected_decision"] != ["SNAPSHOT-CLIPPED"], \
        f"{d['fixture_id']} expects a clip in a mode that drops nothing"


def test_both_modes_have_fixtures():
    modes = {json.loads(m.read_text())["mode"] for m in FIXTURES}
    assert modes == MODES, f"a mode with no fixture is untested: {MODES - modes}"


def test_the_over_length_counterexample_really_is_over_length():
    """Fixture 09 supplies a description that must be rejected for length. A counterexample that would
    in fact pass tests nothing, and its green run is the false negative issue #42 is about — the same
    check `test_the_ceiling_fixture_actually_breaches_the_ceiling` makes one mode over.

    Counted with `scripts/plain_language.py`, which is the point of the extraction: the fixture and the
    decision-request hook now measure length with the same function rather than two copies of it."""
    m = SKILL_DIR / "self-test" / "09-title-is-not-a-description" / "manifest.json"
    text = json.loads(m.read_text())["counterexamples"]["over_the_bound"]
    over = plain_language.over_ceiling(text, ceiling=PER_ROW_BOUND)
    assert over, f"the counterexample is {plain_language.words(text)} words, within the {PER_ROW_BOUND} bound"


def test_the_reworded_title_counterexample_is_short_enough_to_be_tempting():
    """The rewording failure is not caught by length — that is exactly why it needs its own rule. A
    counterexample that also breached the bound would let a length check appear to cover it."""
    m = SKILL_DIR / "self-test" / "09-title-is-not-a-description" / "manifest.json"
    text = json.loads(m.read_text())["counterexamples"]["reworded_title"]
    assert plain_language.over_ceiling(text, ceiling=PER_ROW_BOUND) is None, \
        "this counterexample must fail on rewording alone, not on length"


def test_counterexamples_are_forbidden_outputs_and_never_candidate_prose():
    """`CLAUDE.md` records that a board fixture may not supply candidate prose — text the run could
    select instead of composing. A counterexample is the opposite: prose the run must NOT produce. The
    distinction is checkable, so it is checked. Every fixture carrying counterexamples must also carry
    a `must_not` clause, which is what makes them forbidden rather than offered."""
    for m in FIXTURES:
        d = json.loads(m.read_text())
        if "counterexamples" in d:
            assert d.get("must_not"), f"{d['fixture_id']} supplies prose and forbids nothing"
        assert "candidates" not in d and "suggestions" not in d, \
            f"{d['fixture_id']} supplies candidate prose, which turns composition into selection"
