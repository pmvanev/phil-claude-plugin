"""Structural tests for `rules/test-patterns.md` and the four skills that apply it.

The rule's smell catalogue routes every test smell to the command that fixes it. A route is a claim
about another skill — that it has a move for the smell, and that the move changes, or never changes,
what the test asserts. Those claims live in two files that change independently, so this file pins
them against each other:

- every route names a command that exists, or says `report only`;
- a smell routed to `refactor-tests` never changes what a test asserts, and names one of that skill's
  moves; a smell routed to `redesign-tests` always changes it, and names one of that skill's moves;
- the four skills name the rule, and the two new fixtures stay well-formed.

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
        assert any(m in _plain(row["Fix"]) for m in REFACTOR_TESTS_MOVES), (
            f"{row['Smell']} routes to refactor-tests but names none of its moves"
        )


def test_a_behavioural_route_names_a_redesign_tests_move_and_changes_the_assertion():
    routed = [r for r in _catalogue_rows() if _plain(r["Route"]) == "/phil:redesign-tests"]
    assert routed, "nothing routes to redesign-tests — the catalogue and the skill have drifted apart"
    for row in routed:
        assert _plain(row["Changes the assertion?"]).startswith("Yes"), row["Smell"]
        assert any(m in _plain(row["Fix"]) for m in REDESIGN_TESTS_MOVES), (
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


def test_rc01_is_wellformed_and_green():
    for name in ("manifest.json", "expected.md", "expected-backlog.md", "invoice.py",
                 "test_invoice.py"):
        assert (RC01 / name).exists(), name
    json.loads((RC01 / "manifest.json").read_text())
    assert _suite_green(RC01), "a review fixture with a red suite tests the wrong thing"


def test_rc01_every_test_finding_names_a_catalogue_fix_and_route():
    backlog = (RC01 / "expected-backlog.md").read_text()
    items = re.split(r"^### \[R\d{3}\]", backlog, flags=re.M)[1:]
    assert len(items) == 3
    fixes = " ".join(_plain(r["Fix"]) for r in _catalogue_rows())
    routes = {_plain(r["Route"]) for r in _catalogue_rows()}
    smells = {_plain(r["Smell"]) for r in _catalogue_rows()}
    for item in items:
        smell = re.search(r"- \*\*Smell\*\*: (.+)", item).group(1).strip()
        refactoring = re.search(r"- \*\*Refactoring\*\*: (.+)", item).group(1).strip()
        route = _plain(re.search(r"- \*\*Route\*\*: (.+)", item).group(1).strip())
        assert smell in smells, smell
        assert refactoring in fixes, refactoring
        assert route in routes, route
    assert "send_receipt" not in backlog, "a mock at an unmanaged dependency is behaviour, not a smell"
