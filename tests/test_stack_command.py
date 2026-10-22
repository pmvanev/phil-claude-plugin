"""`/phil:stack show` names the verb that bare `/phil:stack` runs.

Asked for 2026-10-22: the skill calls the read verb `show` throughout, and the command offered only
`push` and `pop` by name, so `/phil:stack show` fell through prose that said what to do with no argument,
`push` and `pop`, and nothing else.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMMAND = REPO / "commands" / "stack.md"
STACK_PATH = REPO / "skills" / "session-handoff" / "references" / "stack.md"


def _frontmatter(path):
    return path.read_text().split("---", 2)[1]


def _flat(path):
    return " ".join(path.read_text().split("---", 2)[2].split())


def test_the_argument_hint_offers_show():
    hint = re.search(r"^argument-hint: (.+)$", _frontmatter(COMMAND), re.M).group(1)
    assert "[show]" in hint, hint


def test_the_command_runs_show_for_the_word_or_no_argument():
    assert "No argument, or `show`, shows the stack." in _flat(COMMAND)


def test_the_show_path_names_both_invocations():
    heading = re.search(r"^## show — (.+)$", STACK_PATH.read_text(), re.M).group(1)
    assert "`/phil:stack`" in heading and "`/phil:stack show`" in heading, heading
