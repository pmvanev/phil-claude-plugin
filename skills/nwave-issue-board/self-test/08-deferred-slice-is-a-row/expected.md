# Expected — 08 (a deferred slice is a row, not a silence)

> **Rewritten 2026-08-14.** This fixture was `08-deferred-slice-not-a-card` and asserted that a deferred
> slice gets **no card**, because a card on a board does not misinform someone — it assigns them. That
> reasoning was right and the mechanism is gone: there are no slice cards to withhold.

**Expected outcome:** `DEFERRED-ROW-NOT-OMITTED`. Slice 03 appears in the roster with a `⊘` glyph and a
note naming the deferral, and **slice 04 is what the reader is pointed at next.**

**This is strictly better than the old behaviour, and worth saying so.** Withholding the card kept anyone
from being assigned deferred work, but it also erased the slice: a reader saw slices 01, 02, 04, 05 and had
no way to know 03 existed, was considered, and was set aside. The row says all three.

`phil:nwave-slice-status` treats the `DEFERRED` marker as overriding every other source; honour what it
returns rather than re-deriving.

**Gate failures:**

- Omitting the row. The old rule's letter, applied where its reason no longer holds.
- Giving slice 03 a `·` glyph. *Not started* invites someone to start it.
- Pointing the reader at slice 03 as current or next.
- Renumbering the remaining slices to close the gap. The numbers are the briefs' and are not this
  skill's to reassign.
