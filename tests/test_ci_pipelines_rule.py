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
RUNNERS = REPO / "rules" / "ci-runners.md"
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


def _runner_rows():
    section = RUNNERS.read_text().split("## Always-flag", 1)[1].split("\n## ", 1)[0]
    return {_plain(c[0]): {"Preferred form": c[2]} for c in
            (_cells(l) for l in section.splitlines() if l.startswith("| RUN-"))}


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
            if row_id == "Advisory":
                assert fix == "none — the author decides", f"an Advisory item proposes a fix: {fix!r}"
                continue
            if row_id.startswith("PIPE-"):
                assert row_id in pipe, f"{row_id} heads no always-flag row"
                forms = [_plain(pipe[row_id]["Preferred form"])]
            elif row_id.startswith("RUN-"):
                runner = _runner_rows()
                assert row_id in runner, f"{row_id} heads no ci-runners.md row"
                forms = [_plain(runner[row_id]["Preferred form"])]
            else:
                owning = [r for r in security if re.search(rf"\b{re.escape(row_id)}\b", r["Cite"])]
                assert owning, f"{row_id} heads no security.md row"
                forms = [_plain(r["Preferred form"]) for r in owning]
            assert any(_takes_the_form(fix, f) for f in forms), f"{row_id}: {fix!r} is not its row's fix"


def test_no_fixture_expects_an_item_on_a_look_alike():
    """Only the items count: the trigger matrix names every job, look-alikes included."""
    for manifest in FIXTURES:
        backlog = (manifest.parent / "expected-backlog.md").read_text().split("\n## Backlog", 1)[1]
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


# Slice 02: the declared policy, the skip-needs-a-gate rows and the trigger matrix.
TEST_ARCHITECTURE = REPO / "rules" / "test-architecture.md"
SOURCES = ("MR", "docs-only MR", "main push", "docs-only main", "schedule", "tag", "web or API")


def _row(id_):
    return next(r for r in _pipe_rows() if r["Id"] == id_)


def test_the_rule_has_both_halves_and_a_declared_policy():
    text = RULE.read_text()
    for heading in ("## Principles", "## The declared policy", "## Always-flag", "## Advisory", "## Do not flag"):
        assert f"\n{heading}" in text, heading
    assert text.index("## Principles") < text.index("## Always-flag") < text.index("## Advisory") < text.index("## Do not flag")


def test_the_policy_block_names_its_fields():
    section = RULE.read_text().split("## The declared policy", 1)[1].split("\n---\n", 1)[0]
    assert "## CI policy" in section, "the block's heading in a project's CLAUDE.md"
    for field in ("Pipelines", "Docs-only paths", "MR", "Main", "Schedule", "Merge", "Secret scan", "Andon", "Notify"):
        assert f"**{field}**" in section, field


def test_a_policy_row_fires_only_against_a_declared_field():
    """A reviewer that flags a project's choice as a defect trains the reader to skip it (D6)."""
    rule = " ".join(RULE.read_text().split())
    assert "fires only against a field the project declared" in rule
    departure = next(r for r in _pipe_rows() if "declared policy" in r["Violation"])
    assert "trigger matrix" in departure["Violation"]


def test_every_skip_names_its_gate():
    """Mutation ran only in MR pipelines, work merged to main directly, and it ran nowhere for two days."""
    violations = {r["Id"]: r["Violation"] for r in _pipe_rows()}
    forced = [i for i, v in violations.items() if "lockfile" in v and "CI configuration" in v]
    assert forced, "no row forces a full run when the selector's own inputs change"
    assert any("mutation" in v and "schedule" in v for v in violations.values()), "no row asks for a full mutation run"
    assert "less than the full test suite" in _row("PIPE-2")["Violation"], "main may run a change-scoped subset"


def test_docs_only_is_an_allow_list():
    """`changes:` matches when ANY path matches, so `changes: [docs/**] when: never` skips a code change too (D9)."""
    violations = " ".join(r["Violation"] for r in _pipe_rows())
    assert "when: never" in violations and "any changed path" in violations
    assert "no list names" in violations, "a new directory must not silently skip every test"


def test_a_schedule_never_starts_a_deploy_on_its_own():
    row = next(r for r in _pipe_rows() if "deploy" in r["Violation"] and "schedule" in r["Violation"]
               and r["Id"] != "PIPE-3")
    assert "$CI_PIPELINE_SOURCE" in row["Preferred form"] and "github.event_name" in row["Preferred form"]


def test_a_need_on_a_job_rules_can_exclude_is_optional():
    row = next(r for r in _pipe_rows() if "needs:" in r["Violation"])
    assert "optional: true" in row["Preferred form"]


def test_a_bare_variable_inside_a_compound_rule_is_flagged():
    """beatrix pipeline 641: `$ROLLBACK_TAG && …` matched with the tag empty. GitLab's docs say it should
    not; its evaluator (`lexeme/and.rb`) returns Ruby's `"" && x`, and Ruby's empty string is true."""
    row = next(r for r in _pipe_rows() if "&&" in r["Violation"])
    assert '!= ""' in row["Preferred form"] and "!= null" in row["Preferred form"]
    assert "lexeme/and.rb" in row["Cite"], "the docs contradict the behaviour; cite the evaluator"


def test_review_ci_writes_the_trigger_matrix():
    skill = " ".join(SKILL.read_text().split())
    assert "## Trigger matrix" in SKILL.read_text()
    for source in SOURCES:
        assert source in skill, source
    assert "## CI policy" in skill, "the review reads the declared policy"


def test_an_advisory_bullet_is_a_question_for_the_author():
    skill = " ".join(SKILL.read_text().split())
    assert "An Advisory bullet is a question" in skill


def test_test_architecture_points_at_the_pipeline_rule():
    """Suite speed is test-architecture's; pipeline speed is ci-pipelines' (D11, D17)."""
    assert "ci-pipelines.md" in TEST_ARCHITECTURE.read_text()


def test_a_matrix_fixture_expects_every_source():
    matrix_fixtures = [m for m in FIXTURES if json.loads(m.read_text()).get("matrix")]
    assert matrix_fixtures, "no fixture pins the trigger matrix"
    for manifest in matrix_fixtures:
        expected = (manifest.parent / "expected-backlog.md").read_text()
        header = next(line for line in expected.splitlines() if line.startswith("| Job"))
        assert [c.strip() for c in header.strip("|").split("|")][1:] == list(SOURCES), header


# Lessons from fixture 02's first drive, the two plugin-dev reviews and the beatrix dogfood.

def test_the_matrix_shows_a_refused_pipeline_on_its_own_row():
    """One `needs:` defect refuses every MR pipeline; the first drive marked fourteen job cells for it."""
    skill = " ".join(SKILL.read_text().split())
    assert "`(pipeline)`" in skill and "as if the pipeline were created" in skill
    for manifest in (m for m in FIXTURES if json.loads(m.read_text()).get("matrix")):
        lines = (manifest.parent / "expected-backlog.md").read_text().splitlines()
        first = lines[lines.index(next(l for l in lines if l.startswith("| Job"))) + 2]
        assert first.startswith("| (pipeline) |"), first


def test_a_job_that_exits_early_satisfies_a_field_that_excludes_it():
    """PIPE-21's own GitLab fix is a step that exits early, so that cell is no departure."""
    assert "satisfies a field that excludes it" in " ".join(RULE.read_text().split())


def test_inherited_rules_are_replaced_not_joined():
    """`default:` cannot hold `rules:`, and a job's own `rules:` replaces those from `extends:`."""
    skill = " ".join(SKILL.read_text().split())
    assert "its own `rules:` if it has them, otherwise those from `extends:`" in skill
    assert "each `!reference` inlined where it stands" in skill


def test_speed_is_never_must_fix_and_is_raised_only_with_durations():
    """The skill said speed is filed never, while the rule listed speed bullets under Advisory."""
    skill = " ".join(SKILL.read_text().split())
    rule = " ".join(RULE.read_text().split())
    assert "Speed as a must-fix item" in skill
    assert "only with job durations in hand" in rule


def test_a_recorded_decision_turns_a_policy_departure_into_a_question():
    """beatrix records mutation on demand only, after three VM crashes; a pasted default policy contradicted it."""
    rule = " ".join(RULE.read_text().split())
    skill = " ".join(SKILL.read_text().split())
    assert "a recorded decision contradicts" in rule
    assert "recorded decisions" in skill


def test_a_field_no_job_carries_out_is_one_item_at_the_field():
    """beatrix runs no mutation job at all, so PIPE-24 had no cell to mark."""
    assert "A field no job carries out" in " ".join(RULE.read_text().split())


def test_path_lists_fail_closed_when_no_test_runs():
    """In beatrix two non-test jobs run on every change, which kept PIPE-22 silent."""
    assert "no test job runs" in _row("PIPE-22")["Violation"]


def test_changes_on_a_no_push_source_is_not_flagged_where_the_project_means_it():
    """beatrix runs every job in a hand-run main pipeline on purpose, and a test pins it."""
    do_not = RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0]
    assert "means to run there" in do_not


def test_pipe_17_names_what_a_deploy_job_is_and_spares_a_declared_scheduled_deploy():
    row = _row("PIPE-17")
    assert "`environment:`" in row["Violation"]
    assert "Schedule field" in row["Violation"]


# The andon: a red main is the team's, not its author's. Both forges tell only the person who started
# the run, so a broken main went unheard until someone else's MR failed on it (2026-10-22).

def test_a_red_main_pulls_the_andon_cord():
    rule = " ".join(RULE.read_text().split())
    assert "### A red main pulls the andon cord" in RULE.read_text()
    assert "who hears it" in rule.split("This rule owns", 1)[1].split(".", 1)[0]
    assert "stopping the line on a red main" in rule.split("Neighbouring rules", 1)[1].split(";", 1)[0], \
        "the principle hands the response to continuous-delivery.md, so the scope must say it owns it"
    row = _row("PIPE-25")
    assert "Andon field" in row["Violation"], "a policy row fires only against a declared field"
    assert "at most the person who started the run" in row["Violation"]
    for form in ("if: failure()", "workflow_run", "notify_only_broken_pipelines: true", "branches_to_be_notified: default"):
        assert form in row["Preferred form"], form


def test_a_workflow_run_andon_ignores_pull_request_runs():
    """workflow_run fires for a pull request's runs too, and a fork's branch may be named main; the
    plugin validator found the first form pulling the cord on a failed MR (2026-10-22)."""
    form = _row("PIPE-25")["Preferred form"]
    assert "branches: [<default branch>]" in form
    assert "github.event.workflow_run.event == 'push'" in form


def test_an_andon_in_a_setting_or_an_app_is_a_question():
    """GitLab's Pipeline status emails and a chat app's subscription are both invisible to the file."""
    policy = " ".join(RULE.read_text().split("## The declared policy", 1)[1].split("\n---\n", 1)[0].split())
    assert "Pipeline status emails" in policy and "a chat app's subscription" in policy


def test_an_undeclared_andon_is_advisory_and_an_mr_failure_is_its_authors():
    advisory = RULE.read_text().split("## Advisory", 1)[1].split("\n## ", 1)[0]
    do_not = RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0]
    assert "A red main only its author hears about" in advisory
    assert "An MR pipeline's failure that reaches only its author" in do_not
    assert "An andon job's own write grant" in do_not


def test_review_ci_reads_a_job_that_runs_on_failure_and_lists_notification_settings():
    skill = " ".join(SKILL.read_text().split())
    assert "`on failure`" in skill
    assert "notification integrations" in skill


def test_the_backlog_template_offers_the_on_failure_cell_and_notes_what_starts_it():
    """The skill review found the template an agent copies missing the new value (2026-10-22)."""
    text = SKILL.read_text()
    template = next(l for l in text.splitlines() if l.startswith("| {job} |"))
    assert "on failure" in template
    assert "note the jobs whose failure starts it" in " ".join(text.split())


def test_a_github_pipe_25_is_must_fix_only_where_a_workflow_must_carry_the_channel():
    """A chat app's subscription can pull the cord unseen; only an issue or a webhook needs a job."""
    policy = " ".join(RULE.read_text().split("## The declared policy", 1)[1].split("\n---\n", 1)[0].split())
    assert "On GitHub, PIPE-25 is must-fix where the field names an issue or a webhook" in policy
    severities = {}
    for m in FIXTURES:
        backlog = (m.parent / "expected-backlog.md").read_text()
        for item in _items(backlog):
            if _plain(_field(item, "Row")) == "PIPE-25":
                severities[m.parent.name] = _field(item, "Severity")
    assert "must-fix" in severities.values() and "question" in severities.values(), severities


def test_a_github_fixture_expects_pipe_25():
    """Every other fixture is GitLab, where the andon is a setting and the row can only ask."""
    hits = [m for m in FIXTURES if list(m.parent.glob(".github/workflows/*.yml"))
            and "- **Row**: PIPE-25" in (m.parent / "expected-backlog.md").read_text()]
    assert hits, "no GitHub fixture files a missing andon"


# The author tier: a failure or a warning reaches the person who started the pipeline. GitLab sends
# pipeline email only at the Watch or Custom level, GitHub only to users who subscribed, and a job
# allowed to fail passes on both, so by default nobody hears either (docs read 2026-10-22).

def test_the_rule_does_not_claim_a_forge_tells_anyone_by_default():
    rule = " ".join(RULE.read_text().split())
    assert "Each forge tells one person" not in rule
    assert "Watch or Custom" in rule and "subscribed" in rule


def test_a_failure_or_a_warning_names_the_person_who_started_the_pipeline():
    assert "### A failure or a warning names whoever started the pipeline" in RULE.read_text()
    row = _row("PIPE-26")
    assert "Notify field" in row["Violation"], "a policy row fires only against a declared field"
    assert "allow_failure: true" in row["Violation"] and "continue-on-error: true" in row["Violation"]
    for form in ("when: on_failure", ".post", "if: failure()", "./scripts/ci/run.sh inform"):
        assert form in row["Preferred form"], form


def test_an_undeclared_notify_is_advisory_and_its_grants_are_not_flagged():
    advisory = RULE.read_text().split("## Advisory", 1)[1].split("\n## ", 1)[0]
    do_not = RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0]
    assert "A failure or a warning that names nobody" in advisory
    assert "`pull-requests: write`" in do_not and "`NOTIFY_TOKEN`" in do_not


def test_a_gitlab_fixture_expects_pipe_26_and_clears_pipe_9():
    hits = [m for m in FIXTURES if (m.parent / ".gitlab-ci.yml").exists()
            and "- **Row**: PIPE-26" in (m.parent / "expected-backlog.md").read_text()]
    assert hits, "no GitLab fixture files a silent warning"
    for m in hits:
        assert "- **Row**: PIPE-9" not in (m.parent / "expected-backlog.md").read_text(), \
            "a job that gates nothing and says so is PIPE-9's Do-not-flag case"



def test_pipe_9s_do_not_flag_clears_only_pipe_9():
    """The second skill review: the bullet cleared fixture 06's only item, read literally (2026-10-22)."""
    do_not = " ".join(RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0].split())
    assert "That clears PIPE-9 only: under a declared Notify field it is PIPE-26" in do_not


def test_pipe_26_keeps_the_schedule_and_the_andon_out_of_its_github_form():
    """A schedule has no author; and two last jobs that each need every other job form a cycle."""
    form = _row("PIPE-26")["Preferred form"]
    assert "github.event_name != 'schedule'" in form
    assert "`when: on_failure` as its last rule, after one that skips the schedule" in form, \
        "the fixture 06 drive found the GitLab form silent on the schedule its GitHub form skips"
    assert "every job but the andon" in form


def test_review_ci_lists_ci_variables_as_unread_and_reads_head_by_a_granted_verb():
    skill = " ".join(SKILL.read_text().split())
    assert "CI/CD variables, such as a token a job reads" in skill
    assert "git rev-parse --verify HEAD" in skill and "`git rev-parse HEAD`" not in skill


DEPLOY_ROWS = ("PIPE-27", "PIPE-28", "PIPE-29", "PIPE-30", "PIPE-31")


def test_a_deploy_waits_for_every_gate_and_ships_the_one_tested_artifact():
    """continuous-delivery.md states MinimumCD's single path, final verdict and immutable artifact, and
    this rule deferred to it, so review-ci checked none of them (2026-10-22)."""
    rows = {r["Id"]: r for r in _pipe_rows()}
    assert "`always()`" in rows["PIPE-27"]["Violation"] and "`when: always`" in rows["PIPE-27"]["Violation"]
    p27 = rows["PIPE-27"]["Violation"]
    assert "directly or through the jobs they need" in p27, "`needs:` reach through chains on both forges"
    assert "one GitHub workflow run with the `workflow_run` runs it starts" in p27, "the pipeline a gate must be in"
    assert "whose `needs:` do not reach every gating job that checks what it ships" in p27, \
        "a dev deploy that later gates run against is the pipeline's shape, not a defect (fixture 02)"
    assert "a status function other than `success()`" in p27, "`success() || failure()` overrides it too"
    assert "a GitLab deploy, or a job its `needs:` pass through, marked `when: always`" in p27, \
        "GitHub skips down the whole chain; GitLab's `on_success` reads only the needed jobs"
    assert "was not a `pull_request` run" in p27, "`branches:` matches a fork's branch named main"
    assert "A job that stops or tears down an environment is no deploy" in p27
    p31 = rows["PIPE-31"]["Violation"]
    assert "A deploy no gate guards" in p31 and "of an artifact no gated run built" in p31, \
        "MinimumCD's single path: a hotfix workflow beside the gating one (second review, 2026-10-22)"
    assert "is PIPE-9" in p27 and "PIPE-17 or PIPE-28" in p27, "a tolerated or never-run gate has its own row"
    assert "`workflow_run`" in p27 and "`workflow_run`" in rows["PIPE-28"]["Violation"]
    for row_id in ("PIPE-29", "PIPE-30"):
        assert "A deploy job that builds is PIPE-11" in rows[row_id]["Violation"], row_id
    assert "`SKIP_TESTS`" in rows["PIPE-28"]["Violation"]
    assert "the deploy still runs" in rows["PIPE-28"]["Violation"], "a GitHub deploy that needs the test skips with it"
    assert "once per environment" in rows["PIPE-29"]["Violation"]
    assert "digest" in rows["PIPE-30"]["Preferred form"]
    for row_id in DEPLOY_ROWS:
        assert "MinimumCD" in rows[row_id]["Cite"], row_id
    rule = RULE.read_text()
    assert "MinimumCD.org" in rule.split("Guidelines drawn from", 1)[1].split("\n\n", 1)[0], "the header names every source"
    assert "MinimumCD.org's practice pages on 2026-10-22" in rule


def test_a_rollback_and_a_runtime_matrix_are_not_deploy_defects():
    do_not = " ".join(RULE.read_text().split("## Do not flag", 1)[1].split("\n## ", 1)[0].split())
    assert "A rollback that redeploys an earlier artifact without rerunning the tests" in do_not
    assert "A test matrix over runtimes or platforms" in do_not
    assert "A third-party action or image pinned by a mutable tag" in do_not
    assert "The pipeline's own image deployed by a tag that can move is PIPE-30" in do_not
    assert "It clears PIPE-7, not PIPE-27" in do_not, "a manual production start still waits for every gate"
    assert "It clears PIPE-27, PIPE-28 and PIPE-31" in do_not, "fixture 02's rollback skips the tests by design"
    assert "A promotion that reads its digest, at promote time, from the record a gated run wrote" in do_not
    assert "(a third-party action or image pinned by a mutable tag)" in RULE.read_text()


def test_rollback_and_a_production_like_environment_are_questions():
    advisory = " ".join(RULE.read_text().split("## Advisory", 1)[1].split("\n## ", 1)[0].split())
    assert "**A deployable with no rollback the files show**" in advisory
    assert "**A deploy to production that no earlier environment precedes.**" in advisory


def test_a_fixture_expects_every_deploy_row_beside_its_look_alikes():
    fixture = REPO / "skills" / "review-ci" / "self-test" / "07-deploy-what-passed"
    backlog = (fixture / "expected-backlog.md").read_text()
    rows = [_plain(_field(item, "Row")) for item in _items(backlog)]
    assert sorted(r for r in rows if r.startswith("PIPE-")) == list(DEPLOY_ROWS), rows
    assert "Cite**: ci-pipelines.md — Advisory: A deployable with no rollback the files show" in backlog
    decoys = json.loads((fixture / "manifest.json").read_text())["decoys"]
    for decoy in ("rollback.yml", "python-version", "DIGEST: ${{ needs.build.outputs.digest }}"):
        assert decoy in decoys, decoy
    assert "hotfix.yml" in backlog, "the hotfix path is PIPE-31's seed"
    assert "`07-deploy-what-passed/`" in (SKILL.parent / "self-test" / "README.md").read_text()
    assert "07-deploy-what-passed" in SKILL.read_text()
