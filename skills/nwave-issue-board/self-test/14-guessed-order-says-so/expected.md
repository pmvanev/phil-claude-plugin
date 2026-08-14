# Expected outcome — fixture 14 (a guess published as a schedule)

No `roadmap.json` means no sequence has been decided. Slice file numbers are the only signal, so
they are the right order to publish — declining to order the column just hands the decision to
creation time, which knows less.

The failure is not the guess. It is publishing the guess in the form a decided order takes: three
cards in a column, indistinguishable from a sequence someone agreed to, one wave before anyone did.

**Expected decision:** `ORDER-STATED-AS-PROVISIONAL`.

**Checkable assertions (all must hold):**

1. Cards are positioned `01, 02, 03` — slice file number ascending.
2. The roster carries the basis, in words: `Order: slice number, provisional until /nw-roadmap`.
3. The order is never described as the roadmap's, the plan's, or the sequence.
4. No step rows are invented, per fixture 07. The absent roadmap constrains both.
5. The roster is generated in one pass; there are no slice numbers to wait for — slice numbers do not exist until the
   issues do, and neither does the order they are published in.

**Gate failure (blocks the skill change):** an unlabelled guess published as an order; OR the column
left unordered because the schedule is unknown; OR a sequence invented from slice titles, file
timestamps, or a dependency mentioned in a slice file.

## Amended 2026-08-14 — no slice issues are created, and the "final" case

Two changes, neither touching what this fixture pins.

**No slice issues.** The situation said the feature issue *and three slice issues* are created by the
invocation. Only the feature issue is created now; the three slices become roster rows. The provisional-order
line moves from beside a GitLab roster of bare references to beside the generated roster, and applies on both
forges identically.

**The line has a second form.** `Order: slice number, provisional until /nw-roadmap` promises a correction.
Where `/nw-roadmap` will never run, write `Order: slice number — final; /nw-roadmap does not run in this
repo` instead. Additional gate failure: **writing "provisional until /nw-roadmap" where nothing will ever
supersede it** — an order that advertises a correction it will never receive is worse than one that admits it
is final, because a reader defers to it while waiting.
