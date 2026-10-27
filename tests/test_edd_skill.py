"""`skills/edd/SKILL.md`: the evidence gate's loops must end, and its dispatch must reach its agent.

Found 2026-10-13, all predating that day's hardening:
- A developer rejecting reused evidence as irrelevant went through the reject branch, which rebuilds via
  the engine; fixture 03 says it commissions fresh evidence only.
- A reject looped back through the engine with no exit, and DOCUMENT ran only "on completion", so a run
  stopped over a standing reject recorded nothing.
- A producer reporting that it could not execute was neither narration nor evidence, and the only branch
  re-commissioned it forever.
- The dispatch named `agents/edd-evidence-producer`, not the Agent type, and passed none of the inputs the
  agent's contract expects.
- "The plugin's evolution convention" names a directory a user's repository does not have.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "edd" / "SKILL.md"


def _flat():
    return " ".join(SKILL.read_text().split())


def test_an_irrelevance_reject_commissions_evidence_and_rebuilds_nothing():
    assert "commission fresh evidence and rebuild nothing" in _flat()


def test_the_developer_can_stop_over_a_standing_reject_and_the_trail_records_it():
    body = _flat()
    assert "The developer may stop instead" in body
    assert "a run stopped over a standing reject writes the trail too" in body


def test_a_producer_that_cannot_execute_goes_to_the_developer():
    assert "cannot produce executed evidence" in _flat()
    assert "report it to the developer rather than re-commissioning" in _flat()


def test_the_dispatch_names_the_agent_type_and_its_inputs():
    body = _flat()
    assert "`phil:edd-evidence-producer`" in body
    assert "`expectation`, its `classification`, the `target` and any `context`" in body


def test_the_evolution_summary_has_a_home_in_any_repo():
    body = _flat()
    assert "the plugin's evolution convention" not in body
    assert "creating `docs/evolution/` if absent" in body


# --- edd-article-alignment slice 01 (2026-10-27): capture covers the ground, and every expectation
# gets executed evidence unless the developer opts the checkable ones out. Source: Laforgia,
# "Expectation-Driven Development"; decisions D1, D4, D5, D6 in
# docs/feature/edd-article-alignment/feature-delta.md.

AGENT = REPO / "agents" / "edd-evidence-producer.md"


def _section(heading):
    """The flattened text of the `## <heading>` section, up to the next `## ` heading."""
    text = SKILL.read_text()
    start = text.index(f"\n## {heading}")
    end = text.find("\n## ", start + 1)
    return " ".join(text[start:end if end != -1 else None].split())


def test_capture_checks_the_article_coverage_categories():
    capture = _section("CAPTURE")
    for category in ("happy path", "past edge cases", "non-functional requirements", "must not happen"):
        assert category in capture, category


def test_capture_sizes_each_expectation_to_one_breath_and_orders_by_risk():
    capture = _section("CAPTURE")
    assert "more than one breath" in capture
    assert "order the list by risk" in capture.lower()


def test_capture_applies_the_writing_standard_to_composed_words_only():
    capture = _section("CAPTURE")
    assert "rules/writing.md" in capture
    assert "`you wrote`" in capture
    assert "`composed`" in capture


def test_the_opt_out_covers_checkable_expectations_only_and_the_record_names_them():
    opt_out = _section("OPT-OUT")
    assert "Ask once" in opt_out
    assert "A qualitative expectation cannot be opted out" in opt_out
    assert "names every expectation trusted to the tests" in opt_out


def test_the_off_ramp_exit_is_retired():
    body = _flat()
    assert "## OFF-RAMP" not in SKILL.read_text()
    assert "phil:edd would only add ceremony" not in body


def test_checkable_evidence_is_the_scenario_run_not_a_suite_summary():
    gate = _section("EVIDENCE")
    assert "its inputs and the verbatim output" in gate
    assert '"all tests passed"' in gate


def test_an_expectation_not_executable_in_the_loop_goes_to_the_developer():
    assert "not executable in the loop" in _section("CLASSIFY")
    assert "spot-check it by hand or stop" in _section("EVIDENCE")


def test_the_trail_is_written_for_every_run_that_built():
    document = _section("DOCUMENT")
    assert "every run that built" in document
    assert "≥1 adjudicated" not in document


def test_the_producer_gathers_evidence_for_checkable_expectations_too():
    agent = " ".join(AGENT.read_text().split())
    assert "for one qualitative expectation" not in agent
    assert "a checkable expectation" in agent
    assert "a test runner's pass count is not evidence" in agent


# --- slice 01 review findings (skill-reviewer, plugin-validator, fixture driver; 2026-10-27).
# Each closes a path the first draft left open: the not-executable route ran after the producer was
# dispatched, had no guard and no verdict; reused engine evidence came from the builder; "irrelevant"
# could only be a reject; narration re-commissioned without end; an approval test's first read
# vanished under the opt-out; and split or edited lines lost their provenance.

def test_evidence_skips_opted_out_rows_and_routes_not_executable_before_any_dispatch():
    gate = _section("EVIDENCE")
    assert "Skip every expectation trusted to the tests" in gate
    assert gate.index("not executable in the loop") < gate.index("Reuse if it already exists")


def test_not_executable_in_the_loop_needs_a_developer_confirmed_blocker():
    assert "the developer confirms the concrete blocker" in _section("CLASSIFY")


def test_a_producer_that_cannot_run_is_split_by_cause():
    gate = _section("EVIDENCE")
    assert "the build is missing" in gate
    assert "the environment cannot run it" in gate


def test_a_spot_check_ends_in_a_verdict_and_a_stop_is_not_done():
    adjudicate = _section("ADJUDICATE")
    assert "A hand spot-check ends in a verdict too" in adjudicate
    assert "A stop over an unproven expectation is reported not done" in adjudicate


def test_reused_evidence_is_re_run_by_the_producer_not_taken_from_the_builder():
    assert "re-run its reproduce command" in _section("EVIDENCE")


def test_irrelevant_evidence_is_not_a_reject():
    assert "is not a reject" in _section("ADJUDICATE")


def test_re_commissioning_narration_is_bounded():
    assert "a second narrated return" in _section("EVIDENCE")


def test_an_approval_test_row_cannot_be_opted_out():
    assert "An expectation an approval test pins cannot be opted out" in _section("OPT-OUT")


def test_a_red_oracle_blocks_done():
    assert "A red oracle blocks done" in _section("BUILD")


def test_past_edge_cases_are_never_invented():
    assert "never invent a past bug" in _section("CAPTURE")


def test_a_split_or_edited_line_keeps_its_provenance():
    capture = _section("CAPTURE")
    assert "keep the original `you wrote` line" in capture
    assert "`you edited`" in capture


def test_the_standards_are_read_not_only_named():
    body = _flat()
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in body
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md`" in body


def test_the_producer_receives_the_classification_and_runs_state_changing_scenarios_aside():
    assert "`classification`" in _section("EVIDENCE")
    agent = " ".join(AGENT.read_text().split())
    assert "`classification`" in agent
    assert "scratch copy" in agent


# --- slice 01 re-drive findings (2026-10-27): fixture 09 ambiguous, and loops with no stated exit.

def test_a_test_suite_run_is_not_reusable_evidence():
    assert "A test-suite run is not reusable evidence" in _section("EVIDENCE")


def test_a_retry_after_narration_names_the_scenario_and_drops_the_context():
    assert "name the scenario to run and send no `context`" in _section("EVIDENCE")


def test_every_repeat_failure_goes_to_the_developer_with_a_stop():
    assert "after a second red oracle on the same expectation" in _section("BUILD")
    gate = _section("EVIDENCE")
    assert "after a second cannot-run for the same build" in gate
    assert "spot-check it by hand, or stop" in gate


def test_a_second_unanswered_ask_ends_the_run_not_done():
    assert "a second unanswered ask ends the run, reported not done" in _section("ADJUDICATE")


def test_the_developer_outranks_a_green_oracle():
    assert "The developer's reject outranks a green oracle" in _section("ADJUDICATE")


def test_the_producer_has_an_approval_test_path():
    agent = " ".join(AGENT.read_text().split())
    assert "`approval test`" in agent
