# Expected outcome — fixture 09 (do not hand-build what the forge maintains)

**Where it fails silently.** A roster table in the feature description looks helpful and renders
correctly. It is also a second copy of the parent's own child list — and the copy that nobody
regenerates when a slice is added, renamed, or closed. Within a week the description and the sub-issue
list disagree, and the description is the one people read first.

**Expected decision:** `NATIVE-HIERARCHY`.

**Checkable assertions (all must hold):**

1. The four slice issues are attached to the feature as sub-issues, using the commands in
   `phil:issue-board`.
2. The feature description contains **no** roster table of slice references.
3. The wave label and any generated block on the feature issue are unaffected — the rule removes the
   duplicated roster, not the wave.
4. Nothing here restates the sub-issue commands or the `gh` version they were verified against; those
   live in `phil:issue-board`.

**Gate failure (blocks the skill change):** a roster table written into the feature description on a
forge whose parent already rolls up children; OR slices left unattached because the roster was
skipped.
