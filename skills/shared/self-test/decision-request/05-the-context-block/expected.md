# Expected outcome — fixture 05, the context block

**Expected decision:** `CONFORMS`. **Finding set:** empty.

A real three-part ask, recorded verbatim, that genuinely needed its evidence — and put it above the
question, behind a horizontal rule, in the shape the standard prescribes.

## The clause this fixture was missing until now

Slice 01 shipped [D5] — separated, above, bounded in practice — with **no instance behind it**. Its one
conforming ask fit in 143 words and displaced nothing, so the escape hatch that makes a hard ceiling
affordable had never been used. Slice 02's AC8 asked for a fixture whose ask genuinely needs a detail
block, carrying tokens the ask may not.

This is that instance, and it is real rather than constructed:

- **Context block, 53 words**, carrying an artifact path — a token the counted ask may not contain.
- **A marker line** between the context and the framing.
- **Framing 148 words**, zero forbidden tokens, all three elements present.
- **Three questions at 100, 91 and 102 words** with their options — all inside the per-question limit.
- **Nothing between the framing and the call**, and nothing after it.
- **Three questions, three tagged decision/consequence pairs.**

**It shipped with one pair, and that was a defect.** Under the singular first version of the standard,
one `decision` and one `consequence` satisfied a three-decision ask — so this fixture's `consequence`
region held an unrelated *third decision* rather than any statement of what turned on an answer, while
certifying that the framing-presence check worked. Re-tagged into three pairs, along the clause
boundaries the recording already had. `framing_pairs: 3` is asserted, and a three-question turn with
fewer pairs is now a `BARE-LIST`.

## The passing side of two checks

Every check needs a green instance as well as a red one, or a check stuck permanently on looks like a
working check. This is the only fixture with a recorded emission that fires nothing, so it is the passing
side of `BARE-LIST` and `BURIED-ASK`, and
`test_the_context_block_is_exempt_from_the_vocabulary_rule` uses it to assert the exemption directly: a
forbidden token in the context must never become a finding. If it could, there would be nowhere for a
path or a card number to go and the ask would have to carry them — which is the failure the whole design
avoids.

## Gate failures

- Reading `CONFORMS` as "well framed". The four checks are countable clauses; whether the question was
  *good* is a reading, and this file is where that reading is recorded rather than automated.
- Deleting the context to shorten the fixture. The context is the fixture's entire point.
