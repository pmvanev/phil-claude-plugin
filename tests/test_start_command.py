"""`commands/start.md` loads `skills/start/SKILL.md`; together they carry start-work's slice 01 and 02
decisions.

Slice 01 is the start report: it resolves the argument to one open card, applies the refusals, describes
the card and recommends a route. Slice 02 claims the card before the description: In Progress, assigned
to the signed-in account, both read back. Each test pins one decision from
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
    _, body = _parts(SKILL)
    order = ["The repo's recorded build path", "The card's wave", "Who would see the change",
             "Whether it fits one sitting"]
    found = [body.find(rule) for rule in order]
    assert -1 not in found, dict(zip(order, found))
    assert found == sorted(found), "the route rules must appear in D9's order"
    assert "quote the rule and name its file" in body


def test_the_wave_table_is_read_never_restated():
    """`phil:nwave-issue-board` owns the wave to command table."""
    _, body = _parts(SKILL)
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
        assert "Write only the claim before the launch" in _parts(path)[1], path.name
    _, body = _parts(SKILL)
    assert "Send only `query` documents through `gh api graphql`, never `mutation`" in body


def test_every_bash_grant_is_used():
    """plugin-validator, 2026-11-03: `Bash(gh issue view:*)` was copied from `/phil:done` and never
    called."""
    front, _ = _parts(COMMAND)
    body = _parts(SKILL)[1] + " " + _claim()
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
    _, body = _parts(SKILL)
    assert "DONE WHEN holds exactly one item the card states" in body
    assert "A `NO-DONE-WHEN` card never goes inline" in body


def test_a_build_path_names_a_command_and_skips_a_step_already_run():
    """skill-reviewer, 2026-11-03: "test first" read as a build path, and card 80 was sent back to
    nw-discuss after DISCUSS had run."""
    _, body = _parts(SKILL)
    assert "A principle that names no command, such as \"test first\", is no build path" in body
    assert "name the rule's next step instead" in body


def test_no_skill_runs_before_the_yes():
    """skill-reviewer and plugin-validator, 2026-11-03: rule 2's fallback invoked nwave-slice-status
    before the yes, which runs git verbs this command does not grant and returns no wave."""
    _, body = _parts(SKILL)
    assert "nwave-slice-status" not in body
    assert "A label the table has no row for goes on to rule 3" in body


def test_outcomes_print_before_the_launch():
    """skill-reviewer, 2026-11-03: a launched route runs on past the skill, so outcomes reported "when
    the run ends" never printed."""
    _, body = _parts(SKILL)
    assert "Print the outcome tokens, then launch" in body


def test_other_launches_only_a_named_route():
    """skill-reviewer, 2026-11-03: any text under Other launched something."""
    _, body = _parts(SKILL)
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
    assert "Never choose a Status option by its name" in _claim()


def test_wrote_nothing_counts_write_calls():
    """plugin-validator and skill-reviewer, 2026-11-03: fixture 25 wrote nothing but made a write call."""
    _, body = _parts(SKILL)
    assert "A failed write is still a write call" in body
