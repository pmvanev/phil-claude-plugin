"""Structural tests for the issue-board self-test fixtures.

The fixtures are **model-driven by design** — judging whether a run of a prose skill reached the
right decision is not automatable, and this file does not pretend otherwise. What it checks is that
a fixture stays well-formed and keeps referring to outcomes the skill actually defines.

That gap is not hypothetical. Measured 2026-09-04 at 0.83.0: **8 of 13 self-test suites in this repo
had no driver at all, leaving 131 fixtures behind no gate** — including `groom-issues`, the largest
suite in the repo at 43. Every one of those READMEs calls itself a gate. This suite was created the
same day and shipped with a driver rather than joining them (issue #42).

Pattern copied from `tests/test_board_setup_fixtures.py`, which is the reason this suite uses the
`fixture_id` / `expected_decision` manifest scheme: the repo has two competing schemes and only that
one has a portable driver. See `skills/issue-board/self-test/README.md`.
"""

import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "issue-board"
SELF_TEST = SKILL_DIR / "self-test"
FIXTURES = sorted(SELF_TEST.glob("*/manifest.json"))

# Terminal outcomes, per self-test/README.md `## Decision outcomes`. The vocabulary grows with the
# suite: an outcome is added when a fixture needs it, never in advance.
TERMINAL = {"CHAIN-COMPOSED"}


def test_the_suite_exists_at_all():
    """issue-board was the only board-family skill with no suite. This is the regression."""
    assert SELF_TEST.is_dir(), "skills/issue-board/self-test/ must exist"
    assert (SELF_TEST / "README.md").is_file(), "a suite nobody can drive is not a suite"
    assert FIXTURES, "at least one fixture"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_a_companion_expected(manifest):
    d = json.loads(manifest.read_text())
    assert d.get("fixture_id"), "every fixture names itself"
    assert d["fixture_id"] == manifest.parent.name, "fixture_id must match its directory"
    assert (manifest.parent / "expected.md").is_file()
    assert d.get("situation"), "the shared convention: every fixture states its situation"
    assert d.get("expected_guard"), "the shared convention: every fixture names its guard"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_decision_is_exactly_one_defined_outcome(manifest):
    d = json.loads(manifest.read_text())
    dec = d["expected_decision"]
    assert isinstance(dec, list) and len(dec) == 1, \
        f"{d['fixture_id']} expects {dec} — exactly one terminal outcome"
    assert dec[0] in TERMINAL, f"{dec[0]} is not an outcome this suite defines"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_no_fixture_supplies_candidate_prose(manifest):
    """A fixture offering variants to choose between tests SELECTION, and selection is passed by
    'publish the shorter string' — the word ceiling board-prose-standard [D5] refuses. This is the
    correction skill-reviewer finding C2 forced on nwave-issue-board's fixtures 30 and 31."""
    raw = manifest.read_text()
    for banned in ("candidate_descriptions", "candidate_rendering", "candidates"):
        assert banned not in raw, \
            f"{manifest.parent.name} supplies candidate prose ({banned}) — supply the facts instead"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_composition_fixture_supplies_enumerable_facts(manifest):
    """The replacement for candidate prose: state the facts the composed text must cover."""
    d = json.loads(manifest.read_text())
    expected = (manifest.parent / "expected.md").read_text()
    if "enumerable_facts" in d:
        assert d["enumerable_facts"], "enumerable_facts must not be empty"
        assert "enumerable_facts" in expected or "fact" in expected.lower(), \
            "expected.md must assert against the facts the manifest declares"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_no_fixture_asserts_a_word_count(manifest):
    """[D5]: brevity is a principle, not a count. A fixture pinning a number would pin one of the
    standard's eleven principles and license the other ten to fail."""
    text = manifest.read_text() + (manifest.parent / "expected.md").read_text()
    for m in re.finditer(r"(?:under|at most|fewer than|max(?:imum)? of|no more than)\s+\d+\s+words", text, re.I):
        pytest.fail(f"{manifest.parent.name} asserts a word ceiling: {m.group(0)!r}")


def test_every_defined_outcome_has_a_fixture():
    """Coverage, in the direction that actually rots: an outcome defined and never exercised."""
    claimed = set()
    for manifest in FIXTURES:
        claimed.update(json.loads(manifest.read_text())["expected_decision"])
    uncovered = TERMINAL - claimed
    assert not uncovered, f"outcomes defined with no fixture: {sorted(uncovered)}"


def test_readme_documents_every_outcome_the_fixtures_use():
    """The index and the fixtures must agree. nwave-issue-board's outcome roster fell out of step
    with its fixture table the same way, caught by review rather than by a test."""
    readme = (SELF_TEST / "README.md").read_text()
    for outcome in sorted(TERMINAL):
        assert f"`{outcome}`" in readme, f"{outcome} is not documented in self-test/README.md"
