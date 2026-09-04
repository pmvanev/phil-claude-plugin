# Expected outcome — fixture 21 (the restatement changes nothing at the feature tier)

**Pins:** the identity claim in *the bound* — *"at the feature tier this produces the two tables it
always did, unchanged."*

**Expected, arm A:** byte-identical to fixture 01's block. Two tables — the slice roster, and the
current slice's step table. **No feature roster**, no `Story:` header line, no third table.

**Expected, arm B (no roadmap):** **one** table — the slice roster — and the line saying no step table
is coming. This arm is the whole point. The bound reads *at most one feature's slices, and where a
roadmap exists, at most one slice's steps*; written as **exactly one** it would demand a step table this
feature cannot supply, and fixtures `07` and `14` would silently become non-compliant. **Arm A cannot
detect that**, because it is provisioned with a roadmap and never visits the branch.

**Why this fixture is a regression test and not a feature test.** Nothing here is about stories. It
asserts that generalising a rule did not quietly alter the behaviour the rule already governed — the
failure mode of every restatement, and invisible precisely because the new prose reads correctly.

**How the purpose-form yields the count-form here.** One feature declares no story, so it is the
current feature and the only one; its slices are therefore *the one enumerated roster*, and its current
slice is *the one enumerated step table*. Two tables. The old sentence is the new sentence evaluated at
N=1 — which is what makes it a restatement rather than a replacement.

**A card with no story declaration never enters the story tier at all.** Membership is opt-in: a feature
declaring nothing stays a feature card. That is what `[D2]`'s *MAY* buys, and it is why **no existing
fixture in this suite needed rewriting** for the story tier.

**Gate failures:**

- Emitting a feature roster with one row. A one-row roster above a slice roster is a new table where
  none shipped, and it costs a row on every single-feature card in existence.
- Emitting a `Story:` header line with an empty or inferred slug.
- Treating "no `Story:` line" as an error or as `unknown`. It is the normal case.
- Inferring membership from a directory name, a milestone, or a shared prefix. Membership is **declared**
  at column 0 or it does not exist.
- Any diff against fixture 01's expected block on arm A. The assertion is identity.
- Demanding a step table on arm B, or emitting an empty one. The bound is a ceiling; `07` and `14`
  render one table legitimately and must keep passing.
