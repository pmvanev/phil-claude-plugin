# Expected — 34 (the stack verbs leave the exchanges alone)

**Expected decision:** `PUSHED` (run A), then `POPPED` (run B).

## Run A

The snapshot is read through `head`, so the region never enters this session. `## Stack` is created
with one frame, `crossed 0`, at the end of the body, and the body goes back through `carry`, which puts
the region beneath it byte-identical. Header reproduced byte-for-byte.

## Run B

Read through `head` again. The frame goes, and with it the `## Stack` section. The why and next action
exist, so the file stays. `carry` again keeps the region byte-identical and last.

## Gate failures

- **Appending the stack after the closing marker.** It sits where no reader of the sections looks, and
  the region is no longer last.
- **Treating the reply's `## Findings` as a section**, for instance by writing the stack beneath it.
  Only the markers bound the region; a heading inside it belongs to the reply.
- **Regenerating the region.** Reading the whole file and writing it back retypes a previous session's
  words — the refusal the script exists to avoid, and the natural way to lose a byte.
