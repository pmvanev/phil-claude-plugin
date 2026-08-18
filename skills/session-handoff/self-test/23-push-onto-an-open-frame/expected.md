# Expected — 23 (going deeper, which is the case the stack is shaped for)

**Pins:** issue #29's done-when, which names *"push while a frame is open"* as required coverage, and the
frame template at `SKILL.md` § push step 3.

**Expected decision:** `PUSHED`, at depth 2:

```
PUSHED — frame 2 · the fixture runner · it needed a flag it did not have
  under: Wave-to-command table · the task in hand
  stack now 2 deep
```

and the file's stack reads:

```
1. Wave-to-command table · the task in hand · open since 2026-08-12T14:05Z · crossed 0
2. └ The fixture runner · it needed a flag it did not have · open since 2026-08-12T17:05Z · crossed 0
```

**This fixture exists because every other push fixture creates a depth-1 stack.** 16 pushes onto an empty
`## Stack`; 20 pushes with no snapshot at all. Neither produces an indent, an elbow, or a second frame —
so the shape the format is actually *for* was asserted nowhere. The nesting is not decoration: reading
top-down is how you find what you were diverted *from*, and it only works if depth is rendered.

**Frame 1 is untouched — byte-for-byte, including its `crossed 0`.** A push is not a capture, so it
increments nothing. `crossed` moves only at a wind-down.

**The new frame is `crossed 0`, always.** Whatever the frames above it carry, a frame pushed now has
survived no wind-downs.

**Frame 1 carries no `└` and no indent; frame 2 carries both.** The template's elbow is conditional on
depth, which is easy to bake in wrongly — an implementation that writes `└` on frame 1 satisfies a
literal reading of the template string and produces a stack that renders as though its outermost level
were nested under something absent.

**Gate failures:**

- The new frame appended without indent or elbow, i.e. as a sibling of frame 1.
- The new frame inserted first, or anywhere but last. Innermost-last is the ordering the whole format
  depends on.
- Incrementing frame 1's `crossed`, or restamping its `open since`.
- Any change to `Why`, `Next`, or the header.
- Writing the new frame with a non-zero `crossed`, or omitting `crossed` entirely.
- An abbreviated `17:05Z` on the new frame. Deeper frames carry the full date; the staleness rule and the
  age render both read it.
