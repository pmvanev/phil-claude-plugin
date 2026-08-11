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
5. The roster is written in a second pass, per fixture 10 — slice numbers do not exist until the
   issues do, and neither does the order they are published in.

**Gate failure (blocks the skill change):** an unlabelled guess published as an order; OR the column
left unordered because the schedule is unknown; OR a sequence invented from slice titles, file
timestamps, or a dependency mentioned in a slice file.
