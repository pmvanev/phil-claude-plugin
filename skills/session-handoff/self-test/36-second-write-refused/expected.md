# Expected — 36 (the second write is refused)

**Expected decision:** `CAPTURE` + `WRITE-REFUSED`.

## What must appear

- `CAPTURE`: the capture happened — step 9 wrote the why, the next action, the stack and two exchanges.
- `WRITE-REFUSED` in place of the counting line, with **both hashes**, what step 9 wrote, and the plain
  statement that the file has since changed beneath it and may no longer hold any of that.
- No projection outcome: the work has no card.

## The trap

The tempting sentence is *the snapshot from step 9 still stands*. It cannot be known: the hash changed,
so another writer's content is on disk, and it may have replaced this session's entirely. Describing the
file would assert a fact this session never read. Say what was written and that it changed; stop.

## Gate failures

- **Retrying, or merging.** Either resolves the competing write, which is arbitration.
- **Claiming the payload stands**, or reporting a count of what is on disk. Both describe another
  writer's file.
- **Reporting the handoff's exchange as recorded.** It was not.
