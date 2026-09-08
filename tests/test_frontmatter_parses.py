"""Every skill and command's YAML frontmatter must parse.

**Written because the suite was green over an unloadable skill.** `skills/board-snapshot/SKILL.md`
shipped a `description:` whose unquoted plain scalar contained a colon-space, which YAML reads as a
nested mapping key. `yaml.safe_load` refused it, so the skill's name and description could not be read
and it would not have registered for auto-discovery — while `pytest`, `check-invariants.py`,
`check-readonly-commands.py` and `check-rule-reachability.py` all passed. Nothing in this repo parsed
skill frontmatter, so nothing could have noticed.

The failure shape is the one `CLAUDE.md` keeps recording: **partial and silent**. The command still
loaded, the file still read, and only the routing quietly never fired.

Found 2026-09-08 by `plugin-dev:plugin-validator`, which is the reviewer `CLAUDE.md` requires after
authoring — and which is not a build step. This file is the mechanism, per route 2.
"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(ROOT.glob("skills/*/SKILL.md"))
COMMANDS = sorted(ROOT.glob("commands/*.md"))


def _frontmatter(path: Path):
    text = path.read_text()
    assert text.startswith("---\n"), f"{path} has no frontmatter block"
    parts = text.split("---", 2)
    assert len(parts) >= 3, f"{path} has an unterminated frontmatter block"
    return yaml.safe_load(parts[1])


def test_the_corpus_is_not_empty():
    """A glob that silently matched nothing would make every test below vacuously true."""
    assert len(SKILLS) >= 20, f"expected the repo's skills, found {len(SKILLS)}"
    assert len(COMMANDS) >= 20, f"expected the repo's commands, found {len(COMMANDS)}"


@pytest.mark.parametrize("path", SKILLS, ids=lambda p: p.parent.name)
def test_skill_frontmatter_parses(path):
    fm = _frontmatter(path)
    assert isinstance(fm, dict), f"{path} frontmatter is not a mapping"
    assert fm.get("name"), f"{path} declares no name"
    assert fm.get("description"), f"{path} declares no description"


@pytest.mark.parametrize("path", SKILLS, ids=lambda p: p.parent.name)
def test_skill_name_matches_its_directory(path):
    """A name that disagrees with its directory is a skill nobody can invoke by the name they read."""
    assert _frontmatter(path)["name"] == path.parent.name


@pytest.mark.parametrize("path", COMMANDS, ids=lambda p: p.stem)
def test_command_frontmatter_parses(path):
    fm = _frontmatter(path)
    assert isinstance(fm, dict), f"{path} frontmatter is not a mapping"
    assert fm.get("description"), f"{path} declares no description"


def test_the_check_fails_on_the_input_that_motivated_it():
    """`CLAUDE.md`: test that a new check fails on the input that motivated it before trusting a green
    run. The first version of `check-readonly-commands.py` passed because it was never called."""
    broken = "---\nname: x\ndescription: A bounded check: what is blocked\n---\n"
    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(broken.split("---", 2)[1])
