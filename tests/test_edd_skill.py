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
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "edd" / "SKILL.md"


def _flat():
    """The skill and every `skills/edd/references/` file it tells the executor to read, flattened."""
    text = SKILL.read_text()
    for name in dict.fromkeys(re.findall(r"skills/edd/references/([\w-]+\.md)", text)):
        text += "\n" + (SKILL.parent / "references" / name).read_text()
    return " ".join(text.split())


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
    """The flattened text of the `## <heading>` section, up to the next `## ` heading, followed by any
    `skills/edd/references/` file the section tells the executor to read — the step's detail lives
    there, and an assertion about the step must reach it."""
    text = SKILL.read_text()
    start = text.index(f"\n## {heading}")
    end = text.find("\n## ", start + 1)
    section = text[start:end if end != -1 else None]
    for name in re.findall(r"skills/edd/references/([\w-]+\.md)", section):
        section += "\n" + (SKILL.parent / "references" / name).read_text()
    return " ".join(section.split())


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


# --- slice 03 structure (2026-10-27): EVIDENCE and REVIEW detail moved verbatim to references/, to keep
# the always-loaded body under plugin-dev's 5,000-word cap. A step that points at a file that is not
# there would load nothing, silently.

def test_every_reference_the_skill_names_exists_and_is_read_before_its_step():
    text = SKILL.read_text()
    names = re.findall(r"`\$\{CLAUDE_PLUGIN_ROOT\}/skills/edd/references/([\w-]+\.md)`", text)
    assert names, "the skill names no reference"
    for name in names:
        assert (SKILL.parent / "references" / name).is_file(), name
        assert f"Read `${{CLAUDE_PLUGIN_ROOT}}/skills/edd/references/{name}` before" in " ".join(text.split()), name


# --- edd-article-alignment slice 03 (2026-10-27): every accepted expectation is pinned by a test meeting
# this plugin's testing standards, and the built code is reviewed and repaired with this plugin's own
# skills, serious findings blocking done. Decisions D2 (review-code and ux-review rows) and D8.

def test_stabilize_runs_after_adjudicate_and_before_findings():
    text = SKILL.read_text()
    assert text.index("\n## ADJUDICATE") < text.index("\n## STABILIZE") < text.index("\n## FINDINGS")


def test_stabilize_reads_the_testing_standards_and_writes_no_test_itself():
    stabilize = _section("STABILIZE")
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/testing.md`" in stabilize
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/test-patterns.md`" in stabilize
    assert "writes no test itself" in stabilize


def test_an_accepted_qualitative_output_is_pinned_by_an_approval_test_of_the_accepted_evidence():
    assert "whose approved output is the evidence the developer accepted" in _section("STABILIZE")


def test_an_unpinned_accepted_expectation_blocks_done():
    assert "An accepted expectation no test pins blocks done" in _section("STABILIZE")


def test_review_code_runs_and_its_serious_findings_block():
    stabilize = _section("STABILIZE")
    assert "`phil:review-code`" in stabilize
    assert "Priority 1" in stabilize
    assert "Priority 6 finding on a pinning test" in stabilize


def test_advisory_findings_go_to_the_skill_that_owns_them():
    stabilize = _section("REPAIR")
    for skill in ("`phil:refactor`", "`phil:refactor-loop`", "`phil:refactor-tests`",
                  "`phil:redesign-tests`", "`phil:clean-comments`"):
        assert skill in stabilize, skill


def test_a_ui_change_runs_ux_review_and_a_must_fix_blocks():
    stabilize = _section("STABILIZE")
    assert "`phil:ux-review`" in stabilize
    assert "`must-fix`" in stabilize


def test_findings_clears_every_blocking_source():
    findings = _section("FINDINGS")
    for source in ("Priority 1", "`must-fix`", "no test pins"):
        assert source in findings, source


def test_pinning_and_repair_are_not_rebuilds():
    assert "Pinning tests and running a repair are not rebuilds" in _section("STABILIZE")


def test_the_one_line_standards_citation_is_retired():
    assert "The standards to work under are" not in SKILL.read_text()


def test_the_trail_records_pins_and_repairs():
    document = _section("DOCUMENT")
    assert "pinning test" in document
    assert "repair" in document


# --- slice 03 review findings (skill-reviewer, plugin-validator, fixture driver; 2026-10-27). The first
# draft cleared a fixed review-code finding on the builder's word, blocked spot-checks with no exit,
# called review-code with an argument it does not take, made its Advisory questions block, never ran
# or compared the pins, routed repairs by a Route that does not name their owner, claimed gates three
# repair skills lack, and ran repairs before the blockers cleared.

def test_a_rebuild_re_enters_stabilize_and_a_finding_clears_only_on_a_clean_re_run():
    assert "re-enters STABILIZE" in _section("BUILD")
    assert "clears it only when the re-run does not reproduce it" in _section("FINDINGS")


def test_a_spot_checked_expectation_reaches_findings_with_only_waive_and_stop():
    assert "spot-checked by hand, which no test can pin here" in _section("FINDINGS")


def test_build_records_a_base_and_review_code_runs_once_per_changed_file():
    assert "`base`" in _section("BUILD")
    assert "once per changed file" in _section("STABILIZE")


def test_review_codes_advisory_and_load_time_items_do_not_block():
    stabilize = _section("STABILIZE")
    assert "except an item whose Smell is `Advisory` or an `LWS-n` id" in stabilize


def test_pins_are_test_only_shown_green_and_matched_byte_for_byte():
    stabilize = _section("STABILIZE")
    assert "a change outside test files is a rebuild" in stabilize
    assert "the engine's oracle run after pinning" in stabilize
    assert "byte for byte" in stabilize


def test_repair_runs_after_findings_and_before_document():
    text = SKILL.read_text()
    assert (text.index("\n## STABILIZE") < text.index("\n## FINDINGS")
            < text.index("\n## REPAIR") < text.index("\n## DOCUMENT"))


def test_repairs_are_grouped_by_smell_and_each_gate_is_stated_truthfully():
    repair = _section("REPAIR")
    assert "group them by Smell and Priority, not by Route" in repair
    assert "`phil:clean-comments` has no gate of its own" in repair
    assert "never over a pinning test" in repair


def test_advisory_ux_findings_are_recorded():
    assert "every `consider`" in _section("STABILIZE")


def test_the_reviewers_independence_is_stated_in_the_body():
    text = " ".join(SKILL.read_text().split())
    review = text[text.index("## REVIEW"):text.index("## ADJUDICATE")]
    assert "never sees the builder's reasoning" in review


# --- slice 03 re-drive (2026-10-27): 16 of 19; 17 and 18 open. No post-pin oracle run was ever asked
# for, a test-only fix was both a rebuild and not, the repair order fought phil:refactor's inline mode,
# per-file review double-filed a test finding, and refactor-loop needs a Workflow grant edd lacks.

REPAIR_REF = SKILL.parent / "references" / "repair.md"


def test_the_engine_runs_its_oracle_after_pinning_and_that_run_replaces_oracle_result():
    assert "replaced on every rebuild and every pin commit" in _section("BUILD")
    assert "run its oracle with the pins committed" in _section("STABILIZE")


def test_a_test_only_fix_is_not_a_rebuild():
    assert "A fix whose change touches only test and approved-output files is not a rebuild" in _section("FINDINGS")


def test_a_finding_filed_by_two_per_file_runs_is_one_finding():
    assert "one finding, however many runs filed it" in _section("STABILIZE")


def test_repairs_run_in_an_order_that_respects_each_skills_interface():
    repair = " ".join(REPAIR_REF.read_text().split())
    assert "Run the `phil:clean-comments` group first" in repair
    assert "commit each diff the developer approves" in repair
    assert "also removes the comment items in that file" in repair
    assert "held in the conversation, never on disk" in repair


def test_refactor_loop_is_recommended_never_run():
    repair = " ".join(REPAIR_REF.read_text().split())
    assert "recommend `/phil:refactor-loop`" in repair
    assert "never runs it" in repair


# --- edd-article-alignment slice 04 (2026-10-27): the living record is written to this plugin's writing
# standards, and neither the evidence nor the developer's words are edited. Decisions D9, D11.

def test_document_reads_the_writing_standards_and_reviews_composed_drafts_before_writing():
    document = _section("DOCUMENT")
    assert "Read `${CLAUDE_PLUGIN_ROOT}/rules/writing.md`" in document
    assert "`${CLAUDE_PLUGIN_ROOT}/rules/technical-communication.md`" in document
    assert "`phil:red-team-prose`" in document
    assert "before anything is written to disk" in document


def test_fixes_touch_composed_spans_only_and_evidence_never_enters_the_review():
    document = _section("DOCUMENT")
    assert "only to spans inside a `composed` field" in document
    assert "never passed to the review" in document
    assert "byte-identical to what the producer captured" in document


def test_a_fitness_finding_blocks_done_until_fixed_or_waived():
    document = _section("DOCUMENT")
    assert "A `[fitness]` finding blocks done" in document
    assert "After a second fix round on the same document" in document


# --- the article's "A Practical Protocol", checked step by step (2026-10-27): six gaps.

def test_step_2_the_engine_builds_from_the_confirmed_expectations():
    assert "Hand the engine the confirmed expectations, in risk order, as its specification" in _section("BUILD")


def test_step_1_non_functional_requirements_include_error_handling():
    assert "performance, error handling, security, limits" in _section("CAPTURE")


def test_step_3_an_engine_that_cannot_meet_an_expectation_explains_why_and_the_developer_decides():
    build = _section("BUILD")
    assert "If the engine reports it cannot meet an expectation" in build
    assert "reword it, drop it on the record, or stop" in build


def test_step_5_a_challenge_can_tighten_a_vague_expectation():
    adjudicate = _section("ADJUDICATE")
    assert "a rewording that tightens a vague expectation" in adjudicate
    assert "its earlier evidence no longer stands" in adjudicate


def test_partially_verifiable_evidence_is_named():
    assert "partially verifiable" in _section("EVIDENCE")


def test_step_6_a_not_executable_expectation_is_pinned_outside_the_loop():
    assert "a test that runs outside the loop" in _section("STABILIZE")
    assert "`pinned, not run here`" in _section("STABILIZE")


# --- slice 04 review findings (skill-reviewer, plugin-validator; 2026-10-27). red-team-prose's Step 6
# applies every fix on one yes and cannot filter by provenance, and its no-argument mode reviews the
# whole conversation, evidence included. The draft now leaves the developer's words and the evidence
# out of the review structurally, and this skill owns the apply question.

DOCUMENT_REF = SKILL.parent / "references" / "document.md"


def _document_ref():
    return " ".join(DOCUMENT_REF.read_text().split())


def test_drafts_live_outside_the_repository_with_the_developers_words_as_placeholders():
    ref = _document_ref()
    assert "a temporary directory outside the repository" in ref
    assert "replaced by a placeholder naming it" in ref
    assert "referenced by path, never inlined" in ref


def test_this_skill_owns_the_apply_question_not_red_team_prose():
    ref = _document_ref()
    assert "its Steps 1 to 5 only" in ref
    assert "this skill's own ask replaces its Step 6" in ref


def test_the_fitness_ask_names_fix_waive_and_stop_and_a_fix_invents_nothing():
    ref = _document_ref()
    assert "`fix`, `waive` and `stop`" in ref
    assert "never inventing one" in ref


def test_writing_restores_the_developers_words_and_checks_both_against_the_record():
    ref = _document_ref()
    assert "restore each placeholder with the developer's words, verbatim" in ref
    assert "against the hash recorded at capture" in ref


def test_every_free_text_answer_is_recorded_as_the_developers():
    assert "Every free-text answer is recorded labelled `you wrote`" in _section("Every ask")


def test_only_the_developer_drops_an_expectation_and_the_record_says_so():
    assert "only the developer may drop one, at BUILD's cannot-meet ask" in _section("ADJUDICATE")
    assert "dropped by the developer" in _section("DOCUMENT")


def test_a_stop_once_build_has_started_writes_the_trail():
    assert "a stop once BUILD has started writes the trail" in _section("Every ask")


def test_an_out_of_loop_pin_has_its_own_dispatch_and_is_exempt_from_the_green_check():
    assert "exempt from the green check" in _section("STABILIZE")


def test_a_reworded_expectation_gets_evidence_and_a_fresh_review():
    adjudicate = _section("ADJUDICATE")
    assert "gets evidence whatever OPT-OUT said, and REVIEW re-runs with the new wording" in adjudicate


def test_the_producer_says_what_a_partial_run_leaves_unshown():
    agent = " ".join(AGENT.read_text().split())
    assert "what the run leaves unshown" in agent


# --- slice 04 fixture drive (2026-10-27): 18 of 22; 15 regressed when DOCUMENT began asking after a stop.

def test_a_run_that_has_ended_writes_its_reviewed_trail_without_asking():
    assert "ask nothing: apply no fix, record every finding as standing" in _document_ref()


def test_an_engines_cannot_meet_report_comes_before_the_red_oracle_rule():
    assert "comes before the red-oracle rule" in _section("BUILD")


def test_a_dropped_expectation_never_counts_as_met_and_does_not_block_done():
    assert "does not block done: the developer decided it" in _section("BUILD")


def test_a_build_reword_gets_evidence_whatever_opt_out_said():
    assert "gets evidence whatever OPT-OUT said, since the opt-out never saw it" in _section("BUILD")
