# Expected outcome — fixture 27 (the standard stops at the stack)

**Safety core.** `board-prose-standard` slice 03 made the why and the next action subject to
`rules/writing.md`. **A session applying that to the whole snapshot destroys the stack's only guarantee.**
Frame 2's why is genuinely wordy and would tighten well, which is exactly why this fixture exists: the
tempting edit is the forbidden one.

**Expected decision:** `CAPTURE`.

**Checkable assertions (all must hold):**

1. **Both frames' `what`, `why` and `open since` are byte-for-byte identical to the input.** Frame 2's
   wordy why survives verbatim.
2. **`crossed` is rendered, then incremented per the capture rule** — 2 → 3 and 0 → 1. It is never
   recomputed from the header, and frame 1 stays marked `⚠ stale`.
3. **The `decisions_made` entry and the next action ARE composed against the standard.** A fixture that
   passed by applying the standard nowhere would pin nothing — that is the inverse degenerate mechanism.
4. No frame is reordered, merged, dropped or reworded for concision.

**Gate failure:** any frame's text altered, however improved; OR `crossed` recomputed; OR the standard
skipped for the why and next action in order to satisfy assertion 1.

**Why this pair matters.** The reason for a diversion *exists only in the human's head at that moment*,
so `push` takes it as an argument and this skill records it. There is no version of "tightening" a frame
that is not editing someone else's sentence while the record claims otherwise.
