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
# Decision outcomes the spine must produce (SKILL.md "Decision outcomes" is authoritative):
#   CAPTURE · NO-OP · REFUSE-DERIVABLE · PROJECTED · PROJECTION-UNREFRESHED · RESUME-CURRENT ·
#   RESUME-STALE · RECONSTRUCT · ROUTE · ROUTE-LIVE-WINS · ASK-OWNER ·
#   BOARD-AGREES · BOARD-DIVERGES · BOARD-UNREADABLE · REPORT-CLAIM-CONFLICT ·
#   PUSHED · POPPED · SHOWN · STACK-EMPTY · STACK-UNKNOWN · WRITE-REFUSED
#
# REPORT-CLAIM-CONFLICT belongs to slice 03, tested and deliberately not built; it is kept here because
# its scenario is kept. Every other outcome above is live.

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

  # --- Issue #24 — the board is the other record of what is in flight -------------------------
  # The residual slice 03 left standing: not "record which card was claimed", but "notice when the
  # two records of what is in flight disagree".

  @issue-24 @error @fixture(13-board-diverges-from-snapshot) @contract-shape:pure-function
  Scenario: The work moved on even though the code did not
    Given a resume point that still matches the state of the work in progress
    But the team's shared record names a different piece of work as the one in hand
    When a fresh session picks it up
    Then it still says the resume point matches
    And it reports that the two records of what is in hand disagree
    And it names both pieces of work and where each came from
    And it does not choose between them

  @issue-24 @fixture(14-board-agrees-with-snapshot) @contract-shape:bounded-change
  Scenario: Agreement is stated, so silence never has to be interpreted
    Given a resume point naming the same work the team's shared record has in hand
    When a fresh session picks it up
    Then it says the two records agree
    And it names the piece of work they agree on

  @issue-24 @error @fixture(15-board-unreadable-says-so) @contract-shape:pure-function
  Scenario: A comparison that could not be made is admitted, never assumed
    Given a resume point in a project that keeps no shared record of work in hand
    When a fresh session picks it up
    Then it says the comparison could not be made, and why
    And it does not report the two records as agreeing
    And it still presents the resume point and names the owner

  # --- live-work-stack (issue #29), slice 01: the stack gains operations -------------------------
  # The stack was persisted from 2026-08-14 and had no operations: it was recorded only when the
  # session was put down, which is when Kai has stopped needing it. These scenarios are the live view.
  # Slice 02 adds pop and the stale-frame mark.

  @issue-29 @happy @fixture(16-push-preserves-payload) @contract-shape:pure-function
  Scenario: A diversion is recorded the moment it is taken, onto a record someone else left
    Given a resume point a previous session left behind, carrying its reasoning and its next action
    And a session that has picked that work up and is now leaving it for something blocking it
    When the session records the diversion, naming what it is entering and why
    Then the diversion is added to the work stack
    And the previous session's reasoning and next action are left exactly as they were
    And the freshness stamp is left exactly as it was, because no new state of play was captured

  @issue-29 @error @fixture(17-competing-write-refused) @contract-shape:pure-function
  Scenario: A record that moved while it was being read is never written over
    Given a session partway through recording a diversion
    And the shared record changed after it was read and before it could be written
    When the session tries to write
    Then it refuses, and says what it saw before and after
    And it records nothing
    And it does not try again, because choosing a winner is not its to do
    And it says back the diversion it did not record, so the reason is not lost with the attempt

  @issue-29 @happy @fixture(18-show-at-depth) @contract-shape:pure-function
  Scenario: Several diversions deep, the way back is legible without re-reading the session
    Given a session three diversions deep
    When it asks where it is
    Then it is shown every level, what each one is, why it was entered, and how long it has been open
    And the level it is currently at is marked
    And no level is judged stale, because none of them has outlived a wind-down

  @issue-29 @error @fixture(19-unknown-is-not-none) @contract-shape:pure-function
  Scenario: Nothing written down and nothing to write down are different answers
    Given no resume point exists at all
    When a session asks where it is
    Then it says nobody has written anything down
    And it does not say there were no diversions, which nobody established
    But given a resume point that a session left with no diversions to record
    Then asking the same question says there were none

  @issue-29 @error @fixture(20-push-with-no-resume-point) @contract-shape:pure-function
  Scenario: A diversion can be the first thing ever recorded
    Given no resume point exists
    And a session takes a diversion
    When it records the diversion
    Then a resume point is created carrying the diversion alone
    And the reasoning and the next action are marked as never recorded, not as empty
    And the record says plainly that no state of play has been captured against it

  @issue-29 @happy @fixture(21-pop-to-the-parent) @contract-shape:pure-function
  Scenario: Coming back from a detour puts the thing it interrupted back in hand
    Given a session three diversions deep
    When it closes the innermost one
    Then that level is dropped
    And it is told what it is back to, by name
    And the reasoning, the next action and the freshness stamp are left exactly as they were

  @issue-29 @error @fixture(22-never-popped-frame-is-stale) @contract-shape:pure-function
  Scenario: A diversion left open across a wind-down stops looking current
    Given a diversion that was open before the session was last put down, and is open still
    When a session asks where it is
    Then that level is marked, because it has now outlived two of them
    And a level that has outlived only one is not marked, because carrying work across one is the point
    And a level that has outlived none is not marked however old it is, because age is not the measure

  @issue-29 @happy @fixture(23-push-onto-an-open-frame) @contract-shape:pure-function
  Scenario: A diversion taken during a diversion nests under it
    Given a session already one diversion deep
    When it records a second one
    Then the new level sits beneath the first, not beside it
    And the level it interrupted is left exactly as it was

  @issue-29 @happy @fixture(24-capture-carries-the-stack-forward) @contract-shape:pure-function
  Scenario: Putting the session down carries open diversions forward without rewriting them
    Given a session ending while two diversions are still open
    And the session's own account of them is incomplete and imprecise
    When it is put down
    Then every open diversion is carried forward exactly as it was recorded
    And each is counted as having survived one more wind-down
    And none is dropped because the account failed to mention it

  @issue-29 @error @fixture(25-pop-nothing-two-ways) @contract-shape:pure-function
  Scenario: Closing a diversion when there is none says which nothing it found
    Given no record exists at all
    When a session closes a diversion
    Then it says nobody has written anything down
    But given a record that was left with no diversions
    Then it says there were none
    And neither writes anything

  @issue-29 @error @fixture(26-pop-refuses-and-reports-stale) @contract-shape:pure-function
  Scenario: Closing a diversion obeys the same write rules as opening one
    Given a record that changed after it was read
    When a session closes a diversion
    Then it refuses and records nothing, exactly as opening one would
    But given the diversion being closed had outlived two wind-downs
    Then closing it says so, because otherwise the drift leaves with it
