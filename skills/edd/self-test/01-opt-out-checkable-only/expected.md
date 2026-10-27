# Expected outcome — fixture 01 (the opt-out covers checkable expectations only)

The developer answers yes to "trust the tests for the checkable expectations this run?". Two
expectations are checkable; one is qualitative with a developer-confirmed reason.

**Pins:** edd-article-alignment slice 01, AC2.2, D1 — *"Given an opt-out, then no checkable
expectation gets evidence, no qualitative expectation is skipped, and the record states which
expectations were trusted to the tests."* Replaces edd-loop's off-ramp fixture: the run no longer
exits; it builds.

**Expected decision:** `OPT-OUT`.
- The opt-out question is asked once, after the classification table.
- Both checkable rows are marked `trusted to the tests`; no evidence is commissioned for either, and
  the engine's oracle alone proves them.
- The qualitative expectation still gets executed evidence from the non-builder producer and goes to
  the developer to adjudicate.
- The build is delegated to nwave — the run does **not** exit after classification.
- The trail names both checkable expectations as trusted to the tests.

**Gate failure (blocks the skill change):** evidence is commissioned for a checkable expectation
after the opt-out; the qualitative expectation is skipped; the record omits which expectations were
trusted to the tests; or the run recommends an engine and exits instead of building.
