# Slice 06 — Consolidate the existing board

**Goal:** Turn each existing feature-plus-slice-cards group into a single feature card, without the
parent reporting work as finished that is not.

**Stories:** S1, S2 (both read against a board that actually holds feature cards)
**Backbone activity:** A1 — find the work.

> **Added by the amendment pass, 2026-08-14.** The original wave had no migration slice and did not list
> migration as out-of-scope either. It was simply absent.

## Learning hypothesis

**Disproves** the consolidation approach if one feature cannot be consolidated without its parent lying
about completion — in which case the migration needs a mechanism other than closing children, and the
candidates are: relabel-and-leave-open, remove the sub-issue edge before closing, or accept a transient
false rollup and say so on the card.
**Confirms**, if it holds, that the remaining features are mechanical to migrate one at a time.

## Why grooming will not find this

The board holds `session-handoff` #9 with slices #11/#10/#12, `groom-issues` #5 with its slices, and
others. Under [D2] those slice cards should not exist. **Every set-level class comes back negative:**
not duplicates (a legitimate decomposition, no overlapping content to quote), not oversized (each is small
and independently demonstrable — carpaccio guarantees it), not overcome by events, not ungrouped effort
(they are already sub-issues of a parent).

So `/phil:groom-issues` reports the old-paradigm board **clean**, correctly, against its own oracle.
Consolidation is a **one-time migration, not a grooming operation**, and slice 05 must not be stretched to
cover it — an oracle taught to flag correctly-formed cards is the loosening slice 05 exists to refuse.

## The three hazards

1. **Closing slice cards makes every migrated feature read 100% done.** GitHub's `subIssuesSummary`
   counts closed sub-issues as completed. The repo's own measurement is three *open* sub-issues returning
   `{total: 3, completed: 0}` (`gh` 2.97.0, 2026-08-12), so closing all three renders the parent `3/3`,
   100%. Anyone reading the board mid-migration sees finished features. **The sub-issue relationship has
   to go, not just the children's state.**
2. **The un-parent operation is unverified.** The repo has confirmed `--add-sub-issue` and `--parent`
   only. Whatever removes the edge must be checked before it is relied on — this is exactly the
   absolute-negative trap `docs/evolution/2026-08-10-issue-board.md:98-101` records: *"X has no Y" reads
   as settled and gets no re-check.* Verify the removal call and its `gh` version before the first write.
3. **Auto-close on Done is enabled in this repo.** A status write closes the issue and a later
   `gh issue close -c` silently drops its comment. **Post the pointer comment first, then close.**
   Consolidating a dozen slice cards is a dozen chances to lose the record of where the work went.

## IN scope

- **Verify the un-parent call first**, on one card, and record the command and `gh` version. No bulk
  action before that.
- **One feature migrated end to end** as the unit of work: remove the sub-issue edges, post a pointer
  comment on each child naming the feature card and the slice row it became, then close the children,
  then generate the feature card's projection.
- **A pre/post rollup read** on that feature, proving the parent does not report false completion at any
  point in the sequence.
- The remaining features migrated the same way, one at a time.
- A short migration note in `CLAUDE.md`'s *Issue board* section recording that slice cards are historical
  and what replaced them, so a reader finding a closed slice card is not misled.

## OUT scope

- **Deleting anything.** Children are closed with a pointer; their comments are the record of how the work
  actually went.
- **Reopening the paradigm question.** A feature that turns out not to fit one card is a finding for the
  report, not a licence to leave its slices carded.
- Grooming the migrated board (slice 05 settles the oracle; running it is separate), any repo other than
  `pmvanev/phil-claude-plugin`, and automating this across repos.

## Acceptance criteria

1. The un-parent call is verified on one card and recorded with its `gh` version **before** any bulk work.
2. **KPI-2:** each migrated feature has exactly one card.
3. **At no point in the sequence does a migrated feature report completion it has not reached.** Read
   `subIssuesSummary` before, between, and after; if the sequence cannot avoid a transient false rollup,
   the card says so in its projection while the transient lasts.
4. Every closed child carries a comment naming the feature card and the slice row it became, posted
   **before** the close.
5. No child is deleted, and no child's comments are lost.
6. A reader arriving at a closed slice card can find the current home of that work in one hop.
7. The migration states which features it did **not** migrate and why, rather than reporting the board
   consolidated.

## Dependencies

Slices 02 (the mapping is normative), 03 (the columns exist), and 04 (the projection carries content).
Migrating before those three would consolidate cards into a shape nothing yet asserts.

Independent of slice 05 — the oracle's edges and which cards exist are separate concerns.

## Effort

~half a day for the first feature including the verification and the rollup reads; roughly an hour per
feature after that. The first one is the slice; the rest is mechanical.

Reference class: the 2026-08-12 sub-issue verification pass, which created real parent/child cards on this
board and read the GraphQL counters back in one sitting. Same board, same counters, opposite direction.

## Pre-slice SPIKE — yes, and it is small

Hazard 2 is a genuine unknown with a write on the other side of it. Before this slice starts, confirm on
one throwaway parent/child pair that the un-parent operation exists, and whether removing the edge alone
drops the child out of `subIssuesSummary`. If removal does not exist, the sequence changes and the
hypothesis fires at the cheapest possible moment.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — no new prose surface at all. One verified call, one sequence, one `CLAUDE.md` note. |
| Depends on a new abstraction? | No. Depends on the projection from 04, which ships before it. |
| Disproves a pre-commitment? | Yes — that consolidation is possible without a false rollup. It is the one slice whose failure changes the mechanism rather than the wording. |
| Synthetic data only? | No — the real board, and the SPIKE's throwaway pair is explicitly labelled as the exception. |
| Duplicate of another slice at scale? | No. 05 changes what the oracle says; this changes which cards exist. |
