# Expected — 25 (popping nothing, twice, differently)

**Pins:** slice-02 AC2, and the `unknown` / `none` distinction fixture 19 pins for `show`.

**Expected decisions:** run A reports `STACK-UNKNOWN`; run B reports `STACK-EMPTY`. Neither writes:

```
Run A:  STACK-UNKNOWN — no snapshot at this worktree root. Nothing to pop, and nothing recorded.
Run B:  STACK-EMPTY — snapshot present (captured 2026-08-12T17:30Z), no diversions recorded.
```

**The two nothings are different answers, and `pop` inherits that from `show`.** `unknown` is a claim
about the **record** — nobody wrote anything down. `none` is a claim about the **work** — a session
recorded its state and had no diversions. An earlier draft of pop's prose merged them into one clause
(*"popping an empty or absent stack… say the stack is empty"*), which gives the `none` answer for the
`unknown` situation: asserting a fact about the work when what is missing is the record. The skill
forbids that collapse twenty lines earlier, and fixture 19 already pins it on the other verb.

**Neither run writes.** Not the file, not a rewritten-but-identical file, and no hash is taken — there is
nothing to compare-and-swap over. This is the assertion whose failure is silent: rewriting the file to
prove it was read produces byte-identical output on run B and passes any check that only diffs content.
The observable is that no write is attempted at all.

**Run A does not create a snapshot.** `push` creates one because a diversion is payload; a pop has no
payload and nothing to record. Creating a header here would manufacture a fingerprint nobody asked for.

**Neither is an error.** Popping when there is nothing to pop is an ordinary thing to do — usually one
pop too many at the end of a chain — and reporting a fault teaches the user to avoid the verb.

**Gate failures:**

- The same outcome for both runs, in either direction.
- Run A reporting `STACK-EMPTY`, or run B reporting `STACK-UNKNOWN`.
- Reporting `POPPED` on either.
- Writing, rewriting, or creating any file.
- Taking a hash.
- Raising an error, or reporting a generic failure.
