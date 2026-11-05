"""`commands/autopilot.md` loads `skills/autopilot/SKILL.md`; together they carry autopilot's slice 01.

Slice 01 is the walking skeleton: the run claims the card through `/phil:start`'s steps, reads the
repo's build path from its prose, prints each step beside its source line with the writes the path
authorizes, records both on the card, and stops before the first step. Each test pins one decision from
`docs/feature/autopilot/feature-delta.md` as a string the prose must keep. A test cannot prove a run
obeys the sentence; it proves the sentence is still there to obey, and it fails when someone deletes it.
"""
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "autopilot.md"
SKILL = REPO / "skills" / "autopilot" / "SKILL.md"


def _parts(path):
    _, front, body = path.read_text().split("---", 2)
    return yaml.safe_load(front), " ".join(body.split())


def _tools():
    front, _ = _parts(COMMAND)
    return {t.strip() for t in front["allowed-tools"].split(",")}


def test_the_command_declares_its_grant_and_loads_the_skill():
    """D11: the run writes to the forge and git."""
    front, body = _parts(COMMAND)
    assert front["mutates"] is True
    assert front.get("argument-hint")
    assert "${CLAUDE_PLUGIN_ROOT}/skills/autopilot/SKILL.md" in body


def test_no_file_write_and_no_bare_bash_is_granted():
    tools = _tools()
    assert not tools & {"Write", "Edit", "NotebookEdit"}, tools
    assert "Bash" not in tools, "a bare Bash grant can do anything"


def test_slice_01_grants_the_comment_and_no_filing_or_launch():
    """D6 records on the card; slice 01 files no card (D9) and launches no step (slice 02 adds Skill)."""
    tools = _tools()
    assert "Bash(gh issue comment:*)" in tools
    assert "Bash(gh issue create:*)" not in tools
    assert "Skill" not in tools


def test_the_skill_has_plugin_dev_frontmatter():
    front, _ = _parts(SKILL)
    assert front["name"] == "autopilot"
    assert front["description"].startswith("This skill should be used when")


def test_the_writing_standard_is_named_from_the_plugin_root_and_read():
    """D6, AC2.4: the card comment is composed prose on the board. A bare path resolves against the
    consumer's repo, so the citation must carry the plugin root."""
    for path in (COMMAND, SKILL):
        _, body = _parts(path)
        bare = [m.start() for m in re.finditer(r"rules/writing\.md", body)
                if not body[:m.start()].endswith("${CLAUDE_PLUGIN_ROOT}/")]
        assert not bare, f"{path.name}: a bare rules/writing.md resolves against the consumer's repo"
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in _parts(SKILL)[1]


def test_every_ask_follows_the_decision_request_standard():
    _, body = _parts(SKILL)
    assert "${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md" in body


def test_every_gh_call_names_the_repo():
    for path in (SKILL, COMMAND):
        _, body = _parts(path)
        assert "Pass `-R <owner/repo>` on every `gh issue` call" in body, path.name
        assert "the owner and repo as variables to" in body, path.name


def test_the_claim_and_worktree_come_from_start_and_its_route_never_runs():
    """D5: compose the command that owns the step."""
    _, body = _parts(SKILL)
    assert "${CLAUDE_PLUGIN_ROOT}/skills/start/SKILL.md" in body
    assert "RESOLVE, CHECK, CLAIM and WORKTREE" in body
    assert "Skip its DESCRIBE and ROUTE" in body


def test_a_declared_path_beats_detection():
    """D2, AC1.1."""
    _, body = _parts(SKILL)
    assert "A declared path beats detection" in body
    assert "`AGENTS.md`" in body


def test_a_fallback_is_named_with_the_rule_that_chose_it():
    """D2, AC1.2."""
    _, body = _parts(SKILL)
    assert "FALLBACK-PATH" in body
    assert "name the rule that chose it" in body


def test_each_step_is_printed_beside_its_source_line():
    """D2, AC1.3: nothing can check a prose reading, so the run shows it."""
    _, body = _parts(SKILL)
    assert "beside the line it came from, quoted in its own words" in body


def test_the_authorized_writes_are_listed_before_any_step():
    """D4, AC1.4."""
    _, body = _parts(SKILL)
    assert "AUTHORIZED" in body
    assert "only the writes the path names" in body


def test_slice_01_runs_no_step():
    _, body = _parts(SKILL)
    assert "Stop before the first step of the path" in body


def test_gitlab_stops_with_a_named_outcome():
    """D10 and CLAUDE.md: a surface that covers one forge says so and stops on the other."""
    for path in (SKILL, COMMAND):
        _, body = _parts(path)
        assert "GITHUB-ONLY" in body, path.name
    assert "covers GitHub only" in _parts(SKILL)[1]


def test_no_match_offers_no_filing():
    """D9: filing a card is a write the path does not name."""
    _, body = _parts(SKILL)
    assert "offer no filing" in body


def test_an_identical_record_is_never_posted_twice():
    _, body = _parts(SKILL)
    assert "ALREADY-RECORDED" in body


def test_the_nwave_fallback_needs_a_wave_label():
    """Route rule 2 and `phil:nwave-issue-board`: no label, no wave. Both reviewers caught the first draft
    sending an unlabelled bug fix through DISCUSS to DELIVER (fixture 10)."""
    _, body = _parts(SKILL)
    assert "**A card with a `wave:` label**" in body
    assert "no label, or a label the table has no row for" in body
    assert "from DISCUSS with no label" not in body


def test_starts_endings_go_on_to_path():
    """Start's text names `/phil:resume`, DESCRIBE and ROUTE as next; autopilot runs PATH instead."""
    _, body = _parts(SKILL)
    assert "go on to PATH instead" in body
    assert "without its `next:` clause" in body
    assert "go on to PATH and RECORD" in body


def test_a_step_already_run_is_marked_done():
    """D5: the path names the next step, read from disk, never from memory."""
    _, body = _parts(SKILL)
    assert "whose `Board:` line names the card" in body
    assert "name the first step not done as the next" in body


def test_a_question_writes_nothing():
    """The yes comes from running the command, not from loading the skill."""
    _, body = _parts(SKILL)
    assert "print the path and write nothing" in body


def test_the_duplicate_check_compares_only_what_is_quoted():
    """Composed labels differ run to run; comparing them would post a duplicate every time (fixture 04)."""
    _, body = _parts(SKILL)
    assert "The comment's first line is exactly `**Autopilot · build path**`" in body
    assert "they are not compared" in body
    assert "A read that fails posts nothing: `RECORD-FAILED`" in body


def test_the_example_authorizes_no_close():
    """This repo's CLAUDE.md names no close or cleanup; the first draft's example authorized one."""
    _, body = _parts(SKILL)
    example = body.split("Starting the run authorizes:", 1)[1].split("```", 1)[0]
    assert "close" not in example and "cleanup" not in example, example


def test_claude_md_lists_the_path_comment_among_board_surfaces():
    """CLAUDE.md, 'Board surfaces that compose prose': every such surface is named there."""
    text = " ".join((REPO / "CLAUDE.md").read_text().split())
    section = text.split("## Board surfaces that compose prose", 1)[1].split(" ## ", 1)[0]
    assert "`/phil:autopilot`'s path comment" in section
