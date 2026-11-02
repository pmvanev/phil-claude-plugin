"""`commands/done.md` loads `skills/done/SKILL.md`; together they carry finish-work's slice 01 decisions.

Slice 01 is the ready-to-close report: it lists every ask with its evidence and says whether the work
landed, and it writes nothing. Each test pins one decision from
`docs/feature/finish-work/feature-delta.md` as a string the prose must keep. A test cannot prove a run
obeys the sentence; it proves the sentence is still there to obey, and it fails when someone deletes it.
"""
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "done.md"
SKILL = REPO / "skills" / "done" / "SKILL.md"


def _parts(path):
    _, front, body = path.read_text().split("---", 2)
    return yaml.safe_load(front), " ".join(body.split())


def test_the_command_declares_its_grant_and_loads_the_skill():
    front, body = _parts(COMMAND)
    assert front["mutates"] is True, "D10: gh api graphql can mutate, so the grant mutates"
    assert front.get("argument-hint")
    assert "${CLAUDE_PLUGIN_ROOT}/skills/done/SKILL.md" in body


def test_no_file_write_is_granted():
    """Slice 02 writes to the forge only: the comment, the Status and the close. No grant writes a file."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    assert not tools & {"Write", "Edit", "NotebookEdit"}, tools
    assert "Bash" not in tools, "a bare Bash grant can do anything"


def test_the_skill_has_plugin_dev_frontmatter():
    front, _ = _parts(SKILL)
    assert front["name"] == "done"
    assert front["description"].startswith("This skill should be used when")


def test_the_writing_standard_is_named_from_the_plugin_root_and_read():
    """D6: the report is composed prose. A bare path resolves against the consumer's repo."""
    for path in (COMMAND, SKILL):
        _, body = _parts(path)
        bare = [m.start() for m in re.finditer(r"rules/writing\.md", body)
                if not body[:m.start()].endswith("${CLAUDE_PLUGIN_ROOT}/")]
        assert not bare, f"{path.name}: a bare rules/writing.md resolves against the consumer's repo"
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in _parts(SKILL)[1]


def test_the_asks_come_from_the_card_and_the_session():
    """D1, AC1.1, AC1.2."""
    _, body = _parts(SKILL)
    assert "checklist" in body and "*Done when*" in body
    assert "the current session" in body


def test_a_sentence_is_not_evidence():
    """D1, AC1.3: an ask whose only support is a claim that it was done stays open."""
    _, body = _parts(SKILL)
    assert "A sentence saying an ask was done is not evidence" in body
    assert "A ticked box is not evidence" in body


def test_it_never_merges_and_never_calls_no_pipeline_green():
    """D2, AC2.3, AC2.4."""
    _, body = _parts(SKILL)
    assert "Never merge" in body
    assert "`no pipeline`, never green" in body


def test_every_gh_call_names_the_repo():
    """`phil:issue-board`: an inferred remote reads the wrong repo successfully. `gh api graphql` takes
    no `-R` (it fails with "unknown shorthand flag"), so the repo reaches it as query variables."""
    for path in (SKILL, COMMAND):
        _, body = _parts(path)
        assert "Pass `-R <owner/repo>` on every `gh issue` call" in body, path.name
        assert "which takes no `-R`" in body, path.name
    assert "on every `gh` call" not in _parts(SKILL)[1]


def test_reads_go_through_graphql_and_writes_through_named_commands():
    _, body = _parts(SKILL)
    assert "Send only `query` documents through `gh api graphql`, never `mutation`" in body
    assert "Write nothing before the developer's yes" in body


def test_a_branch_never_identifies_the_work_by_name_alone():
    """D8: the forge here links no pull request to its card, so the card's pull requests are found by
    the card's number in their title or body — never by a branch name."""
    _, body = _parts(SKILL)
    assert "never by a branch name" in body


def test_landing_needs_a_merge_into_the_default_branch():
    """plugin-validator, 2026-11-02: a pull request closed unmerged satisfied LANDED on its own, and a
    stacked pull request merged into a feature branch counted as landed."""
    _, body = _parts(SKILL)
    assert "at least one pull request merged into the default branch" in body
    assert "merged into any other base has not landed" in body


def test_no_pipeline_never_fires_not_landed():
    """plugin-validator, 2026-11-02: `NOT-LANDED` read "main not green", which a repo with no pipeline
    also is, contradicting fixture 05."""
    _, body = _parts(SKILL)
    assert "main not green" not in body
    assert "`NOT-LANDED` (a pull request open, missing or merged elsewhere, or a head rollup of" in body


def test_every_evidence_kind_has_its_lookup():
    """plugin-validator, 2026-11-02: two of three evidence kinds named no call, so a run invented one."""
    _, body = _parts(SKILL)
    assert "associatedPullRequests" in body
    assert 'object(expression:"<branch>:<path>")' in body


def test_a_truncated_pull_request_list_is_never_judged():
    """skill-reviewer, 2026-11-02: a fixed 50-hit window passed an open pull request at hit 51."""
    _, body = _parts(SKILL)
    assert "gh api graphql --paginate" in body and "$endCursor" in body
    assert "pageInfo{ hasNextPage endCursor }" in body
    assert "Judge no list the query cut short" in body


def test_a_search_hit_must_name_the_card_exactly():
    """skill-reviewer, 2026-11-02: "a whole word" kept `line 75` as a hit for issue 75."""
    _, body = _parts(SKILL)
    assert "with `<n>` not followed by a digit" in body


def test_an_ask_naming_no_evidence_is_searched_for():
    """skill-reviewer, 2026-11-02: the skill marked such an ask open without looking, while fixtures
    02 and 06 expected a search."""
    _, body = _parts(SKILL)
    assert "Look for evidence an ask does not name" in body
    assert "`no evidence found`" in body
    assert "ticked, no evidence named" not in body


def test_the_default_branch_is_never_hardcoded():
    """skill-reviewer, 2026-11-02: a consumer's default branch may not be main."""
    _, body = _parts(SKILL)
    assert "The default branch is `defaultBranchRef.name`" in body


def test_a_commit_is_looked_up_by_expression():
    """Run live 2026-11-02: `object(oid:)` refuses anything but a full 40-character sha, and a
    checklist cites short ones; `object(expression:)` takes either."""
    _, body = _parts(SKILL)
    assert 'object(expression:"<sha>")' in body
    assert "object(oid:" not in body


def test_a_numbered_requirement_list_is_read():
    """Dogfood, `/phil:done 75` on 1.17.0: the card's six steps sat under *What it does*, outside every
    source the skill read."""
    _, body = _parts(SKILL)
    assert "*What it does*, *Scope*, *Requirements* or *Acceptance criteria*" in body


def test_a_card_or_board_edit_is_verified_on_the_card():
    """Dogfood, `/phil:done 75` on 1.17.0: three of eight asks edited the card or the board, and the
    evidence table named only a pull request, a commit or a file."""
    _, body = _parts(SKILL)
    assert "| The card's body |" in body
    assert "| The card's board state |" in body


def test_a_terse_reply_is_quoted_with_what_it_approved():
    """Dogfood, `/phil:done 75` on 1.17.0: `"proceed"` alone reads as nothing."""
    _, body = _parts(SKILL)
    assert '`"proceed" (commit, push, open the pull request)`' in body


def test_the_card_filter_is_given_as_a_pattern_jq_accepts():
    """Dogfood, `/phil:done 75` on 1.17.0: `jq` has no lookahead, so the prose rule was translated by
    hand."""
    _, body = _parts(SKILL)
    assert 'test("(#|issue )<n>([^0-9]|$)"; "i")' in body
    assert "?!" not in body


def test_the_grant_holds_exactly_the_close_writes():
    """D5: comment, Status, close. Each write is a named subcommand, never bare `gh` or `Bash`."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    for grant in ("Bash(gh issue comment:*)", "Bash(gh project item-edit:*)", "Bash(gh issue close:*)",
                  "Bash(gh issue edit:*)", "AskUserQuestion"):
        assert grant in tools, grant
    assert not {t for t in tools if t in ("Bash(gh:*)", "Bash(gh issue:*)")}


def test_the_comment_is_posted_before_done_and_both_read_back():
    """D5, AC3.1: `gh issue close -c` on a closed issue drops the comment silently, and Done closes the
    issue here. The order is the rule."""
    _, body = _parts(SKILL)
    i_comment = body.index("1. **Post the closing comment**")
    i_status = body.index("2. **Write Status=Done**")
    i_close = body.index("3. **Close the issue if it is still open**")
    assert i_comment < i_status < i_close
    assert "never `gh issue close -c`" in body
    assert "Read the card back" in body


def test_one_plan_one_yes():
    """D3: every write is shown and approved once; a stop writes nothing."""
    _, body = _parts(SKILL)
    assert "Ask once" in body
    assert "`stop` writes nothing" in body


def test_an_open_ask_is_answered_before_any_plan():
    """D1: the developer does it, names its evidence, or drops it with a reason the comment keeps."""
    _, body = _parts(SKILL)
    assert "drop it with a reason" in body
    assert "The closing comment quotes every dropped ask with its reason" in body


def test_the_generated_block_is_refreshed_by_its_one_writer():
    """D4: `/phil:done` never edits the block; it asks `phil:nwave-issue-board` to refresh it."""
    _, body = _parts(SKILL)
    assert "<!-- nwave:status:begin -->" in body
    assert "Edit nothing between the markers" in body
    assert "phil:nwave-issue-board" in body


def test_the_finished_state_is_derived_from_the_closed_issue():
    """D4, AC3.3: deleting the snapshot and regenerating rendered `Stack: unknown` on finished work."""
    projection = (REPO / "skills" / "nwave-issue-board" / "references" / "projection.md").read_text()
    flat = " ".join(projection.split())
    assert "**A closed card renders `Finished <YYYY-MM-DD>.` in place of all three.**" in flat
    assert "closedAt" in flat
    skill = " ".join((REPO / "skills" / "nwave-issue-board" / "SKILL.md").read_text().split())
    assert "On a closed card, render `Finished <YYYY-MM-DD>.` in place of its reasoning sections" in skill
    assert "or the card is closed, read `references/projection.md` whole" in skill, \
        "skill-reviewer, 2026-11-02: the load trigger never fired on a closed card with no snapshot"
    assert "the card closing" in skill
    assert "Five rules" in flat and "UTC date" in flat
    assert "deletes the snapshot when it closes" not in flat, "a claim slice 03 has not yet made true"
    fixture = REPO / "skills" / "nwave-issue-board" / "self-test" / "32-closed-card-renders-finished"
    assert "`Finished 2026-11-03.`" in (fixture / "expected.md").read_text()


def test_the_closing_comment_is_a_board_surface_that_composes_prose():
    """CLAUDE.md, *Board surfaces that compose prose*: each names rules/writing.md and ships a fixture."""
    claude = " ".join((REPO / "CLAUDE.md").read_text().split())
    assert "`/phil:done`'s closing comment" in claude
    assert "Nine surfaces do" in claude


def _section(name):
    text = " ".join(SKILL.read_text().split())
    return text.split(f"## {name}", 1)[1].split(" ## ", 1)[0]


def test_the_closing_comment_cites_the_writing_standard():
    """skill-reviewer, 2026-11-02: only REPORT's citation was pinned; PLAN's could go unnoticed, and
    CLAUDE.md requires a board surface's citation to fail a fixture when removed."""
    assert "${CLAUDE_PLUGIN_ROOT}/rules/writing.md" in _section("PLAN")


def test_close_stops_at_the_first_failed_write():
    """skill-reviewer, 2026-11-02: with no stop rule, a failed comment followed by Done closed the card
    with no comment."""
    close = _section("CLOSE")
    assert "stop at the first write that fails" in close
    assert "`CLOSE-FAILED`" in close


def test_the_comment_heredoc_quotes_its_delimiter():
    """skill-reviewer, 2026-11-02: the comment quotes the developer's words, and an unquoted heredoc runs
    their backticks and `$`."""
    assert "--body-file - <<'EOF'" in SKILL.read_text()


def test_the_status_write_targets_the_boards_own_item():
    """skill-reviewer and plugin-validator, 2026-11-02: a card on two boards could take the other's item."""
    assert "take the node whose `project.id` is the board's project id" in _section("CLOSE")


def test_close_reads_the_state_before_closing():
    """skill-reviewer, 2026-11-02: step 3 decided on the state without reading it."""
    assert "only on `OPEN`" in _section("CLOSE")


def test_the_writing_flags_the_grant_allows_are_forbidden():
    """skill-reviewer, 2026-11-02: the grants admit `--edit-last`, `--delete-last` and `--clear`."""
    inv = _section("Invariants")
    for flag in ("--edit-last", "--delete-last", "--clear"):
        assert flag in inv, flag
