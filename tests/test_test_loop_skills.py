"""`refactor-tests` and `redesign-tests` run one human-gated loop; both must keep its promises.

Found 2026-10-13, all predating that day's hardening:
- Each opened by promising every change is "applied only after" approval, while its own loop applies
  the change to the working tree before the human gate; the promise is about the commit.
- Each said to stage only the touched test file, but a plain `git commit` also takes whatever the
  developer had already staged.
- Neither said what an "Other" answer, or no answer, does at the gate — with the change already applied.
- Scoped mode has no backlog, yet the commit subject, item marking and resume all read one.
- "Reject/skip/quit always ... write nothing" sat beside instructions to mark the backlog.
- In refactor-tests the gate's rules named `abort` while its options named `quit`.
"""
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SKILLS = ["refactor-tests", "redesign-tests"]


def _flat(skill):
    return " ".join((REPO / "skills" / skill / "SKILL.md").read_text().split())


@pytest.mark.parametrize("skill", SKILLS)
def test_the_promise_is_about_the_commit(skill):
    body = _flat(skill)
    assert "only after the developer approves" in body
    assert "apply every" not in body and "applied only after" not in body
    feature = " ".join((REPO / "skills" / skill / "acceptance.feature").read_text().split())
    assert "applied only after I approve" not in feature


@pytest.mark.parametrize("skill", SKILLS)
def test_the_commit_takes_only_the_touched_files(skill):
    assert "git commit -m <message> -- <files>" in _flat(skill)


@pytest.mark.parametrize("skill", SKILLS)
def test_any_other_answer_reverts(skill):
    assert "Any other answer, or none, reverts as **reject** does" in _flat(skill)


@pytest.mark.parametrize("skill", SKILLS)
def test_scoped_mode_writes_its_items_to_the_backlog(skill):
    assert "A scoped run first writes its items into" in _flat(skill)


@pytest.mark.parametrize("skill", SKILLS)
def test_a_declined_change_writes_nothing_to_the_tests_or_git(skill):
    body = _flat(skill)
    assert "revert cleanly and write nothing." not in body
    assert "write nothing to the test files or git" in body


def test_refactor_tests_names_one_fourth_option():
    body = _flat("refactor-tests")
    assert "`abort` ends the loop" not in body
    assert "`quit` ends the loop" in body


@pytest.mark.parametrize("skill", SKILLS)
def test_the_whole_tree_is_clean_and_a_revert_removes_created_files(skill):
    """A move or rewrite may write conftest.py or a new helper, beyond the target test file."""
    body = _flat(skill)
    assert "`git status --porcelain` shows no change outside the backlog files" in body
    assert "and remove any file it created" in body
