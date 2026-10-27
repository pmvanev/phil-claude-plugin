# Expected outcome — fixture 01 (the opt-out covers checkable expectations only)

The developer answers yes to "trust the tests for the checkable expectations this run?". Two
expectations are checkable; one is qualitative with a developer-confirmed reason.

**Pins:** edd-article-alignment slice 01, AC2.2, D1 — *"Given an opt-out, then no checkable
expectation gets evidence, no qualitative expectation is skipped, and the record states which
expectations were trusted to the tests."* Replaces edd-loop's off-ramp fixture: the run no longer
exits; it builds.

**Expected decision:** `OPT-OUT`.
- The tool asks the opt-out question once, after the classification table.
- The tool marks both checkable rows `trusted to the tests` and commissions evidence for neither; the
  engine's oracle alone proves them.
- The qualitative expectation still gets executed evidence from the non-builder producer and goes to
  the developer to adjudicate.
- The tool delegates the build to nwave — the run does **not** exit after classification.
- The trail names both checkable expectations as trusted to the tests.

**Gate failure (blocks the skill change):** evidence is commissioned for a checkable expectation
after the opt-out; the qualitative expectation is skipped; the record omits which expectations were
trusted to the tests; or the run recommends an engine and exits instead of building.
