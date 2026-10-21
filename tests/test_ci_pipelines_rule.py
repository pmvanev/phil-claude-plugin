"""`rules/ci-pipelines.md` and `review-ci`, which applies it.

Every always-flag row carries the rule's own `PIPE-n` id and cites the CI bad practice it rests on by
its Zampetti et al. id. A reviewer copies the id and the row's Preferred form into the backlog. A wrong
Zampetti id is a citation the reader trusts and cannot check, and a fixture whose expected item drifts
from its row pins nothing. This file holds the rule's Zampetti ids to the set checked against the paper,
and each fixture's expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it. Whether a reviewer flagged the seeded defect and left the look-alike alone is model
judgement, which each fixture's `expected.md` carries and a human drives.

Written 2026-10-21, when the rule landed.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "ci-pipelines.md"
SECURITY = REPO / "rules" / "security.md"
SKILL = REPO / "skills" / "review-ci" / "SKILL.md"
COMMAND = REPO / "commands" / "review-ci.md"
FIXTURES = sorted((REPO / "skills" / "review-ci" / "self-test").glob("*/manifest.json"))

# Checked against Tables 4-10 and the body text of the accepted manuscript of Zampetti et al., "An
# Empirical Characterization of Bad Practices in Continuous Integration" (EMSE 25, 2020), on
# 2026-10-21. An id joins this set only after the same check; that is V1 of
# docs/feature/ci-pipeline-standard/.
VERIFIED_ZAMPETTI = {
    "R10", "BP2", "BP6", "BP7", "BP8", "BP10", "BP11", "BP13", "BP16", "BP17", "BP25", "BP26",
    "BP28", "BP29", "BM1", "Q5", "Q10", "Q11", "D1",
}
ZAMPETTI_ID = r"\b(?:R|I|BP|BM|Q|D|C)\d{1,2}\b"


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _table_rows(text, start, end, header):
    section = text.split(start, 1)[1].split(end, 1)[0]
    return [_cells(line) for line in section.splitlines()
            if line.startswith("|") and not line.startswith("|---") and not line.startswith(header)]


def _pipe_rows():
    rows = []
    for id_, violation, preferred, cite in _table_rows(RULE.read_text(), "## Always-flag", "\n## ", "| Id"):
        rows.append({"Id": _plain(id_), "Violation": violation, "Preferred form": preferred, "Cite": cite})
    return rows


def _security_rows():
    rows = []
    for violation, preferred, cite in _table_rows(SECURITY.read_text(), "## Always-flag", "\n## Advisory", "| Violation"):
        rows.append({"Violation": violation, "Preferred form": preferred, "Cite": cite})
    return rows


def _takes_the_form(fix, form):
    """The row's form verbatim, alone or followed by ` — here: ` and this pipeline's change."""
    return fix == form or fix.startswith(form + " — here: ")


def _items(backlog):
    return re.split(r"^### \[C\d{3}\]", backlog, flags=re.M)[1:]


def _field(item, name):
    m = re.search(rf"- \*\*{name}\*\*: (.+)", item)
    assert m, f"an expected item has no {name} field"
    return m.group(1).strip()


def test_the_table_is_not_empty():
    """A table that parses to nothing passes every test below silently."""
    assert len(_pipe_rows()) >= 15


def test_every_row_has_a_unique_pipe_id():
    ids = [r["Id"] for r in _pipe_rows()]
    assert all(re.fullmatch(r"PIPE-\d+", i) for i in ids), ids
    assert len(ids) == len(set(ids)), "a PIPE id names two rows"


def test_every_row_cites_a_zampetti_id_or_a_named_source():
    for row in _pipe_rows():
        assert re.search(ZAMPETTI_ID, row["Cite"]) or "docs" in row["Cite"], row["Id"]


def test_every_zampetti_id_in_the_rule_was_checked_against_the_paper():
    cited = set(re.findall(r"Zampetti ((?:(?:R|I|BP|BM|Q|D|C)\d{1,2}(?:, )?)+)", RULE.read_text()))
    ids = {i for group in cited for i in group.split(", ") if i}
    assert ids, "the rule cites no Zampetti id at all"
    unchecked = sorted(ids - VERIFIED_ZAMPETTI)
    assert not unchecked, f"check these against the paper's tables, then add them here: {unchecked}"


def test_the_rule_dates_what_it_was_checked_against():
    assert "Checked against Zampetti et al. (EMSE 2020) on 2026-10-21" in RULE.read_text()


def test_the_rule_cites_security_rows_rather_than_restating_them():
    """Mutable tags and pull_request_target belong to security.md (D5)."""
    for row in _pipe_rows():
        for owned in ("pull_request_target", "mutable tag", "write-all", "without the lockfile", "npm install", "CWE-"):
            assert owned not in row["Violation"] + row["Cite"], f"{row['Id']} restates security.md: {owned}"
    assert "Supply-chain rows stay in `security.md`" in RULE.read_text()


def test_review_ci_reads_both_rules_and_names_findings_by_row():
    body = " ".join(SKILL.read_text().split())
    assert "rules/ci-pipelines.md` on every run" in body
    assert "Supply chain and build" in body
    assert "Name each finding by its row's id" in body
    assert "Copy the row's Preferred form verbatim" in body
    assert "Edit none of the reviewed files" in body


def test_review_ci_command_declares_its_grant():
    text = COMMAND.read_text()
    assert re.search(r"^mutates: true$", text, re.M), "review-ci writes its backlog, so it mutates"
    assert "skills/review-ci/SKILL.md" in text


def test_the_fixtures_are_found():
    """A glob that matches nothing passes both fixture tests below silently."""
    assert FIXTURES


def test_every_expected_item_takes_its_id_and_fix_from_one_row():
    """Checked against the id's own row, so an item cannot borrow another row's fix."""
    pipe = {r["Id"]: r for r in _pipe_rows()}
    security = _security_rows()
    for manifest in FIXTURES:
        want = json.loads(manifest.read_text())["min_items"]
        items = _items((manifest.parent / "expected-backlog.md").read_text())
        assert len(items) >= want, f"{manifest.parent.name} seeds {want} defects"
        for item in items:
            row_id = _plain(_field(item, "Row"))
            fix = _plain(_field(item, "Preferred form"))
            if row_id.startswith("PIPE-"):
                assert row_id in pipe, f"{row_id} heads no always-flag row"
                forms = [_plain(pipe[row_id]["Preferred form"])]
            else:
                owning = [r for r in security if re.search(rf"\b{re.escape(row_id)}\b", r["Cite"])]
                assert owning, f"{row_id} heads no security.md row"
                forms = [_plain(r["Preferred form"]) for r in owning]
            assert any(_takes_the_form(fix, f) for f in forms), f"{row_id}: {fix!r} is not its row's fix"


def test_no_fixture_expects_an_item_on_a_look_alike():
    for manifest in FIXTURES:
        backlog = (manifest.parent / "expected-backlog.md").read_text()
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy not in backlog, f"{manifest.parent.name}: {decoy} is a Do-not-flag case"


def test_every_look_alike_is_in_the_fixture():
    """A decoy the fixture never holds proves nothing by its absence from the backlog."""
    for manifest in FIXTURES:
        corpus = "".join(p.read_text() for p in manifest.parent.rglob("*")
                         if p.is_file() and p.name not in {"manifest.json", "expected.md", "expected-backlog.md"})
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy in corpus, f"{manifest.parent.name}: {decoy} is not in the fixture"


def test_one_edit_that_fixes_several_jobs_is_one_item():
    """The first drive filed PIPE-12 twice, at the job writing the cache and the job reading it."""
    rule = " ".join(RULE.read_text().split())
    skill = " ".join(SKILL.read_text().split())
    assert "One item per missing protection, filed where the edit goes" in rule
    assert "filed at the consumer" in rule
    assert "a defect between a producing and a consuming job is one item, at the consumer" in skill


def test_a_premise_in_an_unread_setting_files_nothing():
    """The first drive asked whether a merge queue was on, though nothing in the files suggested one."""
    rule = " ".join(RULE.read_text().split())
    skill = " ".join(SKILL.read_text().split())
    assert "Where a row's premise, not its guard, sits in an unread setting" in rule
    assert "list the setting under Not read and file nothing" in skill


def test_a_premise_a_read_file_states_makes_the_row_fire():
    """The modive dogfood filed no PIPE-6 although its own comment said auto-cancel was on."""
    rule = " ".join(RULE.read_text().split())
    assert "unless a file the review read states the premise" in rule


def test_one_value_repeated_in_a_file_is_one_item():
    """The modive dogfood filed six CWE-829 items for one `node:24-alpine` string."""
    rule = " ".join(RULE.read_text().split())
    assert "The same value at several sites in one file" in rule


def test_compare_to_guards_a_pipeline_with_no_push_event():
    """GitLab documents `compare_to` for exactly this case; an earlier wording dropped it."""
    pipe3 = next(r for r in _pipe_rows() if r["Id"] == "PIPE-3")
    assert "compare_to" in pipe3["Violation"] and "compare_to" in pipe3["Preferred form"]
