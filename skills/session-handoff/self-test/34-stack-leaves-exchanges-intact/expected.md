# Expected — 34 (the stack verbs leave the exchanges alone)

**Expected decision:** `PUSHED` (run A), then `POPPED` (run B).

## Run A

`## Stack` is created with one frame, `crossed 0`, **before** `<!-- session-handoff:exchanges -->`. The
region stays last in the file and byte-identical, header reproduced byte-for-byte.

## Run B

The frame goes, and with it the `## Stack` section. The why and next action exist, so the file stays.
The region is again byte-identical and last.

## Gate failures

- **Appending the stack after the closing marker.** It sits where no reader of the sections looks, and
  the region is no longer last.
- **Treating the reply's `## Findings` as a section**, for instance by writing the stack beneath it.
  Only the markers bound the region; a heading inside it belongs to the reply.
- **Any change inside the markers.** Whole-file regeneration is the natural way to lose one.
