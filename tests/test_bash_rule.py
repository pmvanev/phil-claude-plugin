"""`rules/bash.md` and `review-code`, which applies it.

Every always-flag row carries the rule's own `SH-n` id, a Hazard mark and the linter rule that catches
it where one exists. A reviewer copies the id and the row's Preferred form into the backlog, at
Priority 7, or at Priority 1 where the row is a hazard. This file holds the ids unique, keeps the rows a
linter misses in the table, keeps a POSIX `sh` script and an explicitly checked script out of it, and
holds each fixture's expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it. Whether a reviewer flagged the seeded defect and left the decoy alone is model
judgement, which the fixture's `expected.md` carries and a human drives.

Written 2026-11-06, for the Bash rule (issue 79, slice 01).
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "bash.md"
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
README = REPO / "README.md"
RESEARCH = "docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md"
FIXTURES = sorted((REPO / "skills" / "review-code" / "self-test").glob("*-shell-*/manifest.json"))
COLUMNS = ("Id", "Violation", "Preferred form", "Hazard", "Linter", "Cite")


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _section(heading):
    return RULE.read_text().split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def _rows():
    return [dict(zip(COLUMNS, _cells(line)))
            for line in _section("Always-flag").splitlines() if line.startswith("| SH-")]


def _flat(text):
    return " ".join(text.split())


def _takes_the_form(fix, form):
    """The row's form verbatim, alone or followed by ` — here: ` and this code's change."""
    return fix == form or fix.startswith(form + " — here: ")


def _items(backlog):
    return re.split(r"^### \[R\d{3}\]", backlog, flags=re.M)[1:]


def _field(item, name):
    m = re.search(rf"- \*\*{name}\*\*: (.+)", item)
    assert m, f"an expected item has no {name} field"
    return m.group(1).strip()


def test_the_rule_matches_shell_files_and_cites_its_research():
    """D9 and D14: the globs mirror the match review-code applies; every row's source is on record."""
    head = RULE.read_text().split("---", 2)[1]
    for glob in ('"**/*.sh"', '"**/*.bash"'):
        assert glob in head, glob
    assert RESEARCH in RULE.read_text()


def test_the_table_is_not_empty_and_every_row_is_whole():
    """A table that parses to nothing passes every test below silently."""
    rows = _rows()
    assert len(rows) >= 10
    for row in rows:
        assert len(row) == len(COLUMNS) and all(row.values()), row.get("Id")


def test_every_row_has_a_unique_sh_id_a_hazard_mark_and_a_linter_cell():
    ids = [_plain(r["Id"]) for r in _rows()]
    assert all(re.fullmatch(r"SH-\d+", i) for i in ids), ids
    assert len(ids) == len(set(ids)), "an SH id names two rows"
    for row in _rows():
        assert _plain(row["Hazard"]) in {"hazard", "—"}, row["Id"]
        linter = _plain(row["Linter"])
        assert linter == "none" or re.search(r"SC\d{4}|require-double-brackets", linter), row["Id"]


def test_the_failures_no_linter_catches_are_hazard_rows():
    """The gap the feature measured: ShellCheck flags neither an unchecked failure nor a lost pipe status."""
    by_violation = {_flat(r["Violation"]): r for r in _rows()}
    for phrase in ("goes unchecked", "loses the status of every command but the last"):
        matches = [r for v, r in by_violation.items() if phrase in v]
        assert len(matches) == 1, phrase
        assert _plain(matches[0]["Hazard"]) == "hazard" and _plain(matches[0]["Linter"]) == "none", phrase


def test_no_row_flags_a_script_merely_for_lacking_set_e():
    """Conflict B-1: Wooledge and ShellCheck's SC2310 page prefer explicit checks; both forms are a fix."""
    for row in _rows():
        assert not re.search(r"\bno `?set -e`?\s*$", row["Violation"].strip()), row["Id"]
    unchecked = next(r for r in _rows() if "goes unchecked" in r["Violation"])
    assert "|| exit" in unchecked["Preferred form"] and "set -euo pipefail" in unchecked["Preferred form"]
    assert "every command whose failure matters is checked" in _flat(_section("Do not flag"))


def test_bash_only_rows_never_reach_a_posix_script():
    """D8: `#!/bin/sh` owes no `pipefail`, `[[ ]]` or `local`; only a Bash feature used there is a defect.

    A row whose fix demands a Bash feature must scope its Violation to Bash.
    """
    for row in _rows():
        if re.search(r"pipefail|\[\[|`local", row["Preferred form"]) and "#!/bin/sh" not in row["Violation"]:
            violation = _flat(row["Violation"])
            assert "Bash script" in violation or "Bash function" in violation, row["Id"]
    posix = [r for r in _rows() if "#!/bin/sh" in r["Violation"]]
    assert len(posix) == 1 and _plain(posix[0]["Hazard"]) == "hazard"
    assert "`#!/bin/sh` script" in _flat(_section("Do not flag"))


def test_a_sourced_library_is_not_a_missing_shebang():
    """D8 as refined: Google says a library has a `.sh` extension and no shebang."""
    shebang = [r for r in _rows() if "SC2148" in r["Linter"]]
    assert len(shebang) == 1 and "shellcheck shell=" in shebang[0]["Violation"]
    assert "shellcheck shell=" in _section("Do not flag")


def test_rewriting_in_another_language_is_advisory_with_googles_threshold():
    """D10: length is a judgement the author makes, not a defect on a line."""
    advisory = _flat(_section("Advisory"))
    assert "A reviewer raises these; the author decides." in advisory
    assert "more than 100 lines long, or that uses non-straightforward control flow logic" in advisory
    for row in _rows():
        assert "100 lines" not in row["Violation"], row["Id"]


def test_a_linter_stands_a_row_down_only_where_its_rule_is_enabled():
    """D13 as refined: a project's CI running ShellCheck says nothing about an opt-in check."""
    do_not_flag = _flat(_section("Do not flag"))
    assert "enables that row's check" in do_not_flag
    assert "A row whose Linter cell reads none never stands down" in do_not_flag


def test_a_sourced_file_is_judged_by_its_callers_options():
    """Dogfood 2026-11-06: read alone, three sourced files drew false SH-1 and SH-2 items."""
    assert "A sourced file runs under its caller's options" in _flat(RULE.read_text())


def test_a_check_that_returns_failure_under_errexit_is_a_hazard_row():
    """Dogfood 2026-11-06: a health check's first `return 1` ended the script; ShellCheck was silent."""
    rows = [r for r in _rows() if "reports a result" in _flat(r["Violation"])]
    assert len(rows) == 1
    assert _plain(rows[0]["Hazard"]) == "hazard" and _plain(rows[0]["Linter"]) == "none"


def test_a_linter_stands_a_row_down_only_at_a_severity_ci_reports():
    """Dogfood 2026-11-06: SC2086 is info, so `shellcheck -S warning` in CI never reports SH-4."""
    assert "at the severity its CI reports" in _flat(_section("Do not flag"))


def test_bash_only_fixes_say_so():
    """Dogfood 2026-11-06: an array is no fix in a POSIX script, nor an EXIT trap in a sourced one."""
    forms = {_plain(r["Id"]): _flat(r["Preferred form"]) for r in _rows()}
    assert "in Bash, build a command line in an array" in forms["SH-4"]
    assert "in a sourced file, remove it on every return path" in forms["SH-8"]
    assert "grep" in forms["SH-2"]


def test_the_rule_leaves_injection_to_security_md():
    """D12: shell injection is CWE-78, filed once under security.md."""
    assert "`security.md`" in RULE.read_text() and "CWE-78" in RULE.read_text()
    for row in _rows():
        assert "inject" not in row["Violation"].lower(), row["Id"]


def test_review_code_names_the_rule_and_its_match():
    body = _flat(SKILL.read_text())
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/bash.md` (`.sh/.bash`, and an extensionless file whose first line is a shebang naming `sh` or `bash`)" in body
    assert "an extensionless file whose first line is a shebang naming `sh` or `bash`" in body.split("### Directory Path", 1)[1]


def test_review_code_files_a_row_by_id_and_promotes_a_hazard():
    """D4: Priority 7 by row id; a row the rule marks hazard is a Priority 1 item."""
    body = _flat(SKILL.read_text())
    assert "Where a language rule names its rows by id" in body
    assert "at Priority 1 where the row's Hazard column reads `hazard`" in body
    assert "The Hazard column alone decides" in body, "the idiom-promotion sentence would compete with it"
    assert "for a language row with an id, that id, e.g. `SH-2`" in body


def test_an_extensionless_script_is_a_file_argument():
    """Skill review 2026-11-06: `bin/healthcheck` matched no row of the Parse table."""
    assert "| Is a file, an extensionless script included | File path |" in SKILL.read_text()


def test_a_file_named_alone_meets_the_standards_its_gather_mode_would_hold_it_to():
    """Skill review 2026-11-06: `deploy.sh` named alone drew Priority 2-5 items a directory run would not."""
    assert "meets the same standards here as in a directory" in _flat(SKILL.read_text())


def test_a_stand_down_on_an_ungathered_file_reads_that_file():
    """Skill review 2026-11-06: the CI config and `.shellcheckrc` sit outside both gather modes."""
    body = _flat(SKILL.read_text())
    assert "`.shellcheckrc`, the script that sources this one — read it" in body


def test_readme_lists_the_rule():
    rules_line = next(line for line in README.read_text().splitlines() if line.startswith("- **Rules** —"))
    assert re.search(r"\bbash\b", rules_line)


def test_the_fixtures_are_found():
    """A glob that matches nothing passes every fixture test below silently."""
    assert FIXTURES


def test_every_expected_item_takes_its_id_fix_and_priority_from_its_row():
    """Checked against the id's own row, so an item cannot borrow another row's fix or tier."""
    rows = {_plain(r["Id"]): r for r in _rows()}
    for manifest in FIXTURES:
        want = json.loads(manifest.read_text())["min_items"]
        items = _items((manifest.parent / "expected-backlog.md").read_text())
        assert len(items) >= want, f"{manifest.parent.name} seeds {want} defects"
        for item in items:
            if _plain(_field(item, "Smell")) == "Advisory":
                continue
            row_id = _plain(_field(item, "Smell"))
            assert row_id in rows, f"{row_id} heads no always-flag row"
            fix = _plain(_field(item, "Refactoring"))
            assert _takes_the_form(fix, _plain(rows[row_id]["Preferred form"])), f"{row_id}: {fix!r}"
            hazard = _plain(rows[row_id]["Hazard"]) == "hazard"
            assert _field(item, "Priority") == ("1" if hazard else "7"), row_id
            assert _field(item, "Route") == ("report only" if hazard else "`/phil:refactor`"), row_id


def test_no_fixture_expects_an_item_on_a_decoy():
    for manifest in FIXTURES:
        backlog = (manifest.parent / "expected-backlog.md").read_text().split("\n## Backlog", 1)[1]
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy not in backlog, f"{manifest.parent.name}: {decoy} is a Do-not-flag case"


def test_every_decoy_is_in_the_fixture():
    """A decoy the fixture never holds proves nothing by its absence from the backlog."""
    for manifest in FIXTURES:
        corpus = "".join(p.read_text() for p in manifest.parent.rglob("*")
                         if p.is_file() and "__pycache__" not in p.parts
                         and p.name not in {"manifest.json", "expected.md", "expected-backlog.md"})
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy in corpus, f"{manifest.parent.name}: {decoy} is not in the fixture"
