# Expected — 39 (`show` by name)

**Pins:** the `show` heading in `references/stack.md`, which names both invocations.

**Expected decision:** `SHOWN`, rendered exactly as fixture `18` renders the same snapshot. `show` is the
verb bare `/phil:stack` runs; the argument names it and changes nothing else.

**Gate failures:**

- Any difference from fixture `18`'s render.
- Reporting `show` as an unknown argument, or asking what it means.
- Reading `show` as a frame to push, or asking for its why.
- Writing the file.
