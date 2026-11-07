"""`/phil:board-snapshot` and `/phil:resume` read a GitLab board as they read a GitHub one.

Card 76's checklist, 2026-11-06: both covered GitHub only, against `CLAUDE.md`'s rule that every surface
driving a board supports both forges. `phil:issue-board` owns how a GitLab board is read; the two
surfaces cite it. Each test pins a sentence the prose must keep: it proves the sentence is there to obey,
never that a run obeys it.
"""
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ISSUE_BOARD = REPO / "skills" / "issue-board" / "SKILL.md"
SNAPSHOT_CMD = REPO / "commands" / "board-snapshot.md"
SNAPSHOT = REPO / "skills" / "board-snapshot" / "SKILL.md"
SNAPSHOT_GITLAB = REPO / "skills" / "board-snapshot" / "references" / "gitlab.md"
RESUME_CMD = REPO / "commands" / "resume.md"
BOOTSTRAP = REPO / "skills" / "session-handoff" / "references" / "bootstrap.md"


def _flat(path):
    return " ".join(path.read_text().split())


def _grant(path):
    front = yaml.safe_load(path.read_text().split("---", 2)[1])
    return {t.strip() for t in front["allowed-tools"].split(",")}


def test_issue_board_owns_how_a_gitlab_board_is_read():
    text = _flat(ISSUE_BOARD)
    assert "## Read a GitLab board's columns" in ISSUE_BOARD.read_text()
    assert "order_by=relative_position&sort=asc" in text
    assert "--paginate" in text
    assert "**An open issue with no status label sits in the board's Open list**" in text
    assert "every open issue is on the board" in text


def test_board_snapshot_reads_gitlab_instead_of_refusing_it():
    skill = _flat(SNAPSHOT)
    assert "GitHub Projects v2 only" not in skill
    assert "GitLab is not implemented" not in skill
    assert "`${CLAUDE_PLUGIN_ROOT}/skills/board-snapshot/references/gitlab.md`" in skill
    gitlab = _flat(SNAPSHOT_GITLAB)
    assert "*Read a GitLab board's columns*" in gitlab
    assert "`OFF-BOARD` never fires on GitLab" in gitlab


def test_board_snapshot_grants_gitlab_reads_and_sends_only_gets():
    grant = _grant(SNAPSHOT_CMD)
    assert {"Bash(glab api:*)", "Bash(jq:*)"} <= grant, grant
    body = _flat(SNAPSHOT_CMD)
    assert "Send `glab api` only GETs" in body
    assert "--hostname <host>" in body


def test_resume_reads_a_gitlab_board():
    grant = _grant(RESUME_CMD)
    assert {"Bash(glab api:*)", "Bash(jq:*)"} <= grant, grant
    assert "Send `glab api` only GETs" in _flat(RESUME_CMD)
    text = _flat(BOOTSTRAP)
    assert "On GitLab" in text and "*Read a GitLab board's columns*" in text
    assert re.search(r"the card carrying the In Progress label where any card does, the top card of "
                     r"the To Do label's column otherwise", text)


def _glab_api_calls(text):
    """Each `glab api` command, its backslash-continued lines joined."""
    joined = re.sub(r"\\\n\s*", " ", text)
    return [line for line in joined.splitlines() if "glab api" in line]


WRITE_FLAG = re.compile(r"\s(-f|-F|--field|--raw-field|--input|--form|-X|--method)(\s|=|$)")


def test_no_gitlab_read_carries_a_write_flag():
    """`glab api` turns into a POST once a field is added; every read here stays a GET."""
    for path in (SNAPSHOT_GITLAB, ISSUE_BOARD, BOOTSTRAP):
        for call in _glab_api_calls(path.read_text()):
            if "reorder" not in call:
                assert not WRITE_FLAG.search(call), f"{path.name}: {call.strip()}"


def test_the_write_flag_check_refuses_a_planted_write():
    """Watched red first: a continued call carrying `-f` at the end of its second line is caught."""
    planted = 'glab api --hostname h \\\n  "projects/p/issues" -f'
    assert any(WRITE_FLAG.search(c) for c in _glab_api_calls(planted))


def test_a_missing_status_label_is_never_read_as_an_empty_column():
    """A label filter naming a label the project lacks answers `200 []` (modive, 2026-11-06)."""
    assert "Confirm each status label exists before trusting an empty column" in _flat(ISSUE_BOARD)
    assert "confirm each status label exists" in _flat(SNAPSHOT_GITLAB)
    assert "a missing status label" in _flat(BOOTSTRAP)


def test_drift_maps_to_gitlab_halves():
    text = _flat(SNAPSHOT_GITLAB)
    assert "**A closed card outside Done never fires on GitLab**" in text
    assert "**A card carrying two status labels** appears in each column it holds" in text
