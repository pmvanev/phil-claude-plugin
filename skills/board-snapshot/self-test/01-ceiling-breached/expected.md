# Expected — BSNAP-SELFTEST-01

`SNAPSHOT-CLIPPED` · `READ-ONLY`

## What must happen

All 7 blocked cards render, each naming what it waits on, quoted from its `## Chain` line. All 6
in-flight cards render. Those two sections alone consume most of the budget. The queued section prints **fewer than the 5 requested** and states the number
withheld — "37 more queued" or equivalent, as a number rather than "and others".

The whole rendered output, counted including the report lines, is **at or under 200 words**.

## What must NOT happen

The ceiling is not breached. No blocked or in-flight card is dropped — the queued section is the only one
that gives ground, because it is the only one with a defensible stopping point.

The run does not report `SNAPSHOT-RENDERED`. Clipping is a different outcome and hiding it inside the
successful one is the failure this fixture is for.

## Why this fixture exists

This is the only path the ceiling actually governs, and it is unreachable from the live board. A suite
built only from real data would report green while never having tested the feature's central constraint.

It is sized so the mandatory sections consume most of the budget and stay inside it — the ordinary clip,
where the queued section gives ground and the ceiling holds. Fixture 13 carries the case where they do
not fit, which has the opposite answer. **The first sizing of this fixture was wrong** — 3 blocked and 4 in flight could not breach
200 words at all, so the fixture claimed to test a clip it could never provoke. `tests/` caught it before
the suite was trusted, which is the reason that check exists.
