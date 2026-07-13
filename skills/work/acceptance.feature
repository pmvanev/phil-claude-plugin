# Acceptance specification — phil:work
#
# Scenario SSOT for the feature. Business language only (per DISTILL Pillar 1); the mechanics
# live in the self-test fixtures (self-test/) and, at runtime, in SKILL.md (built in DELIVER).
#
# Validated two ways, exactly as refactor-tests/redesign-tests are:
#   - deterministic safety mechanics -> the golden fixtures under self-test/ (see each @fixture tag)
#   - human-gated / judgment scenarios -> same-day dogfood on this plugin's own initiatives (the slices)
# There is no CI runner in this plugin; the fixtures are driven by a human or the model, exactly
# as refactor/self-test/ is. Tags carry traceability, not a pytest collector.
#
# The software under test is the ORCHESTRATOR's decision behaviour: what it frames, how it routes,
# and — above all — that a delegate failure never leaves the tree red and a missed goal is never
# reported as done. These bugs are silent: a decorative gate looks exactly like a smooth run.

Feature: Carry an invisible technical initiative through with discipline
  As Quinn, a codebase steward,
  I want a wave-based workflow that frames, plans, and sequences the work and delegates each
  wave to the right existing skill,
  so I can carry refactors, re-architectures, and cleanups through safely with a decision trail —
  never claiming done when behaviour broke or the goal was missed.

  # --- FRAME: scope the initiative --------------------------------------------------------
  @slice-01 @slice-04 @frame @error @fixture:01-frame-refuses-vague-goal
  Scenario: The tool refuses to start on an uncheckable goal
    Given an initiative whose goal cannot be checked (for example "make it better")
    When Quinn starts the workflow
    Then the tool declines to proceed
    And it asks for a checkable goal, or offers to continue on a behaviour-preservation-only basis
    And nothing is changed until a checkable goal or preservation-only is agreed

  @slice-01 @frame @offramp @fixture:02-frame-offramp-trivial
  Scenario: A trivial initiative is sent straight to a single skill, with no ceremony
    Given an initiative small enough for one existing tactical skill to handle
    When Quinn starts the workflow
    Then the tool recommends running that one skill directly
    And it exits without framing, planning, or opening a decision trail

  # --- WALKING SKELETON: one initiative, end-to-end ---------------------------------------
  @slice-01 @walking_skeleton @fixture:03-walking-skeleton-end-to-end
  Scenario: One initiative is carried end-to-end through a single delegated skill
    Given a real initiative with a checkable goal and a passing preservation oracle
    When Quinn runs the workflow and confirms the framed goal and preservation contract
    Then the tool delegates the change to one existing skill
    And the preservation oracle still passes afterwards
    And a decision record is written for the initiative
    And Quinn sees a summary naming the goal, the preservation result, and the commit made

  # --- EXECUTE: route each wave to the skill that owns the right gate ----------------------
  @slice-05 @execute @routing @fixture:04-route-code-to-loop
  Scenario: A code change is handed to the gated code-refactoring loop
    Given a wave that changes executable code
    When the tool executes that wave
    Then it delegates to the code-refactoring loop whose test-suite gate is the preservation oracle
    And the tool does not run a preservation gate of its own

  @slice-05 @execute @routing @fixture:05-route-prose-to-approval
  Scenario: A prose change is handed to the approval-based cleaner
    Given a wave that changes a prose artifact such as a skill, rule, or agent
    When the tool executes that wave
    Then it delegates to the approval-based cleaner whose human diff review is the preservation oracle
    And the tool does not run a preservation gate of its own

  # --- SEQUENCING GATE: a delegate failure never leaves the tree red ----------------------
  @slice-02 @execute @error @fixture:06-delegate-failure-leaves-last-good
  Scenario: A failed wave stops the sequence and leaves the tree in its last-good state
    Given a roadmap of several waves
    When a wave's delegate fails (its suite goes red, its self-test breaks, or its diff is rejected)
    Then the tool stops the sequence at that wave
    And the working tree is left in its last-good state, never red
    And the failure is recorded, and later waves are not run
    And the run is not reported as done

  # --- VERIFY: honesty about the goal -----------------------------------------------------
  @slice-04 @verify @error @fixture:07-verify-reports-goal-not-met
  Scenario: A run that preserves behaviour but misses the goal is reported as not achieved
    Given a completed sequence whose preservation oracle passed
    But whose declared goal metric was not reached
    When the tool verifies the initiative
    Then it reports the goal as not achieved, with the metric reading as evidence
    And it does not report the initiative as done
