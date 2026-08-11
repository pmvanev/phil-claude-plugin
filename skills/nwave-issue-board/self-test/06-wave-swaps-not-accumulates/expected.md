# Expected outcome — fixture 06 (the wave is single-valued)

**Where it fails silently.** Adding a label always succeeds. On a forge without scoped labels nothing
drops the sibling, so a feature walked through four waves ends up carrying four wave labels — and the
question the label exists to answer, *where is this feature*, no longer has one answer. Every command
along the way reported success.

**Expected decision:** `WAVE-SWAPPED`.

**Checkable assertions (all must hold):**

1. After the transition the feature issue carries exactly one wave label, for DELIVER.
2. The removal happens in the same call as the addition, per `phil:issue-board`'s rule that a label
   swap is one operation.
3. The three stale wave labels are removed, not left because "only the newest matters".
4. The generated block's wave line agrees with the label. Both are written in the same operation.

**Gate failure (blocks the skill change):** more than one wave label after the transition; OR a label
added with no corresponding removal; OR the block and the label disagreeing.
