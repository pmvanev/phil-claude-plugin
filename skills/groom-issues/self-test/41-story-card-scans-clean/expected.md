# Expected outcome — fixture 41 (a correct story card scans clean)

**Pins:** the oversized rule's story extension — *"a story card is the same argument one level up, and
the paragraph is extended rather than edited."*

**Expected: zero findings.** No oversized finding, no split proposal, no ungrouped-effort finding (it
carries a goal), no decomposed-feature finding (its members are features, not slices, and they are rows
rather than cards).

**Why it passes the rule that would seem to catch it.** The card is large and holds four demonstrable
things — but *oversized* asks whether the work **can be demonstrated on its own**, and each member can.
The features are worked **sequentially by one owner**, so no two occupy different columns at once, which
is exactly what `phil:issue-board`'s split clause requires before a split is warranted.

**This half is the one that must be checked without touching the rule.** The tempting repair for the
*other* half — fixture 42, where a story card genuinely is wrong — is to make oversized sensitive to
size. That would report **this** card every run. The family stores no marker, so a declined split returns
forever while an accepted one only has to be accepted once: one careless acceptance dismantles a correct
story into feature cards permanently.

**The two halves resolve opposite ways and share no rule.** 41 passes on demonstrability; 42 fires on
concurrency. A single oracle tuned to satisfy both would be tuned wrong, and that is the gate.

**Gate failures:**

- Any oversized finding. The defect, stated.
- Proposing a split into feature cards. Correct only under the concurrency signal, which does not fire here.
- Reporting ungrouped effort. The card has a goal; a story and a goal coexist.
- Reporting the members as a decomposed feature. They are features, and they are rows, not cards.
- Passing this card by a rule that also passes fixture 42. Getting one right the wrong way is a failure.
- **Firing the two-in-flight check on the second `▶` from the slice roster.** This card has ONE member in
  flight, but its block carries two tables and `▶` means `current` at slice level — so a check that counts
  glyphs rather than reading the feature roster's state word reports this correct card. **This is the only
  gate failure that makes the 41/42 pair prove anything**; without it both pass under a broken rule.
- Reaching zero findings by editing the demonstrability text.
