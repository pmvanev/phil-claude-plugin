# Expected — BS-SELFTEST-04

`MALFORMED-MARKERS`

## What must happen

Refuse. The file is byte-unchanged. The reason names the shape found — `begin` with no `end`,
nested markers, or an `end` preceding its `begin`.

## What must NOT happen

**No inference of the region's extent.** Not by scanning to the next heading, not to the next blank
line, not to end-of-file. No repair by inserting a closing marker. No region written anywhere.

## Why this fixture exists

Guessing an extent is how prose gets deleted. Everything between an inferred `begin` and an
inferred `end` is treated as generated and therefore disposable — and in this feature's target
files, the text most likely to sit there is a hazard recorded after contact that no probe can
regenerate.

A repair is worse than a refusal for the same reason: inserting an `end` marker decides where the
region stops, which is exactly the judgement that was unavailable.

The failure is silent either way. A file with a guessed region looks like a file with a region.
