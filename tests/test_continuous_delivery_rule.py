"""`rules/continuous-delivery.md` against the MinimumCD.org minimums it cites.

Four rules have named MinimumCD.org as a source since the initial commit on 2026-03-05. Only
`continuous-delivery.md` held any of its content, and it stated fewer than half the site's minimums.
A source the reader trusts and cannot find in the text is a false citation. This file holds each
minimum, as checked against minimumcd.org and its practice pages on 2026-10-22, to a line in the
rule, and keeps the citation off rules that carry none of the site's content.

**What this cannot check.** It verifies the rule *states* each minimum, not that any skill *applies*
it; `scripts/check-rule-reachability.py` proves only that something names the rule.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "continuous-delivery.md"

# One line of the rule per MinimumCD minimum, keyed by the site's own wording.
MINIMUMS = {
    "The application pipeline is the only way to deploy to any environment":
        "The pipeline is the only way to deploy, to any environment",
    "The pipeline decides the releasability of changes, its verdict is definitive":
        "no human overrides its verdict",
    "Artifacts created by the pipeline always meet the organization's definition of deployable":
        "definition of deployable",
    "Immutable artifact (no human changes after commit)":
        "no human changes an artifact after the pipeline builds it",
    "All feature work stops when the main pipeline is red":
        "nothing merges but the fix or its revert",
    "Production-like test environment":
        "Test in production-like environments",
    "Rollback on-demand":
        "Roll back on demand",
    "Application configuration deploys with artifact":
        "Ship application configuration with the artifact",
    "Work integrates to the trunk at a minimum daily":
        "Integrate code at least daily",
    "Work has automated testing before merge to trunk":
        "before it merges to trunk",
    "Work is tested with other work automatically on merge":
        "again with everyone else's work after it merges",
    "New work does not break delivered work":
        "Delivered work keeps working when new work lands",
    "If branches from the trunk are used: they originate from, re-integrate to, and are removed":
        "starts from trunk, merges back to it, and is deleted after the merge",
}


def test_the_rule_states_every_minimumcd_minimum():
    rule = RULE.read_text()
    missing = [minimum for minimum, line in MINIMUMS.items() if line not in rule]
    assert not missing, missing


def test_rollback_and_the_schema_rule_agree():
    """The rule said "roll forward, not back", where MinimumCD makes rollback the default."""
    rule = RULE.read_text()
    assert "Roll forward, not back" not in rule
    assert "expand, then contract" in rule, "a schema change keeps the previous release runnable"


def test_the_production_like_anti_pattern_reads_as_one():
    rule = RULE.read_text()
    assert "Deploying only to production-like environments late" not in rule


def test_only_rules_holding_its_content_cite_minimumcd():
    for name in ("coding", "testing", "architecture"):
        assert "MinimumCD" not in (REPO / "rules" / f"{name}.md").read_text(), name
    assert "MinimumCD.org" in RULE.read_text()
