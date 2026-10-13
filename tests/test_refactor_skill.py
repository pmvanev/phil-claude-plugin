"""`skills/refactor/SKILL.md` must keep the safety its siblings gained on 2026-10-13.

Found that day, all predating its hardening:
- No clean-tree check before a loop that reverts, so an undo could discard the developer's edits.
- "Undo" was never defined: it missed created files, and a red tidying's undo wiped the green primary
  refactoring with it.
- "Stage only the files you modified" let a plain `git commit` take whatever was already staged.
- `review-code` now appends to the backlog, so inline mode worked other scopes' items, and the list was
  no longer sorted by priority as the skill assumed.
- Inline mode said to run `/phil:review-code`, which the command's grant cannot invoke.
- The test-runner detection was a hand copy of the shared fragment, including the quoted "risky" ask the
  next paragraph forbids.
- Tidyings could absorb other items' smells into one commit, and a later item's recorded lines no longer
  pointed at its smell once earlier commits moved code.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "refactor" / "SKILL.md"
FRAGMENT = REPO / "skills" / "shared" / "test-runner-detection.md"


def _flat(path=SKILL):
    return " ".join(path.read_text().split())


def test_the_tree_is_clean_before_the_loop():
    assert "git status --porcelain -- . ':!.refactoring-backlog.md'" in _flat()


def test_undo_is_defined_and_a_red_tidying_undoes_only_itself():
    body = _flat()
    assert "remove any file the step created" in body
    assert "undo only that tidying" in body


def test_the_commit_takes_only_the_item_s_files():
    assert "git commit -m <message> -- <files>" in _flat()


def test_inline_mode_works_only_the_scope_it_reviewed_in_priority_order():
    body = _flat()
    assert "only the items under the `Scope:` line the review just wrote" in body
    assert "Sort the working list by Priority" in body


def test_inline_mode_reads_review_code_rather_than_invoking_it():
    assert "${CLAUDE_PLUGIN_ROOT}/skills/review-code/SKILL.md" in _flat()


def test_test_runner_detection_comes_from_the_shared_fragment():
    body = _flat()
    assert "${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md" in body
    assert "Refactoring without tests is risky" not in body
    fragment = _flat(FRAGMENT)
    assert "Refactoring without tests is risky" not in fragment
    assert "`go.test`" not in fragment


def test_tidyings_stay_inside_their_item_and_moved_lines_are_found_by_content():
    body = _flat()
    assert "leave a tidying that another pending item names to that item" in body
    assert "find the smell by its content" in body
