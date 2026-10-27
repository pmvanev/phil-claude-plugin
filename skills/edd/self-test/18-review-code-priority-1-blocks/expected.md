# Expected outcome — fixture 18 (review-code's serious findings block; advisories go to their owners)

`phil:review-code` runs once on each changed file, and the run's `Scope:` blocks hold four items.

**Pins:** edd-article-alignment slice 03, AC4.3 + AC4.4 — Priority 1, or Priority 6 on a pinning
test, blocks done until fixed or waived; advisory findings go to the skill that owns them.

**Expected decision:** `REVIEW-CODE-GATE`.
- R001 (Priority 1, CWE-22 — not an `Advisory`) blocks done and goes to FINDINGS. Avery waives it with
  a reason; the record keeps R001, the reason and a timestamp.
- R004 (Priority 6, Eager Test) sits in `tests/acceptance/test_export.py`, which holds the pinning
  test `test_dry_run_lists_paths`, so it blocks too. Avery answers `fix`; the engine splits the test.
  The change touches only test files, so it is not a rebuild: STABILIZE re-checks the pins and re-runs
  `phil:review-code`, and R004 clears only when the re-run does not reproduce it. The runs on
  `src/export.py` and `test_export.py` may both file R004; they are one finding.
- Only after FINDINGS clears both does REPAIR offer the advisories, grouped by smell rather than by
  Route: R003 (a redundant comment, Priority 5) to `phil:clean-comments`, run first — with the gate
  this skill supplies (the suite, then Avery's approval of the diff) and a commit of the approved
  diff — then R002 (a naming smell) to `phil:refactor`.
- `stabilize.md` records every item, the waiver, the fix, and each repair run.

**Gate failure (blocks the skill change):** R001 or R004 is offered as a repair or ignored; R004 clears
on the engine's word, or as a rebuild that re-runs REVIEW; a repair runs before FINDINGS clears the
blockers; `phil:refactor` runs before `phil:clean-comments`; R003 goes to `phil:refactor`
because its Route says so; or `phil:clean-comments` runs with no suite and no approval.
