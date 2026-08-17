# Expected — BS-SELFTEST-05

`REGION-PRESENT`

## What must happen

Stop, changing nothing. Name **slice 05** as the owner of re-run and staleness, so the outcome
reads as a boundary rather than a breakage.

## What must NOT happen

No rewrite of the existing region, even when the probe returned different values — *especially*
then. No second region. No comparison-and-repair.

## Why this fixture exists

A stale region is the case that most invites helpfulness, and slice 05 exists because the safe
answer is not obvious: which values changed, whether a vanished option id means the option was
deleted or the probe was pointed at the wrong board, and whether a re-run should write zero bytes
when nothing moved.

Answering any of that here means inventing slice 05 mid-run, undefined and reporting success. The
skill says outright that running twice is undefined until slice 05 ships, and this is the fixture
that keeps that promise honest.
