"""`commands/start.md` loads `skills/start/SKILL.md`; together they carry start-work's slice 01 and 02
decisions, and slice 03's.

Slice 01 is the start report: it resolves the argument to one open card, applies the refusals, describes
the card and recommends a route. Slice 02 claims the card before the description: In Progress, assigned
to the signed-in account, both read back. Slice 03 moves the session into the card's worktree, or hands
a card already underway to `/phil:resume`. Each test pins one decision from
`docs/feature/start-work/feature-delta.md` as a string the prose must keep. A test cannot prove a run
obeys the sentence; it proves the sentence is still there to obey, and it fails when someone deletes it.
"""
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "start.md"
SKILL = REPO / "skills" / "start" / "SKILL.md"


def _parts(path):
    _, front, body = path.read_text().split("---", 2)
    return yaml.safe_load(front), " ".join(body.split())


def test_the_command_declares_its_grant_and_loads_the_skill():
    """D11: the grant mutates — `gh api graphql` carries mutations, and slices 02 and 03 write."""
    front, body = _parts(COMMAND)
    assert front["mutates"] is True
    assert front.get("argument-hint")
    assert "${CLAUDE_PLUGIN_ROOT}/skills/start/SKILL.md" in body


def test_no_file_write_is_granted():
    """Slice 02 writes to the forge only: a filed card, the board item, the Status, an assignee."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    assert not tools & {"Write", "Edit", "NotebookEdit"}, tools
    assert "Bash" not in tools, "a bare Bash grant can do anything"


def test_the_skill_has_plugin_dev_frontmatter():
    front, _ = _parts(SKILL)
    assert front["name"] == "start"
    assert front["description"].startswith("This skill should be used when")


def test_the_writing_standard_is_named_from_the_plugin_root_and_read():
    """D10, AC2.4: the description and the report are composed prose. A bare path resolves against the
    consumer's repo, so the citation must carry the plugin root."""
    for path in (COMMAND, SKILL):
        _, body = _parts(path)
        bare = [m.start() for m in re.finditer(r"rules/writing\.md", body)
                if not body[:m.start()].endswith("${CLAUDE_PLUGIN_ROOT}/")]
        assert not bare, f"{path.name}: a bare rules/writing.md resolves against the consumer's repo"
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in _parts(SKILL)[1]


def test_every_ask_follows_the_decision_request_standard():
    """The command grants AskUserQuestion, so its skill must reference the shared standard
    (`scripts/check-decision-request-reference.py` enforces the reference; this pins where)."""
    _, body = _parts(SKILL)
    assert "${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md" in body


def test_every_gh_call_names_the_repo():
    """`phil:issue-board`: an inferred remote reads the wrong repo successfully. `gh api graphql` takes
    no `-R`, so the repo reaches it as query variables."""
    for path in (SKILL, COMMAND):
        _, body = _parts(path)
        assert "Pass `-R <owner/repo>` on every `gh issue` call" in body, path.name
        assert "the owner and repo as variables to" in body, path.name
        assert "which takes no `-R`" in body, path.name


def test_it_never_picks_among_matches():
    """D4, AC1.1: several matches are listed and the developer picks."""
    _, body = _parts(SKILL)
    assert "Never pick among matches" in body
    assert "describes and routes nothing until the developer picks" in body


def test_a_number_naming_a_pull_request_is_no_card():
    """`issueOrPullRequest` answers a pull request's number too; a pull request is not a card."""
    _, body = _parts(SKILL)
    assert "issueOrPullRequest" in body
    assert "`PullRequest` is no card" in body


def test_no_match_files_only_on_a_yes_in_the_developers_words():
    """D4, AC1.2, AC3.5."""
    _, body = _parts(SKILL)
    assert "File only on the developer's yes" in body
    assert "titled in the developer's words" in body


def test_a_closed_card_is_refused_and_reopen_is_named():
    """D7, AC1.3."""
    _, body = _parts(SKILL)
    assert "Refuse a closed card" in body
    assert "gh issue reopen" in body


def test_an_open_card_in_done_is_a_defect_and_asks():
    """D7, AC1.3: CLAUDE.md names an open issue in Done as a defect."""
    _, body = _parts(SKILL)
    assert "An open card in `Done` is a defect" in body


def test_someone_elses_card_stays_theirs():
    """D6, AC1.4: name the login and ask; never remove an assignee."""
    _, body = _parts(SKILL)
    assert "name every assignee's login and ask" in body
    assert "Never remove an assignee" in body


def test_the_developer_is_the_signed_in_account():
    """D5: `viewer { login }`, never git's `user.name`."""
    _, body = _parts(SKILL)
    assert "viewer{ login }" in body
    assert "never git's `user.name`" in body


def test_the_description_invents_nothing():
    """D10, AC2.3: a card with no way to tell when it is done says so and names phil:groom-ask."""
    _, body = _parts(SKILL)
    assert "never supply a criterion the card does not hold" in body
    assert "/phil:groom-ask" in body


def test_the_route_rules_apply_in_order():
    """D9, AC2.2: the repo's recorded build path comes first, then the wave label and nWave artifacts,
    then visible versus invisible, then size."""
    body = _route()
    order = ["The repo's recorded build path", "The card's wave", "Who would see the change",
             "Whether it fits one sitting"]
    found = [body.find(rule) for rule in order]
    assert -1 not in found, dict(zip(order, found))
    assert found == sorted(found), "the route rules must appear in D9's order"
    assert "quote the rule and name its file" in body


def test_the_wave_table_is_read_never_restated():
    """`phil:nwave-issue-board` owns the wave to command table."""
    body = _route()
    assert "${CLAUDE_PLUGIN_ROOT}/skills/nwave-issue-board/SKILL.md" in body
    named = set(re.findall(r"/nw-[a-z]+", body))
    assert len(named) <= 1, f"{named}: the table is restated; read it from its owner"
    assert "| `wave:" not in body, "a row of the wave table is restated"


def test_the_route_launches_only_on_a_yes():
    """D9, AC2.1."""
    _, body = _parts(SKILL)
    assert "Launch nothing without the developer's yes" in body


def test_only_the_claim_is_written_before_the_launch():
    """skill-reviewer and plugin-validator, 2026-11-03: an unscoped "Write nothing" contradicted the
    inline route, which edits files once the developer says yes. Slice 02 adds the claim."""
    for path in (SKILL, COMMAND):
        assert "Write only the claim and the worktree before the launch" in _parts(path)[1], path.name
    _, body = _parts(SKILL)
    assert "Send only `query` documents through `gh api graphql`, never `mutation`" in body


def test_every_bash_grant_is_used():
    """plugin-validator, 2026-11-03: `Bash(gh issue view:*)` was copied from `/phil:done` and never
    called."""
    front, _ = _parts(COMMAND)
    body = " ".join([_parts(SKILL)[1], _claim(), _worktree(), _route(), _gitlab()])
    for grant in re.findall(r"Bash\(([^:)]+):\*\)", front["allowed-tools"]):
        assert grant in body, f"granted and never used: {grant}"


def test_a_missing_number_is_no_match():
    """plugin-validator, run live 2026-11-03: a number naming nothing makes gh exit 1 with NOT_FOUND,
    never a null answer."""
    _, body = _parts(SKILL)
    assert "`NOT_FOUND` error: `NO-MATCH`" in body


def test_the_search_keeps_its_scope():
    """skill-reviewer, 2026-11-03: an argument such as `is:closed` or a stray `'` changed or broke the
    search."""
    _, body = _parts(SKILL)
    assert "Strip the qualifiers that would change the search's scope" in body
    assert "escape each `'`" in body


def test_every_early_stop_has_an_outcome():
    """plugin-validator and skill-reviewer, 2026-11-03: no forge line, GitLab and a failed read matched
    none of the terminal outcomes."""
    _, body = _parts(SKILL)
    assert "`CANNOT-RUN`** — the run could not begin" in body


def test_inline_needs_a_stated_done_when():
    """skill-reviewer, 2026-11-03: rule 4 keyed on the run's own one-sentence ASKS, so nearly every card
    went inline and fixture 06 contradicted the rules."""
    body = _route()
    assert "DONE WHEN holds exactly one item the card states" in body
    assert "A `NO-DONE-WHEN` card never goes inline" in body


def test_a_build_path_names_a_command_and_skips_a_step_already_run():
    """skill-reviewer, 2026-11-03: "test first" read as a build path, and card 80 was sent back to
    nw-discuss after DISCUSS had run."""
    body = _route()
    assert "A principle that names no command, such as \"test first\", is no build path" in body
    assert "name the rule's next step instead" in body


def test_no_skill_runs_before_the_yes():
    """skill-reviewer and plugin-validator, 2026-11-03: rule 2's fallback invoked nwave-slice-status
    before the yes, which runs git verbs this command does not grant and returns no wave."""
    body = _route()
    assert "nwave-slice-status" not in body
    assert "A label the table has no row for goes on to rule 3" in body


def test_outcomes_print_before_the_launch():
    """skill-reviewer, 2026-11-03: a launched route runs on past the skill, so outcomes reported "when
    the run ends" never printed."""
    body = _route()
    assert "Print the outcome tokens, then launch" in body


def test_other_launches_only_a_named_route():
    """skill-reviewer, 2026-11-03: any text under Other launched something."""
    body = _route()
    assert "Other naming no route is unanswered" in body


def test_done_when_items_are_counted_never_merged():
    """skill-reviewer, 2026-11-03: `/phil:done` checks these items later, so a merged one goes missing."""
    _, body = _parts(SKILL)
    assert "Merge none and drop none" in body


CLAIM_REF = REPO / "skills" / "start" / "references" / "claim.md"


def _section(name):
    text = " ".join(SKILL.read_text().split())
    return text.split(f"## {name}", 1)[1].split(" ## ", 1)[0]


def _claim():
    """The CLAIM step's procedure lives in its reference, as `/phil:done`'s CLEAR does."""
    return " ".join(CLAIM_REF.read_text().split())


def test_the_grant_holds_exactly_the_claim_writes():
    """D8, AC3.5: each write is a named subcommand, never bare `gh`."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    for grant in ("Bash(gh project item-add:*)", "Bash(gh project item-edit:*)", "Bash(gh issue edit:*)",
                  "Bash(gh issue create:*)"):
        assert grant in tools, grant
    for broad in ("Bash(gh:*)", "Bash(gh issue:*)", "Bash(gh project:*)"):
        assert broad not in tools, broad


def test_the_claim_runs_in_issue_boards_order():
    """D8, AC3.1: add the item before writing its Status, assign, then read both back."""
    claim = _claim()
    steps = ["gh project item-add", "gh project item-edit", "--add-assignee", "Read the claim back"]
    found = [claim.find(s) for s in steps]
    assert -1 not in found, dict(zip(steps, found))
    assert found == sorted(found), "the claim must run in phil:issue-board's order"


def test_item_add_is_read_back_never_trusted():
    """`phil:issue-board`: `gh project item-add` exits 0 whether or not the item landed."""
    assert "The exit code is not evidence that the item landed" in _claim()


def test_a_read_back_mismatch_is_reported_never_repaired():
    """AC3.2."""
    claim = _claim()
    assert "re-read once" in claim
    assert "`READ-BACK-MISMATCH`" in claim and "repair nothing" in claim


def test_no_board_block_writes_no_status():
    """D8, AC3.4."""
    claim = _claim()
    assert "With no board block, or a block missing any constant" in claim
    assert "name `/phil:board-setup` and write no Status" in claim


def test_an_unassignable_account_is_reported_and_nothing_assigned():
    """D5, AC3.3. Run live 2026-11-03: an unknown login exits 1 with `Could not resolve to a user or
    bot`."""
    claim = _claim()
    assert "`NOT-ASSIGNED`" in claim and "assign no one else" in claim


def test_no_signed_in_account_cannot_run():
    """D5, AC3.3: every read needs the signed-in account, so its absence stops the run."""
    _, body = _parts(SKILL)
    assert "With no signed-in account, name `gh auth login`: `CANNOT-RUN`" in body


def test_a_failed_write_stops_the_claim():
    """D8: nothing past a failed write runs, and a missing `project` scope is named."""
    claim = _claim()
    assert "Stop the claim at the first board write that fails" in claim
    assert "gh auth refresh -s project" in claim


def test_go_on_past_someone_else_adds_beside_them():
    """D6, AC1.4."""
    assert "adds the developer beside them" in _section("CHECK")


def test_the_grant_flags_that_write_too_much_are_forbidden():
    """The grants admit `--remove-assignee`, `--clear` and every other `gh issue edit` flag."""
    inv = _section("Invariants")
    assert "Use `gh issue edit` only with `--add-assignee`" in inv
    for flag in ("--remove-assignee", "--clear"):
        assert flag in inv, flag


def test_a_filed_card_is_added_in_the_same_breath():
    """`phil:issue-board`: a card created and never added is invisible on a board grouped by Status."""
    claim = _claim()
    assert -1 < claim.find("gh issue create") < claim.find("step 1 adds it in the same breath")


def test_the_board_gets_no_composed_prose():
    """CLAUDE.md, Board surfaces that compose prose: a surface that composes none says so."""
    _, body = _parts(SKILL)
    assert "composes no prose on the board" in body


def test_the_skill_reads_its_claim_reference_whole():
    _, body = _parts(SKILL)
    assert "Read `${CLAUDE_PLUGIN_ROOT}/skills/start/references/claim.md` whole before the first claim write" in body


def test_the_read_back_checks_only_writes_that_ran():
    """skill-reviewer, 2026-11-03: demanding In Progress and the developer on every run contradicted
    fixtures 22, 23 and 25."""
    claim = _claim()
    assert "only where a board block exists and the Status write did not fail" in claim
    assert "only where the assign did not fail" in claim


def test_the_read_back_checks_every_earlier_assignee():
    """skill-reviewer, 2026-11-03: a run that replaced colleague still read back CLAIMED, so "never
    remove an assignee" had no evidence behind it."""
    assert "Every login RESOLVE read among the assignees" in _claim()


def test_an_assign_that_fails_or_does_not_hold_is_not_assigned():
    """plugin-validator and skill-reviewer, 2026-11-03: a failed assign fell to CLAIM-FAILED and
    skipped the read-back; the forge can also drop an assignee with exit 0."""
    claim = _claim()
    assert "An assign that fails, for any reason, is `NOT-ASSIGNED`, never `CLAIM-FAILED`" in claim
    assert "An assign that exits 0 but reads back without `viewer.login` is `NOT-ASSIGNED` too" in claim


def test_an_item_that_never_lands_fails_the_claim():
    """plugin-validator, 2026-11-03: no rule covered a re-read with no board node."""
    claim = _claim()
    assert "still none is `CLAIM-FAILED`" in claim
    assert "and neither is its output" in claim


def test_no_failure_after_filing_reads_as_cannot_run():
    """skill-reviewer, 2026-11-03: a failure after `gh issue create` reported CANNOT-RUN, and so
    WROTE-NOTHING, beside a card it had filed."""
    assert "Once a card is filed, no failure is `CANNOT-RUN`" in _claim()


def test_a_failed_read_mid_claim_is_never_claimed():
    """skill-reviewer, 2026-11-03."""
    assert "A read that fails after the claim's first write leaves the claim unverified" in _claim()


def test_a_failed_write_is_read_back_before_it_is_reported():
    """skill-reviewer, 2026-11-03, after `phil:issue-board`: a write that timed out may have landed."""
    assert "read the card back once and report what it shows" in _claim()


def test_other_at_filing_is_a_proposed_title_not_a_yes():
    """skill-reviewer, 2026-11-03."""
    assert "Words typed under Other are a proposed title, not a yes" in _claim()


def test_filing_uses_only_the_developers_title():
    """skill-reviewer, 2026-11-03: a template or a body file puts words on the card that are not the
    developer's."""
    assert "Use `gh issue create` only with `-R`, `--title` and `--body ''`" in _claim()
    assert "Use `gh issue create` only with `-R`, `--title` and `--body ''`" in _section("Invariants")


def test_no_status_option_is_chosen_by_name():
    """skill-reviewer, 2026-11-03: a block missing the In Progress id left a run matching by name."""
    assert "On GitHub, never choose a Status option by its name" in _claim()


def test_wrote_nothing_counts_write_calls():
    """plugin-validator and skill-reviewer, 2026-11-03: fixture 25 wrote nothing but made a write call."""
    _, body = _parts(SKILL)
    assert "A failed write is still a write call" in body


WORKTREE_REF = REPO / "skills" / "start" / "references" / "worktree.md"
ROUTE_REF = REPO / "skills" / "start" / "references" / "route.md"


def _route():
    """ROUTE's rules live in their reference; the skill keeps the outline. Read both, so a rule that
    drifts back into the skill still counts."""
    return _parts(SKILL)[1] + " " + " ".join(ROUTE_REF.read_text().split())


def test_the_skill_reads_its_route_reference_whole():
    _, body = _parts(SKILL)
    assert "Read `${CLAUDE_PLUGIN_ROOT}/skills/start/references/route.md` whole before naming a route" in body


def _worktree():
    return " ".join(WORKTREE_REF.read_text().split())


def test_the_grant_holds_the_worktree_tools_and_only_a_fetch_of_git_writes():
    """D1: Claude Code's worktree tool cuts the worktree; git lists them and fetches the default branch.
    Probed 2026-11-03: the tool runs with no grant in the default mode, so the grant declares it."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    for grant in ("EnterWorktree", "ExitWorktree", "Bash(git worktree list:*)", "Bash(git fetch:*)"):
        assert grant in tools, grant
    for broad in ("Bash(git worktree:*)", "Bash(git worktree add:*)", "Bash(git worktree remove:*)",
                  "Bash(git:*)", "Bash(git push:*)", "Bash(git branch:*)"):
        assert broad not in tools, broad


def test_the_skill_reads_its_worktree_reference_whole():
    _, body = _parts(SKILL)
    assert "${CLAUDE_PLUGIN_ROOT}/skills/start/references/worktree.md` whole" in body


def test_a_card_never_gets_a_second_worktree():
    """D2, D3, AC4.2."""
    wt = _worktree()
    assert "Never cut a second worktree for a card that has one" in wt
    assert "a name starting `issue-<n>-`" in wt
    assert "the head branch of the developer's open pull request naming the card" in wt


def test_several_candidate_worktrees_are_the_developers_pick():
    """D3."""
    assert "list each with its branch and its lock, and ask which to enter" in _worktree()


def test_a_card_underway_goes_to_resume_and_no_other_route():
    """D2, AC4.3."""
    wt = _worktree()
    assert "`UNDERWAY`" in wt and "name `/phil:resume` as the next step" in wt
    assert "recommend no other route" in wt


def test_a_session_in_another_worktree_moves_only_on_a_yes():
    """AC4.4."""
    assert "move the session only on the developer's yes" in _section("CHECK")


def test_a_worktree_is_never_removed():
    """Out of scope: removing a worktree is `/phil:done`'s call, which since 1.25.0 removes one its own
    session made once it reads clean at the merged tip."""
    wt = _worktree()
    assert "`ExitWorktree` only with `keep`" in wt
    assert "ExitWorktree` only with `keep`" in _section("Invariants")


def test_the_run_fetches_because_the_tool_may_not():
    """plugin-validator, 2026-11-03, read from Claude Code 2.1.317's source: the tool fetches only when
    the last fetch is a day old (`P$r=86400000`). The first probe ran on a clone that had never fetched,
    so it always fetched there; a repo fetched today branched from a stale ref."""
    wt = _worktree()
    assert "`git fetch origin <default>`" in wt
    assert "The tool fetches only when the last fetch is a day old" in wt
    assert "The tool fetches before it branches" not in wt


def test_the_base_is_checked_against_the_remotes_head():
    """plugin-validator and skill-reviewer, 2026-11-03: comparing against the same stale local ref could
    never see a stale base, and inferring `worktree.baseRef: head` blamed the wrong cause."""
    wt = _worktree()
    assert "Name the path, the branch and the base commit" in wt
    assert "defaultBranchRef{ name target{ oid } }" in wt
    assert "read `worktree.baseRef` from" in wt


def test_a_worktree_another_session_holds_asks_first():
    """Seen 2026-11-03: a worktree in use carries `locked claude session <name> (pid …)`."""
    assert "`claude session <name> (pid <pid> …)` may be another live session" in _worktree()


def test_a_refused_worktree_is_reported_never_worked_around():
    wt = _worktree()
    assert "`WORKTREE-FAILED`" in wt and "quote the refusal" in wt


def test_a_session_already_in_the_cards_worktree_moves_nowhere():
    """skill-reviewer and plugin-validator, 2026-11-03: the second run, the brief's dogfood moment, asked
    about its own session's lock and reported a move that never happened."""
    assert "Call no tool and skip the lock ask, because the lock is this session's" in _worktree()


def test_a_refused_enter_still_ends_underway():
    """skill-reviewer and plugin-validator, 2026-11-03: a refusal sent an underway card to ROUTE."""
    assert "A card underway still ends `UNDERWAY`" in _worktree()


def test_any_locked_worktree_asks_first():
    """skill-reviewer, 2026-11-03: only a `claude session` lock asked, and the rule sat after the bullet
    that enters."""
    wt = _worktree()
    i = wt.find("Ask before entering any candidate whose entry has a `locked` line")
    assert -1 < i < wt.find("**One worktree**")


def test_a_surviving_branch_or_prunable_entry_is_handled():
    """skill-reviewer, 2026-11-03: a leftover `worktree-issue-<n>-*` branch collided with the cut, and a
    `prunable` entry counted as the card's."""
    wt = _worktree()
    assert "git rev-parse --symbolic --branches='worktree-issue-<n>-*'" in wt
    assert "An entry marked `prunable` has lost its folder: it is not the card's" in wt


def test_the_pull_request_search_reads_every_page():
    """skill-reviewer, 2026-11-03: the first 20 hits could hide the card's pull request."""
    assert "gh api graphql --paginate" in _worktree()


def test_leaving_a_worktree_is_checked_before_a_cut():
    """plugin-validator and skill-reviewer, 2026-11-03: ExitWorktree does nothing outside a session the
    tool entered itself."""
    assert "where it is not the main checkout, cut nothing and report `WORKTREE-FAILED`" in _worktree()


def test_check_reads_the_worktree_reference_before_step_4():
    """plugin-validator and skill-reviewer, 2026-11-03: step 4 used "the card's worktrees" before the
    reference that defines them was read."""
    check = _section("CHECK")
    assert "Read `${CLAUDE_PLUGIN_ROOT}/skills/start/references/worktree.md` whole first" in check


def test_a_failed_claim_goes_on_to_the_worktree():
    """skill-reviewer, 2026-11-03: claim.md sent a failed claim straight to DESCRIBE, skipping WORKTREE,
    so a route could launch in the main checkout."""
    claim = _claim()
    assert "Then go on to WORKTREE" in claim
    assert "Then go on to DESCRIBE" not in claim


def test_an_empty_slug_still_names_the_worktree():
    """plugin-validator, 2026-11-03."""
    assert "An empty slug names the worktree `issue-<n>`" in _worktree()


# --- Slice 04: GitLab --------------------------------------------------------------------------------
#
# Issue 98: on a GitLab forge line the run stopped with `CANNOT-RUN`, and CLAUDE.md asks every surface
# that drives issues, boards, branches or worktrees to support both forges. Decisions D12-D21 in
# `docs/feature/start-work/feature-delta.md`; the pattern is `skills/done/references/gitlab.md`.

GITLAB_REF = REPO / "skills" / "start" / "references" / "gitlab.md"


def _gitlab():
    return " ".join(GITLAB_REF.read_text().split())


def test_gitlab_is_supported_not_refused():
    """AC5.8: no run ends `CANNOT-RUN` because the forge is GitLab."""
    front, body = _parts(SKILL)
    assert "covers GitHub only" not in body
    assert "a GitLab forge" not in _section("Decision outcomes")
    assert "GitLab" in front["description"]
    assert "GitLab" in _parts(COMMAND)[0]["description"]
    assert ("Read `${CLAUDE_PLUGIN_ROOT}/skills/start/references/gitlab.md` whole before RESOLVE"
            in body)


def test_the_gitlab_grant_names_each_subcommand():
    """D20: each GitLab write is a named subcommand, never bare `glab`."""
    front, _ = _parts(COMMAND)
    tools = {t.strip() for t in front["allowed-tools"].split(",")}
    for grant in ("Bash(glab api:*)", "Bash(jq:*)", "Bash(glab issue create:*)",
                  "Bash(glab issue update:*)"):
        assert grant in tools, grant
    assert not tools & {"Bash(glab:*)", "Bash(glab issue:*)"}


def test_every_glab_call_names_the_project_and_host():
    """D16, AC5.9: glab 1.112.0 sends a bare `-R <group/project>` to gitlab.com outside a checkout of the
    host, and fills `:id` and `:fullpath` from the working directory's remote."""
    gl = _gitlab()
    assert ("Pass `-R https://<host>/<group/project>` on every `glab issue` call and `--hostname <host>` on "
            "every `glab api` call") in gl
    assert "never `:id` or `:fullpath`" in gl
    assert "-R <group/project>" not in gl.replace("a bare `-R <group/project>`", "")
    assert "pass `-R https://<host>/<group/project>` on every `glab issue` call" in _parts(COMMAND)[1]


def test_a_glab_read_never_sends_a_field():
    """D16, AC5.9: `glab api` sends a POST once a field is added, so a read that passes one writes."""
    gl = _gitlab()
    assert "Never pass `-f`, `-F`, `--field`, `--raw-field`, `--input`, `--form`, `-X` or `--method`" in gl
    assert "Send `glab api` only GETs" in _parts(COMMAND)[1]
    assert "On GitLab, send `glab api` only GETs" in _section("Invariants")


def test_the_gitlab_assign_adds_and_never_replaces():
    """D14, AC5.2: `glab issue update --help`, 1.112.0: a login without a prefix replaces every
    assignee, and exits 0."""
    gl = _gitlab()
    assert "--assignee +<login>" in gl
    assert not re.search(r"--assignee [<'\"]?[a-z<]", gl.replace("--assignee +<login>", "")), \
        "a bare --assignee replaces every assignee"
    assert "--assignee +<login>" in _section("Invariants")
    assert "--assignee +<login>" in _parts(COMMAND)[1]


def test_the_gitlab_claim_is_one_label_swap():
    """D13, AC5.9: a GitLab column is a label; a board list moves nothing and adds a column."""
    gl = _gitlab()
    assert "--label '<in-progress>' --unlabel '<others>'" in gl
    assert "Never create a board list" in gl
    assert "runs no `item-add`" in gl


def test_the_in_progress_label_is_matched_by_name_and_asked_when_unclear():
    """D12, AC5.3: the developer's answer. Nothing records which label is which column."""
    gl = _gitlab()
    assert "`in-progress`, `in progress` or `doing`" in gl
    assert "Where none or several labels match In Progress, ask which label to use" in gl
    assert "write no status label until the developer answers" in gl


def test_gitlab_done_is_the_closed_list():
    """D15, AC5.4: modive's block says to close a finished issue rather than label it."""
    gl = _gitlab()
    assert "glab issue reopen <n> -R <repo>" in gl
    assert "A family with no done label never fires that check" in gl


def test_gitlab_filing_passes_only_the_title_and_an_empty_description():
    """D19, AC5.7. Settled 2026-11-05 with glab 1.112.0 outside a terminal: `--description ''` gets past
    the non-interactive check and opens no editor; without it glab refuses."""
    gl = _gitlab()
    assert "glab issue create -R <repo> --title '<the words>' --description '' --yes" in gl
    assert "Use `glab issue create` only with `-R`, `--title`, `--description ''` and `--yes`" in gl


def test_the_gitlab_search_reads_one_page_of_21():
    """Settled 2026-11-05: a paginated `glab api` prints one array per page, so `length` counts each page
    alone. RESOLVE needs only whether more than 20 matched."""
    gl = _gitlab()
    assert "per_page=21" in gl
    assert "the one list read without `--paginate`" in gl


def test_gitlab_underway_reads_the_developers_merge_requests():
    """D18, AC5.5."""
    gl = _gitlab()
    assert "merge_requests?state=opened&author_username=<login>" in gl
    assert 'test("(#|issue )<n>([^0-9]|$)"; "i")' in gl
    assert "repository/branches/<default>" in gl
    assert "`!<n>`" in gl


def test_gitlab_no_signed_in_account_names_the_login():
    """D16."""
    assert "glab auth login --hostname <host>" in _gitlab()


def test_the_gitlab_reference_adds_no_outcome_token():
    """D20, and the slice's learning hypothesis: the reference confirms "call for call" only if it adds no
    outcome."""
    from test_start_fixtures import REPORT_LINES, TERMINAL
    named = set(re.findall(r"`([A-Z][A-Z-]{3,})`", GITLAB_REF.read_text()))
    assert named <= TERMINAL | REPORT_LINES, named - (TERMINAL | REPORT_LINES)


# skill-reviewer and plugin-validator, 2026-11-05, over slice 04's first draft.

def test_gitlab_governs_where_it_differs():
    """Both reviewers: the reference said every GitHub rule stands, and four contradicted it."""
    assert "Where this file and those differ, this file governs on GitLab" in _gitlab()
    assert "On GitHub, never choose a Status option by its name" in _claim()
    inv = _section("Invariants")
    assert "No label but GitLab's status labels" in inv


def test_the_in_progress_label_must_exist_before_the_swap():
    """Both reviewers: `--label` with an unknown name creates the label, exits 0, and reads back as set.
    Read live 2026-11-05: a missing label answers `404 Label Not Found`."""
    gl = _gitlab()
    assert "projects/<p>/labels/<encoded label>" in gl
    assert "`404 Label Not Found`" in gl
    assert "Accept only an answer the family lists" in gl


def test_gitlab_free_holds_one_assignee():
    """Both reviewers: GitLab Free keeps one assignee per issue, so "beside them" cannot hold there."""
    gl = _gitlab()
    assert "GitLab Free holds one assignee per issue" in gl
    assert "a block that names no tier counts as Free" in gl


def test_a_project_404_is_not_a_missing_card():
    """Both reviewers, read live 2026-11-05: a mistyped or hidden project answers `404 Project Not Found`."""
    gl = _gitlab()
    assert "`404 Project Not Found`" in gl
    i_project, i_card = gl.find("Read `projects/<p>` first"), gl.find("projects/<p>/issues/<n>")
    assert -1 < i_project < i_card


def test_the_merge_request_read_filters_in_jq_alone():
    """skill-reviewer: GitLab's search may drop short words; the author and state already narrow it."""
    gl = _gitlab()
    assert "merge_requests?state=opened&author_username=<login>&per_page=100" in gl
    assert "&search=<n>" not in gl


def test_a_scoped_wave_label_routes():
    """skill-reviewer: `phil:nwave-issue-board` writes `wave::<name>` where scoped labels exist."""
    gl = _gitlab()
    assert "Read `wave::<name>` as `wave: <name>`" in gl
    assert "A `wave::` label is never a status label" in gl


def test_more_than_20_matches_says_so_without_a_count():
    """skill-reviewer: one page of 21 holds no total."""
    assert "say more than 20 matched" in _gitlab()
