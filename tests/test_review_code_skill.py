"""`skills/review-code/SKILL.md`: what a review reads, writes and routes.

Found 2026-10-13, all predating that day's hardening:
- Step 3 replaced `.refactoring-backlog.md` whole, destroying an in-progress `/phil:refactor` run and
  reusing IDs earlier commits cite.
- `refactor-loop` seeds from this skill after its clean-tree check, and the backlog it writes made the
  loop's own APPLY check HALT on the first iteration.
- `--changes` missed untracked files, read deleted ones, failed with no parent commit, and never read
  the tests of the code it reviewed — the reason File Path mode gives for reading them applies to all.
- The catalogue-name rule could not be met for Priority 1, Priority 7, or a smell the catalogue does
  not hold; Priority 7 had no route, and a test-file idiom fix routed to a refactor that edits tests.
- Directory mode globbed `node_modules/` and `.venv/` alike, and handed reading to an Explore agent
  whose summary cannot give the exact lines the backlog records.
- "Longer than 20 lines" and "more than 3 arguments" let pass what `coding.md` calls long.
- "Has a file extension" was tested before "is a directory", so `.` and `conf.d/` read as files.
- The self-test drove `/phil:review-code`, which runs the released copy, not the edit under test.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
LOOP = REPO / "skills" / "refactor-loop" / "SKILL.md"


def _flat(path=SKILL):
    return " ".join(path.read_text().split())


def test_an_existing_backlog_is_extended_never_replaced():
    assert "never drop or renumber an existing item" in _flat()


def test_refactor_loop_s_clean_checks_ignore_the_seeded_backlog():
    loop = _flat(LOOP)
    assert loop.count("':!.refactoring-backlog.md'") >= 2
    assert "only items whose **Route** is `/phil:refactor`" in loop


def test_changes_mode_covers_untracked_deleted_and_parentless_cases_and_reads_tests():
    body = _flat()
    assert "git ls-files --others --exclude-standard" in body
    assert "Skip deleted files" in body
    assert "With no parent commit" in body
    assert "find the tests of each changed production file" in body


def test_findings_the_catalogue_cannot_name_have_a_rule_and_priority_7_a_route():
    body = _flat()
    assert "the catalogue names no refactoring for it" in body
    assert "a Priority 7 item routes to `/phil:refactor` in production code and `report only` in a test file" in body


def test_directory_mode_skips_vendored_trees_and_reads_files_itself():
    body = _flat()
    assert "`node_modules/`" in body
    assert "use an Explore agent to parallelize reading" not in body


def test_thresholds_match_coding_md():
    body = _flat()
    assert "Functions of 20 lines or more" in body
    assert "three or more arguments without a stated reason" in body


def test_a_directory_is_recognised_before_an_extension():
    text = SKILL.read_text()
    assert text.index("| Is a directory") < text.index("| Has a file extension")


def test_the_self_test_drives_this_working_tree():
    assert "drive this working tree's `SKILL.md` by hand" in _flat()
