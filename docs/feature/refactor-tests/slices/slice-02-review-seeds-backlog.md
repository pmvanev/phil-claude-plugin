# Slice 02 — Review pass seeds a backlog

**Goal:** `--review` scans test files and writes a prioritized `.test-refactoring-backlog.md`
covering the full D5 structure-only smell set.

**IN scope**
- `/phil:refactor-tests --review <path>`.
- Detect all D5 smells: duplicated setup, missing AAA, vague name, long test.
- Write `.test-refactoring-backlog.md` with `file:line`, named move, priority (D4).
- Test-file globs match `rules/testing.md` scope.

**OUT scope**
- Applying moves (slices 01/03 own apply).
- Behavior-changing smells / deletion (out of scope, feature-delta).

**Learning hypothesis**
Disproves that a `testing.md`-derived detector produces a useful backlog **if** >20% of
flagged items are false positives on a real suite (KPI: detection precision).

**Acceptance criteria:** S1 AC1.1–AC1.3 (feature-delta.md).

**Production data + dogfood:** run `--review` on this plugin's test tree; hand-audit the
backlog for false positives the same day.

**Dependencies:** slice 01 (command scaffold + test-file detection).

**Effort:** ≤ 1 day. **Reference class:** mirrors `/phil:review-code` producing a backlog,
narrowed to the test-smell taxonomy.

**Pre-slice SPIKE:** none.
