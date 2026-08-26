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


# Every surface that can load a fragment. Scoping this to `skills/*/SKILL.md` was the first version's
# defect: `agents/adversarial-reviewer.md` is a real consumer of `test-runner-detection.md`, so the
# derivation under-reported by one and the row-match test passed green anyway — this file's own docstring
# defect, reproduced inside the fix for it.
def _consumer_files():
    yield from (REPO / "skills").glob("*/SKILL.md")
    yield from (REPO / "skills").glob("*/references/*.md")
    yield from (REPO / "agents").glob("*.md")
    yield from (REPO / "commands").glob("*.md")


def _consumer_name(path):
    """`skills/foo/SKILL.md` -> `foo`; `agents/bar.md` -> `agents/bar`; `commands/baz.md` -> `baz`."""
    if path.name == "SKILL.md":
        return path.parent.name
    if path.parent.name in {"agents", "commands"}:
        return f"{path.parent.name}/{path.stem}"
    return f"{path.parent.parent.name}/{path.stem}"


def _loaders(fragment_name):
    """Every file referencing the fragment, on any surface. Derived, never trusted."""
    return sorted({
        _consumer_name(p) for p in _consumer_files()
        if f"shared/{fragment_name}" in p.read_text()
    })


# `skills/shared/README.md` mandates the absolute form, because a bare relative path is left literal in
# a skill body and resolves against the USER's project, where it does not exist. Presence is not enough:
# the first version of `_loaders` matched both forms, so six broken references passed for free.
REQUIRED_FORM = "${CLAUDE_PLUGIN_ROOT}/skills/shared/"


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


@pytest.mark.parametrize("fragment", FRAGMENTS, ids=lambda p: p.name)
def test_every_reference_uses_the_absolute_plugin_path(fragment):
    """The form, not just the presence. A bare `skills/shared/x.md` in a skill body is not interpolated
    and resolves against the user's project — so the instruction silently fails at runtime, which is
    exactly what four skills and one agent were doing until 2026-08-21."""
    bad = []
    for p in _consumer_files():
        text = p.read_text()
        if f"shared/{fragment.name}" not in text:
            continue
        # Per REFERENCE, not per line. Membership was enough before, so appending
        # ", see also skills/shared/decision-request.md" to an already-compliant sentence passed
        # clean — one bare path per line, free, in the check written because six of them shipped.
        for ref in re.findall(r"[\w${}./-]*shared/" + re.escape(fragment.name), text):
            if not ref.startswith(REQUIRED_FORM):
                bad.append(f"{p.relative_to(REPO)}: {ref}")
    assert not bad, (
        "references must use ${CLAUDE_PLUGIN_ROOT}/skills/shared/<fragment>, per skills/shared/README.md:\n"
        + "\n".join(bad)
    )
