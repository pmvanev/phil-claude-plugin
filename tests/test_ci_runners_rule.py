"""`rules/ci-runners.md` and `review-ci`, which applies it to runner configuration.

Every always-flag row carries the rule's own `RUN-n` id. A security row cites the CWE that MITRE's
vulnerability-mapping guidance allows for it; a row about autoscaler semantics cites the source it was
read from, at the revision the fleet runs. A wrong CWE is a citation the reader trusts and cannot check,
and an autoscaler claim read from `main` may not hold for the pinned build.

**What this cannot check.** Whether a review files the seeded items is model judgement, which the
fixture's `expected.md` carries and a human drives.

Written 2026-10-21, with slice 05 of `docs/feature/ci-pipeline-standard/`.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "ci-runners.md"
PIPELINES = REPO / "rules" / "ci-pipelines.md"
SKILL = REPO / "skills" / "review-ci" / "SKILL.md"
FIXTURE = REPO / "skills" / "review-ci" / "self-test" / "03-runner-config"

# Checked against MITRE CWE 4.20 on 2026-10-21, each by its vulnerability-mapping usage: 653 and 250 and
# 266 ALLOWED; 522 and 863 ALLOWED-WITH-REVIEW. 668 and 269 were the research's candidates and are
# DISCOURAGED. An id joins this set only after the same check; that is V2 of the feature.
VERIFIED_CWE = {"CWE-653", "CWE-250", "CWE-266", "CWE-522", "CWE-863"}
TASKSCALER_REVISION = "1f87885729aa"


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _rows(text=None):
    text = text or RULE.read_text()
    section = text.split("## Always-flag", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if line.startswith("| RUN-"):
            id_, violation, preferred, cite = _cells(line)
            rows.append({"Id": id_, "Violation": violation, "Preferred form": preferred, "Cite": cite})
    return rows


def _row(id_):
    return next(r for r in _rows() if r["Id"] == id_)


def test_the_rule_has_both_halves():
    text = RULE.read_text()
    for heading in ("## Principles", "## Always-flag", "## Advisory", "## Do not flag", "## Sources and Synthesis"):
        assert f"\n{heading}" in text, heading
    assert len(_rows()) >= 12


def test_every_row_has_a_unique_run_id():
    ids = [r["Id"] for r in _rows()]
    assert all(re.fullmatch(r"RUN-(\d+|T\d)", i) for i in ids), ids
    assert len(ids) == len(set(ids))


def test_a_bare_retry_stays_with_the_pipeline_rule():
    """The research's RUN-11 restated PIPE-10; the id stays unused rather than reassigned."""
    assert "RUN-11" not in [r["Id"] for r in _rows()]
    assert "RUN-11 is unused" in RULE.read_text()


def test_every_cwe_the_rule_cites_was_checked_against_mitre():
    cited = set(re.findall(r"CWE-\d+", " ".join(r["Cite"] for r in _rows())))
    assert cited, "no runner row cites a CWE"
    assert not cited - VERIFIED_CWE, f"check these against MITRE first: {sorted(cited - VERIFIED_CWE)}"
    for discouraged in ("CWE-668", "CWE-269"):
        assert discouraged not in cited, f"MITRE discourages {discouraged} for mapping"


def test_every_security_row_cites_a_cwe_and_every_other_row_its_source():
    """The Isolation and Credentials rows are security defects and cite a CWE; RUN-12, RUN-13 and the
    fleet-answer rows are not, and cite the source that decides them."""
    for row in _rows():
        number = row["Id"].split("-")[1]
        if number.isdigit() and int(number) <= 10:
            assert re.search(r"CWE-\d+", row["Cite"]), row["Id"]
        else:
            assert re.search(r"taskscaler|deprecation|drift", row["Cite"]), row["Id"]


def test_the_scale_factor_row_cites_the_revision_the_fleet_runs():
    row = _row("RUN-12")
    assert TASKSCALER_REVISION in row["Cite"] and "capacity.go" in row["Cite"]
    assert "Checked against MITRE CWE 4.20 on 2026-10-21" in RULE.read_text()


def test_the_socket_row_turns_on_reuse_not_on_the_socket():
    """On a one-job machine the VM is the boundary; the research's case rests on it."""
    assert "max_use_count" in _row("RUN-1")["Violation"]
    do_not = RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0]
    assert "one-job machine" in do_not


def test_fleet_answers_name_what_they_read():
    assert "live system" in _row("RUN-T1")["Violation"]
    assert "no longer runs on" in _row("RUN-T2")["Violation"]
    assert "this rule's own extension" in _row("RUN-T2")["Cite"]


def test_the_two_rules_point_at_each_other():
    assert "ci-runners.md" in PIPELINES.read_text()
    assert "ci-pipelines.md" in RULE.read_text()


def test_review_ci_gathers_runner_configuration_and_applies_the_rule():
    skill = " ".join(SKILL.read_text().split())
    assert "rules/ci-runners.md" in skill
    assert "config.toml" in skill
    assert "which platform is live" in skill


def test_the_runner_fixture_expects_items_that_take_their_fix_from_their_row():
    manifest = json.loads((FIXTURE / "manifest.json").read_text())
    backlog = (FIXTURE / "expected-backlog.md").read_text().split("\n## Backlog", 1)[1]
    items = re.split(r"^### \[C\d{3}\]", backlog, flags=re.M)[1:]
    assert len(items) >= manifest["min_items"]
    run_rows = {r["Id"]: r for r in _rows()}
    seen = set()
    for item in items:
        row_id = re.search(r"- \*\*Row\*\*: (.+)", item).group(1).strip().strip("`")
        fix = re.sub(r"[*`]", "", re.search(r"- \*\*Preferred form\*\*: (.+)", item).group(1)).strip()
        seen.add(row_id)
        if row_id.startswith("RUN-"):
            form = re.sub(r"[*`]", "", run_rows[row_id]["Preferred form"]).strip()
            assert fix == form or fix.startswith(form + " — here: "), f"{row_id}: {fix!r}"
    for seeded in ("RUN-1", "RUN-12", "RUN-4", "PIPE-10"):
        assert seeded in seen, seeded
    for decoy in manifest["decoys"]:
        assert decoy not in backlog, decoy


# Lessons from the dogfood over runbooks' runners (2026-10-21).

def test_metadata_is_flagged_only_where_jobs_should_not_hold_the_role():
    """The role pools exist so their jobs use the role; RUN-5 fired on them as written."""
    assert "not meant to hold" in _row("RUN-5")["Violation"]


def test_a_recorded_decision_that_accepts_a_risk_makes_a_question():
    """runbooks' deploying.md records the shared deploy role's reach as accepted, for now."""
    assert "accepts the risk" in " ".join(RULE.read_text().split())


def test_a_document_that_misstates_what_a_setting_does_is_rt1():
    """runbooks' README promised 'one ready per busy instance' from a scale_factor that never acts."""
    assert "what a setting does" in _row("RUN-T1")["Violation"]


def test_the_review_says_when_it_did_not_read_the_default_branch():
    assert "not the default branch" in " ".join(SKILL.read_text().split())
