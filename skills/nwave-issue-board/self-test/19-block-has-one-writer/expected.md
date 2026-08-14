# Expected — 19 (one writer, whole block, two sources)

**Pins:** *one writer owns the whole block* — added 2026-08-14 after the first live run did it the other way.

**Expected outcome:** `WHOLE-BLOCK-REGENERATED`. The block is rewritten in full between its markers, with
position read fresh from `phil:nwave-slice-status` and reasoning read fresh from `.session-handoff.md` —
**both, on every refresh, even though only one of them changed.**

**Why re-reading the unchanged source is the point.** The tempting optimisation is to refresh only what
moved: rewrite the roster, leave the reasoning alone. That works, and it works by *care* rather than by
construction — two writers in one delimited region, kept apart by whoever happens to be paying attention.
The first live projection of a handoff did exactly this, appending inside the markers and preserving the
position by hand. It succeeded, which is what makes the pattern dangerous: nothing failed, so nothing said
the discipline was load-bearing.

**What breaks when the discipline lapses.** The next writer that regenerates the block *properly* — from its
own single source — silently drops whatever the other one had put there. On this card that means a position
refresh erases the why, the next action and the stack: **the only record of reasoning that no artifact
holds**, deleted by a routine boundary refresh that reports success.

**Where a source is absent, its section renders `unknown`** rather than being omitted or preserved stale.
That is precisely what makes whole-block regeneration safe: there is no case where regenerating destroys
information, because a missing source produces an honest section rather than a gap the writer is tempted to
fill from the old copy.

**Gate failures:**

- Refreshing the position and leaving the reasoning untouched — the pattern this fixture exists to forbid,
  and the one that reads as an optimisation.
- Preserving the previous reasoning by copying it out of the rendered block and back in. That treats the
  card as a source, which inverts the one-way rule: the block is a projection, never an input.
- Introducing a second marker pair so each writer owns a region. Two regions is two writers with extra
  steps, and it doubles the ways a description rewrite can go wrong.
- Rendering the unchanged reasoning with a *new* capture timestamp. The timestamp belongs to the snapshot,
  not to the refresh; bumping it claims the reasoning was re-witnessed.
