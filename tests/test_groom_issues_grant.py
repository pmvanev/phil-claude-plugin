"""Pins the grant/rule coupling that issue #30 was about — site 12 of the sites checklist.

`skills/groom-issues/self-test/README.md` § *The sites checklist* records the defect: a rule can be
perfectly written, reviewed and fixtured, and still unexecutable, because the command's grant does not
hold the call it requires. `scripts/check-readonly-commands.py` cannot see that — it verifies a
`mutates: false` command grants nothing dangerous, never that a `mutates: true` command grants what its
skill demands.

The decomposed-feature class was that defect for three weeks: its evidence table ranked a real
parent/child edge first, sufficient on its own to offer an irreversible consolidation, while the command
held `gh issue list` and nothing else. `parent` and `subIssues` are GraphQL-only. So the class reported
CLEAN on every board whose slice cards were properly parented — the population it exists for.

Nothing failed, which is why this file exists rather than a note.

The suite under `skills/groom-issues/self-test/` has no driver (issue #42), so these are the only
executable assertions behind the fixtures amended and added for #30.
"""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCAN = REPO / "commands" / "groom-issues.md"
SET = REPO / "commands" / "groom-set.md"
SKILL = REPO / "skills" / "groom-issues" / "SKILL.md"
FIXTURES = REPO / "skills" / "groom-issues" / "self-test"


def frontmatter(path):
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, f"{path.name} has no frontmatter"
    return match.group(1)


def grants(path):
    line = next(l for l in frontmatter(path).splitlines() if l.startswith("allowed-tools:"))
    return [g.strip() for g in line.split(":", 1)[1].split(",")]


# --- the call the rule requires --------------------------------------------------------------

def test_the_scan_holds_the_call_its_strongest_evidence_tier_needs():
    """The motivating input. This assertion fails on every commit before 2026-09-04."""
    assert "Bash(gh api graphql:*)" in grants(SCAN), (
        "the decomposed-feature class ranks a real parent/child edge as its strongest evidence, and "
        "`parent`/`subIssues` are GraphQL-only — without this grant the class reports clean on exactly "
        "the boards it was written for"
    )


def test_the_scan_declares_it_can_mutate_because_the_grant_permits_it():
    """`gh api graphql` accepts a mutation document, so `mutates: false` beside it would be false.

    The declaration is a claim about the GRANT, never about intent — `CLAUDE.md`, *Every command
    declares whether it can mutate*. `resume` set the precedent on 2026-08-17: `mutates: true` while
    writing nothing.
    """
    assert "mutates: true" in frontmatter(SCAN)


def test_the_scan_still_cannot_touch_a_file():
    """Half the guarantee stayed mechanical, and the split is the whole point of the trade."""
    for tool in ("Write", "Edit", "NotebookEdit"):
        assert tool not in grants(SCAN), f"{tool} would remove the half that is still enforced"


# --- the promise that replaced the enforcement ------------------------------------------------

def test_the_forge_half_of_the_guarantee_is_carried_in_prose():
    """Nothing in the tool list now forbids a forge write, so the never-do list must."""
    skill = SKILL.read_text()
    assert "mutation" in skill and "gh api graphql" in skill
    assert re.search(r"never\s+`?mutation|`mutation`\s+document", skill, re.I), (
        "the skill must forbid a mutation document in as many words — it is the only thing that does"
    )
    assert "query" in SCAN.read_text()


@pytest.mark.parametrize("retired", [
    "not `gh api`, which would permit",
    "This command is **read-only**, and enforced rather than declared.",
])
def test_the_refuted_sentences_are_gone(retired):
    """Assert the old claim ABSENT, not merely superseded.

    Same discipline as `test_check_readonly_commands.py`: a refuted sentence left standing gets
    re-derived by the next reader, who then "restores" the enforcement by removing the grant and
    silently re-breaks the class.
    """
    assert retired not in SCAN.read_text()


# --- the deliberate non-widening ---------------------------------------------------------------

def test_the_resolver_did_not_get_the_same_grant():
    """The asymmetry is the decision, not an oversight.

    The scan only reports, so a promise not to mutate costs it nothing it was going to do. `groom-set`
    exists to make irreversible writes, and the identical grant beside `gh issue close` is a materially
    larger promise. `REFUSE-UNGRANTED` still covers its rollup read.
    """
    assert "Bash(gh api graphql:*)" not in grants(SET)
    assert "REFUSE-UNGRANTED" in SKILL.read_text()


# --- the fixture the card asked for -------------------------------------------------------------

def test_a_fixture_pins_the_board_that_used_to_report_clean():
    fixture = FIXTURES / "45-parent-edge-is-read"
    assert (fixture / "manifest.json").is_file()
    assert (fixture / "expected.md").is_file()


def test_that_fixture_isolates_the_read_by_carrying_no_other_evidence():
    """A fixture with tier-2 or tier-3 evidence alongside would pass without the read happening.

    Same trap as fixtures 28/29 in `nwave-issue-board`: a case where two rules agree pins neither.
    """
    import json
    manifest = json.loads((FIXTURES / "45-parent-edge-is-read" / "manifest.json").read_text())
    assert manifest["evidence"] == [
        "real parent/child edge: #71, #72, #73, #74 are sub-issues of #70"
    ], "the parent edge must be the only tie, or the fixture tests the class and not the read"
    assert len(manifest["absent_evidence"]) == 3


def test_a_surfaced_candidate_forbids_a_clean_terminal():
    """`SURFACE-CANDIDATE` is additive and never stands alone.

    Fixture 45 exposed the gap: a board with no body defects and four properly parented slice cards
    satisfies `REPORT-CLEAN` by the letter of the vocabulary while misreporting itself. Defects between
    issues are defects. The rule is stated in SKILL.md § *Decision outcomes*; this pins it.
    """
    import json
    manifest = json.loads((FIXTURES / "45-parent-edge-is-read" / "manifest.json").read_text())
    assert manifest["expected_decision"] == ["REPORT-DEFECT", "SURFACE-CANDIDATE"]
    assert "`REPORT-CLEAN` is unavailable on any run that surfaced a candidate" in SKILL.read_text()


def test_a_github_scan_makes_two_calls_not_one():
    """The parent-edge read is a second call, and four pre-existing manifests said otherwise.

    A GitHub scan making one call now is one that skipped the parent-edge check — which is the exact
    board state issue #30 was about, re-encoded as a fixture that would pass.
    """
    import json
    for name in ("01-scan-and-report", "03-clean-board",
                 "09-unevaluated-is-not-clean", "10-one-sided-chain"):
        manifest = json.loads((FIXTURES / name / "manifest.json").read_text())
        assert manifest["forge"] == "github"
        assert manifest["scan"]["calls_made"] == 2, name


def test_the_counter_fixture_still_reports_unevaluated_after_the_grant():
    """The grant fixed the read and not the oracle, and 39 is where that separation is pinned.

    Issue #30's body treated the two rules as one problem — *"two rules in one skill now depend on a
    GraphQL read nothing in the family can make"*. True of the read; wrong about what reading it buys.
    The completion counter counts CLOSED children, not built ones, and no grant changes that.
    """
    import json
    manifest = json.loads(
        (FIXTURES / "39-rollup-counts-closed-not-done" / "manifest.json").read_text()
    )
    assert manifest["expected_decision"] == ["REPORT-UNEVALUATED"]
    assert "did NOT make the CHECK possible" in manifest["grant_note"]
    assert "reads" not in manifest, (
        "the grant is authorised for the parent edge alone; a `reads` key here would have the fixture "
        "instruct a call the skill's never-do list forbids"
    )
