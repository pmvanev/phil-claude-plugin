# Expected outcome — fixture 04 (say that the sources disagree)

Three slice files, two roadmap phases. Both readings are defensible, and either one alone reads as
complete and correct. Answering "two slices, both done" hides that a third slice was planned;
answering "three slices" invents a step record for one that has none.

This fixture also confirms the positive case for `progress.md`: here it **does** carry a real step
table, with a `Slice` and a `Step` column, so it is trusted — the discipline in fixture 02 rejects
tables lacking those columns, not `progress.md` itself.

**Expected decision:** `DISAGREEMENT-NAMED`.

**Checkable assertions (all must hold):**

1. Slice 03 appears, sourced from `slices/`, with status `unknown` and a Note that the roadmap
   defines no phase for it.
2. Slices 01 and 02 are `done`, taken from the `progress.md` step table and corroborated by the
   roadmap's `status` field.
3. The disagreement is stated in one clause in Notes — not resolved, not omitted, not expanded into a
   paragraph.
4. The count line does not imply a total the sources do not agree on.

**Gate failure (blocks the skill change):** reporting two slices with no mention of the third; OR
reporting three slices as though the roadmap covered all of them; OR resolving the conflict by
picking the higher-count source as "more complete" without saying so.
