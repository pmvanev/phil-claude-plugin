# Expected — 18 (depth 3, read both ways, nothing judged)

**Pins:** slice-01 AC2, and KPI-3 — the question answered without re-reading the session.

**Expected decision:** `SHOWN`, with all three frames, each carrying what it is, why it was entered, and how
long it has been open. The innermost is marked as where attention is:

```
SHOWN — 3 deep

1. Wave-to-command table · the task in hand · open 3h25m
2. └ Fixture 07 · it contradicted the table, so it had to be settled first · open 50m
3.   └ The fixture runner · it needed a flag it did not have · open 25m   ← you are here

Read bottom-up for where you are; top-down for what you were diverted from.
```

**Everything the render needs comes from the snapshot, and nothing else.** Ages are `now` minus each
frame's `open since`, which is why every frame — not only the first — stamps a full `YYYY-MM-DDTHH:MMZ`.
The abbreviated `16:40Z` this format shipped with was fine while the stack was only displayed; it cannot
support subtraction, and a frame open across a handoff has very likely crossed midnight.

**No frame is marked stale, and that is an assertion, not an omission.** Staleness marking is slice 02.
The mark it would need — *open across N boundaries* — is **not computable from this format**: the header
carries one `captured:`, overwritten every capture, so *whether* a frame outlived a capture is derivable
and *how many* is not. An earlier draft of this fixture supplied `captures_since_frame_N` as manifest
input, which made it pass on data the real snapshot can never carry — a fixture defending a behaviour
neither it nor the implementation could actually produce.

**Why "you are here" is on the innermost.** The stack has a shape; the ordering is the payload. A
rendering that lists frames without saying which end is current makes the reader count.

**Gate failures:**

- Any frame missing its age, or an age computed from a bare `HH:MMZ`.
- Marking any frame stale, `⚠`-flagging one, or reporting a boundary count. All slice 02.
- Accepting capture-history input from the manifest. The snapshot is the only input `show` gets.
- Writing the file. `show` is read-only; rewriting to "normalise" the format is a defect.
- Rendering innermost-first, or dropping the nesting indents. The shape is the content.
- Reporting `RESUME-CURRENT` or any read-back outcome. The paths do not interleave.
