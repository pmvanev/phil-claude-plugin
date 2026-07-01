# Slice 03 — Work the whole backlog

**Goal:** Loop the slice-01 move over every pending backlog item until the suite is clean,
with prune and progress reporting.

**IN scope**
- `/phil:refactor-tests` (no arg) works the existing `.test-refactoring-backlog.md`.
- Per-item propose→approve→apply→suite→commit loop, priority order.
- Prune pass: mark incidentally-resolved items `resolved (incidental)`.
- Progress reporting; interrupt-safe resume.

**OUT scope**
- New smell types beyond D5.
- Single-target mode (S4 — thin add-on, can fold into slice 01's arg handling).

**Learning hypothesis**
Disproves that the loop stays coherent across many items **if** backlog/state tracking drifts
(items double-applied, prune misfires, or resume loses place).

**Acceptance criteria:** S3 AC3.1–AC3.4 (feature-delta.md).

**Production data + dogfood:** run the full loop against this plugin's test suite from a
slice-02 backlog; confirm a measurably cleaner suite the same day.

**Dependencies:** slices 01 (apply loop) + 02 (backlog).

**Effort:** ≤ 1 day. **Reference class:** mirrors `phil:refactor`'s backlog loop (Phases
7–8) with the approval gate from slice 01.

**Pre-slice SPIKE:** none.
