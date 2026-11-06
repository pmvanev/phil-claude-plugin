"""`commands/autopilot.md` loads `skills/autopilot/SKILL.md` and its references; together they carry
autopilot's slices 01 to 03.

Slice 01 claims the card, reads the build path, prints and records it. Slices 02 and 03 run the path:
each step through the command that owns it, each question answered by a recorded rule or the
recommendation and recorded on the card, a blocker described on the card and handed off, a later run
resumed where the last stopped. Each test pins one decision from `docs/feature/autopilot/feature-delta.md`
as a string the prose must keep. A test cannot prove a run obeys the sentence; it proves the sentence
is still there to obey, and it fails when someone deletes it.
"""
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "autopilot.md"
SKILL_DIR = REPO / "skills" / "autopilot"
SKILL = SKILL_DIR / "SKILL.md"
RUN = SKILL_DIR / "references" / "run.md"
RECORD = SKILL_DIR / "references" / "record.md"


def _parts(path):
    _, front, body = path.read_text().split("---", 2)
    return yaml.safe_load(front), " ".join(body.split())


def _flat(path):
    return " ".join(path.read_text().split())


def _all():
    """The skill body and its references: a pin holds wherever the skill keeps the sentence."""
    return " ".join([_parts(SKILL)[1], _flat(RUN), _flat(RECORD)])


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
    """The work a step does runs under the session's own permissions, as `/phil:start`'s inline route
    does; the grant holds only autopilot's own calls."""
    tools = _tools()
    assert not tools & {"Write", "Edit", "NotebookEdit"}, tools
    assert "Bash" not in tools, "a bare Bash grant can do anything"


def test_the_grant_launches_steps_and_records_and_files_no_card():
    """D5 launches each step's owner through Skill; D6 records on both forges; D9 files no card."""
    tools = _tools()
    assert {"Skill", "Bash(gh issue comment:*)", "Bash(glab issue note:*)"} <= tools
    assert not tools & {"Bash(gh issue create:*)", "Bash(glab issue create:*)"}


def test_the_skill_has_plugin_dev_frontmatter():
    front, _ = _parts(SKILL)
    assert front["name"] == "autopilot"
    assert front["description"].startswith("This skill should be used when")


def test_the_skill_reads_each_reference_whole():
    body = _parts(SKILL)[1].lower()
    for ref in ("references/run.md", "references/record.md"):
        assert f"read `${{claude_plugin_root}}/skills/autopilot/{ref}` whole" in body, ref


def test_the_writing_standard_is_named_from_the_plugin_root_and_read():
    """D6, AC2.4: the card comments are composed prose on the board. A bare path resolves against the
    consumer's repo, so the citation must carry the plugin root."""
    for path in (COMMAND, SKILL, RUN, RECORD):
        text = " ".join(path.read_text().split())
        bare = [m.start() for m in re.finditer(r"rules/writing\.md", text)
                if not text[:m.start()].endswith("${CLAUDE_PLUGIN_ROOT}/")]
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


def test_plan_runs_no_step():
    """Slice 01's behaviour survives as `--plan`: print and record the path, run nothing."""
    _, body = _parts(SKILL)
    assert "With `--plan`, stop before the first step of the path" in body


def test_landing_waits_for_a_later_release():
    """Slice 04 owns the push, the pull request and the merge."""
    assert "Stop before the first landing step" in _all()


def test_gitlab_ships_with_github():
    """D10 and CLAUDE.md (2026-11-05): a surface never ships covering one forge."""
    text = _all()
    assert "${CLAUDE_PLUGIN_ROOT}/skills/start/references/gitlab.md" in text
    assert "glab issue note <n> -R <repo> --message" in text
    assert "--hostname <host>" in text
    for path in (SKILL, COMMAND, RUN, RECORD):
        raw = path.read_text()
        assert "GITHUB-ONLY" not in raw and "GitHub only" not in raw, path.name
    assert {"Bash(glab api:*)", "Bash(jq:*)", "Bash(glab issue update:*)"} <= _tools()


def test_done_is_the_developers():
    """D13: the developer inspects and approves before anything calls the work done."""
    _, skill = _parts(SKILL)
    _, command = _parts(COMMAND)
    assert "**Leave done to the developer**" in skill
    assert "run no `/phil:done`, close no card, authorize no close" in skill
    assert "run no `/phil:done`, and close no card" in command
    assert "a close never is" in skill


def test_a_close_by_side_effect_is_the_developers_too():
    """D13: a Done Status, a done label, or a closing keyword closes the card as surely as /phil:done."""
    _, body = _parts(SKILL)
    assert "a Done Status, or a done label" in body
    assert "never after a closing keyword such as `Closes`, `Fixes` or `Resolves`" in body
    assert "Next: yours — step <k>" in body


def test_no_match_offers_no_filing():
    """D9: filing a card is a write the path does not name."""
    assert "offer no filing" in _parts(SKILL)[1]


def test_an_identical_record_is_never_posted_twice():
    text = _all()
    assert "ALREADY-RECORDED" in text
    assert "they are not compared" in text


def test_no_note_line_starts_a_gitlab_quick_action():
    """GitLab runs a note line that starts with `/close` with the poster's rights."""
    assert "never with `/`: GitLab runs a note line that starts with a quick action" in _all()


def test_a_failed_glab_read_is_judged_by_glab_not_jq():
    assert "judge the read by `glab`'s own output" in _all()


def test_the_nwave_fallback_needs_a_wave_label():
    _, body = _parts(SKILL)
    assert "**A card with a `wave:` label**" in body
    assert "no label, or a label the table has no row for" in body


def test_starts_endings_go_on_to_path():
    _, body = _parts(SKILL)
    assert "go on to PATH instead" in body
    assert "without its `next:` clause" in body


def test_a_step_already_run_is_marked_done():
    """D5: the run learns where it stands from disk and the card, never from memory."""
    text = _all()
    assert "whose `Board:` line names the card" in text
    assert "a step comment marks it done" in text


def test_a_question_writes_nothing():
    """The yes comes from running the command, not from loading the skill."""
    assert "print the path and write nothing" in _parts(SKILL)[1]


# --- slices 02 and 03: run the path -----------------------------------------------------------

def test_the_developers_standing_prompt_is_carried_verbatim():
    """D12: the developer's own prompt answers a launched route's questions; no hook ships."""
    quote = " ".join(line[2:] for line in RUN.read_text().splitlines() if line.startswith("> "))
    assert ("proceed as independently as possible (through each wave if using nwave). keep the issue "
            "updated as you go.") in quote
    assert ("go with our recommendations to questions/options that arise unless you feel I really need "
            "to weight in.") in quote
    assert not (REPO / "hooks" / "autopilot").exists(), "D12 ships no hook"


def test_a_question_is_answered_by_rule_then_blocker_then_recommendation():
    """D1, D9, AC2.1–AC2.3, in that order."""
    text = _flat(RUN)
    rule = text.index("**A recorded rule answers it**")
    blocker = text.index("**One of the three kinds stops the run**")
    rec = text.index("**Otherwise take the recommendation**")
    assert rule < blocker < rec


def test_the_three_kinds_are_d1s():
    text = _flat(RUN)
    for kind in ("an outward or irreversible write the path does not name",
                 "an input only the developer holds",
                 "a check that still fails after two fixes"):
        assert kind in text, kind


def test_no_answer_is_passed_off_as_the_developers():
    """Spike row 5: a pre-filled answer reads as 'User answered', a false record."""
    text = _flat(RUN)
    assert "Never call the question tool during a run" in text
    assert "never write that the developer answered" in text


def test_a_check_is_a_circuit_breaker():
    """D1's third kind, named as the protocol it is."""
    assert "circuit breaker, `k = 2`" in _flat(RUN)


def test_a_blocker_is_described_then_handed_off():
    """D8, AC3.1: the comment first, then /phil:handoff."""
    text = _flat(RUN)
    assert text.index("Post the blocker comment first") < text.index("then run `/phil:handoff`")


def test_a_later_run_resumes_where_the_last_stopped():
    """AC3.2: the next step is the first one neither the disk nor a step comment marks done."""
    assert "RESUMED" in _all()
    assert "the first step neither the disk nor a step comment marks done" in _all()


def test_each_step_posts_its_decisions():
    """D6, AC2.2: one comment per step, its decisions listed."""
    text = _flat(RECORD)
    assert "`**Autopilot · step <k> of <m>**`" in text
    assert "`**Autopilot · blocked at step <k> of <m>**`" in text
    assert "blocked at step <k>**`" not in text, "one blocker header, with its `of <m>`"


def test_an_approval_a_route_reserves_is_the_developers():
    """D1's second kind covers a launched route's human gate (fixture 25)."""
    assert "an approval a launched route reserves for them" in _flat(RUN)


def test_an_agent_step_launches_through_the_agent_tool():
    """This repo's own review passes are agents, which the Skill tool cannot launch."""
    assert "launch it through the Agent tool" in _flat(RUN)


def test_a_mixed_step_leaves_its_landing_and_is_not_done():
    """Fixture 22: the work is done, the landing is left, and the step is not marked done."""
    text = _all()
    assert "`— work done, landing left`" in text


def test_a_step_comment_matches_only_its_own_source_line():
    """A changed path renumbers steps; a step comment marks a step done only for the same line."""
    assert "quotes the same source line the path gives that step now" in _flat(RUN)


def test_progress_marks_are_not_compared_on_the_path_comment():
    """Fixture 20: progress lives in step comments, so a resumed run does not repost the path."""
    assert "The `done` marks and the words the run composed may differ; they are not compared" in _flat(RECORD)


def test_a_denied_tool_call_is_a_blocker():
    assert "A tool call the session denies is a blocker" in _flat(RUN)


def test_the_report_prints_before_the_handoff():
    """`/phil:handoff` ends the turn's recorded exchange; autopilot's report must come first."""
    text = _flat(RUN)
    assert text.index("print the REPORT") < text.index("then run `/phil:handoff`")


def test_the_cleanup_line_defers_to_d13():
    assert "The prompt's cleanup line is `/phil:done`'s" in _flat(RUN)


def test_claude_md_lists_the_path_comment_among_board_surfaces():
    """CLAUDE.md, 'Board surfaces that compose prose': every such surface is named there."""
    text = " ".join((REPO / "CLAUDE.md").read_text().split())
    section = text.split("## Board surfaces that compose prose", 1)[1].split(" ## ", 1)[0]
    assert "`/phil:autopilot`'s path, step and blocker comments" in section
