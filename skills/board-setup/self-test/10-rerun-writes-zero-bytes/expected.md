# Expected — BS-SELFTEST-10

`UNCHANGED`. Zero bytes written.

## What must happen

Nothing is written — not one byte, including the stamp. `git diff --stat` is empty. The report says
the board has not moved, and distinguishes that from a stamp-only difference.

## The timestamp decision, which this fixture pins

**The stamp is not refreshed on a no-change run.** The brief required this be decided rather than
left open, and the two candidate answers are not equivalent: excluding the stamp from the *comparison*
while still *writing* it would fail KPI-3 while looking correct.

## What must NOT happen

`REGION-PRESENT` must not be reported — it is retired, having been slice 02's way of deferring to the
re-run that now exists.

And **`unchanged` must never be rendered for a probe that could not be read.** Those are the two most
different answers this step can give: one says the board is as recorded, the other says nobody knows.

## Why this fixture exists

This is what turns the command from a scaffolder into a check. A command that must be run once at
adoption gets run once; one that can be run habitually gets run habitually — but only if a re-run is
quiet.

A run that rewrites the file to move a clock produces a diff every time. The diffs stop being read,
and the block decays into issue #31's unnoticed-stale state **while looking maintained**, which is
worse than looking neglected.
