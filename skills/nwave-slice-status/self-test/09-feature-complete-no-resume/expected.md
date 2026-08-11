# Expected outcome — fixture 09 (finished work has nothing to resume)

"`current` is the first step that is not done" has no answer here. An instruction that always
produces a `current` row and always prints a resume command will invent both — pointing the user at
`/nw-continue` for a feature with nothing left, which either wastes their time or starts a wave on
finished work.

**Expected decision:** `COMPLETE`.

**Checkable assertions (all must hold):**

1. Every row is `done`. No row is `current` or `next`.
2. Each slice closes with `slice complete`, and the feature closes with `feature complete`.
3. No resume command appears anywhere in the output.
4. The count lines are consistent and label their scope — per-slice counts plus one feature-level
   count, each matching the rows above it.

**Gate failure (blocks the skill change):** a `current` row chosen by position from a table of
finished steps; OR a `resume with: /nw-continue …` line on a complete feature; OR closing with a
congratulatory summary, which is still commentary the user did not ask for.

**Boundary.** `feature complete` is a claim about the record, not the software. When the record says
every step is done, say so — do not soften it with speculation about work that might remain, and do
not verify it by running anything.
