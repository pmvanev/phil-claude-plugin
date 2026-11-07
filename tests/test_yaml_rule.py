"""`rules/yaml.md` and `review-code`, which applies it.

Every always-flag row carries the rule's own `YAML-n` id, a Hazard mark and the yamllint rule that
catches it where one exists. A reviewer copies the id and the row's Preferred form into the backlog.
This file holds the ids unique, keeps the consumer table that scopes the rows, keeps GitHub Actions'
`on:` and a Helm template out of the rule, and holds each fixture's expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it. Whether a reviewer flagged the seeded defect and left the decoy alone is model
judgement, which the fixture's `expected.md` carries and a human drives.

Written 2026-11-06, for the YAML rule (issue 79, slice 02).
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "yaml.md"
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
PIPELINES = REPO / "rules" / "ci-pipelines.md"
README = REPO / "README.md"
RESEARCH = "docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md"
FIXTURES = sorted((REPO / "skills" / "review-code" / "self-test").glob("*-yaml-*/manifest.json"))
COLUMNS = ("Id", "Violation", "Preferred form", "Hazard", "Linter", "Cite")


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _section(heading):
    return RULE.read_text().split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def _rows():
    return [dict(zip(COLUMNS, _cells(line)))
            for line in _section("Always-flag").splitlines() if line.startswith("| YAML-")]


def _row(phrase):
    matches = [r for r in _rows() if phrase in _flat(r["Violation"])]
    assert len(matches) == 1, phrase
    return matches[0]


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


def test_the_rule_matches_yaml_files_and_cites_its_research():
    head = RULE.read_text().split("---", 2)[1]
    for glob in ('"**/*.yml"', '"**/*.yaml"'):
        assert glob in head, glob
    assert RESEARCH in RULE.read_text()


def test_the_rule_states_its_hazard_and_tier_tests():
    """Addendum 2026-11-06: a row's tier follows a stated test, never the researcher's reading."""
    text = _flat(RULE.read_text())
    assert "A row is a hazard when a miss changes what a parser makes of the file" in text
    assert "A defect no source names stays Advisory" in text


def test_the_table_is_not_empty_and_every_row_is_whole():
    rows = _rows()
    assert len(rows) >= 5
    for row in rows:
        assert len(row) == len(COLUMNS) and all(row.values()), row.get("Id")


def test_the_ids_are_unique_and_run_without_a_gap():
    ids = [_plain(r["Id"]) for r in _rows()]
    assert all(re.fullmatch(r"YAML-\d+", i) for i in ids), ids
    assert [int(i.split("-")[1]) for i in ids] == list(range(1, len(ids) + 1)), ids


def test_every_row_has_a_hazard_mark_and_a_linter_cell():
    for row in _rows():
        assert _plain(row["Hazard"]) in {"hazard", "—"}, row["Id"]
        linter = _plain(row["Linter"])
        assert linter == "none" or linter.startswith("yamllint "), row["Id"]


def test_the_card_asks_for_booleans_octals_floats_and_duplicate_keys():
    """US-02: implicit booleans, octals and floats, duplicate keys, and a merge key that overrides."""
    assert "truthy" in _row("YAML 1.1 boolean")["Linter"]
    assert "octal-values" in _row("leading zero")["Linter"]
    assert _plain(_row("trailing zero")["Linter"]) == "none", "no yamllint rule catches `3.10`"
    dup = _row("same key twice")
    assert "`<<`" in dup["Violation"] and "forbid-duplicated-merge-keys" in dup["Linter"]


def test_the_consumer_table_scopes_the_boolean_and_base_60_rows():
    """D5 as revised: an unquoted `no` is a string to GitHub Actions and false to GitLab CI."""
    text = _flat(RULE.read_text())
    for consumer in ("GitHub Actions", "GitLab CI", "Kubernetes", "Helm values", "Ansible", "Compose"):
        assert consumer in text.split("## Principles", 1)[0], consumer
    assert "Where the review cannot name the consumer" in text
    assert "GitHub Actions" in _flat(_section("Do not flag")).split("`on:`", 1)[1]
    assert "Psych" in _row("base-60")["Violation"] and "PyYAML" in _row("base-60")["Violation"]


def test_psych_reads_a_leading_zero_clock_as_base_60():
    """Local parse 2026-11-06: Psych read `08:30` as 30600, though the Addendum said it stays a string."""
    assert "`08:30`" in _row("base-60")["Violation"]


def test_a_merge_key_override_is_advisory_and_a_second_merge_key_is_a_duplicate():
    """Addendum: the override turns on intent. Local parse: two `<<` keys merge in the reverse order."""
    advisory = _flat(_section("Advisory"))
    assert "own key" in advisory and "merged" in advisory
    assert "reverse" in _flat(RULE.read_text())


def test_parser_defined_keys_and_helm_templates_are_not_flagged():
    """D6 and D7."""
    do_not_flag = _flat(_section("Do not flag"))
    assert "`on:`" in do_not_flag
    assert "`templates/`" in do_not_flag
    assert "`templates/`" in _flat(RULE.read_text()).split("## Principles", 1)[0]


def test_a_number_meant_as_a_number_is_not_flagged():
    """Dogfood 2026-11-06: 329 trailing-zero values in the sibling repos, every one a number."""
    assert "A number meant as a number" in _flat(_section("Do not flag"))


def test_a_linter_stands_a_row_down_only_where_its_rule_is_enabled_at_a_reported_level():
    """D13: yamllint's `truthy` defaults to warning, which exits 0 without `--strict`."""
    do_not_flag = _flat(_section("Do not flag"))
    assert "enables that row's rule" in do_not_flag
    assert "--strict" in do_not_flag
    assert "A row whose Linter cell reads none never stands down" in do_not_flag


def test_the_rule_leaves_unsafe_loading_and_secrets_to_security_md():
    """D5's ownership: CWE-502 and a credential literal are `security.md`'s, filed once."""
    text = RULE.read_text()
    assert "`security.md`" in text and "CWE-502" in text and "CWE-798" in text
    assert "`ci-pipelines.md`" in text


def test_ci_pipelines_points_to_the_yaml_rule():
    assert "`yaml.md`" in PIPELINES.read_text().split("## Principles", 1)[0]


def test_review_code_names_the_rule_and_gathers_yaml_outside_helm_templates():
    body = _flat(SKILL.read_text())
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/yaml.md` (`.yml/.yaml`, outside a Helm chart's `templates/` — a `templates/` beside a `Chart.yaml`)" in body
    directory = body.split("### Directory Path", 1)[1].split("## Step 2", 1)[0]
    assert "`**/*.{yml,yaml}`" in directory
    assert "a YAML file against `yaml.md`" in directory
    changes = body.split("### `--changes`", 1)[1].split("### File Path", 1)[0]
    assert "a YAML file against `yaml.md`" in changes
    assert "`yaml.md`'s `YAML-n`" in body
    assert "`.yamllint`" in body


def test_readme_lists_the_rule():
    rules_line = next(line for line in README.read_text().splitlines() if line.startswith("- **Rules** —"))
    assert re.search(r"\byaml\b", rules_line)


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
            if smell == "Advisory" or smell.startswith("CWE-"):
                continue
            assert smell in rows, f"{smell} heads no always-flag row"
            fix = _plain(_field(item, "Refactoring"))
            assert _takes_the_form(fix, _plain(rows[smell]["Preferred form"])), f"{smell}: {fix!r}"
            hazard = _plain(rows[smell]["Hazard"]) == "hazard"
            assert _field(item, "Priority") == ("1" if hazard else "7"), smell
            assert _field(item, "Route") == ("report only" if hazard else "`/phil:refactor`"), smell


def test_a_defect_two_rules_describe_is_filed_once_under_security():
    """US-02: a credential literal with a leading zero is CWE-798, never also a YAML row."""
    for manifest in FIXTURES:
        items = _items((manifest.parent / "expected-backlog.md").read_text())
        secret = [i for i in items if _plain(_field(i, "Smell")) == "CWE-798"]
        assert len(secret) == 1, manifest.parent.name
        lines = (_field(secret[0], "File"), _field(secret[0], "Lines"))
        others = [i for i in items if (_field(i, "File"), _field(i, "Lines")) == lines]
        assert others == secret, "the secret's line is filed twice"


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
