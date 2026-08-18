# Expected — 22 (three old frames, one stale)

**Pins:** slice-02 AC3 and AC4, and issue #29's done-when — *"a never-popped frame is visible as stale
rather than silently wrong."*

**Expected decision:** `SHOWN`. All three frames are more than a day old. Exactly one is marked:

```
SHOWN — 3 deep

1. Wave-to-command table · the task in hand · open 51h25m · crossed 2   ⚠ stale
2. └ Fixture 07 · it contradicted the table, so it had to be settled first · open 48h50m · crossed 1
3.   └ The fixture runner · it needed a flag it did not have · open 48h25m · crossed 1   ← you are here

Read bottom-up for where you are; top-down for what you were diverted from.
```

**Frame 2 is the whole fixture.** It has survived a wind-down — `crossed 1` — and is 48 hours old, and it
is **not marked**. That is the case an earlier draft of this rule got wrong: it compared `open since`
against the header's `captured:` and marked anything earlier, which marks *every frame carried across a
boundary*. Carrying a diversion across a boundary is what this feature exists to do, so the mark fired on
the designed behaviour and on the abandoned frame alike, with the same glyph and the same warning prose.

**A mark that fires on the normal case is a decoration, not an alarm.** At `crossed 2` the claim is real:
the diversion was still open through two separate sessions ending. Frame 2 has been carried once, which is
ordinary.

**Frame 3 is 48 hours old and `crossed 1`.** Not marked, and this is the second half of the same
assertion: **age is never the oracle.** `crossed` counts wind-downs, never elapsed time.

It reads `1` rather than `0` because it must: every frame here predates the header's `captured:`, so every
frame was in the file at that capture and none can be `crossed 0`. A fixture showing `crossed 0` beneath a
later `captured:` encodes a snapshot no sequence of pushes and captures can produce.

**`crossed` renders where non-zero, so the mark shows its working.** A reader seeing `⚠ stale` beside
`crossed 2` can check the judgement; a bare glyph asks to be trusted.

**Gate failures:**

- **Marking frame 2.** The regression this fixture exists for. A rule that has quietly reverted to
  "predates `captured:`" marks it, and a marked frame looks like a working detector.
- Marking frame 2 or 3, or any mark that varies with age.
- Leaving frame 1 unmarked.
- Computing `crossed` from the header rather than reading it off the frame. It is stored precisely
  because it cannot be computed.
- Writing `⚠ stale` into the file. The mark is render-time; the file stores `crossed`.
- Writing the file at all. `show` is read-only.
