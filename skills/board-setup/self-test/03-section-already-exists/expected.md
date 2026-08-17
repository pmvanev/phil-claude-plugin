# Expected — BS-SELFTEST-03

`WROTE-BESIDE-PROSE`

## What must happen

The region is inserted immediately after the `## Issue board` heading. Every byte outside the
markers is unchanged — verifiable by excising the region and comparing to the original. The three
drift bucket counts are reported, and any contradiction is listed in full rather than counted.

## What must NOT happen

No second `## Issue board` section. No hand-written bullet edited, reflowed or retired without an
explicit answer. No blank line added around the region: readability outside the markers is not this
command's to spend, and a blank line is a byte that was not there before.

**`SECTION-EXISTS` must not be reported.** It is retired.

## Why this fixture changed

Until slice 02, this was the case where the temptation was strongest and the damage was worst: the
probe had succeeded, the values were in hand, and the existing section was *right there*. The
answer was to stop.

Slice 02 is that thing, so the fixture inverts — but the reason it existed does not go away, it
moves into the guarantee. This repo's own block is still the hardest case in existence: mostly
prose recorded after contact, and **no probe can reproduce a line of it**. What makes insertion
safe now is not confidence, it is AC1 — content outside the markers byte-identical on every path,
held by a script and checked before anything reaches disk.

A run that inserts correctly but reflows one bullet has failed this fixture just as badly as one
that overwrites the section.
