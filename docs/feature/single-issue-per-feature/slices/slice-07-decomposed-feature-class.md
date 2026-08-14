# Slice 07 — The decomposed-feature defect class

**Goal:** Teach the grooming oracle to recognise a feature that was decomposed into slice cards under
retired rules, and to offer consolidation one candidate at a time, ask-first.

**Stories:** S5, S6 · **Subsumes slice 06**, whose scope was this board's migration and which slice 01
found near-empty.
**Backbone activity:** A1 — find the work.

## Why this is a class and not a migration

Slice 05 made the *existing* rules correct under the new paradigm. It did nothing about boards already
shaped by the old ones — and **the skill ships to consumers**, whose boards carry exactly that shape.
Worse, the old rules likely *produced* it: `groom-set`'s split, under the retired *"one issue per
independently demonstrable thing"*, would have cut a feature into precisely the slice cards the new
paradigm wants merged. **Grooming is what encounters the wreckage of its own earlier advice.**

**None of the four existing set-level classes fires on it** — verified against this repo's board
2026-08-14. Not duplicates (a decomposition has no overlapping content to quote), not oversized (each slice
card is small and demonstrable), not overcome by events, not ungrouped effort (they are already grouped).
So the oracle reports such a board **clean**, correctly, and uselessly.

## Learning hypothesis

**Disproves** that this class can be identified reliably enough to offer an irreversible consolidation — if
the evidence cannot separate a decomposed feature from a set of genuinely independent cards, the honest
outcome is to *report* it and never offer, and the whole operation collapses to a finding.
**Confirms**, if it holds, that a board shaped by retired rules can be brought forward without hand
archaeology.

## The class, and its evidence ranked

**N open cards that are slices of one feature.** Evidence, strongest first:

| # | Signal | Weight |
|---|---|---|
| 1 | A real parent/child edge — sub-issues on GitHub | **Sufficient.** The forge asserts it; nothing is inferred. |
| 2 | Bodies naming the same `docs/feature/<id>/` directory | **Sufficient.** The artifacts assert it. |
| 3 | Titles carrying `slice NN` or `<feature> slice NN` | **Report, never offer.** A naming convention is a habit, not a fact. |
| 4 | A shared milestone | **Never evidence.** A milestone is a goal and holds unrelated work by design. |

**Quote the evidence, never characterise it** — the same rule the other four classes carry. "These look
like slices of one feature" is the finding restating its own conclusion.

## The archaeology problem, and why consolidation has three shapes

A previous split *"closed the original as superseded, or kept it as the container the new cards hang
under"*. So the target of a consolidation may already exist, may be closed, or may not exist at all. The
operation must establish which and ask:

- **(a) An open parent exists** → absorb the children into its roster and close them.
- **(b) No parent, but a closed original is findable** → that closed card is probably the right feature
  card. **Reopening is its own hazard**: `gh issue reopen` restores the issue and **not** the Status field,
  so the card lands OPEN while sitting in Done — a combination no view flags (`CLAUDE.md`).
- **(c) Neither** → consolidation requires *creating* the feature card, which is a create, and creates take
  the two-pass discipline for their cross-references.

**Never guess between (a), (b) and (c).** They have different blast radii and (b) is the one a session will
get wrong, because a closed card does not appear in the default list it just read.

## Hazards, inherited and new

1. **Closing children inflates the parent's rollup to 100%.** `subIssuesSummary` counts closed sub-issues as
   completed, so consolidating by closing renders every migrated feature done. **Remove the edge; do not
   merely close the child.**
2. **The un-parent operation is unverified.** Only `--add-sub-issue` and `--parent` have ever been confirmed
   here. See the SPIKE.
3. **Auto-close on Done drops a later comment.** Post the pointer comment *before* closing.
4. **The offer returns every run.** No marker is stored, so a declined consolidation reappears — say so at
   the decline, as every other set-level candidate does.

## IN scope

- The class, its ranked evidence, and the three consolidation shapes, in `groom-issues`.
- The consolidation operation in `/phil:groom-set` — ask-first, one candidate at a time, re-derived between
  candidates.
- A new decision outcome for it, and the `SURFACE-CANDIDATE` reporting path in the scan.
- Fixtures: evidence 1 offered · evidence 3 reported-not-offered · the closed-original case (b) · the
  rollup hazard.

## OUT scope

- Consolidating this repo's board. Every slice card here is already closed, so there is nothing live to
  consolidate; the SPIKE's synthetic pair is the only board write.
- Retro-consolidating closed history. Closed cards are the record of how the work went.
- Any repo other than `pmvanev/phil-claude-plugin`.

## Acceptance criteria

1. A decomposed feature with a real parent edge is **surfaced with its evidence quoted**, and resolving it
   asks before any write.
2. Title-only evidence produces a **report and no offer.** A fixture pins that the offer is withheld.
3. A shared milestone alone produces **nothing** — not a finding, not an offer.
4. The three shapes are distinguished before any write, and case (b) states the reopen/Status hazard.
5. No child is closed while its parent edge still exists.
6. A declined consolidation leaves no trace and says it will return.
7. The un-parent call is verified and recorded with its `gh` version **before** any bulk work.

## Pre-slice SPIKE — RUN 2026-08-14, and it passed

**The un-parent operation exists**, at both levels, on `gh` 2.97.0: GraphQL `removeSubIssue`, and
`gh issue edit --remove-sub-issue <n>` / `--remove-parent`. Confirmed by schema and `--help` inspection,
so hazard 2 is closed.

**The behaviour was measured**, on a throwaway child of #26 (issue #27, since closed):

| Step | `subIssuesSummary` |
|---|---|
| child added, open | `total=1 completed=0 pct=0` |
| **child closed** | `total=1 completed=1 pct=100` |
| **edge removed** | `total=0 completed=0 pct=0` |

So **removal genuinely drops the child from the rollup** rather than hiding it, and the safe order is
**remove the edge, then close the child.** #26 is back to `{0, 0}`, its correct state under this paradigm.

### The hazard is sharper than slice 06 framed it, and it is live on this board

Read `session-handoff` #9 with zero writes: **`total=3 completed=3 percent=100%`**, children #11/#10/#12 all
closed. But **slice 03 of that feature was tested and deliberately NOT built** — its own skill says so in as
many words — and its card #12 is closed all the same.

**The rollup counts *closed*, not *done*.** A won't-build close is indistinguishable from a shipped one, and
#9 has been reporting 100% complete for a feature that shipped two of three slices since the day it closed.
That is not a migration hazard waiting to happen; it is a wrong number on the board now.

Two consequences for this slice: consolidation by closing is doubly wrong — it inflates the count *and* the
inflation is unreadable as inflation — and the fixture for hazard 1 should use **this real case**, not a
constructed one, because a constructed one would have to invent the very ambiguity that already exists here.

## Effort and reference class

~1 day. Reference class: slice 03 of `groom-issues` (the set-level loop), which shipped four ask-first
operations with their evidence rules at about this size.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one class, one operation, four fixtures. |
| Depends on a new abstraction? | No. Consumes the mapping (02) and the oracle (05). |
| Disproves a pre-commitment? | Yes — that the class is identifiable enough to act on. If not, it collapses to a finding. |
| Synthetic data only? | The SPIKE pair is synthetic and labelled; the class definition came off this board's real (closed) structure. |
| Duplicate of another slice at scale? | No. 05 fixed what the rules SAY; this adds a shape they cannot currently see. |
