"""`rules/security.md` and `review-code`, which applies it.

Every always-flag row names a defect by CWE id, and a reviewer copies that id and the row's Preferred
form into the backlog. So a wrong id is a citation the reader trusts and cannot check, and a fixture
whose expected item drifts from its row pins nothing. This file holds the rule's ids to the set that
was resolved in MITRE's CWE database, and the fixture's expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it — whether a reviewer flagged the seeded defect and left the decoy alone is model
judgement, which `self-test/02-security-findings-cite-a-cwe/expected.md` carries and a human drives.

Written 2026-10-20, when the rule landed.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "security.md"
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
RC02 = REPO / "skills" / "review-code" / "self-test" / "02-security-findings-cite-a-cwe"

# Resolved through MITRE's CWE API (content version 4.20, 2026-04-30) on 2026-10-20. An id joins this
# set only after the same lookup; that is decision D5 of docs/feature/security-standards-rule/.
VERIFIED_CWE = {
    22, 77, 78, 79, 88, 89, 94, 95, 208, 209, 250, 256, 295, 297, 306, 307, 321, 323, 327, 328, 329,
    330, 338, 347, 352, 384, 427, 494, 502, 532, 601, 611, 614, 636, 639, 732, 770, 798, 829, 862,
    916, 918, 943, 1004, 1104, 1333, 1336, 1357, 1395, 1427,
}

# Functions in fixture 02 that look like a defect and are not one. A backlog naming any of them has
# flagged a Do-not-flag case.
DECOYS = ("cache_key", "display_order", "cards_sorted", "hash_password", "login", "password123")


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _always_flag_rows():
    text = RULE.read_text()
    section = text.split("## Always-flag", 1)[1].split("\n## Advisory", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Violation"):
            continue
        violation, preferred, cite = _cells(line)
        rows.append({"Violation": violation, "Preferred form": preferred, "Cite": cite})
    return rows


def _items(backlog):
    return re.split(r"^### \[R\d{3}\]", backlog, flags=re.M)[1:]


def _field(item, name):
    m = re.search(rf"- \*\*{name}\*\*: (.+)", item)
    assert m, f"an expected item has no {name} field"
    return m.group(1).strip()


def test_the_table_is_not_empty():
    """A table that parses to nothing passes every test below silently."""
    assert len(_always_flag_rows()) >= 30


def test_every_row_cites_a_cwe_id_or_a_nist_section():
    for row in _always_flag_rows():
        assert re.search(r"CWE-\d+|NIST 800-63B-4 §", row["Cite"]), row["Violation"]


def test_every_cwe_id_in_the_rule_was_resolved():
    cited = {int(n) for n in re.findall(r"CWE-(\d+)", RULE.read_text())}
    assert cited, "the rule cites no CWE id at all"
    unverified = sorted(cited - VERIFIED_CWE)
    assert not unverified, f"resolve these in MITRE's CWE database, then add them here: {unverified}"


def test_the_rule_dates_the_editions_it_was_checked_against():
    assert "Checked against CWE 4.20 (2026-04-30)" in RULE.read_text()


def test_review_code_reads_the_rule_on_every_run_and_names_findings_by_cwe():
    body = " ".join(SKILL.read_text().split())
    assert "rules/security.md` on every run" in body
    assert "Name each finding by the CWE id of its row" in body
    assert "Count it under Advisory, never under Priority 1" in body


def test_rc02_expects_every_security_item_to_take_its_id_and_fix_from_one_row():
    """Checked against the id's own row, so an item cannot borrow another row's fix."""
    rows = _always_flag_rows()
    items = [i for i in _items((RC02 / "expected-backlog.md").read_text()) if "**Smell**: CWE-" in i]
    assert len(items) >= 10, "fixture 02 seeds ten defects"
    for item in items:
        smell = _plain(_field(item, "Smell"))
        fix = _plain(_field(item, "Refactoring"))
        owning = [r for r in rows if re.search(rf"\b{re.escape(smell)}\b", r["Cite"])]
        assert owning, f"{smell} heads no always-flag row"
        assert any(fix == _plain(r["Preferred form"]) for r in owning), f"{smell}: {fix!r} is not its row's fix"
        assert _plain(_field(item, "Route")) == "report only", smell


def test_rc02_expects_no_item_on_a_decoy():
    backlog = (RC02 / "expected-backlog.md").read_text()
    for decoy in DECOYS:
        assert decoy not in backlog, f"{decoy} is a Do-not-flag case"
