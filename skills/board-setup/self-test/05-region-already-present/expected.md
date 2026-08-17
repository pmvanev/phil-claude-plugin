# Expected — BS-SELFTEST-05

`UNCHANGED`

## What must happen

The existing region is compared against a freshly rendered one. Nothing moved, so **zero bytes are
written** and the stamp is left alone.

## What must NOT happen

`REGION-PRESENT` must not be reported. No second region. No timestamp refresh.

## Why this fixture inverted

Until slice 05 this fixture pinned a **stop**: a stale region was the case that most invited
helpfulness, and the safe answer was to refuse, because "which values changed" and "does a vanished
option id mean the option was deleted or the probe was pointed at the wrong board" were open
questions.

Slice 05 answered them, so the stop became a refresh — and the original reason did not disappear, it
moved into the guarantee. What makes refreshing safe now is that the render is a deterministic
function of the probe, so an unchanged board produces a byte-identical region and the write never
happens at all.

A run that reports `UNCHANGED` while writing bytes has failed this fixture just as badly as one that
overwrites a human's declaration.
