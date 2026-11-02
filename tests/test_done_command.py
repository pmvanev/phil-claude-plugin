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


CLEAR = REPO / "skills" / "done" / "references" / "clear.md"


def _clear():
    return " ".join(CLEAR.read_text().split())


def test_clear_is_read_before_the_plan():
    """Slice 03 keeps the skill body under plugin-dev's 3,000-word flag by moving CLEAR to a reference."""
    assert "Read `${CLAUDE_PLUGIN_ROOT}/skills/done/references/clear.md` whole before composing the plan" \
        in _parts(SKILL)[1], "skill-reviewer, 2026-11-02: a bare reference path resolves against the user's repo"


def test_the_cleanup_grants_are_narrow():
    """D9: every delete is a named subcommand. No `rm`, no `git branch` with its `-D`, no `git -C`."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    for grant in ("Bash(git worktree list:*)", "Bash(git branch -d:*)", "Bash(git branch -D:*)",
                  "Bash(git merge-base:*)", "Bash(git push --delete:*)",
                  "Bash(python3:*)", "Bash(git remote get-url:*)"):
        assert grant in tools, grant
    for broad in ("Bash(rm:*)", "Bash(git branch:*)", "Bash(git -C:*)", "Bash(git push:*)", "Bash(git:*)",
                  "Bash(git worktree remove:*)"):
        assert broad not in tools, broad


def test_nothing_is_forced_but_a_branch_the_developer_chose():
    """D9, amended 2026-11-02 by the developer: `-D` only for an unmerged branch the developer chose to
    force-delete at its own question; `--force` and `-f` never."""
    clear = _clear()
    assert "Never pass `--force` or `-f`" in clear, \
        "plugin-validator, 2026-11-02: `git branch -d -f` deleted a branch git had just refused"
    assert "Never pass `--force` or `-f`" in _parts(COMMAND)[1]
    assert "Pass `-D` only for a branch the developer chose to force-delete at its own question" in clear
    assert "Pass `-D` only for a branch the developer chose to force-delete at its own question" \
        in _parts(COMMAND)[1]
    assert "report the refusal and leave the item" in clear


def test_worktrees_are_listed_and_never_removed():
    """The developer's answer, 2026-11-02, after an adversarial run showed a clean-looking worktree can
    hold a nested repository, hidden edits, submodules or commits only its own history remembers."""
    clear = _clear()
    assert "Never remove a worktree" in clear
    assert "session-exchanges.py retire" in clear and "session-exchanges.py head" in clear
    assert clear.index("1. **Snapshots**") < clear.index("2. **Local branches**") \
        < clear.index("3. **Remote branches**")
    assert "the developer runs them" in clear


def test_branches_come_from_the_cards_pull_requests():
    """D8: a branch matching the card only by name is never a candidate."""
    assert "headRefName" in _parts(SKILL)[1]
    assert "never a branch matched by name" in _clear()


def test_held_items_survive_and_are_never_offered_for_deletion():
    """Slice 03 settled D3 against D9: deleting an unmerged branch needs a force, so it is listed as
    surviving, with the reason, and never offered."""
    clear = _clear()
    assert "listed as surviving, with the reason" in clear
    assert "A branch any worktree has checked out, locally and on the remote" in clear


def test_the_plan_lets_the_developer_keep_the_local_snapshot():
    """The snapshot where `/phil:done` runs may belong to other work, and one yes is all or nothing."""
    clear = _clear()
    assert "**yes, and retire the snapshot here too**" in clear, \
        "skill-reviewer, 2026-11-02: the snapshot here records no branch, so keeping it is the default"
    assert "A plain yes keeps it" in clear


def test_the_cleanup_outcomes_are_defined():
    _, body = _parts(SKILL)
    section = body.split("## Decision outcomes", 1)[1]
    assert "`CLEARED`" in section and "`LEFT`" in section


def test_every_delete_needs_the_merged_tip():
    """plugin-validator and skill-reviewer, 2026-11-02: `git push --delete` has no merge check, and
    `git branch -d` passes a branch merged only into its own remote. The skill's tip check is the guard."""
    clear = _clear()
    assert "only when its tip is the `headRefOid` of a pull request merged into `<default>`" in clear
    assert "target{ oid }" in clear
    assert "The lease refuses the delete if the tip moved after the check" in clear


def test_shared_and_foreign_branches_are_held():
    """skill-reviewer and plugin-validator, 2026-11-02: a release branch, a fork's head, a protected
    branch or one an open pull request uses became a candidate."""
    assert _parts(SKILL)[1].count("isCrossRepository") == 2, "both FIND queries must read it"
    clear = _clear()
    for phrase in ("`<default>` itself", "a pull request from a fork", "branchProtectionRule",
                   "the head or the base of an open pull request"):
        assert phrase in clear, phrase


def test_a_held_branch_holds_its_worktree_and_snapshot():
    """Both reviewers, 2026-11-02: a worktree on a held branch, and the snapshot in it, were deleted."""
    assert "A worktree whose branch is held, and the snapshot inside it" in _clear()


def test_a_dirty_worktree_is_held_before_the_plan():
    """skill-reviewer, 2026-11-02: the snapshot was retired before git refused the worktree."""
    clear = _clear()
    assert "scripts/worktree-state.py" in clear
    assert "In a worktree that reads `DIRTY` or `UNREADABLE`, keep the snapshot" in clear


def test_the_remote_is_the_forges():
    """skill-reviewer, 2026-11-02: the remote came from local config and was never checked."""
    clear = _clear()
    assert "git remote get-url --push --all <remote>" in clear, \
        "adversarial run, 2026-11-02: a pushurl or pushInsteadOf sent the delete to a fork"
    assert "--force-with-lease=refs/heads/<branch>:<headRefOid> <remote> refs/heads/<branch>" in clear, \
        "adversarial run, 2026-11-02: a commit pushed between the re-read and the delete was lost"
    assert "git push --delete <remote> <branch>" not in clear, "an unqualified refspec can match a tag"


def test_only_the_developers_own_pull_requests_give_candidates():
    """adversarial run, 2026-11-02: a colleague's merged pull request that mentioned the card made their
    branch a candidate."""
    assert _parts(SKILL)[1].count("author{ login }") == 2
    assert "viewer{ login }" in _parts(SKILL)[1]
    assert "a pull request someone else opened" in _clear()


def test_the_card_is_read_back_before_anything_is_cleared():
    close = _section("CLOSE")
    assert close.index("**Read the card back**") < close.index("**Clear what the work left behind**")


def test_left_covers_every_way_an_item_survives():
    _, body = _parts(SKILL)
    assert "held, kept at the developer's answer, or refused" in body
    assert "Any refusal or error in CLEAR leaves that item and goes on" in _clear()


def test_the_plan_stop_rule_spares_both_yeses():
    """Both reviewers, 2026-11-02: "any answer but yes" made the third answer a stop."""
    assert "Any answer but the two yeses, Other included, is a stop" in _section("PLAN")


def test_python3_runs_only_the_two_scripts_and_their_read_or_retire():
    _, body = _parts(COMMAND)
    assert "Run `python3` only on `${CLAUDE_PLUGIN_ROOT}/scripts/session-exchanges.py` with `head` or" \
        " `retire`, and on `${CLAUDE_PLUGIN_ROOT}/scripts/worktree-state.py`" in body


def test_an_unmerged_branch_is_offered_for_force_delete_one_at_a_time():
    """The developer's answer, 2026-11-02, closing issue 75's last requirement: an unmerged branch
    survives unless the developer says otherwise, and says so for that branch alone."""
    clear = _clear()
    assert "## FORCE — an unmerged branch, one at a time" in clear
    assert "**keep** — the default" in clear
    assert "showing every commit the delete would lose" in clear
    assert "git log --format='%h %an <%ae> %s' <remote>/<default>..refs/heads/<branch>" in clear
    assert "compare(headRef:" in clear
    assert "--force-with-lease=refs/heads/<branch>:<shown tip>" in clear


def test_force_is_never_offered_for_what_is_not_the_developers_to_lose():
    """A colleague's branch, a fork's, a protected one, or one an open pull request or a worktree uses is
    held whatever the developer answers; only the developer's own unmerged branch is offered."""
    clear = _clear()
    assert "Offer it only for the developer's own branch" in clear
    assert "Never offer to remove a worktree" in clear


def test_a_dirty_worktree_is_listed_with_its_changes():
    """The developer's answer, 2026-11-02: worktrees stay listed, never removed, with any uncommitted
    changes shown beside them."""
    assert "show the changes `worktree-state.py` printed under it" in _clear()


def test_force_is_offered_only_for_a_branch_that_is_still_the_developers():
    """Adversarial run, 2026-11-02: a colleague's branch reusing the name of the developer's closed pull
    request was offered, its commits shown with no author, and the leased delete went through."""
    clear = _clear()
    assert "descends from the pull request's `headRefOid`" in clear
    assert "git merge-base --is-ancestor <headRefOid> refs/heads/<branch>" in clear
    assert "every commit it would lose was authored by `viewer.login`" in clear
    assert "author{ name user{ login } }" in clear


def test_the_local_force_delete_rechecks_its_tip():
    """Adversarial run, 2026-11-02: `git branch -D` has no lease, and a commit made after the question
    was deleted unseen."""
    assert "Read the local tip again just before `-D`" in _clear()


def test_a_list_too_long_to_show_is_never_offered():
    """Adversarial run, 2026-11-02: compare lists the oldest commits first, so past 50 the tip went
    unshown."""
    assert "Where `aheadBy` exceeds 50, do not offer it" in _clear()


def test_the_shown_tip_comes_from_the_same_read_as_the_list():
    assert "headTarget{ oid }" in _clear()


def test_the_remote_copy_goes_only_after_the_local_one():
    """Adversarial run, 2026-11-02: a worktree mid-rebase hides its branch from `git worktree list`, git
    refused the local `-D`, and the remote delete still ran."""
    assert "Force-delete the remote copy only after the local delete succeeded" in _clear()
