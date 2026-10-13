"""`eos`, `clean-comments`, `extract-method` and `spirit-walk`: defects that predate their 2026-10-13
hardening.

- `clean-comments` said deleting a comment never changes behaviour; doctests, docstrings read at run
  time, build directives, lint and type pragmas and shebangs are comments that do.
- `eos`'s and `clean-comments`' examples turned "a while" into "5 minutes": a fact the text never held,
  written into the file. Two `eos` rows contradicted its own Safety ("Implement → Build" replaces a domain
  term; "Not important → Trivial" overstates).
- `extract-method` had no clean-tree check, no baseline run and no defined undo, on a grant with bare Bash.
- The three editing skills tested an extension before a directory, accepted a bare line range naming no
  file, and globbed `node_modules/` and `self-test/` alike.
- `spirit-walk` recommends `git blame` and `git log -S`, both of which ran a repo-configured textconv
  filter on git 2.53.0 (verified 2026-10-13); `-u` and `--patch` slipped past its `-p` ban; its
  double-quoted `-S` template let the shell expand `$`; and it named web tools its grant lacks.
"""
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
EDITORS = ["eos", "clean-comments", "extract-method"]


def _flat(skill):
    return " ".join((SKILLS / skill / "SKILL.md").read_text().split())


def test_clean_comments_names_the_comments_that_carry_behaviour():
    body = _flat("clean-comments")
    assert "Deleting a comment never changes behavior" not in body
    for kind in ("doctest", "build directive", "pragma", "shebang", "read at run time"):
        assert kind in body, kind


@pytest.mark.parametrize("skill", ["eos", "clean-comments"])
def test_no_edit_invents_a_fact(skill):
    assert "Use only a fact the text or its code already holds" in _flat(skill)


def test_eos_tables_agree_with_its_safety():
    text = (SKILLS / "eos" / "SKILL.md").read_text()
    assert "| Implement | Build |" not in text
    assert "| Not important | Trivial |" not in text


def test_extract_method_checks_the_tree_takes_a_baseline_and_defines_undo():
    body = _flat("extract-method")
    assert "git status --porcelain" in body
    assert "${CLAUDE_PLUGIN_ROOT}/skills/shared/test-runner-detection.md" in body
    assert "Run the suite once before the first extraction" in body
    assert "remove any file the step created" in body


@pytest.mark.parametrize("skill", EDITORS)
def test_editors_parse_a_directory_first_and_refuse_a_bare_range(skill):
    text = (SKILLS / skill / "SKILL.md").read_text()
    assert text.index("| Is a directory") < text.index("| Has a file extension")
    assert "A bare line range names no file: ask which file" in _flat(skill)


@pytest.mark.parametrize("skill", EDITORS)
def test_editors_skip_vendored_generated_and_fixture_trees(skill):
    body = _flat(skill)
    assert "`node_modules/`" in body and "`self-test/`" in body


def test_spirit_walk_reads_history_without_running_filters():
    body = _flat("spirit-walk")
    assert "git log -S '<snippet>' --no-textconv" in body
    assert "git blame --no-textconv" in body
    assert "`-u`, `--patch`" in body
    assert "**WebSearch / WebFetch**" not in body
