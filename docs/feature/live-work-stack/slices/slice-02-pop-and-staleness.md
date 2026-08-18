# Slice 02 — Pop on return, and a frame that outlived its welcome

**Goal:** The innermost frame can be popped when the detour closes, and a frame that was never
popped is visible as stale rather than silently trusted.

**Stories:** S2 (return to the parent frame), S4 (see a frame that has gone stale)
**Carries:** [D4] — the staleness rule moves to where the stack is recorded, not only where it is published.

## Learning hypothesis

**Disproves** the claim that a manually-maintained stack is trustworthy, if dogfooding produces
frames that are pushed and never popped even with pop available — in which case the honest v2 is a
stack that expires rather than one that waits to be told.
**Confirms**, if it holds, that push/pop is a discipline Kai will actually keep, and that marking is
sufficient without an expiry policy.

## IN scope

- **`/phil:stack pop`** — deletes the innermost frame, names the frame now in hand, and writes the
  whole file back, same authority and same session guard as slice 01.
- **Staleness marking.** A frame open across a `/phil:handoff` capture is marked in the trace. This
  reuses `nwave-issue-board`'s existing wording — *a frame open longer than one boundary is marked* —
  rather than minting an age threshold, and makes it readable locally instead of only on the card.
- **[D4] recorded**: the rule now lives in `skills/session-handoff/SKILL.md` beside the recorder,
  with `nwave-issue-board` keeping its own copy for the projection. Issue #29's Done-when asserted
  this rule was *"already in `session-handoff`"*; it was not, and the correction is the slice.
- **`show` renders age for every frame**, so the human judges the frames the boundary rule does not
  reach.

## OUT scope

- **Automatic expiry or auto-pop.** A frame the tool closed on Kai's behalf is a frame whose reason
  nobody read. Marking is the honest limit until dogfooding says otherwise — which is this slice's
  own learning hypothesis.
- **Popping a frame other than the innermost.** That is editing the stack, not navigating it. Delete
  the line by hand; the format is prose on purpose.
- **Arbitration.** Unchanged, still out.

## Acceptance criteria

1. `/phil:stack pop` at depth 3 leaves depth 2, names the frame now in hand, and leaves `Why` and
   `Next` byte-identical.
2. `/phil:stack pop` on an empty or absent stack says so and **writes nothing** — not an error, and
   not a rewritten file.
3. A frame open across a `/phil:handoff` capture is marked in the bare `/phil:stack` trace on the
   next read. A fixture pins the boundary crossing.
4. Every frame in the trace carries its age, marked or not.
5. `skills/session-handoff/SKILL.md` states the staleness rule, and `nwave-issue-board`'s copy is
   reconciled with it rather than left to drift — one rule, stated in both places, with the
   recorder named as the source.

## Dependencies

Slice 01. Pop needs frames to pop, the session guard, and the whole-file writer.

## Effort

~1 day, most of it the boundary-crossing fixture (AC3), which needs a capture between two reads.

Reference class: slice 01, minus the header change and plus one fixture.

## Carpaccio taste tests

| Test | Result |
|---|---|
| Ships 4+ new components? | No — one verb on an existing command, one rule in an existing skill. |
| Depends on a new abstraction? | No. Slice 01 shipped the writer; this adds a second operation to it. |
| Disproves a pre-commitment? | Yes — that a hand-maintained stack stays honest. Frames left unpopped during dogfood refute it. |
| Synthetic data only? | No. AC3 needs a real capture between two real reads. |
| Duplicate of another slice at scale? | No. Slice 01 grows the stack; this shrinks it and audits it. |
