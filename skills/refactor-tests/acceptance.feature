# Acceptance specification — phil:refactor-tests
#
# Scenario SSOT for the feature. Business language only (per DISTILL Pillar 1); the mechanics
# live in the self-test fixtures (self-test/) and, at runtime, in SKILL.md.
#
# These scenarios are validated two ways:
#   - deterministic safety mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - human-gated + detection scenarios -> same-day dogfood on this plugin's own tests (the slices)
# There is no CI runner in this plugin; the fixtures are driven by a human or the model, exactly
# as refactor/self-test/ is. Tags carried for traceability, not for a pytest collector.

Feature: Clean test code to testing.md standards without weakening what the tests verify
  As Tess, a test maintainer,
  I want structure-only test refactorings applied only after I approve each diff,
  so I can keep trusting my suite as a safety net.

  # --- S1: Review tests for structure smells -----------------------------------------------
  @us-S1 @review @fixture:05-review-seeds-backlog
  Scenario: A review pass seeds a prioritized backlog
    Given a folder of test files that contain structure smells
    When Tess runs a review of that folder
    Then a test-refactoring backlog is written
    And each item names the file and location, the named move, and a priority
    And only structure-only moves appear — no behaviour changes and no deletions
    And non-test files are left out of the backlog

  # --- S2: Apply one move, human-approved (WALKING SKELETON) --------------------------------
  @us-S2 @walking_skeleton @human-gate @fixture:03-approve-commit-on-green
  Scenario: One approved move is applied, verified, and committed
    Given a test file with a duplicated setup and a green suite
    When the tool proposes a single move to extract the shared setup
    Then Tess sees the named move and a one-line reason, and nothing is committed yet
    When Tess reviews the change in her editor and approves it
    Then the suite is run and stays green
    And exactly one commit is made containing only that change

  @us-S2 @error @human-gate @fixture:04-reject-reverts-clean
  Scenario: A rejected move leaves the suite untouched
    Given a proposed move that keeps the suite green
    When Tess reviews the change and rejects it
    Then the change is undone and nothing is written
    And the item is skipped

  @us-S2 @error @fixture:02-postapply-red-autorevert
  Scenario: A move that breaks the suite is reverted before Tess is asked
    Given a proposed move that silently changes what a test checks
    When the tool applies it and runs the suite
    Then the suite goes red
    And the change is undone automatically and the item is marked blocked
    And Tess is never asked to approve a broken change

  @us-S2 @error @fixture:01-baseline-red-stop
  Scenario: The tool never refactors on a red suite
    Given a suite that is already failing
    When Tess runs the tool
    Then it reports the failing suite and proposes no move
    And nothing is changed or committed

  # --- S3: Work the whole backlog ----------------------------------------------------------
  @us-S3 @loop @requires-human
  Scenario: The backlog is worked one approved move at a time
    Given a backlog with several pending items
    When Tess works the backlog
    Then the tool loops the approved-move cycle over each item in priority order
    And after each landed item it marks any incidentally-resolved items as resolved
    And it reports progress after each item, naming how many are done and what is next

  @us-S3 @loop @requires-human
  Scenario: The loop can be interrupted and resumed
    Given a backlog that is partway worked
    When Tess interrupts the loop
    Then progress is saved
    And a later run resumes from the next pending item without redoing finished ones

  # --- S4: Target a single file or test ----------------------------------------------------
  @us-S4 @scoped @requires-human
  Scenario: Cleanup can be scoped to a single file
    Given a single test file Tess is working on
    When she runs the tool pointed at just that file
    Then detection and moves are scoped to that file only
    And the same approve, verify, revert, and commit guarantees as a full run apply
