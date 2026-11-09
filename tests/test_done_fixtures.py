"""Structural tests for the done self-test fixtures.

The fixtures are **model-driven by design** — judging whether a run rendered the right report is not
automatable here, and this file does not pretend otherwise. It checks that each fixture is well-formed,
names outcomes `skills/done/SKILL.md` defines, and that together they cover every outcome. The pattern is
`tests/test_board_snapshot_fixtures.py`.

This driver ships with the suite: issue 42 records suites in this repo whose READMEs call themselves
gates while nothing runs them.
"""
import json
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "done"
FIXTURES = sorted((SKILL_DIR / "self-test").glob("*/manifest.json"))

TERMINAL = {"NOT-READY", "STOPPED", "CLOSED", "CLOSE-FAILED", "FINISHED"}
REPORT_LINES = {"OPEN-ASKS", "NOT-LANDED", "NO-PIPELINE", "ASK-DROPPED", "READ-BACK-MISMATCH",
                "BLOCK-REFRESHED", "CLEARED", "LEFT", "WROTE-NOTHING"}


def test_the_skill_defines_exactly_these_outcomes():
    """The sets above are the skill's own. If the skill renames one, this fails before the fixtures
    quietly name an outcome nothing defines."""
    text = (SKILL_DIR / "SKILL.md").read_text()
    section = text.split("## Decision outcomes", 1)[1].split("\n## ", 1)[0]
    named = set(re.findall(r"`([A-Z][A-Z-]+)`", section))
    assert named == TERMINAL | REPORT_LINES, named


def test_slice_01_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("01-open-checklist-item", "02-narrated-only", "03-open-pull-request",
                   "04-red-main", "05-no-pipeline", "06-session-ask-beside-the-card"):
        assert wanted in names, f"slice 01 brief names fixture {wanted}"


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
def test_wrote_nothing_exactly_when_nothing_was_written(manifest):
    """Keyed on the writes, not the close: a run whose read-back finds the card open still wrote, and a
    CLOSE-FAILED run whose first write failed wrote nothing (skill-reviewer, 2026-11-02)."""
    d = json.loads(manifest.read_text())
    assert isinstance(d.get("writes"), list), f"{d['fixture_id']} must list the writes it expects"
    assert ("WROTE-NOTHING" in d["expected_report_lines"]) is (d["writes"] == []), d["fixture_id"]
    if d["expected_decision"][0] in ("NOT-READY", "STOPPED"):
        assert d["writes"] == [], d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_past_the_report_states_the_developers_answers(manifest):
    """STOPPED and CLOSED depend on what the developer answered; a fixture that omits it is unjudgeable."""
    d = json.loads(manifest.read_text())
    if d["expected_decision"][0] in ("STOPPED", "CLOSED", "CLOSE-FAILED"):
        assert d.get("developer_answers"), d["fixture_id"]
    if d["expected_decision"][0] == "FINISHED" and d["writes"]:
        assert d.get("developer_answers"), f"{d['fixture_id']}: a write runs only on an answer"


def test_slice_02_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("14-ask-dropped-with-a-reason", "15-comment-before-done", "16-read-back-mismatch",
                   "17-finished-block", "18-stop-at-the-plan", "19-a-write-fails",
                   "20-stop-at-resolve", "21-card-not-on-this-board", "22-card-already-closed"):
        assert wanted in names, f"slice 02 brief names fixture {wanted}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_an_open_ask_or_an_unlanded_merge_never_reads_ready(manifest):
    d = json.loads(manifest.read_text())
    lines = set(d["expected_report_lines"])
    if "NOT-LANDED" in lines:
        assert d["expected_decision"] == ["NOT-READY"], d["fixture_id"]
    if "OPEN-ASKS" in lines and "ASK-DROPPED" not in lines:
        assert d["expected_decision"] in (["NOT-READY"], ["STOPPED"]), d["fixture_id"]


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_every_fixture_forbids_merging(manifest):
    """D2, AC2.4: the command never merges, whatever it finds."""
    must_not = " ".join(json.loads(manifest.read_text())["must_not"]).lower()
    assert "merge" in must_not


def test_every_outcome_has_a_fixture():
    decisions, lines = set(), set()
    for m in FIXTURES:
        d = json.loads(m.read_text())
        decisions |= set(d["expected_decision"])
        lines |= set(d["expected_report_lines"])
    assert TERMINAL - decisions == set(), TERMINAL - decisions
    assert REPORT_LINES - lines == set(), REPORT_LINES - lines


def test_slice_03_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("23-earlier-sessions-worktree-removed", "24-unmerged-branch-survives", "25-dirty-worktree-survives",
                   "26-name-only-branch-is-no-candidate", "27-clean-finish-asks-once",
                   "28-retire-the-snapshot-here", "29-current-worktree-removed-last",
                   "30-remote-tip-ahead-of-the-merge", "31-local-tip-ahead-of-the-merge",
                   "32-retire-refused", "33-shared-or-foreign-branch-held",
                   "34-push-url-names-another-repo", "35-another-authors-pull-request",
                   "36-force-delete-an-unmerged-branch", "37-colleague-reused-the-name",
                   "38-too-many-commits-to-show"):
        assert wanted in names, f"slice 03 brief names fixture {wanted}"


def test_a_clean_finish_asks_exactly_one_question():
    """KPI and AC4.5: ceremony on a clean finish is the anxiety the plan's one yes answers."""
    d = json.loads((SKILL_DIR / "self-test" / "27-clean-finish-asks-once" / "manifest.json").read_text())
    assert d["questions_asked"] == 1


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_no_fixture_expects_a_force(manifest):
    """D9: a fixture expecting a forced delete would teach the run to use one."""
    d = json.loads(manifest.read_text())
    forced = [w for w in d.get("writes", []) if " -f " in w
              or ("--force" in w and "--force-with-lease=" not in w)]
    assert not forced, d["fixture_id"]
    if any(" -D" in w for w in d.get("writes", [])):
        assert any(a.startswith("force-delete") for a in d.get("developer_answers", [])), \
            f"{d['fixture_id']}: `-D` runs only on the developer's own answer for that branch"
    removals = [w for w in d.get("writes", []) if "remove the worktree" in w]
    if removals:
        situation = d["situation"]
        assert any(k in situation for k in ("unlocked", "no lock", "`EnterWorktree`")), \
            f"{d['fixture_id']}: a removed worktree's situation must rule out another session's lock"
    if removals:
        assert d.get("worktree_state") == "CLEAN", \
            f"{d['fixture_id']}: a worktree goes only where worktree-state.py reads it CLEAN"


def test_any_clean_worktree_fixtures_exist():
    """The developer's answer, 2026-11-05: a clean, unlocked worktree at the merged tip goes, whoever
    made it; a lock still holds one."""
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("23-earlier-sessions-worktree-removed", "29-current-worktree-removed-last",
                   "50-locked-worktree-is-held", "51-locked-session-worktree-is-listed"):
        assert wanted in names, wanted
    locked = json.loads((SKILL_DIR / "self-test" / "50-locked-worktree-is-held" / "manifest.json")
                        .read_text())
    assert not [w for w in locked["writes"] if "remove the worktree" in w]


def test_slice_05_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("47-session-worktree-removed", "48-hidden-work-holds-the-worktree",
                   "49-session-worktree-with-a-snapshot"):
        assert wanted in names, f"slice 05 names fixture {wanted}"


def test_slice_04_fixtures_exist():
    names = {m.parent.name for m in FIXTURES}
    for wanted in ("39-gitlab-card-closes", "40-gitlab-pipeline-still-running",
                   "41-gitlab-fork-merge-request-held", "42-no-card-clean-finish",
                   "43-no-card-open-session-task", "44-no-card-retire-the-snapshot-only",
                   "45-no-card-branch-the-session-never-named", "46-no-card-reused-branch-name"):
        assert wanted in names, f"slice 04 brief names fixture {wanted}"


CARD_WRITES = ("comment", "note", "status", "close")


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_a_run_without_a_card_writes_nothing_to_a_card(manifest):
    """Slice 04: with no argument the run closes no card, whatever the session mentioned."""
    d = json.loads(manifest.read_text())
    if not d.get("no_card"):
        return
    assert d["expected_decision"][0] in ("FINISHED", "NOT-READY", "STOPPED"), d["fixture_id"]
    touched = [w for w in d["writes"] if any(k in w.lower() for k in CARD_WRITES)]
    assert not touched, f"{d['fixture_id']}: {touched}"


@pytest.mark.parametrize("manifest", FIXTURES, ids=lambda p: p.parent.name)
def test_finished_belongs_to_a_run_without_a_card(manifest):
    d = json.loads(manifest.read_text())
    assert (d["expected_decision"][0] == "FINISHED") <= bool(d.get("no_card")), d["fixture_id"]
    if d.get("no_card"):
        assert d["expected_decision"][0] not in ("CLOSED", "CLOSE-FAILED"), d["fixture_id"]


def test_a_no_card_finish_holding_only_the_snapshot_asks_once():
    d = json.loads((SKILL_DIR / "self-test" / "44-no-card-retire-the-snapshot-only" /
                    "manifest.json").read_text())
    assert d["questions_asked"] == 1, "one question, about the snapshot alone"



VERDICT_FIXTURES = [m for m in FIXTURES if "snapshot_verdict" in json.loads(m.read_text())]
VERDICT_SHAPES = (
    r"STALE — snapshot at [0-9a-f]{7,}, HEAD is now [0-9a-f]{7,} \(\d+ commits?\); tree (clean|dirty)",
    r"STALE — snapshot at [0-9a-f]{7,}, not in HEAD's history \(another branch, or rebased\); HEAD is now [0-9a-f]{7,}",
    r"STALE — snapshot at [0-9a-f]{7,} recorded a (clean|dirty) tree; the tree is now (clean|dirty)",
    r"CURRENT — snapshot at [0-9a-f]{7,}, HEAD; tree (clean|dirty)",
)


@pytest.mark.parametrize("manifest", VERDICT_FIXTURES, ids=lambda p: p.parent.name)
def test_the_snapshot_here_carries_a_verdict_and_survives_a_plain_yes(manifest):
    """The developer's answer, 2026-11-09: the plan marks the snapshot here STALE or CURRENT, as
    /phil:resume judges it, and a plain yes still keeps it, because a note about other work in flight
    turns stale too once anything merges."""
    d = json.loads(manifest.read_text())
    assert any(re.fullmatch(s, d["snapshot_verdict"]) for s in VERDICT_SHAPES), d["snapshot_verdict"]
    assert d["developer_answers"] == ["yes"]
    assert not [w for w in d["writes"] if "snapshot" in w], "a plain yes keeps the snapshot here"
    assert "LEFT" in d["expected_report_lines"]


def test_every_verdict_shape_has_a_fixture_and_appears_in_clear():
    """A run that marks every snapshot STALE must fail a fixture (skill-reviewer, 2026-11-09)."""
    verdicts = [json.loads(m.read_text())["snapshot_verdict"] for m in VERDICT_FIXTURES]
    for shape in (VERDICT_SHAPES[0], VERDICT_SHAPES[1], VERDICT_SHAPES[3]):
        assert any(re.fullmatch(shape, v) for v in verdicts), shape
    clear = (SKILL_DIR / "references" / "clear.md").read_text()
    for shape in VERDICT_SHAPES:
        assert re.search(shape, clear), shape
