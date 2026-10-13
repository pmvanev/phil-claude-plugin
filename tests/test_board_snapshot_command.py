"""`commands/board-snapshot.md` loads `skills/board-snapshot/SKILL.md`; what it restates must agree with
the skill.

Found 2026-10-13, all predating that day's hardening: the command named `rules/writing.md` by a bare path
that resolves against the consumer's repo, left the off-board line out of the composed list, asked for a
project id the query never uses, told the run to end with one resolving "command" where the skill names a
resolver per report line, and never said how to choose the target its argument-hint offers. Inside the
skill, "never `gh issue list`" read as banning the reconciliation call the skill prescribes.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "board-snapshot.md"
SKILL = REPO / "skills" / "board-snapshot" / "SKILL.md"


def _flat(path):
    return " ".join(path.read_text().split("---", 2)[2].split())


def test_the_writing_standard_is_named_from_the_plugin_root_and_read():
    body = _flat(COMMAND)
    bare = [m.start() for m in re.finditer(r"rules/writing\.md", body)
            if not body[:m.start()].endswith("${CLAUDE_PLUGIN_ROOT}/")]
    assert not bare, "a bare rules/writing.md resolves against the consumer's repo"
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in body


def test_the_command_lists_every_report_line_the_skill_composes():
    skill = _flat(SKILL)
    lines = re.search(r"the (drift, [a-z, -]+ and inflation) lines", skill).group(1)
    assert "off-board" in lines
    assert f"the {lines} lines" in _flat(COMMAND)


def test_the_constants_are_the_ones_the_query_uses():
    """The skill's query takes `-f o=<owner> -F n=<project-number> -f f=Status`; the command names those
    three and nothing the query does not use."""
    inputs = re.findall(r"-[fF] (\w)=<?([\w-]+)", SKILL.read_text())
    assert {k for k, _ in inputs} == {"o", "n", "f"}, inputs
    body = _flat(COMMAND)
    assert "project id" not in body
    assert "the owner, the project number and the Status field" in body


def test_each_report_line_names_its_own_resolver_and_every_outcome_is_reported():
    body = _flat(COMMAND)
    assert "End by naming the command that acts on anything reported" not in body
    assert "Each report line names its resolver where the skill gives one" in body
    drift = re.search(r"\*\*Drift\*\*.*?`(phil:[\w-]+)`", _flat(SKILL)).group(1)
    example = re.search(r"1 card in Done while open; `(phil:[\w-]+)`", body).group(1)
    assert example == drift, "the command's drift example must name the skill's drift resolver"
    assert "every outcome the skill's `## Decision outcomes` requires" in body
    assert "`READ-ONLY`" in body


def test_the_target_is_the_forge_line_and_a_mismatch_stops():
    body = _flat(COMMAND)
    assert "The target is the repo the constants' forge line names" in body
    assert "When the argument differs, or `CLAUDE.md` holds no board constants, stop" in body
    assert "Pass `-R <owner/repo>` on every `gh issue` call" in body


def test_the_skill_bans_gh_issue_list_for_the_board_read_only():
    skill = _flat(SKILL)
    assert "never `gh issue list`, which returns no Status at all, for the board read" in skill
    assert "gh issue list -R <owner/repo> --state open" in SKILL.read_text()
