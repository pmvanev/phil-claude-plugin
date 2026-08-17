"""Tests for `scripts/check-readonly-commands.py` — the checker that guards every command's grant.

This file exists because of a recorded incident. `CLAUDE.md`: the first version of the
path-or-variable check *silently passed* — the function was written and never called, which is this
board's recurring defect reproduced inside the fix for it. The instruction it ends with is "test
that a new check fails on the input that motivated it before trusting a green run", and until now
the checker itself was the one script in `scripts/` with no test.

A green run from an unexercised checker is indistinguishable from a green run from a working one.
"""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-readonly-commands.py"


def load():
    spec = importlib.util.spec_from_file_location("check_readonly_commands", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cc = load()


# --- the motivating input: a grant carrying a variable or a path -------------------------

def test_a_grant_with_a_variable_is_rejected():
    """The exact defect `board-setup` shipped: `allowed-tools` does not interpolate, so this
    matches nothing and prompts on every run while looking narrower than any real grant."""
    assert cc.check_grant_is_matchable(
        "x.md", "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/probe-board.py:*)")


def test_a_grant_with_a_path_is_rejected():
    """Permission rules are literal prefix matches, so a relative path is equally unmatchable."""
    assert cc.check_grant_is_matchable("x.md", "Bash(python3 scripts/probe-board.py:*)")


def test_a_bare_executable_grant_is_accepted():
    assert cc.check_grant_is_matchable("x.md", "Bash(python3:*)") is None


def test_a_multi_word_verb_grant_is_accepted():
    """`Bash(git ls-tree:*)` is two words and no path — the shape 210 of 211 audited grants use."""
    assert cc.check_grant_is_matchable("x.md", "Bash(git ls-tree:*)") is None


# --- the whole check, over the real tree -------------------------------------------------

def test_the_repo_passes_its_own_check():
    assert cc.main() == 0


def test_the_reported_count_matches_the_grants_actually_inspected(capsys):
    """The success line claimed 204 `Bash(...)` grants when 43 exist — it was counting every grant
    of every kind. An auditor reading the inflated number would infer roughly five times the
    coverage that exists."""
    import re
    cc.main()
    out = capsys.readouterr().out
    m = re.search(r"(\d+) `Bash\(\.\.\.\)` grant\(s\) verified matchable", out)
    assert m, out

    root = SCRIPT.resolve().parent.parent
    actual = sum(
        len(re.findall(r"Bash\(", fm.group(1)))
        for p in (root / "commands").glob("*.md")
        for fm in [re.search(r"^---\n(.*?)\n---", p.read_text(), re.S)] if fm
    )
    assert int(m.group(1)) == actual, f"reported {m.group(1)}, actual Bash() grants {actual}"
