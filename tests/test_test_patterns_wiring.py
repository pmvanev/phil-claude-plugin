"""Structural tests for `rules/test-patterns.md` and the four skills that apply it.

The rule's smell catalogue routes every test smell to the command that fixes it. A route is a claim
about another skill — that it has a move for the smell, and that the move changes, or never changes,
what the test asserts. Those claims live in two files that change independently, so this file pins
them against each other:

- every route names a command that exists, or says `report only`;
- a smell routed to `refactor-tests` never changes what a test asserts, and names one of that skill's
  moves; a smell routed to `redesign-tests` always changes it, and names one of that skill's moves;
- every skill and agent that judges or writes tests names the rule, and the fixtures stay
  well-formed.

**What this cannot check.** It verifies a skill *names* the rule, not that a run *applies* it — the gap
`scripts/check-rule-reachability.py` states in its own header. Whether a reviewer cited the right smell
is model judgement; the fixtures' `expected.md` files carry that, and a human drives them.

Written 2026-10-09, when the rule landed.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "test-patterns.md"
SKILLS = REPO / "skills"

REFACTOR_TESTS_MOVES = (
    "Extract Fixture/Helper",
    "Reorder into Arrange-Act-Assert",
    "Rename",
    "Extract Test Helper",
)
REDESIGN_TESTS_MOVES = (
    "Assert on observable outcome",
    "Replace mock with real collaborator",
    "Replace mock with fake",
    "Inject clock / static timestamp",
    "Seed RNG",
    "Isolate shared state",
)

RD07 = SKILLS / "redesign-tests" / "self-test" / "07-unmanaged-mock-is-behaviour"
RC01 = SKILLS / "review-code" / "self-test" / "01-test-findings-name-a-pattern"


def _catalogue_rows():
    """Rows of the table under `### Smell Catalogue`, as dicts keyed by header."""
    text = RULE.read_text()
    section = text.split("### Smell Catalogue", 1)[1].split("\n### ", 1)[0]
    lines = [ln for ln in section.splitlines() if ln.startswith("|")]
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(dict(zip(header, cells)))
    return rows


def _plain(cell):
    return re.sub(r"[*`]", "", cell)


def test_the_catalogue_is_not_empty():
    """A table that parses to nothing passes every routing test below silently."""
    assert len(_catalogue_rows()) >= 10


def test_every_route_names_a_command_that_exists():
    for row in _catalogue_rows():
        route = _plain(row["Route"])
        if route == "report only":
            continue
        m = re.fullmatch(r"/phil:([a-z-]+)", route)
        assert m, f"{row['Smell']}: route {route!r} is neither a /phil: command nor 'report only'"
        assert (REPO / "commands" / f"{m.group(1)}.md").exists(), f"{route} has no command file"


def test_a_structural_route_names_a_refactor_tests_move_and_keeps_the_assertion():
    routed = [r for r in _catalogue_rows() if _plain(r["Route"]) == "/phil:refactor-tests"]
    assert routed, "nothing routes to refactor-tests — the catalogue and the skill have drifted apart"
    for row in routed:
        assert _plain(row["Changes the assertion?"]).startswith("No"), row["Smell"]
        assert set(REFACTOR_TESTS_MOVES) & _fix_names(row["Fix"]), (
            f"{row['Smell']} routes to refactor-tests but names none of its moves"
        )


def test_a_behavioural_route_names_a_redesign_tests_move_and_changes_the_assertion():
    routed = [r for r in _catalogue_rows() if _plain(r["Route"]) == "/phil:redesign-tests"]
    assert routed, "nothing routes to redesign-tests — the catalogue and the skill have drifted apart"
    for row in routed:
        assert _plain(row["Changes the assertion?"]).startswith("Yes"), row["Smell"]
        assert set(REDESIGN_TESTS_MOVES) & _fix_names(row["Fix"]), (
            f"{row['Smell']} routes to redesign-tests but names none of its moves"
        )


def test_the_moves_this_file_pins_are_the_moves_the_skills_define():
    """Otherwise the two lists above go stale while every routing test stays green."""
    refactor = (SKILLS / "refactor-tests" / "SKILL.md").read_text()
    redesign = (SKILLS / "redesign-tests" / "SKILL.md").read_text()
    for move in REFACTOR_TESTS_MOVES:
        assert f"**{move}**" in refactor, move
    for move in REDESIGN_TESTS_MOVES:
        assert f"**{move}**" in redesign, move


def test_each_test_skill_names_the_rule():
    for skill in ("review-code", "redesign-tests", "refactor-tests", "refactor"):
        assert "rules/test-patterns.md" in (SKILLS / skill / "SKILL.md").read_text(), skill


def test_each_loader_that_judges_or_writes_tests_names_the_rule():
    """These reached the rule only through `testing.md`'s pointer, which a model may not follow."""
    loaders = [SKILLS / s / "SKILL.md" for s in ("adversarial-review", "edd", "work")]
    loaders += [REPO / "agents" / f"{a}.md"
                for a in ("adversarial-reviewer", "adversarial-verifier", "refactor-critic-correctness")]
    for path in loaders:
        assert "rules/test-patterns.md" in path.read_text(), path.relative_to(REPO)


def test_review_code_backlog_carries_a_route_and_all_seven_priorities():
    body = (SKILLS / "review-code" / "SKILL.md").read_text()
    assert "- **Route**:" in body
    assert "**Priority**: {1-7}" in body


def test_review_code_keeps_test_files_out_of_the_production_priorities():
    """Otherwise a long test is a Long Function and its expected literals are Magic Numbers, routed to
    a loop that extracts them."""
    body = (SKILLS / "review-code" / "SKILL.md").read_text()
    assert "Priorities 2–5 apply to production code only" in body


def test_both_detectors_judge_a_mock_by_what_it_stands_in_for():
    """Judging by ownership flags an owned port wrapping a gateway — fixture 07's first test."""
    for skill in ("review-code", "redesign-tests"):
        body = (SKILLS / skill / "SKILL.md").read_text()
        assert "stands in for, not who owns its" in body, skill


def test_refactor_works_only_the_items_routed_to_it():
    body = (SKILLS / "refactor" / "SKILL.md").read_text()
    assert "skipped (routed to" in body


def _suite_green(cwd):
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=str(cwd), capture_output=True, text=True,
    )
    return result.returncode == 0


def test_rd07_is_wellformed_and_green():
    for name in ("manifest.json", "expected.md", "expected-backlog.md", "orders.py",
                 "test_orders_boundaries.py"):
        assert (RD07 / name).exists(), name
    json.loads((RD07 / "manifest.json").read_text())
    assert _suite_green(RD07), "a review fixture with a red suite tests the wrong thing"


def test_rd07_flags_the_owned_mock_and_never_the_unmanaged_one():
    backlog = (RD07 / "expected-backlog.md").read_text()
    assert len(re.findall(r"^### \[RD\d{3}\]", backlog, re.M)) == 1
    assert "test_place_sends_confirmation" not in backlog


REVIEW_CODE_FIXTURES = sorted((SKILLS / "review-code" / "self-test").glob("*/manifest.json"))


def test_every_review_code_fixture_is_wellformed_and_green():
    """The README promises this for each fixture, so a second one is checked the day it lands."""
    assert REVIEW_CODE_FIXTURES
    for manifest in REVIEW_CODE_FIXTURES:
        fixture = manifest.parent
        json.loads(manifest.read_text())
        for name in ("expected.md", "expected-backlog.md"):
            assert (fixture / name).exists(), f"{fixture.name}/{name}"
        assert _suite_green(fixture), f"{fixture.name}: a review fixture with a red suite tests the wrong thing"


def _fix_names(cell):
    """The names a Fix cell offers: each alternative, and its head before `for`, `as`, `to` and the like.

    So `Parameterized Test for the loop` offers `Parameterized Test`, and a bare `Assert` offers nothing.
    """
    names = set()
    for seg in re.split(r",\s*(?:or\s+)?|;\s*|\s+—\s+|:\s+|\s+or\s+", _plain(cell)):
        seg = seg.strip()
        if seg:
            names.add(seg)
            names.add(re.split(r"\s+(?:for|as|that|with|to|through)\s+", seg)[0])
    return names


def _field(item, name, where):
    m = re.search(rf"- \*\*{name}\*\*: (.+)", item)
    assert m, f"{where}: an expected Priority 6 item has no {name} field"
    return m.group(1).strip()


def test_fix_names_reject_a_fragment():
    assert "Parameterized Test" in _fix_names("Parameterized Test for the loop, literal expected values")
    assert "Rename" not in _fix_names("Renamed helper")
    assert "Assert" not in _fix_names("Assert on observable outcome: an Expected Object")


def test_every_expected_test_finding_takes_smell_fix_and_route_from_one_row():
    """Checked against the smell's own row, so a smell from one row cannot borrow another's route."""
    rows = {_plain(r["Smell"]): r for r in _catalogue_rows()}
    for manifest in REVIEW_CODE_FIXTURES:
        backlog = (manifest.parent / "expected-backlog.md").read_text()
        for item in re.split(r"^### \[R\d{3}\]", backlog, flags=re.M)[1:]:
            if not re.search(r"- \*\*Priority\*\*: 6\b", item):
                continue
            where = manifest.parent.name
            smell = _field(item, "Smell", where)
            refactoring = _field(item, "Refactoring", where)
            route = _plain(_field(item, "Route", where))
            assert smell in rows, f"{where}: {smell} is not a catalogue smell"
            assert refactoring in _fix_names(rows[smell]["Fix"]), f"{smell}: {refactoring} is not its row's fix"
            assert route == _plain(rows[smell]["Route"]), f"{smell}: {route} is not its row's route"


def test_rc01_finds_three_smells_and_leaves_the_gateway_test_alone():
    backlog = (RC01 / "expected-backlog.md").read_text()
    assert len(re.findall(r"^### \[R\d{3}\]", backlog, re.M)) == 3
    assert "send_receipt" not in backlog, "a mock at an unmanaged dependency is behaviour, not a smell"
