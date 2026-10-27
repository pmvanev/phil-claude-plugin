# Acceptance specification — phil:edd
#
# Scenario SSOT for the feature. Business language only; the mechanics live in the self-test
# fixtures (self-test/) and, at runtime, in SKILL.md.
#
# Validated two ways, exactly as phil:work / refactor-tests are:
#   - deterministic decision mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - human-gated / judgment scenarios -> same-day dogfood on this plugin's own intents (the slices)
# No driver runs the fixtures (issue 42); a human or the model drives them. Tags carry traceability,
# not a pytest collector. tests/test_edd_skill.py is what fails the build.
#
# The software under test is the expectation loop and its evidence gate, after Andrea Laforgia's
# Expectation-Driven Development: capture checked for coverage, size and risk; executed evidence for
# every expectation unless the developer trusts the tests for the checkable ones; evidence only from
# a non-builder; narration — a pass count included — never accepted; and no done over a rejected
# expectation. These bugs are silent: an opt-out that skips a qualitative expectation, or a gate
# that accepts a green suite as proof, looks exactly like a smooth run.
#
# Decision outcomes the loop must produce:
#   CAPTURE-GAPS · CLASSIFY-CHECKABLE · OPT-OUT · GATE-RERUN-EXISTING · GATE-COMMISSION ·
#   REJECT-NARRATION · SPOT-CHECK · REVIEW-THEN-ASK · CHALLENGE · BLOCK-DONE · WAIVE-RECORDED ·
#   REPORT-NOT-DONE · PIN-APPROVAL · REVIEW-CODE-GATE · UX-GATE · DOCUMENT-TRAIL

Feature: Prove every expectation is met with executed evidence
  As Avery, an expectation owner delegating build work to AI agents,
  I want my expectations checked for coverage, size and risk, and executed evidence for each one —
  gathered by someone other than the builder — unless I choose to trust the tests for the checkable
  ones,
  so I can trust AI-produced work against my real intent, without trusting a green suite the builder
  wrote and without the builder grading its own homework.

  # --- CAPTURE: coverage, size and risk ---------------------------------------------------
  @edd-article-alignment @slice-01 @capture @fixture:11-capture-coverage-size-risk
  Scenario: A draft that misses categories and packs two behaviours is filled in before anything is built
    Given a draft with no past edge case and one expectation stating two behaviours
    When the tool checks the draft before Avery confirms it
    Then it names each missing category with a suggestion marked as its own, not Avery's, never inventing a past bug
    And it proposes splitting the double expectation in two
    And it orders the list by risk, worst first
    And Avery's own wording reaches the list unchanged

  # --- CLASSIFY: the honesty rule ---------------------------------------------------------
  @edd-loop @classify @fixture:02-classify-honesty-rule
  Scenario: An unclear expectation is treated as checkable unless there is a concrete reason otherwise
    Given an expectation whose provability by an engine is unclear
    When the tool classifies it
    Then it treats the expectation as checkable by default
    And it asks Avery to confirm before it will ever treat an expectation as qualitative
    And an expectation offered as qualitative without a concrete reason is treated as checkable

  # --- OPT-OUT: trusting the tests is Avery's call, and covers checkable expectations only --
  @edd-article-alignment @slice-01 @opt-out @fixture:01-opt-out-checkable-only
  Scenario: Trusting the tests skips evidence for checkable expectations only, and the record says so
    Given checkable expectations and one qualitative expectation
    And Avery chooses to trust the tests for the checkable ones this run
    When the loop runs
    Then no evidence is gathered for the checkable expectations
    And the qualitative expectation still gets executed evidence for Avery to judge
    And the build still runs
    And the record names every expectation trusted to the tests

  # --- EVIDENCE: a checkable expectation shows its scenario --------------------------------
  @edd-article-alignment @slice-01 @gate @separation-of-powers @fixture:08-checkable-scenario-evidence
  Scenario: A checkable expectation gets its scenario run when Avery has not opted out
    Given a checkable expectation and no opt-out
    When evidence is gathered for it
    Then Avery sees one scenario's inputs and its verbatim output, with the command that reproduces it
    And whoever produced the evidence is not whoever built the thing

  @edd-article-alignment @slice-01 @gate @error @fixture:09-pass-count-is-narration
  Scenario: A test runner's pass count is rejected as narration
    Given evidence for a checkable expectation that shows only how many tests passed
    When the gate checks whether it is acceptable evidence
    Then the tool rejects it as narration
    And it gathers the scenario itself in its place

  @edd-article-alignment @slice-01 @gate @fixture:10-not-executable-in-the-loop
  Scenario: An expectation no agent can run here goes to Avery to spot-check
    Given an expectation that cannot be run or watched inside the loop
    And Avery has confirmed what stops it running here
    When evidence is gathered for it
    Then the tool commissions nothing and names that blocker
    And Avery spot-checks it by hand or stops
    And a spot-check ends in Avery's accept or reject, like any other evidence
    And the record says which, in Avery's own words

  # --- EVIDENCE GATE: reuse evidence the engine already produced --------------------------
  @edd-loop @gate @fixture:03-gate-evidence-exists
  Scenario: Evidence the engine already captured is re-run by the producer, not taken from the builder
    Given a qualitative expectation and an engine run that already captured executed evidence with its reproduce command
    When the gate runs for that expectation
    Then the producer re-runs that reproduce command and captures what it emits
    And no new scenario is designed
    And Avery adjudicates the expectation against the producer's capture
    And if Avery says it does not show the expectation, fresh evidence is gathered and nothing is rebuilt

  # --- EVIDENCE GATE: commission new executed evidence, from a non-builder ----------------
  @edd-loop @gate @separation-of-powers @fixture:04-gate-commission-new
  Scenario: A qualitative expectation with no evidence gets fresh executed evidence from a non-builder
    Given a qualitative expectation for which no relevant evidence exists yet
    When the gate runs for that expectation
    Then the tool commissions a fresh executed artifact — a real run or render captured verbatim with the command that reproduces it
    And whoever produced the evidence is not whoever built the thing
    And it asks Avery to adjudicate the expectation against that evidence

  # --- EVIDENCE GATE: narration is not evidence -------------------------------------------
  @edd-loop @gate @error @fixture:05-reject-narration
  Scenario: A described-but-not-run claim is rejected as insufficient
    Given a claim offered as evidence that is only a description, with no reproducible artifact
    When the gate checks whether it is acceptable evidence
    Then the tool rejects it as narration, not evidence
    And it commissions a real executed artifact in its place before any adjudication

  # --- ADJUDICATE: a rejected expectation blocks done -------------------------------------
  @edd-loop @adjudicate @error @fixture:06-blocked-done
  Scenario: A rejected expectation is never reported as done
    Given an expectation whose executed evidence Avery has rejected
    When the tool determines whether the work is done
    Then it does not report the work as done
    And it iterates that expectation rather than moving on
    And no completion is claimed while any expectation stands rejected

  # --- REVIEW: an independent adversary before any verdict -------------------------------
  @edd-article-alignment @slice-02 @review @separation-of-powers @fixture:12-review-before-verdict
  Scenario: The built work is attacked by an independent reviewer before Avery judges it
    Given evidence has been gathered for every expectation not opted out
    When the review runs
    Then an independent reviewer attacks the built work against the expectations and the standards, never seeing the builder's reasoning
    And an independent judge confirms or refutes each finding
    And each confirmed finding reaches Avery beside the evidence it bears on, with the four challenge questions

  @edd-article-alignment @slice-02 @review @error @fixture:14-unwaived-major-blocks-done
  Scenario: A confirmed major finding blocks done until it is fixed or waived by name
    Given Avery has accepted an expectation and a confirmed major finding still stands
    When the tool determines whether the work is done
    Then the tool puts the finding to Avery to fix, waive or stop
    And it does not report the work as done while the finding stands
    And a waiver must name the finding and give a reason, which the record keeps with a timestamp

  # --- CHALLENGE and STOP: Avery pushes on the evidence, and can end any loop -------------
  @edd-article-alignment @slice-02 @adjudicate @fixture:13-challenge-rebuilds-nothing
  Scenario: A challenge gathers evidence for the named scenario and rebuilds nothing
    Given Avery has read the evidence and the four challenge questions
    When Avery challenges it, naming the scenario that would break it
    Then evidence is gathered for that scenario
    And nothing is rebuilt
    And Avery is asked again, with all four answers offered

  @edd-article-alignment @slice-02 @adjudicate @error @fixture:15-stop-over-a-standing-challenge
  Scenario: A stop over a standing challenge ends the run, not done, with the challenge on record
    Given Avery has challenged an expectation
    When Avery stops instead of answering
    Then nothing more is commissioned or asked
    And the record keeps the standing challenge and the expectation as unproven
    And the run is reported not done

  # --- STABILIZE: pin to the testing standards, review and repair with this plugin's skills -
  @edd-article-alignment @slice-03 @stabilize @error @fixture:16-unpinned-expectation-blocks-done
  Scenario: An accepted expectation no test pins blocks done until the engine pins it
    Given two accepted expectations and an engine that pins only one of them
    When the tool stabilizes the work
    Then the unpinned expectation blocks done
    And fixing it means the engine writes the pinning test, without a rebuild or a new round of verdicts

  @edd-article-alignment @slice-03 @stabilize @fixture:17-approval-test-from-accepted-evidence
  Scenario: An accepted qualitative output is pinned by an approval test of exactly what Avery accepted
    Given Avery accepted a qualitative expectation on a captured output
    When the tool stabilizes the work
    Then the engine pins it with an approval test whose approved output is that evidence, word for word
    And Avery's accept counts as the first approval

  @edd-article-alignment @slice-03 @stabilize @error @fixture:18-review-code-priority-1-blocks
  Scenario: The plugin's code review blocks on serious findings and hands the rest to their owners
    Given the plugin's code review finds a security defect, a weak pinning test, and two smaller smells
    When the tool stabilizes the work
    Then the security defect and the weak pinning test block done until fixed or waived
    And the smaller smells are offered to the plugin skill that owns each, which runs under its own gate

  @edd-article-alignment @slice-03 @stabilize @fixture:19-ui-change-runs-ux-review
  Scenario: A change to the UI is audited for usability and accessibility
    Given the change touches UI files
    When the tool stabilizes the work
    Then the plugin's UX audit runs over them
    And a must-fix finding blocks done while a consider finding advises

  # --- DOCUMENT: a trail for every run that built ----------------------------------------
  @edd-article-alignment @slice-01 @document @fixture:07-trail-every-run-that-built
  Scenario: Every run that built leaves a record, and a run stopped before building leaves none
    Given a completed loop in which the engine built
    When the tool finishes
    Then it records the expectations, the executed evidence, and Avery's verdicts as living documentation
    And it writes a durable summary alongside the repository's other evolution records
    And a run in which Avery trusted the tests records which expectations were trusted
    But a run Avery stopped before anything was built records no trail at all
