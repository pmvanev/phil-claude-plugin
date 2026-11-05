"""Structural tests for the start self-test fixtures.

The fixtures are **model-driven by design** — judging whether a run rendered the right report is not
automatable here, and this file does not pretend otherwise. It checks that each fixture is well-formed,
names outcomes `skills/start/SKILL.md` defines, and that together they cover every outcome. The pattern is
`tests/test_done_fixtures.py`.
"""
import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "start"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

TERMINAL = {"LAUNCHED", "NOT-LAUNCHED", "UNDERWAY", "STOPPED", "NO-MATCH", "REFUSED-CLOSED", "CANNOT-RUN"}
REPORT_LINES = {"PICKED", "ANOTHERS-CARD", "OPEN-IN-DONE", "NO-DONE-WHEN", "BUILD-PATH",
                "ROUTE-OVERRIDDEN", "FILED", "CLAIMED", "NO-BOARD-BLOCK", "NOT-ASSIGNED", "CLAIM-FAILED",
                "READ-BACK-MISMATCH", "WORKTREE-CUT", "WORKTREE-ENTERED", "WORKTREE-FAILED",
                "WROTE-NOTHING"}


def test_the_skill_defines_exactly_these_outcomes():
    """The sets above are the skill's own. If the skill renames one, this fails before the fixtures
    quietly name an outcome nothing defines."""
    text = (SKILL_DIR / "SKILL.md").read_text()
    section = text.split("## Decision outcomes", 1)[1].split("\n## ", 1)[0]
    named = set(re.findall(r"`([A-Z][A-Z-]+)`", section))
    assert named == TERMINAL | REPORT_LINES, named


def test_slice_03_fixtures_exist():
    """The slice 03 brief names five fixtures."""
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("31-no-worktree-cut-fresh", "32-worktree-entered", "33-two-candidate-worktrees",
                   "34-snapshot-in-the-worktree", "35-session-in-another-worktree"):
        assert wanted in names, f"slice 03 names fixture {wanted}"


def test_slice_02_fixtures_exist():
    """The slice 02 brief names seven fixtures; another's card answered yes is 14."""
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("14-go-on-past-another", "19-card-not-on-the-board", "20-read-back-mismatch",
                   "21-no-signed-in-account", "22-unassignable-account", "23-no-board-block",
                   "24-filed-on-a-yes", "26-item-never-lands", "27-done-with-no-board-block",
                   "28-assign-silently-dropped", "29-read-fails-mid-claim", "30-blocked-card"):
        assert wanted in names, f"slice 02 names fixture {wanted}"


def test_slice_01_fixtures_exist():
    """The slice 01 brief names seven fixtures; issue 80 names the route that launches nothing."""
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("01-several-matches", "02-no-match", "03-closed-card", "04-open-card-in-done",
                   "05-someone-elses-card", "06-no-done-when", "07-build-path-overrides",
                   "08-no-yes-no-launch"):
        assert wanted in names, f"slice 01 names fixture {wanted}"


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
def test_a_run_that_stops_before_the_claim_wrote_nothing(manifest):
    """Only a run that reaches CLAIM writes. Before it, the grant accepts a mutation document, so the
    run vouches for itself."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] in {"STOPPED", "NO-MATCH", "REFUSED-CLOSED", "CANNOT-RUN"}:
        assert "WROTE-NOTHING" in d["expected_report_lines"], d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_filed_card_is_a_write(manifest):
    d = json.loads(manifest.read_text())
    if "FILED" in d["expected_report_lines"]:
        assert "WROTE-NOTHING" not in d["expected_report_lines"], d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_fixture_forbids_a_board_write(manifest):
    """Each fixture names a Status or assignee write the run must not make."""
    must_not = " ".join(json.loads(manifest.read_text())["must_not"]).lower()
    assert "status" in must_not or "assign" in must_not, manifest.parent.name


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_without_a_route_question_launches_nothing(manifest):
    """D9: a run that stopped before the route, or found no card, launched nothing."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] in {"STOPPED", "NO-MATCH", "REFUSED-CLOSED", "CANNOT-RUN"}:
        assert "ROUTE-OVERRIDDEN" not in d["expected_report_lines"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_an_override_is_a_launch(manifest):
    d = json.loads(manifest.read_text())
    if "ROUTE-OVERRIDDEN" in d["expected_report_lines"]:
        assert d["expected_decision"] == ["LAUNCHED"], d["fixture_id"]


def test_every_outcome_has_a_fixture():
    decisions, lines = set(), set()
    for m in FIXTURES:
        d = json.loads(m.read_text())
        decisions |= set(d["expected_decision"])
        lines |= set(d["expected_report_lines"])
    assert TERMINAL - decisions == set(), TERMINAL - decisions
    assert REPORT_LINES - lines == set(), REPORT_LINES - lines


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_claim_that_made_a_write_call_never_wrote_nothing(manifest):
    """A failed write is still a write call (plugin-validator, 2026-11-03)."""
    lines = set(json.loads(manifest.read_text())["expected_report_lines"])
    if lines & {"CLAIM-FAILED", "NOT-ASSIGNED", "READ-BACK-MISMATCH", "FILED"}:
        assert "WROTE-NOTHING" not in lines, manifest.parent.name


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_cut_worktree_is_a_write(manifest):
    lines = set(json.loads(manifest.read_text())["expected_report_lines"])
    if "WORKTREE-CUT" in lines:
        assert "WROTE-NOTHING" not in lines, manifest.parent.name


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_card_underway_routes_nowhere_and_cuts_nothing(manifest):
    """D2, AC4.3: a card underway names /phil:resume, recommends no route, and gets no second worktree."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"] == ["UNDERWAY"]:
        lines = set(d["expected_report_lines"])
        assert not lines & {"ROUTE-OVERRIDDEN", "BUILD-PATH", "WORKTREE-CUT"}, d["fixture_id"]


GITLAB_FIXTURES = [m for m in FIXTURES if "-gitlab-" in m.parent.name]


def test_slice_04_fixtures_exist():
    """Story 5 names eight fixtures."""
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("48-gitlab-claim-cut-fresh", "49-gitlab-another-assignee-kept",
                   "50-gitlab-no-in-progress-label", "51-gitlab-closed-card", "52-gitlab-blocked-label",
                   "53-gitlab-merge-request-underway", "54-gitlab-no-status-family",
                   "55-gitlab-filed-on-a-yes", "56-gitlab-open-with-a-done-label",
                   "57-gitlab-free-another-assignee", "58-gitlab-label-not-on-the-project",
                   "59-gitlab-several-in-progress-labels"):
        assert wanted in names, f"slice 04 names fixture {wanted}"


@pytest.mark.parametrize("manifest", GITLAB_FIXTURES, ids=lambda p: p.parent.name)
def test_every_gitlab_fixture_forbids_the_four_gitlab_traps(manifest):
    """AC5.9: a bare `-R <group/project>`, a field or method on `glab api`, a bare `--assignee`, a board
    list. Each reports success while doing the wrong thing."""
    must_not = " ".join(json.loads(manifest.read_text())["must_not"])
    for trap in ("bare `-R", "`glab api`", "bare `--assignee`", "board list"):
        assert trap in must_not, f"{manifest.parent.name} does not forbid {trap}"


@pytest.mark.parametrize("manifest", GITLAB_FIXTURES, ids=lambda p: p.parent.name)
def test_no_gitlab_fixture_stops_for_the_forge(manifest):
    """AC5.8."""
    d = json.loads(manifest.read_text())
    assert d["expected_decision"] != ["CANNOT-RUN"], d["fixture_id"]
    assert any("because the forge is GitLab" in m for m in d["must_not"]), d["fixture_id"]
