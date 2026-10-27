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
    assert "`expectation`, its `classification`, the `target`, any named `scenario` and any `context`" in body


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
    assert "name the scenario to run as `scenario` and send no `context`" in _section("EVIDENCE")


def test_every_repeat_failure_goes_to_the_developer_with_a_stop():
    assert "after a second red oracle on the same expectation" in _section("BUILD")
    gate = _section("EVIDENCE")
    assert "after a second cannot-run for the same expectation" in gate
    assert "spot-check it by hand, or stop" in gate


def test_a_second_unanswered_ask_ends_the_run_not_done():
    assert "two consecutive unanswered asks end the run, reported not done" in _section("Every ask")


def test_the_developer_outranks_a_green_oracle():
    assert "The developer's reject outranks a green oracle" in _section("ADJUDICATE")


def test_the_producer_has_an_approval_test_path():
    agent = " ".join(AGENT.read_text().split())
    assert "`approval test`" in agent


# --- edd-article-alignment slice 02 (2026-10-27): an independent adversary attacks the work before any
# verdict, and the developer can challenge evidence instead of only accepting or rejecting it.
# Decisions D2 (adversarial-review row) and D7.

ADVERSARIAL = REPO / "skills" / "adversarial-review" / "SKILL.md"


def test_review_runs_after_evidence_and_before_any_verdict():
    text = SKILL.read_text()
    assert text.index("\n## EVIDENCE") < text.index("\n## REVIEW") < text.index("\n## ADJUDICATE")


def test_review_composes_the_reviewer_and_judge_under_their_contract():
    review = _section("REVIEW")
    assert "`phil:adversarial-reviewer`" in review
    assert "`phil:adversarial-verifier`" in review
    assert "`{ target, intent, standards, oracle_result? }`" in review
    assert "never the builder's reasoning" in review


def test_a_confirmed_major_blocks_done_until_fixed_or_waived_by_name():
    review = _section("REVIEW")
    assert "A judge-confirmed `major` finding blocks done" in review
    assert "waives it by name, with a reason the record keeps" in review


def test_the_ask_carries_the_articles_four_challenge_questions():
    adjudicate = _section("ADJUDICATE")
    for question in ("Do the numbers add up?", "Were the edge cases actually run?",
                     "What input would break it?", "What scenario is missing?"):
        assert question in adjudicate, question


def test_the_answer_set_is_accept_reject_challenge_stop():
    adjudicate = _section("ADJUDICATE")
    assert "`accept`, `reject`, `challenge` and `stop`" in adjudicate


def test_a_challenge_gathers_evidence_and_rebuilds_nothing():
    adjudicate = _section("ADJUDICATE")
    assert "A challenge commissions evidence for the named scenario and rebuilds nothing" in adjudicate
    assert "A challenge that adds an expectation sends it through CLASSIFY" in adjudicate


def test_the_trail_records_challenges_and_waivers():
    document = _section("DOCUMENT")
    assert "challenge" in document
    assert "waiver" in document


def test_adversarial_review_names_edd_as_a_composing_host():
    flat = " ".join(ADVERSARIAL.read_text().split())
    assert "`phil:edd` composes it at its REVIEW step" in flat


# --- slice 02 review findings (skill-reviewer, plugin-validator, fixture driver; 2026-10-27).
# The first draft blocked done on a confirmed major with no way to clear it, routed on raw severity,
# hid the review's label, let a stale oracle result and the builder's notes reach the reviewer, and
# left free-text answers and several asks without a stop.

COMMAND = REPO / "commands" / "edd.md"


def test_build_captures_the_oracle_run_and_replaces_it_on_every_rebuild():
    build = _section("BUILD")
    assert "`oracle_result`" in build
    assert "replaced on every rebuild" in build


def test_a_rebuild_re_runs_review_and_a_waiver_lapses_when_its_span_changes():
    body = _flat()
    assert "A rebuild re-runs REVIEW on the whole target" in body
    assert "A waiver stands only while its finding's span is unchanged" in body


def test_review_routes_on_corrected_severity_and_shows_the_label():
    review = _section("REVIEW")
    assert "after the judge's `corrected_severity`" in review
    assert "`overall_label`" in review
    assert "`cannot-assess`" in review
    assert "never as approval" in review
    assert "Read `${CLAUDE_PLUGIN_ROOT}/skills/adversarial-review/SKILL.md`" in review


def test_review_target_excludes_the_engines_own_notes():
    assert "excluding the engine's own logs, plans, notes and commit messages" in _section("REVIEW")


def test_findings_step_clears_a_confirmed_major_by_fix_waive_or_stop_and_is_bounded():
    text = SKILL.read_text()
    assert text.index("\n## ADJUDICATE") < text.index("\n## FINDINGS") < text.index("\n## DOCUMENT")
    findings = _section("FINDINGS")
    assert "`fix`, `waive` and `stop`" in findings
    assert "rows trusted to the tests" in findings
    assert "After a second fix round on the same finding" in findings


def test_every_adjudication_answer_names_its_cost_and_the_questions_sit_in_the_context_block():
    adjudicate = _section("ADJUDICATE")
    assert "Name each answer's cost" in adjudicate
    assert "four challenge questions in the context block" in adjudicate


def test_a_challenge_respects_spot_checks_and_reviews_an_added_expectation():
    adjudicate = _section("ADJUDICATE")
    assert "asks the developer to spot-check the named scenario" in adjudicate
    assert "re-run REVIEW with the added expectation in its intent" in adjudicate


def test_every_ask_offers_stop_and_two_consecutive_unanswered_asks_end_the_run():
    asks = _section("Every ask")
    assert "offers `stop`" in asks
    assert "two consecutive unanswered asks end the run" in asks


def test_only_a_row_with_a_concrete_oracle_can_be_opted_out():
    assert "cannot name as a concrete assertion cannot be opted out" in _section("OPT-OUT")


def test_the_command_describes_review_and_challenge():
    description = COMMAND.read_text().split("\n")[1]
    assert "review" in description
    assert "challenge" in description


# --- slice 02 second re-drive (2026-10-27): 14 of 15; fixture 13 ambiguous for want of a channel.

def test_a_named_scenario_reaches_the_producer():
    agent = " ".join(AGENT.read_text().split())
    assert "`scenario?`" in agent
    assert "run exactly that scenario" in agent


def test_findings_starts_once_every_asked_expectation_is_accepted():
    assert "Once every expectation put to the developer is accepted" in _section("FINDINGS")


def test_every_second_cap_binds_from_the_second_on():
    assert "the second and every one after it" in _section("Every ask")


def test_a_recurring_finding_keeps_its_count_and_its_waiver():
    findings = _section("FINDINGS")
    assert "the same finding when its span names the same lines and its mechanism the same defect" in findings


def test_the_developer_gives_the_qualitative_reason():
    classify = _section("CLASSIFY")
    assert "only when the developer gives a **concrete reason**" in classify
    assert "gives or confirms" not in classify
