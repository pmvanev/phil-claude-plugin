"""`rules/lambda-web-app-speed.md` and `review-code`, which applies it.

Every always-flag row carries the rule's own `LWS-n` id, and a reviewer copies the id and the row's
Preferred form into the backlog. A fixture whose expected item drifts from its row pins nothing, and a
GovCloud row whose availability fact went stale flags a design the partition now allows. This file
holds the ids unique, the GovCloud rows dated, the review's read of the rule scoped, and each fixture's
expected items to their rows.

**What this cannot check.** It verifies a fixture *expects* the right item, not that a review
*produces* it. Whether a reviewer flagged the seeded defect and left the look-alike alone is model
judgement, which the fixture's `expected.md` carries and a human drives.

Written 2026-10-26, when the rule's reviewer half landed (issue 59, slice 01).
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE = REPO / "rules" / "lambda-web-app-speed.md"
CODING = REPO / "rules" / "coding.md"
SKILL = REPO / "skills" / "review-code" / "SKILL.md"
FIXTURES = sorted((REPO / "skills" / "review-code" / "self-test").glob("*-load-time-*/manifest.json"))


def _plain(cell):
    return re.sub(r"[*`]", "", cell).strip()


def _cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def _rows():
    section = RULE.read_text().split("## Always-flag", 1)[1].split("\n## ", 1)[0]
    return [dict(zip(("Id", "Violation", "Preferred form", "Cite"), _cells(line)))
            for line in section.splitlines() if line.startswith("| LWS-")]


def _do_not_flag():
    return RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0]


def _takes_the_form(fix, form):
    """The row's form verbatim, alone or followed by ` — here: ` and this code's change."""
    return fix == form or fix.startswith(form + " — here: ")


def _items(backlog):
    return re.split(r"^### \[R\d{3}\]", backlog, flags=re.M)[1:]


def _field(item, name):
    m = re.search(rf"- \*\*{name}\*\*: (.+)", item)
    assert m, f"an expected item has no {name} field"
    return m.group(1).strip()


def test_the_table_is_not_empty():
    """A table that parses to nothing passes every test below silently."""
    assert len(_rows()) >= 15


def test_every_row_has_a_unique_lws_id_and_a_source():
    ids = [_plain(r["Id"]) for r in _rows()]
    assert all(re.fullmatch(r"LWS-\d+", i) for i in ids), ids
    assert len(ids) == len(set(ids)), "an LWS id names two rows"
    for row in _rows():
        assert row["Cite"], f"{row['Id']} cites no source"


def test_every_govcloud_row_dates_the_page_it_read():
    """Partition availability changes; a row that cites it says when it was true (V1)."""
    for row in _rows():
        if "GovCloud" in row["Violation"]:
            assert re.search(r"GovCloud \(US\) User Guide, Lambda, read \d{4}-\d{2}-\d{2}", row["Cite"]), row["Id"]


def test_the_cloudfront_row_fires_only_where_cloudfront_exists():
    """D10: a row that flags the only design a partition allows teaches readers to skip it."""
    routing = [r for r in _rows() if "Lambda origin" in r["Violation"]]
    assert len(routing) == 1
    assert "partition offers CloudFront" in routing[0]["Violation"]
    assert "partition offers no CloudFront" in _do_not_flag()


def test_keeping_warm_is_never_a_defect_by_its_absence():
    """D9: provisioned concurrency, SnapStart and a heartbeat are priced choices."""
    assert "No provisioned concurrency, SnapStart or heartbeat" in _do_not_flag()
    for row in _rows():
        assert not re.search(r"\bno (provisioned concurrency|SnapStart|ping|heartbeat)", row["Violation"], re.I), row["Id"]


def test_bytecode_is_flagged_only_when_built_for_another_python():
    """D11: shipping .pyc and shipping none are both legitimate; a mismatched version is not."""
    assert "A package without `.pyc` files" in _do_not_flag()
    bytecode = [r for r in _rows() if ".pyc" in r["Violation"]]
    assert len(bytecode) == 1 and "other than the function's `runtime`" in bytecode[0]["Violation"]


def test_the_rule_cites_coding_md_rather_than_restating_it():
    """D6: pooling and batching stay in coding.md; the rule names the Lambda form only."""
    text = RULE.read_text()
    assert "`coding.md` §8" in text and "§15" in text
    for row in _rows():
        assert "pool size" not in row["Violation"].lower(), f"{row['Id']} restates coding.md §8"
    assert "lambda-web-app-speed.md" in CODING.read_text(), "coding.md §8 points at the Lambda form"


def test_review_code_reads_the_rule_only_in_a_repository_that_deploys_to_lambda():
    """D4: the rule fires on nothing else, so reading it everywhere would only cost the review."""
    body = " ".join(SKILL.read_text().split())
    assert "Where the repository deploys to AWS Lambda" in body
    assert "rules/lambda-web-app-speed.md` before Priority 1, and apply it to every file the review gathers" in body
    assert "Skip it in any other repository" in body
    for glob in ("*.tf", "template.y*ml", "serverless.y*ml", ".size-limit*"):
        assert glob in body, f"review-code never gathers {glob}"


def test_build_dependency_and_ci_files_meet_the_rule_too():
    """LWS-5, LWS-6 and LWS-17 fire in files the review once checked against security.md alone."""
    body = " ".join(SKILL.read_text().split())
    assert "security.md` alone" not in body
    assert body.count("Check those against `security.md` and, where the review read it, `lambda-web-app-speed.md`") == 2


def test_an_unsettled_fact_is_an_advisory_question_naming_the_row():
    body = " ".join(SKILL.read_text().split())
    assert "a Rationale naming the `LWS-n` row and the unread source" in body


def test_review_code_names_load_time_findings_by_row_and_counts_them_apart():
    body = " ".join(SKILL.read_text().split())
    assert "Name each finding by its row's `LWS-n` id" in body
    assert "under the `LWS-n` id" in body, "a coding.md overlap would be filed twice"
    assert "**Load time (`LWS-n` rows)**" in body
    assert "Advisory and load-time items excluded" in body


def test_the_fixtures_are_found():
    """A glob that matches nothing passes every fixture test below silently."""
    assert FIXTURES


def test_every_expected_item_takes_its_id_and_fix_from_its_row():
    """Checked against the id's own row, so an item cannot borrow another row's fix."""
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
            assert _field(item, "Route") == "report only", row_id
            assert _field(item, "Priority") == "1", row_id


def test_no_fixture_expects_an_item_on_a_look_alike():
    for manifest in FIXTURES:
        backlog = (manifest.parent / "expected-backlog.md").read_text().split("\n## Backlog", 1)[1]
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy not in backlog, f"{manifest.parent.name}: {decoy} is a Do-not-flag case"


def test_every_look_alike_is_in_the_fixture():
    """A look-alike the fixture never holds proves nothing by its absence from the backlog."""
    for manifest in FIXTURES:
        # The wiring test runs each fixture's suite, which leaves bytecode behind.
        corpus = "".join(p.read_text() for p in manifest.parent.rglob("*")
                         if p.is_file() and "__pycache__" not in p.parts
                         and p.name not in {"manifest.json", "expected.md", "expected-backlog.md"})
        for decoy in json.loads(manifest.read_text())["decoys"]:
            assert decoy in corpus, f"{manifest.parent.name}: {decoy} is not in the fixture"


def _section(heading):
    return RULE.read_text().split(f"## {heading}", 1)[1].split("\n## ", 1)[0]


def test_the_principles_cover_ranking_stopping_init_warmth_assets_bundle_and_views():
    """Slice 04: the Principles half is whole once each part of the path has one."""
    principles = " ".join(_section("Principles").split())
    for phrase in ("Rank fixes by the time they save", "Stop at the target", "Hold INIT to a budget",
                   "Buy warmth on purpose", "Serve what never changes from the edge",
                   "Send the first route's code alone", "Show a view's cached data at once"):
        assert phrase in principles, phrase


def test_the_advisory_list_holds_the_judgement_calls_and_cites_each():
    advisory = " ".join(_section("Advisory").split())
    assert "A reviewer raises these; the author decides." in advisory
    for phrase in ("compiled bytecode", "50 MB", "background request", "Lambda Web Functions",
                   "proves the deployment"):
        assert phrase in advisory, phrase


def test_a_background_request_as_activity_cites_the_nist_text_read_for_v3():
    advisory = " ".join(_section("Advisory").split())
    assert "SP 800-63B-4" in advisory and "read 2026-10-26" in advisory
    assert "presence of an access token" in advisory


def test_no_principle_or_advisory_line_is_an_always_flag_row():
    """D8: a judgement call filed as a defect borrows authority it has not earned."""
    for heading in ("Principles", "Advisory"):
        assert "| LWS-" not in _section(heading), heading


def test_every_advisory_bullet_names_its_source():
    bullets = [b for b in _section("Advisory").split("\n- ")[1:]]
    assert len(bullets) >= 5
    for bullet in bullets:
        assert "*Source:" in bullet, bullet[:60]


def _advisory_titles():
    return [b.split("**")[1].rstrip(".") for b in _section("Advisory").split("\n- ")[1:]]


def test_every_expected_advisory_item_is_a_question_naming_its_bullet():
    titles = _advisory_titles()
    expected = [i for m in FIXTURES for i in _items((m.parent / "expected-backlog.md").read_text())
                if _plain(_field(i, "Smell")) == "Advisory"]
    assert expected, "no fixture expects an Advisory question"
    for manifest in FIXTURES:
        items = [i for i in _items((manifest.parent / "expected-backlog.md").read_text())
                 if _plain(_field(i, "Smell")) == "Advisory"]
        for item in items:
            assert _field(item, "Refactoring") == "none — the author decides"
            assert _field(item, "Route") == "report only" and _field(item, "Priority") == "1"
            assert any(title in _field(item, "Rationale") for title in titles), _field(item, "Rationale")


def test_review_code_raises_the_rules_advisory_bullets_only_where_a_file_shows_the_subject():
    body = " ".join(SKILL.read_text().split())
    assert "Raise the rule's Advisory bullets" in body and "only where a file the review read shows" in body


def test_every_always_flag_row_is_planted_in_some_fixture():
    """A row no fixture plants can drift from what a review files, and no drive would notice."""
    planted = {_plain(_field(i, "Smell")) for m in FIXTURES
               for i in _items((m.parent / "expected-backlog.md").read_text())}
    missing = sorted({_plain(r["Id"]) for r in _rows()} - planted, key=lambda i: int(i.split("-")[1]))
    assert not missing, f"no fixture plants {missing}"
