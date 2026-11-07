"""`rules/iac.md` and `review-code`, which applies it.

Every always-flag row carries the rule's own `IAC-n` id, a Hazard mark and a Linter cell. The rule
states each row in terms no single tool owns, so a Terraform file and a later tool's file meet the same
row; the tool's spelling belongs in the tool's rule. This file holds the ids unique, keeps tool syntax
out of the rows, keeps `continuous-delivery.md`'s bullets pointing here, and holds each fixture's
expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it. Whether a reviewer flagged the seeded defect and left the decoy alone is model
judgement, which the fixture's `expected.md` carries and a human drives.

Written 2026-11-06, for the IaC rule (issue 79, slice 03).
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "iac.md"
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
CD = REPO / "rules" / "continuous-delivery.md"
README = REPO / "README.md"
RESEARCH = "docs/research/iac/iac-terraform-bash-yaml-canonical-sources.md"
FIXTURES = sorted((REPO / "skills" / "review-code" / "self-test").glob("*-iac-*/manifest.json"))
COLUMNS = ("Id", "Violation", "Preferred form", "Hazard", "Linter", "Cite")
TOOL_SYNTAX = ("terraform", ".tf", "tfstate", ".hcl", "~>", "required_providers", "count", "for_each",
               "workspace", "pulumi", "cloudformation")


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _section(heading):
    return RULE.read_text().split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def _rows():
    return [dict(zip(COLUMNS, _cells(line)))
            for line in _section("Always-flag").splitlines() if line.startswith("| IAC-")]


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
    assert "A row is a hazard when a miss changes what an apply does" in text
    assert "A row with no hazard is an idiom: a cited source names its preferred form" in text
    assert "A defect no source names stays Advisory" in text


def test_the_table_is_whole_and_the_ids_run_without_a_gap():
    rows = _rows()
    assert len(rows) >= 5
    for row in rows:
        assert len(row) == len(COLUMNS) and all(row.values()), row.get("Id")
    ids = [_plain(r["Id"]) for r in rows]
    assert all(re.fullmatch(r"IAC-\d+", i) for i in ids), ids
    assert [int(i.split("-")[1]) for i in ids] == list(range(1, len(ids) + 1)), ids


def test_every_row_has_a_hazard_mark_and_a_linter_cell():
    for row in _rows():
        assert _plain(row["Hazard"]) in {"hazard", "—"}, row["Id"]
        assert _plain(row["Linter"]), row["Id"]


def test_no_row_names_a_tool():
    """Slice 03's learning hypothesis: a row a reader needs one tool's knowledge to judge moves to that tool's rule."""
    for row in _rows():
        text = (row["Violation"] + " " + row["Preferred form"]).lower()
        for word in TOOL_SYNTAX:
            assert not re.search(rf"(?<![a-z]){re.escape(word)}(?![a-z])", text), f"{row['Id']} names {word!r}"


def test_the_card_covers_state_drift_pinning_secrets_modules_and_environments():
    """The card's Covers list, each row where the evidence check left it."""
    assert _plain(_row("committed to version control")["Hazard"]) == "hazard"
    assert _plain(_row("share one state")["Hazard"]) == "hazard"
    assert _plain(_row("lock")["Hazard"]) == "hazard"
    assert _plain(_row("from below only")["Hazard"]) == "—"
    assert "reusable module" in _row("configures its own")["Violation"]
    assert _plain(_row("repeats another root")["Hazard"]) == "—"
    advisory = _flat(_section("Advisory"))
    for subject in ("locking", "drift", "reviewed", "imperative"):
        assert subject in advisory, subject


def test_the_principles_quote_morris_from_his_own_pages():
    """Evidence check 2026-11-06: the book is unread, so quote only what his posts say."""
    principles = _flat(_section("Principles"))
    assert "manage necessary variation between environments with parameters" in principles
    assert "fed into the pipeline" in principles


def test_secrets_stay_with_security_md():
    text = RULE.read_text()
    assert "`security.md`" in text and "CWE-798" in text and "CWE-312" in text
    for row in _rows():
        assert "secret" not in row["Violation"].lower(), row["Id"]


def test_lower_bound_tool_constraints_and_module_locks_are_not_flagged():
    do_not_flag = _flat(_section("Do not flag"))
    assert "lower bound" in do_not_flag
    assert "never applied as a root" in do_not_flag


def test_continuous_delivery_keeps_its_bullets_and_points_here():
    section = CD.read_text().split("### Infrastructure as Code", 1)[1].split("\n---", 1)[0]
    for bullet in ("Treat infrastructure like application code", "Provision environments automatically",
                   "Never make manual changes to production", "Environments are disposable and reproducible"):
        assert bullet in section, bullet
    assert "`iac.md`" in section


def test_review_code_names_the_rule_and_gathers_terraform_on_every_run():
    body = _flat(SKILL.read_text())
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/iac.md` (`.tf`" in body
    directory = body.split("### Directory Path", 1)[1].split("## Step 2", 1)[0]
    assert "`**/*.tf`" in directory.split("where the review", 1)[0], "Terraform is gathered on every run"
    assert "an infrastructure file against `iac.md`" in directory
    assert "`iac.md`'s `IAC-n`" in body


def test_readme_lists_the_rule():
    rules_line = next(line for line in README.read_text().splitlines() if line.startswith("- **Rules** —"))
    assert re.search(r"\biac\b", rules_line)


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
            if smell == "Advisory" or not smell.startswith("IAC-"):
                continue
            assert smell in rows, f"{smell} heads no always-flag row"
            fix = _plain(_field(item, "Refactoring"))
            assert _takes_the_form(fix, _plain(rows[smell]["Preferred form"])), f"{smell}: {fix!r}"
            hazard = _plain(rows[smell]["Hazard"]) == "hazard"
            assert _field(item, "Priority") == ("1" if hazard else "7"), smell
            assert _field(item, "Route") == ("report only" if hazard else "`/phil:refactor`"), smell


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
