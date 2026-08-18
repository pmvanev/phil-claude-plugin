"""Structural tests for the session-handoff self-test fixtures.

The fixtures are **model-driven by design** — judging whether a read-back reached the right decision
is not automatable here, and this file does not pretend otherwise. What it checks is that a fixture is
still well-formed and still names outcomes the skill actually defines.

Written 2026-08-17, when the #24 board-divergence fixtures (13-15) were added and
`plugin-dev:plugin-validator` pointed out that fifteen fixtures had zero automated coverage: they parse
because they were hand-authored carefully, not because anything verifies it. That is this board's
recurring defect — fixtures 13 and 14 exist precisely so the divergence check "cannot pass by never
firing", and nothing was asserting the fixtures themselves.

The sibling `tests/test_board_setup_fixtures.py` is the template, and it earned its keep by catching
outcome drift when a later slice retired an outcome three fixtures still referenced. Same risk here:
`SKILL.md`'s outcome vocabulary has grown three times.
"""

import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "session-handoff"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

# Per SKILL.md's `## Decision outcomes`. A capture run reports one of CAPTURE / NO-OP; a read-back
# reports one freshness verdict, one owner outcome, and — on the two paths with a recorded next
# action — one board outcome.
CAPTURE_TERMINAL = {"CAPTURE", "NO-OP"}
FRESHNESS = {"RESUME-CURRENT", "RESUME-STALE", "RECONSTRUCT"}
OWNER = {"ROUTE", "ROUTE-LIVE-WINS", "ASK-OWNER"}
BOARD = {"BOARD-AGREES", "BOARD-DIVERGES", "BOARD-UNREADABLE"}
ADDITIONAL = {"REFUSE-DERIVABLE", "PROJECTED", "PROJECTION-UNREFRESHED"}

# Slice 03 was tested and deliberately NOT built. Its outcome stays in the vocabulary because its
# fixtures stay — they are a standing record of what the skill would have to do. A fixture may expect
# it; nothing else may.
UNBUILT = {"REPORT-CLAIM-CONFLICT"}

# The stack path (`/phil:stack`, live-work-stack slice 01). Terminal and self-contained: a stack run
# reports exactly one of these and NONE of the sets above — the three paths do not interleave, which
# is why this is its own set rather than an addition to CAPTURE_TERMINAL.
STACK = {"PUSHED", "POPPED", "SHOWN", "STACK-EMPTY", "STACK-UNKNOWN", "WRITE-REFUSED"}

LIVE = CAPTURE_TERMINAL | FRESHNESS | OWNER | BOARD | ADDITIONAL | STACK
KNOWN = LIVE | UNBUILT


def _outcomes(manifest: Path) -> list[str]:
    """`expected_decision` is a bare token, an `A + B` string, or a JSON list — all three shapes are
    in the corpus. Normalising here rather than converging the fixtures keeps this file a *reader* of
    them; rewriting eight manifests to suit a test written afterwards would edit the evidence."""
    raw = json.loads(manifest.read_text())["expected_decision"]
    items = raw if isinstance(raw, list) else [raw]
    return [tok.strip() for item in items for tok in str(item).split("+") if tok.strip()]


def test_every_fixture_is_registered_in_the_readme():
    """The README is the fixture register per SKILL.md. A fixture missing from it is invisible."""
    register = (SKILL_DIR / "self-test" / "README.md").read_text()
    missing = [m.parent.name for m in FIXTURES if m.parent.name not in register]
    assert not missing, f"fixtures absent from the register: {missing}"


def test_fixture_count_is_contiguous_from_01():
    """A gap means a fixture was deleted rather than retired-in-place, which erases its reasoning."""
    numbers = sorted(int(m.parent.name[:2]) for m in FIXTURES)
    assert numbers == list(range(1, len(numbers) + 1)), f"non-contiguous fixture numbering: {numbers}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_manifest_parses_and_has_a_companion_expected(manifest):
    d = json.loads(manifest.read_text())
    assert re.fullmatch(r"SH-SELFTEST-\d\d", d.get("fixture_id", "")), \
        f"fixture_id must be SH-SELFTEST-NN, got {d.get('fixture_id')!r}"
    assert d.get("situation"), "every fixture states its situation"
    assert (manifest.parent / "expected.md").exists()


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_expected_decision_names_only_known_outcomes(manifest):
    unknown = [o for o in _outcomes(manifest) if o not in KNOWN]
    assert not unknown, (
        f"{manifest.parent.name} expects {unknown}, which SKILL.md's `## Decision outcomes` "
        f"does not define — either the outcome was retired or the fixture has drifted"
    )


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_read_back_reports_at_most_one_of_each_triple(manifest):
    """The exactly-one-of rule SKILL.md states. Two from one triple is a self-contradicting fixture."""
    outcomes = set(_outcomes(manifest))
    for name, triple in (("freshness", FRESHNESS), ("owner", OWNER), ("board", BOARD)):
        overlap = outcomes & triple
        assert len(overlap) <= 1, f"{manifest.parent.name} expects {overlap} from the {name} triple"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_board_outcome_requires_a_board_to_have_been_read(manifest):
    """A fixture expecting a BOARD-* outcome must supply the board state the check read, or it
    asserts a conclusion drawn from nothing.

    One direction only. Fixtures 06-09 already carry `board_state` for unrelated purposes — a wave
    label to route from, a claimed card — and predate the board triple by four days. Requiring the
    converse would fail four working fixtures to satisfy a symmetry nothing needs."""
    d = json.loads(manifest.read_text())
    if not set(_outcomes(manifest)) & BOARD:
        pytest.skip("not a board-checking fixture")
    assert "board_state" in d, \
        f"{manifest.parent.name} expects a BOARD-* outcome but supplies no board_state to read"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_an_unreadable_board_never_expects_agreement(manifest):
    """`BOARD-UNREADABLE` is a claim about the record; `BOARD-AGREES` is a claim about the work.
    Fixture 15 exists because defaulting one to the other is the silent failure."""
    d = json.loads(manifest.read_text())
    board = d.get("board_state")
    if not isinstance(board, dict) or board.get("readable") is not False:
        pytest.skip("fixture supplies a readable board, or none")
    assert "BOARD-UNREADABLE" in _outcomes(manifest), \
        f"{manifest.parent.name} marks the board unreadable but does not expect BOARD-UNREADABLE"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_freshness_verdict_needs_both_dirty_flags(manifest):
    """SKILL.md fires RESUME-STALE when the dirty flag differs **in either direction**, so a fixture
    stating only the read-back value leaves a load-bearing input implicit. Caught by
    `plugin-dev:plugin-validator` on fixtures 13 and 15, whose capture-time value was unstated.

    Scoped to the board fixtures on purpose. Fixtures 01, 04 and 11 predate the convention — 04 states
    one flag, 01 and 11 state none — and retrofitting them would edit the inputs of fixtures pinning
    other slices' behaviour, from a card that owns none of it. Left as a known gap rather than a silent
    one; widening this scope is the fix if it ever bites."""
    d = json.loads(manifest.read_text())
    if not set(_outcomes(manifest)) & BOARD:
        pytest.skip("predates the both-flags convention; see the docstring")
    assert "working_tree_dirty" in d and "working_tree_dirty_at_capture" in d, (
        f"{manifest.parent.name} compares fingerprints but does not state both dirty flags"
    )


def test_the_divergent_and_agreeing_cases_both_exist():
    """Issue #24's done-when, asserted directly: one fixture covers divergence and one covers
    agreement, "so the check cannot pass by never firing". A suite holding only one of them is
    satisfiable by a spine that always answers the same way."""
    expected = {o for m in FIXTURES for o in _outcomes(m)}
    assert "BOARD-DIVERGES" in expected, "no fixture covers the divergent case"
    assert "BOARD-AGREES" in expected, "no fixture covers the agreeing case"
    assert "BOARD-UNREADABLE" in expected, "no fixture covers the unreadable board"
