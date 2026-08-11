# Expected outcome — fixture 10 (a missing step record does not erase the roster)

This is where two instructions can pull opposite ways. The slice roster is called the most reliable
source available, and the degradation rule fires on "no roadmap and no progress file". Read
carelessly, the second discards what the first just established, and the user is told there is
nothing here while three well-formed slice files sit on disk.

**Expected decision:** `ROSTER-ONLY`.

**Checkable assertions (all must hold):**

1. Three rows, one per slice file, each carrying its goal line.
2. Every status is `unknown` — no step record exists, and no status may be inferred from the slice
   files, which describe intent rather than progress.
3. One line states that the feature has no step-level record, and suggests `/nw-roadmap`.
4. The roster is not discarded, and the output is not reduced to a list of wave directories. That
   response belongs to fixture 07, where `slices/` is absent too.

**Gate failure (blocks the skill change):** reporting "no step-level record" while suppressing the
three slices; OR inferring status from the presence of IN/OUT scope prose; OR marking the slices
`not started`, which claims the work has not begun when the record simply does not say.
