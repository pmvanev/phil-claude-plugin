"""Structural tests for `skills/harden-instructions/` (formerly `claude-md`) and the rules it applies.

`rules/agent-instructions.md` reaches a run only because the skill names it, and the skill's promise
to leave generated regions alone exists only in its prose. These tests pin both mentions and keep the
self-test fixtures well-formed.

**What this cannot check.** A mention is not an application — the gap
`scripts/check-rule-reachability.py` states in its own header. Whether a run left a region untouched
or kept a rule's meaning is judged by a human against each fixture's `expected.md`.

Written 2026-10-13, when the rule landed.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "harden-instructions" / "SKILL.md"
SELF_TEST = REPO / "skills" / "harden-instructions" / "self-test"
COMMANDS = REPO / "commands"
RULE = REPO / "rules" / "agent-instructions.md"


def _fixtures():
    return sorted(p for p in SELF_TEST.iterdir() if p.is_dir() and p.name[:2].isdigit())


def test_the_skill_names_its_rules():
    text = SKILL.read_text()
    assert "rules/agent-instructions.md" in text
    assert "rules/claude-md.md" in text


def test_the_claude_md_rule_points_at_agent_instructions():
    assert "agent-instructions.md" in (REPO / "rules" / "claude-md.md").read_text()


def test_the_skill_promises_to_leave_generated_regions_unchanged():
    text = SKILL.read_text()
    assert re.search(r"generated regions? byte-for-byte unchanged", text, re.I)
    assert ":begin -->" in text and ":end -->" in text


def test_the_skill_cuts_history_only_when_a_commit_holds_it():
    text = SKILL.read_text()
    assert "status --porcelain --ignored" in text
    assert "git show" in text


def test_the_command_grants_the_git_reads_the_skill_runs():
    grant = (COMMANDS / "harden-instructions.md").read_text()
    assert "Bash(git -C:*)" in grant


def test_the_old_name_still_runs_the_skill_and_says_it_was_renamed():
    """Removing `/phil:claude-md` outright turns muscle memory into "unknown command"."""
    alias = (COMMANDS / "claude-md.md").read_text()
    assert "skills/harden-instructions/SKILL.md" in alias
    assert "/phil:harden-instructions" in alias.split("---", 2)[2]


def test_every_profile_is_named_with_its_layout_standard():
    text = SKILL.read_text()
    for profile in ("**Project memory**", "**Skill**", "**Agent**", "**Command**", "**Reference**"):
        assert profile in text, profile
    assert "rules/claude-md.md" in text
    assert "skill-development" in text


def test_a_shipped_file_is_never_judged_against_the_authoring_repository():
    """A skill runs in the user's repository; a file missing here says nothing about it there."""
    text = SKILL.read_text()
    assert "**Shipped and local files.**" in text
    assert "authoring-time only" in text


def test_the_alias_keeps_its_old_no_argument_behaviour():
    alias = (COMMANDS / "claude-md.md").read_text()
    assert "$ARGUMENTS` empty" in alias


def test_frontmatter_is_frozen():
    """A skill's description decides when it triggers; an edit there changes behaviour silently."""
    assert re.search(r"frontmatter byte-for-byte unchanged", SKILL.read_text(), re.I)


def test_git_reads_run_against_the_targets_repository():
    """Run from the working directory, a search on another repo's file finds nothing there and
    judges every rule stale."""
    text = SKILL.read_text()
    assert "rev-parse --show-toplevel" in text
    assert "git -C <root> status" in text


def test_directory_mode_skips_self_test_inputs():
    """The fixtures' inputs are flawed on purpose; a directory run that "fixed" them would
    destroy the suite while every test here stayed green."""
    assert "self-test/" in SKILL.read_text().split("## Directory Path", 1)[1].split("\n## ", 1)[0]


def test_a_check_collapses_a_rule_only_when_a_test_proves_it():
    text = SKILL.read_text()
    assert "unproven" in text
    assert (SELF_TEST / "02-enforced-rule-collapses" / "tests").is_dir()
    assert not (SELF_TEST / "05-unproven-check-keeps-prose" / "tests").exists()


def test_the_rule_carries_its_tiers_and_checklist():
    text = RULE.read_text()
    for tier in ("**Enforce**", "**Derive**", "**Name**", "**State**"):
        assert tier in text, tier
    assert "### Quick Reference Checklist" in text


def test_every_fixture_holds_an_input_and_an_expected_outcome():
    fixtures = _fixtures()
    assert len(fixtures) >= 6
    for f in fixtures:
        assert (f / "CLAUDE.md").is_file() or (f / "SKILL.md.input").is_file(), f.name
        assert (f / "expected.md").is_file(), f.name


def test_a_fixture_exercises_the_skill_profile():
    assert any((f / "SKILL.md.input").is_file() for f in _fixtures())


def test_no_fixture_ships_a_file_named_skill_md():
    """A flawed-on-purpose `SKILL.md` below `skills/` risks discovery as a real skill in every install."""
    assert not list(SELF_TEST.rglob("SKILL.md"))


def test_fixture_01_markers_pair_up():
    text = (SELF_TEST / "01-generated-region-untouched" / "CLAUDE.md").read_text()
    begins = re.findall(r"<!-- (\S+):begin -->", text)
    ends = re.findall(r"<!-- (\S+):end -->", text)
    assert begins and begins == ends


def test_the_readme_lists_every_fixture():
    readme = (SELF_TEST / "README.md").read_text()
    for f in _fixtures():
        assert f.name in readme, f.name
