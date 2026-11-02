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


def test_slice_01_grants_no_file_write():
    """The report writes nothing. Slices 02 and 03 add the writes, and this test with them."""
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


def test_slice_01_writes_nothing():
    _, body = _parts(SKILL)
    assert "Write nothing" in body
    assert "Send only `query` documents through `gh api graphql`, never `mutation`" in body


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
    assert "issueCount" in body and "pageInfo{ hasNextPage }" in body
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
