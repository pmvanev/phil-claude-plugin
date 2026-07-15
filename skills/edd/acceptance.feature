# Acceptance specification — phil:edd
#
# Scenario SSOT for the feature. Business language only (per DISTILL Pillar 1); the mechanics
# live in the self-test fixtures (self-test/) and, at runtime, in SKILL.md (built in DELIVER).
#
# Validated two ways, exactly as phil:work / refactor-tests are:
#   - deterministic decision mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - human-gated / judgment scenarios -> same-day dogfood on this plugin's own intents (the slices)
# There is no CI runner in this plugin; the fixtures are driven by a human or the model, exactly as
# skills/work/self-test/ is. Tags carry traceability, not a pytest collector.
#
# The software under test is the FRONT-DOOR + GATE decision behaviour: how phil:edd classifies an
# expectation, when it off-ramps (adding NOTHING), and — above all — that the qualitative gate
# accepts only EXECUTED evidence, keeps the evidence-producer distinct from the builder, and never
# reports done over a rejected expectation. These bugs are silent: an off-ramp that quietly builds a
# gate, or a gate that accepts narration, looks exactly like a smooth run.
#
# Decision outcomes the front-door/gate must produce:
#   OFF-RAMP · CLASSIFY-CHECKABLE · GATE-POINT-EXISTING · GATE-COMMISSION ·
#   REJECT-NARRATION · BLOCK-DONE · DOCUMENT-TRAIL

Feature: Prove qualitative expectations are met with executed evidence
  As Avery, an expectation owner delegating build work to AI agents,
  I want a thin front-door that off-ramps to my existing engines whenever they already prove my
  intent, and only for the expectations no test can cheaply assert attaches a gate that makes me
  adjudicate EXECUTED evidence,
  so I can trust AI-produced work against my real intent — without ceremony where it isn't needed,
  and without the builder grading its own homework.

  # --- OFF-RAMP: add nothing when the engine already proves it ----------------------------
  @slice-01 @walking_skeleton @offramp @fixture:01-offramp-all-checkable
  Scenario: An all-checkable intent is sent straight to the engine, with no ceremony
    Given an intent whose every expectation the existing engines can already prove
    When Avery runs the expectation loop
    Then the tool shows how each expectation is provable and by which engine
    And it recommends running that engine directly
    And it exits without commissioning evidence or opening any trail

  # --- CLASSIFY: bias toward the off-ramp -------------------------------------------------
  @slice-01 @classify @fixture:02-classify-bias-to-offramp
  Scenario: An unclear expectation is treated as provable unless there is a concrete reason otherwise
    Given an expectation whose provability by an engine is unclear
    When the tool classifies it
    Then it treats the expectation as engine-provable by default
    And it asks Avery to confirm before it will ever treat an expectation as qualitative
    And an expectation offered as qualitative without a concrete reason is treated as engine-provable

  # --- EVIDENCE GATE: reuse evidence the engine already produced --------------------------
  @slice-02 @gate @fixture:03-gate-evidence-exists
  Scenario: A qualitative expectation reuses evidence the engine already produced
    Given a qualitative expectation and an engine run that already produced relevant executed evidence
    When the gate runs for that expectation
    Then the tool points Avery at the existing executed evidence
    And it does not commission any new evidence
    And it asks Avery to adjudicate the expectation against that evidence

  # --- EVIDENCE GATE: commission new executed evidence, from a non-builder ----------------
  @slice-02 @gate @separation-of-powers @fixture:04-gate-commission-new
  Scenario: A qualitative expectation with no evidence gets fresh executed evidence from a non-builder
    Given a qualitative expectation for which no relevant evidence exists yet
    When the gate runs for that expectation
    Then the tool commissions a fresh executed artifact — a real run or render captured verbatim with the command that reproduces it
    And whoever produced the evidence is not whoever built the thing
    And it asks Avery to adjudicate the expectation against that evidence

  # --- EVIDENCE GATE: narration is not evidence -------------------------------------------
  @slice-02 @gate @error @fixture:05-reject-narration
  Scenario: A described-but-not-run claim is rejected as insufficient
    Given a claim offered as evidence that is only a description, with no reproducible artifact
    When the gate checks whether it is acceptable evidence
    Then the tool rejects it as narration, not evidence
    And it commissions a real executed artifact in its place before any adjudication

  # --- ADJUDICATE: a rejected expectation blocks done -------------------------------------
  @slice-02 @adjudicate @error @fixture:06-blocked-done
  Scenario: A rejected qualitative expectation is never reported as done
    Given a qualitative expectation whose executed evidence Avery has rejected
    When the tool determines whether the work is done
    Then it does not report the work as done
    And it iterates that expectation rather than moving on
    And no completion is claimed while any expectation stands rejected

  # --- DOCUMENT: living docs only when the gate actually ran ------------------------------
  @slice-02 @document @fixture:07-living-docs-gate-ran-only
  Scenario: Expectations, evidence, and verdicts are recorded only when the gate ran
    Given a completed loop in which at least one qualitative expectation was adjudicated
    When the tool finishes
    Then it records the expectations, the executed evidence, and Avery's verdicts as living documentation
    And it writes a durable summary alongside the plugin's other evolution records
    But an off-ramp-only run records no such trail at all
