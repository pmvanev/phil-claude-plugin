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

**On fixtures that assert word counts — a sanctioned exception, recorded so it does not read as a leak.**
`CLAUDE.md` documents two opposite rulings on this. `tests/test_issue_board_fixtures.py` forbids a
fixture asserting a word count, because that suite's subject is *composition* and a word ceiling in a
fixture would pin one of `rules/writing.md`'s eleven principles of composition and license the other ten to fail.
`tests/test_board_snapshot_fixtures.py` deliberately breaks that rule and says why in its own docstring:
that skill's ceilings are a **specified feature**, so counting is the subject rather than a proxy for it.

Since 2026-09-09 (issue #43) this suite is in board-snapshot's position, not issue-board's. Fixtures 28,
29 and 31 carry measured word costs because a 300-word ceiling is a specified feature of `/phil:handoff`
and `/phil:resume`, and a ceiling fixture whose arithmetic does not force the clip is not testing the
ceiling — both 28 and 29 shipped estimates that measurement refuted, on the same day, which is why the
numbers are now inputs in the manifests rather than adjectives in the prose.

**Fixture 30 is deliberately on the other side of that line** and asserts no count: its subject is
whether the standard reaches the report's composed sentences, and it sits far inside the ceiling
precisely so length cannot be mistaken for the thing under test. `candidate_prose_supplied: false`
is explicit there for the same reason — supplying two wordings would test selection, which is passed
by picking the shorter string.
"""

import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "session-handoff"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))


def _subset(predicate, label):
    """Fixtures matching `predicate`, for a test that applies to some of them.

    **These tests used to parametrize over every fixture and `pytest.skip` the ones they did not
    apply to** — 74 skips from three tests, all of them noise. Filtering at collection instead reports
    what actually ran.

    The trade is that a filter matching nothing passes silently, where a skip at least printed a line.
    `test_every_subset_is_non_empty` closes that: an empty subset is a filter bug, and the one thing
    worse than a noisy skip is a green test over nothing."""
    matched = [m for m in FIXTURES if predicate(m)]
    SUBSETS[label] = matched
    return matched


SUBSETS: dict[str, list[Path]] = {}

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

# The 300-word report ceiling (issue #43, 2026-09-09). Additional outcomes on the two report paths, and
# **mutually exclusive** — see `test_a_run_never_both_clips_and_breaches`. A stack run reports neither,
# because `/phil:stack` deliberately carries no ceiling.
REPORT_SHAPE = {"REPORT-CLIPPED", "CEILING-BREACHED"}

LIVE = CAPTURE_TERMINAL | FRESHNESS | OWNER | BOARD | ADDITIONAL | STACK | REPORT_SHAPE
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


BOARD_FIXTURES = _subset(lambda m: bool(set(_outcomes(m)) & BOARD), "board-checking")


@pytest.mark.parametrize("manifest", BOARD_FIXTURES, ids=lambda p: p.parent.name)
def test_a_board_outcome_requires_a_board_to_have_been_read(manifest):
    """A fixture expecting a BOARD-* outcome must supply the board state the check read, or it
    asserts a conclusion drawn from nothing.

    One direction only. Fixtures 06-09 already carry `board_state` for unrelated purposes — a wave
    label to route from, a claimed card — and predate the board triple by four days. Requiring the
    converse would fail four working fixtures to satisfy a symmetry nothing needs."""
    d = json.loads(manifest.read_text())
    assert "board_state" in d, \
        f"{manifest.parent.name} expects a BOARD-* outcome but supplies no board_state to read"


def _marks_board_unreadable(m):
    board = json.loads(m.read_text()).get("board_state")
    return isinstance(board, dict) and board.get("readable") is False


UNREADABLE_FIXTURES = _subset(_marks_board_unreadable, "unreadable-board")


@pytest.mark.parametrize("manifest", UNREADABLE_FIXTURES, ids=lambda p: p.parent.name)
def test_an_unreadable_board_never_expects_agreement(manifest):
    """`BOARD-UNREADABLE` is a claim about the record; `BOARD-AGREES` is a claim about the work.
    Fixture 15 exists because defaulting one to the other is the silent failure."""
    assert "BOARD-UNREADABLE" in _outcomes(manifest), \
        f"{manifest.parent.name} marks the board unreadable but does not expect BOARD-UNREADABLE"


@pytest.mark.parametrize("manifest", BOARD_FIXTURES, ids=lambda p: p.parent.name)
def test_a_freshness_verdict_needs_both_dirty_flags(manifest):
    """SKILL.md fires RESUME-STALE when the dirty flag differs **in either direction**, so a fixture
    stating only the read-back value leaves a load-bearing input implicit. Caught by
    `plugin-dev:plugin-validator` on fixtures 13 and 15, whose capture-time value was unstated.

    Scoped to the board fixtures on purpose. Fixtures 01, 04 and 11 predate the convention — 04 states
    one flag, 01 and 11 state none — and retrofitting them would edit the inputs of fixtures pinning
    other slices' behaviour, from a card that owns none of it. Left as a known gap rather than a silent
    one; widening this scope is the fix if it ever bites."""
    d = json.loads(manifest.read_text())
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


# ---------------------------------------------------------------------------
# Frame-format invariants (live-work-stack slice 02, 2026-08-18)
#
# `crossed` counts wind-downs a frame has survived: written 0 by push, incremented by CAPTURE for
# every frame already in the file. Two invariants follow, and both were violated by four fixtures
# before the third review pass caught them by reading — nothing here was checking.
#
# That is this board's recurring defect in its sharpest form: fixture 26 encoded a state no sequence
# of pushes and captures can produce, AND its prose drew the opposite lesson from it, so a correct
# implementation would have failed its gate. A fixture that pins an unreachable state is worse than
# no fixture; it teaches the inverse of the rule.

FRAME_RE = re.compile(r"open since (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z).*?crossed (\d+|\?)\s*$")


def _stacks(manifest: Path):
    """Yield (label, header, stack) for the manifest and any run_a/run_b sub-cases."""
    d = json.loads(manifest.read_text())
    for key in (None, "run_a", "run_b"):
        src = d if key is None else d.get(key)
        if not isinstance(src, dict):
            continue
        stack = src.get("snapshot_stack")
        if not stack:
            continue
        header = src.get("snapshot_header") or d.get("snapshot_header") or {}
        yield (manifest.parent.name + (f"/{key}" if key else ""), header, stack)


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda m: m.parent.name)
def test_crossed_never_increases_with_depth(manifest: Path):
    """`CAPTURE` increments every frame together, so a child cannot outrank its parent."""
    for label, _header, stack in _stacks(manifest):
        counts = []
        for frame in stack:
            m = FRAME_RE.search(frame)
            counts.append(int(m.group(2)) if m and m.group(2).isdigit() else None)
        for i in range(len(counts) - 1):
            a, b = counts[i], counts[i + 1]
            assert a is None or b is None or b <= a, (
                f"{label}: crossed increases with depth {counts} — unreachable: a frame cannot have "
                f"been present at a capture its parent missed"
            )


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda m: m.parent.name)
def test_crossed_zero_means_pushed_since_the_last_capture(manifest: Path):
    """A frame predating a real `captured:` was in the file at that capture, so it is at least 1."""
    for label, header, stack in _stacks(manifest):
        captured = header.get("captured")
        if not captured or captured == "never":
            continue
        for frame in stack:
            m = FRAME_RE.search(frame)
            if not m or not m.group(2).isdigit():
                continue
            if m.group(1) < captured and int(m.group(2)) == 0:
                pytest.fail(
                    f"{label}: frame opened {m.group(1)} reads `crossed 0` under `captured: {captured}` "
                    f"— it was in the file at that capture, so it cannot be 0"
                )


# ---------------------------------------------------------------------------
# The report ceiling (issue #43, 2026-09-09)


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_never_both_clips_and_breaches(manifest):
    """`REPORT-CLIPPED` and `CEILING-BREACHED` are mutually exclusive, per SKILL.md.

    Where the mandatory content alone exceeds 300 words, withholding a decision saves nothing and the
    ceiling gives way — so a run reporting both has clipped for appearance while breaching anyway. The
    pair is the one place a fixture could assert compliance and a breach at the same time and look
    reasonable doing it."""
    outcomes = set(_outcomes(manifest)) & REPORT_SHAPE
    assert len(outcomes) <= 1, (
        f"{manifest.parent.name} expects {sorted(outcomes)} — clipping and breaching cannot both hold"
    )


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_stack_run_reports_no_ceiling_outcome(manifest):
    """`/phil:stack` has no ceiling, decided 2026-09-09 and recorded in SKILL.md. A stack fixture
    expecting one asserts a regime the skill refuses to have — which is exactly how somebody would
    "fix" the family's two prose regimes without noticing the decision."""
    outcomes = set(_outcomes(manifest))
    if outcomes & STACK:
        assert not (outcomes & REPORT_SHAPE), (
            f"{manifest.parent.name} is a stack fixture expecting {sorted(outcomes & REPORT_SHAPE)}; "
            f"the stack path carries no ceiling"
        )


CEILING_FIXTURES = _subset(lambda m: bool(set(_outcomes(m)) & REPORT_SHAPE), "report-ceiling")


@pytest.mark.parametrize("manifest", CEILING_FIXTURES, ids=lambda p: p.parent.name)
def test_a_ceiling_fixture_states_what_may_not_be_dropped(manifest):
    """The ceiling's whole risk is that a report drops a safety property to fit. A fixture pinning the
    ceiling without a `must_not` pins the bound and not the refusals, and the bound alone is satisfied
    by printing less of anything."""
    d = json.loads(manifest.read_text())
    assert d.get("must_not"), f"{manifest.parent.name} pins the ceiling but states no must_not"


CEILING = 300  # SKILL.md, "The report has a ceiling; the record never does"


def _why_total(d):
    """The recorded why's length, under either key the corpus uses."""
    for k in ("snapshot_why_total_words", "recorded_why_total_words"):
        if k in d:
            return d[k]
    return None


@pytest.mark.parametrize("manifest", CEILING_FIXTURES, ids=lambda p: p.parent.name)
def test_a_ceiling_fixture_measures_its_own_budget(manifest):
    """A ceiling fixture must carry measured word costs whose parts sum to their stated total.

    **Added because the defect shipped three times in one day.** Fixtures 28, 29 and 31 each first
    asserted a budget from estimated word costs, and measurement refuted all three — 29's six-deep
    stack was said to breach at ~280 when the real figure was 217, and 28's "room for about two
    decisions" would in fact have fitted all eleven recorded items. An adjective in the prose cannot be
    checked; a number in the manifest can."""
    d = json.loads(manifest.read_text())
    m = d.get("mandatory_word_cost_measured")
    assert m, f"{manifest.parent.name} pins the ceiling but measures no word cost"
    parts = {k: v for k, v in m.items() if isinstance(v, int) and k not in ("total", "room_left_for_the_echo", "room_left_for_the_why")}
    assert sum(parts.values()) == m["total"], (
        f"{manifest.parent.name}: measured parts {parts} sum to {sum(parts.values())}, "
        f"not the stated total {m['total']}"
    )
    for room_key in ("room_left_for_the_echo", "room_left_for_the_why"):
        if room_key in m:
            assert m[room_key] == CEILING - m["total"], (
                f"{manifest.parent.name}: {room_key} is {m[room_key]}, "
                f"but {CEILING} - {m['total']} is {CEILING - m['total']}"
            )


@pytest.mark.parametrize("manifest", CEILING_FIXTURES, ids=lambda p: p.parent.name)
def test_a_ceiling_fixture_arithmetic_forces_its_own_outcome(manifest):
    """The situation must actually produce the outcome the fixture expects.

    A `REPORT-CLIPPED` fixture whose why fits in the remaining budget clips nothing, and a
    `CEILING-BREACHED` fixture whose mandatory content fits under the bound breaches nothing. Either
    way the fixture passes by doing the opposite of what it tests, and reads exactly like one that
    works — the unreachable-state defect the register records about fixture 26."""
    d = json.loads(manifest.read_text())
    outcomes = set(_outcomes(manifest))
    total = d["mandatory_word_cost_measured"]["total"]

    if "CEILING-BREACHED" in outcomes:
        assert total > CEILING, (
            f"{manifest.parent.name} expects CEILING-BREACHED but its mandatory content is {total} "
            f"words, which fits under {CEILING} — nothing would breach"
        )
    if "REPORT-CLIPPED" in outcomes:
        assert total <= CEILING, (
            f"{manifest.parent.name} expects REPORT-CLIPPED but its mandatory content alone is "
            f"{total} words — that is a breach, not a clip"
        )
        why = _why_total(d)
        assert why is not None, f"{manifest.parent.name} expects a clip but states no recorded why length"
        assert why > CEILING - total, (
            f"{manifest.parent.name} expects REPORT-CLIPPED but its {why}-word why fits in the "
            f"{CEILING - total} words left — nothing would be withheld"
        )


def test_both_ceiling_branches_have_a_fixture():
    """Issue #43's done-when, asserted the way #24's was: the clip case and the breach case both exist,
    so the ceiling cannot pass by always resolving the same way."""
    expected = {o for m in FIXTURES for o in _outcomes(m)}
    assert "REPORT-CLIPPED" in expected, "no fixture covers the clipped report"
    assert "CEILING-BREACHED" in expected, "no fixture covers the mandatory content breaching"


@pytest.mark.parametrize("label", sorted(SUBSETS))
def test_every_subset_is_non_empty(label):
    """The hazard introduced by replacing skips with filters: a predicate that matches nothing makes
    every test over it pass without running. A skip at least printed a line; a filter is silent.

    So an empty subset fails here. This is the only assertion in the file that exists to protect the
    other assertions rather than the fixtures."""
    assert SUBSETS[label], f"the {label!r} subset matched no fixture — the filter is broken, not the corpus"


# The one fixture that states a dirty flag while sitting outside the both-flags rule. Named because
# converting a skip into a filter hid an exemption that used to print a line every run.
EXEMPT_FROM_BOTH_FLAGS = {"04-stale-refuses-to-resume"}


def test_the_fixtures_outside_the_both_flags_rule_are_a_known_set():
    """`test_a_freshness_verdict_needs_both_dirty_flags` applies to board fixtures only, and the
    exemption used to be visible as a skip line. Filtering hid it, so it is asserted instead.

    **Measured rather than inherited.** The old skip's docstring said fixtures 01, 04 and 11 predate
    the convention. In fact only `04-stale-refuses-to-resume` states a dirty flag at all outside the
    board fixtures, and it states one of the two; 01 and 11 state none, so they are not exempt from
    this rule — they never reach it. The first version of this assertion carried the docstring's three
    guessed names and failed on the real one, which is the check doing its job on its own author.

    Retrofitting 04 would edit inputs pinning another slice's behaviour, so it stays a known gap. If a
    NEW fixture starts comparing fingerprints outside the rule, this fails and someone decides."""
    exempt = {m.parent.name for m in FIXTURES} - {m.parent.name for m in BOARD_FIXTURES}
    carries_a_flag = {
        name for name in exempt
        if "working_tree_dirty" in (SKILL_DIR / "self-test" / name / "manifest.json").read_text()
    }
    assert carries_a_flag == EXEMPT_FROM_BOTH_FLAGS, (
        f"the set of fixtures comparing fingerprints outside the both-flags rule changed: "
        f"expected {sorted(EXEMPT_FROM_BOTH_FLAGS)}, found {sorted(carries_a_flag)}")
