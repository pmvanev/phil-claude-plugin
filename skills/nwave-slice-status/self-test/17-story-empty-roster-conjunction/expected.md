# Expected outcome — fixture 17 (the empty-roster guard, tested on its conjunction)

**Pins:** *The story-level state, on request* — the two distinct emptinesses, and the fact that they
resolve differently.

**Expected output — case A, no feature declares the slug:**

```
Story: no-such-story — unknown · no feature declares this slug
```

**No count.** `0 of 0 features done` reads as completion and is the same lie arithmetically that the
feature fold already refuses.

**Expected output — case B, members exist but none is assessable:**

```
Story: payments-rework — unknown · 0 of 2 features done
Notes: bedrock-setup and saved-sessions declare this story but neither has a roster
```

**A count, because there is something to count.** Two features really are in this story; what is unknown
is their state, not their existence.

**Why the pair, and why one fixture rather than two.** These reach `unknown` by different rows. Case A
fires the **empty-roster guard**, the row that sits above every test quantified over members. Case B
fires the **existential `unknown` row** near the bottom, with the guard never consulted. A guard written
for only one case is green on the other and ships:

- Guard only case A → case B's three universals are quantified over two members that are neither `done`
  nor `deferred`, so *"every feature that is not `deferred` is `done`"* is **false** and case B survives.
  This direction happens to be safe, which is exactly why testing only it proves nothing.
- Guard only case B → case A's universals are vacuously **true**, so it answers **`done`**. That is the
  costly direction, and it is the one a single-clause fixture misses.

**What `done` would cost here.** `phil:nwave-issue-board` maps `done` to the Done column and this
plugin's board has auto-close enabled, so the rendering closes the issue. One level up from the feature
fold, **the closed card holds N features** — the whole story, none of it assessed, closed by a call that
reports success. Fixture 14 is this defect at feature scale; the shape is inherited only if it is
re-pinned, because a shared shape is not a shared test.

**Gate failures:**

- Returning `done` in case A. The defect, stated.
- Returning `to do` in either case. A claim about the work from a fact about the record.
- Returning `deferred` in case A. *Every member is `deferred`* is vacuous over no members; nothing was
  set aside.
- Emitting a count in case A. `0 of 0` reads as completion.
- Omitting the count in case B. It suppresses the fact that two real features are in this story.
- Passing case A while failing case B, or the reverse. The conjunction is the assertion.
- Treating a slug that matches nothing as an error and stopping. It is a legitimate answer: `unknown`.
- Writing a board column for either. The publisher's mapping says **no column — do not write one**.
