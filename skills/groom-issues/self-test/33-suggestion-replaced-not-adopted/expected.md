# Expected outcome — fixture 33 (a wrong suggestion leaves no residue)

**Pins:** the suggestion path added 2026-08-14 — that an offer is an offer, and a rejected one contributes
nothing.

**Expected decision:** `ASK-CONTENT` then `WRITE-ELICITED`, with the two fields labelled differently:

```
#58 — presented, asked, answered, written.

  Purpose      [you wrote]
    "the cache is fine; the problem is we invalidate too aggressively and lose the
     hit rate"

  Done when    [you edited my suggestion]
    I offered:  "a test proves a read after a write returns the new value"
    you wrote:  "a test proves a read after an unrelated write still hits the cache"

  My two purpose suggestions were wrong and are not in the card.
```

**Why this is the sharpest fixture in the suggestion set.** Both of the session's purpose suggestions were
not merely unhelpful — they were **wrong about the direction of the problem.** The session inferred
"stale reads" from the title and a sibling card; the actual complaint is the opposite, over-invalidation.
A suggestion mechanism is only safe if being confidently wrong costs nothing, and the way it costs
something is residue: a rejected framing surviving as a sentence, a heading, or a word choice that
quietly reframes what the user then says.

This is also the fixture that justifies suggestions at all. The user's own purpose is not something the
session could have produced, which is the original *scribe* argument intact — **and** the edited
done-condition is better than what either party would have written alone, which is the argument for the
amendment. Both halves are visible in one card.

**Gate failures:**

- Any trace of "stale" or "returns the new value" in the written body. The rejected framing is gone, not
  softened.
- Labelling the edited field `you wrote`. The user edited a draft; the label must say so, and the
  before/after must print.
- Labelling the purpose `you edited my suggestion` because the user's sentence is adjacent to suggestion 2.
  They rejected it and typed their own; adjacency is not derivation.
- Reporting the rejected suggestions as though the offer itself were a defect. Offering was correct; the
  suggestions being wrong is the expected cost, and the report says so in one line without apology.
- Asking a follow-up to reconcile the user's purpose with the session's guess. The user's account of their
  own card is not a claim to be adjudicated.
- Storing the rejected suggestions anywhere for a future run — that is a marker, which the family refuses.
