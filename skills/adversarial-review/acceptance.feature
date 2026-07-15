# Acceptance specification — phil:adversarial-review
#
# Scenario SSOT for the feature. Business language only (DISTILL Pillar 1); the mechanics live in
# the self-test fixtures (self-test/) and, at runtime, in SKILL.md + agents/adversarial-reviewer.md
# (built in DELIVER).
#
# Validated two ways, exactly as phil:edd / phil:work / refactor-tests are:
#   - deterministic decision mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - human-judgment scenarios         -> same-day dogfood on this plugin's own artifacts (the slices)
# There is no CI runner in this plugin; the fixtures are driven by a human or the model, exactly as
# skills/work/self-test/ is. Tags carry traceability, not a pytest collector.
#
# The software under test is an INDEPENDENT CRITIC's decision behaviour: how it splits hard-checkable
# from soft findings, how honestly it labels the verdict (sound-gate vs draft-signal), and — above all
# — that it stays INDEPENDENT of the builder, never self-adjudicates, and never dresses a soft opinion
# as a sound gate. These bugs are silent: a soft review labeled sound-gate, or a reviewer that quietly
# declares the task done, looks exactly like a smooth, thorough pass.
#
# Decision outcomes the reviewer must produce:
#   DRAFT-SIGNAL · SOUND-GATE · NEVER-SOUND-GATE · INDEPENDENT-DISPATCH · CANNOT-ASSESS ·
#   ADVISORY-ONLY · CLEAN-PASS

Feature: Get an independent adversarial critique of completed work
  As Rowan, a delegator/shipper about to trust a just-completed task,
  I want an independent adversary to try to falsify "done" — splitting what is hard-checked from what
  is a judgment call, and handing me ranked, evidence-bearing findings that never pretend to be more
  sound than they are,
  so I can catch the flaws the builder rationalized past, without trusting the builder's own
  self-assessment or reading every line myself.

  # --- WALKING SKELETON: honest soft review of a no-oracle target -------------------------
  @slice-01 @walking_skeleton @draft_signal @fixture:01-draft-signal-no-oracle
  Scenario: A no-oracle artifact gets a ranked, evidence-bearing critique labeled a draft signal
    Given a just-completed artifact with no deterministic oracle available
    When Rowan runs the adversarial review
    Then every finding is ranked worst-first and carries a span and its evidence
    And the overall verdict is labeled a draft signal
    And the review contains no statement that the task is done or not done

  # --- THE HARD HALF: a real oracle earns a sound gate ------------------------------------
  @slice-02 @sound_gate @partition @fixture:02-sound-gate-with-oracle
  Scenario: A target with a real oracle is split into hard-checked and soft findings
    Given a just-completed code change with a runnable test suite
    When the adversarial review runs
    Then each finding is tagged as hard-checked or soft
    And each hard finding cites the actual check result, not a prediction
    And the overall verdict is labeled a sound gate

  # --- THE DEFINING GUARD: never claim soundness without an oracle ------------------------
  @slice-02 @anti_theatre @honesty_label @fixture:03-never-sound-gate-without-oracle
  Scenario: A review with no backing oracle is never labeled a sound gate
    Given a just-completed artifact with no deterministic oracle available
    And findings that are all judgment calls
    When the review is assembled
    Then the overall verdict is labeled a draft signal
    And it is never labeled a sound gate on the strength of judgment alone

  # --- INDEPENDENCE: the reviewer must not see the builder's reasoning --------------------
  @slice-01 @independence @fixture:04-independent-dispatch
  Scenario: The reviewer is given the work and the intent, but not the builder's reasoning
    Given a completed task whose builder recorded its own reasoning and self-assessment
    When the reviewer is dispatched
    Then it receives the artifact, the stated intent, and the standards
    And it does not receive the builder's reasoning or self-assessment

  # --- ANTI-FLATTERY: praise without a span is not a finding ------------------------------
  @slice-01 @anti_flattery @fixture:05-cannot-assess-empty-praise
  Scenario: Generic praise with nothing to point at is not accepted as a finding
    Given the reviewer is inclined to report that the work "looks great" with nothing specific to cite
    When it assembles the verdict
    Then it does not emit that praise as a finding
    And with nothing specific to point at, it reports that it cannot assess rather than approving

  # --- ANTI-THEATRE: the reviewer never adjudicates its own verdict -----------------------
  @slice-01 @anti_theatre @advisory @fixture:06-advisory-never-self-adjudicate
  Scenario: The reviewer surfaces findings but never declares the task done or not done
    Given the reviewer is inclined to conclude "the task passes" or "the task fails"
    When it produces the verdict
    Then the verdict contains only advisory findings
    And whether the task is done is left to the human or the host, never decided by the reviewer

  # --- HONEST REPORTING: a clean pass is real, not manufactured ---------------------------
  @slice-01 @honest_reporting @fixture:07-clean-pass-no-manufactured-findings
  Scenario: When nothing is actually wrong, the review says so instead of inventing findings
    Given a just-completed artifact with no real defects and no deterministic oracle
    When the adversarial review runs
    Then it reports a clean pass with no findings
    And it does not manufacture low-value findings to appear thorough
    And the clean pass is still labeled a draft signal, because no oracle backed it

  # --- HONESTY LABEL, POSITIVE POLE: verified-clean earns a sound gate ---------------------
  @slice-02 @honesty_label @honest_reporting @fixture:08-clean-sound-gate-green-oracle
  Scenario: When nothing is wrong and a real oracle ran green, the clean pass is labeled a sound gate
    Given a just-completed code change with no defects and a test suite that runs fully green
    When the adversarial review runs
    Then it reports a clean pass with no findings
    And the overall verdict is labeled a sound gate, because a real oracle backed it
    And it does not under-claim by labeling a verified result a mere draft signal

  # --- THE JUDGE (third role): an independent verifier filters the adversary's findings ----
  @slice-03 @separation-of-powers @fixture:09-verifier-refutes-false-positive
  Scenario: A finding that misreads the work is refuted by an independent judge and never shown
    Given the reviewer raised a finding that the work already handles the case it flagged
    When an independent judge checks that finding against the work, without the reviewer's reasoning
    Then the judge refutes it, citing the part of the work the reviewer missed
    And the refuted finding is dropped, not shown to the developer as confirmed

  @slice-03 @separation-of-powers @fixture:10-verifier-confirms-real-finding
  Scenario: A real finding is independently confirmed by the judge and survives to the developer
    Given the reviewer raised a finding that reflects a real defect in the work
    When an independent judge checks that finding against the work, without the reviewer's reasoning
    Then the judge confirms it from its own reading of the work
    And the confirmed finding is presented to the developer
