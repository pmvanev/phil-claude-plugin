"""`skills/ux-review/SKILL.md`: the checklist must mirror `rules/ux.md`, and the review must read, write and
report as its sibling `review-code` now does.

Found 2026-10-13, all predating that day's hardening:
- The always-flag reduced-motion row in `ux.md` — the row fixture 02 exists for — was missing from the
  must-fix checklist, and the advisory list omitted the motion-budget and small-size legibility items.
- The first must-fix row flagged `onClick` on a `<div>`, the element-semantics bullet the skill's own
  Do-not-flag list assigns to `react.md`; `ux.md`'s row is about keyboard operation, focus and traps.
- No operative step said the review leaves the reviewed files unmodified; fixture 08 relies on it.
- Step 4 never reported which files were reviewed or skipped; fixture 07 gates on it.
- `--changes`, the directory glob, Explore-agent reading, backlog replacement, extension-before-
  directory parsing and the released-copy self-test carried the defects `review-code` lost in f0a7fd5.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "ux-review" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split())


def _section(title):
    return " ".join(SKILL.read_text().split(title, 1)[1].split("\n### ", 1)[0].split())


def test_the_reduced_motion_row_is_must_fix():
    assert "no reduced-motion variant" in _section("### Must-fix")


def test_the_advisory_list_carries_the_motion_budget_and_small_size_legibility():
    consider = _section("### Consider")
    assert "motion & effect budget" in consider.lower()
    assert "legibility at small sizes" in consider.lower()


def test_element_semantics_stay_with_react_md():
    assert "`onClick` on a `<div>`" not in _section("### Must-fix")


def test_the_review_edits_nothing_and_reports_its_scope():
    body = _flat()
    assert "Edit none of the reviewed files" in body
    assert "which files were reviewed and which were skipped as non-UI" in body


def test_changes_mode_globbing_reading_and_the_backlog_match_review_code():
    body = _flat()
    assert "git ls-files --others --exclude-standard" in body
    assert "`node_modules/`" in body
    assert "use an Explore agent to parallelize reading" not in body
    assert "never drop or renumber an existing item" in body
    text = SKILL.read_text()
    assert text.index("| Is a directory") < text.index("| Has a file extension")
    assert "drive this working tree's `SKILL.md` by hand" in body
