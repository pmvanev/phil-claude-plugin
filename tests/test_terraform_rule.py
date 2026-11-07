"""`rules/terraform.md` and `review-code`, which applies it.

`terraform.md` holds the defects only Terraform has, each by its own `TF-n` id, and gives the Terraform
spelling of each `iac.md` row without copying the row: a review files those under the `IAC-n` id. This
file holds the ids unique, keeps the 0/1 `count` toggle and a lower-bound `required_version` out of the
table, checks the spelling table against `iac.md`, and holds each fixture's expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it. Whether a reviewer flagged the seeded defect and left the decoy alone is model
judgement, which the fixture's `expected.md` carries and a human drives.

Written 2026-11-06, for the Terraform rule (issue 79, slice 04).
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "terraform.md"
IAC = REPO / "rules" / "iac.md"
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
README = REPO / "README.md"
RESEARCH = "docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md"
FIXTURES = sorted((REPO / "skills" / "review-code" / "self-test").glob("*-terraform-*/manifest.json"))
COLUMNS = ("Id", "Violation", "Preferred form", "Hazard", "Linter", "Cite")


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _section(heading, text=None):
    return (text or RULE.read_text()).split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def _rows(text=None, prefix="TF"):
    return [dict(zip(COLUMNS, _cells(line)))
            for line in _section("Always-flag", text).splitlines() if line.startswith(f"| {prefix}-")]


def _row(phrase):
    matches = [r for r in _rows() if phrase in _flat(r["Violation"])]
    assert len(matches) == 1, phrase
    return matches[0]


def _flat(text):
    return " ".join(text.split())


def _takes_the_form(fix, form):
    return fix == form or fix.startswith(form + " — here: ")


def _items(backlog):
    return re.split(r"^### \[R\d{3}\]", backlog, flags=re.M)[1:]


def _field(item, name):
    m = re.search(rf"- \*\*{name}\*\*: (.+)", item)
    assert m, f"an expected item has no {name} field"
    return m.group(1).strip()


def test_the_rule_matches_terraform_files_and_cites_its_research():
    head = RULE.read_text().split("---", 2)[1]
    assert '"**/*.tf"' in head
    assert RESEARCH in RULE.read_text()


def test_the_rule_states_its_hazard_and_tier_tests():
    text = _flat(RULE.read_text())
    assert "A row is a hazard when a miss changes what a plan or an apply does" in text
    assert "A row with no hazard is an idiom: a cited source names its preferred form" in text


def test_the_table_is_whole_and_the_ids_run_without_a_gap():
    rows = _rows()
    assert len(rows) >= 5
    for row in rows:
        assert len(row) == len(COLUMNS) and all(row.values()), row.get("Id")
    ids = [_plain(r["Id"]) for r in rows]
    assert all(re.fullmatch(r"TF-\d+", i) for i in ids), ids
    assert [int(i.split("-")[1]) for i in ids] == list(range(1, len(ids) + 1)), ids


def test_every_row_has_a_hazard_mark_and_a_linter_cell():
    for row in _rows():
        assert _plain(row["Hazard"]) in {"hazard", "—"}, row["Id"]
        linter = _plain(row["Linter"])
        assert linter == "none" or "terraform_" in linter, row["Id"]


def test_count_over_a_collection_is_a_hazard_no_linter_catches():
    """D11: four measured `count = length(…)` sites; TFLint has no rule that reads `count`."""
    row = _row("count.index")
    assert _plain(row["Hazard"]) == "hazard" and _plain(row["Linter"]) == "none"
    assert "for_each" in row["Preferred form"] and "moved" in row["Preferred form"]
    assert "shifts" in row["Violation"], "Evidence check: later instances shift; not all are recreated"


def test_a_duplicate_map_key_is_a_hazard():
    """Gap 8 closed: Terraform keeps the last key and plan does not warn (HCSEC-2023-26)."""
    row = _row("duplicate key")
    assert _plain(row["Hazard"]) == "hazard" and "terraform_map_duplicate_keys" in row["Linter"]
    assert "HCSEC-2023-26" in row["Cite"]


def test_the_card_covers_typing_and_module_pins():
    assert "terraform_typed_variables" in _row("no `type`")["Linter"]
    assert _plain(_row("no `version`")["Hazard"]) == "hazard"


def test_the_toggle_and_a_lower_bound_required_version_are_not_flagged():
    """D11 and US-04: 78 toggles and 45 lower-bound constraints are documented practice."""
    do_not_flag = _flat(_section("Do not flag"))
    assert "? 1 : 0" in do_not_flag
    assert "required_version" in do_not_flag
    assert "child module" in do_not_flag


def test_the_rows_the_evidence_check_moved_are_advisory():
    """Addendum: `required_version` rests on "we also recommend"; `fmt` is a CI check; deprecated syntax is the linter's."""
    advisory = _flat(_section("Advisory"))
    for subject in ("required_version", "terraform fmt", "sensitive"):
        assert subject in advisory, subject
    for row in _rows():
        assert "required_version" not in row["Violation"], row["Id"]


def test_every_iac_row_has_a_terraform_spelling_and_none_is_copied():
    """Slice 04's learning hypothesis: terraform.md points to iac.md without restating it."""
    iac_ids = [_plain(r["Id"]) for r in _rows(IAC.read_text(), "IAC")]
    spelling = _section("The Terraform form of each IAC row")
    for iac_id in iac_ids:
        assert f"| {iac_id} |" in spelling, iac_id
    assert not any(line.startswith("| IAC-") for line in _section("Always-flag").splitlines())
    assert "under its `IAC-n` id" in _flat(spelling)


def test_a_linter_stands_a_row_down_only_where_its_rule_runs():
    do_not_flag = _flat(_section("Do not flag"))
    assert "enables the rule it names" in do_not_flag
    assert "--recursive" in do_not_flag
    assert "A row whose Linter cell reads none never stands down" in do_not_flag


def test_review_code_names_the_rule_beside_iac():
    body = _flat(SKILL.read_text())
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/terraform.md` (`.tf`)" in body
    assert "`terraform.md`'s `TF-n`" in body
    assert "A `.tf` file is checked against both `iac.md` and `terraform.md`" in body


def test_readme_lists_the_rule():
    rules_line = next(line for line in README.read_text().splitlines() if line.startswith("- **Rules** —"))
    assert re.search(r"\bterraform\b", rules_line)


def test_the_fixtures_are_found():
    assert FIXTURES


def test_every_expected_item_takes_its_id_fix_and_priority_from_its_row():
    rows = {_plain(r["Id"]): r for r in _rows()}
    for manifest in FIXTURES:
        want = json.loads(manifest.read_text())["min_items"]
        items = _items((manifest.parent / "expected-backlog.md").read_text())
        assert len(items) >= want, f"{manifest.parent.name} seeds {want} defects"
        for item in items:
            smell = _plain(_field(item, "Smell"))
            if not smell.startswith("TF-"):
                continue
            assert smell in rows, f"{smell} heads no always-flag row"
            fix = _plain(_field(item, "Refactoring"))
            assert _takes_the_form(fix, _plain(rows[smell]["Preferred form"])), f"{smell}: {fix!r}"
            hazard = _plain(rows[smell]["Hazard"]) == "hazard"
            assert _field(item, "Priority") == ("1" if hazard else "7"), smell
            assert _field(item, "Route") == "report only", f"{smell}: no test suite checks a plan"


def test_no_fixture_expects_an_item_on_a_decoy():
    for manifest in FIXTURES:
        backlog = (manifest.parent / "expected-backlog.md").read_text().split("\n## Backlog", 1)[1]
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy not in backlog, f"{manifest.parent.name}: {decoy} is a Do-not-flag case"


def test_every_decoy_is_in_the_fixture():
    for manifest in FIXTURES:
        corpus = "".join(str(p.relative_to(manifest.parent)) + "\n" + p.read_text()
                         for p in manifest.parent.rglob("*")
                         if p.is_file() and "__pycache__" not in p.parts
                         and p.name not in {"manifest.json", "expected.md", "expected-backlog.md"})
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy in corpus, f"{manifest.parent.name}: {decoy} is not in the fixture"
