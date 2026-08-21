"""Keeps `skills/shared/README.md`'s loader table honest by deriving it.

Written 2026-08-21, during slice 01 of `decision-request-standard`, because the table was wrong at
the moment a new row was about to be added to it. It claimed `test-runner-detection.md` was loaded by
`work` and `edd` — neither references it — and omitted `adversarial-review` and `refactor-loop`, which
do. The fragment's own header disagreed with both, naming `refactor`. Three hand-maintained registries,
three answers.

A stale registry is worse than no registry: the next author copies the pattern *and* the wrong list,
and a reader auditing consumers audits the wrong four skills. Deriving it costs one glob.

Scope note: this checks the *table*, not conformance. Whether a referencing skill's asks obey
`decision-request.md` is not checkable here — slice 03 owns the build-level reference check and
inherits the same limit.
"""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SHARED = REPO / "skills" / "shared"
README = SHARED / "README.md"

FRAGMENTS = sorted(p for p in SHARED.glob("*.md") if p.name != "README.md")


def _loaders(fragment_name):
    """Skills whose SKILL.md references the fragment, derived."""
    return sorted(
        p.parent.name
        for p in (REPO / "skills").glob("*/SKILL.md")
        if f"shared/{fragment_name}" in p.read_text()
    )


def _table_rows():
    """Parse the README's `| file | loaders |` table into {filename: [skills]}."""
    rows = {}
    for line in README.read_text().splitlines():
        m = re.match(r"^\|\s*`([^`]+\.md)`\s*\|(.+)\|\s*$", line)
        if m:
            rows[m.group(1)] = sorted(re.findall(r"`([^`]+)`", m.group(2)))
    return rows


def test_every_fragment_has_a_row():
    missing = [f.name for f in FRAGMENTS if f.name not in _table_rows()]
    assert not missing, f"fragments absent from the README table: {missing}"


def test_no_row_names_a_fragment_that_does_not_exist():
    names = {f.name for f in FRAGMENTS}
    ghosts = [k for k in _table_rows() if k not in names]
    assert not ghosts, f"README table rows for missing fragments: {ghosts}"


@pytest.mark.parametrize("fragment", FRAGMENTS, ids=lambda p: p.name)
def test_the_row_matches_the_derived_loaders(fragment):
    """The assertion that would have caught the 2026-08-21 drift."""
    claimed = _table_rows().get(fragment.name, [])
    actual = _loaders(fragment.name)
    assert claimed == actual, (
        f"{fragment.name}: README claims {claimed}, derived {actual}"
    )


@pytest.mark.parametrize("fragment", FRAGMENTS, ids=lambda p: p.name)
def test_a_fragment_is_loaded_by_someone(fragment):
    """An unreferenced fragment is inert — the failure mode `spirit-walk` demonstrates, where a rule
    was written in the one place that could not fire it."""
    assert _loaders(fragment.name), f"{fragment.name} is referenced by no skill"


@pytest.mark.parametrize("fragment", FRAGMENTS, ids=lambda p: p.name)
def test_a_fragment_carries_no_frontmatter(fragment):
    """`skills/shared/` holds no SKILL.md by design, per its README. Frontmatter here would read as a
    registrable skill."""
    assert not fragment.read_text().startswith("---"), f"{fragment.name} carries frontmatter"
