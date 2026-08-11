# Expected outcome — fixture 04 (say that the sources disagree; never schedule deferred work)

Three slice files, two roadmap phases. Both readings are defensible and either alone reads as
complete: "two slices, both done" hides that a third was planned, while "three slices, one to go"
schedules work the project explicitly dropped.

Slices 01 and 02 are done, so slice 03 is the first not-done slice — which is exactly what a
positional rule would call `next`. Its own file says **do NOT build in this cycle**. This is the
worst output the skill can produce: it does not merely misreport, it directs the user to do
abandoned work.

This fixture also confirms the positive case for `progress.md`: here it **does** carry a real step
table with `Slice` and `Step` columns, so it is trusted. The discipline in fixture 02 rejects tables
lacking those columns, not `progress.md` itself.

**Expected decision:** `DISAGREEMENT-NAMED`.

**Checkable assertions (all must hold):**

1. Slice 03 is `deferred`. Never `next`, never `current`, never `not started`.
2. Its deferral is visible in the output — the marker is the reason, and a bare `deferred` with no
   cause invites the user to override it.
3. Slices 01 and 02 are `done`, from the `progress.md` step table, corroborated by the roadmap.
4. The roster disagreement is stated in one clause: three slice files, two roadmap phases.
5. The goal line is found despite the `**Goal (one sentence):**` format — a matcher keyed to the
   literal `**Goal.**` finds nothing here and must not silently omit the intent line.
6. The count line does not imply a total the sources do not agree on, and does not count the deferred
   slice as outstanding work.

**Gate failure (blocks the skill change):** slice 03 reported as `next` or `current`; OR reporting
two slices with no mention of the third; OR resolving the conflict by preferring the higher-count
source without saying so; OR omitting the goal line because the format did not match.
