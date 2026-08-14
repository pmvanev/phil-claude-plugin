# Expected — 13 (array order beats the numbers that agree with each other)

> **Rewritten 2026-08-14.** This fixture was `13-order-follows-roadmap` and pinned the *board column's*
> order across four slice cards, via `reprioritizeSubIssue`. There are no slice cards now, so the same
> assertion moves to the roster rows — and the mutation it depended on, **never exercised against a real
> board**, is no longer needed by anything.

**Expected outcome:** `ROSTER-ORDER-FOLLOWS-ROADMAP`. Roster rows render **01, 03, 02, 04**.

**Why this is still the suite's subtlest ordering case.** Two independent signals — the slice file numbers
and their natural sort — agree with each other and disagree with `phases[]`. Nothing errors either way, and
the wrong order is the one that looks tidy. `phases[]` decides; a `deps` entry or a sequence implied in a
brief does not override it.

**What got cheaper.** The old version needed a per-sub-issue position write, and GitHub's board column and
sub-issue list were two separate orders that had to be set independently. A generated table has one order
and it is the array's.

**Gate failures:**

- Rendering 01, 02, 03, 04 — the file-number order, which both other signals endorse.
- Sorting by anything derived from the issue itself. There is one issue.
- Reordering to put `▶ current` first. Position carries the schedule, not the status.
