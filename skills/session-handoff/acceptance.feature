# Acceptance specification — phil:session-handoff
#
# Scenario SSOT for the feature. Business language only (DISTILL Pillar 1); the mechanics live in the
# self-test fixtures (self-test/) and, at runtime, in SKILL.md (built in DELIVER).
#
# Validated two ways, exactly as phil:work / phil:edd / adversarial-review are:
#   - deterministic decision mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - judgment scenarios               -> same-day dogfood on this repo's own sessions
# There is no CI runner in this plugin; fixtures are driven by a human or the model. Tags carry
# traceability, not a pytest collector.
#
# The software under test is the CAPTURE + READ-BACK decision behaviour: what the spine records, what
# it REFUSES to record, whether it tells the truth about freshness, and whether it routes the work or
# does it. These bugs are silent. A snapshot that quietly records derivable state looks like a fuller
# snapshot. A stale snapshot presented as current looks like a smooth resume — and is the exact
# failure this repo's own continue.md exhibits today.
#
# Decision outcomes the spine must produce:
#   CAPTURE · NO-OP · REFUSE-DERIVABLE · RESUME-CURRENT · RESUME-STALE · RECONSTRUCT ·
#   ROUTE · ROUTE-LIVE-WINS · ASK-OWNER · REPORT-CLAIM-CONFLICT

Feature: Carry work across the session boundary without a re-briefing
  As Kai, a developer carrying multi-session work,
  I want the next session to pick up with the reasoning, the intended next action, and the correct
  entry point already in hand,
  So that momentum survives the boundary instead of being re-explained or freelanced away.

  # --- Slice 01 — snapshot and resume -------------------------------------------------------

  @walking_skeleton @driving_port @real-io @slice-01 @fixture(01-capture-and-resume) @contract-shape:bounded-change
  Scenario: A session hands its reasoning to the next one
    Given a session that decided something and named what to do next
    When the session is put down and a fresh one picks the work up
    Then the fresh session is told what was decided and what to do next
    And it is told the resume point is still current

  @slice-01 @error @fixture(02-no-op-session) @contract-shape:unbounded-preservation
  Scenario: A session that achieved nothing leaves nothing behind
    Given a session that advanced no work
    When the session is put down
    Then nothing is recorded
    And the reason nothing was recorded is stated

  @slice-01 @error @fixture(03-refuse-derivable) @contract-shape:bounded-change
  Scenario: The resume point refuses to duplicate what is already recorded elsewhere
    Given a session whose position is already recorded in the project's own files
    When the session is put down
    Then that position is not copied into the resume point
    And it is looked up again when the work is picked up

  @slice-01 @error @real-io @fixture(04-stale-refuses-to-resume) @contract-shape:pure-function
  Scenario: A resume point that no longer matches the work says so before anything else
    Given a resume point recorded before the work moved on
    When a fresh session picks the work up
    Then it is told the resume point is out of date, and by how much
    And it is not handed the resume point as though it were current

  @slice-01 @error @fixture(05-no-resume-point) @contract-shape:pure-function
  Scenario: With no resume point, what is reconstructed is labelled as reconstructed
    Given no resume point exists
    When a fresh session picks the work up
    Then the position is worked out from the project's own files
    And the briefing says it was worked out rather than recorded

  # --- Slice 02 — entry-point routing -------------------------------------------------------

  @slice-02 @driving_port @fixture(06-route-to-owner) @contract-shape:unbounded-preservation
  Scenario: Work is handed to whatever owns it
    Given work that belongs to a particular way of working
    When a fresh session picks it up
    Then the session names the way that work is meant to be done
    And it hands the work over rather than doing it itself

  @slice-02 @error @fixture(07-live-wins-over-recorded) @contract-shape:unbounded-preservation
  Scenario: A recorded owner that has since changed does not win
    Given a resume point naming an owner that has since changed
    When a fresh session picks the work up
    Then the current owner is used
    And the disagreement is pointed out rather than quietly settled

  @slice-02 @error @fixture(08-unknown-owner-asks) @contract-shape:unbounded-preservation
  Scenario: An unknown owner is admitted, never guessed
    Given work whose owner cannot be determined
    When a fresh session picks it up
    Then the session says the owner is unknown and asks
    And it does not begin the work

  # --- Slice 03 — claimed-card link ---------------------------------------------------------

  @slice-03 @fixture(09-claim-and-basis) @contract-shape:bounded-change
  Scenario: The next session resumes the same piece of work, for the same reason
    Given a session working an agreed piece of work for a stated reason
    When a fresh session picks up
    Then it resumes that same piece of work
    And it repeats the reason it was chosen

  @slice-03 @error @fixture(10-competing-claim) @contract-shape:pure-function
  Scenario: Two sessions claiming the same work is reported, not silently resolved
    Given two sessions that each claim the same piece of work
    When one of them picks the work up
    Then the competition is reported
    And neither claim is discarded
