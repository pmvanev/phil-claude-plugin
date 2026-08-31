"""Structural tests for the ux-review self-test fixtures.

The fixtures are **model-driven by design** — judging whether an auditor cited the right success
criterion is not automatable here, and this file does not pretend otherwise. What it checks is that a
fixture is still well-formed and still names outcomes the skill actually defines.

Written 2026-08-31, when the suite was created. `ux-review` had been the only reviewer skill in the
plugin with no self-test at all, which surfaced only when four edits to what it must and must not flag
turned out to be pinned by nothing. `tests/test_session_handoff_fixtures.py` is the template, and its
docstring records why that template exists: hand-authored fixtures parse because someone was careful,
not because anything verifies it.
"""
import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "ux-review"
SELF_TEST = SKILL_DIR / "self-test"
FIXTURES = sorted(SELF_TEST.glob("*/manifest.json"))
README = (SELF_TEST / "README.md").read_text()

# Per README's outcome list. A run reports exactly one of these.
KNOWN = {
    "BACKLOG-WRITTEN",
    "BOUNDARY-HELD",
    "COUNT-CAP-NOT-FLAGGED",
    "EXEMPT-NOT-FLAGGED",
    "CITATION-CORRECT",
    "RUNTIME-DEFERRED",
    "SCOPE-FILTERED",
    "NEVER-EDITS",
}


def test_the_suite_is_not_empty():
    """A suite that discovers nothing passes every other test in this file silently."""
    assert len(FIXTURES) >= 8


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_a_companion_expected(manifest):
    data = json.loads(manifest.read_text())
    assert data["fixture"] == manifest.parent.name, "fixture key must match its directory"
    assert (manifest.parent / "expected.md").exists()
    for key in ("situation", "invocation", "expected_outcome", "expected_guard"):
        assert data.get(key), f"{manifest.parent.name} is missing {key}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_outcome_is_a_known_token(manifest):
    assert json.loads(manifest.read_text())["expected_outcome"] in KNOWN


def test_every_fixture_is_registered_in_the_readme():
    """The README is the fixture register. A fixture missing from it is invisible."""
    for manifest in FIXTURES:
        assert f"`{manifest.parent.name}/`" in README


def test_readme_lists_no_fixture_that_does_not_exist():
    on_disk = {m.parent.name for m in FIXTURES}
    listed = set(re.findall(r"`(\d\d-[a-z0-9-]+)/`", README))
    assert listed - on_disk == set(), "README names fixtures that are not on disk"


def test_fixture_numbering_is_contiguous_from_01():
    numbers = sorted(int(m.parent.name[:2]) for m in FIXTURES)
    assert numbers == list(range(1, len(numbers) + 1))


def test_every_known_outcome_is_actually_exercised():
    """An outcome in the vocabulary that no fixture produces is a gate that cannot fire."""
    used = {json.loads(m.read_text())["expected_outcome"] for m in FIXTURES}
    assert KNOWN - used == set(), f"outcomes declared but never exercised: {KNOWN - used}"


def test_exactly_one_walking_skeleton():
    flagged = [m.parent.name for m in FIXTURES
               if json.loads(m.read_text()).get("walking_skeleton")]
    assert flagged == ["01-backlog-from-real-defects"]


def test_the_boundary_fixture_carries_both_halves():
    """Fixture 02 is worthless if it only tests the side that must fire.

    The defect it guards is CONFLATION — a reviewer that flags taste, or that skips motion because
    'aesthetics are out of scope'. One file must therefore contain both, or the fixture proves only
    that the reviewer can find one thing.
    """
    data = json.loads((SELF_TEST / "02-motion-cost-in-scope-taste-is-not" / "manifest.json").read_text())
    blob = json.dumps(data).lower()
    assert "reduced-motion" in blob or "reduced motion" in blob
    assert "palette" in blob or "typeface" in blob
    expected = (SELF_TEST / "02-motion-cost-in-scope-taste-is-not" / "expected.md").read_text()
    assert "Gate failures" in expected
    assert "consider" in expected.lower(), "raising taste as a soft finding must also be a failure"
