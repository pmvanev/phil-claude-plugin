# Acceptance specification — phil:redesign-tests
#
# Scenario SSOT for the feature. Business language only (DISTILL Pillar 1); the mechanics live in
# the self-test fixtures (self-test/) and, at runtime, in SKILL.md.
#
# These scenarios are validated two ways:
#   - deterministic safety mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - human-gated + detection scenarios -> same-day dogfood on this plugin's own tests (the slices)
# There is no CI runner in this plugin; the fixtures are driven by a human or the model, exactly as
# refactor/self-test/ and refactor-tests/self-test/ are. Tags carried for traceability, not a collector.
#
# KEY DIFFERENCE from refactor-tests: the proposed moves DELIBERATELY CHANGE what a test verifies
# (implementation -> behaviour). The human is the SOLE oracle, so every proposal carries a
# coverage-equivalence claim the human validates (ADR-004).

Feature: Rewrite tests that verify implementation into tests that verify behaviour
  As Tess, a test maintainer,
  I want behaviour-changing test rewrites applied only after I approve each diff and its
  coverage-equivalence claim,
  so my suite survives refactoring and catches real regressions instead of noise.

  # --- S2: Review tests for behavioural smells ---------------------------------------------
  @us-S2 @review @fixture:05-review-seeds-backlog
  Scenario: A review pass seeds a prioritized behavioural backlog
    Given a folder of test files that contain behavioural smells
    When Tess runs a review of that folder
    Then a separate test-redesign backlog is written
    And each item names the file and location, the smell type, and the proposed rewrite intent
    And only behavioural smells appear — implementation-coupling, excessive mocking, flakiness
    And non-test files are left out of the backlog

  # --- S1: Rewrite one coupled test, human-approved (WALKING SKELETON) ----------------------
  @us-S1 @walking_skeleton @human-gate @fixture:03-approve-commit-on-green
  Scenario: One approved behavioural rewrite is applied, verified, and committed
    Given a test that asserts on how the code works and a green suite
    When the tool proposes a single rewrite that asserts on the observable outcome instead
    Then Tess sees the rewrite, a one-line reason, and a coverage-equivalence claim, and nothing is committed yet
    When Tess reviews the change in her editor and approves it
    Then the suite is run and stays green
    And exactly one commit is made containing only that change

  @us-S1 @error @human-gate @fixture:04-reject-reverts-clean
  Scenario: A rejected rewrite leaves the suite untouched
    Given a proposed rewrite that keeps the suite green
    When Tess reviews the change and rejects its coverage-equivalence claim
    Then the change is undone and nothing is written
    And the item is skipped

  @us-S1 @error @fixture:02-postapply-red-autorevert
  Scenario: A rewrite that breaks the suite is reverted before Tess is asked
    Given a proposed rewrite that gets the new assertion wrong
    When the tool applies it and runs the suite
    Then the suite goes red
    And the change is undone automatically and the item is marked blocked
    And Tess is never asked to approve a broken change

  @us-S1 @error @fixture:01-baseline-red-stop
  Scenario: The tool never redesigns on a red suite
    Given a suite that is already failing
    When Tess runs the tool
    Then it reports the failing suite and proposes no rewrite
    And nothing is changed or committed

  # --- S3: Excessive-mocking rewrites ------------------------------------------------------
  @us-S3 @mocking @fixture:06-missing-fake-skips
  Scenario: An over-mock rewrite that needs a non-existent fake is skipped, not scaffolded
    Given an over-mocked test whose behavioural rewrite would need a fake that does not exist
    When the tool considers the rewrite
    Then it surfaces that the fake is missing and skips the item
    And it never invents unreviewed test scaffolding

  # --- S3/S4: The behavioural families are worked one approved rewrite at a time ------------
  @us-S3 @us-S4 @loop @requires-human
  Scenario: The backlog is worked one approved rewrite at a time
    Given a backlog with several pending behavioural items
    When Tess works the backlog
    Then the tool loops the approved-rewrite cycle over each item in priority order
    And after each landed item it marks any incidentally-resolved items as resolved
    And it reports progress after each item, naming how many are done and what is next

  # --- S4: Flakiness rewrites carry an extra stability check --------------------------------
  @us-S4 @flakiness @requires-human
  Scenario: A determinism rewrite is confirmed stable before Tess is asked
    Given a flaky test that depends on the current time or unseeded randomness
    When the tool proposes a deterministic rewrite
    Then it runs the suite several times to confirm the flake is gone before pausing for approval
    And if stability cannot be confirmed the item is reverted and marked blocked

  # --- Scoped mode -------------------------------------------------------------------------
  @us-S1 @scoped @requires-human
  Scenario: Redesign can be scoped to a single file or test
    Given a single test Tess is working on
    When she runs the tool pointed at just that file or test
    Then detection and rewrites are scoped to that target only
    And the same approve, verify, revert, and commit guarantees as a full run apply
