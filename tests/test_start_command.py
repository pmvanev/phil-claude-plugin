"""`commands/start.md` loads `skills/start/SKILL.md`; together they carry start-work's slice 01 decisions.

Slice 01 is the start report: it resolves the argument to one open card, applies the refusals, describes
the card and recommends a route, and writes nothing. Each test pins one decision from
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


def test_slice_01_grants_no_file_write():
    """The report writes nothing. Slices 02 and 03 add the writes, and change this test with them."""
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
    """`phil:issue-board`: an inferred remote reads the wrong repo successfully. Every call is
    `gh api graphql`, which takes no `-R`, so the repo reaches it as query variables."""
    for path in (SKILL, COMMAND):
        _, body = _parts(path)
        assert "Pass the owner and repo as variables to" in body, path.name
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


def test_no_match_files_nothing():
    """D4, AC1.2: filing is slice 02's, and only on a yes."""
    _, body = _parts(SKILL)
    assert "File nothing" in body


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


def test_slice_01_writes_nothing_before_the_launch():
    """skill-reviewer and plugin-validator, 2026-11-03: an unscoped "Write nothing" contradicted the
    inline route, which edits files once the developer says yes."""
    for path in (SKILL, COMMAND):
        assert "Write nothing before the launch" in _parts(path)[1], path.name
    _, body = _parts(SKILL)
    assert "Send only `query` documents through `gh api graphql`, never `mutation`" in body


def test_every_bash_grant_is_used():
    """plugin-validator, 2026-11-03: `Bash(gh issue view:*)` was copied from `/phil:done` and never
    called."""
    front, _ = _parts(COMMAND)
    _, body = _parts(SKILL)
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
