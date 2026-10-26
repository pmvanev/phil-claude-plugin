"""`/phil:lambda-web-app-speed` and its skill, which measure a Lambda web app's cold path.

The command reads a person's AWS account with a role that can usually do far more than read, so what
keeps it read-only is its grant and its prose together. This file holds the grant to AWS read verbs,
the prose to forbidding every write and every forced cold start (D12), the fetch to the one filter the
script expects, and every number to the command that produced it.

**What this cannot check.** `python3` is granted to run `cold-path.py` and `phases.py`, and `python3`
can write; that is why the command declares `mutates: true`. Whether a run uses it for anything else is
model behaviour, which the skill's prose carries.

Written 2026-10-26, with slice 02 of `docs/feature/lambda-web-app-speed/` (issue 59).
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "lambda-web-app-speed.md"
SKILL = REPO / "skills" / "lambda-web-app-speed" / "SKILL.md"
SCRIPT = REPO / "skills" / "lambda-web-app-speed" / "scripts" / "cold-path.py"
RULE = REPO / "rules" / "lambda-web-app-speed.md"
READ_VERB = re.compile(r"^aws (sts|lambda|logs) (get|list|filter)-[a-z-]+$")


def _frontmatter(path):
    return path.read_text().split("---", 2)[1]


def _grants():
    line = re.search(r"^allowed-tools:\s*(.+)$", _frontmatter(COMMAND), re.M).group(1)
    return [g.strip() for g in line.split(",")]


def _body(path):
    return " ".join(path.read_text().split())


def test_the_command_declares_its_grant_can_mutate():
    """python3 runs the script, and python3 can write; mutates is about the grant (CLAUDE.md)."""
    assert re.search(r"^mutates: true$", _frontmatter(COMMAND), re.M)


def test_every_aws_grant_is_a_read_verb():
    aws = [g[len("Bash("):].split(":")[0] for g in _grants() if g.startswith("Bash(aws")]
    assert aws, "the command reaches AWS through no grant"
    for verb in aws:
        assert READ_VERB.match(verb), f"{verb} is not a get, list or filter verb"


def test_the_command_grants_no_editor_and_no_bare_shell():
    for grant in _grants():
        assert grant not in {"Write", "Edit", "NotebookEdit", "Bash"}, grant


def test_the_skill_forbids_every_write_and_every_forced_cold_start():
    body = _body(SKILL)
    for phrase in ("Never invoke the function", "deploy", "change its configuration", "force a cold start",
                   "do not suggest forcing one"):
        assert phrase in body, phrase
    assert "`python3` runs `cold-path.py`, `phases.py` and `rank.py`, and nothing else" in body


def test_the_fetch_uses_the_filter_the_script_reads():
    pattern = """--filter-pattern '?"REPORT RequestId" ?INIT_REPORT'"""
    assert pattern in SCRIPT.read_text()
    assert pattern in SKILL.read_text()


def test_the_window_comes_from_the_script_not_arithmetic_by_hand():
    """A start time worked out by hand is silently wrong, and the citation then vouches for it."""
    body = _body(SKILL)
    assert "cold-path.py --window <LastModified>" in body and "--days 14" in body
    assert "--max-items" in body, "without a cap the CLI drops NextToken, and truncation never shows"


def test_the_account_and_region_come_from_the_function_arn():
    assert "FunctionArn:FunctionArn" in SKILL.read_text()


def test_every_number_cites_the_command_that_produced_it():
    body = _body(SKILL)
    assert "Measured with:" in body
    assert "Print no raw log event" in body


def test_the_window_starts_at_the_last_change():
    body = _body(SKILL)
    assert "LastModified" in body and "mixes versions" in body


def test_the_skill_reads_the_rule_principles_before_measuring():
    assert "rules/lambda-web-app-speed.md" in SKILL.read_text()


def test_the_rule_names_both_hidden_cold_starts():
    principles = RULE.read_text().split("## Principles", 1)[1].split("\n## ", 1)[0]
    for phrase in ("INIT timeout", "suppressed init", "in time order"):
        assert phrase in principles, phrase


def test_the_readme_lists_the_command():
    assert "/phil:lambda-web-app-speed" in (REPO / "README.md").read_text()


def test_the_rule_times_concurrent_work_by_the_clock_and_fixes_the_largest_slice_first():
    principles = " ".join(RULE.read_text().split("## Principles", 1)[1].split("\n## ", 1)[0].split())
    for phrase in ("by the clock", "never summed", "Fix the largest slice first", "measure again"):
        assert phrase in principles, phrase


def test_the_skill_ranks_by_time_saved_and_draws_the_line():
    body = _body(SKILL)
    for phrase in ("scripts/rank.py", "Draw every figure from Steps 1, 3 and 4", "experiment",
                   "the target", "Stop at the line"):
        assert phrase in body, phrase


def test_the_target_is_the_projects_or_named_as_an_assumption():
    body = _body(SKILL)
    assert "the project's own cold-path budget" in body and "Borrow no client-side target" in body
