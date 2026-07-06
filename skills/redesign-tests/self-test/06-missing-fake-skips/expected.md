# Expected outcome — fixture 06 (over-mock rewrite needs a missing fake → SKIP)

Baseline is green: `test_place_charges_and_saves` passes with both collaborators mocked. The item
is a genuine excessive-mocking smell — but a faithful behavioural rewrite needs a
`FakePaymentGateway` to observe the charge, and the SUT ships no such fake (and no gateway safe to
call for real).

**Pins:** AC3.2 — *"If a rewrite needs a fake/collaborator that does not already exist, the tool
surfaces that and **skips** the item rather than inventing unreviewed scaffolding."*

**How the loop drives it:** consider the rewrite named in the manifest. Detect that
`fake_required` is set and `fake_exists: false`.

**Expected gate outcome:** `SKIP`. The tool reports that the rewrite is blocked on a missing fake
(`FakePaymentGateway`), marks the item `skipped (missing fake)`, and moves on. **No test file is
written and no fake class is invented.**

**Gate failure (blocks the skill change):** the tool writes a new `FakePaymentGateway` (or any test
double) that was never reviewed; applies a partial rewrite that drops the charge assertion silently
(that would be silent coverage loss — the exact D7 risk this feature guards against); or edits the
SUT to add a fake. Any of these means the skip-not-scaffold guard is decorative.
