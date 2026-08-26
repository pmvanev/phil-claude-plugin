"""Tests for `scripts/check-decision-request-reference.py` — the [D10] enforcement check.

Two things are pinned here, and the second is the one that matters.

**That the check fails on every input that motivated it.** `CLAUDE.md`'s standing rule, written after
`check-readonly-commands.py`'s first version was written, never called, and silently passed. Four inputs
motivated this check and each has a case below; a valid exemption has one too, because a check that
cannot pass is as useless as one that cannot fail.

**That the check's own documented limits stay documented.** Its signal is genuinely shallow — a resolved
reference, never a conforming ask — and the value of a shallow signal depends entirely on the shallowness
being stated. `CLAUDE.md` records the alternative: *"absence of `Write` never meant read-only"*, a green
check standing in for the property nobody measured.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check-decision-request-reference.py"
REF = "${CLAUDE_PLUGIN_ROOT}/skills/shared/decision-request.md"


def _run(root: Path):
    proc = subprocess.run([sys.executable, str(root / "scripts" / SCRIPT.name)],
                          capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout


@pytest.fixture
def tree(tmp_path):
    """A minimal plugin: one command granting the tool, one skill referencing the standard."""
    (tmp_path / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp_path / "scripts" / SCRIPT.name)
    (tmp_path / "skills" / "shared").mkdir(parents=True)
    (tmp_path / "skills" / "shared" / "decision-request.md").write_text("# the standard\n")
    (tmp_path / "skills" / "asker").mkdir()
    (tmp_path / "skills" / "asker" / "SKILL.md").write_text(
        f"---\nname: asker\ndescription: d\n---\n\nAsk via AskUserQuestion, following `{REF}`.\n")
    (tmp_path / "commands").mkdir()
    (tmp_path / "commands" / "ask.md").write_text(
        "---\ndescription: d\nmutates: true\n"
        "allowed-tools: Read, AskUserQuestion, Skill\n---\n\n"
        "Load `${CLAUDE_PLUGIN_ROOT}/skills/asker/SKILL.md`.\n")
    return tmp_path


def test_a_wired_tree_is_silent(tree):
    rc, out = _run(tree)
    assert rc == 0 and out == "", out


def test_direction_a_a_grant_with_no_standard(tree):
    """The state nine of thirteen commands were in. The command can ask; nothing tells it how."""
    p = tree / "skills" / "asker" / "SKILL.md"
    p.write_text(p.read_text().replace(f", following `{REF}`", ""))
    rc, out = _run(tree)
    assert rc == 1 and "none of those references" in out


def test_a_reference_by_bare_path_is_not_a_reference(tree):
    """Present but inert: a bare relative path is left literal in a skill body and resolves against the
    USER's project. Six such references shipped in this repo before 2026-08-21."""
    p = tree / "skills" / "asker" / "SKILL.md"
    p.write_text(p.read_text().replace(REF, "skills/shared/decision-request.md"))
    rc, out = _run(tree)
    assert rc == 1 and "not ${CLAUDE_PLUGIN_ROOT}" in out


def test_direction_b_an_ask_site_with_no_grant(tree):
    """The live defect this direction was added for. `skills/refactor/SKILL.md` asked "Refactoring
    without tests is risky. Continue anyway?" while `commands/refactor.md` granted no such tool — so the
    call was refused, and a refused tool looks like a skipped step.

    A one-directional check would have reported that tree clean.
    """
    p = tree / "commands" / "ask.md"
    p.write_text(p.read_text().replace(", AskUserQuestion", ""))
    rc, out = _run(tree)
    assert rc == 1 and "the ask is dead" in out


def test_an_exemption_must_carry_a_reason(tree):
    """Silence is never conformance, and neither is a token gesture at one."""
    p = tree / "commands" / "ask.md"
    (tree / "skills" / "asker" / "SKILL.md").write_text("---\nname: asker\ndescription: d\n---\n\nnothing\n")
    p.write_text(p.read_text() + "\n<!-- decision-request-exempt: why -->\n")
    rc, out = _run(tree)
    assert rc == 1 and "no usable reason" in out


def test_a_reasoned_exemption_passes(tree):
    """A check with no expressible exemption gets satisfied by a fake reference instead."""
    (tree / "skills" / "asker" / "SKILL.md").write_text("---\nname: asker\ndescription: d\n---\n\nnothing\n")
    p = tree / "commands" / "ask.md"
    p.write_text(p.read_text() + "\n<!-- decision-request-exempt: this command never questions a human -->\n")
    rc, out = _run(tree)
    assert rc == 0 and out == "", out


def test_an_exemption_on_the_skill_also_counts(tree):
    """The marker is an HTML comment precisely so it works in either file. A command's grant and the
    skill that carries its behaviour are two halves of one decision."""
    p = tree / "skills" / "asker" / "SKILL.md"
    p.write_text("---\nname: asker\ndescription: d\n---\n\nnothing"
                 "\n<!-- decision-request-exempt: this skill never questions a human -->\n")
    rc, out = _run(tree)
    assert rc == 0 and out == "", out


def test_the_scripts_header_states_what_it_does_not_check():
    """AC6, and the reason this check is worth having at all.

    A shallow signal is acceptable when its shallowness is stated and unacceptable when it is not.
    Deleting these sentences would leave a green check that reads as conformance — the
    `check-readonly-commands.py` failure, one artifact over.
    """
    body = " ".join(SCRIPT.read_text().split())
    assert "It does not check that any ask **conforms**" in body
    assert "can still emit a bare option list" in body
    assert "Conformance in flight is unenforced" in body


def test_the_header_records_both_directions_and_why():
    """A later reader will see direction B as redundant with direction A and delete it. The live defect
    it caught is the argument, and it has to be in the file."""
    body = " ".join(SCRIPT.read_text().split())
    assert "Direction A" in body and "Direction B" in body
    assert "skills/refactor/SKILL.md" in body, (
        "the instance that justifies direction B must be named, or the direction reads as symmetry "
        "for its own sake"
    )


def test_the_real_repo_is_wired():
    """The check against this repo, not a fixture. Slice 03's AC3."""
    rc, out = _run(REPO)
    assert rc == 0, out
